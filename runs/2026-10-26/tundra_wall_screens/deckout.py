"""deckout.py LIST GAMES_PER_OPP -- how this deck's games end: its own deck-outs."""
import sys, glob, os, random, hashlib
sys.path.insert(0, '/home/user/Pokemon-card-search'); os.chdir('/home/user/Pokemon-card-search')
import simulate_versus as SV
me = os.path.splitext(os.path.basename(sys.argv[1]))[0]
A = SV.load_model(sys.argv[1], me)[0]
if os.environ.get("PILOT"): SV.PILOT_BY_NAME[me] = os.environ["PILOT"]
n = int(sys.argv[2])
_tt = SV.take_turn
stats = {"games": 0, "my_deckout": 0, "opp_deckout": 0, "wins": 0}
def tt(pl, opp, *a, **k):
    r = _tt(pl, opp, *a, **k)
    if r == "deck_out":
        stats["my_deckout" if pl.name == me else "opp_deckout"] += 1
    return r
SV.take_turn = tt
for f in sorted(glob.glob('decks/field/*.txt')):
    opp = os.path.splitext(os.path.basename(f))[0]
    B = SV.load_model(f, opp)[0]
    random.seed(int(hashlib.sha256(f"dk|{opp}".encode()).hexdigest()[:12], 16))
    for _ in range(n):
        r = SV.run_game(A, B); stats["games"] += 1; stats["wins"] += r["winner"] == me
print(me, stats)
