#!/usr/bin/env python3
"""Two-player match simulator: any decklist vs. any decklist.

This replaces simulate_match.py, which could only ever play one hardcoded
deck against one hardcoded opponent, tracked Energy as a plain count, and
modeled no knockouts or Prize cards at all. This version reads TWO
decklists in the project's normal plain-text format and plays real games
to a win condition, so a build can be tested against an actual meta deck
rather than only measured for how fast it assembles in a vacuum.

What is modeled
  * Full board: Active + up to 5 Bench per player, damage counters, HP,
    Energy tracked BY TYPE, Pokemon Tools' presence (not their effects).
  * Evolution (including the "not the turn it entered play" rule and the
    no-evolving-on-your-first-turn rule), Rare Candy, and Grand Tree.
  * Attacks: type-correct cost payment, Weakness (x2), knockouts, and
    Prize cards taken -- including 2 for a rule-box ex and 3 for a Mega
    Evolution ex, read from each card's own rules text.
  * Retreating, paid by discarding Energy equal to the retreat cost.
  * ABILITIES, via the ability_ir compiler + ability_engine runtime.
    Card text compiles into a structured IR (trigger / conditions / costs /
    actions) and the runtime executes it, so draw, search, Energy
    acceleration, healing, counter movement, retaliation, damage reduction
    and damage buffs all run through ONE code path instead of a bespoke
    handler per family. 278 of the pool's 282 Abilities compile (98.6%).
    Abilities are read from each Pokemon's EXACT printing, because they
    are printing-specific (Alakazam MEG 56 has Psychic Draw; TWM 82 has
    none). Every run prints which Abilities are executing per deck and
    which are not, so a deck leaning on an uncompiled Ability is visibly
    undervalued rather than quietly so.
    Tools/Special Energy carrying retaliation (Punk Helmet, Spiky Energy,
    Deluxe Bomb) keep a small dedicated index, since they are not Pokemon.
  * Win by Prizes, by the opponent having no Pokemon in play, or by the
    opponent being unable to draw at the start of their turn.

Stated simplifications (read these before trusting a win rate)
  * Both players use the SAME generic heuristic AI: develop the board,
    evolve when possible, attach Energy to the Active, use draw
    Abilities, then attack with the highest-damage payable attack. It
    does not sequence combos, hold cards for a bigger turn, or play
    around anything. A deck whose plan depends on precise sequencing
    will be UNDERRATED here relative to a deck that just attacks.
  * ATTACK RIDERS now run through the same IR as Abilities: "is now
    Poisoned", "discard an Energy from your opponent's Active", mill and
    heal riders are compiled from the attack's own text and applied after
    damage. Attack selection values those riders in damage-equivalents,
    so a 0-damage setup attack (Arbok's Panic Poison) is actually chosen.
  * Attack DAMAGE is computed; remaining SIDE-EFFECTS are not executed.
    Scaling clauses are resolved live -- "for each card in your hand",
    "for each of your <family> Pokemon in play", bench counts, attached
    Energy, damage counters, Prizes taken -- as are coin flips and the
    attack-copying pattern (Persian ex's Haughty Order actually looks at
    the opponent's deck). But riders like "discard an Energy from your
    opponent", extra Bench damage, self-damage, and retreat locks do NOT
    happen. Any attack whose text could not be scored is listed in the
    report as UNSCORED rather than silently counted as weak.
  * Trainer coverage is a registry of this project's common staples; any
    Trainer outside it is simply never played, and every such name is
    reported at the end of a run rather than hidden.
  * Special Energy provides its listed types where the dataset states
    them, otherwise it is treated as providing any one type.
  * 4 of 282 Abilities do not compile, and all four are structural rules
    rather than turn actions (Palafin's in-place transform, Eevee ex's
    evolution legality, Cinderace's setup-phase rule). Listed per deck.
  * Compiled != executed. Several ops parse but are still inert in the
    runtime (SET_TYPE, ATTACK_TWICE, EXTRA_TOOLS, ENERGY_PROVIDES_EXTRA,
    IGNORE_OPPONENT_EFFECTS, RETURN_TO_HAND_ON_KO, LOCK_COUNTER_MOVEMENT),
    as are the passive-query ops the engine does not consult yet (LOCK's
    ability-lock form, SET_WEAKNESS, MODIFY_PRIZE, ENDURE, EVOLVE_EARLY).
  * CHOICE Abilities are resolved by a fixed heuristic, not by good play.
    Munkidori-style counter movement always dumps onto the opponent's
    Active off your most-damaged Pokemon; a human would sometimes aim at
    a Benched target to set up a later knockout. Treat those results as a
    floor, not a measurement.
  * SPECIAL CONDITIONS are modeled: Poison (10/turn) and Burn (20/turn with
    a recovery flip) at Pokemon Checkup, Asleep/Paralyzed blocking attacks,
    Confused as a 50% attack failure with 30 self-damage, the
    Asleep/Confused/Paralyzed exclusivity rule, and -- importantly --
    conditions clearing on retreat and on evolution. Abilities that add
    checkup damage (Pecharunt, Magmortar) are honoured.
  * No Stadium effects besides Grand Tree.

Usage
  python3 simulate_versus.py deckA.txt deckB.txt            # 500 games
  python3 simulate_versus.py deckA.txt deckB.txt 2000       # N games
  python3 simulate_versus.py deckA.txt deckB.txt --verbose  # one game log
"""
import random
import sys
import statistics
from collections import defaultdict

sys.path.insert(0, ".")
import tcg_model as M
import ability_ir as IR
import ability_engine as AE

MAX_BENCH = 5
STARTING_PRIZES = 6
MAX_TURNS = 40  # hard stop so a stalled pairing can't loop forever


# --------------------------------------------------------------------------
# Board objects
# --------------------------------------------------------------------------

class InPlay:
    __slots__ = ("name", "damage", "energy", "energy_names", "entered_turn",
                 "evolved_this_turn", "tool", "conditions", "attack_locked")

    def __init__(self, name, turn):
        self.name = name
        self.damage = 0
        self.energy = []          # list of type-lists, one per attached Energy card
        self.energy_names = []    # parallel list of the Energy cards' names
        self.entered_turn = turn
        self.evolved_this_turn = False
        # Set by attacks that lock their own user out of attacking next
        # turn (N's Zekrom's Rampaging Thunder, Iono's Bellibolt ex's
        # Thunderous Bolt). Without it the AI re-used a 250-damage
        # once-every-other-turn attack every single turn.
        self.attack_locked = False
        self.tool = None
        self.conditions = set()   # asleep / burned / confused / paralyzed / poisoned

    def energy_count(self):
        return len(self.energy)


class Player:
    def __init__(self, name, POKEMON, decklist, EFFECTS=None):
        self.name = name
        self.POKEMON = POKEMON
        # Pokemon name -> [compiled ability_ir.Effect]. MUST be populated:
        # an earlier integration left this empty and every Ability silently
        # no-opped, which is exactly what test_ability_engine.py now guards.
        self.EFFECTS = EFFECTS if EFFECTS is not None else {}
        self.deck = list(decklist)
        self.hand = []
        self.active = None
        self.bench = []
        self.discard = []
        self.prizes = STARTING_PRIZES
        self.supporter_played = False
        # Set by turn-scoped damage Supporters (Black Belt's Training),
        # cleared at the start of every turn.
        self.turn_buff_vs_ex = 0
        # Unrestricted version of the same thing (Gladion's Final Battle),
        # which applies to any Active rather than only a Pokemon ex.
        self.turn_buff_any = 0
        self.stadium = None
        self.lost_pokemon_last_turn = False
        self.abilities_used = set()
        self.played_supporters_this_turn = set()
        self.deck_out = False
        # Energy types this deck can actually put on a Pokemon. Attacks
        # needing a type outside this set can never be cast, so they must
        # not drive Energy attachment -- see energy_shortfall.
        self.energy_types = set()

    # -- basic zone helpers ------------------------------------------------
    def draw(self, n=1):
        for _ in range(n):
            if not self.deck:
                self.deck_out = True
                return
            self.hand.append(self.deck.pop())

    def in_play(self):
        out = [self.active] if self.active else []
        return out + self.bench

    def in_play_names(self):
        return [p.name for p in self.in_play()]

    def has_basic_in_hand(self):
        return any(k == "Pokemon" and self.POKEMON[n]["stage"] == "Basic"
                   for k, n in self.hand)

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

    def info(self, p):
        return self.POKEMON[p.name]


# --------------------------------------------------------------------------
# Energy handling
# --------------------------------------------------------------------------

RETALIATE_CARDS = {}   # card name -> retaliation dict (Tools and Special Energy)


def build_retaliate_index(cards):
    idx = {}
    for c in cards:
        if c.get("supertype") == "Pokémon":
            continue
        r = M.parse_tool_or_energy_retaliation(c)
        if r:
            idx[c["name"]] = r
    return idx


# Populated in main(); lets helpers that don't take cards_by_name resolve
# an Energy card's types (N's PP Up pulls one out of the discard pile).
_CARDS_BY_NAME = {}


def energy_types_for(card_name, cards_by_name):
    """What types a single Energy card provides."""
    m = M.BASIC_ENERGY_RE.match(card_name)
    if m:
        return [m.group(1)]
    card = (cards_by_name.get(card_name) or [None])[0]
    if card:
        listed = card.get("types") or []
        if listed:
            return list(listed)
    return list(M.REAL_TYPES)  # unknown Special Energy: treat as any


def effective_cost(pl, spot, cost, opp=None):
    """The attack cost as it stands right now, after any Ability that
    ignores part of it. Decidueye ex's Sniper's Eye turns Crushing Arrow
    from GrassColorlessColorlessColorless into a single Grass -- but only
    while the opponent holds exactly 4 cards, so this is re-derived on
    every pricing rather than baked into the card."""
    ignored = AE.query_ignored_cost_types(pl, spot, opp)
    if "ALL" in ignored:
        return []
    cost = [c for c in cost if c not in ignored] if ignored else list(cost)

    # Counted reductions (Food Prep: "cost Colorless less for each Kofu
    # card in your discard pile"). Colorless symbols come off first --
    # a typed requirement can only be removed by a reduction naming that
    # type, which is why Haymaker still needs its one Water.
    reduce = AE.query_cost_reduction(pl, spot, opp)
    for typ, n in reduce.items():
        for _ in range(n):
            if typ in cost:
                cost.remove(typ)
            elif typ == "Colorless":
                break
    return cost


