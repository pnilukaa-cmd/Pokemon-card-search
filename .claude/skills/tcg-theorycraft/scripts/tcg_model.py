#!/usr/bin/env python3
"""Shared card/decklist model for this project's simulators.

Extracted from simulate_baseline.py so that the single-player baseline
simulator and the two-player versus simulator build their Pokemon models
from exactly the same code, against the same real card data, instead of
each hand-rolling its own (which is how simulate_deck.py and
simulate_match.py both ended up with hardcoded stats that silently
drifted from the actual cards).

What lives here:
  * decklist parsing that PRESERVES the SET/NUM tokens, so a card can be
    resolved to its exact printing rather than pooling every printing
    that shares a name
  * Pokemon stat extraction (stage / evolvesFrom / HP / retreat / types /
    weakness / attacks) straight from pokemon_standard_cards.json
  * an Ability parser for the draw-Ability family (see parse_ability)

Ability parsing is deliberately conservative. It was written against the
full enumerated list of every draw Ability in the Standard pool (19 of
them at time of writing, small enough to read individually rather than
trust a regex blind), and anything it cannot faithfully represent is
returned with an `unmodeled` reason string instead of being silently
approximated. Callers are expected to surface those reasons in their
reports, the same "visible gap, never a silent one" contract the Trainer
effect registry already follows.
"""
import json
import re
from collections import defaultdict

CARDS_PATH = "pokemon_standard_cards.json"

LINE_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")

SYMBOL_TO_TYPE = {
    "G": "Grass", "R": "Fire", "W": "Water", "L": "Lightning",
    "P": "Psychic", "F": "Fighting", "D": "Darkness", "M": "Metal",
    "Y": "Fairy", "N": "Dragon", "C": "Colorless",
}

REAL_TYPES = ["Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting",
              "Darkness", "Metal", "Fairy", "Dragon", "Colorless"]

BASIC_ENERGY_RE = re.compile(r"^(" + "|".join(REAL_TYPES) + r") Energy$")


def load_cards(path=CARDS_PATH):
    with open(path) as f:
        return json.load(f)


# --------------------------------------------------------------------------
# Decklist parsing
# --------------------------------------------------------------------------

def parse_decklist_entries(text):
    """Returns [{count, name, set, number}], keeping SET/NUM when present."""
    out = []
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if not m:
            continue
        count, rest = int(m.group(1)), m.group(2)
        tokens = rest.split()
        set_code = number = None
        if tokens and tokens[-1].isdigit():
            number = tokens[-1]
            tokens = tokens[:-1]
            if tokens and re.fullmatch(r"[A-Za-z0-9]{2,6}", tokens[-1]) and tokens[-1].isupper():
                set_code = tokens[-1]
                tokens = tokens[:-1]
        name = " ".join(tokens).strip()
        if not name:
            continue

        def expand(mm):
            return SYMBOL_TO_TYPE.get(mm.group(1).upper(), mm.group(0))
        name = re.sub(r"\{(\w)\}", expand, name)
        name = re.sub(r"^Basic (\w+) Energy$", r"\1 Energy", name)
        out.append({"count": count, "name": name, "set": set_code, "number": number})
    return out


def build_card_index(cards):
    by_name = defaultdict(list)
    by_setnum = {}
    for c in cards:
        by_name[c["name"]].append(c)
        code = (c.get("set") or {}).get("ptcgoCode")
        num = c.get("number")
        if code and num:
            by_setnum[(c["name"], code, num)] = c
    return by_name, by_setnum


def resolve_card(entry, by_name, by_setnum):
    """Returns (card_or_None, matched_exact_printing: bool)."""
    if entry["set"] and entry["number"]:
        c = by_setnum.get((entry["name"], entry["set"], entry["number"]))
        if c:
            return c, True
    matches = by_name.get(entry["name"])
    if matches:
        return matches[0], False
    return None, False


# --------------------------------------------------------------------------
# Pokemon stats
# --------------------------------------------------------------------------

def stage_of(card):
    subtypes = card.get("subtypes") or []
    if "Basic" in subtypes:
        return "Basic"
    if "Stage 1" in subtypes:
        return "Stage 1"
    if "Stage 2" in subtypes:
        return "Stage 2"
    return "Basic" if not card.get("evolvesFrom") else "Stage 1"


