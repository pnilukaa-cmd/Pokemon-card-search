"""Share of a deck's own turns (from turn 3) with each named Pokemon in play,
and with a Mega Froslass ex that can attack. inplay.py DECK GAMES NAMES opp..."""
import os, sys, random, collections, contextlib, io
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, names, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(","), sys.argv[4:]
A = SV.load_model(deck, "me")[0]
cnt, turns, rr, wins = collections.Counter(), [0], [0], [0]
orig_fin = SV.finish_turn
def fin(pl, opp, log):
    if pl.name == "me" and pl.round_no >= 3:
        turns[0] += 1
        have = set(n.split(" (")[0] for n in pl.in_play_names())
        for n in names:
            cnt[n] += n in have
        cnt["Snorunt or Mega Froslass ex"] += bool(have & {"Snorunt", "Mega Froslass ex"})
    return orig_fin(pl, opp, log)
SV.finish_turn = fin
n = 0
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(3000 + i)
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        n += 1; wins[0] += r["winner"] == "me"
        out = buf.getvalue()
        rr[0] += out.count("me: Mega Froslass ex uses Resentful Refrain")
        cnt["Mega Froslass ex Knocked Out"] += out.count("KO on Mega Froslass ex")
print(f"wins {wins[0]}/{n}, {turns[0] / n:.1f} own turns from turn 3 a game, Resentful Refrain {rr[0] / n:.2f} a game")
for k in names + ["Snorunt or Mega Froslass ex"]:
    print(f"  {k:30s} in play {cnt[k] / max(1, turns[0]) * 100:5.1f}% of those turns")
print(f"  Mega Froslass ex Knocked Out {cnt['Mega Froslass ex Knocked Out'] / n:.2f} a game")
