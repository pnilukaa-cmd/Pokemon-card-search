"""Aggregate round-robin shards into a field table and patch every deck file."""
import glob, json, os, re, statistics, sys, datetime

SP = "/tmp/claude-0/-home-user-Pokemon-card-search/e648d066-66e0-5170-a656-2af4bb2d2aa0/scratchpad"
REPO = "/home/user/Pokemon-card-search"

games = None
wins = {}
unplayable = set()
# base run first, then the re-run of the two decks that were fixed
# mid-flight -- same per-pair seeds, so the override is exact.
for f in (sorted(glob.glob(os.path.join(SP, "rr_[0-9]*.json")))
          + sorted(glob.glob(os.path.join(SP, "rrfix_*.json")))):
    d = json.load(open(f))
    games = d["games"]
    unplayable |= set(d.get("unplayable") or [])
    wins.update(d["results"])

names = sorted({n for k in wins for n in k.split("|")})
rate = {}                                  # rate[a][b] = a's win % vs b
for k, w in wins.items():
    a, b = k.split("|")
    rate.setdefault(a, {})[b] = 100.0 * w / games
    rate.setdefault(b, {})[a] = 100.0 * (games - w) / games

summary = {}
for n in names:
    vals = list(rate[n].values())
    summary[n] = {
        "mean": statistics.mean(vals),
        "median": statistics.median(vals),
        "winning": sum(1 for v in vals if v > 50),
        "played": len(vals),
        "best": max(rate[n].items(), key=lambda x: x[1]),
        "worst": min(rate[n].items(), key=lambda x: x[1]),
    }

order = sorted(names, key=lambda n: -summary[n]["mean"])
stamp = datetime.date.today().isoformat()

# ---- the field table -------------------------------------------------
out = [f"# Field results — every deck against every other deck\n",
       f"Full round robin over **{len(names)} decks**, "
       f"**{games} games** per pairing, {len(wins)} pairings, "
       f"{len(wins)*games:,} games. Each pairing uses its own fixed seed, so "
       f"a re-run of this field reproduces exactly.\n",
       f"Measured {stamp}, after the ex audit. **These supersede every "
       f"number recorded in the deck files before this date** — the audit "
       f"changed damage on a large number of cards (typed Energy scalers "
       f"counting the wrong Energy, discard-cost attacks that were never "
       f"charged, attack gates that were never enforced), so older figures "
       f"are not comparable with these or with each other.\n",
       "Two changes to the field itself: `AAA_tr_crobat_absol_snipe` was a "
       "byte-identical duplicate of `tr_crobat_absol_bench_snipe` and had "
       "been inflating that archetype's presence in every past measurement; "
       "`veluza_sinistcha_ex_tea_service` had a deck file but no entry in "
       "the field and had never been measured at all.\n",
       "| # | deck | mean | median | winning | best matchup | worst |",
       "|---|---|---|---|---|---|---|"]
for i, n in enumerate(order, 1):
    s = summary[n]
    out.append(f"| {i} | `{n}` | **{s['mean']:.1f}%** | {s['median']:.1f}% | "
               f"{s['winning']}/{s['played']} | {s['best'][0]} "
               f"({s['best'][1]:.0f}%) | {s['worst'][0]} ({s['worst'][1]:.0f}%) |")
if unplayable:
    out.append("\n## Excluded\n")
    out.append("No Basic Pokémon the engine can put into play, so they "
               "mulligan out and lose on turn 2 — a meaningless 100% for "
               "everyone else:\n")
    for u in sorted(unplayable):
        out.append(f"- `{u}`")

out.append("\n## Full matrix\n")
out.append("Row's win rate against column.\n")
short = {n: n[:14] for n in order}
out.append("| |" + "|".join(short[n] for n in order) + "|")
out.append("|---|" + "---|" * len(order))
for a in order:
    cells = []
    for b in order:
        cells.append("—" if a == b else f"{rate[a][b]:.0f}")
    out.append(f"| **{short[a]}** |" + "|".join(cells) + "|")

open(os.path.join(REPO, "decks", "FIELD_RESULTS.md"), "w").write("\n".join(out) + "\n")
print(f"wrote decks/FIELD_RESULTS.md ({len(names)} decks, {len(wins)} pairings)")
json.dump({"stamp": stamp, "games": games,
           "summary": {k: {kk: vv for kk, vv in v.items()} for k, v in summary.items()}},
          open(os.path.join(SP, "field_summary.json"), "w"), indent=1, default=str)
for n in order:
    s = summary[n]
    print(f"  {s['mean']:5.1f}%  {s['median']:5.1f}%  {s['winning']:2d}/{s['played']}  {n}")
