"""Paired mean difference between two vs_field JSON outputs (same tag/games)."""
import json, sys, math
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
def rates(d):
    g = int(d["games"])
    return {k: 100.0 * v / g for k, v in d["results"].items()}
ra, rb = rates(a), rates(b)
common = sorted(set(ra) & set(rb))
diffs = [rb[k] - ra[k] for k in common]
n = len(diffs); m = sum(diffs) / n
sd = math.sqrt(sum((x - m) ** 2 for x in diffs) / (n - 1))
print(f"{sys.argv[2].split('/')[-1]} - {sys.argv[1].split('/')[-1]}: {m:+.2f} +/- {sd/math.sqrt(n):.2f} over {n} opponents; better on {sum(x>0 for x in diffs)}, worse on {sum(x<0 for x in diffs)}")
