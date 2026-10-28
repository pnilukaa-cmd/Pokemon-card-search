"""Where a deck's Energy cards are at the end of each of its own turns:
deck, hand, in play, discard, Prize cards. energy_where.py DECK GAMES opp..."""
import os, sys, random, collections
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
tot = collections.defaultdict(lambda: collections.Counter())
n = collections.Counter()
orig = SV.finish_turn
def spy(pl, opp, log):
    if pl.name == "me":
        t = pl.round_no
        isE = lambda c: c[0] == "Energy"
        n[t] += 1
        tot[t]["deck"] += sum(map(isE, pl.deck))
        tot[t]["hand"] += sum(map(isE, pl.hand))
        tot[t]["prizes"] += sum(map(isE, pl.prize_cards))
        tot[t]["in play"] += sum(len(s.energy_names) for s in pl.in_play())
        tot[t]["discard"] += sum(1 for c in pl.discard if isinstance(c, str) and "Energy" in c)
    return orig(pl, opp, log)
SV.finish_turn = spy
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(3000 + i)
    for _ in range(games):
        SV.run_game(A, B)
print(f"{os.path.basename(deck)}  turn: deck / hand / in play / discard / prizes")
for t in sorted(n)[:6]:
    print(f"  {t}: " + " / ".join(f"{tot[t][k]/n[t]:.2f}" for k in ("deck", "hand", "in play", "discard", "prizes")))
