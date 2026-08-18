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
  * Draw Abilities, via tcg_model.parse_ability -- amounts, draw-to-N,
    on-evolve triggers, Active-only conditions, after-a-KO conditions,
    named-card-in-play conditions, and hand/Energy discard costs.
  * Win by Prizes, by the opponent having no Pokemon in play, or by the
    opponent being unable to draw at the start of their turn.

Stated simplifications (read these before trusting a win rate)
  * Both players use the SAME generic heuristic AI: develop the board,
    evolve when possible, attach Energy to the Active, use draw
    Abilities, then attack with the highest-damage payable attack. It
    does not sequence combos, hold cards for a bigger turn, or play
    around anything. A deck whose plan depends on precise sequencing
    will be UNDERRATED here relative to a deck that just attacks.
  * Attack DAMAGE is computed, but attack SIDE-EFFECTS are not executed.
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
  * No Special Conditions, no Abilities other than the draw family, no
    Stadium effects besides Grand Tree.

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

MAX_BENCH = 5
STARTING_PRIZES = 6
MAX_TURNS = 40  # hard stop so a stalled pairing can't loop forever


# --------------------------------------------------------------------------
# Board objects
# --------------------------------------------------------------------------

class InPlay:
    __slots__ = ("name", "damage", "energy", "entered_turn", "evolved_this_turn", "tool")

    def __init__(self, name, turn):
        self.name = name
        self.damage = 0
        self.energy = []          # list of type-lists, one per attached Energy card
        self.entered_turn = turn
        self.evolved_this_turn = False
        self.tool = None

    def energy_count(self):
        return len(self.energy)


class Player:
    def __init__(self, name, POKEMON, decklist):
        self.name = name
        self.POKEMON = POKEMON
        self.deck = list(decklist)
        self.hand = []
        self.active = None
        self.bench = []
        self.discard = []
        self.prizes = STARTING_PRIZES
        self.supporter_played = False
        self.stadium = None
        self.lost_pokemon_last_turn = False
        self.abilities_used = set()
        self.played_supporters_this_turn = set()
        self.deck_out = False

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


def try_use_draw_abilities(pl, log, on_evolve_only=False, just_evolved=None):
    """Fire every legal draw Ability once per turn."""
    for p in pl.in_play():
        for ab in pl.info(p)["abilities"]:
            if ab["kind"] != "draw":
                continue
            if ab["trigger"] == "on_evolve":
                # only fires the moment it evolves, handled by caller
                if just_evolved is not p:
                    continue
            elif on_evolve_only:
                continue
            key = ability_key(p, ab)
            if key in pl.abilities_used:
                continue
            if ab.get("requires_active") and p is not pl.active:
                continue
            if ab.get("requires_ko_last_turn") and not pl.lost_pokemon_last_turn:
                continue
            need = ab.get("requires_in_play")
            if need and need not in pl.in_play_names():
                continue
            need_played = ab.get("requires_played_this_turn")
            if need_played and need_played not in pl.played_supporters_this_turn:
                continue

            # costs
            cost_hand = ab.get("cost_discard_hand") or 0
            if cost_hand:
                if len(pl.hand) < cost_hand:
                    continue
            etype = ab.get("cost_discard_energy_hand")
            energy_idx = None
            if etype:
                energy_idx = next(
                    (i for i, (k, n) in enumerate(pl.hand)
                     if k == "Energy" and n.startswith(etype)), None)
                if energy_idx is None:
                    continue
            self_etype = ab.get("cost_discard_energy_self")
            if self_etype:
                hit = next((i for i, prov in enumerate(p.energy) if self_etype in prov), None)
                if hit is None:
                    continue

            target = ab.get("draw_to")
            amount = ab.get("amount")
            if target is not None and len(pl.hand) >= target:
                continue

            # pay
            if etype:
                k, n = pl.hand.pop(energy_idx)
                pl.discard.append(n)
            if self_etype:
                p.energy.pop(hit)
                pl.discard.append(f"{self_etype} Energy")
            for _ in range(cost_hand):
                if pl.hand:
                    k, n = pl.hand.pop(0)
                    pl.discard.append(n)

            before = len(pl.hand)
            if target is not None:
                while len(pl.hand) < target and pl.deck:
                    pl.draw(1)
            else:
                pl.draw(amount or 0)
            drew = len(pl.hand) - before
            pl.abilities_used.add(key)
            log.append(f"  {pl.name}: {p.name} uses {ab['name']} -> drew {drew}")

            if ab.get("cost_shuffle_self") and drew > 0:
                pl.deck.append(("Pokemon", p.name))
                if p is pl.active:
                    # Real rule: the Active Spot cannot be left empty while
                    # you still have Benched Pokemon -- promote one.
                    pl.active = pl.bench.pop(0) if pl.bench else None
                elif p in pl.bench:
                    pl.bench.remove(p)
                random.shuffle(pl.deck)
                log.append(f"  {pl.name}: {p.name} shuffles itself back into the deck")
                return  # board changed; stop iterating this pass


