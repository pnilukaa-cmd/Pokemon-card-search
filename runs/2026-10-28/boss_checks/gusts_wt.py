"""How a deck's Boss's Orders plays out: per gust, was the dragged-up
Pokemon Knocked Out that same turn, and what Supporter was given up.
gusts.py DECK GAMES opp1.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad/wt_td"); os.chdir("/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad/wt_td")
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
st = collections.Counter()
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(2000 + i)
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            SV.run_game(A, B, verbose=True)
        turn, gust = [], None
        for ln in buf.getvalue().splitlines() + ["-- end"]:
            if ln.startswith("--"):
                if gust:
                    st["gusts"] += 1
                    ko = any(f"KO on {gust}" in t for t in turn)
                    st["gust_ko"] += ko
                    held = [t for t in turn if "me: " in t and ("Lillie" in t or "Hilda" in t or "Jacinthe" in t)]
                gust, turn = None, []
                continue
            turn.append(ln)
            m = re.search(r"me: Boss's Orders -> drags up (.+)$", ln.strip())
            if m:
                gust = m.group(1).strip()
        st["games"] += 1
g = st["games"]
print(f"{os.path.basename(deck)}: {st['gusts']/g:.2f} Boss's Orders a game; "
      f"the dragged-up Pokemon Knocked Out that turn in {100*st['gust_ko']/max(st['gusts'],1):.0f}%")