def can_pay(cost, attached):
    """cost: list of type strings. attached: list of type-lists.
    Greedy but correct enough: satisfy typed requirements first (each with
    an Energy that can provide that type), then Colorless with whatever
    is left over."""
    if not cost:
        return True
    pool = list(attached)
    typed = [c for c in cost if c != "Colorless"]
    colorless = len(cost) - len(typed)
    for need in typed:
        hit = None
        for i, prov in enumerate(pool):
            if need in prov:
                hit = i
                break
        if hit is None:
            return False
        pool.pop(hit)
    return len(pool) >= colorless


# --------------------------------------------------------------------------
# Draw Abilities
# --------------------------------------------------------------------------

def ability_key(p, ab):
    return (id(p), ab["name"])


ACTIVATED = (IR.Trigger.ONCE_PER_TURN, IR.Trigger.ANY_TIMES_PER_TURN)


def sweep_knocked_out(pl, opp, log):
    """Remove Pokemon killed outside the attack step and award the Prizes.

    Abilities that Knock their own user Out (Cursed Blast) resolve here --
    do_attack owns the damage path, and without this the self-KO cost was
    silently free.
    """
    for owner, taker in ((pl, opp), (opp, pl)):
        for spot in list(owner.in_play()):
            if spot.damage < owner.POKEMON[spot.name]["hp"]:
                continue
            taken = owner.POKEMON[spot.name]["prize_value"]
            owner.discard.append(spot.name)
            if spot is owner.active:
                owner.active = None
            elif spot in owner.bench:
                owner.bench.remove(spot)
            taker.prizes -= taken
            owner.lost_pokemon_last_turn = True
            log.append(f"  {owner.name}: {spot.name} Knocked Out "
                       f"(+{taken} Prize to {taker.name})")
            if owner.active is None and owner.bench:
                owner.bench.sort(
                    key=lambda p: (_ready_damage(owner, taker, p),
                                   owner.POKEMON[p.name]["hp"] - p.damage),
                    reverse=True)
                owner.active = owner.bench.pop(0)
                log.append(f"  {owner.name}: promotes {owner.active.name}")


def use_stadium(pl, log):
    """Once-per-turn Stadium effects the owner can use.

    Prism Tower is a repeatable DISCARD outlet at no Supporter cost, which
    matters in a deck whose payoff counts its own Pokemon in the discard;
    Team Rocket's Factory is a draw. Both were previously inert -- every
    Stadium was.
    """
    if pl.stadium == "Prism Tower":
        # Discard 2 from hand to draw 1. Only worth it when the two cards
        # going are fuel; otherwise it is straight card disadvantage.
        fuel = [c for c in pl.hand
                if c[0] == "Pokemon" and _is_discard_fuel(pl, c[1])][:2]
        if len(fuel) == 2:
            for c in fuel:
                pl.remove_from_hand(*c)
                pl.discard.append(c[1])
            pl.draw(1)
            log.append(f"  {pl.name}: Prism Tower (discard 2 fuel, draw 1)")
    elif pl.stadium == "Team Rocket's Factory":
        if any("Team Rocket" in n for n in pl.played_supporters_this_turn):
            pl.draw(2)
            log.append(f"  {pl.name}: Team Rocket's Factory (draw 2)")


def use_abilities(pl, opp, turn, log, just_evolved=None):
    """Fire every activated Ability whose conditions and costs are met.

    One code path for the whole compiled IR -- draw, search, Energy
    acceleration, healing, counter movement and the rest -- instead of a
    bespoke handler per family.
    """
    def make_inplay(name):
        return InPlay(name, turn)

    for p in list(pl.in_play()):
        for eff in pl.EFFECTS.get(p.name, []):
            if eff.unsupported:
                continue
            if just_evolved is not None:
                if eff.trigger != IR.Trigger.ON_EVOLVE or p is not just_evolved:
                    continue
            elif eff.trigger not in ACTIVATED:
                continue
            key = (id(p), eff.name)
            if key in pl.abilities_used and eff.trigger != IR.Trigger.ANY_TIMES_PER_TURN:
                continue
            if AE.activate(eff, pl, opp, p, log, make_inplay=make_inplay):
                pl.abilities_used.add(key)
                log.append(f"  {pl.name}: {p.name} uses {eff.name}")


# --------------------------------------------------------------------------
# Trainer effects (compact registry; unknown Trainers are never played)
# --------------------------------------------------------------------------

def basics_in_hand(pl):
    return [n for k, n in pl.hand if k == "Pokemon" and pl.POKEMON[n]["stage"] == "Basic"]


def _lead_score(pl, name):
    """Rank a Basic as an opening Active. Prefer something that evolves into
    a real threat, then something that can actually attack -- picking purely
    by HP led with support pieces like Munkidori (110 HP, Ability-only) over
    the deck's actual attacker."""
    info = pl.POKEMON[name]
    evolves_into = any(o["evolves_from"] == name for o in pl.POKEMON.values())
    has_attack = any(a["damage"] > 0 for a in info["attacks"])
    return (2 if evolves_into else 0) + (1 if has_attack else 0), info["hp"]


def _discard_payoffs(pl):
    """(ability name, threshold) for every payoff this deck runs that
    counts its own Pokemon in the discard pile."""
    out = []
    for name in {n for _, n in pl.deck} | set(pl.in_play_names()):
        for atk in pl.POKEMON.get(name, {}).get("attacks", []):
            eff = _attack_ir(atk)
            for c in eff.conditions:
                if c["kind"] == "named_ability_in_discard":
                    out.append((c["ability"].lower(), c["count"]))
    return out


def _is_discard_fuel(pl, name):
    """Is this Pokemon worth more in the discard than on the Bench?"""
    payoffs = _discard_payoffs(pl)
    if not payoffs:
        return False
    abilities = [(ab.get("name") or "").lower()
                 for ab in pl.POKEMON.get(name, {}).get("abilities") or []]
    for want, need in payoffs:
        if want not in abilities:
            continue
        have = sum(1 for c in pl.discard
                   if want in [(a.get("name") or "").lower()
                               for a in pl.POKEMON.get(c, {}).get("abilities") or []])
        if have < need:
            return True
    return False


def play_basics(pl, turn, log):
    if pl.active is None:
        bs = basics_in_hand(pl)
        if bs:
            best = max(bs, key=lambda n: _lead_score(pl, n))
            pl.remove_from_hand("Pokemon", best)
            pl.active = InPlay(best, turn)
            log.append(f"  {pl.name}: {best} to Active")
    for kind, name in list(pl.hand):
        if kind == "Pokemon" and pl.POKEMON[name]["stage"] == "Basic" and len(pl.bench) < MAX_BENCH:
            # Hold back a Pokemon whose job is to be DISCARDED. A deck
            # whose payoff counts its own Pokemon in the discard pile
            # (Dhelmise's Vengeful Anchor, Sinistcha's Matcha Spin) has to
            # choose between benching a body and fuelling the attack --
            # benching everything on sight simply never turned those
            # attacks on. Only holds back once there is a board already.
            if len(pl.bench) >= 2 and _is_discard_fuel(pl, name):
                continue
            pl.remove_from_hand(kind, name)
            pl.bench.append(InPlay(name, turn))
            log.append(f"  {pl.name}: benches {name}")


def try_evolve(pl, opp, turn, log, first_turn):
    for kind, name in list(pl.hand):
        if kind != "Pokemon":
            continue
        pre = pl.POKEMON[name]["evolves_from"]
        if not pre:
            continue
        for spot in pl.in_play():
            if spot.name != pre:
                continue
            # Normal timing: the Pokemon must have been in play since a
            # previous turn, and one Pokemon evolves at most once per turn.
            # (The second half was missing, so any Basic could run all the
            # way to Stage 2 in a single turn and every Stage 2 line
            # simulated a full turn faster than it really is.)
            normal = (not first_turn and turn > spot.entered_turn
                      and not spot.evolved_this_turn)
            # Luxio's Fighting Roar is the printed exception to both halves.
            if normal or AE.query_evolves_early(pl, spot, opp):
                pl.remove_from_hand(kind, name)
                spot.name = name
                spot.evolved_this_turn = True
                clear_conditions(spot, "evolved", log, pl.name)
                log.append(f"  {pl.name}: {pre} -> {name}")
                use_abilities(pl, opp, turn, log, just_evolved=spot)
                break


def effect_rare_candy(pl, opp, turn, log, first_turn):
    if first_turn:
        return False
    s2 = [n for k, n in pl.hand if k == "Pokemon" and pl.POKEMON[n]["stage"] == "Stage 2"]
    for spot in pl.in_play():
        if turn <= spot.entered_turn or pl.POKEMON[spot.name]["stage"] != "Basic":
            continue
        for name in s2:
            s1 = pl.POKEMON[name]["evolves_from"]
            s1info = pl.POKEMON.get(s1)
            if s1info and s1info["evolves_from"] == spot.name:
                pl.remove_from_hand("Item", "Rare Candy")
                pl.discard.append("Rare Candy")
                pl.remove_from_hand("Pokemon", name)
                spot.name = name
                spot.evolved_this_turn = True
                log.append(f"  {pl.name}: Rare Candy -> {name}")
                use_abilities(pl, opp, turn, log, just_evolved=spot)
                return True
    return False


def search_pokemon_from_deck(pl, pred):
    for i, (k, n) in enumerate(pl.deck):
        if k == "Pokemon" and pred(n):
            pl.deck.pop(i)
            random.shuffle(pl.deck)
            return n
    return None


def want_pokemon(pl, name):
    """Rough desirability: something we can actually put into play or evolve."""
    info = pl.POKEMON[name]
    if info["stage"] == "Basic":
        return True
    return info["evolves_from"] in pl.in_play_names()


