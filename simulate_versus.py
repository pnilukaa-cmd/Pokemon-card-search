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
import hashlib
import os
import re as _re
import random
import sys
import statistics
from collections import defaultdict

sys.path.insert(0, ".")
import tcg_model as M
import ability_ir as IR
import ability_engine as AE
import policies as POL

MAX_BENCH = 5
STARTING_PRIZES = 6
DEFAULT_POLICY = "v2"
# Per-player pilot override by player name (vs_field.py sets the candidate's).
PILOT_BY_NAME = {}
MAX_TURNS = 40  # hard stop so a stalled pairing can't loop forever


# --------------------------------------------------------------------------
# Board objects
# --------------------------------------------------------------------------

class InPlay:
    __slots__ = ("name", "damage", "energy", "energy_names", "entered_turn",
                 "shield", "turn_buff",
                 "evolved_this_turn", "tool", "conditions", "attack_locked",
                 "retreat_locked", "attack_locked_by_opponent", "prev_damage",
                 "healed_this_turn", "promoted_this_turn", "last_attack_used",
                 "damage_penalty", "takes_more", "next_turn_attack_buff",
                 "delayed_discard", "extra_prize", "no_weakness",
                 "damage_taken_last_turn", "retaliate_counters", "under")

    def __init__(self, name, turn):
        self.name = name
        # The Evolution stack beneath this card, bottom first. A Knock Out
        # discards the whole pile; only the top card name used to go.
        self.under = []
        self.damage = 0
        self.energy = []          # list of type-lists, one per attached Energy card
        self.energy_names = []    # parallel list of the Energy cards' names
        self.entered_turn = turn
        self.evolved_this_turn = False
        # Lurantis ex's Lively Cutter is 60 that becomes 260 "if this
        # Pokemon was healed during this turn".
        self.healed_this_turn = False
        # Set by attacks that lock their own user out of attacking next
        # turn (N's Zekrom's Rampaging Thunder, Iono's Bellibolt ex's
        # Thunderous Bolt). Without it the AI re-used a 250-damage
        # once-every-other-turn attack every single turn.
        #
        # All three locks are turn COUNTERS, decremented at the end of the
        # owner's every turn (see tick_attack_locks): 2 for a lock on your
        # own next turn, 1 for one the opponent put on "your next turn".
        # They used to be booleans cleared only when read in the Active
        # Spot, so a locked Pokemon that went to the Bench kept its lock
        # and lost a turn whenever it came back, however much later.
        self.attack_locked = 0
        # Set ON THE DEFENDER by "During your opponent's next turn, the
        # Defending Pokemon can't retreat / can't attack". These are the
        # two most common lock effects in the pool (44 card effects between
        # them) and were compiled and then thrown away, so every retreat
        # -lock control deck measured as if its main line did nothing.
        self.retreat_locked = 0
        self.attack_locked_by_opponent = 0
        # "During your opponent's next turn, prevent all damage done to
        # this Pokemon" / "this Pokemon takes N less damage": set by the
        # attack, read by do_attack, gone after the owner's next turn.
        self.shield = None
        # "+N damage from this Pokemon's attacks during this turn", from its
        # own Ability (Feraligatr's Torrential Heart). Cleared at end of turn.
        self.turn_buff = 0
        # Damage on this Pokemon immediately BEFORE the current hit. An
        # "if this Pokemon has full HP" clause is about the state the
        # attack found it in, not the state it left behind, and reading
        # spot.damage after the fact makes such a clause never true.
        self.prev_damage = 0
        self.tool = None
        self.conditions = set()   # asleep / burned / confused / paralyzed / poisoned
        # Mega Lopunny ex's Gale Thrust is 60 that becomes 230 "if this
        # Pokemon moved from your Bench to the Active Spot this turn".
        self.promoted_this_turn = False
        # Weezing's Crazy Blast is 50 that becomes 170 "if this Pokemon
        # used Pervasive Gas during your last turn".
        self.last_attack_used = None
        # "During your opponent's next turn, attacks used by the Defending
        # Pokemon do N less damage." Ten attacks in the pool say this and
        # none of them did anything. Cleared when the penalised player's
        # turn ends, so it lasts exactly the one turn the card says.
        self.damage_penalty = 0
        # "During your next turn, the Defending Pokemon takes N more damage."
        self.takes_more = 0
        # "During your next turn, this Pokemon's <named> attack does N more
        # damage" (or has base damage N). (attack name, amount, absolute).
        self.next_turn_attack_buff = None
        # "At the end of your opponent's next turn, discard the Defending
        # Pokemon", "take 1 more Prize card if it is Knocked Out", and
        # "during your opponent's next turn, this Pokemon has no Weakness".
        self.delayed_discard = False
        self.extra_prize = 0
        self.no_weakness = False
        # Mega Heracross ex's Juggernaut Horn adds however much this Pokemon
        # was hit for last turn; Zamazenta's Strong Bash puts counters back
        # on whatever hits it.
        self.damage_taken_last_turn = 0
        self.retaliate_counters = 0

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
        # The six face-down cards, unreachable all game.
        self.prize_cards = []
        self.supporter_played = False
        # Set by turn-scoped damage Supporters (Black Belt's Training),
        # cleared at the start of every turn.
        self.turn_buff_vs_ex = 0
        # Unrestricted version of the same thing (Gladion's Final Battle),
        # which applies to any Active rather than only a Pokemon ex.
        self.turn_buff_any = 0
        # "During your opponent's next turn, all of your <type> Pokemon
        # take N less damage" (Iron Defender). Set when the Item is
        # played and read while the OPPONENT attacks, so unlike the
        # turn_buff_* fields above it is cleared at the start of this
        # player's NEXT turn rather than the one it was played on.
        self.turn_shield = 0
        self.turn_shield_type = None
        self._shield_armed = False
        self.stadium = None
        # The Stadium the OTHER player put down. A Stadium is shared, so
        # both sides read whichever one is on the table.
        self._opp_stadium = None
        self.lost_pokemon_last_turn = False
        # The names, lower-cased and joined, so a family-scoped clause
        # ("if any of your HOP'S Pokemon were Knocked Out...") can tell
        # whose Knock Out it was.
        self.lost_pokemon_names = ""
        self.abilities_used = set()
        self.played_supporters_this_turn = set()
        self.deck_out = False
        # Set by Budew's Itchy Pollen and friends; cleared at the
        # start of this player's next turn.
        self.item_locked = False
        # Which pilot this player uses. Every AI change applies to BOTH
        # sides by default, which makes a win rate blind to whether the
        # change is an improvement -- so the policy is per-player and
        # ai_selfplay.py can put one pilot against another with the deck
        # held fixed.
        #
        # Read at eleven decision points via POL.knob -- attack valuation,
        # overkill, Prize liability, rider and setup weighting, retreat,
        # self-lock, Energy attachment, hand-cost pitching and promotion.
        # policies.py names the pilots; GREEDY reproduces the engine's
        # historical behaviour exactly, so a greedy-vs-greedy run reading
        # anything other than +0.00 means the plumbing is broken rather
        # than the pilot being interesting.
        #
        # What is NOT here, and what the next pilot will want: the turn
        # number. run_game keeps turn_no as a local, so no knob can vary
        # with the phase of the game -- `setup` is "always setup" rather
        # than "setup until the board is built".
        self.policy = PILOT_BY_NAME.get(name, DEFAULT_POLICY)
        # Turn context, refreshed by take_turn; defaults for boards built
        # outside a game (tests, the lookahead's copies).
        self.round_no = 1
        self._first_turn = False
        self._goes_first = True
        self._cards_by_name = _CARDS_BY_NAME
        # Re-entry guard for Festival Lead's second attack.
        self._attacking_twice = False
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
        """A Basic Pokemon you could legally open on.

        A Fossil is an ITEM whose text says to play it "as if it were" a
        Basic Pokemon -- and Items are played during your turn, which setup
        is not. So a Fossil does NOT satisfy the opening-hand requirement
        and does not stop a mulligan. Counting it as one made a deck whose
        only "Basics" are Fossils look playable when it cannot start a game
        at all.
        """
        return any(k == "Pokemon"
                   and self.POKEMON[n]["stage"] == "Basic"
                   and not self.POKEMON[n].get("is_fossil")
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


_PROVIDES_ONE_RE = _re.compile(
    r"it provides (" + "|".join(M.REAL_TYPES) + r") Energy", _re.I)
_PROVIDES_EVERY_RE = _re.compile(r"provides every type of energy", _re.I)
_PROVIDES_N_RE = _re.compile(
    r"provides (\d+) in any combination of (.+?)(?:\.|$)", _re.I)


# "If this card is attached to a <stage> Pokemon, this card provides every
# type of Energy but provides only N Energy at a time." Prism Energy (Basic)
# and Neo Upper Energy (Stage 2).
_PROVIDES_EVERY_IF_RE = _re.compile(
    r"if this card is attached to an? ([\w ]+?) pok[eé]mon, this card"
    r" provides every type of energy but provides only (\d+) energy at a time",
    _re.I)


_PROVIDES_N_IF_RE = _re.compile(
    r"if this card is attached to an? ([\w' ]+?) pok[e\u00e9]mon, "
    r"it provides ([A-Za-z]+) energy instead", _re.I)


def energy_provisions(card_name, cards_by_name, stage=None):
    """The Energy a single card provides, as one entry PER Energy.

    Special Energy was previously all treated as "any type", because the
    fallback for an unrecognised card was the whole type list. Every
    Special Energy in this pool hit that fallback -- Shadowy Darkness
    Energy says plainly "it provides Darkness Energy" and was being
    counted as able to pay a Fire cost. It also ignored the ones that
    provide more than one: Team Rocket's Energy provides TWO, which is
    the entire reason a 3-Energy attack like Spinning Tail is playable.
    """
    m = M.BASIC_ENERGY_RE.match(card_name)
    if m:
        return [[m.group(1)]]
    card = (cards_by_name.get(card_name) or [None])[0]
    if not card:
        return [list(M.REAL_TYPES)]
    text = " ".join(card.get("rules") or [])

    m = _PROVIDES_N_RE.search(text)
    if m:
        types = [t.capitalize() for t in
                 _re.findall(r"(" + "|".join(M.REAL_TYPES) + r") Energy",
                             m.group(2), _re.I)]
        return [types or list(M.REAL_TYPES)] * int(m.group(1))
    # "provides every type ... but only N at a time". Two cards reach that
    # clause CONDITIONALLY on what they are attached to -- Prism Energy on a
    # Basic, Neo Upper Energy on a Stage 2 -- and both were treated as
    # having met it unconditionally, on the grounds that it is how they are
    # played. That is an assumption, and where the caller knows the stage
    # there is no need to make it. It also hid a real undercount: Neo Upper
    # provides TWO Energy at a time, the same shape as Team Rocket's Energy,
    # and was counted as one.
    m = _PROVIDES_EVERY_IF_RE.search(text)
    if m:
        want, count = m.group(1).strip().lower(), int(m.group(2))
        if stage is None or stage.lower() == want:
            return [list(M.REAL_TYPES)] * count
        mm = _PROVIDES_ONE_RE.search(text)
        return [[mm.group(1).capitalize()]] if mm else [["Colorless"]]
    if _PROVIDES_EVERY_RE.search(text):
        return [list(M.REAL_TYPES)]
    # "If this card is attached to an Evolution Pokemon, it provides
    # ColorlessColorlessColorless Energy INSTEAD." Ignition Energy is the
    # only card in the pool with this shape, and _PROVIDES_ONE_RE below
    # matched its first sentence and returned a single Colorless -- a third
    # of what it provides on the Stage 2s it is played for. Checked before
    # that rule, which would otherwise always win.
    m = _PROVIDES_N_IF_RE.search(text)
    if m:
        want = m.group(1).strip().lower()
        types = [t.capitalize() for t in
                 _re.findall("|".join(M.REAL_TYPES), m.group(2), _re.I)]
        met = (stage is not None
               and (stage.lower() != "basic" if want == "evolution"
                    else stage.lower() == want))
        if met and types:
            return [[t] for t in types]
        mm = _PROVIDES_ONE_RE.search(text)
        if mm:
            return [[mm.group(1).capitalize()]]
    m = _PROVIDES_ONE_RE.search(text)
    if m:
        return [[m.group(1).capitalize()]]
    listed = card.get("types") or []
    if listed:
        return [list(listed)]
    return [list(M.REAL_TYPES)]


def energy_types_for(card_name, cards_by_name):
    """What types the FIRST Energy provided by this card covers.

    No stage is passed: this feeds the deck-wide set of Energy types the
    deck can ever produce, where the permissive reading is the right one.
    """
    return energy_provisions(card_name, cards_by_name)[0]


_TOOL_COST_CUT_RE = _re.compile(
    r"attacks used by the ([\w'’ -]*?) ?pok[eé]mon this card is attached to cost "
    r"(\d+ )?(" + "|".join(M.REAL_TYPES) + r") less", _re.I)


def _tool_cost_cut(pl, spot):
    tool = getattr(spot, "tool", None)
    if not tool:
        return None
    card = _CARDS_BY_NAME.get(tool)
    card = card[0] if isinstance(card, list) and card else card
    m = _TOOL_COST_CUT_RE.search(" ".join((card or {}).get("rules") or []))
    if not m:
        return None
    fam = m.group(1).strip()
    info = pl.POKEMON.get(spot.name) or {}
    if fam and fam.capitalize() in M.REAL_TYPES:
        if fam.capitalize() not in (info.get("types") or []):
            return None
    elif fam and fam.lower() not in spot.name.lower():
        return None
    return m.group(3).capitalize(), int(m.group(2) or 1)


def effective_cost(pl, spot, cost, opp=None, atk_name=None):
    """The attack cost as it stands right now, after any Ability that
    ignores part of it. Decidueye ex's Sniper's Eye turns Crushing Arrow
    from GrassColorlessColorlessColorless into a single Grass -- but only
    while the opponent holds exactly 4 cards, so this is re-derived on
    every pricing rather than baked into the card."""
    # A wholesale override replaces the printed cost outright, so it is
    # settled before any of the subtractive machinery below.
    override = AE.query_cost_override(pl, spot, atk_name, opp)
    if override is not None:
        return ["Colorless"] * override

    ignored = AE.query_ignored_cost_types(pl, spot, opp)
    if "ALL" in ignored:
        return []
    cost = [c for c in cost if c not in ignored] if ignored else list(cost)

    # Counted reductions (Food Prep: "cost Colorless less for each Kofu
    # card in your discard pile"). Colorless symbols come off first --
    # a typed requirement can only be removed by a reduction naming that
    # type, which is why Haymaker still needs its one Water.
    # A tax is added before any discount is taken off, so a card that both
    # taxes and discounts nets out rather than one silently winning.
    tax = AE.query_cost_tax(pl, spot, opp)
    if tax:
        cost += ["Colorless"] * tax
    # A Tool that discounts its holder's attacks: Hop's Choice Band ("Attacks
    # used by the Hop's Pokemon this card is attached to cost Colorless
    # less"). Only its +30 half was modelled.
    tool_cut = _tool_cost_cut(pl, spot)
    if tool_cut:
        typ, n = tool_cut
        for _ in range(n):
            if typ in cost:
                cost.remove(typ)

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
            hp = effective_hp(owner, spot)
            if spot.damage < hp:
                continue
            # Resolute Heart and friends: a lethal hit leaves it on 10 HP
            # instead of Knocking it Out.
            if AE.query_endures(owner, spot, taker):
                spot.damage = hp - 10
                log.append(f"  {owner.name}: {spot.name} endures the hit "
                           f"(left on 10 HP)")
                continue
            taken = owner.POKEMON[spot.name]["prize_value"]
            # Togekiss's Wonder Kiss and friends change how many Prizes a
            # Knock Out is worth, which is a change to the win condition
            # itself -- the most consequential thing on the dead-op list.
            taken = max(0, taken + AE.query_prize_modifier(
                taker, owner, spot, taker.active if spot is owner.active else None))
            AE.discard_pokemon(owner, spot)
            owner.lost_pokemon_names += spot.name.lower() + "|"
            if spot is owner.active:
                owner.active = None
            elif spot in owner.bench:
                owner.bench.remove(spot)
            taker.prizes -= taken
            # Taking a Prize puts that card in your hand. Now that the
            # Prizes are really set aside, this is where they come back --
            # without it, removing them would be a pure cost that never
            # pays anything back, and a KO would be worth less than it is.
            for _ in range(taken):
                if taker.prize_cards:
                    taker.hand.append(taker.prize_cards.pop())
            owner.lost_pokemon_last_turn = True
            log.append(f"  {owner.name}: {spot.name} Knocked Out "
                       f"(+{taken} Prize to {taker.name})")
            if owner.active is None and owner.bench:
                _promote_after_ko(owner, taker, log)


# Stadiums whose text does nothing for the player who plays them, or
# whose effect this engine does not act on. Everything else with a
# compiled effect is worth putting down.
_STADIUM_OPS_WORTH_PLAYING = None


def _stadium_value(pl, opp, name):
    """Rough worth of a Stadium against the opponent's board right now.

    Only the two damage walls are priced; any other modelled Stadium is 1.
    """
    eff = trainer_effect_ir(name)
    for a in (eff.actions if eff else []):
        if a.op != IR.Op.PREVENT_DAMAGE:
            continue
        f = a.filter or {}
        if f.get("attacker_is_ex"):
            # Neutralization Zone: worth it while their attackers are ex and
            # mine are not.
            theirs = sum(opp.POKEMON.get(p.name, {}).get("prize_value", 1) >= 2
                         for p in opp.in_play())
            mine = sum(not pl.POKEMON[p.name]["rule_box"] for p in pl.in_play())
            return 1 + 2 * theirs * (mine > 0)
        if f.get("bench_counters"):
            # Battle Cage: worth it against a deck that places counters.
            places = any(a2.op in (IR.Op.PLACE_COUNTERS, IR.Op.MOVE_COUNTERS)
                         and not (a2.filter or {}).get("attack_damage")
                         for effs in opp.EFFECTS.values() for e in effs
                         for a2 in e.actions)
            return 3 if places else 1
    return 1


def _stadium_has_effect(name, pl):
    """Does this Stadium do anything this player can use right now?

    Two reasons to put one down: my own cards are gated on it by name, or
    its own text compiles to an effect this engine models. The Bench-cap
    case additionally checks that this player can benefit.

    Originally this only recognised a Bench-cap Stadium.
    """
    # A Stadium my own cards NAME is worth playing whatever its own text
    # does. Festival Grounds is the case that exposed this: its printed
    # effect (Special Condition immunity for anything with Energy on it)
    # compiles to nothing this engine models, so "does the Stadium do
    # something?" answered no -- while three Pokemon in the deck read "if
    # Festival Grounds is in play, this Pokemon may use an attack it has
    # twice". The gate matters even when the gate-keeper's own text does
    # not.
    for effs in pl.EFFECTS.values():
        for eff in effs:
            if eff.unsupported:
                continue
            for cond in (eff.conditions or []):
                if (cond.get("kind") == "stadium_in_play"
                        and cond.get("name") == name):
                    return True

    global _STADIUM_OPS_WORTH_PLAYING
    if _STADIUM_OPS_WORTH_PLAYING is None:
        _STADIUM_OPS_WORTH_PLAYING = TRAINER_IR_OPS | {
            IR.Op.BENCH_CAP, IR.Op.CONDITION_IMMUNITY, IR.Op.MODIFY_RETREAT,
            IR.Op.BUFF_DAMAGE, IR.Op.REDUCE_DAMAGE, IR.Op.MODIFY_HP,
            # Neutralization Zone and Battle Cage (read by query_prevented
            # and query_bench_counters_blocked). Missing here, neither was
            # ever put down: 9 and 3 turns a game sitting in hand.
            IR.Op.PREVENT_DAMAGE,
        }
    # A Stadium whose only value is its ONCE-PER-TURN effect is still worth
    # putting down. Checking the passive IR alone meant Fossil Quarry never
    # reached the table even after use_stadium learned to resolve it -- the
    # same shape as Festival Grounds, one layer further in.
    if stadium_turn_effect_ir(name) is not None:
        return True
    # Academy at Night: worth it to a deck with a Seek Inspiration attacker.
    if _HAND_TO_TOP_RE.search(_card_text(name)) and _seek_attackers(pl):
        return True

    eff = trainer_effect_ir(name)
    if eff is None or eff.unsupported:
        return False
    for act in eff.actions:
        if act.op is IR.Op.BENCH_CAP:
            need = (act.filter or {}).get("requires_subtype")
            if not need:
                return True
            if any(need in ((pl.POKEMON.get(p.name) or {}).get("subtypes")
                            or [])
                   for p in pl.in_play()):
                return True
        elif act.op is IR.Op.MODIFY_ATTACK_COST and (act.filter or {}).get("requires_subtype"):
            # Nighttime Mine taxes every Tera attacker, both sides: worth it
            # only when the Tera Pokemon are the opponent's. The op was read
            # by the cost path and missing here, so it was never played.
            need = act.filter["requires_subtype"]
            opp = getattr(pl, "_opp_ref", None)
            mine = any(need in ((pl.POKEMON.get(p.name) or {}).get("subtypes") or [])
                       for p in pl.in_play())
            theirs = opp is not None and any(
                need in ((opp.POKEMON.get(p.name) or {}).get("subtypes") or [])
                for p in opp.in_play())
            if theirs and not mine:
                return True
        elif act.op in _STADIUM_OPS_WORTH_PLAYING:
            return True
    return False


def bench_cap(pl):
    """How many Benched Pokemon this player may have right now.

    Five, unless a Stadium in play says otherwise. Area Zero Underdepths
    raises it to 8 for any player with a Tera Pokemon in play, and the cap
    was a module constant so the Stadium was inert -- three Bench slots in
    a deck built on a Tera attacker.
    """
    stadium = pl.stadium or getattr(pl, "_opp_stadium", None)
    if not stadium:
        return MAX_BENCH
    eff = trainer_effect_ir(stadium)
    if eff is None or eff.unsupported:
        return MAX_BENCH
    for act in eff.actions:
        if act.op is not IR.Op.BENCH_CAP:
            continue
        need = (act.filter or {}).get("requires_subtype")
        if need:
            have = any(need in ((pl.POKEMON.get(p.name) or {}).get("subtypes")
                                or [])
                       for p in pl.in_play())
            if not have:
                continue
        return max(MAX_BENCH, act.amount or MAX_BENCH)
    return MAX_BENCH


_STADIUM_ONCE_RE = _re.compile(
    r"once during each player'?s turn, that player may ", _re.I)
# The card is written from a neutral third person ("that player may search
# THEIR deck"); every rule in ability_ir is written for the card's own
# controller ("your deck"). Normalising the person is the whole difference
# between these compiling and not.
# Ordered: the multi-word forms first, then a general "their X" -> "your X"
# sweep and a general "that player <verb>" -> "you <verb>". The hand-listed
# pairs alone left "1 of THEIR Basic Pokemon" and a second "THAT PLAYER may"
# standing in Grand Tree, so it compiled to nothing.
_STADIUM_PERSON = [
    ("their deck", "your deck"), ("their hand", "your hand"),
    ("their discard pile", "your discard pile"),
    ("their Bench", "your Bench"), ("their Active", "your Active"),
    ("their Benched", "your Benched"), ("their Prize", "your Prize"),
    ("that player shuffles", "you shuffle"),
    ("that player draws", "you draw"),
]
_STADIUM_PERSON_RE = [
    (_re.compile(r"\bthat player may\b", _re.I), "you may"),
    (_re.compile(r"\bthat player\b", _re.I), "you"),
    # NOT "in their name" -- there, "their" refers to the CARDS being
    # searched for, not the player, and rewriting it broke Fossil Quarry
    # which had been working.
    (_re.compile(r"\btheir\b(?! name\b)"), "your"),
    (_re.compile(r"\bthey may\b", _re.I), "you may"),
]
_STADIUM_TURN_CACHE = {}


def stadium_turn_effect_ir(name):
    """Compiled IR for a "once during each player's turn" Stadium, or None.

    use_stadium was a hand-written if/elif over two cards -- the exact
    one-card-at-a-time shape the IR exists to replace. Four more Stadiums
    in the pool compile once the person is normalised (Fossil Quarry,
    Levincia, Lumiose City, Spikemuth Gym) and any future one comes along
    for free.
    """
    if name in _STADIUM_TURN_CACHE:
        return _STADIUM_TURN_CACHE[name]
    eff = None
    if not _CARDS_BY_NAME:
        _CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
    card = _CARDS_BY_NAME.get(name)
    card = card[0] if isinstance(card, list) and card else card
    if isinstance(card, dict):
        text = " ".join(card.get("rules") or [])
        for boiler in _TRAINER_BOILERPLATE:
            text = text.replace(boiler, "")
        if _STADIUM_ONCE_RE.search(text):
            text = _STADIUM_ONCE_RE.sub("you may ", text)
            for a, b in _STADIUM_PERSON:
                text = text.replace(a, b)
            for rx, b in _STADIUM_PERSON_RE:
                text = rx.sub(b, text)
            compiled = IR.compile_effect("trainer", name, " ".join(text.split()))
            if not compiled.unsupported and compiled.actions:
                eff = compiled
    _STADIUM_TURN_CACHE[name] = eff
    return eff


_RESOLVING = [False]


def _visible_top(pl):
    """The top card of `pl`'s deck if the player may use it: always while
    an attack resolves, otherwise only if they put it there themselves."""
    if not pl.deck:
        return None
    if _RESOLVING[0]:
        return pl.deck[-1]
    k = getattr(pl, "_known_top", None)
    if not k:
        return None
    n_at, cards = k
    gone = n_at - len(pl.deck)
    if 0 <= gone < len(cards) and pl.deck[-1] == cards[-1 - gone]:
        return pl.deck[-1]
    return None


def _note_known_top(pl, n):
    """The player just put the top `n` cards of their deck there."""
    pl._known_top = (len(pl.deck), list(pl.deck[-n:]))


def _unseen_own(pl):
    return list(pl.deck) + list(getattr(pl, "prize_cards", []) or [])


def _expected_over(pool, f):
    """Mean of f over the cards, evaluated once per distinct card."""
    if not pool:
        return 0
    from collections import Counter
    return sum(n * f(c) for c, n in Counter(pool).items()) / len(pool)


def _expected_max(pool, f, k):
    """E[max f] over k cards drawn from `pool` (with replacement)."""
    vals = sorted(f(c) for c in pool)
    if not vals:
        return 0
    n, e, prev = len(vals), 0.0, 0.0
    for i, v in enumerate(vals):
        cdf = ((i + 1) / n) ** k
        e += v * (cdf - prev)
        prev = cdf
    return e


def _seek_attackers(pl):
    """Pokemon in play with a "discard the top card of your deck ... use it
    as this attack" attack (Slowking's Seek Inspiration), Active first."""
    return [p for p in pl.in_play()
            if any(_SELF_TOP_COPY_RE.search(a.get("text") or "")
                   for a in pl.POKEMON[p.name]["attacks"])]


def _top_copy_value(pl, opp, spot, card):
    kind, name = card
    info = (pl.POKEMON.get(name) or {}) if kind == "Pokemon" else {}
    if not info or info.get("rule_box"):
        return 0
    return max((attack_value(pl, opp, spot, a) for a in info.get("attacks") or []),
               default=0)


def _top_copy_want(pl, pool=None):
    """The Pokemon a Seek attacker would most like to find on top of the
    deck, from `pool` (default: the deck). None without a Seek attacker."""
    opp = getattr(pl, "_opp_ref", None)
    seekers = _seek_attackers(pl)
    if opp is None or opp.active is None or not seekers:
        return None
    cands = [c for c in (pl.deck if pool is None else pool) if c[0] == "Pokemon"]
    best = max(cands, key=lambda c: _top_copy_value(pl, opp, seekers[0], c),
               default=None)
    if best is None or _top_copy_value(pl, opp, seekers[0], best) <= 0:
        return None
    return best[1]


AE.TOP_COPY_WANT = _top_copy_want


def _transform_pick(pl, opp, spot, cands, use_forced=False):
    """What Ditto's Surprisingly Transform should become: the Pokemon
    that hits hardest next turn with the Energy already attached plus one
    more from hand, then the one that survives best. The lookahead pilot's
    own choice (_forced_transform) wins when it is still in the deck."""
    if use_forced:
        forced = getattr(pl, "_forced_transform", "unset")
        pl._forced_transform = "unset"
        if forced != "unset" and forced in cands:
            return forced
    if opp is None or opp.active is None:
        return cands[0]
    extra = {n for k, n in pl.hand if k == "Energy"}
    extra_prov = [energy_provisions(n, _CARDS_BY_NAME)[0] for n in extra][:1] or [[]]

    def score(name):
        tmp = _clone_spot(spot)
        tmp.name = name
        best = 0
        for atk in pl.POKEMON[name]["attacks"]:
            cost = effective_cost(pl, tmp, atk["cost"], opp, atk.get("name"))
            if can_pay(cost, tmp.energy) or (extra_prov[0] and can_pay(cost, tmp.energy + extra_prov)):
                best = max(best, min(attack_value(pl, opp, tmp, atk), 10 ** 4))
        return (best, effective_hp(pl, tmp) - tmp.damage)
    return max(cands, key=score)


AE.TRANSFORM_PICK = lambda pl, opp, spot, cands: _transform_pick(pl, opp, spot, cands, True)

AE.BENCH_LIMIT = lambda pl: bench_cap(pl)

# Academy at Night: "Once during each player's turn, that player may put a
# card from their hand on top of their deck." Inert until now, and it is
# the combo half of meta_slowking: it sets the card Seek Inspiration
# discards and copies.
_HAND_TO_TOP_RE = _re.compile(
    r"may put a card from their hand on top of their deck", _re.I)


def _stadium_hand_to_top(pl, log):
    name = pl.stadium or getattr(pl, "_opp_stadium", None)
    if not name or not _HAND_TO_TOP_RE.search(_card_text(name)):
        return
    opp = getattr(pl, "_opp_ref", None)
    if opp is None or pl.active is None or pl.active not in _seek_attackers(pl):
        return
    seek = next(a for a in pl.POKEMON[pl.active.name]["attacks"]
                if _SELF_TOP_COPY_RE.search(a.get("text") or ""))
    if not can_pay(effective_cost(pl, pl.active, seek["cost"], opp, seek.get("name")),
                   pl.active.energy):
        return
    want = _top_copy_want(pl, pool=pl.hand)
    if want is None:
        return
    top = _visible_top(pl)
    here = (_top_copy_value(pl, opp, pl.active, top) if top is not None else
            _expected_over(_unseen_own(pl),
                           lambda c: _top_copy_value(pl, opp, pl.active, c)))
    if _top_copy_value(pl, opp, pl.active, ("Pokemon", want)) <= here:
        return
    pl.remove_from_hand("Pokemon", want)
    pl.deck.append(("Pokemon", want))
    _note_known_top(pl, 1)
    log.append(f"  {pl.name}: {name} puts {want} on top of the deck")


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
        return
    # Everything else, straight off the card text. The Stadium in play may
    # be the OPPONENT's -- "each player" means each player -- so this fires
    # on whichever Stadium is on the table.
    else:
        name = pl.stadium or getattr(pl, "_opp_stadium", None)
        if not name:
            return
        eff = stadium_turn_effect_ir(name)
        if eff is None:
            return
        acts = [a for a in eff.actions if a.op in TRAINER_IR_OPS]
        if not acts:
            return
        did = False
        for act in acts:
            if AE.apply_action(act, pl, pl, pl.active, log,
                               make_inplay=lambda n: InPlay(n, 0)) is not False:
                did = True
        if did:
            log.append(f"  {pl.name}: {name} (from card text)")


# An optional draw is declined once it would leave the deck this thin.
# Nothing held the pilot back before: a draw Ability fired every turn it
# could, and N's Zoroark ex's Trade (draw 2, about nine uses a game) emptied
# its own deck in 63% of that deck's games -- the loss was by deck-out, not
# on the board.
DRAW_FLOOR = 6


def _self_damage_buff_ok(pl, opp, p, eff):
    """Feraligatr's Torrential Heart: 5 counters on itself for +120 this
    turn. It fired every turn on every Feraligatr in play -- Benched ones
    too -- and the +120 was never applied, so the deck hurt itself for
    nothing. Worth it only on the Active that is about to attack, when it
    survives the cost, and when the extra damage takes a Knock Out or it
    survives the reply anyway.
    """
    ops = [a.op for a in eff.actions]
    if IR.Op.BUFF_DAMAGE not in ops or IR.Op.PLACE_COUNTERS not in ops:
        return True
    if p is not pl.active or opp.active is None:
        return False
    cost = sum((a.amount or 0) * 10 for a in eff.actions
               if a.op == IR.Op.PLACE_COUNTERS and a.target == IR.Target.SELF)
    buff = sum(a.amount or 0 for a in eff.actions if a.op == IR.Op.BUFF_DAMAGE)
    left = effective_hp(pl, p) - p.damage
    if left <= cost:
        return False
    spare = 1 if any(k == "Energy" for k, _ in pl.hand) else 0
    atks = [a for a in pl.POKEMON[p.name]["attacks"]
            if len(a["cost"]) <= p.energy_count() + spare]
    if not atks:
        return False
    hit = max(attack_damage(pl, opp, p, a, record=False) for a in atks)
    their = effective_hp(opp, opp.active) - opp.active.damage
    ko_now, ko_buffed = hit >= their, hit + buff >= their
    survives = left - cost > _ready_damage(opp, pl, opp.active)
    return (ko_buffed and not ko_now) or (survives and not ko_now)


def _draw_would_deck_out(pl, eff):
    n = sum((a.amount or 1) for a in eff.actions if a.op == IR.Op.DRAW
            and a.target != IR.Target.BOTH_ALL)
    return n > 0 and len(pl.deck) - n < DRAW_FLOOR


def _self_condition_ok(pl, opp, eff, turn):
    """Dark Bell: "Both Active non-Darkness Pokemon are now Confused."

    It hits your own Active as well, and it was played whenever it was in
    hand -- 0.33 times a game the mill deck's own Dudunsparce ex then
    failed its attack. Worth it only when your own Active does not care:
    it is exempt, will not attack this turn anyway, is already Confused,
    or can evolve this turn (evolving cures it).
    """
    for a in eff.actions:
        if a.op != IR.Op.APPLY_CONDITION or a.target != IR.Target.BOTH_ALL:
            continue
        me = pl.active
        if me is None:
            return True
        exempt = (a.filter or {}).get("type_not")
        if exempt and exempt in (pl.POKEMON[me.name].get("types") or []):
            continue
        conds = set(a.filter.get("conditions") or [])
        if conds <= me.conditions:
            continue
        # "Will it attack this turn?" -- Items resolve BEFORE the turn's
        # Energy attachment, so an Active one Energy short with an Energy
        # in hand is about to attack. Asking _ready_damage alone waved Dark
        # Bell through on exactly those turns.
        spare = 1 if any(k == "Energy" for k, _ in pl.hand) else 0
        if not any(len(a["cost"]) <= me.energy_count() + spare
                   for a in pl.POKEMON[me.name]["attacks"]):
            continue
        base = M.base_of(pl.POKEMON, me.name)
        can_evolve = (turn > me.entered_turn and not me.evolved_this_turn
                      and any(k == "Pokemon" and pl.POKEMON.get(n, {}).get("evolves_from") == base
                              for k, n in pl.hand))
        if can_evolve:
            continue
        return False
    return True


def _flute_worth_it(pl, opp):
    """Accompanying Flute hands the opponent free Basics. That is only a
    plan if you can then drag one up: a gust in hand, or a gust attack on
    something in play that can use it."""
    if len(opp.bench) >= 5:
        return False
    if any(n in ("Boss's Orders", "Team Rocket's Giovanni", "Prime Catcher")
           for _, n in pl.hand):
        return True
    for p in pl.in_play():
        for atk in pl.POKEMON[p.name]["attacks"]:
            if any(a.op == IR.Op.SWITCH and (a.filter or {}).get("gust")
                   for a in _attack_ir(atk).actions):
                return True
    return False


def _deck_left_after(pl, draw, returned=0):
    return len(pl.deck) + returned - draw


def _draw_trainer_worth_it(pl, opp, eff, n_cards):
    """Is a drawing Trainer worth resolving now?

    Two checks, both about the draw itself. A card that first shuffles or
    discards the hand is a reset, worth it only while it hands back more
    than it takes. And no draw may leave the deck under DRAW_FLOOR.
    """
    draws = [a for a in eff.actions if a.op == IR.Op.DRAW
             and a.target != IR.Target.BOTH_ALL]
    if not draws:
        return True
    rest = len(pl.hand) - n_cards          # hand once the card itself is played
    amount = 0
    for a in draws:
        f = a.filter or {}
        if f.get("up_to_hand_size") is not None:
            amount += max(0, f["up_to_hand_size"] - rest)
            continue
        amt = a.amount or 1
        if f.get("coin"):
            amt = sum(f["coin"]) / 2          # expected: plan on the average
        if f.get("per_opp_hand"):
            amt = len(opp.hand)
        ii = f.get("instead_if")
        if ii:
            who = pl if ii["who"] == "self" else opp
            have = who.prizes
            if have == ii["count"] if ii["cmp"] == "==" else have <= ii["count"]:
                amt = f["instead"]
        amount += amt
    shuffles = any(a.op == IR.Op.SHUFFLE_HAND_INTO_DECK for a in eff.actions)
    dumps = any(a.op == IR.Op.DISCARD_FROM_SELF and (a.amount or 0) >= 99
                for a in eff.actions)
    if (shuffles or dumps) and rest >= amount:
        return False
    return _deck_left_after(pl, amount, rest if shuffles else 0) >= DRAW_FLOOR


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
            if _draw_would_deck_out(pl, eff):
                continue
            if not _self_damage_buff_ok(pl, opp, p, eff):
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
    printed = M.base_of(pl.POKEMON, name)
    evolves_into = any(o["evolves_from"] == printed for o in pl.POKEMON.values())
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


# A copy attack (N's Zoroark ex's Night Joker) is only as good as the
# Benched Pokemon it borrows from, and the Bench was filled with whatever
# Basic came to hand first: N's Zekrom sat in hand behind a full Bench of
# Meowth ex, Fezandipiti ex and Yveltal on 105 of 623 turns, and a donor
# was in play on only 62% of them. The deck's whole plan is to keep that
# space open.
_DONOR_MIN_DAMAGE = 90


def _copy_plan(pl):
    """(copy attackers, their Basic line, donors) for this deck, from text."""
    cached = getattr(pl, "_copy_plan_cache", None)
    if cached is not None:
        return cached
    attackers, fams = set(), set()
    for name, info in pl.POKEMON.items():
        for a in info["attacks"]:
            m = _COPY_OWN_BENCH_RE.search(a.get("text") or "")
            if m:
                attackers.add(name)
                fams.add((m.group(1) or "").strip().lower())

    donors = set()
    for name, info in pl.POKEMON.items():
        if name in attackers:
            continue
        if not any(f in name.lower() for f in fams):
            continue
        if any((b["damage"] or 0) >= _DONOR_MIN_DAMAGE
               and not _USE_AS_THIS_RE.search(b.get("text") or "")
               for b in info["attacks"]):
            donors.add(name)
    def with_line(names):
        out = set()
        for name in names:
            cur = name
            while cur:
                out.add(cur)
                prev = pl.POKEMON.get(cur, {}).get("evolves_from")
                cur = next((n for n in pl.POKEMON
                            if M.base_of(pl.POKEMON, n) == prev), None) if prev else None
        return out

    # Both lines include the Basics they evolve from: a Benched N's
    # Darumaka is how N's Darmanitan gets to be a donor at all.
    pl._copy_plan_cache = (attackers, with_line(attackers), with_line(donors))
    return pl._copy_plan_cache


def _missing_pieces(pl):
    """Copy-plan Pokemon to fetch first, Basics before what evolves from them."""
    attackers, line, donors = _copy_plan(pl)
    if not attackers or not donors:
        return {}
    here = [p.name for p in pl.in_play()] + [n for k, n in pl.hand if k == "Pokemon"]
    want = {}
    if sum(n in line for n in here) < 2:
        want.update({n: 1 for n in line if pl.POKEMON[n]["stage"] == "Basic"})
    # The donor ranks first: an attacker line without one has nothing to copy.
    if not any(n in donors for n in here):
        want.update({n: 0 for n in donors if pl.POKEMON[n]["stage"] == "Basic"})
    return want


def _bench_plan(pl):
    """(key Pokemon names, Bench slots to hold open for them)."""
    attackers, line, donors = _copy_plan(pl)
    if not attackers or not donors:
        return set(), 0
    here = [p.name for p in pl.in_play()]
    still = {n for _, n in pl.deck} | {n for _, n in pl.hand}
    reserve = 0
    if not any(n in donors for n in here) and donors & still:
        reserve += 1
    if sum(n in line for n in here) < 2 and line & still:
        reserve += 1
    return line | donors, reserve


def play_basics(pl, turn, log):
    if pl.active is None:
        bs = basics_in_hand(pl)
        if bs:
            best = max(bs, key=lambda n: _lead_score(pl, n))
            pl.remove_from_hand("Pokemon", best)
            pl.active = InPlay(best, turn)
            log.append(f"  {pl.name}: {best} to Active")
    core, reserve = _bench_plan(pl)
    hand = sorted(pl.hand, key=lambda c: c[1] not in core)   # key pieces first
    for kind, name in hand:
        if kind == "Pokemon" and pl.POKEMON[name]["stage"] == "Basic" and len(pl.bench) < bench_cap(pl):
            # Keep room for the pieces the deck is built around (see
            # _bench_plan): a support Basic does not take the last slots.
            if name not in core and bench_cap(pl) - len(pl.bench) - 1 < reserve:
                continue
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
            on_bench_entry(pl, pl.bench[-1], log)
            if turn:
                on_play_from_hand(pl, pl.bench[-1], turn, log)


def on_play_from_hand(pl, spot, turn, log):
    """ON_PLAY Abilities: "when you play this Pokemon from your hand onto
    your Bench during your turn". Nothing called this trigger, so Meowth ex
    (in six field decks), Iron Leaves ex, Chien-Pao, Bloodmoon Ursaluna and
    the rest were vanilla Pokemon. Only the hand-to-Bench site calls it: a
    Pokemon searched straight onto the Bench was not played from hand."""
    opp = getattr(pl, "_opp_ref", None)
    if opp is None or spot not in pl.bench:
        return
    for eff in pl.EFFECTS.get(spot.name, []):
        if eff.unsupported or eff.trigger != IR.Trigger.ON_PLAY:
            continue
        # By name: "You can't use more than 1 Last-Ditch Catch Ability
        # each turn" limits the name, not the copy.
        key = ("on_play", eff.name)
        if key in pl.abilities_used:
            continue
        ops = {a.op for a in eff.actions}
        if any(a.op == IR.Op.SWITCH and (a.filter or {}).get("self_in")
               for a in eff.actions):
            if _switch_in_on_play(pl, opp, spot, log):
                pl.abilities_used.add(key)
                log.append(f"  {pl.name}: {spot.name} uses {eff.name}")
            continue
        # "you may discard a Stadium in play": only someone else's.
        if IR.Op.DISCARD_STADIUM in ops and (getattr(pl, "stadium", None)
                                             or not getattr(opp, "stadium", None)):
            continue
        if _draw_would_deck_out(pl, eff):
            continue
        if AE.activate(eff, pl, opp, spot, log,
                       make_inplay=lambda n: InPlay(n, turn)):
            pl.abilities_used.add(key)
            log.append(f"  {pl.name}: {spot.name} uses {eff.name}")


def _switch_in_on_play(pl, opp, spot, log):
    """Rapid Vernier: switch the Pokemon just played into the Active Spot
    and move any Energy from your other Pokemon onto it. Taken only when
    the moved Energy pays for an attack that beats what the current Active
    can do right now -- stripping the Bench to promote a worse attacker is
    what "you may" is there to avoid."""
    me = pl.active
    if me is None or spot not in pl.bench:
        return False
    donors = [me] + [p for p in pl.bench if p is not spot]
    atks = sorted(pl.POKEMON[spot.name]["attacks"],
                  key=lambda a: -len(a["cost"]))
    plan = None
    for atk in atks:
        cost = effective_cost(pl, spot, atk["cost"], opp, atk.get("name"))
        have = list(spot.energy)
        if can_pay(cost, have):
            plan = []
            break
        pool = [(d, i) for d in donors for i in range(len(d.energy))]
        take = []
        for need in [c for c in cost if c != "Colorless"]:
            hit = next((x for x in pool if need in x[0].energy[x[1]]), None)
            if hit is None:
                break
            pool.remove(hit)
            take.append(hit)
            have.append(hit[0].energy[hit[1]])
        while not can_pay(cost, have) and pool:
            hit = pool.pop(0)
            take.append(hit)
            have.append(hit[0].energy[hit[1]])
        if can_pay(cost, have):
            plan = take
            break
    if plan is None:
        return False
    before = _ready_damage(pl, opp, me)
    # Try it, and put everything back if it is not an upgrade.
    saved = {id(d): (list(d.energy), list(getattr(d, "energy_names", []) or []))
             for d in donors + [spot]}
    for d, i in sorted(plan, key=lambda x: -x[1]):
        prov = d.energy[i]
        name = AE.pop_energy(d, i)
        spot.energy.append(prov)
        if name and getattr(spot, "energy_names", None) is not None:
            spot.energy_names.append(name)
    after = _ready_damage(pl, opp, spot)
    if after <= before:
        for d in donors + [spot]:
            d.energy, names = saved[id(d)]
            if hasattr(d, "energy_names"):
                d.energy_names = names
        return False
    pl.bench.remove(spot)
    AE.leaving_active(me, log)
    pl.bench.append(me)
    pl.active = spot
    log.append(f"    {spot.name} switches in with {len(plan)} moved Energy")
    return True


# Risky Ruins is the only card in this pool that fires when a Pokemon is
# PUT ONTO THE BENCH, and the Ability IR has no such trigger: it compiled
# the card as a plain `passive` PLACE_COUNTERS, which no consumer reads, so
# the Stadium was played and then did nothing at all. Matched on the
# WORDING rather than the card name so a second printing of the same text
# is covered without another edit.
_BENCH_ENTRY_RE = _re.compile(
    r"whenever any player puts a (?P<basic>basic )?"
    r"(?:non-(?P<not_type>[\w]+) )?pok[e\u00e9]mon onto their bench"
    r"[^.]*?place (?P<n>\d+) damage counters? on that pok[e\u00e9]mon",
    _re.I)


def on_bench_entry(pl, spot, log=None):
    """Apply the in-play Stadium's bench-entry text to a Pokemon just benched.

    Called from every site that puts a Pokemon onto the Bench from hand or
    deck -- NOT from retreat or promotion, which move a Pokemon that is
    already in play and are not "puts onto their Bench".
    """
    name = getattr(pl, "stadium", None) or getattr(pl, "_opp_stadium", None)
    if not name:
        return
    if not _CARDS_BY_NAME:
        _CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
    card = _CARDS_BY_NAME.get(name)
    card = card[0] if isinstance(card, list) and card else card
    if not isinstance(card, dict):
        return
    m = _BENCH_ENTRY_RE.search(" ".join(card.get("rules") or []))
    if not m:
        return
    info = pl.POKEMON.get(spot.name) or {}
    if m.group("basic") and info.get("stage") != "Basic":
        return
    not_type = m.group("not_type")
    if not_type and not_type.capitalize() in (info.get("types") or []):
        return
    spot.damage += int(m.group("n")) * 10
    if log is not None:
        log.append(f"  {pl.name}: {name} puts {int(m.group('n'))} counters "
                   f"on {spot.name}")


def try_evolve(pl, opp, turn, log, first_turn):
    for kind, name in list(pl.hand):
        if kind != "Pokemon":
            continue
        pre = pl.POKEMON[name]["evolves_from"]
        if not pre:
            continue
        for spot in pl.in_play():
            if M.base_of(pl.POKEMON, spot.name) != pre:
                continue
            # Normal timing: the Pokemon must have been in play since a
            # previous turn, and one Pokemon evolves at most once per turn.
            # (The second half was missing, so any Basic could run all the
            # way to Stage 2 in a single turn and every Stage 2 line
            # simulated a full turn faster than it really is.)
            # "Your first turn" is round 1 for BOTH players: the player
            # going second could evolve on theirs (first_turn is only the
            # going-first player's, which is the attack/Supporter rule).
            normal = (turn > 1 and turn > spot.entered_turn
                      and not spot.evolved_this_turn)
            # Luxio's Fighting Roar is the printed exception to both halves.
            if normal or AE.query_evolves_early(pl, spot, opp):
                pl.remove_from_hand(kind, name)
                spot.under.append(spot.name)
                spot.name = name
                spot.evolved_this_turn = True
                AE.clear_attack_locks(spot)
                clear_conditions(spot, "evolved", log, pl.name)
                log.append(f"  {pl.name}: {pre} -> {name}")
                use_abilities(pl, opp, turn, log, just_evolved=spot)
                break


def _evolves_from_in_pool(name):
    """What a card evolves from, looked up in the whole card pool.

    Needed because a Rare Candy deck usually does NOT run the Stage 1 it
    is skipping, so the deck's own POKEMON map cannot answer the question.
    """
    card = _CARDS_BY_NAME.get(name)
    if isinstance(card, list):
        card = card[0] if card else None
    if isinstance(card, dict):
        return card.get("evolvesFrom")
    return None


def _candy_first(pl, opp, turn, log, first_turn):
    hidden = _locked_in_hand(pl, opp)
    if ("Item", "Rare Candy") in hidden:
        return
    while ("Item", "Rare Candy") in pl.hand:
        if not effect_rare_candy(pl, opp, turn, log, first_turn):
            break


def effect_rare_candy(pl, opp, turn, log, first_turn):
    # "You can't use this card during your first turn" -- either player's.
    if first_turn or turn <= 1:
        return False
    s2 = [n for k, n in pl.hand if k == "Pokemon" and pl.POKEMON[n]["stage"] == "Stage 2"]
    for spot in pl.in_play():
        if turn <= spot.entered_turn or pl.POKEMON[spot.name]["stage"] != "Basic":
            continue
        for name in s2:
            s1 = pl.POKEMON[name]["evolves_from"]
            # Rare Candy says "skipping the Stage 1", so the middle card
            # only has to exist in the CARD POOL -- not in this deck. Reading
            # it out of pl.POKEMON (which is built from the decklist) made
            # Rare Candy silently refuse in every deck that runs the Basic
            # and the Stage 2 without the Stage 1, which is the normal way
            # to build a Rare Candy line.
            mid = M.info_named(pl.POKEMON, s1)
            if mid:
                s1_from = mid["evolves_from"]
            else:
                s1_from = _evolves_from_in_pool(s1)
            if s1_from == M.base_of(pl.POKEMON, spot.name):
                pl.remove_from_hand("Item", "Rare Candy")
                pl.discard.append("Rare Candy")
                pl.remove_from_hand("Pokemon", name)
                spot.under.append(spot.name)
                spot.name = name
                spot.evolved_this_turn = True
                AE.clear_attack_locks(spot)
                log.append(f"  {pl.name}: Rare Candy -> {name}")
                use_abilities(pl, opp, turn, log, just_evolved=spot)
                return True
    return False


def search_pokemon_from_deck(pl, pred):
    # A search takes the first match in a shuffled deck -- i.e. anything.
    # While a copy-attack deck is missing a piece of its plan, that piece
    # comes first (see _bench_plan); otherwise the order is unchanged.
    first = _missing_pieces(pl)
    order = sorted(range(len(pl.deck)), key=lambda i: first.get(pl.deck[i][1], 9))
    for i in order:
        k, n = pl.deck[i]
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
    return info["evolves_from"] in [M.base_of(pl.POKEMON, n)
                                    for n in pl.in_play_names()]


def _locked_in_hand(pl, opp):
    """The cards in hand a play lock forbids right now (AE.play_locks)."""
    kinds, except_family = AE.play_locks(pl, opp)
    if not kinds:
        return []
    out = []
    for c in pl.hand:
        k, n = c
        card = _CARDS_BY_NAME.get(n)
        card = card[0] if isinstance(card, list) and card else (card or {})
        if (k in kinds
                or ("ace_spec" in kinds and "ACE SPEC" in (card.get("subtypes") or []))
                or ("ability_pokemon" in kinds and k == "Pokemon"
                    and (pl.POKEMON.get(n) or {}).get("abilities")
                    and not (except_family and n.lower().startswith(except_family)))):
            out.append(c)
    return out


def _under_play_lock(fn):
    """Run a step that plays cards from hand with the locked cards set
    aside, so every hand-playing path obeys the lock without its own check."""
    def run(pl, *a, **k):
        opp = getattr(pl, "_opp_ref", None)
        hidden = _locked_in_hand(pl, opp) if opp is not None else []
        for c in hidden:
            pl.hand.remove(c)
        try:
            return fn(pl, *a, **k)
        finally:
            pl.hand.extend(hidden)
    run.__wrapped__ = fn
    return run


def play_items(pl, opp, turn, log, first_turn):
    # Budew's Itchy Pollen and Bronzong's Evolution Jammer shut the Item
    # phase off for a turn. The flag is consumed here so it lasts exactly
    # the one turn the card says it does.
    if pl.item_locked:
        log.append(f"  {pl.name}: can't play Item cards this turn (locked)")
    # Iron Defender: "during your opponent's next turn, all of your Metal
    # Pokemon take 30 less damage". Its compiled op is REDUCE_DAMAGE,
    # which play_trainer_from_ir does not resolve because it is a passive
    # op, so the card did nothing at all when played. It is an ITEM, so it
    # belongs here and not in the Supporter chain -- putting it there
    # would also have burned the one Supporter play of the turn.
    # Only worth it while there is actually a Metal Pokemon to shield.
    while ("Item", "Iron Defender") in pl.hand and not pl.turn_shield:
        if not any("Metal" in (pl.POKEMON.get(sp.name, {}).get("types") or [])
                   for sp in pl.in_play()):
            break
        pl.remove_from_hand("Item", "Iron Defender")
        pl.discard.append("Iron Defender")
        pl.turn_shield, pl.turn_shield_type = 30, "Metal"
        pl._shield_armed = True
        log.append(f"  {pl.name}: Iron Defender (Metal takes 30 less next turn)")

    while ("Item", "Rare Candy") in pl.hand:
        if not effect_rare_candy(pl, opp, turn, log, first_turn):
            break

    while ("Item", "Buddy-Buddy Poffin") in pl.hand and len(pl.bench) < bench_cap(pl):
        got = []
        for _ in range(2):
            if len(pl.bench) + len(got) >= bench_cap(pl):
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
            on_bench_entry(pl, pl.bench[-1], log)
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
        # A Stadium is worth playing if it has ANY modelled effect, not
        # only if it is in one of the two hand-written registries. Area
        # Zero Underdepths raises the Bench cap to 8 for a Tera deck and
        # was never played at all, because nothing had added it to a set --
        # the same "it compiles, nothing reaches it" gap as everywhere else.
        if kind != "Stadium":
            continue
        if (name not in RETREAT_STADIUMS and name not in EFFECT_STADIUMS
                and not _stadium_has_effect(name, pl)):
            continue
        # "A Stadium with the same name can't be played" -- whoever's it is.
        if name in (pl.stadium, opp.stadium):
            continue
        # My own Stadium stays unless this one is worth more right now. A
        # deck with two (Neutralization Zone and Battle Cage) otherwise
        # threw its own down every turn to replace it with the other.
        if pl.stadium and _stadium_value(pl, opp, name) <= _stadium_value(pl, opp, pl.stadium):
            continue
        pl.remove_from_hand(kind, name)
        # The Stadium it replaces goes to ITS owner's discard pile. This
        # discarded the new Stadium instead -- one copy in play and one in
        # the discard -- and the replaced one left the game.
        if pl.stadium:
            pl.discard.append(pl.stadium)
        if opp.stadium:
            opp.discard.append(opp.stadium)
        pl.stadium = name
        opp.stadium = None
        # A Stadium is SHARED -- "both yours and your opponent's" is the
        # standard wording -- so the other player has to be able to see it.
        # _opp_stadium was read in three places and assigned in none, which
        # meant a Stadium your opponent played did nothing to you at all.
        pl._opp_stadium = None
        opp._opp_stadium = name
        log.append(f"  {pl.name}: plays Stadium {name}")
        break

    while ("Item", "N's PP Up") in pl.hand:
        # To the N's Pokemon that is short of Energy, the deck's copy
        # attacker first. It went to the first N's Pokemon on the Bench --
        # a Zorua, or a Zoroark ex already paid up -- while the Active
        # Zoroark sat one Darkness short on 175 of 400 idle turns.
        attackers = _copy_plan(pl)[0]
        short = [p for p in pl.bench
                 if "N's" in p.name and energy_shortfall(pl, p) > 0]
        target = max(short, key=lambda p: (p.name in attackers,
                                           -energy_shortfall(pl, p),
                                           _potential_damage(pl, p)),
                     default=None)
        e = next((n for n in pl.discard if n.endswith("Energy")), None)
        if target is None or e is None:
            break
        pl.remove_from_hand("Item", "N's PP Up")
        pl.discard.append("N's PP Up")
        pl.discard.remove(e)
        target.energy.extend(energy_provisions(
            e, _CARDS_BY_NAME, (pl.POKEMON.get(target.name) or {}).get("stage")))
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
        for i in cards_to_pitch(pl, 2):
            pl.discard.append(pl.hand.pop(i)[1])
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
        first = _missing_pieces(pl)
        pick = min((n for n in pl.discard if n in first), key=first.get, default=None) or \
            next((n for n in pl.discard if n in pl.POKEMON), None)
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

    # Every other Item, straight off the card text. Items are unlimited
    # per turn, so this loops until nothing more resolves -- but each pass
    # must place at least one card, or a card that fizzles would spin here
    # forever.
    for _ in range(12):
        played = False
        for kind, name in [c for c in pl.hand if c[0] == "Item"]:
            if name in KNOWN_TRAINERS:
                continue
            if play_trainer_from_ir(pl, opp, kind, name, log, turn):
                played = True
                break
        if not played:
            break


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


def _gust_supporter(pl, opp, name, target, log):
    """Boss's Orders / Giovanni, resolved on `target`."""
    pl.remove_from_hand("Supporter", name)
    pl.discard.append(name)
    pl.supporter_played = True
    pl.played_supporters_this_turn.add(name)
    opp.bench.remove(target)
    clear_conditions(opp.active, "left the Active Spot", log, opp.name)
    opp.bench.append(opp.active)
    opp.active = target
    log.append(f"  {pl.name}: {name} -> drags up {target.name}")


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
        # Bottoming a card is not discarding it, but it is still the two
        # cards you least want, not the two at the front of the list.
        for i in cards_to_pitch(pl, 2):
            pl.deck.insert(0, pl.hand.pop(i))
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
        if ("Carmine" in hand_names and len(pl.hand) - 1 < 5
                and _deck_left_after(pl, 5) >= DRAW_FLOOR):
            use("Carmine")
            for c in list(pl.hand):
                pl.remove_from_hand(*c)
                pl.discard.append(c[1])
            pl.draw(5)
            log.append(f"  {pl.name}: Carmine")
            return
        # Lillie's Determination draws 8, not 6, while you still have all
        # 6 Prize cards -- which is most of the turns it is played on.
        lillie = 8 if pl.prizes == STARTING_PRIZES else 6
        for name, amount in (("Lillie's Determination", lillie), ("Professor's Research", 7)):
            back = len(pl.hand) - 1 if name == "Lillie's Determination" else 0
            if name in hand_names and _deck_left_after(pl, amount, back) >= DRAW_FLOOR:
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
                    pl.draw(amount)
                log.append(f"  {pl.name}: {name}")
                return
        if "Team Rocket's Ariana" in hand_names and _deck_left_after(
                pl, max(0, (8 if all(n.startswith("Team Rocket's") for n in pl.in_play_names())
                            else 5) - (len(pl.hand) - 1))) >= DRAW_FLOOR:
            all_tr = bool(pl.in_play_names()) and all(
                n.startswith("Team Rocket's") for n in pl.in_play_names())
            use("Team Rocket's Ariana")
            supporter_draw_to(pl, 8 if all_tr else 5, log, "Team Rocket's Ariana")
            return
        if "Iono" in hand_names and _deck_left_after(
                pl, max(1, opp.prizes), len(pl.hand) - 1) >= DRAW_FLOOR:
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
                if t is pl.active and not AE.query_condition_immunity(
                        pl, t, "poisoned", opp):
                    AE.apply_condition(t, "poisoned")
            random.shuffle(pl.deck)
            log.append(f"  {pl.name}: Janine's Secret Art -> {', '.join(attached)}")
            return

    # Gust effects: drag up their weakest benched Pokemon
    for name in ("Boss's Orders", "Team Rocket's Giovanni"):
        if name in hand_names and opp.bench and opp.active is not None:
            target = choose_gust_target(pl, opp)
            if target is None:
                continue          # nothing on the Bench beats the Active
            if POL.knob(pl, "lookahead_samples"):
                def apply(me, them, i, name=name):
                    _gust_supporter(me, them, name, them.bench[i], [])
                i = lookahead_pick(pl, opp, list(range(len(opp.bench))), apply,
                                   0, opp.bench.index(target))
                target = opp.bench[i]
            _gust_supporter(pl, opp, name, target, log)
            return

    # Anything the registry above does not know, straight off the card
    # text. Ordered so a Supporter that draws or searches is tried before
    # one that only disrupts, which matches how the hand-written cases are
    # ordered and keeps the AI developing before it interferes.
    for name in sorted(hand_names, key=lambda n: -_ir_supporter_rank(n)):
        if play_trainer_from_ir(pl, opp, "Supporter", name, log, turn):
            return


# --------------------------------------------------------------------------
# Trainers the registry above does not cover, played straight from the IR
# --------------------------------------------------------------------------
# The hand-written registry models 30 of the 257 Trainers in Standard.
# The IR already parses 182 of them and the simulator was throwing all of
# it away, so any deck built out of anything but a short list of staples
# had most of its Trainer line sitting inert in hand for the whole game --
# and every win rate measured here inherited that.
#
# Hand-written effects still win where they exist: they encode targeting
# judgement (which Pokemon to gust, which Energy to attach) that the IR
# does not carry. This is the fallback for everything else.

# Reminder text printed on every card of a type, carrying no effect.
_TRAINER_BOILERPLATE = (
    "You may play any number of Item cards during your turn.",
    "You may play only 1 Supporter card during your turn.",
    "You can't have more than 1 ACE SPEC card in your deck.",
    "You may play only 1 Stadium card during your turn.",
    "Put it next to the Active Spot, and discard it if another Stadium "
    "comes into play.",
    "A Stadium with the same name can't be played.",
    "You may attach any number of Pokémon Tools to your Pokémon during "
    "your turn.",
    "You may attach only 1 Pokémon Tool to each Pokémon, and it stays "
    "attached.",
)

_TRAINER_IR_CACHE = {}


def trainer_effect_ir(name):
    """Compiled IR for a Trainer, or None if nothing useful parses."""
    if name in _TRAINER_IR_CACHE:
        return _TRAINER_IR_CACHE[name]
    # The card index is filled by run_game. Anything that asks before then
    # (load_model's coverage report does) would otherwise cache a None for
    # every Trainer and the IR fallback would be dead for the whole run.
    if not _CARDS_BY_NAME:
        _CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
    card = _CARDS_BY_NAME.get(name)
    card = card[0] if isinstance(card, list) and card else card
    eff = None
    if isinstance(card, dict):
        text = " ".join(card.get("rules") or [])
        for boiler in _TRAINER_BOILERPLATE:
            text = text.replace(boiler, "")
        text = " ".join(text.split())
        if text:
            compiled = IR.compile_effect("trainer", name, text)
            if not compiled.unsupported and compiled.actions:
                eff = compiled
    _TRAINER_IR_CACHE[name] = eff
    return eff


# Ops a Trainer may carry out. Deliberately excludes the passive/static
# ops, which describe a property of something in play and mean nothing on
# a card that goes to the discard the moment it resolves.
# ability_engine needs a Trainer's compiled IR (a Tool or Energy granting
# Special Condition immunity, a Stadium doing the same) and cannot import
# this module back. Hand it the function.
def pitch_rank(pl, kind, name):
    """How badly this player wants to KEEP a card. Low pitches first.

    Only used to pay a "discard a card from your hand" cost, which the
    engine used to pay with hand[0] -- whatever happened to be sitting
    there. The ordering is deliberately coarse; the point is not to find
    the optimal discard but to stop throwing away the two things a deck
    can least afford.

    Energy is ranked by whether anything in play is actually short of it,
    so a deck that is paid up pitches spares freely and a deck that is
    starving holds them. A Pokemon is worth keeping while it can still be
    put into play or evolve something already there -- a fourth copy of a
    Stage 2 with no Stage 1 down is just a card.
    """
    if kind == "Energy":
        short = any(energy_shortfall(pl, p) > 0 for p in pl.in_play())
        return (30 if short else 10) * POL.knob(pl, "pitch_energy_guard")
    if kind == "Pokemon":
        info = pl.POKEMON.get(name) or {}
        if info.get("stage") == "Basic":
            # A Basic is the thing you cannot come back without, but a
            # fifth one with a full Bench is not.
            return 25 if len(pl.in_play()) < 4 else 12
        pre = info.get("evolves_from")
        if pre in [M.base_of(pl.POKEMON, n) for n in pl.in_play_names()]:
            return 28
        # A Stage 1 with no Stage 1 target is NOT a dead card while its
        # pre-evolution is still in the deck -- that is next turn's Poffin.
        # Ranking it dead pitched N's Zoroark ex, the deck's only win
        # condition, 317 times in 300 games.
        if any(n == pre for _, n in pl.deck) or any(n == pre for _, n in pl.hand):
            return 22
        return 5                      # the line is genuinely unreachable
    if kind == "Supporter":
        return 15
    if kind == "Stadium":
        return 8
    return 6                          # Items and Tools are the spare change


def cards_to_pitch(pl, n, exclude=None):
    """The n cards in hand this player can most afford to lose.

    Three places paid a hand cost by taking whatever sat at the front of
    the list -- Ultra Ball's two, Kofu's two, and every compiled
    "discard a card from your hand" cost. Ultra Ball is in all 44 decks
    here, so the blind version ran in essentially every game ever
    measured.

    Measured against the unfixed engine on identical seeds, 44 decks x 8
    opponents x 100 games: mean -0.03 points, 95% CI [-0.81, +0.74]. Read
    that as "field-neutral", NOT as "no effect" -- the aggregate is zero
    by construction, because the panel opponents get the fix too. The
    per-deck numbers are where it shows: 43 of 44 decks moved, mean
    absolute change 2.07 points, 22 decks moved by 2 or more, range -6.50
    (arbok_team_rockets_muk_condition_stack) to +6.25
    (toxic_slumber_vileplume_ex). It is a substantial re-ranking that
    happens to sum to nothing.
    """
    idx = [i for i, c in enumerate(pl.hand) if c != exclude]
    idx.sort(key=lambda i: (pitch_rank(pl, *pl.hand[i]), i))
    return sorted(idx[:n], reverse=True)      # reverse: safe to pop in order


AE.PITCH_RANK = pitch_rank


def _card_kind(pl, name):
    if name in pl.POKEMON:
        return "Pokemon"
    card = _CARDS_BY_NAME.get(name)
    card = card[0] if isinstance(card, list) and card else card
    if not isinstance(card, dict):
        return "Energy" if str(name).lower().endswith("energy") else None
    if card.get("supertype") == "Energy":
        return "Energy"
    subs = card.get("subtypes") or []
    for k, sub in (("Supporter", "Supporter"), ("Stadium", "Stadium"),
                   ("Tool", "Pokémon Tool"), ("Item", "Item")):
        if sub in subs:
            return k
    return None


AE.CARD_KIND = _card_kind


def _card_text(name):
    card = _CARDS_BY_NAME.get(name)
    card = card[0] if isinstance(card, list) and card else card
    return " ".join((card or {}).get("rules") or [])


AE.CARD_TEXT = _card_text
AE.ENERGY_PASSIVES = lambda pl, spot, op=None: energy_passives(pl, spot, op)


def _energy_provides(pl, name, spot):
    # Deck models spell Basic Energy "Fire Energy"; accept "Basic Fire Energy" too.
    name = _re.sub(r"^basic\s+", "", str(name), flags=_re.I)
    got = energy_provisions(name, _CARDS_BY_NAME,
                            (pl.POKEMON.get(spot.name) or {}).get("stage"))
    return got[0] if got else None


AE.ENERGY_PROVIDES = _energy_provides
AE.SWITCH_RANK = lambda pl, opp, spot: _ready_damage(pl, opp, spot)
AE.TRAINER_IR = trainer_effect_ir
AE.ON_BENCH_ENTRY = lambda pl, spot, log=None: on_bench_entry(pl, spot, log)
# A lambda, not the function object: the hooks are wired well above
# where _clause_count is defined, so bind it at call time.
AE.CLAUSE_COUNT = lambda clause, pl, opp, spot: _clause_count(clause, pl, opp, spot)


TRAINER_IR_OPS = {
    IR.Op.DRAW, IR.Op.SEARCH_TO_HAND, IR.Op.SEARCH_TO_BENCH,
    IR.Op.FROM_DISCARD_TO_HAND, IR.Op.ATTACH_ENERGY, IR.Op.MOVE_ENERGY,
    IR.Op.HEAL, IR.Op.SWITCH, IR.Op.PLACE_COUNTERS, IR.Op.MOVE_COUNTERS,
    IR.Op.DISCARD_FROM_OPPONENT, IR.Op.DISCARD_ENERGY_FROM_OPPONENT,
    IR.Op.MILL_OPPONENT, IR.Op.LOOK_AT_DECK, IR.Op.SHUFFLE_SELF_INTO_DECK,
    IR.Op.REVEAL_OPPONENT_HAND, IR.Op.SET_OPPONENT_HAND, IR.Op.LOCK,
    IR.Op.APPLY_CONDITION, IR.Op.DISCARD_STADIUM, IR.Op.SEARCH_TO_DISCARD,
    IR.Op.SWAP_HAND_WITH_DECK, IR.Op.SHUFFLE_HAND_INTO_DECK, IR.Op.FORCE_BENCH_OPPONENT,
    IR.Op.FILL_OPPONENT_BENCH, IR.Op.DISCARD_TOOL_ANY,
    IR.Op.SWAP_IN_PLACE, IR.Op.DISCARD_FROM_SELF, IR.Op.DEVOLVE,
    IR.Op.DISCARD_TO_DECK, IR.Op.CLEAR_CONDITIONS,
    IR.Op.SEARCH_TO_TOP_OF_DECK, IR.Op.REROLL_PRIZES, IR.Op.EVOLVE_FROM_DECK,
    # Repel and its family. The executor for this op has existed since
    # Abilities were wired in and the attack path already resolves it --
    # it was simply never in the set that playing a TRAINER resolves, so
    # Repel was an Item that did nothing when played.
    IR.Op.FORCE_SWITCH_OPPONENT,
}


_IR_SUPPORTER_VALUE = {
    IR.Op.SEARCH_TO_HAND: 5, IR.Op.DRAW: 4, IR.Op.SEARCH_TO_BENCH: 4,
    IR.Op.ATTACH_ENERGY: 4, IR.Op.FROM_DISCARD_TO_HAND: 3,
    IR.Op.SET_OPPONENT_HAND: 3, IR.Op.HEAL: 2, IR.Op.SWITCH: 2,
    IR.Op.DISCARD_ENERGY_FROM_OPPONENT: 2, IR.Op.PLACE_COUNTERS: 2,
}


def _ir_supporter_rank(name):
    eff = trainer_effect_ir(name)
    if eff is None:
        return -1
    return max((_IR_SUPPORTER_VALUE.get(a.op, 1) for a in eff.actions), default=0)


def play_trainer_from_ir(pl, opp, kind, name, log, turn=0):
    """Resolve an unregistered Trainer through the compiled IR.

    Returns True only if something actually happened -- a card whose
    effect fizzles (searching an empty deck, healing an undamaged board)
    must not be spent, or the AI throws its one Supporter per turn away
    on a card that did nothing.
    """
    eff = trainer_effect_ir(name)
    if eff is None:
        return False
    # The card has to still BE in hand. play_items iterates a snapshot of
    # the hand, and since this function started paying costs a failed play
    # can discard from hand -- so a later entry in that snapshot may name a
    # card that has already been pitched. Checking this only further down,
    # after the coin-flip branch had already called remove_from_hand,
    # crashed two shards of a 946-pairing field run.
    extra = 1 if any(c["kind"] == "play_two_copies" for c in eff.costs) else 0
    if pl.hand.count((kind, name)) < 1 + extra:
        return False
    if eff.conditions and not AE.conditions_met(eff, pl, opp, pl.active):
        return False
    actions = [a for a in eff.actions if a.op in TRAINER_IR_OPS]
    if not actions:
        return False
    if not _draw_trainer_worth_it(pl, opp, eff, 1 + extra):
        return False
    if not _self_condition_ok(pl, opp, eff, turn):
        return False
    if any(a.op == IR.Op.FILL_OPPONENT_BENCH for a in eff.actions) \
            and not _flute_worth_it(pl, opp):
        return False
    # A Trainer whose text is a coin flip has to actually flip. Crushing
    # Hammer is "Flip a coin. If heads, discard an Energy" and was resolving
    # unconditionally once it resolved at all.
    if getattr(eff, "chance", 1.0) < 1.0 and random.random() >= eff.chance:
        pl.remove_from_hand(kind, name)
        pl.discard.append(name)
        if kind == "Supporter":
            pl.supporter_played = True
            pl.played_supporters_this_turn.add(name)
        log.append(f"  {pl.name}: {name} -- flipped tails")
        return True

    def make_inplay(n):
        return InPlay(n, turn)

    # Costs. This path never paid them, so Secret Box fetched four cards
    # for free and Transformation Tome would have swapped once per copy
    # instead of once per PAIR. The card being played is taken out of hand
    # first so it cannot be discarded to pay for itself, and put back if
    # the cost turns out to be unaffordable.
    for _ in range(1 + extra):
        pl.remove_from_hand(kind, name)
    if eff.costs and not AE.pay_costs(eff, pl, pl.active, log):
        pl.hand.extend([(kind, name)] * (1 + extra))
        return False

    did = False
    for act in actions:
        if AE.apply_action(act, pl, opp, pl.active, log,
                           make_inplay=make_inplay) is not False:
            did = True
    if not did:
        # Nothing happened, so the card was not spent -- but a cost already
        # paid cannot be taken back, and the only costs here discard from
        # hand or from the board. Return the card and accept that; the
        # alternative is a snapshot/restore of the whole player.
        pl.hand.extend([(kind, name)] * (1 + extra))
        return False
    pl.discard.extend([name] * (1 + extra))
    if kind == "Supporter":
        pl.supporter_played = True
        pl.played_supporters_this_turn.add(name)
    log.append(f"  {pl.name}: {name} (from card text)")
    return True


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
# "This attack's damage isn't affected by Resistance." Nine attacks say it
# and Resistance was applied to all of them -- 30 damage a swing, on cards
# whose whole point is punching through a resisted type.
# "isn't affected by Resistance", and the wider "isn't affected by Weakness
# or Resistance, or by any effects on your opponent's Active Pokemon" -- six
# more attacks whose whole purpose is punching through a resisted type.
_IGNORES_RESISTANCE_RE = _re.compile(
    r"damage isn'?t affected by (?:weakness or )?resistance", _re.I)
_IGNORES_WEAKNESS_RE = _re.compile(
    r"damage isn'?t affected by weakness", _re.I)
# "If <clause>, this attack does nothing." Always written as the FAILURE
# case, so parse_conditions turns each into the positive REQUIREMENT and
# this returns 0 when the requirement is not met. Twelve attacks in the
# pool, every one of which was dealing full damage unconditionally.
_FLIP_ANY_RE = _re.compile(r"flip (?:a coin|\d+ coins)", _re.I)
_BASE_DAMAGE_IS_RE = _re.compile(r"this attack'?s base damage is (\d+)", _re.I)
_REFLECT_DAMAGE_RE = _re.compile(
    r"was damaged by an attack during your opponent'?s last turn, this attack"
    r" does that much more damage", _re.I)
_ATTACK_REQUIRES_RE = _re.compile(
    r"\bif [^.]{4,120}?, this attack does nothing"
    r"|you can use this attack only if ", _re.I)
_FLIP_UNTIL_TAILS_RE = _re.compile(r"flip a coin until you get tails", _re.I)
# "Flip a coin. If tails, this attack does nothing." Twenty attacks in the
# pool say this and every one of them was paying full damage on every use --
# parse_chance reads the odds correctly, but nothing in the damage model
# applied them, because the clause carries no damage NUMBER of its own for
# the bonus paths to latch onto.
_FLIP_ALL_OR_NOTHING_RE = _re.compile(
    r"flip (?:a coin|(\d+) coins)[^.]{0,40}\.?\s*if (?:tails|you get tails)"
    r"[^.]{0,20}this attack does nothing", _re.I)
_MORE_DMG_FLIP_RE = _re.compile(
    r"flip a coin[^.]{0,30}\.?\s*if heads, this attack does (\d+) more damage",
    _re.I)
_FLIP_N_RE = _re.compile(r"flip (\d+) coins", _re.I)
_FLIP_PER_EACH_RE = _re.compile(r"flip a coin for each ([^.]+)", _re.I)
_PER_HEADS_DMG_RE = _re.compile(r"does (\d+) damage[^.]*?for each heads", _re.I)
_DOES_DMG_LOOSE_RE = _re.compile(r"does (\d+) damage[^.]*?for each", _re.I)
_ALSO_DOES_FOR_EACH_RE = _re.compile(
    r"also does (\d+) damage to[^.]*?for each", _re.I)


# Tools whose whole job is Retreat Cost. Gravity Gemstone taxes BOTH
# Actives, which is why it sits on an attacker that never wants to retreat.
RETREAT_TOOLS = {"Air Balloon": -2, "Rescue Board": -1, "Gravity Gemstone": 1}

# Tools whose whole effect is extra damage. min_prize 2 means "only
# against a Pokemon ex", which is true of nearly every booster in the pool.
# Hand-maintained, and it was missing two of the three Tools in the pool
# whose text grants flat bonus damage. Both carry a restriction, and both
# are entered WITH it -- an ungated entry would be the same dropped-clause
# bug as Poffin's HP cap and Poke Pad's Rule Box.
DAMAGE_TOOLS = {
    "Brave Bangle": {"amount": 30, "min_prize": 2, "holder_no_rule_box": True},
    "Maximum Belt": {"amount": 50, "min_prize": 2},
    "Light Ball": {"amount": 50, "min_prize": 2},
    # +40 only while the Pokemon holding it is Poisoned.
    "Binding Mochi": {"amount": 40, "min_prize": 0, "holder_condition": "poisoned"},
    # +30 only on a Hop's Pokemon. Its other half -- "attacks cost
    # Colorless less" -- is NOT modelled, so this is the conservative
    # half of the card.
    "Hop's Choice Band": {"amount": 30, "min_prize": 0, "holder_family": "Hop's"},
}


def damage_tool_applies(pl, tool, holder):
    """Does this Tool's bonus actually apply to `holder` right now?"""
    if tool.get("holder_no_rule_box") and \
            pl.POKEMON[holder.name]["prize_value"] != 1:
        return False
    fam = tool.get("holder_family")
    if fam and fam.lower() not in holder.name.lower():
        return False
    cond = tool.get("holder_condition")
    if cond and cond not in getattr(holder, "conditions", set()):
        return False
    return True

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
    tool = getattr(spot, "tool", None)
    if tool and AE.query_tools_disabled(pl, opp):
        tool = None                     # Jamming Tower
    tool_mod = RETREAT_TOOLS.get(tool, 0)
    tool_mod += sum(a.amount or 0 for _, a in energy_passives(pl, spot, IR.Op.MODIFY_RETREAT))
    if st and st["amount"] > -99:
        if not st["family"] or st["family"].lower() in spot.name.lower():
            tool_mod += st["amount"]
    if spot is pl.active and opp is not None and opp is not pl and opp.active:
        if getattr(opp.active, "tool", None) == "Gravity Gemstone":
            tool_mod += 1
    return AE.effective_retreat(pl, spot, opp, tool_mod)


ENERGY_TYPES = ("Grass", "Fire", "Water", "Lightning", "Psychic",
                "Fighting", "Darkness", "Metal", "Dragon", "Fairy",
                "Colorless")

_TYPED_ENERGY_RE = _re.compile(
    r"\b(grass|fire|water|lightning|psychic|fighting|darkness|metal|dragon|"
    r"fairy|colorless)\s+energy", _re.I)


def energy_units(pl, spot):
    """How many Energy this Pokemon effectively has, after any Ability that
    makes one card provide more (Meganium's Wild Growth)."""
    total = len(spot.energy)
    for e in spot.energy:
        for typ in e:
            total += AE.query_energy_bonus(pl, spot, typ)
            break
    return total


def _energy_matching(clause, spots):
    """Energy on `spots`, restricted to the type the clause names.

    "for each Psychic Energy attached to this Pokemon" was being counted as
    "for each Energy attached to this Pokemon" -- every typed scaler in the
    pool over-counted by exactly the off-type Energy attached, which
    silently inflates any deck running a second Energy type. Azumarill ex
    read as 220 where the card says 140.
    """
    m = _TYPED_ENERGY_RE.search(clause or "")
    want = m.group(1).capitalize() if m else None
    n = 0
    for s in spots:
        if s is None:
            continue
        if want is None:
            n += s.energy_count()
        else:
            n += sum(1 for prov in s.energy if want in prov)
    return n


_BENCH_FILTERS = (
    ("that has any damage counters on it", lambda s: s.damage > 0),
    ("that has damage counters on it", lambda s: s.damage > 0),
    ("that has any energy attached", lambda s: s.energy_count() > 0),
    ("that has a pok\u00e9mon tool attached", lambda s: getattr(s, "tool", None)),
)


def _bench_matching(clause, spots):
    """Bench count, honouring a trailing "that has ..." filter.

    Gourgeist ex's Horrifying Rondo pays per Benched Pokemon *that has any
    damage counters on it*; the count ignored the filter and paid for the
    whole Bench.
    """
    c = (clause or "").lower()
    for phrase, pred in _BENCH_FILTERS:
        if phrase in c:
            return sum(1 for s in spots if s is not None and pred(s))
    return len([s for s in spots if s is not None])


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
    # "Your opponent reveals their hand. This attack does 50 damage for
    # each Trainer card you find there." -- "there" is the revealed hand.
    if "you find there" in c:
        kinds = {"trainer": ("Item", "Supporter", "Stadium", "Tool"),
                 "item": ("Item",), "supporter": ("Supporter",),
                 "pok": ("Pokemon",), "energy": ("Energy",)}
        for word, want in kinds.items():
            if word in c:
                if _RESOLVING[0]:
                    return sum(1 for k, _ in opp.hand if k in want)
                # Before the reveal: the hand's size times the share of
                # such cards among everything of theirs we can't see.
                pool = (list(opp.deck) + list(opp.hand)
                        + list(getattr(opp, "prize_cards", []) or []))
                return round(len(opp.hand) *
                             _expected_over(pool, lambda x: x[0] in want))
        return len(opp.hand)
    if "benched pok" in c and "both yours and your opponent" in c:
        return _bench_matching(c, list(pl.bench) + list(opp.bench))
    if "your opponent's benched pok" in c:
        return _bench_matching(c, opp.bench)
    if "your benched pok" in c:
        return _bench_matching(c, pl.bench)
    if "energy attached to your opponent's active" in c:
        return _energy_matching(c, [opp.active]) if opp and opp.active else 0
    # "attached to all of your Pokemon" counts the whole board, not the
    # Active -- Hydrapple ex's Syrup Storm and Mega Gardevoir ex's Mega
    # Symphonia are both board-wide and were scoring base damage only.
    # Checked before the Active-only clause, which "to all of your Pokemon"
    # would otherwise never reach.
    if "energy attached to all of your pok" in c:
        return _energy_matching(c, ([pl.active] if pl.active else []) + list(pl.bench))
    if "energy attached to this pok" in c:
        return _energy_matching(c, [spot])
    # Azelf's Neurokinesis and Trevenant's Overwhelming Pain count the
    # WHOLE opposing board, not just the Active -- which is the entire
    # reason they pair with a spread attack. Checked before the Active-only
    # clause below, which would otherwise never be reached for this wording
    # but is the narrower reading either way.
    if "damage counter on all of your opponent's pok" in c:
        spots = ([opp.active] if opp.active else []) + list(opp.bench)
        return sum(s.damage // 10 for s in spots)
    if "damage counter on your opponent's active" in c:
        return (opp.active.damage // 10) if opp.active else 0
    # "does 30 damage to 1 of your opponent's Pokemon for each damage
    # counter on THAT POKEMON" -- Greninja ex 30C's Stealthy Slash. "That
    # Pokemon" is whichever one the attack chose; the engine resolves
    # damage against the Active, so that is the one this counts. The Bench
    # reading is the card's real power and is NOT modelled, so this is a
    # floor on the attack, never an overstatement.
    # "100 damage for each Special Condition affecting your opponent's
    # Active Pokemon" -- Cradily's Miasma Wind and Team Rocket's Muk's
    # Hazardous Venom, both of which were scoring a flat 100 because no
    # clause rule counted conditions. Capped in practice at three by the
    # Asleep/Confused/Paralyzed exclusivity AE.apply_condition enforces.
    if "special condition affecting your opponent's active" in c:
        return len(opp.active.conditions) if opp and opp.active else 0
    if "damage counter on that pok" in c:
        return (opp.active.damage // 10) if opp and opp.active else 0
    if "damage counter on this pok" in c:
        return spot.damage // 10
    if "prize card your opponent has taken" in c:
        return STARTING_PRIZES - opp.prizes
    if "prize card you have taken" in c:
        return STARTING_PRIZES - pl.prizes
    # Energy counted somewhere other than one Pokemon.
    if "energy attached to all of your opponent's pok" in c:
        return _energy_matching(
            c, ([opp.active] if opp.active else []) + list(opp.bench))
    if "energy attached to both active pok" in c:
        return _energy_matching(c, [pl.active, opp.active if opp else None])
    if "energy card in your discard pile" in c:
        return sum(1 for x in pl.discard if "energy" in str(x).lower())
    if "energy card in your opponent's discard pile" in c:
        return sum(1 for x in opp.discard if "energy" in str(x).lower())
    # "for each Stage 2 Pokemon on your Bench" and friends -- a stage
    # filter on a Bench count, which the plain Bench clauses above do not
    # reach because the wording puts the filter first.
    m = _re.search(r"(basic|stage 1|stage 2) pok[eé]mon on your bench", c)
    if m:
        want = m.group(1).title().replace("Stage 1", "Stage 1")
        return sum(1 for b in pl.bench
                   if (pl.POKEMON.get(b.name) or {}).get("stage") == want)
    # "for each of your opponent's Pokemon ex in play". Checked before the
    # generic "of your <family> Pokemon in play" rule below, which would
    # otherwise read "opponent's" as a name fragment and count MY board.
    if "opponent's pok" in c and "in play" in c:
        spots = ([opp.active] if opp.active else []) + list(opp.bench)
        if "pok\u00e9mon ex" in c or "pokemon ex" in c:
            return sum(1 for sp in spots
                       if (opp.POKEMON.get(sp.name) or {}).get("prize_value", 1) >= 2)
        return len(spots)
    # "for each of your <A> and <B> in play" -- Beedrill ex counts both its
    # own printings, which is a name list rather than a family word.
    m = _re.search(r"of your ([\w'’ ]+?) and ([\w'’ ]+?) in play", c)
    if m:
        names = pl.in_play_names()
        a, b = m.group(1).strip(), m.group(2).strip()
        return sum(1 for n in names
                   if n.lower() == a or n.lower() == b)
    # "for each of your Pokemon that has \"Tauros\" in its name" -- a NAME
    # fragment in quotes rather than a family word, optionally narrowed to
    # the ones carrying damage. Both of this shape's users are the Tauros
    # pair: Target Together flips one coin per named Pokemon in play, and
    # Raging Charge counts only the damaged ones. Checked BEFORE the generic
    # "of your <family> Pokemon in play" rule below, which matches the same
    # text with an empty family and would count the whole board.
    m = _re.search(
        r"of your pok[eé]mon(?: in play)? that has [\"“']([^\"”']+)[\"”'] in its name"
        r"(?P<dmg> that has any damage counters on it)?", c)
    if m:
        want = m.group(1).strip().lower()
        spots = ([spot] if spot else []) + [
            b for b in pl.bench if b is not spot]
        if pl.active is not None and pl.active is not spot:
            spots.append(pl.active)
        hits = [sp for sp in spots if want in sp.name.lower()]
        if m.group("dmg"):
            hits = [sp for sp in hits if sp.damage > 0]
        return len(hits)
    # Three shapes that returned None, so the attack scored its printed
    # base: Team Rocket's Porygon2 / Porygon-Z's R Command (Supporters with
    # "Team Rocket" in the discard), Team Rocket's Weezing's Explode Together
    # Now (Koffing or Weezing in play, BOTH sides), Dartrix's United Wings
    # (Pokemon in the discard that have the United Wings attack).
    m = _re.search(r"(supporter|item|trainer|pok[eé]mon) cards? that ha(?:s|ve) "
                   r"[\"“']([^\"”']+)[\"”'] in (?:its|their) name in your discard pile", c)
    if m:
        kind, frag = m.group(1), m.group(2).lower()
        kinds = {"supporter": ("Supporter",), "item": ("Item",),
                 "trainer": ("Supporter", "Item", "Tool", "Stadium")}.get(kind, ("Pokemon",))
        return sum(1 for x in pl.discard
                   if frag in str(x).lower() and _card_kind(pl, x) in kinds)
    m = _re.search(r"pok[eé]mon in play that ha(?:s|ve) [\"“']([^\"”']+)[\"”']"
                   r"(?: or [\"“']([^\"”']+)[\"”'])? in (?:its|their) name", c)
    if m:
        frags = [x.lower() for x in (m.group(1), m.group(2)) if x]
        names = list(pl.in_play_names())
        if "both yours and your opponent" in c and opp is not None:
            names += list(opp.in_play_names())
        return sum(1 for n in names if any(fr in n.lower() for fr in frags))
    m = _re.search(r"pok[eé]mon in your discard pile that ha(?:s|ve) the ([\w'’ -]+?) attack", c)
    if m:
        want = m.group(1).strip().lower()
        return sum(1 for x in pl.discard if any(
            a["name"].lower() == want for a in (pl.POKEMON.get(x) or {}).get("attacks", [])))
    # "flip a coin for each MAUSHOLD YOU HAVE IN PLAY" -- a bare card name
    # with no "Pokemon" in the phrase, which none of the rules above reach.
    m = _re.search(r"^([\w'’ -]+?) you have in play$", clause.strip(), _re.I)
    if m:
        want = m.group(1).strip().lower()
        return sum(1 for n in pl.in_play_names() if want in n.lower())
    # "for each of your <Family> Pokemon in play" / "of your Pokemon in play"
    m = _re.search(r"of your ([\w'’ -]*?)\s*pok[eé]mon in play", c)
    if m:
        fam = m.group(1).strip()
        names = pl.in_play_names()
        if not fam:
            return len(names)
        # "for each of your GRASS Pokemon in play" is a TYPE, not a name.
        # Matching it as a name substring meant Torterra ex's Forest March
        # counted zero Grass Pokemon on a board where Torterra ex itself is
        # the Grass Pokemon -- the attack scored 0 and the AI never used it.
        # Same for the stage words.
        if fam.capitalize() in ENERGY_TYPES:
            want = fam.capitalize()
            return sum(1 for n in names
                       if want in ((pl.POKEMON.get(n) or {}).get("types") or []))
        if fam.lower() in ("basic", "stage 1", "stage 2", "evolution"):
            want = fam.title()
            if want == "Evolution":
                return sum(1 for n in names
                           if (pl.POKEMON.get(n) or {}).get("stage") != "Basic")
            return sum(1 for n in names
                       if (pl.POKEMON.get(n) or {}).get("stage") == want)
        return sum(1 for n in names if fam.lower() in n.lower())
    return None


_REVEAL_TOP_RE = _re.compile(
    r"reveal the top (\d+) cards of your opponent's deck", _re.I)
_USE_AS_THIS_RE = _re.compile(r"use it as this attack", _re.I)
_SELF_TOP_COPY_RE = _re.compile(
    r"discard the top card of your deck.{0,90}?use it as this attack",
    _re.I | _re.S)
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

    Making that halving CONDITIONAL on the swing taking a Prize was tried
    and rejected: "lockaware" waived the penalty on a lethal swing, on the
    theory that a lock which buys a Prize has paid for itself. It scored
    -3.80 points over 1500 mirror games on each of the two decks that own
    a copy-attack, worse on both, and the diagnosis says why -- waiving
    the penalty makes the locking attack MORE attractive, so it was picked
    more often (4450 vs 4021 borrows) and spent MORE turns locked out (150
    vs 130), which is the opposite of the intent.
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
            score += attack_rider_value(pl, opp, a, spot)
            if _SELF_ATTACK_LOCK_RE.search(a.get("text") or ""):
                score /= POL.knob(pl, "self_lock_divisor")
            if score > best_score:
                best, best_score = a, score
    return best


def copied_attack(pl, opp, spot, text):
    """The actual attack dict a copy-attack is borrowing, or None.

    Copying an attack has to copy its RIDERS too, not just its damage
    number. Kyurem's Trifrost carries all of its damage in a rider (110 to
    three Pokemon), so a Slowking copying it scored zero -- the win
    condition of a top-meta deck resolving to nothing at all. Picking the
    borrowed attack once, here, lets both attack_damage and
    attack_side_effects work from the same choice.
    """
    # The guard belongs HERE, not around the callers: this function scores
    # candidate attacks with attack_value(), which routes back through
    # attack_rider_value() and into copied_attack() again. Guarding only
    # the recursive call left that inner path unbounded, and the field run
    # blew the stack on a deck holding two different copy-attacks.
    # spot can be None: attack_rider_value() has no attacker argument and
    # passes pl.active, and the Bench is sorted inside do_attack() at a
    # moment when the Active has just been Knocked Out. Without this the
    # borrowed attack was scored against a None attacker and the whole
    # field run died on an AttributeError.
    if spot is None or _COPY_DEPTH[0] >= _MAX_COPY_DEPTH:
        return None
    _COPY_DEPTH[0] += 1
    try:
        return _copied_attack_inner(pl, opp, spot, text)
    finally:
        _COPY_DEPTH[0] -= 1


def _copied_attack_inner(pl, opp, spot, text):
    if _COPY_OWN_BENCH_RE.search(text):
        return _best_borrowed(pl, opp, spot, text)
    if _COPY_DEFENDING_RE.search(text) and opp.active:
        best, val = None, -1
        for a in opp.POKEMON[opp.active.name]["attacks"]:
            v = attack_value(opp, pl, opp.active, a)
            if v > val:
                best, val = a, v
        return best
    if _SELF_TOP_COPY_RE.search(text):
        top = _visible_top(pl)
        if top is None:
            return None                   # unknown until it is discarded
        kind, name = top
        if kind != "Pokemon":
            return None
        info = pl.POKEMON.get(name) or {}
        if info.get("rule_box"):
            return None
        best, val = None, -1
        for a in info.get("attacks") or []:
            v = attack_value(pl, opp, spot, a)
            if v > val:
                best, val = a, v
        return best
    m = _REVEAL_TOP_RE.search(text)
    if m and _USE_AS_THIS_RE.search(text):
        depth = int(m.group(1))
        if not _RESOLVING[0]:
            return None                   # their deck is hidden until revealed
        top = opp.deck[-depth:]           # the top: draw() pops the end
        best, val = None, -1
        for kind, name in top:
            if kind != "Pokemon":
                continue
            for a in (opp.POKEMON.get(name) or {}).get("attacks") or []:
                v = attack_value(pl, opp, spot, a)
                if v > val:
                    best, val = a, v
        return best
    return None


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

    # "Discard the top card of your deck, and if that card is a Pokemon that
    # doesn't have a Rule Box, choose 1 of its attacks and use it as this
    # attack." -- Slowking's Seek Inspiration. It matched the copy-attack
    # regex and then neither branch below, so it fell through to a printed
    # damage of nothing: the whole win condition of a top-meta deck scored
    # 0. Kyurem is in that list to be COPIED, not cast, which is also why
    # check_energy_support flags Trifrost as uncastable there and is right
    # to but harmless.
    if _SELF_TOP_COPY_RE.search(text):
        def copy_dmg(card):
            kind, name = card
            info = pl.POKEMON.get(name) or {}
            if kind != "Pokemon" or info.get("rule_box"):
                return 0
            return max((attack_damage(pl, opp, spot, a, record=False)
                        for a in info.get("attacks") or []), default=0)
        top = _visible_top(pl)
        if top is not None:
            return copy_dmg(top)
        # Unseen: what the top card is worth on average. Reading the real
        # top let the pilot pick Seek Inspiration only when it would hit.
        return _expected_over(_unseen_own(pl), copy_dmg)

    m = _REVEAL_TOP_RE.search(text)
    if m and _USE_AS_THIS_RE.search(text):
        depth = int(m.group(1))

        def borrow_dmg(card):
            kind, name = card
            if kind != "Pokemon":
                return 0
            # Evaluate the borrowed attack from our own board's point of
            # view -- a scaling clause reads our state, not theirs.
            return max((attack_damage(pl, opp, spot, a, record=False)
                        for a in opp.POKEMON[name]["attacks"]), default=0)
        if _RESOLVING[0]:
            top = opp.deck[-depth:] if depth <= len(opp.deck) else list(opp.deck)
            return max((borrow_dmg(c) for c in top), default=0)
        # Unseen: the expected best of `depth` cards from what we can't see.
        pool = list(opp.deck) + list(opp.hand) + list(getattr(opp, "prize_cards", []) or [])
        return _expected_max(pool, borrow_dmg, depth)
    return None


# --------------------------------------------------------------------------
# "Discard N, and this attack does X damage for each card you discarded"
# --------------------------------------------------------------------------
# Eleven ex attacks in this pool -- Raging Bolt ex, Mega Charizard X ex,
# Scizor ex, Team Rocket's Mewtwo ex, Jolteon ex, Mega Clefable ex, Mega
# Diancie ex, Wugtrio ex and friends -- pay for their damage by discarding
# Energy they choose at attack time. Every one of them was scoring its
# PRINTED base and nothing else, so Raging Bolt ex read as a 70-damage
# attacker rather than a 350-damage one.
#
# The count has to be computed the same way in two places (valuation, which
# runs many times per turn and must not mutate anything, and execution,
# which must actually pay the cost) or the attack becomes free damage --
# which is exactly the bug Cursed Blast's self-KO had.

_DISCARDED_THIS_WAY_RE = _re.compile(r"you discarded in this way", _re.I)
_DISCARD_CLAUSE_RE = _re.compile(
    r"discard (?:up to |any amount of )?(all|\d+)?\s*"
    r"(?:(basic|special)\s+)?"
    r"(?:(grass|fire|water|lightning|psychic|fighting|darkness|metal|dragon|"
    r"fairy|colorless)\s+)?"
    r"energy(?:\s+cards?)?\s+from\s+"
    r"(?:among\s+)?(this pok[eé]mon|your hand|your benched pok[eé]mon|"
    r"your pok[eé]mon)", _re.I)
_DISCARD_DMG_RE = _re.compile(
    r"does (\d+) (more )?damage[^.]*?for each (?:card|energy card)", _re.I)


def _energy_type_of(name):
    """The type a Basic Energy card name provides, or None."""
    m = _re.match(r"(?:basic\s+)?(\w+) energy", (name or "").strip(), _re.I)
    return m.group(1).capitalize() if m else None


_MILL_SCALER_RE = _re.compile(
    r"discard the top (\d+|)\s*cards? of (?:your|each player'?s) deck", _re.I)
_MILL_DMG_RE = _re.compile(
    r"does (\d+) (more )?damage[^.]*?for each (?:(basic )?([a-z]+) )?"
    r"(?:energy )?card", _re.I)


_HAND_NAME_SCALER_RE = _re.compile(
    r"discard any number of (supporter|item|pok[eé]mon|trainer) cards? that "
    r"have \"([^\"]+)\" in their name from your hand", _re.I)


def hand_name_scaler_damage(pl, atk):
    """"Discard any number of Supporters with X in their name ... N each".

    Team Rocket's Honchkrow's Rocket Feathers, which scored a flat 60
    instead of 60 per card discarded.
    """
    text = atk.get("text") or ""
    if not _DISCARDED_THIS_WAY_RE.search(text):
        return None
    hm = _HAND_NAME_SCALER_RE.search(text)
    dm = _DISCARD_DMG_RE.search(text)
    if not hm or not dm:
        return None
    frag = hm.group(2).lower()
    n = sum(1 for k, name in pl.hand if frag in str(name).lower())
    base = atk["damage"] or 0
    return (base + int(dm.group(1)) * n) if dm.group(2) else int(dm.group(1)) * n


def mill_scaler_damage(pl, atk):
    """Damage from "discard the top N of your deck, X per <card> found".

    Five attacks in the pool score this way (Magcargo ex, Quagsire, Mega
    Abomasnow ex, Misty's Gyarados, Avalugg) and all of them read as their
    printed base. Counts the ACTUAL top N of the deck rather than guessing,
    so the number matches what the discard will really turn up.
    """
    text = atk.get("text") or ""
    if not _DISCARDED_THIS_WAY_RE.search(text):
        return None
    mm = _MILL_SCALER_RE.search(text)
    dm = _MILL_DMG_RE.search(text)
    if not mm or not dm:
        return None
    n = int(mm.group(1)) if mm.group(1) else 1   # "the top card" = 1
    want = (dm.group(4) or "").lower()
    def hit(card):
        kind, name = card
        if want and want not in ("card", "cards"):
            return 1 if want in str(name).lower() else 0
        return 1 if kind == "Energy" else 0
    if _RESOLVING[0]:
        hits = sum(hit(c) for c in pl.deck[-n:])      # the real top N
    else:
        # The pilot can't see its own top N: the expected count.
        hits = round(n * _expected_over(_unseen_own(pl), hit))
    per = int(dm.group(1))
    base = atk["damage"] or 0
    return (base + per * hits) if dm.group(2) else (per * hits)


def _discard_scaler(text):
    """(max_count, per_damage, is_bonus, where, etype, basic_only) or None."""
    if not _DISCARDED_THIS_WAY_RE.search(text or ""):
        return None
    dc = _DISCARD_CLAUSE_RE.search(text)
    dm = _DISCARD_DMG_RE.search(text)
    if not dc or not dm:
        return None
    # "Discard ALL Fire Energy from this Pokemon ... for each card you
    # discarded in this way" -- Heatran's Steel Burst and Galvantula's
    # Discharge. The clause accepted "up to N" and "any amount" but not
    # "all", so these got neither the scaling damage nor the cost charged.
    g = (dc.group(1) or "").lower()
    cap = 99 if g in ("", "all") else int(g)
    basic_only = (dc.group(2) or "").lower() == "basic"
    etype = dc.group(3).capitalize() if dc.group(3) else None
    where = dc.group(4).lower()
    return (cap, int(dm.group(1)), bool(dm.group(2)), where, etype, basic_only)


def _discard_candidates(pl, spot, where, etype, basic_only):
    """Energy that may be discarded, cheapest-to-lose first.

    Bench Energy is spent before the Active's, and the Active keeps enough
    to pay for an attack next turn -- otherwise the sim happily strips its
    own attacker bare every single turn, which no player would do.
    """
    out = []
    if "hand" in where:
        for i, (k, n) in enumerate(pl.hand):
            if k != "Energy":
                continue
            t = _energy_type_of(n)
            if etype and t != etype:
                continue
            if basic_only and "basic" not in n.lower() and t is None:
                continue
            out.append(("hand", i, n))
        return out

    spots = []
    if "this pok" in where:
        spots = [(spot, 0)]
    elif "benched" in where:
        spots = [(b, 0) for b in pl.bench]
    else:                                   # "your Pokemon" / "among your Pokemon"
        spots = [(b, 0) for b in pl.bench] + [(spot, 1)]
    for sp, is_active in spots:
        if sp is None:
            continue
        keep = 0
        if is_active:
            info = pl.POKEMON.get(sp.name) or {}
            costs = [len(a["cost"]) for a in info.get("attacks") or []]
            keep = min(costs) if costs else 0
        avail = list(range(len(sp.energy)))
        if etype:
            avail = [i for i in avail if etype in sp.energy[i]]
        drop = max(0, len(avail) - (len(sp.energy) - keep))
        if drop:
            avail = avail[:-drop] if drop < len(avail) else []
        for i in avail:
            out.append(("spot", sp, i))
    return out


def discard_scaler_damage(pl, spot, atk):
    """Damage this attack gets from what it CAN discard right now, or None."""
    parsed = _discard_scaler(atk.get("text") or "")
    if not parsed:
        return None
    cap, per, is_bonus, where, etype, basic_only = parsed
    n = min(cap, len(_discard_candidates(pl, spot, where, etype, basic_only)))
    base = atk["damage"] or 0
    return (base + per * n) if is_bonus else (per * n)


def pay_discard_scaler(pl, spot, atk, log):
    """Actually discard what discard_scaler_damage() was paid for."""
    parsed = _discard_scaler(atk.get("text") or "")
    if not parsed:
        return
    cap, per, is_bonus, where, etype, basic_only = parsed
    picks = _discard_candidates(pl, spot, where, etype, basic_only)[:cap]
    if not picks:
        return
    hand_idx = sorted((i for kind, i, _ in picks if kind == "hand"), reverse=True)
    for i in hand_idx:
        pl.discard.append(pl.hand[i][1])
        pl.hand.pop(i)
    by_spot = {}
    for kind, sp, i in picks:
        if kind == "spot":
            by_spot.setdefault(id(sp), (sp, []))[1].append(i)
    for sp, idxs in by_spot.values():
        for i in sorted(idxs, reverse=True):
            nm = AE.pop_energy(sp, i)
            if nm:
                pl.discard.append(nm)
                AE.note_attack_discard(pl, sp, nm)
    log.append(f"  {pl.name}: discards {len(picks)} for {atk['name']}")



_COPY_DEPTH = [0]
_MAX_COPY_DEPTH = 2


def _flip_damage(pl, opp, spot, atk, base, text):
    """Resolve only the coin-flip damage shapes, or None if none apply.

    Split out so Backtrack Badge can evaluate them twice and keep the
    better roll without re-running the whole damage model.
    """
    if _FLIP_ALL_OR_NOTHING_RE.search(text):
        odds = _attack_ir(atk).chance
        return base if random.random() < (odds if odds < 1.0 else 0.5) else 0
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
        return (int(m2.group(1)) if m2 else base) * heads
    m = _MORE_DMG_FLIP_RE.search(text)
    if m and not _FOR_EACH_RE.search(text):
        odds = _attack_ir(atk).chance
        if odds < 1.0:
            return base + (int(m.group(1)) if random.random() < odds else 0)
    return None


def attack_damage(pl, opp, spot, atk, record=True):
    """Best-effort damage for one attack in the current board state."""
    text = atk.get("text") or ""
    base = atk["damage"]

    # "During your next turn, this Pokemon's <named> attack does N more
    # damage" / "...'s base damage is N". Metagross's Meteor Mash and three
    # others build on themselves and none of them did.
    buff = getattr(spot, "next_turn_attack_buff", None)
    if buff and buff[0] and buff[0].lower() == (atk.get("name") or "").lower():
        base = buff[1] if buff[2] else (base or 0) + buff[1]

    # "If this Pokemon was damaged by an attack during your opponent's last
    # turn, this attack does THAT MUCH more damage." No number in the text
    # for the flat-bonus path to read; the number is on the board.
    if _REFLECT_DAMAGE_RE.search(text):
        base = (base or 0) + getattr(spot, "damage_taken_last_turn", 0)

    # "If <clause>, this attack's base damage is N."
    m = _BASE_DAMAGE_IS_RE.search(text)
    if m and opp is not None:
        eff = _attack_ir(atk)
        if not eff.conditions or AE.conditions_met(eff, pl, opp, spot, atk):
            base = int(m.group(1))

    # A copy-attack evaluates the attack it borrows, which can itself be a
    # copy-attack -- Team Rocket's Persian ex's Haughty Order reads the
    # opponent's DECK, and in a mirror that deck contains another Persian
    # ex, so it copied itself forever. Only a mirror (or two copier decks
    # meeting) reaches it, which is why the field never crashed and the
    # self-play harness did on its first run.
    if opp is not None and _USE_AS_THIS_RE.search(text):
        if _COPY_DEPTH[0] >= _MAX_COPY_DEPTH:
            return base or 0
        _COPY_DEPTH[0] += 1
        try:
            copied = _copied_attack_damage(pl, opp, spot, text)
        finally:
            _COPY_DEPTH[0] -= 1
        if copied is not None:
            return copied

    scaled = discard_scaler_damage(pl, spot, atk)
    if scaled is not None:
        return scaled
    milled = mill_scaler_damage(pl, atk)
    if milled is not None:
        return milled
    handed = hand_name_scaler_damage(pl, atk)
    if handed is not None:
        return handed

    # "If <condition>, this attack does N more damage" -- a flat bonus
    # gated on something the IR already parses as a condition. Dhelmise's
    # Vengeful Anchor is 30 that becomes 170 once four Hide 'n' Sneak
    # Pokemon are in the discard, and nothing was reading the clause.
    m = _COND_FLAT_BONUS_RE.search(text)
    if m and not _FOR_EACH_RE.search(text) and opp is not None:
        eff = _attack_ir(atk)
        if eff.conditions:
            return base + (int(m.group(1))
                           if AE.conditions_met(eff, pl, opp, spot, atk) else 0)

    # "Flip a coin. If heads, this attack does N more damage." The
    # conditional-bonus path below needs a parsed CONDITION to gate on and
    # a coin flip is not one, so these silently paid base damage. Now
    # actually flipped, at the odds parse_chance reports.
    m = _MORE_DMG_FLIP_RE.search(text)
    if m and not _FOR_EACH_RE.search(text):
        odds = _attack_ir(atk).chance
        if odds < 1.0:
            return base + (int(m.group(1)) if random.random() < odds else 0)

    # A requirement the board has to satisfy, or the attack is called off.
    # Checked before the flips so a card carrying both resolves the
    # requirement first.
    # Backtrack Badge lets a Colorless attacker re-flip its coins once and
    # keep the better result, so the whole flip block is evaluated twice.
    if (opp is not None and spot is not None
            and _FLIP_ANY_RE.search(text) and AE.query_reflip(pl, spot)):
        first = _flip_damage(pl, opp, spot, atk, base, text)
        second = _flip_damage(pl, opp, spot, atk, base, text)
        if first is not None and second is not None:
            return max(first, second)

    if opp is not None and _ATTACK_REQUIRES_RE.search(text):
        eff = _attack_ir(atk)
        if eff.conditions and not AE.conditions_met(eff, pl, opp, spot, atk):
            return 0

    # All-or-nothing flip: the whole attack is called off on tails. Checked
    # BEFORE the scaling flips below, because "flip 2 coins ... if either is
    # tails, this attack does nothing" matches _FLIP_N_RE too and would
    # otherwise be treated as a per-heads scaler.
    if _FLIP_ALL_OR_NOTHING_RE.search(text):
        odds = _attack_ir(atk).chance
        if odds >= 1.0:
            odds = 0.5
        return base if random.random() < odds else 0

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

    # "Flip a coin for each of your Pokemon that has X in its name. This
    # attack does 50 damage for each heads." The coin COUNT is itself a
    # board scaler, so neither _FLIP_N_RE (which wants a literal digit) nor
    # the generic "for each" block below reads it correctly -- the latter
    # finds the FLIP clause first and returns the all-heads figure, i.e.
    # exactly double the true mean.
    m = _FLIP_PER_EACH_RE.search(text)
    if m and "for each heads" in text.lower():
        n = _clause_count(m.group(1), pl, opp, spot)
        if n is not None:
            if AE.query_reflip(pl, spot):
                # Backtrack Badge re-flips the whole set once and keeps the
                # better result, which is the entire reason this deck plays it.
                a = sum(1 for _ in range(n) if random.random() < 0.5)
                b = sum(1 for _ in range(n) if random.random() < 0.5)
                heads = max(a, b)
            else:
                heads = sum(1 for _ in range(n) if random.random() < 0.5)
            # NOT _DOES_DMG_RE: that is "does N damage for each", and this
            # card says "does 50 damage TO THE CHOSEN POKEMON for each
            # heads". The interposed phrase breaks the adjacent match and
            # the per-heads figure silently fell back to base, which is 0
            # on this card -- so the attack dealt nothing at all.
            m2 = _PER_HEADS_DMG_RE.search(text) or _DOES_DMG_RE.search(text)
            per = int(m2.group(1)) if m2 else (base or 0)
            return per * heads
        elif record:
            UNSCORED_ATTACKS.add(f"{getattr(spot, 'name', '?')}/{atk['name']}")

    # "This attack does 130 damage. It ALSO does 10 damage to each of your
    # opponent's Benched Pokemon FOR EACH Prize card your opponent has
    # taken." The scaling clause belongs to the SECONDARY sentence; the
    # main damage is the printed base and the splash is a rider. Kyurem ex
    # and Palafin are the two cards in the pool shaped this way, and both
    # were being scored as base * count -- 130 x three Prizes is 390 for an
    # attack that hits the Active for 130.
    also = _ALSO_DOES_FOR_EACH_RE.search(text)
    if also and (not _FOR_EACH_RE.search(text[:also.start()])):
        return base

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
            # _DOES_DMG_RE wants "does N damage for each" adjacent. Cards
            # that name their target in between ("does 30 damage to 1 of
            # your opponent's Pokemon for each damage counter") broke the
            # match and fell through to base, which is 0 on those cards.
            m = _DOES_DMG_RE.search(text) or _DOES_DMG_LOOSE_RE.search(text)
            if m:                      # "does N damage for each X"
                return int(m.group(1)) * count
            if base:
                return base * count
        elif record:
            UNSCORED_ATTACKS.add(f"{getattr(spot, 'name', '?')}/{atk['name']}")
        return base

    # Flat damage-counter placement with no scaling clause.
    m = _COUNTERS_RE.search(text)
    if m and not base:
        # If the rider path is going to place these counters itself, this
        # function must return 0 or the Active is charged twice -- once as
        # attack damage (which also wrongly picks up Weakness, since
        # placing counters ignores Weakness and Resistance) and again as
        # counters. Returning the flat number here also skipped the
        # attack's own gate: Matcha Spin was dealing 40 at zero Hide 'n'
        # Sneak fuel, when it is supposed to do nothing at all below 6.
        eff = _attack_ir(atk)
        if not eff.unsupported and any(
                a.op is IR.Op.PLACE_COUNTERS and a.op in ATTACK_RIDER_OPS
                for a in eff.actions):
            return 0
        return int(m.group(1)) * 10

    # "This attack does N damage to 1 of your opponent's Pokemon" -- the
    # bench-snipe shape, which carries its number in the text rather than
    # in the damage field.
    m = _FLAT_DOES_RE.search(text)
    if m and not base:
        # Same trap as the counter branch above: now that the snipe shape
        # compiles to a rider that places the counters itself, returning
        # the number here as well charges the target twice -- and as
        # attack damage it would wrongly pick up Weakness, which the
        # card's own reminder text says does not apply on the Bench.
        eff = _attack_ir(atk)
        if not eff.unsupported and any(
                a.op is IR.Op.PLACE_COUNTERS and a.op in ATTACK_RIDER_OPS
                for a in eff.actions):
            return 0
        return int(m.group(1))

    if not base and text and record:
        UNSCORED_ATTACKS.add(f"{getattr(spot, 'name', '?')}/{atk['name']}")
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
    act_types = AE.query_types(defender, act)
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


def _expected_heads(flips, reflip):
    """Expected heads from `flips` coins, or from the better of two sets
    when a Tool lets you re-flip (Backtrack Badge)."""
    if flips <= 0:
        return 0.0
    if not reflip:
        return flips / 2.0
    from math import comb
    p = [comb(flips, k) / (2 ** flips) for k in range(flips + 1)]
    cdf, out, run = [], 0.0, 0.0
    for k in range(flips + 1):
        run += p[k]; cdf.append(run)
    for k in range(flips + 1):
        below = cdf[k - 1] if k else 0.0
        out += k * (cdf[k] ** 2 - below ** 2)
    return out


def attack_rider_value(pl, opp, atk, spot=None):
    """Damage-equivalent worth of an attack's side effects, right now.

    `spot` is the Pokemon that would be USING the attack. It used to be
    inferred as pl.active, which is right for the ordinary "what should my
    Active do" question and wrong everywhere else -- _ready_damage() asks
    this about each BENCHED Pokemon in turn while deciding who to promote,
    and it asks at a moment when the Active has just been Knocked Out and
    pl.active is None. So a copy-attack on the Bench was scored as if a
    different Pokemon (or nothing at all) were holding it, and a condition
    like "if this Pokemon is in the Active Spot" was checked against the
    wrong body. Defaults to pl.active so callers that mean the Active can
    stay as they are.

    Measured, because "obviously right" is not the same as "changes
    anything": paired against the unfixed engine on identical seeds, 44
    decks x 8 opponents x 100 games, mean -0.01 points, 95% CI [-0.08,
    +0.06], and only 8 of 44 decks moved at all. It is a correctness fix
    with no measurable effect on the field, which is what you would
    expect -- it only bites on a copy-attack or a conditional attack held
    by a BENCHED Pokemon. Kept because the next such attack should not
    have to rediscover it.
    """
    text = atk.get("text") or ""
    if not text or opp is None or not opp.active:
        return 0
    if spot is None:
        spot = pl.active
    # A copy-attack is worth what the attack it borrows is worth. Without
    # this the AI never CHOSE one: Slowking's Seek Inspiration resolves a
    # copied Trifrost for 330 across three Pokemon and still scored zero,
    # so it was passed over for a 120-damage Super Psy Bolt every time.
    if _USE_AS_THIS_RE.search(text):
        # `borrowed is not atk` only stops a DIRECT self-copy. Two copy
        # attacks pointed at each other (Zoroark's Foul Play into an
        # opposing copier) recurse forever, and copied_attack's own depth
        # guard cannot see it: that guard is released in a `finally` before
        # this function recurses, so the counter is back to zero every time.
        # Hold the depth across the recursive call, exactly as attack_damage
        # already does. This crashed a 192-job shard with RecursionError.
        if _COPY_DEPTH[0] >= _MAX_COPY_DEPTH:
            return 0
        if _SELF_TOP_COPY_RE.search(text) and _visible_top(pl) is None:
            # Seek Inspiration with the top unseen: the average rider over
            # what the top card could be.
            def rv(card):
                kind, name = card
                info = pl.POKEMON.get(name) or {}
                if kind != "Pokemon" or info.get("rule_box"):
                    return 0
                b = max(info.get("attacks") or [],
                        key=lambda a: attack_value(pl, opp, spot, a), default=None)
                return attack_rider_value(pl, opp, b, spot) if b else 0
            _COPY_DEPTH[0] += 1
            try:
                return _expected_over(_unseen_own(pl), rv)
            finally:
                _COPY_DEPTH[0] -= 1
        borrowed = copied_attack(pl, opp, spot, text)
        if borrowed is not None and borrowed is not atk:
            _COPY_DEPTH[0] += 1
            try:
                return attack_rider_value(pl, opp, borrowed, spot)
            finally:
                _COPY_DEPTH[0] -= 1
    eff = _attack_ir(atk)
    if eff.unsupported:
        return 0
    if eff.conditions and not AE.conditions_met(eff, pl, opp, spot):
        return 0
    value = 0
    for act in eff.actions:
        if act.op == IR.Op.SWAP_FROM_DECK and spot is not None:
            # Surprisingly Transform: worth what the Pokemon it becomes hits
            # for next turn, times the chance of the flip (Backtrack Badge
            # flips a tails again), halved for the turn it waits.
            cands = sorted({n for k, n in pl.deck if k == "Pokemon" and n != spot.name})
            if cands:
                pick = _transform_pick(pl, opp, spot, cands)
                tmp = _clone_spot(spot)
                tmp.name = pick
                nxt = max((min(attack_value(pl, opp, tmp, a), 10 ** 4)
                           for a in pl.POKEMON[pick]["attacks"]), default=0)
                p = getattr(eff, "chance", 1.0)
                if AE.query_reflip(pl, spot):
                    p = 1 - (1 - p) ** 2
                value += 0.5 * p * max(nxt, 1)
            continue
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
            # "for each heads" mills act.amount PER HEADS, with one coin per
            # Maushold in play. Pricing it at the flat act.amount valued a
            # full board's 5.1 cards at 2, so the greedy pilot preferred
            # Pound's 40 damage and used the deck-out attack 3.5 times in a
            # 21-turn game. The executor already scales the mill itself;
            # this is the valuation catching up.
            per = (act.filter or {}).get("per_heads")
            n = (act.amount or 1)
            if per:
                flips = _clause_count(per, pl, opp, spot)
                n = n * _expected_heads(flips or 0, AE.query_reflip(pl, spot))
            value += n / left * 6 * 250
        elif act.op == IR.Op.DISCARD_FROM_OPPONENT:
            value += 10 * (act.amount or 1)
        elif act.op == IR.Op.DAMAGE_TO_HP_THRESHOLD:
            # Worth exactly the counters it would place, which on a big
            # Active is the largest single hit in the pool.
            spots = ([opp.active] if act.target is IR.Target.OPP_ACTIVE
                     else list(opp.bench))
            for sp in spots:
                if sp is None:
                    continue
                hp = (opp.POKEMON.get(sp.name) or {}).get("hp") or 0
                value += max(0, max(0, hp - (act.amount or 0)) - sp.damage)
        elif act.op == IR.Op.CONDITIONAL_KO:
            for victim in conditional_ko_targets(pl, opp, atk):
                # Worth the whole Pokemon: it dies regardless of HP.
                value += opp.POKEMON.get(victim.name, {}).get("hp", 200)
        elif act.op == IR.Op.DEVOLVE:
            # Espeon ex's Amazez had no price at all, so it scored 0 beside
            # a 160-damage alternative and was never chosen in 120 games.
            # Devolving is worth the Stage it removes: the card goes back to
            # hand, the HP drops, and any excess damage carries over.
            targets = ([opp.active] if act.target is IR.Target.OPP_ACTIVE
                       else opp.in_play())
            hit = [t for t in targets if t is not None
                   and (opp.POKEMON.get(t.name) or {}).get("evolves_from")]
            if act.amount and act.amount < 99:
                hit = sorted(hit, key=lambda t:
                             -((opp.POKEMON.get(t.name) or {}).get("hp") or 0)
                             )[:act.amount]
            for t in hit:
                info = opp.POKEMON.get(t.name) or {}
                prev = M.info_named(opp.POKEMON, info.get("evolves_from")) or {}
                value += max(0, (info.get("hp") or 0) - (prev.get("hp") or 0))
        elif act.op == IR.Op.PLACE_COUNTERS and act.target in (
                IR.Target.OPP_ANY, IR.Target.OPP_ALL, IR.Target.OPP_BENCHED):
            per = act.filter.get("per_discard_card")
            if per:
                # Re-Brew is worth whatever fuel is sitting in the discard
                # right now -- zero on an empty pile, 100+ on a loaded one.
                want = per.replace("basic ", "").strip()
                fuel = sum(1 for c in pl.discard if want in c.lower())
                value += (act.amount or 0) * 10 * fuel
            elif act.target is IR.Target.OPP_ALL:
                # A board-wide spread is worth what it actually places:
                # 4 counters on each of six Pokemon is 240, not 40. Pricing
                # it as a single target is what kept the AI from ever
                # setting up its own payoff.
                spots = ([opp.active] if opp.active else []) + list(opp.bench)
                # A per-target coin flip is worth its expectation, not its
                # ceiling. Mega Zygarde ex's Nullifying Zero priced at the
                # ceiling would be chosen over a guaranteed Knock Out.
                odds = act.filter.get("chance_each", 1.0)
                value += int((act.amount or 0) * 10 * max(len(spots), 1) * odds)
            else:
                value += (act.amount or 0) * 10 * act.filter.get("targets", 1)
        elif act.op == IR.Op.MULTIPLY_COUNTERS:
            # Worth exactly the damage it would add, which is zero on a
            # clean board and enormous on a spread one. Pricing it flat
            # would have the AI use it turn one and never again.
            spots = ([opp.active] if opp.active else []) + list(opp.bench)
            if act.filter.get("targets"):
                spots = sorted(spots, key=lambda s: -s.damage)[:act.filter["targets"]]
            value += sum(s.damage * ((act.amount or 2) - 1) for s in spots)
        elif act.op == IR.Op.MOVE_COUNTERS:
            value += 20
        elif act.op == IR.Op.SEARCH_TO_BENCH:
            # Worth something only while there is Bench room to fill.
            room = max(0, 5 - len(pl.bench))
            value += 35 * min(act.amount or 1, room)
        # A3. The setup riders had no price at all, so a 0-damage attack
        # that accelerated Energy or dug for a piece scored zero and the
        # AI would never spend a turn on it -- the single clearest reason
        # this simulator could not pilot a deck that has to set up before
        # it can threaten anything.
        elif act.op == IR.Op.ATTACH_ENERGY:
            # An Energy attach is roughly a turn of tempo, and worth more
            # while the Active is still short of its own attack cost.
            short = energy_shortfall(pl, pl.active) if pl.active else 0
            value += (45 if short else 20) * (act.amount or 1)
        elif act.op == IR.Op.SEARCH_TO_HAND:
            value += 25 * (act.amount or 1)
        elif act.op == IR.Op.DRAW:
            value += 15 * (act.amount or 1)
        elif act.op == IR.Op.FROM_DISCARD_TO_HAND:
            value += 20 * (act.amount or 1)
        elif act.op == IR.Op.SWITCH:
            value += 15
    # How much this pilot cares about a rider at all, and separately about
    # the ones that BUILD the board rather than affect the opponent. setup
    # pays well over the odds for the second kind; aggro discounts both.
    scale = POL.knob(pl, "rider_scale")
    if any(a.op in _SETUP_RIDER_OPS for a in eff.actions):
        scale = POL.knob(pl, "setup_scale")
    return int(value * scale * getattr(eff, "chance", 1.0))


# Riders that develop your own board rather than doing anything to the
# opponent. A deck that has to assemble something lives on these.
_SETUP_RIDER_OPS = {
    IR.Op.ATTACH_ENERGY, IR.Op.SEARCH_TO_BENCH, IR.Op.SEARCH_TO_HAND,
    IR.Op.DRAW, IR.Op.FROM_DISCARD_TO_HAND, IR.Op.RECOVER_TO_BENCH,
    IR.Op.HEAL, IR.Op.MOVE_ENERGY,
}


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


def conditional_ko_targets(pl, opp, atk):
    """EVERY opposing Pokemon this attack Knocks Out, not just one.

    Yveltal ex's Soul Destroyer Knocks Out *each* Pokemon at or below its
    HP line. Returning a single victim priced it as one Knock Out, so the
    AI always preferred Dark Strike's flat 210 and the attack was never
    used in 120 games.
    """
    eff = _attack_ir(atk)
    if eff.unsupported:
        return []
    out = []
    for act in eff.actions:
        if act.op != IR.Op.CONDITIONAL_KO:
            continue
        pool = ([opp.active] if act.target == IR.Target.OPP_ACTIVE
                else opp.in_play())
        pool = [p for p in pool if p is not None]
        cap = act.filter.get("max_remaining_hp")
        if cap is not None:
            out += [p for p in pool
                    if ((opp.POKEMON.get(p.name) or {}).get("hp") or 0)
                    - p.damage <= cap]
            continue
        one = conditional_ko_target(pl, opp, atk)
        if one is not None:
            out.append(one)
    seen, uniq = set(), []
    for p in out:
        if id(p) not in seen:
            seen.add(id(p))
            uniq.append(p)
    return uniq


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
        pool = ([opp.active] if act.target == IR.Target.OPP_ACTIVE
                else opp.in_play())
        pool = [p for p in pool if p is not None]
        # Mega Darkrai ex's Abyss Eye: any Special Condition on the Active
        # is the whole requirement.
        # Team Rocket's Moltres ex discards the Active outright; Alolan
        # Exeggutor ex Knocks Out a Basic on either side of its flip.
        if act.filter.get("unconditional"):
            return pool[0] if pool else None
        if act.filter.get("basic_only"):
            basics = [p for p in pool
                      if (opp.POKEMON.get(p.name) or {}).get("stage") == "Basic"]
            if basics:
                return max(basics, key=lambda p:
                           (opp.POKEMON.get(p.name) or {}).get("hp") or 0)
            continue
        if act.filter.get("needs_special_condition"):
            for p in pool:
                if getattr(p, "conditions", None):
                    return p
            continue
        # Yveltal ex's Soul Destroyer: everything already below a remaining
        # HP line. Returns the biggest such Pokemon -- the caller KOs one
        # target, so this at least stops the attack reading as 0 damage.
        cap = act.filter.get("max_remaining_hp")
        if cap is not None:
            hurt = [p for p in pool
                    if ((opp.POKEMON.get(p.name) or {}).get("hp") or 0)
                    - p.damage <= cap]
            if hurt:
                return max(hurt, key=lambda p:
                           (opp.POKEMON.get(p.name) or {}).get("hp") or 0)
            continue
        want = (act.filter.get("exact_counters") or 0) * 10
        for p in pool:
            if p.damage == want:
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


# A Prize is the actual currency of the game, and damage is only a means
# to one. Scoring an attack purely on damage made 170-into-a-330-HP-body
# rank equal to 170 that finishes something off, and made every setup play
# look worthless next to chip damage that took no Prizes.
KO_BONUS_PER_PRIZE = 120


def attack_ignores_effects(atk):
    """Does this attack's own text disclaim effects on the defender?"""
    eff = _attack_ir(atk)
    return (not eff.unsupported
            and any(a.op == IR.Op.IGNORE_OPPONENT_EFFECTS for a in eff.actions))


def attack_value(pl, opp, spot, atk):
    if opp is not None and attack_wins_game(pl, opp, spot, atk):
        return 10 ** 6            # nothing outranks winning on the spot
    dmg = attack_damage(pl, opp, spot, atk) if opp is not None else atk["damage"]
    value = dmg + attack_rider_value(pl, opp, atk, spot)
    if opp is not None and opp.active is not None:
        remaining = effective_hp(opp, opp.active) - opp.active.damage
        if dmg >= remaining:
            prize = opp.POKEMON[opp.active.name]["prize_value"]
            ko_bonus = POL.knob(pl, "ko_bonus_per_prize")
            # A Knock Out is worth more when it finishes more of the race.
            # prizewise scales it by how much of the six it actually takes;
            # every other pilot reads a flat rate, which is what the engine
            # has always done.
            if POL.knob(pl, "prize_liability") and getattr(pl, "prizes", 6) > 0:
                ko_bonus = ko_bonus * (1.0 + prize / max(pl.prizes, 1))
            value += ko_bonus * prize
            # Overkill past the Knock Out buys nothing, so a smaller
            # attack that still kills is preferred and the bigger one is
            # saved for something that needs it.
            value -= max(0, dmg - remaining) * POL.knob(pl, "overkill_penalty")
    # What this attacker is worth losing. A 3-Prize MEGA ex standing in the
    # Active Spot is a liability the greedy pilot never priced.
    liab = POL.knob(pl, "prize_liability")
    if liab and spot is not None:
        value -= liab * ((pl.POKEMON.get(spot.name) or {}).get("prize_value", 1) - 1)
    return value


def best_attack(pl, spot, only_payable=True, opp=None):
    info = pl.POKEMON[spot.name]
    best, best_val = None, -1
    # Relicanth's Memory Dive lends every evolved Pokemon its own
    # pre-evolutions' attacks. They are priced and paid for exactly like a
    # printed one.
    for atk in list(info["attacks"]) + AE.query_extra_attacks(pl, spot):
        if only_payable and not can_pay(effective_cost(pl, spot, atk["cost"], opp,
                                                       atk.get("name")),
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
    # An attack that pays MORE for Energy beyond its cost is not "paid up"
    # at its printed cost. Mega Excadrill ex's Maximum Drilling is 200 that
    # becomes 330 with 2 Energy beyond its MMM, and attachment stopped at
    # three -- so the bonus was reachable in principle and reached zero
    # times in 148 uses.
    for a in castable:
        for c in _attack_ir(a).conditions or []:
            if c.get("kind") == "self_extra_energy":
                need = max(need, len(a["cost"]) + c["count"])
    return max(0, need - spot.energy_count())


def attach_energy(pl, cards_by_name, log):
    idx = next((i for i, (k, n) in enumerate(pl.hand) if k == "Energy"), None)
    if idx is None:
        return
    forced = getattr(pl, "_forced_attach", "unset")
    if forced != "unset":
        # The lookahead pilot's pick: an index into in_play(), or None.
        pl._forced_attach = "unset"
        if forced is None:
            return
        spots = pl.in_play()
        if forced >= len(spots):
            return
        target = spots[forced]
        kind, name = pl.hand.pop(idx)
        target.energy.extend(energy_provisions(
            name, cards_by_name, (pl.POKEMON.get(target.name) or {}).get("stage")))
        target.energy_names.append(name)
        log.append(f"  {pl.name}: attaches {name} to {target.name}")
        energy_on_attach(pl, target, name, log)
        return
    target = None
    if (POL.knob(pl, "energy_to_active")
            and pl.active and energy_shortfall(pl, pl.active) > 0):
        target = pl.active
    else:
        # Rank EVERY body that still needs Energy by what it would hit for
        # once paid up -- the Active included.
        #
        # This branch first read pl.bench only, which for a pilot with
        # energy_to_active off meant the Active was never fed at all. That
        # is starvation, not a style, and it measured -12.58 points on 43
        # of 44 decks before anyone would have called it a design choice.
        pool = pl.in_play() if not POL.knob(pl, "energy_to_active") else pl.bench
        needy = [p for p in pool if energy_shortfall(pl, p) > 0]
        if needy:
            target = max(needy, key=lambda p: _potential_damage(pl, p))
    # A copy-attack deck has one attacker and a Bench of donors that never
    # attack. With 8 Energy, 38% of attachments went elsewhere -- mostly to
    # whatever a Knock Out had promoted (N's Zekrom, Yveltal, Fezandipiti
    # ex) -- while the Benched Zoroark ex stayed one short. Feed the copy
    # attacker first, the Active one, else the one closest to paid up.
    attackers = _copy_plan(pl)[0]
    if attackers and (target is None or target.name not in attackers):
        short = [p for p in pl.in_play()
                 if p.name in attackers and energy_shortfall(pl, p) > 0]
        if short:
            target = min(short, key=lambda p: (p is not pl.active,
                                               energy_shortfall(pl, p)))
    if target is None:
        return
    kind, name = pl.hand.pop(idx)
    target.energy.extend(energy_provisions(
        name, cards_by_name, (pl.POKEMON.get(target.name) or {}).get("stage")))
    target.energy_names.append(name)
    log.append(f"  {pl.name}: attaches {name} to {target.name}")
    energy_on_attach(pl, target, name, log)


_ON_ATTACH_RE = _re.compile(r"when you attach this card from your hand to (?:a |an )?"
                            r"(?:(\w+) )?pok[eé]mon", _re.I)


def energy_on_attach(pl, target, name, log):
    """"When you attach this card from your hand to a <Type> Pokemon, ..."

    Telepathic Psychic Energy (two Basic Psychic Pokemon onto the Bench,
    9 decklists) and Enriching Energy (draw 4) attached and did nothing
    else: nothing ran an Energy's on-attach effect.
    """
    if M.BASIC_ENERGY_RE.match(name):
        return
    eff = trainer_effect_ir(name)
    if eff is None:
        return
    m = _ON_ATTACH_RE.search(eff.text or "")
    if not m:
        return
    want = (m.group(1) or "").capitalize()
    if want in M.REAL_TYPES and want not in (pl.POKEMON.get(target.name) or {}).get("types", []):
        return
    opp = getattr(pl, "_opp_ref", None) or pl
    for a in eff.actions:
        if a.op in TRAINER_IR_OPS:
            AE.apply_action(a, pl, opp, target, log,
                            make_inplay=lambda n: InPlay(n, pl.round_no))


def _ready_damage(pl, opp, spot):
    """What this Pokemon is worth attacking with RIGHT NOW.

    A3. This ranked on raw damage, which meant the AI could not see the
    two things that decide who should be holding the Active Spot: that a
    smaller attack which actually Knocks Out is worth more than a bigger
    one that does not, and that a setup attack is worth something at all.
    A Benched Pokemon that could take a Prize this turn lost the
    comparison to whatever was already Active and hitting for more.
    """
    if not AE.query_attack_gate(pl, spot):
        return 0        # it cannot attack, so it is not an upgrade
    if spot.attack_locked or spot.attack_locked_by_opponent:
        return 0        # locked out of attacking this turn
    atk = best_attack(pl, spot, opp=opp)
    if not atk:
        return 0
    # Cap the outright-win sentinel so it cannot swamp the arithmetic
    # everywhere this feeds into.
    return min(attack_value(pl, opp, spot, atk), 10 ** 5)


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


# Tools whose whole effect is extra HP, discovered from the card text
# rather than hand-listed. Hero's Cape (+100) is the one that matters:
# it turns a 210 HP attacker into a 310 HP one, which is the difference
# between surviving a Mega ex hit and not.
_HP_TOOLS = None


def hp_tools():
    """Tool name -> HP it grants, discovered from card text.

    The card index is filled by run_game. Anything that reaches this before
    then -- a unit test driving do_attack directly, or any future caller
    outside the match loop -- used to build an EMPTY registry and cache it
    for the life of the process, silently switching off every HP Tool in
    the format. trainer_effect_ir already guards its cache the same way;
    this one did not, and a test that called do_attack without run_game
    found it.
    """
    global _HP_TOOLS
    if _HP_TOOLS is None:
        if not _CARDS_BY_NAME:
            _CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
        _HP_TOOLS = {}
        for name, card in _CARDS_BY_NAME.items():
            card = card[0] if isinstance(card, list) and card else card
            if not isinstance(card, dict):
                continue
            if "Pokémon Tool" not in (card.get("subtypes") or []):
                continue
            m = _re.search(r"gets \+(\d+) HP", " ".join(card.get("rules") or []))
            if m:
                _HP_TOOLS[name] = int(m.group(1))
    return _HP_TOOLS


_HOLDER_TYPE_RE = _re.compile(r"the (\w+) pok[eé]mon this card is attached to", _re.I)


def energy_passives(pl, spot, op=None):
    """Compiled actions of the Special Energy attached to `spot`, honouring
    "the <Type> Pokemon this card is attached to" and "on your Bench".

    Attached Special Energy was read for its type and nothing else:
    Growing Grass Energy's +20 HP, Magnetic Metal Energy's free retreat,
    Shadowy Darkness Energy's Bench shield and Legacy Energy's one Prize
    fewer all did nothing.
    """
    out = []
    types = (pl.POKEMON.get(spot.name) or {}).get("types") or []
    for nm in getattr(spot, "energy_names", None) or []:
        if M.BASIC_ENERGY_RE.match(nm):
            continue
        eff = trainer_effect_ir(nm)
        if eff is None:
            continue
        m = _HOLDER_TYPE_RE.search(eff.text or "")
        if m and m.group(1).capitalize() in M.REAL_TYPES and m.group(1).capitalize() not in types:
            continue
        if _re.search(r"is on your bench", eff.text or "", _re.I) and spot not in pl.bench:
            continue
        for a in eff.actions:
            if op is None or a.op == op:
                out.append((nm, a))
    return out


def _ko_prizes(owner, spot, taker, by_attack=True):
    """Prizes for Knocking Out `spot`: printed, +extra, the Prize-changing
    Abilities on either side (only the counter-KO path asked before), and
    Legacy Energy's one fewer -- once a game, for an attack's damage."""
    taken = (owner.POKEMON[spot.name]["prize_value"] + getattr(spot, "extra_prize", 0)
             + AE.query_prize_modifier(taker, owner, spot,
                                       taker.active if by_attack else None,
                                       by_attack))
    if by_attack and not getattr(owner, "_legacy_used", False):
        for nm, a in energy_passives(owner, spot, IR.Op.MODIFY_PRIZE):
            if a.target == IR.Target.OPPONENT and (a.amount or 0) < 0:
                owner._legacy_used = True
                taken += a.amount
                break
    return max(0, taken)


def effective_hp(pl, spot):
    """Printed HP plus whatever a Tool adds. Every Knock Out check goes
    through here -- reading printed HP directly meant an HP Tool was worth
    nothing, and the Tool was never even attached."""
    base = pl.POKEMON[spot.name]["hp"]
    return (base + hp_tools().get(getattr(spot, "tool", None), 0)
            + AE.query_hp_modifier(pl, spot)
            + sum(a.amount or 0 for _, a in energy_passives(pl, spot, IR.Op.MODIFY_HP)))


def _is_reflip_tool(pl, name):
    """Backtrack Badge, and only when the Active is the type it names."""
    eff = trainer_effect_ir(name)
    if eff is None or eff.unsupported or not pl.active:
        return False
    for act in eff.actions:
        if act.op is not IR.Op.REFLIP_COINS:
            continue
        want = (act.filter or {}).get("type")
        if want and want not in ((pl.POKEMON.get(pl.active.name) or {})
                                 .get("types") or []):
            return False
        return True
    return False


def attach_tools(pl, log):
    # Farfetch'd's Impromptu Carrier pulls a Tool out of the DECK, so the
    # hand loop below would never see it.
    if AE.query_tool_from_deck(pl, pl.active) and pl.active and not pl.active.tool:
        i = next((i for i, (k, n) in enumerate(pl.deck) if k == "Tool"), None)
        if i is not None:
            k, n = pl.deck.pop(i)
            pl.active.tool = n
            random.shuffle(pl.deck)
            log.append(f"  {pl.name}: attaches {n} from deck to {pl.active.name}")

    """Attach a Pokemon Tool to whoever will be holding the Active Spot.
    Only Tools carrying a modeled effect (retaliation) are attached -- any
    other Tool would be decoration the engine cannot honor."""
    for kind, name in list(pl.hand):
        if kind != "Tool":
            continue
        # Retreat and HP Tools were consulted elsewhere in this file but
        # never actually attached, so Air Balloon, Rescue Board and Hero's
        # Cape sat in hand for the whole game.
        if name in hp_tools() or name in RETREAT_TOOLS:
            # Rotom ex's Multi Adapter allows a second Tool; without it a
            # Pokemon holds exactly one.
            if not pl.active:
                continue
            if pl.active.tool and not AE.query_extra_tool_slots(pl, pl.active):
                continue
            pl.remove_from_hand(kind, name)
            pl.active.tool = name
            log.append(f"  {pl.name}: attaches {name} to {pl.active.name}")
            continue
        # A Tool whose only modelled effect is a coin re-flip. query_reflip
        # and _expected_heads were both written and wired, but nothing ever
        # put Backtrack Badge on a Pokemon, so the whole re-flip path was
        # unreachable: the Tool sat in hand for the entire game. It is the
        # one card in the pool with this shape, and it was already in two
        # decklists in this repo doing nothing at all.
        if name not in RETALIATE_CARDS and name not in DAMAGE_TOOLS:
            # Tools that fire when their holder is damaged and do something
            # other than put counters back. Without this they were never
            # attached, so the effect wired above could never fire.
            if name in on_damaged_tools():
                if not pl.active or (pl.active.tool
                                     and not AE.query_extra_tool_slots(pl, pl.active)):
                    continue
                pl.remove_from_hand(kind, name)
                pl.active.tool = name
                log.append(f"  {pl.name}: attaches {name} to {pl.active.name}")
                continue
            if _is_reflip_tool(pl, name):
                if not pl.active or (pl.active.tool
                                     and not AE.query_extra_tool_slots(pl, pl.active)):
                    continue
                pl.remove_from_hand(kind, name)
                pl.active.tool = name
                log.append(f"  {pl.name}: attaches {name} to {pl.active.name}")
            continue
        if name in DAMAGE_TOOLS:
            if not pl.active or pl.active.tool:
                continue
            # Brave Bangle pays out only on an attacker WITHOUT a Rule
            # Box, so putting it on the deck's lone ex is a dead card. The
            # same goes for a family-restricted band on the wrong Pokemon.
            t = DAMAGE_TOOLS[name]
            if t.get("holder_no_rule_box") and \
                    pl.POKEMON[pl.active.name]["prize_value"] != 1:
                continue
            fam = t.get("holder_family")
            if fam and fam.lower() not in pl.active.name.lower():
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


_ON_DAMAGED_TOOLS = None
_WHEN_DAMAGED_RE = _re.compile(
    r"is in the active spot and is damaged by an attack", _re.I)


def on_damaged_tools():
    """Tool name -> what it does when its holder is hit, read off the card.

    Derived from text rather than hand-listed, because the hand-kept
    DAMAGE_TOOLS dict beside this one had silently fallen two cards
    behind the pool. Damage-counter versions (Punk Helmet, Deluxe Bomb)
    are left to the existing retaliate path, which already handles them.
    """
    global _ON_DAMAGED_TOOLS
    if _ON_DAMAGED_TOOLS is None:
        if not _CARDS_BY_NAME:
            _CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
        _ON_DAMAGED_TOOLS = {}
        for name, card in _CARDS_BY_NAME.items():
            card = card[0] if isinstance(card, list) and card else card
            if not isinstance(card, dict):
                continue
            if "Pokémon Tool" not in (card.get("subtypes") or []):
                continue
            text = " ".join(card.get("rules") or [])
            if not _WHEN_DAMAGED_RE.search(text):
                continue
            m = _re.search(r"\bdraw (\d+) cards?", text, _re.I)
            if m:
                _ON_DAMAGED_TOOLS[name] = ("draw", int(m.group(1)))
                continue
            m = _re.search(r"the attacking pok[eé]mon is now (\w+)", text, _re.I)
            if m:
                _ON_DAMAGED_TOOLS[name] = ("condition", m.group(1).lower())
                continue
            if _re.search(r"move an energy from the attacking pok[eé]mon", text, _re.I):
                _ON_DAMAGED_TOOLS[name] = ("move_energy", 1)
    return _ON_DAMAGED_TOOLS


def fire_on_damaged_tool(pl, opp, dmg, log):
    """`opp` holds the Tool and has just been hit by `pl` for `dmg`."""
    if dmg <= 0 or not opp.active or AE.query_tools_disabled(opp, pl):
        return
    entry = on_damaged_tools().get(getattr(opp.active, "tool", None))
    if not entry:
        return
    kind, amount = entry
    if kind == "draw":
        opp.draw(amount)
        log.append(f"  {opp.name}: {opp.active.tool} -- draws {amount}")
    elif kind == "condition" and pl.active is not None:
        AE.apply_condition(pl.active, amount)
        log.append(f"  {opp.name}: {opp.active.tool} -- {pl.active.name} is now {amount}")
    elif kind == "move_energy" and pl.active is not None and pl.active.energy:
        # "to 1 of your opponent's Benched Pokemon" -- the attacker's own
        # Bench, from the point of view of the Pokemon wearing the Tool.
        if pl.bench:
            pl.bench[0].energy.append(pl.active.energy.pop())
            if getattr(pl.active, "energy_names", None):
                pl.bench[0].energy_names.append(pl.active.energy_names.pop())
            log.append(f"  {opp.name}: {opp.active.tool} -- moves an Energy off "
                       f"{pl.active.name}")



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
    if pl.active.retreat_locked:
        log.append(f"  {pl.name}: {pl.active.name} can't retreat this turn")
        return
    # A Paralyzed or Asleep Pokemon CANNOT RETREAT. The engine enforced the
    # "can't attack" half (CANNOT_ATTACK, read in condition_blocks_attack)
    # and let the same Pokemon walk away, which is half the point of
    # Paralysis: it pins the Active in place for a turn. Confused is NOT in
    # this set -- a Confused Pokemon may retreat normally. This is checked
    # AFTER retreat_locked so that a one-turn lock is still consumed here
    # and does not carry over past the Paralysis.
    stuck = pl.active.conditions & CANNOT_ATTACK
    if stuck:
        log.append(f"  {pl.name}: {pl.active.name} can't retreat "
                   f"({', '.join(sorted(stuck))})")
        return
    cost = retreat_of(pl, pl.active, opp)
    if pl.active.energy_count() < cost:
        return
    here = _ready_damage(pl, opp, pl.active)
    # Retreating costs Energy and a turn of tempo, so a Benched option has
    # to be better by more than a rounding error. Priced per Energy the
    # retreat actually discards, otherwise the AI thrashes between two
    # near-equal attackers and never develops either.
    margin = (POL.knob(pl, "retreat_per_energy") * max(cost, 0)
              + POL.knob(pl, "retreat_flat"))
    # v2: when the Active cannot attack AT ALL, the tempo argument for
    # staying put evaporates -- there is no tempo to lose. The flat margin
    # was still being applied, so with a retreat cost of 2 a Benched
    # attacker had to beat 70 damage before the AI would swap to it while
    # the Active stood there doing nothing. Measured: a Benched Pokemon
    # could have attacked on 25% of all idle turns.
    # Loosening this margin when the Active cannot attack looks obviously
    # right -- a Benched Pokemon could have attacked on 25% of all idle
    # turns -- and measured 3 points WORSE. Retreating discards Energy off
    # the Active, so trading a stalled-but-invested Active for a 20-damage
    # Basic throws the investment away. Free-swaps-only and a reduced
    # margin were also tried; neither beat this rule. Do not re-derive it.
    ready = [p for p in pl.bench if _ready_damage(pl, opp, p) > max(here, 0) + margin]
    target = max(ready, key=lambda p: _ready_damage(pl, opp, p)) if ready else None
    # Only pay the retreat cost if the upgrade is worth it.
    if target is not None and _ready_damage(pl, opp, target) <= here:
        target = None
    # The lookahead weighs staying against every retreat it can pay for,
    # through the opponent's reply -- the one decision greedy prices by
    # this turn's damage alone.
    if POL.knob(pl, "lookahead_samples") and pl.bench:
        options = [None] + list(range(len(pl.bench)))
        default = None if target is None else pl.bench.index(target)

        def apply(me, them, i):
            if i is not None:
                _do_retreat(me, me.bench[i], retreat_of(me, me.active, them), [])
        i = lookahead_pick(pl, opp, options, apply, PHASES.index("attack"), default)
        target = None if i is None else pl.bench[i]
    if target is None:
        return
    _do_retreat(pl, target, cost, log)


def _do_retreat(pl, target, cost, log):
    for _ in range(cost):
        nm = AE.pop_energy(pl.active)
        if nm:
            pl.discard.append(nm)
    pl.bench.remove(target)
    clear_conditions(pl.active, "retreated", log, pl.name)
    pl.bench.append(pl.active)
    pl.active = target
    pl.active.promoted_this_turn = True
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
        log.append(f"  {pl.name}: {pl.active.name} can't attack this turn")
        return False
    if pl.active.attack_locked_by_opponent:
        log.append(f"  {pl.name}: {pl.active.name} can't attack "
                   f"(locked by opponent)")
        return False
    # Standing attack gates -- Team Rocket's Mewtwo ex's Power Saver wants
    # 4 or more Team Rocket's Pokemon in play. Re-checked every turn, and
    # until now not checked at all: a deck with four of them in sixty
    # cards attacked freely 182 times in 120 games.
    if not AE.query_attack_gate(pl, pl.active):
        log.append(f"  {pl.name}: {pl.active.name} can't attack "
                   f"(requirement not met)")
        return False
    forced = getattr(pl, "_forced_attack", None)
    if forced is not None:
        atk = forced
        pl._forced_attack = None
    else:
        atk = best_attack(pl, pl.active, opp=opp)
        if atk and POL.knob(pl, "lookahead_samples") and not _LOOKAHEAD[0]:
            atk = lookahead_attack(pl, opp, atk) or atk
    if not atk:
        return False
    # Festival Lead (Dipplin, Seaking, Goldeen): "if Festival Grounds is in
    # play, this Pokemon may use an attack it has twice." The op compiled,
    # was catalogued as a known passive, and nothing ever asked for it, so
    # the whole archetype dealt exactly half its damage. Resolved as a
    # second pass through do_attack rather than doubling the number, so the
    # riders fire twice too and the second swing sees the board the first
    # one left behind -- which is what the card actually does.
    if not pl._attacking_twice and AE.query_attacks_twice(pl, pl.active, opp):
        pl._attacking_twice = True
        try:
            # do_attack's return value is "the game ended", NOT "the attack
            # happened" -- it returns False on the ordinary case of a hit
            # that did not take the last Prize. Reading it the other way
            # round and bailing on False suppressed the second swing in
            # every game, so mind the contract here.
            if do_attack(pl, opp, log):
                return True
            # The card's second sentence is explicit that a Knock Out does
            # not stop it: the opponent promotes (resolved inside the first
            # call) and is attacked into. Only an empty Active Spot on
            # either side ends it early.
            if pl.active is None or opp.active is None:
                return False
            return do_attack(pl, opp, log)
        finally:
            pl._attacking_twice = False
    # From here the attack RESOLVES: it may read the real top of a deck.
    # Before this point (choosing it) only what the player can see counts.
    _RESOLVING[0] = True
    # The alternate win condition resolves before damage and ends the game.
    if attack_wins_game(pl, opp, pl.active, atk):
        pl.prizes = 0
        log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} -- WINS THE GAME OUTRIGHT")
        return True
    for victim in conditional_ko_targets(pl, opp, atk):
        victim.damage = 10 ** 6      # forced Knock Out, HP is irrelevant
        log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} -- "
                   f"{victim.name} Knocked Out outright")

    # A gust attack switches FIRST and its damage goes to the new Active
    # ("Switch in 1 of your opponent's Benched Pokemon ... This attack does
    # 40 damage to the new Active Pokemon"). SWITCH was not a rider op at
    # all, so all 35 switching attacks -- Follow Me, Drag Off, Trading
    # Places, Teleportation Burst -- did nothing.
    for a in _attack_ir(atk).actions:
        if a.op == IR.Op.SWITCH and (a.filter or {}).get("gust") and opp.bench:
            AE.ATTACK_EFFECTS_BY[0] = pl
            try:
                AE.apply_action(a, pl, opp, pl.active, log)
            finally:
                AE.ATTACK_EFFECTS_BY[0] = None
    dmg = attack_damage(pl, opp, pl.active, atk)
    # A 0-damage attack is still worth using when it carries a rider --
    # Arbok's Panic Poison applies three Special Conditions and deals
    # nothing, and bailing on `dmg <= 0` skipped it even after the AI had
    # correctly chosen it.
    if dmg <= 0 and forced is None and attack_rider_value(pl, opp, atk, pl.active) <= 0:
        return False
    atk_types = AE.query_types(pl, pl.active, opp)
    defender = opp.POKEMON[opp.active.name]
    # An Ability can rewrite the defender's Weakness -- Lillie's Clefairy
    # ex's Fairy Zone makes every opposing Dragon weak to Psychic, which is
    # the whole reason it is teched into a Dragapult mirror.
    weak = AE.query_weakness_override(pl, opp, opp.active) or defender["weakness"]
    if (weak and weak in atk_types
            and not getattr(opp.active, "no_weakness", False)
            and not _IGNORES_WEAKNESS_RE.search(
                _borrowed_text(pl, opp, pl.active, atk))):
        dmg *= AE.query_weakness_multiplier(pl, opp)
    # Resistance. 369 cards in this pool carry one and it was not modelled
    # at all, so every attack into a resisted type dealt 30 more damage
    # than the game allows. Applied AFTER Weakness, as the rules order it,
    # and never below zero.
    resist = defender.get("resistance")
    if (resist and resist[0] in atk_types
            and not attack_ignores_effects(atk)
            and not _IGNORES_RESISTANCE_RE.search(
                _borrowed_text(pl, opp, pl.active, atk))):
        dmg = max(0, dmg - resist[1])
    # A debuff the DEFENDER put on this Pokemon last turn.
    pen = getattr(pl.active, "damage_penalty", 0)
    if pen:
        dmg = max(0, dmg - pen)
    # "During your next turn, the Defending Pokemon takes N more damage
    # from attacks" -- after Weakness and Resistance, as the card says.
    dmg += getattr(opp.active, "takes_more", 0)
    dmg += AE.query_damage_buff(pl, pl.active, opp)
    if pl.turn_buff_vs_ex and opp.POKEMON[opp.active.name]["prize_value"] >= 2:
        dmg += pl.turn_buff_vs_ex
    dmg += pl.turn_buff_any
    dmg += getattr(pl.active, "turn_buff", 0) or 0
    # Tools that add damage. Brave Bangle only pays out for an attacker
    # WITHOUT a Rule Box, which is the whole reason it fits a deck of
    # single-Prize attackers.
    tool = (None if AE.query_tools_disabled(pl, opp)
            else DAMAGE_TOOLS.get(getattr(pl.active, "tool", None)))
    if tool and opp.POKEMON[opp.active.name]["prize_value"] >= tool["min_prize"]:
        if damage_tool_applies(pl, tool, pl.active):
            dmg += tool["amount"]
    # Outright prevention (Sylveon's Safeguard, Cornerstone Stance,
    # Rabsca's Spherical Shield). The engine has had query_prevented since
    # Abilities were first wired in, and the game loop never called it --
    # so every damage-prevention wall in the pool did nothing at all, and
    # a deck built out of them measured as if it had no defence.
    # An attacker whose text says its damage "isn't affected by any effects
    # on your opponent's Active Pokemon" skips BOTH the walls and the
    # reduction -- that clause exists to answer exactly those cards.
    # The clause appears on Abilities (Walking Wake ex's Azure Seas) and
    # equally on the attack itself (Koraidon's Shred), so both have to be
    # asked -- the passive query only ever sees the Ability half.
    ignores = (AE.query_ignores_opponent_effects(pl, pl.active, opp)
               or attack_ignores_effects(atk))
    # A prevented hit deals nothing and the attack goes on (its other
    # effects still happen). This used to `return True` -- which is
    # do_attack's "the game ended" -- so every fully prevented attack WON
    # THE GAME for the attacker: every wall that worked lost on the spot.
    shield = None if ignores else AE.query_attack_shield(opp, opp.active, pl, pl.active)
    if not ignores and (AE.query_prevented(opp, opp.active, pl, pl.active)
                        or (shield and shield[0] == "prevent")):
        log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} -- "
                   f"all damage to {opp.active.name} prevented")
        dmg = 0
    reduction = 0 if ignores else damage_reduction_for(opp, opp.active, pl)
    if shield and shield[0] == "reduce":
        reduction += shield[1]
    if not ignores and opp.turn_shield:
        types = opp.POKEMON[opp.active.name].get("types") or []
        if not opp.turn_shield_type or opp.turn_shield_type in types:
            reduction += opp.turn_shield
    if reduction:
        dmg = max(0, dmg - reduction)
    opp.active.prev_damage = opp.active.damage
    opp.active.damage += dmg
    opp.active.damage_taken_last_turn = dmg
    # Counters put back on whatever just hit it, win or lose.
    back_counters = getattr(opp.active, "retaliate_counters", 0)
    if back_counters == -1:
        back_counters = dmg          # "equal to the damage done to this Pokemon"
    if back_counters and dmg > 0 and pl.active is not None:
        pl.active.damage += back_counters
        log.append(f"  {opp.name}: {opp.active.name} puts {back_counters} "
                   f"back on {pl.active.name}")
    # Tools that fire when their holder is damaged and do something other
    # than put counters back: Lucky Helmet draws, Handheld Fan strips an
    # Energy, Team Rocket's Hypnotizer puts the attacker to Sleep.
    fire_on_damaged_tool(pl, opp, dmg, log)
    log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} for {dmg}"
               f"{f' (-{reduction} reduced)' if reduction else ''}"
               f" -> {opp.active.name} at {opp.active.damage}/{opp.POKEMON[opp.active.name]['hp']}")

    pl.active.last_attack_used = atk["name"]
    # "Heal from this Pokemon the same amount of damage you did" is resolved
    # on the rider path, which is handed the attack but not its result.
    AE.DAMAGE_JUST_DEALT[0] = dmg

    if _SELF_ATTACK_LOCK_RE.search(_borrowed_text(pl, opp, pl.active, atk)):
        pl.active.attack_locked = 2

    attack_side_effects(pl, opp, atk, log)


    # Retaliation resolves even if the defender is Knocked Out by this hit.
    back = retaliation_from(opp, pl.active, pl) if dmg > 0 else 0
    if back:
        pl.active.damage += back
        log.append(f"  {opp.name}: retaliation puts {back} back on {pl.active.name}")
    if dmg > 0 and opp.active is not None:
        AE.on_damaged_riders(opp, pl, pl.active, log,
                             make_inplay=lambda n: InPlay(n, pl.round_no))
    if pl.active and pl.active.damage >= effective_hp(pl, pl.active):
        taken = pl.POKEMON[pl.active.name]["prize_value"]
        log.append(f"  {pl.name}: {pl.active.name} KO'd by retaliation (+{taken} to {opp.name})")
        AE.discard_pokemon(pl, pl.active)
        pl.lost_pokemon_names += pl.active.name.lower() + "|"
        pl.active = None
        pl.lost_pokemon_last_turn = True
        opp.prizes -= taken
        if opp.prizes <= 0:
            return True
        if pl.bench:
            pl.active = promote_from_bench(pl, opp)
            if pl.active:
                pl.active.promoted_this_turn = True
        else:
            return True

    if opp.active.damage >= effective_hp(opp, opp.active):
        # Gengar ex's Fainting Spell: the Knock Out may take the attacker
        # with it (resolved by the checkup's Knock Out at the turn's end).
        if AE.query_ko_attacker_on_ko(opp, opp.active, pl) and pl.active is not None:
            pl.active.damage = 10 ** 6
            log.append(f"  {opp.name}: {opp.active.name}'s Fainting Spell -- "
                       f"{pl.active.name} is Knocked Out")
        AE.salvage_energy_on_ko(opp, opp.active, log)
        taken = _ko_prizes(opp, opp.active, pl)
        log.append(f"  {pl.name}: KO on {opp.active.name} (+{taken} prizes)")
        if AE.query_returns_to_hand_on_ko(opp, opp.active):
            opp.hand.append(("Pokemon", opp.active.name))
            AE.discard_pokemon(opp, opp.active, keep_top=True)
        else:
            AE.discard_pokemon(opp, opp.active)
        opp.lost_pokemon_names += opp.active.name.lower() + "|"
        opp.active = None
        opp.lost_pokemon_last_turn = True
        pl.prizes -= taken
        if pl.prizes <= 0:
            return True
        if opp.bench:
            _promote_after_ko(opp, pl, log)
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
    IR.Op.SWAP_FROM_DECK,
    # "Switch this Pokemon with 1 of your Benched Pokemon" after the hit;
    # the gust half is resolved before the damage (see do_attack).
    IR.Op.SWITCH,
    # Found by listing every op that compiles on an attack and is neither
    # a rider nor read by the damage code (2026-09-24): 70 draw attacks
    # (Raging Bolt ex's Burst Roar -- discard the hand, draw 6 -- was a
    # 0-damage attack that did nothing), 42 "prevent all damage done to
    # this Pokemon during your opponent's next turn", 29 "takes N less",
    # 9 evolve-from-deck attacks.
    IR.Op.DRAW, IR.Op.DISCARD_FROM_SELF, IR.Op.SHUFFLE_HAND_INTO_DECK,
    IR.Op.EVOLVE_FROM_DECK, IR.Op.SHUFFLE_SELF_INTO_DECK,
    IR.Op.SEARCH_TO_TOP_OF_DECK, IR.Op.PREVENT_DAMAGE, IR.Op.REDUCE_DAMAGE,
    # Recoil. 75 attacks in the pool say "this Pokemon also does N
    # damage to itself" and none of them compiled, so every recoil
    # attacker in the format was swinging for free.
    IR.Op.SELF_DAMAGE,
    # 59 attacks pay for themselves by discarding their own Energy and
    # none of them did, so they fired at full price every turn.
    IR.Op.DISCARD_SELF_ENERGY,
    IR.Op.DEVOLVE,
    # Medicham ex's Chi-Atsu / Palossand ex's Barite Jail. These are
    # counters, not attack damage, so they belong on the rider path
    # (no Weakness, no damage reduction) -- and without this entry
    # they compiled, were valued, and then never executed.
    IR.Op.DAMAGE_TO_HP_THRESHOLD,
    IR.Op.APPLY_CONDITION,
    IR.Op.DISCARD_ENERGY_FROM_OPPONENT,
    IR.Op.MILL_OPPONENT,
    IR.Op.HEAL,
    IR.Op.DISCARD_FROM_OPPONENT,
    # Lampent's Spreading Light fills the Bench with its own Stage 1 --
    # a 0-damage setup attack that is the entire early game of a deck
    # built on the Stage 2 above it.
    IR.Op.SEARCH_TO_BENCH,
    # 58 attacks in the pool search a card into hand as their whole effect
    # (Noctowl's Talon Hunt, Ponyta's Charge Energy). They were compiled
    # and dropped because only the bench version was in this set.
    IR.Op.SEARCH_TO_HAND,
    IR.Op.FROM_DISCARD_TO_HAND,
    IR.Op.DISCARD_STADIUM,
    IR.Op.LOOK_AT_DECK,
    IR.Op.PLACE_COUNTERS,
    IR.Op.MOVE_COUNTERS,
    IR.Op.MULTIPLY_COUNTERS,
    IR.Op.LOCK,
    IR.Op.FORCE_SWITCH_OPPONENT,
    IR.Op.DISCARD_TOOL_FROM_OPPONENT,
    IR.Op.SELF_BENCH_DAMAGE,
    IR.Op.SELF_ENERGY_TO_HAND,
    IR.Op.WEAKEN_DEFENDER,
    IR.Op.HEAL_AS_DEALT,
    IR.Op.SELF_TO_HAND, IR.Op.SELF_TO_DECK, IR.Op.SELF_DISCARD,
    IR.Op.BENCH_TO_HAND, IR.Op.OPP_BENCH_TO_DECK, IR.Op.OPP_ENERGY_TO_HAND,
    IR.Op.DISCARD_TOOL_FROM_ALL_OPPONENT, IR.Op.RECOVER_TO_BENCH,
    IR.Op.KO_OUTRIGHT, IR.Op.SELF_KO, IR.Op.BUFF_NAMED_ATTACK_NEXT_TURN,
    IR.Op.DEFENDER_TAKES_MORE, IR.Op.CLEAR_CONDITIONS,
    IR.Op.BENCH_SPLASH, IR.Op.SELF_TAKES_MORE,
    IR.Op.DELAYED_DISCARD_DEFENDER, IR.Op.EXTRA_PRIZE_ON_KO,
    IR.Op.REMOVE_WEAKNESS, IR.Op.SET_WEAKNESS, IR.Op.WEAKNESS_MULTIPLIER,
    IR.Op.GRANT_BENCH_ATTACKS,
    IR.Op.MOVE_ENERGY,
    IR.Op.ATTACH_ENERGY, IR.Op.RETALIATE_COUNTERS,
    IR.Op.OPP_ATTACH_FROM_DISCARD,
}


