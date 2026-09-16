"""Put the new field numbers at the top of every deck file, once."""
import json, os, re, glob

SP = "/tmp/claude-0/-home-user-Pokemon-card-search/e648d066-66e0-5170-a656-2af4bb2d2aa0/scratchpad"
REPO = "/home/user/Pokemon-card-search"
d = json.load(open(os.path.join(SP, "field_summary.json")))
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
        f"rate written in the body below this box predates the "
        f"Stadium-passive fix and is not comparable**: 20 Stadiums had inert "
        f"passives, Stadiums a deck wanted but did not name by text were "
        f"never played at all, and blind discard costs pitched arbitrary "
        f"cards instead of ranking them.\n"
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