def play_items(pl, opp, turn, log, first_turn):
    while ("Item", "Rare Candy") in pl.hand:
        if not effect_rare_candy(pl, opp, turn, log, first_turn):
            break

    while ("Item", "Buddy-Buddy Poffin") in pl.hand and len(pl.bench) < MAX_BENCH:
        got = []
        for _ in range(2):
            if len(pl.bench) + len(got) >= MAX_BENCH:
                break
            n = search_pokemon_from_deck(
                pl, lambda x: pl.POKEMON[x]["stage"] == "Basic" and pl.POKEMON[x]["hp"] <= 70)
            if n is None:
                break
            got.append(n)
        if not got:
            break
        pl.remove_from_hand("Item", "Buddy-Buddy Poffin")
        pl.discard.append("Buddy-Buddy Poffin")
        for n in got:
            pl.bench.append(InPlay(n, turn))
        log.append(f"  {pl.name}: Buddy-Buddy Poffin -> {', '.join(got)}")

    # Hole-Digging Shovel: discard the top 2 of your own deck. Item
    # speed, so it stacks with whatever Supporter you played.
    while ("Item", "Hole-Digging Shovel") in pl.hand and len(pl.deck) >= 2:
        pl.remove_from_hand("Item", "Hole-Digging Shovel")
        pl.discard.append("Hole-Digging Shovel")
        for _ in range(2):
            pl.discard.append(pl.deck.pop()[1])
        log.append(f"  {pl.name}: Hole-Digging Shovel (mill 2)")

    # Brilliant Blender: search out up to 5 cards and discard them. Its
    # whole purpose is loading the discard on demand -- here, four Kofu at
    # once, which turns Food Prep on in a single Item.
    while ("Item", "Brilliant Blender") in pl.hand:
        # Dump whatever this deck's payoffs actually count in the discard:
        # Kofu for Food Prep, Basic Grass Energy for Re-Brew. Hard-coding
        # Kofu made the Blender a blank in a Sinistcha ex build.
        wanted = [c for c in pl.deck if c[1] == "Kofu"][:5]
        if len(wanted) < 5 and any(
                "per_discard_card" in a.filter
                for p in pl.in_play() for e in pl.EFFECTS.get(p.name, [])
                for a in e.actions):
            wanted += [c for c in pl.deck
                       if c[0] == "Energy" and "Grass" in c[1]][:5 - len(wanted)]
        if not wanted:
            break
        pl.remove_from_hand("Item", "Brilliant Blender")
        pl.discard.append("Brilliant Blender")
        for card in wanted:
            pl.deck.remove(card)
            pl.discard.append(card[1])
        random.shuffle(pl.deck)
        log.append(f"  {pl.name}: Brilliant Blender -> discards "
                   f"{len(wanted)} Kofu")

    # Pokegear 3.0: top 7, take a Supporter this engine can actually play,
    # so the fetch is worth what the sim scores it at and no more.
    while ("Item", "Pokégear 3.0") in pl.hand:
        pick = next((c for c in reversed(pl.deck[-7:])
                     if c[0] == "Supporter" and c[1] in KNOWN_TRAINERS), None)
        if pick is None:
            break
        pl.remove_from_hand("Item", "Pokégear 3.0")
        pl.discard.append("Pokégear 3.0")
        pl.deck.remove(pick)
        random.shuffle(pl.deck)
        pl.hand.append(pick)
        log.append(f"  {pl.name}: Pokégear 3.0 -> {pick[1]}")

    # N's PP Up: recycle a Basic Energy out of the discard onto a Benched
    # N's Pokemon -- the deck's way back after an attacker is Knocked Out.
    # Stadiums: only those with a modeled effect get played, and playing
    # one replaces whatever is already out (on either side).
    for kind, name in list(pl.hand):
        if kind != "Stadium" or (name not in RETREAT_STADIUMS
                                 and name not in EFFECT_STADIUMS):
            continue
        if pl.stadium == name:
            continue
        pl.remove_from_hand(kind, name)
        pl.discard.append(name)
        pl.stadium = name
        opp.stadium = None
        log.append(f"  {pl.name}: plays Stadium {name}")
        break

    while ("Item", "N's PP Up") in pl.hand:
        target = next((p for p in pl.bench if "N's" in p.name), None)
        e = next((n for n in pl.discard if n.endswith("Energy")), None)
        if target is None or e is None:
            break
        pl.remove_from_hand("Item", "N's PP Up")
        pl.discard.append("N's PP Up")
        pl.discard.remove(e)
        target.energy.append(energy_types_for(e, _CARDS_BY_NAME))
        target.energy_names.append(e)
        log.append(f"  {pl.name}: N's PP Up -> {e} onto {target.name}")

    while ("Item", "Ultra Ball") in pl.hand:
        others = [c for c in pl.hand if c != ("Item", "Ultra Ball")]
        if len(others) < 2:
            break
        n = search_pokemon_from_deck(pl, lambda x: want_pokemon(pl, x))
        if n is None:
            break
        pl.remove_from_hand("Item", "Ultra Ball")
        pl.discard.append("Ultra Ball")
        for c in others[:2]:
            pl.remove_from_hand(*c)
            pl.discard.append(c[1])
        pl.hand.append(("Pokemon", n))
        log.append(f"  {pl.name}: Ultra Ball -> {n}")

    for item in ("Poké Pad", "Nest Ball"):
        while ("Item", item) in pl.hand:
            n = search_pokemon_from_deck(
                pl, lambda x: want_pokemon(pl, x) and not pl.POKEMON[x]["rule_box"])
            if n is None:
                break
            pl.remove_from_hand("Item", item)
            pl.discard.append(item)
            pl.hand.append(("Pokemon", n))
            log.append(f"  {pl.name}: {item} -> {n}")

    while ("Item", "Energy Search") in pl.hand:
        idx = next((i for i, (k, n) in enumerate(pl.deck)
                    if k == "Energy" and M.BASIC_ENERGY_RE.match(n)), None)
        if idx is None:
            break
        pl.remove_from_hand("Item", "Energy Search")
        pl.discard.append("Energy Search")
        card = pl.deck.pop(idx)
        random.shuffle(pl.deck)
        pl.hand.append(card)
        log.append(f"  {pl.name}: Energy Search -> {card[1]}")

    while ("Item", "Night Stretcher") in pl.hand:
        pick = next((n for n in pl.discard if n in pl.POKEMON), None)
        kind = "Pokemon"
        if pick is None:
            pick = next((n for n in pl.discard if M.BASIC_ENERGY_RE.match(n)), None)
            kind = "Energy"
        if pick is None:
            break
        pl.remove_from_hand("Item", "Night Stretcher")
        pl.discard.append("Night Stretcher")
        pl.discard.remove(pick)
        pl.hand.append((kind, pick))
        log.append(f"  {pl.name}: Night Stretcher -> {pick}")


def supporter_draw_to(pl, target, log, label):
    before = len(pl.hand)
    while len(pl.hand) < target and pl.deck:
        pl.draw(1)
    log.append(f"  {pl.name}: {label} -> drew {len(pl.hand) - before}")


def judge_unlocks_attack(pl, opp):
    """Would putting the opponent on exactly 4 cards make this turn's
    attack payable when it isn't right now?

    This is the whole reason a Decidueye ex deck plays Judge from a hand it
    would rather keep: Crushing Arrow costs four Energy at a hand size of 3
    or 5, and one Grass at exactly 4.
    """
    if pl.active is None or opp is None:
        return False
    if best_attack(pl, pl.active, only_payable=True, opp=opp) is not None:
        return False
    saved = opp.hand
    opp.hand = [("Item", "?")] * 4
    try:
        return best_attack(pl, pl.active, only_payable=True, opp=opp) is not None
    finally:
        opp.hand = saved