def attack_side_effects(pl, opp, atk, log):
    """Apply an attack's non-damage rider effects."""
    text = atk.get("text") or ""
    if not text:
        return
    # A copy-attack resolves the attack it borrowed, riders and all.
    #
    # This recursion had no depth guard. "borrowed is not atk" catches only
    # a Pokemon copying its own attack; it does nothing about an A -> B -> A
    # cycle, which is what two copy-attacks facing each other produce.
    # Ethan's Sudowoodo's Try to Imitate borrows the Defending Pokemon's
    # attack, and if THAT is also a copy-attack it borrows straight back,
    # forever. copied_attack's own _COPY_DEPTH guard does not help: it is
    # decremented in its finally before this call recurses, so every level
    # started again from zero. The counter has to be held ACROSS the
    # recursive call, which is the same fix the copy-attack VALUATION path
    # needed earlier. Measured: 981 stack frames before Python gave up,
    # killing a 45,000-game run outright.
    if _USE_AS_THIS_RE.search(text):
        if _COPY_DEPTH[0] >= _MAX_COPY_DEPTH:
            return
        borrowed = copied_attack(pl, opp, pl.active, text)
        if borrowed is not None and borrowed is not atk:
            _COPY_DEPTH[0] += 1
            try:
                attack_side_effects(pl, opp, borrowed, log)
            finally:
                _COPY_DEPTH[0] -= 1
        # Seek Inspiration DISCARDS the card it copies -- whatever it was.
        # It never did, so one Kyurem left on top was copied every turn.
        if _SELF_TOP_COPY_RE.search(text) and pl.deck:
            gone = pl.deck.pop()
            pl.discard.append(gone[1])
            log.append(f"  {pl.name}: {atk['name']} discards {gone[1]} from the top")
        if borrowed is not None and borrowed is not atk:
            return

    # Pay for the damage discard_scaler_damage() already charged the
    # opponent for. Skipping this makes the attack free and repeatable.
    pay_discard_scaler(pl, pl.active, atk, log)
    mm = _MILL_SCALER_RE.search(text)
    if mm and _DISCARDED_THIS_WAY_RE.search(text):
        n = int(mm.group(1)) if mm.group(1) else 1
        for _ in range(min(n, len(pl.deck))):
            pl.discard.append(pl.deck.pop()[1])       # off the top
        log.append(f"  {pl.name}: mills {n} for {atk['name']}")
    hm = _HAND_NAME_SCALER_RE.search(text)
    if hm and _DISCARDED_THIS_WAY_RE.search(text):
        frag = hm.group(2).lower()
        keep = [(k, n2) for k, n2 in pl.hand if frag not in str(n2).lower()]
        gone = len(pl.hand) - len(keep)
        if gone:
            pl.discard.extend(n2 for k, n2 in pl.hand if frag in str(n2).lower())
            pl.hand[:] = keep
            log.append(f"  {pl.name}: discards {gone} named cards for {atk['name']}")
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
        # Backtrack Badge: a failed flip for this attack may be flipped
        # again. Only the damage coins honoured it, so Ditto's Surprisingly
        # Transform -- the reason the Badge is in the deck -- never did.
        if not (AE.query_reflip(pl, pl.active) and random.random() < eff.chance):
            return
        log.append(f"  {pl.name}: {pl.active.tool} -- flips again")
    AE.ATTACK_EFFECTS_BY[0] = pl
    try:
        for act in eff.actions:
            if act.op not in ATTACK_RIDER_OPS:
                continue
            if act.op == IR.Op.SWITCH and (act.filter or {}).get("gust"):
                continue          # resolved before the damage, in do_attack
            AE.apply_action(act, pl, opp, pl.active, log,
                            make_inplay=lambda n: InPlay(n, pl.round_no))
    finally:
        AE.ATTACK_EFFECTS_BY[0] = None


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
    """Pokemon Checkup, for BOTH players.

    The official rule is that a Pokemon Checkup happens between every turn
    and BOTH players resolve Special Conditions on their Active at it. This
    resolved only the Active of the player whose turn had just ended, so
    each Pokemon was checked once per ROUND instead of twice:

      * Poison and Burn dealt exactly HALF their real damage.
      * Asleep got half as many wake-up flips, so Sleep lasted twice as
        long as it should.

    Paralysis is the exception and stays on the turn-ending player only:
    it is cured "at the end of the affected player's next turn", which is
    this checkup and not the one in between.
    """
    _checkup_side(pl, opp, log, clear_paralysis=True)
    _checkup_side(opp, pl, log, clear_paralysis=False)