# --------------------------------------------------------------------------
# Trainer effects (compact registry; unknown Trainers are never played)
# --------------------------------------------------------------------------

def basics_in_hand(pl):
    return [n for k, n in pl.hand if k == "Pokemon" and pl.POKEMON[n]["stage"] == "Basic"]


def play_basics(pl, turn, log):
    if pl.active is None:
        bs = basics_in_hand(pl)
        if bs:
            best = max(bs, key=lambda n: pl.POKEMON[n]["hp"])
            pl.remove_from_hand("Pokemon", best)
            pl.active = InPlay(best, turn)
            log.append(f"  {pl.name}: {best} to Active")
    for kind, name in list(pl.hand):
        if kind == "Pokemon" and pl.POKEMON[name]["stage"] == "Basic" and len(pl.bench) < MAX_BENCH:
            pl.remove_from_hand(kind, name)
            pl.bench.append(InPlay(name, turn))
            log.append(f"  {pl.name}: benches {name}")


def try_evolve(pl, turn, log, first_turn):
    if first_turn:
        return
    for kind, name in list(pl.hand):
        if kind != "Pokemon":
            continue
        pre = pl.POKEMON[name]["evolves_from"]
        if not pre:
            continue
        for spot in pl.in_play():
            if spot.name == pre and turn > spot.entered_turn:
                pl.remove_from_hand(kind, name)
                spot.name = name
                spot.evolved_this_turn = True
                log.append(f"  {pl.name}: {pre} -> {name}")
                try_use_draw_abilities(pl, log, on_evolve_only=True, just_evolved=spot)
                break


def effect_rare_candy(pl, turn, log, first_turn):
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
                try_use_draw_abilities(pl, log, on_evolve_only=True, just_evolved=spot)
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


def play_items(pl, turn, log, first_turn):
    while ("Item", "Rare Candy") in pl.hand:
        if not effect_rare_candy(pl, turn, log, first_turn):
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


def play_supporter(pl, opp, turn, log):
    if pl.supporter_played:
        return
    hand_names = [n for k, n in pl.hand if k == "Supporter"]

    def use(name):
        pl.remove_from_hand("Supporter", name)
        pl.discard.append(name)
        pl.supporter_played = True
        pl.played_supporters_this_turn.add(name)

    # Draw/refresh Supporters, weakest hand first
    if len(pl.hand) <= 4:
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
    "Team Rocket's Giovanni",
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
_FLIP_UNTIL_TAILS_RE = _re.compile(r"flip a coin until you get tails", _re.I)
_FLIP_N_RE = _re.compile(r"flip (\d+) coins", _re.I)


def _clause_count(clause, pl, opp, spot):
    """How many times a 'for each ...' clause applies right now, or None."""
    c = clause.lower()
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


def _copied_attack_damage(pl, opp, spot, text):
    """Attacks that borrow another Pokemon's attack. Returns damage or None.

    Persian ex's Haughty Order (reveal the opponent's top N, use an attack
    found there) and the 'use the Defending Pokemon's attack' pattern are
    both well-defined enough to actually resolve, so they are -- rather
    than scoring the signature attack of a whole archetype as 0.
    The copied attack's own cost is irrelevant: the real card says to use
    it as this attack, which you already paid for.
    """
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


def best_attack(pl, spot, only_payable=True, opp=None):
    info = pl.POKEMON[spot.name]
    best, best_dmg = None, -1
    for atk in info["attacks"]:
        if only_payable and not can_pay(atk["cost"], spot.energy):
            continue
        dmg = attack_damage(pl, opp, spot, atk) if opp is not None else atk["damage"]
        if dmg > best_dmg:
            best, best_dmg = atk, dmg
    return best


def energy_shortfall(pl, spot):
    """How many more Energy the Active needs for its biggest attack."""
    info = pl.POKEMON[spot.name]
    if not info["attacks"]:
        return 0
    need = max(len(a["cost"]) for a in info["attacks"])
    return max(0, need - spot.energy_count())


