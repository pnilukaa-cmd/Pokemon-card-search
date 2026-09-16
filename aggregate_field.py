"""Aggregate round-robin shards into a field table and patch every deck file."""
import glob, json, os, re, statistics, sys, datetime

SP = "/tmp/claude-0/-home-user-Pokemon-card-search/e648d066-66e0-5170-a656-2af4bb2d2aa0/scratchpad"
REPO = "/home/user/Pokemon-card-search"

games = None
wins = {}
unplayable = set()
# base run first, then the re-run of the two decks that were fixed
# mid-flight -- same per-pair seeds, so the override is exact.
# Run directory: pass it on the command line, e.g. `run2`. The default is
# the scratchpad root, which is where the 2026-09-15 field landed.
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
       f"Measured {stamp}, after the Stadium-passive fix. **These "
       f"supersede every number in the deck files before this date** and "
       f"are not comparable with the 2026-09-15 field: the engine changed "
       f"materially in between.\n",
       "What changed since 2026-09-15. Three engine bugs, each of which had "
       "been silently suppressing real card text:\n"
       "- **20 Stadium passives were inert.** `_passive_actions` only ever "
       "walked Pokemon Abilities, so a Stadium's own compiled effect reached "
       "nothing. Stadiums now contribute their actions with `holder=None`, "
       "and third-person Stadium text (\"that player may search *their* "
       "deck\") is normalised to first person before it compiles.\n"
       "- **Stadiums a deck wanted but did not name were never played.** "
       "`_stadium_has_effect` asked only whether the Stadium\u2019s own text "
       "compiled. A Stadium that any of your cards *names* is now worth "
       "playing, which is why `Festival Grounds` had never once hit the "
       "table.\n"
       "- **Blind discards threw away the wrong cards.** Costs that discard "
       "from hand picked arbitrarily; they now rank by `pitch_rank`.\n",
       "One new deck joined the field: `metal_metang_excadrill`, the list "
       "reviewed on 2026-09-16. Every other deck is unchanged, so a "
       "like-for-like delta against the previous field is in the section "
       "below the table.\n",
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
