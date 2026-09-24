"""Card-conservation audit: every card is somewhere, exactly once.

Plays random field pairings and checks, around every major step of a turn
and every executed IR action, that each player's card total (hand, deck,
discard, Prizes, Stadium, and every Pokemon in play with its Evolution
stack, Energy and Tool) is unchanged. Any step that creates or destroys a
card is reported with the step and the change.

Usage:  python3 audit_conservation.py [games_per_deck] [seed]
"""
import collections
import functools
import glob
import random
import sys

import ability_engine as AE
import simulate_versus as SV
import tcg_model as M


def held(p):
    n = len(p.hand) + len(p.deck) + len(p.discard) + len(getattr(p, "prize_cards", []) or [])
    for s in p.in_play():
        n += 1 + len(getattr(s, "under", []) or []) + len(s.energy_names or []) \
            + (1 if s.tool else 0)
    return n + (1 if p.stadium else 0)


STEPS = ("play_basics", "play_items", "play_supporter", "use_abilities", "use_stadium",
         "sweep_knocked_out", "attach_energy", "attach_tools", "try_evolve",
         "try_retreat", "do_attack", "finish_turn", "end_of_turn")


def audit(games_per_deck=3, seed=1, decks="decks/field/*.txt"):
    """{(step, (delta_first, delta_second)): count} -- empty when clean."""
    SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
    players, bad = [], collections.Counter()
    saved = []

    def wrap(mod, name, label=None):
        f = getattr(mod, name)
        saved.append((mod, name, f))

        @functools.wraps(f)
        def w(*a, **k):
            b = tuple(held(p) for p in players)
            r = f(*a, **k)
            d = tuple(x - y for x, y in zip((held(p) for p in players), b))
            if any(d):
                bad[(label(a) if label else name, d)] += 1
            return r
        setattr(mod, name, w)

    wrap(AE, "apply_action", lambda a: "op:" + str(getattr(a[0].op, "value", a[0].op)))
    wrap(AE, "activate", lambda a: "ability:" + a[0].name)
    for fn in STEPS:
        wrap(SV, fn)
    init = SV.Player.__init__

    def pinit(self, *a, **k):
        init(self, *a, **k)
        players.append(self)
        del players[:-2]
    SV.Player.__init__ = pinit
    try:
        models = [SV.load_model(f, f.split("/")[-1][:-4])[0] for f in sorted(glob.glob(decks))]
        random.seed(seed)
        for A in models:
            for _ in range(games_per_deck):
                B = random.choice(models)
                if B[0] != A[0]:
                    SV.run_game(A, B)
    finally:
        SV.Player.__init__ = init
        for mod, name, f in saved:
            setattr(mod, name, f)
    return bad


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    s = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    bad = audit(n, s)
    for k, v in bad.most_common():
        print(v, k)
    print("clean" if not bad else f"{sum(bad.values())} conservation breaks")