def is_rule_box(card):
    subtypes = set(card.get("subtypes") or [])
    return bool(subtypes - {"Basic", "Stage 1", "Stage 2", "Restored"})


def prize_value(card):
    """How many Prize cards the opponent takes when this is Knocked Out.
    Mega Evolution ex give up 3, other ex/V-style rule-box Pokemon give up
    2, everything else 1 -- read off the card's own rules text rather than
    assumed from the subtype, since that text is what states the number."""
    rules = " ".join(card.get("rules") or [])
    if "take 3 Prize cards" in rules:
        return 3
    if "take 2 Prize cards" in rules:
        return 2
    subtypes = set(card.get("subtypes") or [])
    if "MEGA" in subtypes:
        return 3
    if is_rule_box(card):
        return 2
    return 1


DAMAGE_RE = re.compile(r"^\D*(\d+)")


def parse_damage(dmg):
    if not dmg:
        return 0
    m = DAMAGE_RE.match(dmg)
    return int(m.group(1)) if m else 0


def build_pokemon_info(card):
    attacks = []
    for atk in card.get("attacks") or []:
        cost = [c for c in (atk.get("cost") or []) if c != "Free"]
        attacks.append({
            "name": atk["name"],
            "cost": cost,
            "damage": parse_damage(atk.get("damage")),
            "text": atk.get("text") or "",
        })
    retreat = card.get("convertedRetreatCost")
    if retreat is None:
        retreat = len(card.get("retreatCost") or [])
    weak = None
    for w in card.get("weaknesses") or []:
        weak = w.get("type")
        break
    return {
        "stage": stage_of(card),
        "evolves_from": card.get("evolvesFrom"),
        "hp": int(card.get("hp") or 0),
        "retreat": retreat,
        "rule_box": is_rule_box(card),
        "prize_value": prize_value(card),
        "types": card.get("types") or [],
        "weakness": weak,
        "attacks": attacks,
        "abilities": [classify_ability(ab) for ab in (card.get("abilities") or [])],
    }


# --------------------------------------------------------------------------
# Ability parsing (draw family)
# --------------------------------------------------------------------------
# Grounded in the full enumerated set of draw Abilities in the Standard
# pool. Each regex below was checked against the real card text it is
# meant to match -- see the self-test at the bottom of this file, which
# asserts the parser's output for every one of them.

_DRAW_TO_RE = re.compile(r"draw cards until you have (\d+) cards? in your hand", re.I)
_DRAW_N_RE = re.compile(r"\bdraw (\d+) cards?", re.I)
_DRAW_ONE_RE = re.compile(r"\bdraw a card", re.I)

_ON_EVOLVE_RE = re.compile(r"when you play this pok[eé]mon from your hand to evolve", re.I)
_ACTIVE_ONLY_RE = re.compile(r"if this pok[eé]mon is in the active spot", re.I)
_AFTER_KO_RE = re.compile(r"were knocked out during your opponent'?s last turn", re.I)
_REQ_IN_PLAY_RE = re.compile(r"if you have ([A-Z][\w'’ -]+?) in play", re.I)
_REQ_PLAYED_RE = re.compile(r"if you played ([A-Z][\w'’ -]+?) from your hand this turn", re.I)

_COST_DISCARD_HAND_RE = re.compile(
    r"discard (\d+|a) cards? from your hand in order to use", re.I)
_COST_BOTTOM_RE = re.compile(
    r"put a card from your hand on the bottom of your deck in order to use", re.I)
_COST_DISCARD_ENERGY_HAND_RE = re.compile(
    r"discard a basic (\w+) energy card from your hand", re.I)
_COST_DISCARD_ENERGY_SELF_RE = re.compile(
    r"discard a basic (\w+) energy from this pok[eé]mon", re.I)
_SHUFFLE_SELF_RE = re.compile(
    r"shuffle this pok[eé]mon and all attached cards into your deck", re.I)

_TOUCHES_OPPONENT_RE = re.compile(
    r"each player draw|your opponent shuffle|have your opponent", re.I)