def _checkup_side(pl, opp, log, clear_paralysis):
    a = pl.active
    if not a or not getattr(a, "conditions", None):
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
    # Paralysis clears at the end of the affected player's next turn --
    # which is this player's own checkup, not the one in between.
    if clear_paralysis:
        a.conditions.discard("paralyzed")


# --------------------------------------------------------------------------
# Turn / game loop
# --------------------------------------------------------------------------

def extra_draws(a, b, mullA, mullB):
    """Mulligan compensation: the difference, drawn by the player who
    mulliganed less."""
    if mullB > mullA:
        a.draw(mullB - mullA)
    elif mullA > mullB:
        b.draw(mullA - mullB)


def opening_hand(pl):
    """Draw 7 (mulliganing to a Basic), then set the 6 Prizes aside.

    The Prize pile was tracked only as a counter -- both players drew from
    all 60 cards, so nothing was ever unreachable. In reality six cards
    are face down for the whole game, which means a deck is searching 53
    and any single copy is roughly 10% likely to be somewhere no search
    can reach. Leaving that out made every deck's setup look faster than
    it plays, and understated exactly the "I can't find my pieces" failure
    mode that single-copy tech cards actually have.
    """
    mulligans = 0
    while True:
        random.shuffle(pl.deck)
        pl.hand = []
        pl.draw(7)
        if pl.has_basic_in_hand():
            break
        pl.deck.extend(pl.hand)
        pl.hand = []
        mulligans += 1
        if mulligans > 20:
            break
    pl.prize_cards = [pl.deck.pop() for _ in range(STARTING_PRIZES) if pl.deck]
    return mulligans


