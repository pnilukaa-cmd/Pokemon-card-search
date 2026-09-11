#!/usr/bin/env python3
"""What does the field table look like with some decks removed as opponents?

A deck the pilot cannot drive is a free win for everyone else, and a free
win that every deck shares inflates the whole table rather than any part
of it. This answers the question directly instead of by intuition: drop a
deck from every other deck's OPPONENT list and re-rank.

It was written to check a specific suspicion -- that the top of the field
was propped up by beating meta_ns_zoroark, which places last and whose own
file explains why. The suspicion was wrong, and that is the useful part:
removing it costs every deck between 0.4 and 1.4 points, costs the top
three LEAST of all, and leaves ranks 1-18 completely unchanged. A deck
that loses to everything is worth about a point to everyone and slightly
less to the decks already beating everything, because their mean has less
room to move.

Reads the same shard JSON the field table is built from, so it never
re-simulates anything.

Usage:  python3 field_exclude.py <shard-dir> [deck ...]
"""
import glob
import json
import os
import statistics
import sys


def load(shard_dir):
    wins, games = {}, None
    for f in sorted(glob.glob(os.path.join(shard_dir, "rr_[0-9]*.json"))):
        d = json.load(open(f))
        games = d["games"]
        wins.update(d["results"])
    if not wins:
        sys.exit(f"no rr_*.json shards in {shard_dir}")
    return wins, games


def rates(wins, games):
    out = {}
    for k, w in wins.items():
        a, b = k.split("|")
        out.setdefault(a, {})[b] = 100.0 * w / games
        out.setdefault(b, {})[a] = 100.0 * (games - w) / games
    return out


def summarise(rate, drop):
    return {n: statistics.mean(v for b, v in opp.items() if b not in drop)
            for n, opp in rate.items() if n not in drop}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip().splitlines()[-1])
    shard_dir = sys.argv[1]
    drop = set(sys.argv[2:]) or {"meta_ns_zoroark"}
    rate = rates(*load(shard_dir))
    missing = drop - set(rate)
    if missing:
        sys.exit(f"not in this field: {', '.join(sorted(missing))}")

    full, cut = summarise(rate, set()), summarise(rate, drop)
    rank_full = {n: i + 1 for i, n in enumerate(sorted(full, key=lambda n: -full[n]))}
    rank_cut = {n: i + 1 for i, n in enumerate(sorted(cut, key=lambda n: -cut[n]))}

    print(f"Dropping {', '.join(sorted(drop))} as an opponent "
          f"({len(cut)} decks, {len(cut) - 1} opponents each)\n")
    print(f"  {'deck':46s} {'with':>6s} {'without':>8s} {'delta':>7s}   rank")
    moved = 0
    for n in sorted(cut, key=lambda n: cut[n] - full[n]):
        shift = rank_full[n] != rank_cut[n]
        moved += shift
        print(f"  {n:46s} {full[n]:5.1f}% {cut[n]:7.1f}% "
              f"{cut[n] - full[n]:+6.2f}   {rank_full[n]:2d} -> {rank_cut[n]:2d}"
              f"{'  <<' if shift else ''}")
    deltas = [cut[n] - full[n] for n in cut]
    print(f"\n  every deck moves by {min(deltas):+.2f} to {max(deltas):+.2f} points; "
          f"{moved} of {len(cut)} change rank")


if __name__ == "__main__":
    main()
