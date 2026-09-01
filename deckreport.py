"""Emit everything the UI needs about a deck as one JSON blob (B4 backend).

The interface does not re-derive anything. Every figure it shows already
exists in a script here; this collects them into one shape so the page is
a view, not a second implementation that can disagree with the first.

    python3 deckreport.py mydeck.txt --out=report.json
"""

import json
import os
import subprocess
import sys

import deckcheck
import tcg_model as M


def engine_revision():
    import hashlib
    h = hashlib.sha256()
    for f in ("simulate_versus.py", "ability_engine.py", "ability_ir.py",
              "tcg_model.py"):
        try:
            h.update(open(f, "rb").read())
        except OSError:
            pass
    return h.hexdigest()[:10]


def setup_curve(path, trials=800, turns=6):
    import simulate_baseline as B
    POKEMON, DECKLIST, _, _ = B.build_deck_model(open(path).read())
    hits = {name: [0] * (turns + 1) for name in POKEMON}
    for _ in range(trials):
        r = B.run_playthrough(POKEMON, DECKLIST, num_turns=turns)
        for name, t in r["online_turn"].items():
            for k in range(t, turns + 1):
                hits[name][k] += 1
    return {name: [round(100 * hits[name][k] / trials, 1)
                   for k in range(1, turns + 1)]
            for name in POKEMON}


def field(path, folder, games=60, seed=1):
    rows = []
    mine = os.path.splitext(os.path.basename(path))[0]
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".txt") or f[:-4] == mine:
            continue
        out = subprocess.run(
            [sys.executable, "simulate_versus.py", path,
             os.path.join(folder, f), str(games), f"--seed={seed}"],
            capture_output=True, text=True).stdout
        for line in out.splitlines():
            if mine in line and "wins" in line:
                try:
                    rows.append({"opponent": f[:-4],
                                 "win_pct": float(line.split("(")[-1]
                                                  .split("%")[0].strip())})
                except ValueError:
                    pass
                break
    rows.sort(key=lambda r: -r["win_pct"])
    return rows


def report(path, folder=None, games=60):
    text = open(path).read()
    res = deckcheck.validate(text)
    data = {
        "name": os.path.splitext(os.path.basename(path))[0],
        "engine": engine_revision(),
        "size": res.size,
        "basics": res.basics,
        "mulligan_pct": round(res.mulligan_pct, 1),
        "legal": res.ok,
        "errors": res.errors,
        "warnings": res.warnings,
        "unresolved": res.unresolved,
        "energy_supply": res.energy_supply,
        "lines": [{"count": e["count"], "name": e["name"],
                   "set": e["set"], "number": e["number"]}
                  for e in M.parse_decklist_entries(text)],
        "curve": setup_curve(path),
    }
    if folder:
        data["field"] = field(path, folder, games)
        if data["field"]:
            pct = [r["win_pct"] for r in data["field"]]
            data["field_mean"] = round(sum(pct) / len(pct), 1)
            data["field_wins"] = sum(1 for p in pct if p > 50)
    return data


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    folder = args[1] if len(args) > 1 else None
    d = report(args[0], folder)
    out = next((a for a in sys.argv if a.startswith("--out=")), None)
    blob = json.dumps(d, indent=2)
    if out:
        open(out.split("=", 1)[1], "w").write(blob)
        print(f"wrote {out.split('=', 1)[1]}  ({d['size']} cards, "
              f"mulligan {d['mulligan_pct']}%)")
    else:
        print(blob)