def parse_ability(ab):
    """Classify one Ability dict from the card JSON.

    Returns a dict always containing 'name', 'text', and 'kind'. 'kind' is
    'draw' for self-draw Abilities this engine can execute, or 'other' for
    everything else. Draw Abilities additionally carry the amount, trigger,
    conditions, and costs; anything present in the text that the engine
    cannot faithfully honor is recorded in 'unmodeled' so callers can
    report it rather than quietly pretending it isn't there.
    """
    name = ab.get("name") or ""
    text = ab.get("text") or ""
    info = {"name": name, "text": text, "kind": "other", "unmodeled": None}

    if not re.search(r"\bdraw\b", text, re.I):
        return info

    # Abilities whose draw is aimed at (or shared with) the opponent are a
    # different family -- deliberately not treated as self-draw.
    if _TOUCHES_OPPONENT_RE.search(text):
        info["unmodeled"] = "draw effect involves the opponent"
        return info

    draw_to = None
    amount = None
    m = _DRAW_TO_RE.search(text)
    if m:
        draw_to = int(m.group(1))
    else:
        m = _DRAW_N_RE.search(text)
        if m:
            amount = int(m.group(1))
        elif _DRAW_ONE_RE.search(text):
            amount = 1
    if draw_to is None and amount is None:
        info["unmodeled"] = "draw amount not recognized"
        return info

    info["kind"] = "draw"
    info["amount"] = amount
    info["draw_to"] = draw_to
    info["trigger"] = "on_evolve" if _ON_EVOLVE_RE.search(text) else "once_per_turn"
    info["requires_active"] = bool(_ACTIVE_ONLY_RE.search(text))
    info["requires_ko_last_turn"] = bool(_AFTER_KO_RE.search(text))

    req_play = _REQ_IN_PLAY_RE.search(text)
    info["requires_in_play"] = req_play.group(1).strip() if req_play else None
    req_played = _REQ_PLAYED_RE.search(text)
    info["requires_played_this_turn"] = req_played.group(1).strip() if req_played else None

    cost_hand = 0
    m = _COST_DISCARD_HAND_RE.search(text)
    if m:
        cost_hand = 1 if m.group(1).lower() == "a" else int(m.group(1))
    if _COST_BOTTOM_RE.search(text):
        # Mechanically identical for our purposes: one card leaves hand.
        cost_hand = max(cost_hand, 1)
    info["cost_discard_hand"] = cost_hand

    m = _COST_DISCARD_ENERGY_HAND_RE.search(text)
    info["cost_discard_energy_hand"] = m.group(1).capitalize() if m else None
    m = _COST_DISCARD_ENERGY_SELF_RE.search(text)
    info["cost_discard_energy_self"] = m.group(1).capitalize() if m else None

    info["cost_shuffle_self"] = bool(_SHUFFLE_SELF_RE.search(text))

    # Teal Dance-style "attach an Energy, and if you did, draw" is an
    # Energy-acceleration Ability with a draw rider, not a draw engine --
    # flag it so it isn't scored as free card advantage.
    if re.search(r"attach a basic .* energy card from your hand", text, re.I):
        info["kind"] = "other"
        info["unmodeled"] = "draw is conditional on an Energy attachment (acceleration Ability)"
    return info


# --------------------------------------------------------------------------
# Ability parsing: retaliation / damage reduction / counter movement
# --------------------------------------------------------------------------
# These three families are small and fully enumerable (8 retaliation
# Abilities, 18 reduction, a handful of movers), and between them they carry
# the whole game plan of several real decks -- a retaliation deck's entire
# defense is invisible without them.

_DAMAGED_BY_ATTACK_RE = re.compile(r"is damaged by an attack", re.I)
_RETAL_AMOUNT_RE = re.compile(
    r"(?:place|put) (\d+) damage counters? on the attacking pok[eé]mon", re.I)
_RETAL_PER_RE = re.compile(
    r"for each (\w+) energy attached to this pok[eé]mon", re.I)
_REDUCE_RE = re.compile(r"takes? (\d+) less damage from attacks", re.I)
_REDUCE_TEAM_RE = re.compile(r"all of your ([\w ]*?)pok[eé]mon take", re.I)
_MOVE_COUNTERS_RE = re.compile(
    r"move (?:up to )?(\d+) damage counters? from", re.I)