def take_turn(pl, opp, turn, going_first, cards_by_name, log):
    pl.round_no = turn          # "during your first turn" is round 1 for both
    pl._opp_ref = opp
    pl._goes_first = going_first
    # "healed during this turn" is scoped to the turn it happened in.
    for _s in ([pl.active] if pl.active else []) + list(pl.bench):
        _s.healed_this_turn = False
    pl.supporter_played = False
    pl.turn_buff_vs_ex = 0
    pl.turn_buff_any = 0
    # The shield covers exactly the opponent turn that follows the one it
    # was played on. It is armed on play and spent here, one turn later.
    if pl._shield_armed:
        pl._shield_armed = False
    else:
        pl.turn_shield = 0
        pl.turn_shield_type = None
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
    pl._first_turn = first_turn
    pl._cards_by_name = cards_by_name
    # Rare Candy before the ordinary evolutions: evolving the Basic into
    # its Stage 1 first leaves nothing for the Candy to skip.
    if POL.knob(pl, "candy_first"):
        _candy_first(pl, opp, turn, log, first_turn)
    try_evolve(pl, opp, turn, log, first_turn)
    play_items(pl, opp, turn, log, first_turn)
    # The player going first may not play a Supporter on their first turn,
    # except one that says so (Carmine, Team Rocket's Proton). Nothing
    # enforced it: whoever went first got a free Supporter every game.
    hidden = [c for c in pl.hand if c[0] == "Supporter"
              and not _FIRST_TURN_SUPPORTER_RE.search(_card_text(c[1]))] \
        if first_turn else []
    for c in hidden:
        pl.hand.remove(c)
    try:
        if POL.knob(pl, "lookahead_samples") and not _LOOKAHEAD[0]:
            choose_supporter(pl, opp, turn, log)
        else:
            play_supporter(pl, opp, turn, log)
    finally:
        pl.hand.extend(hidden)
    return run_phases(pl, opp, log, 0)


