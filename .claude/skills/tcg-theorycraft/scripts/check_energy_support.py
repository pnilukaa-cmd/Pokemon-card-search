#!/usr/bin/env python3
"""Check whether a decklist's Energy line can actually pay every attack cost
in it, and whether any attacker is gated by an Ability that could block it
from attacking at all.

This automates two checks that previously only happened by eye, reactively,
after a mistake (Team Rocket's Articuno running Water-costed Dark Frost with
zero Water Energy anywhere in the deck; Bastiodon needing 2 Metal Energy
simultaneously attached while the decklist ran exactly one Metal-providing
card total; Team Rocket's Mewtwo ex's Power Saver Ability blocking it from
attacking at all with no other Team Rocket's Pokemon in play). Both were
caught by hand, one turn late. This script runs both checks up front.

What it checks:
  1. Energy-type support: for every attack cost across every named Pokemon
     in the decklist, sum how many Energy cards in the decklist's own Energy
     section could provide each non-Colorless type required (Basic Energy by
     name; Special Energy by parsing its own rules text, reusing
     analyze_mechanics.py's infer_special_energy_types). Flag IMPOSSIBLE if
     the deck's total supply of a type is below what a single attack needs
     simultaneously attached; flag TIGHT if supply exactly equals the
     requirement with zero spare copies.
  2. Attack-gating Abilities: scan every named Pokemon's Ability text for
     phrasing like "can't attack unless" / "can't use this attack unless"
     and surface it as a reminder to verify the condition is actually
     satisfiable by the rest of the decklist (not auto-resolved, since that
     requires reading the specific condition).

Input: a decklist in the same plain-text format used throughout this
project (lines like "4 Card Name SET 123"; "Pokémon:"/"Trainer:"/"Energy:"
headers, blank lines, and a trailing "Total Cards: 60" are all ignored --
only lines starting with a quantity are read).

Known limitation: cards are matched by NAME only, not by exact set+number,
then every attack from every printing sharing that name in the local
dataset is pooled together. If a decklist's specific printing has a
different (rarer) attack set than what's in the local dedup, this can
under- or over-report. Treat a clean result as "no red flag found," not an
ironclad guarantee -- same caveat as every other check in this toolkit.

Usage:
  python3 check_energy_support.py decklist.txt
  python3 check_energy_support.py - < decklist.txt   (read from stdin)
"""
import json
import re
import sys
from collections import defaultdict

sys.path.insert(0, ".")
from analyze_mechanics import infer_special_energy_types, _REAL_TYPES

LINE_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")

# PTCGL shorthand energy symbols, e.g. "Basic {W} Energy" -> Water Energy.
SYMBOL_TO_TYPE = {
    "G": "Grass", "R": "Fire", "W": "Water", "L": "Lightning",
    "P": "Psychic", "F": "Fighting", "D": "Darkness", "M": "Metal",
    "Y": "Fairy", "N": "Dragon", "C": "Colorless",
}


def load_cards():
    with open("pokemon_standard_cards.json") as f:
        return json.load(f)


def parse_decklist(text):
    """Returns list of (count, name) tuples, in the order they appear."""
    lines = []
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if not m:
            continue
        count, rest = int(m.group(1)), m.group(2)
        # Strip a trailing "SET 123"-style printing tag if present -- the
        # last one or two whitespace-separated tokens, if the very last
        # token is numeric. Names never end in a bare number in this pool.
        tokens = rest.split()
        if tokens and tokens[-1].isdigit():
            tokens = tokens[:-1]
            if tokens and re.fullmatch(r"[A-Za-z0-9]{2,6}", tokens[-1]) and tokens[-1].isupper():
                tokens = tokens[:-1]
        name = " ".join(tokens).strip()
        if not name:
            continue
        # Expand any inline PTCGL type-symbol token (e.g. "Magnetic {M}
        # Energy" -> "Magnetic Metal Energy", "Basic {D} Energy" -> "Basic
        # Darkness Energy") -- PTCGL embeds the symbol inside a card's own
        # name for display, both for plain Basic Energy and for Special
        # Energy cards whose real name spells the type out.
        def expand(m):
            return SYMBOL_TO_TYPE.get(m.group(1).upper(), m.group(0))
        name = re.sub(r"\{(\w)\}", expand, name)
        # "Basic <Type> Energy" collapses to just "<Type> Energy" -- that's
        # the actual card name pattern used for Basic Energy in this project
        # (which pokemontcg.io doesn't carry at all; see BASIC_ENERGY_RE
        # below for why that's handled separately from a dataset lookup).
        name = re.sub(r"^Basic (\w+) Energy$", r"\1 Energy", name)
        lines.append((count, name))
    return lines


BASIC_ENERGY_RE = re.compile(r"^(" + "|".join(_REAL_TYPES) + r") Energy$")


