#!/usr/bin/env python3
"""Evaluate EVERY ex Pokemon's attacks in a controlled board state.

The IR's "no rule matched" does not mean the damage is lost -- attack_damage()
is a separate path. This asks the question that actually matters: given a
known board, what number does the simulator produce, and is it the number
the card says?

Board it builds (identical for every card, so numbers are comparable):
  me:  the ex Active with 4 Energy attached (2 of its own type, 2 Psychic)
       and 30 damage on it; 3 Benched Pokemon, 2 of them damaged
  opp: a 200 HP Active with 2 Energy and 50 damage; 4 Benched, 2 damaged
  my hand 5 cards, my discard 6 Energy, opponent has taken 2 Prizes
"""
import re
import sys

import simulate_versus as SV
import tcg_model as M


def build_board(card, cards_by_name):
    name = card["name"]
    POK = {}
    POK[name] = M.build_pokemon_info(card)
    filler = cards_by_name["Dunsparce"]
    filler = filler[0] if isinstance(filler, list) else filler
    POK["Dunsparce"] = M.build_pokemon_info(filler)
    wall = cards_by_name["Mega Heracross ex"]
    wall = wall[0] if isinstance(wall, list) else wall
    POK["Mega Heracross ex"] = M.build_pokemon_info(wall)

    deck = [("Pokemon", "Dunsparce")] * 10 + [("Energy", "Psychic Energy")] * 10
    me = SV.Player("A", POK, list(deck), {})
    op = SV.Player("B", POK, list(deck), {})

    my_type = (POK[name]["types"] or ["Colorless"])[0]
    a = SV.InPlay(name, 0)
    a.energy = [[my_type], [my_type], ["Psychic"], ["Psychic"]]
    a.damage = 30
    me.active = a
    me.bench = []
    for i in range(3):
        b = SV.InPlay("Dunsparce", 0)
        b.damage = 20 if i < 2 else 0
        b.energy = [["Psychic"]]
        me.bench.append(b)
    me.hand = [("Item", "Ultra Ball")] * 5
    me.discard = ["Psychic Energy"] * 6

    oa = SV.InPlay("Mega Heracross ex", 0)
    oa.energy = [["Grass"], ["Grass"]]
    oa.damage = 50
    op.active = oa
    op.bench = []
    for i in range(4):
        b = SV.InPlay("Dunsparce", 0)
        b.damage = 20 if i < 2 else 0
        op.bench.append(b)
    op.prizes = SV.STARTING_PRIZES - 2
    op.hand = [("Item", "Ultra Ball")] * 4
    return me, op, a


TYPED_ENERGY = re.compile(
    r"for each (Grass|Fire|Water|Lightning|Psychic|Fighting|Darkness|Metal|"
    r"Dragon|Fairy|Colorless) Energy", re.I)
FILTERED_BENCH = re.compile(
    r"for each of your (?:Benched )?Pok[eé]mon that ", re.I)


def main():
    cards = M.load_cards()
    by_name, _ = M.build_card_index(cards)
    SV._CARDS_BY_NAME.update(by_name)
    ex, seen = [], set()
    for c in cards:
        st = c.get("subtypes") or []
        if c.get("supertype") != "Pokémon" or not ("ex" in st or "MEGA" in st):
            continue
        if c["name"] in seen:
            continue
        seen.add(c["name"])
        ex.append(c)
    ex.sort(key=lambda c: c["name"])

    rows = []
    for c in ex:
        try:
            me, op, spot = build_board(c, by_name)
        except Exception as exc:
            rows.append((c["name"], "-", "-", f"BOARD ERROR {exc!r}", ""))
            continue
        for atk in M.build_pokemon_info(c)["attacks"]:
            text = atk.get("text") or ""
            SV.UNSCORED_ATTACKS.clear()
            try:
                dmg = SV.attack_damage(me, op, spot, atk)
            except Exception as exc:
                rows.append((c["name"], atk["name"], atk.get("damage"),
                             f"RAISED {exc!r}", text))
                continue
            flags = []
            if SV.UNSCORED_ATTACKS:
                flags.append("UNSCORED")
            if TYPED_ENERGY.search(text):
                flags.append("TYPED-ENERGY-SCALER")
            if FILTERED_BENCH.search(text):
                flags.append("FILTERED-COUNT")
            rows.append((c["name"], atk["name"], atk.get("damage"),
                         dmg, text, flags))
    return rows, ex


if __name__ == "__main__":
    rows, ex = main()
    want = sys.argv[1] if len(sys.argv) > 1 else None
    import collections
    flagged = collections.Counter()
    for r in rows:
        if len(r) < 6:
            print("  ", r)
            continue
        name, an, base, dmg, text, flags = r
        for f in flags:
            flagged[f] += 1
        if want and want not in flags:
            continue
        if want:
            print(f"  {name} / {an}: printed {base!r} -> sim {dmg}")
            print(f"      {text[:140]}")
    print(f"\nex cards: {len(ex)}   attacks evaluated: {len(rows)}")
    for f, n in flagged.most_common():
        print(f"  {n:4d}  {f}")
