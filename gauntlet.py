#!/usr/bin/env python3
"""Play one decklist against EVERY other saved deck and print a table.

Why this exists: opponents were being picked three or four at a time, by
hand, which quietly hid both tails of the distribution and made two
different decks' numbers non-comparable. Running the whole folder is
cheap and removes the sampling choice entirely.

It also screens the opponents. A deck the simulator cannot actually pilot
inflates everyone's win rate against it: `selective_bloom_cradily` runs
zero Basic Pokemon (its Lileep arrives via `Antique Root Fossil`, an Item
the engine does not model as a Basic), so it mulligans out and loses on
turn 2 every game -- a 100% "matchup" that means nothing. Those decks are
listed separately and left out of the summary.

Usage:  python3 gauntlet.py <my-decklist.txt> <dir-of-decklists> [games]
"""
import glob
import os
import re
import statistics
import subprocess
import sys

import tcg_model as M


_CARDS = None


def basics_in(path):
    """How many Basic Pokemon the sim will actually see in this deck."""
    global _CARDS
    if _CARDS is None:
        _CARDS = M.build_card_index(M.load_cards())
    by_name, by_setnum = _CARDS
    n = 0
    for entry in M.parse_decklist_entries(open(path).read()):
        card, _ = M.resolve_card(entry, by_name, by_setnum)
        if card and card.get("supertype") == "Pokémon" \
                and M.stage_of(card) == "Basic":
            n += entry["count"]
    return n


def main():
    me, folder = sys.argv[1], sys.argv[2]
    games = sys.argv[3] if len(sys.argv) > 3 else "150"
    mine = os.path.splitext(os.path.basename(me))[0]

    rows, unplayable = [], []
    for f in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        opp = os.path.splitext(os.path.basename(f))[0]
        if opp == mine or os.path.abspath(f) == os.path.abspath(me):
            continue
        if basics_in(f) == 0:
            unplayable.append(opp)
            continue
        out = subprocess.run([sys.executable, "simulate_versus.py", me, f, games],
                             capture_output=True, text=True).stdout
        m = re.search(r"^\s+" + re.escape(mine) + r"\s+\d+ wins\s+\(\s*([\d.]+)%\)",
                      out, re.M)
        if m:
            rows.append((float(m.group(1)), opp))

    rows.sort(reverse=True)
    print(f"{mine} vs {len(rows)} saved decks, {games} games each\n")
    for pct, opp in rows:
        flag = "  <- check, near-total result" if pct >= 95 or pct <= 5 else ""
        print(f"  {pct:5.1f}%  {opp:48}{'#' * int(pct / 2)}{flag}")

    vals = [p for p, _ in rows]
    if vals:
        print(f"\n  mean {statistics.mean(vals):.1f}%   "
              f"median {statistics.median(vals):.1f}%   "
              f"winning matchups {sum(1 for v in vals if v > 50)}/{len(vals)}")
    if unplayable:
        print("\n  excluded -- no Basic Pokemon the engine can put into play "
              "(e.g. Fossil decks), so they mulligan out and lose on turn 2:")
        for u in unplayable:
            print(f"    {u}")


if __name__ == "__main__":
    main()
