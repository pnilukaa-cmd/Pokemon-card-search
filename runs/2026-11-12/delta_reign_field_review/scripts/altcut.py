"""The same addition with a second cut: the standard cut's first card is
kept, and the cut comes from the next cards in the same order."""
import json, subprocess, sys
S = "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad"
R = "/home/user/Pokemon-card-search"
sys.path.insert(0, f"{S}/dlr2")
import importlib.util
spec = importlib.util.spec_from_file_location("fitmod", f"{S}/dlr2/fit.py")
P = json.load(open(f"{S}/dlr2/profile.json"))
F = json.load(open(f"{S}/dlr2/fit.json"))
src = open(f"{S}/dlr2/fit.py").read().split("fit = {}")[0]
ns = {}; exec(src, ns)
D = json.load(open(f"{S}/dlr2/screen_diffs.json"))
hits = [x for x in D if x["diff"] >= 2.0]
made = 0
for x in hits:
    deck, cand = x["base"], x["cand"]
    line, k, kind = ns["CANDS"][cand]
    std = F[deck][cand]["cut"]
    first = std[0].split(" ", 1)[1]
    d = json.loads(json.dumps(P[deck]))
    d["trainers"] = [t for t in d["trainers"] if t["raw"] != first]
    cut = ns["cuts_for"](d, kind, k)
    if cut is None:
        print("no alt cut", deck, cand); continue
    out = f"{S}/dlr2/alt/{deck}__{cand}_alt.txt"
    args = [f"{line}:+{k}"] + [f"{raw}:-{n}" for raw, n in cut]
    r = subprocess.run([sys.executable, ns["VARIANT"], f"{R}/decks/field/{deck}.txt", out] + args,
                       capture_output=True, text=True, cwd=R)
    if r.returncode:
        print("fail", deck, cand, r.stderr[-150:]); continue
    F[deck][cand]["alt_cut"] = [f"{n} {raw}" for raw, n in cut]
    made += 1
json.dump(F, open(f"{S}/dlr2/fit.json", "w"), indent=1, ensure_ascii=False)
print("alt variants", made)