def play_supporter(pl, opp, turn, log):
    if pl.supporter_played:
        return
    hand_names = [n for k, n in pl.hand if k == "Supporter"]

    def use(name):
        pl.remove_from_hand("Supporter", name)
        pl.discard.append(name)
        pl.supporter_played = True
        pl.played_supporters_this_turn.add(name)

    # Judge is played for the OPPONENT's half first and the draw second.
    # Setting them to exactly 4 is what switches on a conditional
    # cost-reduction Ability (Decidueye ex's Sniper's Eye); a deck built on
    # that will spend the Supporter slot on it even from a full hand.
    if "Judge" in hand_names and (len(pl.hand) - 1 <= 4 or judge_unlocks_attack(pl, opp)):
        use("Judge")
        opp.deck[:0] = opp.hand
        opp.hand = []
        for _ in range(4):
            if opp.deck:
                opp.hand.append(opp.deck.pop())
        pl.deck.extend(pl.hand)
        pl.hand = []
        random.shuffle(pl.deck)
        pl.draw(4)
        log.append(f"  {pl.name}: Judge (both hands to 4)")
        return

    # Gwynn: discard up to 2 Pokemon WITHOUT a Rule Box from hand, and
    # draw 3 for each. Every Hide 'n' Sneak body is single-Prize, so this
    # is Naveen's fuelling job and the format's best draw on one card.
    if "Gwynn" in hand_names:
        fuel = [c for c in pl.hand
                if c[0] == "Pokemon"
                and pl.POKEMON.get(c[1], {}).get("prize_value") == 1][:2]
        if fuel:
            use("Gwynn")
            for c in fuel:
                pl.remove_from_hand(*c)
                pl.discard.append(c[1])
            pl.draw(3 * len(fuel))
            log.append(f"  {pl.name}: Gwynn (discard {len(fuel)}, "
                       f"draw {3 * len(fuel)})")
            return

    # Raifort: look at the top 5 and discard any number -- selective
    # self-mill, so the fuel never has to reach your hand at all.
    if "Raifort" in hand_names:
        top = pl.deck[-5:]
        keep = [c for c in top if not _is_discard_fuel(pl, c[1])]
        pitch = [c for c in top if _is_discard_fuel(pl, c[1])]
        if pitch:
            use("Raifort")
            for c in pitch:
                pl.deck.remove(c)
                pl.discard.append(c[1])
            log.append(f"  {pl.name}: Raifort (discard {len(pitch)} fuel "
                       f"off the top)")
            return

    # Naveen: discard any number from hand, then draw back to 5. In a
    # deck whose payoff counts its own Pokemon in the discard, the discard
    # half IS the effect -- Night Stretcher and friends run it backwards.
    if "Naveen" in hand_names and len(pl.hand) <= 5:
        use("Naveen")
        fuel = [c for c in pl.hand
                if c[0] == "Pokemon" and any(
                    (ab.get("name") or "") == "Hide 'n' Sneak"
                    for ab in pl.POKEMON.get(c[1], {}).get("abilities") or [])]
        for c in fuel:
            pl.remove_from_hand(*c)
            pl.discard.append(c[1])
        while len(pl.hand) < 5 and pl.deck:
            pl.draw(1)
        log.append(f"  {pl.name}: Naveen (discard {len(fuel)} fuel, draw to 5)")
        return

    # Kofu: put 2 cards on the bottom of your deck, draw 4. In a Food Prep
    # deck it is also the discount itself -- every copy played is one more
    # Colorless off Haymaker and Sonic Edge -- so it stays worth playing
    # even from a hand that does not need the cards.
    if "Kofu" in hand_names and len(pl.hand) >= 3:
        use("Kofu")
        for _ in range(2):
            if pl.hand:
                pl.deck.insert(0, pl.hand.pop(0))
        pl.draw(4)
        log.append(f"  {pl.name}: Kofu (bottom 2, draw 4)")
        return

    # Gladion's Final Battle: playable only as the last card in hand, and
    # then +80 for any attacker without a Rule Box -- against ANY Active,
    # not just an ex. It is the only unrestricted booster in the pool, and
    # a deck whose attack can cost zero Energy can actually go hellbent to
    # turn it on.
    if ("Gladion's Final Battle" in hand_names and len(pl.hand) == 1
            and pl.active and pl.POKEMON[pl.active.name]["prize_value"] == 1):
        use("Gladion's Final Battle")
        pl.turn_buff_any = 80
        log.append(f"  {pl.name}: Gladion's Final Battle (+80 this turn)")
        return

    # Turn-scoped damage boost, only worth the Supporter slot on a turn the
    # Active can actually attack an ex with it.
    if "Black Belt's Training" in hand_names and pl.active and opp.active:
        atk = best_attack(pl, pl.active, opp=opp)
        # prize_value >= 2 is exactly "is a Pokemon ex" in this pool
        # (2 for ex, 3 for Mega Evolution ex), which is what the card reads.
        if atk and opp.POKEMON[opp.active.name]["prize_value"] >= 2:
            use("Black Belt's Training")
            pl.turn_buff_vs_ex = 40
            log.append(f"  {pl.name}: Black Belt's Training (+40 vs ex this turn)")
            return

    # Draw/refresh Supporters, weakest hand first
    if len(pl.hand) <= 4:
        if "Carmine" in hand_names and len(pl.hand) - 1 < 5:
            use("Carmine")
            for c in list(pl.hand):
                pl.remove_from_hand(*c)
                pl.discard.append(c[1])
            pl.draw(5)
            log.append(f"  {pl.name}: Carmine")
            return
        for name, amount in (("Lillie's Determination", 6), ("Professor's Research", 7)):
            if name in hand_names:
                use(name)
                if name == "Professor's Research":
                    for c in list(pl.hand):
                        pl.remove_from_hand(*c)
                        pl.discard.append(c[1])
                    pl.draw(7)
                else:
                    pl.deck.extend(pl.hand)
                    pl.hand = []
                    random.shuffle(pl.deck)
                    pl.draw(6)
                log.append(f"  {pl.name}: {name}")
                return
        if "Team Rocket's Ariana" in hand_names:
            all_tr = bool(pl.in_play_names()) and all(
                n.startswith("Team Rocket's") for n in pl.in_play_names())
            use("Team Rocket's Ariana")
            supporter_draw_to(pl, 8 if all_tr else 5, log, "Team Rocket's Ariana")
            return
        if "Iono" in hand_names:
            use("Iono")
            pl.deck.extend(pl.hand)
            pl.hand = []
            random.shuffle(pl.deck)
            pl.draw(max(1, opp.prizes))
            log.append(f"  {pl.name}: Iono")
            return

    if "Team Rocket's Proton" in hand_names:
        got = []
        for _ in range(3):
            n = search_pokemon_from_deck(
                pl, lambda x: pl.POKEMON[x]["stage"] == "Basic" and x.startswith("Team Rocket's"))
            if n is None:
                break
            got.append(n)
        if got:
            use("Team Rocket's Proton")
            pl.hand.extend(("Pokemon", n) for n in got)
            log.append(f"  {pl.name}: Proton -> {', '.join(got)}")
            return

    if "Team Rocket's Petrel" in hand_names:
        idx = next((i for i, (k, n) in enumerate(pl.deck)
                    if k in ("Item", "Supporter", "Stadium", "Tool")), None)
        if idx is not None:
            use("Team Rocket's Petrel")
            card = pl.deck.pop(idx)
            random.shuffle(pl.deck)
            pl.hand.append(card)
            log.append(f"  {pl.name}: Petrel -> {card[1]}")
            return

    for name in ("Dawn", "Hilda"):
        if name in hand_names:
            picks = []
            if name == "Dawn":
                for stage in ("Basic", "Stage 1", "Stage 2"):
                    n = search_pokemon_from_deck(pl, lambda x: pl.POKEMON[x]["stage"] == stage)
                    if n:
                        picks.append(("Pokemon", n))
            else:
                n = search_pokemon_from_deck(pl, lambda x: pl.POKEMON[x]["stage"] != "Basic")
                if n:
                    picks.append(("Pokemon", n))
                i = next((i for i, (k, _) in enumerate(pl.deck) if k == "Energy"), None)
                if i is not None:
                    picks.append(pl.deck.pop(i))
            if picks:
                use(name)
                pl.hand.extend(picks)
                log.append(f"  {pl.name}: {name} -> {', '.join(p[1] for p in picks)}")
                return

    # Janine's Secret Art: search out and attach up to 2 Basic Darkness
    # Energy to Darkness Pokemon. Prefers the Bench, because attaching to
    # the Active Poisons it -- which is also why N's Castle (free retreat
    # for N's Pokemon) is what turns this into a clean load-and-swap.
    if "Janine's Secret Art" in hand_names:
        targets = [p for p in pl.bench + ([pl.active] if pl.active else [])
                   if "Darkness" in pl.POKEMON[p.name]["types"]][:2]
        pool = [c for c in pl.deck if c[0] == "Energy" and "Darkness" in c[1]]
        if targets and pool:
            use("Janine's Secret Art")
            attached = []
            for t in targets:
                e = next((c for c in pl.deck if c[0] == "Energy" and "Darkness" in c[1]), None)
                if e is None:
                    break
                pl.deck.remove(e)
                t.energy.append(["Darkness"])
                t.energy_names.append(e[1])
                attached.append(t.name)
                if t is pl.active:
                    t.conditions.add("poisoned")
            random.shuffle(pl.deck)
            log.append(f"  {pl.name}: Janine's Secret Art -> {', '.join(attached)}")
            return

    # Gust effects: drag up their weakest benched Pokemon
    for name in ("Boss's Orders", "Team Rocket's Giovanni"):
        if name in hand_names and opp.bench and opp.active is not None:
            target = min(opp.bench, key=lambda p: opp.POKEMON[p.name]["hp"] - p.damage)
            use(name)
            opp.bench.remove(target)
            opp.bench.append(opp.active)
            opp.active = target
            log.append(f"  {pl.name}: {name} -> drags up {target.name}")
            return


KNOWN_TRAINERS = {
    "Rare Candy", "Buddy-Buddy Poffin", "Ultra Ball", "Poké Pad", "Nest Ball",
    "Energy Search", "Night Stretcher", "Lillie's Determination",
    "Professor's Research", "Iono", "Team Rocket's Ariana", "Team Rocket's Proton",
    "Team Rocket's Petrel", "Dawn", "Hilda", "Boss's Orders",
    "Team Rocket's Giovanni", "Judge", "Carmine", "Black Belt's Training",
    "Pokégear 3.0", "Janine's Secret Art", "N's PP Up",
    "Kofu", "Brilliant Blender", "Gladion's Final Battle", "Naveen", "Gwynn", "Raifort",
    "Hole-Digging Shovel",
}


# --------------------------------------------------------------------------
# Energy attachment, retreat, attacking
# --------------------------------------------------------------------------

import re as _re

# Scaling clauses this engine understands. Anything else falls back to the
# attack's printed base damage, and the attack name is recorded in
# UNSCORED_ATTACKS so the report can say which attacks were undervalued
# rather than silently treating them as weak.
UNSCORED_ATTACKS = set()

_FOR_EACH_RE = _re.compile(r"for each ([^.]+)", _re.I)
_MORE_DMG_RE = _re.compile(r"(\d+) more damage for each", _re.I)
_DOES_DMG_RE = _re.compile(r"does (\d+) damage for each", _re.I)
_COUNTERS_RE = _re.compile(r"(?:place|put) (\d+) damage counters?", _re.I)
_FLAT_DOES_RE = _re.compile(r"this attack does (\d+) damage to", _re.I)
_COND_FLAT_BONUS_RE = _re.compile(r"this attack does (\d+) more damage", _re.I)
_FLIP_UNTIL_TAILS_RE = _re.compile(r"flip a coin until you get tails", _re.I)
_FLIP_N_RE = _re.compile(r"flip (\d+) coins", _re.I)


# Tools whose whole job is Retreat Cost. Gravity Gemstone taxes BOTH
# Actives, which is why it sits on an attacker that never wants to retreat.
RETREAT_TOOLS = {"Air Balloon": -2, "Rescue Board": -1, "Gravity Gemstone": 1}

# Tools whose whole effect is extra damage. min_prize 2 means "only
# against a Pokemon ex", which is true of nearly every booster in the pool.
DAMAGE_TOOLS = {
    "Brave Bangle": {"amount": 30, "min_prize": 2, "holder_no_rule_box": True},
    "Maximum Belt": {"amount": 50, "min_prize": 2},
    "Light Ball": {"amount": 50, "min_prize": 2},
}

# Stadiums are otherwise unmodeled here. These are the ones whose whole
# effect is Retreat Cost, which the lock/pivot decks live or die on, so
# they get honoured rather than sitting inert. Value is the modifier;
# "family" restricts it to Pokemon whose name contains that string.
# Stadiums with a modeled once-per-turn effect, applied in use_stadium().
EFFECT_STADIUMS = {"Prism Tower", "Team Rocket's Factory"}

RETREAT_STADIUMS = {
    "N's Castle": {"amount": -99, "family": "N's"},
    "Paradise Resort": {"amount": -1, "family": "Psyduck"},
}


def retreat_of(pl, spot, opp=None):
    """Retreat Cost of `spot` right now: printed, plus Abilities from both
    sides, plus its own Tool, plus a Gravity Gemstone on either Active,
    plus a retreat-affecting Stadium."""
    st = RETREAT_STADIUMS.get(pl.stadium or (opp.stadium if opp else None))
    if st and (not st["family"] or st["family"].lower() in spot.name.lower()):
        if st["amount"] <= -99:
            return 0
    tool_mod = RETREAT_TOOLS.get(getattr(spot, "tool", None), 0)
    if st and st["amount"] > -99:
        if not st["family"] or st["family"].lower() in spot.name.lower():
            tool_mod += st["amount"]
    if spot is pl.active and opp is not None and opp is not pl and opp.active:
        if getattr(opp.active, "tool", None) == "Gravity Gemstone":
            tool_mod += 1
    return AE.effective_retreat(pl, spot, opp, tool_mod)