_FIRST_TURN_SUPPORTER_RE = _re.compile(
    r"if you go first, you may use this card during your first turn", _re.I)


def _play_only(pl, opp, turn, log, name):
    """play_supporter with every other Supporter hidden: forces `name`
    (None: play no Supporter this turn)."""
    if name is None:
        return
    hidden = [c for c in pl.hand if c[0] == "Supporter" and c[1] != name]
    for c in hidden:
        pl.hand.remove(c)
    try:
        play_supporter(pl, opp, turn, log)
    finally:
        pl.hand.extend(hidden)


def choose_attach(pl, opp, log):
    """The lookahead pilot's Energy attachment: onto each Pokemon in play,
    or none, played out through the opponent's reply. The attach decision
    was the bottleneck for both the N's Zoroark and the Mew ex lists."""
    if not any(k == "Energy" for k, _ in pl.hand):
        return
    spots = pl.in_play()
    me, them = clone_state(pl, opp)
    _LOOKAHEAD[0] = True
    try:
        attach_energy(me, me._cards_by_name, [])
    finally:
        _LOOKAHEAD[0] = False
    before = [s.energy_count() for s in spots]
    after = [s.energy_count() for s in me.in_play()]
    greedy = next((i for i, (b, a) in enumerate(zip(before, after)) if a > b), None)
    options = list(range(len(spots))) + [None]

    def apply(m, th, i):
        m._forced_attach = i
        attach_energy(m, m._cards_by_name, [])
    pick = lookahead_pick(pl, opp, options, apply, PHASES.index("tools"), greedy)
    pl._forced_attach = pick
    attach_energy(pl, pl._cards_by_name, log)