def parse_defensive_ability(ab):
    """Classify retaliation / damage-reduction Abilities.

    Returns None when the text is not one of these families, so callers can
    fall through to parse_ability.
    """
    name = ab.get("name") or ""
    text = ab.get("text") or ""

    if _DAMAGED_BY_ATTACK_RE.search(text):
        m = _RETAL_AMOUNT_RE.search(text)
        if m:
            per = _RETAL_PER_RE.search(text)
            # Spiritomb-style: triggers off your Active, not off itself.
            team = bool(re.search(r"if your active ([\w ]*?)pok[eé]mon is damaged", text, re.I))
            tmatch = re.search(r"if your active (\w+) pok[eé]mon is damaged", text, re.I)
            return {
                "name": name, "text": text, "kind": "retaliate",
                "counters": int(m.group(1)),
                "per_energy_type": per.group(1).capitalize() if per else None,
                "requires_active": "in the active spot" in text.lower(),
                "protects_team": team,
                "team_type": tmatch.group(1).capitalize() if tmatch else None,
                "unmodeled": None,
            }

    m = _REDUCE_RE.search(text)
    if m:
        team = _REDUCE_TEAM_RE.search(text)
        team_type = None
        cond = None
        if team:
            team_type = (team.group(1) or "").strip().capitalize() or None
        # Conditional reductions (by attacker type, by a second copy in play)
        if re.search(r"from your opponent's \w+ or \w+ pok[eé]mon|as long as you have", text, re.I):
            cond = "conditional (attacker type or board state) -- not evaluated"
        return {
            "name": name, "text": text, "kind": "reduce",
            "amount": int(m.group(1)),
            "protects_team": bool(team),
            "team_type": team_type,
            "requires_bench": "on your bench" in text.lower(),
            "unmodeled": cond,
        }

    m = _MOVE_COUNTERS_RE.search(text)
    if m and "your opponent" in text.lower():
        etype = re.search(r"if this pok[eé]mon has any (\w+) energy attached", text, re.I)
        return {
            "name": name, "text": text, "kind": "move_counters",
            "amount": int(m.group(1)),
            "requires_energy_type": etype.group(1).capitalize() if etype else None,
            "unmodeled": None,
        }
    return None


def classify_ability(ab):
    """parse_defensive_ability first, then the draw-family parser."""
    d = parse_defensive_ability(ab)
    if d is not None:
        return d
    return parse_ability(ab)


TOOL_RETALIATE_RE = re.compile(
    r"(?:place|put) (\d+) damage counters? on the attacking pok[eé]mon", re.I)


def parse_tool_or_energy_retaliation(card):
    """Punk Helmet / Spiky Energy / Deluxe Bomb: same retaliation shape, but
    printed on a Tool or Special Energy rather than a Pokemon."""
    rules = " ".join(card.get("rules") or [])
    if not _DAMAGED_BY_ATTACK_RE.search(rules):
        return None
    m = TOOL_RETALIATE_RE.search(rules)
    if not m:
        return None
    tmatch = re.search(r"if the (\w+) pok[eé]mon this card is attached to", rules, re.I)
    return {
        "counters": int(m.group(1)),
        "requires_type": tmatch.group(1).capitalize() if tmatch else None,
        "requires_active": "in the active spot" in rules.lower(),
        "discard_after": "discard this card" in rules.lower(),
    }


def build_deck_model(text, cards=None):
    """Returns (POKEMON, DECKLIST, fallback_pooled, unresolved).

    POKEMON:   name -> stat dict (see build_pokemon_info)
    DECKLIST:  list of (kind, name) tuples, one per physical card
    fallback_pooled: names matched without an exact SET/NUM hit
    unresolved: names not found in the dataset at all
    """
    entries = parse_decklist_entries(text)
    cards = cards if cards is not None else load_cards()
    by_name, by_setnum = build_card_index(cards)
    POKEMON, DECKLIST = {}, []
    fallback_pooled, unresolved = set(), []
    for entry in entries:
        name, count = entry["name"], entry["count"]
        if BASIC_ENERGY_RE.match(name):
            DECKLIST += [("Energy", name)] * count
            continue
        card, exact = resolve_card(entry, by_name, by_setnum)
        if card is None:
            unresolved.append(name)
            continue
        if not exact:
            fallback_pooled.add(name)
        supertype = card.get("supertype")
        if supertype == "Pokémon":
            if name not in POKEMON:
                POKEMON[name] = build_pokemon_info(card)
            DECKLIST += [("Pokemon", name)] * count
        elif supertype == "Energy":
            DECKLIST += [("Energy", name)] * count
        else:
            subtypes = set(card.get("subtypes") or [])
            if "Supporter" in subtypes:
                kind = "Supporter"
            elif "Pokémon Tool" in subtypes:
                kind = "Tool"
            elif "Stadium" in subtypes:
                kind = "Stadium"
            else:
                kind = "Item"
            DECKLIST += [(kind, name)] * count
    return POKEMON, DECKLIST, fallback_pooled, unresolved


