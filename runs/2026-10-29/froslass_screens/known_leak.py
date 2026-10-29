"""Hand-coded Supporters that still got played off their card text."""
import contextlib, io, os, random, re, sys, glob, collections
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
decks = sorted(glob.glob("decks/field/*.txt"))
models = {d: SV.load_model(d, "me")[0] for d in decks}
opp = {d: SV.load_model(d, "opp")[0] for d in decks}
rx = re.compile(r"^\s*(?:me|opp): (.+?) \(from card text\)")
cnt, tot, games = collections.Counter(), collections.Counter(), 0
random.seed(1)
for i, d in enumerate(decks):
    for j in range(int(sys.argv[1])):
        o = decks[(i * 7 + j * 13 + 1) % len(decks)]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            SV.run_game(models[d], opp[o], verbose=True)
        games += 1
        for ln in buf.getvalue().splitlines():
            m = rx.search(ln)
            if m:
                tot[m.group(1)] += 1
                if m.group(1) in SV.KNOWN_TRAINERS: cnt[m.group(1)] += 1
print("games", games)
print("hand-coded names played off card text:", cnt.most_common())