def choose_supporter(pl, opp, turn, log):
    """The lookahead pilot's Supporter: each distinct Supporter in hand (and
    none) played out through the opponent's reply. Greedy's own pick --
    found by running greedy on a copy -- is the default."""
    names = sorted({n for k, n in pl.hand if k == "Supporter"})
    if pl.supporter_played or len(names) < 1:
        return play_supporter(pl, opp, turn, log)
    me, them = clone_state(pl, opp)
    _LOOKAHEAD[0] = True
    state = random.getstate()
    try:
        play_supporter(me, them, turn, [])
    finally:
        _LOOKAHEAD[0] = False
        random.setstate(state)
    greedy = next(iter(me.played_supporters_this_turn), None)
    options = names + [None]

    def apply(m, th, name):
        _play_only(m, th, turn, [], name)
    pick = lookahead_pick(pl, opp, options, apply, 0, greedy)
    _play_only(pl, opp, turn, log, pick)


# The rest of a turn after the Supporter, as named steps, so a lookahead can
# make a choice in a copy of the game and RESUME the turn from the step
# after it (a gust resumes at "abilities", a retreat at "attack").
PHASES = ("items", "bench", "abilities", "stadium", "sweep", "attach", "tools",
          "evolve", "retreat", "attack")


def run_phases(pl, opp, log, start):
    turn, first_turn = pl.round_no, pl._first_turn
    for ph in PHASES[start:]:
        if ph == "items":
            # Items that reached the hand through the Supporter (Petrel's
            # search, a draw) waited a whole turn: play_items ran only
            # before it.
            if POL.knob(pl, "items_after_supporter"):
                play_items(pl, opp, turn, log, first_turn)
        elif ph == "bench":
            # Basics that reached the hand this turn -- an Ultra Ball, a
            # draw Supporter -- sat there until the NEXT turn, because
            # play_basics only ran before the Items and the Supporter.
            if POL.knob(pl, "bench_after_supporter"):
                play_basics(pl, turn, log)
        elif ph == "abilities":
            use_abilities(pl, opp, turn, log)
        elif ph == "stadium":
            use_stadium(pl, log)
        elif ph == "sweep":
            sweep_knocked_out(pl, opp, log)
        elif ph == "attach":
            if POL.knob(pl, "lookahead_samples") and not _LOOKAHEAD[0]:
                choose_attach(pl, opp, log)
            else:
                attach_energy(pl, pl._cards_by_name, log)
        elif ph == "tools":
            attach_tools(pl, log)
        elif ph == "evolve":
            try_evolve(pl, opp, turn, log, first_turn)
        elif ph == "retreat":
            try_retreat(pl, opp, log)
        elif ph == "attack":
            # Meloetta ex's Debut Performance is the one card that may
            # attack on the very first turn.
            if not first_turn or AE.query_can_attack_first_turn(pl):
                # Academy at Night is "once during each player's turn" --
                # used last, when the Seek attacker is already Active,
                # rather than stacking a card nobody attacks with.
                _stadium_hand_to_top(pl, log)
                if do_attack(pl, opp, log):
                    return "win"
    return finish_turn(pl, opp, log)


