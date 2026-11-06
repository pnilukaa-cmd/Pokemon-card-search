"""What a deck actually does: every action line of its own, per game.
tally.py DECK GAMES_PER_OPP opp1.txt opp2.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
cnt, wins, n = collections.Counter(), 0, 0
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(1000 + i)
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        n += 1; wins += r["winner"] == "me"
        for ln in buf.getvalue().splitlines():
            s = ln.strip()
            if s.startswith("me: ") or s.startswith("checkup: me"):
                s = re.sub(r"\d+", "N", s[4:] if s.startswith("me: ") else s)
                s = re.split(r" -> | for N| at N| \(", s)[0]
                cnt[s[:70]] += 1
print(f"wins {wins} / {n}")
for k, v in cnt.most_common(200):
    print(f"  {v / n:5.2f} {k}")
