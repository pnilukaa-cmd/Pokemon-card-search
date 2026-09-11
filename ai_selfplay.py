#!/usr/bin/env python3
"""Mirror-match one pilot against another with the DECK held fixed.

A field win rate cannot tell you whether an AI change is an improvement,
because the change applies to both sides at once. This does: player A runs
one policy, player B runs another, both playing the SAME decklist, so the
only difference between them is the decision-making. Anything meaningfully
above 50% is a better pilot.

Usage:  python3 ai_selfplay.py <folder> [games-per-deck] [polA] [polB]
"""
import glob
import os
import random
import statistics
import sys

import simulate_versus as SV


# Captured ONCE at import. Grabbing it inside mirror() re-wrapped an
# already-wrapped __init__ on the second call and recursed forever.
_REAL_PLAYER_INIT = SV.Player.__init__


def mirror(path, games, pol_a, pol_b, seed=12345):
    model = SV.load_model(path, "A")[0]
    modelb = SV.load_model(path, "B")[0]
    wins = 0

    def patched(self, name, POKEMON, decklist, EFFECTS=None):
        _REAL_PLAYER_INIT(self, name, POKEMON, decklist, EFFECTS)
        self.policy = pol_a if name == "A" else pol_b

    SV.Player.__init__ = patched
    try:
        random.seed(seed)
        for _ in range(games):
            if SV.run_game(model, modelb)["winner"] == "A":
                wins += 1
    finally:
        SV.Player.__init__ = _REAL_PLAYER_INIT
    return wins


def main():
    folder = sys.argv[1]
    games = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    pol_a = sys.argv[3] if len(sys.argv) > 3 else "v2"
    pol_b = sys.argv[4] if len(sys.argv) > 4 else "v1"
    rows = []
    for f in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        name = os.path.splitext(os.path.basename(f))[0]
        # PAIRED: the same deck, the same seed, the only difference being
        # which policy sits in seat A. Subtracting the control run cancels
        # the seat bias (seat A wins 51.6% of v1-vs-v1 mirrors) and most of
        # the shared variance, which is the only way a 1-point effect is
        # visible at this sample size.
        test = mirror(f, games, pol_a, pol_b)
        ctrl = mirror(f, games, pol_b, pol_b)
        rows.append((100.0 * (test - ctrl) / games, name))
    rows.sort(reverse=True)
    for d, name in rows:
        bar = "#" * int(min(abs(d), 30) / 2)
        print(f"  {d:+6.1f}  {name:46s}{bar}")
    vals = [d for d, _ in rows]
    mean = statistics.mean(vals)
    sd = statistics.pstdev(vals) or 1e-9
    se = sd / (len(vals) ** 0.5)
    print(f"\n  {pol_a} minus {pol_b}, paired per deck over {games} games each")
    print(f"  mean {mean:+.2f} points   95% CI [{mean - 1.96 * se:+.2f}, "
          f"{mean + 1.96 * se:+.2f}]   better on {sum(1 for v in vals if v > 0)}"
          f"/{len(vals)} decks")
    verdict = ("IMPROVEMENT" if mean - 1.96 * se > 0 else
               "REGRESSION" if mean + 1.96 * se < 0 else
               "no detectable difference")
    print(f"  -> {verdict}")


if __name__ == "__main__":
    main()
