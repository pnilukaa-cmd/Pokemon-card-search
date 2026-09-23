"""Put the new field numbers at the top of every deck file, once."""
import json, os, re, glob

REPO = os.path.dirname(os.path.abspath(__file__))
# Run output lives in the repo, not a session scratchpad: the scratchpad
# is deleted with the container, and the 2026-09-15 shards went with it.
SP = os.environ.get("RUNS_DIR", os.path.join(REPO, "runs"))
import sys
RUN = os.path.join(SP, sys.argv[1]) if len(sys.argv) > 1 else SP
d = json.load(open(os.path.join(RUN, "field_summary.json")))
stamp, games, summary = d["stamp"], d["games"], d["summary"]
order = sorted(summary, key=lambda n: -summary[n]["mean"])
rank = {n: i + 1 for i, n in enumerate(order)}

MARK = "<!-- field-results -->"
patched = skipped = 0
for md in sorted(glob.glob(os.path.join(REPO, "decks", "*.md"))):
    slug = os.path.basename(md)[:-3]
    if slug in ("FIELD_RESULTS", "snow_coating_verdict"):
        continue
    text = open(md).read()
    s = summary.get(slug)
    if s is None:
        skipped += 1
        print("  no field entry:", slug)
        continue
    best = eval(s["best"]) if isinstance(s["best"], str) else s["best"]
    worst = eval(s["worst"]) if isinstance(s["worst"], str) else s["worst"]
    block = (
        f"{MARK}\n"
        f"> ### Field results — {stamp}\n"
        f"> **{s['mean']:.1f}% mean · {s['median']:.1f}% median · "
        f"{s['winning']} of {s['played']} winning matchups · "
        f"rank {rank[slug]} of {len(order)}**\n"
        f">\n"
        f"> Best `{best[0]}` {best[1]:.0f}% · worst `{worst[0]}` "
        f"{worst[1]:.0f}%.\n"
        f">\n"
        f"> Full round robin, {games} games per pairing, every deck against "
        f"every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win "
        f"rate written in the body below this box predates {stamp}** and "
        f"was measured against a different field or engine.\n"
        f"{MARK}\n"
    )
    # strip any previous block, then insert after the H1
    text = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK) + r"\n", "",
                  text, flags=re.S)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            lines.insert(i + 1, "\n" + block)
            break
    else:
        lines.insert(0, block)
    open(md, "w").write("\n".join(lines))
    patched += 1
print(f"patched {patched} deck files, {skipped} with no field entry")
