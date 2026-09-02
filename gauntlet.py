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
import concurrent.futures as cf
import glob
import hashlib
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


def _run_matchup(me, opp_path, games, seed, mine):
    cmd = [sys.executable, "simulate_versus.py", me, opp_path, games]
    if seed:
        cmd.append(seed)
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.search(r"^\s+" + re.escape(mine) + r"\s+\d+ wins\s+\(\s*([\d.]+)%\)",
                  out, re.M)
    return float(m.group(1)) if m else None


def engine_revision():
    """Short fingerprint of the code that produced a result.

    A deck file's win rate is only comparable to another measured on the
    same engine, and this project has repeatedly published numbers that
    silently predated a fix. Stamping the run makes a stale figure
    visible instead of merely wrong.
    """
    h = hashlib.sha256()
    for f in sorted(("simulate_versus.py", "ability_engine.py",
                     "ability_ir.py", "tcg_model.py")):
        try:
            h.update(open(f, "rb").read())
        except OSError:
            pass
    return h.hexdigest()[:10]


def main():
    me, folder = sys.argv[1], sys.argv[2]
    games = sys.argv[3] if len(sys.argv) > 3 else "150"
    # A4: --seed=N makes the whole gauntlet reproducible. Without it the
    # mean moved about a point between identical runs, which is the same
    # size as most of the changes being measured.
    seed = next((a for a in sys.argv if a.startswith("--seed=")), None)
    mine = os.path.splitext(os.path.basename(me))[0]

    rows, unplayable, jobs = [], [], []
    for f in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        opp = os.path.splitext(os.path.basename(f))[0]
        if opp == mine or os.path.abspath(f) == os.path.abspath(me):
            continue
        if basics_in(f) == 0:
            unplayable.append(opp)
            continue
        jobs.append((f, opp))

    # Every matchup is an independent process, so run them across the
    # available cores. This was the binding constraint on precision: at
    # 150 games the standard error is ~1%, and the only way to resolve the
    # changes an optimiser actually proposes is more games -- which was
    # unaffordable serially.
    workers = max(1, min(len(jobs), (os.cpu_count() or 1)))
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_run_matchup, me, f, games, seed, mine): opp
                   for f, opp in jobs}
        for fut in cf.as_completed(futures):
            pct = fut.result()
            if pct is not None:
                rows.append((pct, futures[fut]))

    rows.sort(reverse=True)
    stamp = engine_revision()
    print(f"{mine} vs {len(rows)} saved decks, {games} games each"
          f"{' seed ' + seed.split('=')[1] if seed else ''}")
    import math
    n = int(games)
    se = 100.0 * math.sqrt(0.25 / max(n, 1))
    print(f"engine {stamp}   ({workers} workers, 1 s.e. per matchup "
          f"= {se:.1f}% at {n} games)\n")
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