# --------------------------------------------------------------------------
# One-turn lookahead (the "lookahead" pilot)
# --------------------------------------------------------------------------
#
# Greedy scores an attack by what it does THIS turn, so an attack whose whole
# value is the opponent's next turn -- "the Defending Pokemon can't attack",
# "can't retreat", Asleep, a gust into a stuck Pokemon -- is priced by a
# guessed constant or not at all. A Mew ex lock deck measured 17.5% under
# that pilot, and pricing the riders by hand measured at zero.
#
# This plays it out instead. For every attack the Active can pay for: copy
# both players, make that attack, finish the turn, play the opponent's whole
# reply with THEIR pilot, and score the position. Each candidate sees the
# same N seeds, and the real game's random state is restored afterwards, so
# the game itself is only changed by the choice made.

_LOOKAHEAD = [False]
_LOOKAHEAD_SEQ = [0]


def _position_value(pl, opp, ended):
    """Score a position for `pl`. `ended` is "win" / "loss" / None."""
    if ended == "win":
        return 1e6
    if ended == "loss":
        return -1e6
    v = 300.0 * ((STARTING_PRIZES - pl.prizes) - (STARTING_PRIZES - opp.prizes))

    def board(side):
        s = 0.0
        for p in side.in_play():
            info = side.POKEMON.get(p.name) or {}
            hp = effective_hp(side, p) or 1
            s += 120.0 * info.get("prize_value", 1) * min(1.0, p.damage / hp)
            s -= 15.0 * p.energy_count()
        return s
    v += board(opp) - board(pl)
    if _is_mill_deck(pl):
        v -= 30.0 * len(opp.deck)
    return v


