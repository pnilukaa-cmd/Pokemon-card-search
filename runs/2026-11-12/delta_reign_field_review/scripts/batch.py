"""Many candidate decks against one opponent panel, in one process pool.

Seeds exactly as vs_field.py (sha256 of "tag|opponent"), so a variant and
its base deck face the same dice and their difference is paired.
Usage: batch.py <games> <tag> <out.jsonl> <panel.txt|field> deck.txt ...
A result line per (deck, opponent) is appended to out.jsonl, so a run can
be resumed: pairs already in the file are skipped."""
import sys, os, json, hashlib, random, glob
R = "/home/user/Pokemon-card-search"
sys.path.insert(0, R); os.chdir(R)
import simulate_versus as SV, tcg_model as M
games, tag, out, panel = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
decks = sys.argv[5:]
_cards = M.load_cards()
SV._CARDS_BY_NAME.update(M.build_card_index(_cards)[0])
SV.RETALIATE_CARDS = SV.build_retaliate_index(_cards)
if panel == "field":
    opps = [os.path.basename(f)[:-4] for f in sorted(glob.glob(f"{R}/decks/field/*.txt"))]
else:
    opps = [x.strip() for x in open(panel) if x.strip()]
done = set()
if os.path.exists(out):
    for ln in open(out):
        r = json.loads(ln); done.add((r["deck"], r["opp"]))
_models = {}
def model(path, label):
    k = (path, label)
    if k not in _models:
        _models[k] = SV.load_model(path, label)[0]
    return _models[k]
def base_of(deck):
    return os.path.basename(deck)[:-4].split("__")[0]
def play(job):
    deck, opp = job
    me = base_of(deck)
    A = model(deck, me)
    B = model(f"{R}/decks/field/{opp}.txt", opp)
    if opp == me:
        B = (opp + "_opp",) + B[1:]
    random.seed(int(hashlib.sha256(f"{tag}|{opp}".encode()).hexdigest()[:12], 16))
    SV._LOOKAHEAD_SEQ[0] = 0
    w = sum(SV.run_game(A, B)["winner"] == A[0] for _ in range(games))
    return os.path.basename(deck)[:-4], opp, w
jobs = [(d, o) for d in decks for o in opps
        if o != base_of(d) and (os.path.basename(d)[:-4], o) not in done]
import multiprocessing as mp
with mp.get_context("fork").Pool(4) as pool, open(out, "a") as fh:
    for name, opp, w in pool.imap_unordered(play, jobs, chunksize=2):
        fh.write(json.dumps({"deck": name, "opp": opp, "wins": w, "games": games}) + "\n"); fh.flush()
print("DONE", len(jobs))
