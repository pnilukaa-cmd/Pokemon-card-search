"""Per-deck markdown table: every candidate tested, panel and full-field diffs."""
import json, sys, collections, math
S = "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad"
F = json.load(open(f"{S}/dlr2/fit.json"))
def load(path):
    R = collections.defaultdict(dict)
    for l in open(path):
        r = json.loads(l); R[r["deck"]][r["opp"]] = 100.0 * r["wins"] / r["games"]
    return R
def diff(R, base, var):
    if var not in R or base not in R: return None
    c = [o for o in R[var] if o in R[base]]
    if len(c) < 4: return None
    d = [R[var][o] - R[base][o] for o in c]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m, sd / math.sqrt(len(d))
P = load(f"{S}/dlr2/screen.jsonl"); C = load(f"{S}/dlr2/confirm.jsonl")
NAMES = {"aarune": "Aarune", "vest": "Custom Vest", "pyroduct": "Pyroduct", "darkrai": "Darkrai",
         "raikou": "Raikou ex", "heat_rotom": "Heat Rotom ex", "wishiwashi": "Wishiwashi ex",
         "giratina": "Giratina"}
rows = []
for deck in sorted(F):
    cells = []
    for c, x in F[deck].items():
        if c.startswith("_") or not isinstance(x, dict):
            continue
        p = diff(P, deck, f"{deck}__{c}")
        f = diff(C, deck, f"{deck}__{c}")
        s = f"{NAMES[c]} {p[0]:+.1f}" if p else f"{NAMES[c]} ?"
        if f:
            s += f" (field {f[0]:+.1f})"
        cells.append(s)
    base = sum(P[deck].values()) / len(P[deck]) if deck in P else float("nan")
    rows.append(f"| `{deck}` | {base:.0f}% | {'; '.join(cells)} |")
print("| Deck | Panel win % | Candidate: panel change (full field) |")
print("|---|---|---|")
print("\n".join(rows))