def lookahead_pick(pl, opp, options, apply, resume, default):
    """The option whose position after the opponent's reply is best.

    `apply(me, them, option)` makes the choice in a copy of the game and
    returns "win" if that alone ends it. The turn then resumes at PHASES
    index `resume` (None: straight to the end of the turn), the opponent
    plays their whole reply with their own pilot, and the position is
    scored. Every option sees the same N seeds; the real game's random
    state is restored afterwards. Stays with `default` (greedy's choice)
    unless another option is better by more than lookahead_margin.
    """
    if len(options) < 2 or _LOOKAHEAD[0]:
        return default
    n = POL.knob(pl, "lookahead_samples")
    _LOOKAHEAD_SEQ[0] += 1
    base = _LOOKAHEAD_SEQ[0] * 7919
    state = random.getstate()
    _LOOKAHEAD[0] = True
    margin = POL.knob(pl, "lookahead_margin")
    totals = [0.0] * len(options)
    done = 0
    try:
        # Two samples first; the rest only if the options actually differ.
        # Most decisions are ties (every option plays out the same), and
        # paying the full N for those was most of the pilot's cost.
        for s in range(n):
            for k, opt in enumerate(options):
                random.seed(base + s)
                totals[k] += _simulate_from(pl, opp, opt, apply, resume)
            done = s + 1
            if done == min(2, n):
                avg = [x / done for x in totals]
                if max(avg) - min(avg) <= margin:
                    break
        scores = [x / done for x in totals]
    finally:
        _LOOKAHEAD[0] = False
        random.setstate(state)
    i = max(range(len(options)), key=lambda k: scores[k])
    d = options.index(default) if default in options else None
    if d is not None and scores[i] <= scores[d] + POL.knob(pl, "lookahead_margin"):
        return default
    return options[i]


def _self_switch_target(pl, opp, cands, optional):
    """Where "switch this Pokemon with 1 of your Benched Pokemon" goes.

    Mandatory: the healthiest body that can take the next hit. Optional
    ("you may"): only when the Active would be Knocked Out next turn and
    something worth no more Prizes can stand in for it.
    """
    if not cands:
        return None
    left = lambda p: effective_hp(pl, p) - p.damage
    prize = lambda p: pl.POKEMON.get(p.name, {}).get("prize_value", 1)
    best = max(cands, key=lambda p: (left(p), -prize(p)))
    if not optional:
        return best
    me = pl.active
    if me is None or opp.active is None:
        return None
    threat = _ready_damage(opp, pl, opp.active)
    if threat < left(me):
        return None
    if prize(best) > prize(me):
        return None
    return best


AE.SELF_SWITCH_TARGET = _self_switch_target


# Read-only per-deck tables the lookahead's copies share with the real game.
_SHARED_ATTRS = {"POKEMON", "EFFECTS", "_cards_by_name", "_copy_plan_cache"}


def _clone_spot(s):
    c = InPlay.__new__(InPlay)
    for k in InPlay.__slots__:
        if not hasattr(s, k):
            continue
        v = getattr(s, k)
        if isinstance(v, list):
            v = list(v)
        elif isinstance(v, set):
            v = set(v)
        elif isinstance(v, dict):
            v = dict(v)
        setattr(c, k, v)
    return c


def clone_state(pl, opp):
    """Copy both players for a lookahead. deepcopy was 55% of the pilot's
    time; this copies every container and re-clones every Pokemon in play,
    and shares only the static per-deck tables."""
    spots = {}

    def spot(s):
        if s is None:
            return None
        if id(s) not in spots:
            spots[id(s)] = _clone_spot(s)
        return spots[id(s)]

    out = []
    for side in (pl, opp):
        c = Player.__new__(Player)
        for k, v in side.__dict__.items():
            if k in _SHARED_ATTRS or k == "_opp_ref":
                pass
            elif k == "active":
                v = spot(v)
            elif k == "bench":
                v = [spot(s) for s in v]
            elif isinstance(v, list):
                v = list(v)
            elif isinstance(v, set):
                v = set(v)
            elif isinstance(v, dict):
                v = dict(v)
            c.__dict__[k] = v
        out.append(c)
    a, b = out
    if "_opp_ref" in pl.__dict__:
        a._opp_ref = b
    if "_opp_ref" in opp.__dict__:
        b._opp_ref = a
    return a, b


def _hide_information(me, them):
    """Deal the unknown cards afresh in a lookahead copy.

    The copy kept the real deck order and the opponent's real hand, so the
    lookahead played against the actual future: it knew every card either
    player would draw and what the opponent was holding. The pilot knows
    its own hand and nothing else: its deck and Prizes are reshuffled
    together, and the opponent's hand, deck and Prizes are pooled and
    redealt at their current sizes. Each sample draws a different deal
    (lookahead_pick seeds each sample)."""
    for side, hand_hidden in ((me, False), (them, True)):
        pool = list(side.deck) + list(getattr(side, "prize_cards", []) or [])
        nh = len(side.hand)
        if hand_hidden:
            pool += list(side.hand)
        random.shuffle(pool)
        np_ = len(getattr(side, "prize_cards", []) or [])
        if hand_hidden:
            side.hand = pool[:nh]
            pool = pool[nh:]
        side.prize_cards = pool[:np_]
        side.deck = pool[np_:]


def _simulate_from(pl, opp, opt, apply, resume):
    me, them = clone_state(pl, opp)
    _hide_information(me, them)
    log = []
    if resume == "promote":
        return _simulate_promotion(me, them, opt, apply, log)
    if apply(me, them, opt) == "win":
        return _position_value(me, them, "win")
    r = run_phases(me, them, log, resume) if resume is not None \
        else finish_turn(me, them, log)
    if r == "win":
        return _position_value(me, them, "win")
    if r in ("loss", "no_pokemon"):
        return _position_value(me, them, "loss")
    end_of_turn(me, log)
    rnd = me.round_no if getattr(me, "_goes_first", True) else me.round_no + 1
    them.lost_pokemon_last_turn_snapshot = them.lost_pokemon_last_turn
    r = take_turn(them, me, rnd, not getattr(me, "_goes_first", True),
                  me._cards_by_name, log)
    if r == "win":
        return _position_value(me, them, "loss")
    if r in ("loss", "no_pokemon", "deck_out"):
        return _position_value(me, them, "win")
    end_of_turn(them, log)
    return _position_value(me, them, None)


def _simulate_promotion(me, them, opt, apply, log):
    """`me` promotes during `them`'s turn: finish their turn, play mine,
    then their reply, and score the position for `me`."""
    apply(me, them, opt)
    r = finish_turn(them, me, log)
    if r == "win":
        return _position_value(me, them, "loss")
    if r in ("loss", "no_pokemon"):
        return _position_value(me, them, "win")
    end_of_turn(them, log)
    first = getattr(them, "_goes_first", True)
    cards = getattr(them, "_cards_by_name", None) or _CARDS_BY_NAME
    me.lost_pokemon_last_turn_snapshot = me.lost_pokemon_last_turn
    r = take_turn(me, them, them.round_no if first else them.round_no + 1,
                  not first, cards, log)
    if r == "win":
        return _position_value(me, them, "win")
    if r in ("loss", "no_pokemon", "deck_out"):
        return _position_value(me, them, "loss")
    end_of_turn(me, log)
    them.lost_pokemon_last_turn_snapshot = them.lost_pokemon_last_turn
    r = take_turn(them, me, them.round_no + 1, first, cards, log)
    if r == "win":
        return _position_value(me, them, "loss")
    if r in ("loss", "no_pokemon", "deck_out"):
        return _position_value(me, them, "win")
    end_of_turn(them, log)
    return _position_value(me, them, None)


def _gust_attack(atk):
    return any(a.op == IR.Op.SWITCH and (a.filter or {}).get("gust")
               for a in _attack_ir(atk).actions)


def lookahead_attack(pl, opp, greedy_pick):
    """Which attack -- and, for a gust attack, which target."""
    spot = pl.active
    cands, seen = [], set()
    for a in list(pl.POKEMON[spot.name]["attacks"]) + AE.query_extra_attacks(pl, spot):
        if a["name"] in seen or not can_pay(
                effective_cost(pl, spot, a["cost"], opp, a.get("name")), spot.energy):
            continue
        seen.add(a["name"])
        cands.append(a)
    # An option is (attack, gust target, self-switch target, transform
    # target). "unset" leaves a choice to the greedy rule; None declines an
    # optional switch.
    options = []
    for a in cands:
        gusts = list(range(len(opp.bench))) if _gust_attack(a) and opp.bench else [None]
        sw = _self_switch_of(a)
        if sw is not None and pl.bench:
            switches = list(range(len(pl.bench))) + ([None] if sw.get("optional") else [])
        else:
            switches = ["unset"]
        # Surprisingly Transform: which Pokemon from the deck it becomes.
        if any(x.op == IR.Op.SWAP_FROM_DECK for x in _attack_ir(a).actions):
            forms = sorted({n for k, n in pl.deck if k == "Pokemon" and n != spot.name}) or ["unset"]
        else:
            forms = ["unset"]
        options += [(a["name"], g, s, f) for g in gusts for s in switches for f in forms]
    by_name = {a["name"]: a for a in cands}
    greedy_form = "unset"
    if any(x.op == IR.Op.SWAP_FROM_DECK for x in _attack_ir(greedy_pick).actions):
        fc = sorted({n for k, n in pl.deck if k == "Pokemon" and n != spot.name})
        greedy_form = _transform_pick(pl, opp, spot, fc) if fc else "unset"
    default = next((o for o in options if o[0] == greedy_pick["name"]
                    and o[3] == greedy_form), None) or \
        next((o for o in options if o[0] == greedy_pick["name"]), None)

    def apply(me, them, opt):
        me._forced_attack = by_name[opt[0]]
        them._forced_gust = opt[1]
        me._forced_self_switch = opt[2]
        me._forced_transform = opt[3]
        return "win" if do_attack(me, them, []) else None
    pick = lookahead_pick(pl, opp, options, apply, None, default)
    if pick is None or pick == default:
        return greedy_pick
    opp._forced_gust = pick[1]
    pl._forced_self_switch = pick[2]
    pl._forced_transform = pick[3]
    return by_name[pick[0]]


def _self_switch_of(atk):
    for a in _attack_ir(atk).actions:
        if a.op == IR.Op.SWITCH and not (a.filter or {}).get("gust"):
            return a.filter or {}
    return None


def finish_turn(pl, opp, log):
    """Pokemon Checkup and the Knock Outs it causes -- the end of a turn."""
    AE.return_boomerangs(pl, log)
    opp._forced_gust = None
    pl._forced_self_switch = "unset"
    pl._forced_transform = "unset"
    pokemon_checkup(pl, opp, log)
    # Either Active can now die at checkup, since both resolve their
    # conditions there.
    for side, other, mine in ((pl, opp, True), (opp, pl, False)):
        if not (side.active and side.active.damage >= effective_hp(side, side.active)):
            continue
        taken = side.POKEMON[side.active.name]["prize_value"]
        log.append(f"  {side.name}: {side.active.name} KO'd at checkup "
                   f"(+{taken} to {other.name})")
        AE.discard_pokemon(side, side.active)
        side.lost_pokemon_names += side.active.name.lower() + "|"
        side.active = None
        side.lost_pokemon_last_turn = True
        other.prizes -= taken
        if other.prizes <= 0:
            return "loss" if mine else "win"
        if side.bench:
            side.active = promote_from_bench(side, other)
            if side.active:
                side.active.promoted_this_turn = True
        elif mine:
            return "no_pokemon"
        else:
            return "win"
    return None


def _gust_score(pl, opp, spot):
    """How good a Knock Out target this Pokemon is, if dragged up.

    A gust is one of the few genuinely strategic cards the AI holds, and
    it was picking the Benched Pokemon with the lowest remaining HP --
    which ignores the only two things that matter: whether the target can
    actually be Knocked Out this turn, and how many Prizes it is worth.
    Dragging up a 40 HP Basic to take one Prize, while a damaged two-Prize
    ex sits beside it, is the single most common way to lose a Prize race.
    """
    info = opp.POKEMON.get(spot.name) or {}
    left = effective_hp(opp, spot) - spot.damage
    best = 0
    if pl.active is not None:
        atk = best_attack(pl, pl.active, True, opp)
        if atk is not None:
            best = attack_damage(pl, opp, pl.active, atk, record=False)
            weak = info.get("weakness")
            if weak and weak in (pl.POKEMON[pl.active.name]["types"] or []):
                best *= AE.query_weakness_multiplier(pl, opp)
    can_ko = 1 if best >= left else 0
    return (can_ko, info.get("prize_value", 1) if can_ko else 0, -left)


def _is_mill_deck(pl):
    """Does this deck win by decking the opponent out? Three or more
    copies of Pokemon whose attack mills the opponent's deck."""
    cached = getattr(pl, "_mill_deck", None)
    if cached is not None:
        return cached
    names = ([n for k, n in pl.deck if k == "Pokemon"]
             + [n for k, n in pl.hand if k == "Pokemon"]
             + [p.name for p in pl.in_play()])
    millers = {n for n, info in pl.POKEMON.items()
               if any(a.op == IR.Op.MILL_OPPONENT
                      for atk in info["attacks"] for a in _attack_ir(atk).actions)}
    pl._mill_deck = sum(n in millers for n in names) >= 3
    return pl._mill_deck


def _millers(pl):
    """Names of this deck's Pokemon whose attack mills the opponent."""
    return {n for n, info in pl.POKEMON.items()
            if any(a.op == IR.Op.MILL_OPPONENT
                   for atk in info["attacks"] for a in _attack_ir(atk).actions)}


def _stuck(pl, opp, spot):
    """Would `spot`, as opp's Active, neither attack nor pay to retreat?"""
    if _ready_damage(opp, pl, spot) > 0:
        return False
    tax = 1 if pl.active is not None and pl.active.tool == "Gravity Gemstone" else 0
    return spot.energy_count() < retreat_of(opp, spot, pl) + tax


def choose_gust_target(pl, opp):
    """The Benched Pokemon worth dragging up, or None to hold the card."""
    if not opp.bench or opp.active is None:
        return None
    # A mill deck does not need Prizes; it needs turns the opponent cannot
    # use. Drag up something that can neither attack nor pay its way back
    # out (Gravity Gemstone adds one to that bill), and hold the card while
    # the Active is already stuck.
    if _is_mill_deck(pl):
        if _stuck(pl, opp, opp.active):
            return None
        stuck = [p for p in opp.bench if _stuck(pl, opp, p)]
        if stuck:
            return min(stuck, key=lambda p: (p.energy_count(),
                                             -retreat_of(opp, p, pl)))
    # Prize-aware, and deliberately NOT policy-gated -- it is the same kind
    # of change as Phantom Dive's counter budget: the card says you choose,
    # so choosing well is correctness, not strategy. It is also provably
    # safe. When nothing on the Bench can be Knocked Out (81.8% of gust
    # decisions) every score collapses to (0, 0, -left) and picking the max
    # of that IS "lowest HP left" -- the old rule, exactly. The two differ
    # in 1.4% of decisions, always toward the target worth more Prizes.
    #
    # Too rare to measure: +0.37 points, 95% CI [-1.42, +2.15] over 5,700
    # paired games, which is a coin flip. Kept on the argument that it is
    # strictly better in the cases where it applies and identical in the
    # rest, not on a number.
    #
    # The other half of this idea -- HOLDING the gust when the Active is
    # already the better target -- was removed. It changed 39.3% of gust
    # decisions and bought nothing measurable, and a rule that fires that
    # often with no demonstrated benefit is exactly the kind of complexity
    # that rots in this codebase.
    return max(opp.bench, key=lambda p: _gust_score(pl, opp, p))

def _promote_after_ko(owner, taker, log):
    """The new Active after an attack's Knock Out, chosen by `owner`.

    Greedy: whoever can actually fight, falling back to the biggest body.
    Sorting on remaining HP alone put a Bench toolbox piece -- one whose
    attacks the deck cannot even pay for -- into the Active Spot ahead of
    the real attacker. The lookahead pilot plays each candidate out
    through its own next turn and the opponent's reply.
    """
    owner.bench.sort(key=lambda p: (_ready_damage(owner, taker, p),
                                    effective_hp(owner, p) - p.damage),
                     reverse=True)
    i = 0
    if POL.knob(owner, "lookahead_samples") and len(owner.bench) > 1:
        def apply(me, them, k):
            me.active = me.bench.pop(k)
            me.active.promoted_this_turn = True
        i = lookahead_pick(owner, taker, list(range(len(owner.bench))),
                           apply, "promote", 0)
    owner.active = owner.bench.pop(i)
    owner.active.promoted_this_turn = True
    log.append(f"  {owner.name}: promotes {owner.active.name}")


def promote_from_bench(side, opp=None):
    """Choose the new Active after a Knock Out: the healthiest body.

    Promoting the best ATTACKER instead was tried and measured: -0.11
    points, and better on only 10 of 38 decks -- worse on 28. It reads
    like an obvious improvement (a fresh Basic with no Energy cannot
    attack, so the turn after a Knock Out is handed over for free) and it
    is not one. Promoting into a Knock Out with your best attacker mostly
    feeds it to the opponent's next attack, and durability wins the trade.
    Kept as a single function so the decision has one home if it is ever
    revisited with a better idea.
    """
    if not side.bench:
        return None
    if POL.knob(side, "promote") == "attacker":
        # Measured at -0.11 for the greedy pilot and kept off there, but it
        # is a real style: aggro wants to keep swinging, and eating a hit to
        # do it is the trade it is built to make.
        side.bench.sort(key=lambda p: (_ready_damage(side, opp, p),
                                       effective_hp(side, p) - p.damage),
                        reverse=True)
    else:
        side.bench.sort(key=lambda p: effective_hp(side, p) - p.damage,
                        reverse=True)
    return side.bench.pop(0)


def end_of_turn(pl, log):
    """Everything that ends with the turn of the player who just moved."""
    # A next-turn play lock lasted exactly this turn.
    pl.item_locked = False
    pl.turn_play_lock = set()
    pl.lost_pokemon_last_turn = False
    pl.lost_pokemon_names = ""
    # "At the end of your opponent's next turn, discard the
    # Defending Pokemon" -- resolved at the end of the turn it was
    # aimed at, which is this one.
    for spot in list(pl.in_play()):
        if getattr(spot, "delayed_discard", False):
            AE.discard_pokemon(pl, spot)
            if spot is pl.active:
                pl.active = None
            elif spot in pl.bench:
                pl.bench.remove(spot)
            log.append(f"  {pl.name}: {spot.name} is discarded")
    if pl.active is None and pl.bench:
        pl.active = pl.bench.pop(0)
    for spot in pl.in_play():
        AE.tick_attack_locks(spot)
        spot.turn_buff = 0
        spot.promoted_this_turn = False
        # The debuff was for exactly this turn, and this turn is over.
        spot.damage_penalty = 0
        spot.takes_more = 0
        spot.next_turn_attack_buff = None
        spot.no_weakness = False
        spot.extra_prize = 0
        spot.damage_taken_last_turn = 0
        spot.retaliate_counters = 0


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
    # A player may draw 1 card for each extra mulligan the OPPONENT took
    # (only the difference when both did). It was never drawn.
    extra_draws(a, b, mullA, mullB)

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
            end_of_turn(pl, log)
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
    # A Trainer outside KNOWN_TRAINERS is still played if the IR can
    # compile its text, so listing every non-registry name as "no modeled
    # effect" over-reports and invites acting on a gap that is not there.
    unmodeled = sorted({n for k, n in DECKLIST
                        if k in ("Item", "Supporter")
                        and n not in KNOWN_TRAINERS
                        and trainer_effect_ir(n) is None})
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
    # A4: a seed makes a matchup reproducible. Two runs of the same pair
    # differed by more than a point of win rate, which made it impossible
    # to tell a real change from noise -- the whole reason deck files kept
    # carrying numbers nobody could reproduce. Derived from the two deck
    # names so each matchup gets its own stream and a gauntlet stays
    # varied, while any single matchup replays exactly.
    seed_arg = next((a for a in sys.argv if a.startswith("--seed=")), None)
    if seed_arg:
        base = int(seed_arg.split("=", 1)[1])
        # --seed-tag replaces this deck's filename in the seed key, so two
        # DIFFERENT decklists can be run on the SAME random stream. That is
        # common random numbers, and without it a search comparing
        # candidates was comparing them across independent noise: each
        # candidate went to its own temp file, which changed the key, which
        # reshuffled everything. The pairing is most of the variance
        # reduction available here and it costs nothing.
        tag_arg = next((a for a in sys.argv if a.startswith("--seed-tag=")), None)
        tag = tag_arg.split("=", 1)[1] if tag_arg else os.path.basename(pathA)
        key = f"{base}:{tag}:{os.path.basename(pathB)}"
        random.seed(int(hashlib.sha256(key.encode()).hexdigest()[:12], 16))

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


# Every step that plays cards from hand obeys the play locks
# (Daunting Gaze, Potent Glare, an attack's "can't play Items next turn").
play_basics = _under_play_lock(play_basics)
try_evolve = _under_play_lock(try_evolve)
play_items = _under_play_lock(play_items)
attach_tools = _under_play_lock(attach_tools)



def _attack_scope(fn):
    """do_attack sets _RESOLVING once the attack is chosen; this puts it
    back however the attack ends."""
    def run(*a, **k):
        try:
            return fn(*a, **k)
        finally:
            _RESOLVING[0] = False
    run.__wrapped__ = fn
    return run


do_attack = _attack_scope(do_attack)

if __name__ == "__main__":
    main()