def _clause_count(clause, pl, opp, spot):
    """How many times a 'for each ...' clause applies right now, or None."""
    c = clause.lower()
    # Phantom Maze / String Bind / Shadowy Knot all price themselves off the
    # defender's Retreat Cost, which is exactly the number this deck's own
    # Abilities are inflating.
    if "in your opponent's active pok" in c and "retreat cost" in c:
        return retreat_of(opp, opp.active, pl) if opp and opp.active else 0
    if "in this pok" in c and "retreat cost" in c:
        return retreat_of(pl, spot, opp)
    if "card in your hand" in c:
        return len(pl.hand)
    if "card in your opponent's hand" in c:
        return len(opp.hand)
    if "benched pok" in c and "both yours and your opponent" in c:
        return len(pl.bench) + len(opp.bench)
    if "your opponent's benched pok" in c:
        return len(opp.bench)
    if "your benched pok" in c:
        return len(pl.bench)
    if "energy attached to your opponent's active" in c:
        return opp.active.energy_count() if opp.active else 0
    if "energy attached to this pok" in c:
        return spot.energy_count()
    if "damage counter on your opponent's active" in c:
        return (opp.active.damage // 10) if opp.active else 0
    if "damage counter on this pok" in c:
        return spot.damage // 10
    if "prize card your opponent has taken" in c:
        return STARTING_PRIZES - opp.prizes
    # "for each of your <Family> Pokemon in play" / "of your Pokemon in play"
    m = _re.search(r"of your ([\w'’ -]*?)\s*pok[eé]mon in play", c)
    if m:
        fam = m.group(1).strip()
        names = pl.in_play_names()
        if not fam:
            return len(names)
        return sum(1 for n in names if fam.lower() in n.lower())
    return None


_REVEAL_TOP_RE = _re.compile(
    r"reveal the top (\d+) cards of your opponent's deck", _re.I)
_USE_AS_THIS_RE = _re.compile(r"use it as this attack", _re.I)
_COPY_DEFENDING_RE = _re.compile(
    r"choose 1 of your opponent's active pok[eé]mon's attacks and use it as this attack", _re.I)
# N's Zoroark ex's Night Joker: "Choose 1 of your Benched N's Pokemon's
# attacks and use it as this attack." The whole deck is one attacker
# borrowing a Bench full of Basics, so scoring this as 0 would write the
# archetype off entirely. The captured group is the family prefix
# ("N's"), empty when the card has no family restriction.
_COPY_OWN_BENCH_RE = _re.compile(
    r"choose 1 of your benched ([\w'’ -]*?)\s*pok[eé]mon's attacks and use it as this attack", _re.I)


def _best_borrowed(pl, opp, spot, text):
    """Which Benched attack Night Joker should borrow this turn.

    Ranked on damage PER TURN, not damage: an attack that locks its user
    out of attacking next turn only lands every other turn, so N's Zekrom's
    Rampaging Thunder (250, self-locking) is worth 125/turn against N's
    Reshiram's Virtuous Flame (170, no drawback). Ranking on raw damage
    alone had the AI pick the 250 every time and attack half as often.
    """
    m = _COPY_OWN_BENCH_RE.search(text)
    if not m:
        return None
    fam = (m.group(1) or "").strip().lower()
    best, best_score = None, -1.0
    for p in pl.bench:
        if fam and fam not in p.name.lower():
            continue
        for a in pl.POKEMON[p.name]["attacks"]:
            if _USE_AS_THIS_RE.search(a.get("text") or ""):
                continue              # no borrowing a borrow
            score = float(attack_damage(pl, opp, spot, a, record=False))
            score += attack_rider_value(pl, opp, a)
            if _SELF_ATTACK_LOCK_RE.search(a.get("text") or ""):
                score /= 2.0
            if score > best_score:
                best, best_score = a, score
    return best


def _copied_attack_damage(pl, opp, spot, text):
    """Attacks that borrow another Pokemon's attack. Returns damage or None.

    Persian ex's Haughty Order (reveal the opponent's top N, use an attack
    found there) and the 'use the Defending Pokemon's attack' pattern are
    both well-defined enough to actually resolve, so they are -- rather
    than scoring the signature attack of a whole archetype as 0.
    The copied attack's own cost is irrelevant: the real card says to use
    it as this attack, which you already paid for.
    """
    m = _COPY_OWN_BENCH_RE.search(text)
    if m:
        chosen = _best_borrowed(pl, opp, spot, text)
        return attack_damage(pl, opp, spot, chosen, record=False) if chosen else 0

    if _COPY_DEFENDING_RE.search(text):
        if not opp.active:
            return 0
        best = 0
        for a in opp.POKEMON[opp.active.name]["attacks"]:
            best = max(best, attack_damage(opp, pl, opp.active, a, record=False))
        return best

    m = _REVEAL_TOP_RE.search(text)
    if m and _USE_AS_THIS_RE.search(text):
        depth = int(m.group(1))
        top = opp.deck[-depth:] if depth <= len(opp.deck) else list(opp.deck)
        best = 0
        for kind, name in top:
            if kind != "Pokemon":
                continue
            for a in opp.POKEMON[name]["attacks"]:
                # Evaluate the borrowed attack from our own board's point of
                # view -- a scaling clause reads our state, not theirs.
                best = max(best, attack_damage(pl, opp, spot, a, record=False))
        return best
    return None


def attack_damage(pl, opp, spot, atk, record=True):
    """Best-effort damage for one attack in the current board state."""
    text = atk.get("text") or ""
    base = atk["damage"]

    if opp is not None and _USE_AS_THIS_RE.search(text):
        copied = _copied_attack_damage(pl, opp, spot, text)
        if copied is not None:
            return copied

    # "If <condition>, this attack does N more damage" -- a flat bonus
    # gated on something the IR already parses as a condition. Dhelmise's
    # Vengeful Anchor is 30 that becomes 170 once four Hide 'n' Sneak
    # Pokemon are in the discard, and nothing was reading the clause.
    m = _COND_FLAT_BONUS_RE.search(text)
    if m and not _FOR_EACH_RE.search(text) and opp is not None:
        eff = _attack_ir(atk)
        if eff.conditions:
            return base + (int(m.group(1))
                           if AE.conditions_met(eff, pl, opp, spot) else 0)

    # Coin-flip attacks: actually flip.
    if _FLIP_UNTIL_TAILS_RE.search(text):
        heads = 0
        while random.random() < 0.5:
            heads += 1
        m = _MORE_DMG_RE.search(text)
        per = int(m.group(1)) if m else base
        return base + per * heads if m else per * heads
    m = _FLIP_N_RE.search(text)
    if m and "for each heads" in text.lower():
        heads = sum(1 for _ in range(int(m.group(1))) if random.random() < 0.5)
        m2 = _DOES_DMG_RE.search(text)
        per = int(m2.group(1)) if m2 else base
        return per * heads

    fe = _FOR_EACH_RE.search(text)
    if fe:
        count = _clause_count(fe.group(1), pl, opp, spot)
        if count is not None:
            m = _COUNTERS_RE.search(text)
            if m:                      # "Place N damage counters ... for each X"
                return int(m.group(1)) * 10 * count
            m = _MORE_DMG_RE.search(text)
            if m:                      # "does N more damage for each X"
                return base + int(m.group(1)) * count
            m = _DOES_DMG_RE.search(text)
            if m:                      # "does N damage for each X"
                return int(m.group(1)) * count
            if base:
                return base * count
        elif record:
            UNSCORED_ATTACKS.add(f"{spot.name}/{atk['name']}")
        return base

    # Flat damage-counter placement with no scaling clause.
    m = _COUNTERS_RE.search(text)
    if m and not base:
        return int(m.group(1)) * 10

    # "This attack does N damage to 1 of your opponent's Pokemon" -- the
    # bench-snipe shape, which carries its number in the text rather than
    # in the damage field.
    m = _FLAT_DOES_RE.search(text)
    if m and not base:
        return int(m.group(1))

    if not base and text and record:
        UNSCORED_ATTACKS.add(f"{spot.name}/{atk['name']}")
    return base


def damage_reduction_for(pl, spot, opp=None):
    """Every "takes N less damage" Ability now flows through one query."""
    return AE.query_damage_reduction(pl, spot, opp)


def retaliation_from(defender, attacker_spot, attacker_player=None):
    """Counters the DEFENDER puts back on the attacking Pokemon.

    Pokemon Abilities resolve through the IR runtime (which honours the
    type gate on team-wide retaliators like Spiritomb). Tools and Special
    Energy carry the same shape on Trainer/Energy cards, so they keep the
    small dedicated index.
    """
    if not defender.active:
        return 0
    total = AE.query_retaliation(defender, attacker_spot, attacker_player)
    act = defender.active
    act_types = defender.POKEMON[act.name]["types"]
    for cname in ([act.tool] if act.tool else []) + list(getattr(act, "energy_names", [])):
        r = RETALIATE_CARDS.get(cname)
        if not r:
            continue
        if r.get("requires_type") and r["requires_type"] not in act_types:
            continue
        total += r["counters"] * 10
    return total


# Rough value of an attack's non-damage riders, in damage-equivalents. A
# purely damage-ranked AI never picks a 0-damage setup attack, which made
# every Special-Condition deck unplayable in simulation: Arbok's Panic
# Poison (0 damage, applies Burned + Confused + Poisoned, and is the whole
# setup for Muk's 100-per-condition Hazardous Venom) always lost the
# comparison to a vanilla 70-damage attack.
RIDER_VALUE = {
    "poisoned": 30,     # 10/turn ongoing, and it stacks with the below
    "burned": 40,       # 20/turn, though it can flip off
    "asleep": 45,       # denies their attack until they flip out of it
    "paralyzed": 40,    # denies exactly one attack
    "confused": 25,     # ~50% denial
}


def _attack_ir(atk):
    key = (atk["name"], atk.get("text") or "")
    eff = _ATTACK_IR_CACHE.get(key)
    if eff is None:
        eff = IR.compile_effect("attack", atk["name"], atk.get("text") or "")
        _ATTACK_IR_CACHE[key] = eff
    return eff


def attack_rider_value(pl, opp, atk):
    """Damage-equivalent worth of an attack's side effects, right now."""
    text = atk.get("text") or ""
    if not text or opp is None or not opp.active:
        return 0
    eff = _attack_ir(atk)
    if eff.unsupported:
        return 0
    if eff.conditions and not AE.conditions_met(eff, pl, opp, pl.active):
        return 0
    value = 0
    for act in eff.actions:
        if act.op == IR.Op.APPLY_CONDITION:
            already = getattr(opp.active, "conditions", set())
            for c in act.filter.get("conditions") or []:
                if c not in already:          # re-applying an existing one is worth nothing
                    value += RIDER_VALUE.get(c, 20)
        elif act.op == IR.Op.DISCARD_ENERGY_FROM_OPPONENT:
            value += 25 if opp.active.energy else 0
        elif act.op == IR.Op.MILL_OPPONENT:
            # Decking someone out is a whole win, worth six Prizes. Milling
            # N of the D cards they have left is N/D of the way there, so
            # price it against what a Prize is worth in damage (~250, one
            # KO). Flat-rating it at 5/card meant a 0-damage mill attack
            # never beat any attack that dealt damage, so the AI would not
            # play the deck-out plan at all -- the same shape of bug that
            # made Special-Condition decks unplayable before RIDER_VALUE.
            left = max(len(opp.deck), 1)
            value += (act.amount or 1) / left * 6 * 250
        elif act.op == IR.Op.DISCARD_FROM_OPPONENT:
            value += 10 * (act.amount or 1)
        elif act.op == IR.Op.CONDITIONAL_KO:
            victim = conditional_ko_target(pl, opp, atk)
            if victim is not None:
                # Worth the whole Pokemon: it dies regardless of HP.
                value += pl.POKEMON.get(victim.name, {}).get("hp", 200)
        elif act.op == IR.Op.PLACE_COUNTERS and act.target in (
                IR.Target.OPP_ANY, IR.Target.OPP_ALL, IR.Target.OPP_BENCHED):
            per = act.filter.get("per_discard_card")
            if per:
                # Re-Brew is worth whatever fuel is sitting in the discard
                # right now -- zero on an empty pile, 100+ on a loaded one.
                want = per.replace("basic ", "").strip()
                fuel = sum(1 for c in pl.discard if want in c.lower())
                value += (act.amount or 0) * 10 * fuel
            else:
                value += (act.amount or 0) * 10 * act.filter.get("targets", 1)
        elif act.op == IR.Op.MOVE_COUNTERS:
            value += 20
        elif act.op == IR.Op.SEARCH_TO_BENCH:
            # Worth something only while there is Bench room to fill.
            room = max(0, 5 - len(pl.bench))
            value += 35 * min(act.amount or 1, room)
    return int(value * getattr(eff, "chance", 1.0))


_SELF_ATTACK_LOCK_RE = _re.compile(
    r"during your next turn, this pok[eé]mon can'?t (?:attack|use attacks)", _re.I)


def _borrowed_text(pl, opp, spot, atk):
    """An attack's text plus the text of whatever it borrows.

    Night Joker copying Rampaging Thunder inherits its "can't attack next
    turn" clause, so the drawback has to follow the copy.
    """
    text = atk.get("text") or ""
    if not _COPY_OWN_BENCH_RE.search(text):
        return text
    chosen = _best_borrowed(pl, opp, spot, text)
    return (chosen.get("text") or "") if chosen else text


def conditional_ko_target(pl, opp, atk):
    """Which opposing Pokemon this attack Knocks Out outright, if any.

    Mega Absol ex's Terminal Period Knocks Out an Active sitting on
    exactly 6 damage counters no matter its HP -- the payoff for a deck
    that places counters two at a time. Scored on damage it reads as a
    0-damage attack and never gets used.
    """
    eff = _attack_ir(atk)
    if eff.unsupported:
        return None
    for act in eff.actions:
        if act.op != IR.Op.CONDITIONAL_KO:
            continue
        want = (act.filter.get("exact_counters") or 0) * 10
        pool = ([opp.active] if act.target == IR.Target.OPP_ACTIVE
                else opp.in_play())
        for p in pool:
            if p is not None and p.damage == want:
                return p
    return None


def attack_wins_game(pl, opp, spot, atk):
    """Does using this attack, right now, win the game outright?

    Checks the attack itself and -- because N's Zoroark ex's Night Joker
    borrows a Benched Pokemon's attack -- everything it could borrow. This
    is the only way the alternate win condition can be reached in practice:
    Victory Symbol costs Psychic and the deck built around it runs
    Darkness, so it is always cast through the copy.
    """
    def _wins(a):
        text = a.get("text") or ""
        if "win this game" not in text.lower():
            return False
        eff = _attack_ir(a)
        if eff.unsupported:
            return False
        if not any(act.op == IR.Op.WIN_GAME for act in eff.actions):
            return False
        return AE.conditions_met(eff, pl, opp, spot)

    if _wins(atk):
        return True
    m = _COPY_OWN_BENCH_RE.search(atk.get("text") or "")
    if not m:
        return False
    fam = (m.group(1) or "").strip().lower()
    for p in pl.bench:
        if fam and fam not in p.name.lower():
            continue
        if any(_wins(a) for a in pl.POKEMON[p.name]["attacks"]):
            return True
    return False


def attack_value(pl, opp, spot, atk):
    if opp is not None and attack_wins_game(pl, opp, spot, atk):
        return 10 ** 6            # nothing outranks winning on the spot
    dmg = attack_damage(pl, opp, spot, atk) if opp is not None else atk["damage"]
    return dmg + attack_rider_value(pl, opp, atk)


def best_attack(pl, spot, only_payable=True, opp=None):
    info = pl.POKEMON[spot.name]
    best, best_val = None, -1
    for atk in info["attacks"]:
        if only_payable and not can_pay(effective_cost(pl, spot, atk["cost"], opp),
                                        spot.energy):
            continue
        val = attack_value(pl, opp, spot, atk)
        if val > best_val:
            best, best_val = atk, val
    return best


def energy_shortfall(pl, spot):
    """How many more Energy the Active needs for its biggest attack."""
    info = pl.POKEMON[spot.name]
    if not info["attacks"]:
        return 0
    # Only attacks this deck could ever pay for. N's Reshiram's Virtuous
    # Flame costs Fire/Fire/Lightning/Colorless and lives in a mono-Darkness
    # deck: it is never cast, only borrowed by N's Zoroark ex's Night Joker.
    # Counting it here sent every Energy to the Bench toolbox and starved
    # the one Pokemon that actually attacks.
    castable = [a for a in info["attacks"]
                if all(c == "Colorless" or c in pl.energy_types
                       for c in a["cost"])]
    if not castable:
        return 0
    # Deliberately the UNREDUCED cost: a conditional discount (Sniper's
    # Eye) can be off next turn, so keep loading Energy toward the real
    # printed cost rather than stopping at the discounted one.
    need = max(len(a["cost"]) for a in castable)
    return max(0, need - spot.energy_count())


def attach_energy(pl, cards_by_name, log):
    idx = next((i for i, (k, n) in enumerate(pl.hand) if k == "Energy"), None)
    if idx is None:
        return
    target = None
    if pl.active and energy_shortfall(pl, pl.active) > 0:
        target = pl.active
    else:
        # Among Benched Pokemon that still need Energy, feed the one that
        # would hit hardest if promoted -- otherwise Energy trickles onto
        # whichever toolbox Basic happens to be first in the list.
        needy = [p for p in pl.bench if energy_shortfall(pl, p) > 0]
        if needy:
            target = max(needy, key=lambda p: _potential_damage(pl, p))
    if target is None:
        return
    kind, name = pl.hand.pop(idx)
    target.energy.append(energy_types_for(name, cards_by_name))
    target.energy_names.append(name)
    log.append(f"  {pl.name}: attaches {name} to {target.name}")


def _ready_damage(pl, opp, spot):
    atk = best_attack(pl, spot, opp=opp)
    return attack_damage(pl, opp, spot, atk) if atk else 0


def _potential_damage(pl, spot):
    """What this Pokemon would hit for once it IS paid up -- used to decide
    who deserves the Energy, where "what can it do right now" is always 0."""
    # Printed base damage only: a full evaluation needs an opponent board
    # and this is just a ranking, not a damage prediction.
    info = pl.POKEMON[spot.name]
    castable = [a for a in info["attacks"]
                if all(c == "Colorless" or c in pl.energy_types for c in a["cost"])]
    if not castable:
        return 0

    def printed(a):
        # A copy attack (Night Joker) has no damage number of its own; it
        # is worth whatever it can borrow. Ranking it at 0 sent every
        # Energy to the Bench toolbox and starved the actual attacker.
        m = _COPY_OWN_BENCH_RE.search(a.get("text") or "")
        if not m:
            return a["damage"] or 0
        fam = (m.group(1) or "").strip().lower()
        best = 0
        for p in pl.in_play():
            if p is spot or (fam and fam not in p.name.lower()):
                continue
            for b in pl.POKEMON[p.name]["attacks"]:
                if not _USE_AS_THIS_RE.search(b.get("text") or ""):
                    best = max(best, b["damage"] or 0)
        return best

    return max(printed(a) for a in castable)


def attach_tools(pl, log):
    """Attach a Pokemon Tool to whoever will be holding the Active Spot.
    Only Tools carrying a modeled effect (retaliation) are attached -- any
    other Tool would be decoration the engine cannot honor."""
    for kind, name in list(pl.hand):
        if kind != "Tool" or (name not in RETALIATE_CARDS
                              and name not in DAMAGE_TOOLS):
            continue
        if name in DAMAGE_TOOLS:
            if not pl.active or pl.active.tool:
                continue
            # Brave Bangle pays out only on an attacker WITHOUT a Rule
            # Box, so putting it on the deck's lone ex is a dead card.
            if DAMAGE_TOOLS[name].get("holder_no_rule_box") and \
                    pl.POKEMON[pl.active.name]["prize_value"] != 1:
                continue
            pl.remove_from_hand(kind, name)
            pl.active.tool = name
            log.append(f"  {pl.name}: attaches {name} to {pl.active.name}")
            continue
        if not pl.active or pl.active.tool:
            continue
        r = RETALIATE_CARDS[name]
        if r.get("requires_type") and r["requires_type"] not in pl.POKEMON[pl.active.name]["types"]:
            continue
        pl.remove_from_hand(kind, name)
        pl.active.tool = name
        log.append(f"  {pl.name}: attaches {name} to {pl.active.name}")


def use_counter_movers(pl, opp, log):
    """Munkidori-style "move up to N damage counters from 1 of your Pokemon
    to 1 of your opponent's".

    This is a CHOICE Ability, so the engine has to pick for you, and the
    heuristic is an assumption rather than a fact: move as many counters as
    allowed off your most-damaged Pokemon and onto the opponent's Active.
    A human would sometimes aim at a Benched target instead to set up a
    later knockout, which this never does -- so treat the resulting numbers
    as a floor for what a mover is worth, not a measurement of it.
    """
    if not opp.active:
        return
    for p in pl.in_play():
        for ab in pl.POKEMON[p.name]["abilities"]:
            if ab.get("kind") != "move_counters":
                continue
            key = ability_key(p, ab)
            if key in pl.abilities_used:
                continue
            need = ab.get("requires_energy_type")
            if need and not any(need in e for e in p.energy):
                continue
            donors = [q for q in pl.in_play() if q.damage >= 10]
            if not donors:
                continue
            donor = max(donors, key=lambda q: q.damage)
            amount = min(ab["amount"] * 10, donor.damage)
            donor.damage -= amount
            opp.active.damage += amount
            pl.abilities_used.add(key)
            log.append(f"  {pl.name}: {p.name} moves {amount} damage from "
                       f"{donor.name} onto {opp.active.name}")


def try_retreat(pl, opp, log):
    """Retreat when a Benched Pokemon would hit meaningfully harder.

    The earlier version only retreated when the Active literally could not
    attack, which left a big finisher (Persian ex, a Stage 2 ex) sitting on
    the Bench for the whole game while a 20-damage Basic held the Active
    Spot -- a real AI flaw that made every finisher-based deck look far
    worse than it is.
    """
    if not pl.active or not pl.bench:
        return
    cost = retreat_of(pl, pl.active, opp)
    if pl.active.energy_count() < cost:
        return
    here = _ready_damage(pl, opp, pl.active)
    ready = [p for p in pl.bench if _ready_damage(pl, opp, p) > max(here, 0)]
    if not ready:
        return
    target = max(ready, key=lambda p: _ready_damage(pl, opp, p))
    # Only pay the retreat cost if the upgrade is worth it.
    if _ready_damage(pl, opp, target) <= here:
        return
    for _ in range(cost):
        pl.discard.append("Energy")
        pl.active.energy.pop()
    pl.bench.remove(target)
    clear_conditions(pl.active, "retreated", log, pl.name)
    pl.bench.append(pl.active)
    pl.active = target
    log.append(f"  {pl.name}: retreats into {target.name}")


def do_attack(pl, opp, log):
    """Returns True if the game ended."""
    if not pl.active or not opp.active:
        return False
    if pl.active.evolved_this_turn:
        pass  # evolving does not prevent attacking in the real game
    if condition_blocks_attack(pl, log):
        return False
    if pl.active.attack_locked:
        pl.active.attack_locked = False
        log.append(f"  {pl.name}: {pl.active.name} can't attack this turn")
        return False
    atk = best_attack(pl, pl.active, opp=opp)
    if not atk:
        return False
    # The alternate win condition resolves before damage and ends the game.
    if attack_wins_game(pl, opp, pl.active, atk):
        pl.prizes = 0
        log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} -- WINS THE GAME OUTRIGHT")
        return True
    victim = conditional_ko_target(pl, opp, atk)
    if victim is not None:
        victim.damage = 10 ** 6      # forced Knock Out, HP is irrelevant
        log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} -- "
                   f"{victim.name} Knocked Out outright (exact counters)")

    dmg = attack_damage(pl, opp, pl.active, atk)
    # A 0-damage attack is still worth using when it carries a rider --
    # Arbok's Panic Poison applies three Special Conditions and deals
    # nothing, and bailing on `dmg <= 0` skipped it even after the AI had
    # correctly chosen it.
    if dmg <= 0 and attack_rider_value(pl, opp, atk) <= 0:
        return False
    atk_types = pl.POKEMON[pl.active.name]["types"]
    weak = opp.POKEMON[opp.active.name]["weakness"]
    if weak and weak in atk_types:
        dmg *= 2
    dmg += AE.query_damage_buff(pl, pl.active, opp)
    if pl.turn_buff_vs_ex and opp.POKEMON[opp.active.name]["prize_value"] >= 2:
        dmg += pl.turn_buff_vs_ex
    dmg += pl.turn_buff_any
    # Tools that add damage. Brave Bangle only pays out for an attacker
    # WITHOUT a Rule Box, which is the whole reason it fits a deck of
    # single-Prize attackers.
    tool = DAMAGE_TOOLS.get(getattr(pl.active, "tool", None))
    if tool and opp.POKEMON[opp.active.name]["prize_value"] >= tool["min_prize"]:
        if not tool.get("holder_no_rule_box") or \
                pl.POKEMON[pl.active.name]["prize_value"] == 1:
            dmg += tool["amount"]
    reduction = damage_reduction_for(opp, opp.active, pl)
    if reduction:
        dmg = max(0, dmg - reduction)
    opp.active.damage += dmg
    log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} for {dmg}"
               f"{f' (-{reduction} reduced)' if reduction else ''}"
               f" -> {opp.active.name} at {opp.active.damage}/{opp.POKEMON[opp.active.name]['hp']}")

    if _SELF_ATTACK_LOCK_RE.search(_borrowed_text(pl, opp, pl.active, atk)):
        pl.active.attack_locked = True

    attack_side_effects(pl, opp, atk, log)


    # Retaliation resolves even if the defender is Knocked Out by this hit.
    back = retaliation_from(opp, pl.active, pl) if dmg > 0 else 0
    if back:
        pl.active.damage += back
        log.append(f"  {opp.name}: retaliation puts {back} back on {pl.active.name}")
    if pl.active and pl.active.damage >= pl.POKEMON[pl.active.name]["hp"]:
        taken = pl.POKEMON[pl.active.name]["prize_value"]
        log.append(f"  {pl.name}: {pl.active.name} KO'd by retaliation (+{taken} to {opp.name})")
        pl.discard.append(pl.active.name)
        pl.active = None
        pl.lost_pokemon_last_turn = True
        opp.prizes -= taken
        if opp.prizes <= 0:
            return True
        if pl.bench:
            pl.bench.sort(key=lambda p: pl.POKEMON[p.name]["hp"] - p.damage, reverse=True)
            pl.active = pl.bench.pop(0)
        else:
            return True

    if opp.active.damage >= opp.POKEMON[opp.active.name]["hp"]:
        taken = opp.POKEMON[opp.active.name]["prize_value"]
        log.append(f"  {pl.name}: KO on {opp.active.name} (+{taken} prizes)")
        opp.discard.append(opp.active.name)
        opp.active = None
        opp.lost_pokemon_last_turn = True
        pl.prizes -= taken
        if pl.prizes <= 0:
            return True
        if opp.bench:
            # Promote whoever can actually fight, falling back to the
            # biggest body. Sorting on remaining HP alone put a Bench
            # toolbox piece -- one whose attacks the deck cannot even pay
            # for -- into the Active Spot ahead of the real attacker.
            opp.bench.sort(key=lambda p: (_ready_damage(opp, pl, p),
                                          opp.POKEMON[p.name]["hp"] - p.damage),
                           reverse=True)
            opp.active = opp.bench.pop(0)
            log.append(f"  {opp.name}: promotes {opp.active.name}")
        else:
            return True
    return False


