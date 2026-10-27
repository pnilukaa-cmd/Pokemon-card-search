import json, statistics, sys
a = json.load(open(sys.argv[1])); g = a["games"]; r = {k: 100 * v / g for k, v in a["results"].items()}
b = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
rb = {k: 100 * v / b["games"] for k, v in b["results"].items()} if b else {}
print(f"mean {statistics.mean(r.values()):.2f} median {statistics.median(r.values()):.1f} winning {sum(v > 50 for v in r.values())}/{len(r)}")
s = sorted(r, key=r.get)
fmt = lambda k: f"  {k:52s} {r[k]:5.1f}" + (f"  (was {rb[k]:5.1f})" if k in rb else "")
print("worst:"); [print(fmt(k)) for k in s[:9]]
print("best:"); [print(fmt(k)) for k in s[-5:]]
meta = [k for k in r if k.startswith("meta_")]
print("meta:"); [print(fmt(k)) for k in sorted(meta, key=r.get, reverse=True)]
