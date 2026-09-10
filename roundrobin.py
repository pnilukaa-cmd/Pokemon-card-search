"""Full N x N round robin over a field of decklists.

One run per unordered pair -- run_game picks who goes first at random, so
the matchup is symmetric and B's rate is 1 - A's. Each pair gets its own
deterministic seed (common random numbers), so a re-run with the same
field reproduces exactly and two fields are comparable.
"""
import sys, os, glob, json, random, hashlib, itertools
sys.path.insert(0, '/home/user/Pokemon-card-search')
import simulate_versus as SV
import tcg_model as M

field, out_path, shard, nshards, games = (
    sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
tag = sys.argv[6] if len(sys.argv) > 6 else "rr1"

files = sorted(glob.glob(os.path.join(field, "*.txt")))
names = [os.path.splitext(os.path.basename(f))[0] for f in files]

_cards = M.load_cards()
by_name, by_setnum = M.build_card_index(_cards)


def basics_in(path):
    n = 0
    for e in M.parse_decklist_entries(open(path).read()):
        c, _ = M.resolve_card(e, by_name, by_setnum)
        if c and (c.get("supertype") == "Pokémon" or M.fossil_stats(c)) \
                and M.stage_of(c) == "Basic":
            n += e["count"]
    return n


playable = {n: basics_in(f) > 0 for n, f in zip(names, files)}
models = {}
for n, f in zip(names, files):
    if playable[n]:
        models[n] = SV.load_model(f, n)[0]

pairs = [p for p in itertools.combinations([n for n in names if playable[n]], 2)]
mine = [p for i, p in enumerate(pairs) if i % nshards == shard]

res = {}
for a, b in mine:
    seed = int(hashlib.sha256(f"{tag}|{a}|{b}".encode()).hexdigest()[:12], 16)
    random.seed(seed)
    wins = 0
    A = (a,) + models[a][1:]
    B = (b,) + models[b][1:]
    for _ in range(games):
        if SV.run_game(A, B)["winner"] == a:
            wins += 1
    res[f"{a}|{b}"] = wins
json.dump({"games": games, "results": res,
           "unplayable": [n for n in names if not playable[n]]},
          open(out_path, "w"))
print(f"shard {shard}: {len(mine)} pairs done")
