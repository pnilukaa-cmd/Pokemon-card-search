"""Automated deck search (B3) -- gated on the simulator being good enough.

Hill-climbing over a decklist: change a count, measure against the field,
keep what wins. Mechanically simple. The reason it is not simply switched
on is written into the gate below.

    python3 deckopt.py mydeck.txt decks/ --rounds=20

AN OPTIMISER MAXIMISES WHATEVER THE SIMULATOR REPORTS. If the simulator
misprices something, the search will find that misprice faster than it
finds a good deck, and hand back a list tuned to an artifact -- which is
strictly worse than building by hand, because the output looks
quantitative. This project has produced that failure repeatedly: at
various points prevent_damage was never called, turn locks never fired,
self-KO costs were free, Prize cards were never set aside, and a
board-wide spread was priced as if it hit one Pokemon. Each of those was
a strategy a search would have learned to exploit.

So the gate: run audit_engine_coverage.py first, and this refuses to
search until enough of the engine is demonstrably live.
"""

import json
import os
import random
import subprocess
import sys

import deckcheck
import tcg_model as M

COVERAGE_FILE = "engine_coverage.json"
MIN_OPS_FIRING = 40          # of 48
MIN_TRAINER_COVERAGE = 70.0  # percent


def trainer_coverage():
    import simulate_versus as SV
    cards = M.load_cards()
    SV._CARDS_BY_NAME.update({c["name"]: c for c in cards})
    trainers = [c for c in cards if c.get("supertype") == "Trainer"]
    live = [c for c in trainers
            if c["name"] in SV.KNOWN_TRAINERS or SV.trainer_effect_ir(c["name"])]
    return 100.0 * len(live) / max(len(trainers), 1)


def gate(override=False):
    """Returns (ok, reasons). Never silently passes."""
    reasons = []
    if not os.path.exists(COVERAGE_FILE):
        reasons.append(f"{COVERAGE_FILE} missing -- run "
                       f"audit_engine_coverage.py <deck folder> first")
    else:
        cov = json.load(open(COVERAGE_FILE))
        firing = cov.get("ops_firing", 0)
        if firing < MIN_OPS_FIRING:
            reasons.append(f"only {firing} of {cov.get('ops_total', 48)} IR ops "
                           f"fire in play; the bar is {MIN_OPS_FIRING}. Dead ops "
                           f"are effects the search will not know exist: "
                           f"{', '.join(cov.get('dead_ops', [])[:6])}")
        if cov.get("unwired_queries"):
            reasons.append(f"engine queries nothing calls: "
                           f"{', '.join(cov['unwired_queries'])}")
    tc = trainer_coverage()
    if tc < MIN_TRAINER_COVERAGE:
        reasons.append(f"Trainer coverage {tc:.1f}%, bar is {MIN_TRAINER_COVERAGE}%")
    return (not reasons or override), reasons


# --------------------------------------------------------------------------
# The search itself
# --------------------------------------------------------------------------

def parse(text):
    return M.parse_decklist_entries(text)


def render(entries):
    out = []
    for e in entries:
        if e["count"] <= 0:
            continue
        tag = f" {e['set']} {e['number']}" if e["set"] and e["number"] else ""
        out.append(f"{e['count']} {e['name']}{tag}")
    return "\n".join(out)


def score(deck_text, folder, games, seed, sample):
    """Mean win rate over a fixed sample of the field.

    The SAME sample and seed every round, deliberately: a search that
    re-rolls its opponents each round climbs the noise instead of the
    deck.
    """
    tmp = ".deckopt_candidate.txt"
    open(tmp, "w").write(deck_text + "\n")
    total, n = 0.0, 0
    for opp in sample:
        out = subprocess.run(
            [sys.executable, "simulate_versus.py", tmp, opp, str(games),
             f"--seed={seed}"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if ".deckopt_candidate" in line and "wins" in line:
                pct = line.split("(")[-1].split("%")[0].strip()
                try:
                    total += float(pct)
                    n += 1
                except ValueError:
                    pass
    return total / n if n else 0.0


def neighbours(entries, rng):
    """One-card changes: a legal deck is always 60, so every mutation
    moves a copy from one line to another rather than changing the size."""
    out = []
    idxs = list(range(len(entries)))
    rng.shuffle(idxs)
    for i in idxs[:8]:
        for j in idxs[:8]:
            if i == j or entries[i]["count"] <= 0:
                continue
            cap = 4
            if entries[j]["count"] >= cap:
                continue
            cand = [dict(e) for e in entries]
            cand[i]["count"] -= 1
            cand[j]["count"] += 1
            out.append(cand)
    return out


def optimise(path, folder, rounds, games, seed, width):
    rng = random.Random(seed)
    entries = parse(open(path).read())
    pool = sorted(f for f in os.listdir(folder) if f.endswith(".txt"))
    sample = [os.path.join(folder, f) for f in pool]
    rng.shuffle(sample)
    sample = sample[:width]
    print(f"field sample ({len(sample)}): "
          f"{', '.join(os.path.basename(s)[:-4] for s in sample)}\n")

    best = render(entries)
    best_score = score(best, folder, games, seed, sample)
    print(f"start  {best_score:5.1f}%")

    for r in range(1, rounds + 1):
        improved = False
        for cand in neighbours(entries, rng)[:6]:
            text = render(cand)
            res = deckcheck.validate(text)
            if not res.ok:
                continue
            s = score(text, folder, games, seed, sample)
            if s > best_score + 0.5:
                entries, best, best_score = cand, text, s
                print(f"round {r:2}  {s:5.1f}%  accepted")
                improved = True
                break
        if not improved:
            print(f"round {r:2}  no improvement, stopping")
            break
    return best, best_score


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    override = "--i-understand-the-simulator-is-incomplete" in sys.argv
    ok, reasons = gate(override)
    if not ok:
        print("REFUSING TO SEARCH -- the simulator is not good enough to "
              "optimise against:\n")
        for r in reasons:
            print(f"  * {r}")
        print("\nAn optimiser finds the engine's blind spots faster than it "
              "finds a good deck.\nFix the coverage first, or pass "
              "--i-understand-the-simulator-is-incomplete\nto search anyway "
              "and treat the result as a hypothesis, not a measurement.")
        sys.exit(2)
    if override and reasons:
        print("WARNING: searching against an incomplete simulator.")
        for r in reasons:
            print(f"  * {r}")
        print()
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    def opt(flag, default):
        v = next((a for a in sys.argv if a.startswith(flag)), None)
        return int(v.split("=", 1)[1]) if v else default

    text, s = optimise(args[0], args[1], opt("--rounds=", 10),
                       opt("--games=", 40), opt("--seed=", 1),
                       opt("--width=", 6))
    print(f"\nbest {s:.1f}%\n")
    print(text)


if __name__ == "__main__":
    main()
