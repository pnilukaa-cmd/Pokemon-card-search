"""Aggregate round-robin shards into a field table and patch every deck file."""
import glob, json, os, re, statistics, sys, datetime

REPO = os.path.dirname(os.path.abspath(__file__))
# Run output lives in the repo, not a session scratchpad: the scratchpad
# is deleted with the container, and the 2026-09-15 shards went with it.
SP = os.environ.get("RUNS_DIR", os.path.join(REPO, "runs"))

games = None
wins = {}
unplayable = set()
# base run first, then the re-run of the two decks that were fixed
# mid-flight -- same per-pair seeds, so the override is exact.
# Run directory: pass it on the command line, e.g. `run2`, resolved under
# SP. The default is SP itself.
RUN = os.path.join(SP, sys.argv[1]) if len(sys.argv) > 1 else SP

for f in (sorted(glob.glob(os.path.join(RUN, "rr_[0-9]*.json")))
          + sorted(glob.glob(os.path.join(RUN, "rrfix_*.json")))):
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
       f"Measured {stamp}. **These supersede every number in the deck files "
       f"before this date.**\n"]
# The run-specific write-up (what changed, what did not) lives next to the
# shards as NOTES.md, so this script never carries a past run's narrative.
notes = os.path.join(RUN, "NOTES.md")
if os.path.exists(notes):
    out.append(open(notes).read().strip() + "\n")
out += [
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
          open(os.path.join(RUN, "field_summary.json"), "w"), indent=1, default=str)
for n in order:
    s = summary[n]
    print(f"  {s['mean']:5.1f}%  {s['median']:5.1f}%  {s['winning']:2d}/{s['played']}  {n}")
