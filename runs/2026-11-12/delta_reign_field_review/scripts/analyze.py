"""Paired variant - base over the opponents both played, from a batch jsonl."""
import json, sys, math, collections
rows = [json.loads(l) for l in open(sys.argv[1])]
R = collections.defaultdict(dict)
for r in rows:
    R[r["deck"]][r["opp"]] = 100.0 * r["wins"] / r["games"]
out = []
for name, res in R.items():
    if "__" not in name:
        continue
    base, cand = name.split("__")
    if base not in R:
        continue
    common = [o for o in res if o in R[base]]
    if len(common) < 4:
        continue
    d = [res[o] - R[base][o] for o in common]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / max(1, len(d) - 1))
    b = sum(R[base][o] for o in common) / len(common)
    out.append((m, base, cand, b, sd / math.sqrt(len(d)), len(d)))
out.sort(reverse=True)
mode = sys.argv[2] if len(sys.argv) > 2 else "top"
if mode == "top":
    for m, base, cand, b, se, n in out[:int(sys.argv[3]) if len(sys.argv) > 3 else 40]:
        print(f"{m:+6.2f} ±{se:4.2f}  {cand:11s} {base[:46]:46s} base {b:5.1f}% (n={n})")
elif mode == "bycand":
    by = collections.defaultdict(list)
    for m, base, cand, b, se, n in out:
        by[cand].append(m)
    for c, xs in sorted(by.items()):
        xs.sort()
        print(f"{c:11s} decks {len(xs):3d}  mean {sum(xs)/len(xs):+5.2f}  median {xs[len(xs)//2]:+5.2f}"
              f"  >+1.5: {sum(x > 1.5 for x in xs):3d}  >+3: {sum(x > 3 for x in xs):3d}  <-1.5: {sum(x < -1.5 for x in xs):3d}")
elif mode == "json":
    json.dump([dict(zip(("diff", "base", "cand", "base_rate", "se", "n"), x)) for x in out],
              open(sys.argv[3], "w"), indent=0)
