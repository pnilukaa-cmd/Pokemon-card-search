"""Energy on the board, turn by turn, for one deck against a field.

A decklist says "14 Energy" and nothing about whether the Energy reaches
the board. This plays the deck through the full engine -- Abilities,
attacks and Trainers that attach, and Abilities like Meganium's Wild
Growth that make one card provide more -- and at the end of each of the
deck's own turns records:

  * the Energy its Pokemon in play provide, in total and on the Active;
  * whether the Active could pay for an attack (and so attack next turn
    if it survives);
  * the Energy cards left in hand.

Same per-opponent seeding as vs_field.py, so two lists run on the same tag
see the same dice.

Usage:  python3 energy_curve.py <deck.txt> <field_dir> <games> [turns] [tag]

JOBS=<n> plays the opponents on n processes. PILOT=<name> runs the deck
under that pilot, as in vs_field.py.
"""
import glob
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulate_versus as SV

deck, field, games = sys.argv[1], sys.argv[2], int(sys.argv[3])
turns = int(sys.argv[4]) if len(sys.argv) > 4 else 6
tag = sys.argv[5] if len(sys.argv) > 5 else "ec1"

me = os.path.splitext(os.path.basename(deck))[0]
A = SV.load_model(deck, me)[0]
if os.environ.get("PILOT"):
    SV.PILOT_BY_NAME[me] = os.environ["PILOT"]

_finish = SV.finish_turn


def _can_pay(pl, spot, opp):
    return any(SV.can_pay(SV.effective_cost(pl, spot, a["cost"], opp, a.get("name")),
                          SV.provided(pl, spot))
               for a in (pl.POKEMON.get(spot.name) or {}).get("attacks") or [])


def _record(pl, opp, log):
    # Not the lookahead's played-out copies of the game.
    if pl.name == me and not SV._LOOKAHEAD[0]:
        k = getattr(pl, "_ec_turn", 0) + 1
        pl._ec_turn = k
        if k <= turns:
            rows = pl._ec_rows
            rows.append((k,
                         sum(len(SV.provided(pl, s)) for s in pl.in_play()),
                         len(SV.provided(pl, pl.active)) if pl.active else 0,
                         bool(pl.active) and _can_pay(pl, pl.active, opp),
                         sum(1 for c, _ in pl.hand if c == "Energy")))
    return _finish(pl, opp, log)


SV.finish_turn = _record
_new_player = SV.Player


class _Player(_new_player):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._ec_rows = _ROWS


SV.Player = _Player
_ROWS = []


def play(f):
    opp = os.path.splitext(os.path.basename(f))[0]
    B = SV.load_model(f, opp)[0]
    if opp == me:
        B = (opp + "_opp",) + B[1:]
    random.seed(int(hashlib.sha256(f"{tag}|{opp}".encode()).hexdigest()[:12], 16))
    SV._LOOKAHEAD_SEQ[0] = 0
    del _ROWS[:]
    for _ in range(games):
        SV.run_game(A, B)
    return list(_ROWS)


todo = [f for f in sorted(glob.glob(os.path.join(field, "*.txt")))
        if os.path.abspath(f) != os.path.abspath(deck)]
jobs = int(os.environ.get("JOBS", "1"))
rows = []
if jobs > 1:
    import multiprocessing as mp
    with mp.get_context("fork").Pool(jobs) as pool:
        for r in pool.imap(play, todo):
            rows.extend(r)
else:
    for f in todo:
        rows.extend(play(f))

print(f"{me}: {games} games against each of {len(todo)} decks, "
      f"at the end of each of its own turns")
print(f"{'turn':>4} {'games':>6} {'in play':>8} {'Active':>7} {'can attack':>11} {'in hand':>8}")
for k in range(1, turns + 1):
    rs = [r for r in rows if r[0] == k]
    if not rs:
        break
    n = len(rs)
    print(f"{k:>4} {n:>6} {sum(r[1] for r in rs) / n:>8.2f} {sum(r[2] for r in rs) / n:>7.2f}"
          f" {100.0 * sum(r[3] for r in rs) / n:>10.1f}% {sum(r[4] for r in rs) / n:>8.2f}")