# --------------------------------------------------------------------------
# Attack side-effects, via the same IR the Abilities use
# --------------------------------------------------------------------------
# An attack's rider text ("Your opponent's Active Pokemon is now Burned and
# Poisoned", "discard an Energy from your opponent's Active") is the same
# vocabulary as an Ability's, so it goes through the same compiler rather
# than a second parallel parser. Only the ops that make sense as an attack
# rider are applied -- damage itself is already handled by attack_damage().

_ATTACK_IR_CACHE = {}

ATTACK_RIDER_OPS = {
    IR.Op.APPLY_CONDITION,
    IR.Op.DISCARD_ENERGY_FROM_OPPONENT,
    IR.Op.MILL_OPPONENT,
    IR.Op.HEAL,
    IR.Op.DISCARD_FROM_OPPONENT,
    # Lampent's Spreading Light fills the Bench with its own Stage 1 --
    # a 0-damage setup attack that is the entire early game of a deck
    # built on the Stage 2 above it.
    IR.Op.SEARCH_TO_BENCH,
    IR.Op.PLACE_COUNTERS,
    IR.Op.MOVE_COUNTERS,
}


def attack_side_effects(pl, opp, atk, log):
    """Apply an attack's non-damage rider effects."""
    text = atk.get("text") or ""
    if not text:
        return
    key = (atk["name"], text)
    eff = _ATTACK_IR_CACHE.get(key)
    if eff is None:
        eff = IR.compile_effect("attack", atk["name"], text)
        _ATTACK_IR_CACHE[key] = eff
    if eff.unsupported:
        return
    # An attack's rider can be gated the same way an Ability's is --
    # Matcha Spin only spreads counters at 6+ Hide 'n' Sneak Pokemon in
    # the discard. Firing riders unconditionally made those attacks read
    # as always-on.
    if eff.conditions and not AE.conditions_met(eff, pl, opp, pl.active):
        return
    if getattr(eff, "chance", 1.0) < 1.0 and random.random() >= eff.chance:
        return
    for act in eff.actions:
        if act.op not in ATTACK_RIDER_OPS:
            continue
        AE.apply_action(act, pl, opp, pl.active, log)