def energy_type_supply(deck_lines, cards_by_name):
    """Returns dict: type -> total number of Energy card copies in the
    decklist that can provide that type (Basic by name match, Special by
    parsing its own text).

    Basic Energy cards (e.g. "Darkness Energy") are NOT present in
    pokemon_standard_cards.json at all -- confirmed and treated as a known,
    harmless gap throughout this project, since Basic Energy is always
    legal regardless of printing and was never worth fetching. That means
    they can't be found via cards_by_name and have to be recognized by
    their own plain "<Type> Energy" name pattern directly, before falling
    through to a dataset lookup for genuine Special Energy cards."""
    supply = defaultdict(int)
    for count, name in deck_lines:
        basic = BASIC_ENERGY_RE.match(name)
        if basic:
            supply[basic.group(1)] += count
            continue

        matches = cards_by_name.get(name)
        if not matches:
            continue
        card = matches[0]
        if card.get("supertype") != "Energy":
            continue
        provided = card.get("types") or []
        if not provided:
            text = " ".join(card.get("rules") or [])
            provided = infer_special_energy_types(text)
        for t in provided:
            if t == "Any":
                for rt in _REAL_TYPES:
                    supply[rt] += count
            else:
                supply[t] += count
    return supply


def attack_requirements(deck_lines, cards_by_name):
    """Returns list of (pokemon_name, attack_name, cost_list, max_simultaneous_by_type)."""
    seen_attacks = set()
    reqs = []
    for count, name in deck_lines:
        matches = cards_by_name.get(name)
        if not matches or matches[0].get("supertype") != "Pokémon":
            continue
        for card in matches:
            for atk in card.get("attacks") or []:
                key = (name, atk["name"], tuple(atk.get("cost") or []))
                if key in seen_attacks:
                    continue
                seen_attacks.add(key)
                cost = atk.get("cost") or []
                per_type = defaultdict(int)
                for c in cost:
                    # "Free" is the game's 0-cost marker, not a real Energy
                    # type -- it requires nothing attached at all.
                    if c not in ("Colorless", "Free"):
                        per_type[c] += 1
                if per_type:
                    reqs.append((name, atk["name"], cost, dict(per_type)))
    return reqs


def scan_attack_gating_abilities(deck_lines, cards_by_name):
    hits = []
    seen = set()
    for count, name in deck_lines:
        matches = cards_by_name.get(name)
        if not matches or matches[0].get("supertype") != "Pokémon":
            continue
        for card in matches:
            for ab in card.get("abilities") or []:
                text = ab.get("text") or ""
                if re.search(r"can'?t attack unless|can'?t use this attack unless|can'?t attack if", text, re.IGNORECASE):
                    key = (name, ab["name"])
                    if key in seen:
                        continue
                    seen.add(key)
                    hits.append((name, ab["name"], text))
    return hits


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1]).read()
    deck_lines = parse_decklist(src)
    if not deck_lines:
        print("No decklist lines recognized (expected lines like '4 Card Name SET 123').")
        sys.exit(1)

    cards = load_cards()
    cards_by_name = defaultdict(list)
    for c in cards:
        cards_by_name[c["name"]].append(c)

    unmatched = [name for _, name in deck_lines if name not in cards_by_name and "Energy" not in name]
    supply = energy_type_supply(deck_lines, cards_by_name)
    reqs = attack_requirements(deck_lines, cards_by_name)
    gating = scan_attack_gating_abilities(deck_lines, cards_by_name)

    print("===== Energy-type support check =====")
    print(f"Deck's total Energy-by-type supply: {dict(supply) if supply else '(no Energy cards recognized)'}\n")

    impossible, tight, ok = [], [], []
    for pkmn, atk_name, cost, per_type in reqs:
        for t, need in per_type.items():
            have = supply.get(t, 0)
            entry = f"{pkmn} -- {atk_name} ({'/'.join(cost)}) needs {need}x {t}, deck has {have}x {t}-providing Energy"
            if have < need:
                impossible.append(entry)
            elif have == need:
                tight.append(entry)
            else:
                ok.append(entry)

    if impossible:
        print(f"IMPOSSIBLE -- can never be paid ({len(impossible)}):")
        for e in impossible:
            print(f"  {e}")
        print()
    if tight:
        print(f"TIGHT -- exactly enough, zero spare copies ({len(tight)}):")
        for e in tight:
            print(f"  {e}")
        print()
    if not impossible and not tight:
        print("No energy-type shortfalls found across every attack checked.\n")

    print(f"===== Attack-gating Ability scan =====")
    if gating:
        print(f"Found {len(gating)} Ability(ies) that may block attacking entirely -- verify the")
        print("condition is actually satisfiable by the rest of this decklist:\n")
        for name, ab_name, text in gating:
            print(f"  {name} -- {ab_name}: {text}")
    else:
        print("No 'can't attack unless...'-style Ability text found.")
    print()

    if unmatched:
        print(f"===== Names not found in pokemon_standard_cards.json ({len(unmatched)}) =====")
        print("(Check spelling/printing -- or this may be a real gap, see the project's")
        print(" established practice of verifying against the live API before assuming so.)")
        for n in unmatched:
            print(f"  {n}")


if __name__ == "__main__":
    main()