# --------------------------------------------------------------------------
# Self-test: assert the parser against every real draw Ability in the pool
# --------------------------------------------------------------------------

def _self_test():
    cards = load_cards()
    seen = {}
    for c in cards:
        for ab in c.get("abilities") or []:
            if re.search(r"\bdraw\b", ab.get("text") or "", re.I):
                seen[(c["name"], ab["name"])] = parse_ability(ab)

    expectations = {
        ("Toucannon", "Aerial Draw"): dict(kind="draw", amount=1, trigger="once_per_turn",
                                           cost_discard_hand=0, cost_shuffle_self=False),
        ("Rapidash", "Hurried Gait"): dict(kind="draw", amount=1, trigger="once_per_turn"),
        ("Kadabra", "Psychic Draw"): dict(kind="draw", amount=2, trigger="on_evolve"),
        ("Alakazam", "Psychic Draw"): dict(kind="draw", amount=3, trigger="on_evolve"),
        ("Dudunsparce", "Run Away Draw"): dict(kind="draw", amount=3, cost_shuffle_self=True),
        ("Mega Kangaskhan ex", "Run Errand"): dict(kind="draw", amount=2, requires_active=True),
        ("Fezandipiti ex", "Flip the Script"): dict(kind="draw", amount=3,
                                                    requires_ko_last_turn=True),
        ("N's Zoroark ex", "Trade"): dict(kind="draw", amount=2, cost_discard_hand=1),
        ("Team Rocket's Porygon-Z", "Reconstitute"): dict(kind="draw", amount=1,
                                                          cost_discard_hand=2),
        ("Quaquaval", "Up-Tempo"): dict(kind="draw", draw_to=5, cost_discard_hand=1),
        ("Iono's Kilowattrel", "Flashing Draw"): dict(kind="draw", draw_to=6,
                                                      cost_discard_energy_self="Lightning"),
        ("Delphox", "Flaring Magic"): dict(kind="draw", draw_to=7,
                                           cost_discard_energy_hand="Fire"),
        ("Lunatone", "Lunar Cycle"): dict(kind="draw", amount=3, requires_in_play="Solrock",
                                          cost_discard_energy_hand="Fighting"),
        ("Crobat", "Shadowy Envoy"): dict(kind="draw", draw_to=8,
                                          requires_played_this_turn="Janine's Secret Art"),
        # Opponent-facing / rider cases must NOT be scored as self-draw:
        ("Chandelure", "Alluring Light"): dict(kind="other"),
        ("Gothitelle", "Distorted Future"): dict(kind="other"),
        ("Vivillon", "Grand Wing"): dict(kind="other"),
        ("Teal Mask Ogerpon ex", "Teal Dance"): dict(kind="other"),
    }

    failures = []
    for key, want in expectations.items():
        got = seen.get(key)
        if got is None:
            failures.append(f"{key}: ability not found in dataset")
            continue
        for field, value in want.items():
            if got.get(field) != value:
                failures.append(f"{key}: {field} = {got.get(field)!r}, expected {value!r}")

    checked = len(expectations)
    print(f"Draw Abilities found in pool: {len(seen)}")
    print(f"Assertions checked: {checked} abilities")
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures:
            print("  " + f)
        return False
    print("All ability-parser assertions passed.")
    untested = set(seen) - set(expectations)
    if untested:
        print(f"\nNot covered by an assertion ({len(untested)}):")
        for k in sorted(untested):
            print(f"  {k[0]} / {k[1]} -> kind={seen[k]['kind']}")
    return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if _self_test() else 1)