# --------------------------------------------------------------------------
# Special Conditions
# --------------------------------------------------------------------------
# Poisoned/Burned deal damage at Pokemon Checkup. Asleep/Paralyzed stop the
# Pokemon attacking. Confused makes attacking a coin flip. Crucially --
# and this is a rule this project has had to re-check more than once --
# LEAVING THE ACTIVE SPOT (retreating, or being replaced) and EVOLVING both
# clear every Special Condition, which is what gives a conditions deck its
# escape hatch to play around.

CANNOT_ATTACK = {"asleep", "paralyzed"}


def clear_conditions(spot, why, log=None, owner=""):
    if spot is not None and spot.conditions:
        if log is not None:
            log.append(f"  {owner}: {spot.name} clears {', '.join(sorted(spot.conditions))} ({why})")
        spot.conditions = set()


def condition_blocks_attack(pl, log):
    """Returns True if the Active cannot attack this turn."""
    a = pl.active
    if not a or not a.conditions:
        return False
    if a.conditions & CANNOT_ATTACK:
        log.append(f"  {pl.name}: {a.name} can't attack ({', '.join(sorted(a.conditions & CANNOT_ATTACK))})")
        return True
    if "confused" in a.conditions and random.random() < 0.5:
        a.damage += 30
        log.append(f"  {pl.name}: {a.name} is Confused -- attack fails, 30 to itself")
        return True
    return False