def attach_energy(pl, cards_by_name, log):
    idx = next((i for i, (k, n) in enumerate(pl.hand) if k == "Energy"), None)
    if idx is None:
        return
    target = None
    if pl.active and energy_shortfall(pl, pl.active) > 0:
        target = pl.active
    else:
        for spot in pl.bench:
            if energy_shortfall(pl, spot) > 0:
                target = spot
                break
    if target is None:
        return
    kind, name = pl.hand.pop(idx)
    target.energy.append(energy_types_for(name, cards_by_name))
    log.append(f"  {pl.name}: attaches {name} to {target.name}")


def _ready_damage(pl, opp, spot):
    atk = best_attack(pl, spot, opp=opp)
    return attack_damage(pl, opp, spot, atk) if atk else 0


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
    cost = pl.POKEMON[pl.active.name]["retreat"]
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
    pl.bench.append(pl.active)
    pl.active = target
    log.append(f"  {pl.name}: retreats into {target.name}")


def do_attack(pl, opp, log):
    """Returns True if the game ended."""
    if not pl.active or not opp.active:
        return False
    if pl.active.evolved_this_turn:
        pass  # evolving does not prevent attacking in the real game
    atk = best_attack(pl, pl.active, opp=opp)
    if not atk:
        return False
    dmg = attack_damage(pl, opp, pl.active, atk)
    if dmg <= 0:
        return False
    atk_types = pl.POKEMON[pl.active.name]["types"]
    weak = opp.POKEMON[opp.active.name]["weakness"]
    if weak and weak in atk_types:
        dmg *= 2
    opp.active.damage += dmg
    log.append(f"  {pl.name}: {pl.active.name} uses {atk['name']} for {dmg}"
               f" -> {opp.active.name} at {opp.active.damage}/{opp.POKEMON[opp.active.name]['hp']}")
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
            opp.bench.sort(key=lambda p: opp.POKEMON[p.name]["hp"] - p.damage, reverse=True)
            opp.active = opp.bench.pop(0)
            log.append(f"  {opp.name}: promotes {opp.active.name}")
        else:
            return True
    return False


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
    pl.abilities_used = set()
    pl.played_supporters_this_turn = set()
    for spot in pl.in_play():
        spot.evolved_this_turn = False

    first_turn = (turn == 1 and going_first)
    if not first_turn:
        pl.draw(1)
        if pl.deck_out and not pl.hand:
            return "deck_out"

    play_basics(pl, turn, log)
    if pl.active is None:
        return "no_pokemon"
    try_evolve(pl, turn, log, first_turn)
    play_items(pl, turn, log, first_turn)
    play_supporter(pl, opp, turn, log)
    try_use_draw_abilities(pl, log)
    attach_energy(pl, cards_by_name, log)
    try_evolve(pl, turn, log, first_turn)
    try_retreat(pl, opp, log)

    if not first_turn:
        if do_attack(pl, opp, log):
            return "win"
    return None


def run_game(modelA, modelB, verbose=False):
    (nameA, POKA, DECKA), (nameB, POKB, DECKB) = modelA, modelB
    cards_by_name, _ = M.build_card_index(M.load_cards())

    a = Player(nameA, POKA, DECKA)
    b = Player(nameB, POKB, DECKB)
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


def load_model(path, label):
    text = open(path).read()
    POKEMON, DECKLIST, pooled, unresolved = M.build_deck_model(text)
    unmodeled = sorted({n for k, n in DECKLIST
                        if k in ("Item", "Supporter") and n not in KNOWN_TRAINERS})
    return (label, POKEMON, DECKLIST), {
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
    modelA = (labelA, modelA[1], modelA[2])
    modelB = (labelB, modelB[1], modelB[2])

    for label, meta in ((labelA, metaA), (labelB, metaB)):
        print(f"=== {label} ===")
        print(f"  cards: {meta['size']}")
        if meta["unresolved"]:
            print(f"  NOT FOUND in dataset (excluded): {', '.join(meta['unresolved'])}")
        if meta["pooled"]:
            print(f"  matched by name only: {', '.join(meta['pooled'])}")
        if meta["unmodeled"]:
            print(f"  Trainers with no modeled effect (never played): {', '.join(meta['unmodeled'])}")
        draw_abs = [(n, ab["name"]) for n, i in meta["pokemon"].items()
                    for ab in i["abilities"] if ab["kind"] == "draw"]
        if draw_abs:
            print(f"  draw Abilities modeled: {', '.join(f'{a}/{b}' for a, b in draw_abs)}")
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