def pokemon_checkup(pl, opp, log):
    """Between-turns damage from Poisoned/Burned, plus recovery flips."""
    a = pl.active
    if not a or not a.conditions:
        return
    if "poisoned" in a.conditions:
        extra = AE.query_condition_damage_bonus(opp, "poisoned")
        dmg = 10 + extra * 10
        a.damage += dmg
        log.append(f"  checkup: {a.name} takes {dmg} from Poison")
    if "burned" in a.conditions:
        extra = AE.query_condition_damage_bonus(opp, "burned")
        dmg = 20 + extra * 10
        a.damage += dmg
        log.append(f"  checkup: {a.name} takes {dmg} from Burn")
        if random.random() < 0.5:
            a.conditions.discard("burned")
    if "asleep" in a.conditions and random.random() < 0.5:
        a.conditions.discard("asleep")
    # Paralysis clears at the end of the affected player's next turn.
    a.conditions.discard("paralyzed")


# --------------------------------------------------------------------------
# Turn / game loop
# --------------------------------------------------------------------------

def opening_hand(pl):
    mulligans = 0
    while True:
        random.shuffle(pl.deck)
        pl.hand = []
        pl.draw(7)
        if pl.has_basic_in_hand():
            return mulligans
        pl.deck.extend(pl.hand)
        pl.hand = []
        mulligans += 1
        if mulligans > 20:
            return mulligans


def take_turn(pl, opp, turn, going_first, cards_by_name, log):
    pl.supporter_played = False
    pl.turn_buff_vs_ex = 0
    pl.turn_buff_any = 0
    pl.abilities_used = set()
    pl.played_supporters_this_turn = set()
    for spot in pl.in_play():
        spot.evolved_this_turn = False

    first_turn = (turn == 1 and going_first)
    if not first_turn:
        # You lose the moment you must draw and cannot. Hand size has
        # nothing to do with it -- the old check also required an empty
        # hand, which meant a decked-out player kept taking turns forever
        # and no mill deck could ever be scored as winning.
        if not pl.deck:
            return "deck_out"
        pl.draw(1)

    play_basics(pl, turn, log)
    if pl.active is None:
        return "no_pokemon"
    try_evolve(pl, opp, turn, log, first_turn)
    play_items(pl, opp, turn, log, first_turn)
    play_supporter(pl, opp, turn, log)
    use_abilities(pl, opp, turn, log)
    use_stadium(pl, log)
    sweep_knocked_out(pl, opp, log)
    attach_energy(pl, cards_by_name, log)
    attach_tools(pl, log)
    try_evolve(pl, opp, turn, log, first_turn)
    try_retreat(pl, opp, log)

    if not first_turn:
        if do_attack(pl, opp, log):
            return "win"
    pokemon_checkup(pl, opp, log)
    if pl.active and pl.active.damage >= pl.POKEMON[pl.active.name]["hp"]:
        taken = pl.POKEMON[pl.active.name]["prize_value"]
        log.append(f"  {pl.name}: {pl.active.name} KO'd at checkup (+{taken} to {opp.name})")
        pl.discard.append(pl.active.name)
        pl.active = None
        pl.lost_pokemon_last_turn = True
        opp.prizes -= taken
        if opp.prizes <= 0:
            return "loss"
        if pl.bench:
            pl.bench.sort(key=lambda p: pl.POKEMON[p.name]["hp"] - p.damage, reverse=True)
            pl.active = pl.bench.pop(0)
        else:
            return "no_pokemon"
    return None


def run_game(modelA, modelB, verbose=False):
    nameA, POKA, DECKA = modelA[0], modelA[1], modelA[2]
    nameB, POKB, DECKB = modelB[0], modelB[1], modelB[2]
    _cards = M.load_cards()
    cards_by_name, _ = M.build_card_index(_cards)
    _CARDS_BY_NAME.update(cards_by_name)
    global RETALIATE_CARDS
    if not RETALIATE_CARDS:
        RETALIATE_CARDS = build_retaliate_index(_cards)

    effA = compile_effects_for(POKA, modelA[3])
    effB = compile_effects_for(POKB, modelB[3])
    a = Player(nameA, POKA, DECKA, effA)
    b = Player(nameB, POKB, DECKB, effB)
    for pl in (a, b):
        for kind, name in pl.deck:
            if kind == "Energy":
                pl.energy_types.update(energy_types_for(name, cards_by_name))
    mullA = opening_hand(a)
    mullB = opening_hand(b)
    log = []

    first = random.choice([a, b])
    second = b if first is a else a
    if verbose:
        log.append(f"{first.name} goes first (mulligans: {a.name} {mullA}, {b.name} {mullB})")

    # Both players must open with a Basic Active.
    for pl in (first, second):
        play_basics(pl, 0, log)

    winner = None
    turn_no = 0
    for round_no in range(1, MAX_TURNS + 1):
        for pl, opp, goes_first in ((first, second, True), (second, first, False)):
            turn_no += 1
            if verbose:
                log.append(f"-- Turn {turn_no} ({pl.name}) --")
            pl.lost_pokemon_last_turn_snapshot = pl.lost_pokemon_last_turn
            result = take_turn(pl, opp, round_no, goes_first, cards_by_name, log)
            pl.lost_pokemon_last_turn = False
            if result == "win":
                winner = pl
                break
            if result == "loss":
                winner = opp
                break
            if result in ("no_pokemon", "deck_out"):
                winner = opp
                if verbose:
                    log.append(f"{pl.name} loses: {result}")
                break
        if winner:
            break

    if verbose:
        print("\n".join(log))
    return {
        "winner": winner.name if winner else None,
        "turns": turn_no,
        "prizes_a": a.prizes,
        "prizes_b": b.prizes,
        "mulligans_a": mullA,
        "mulligans_b": mullB,
    }


def compile_effects_for(POKEMON, resolved_cards):
    """Compile every in-deck Pokemon's Abilities into IR, once per run.

    `resolved_cards` must come from tcg_model.resolve_deck_cards so each
    Pokemon's EXACT printing is used -- Abilities are printing-specific
    (Alakazam MEG 56 has Psychic Draw, Alakazam TWM 82 has none).
    """
    out = {}
    for name in POKEMON:
        card = resolved_cards.get(name)
        out[name] = IR.compile_card_abilities(card) if card else []
    return out


def load_model(path, label):
    text = open(path).read()
    POKEMON, DECKLIST, pooled, unresolved = M.build_deck_model(text)
    unmodeled = sorted({n for k, n in DECKLIST
                        if k in ("Item", "Supporter") and n not in KNOWN_TRAINERS})
    eff_map = compile_effects_for(POKEMON, M.resolve_deck_cards(text))
    live = sorted(f"{n}/{e.name}" for n, es in eff_map.items()
                  for e in es if not e.unsupported)
    dead = sorted(f"{n}/{e.name} ({e.unsupported})" for n, es in eff_map.items()
                  for e in es if e.unsupported)
    return (label, POKEMON, DECKLIST, M.resolve_deck_cards(text)), {
        "abilities_live": live, "abilities_dead": dead,
        "size": len(DECKLIST), "pooled": sorted(pooled),
        "unresolved": sorted(unresolved), "unmodeled": unmodeled,
        "pokemon": POKEMON,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    verbose = "--verbose" in sys.argv
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    pathA, pathB = args[0], args[1]
    n = int(args[2]) if len(args) > 2 else 500

    modelA, metaA = load_model(pathA, "A")
    modelB, metaB = load_model(pathB, "B")
    labelA = pathA.split("/")[-1].replace(".txt", "")
    labelB = pathB.split("/")[-1].replace(".txt", "")
    modelA = (labelA, modelA[1], modelA[2], modelA[3])
    modelB = (labelB, modelB[1], modelB[2], modelB[3])

    for label, meta in ((labelA, metaA), (labelB, metaB)):
        print(f"=== {label} ===")
        print(f"  cards: {meta['size']}")
        if meta["unresolved"]:
            print(f"  NOT FOUND in dataset (excluded): {', '.join(meta['unresolved'])}")
        if meta["pooled"]:
            print(f"  matched by name only: {', '.join(meta['pooled'])}")
        if meta["unmodeled"]:
            print(f"  Trainers with no modeled effect (never played): {', '.join(meta['unmodeled'])}")
        if meta.get("abilities_live"):
            print(f"  Abilities executing ({len(meta['abilities_live'])}): "
                  f"{', '.join(meta['abilities_live'])}")
        if meta.get("abilities_dead"):
            print(f"  Abilities NOT modeled ({len(meta['abilities_dead'])}) -- this deck is"
                  f" undervalued by however much these matter:")
            for d in meta["abilities_dead"]:
                print(f"      {d}")
    print()

    if verbose:
        run_game(modelA, modelB, verbose=True)
        print()

    UNSCORED_ATTACKS.clear()
    wins = defaultdict(int)
    turns = []
    for _ in range(n):
        r = run_game(modelA, modelB)
        wins[r["winner"]] += 1
        turns.append(r["turns"])

    print(f"===== {n} games =====")
    for label in (labelA, labelB):
        w = wins.get(label, 0)
        print(f"  {label:32s} {w:5d} wins  ({100*w/n:5.1f}%)")
    if wins.get(None):
        print(f"  {'no winner (turn cap)':32s} {wins[None]:5d}       ({100*wins[None]/n:5.1f}%)")
    print(f"  average game length: {statistics.mean(turns):.1f} turns")
    if UNSCORED_ATTACKS:
        print("\nUNSCORED attacks (text could not be turned into a damage number,")
        print("so these were treated as 0 and their user is undervalued here):")
        for a in sorted(UNSCORED_ATTACKS):
            print(f"  {a}")
    print("\nBoth sides use the same generic AI; attack side-effects are not executed."
          "\nSee this file's docstring for the full list of simplifications.")


if __name__ == "__main__":
    main()
