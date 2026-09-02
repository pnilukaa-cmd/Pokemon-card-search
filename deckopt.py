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

import concurrent.futures as cf
import math

import deckcheck
import tcg_model as M


def basics_in(path):
    """Basic Pokemon in a decklist -- the screen gauntlet.py already uses."""
    cards = M.load_cards()
    by_name, by_setnum = M.build_card_index(cards)
    n = 0
    for entry in M.parse_decklist_entries(open(path).read()):
        card, _ = M.resolve_card(entry, by_name, by_setnum)
        if card and card.get("supertype") == "Pokémon" \
                and M.stage_of(card) == "Basic":
            n += entry["count"]
    return n

COVERAGE_FILE = "engine_coverage.json"
MIN_OPS_EXECUTABLE = 44      # of 48 -- can the engine DO the thing at all
MIN_OPS_FIRING = 12          # of 48 -- does this field exercise it
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
        total = cov.get("ops_total", 48)
        # The gate that matters is CAPABILITY: can the engine execute the
        # op at all, given a card that carries it. The dynamic figure
        # measures something narrower -- which ops this particular deck
        # folder happens to exercise -- and a folder of 31 decks does not
        # contain a card for most of the 48, so gating on it would block
        # forever for a reason that has nothing to do with the engine.
        ex = cov.get("ops_executable")
        if ex is None:
            reasons.append("coverage file predates the capability probe; "
                           "re-run audit_engine_coverage.py")
        elif ex < MIN_OPS_EXECUTABLE:
            refused = cov.get("ops_refused", [])
            reasons.append(f"only {ex} of {total} IR ops are executable; the "
                           f"bar is {MIN_OPS_EXECUTABLE}. The engine refuses: "
                           f"{', '.join(refused[:8])}")
        firing = cov.get("ops_firing", 0)
        if firing < MIN_OPS_FIRING:
            reasons.append(f"only {firing} of {total} ops were exercised by the "
                           f"deck field at all; the search would be tuning "
                           f"against a very narrow slice of the game")
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
    tmp = f".deckopt_candidate_{abs(hash(deck_text)) % 10 ** 8}.txt"
    open(tmp, "w").write(deck_text + "\n")
    tag = os.path.splitext(os.path.basename(tmp))[0]

    def one(opp):
        out = subprocess.run(
            [sys.executable, "simulate_versus.py", tmp, opp, str(games),
             f"--seed={seed}"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if tag in line and "wins" in line:
                try:
                    return float(line.split("(")[-1].split("%")[0].strip())
                except ValueError:
                    return None
        return None

    # Each matchup is its own process, so spread them over the cores. The
    # search is measurement-limited, and every factor of N here is a
    # factor of sqrt(N) off the resolution it can achieve.
    try:
        workers = max(1, min(len(sample), os.cpu_count() or 1))
        with cf.ThreadPoolExecutor(max_workers=workers) as pool:
            results = [r for r in pool.map(one, sample) if r is not None]
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return sum(results) / len(results) if results else 0.0


def neighbours(entries, rng):
    """One-card changes: a legal deck is always 60, so every mutation
    moves a copy from one line to another rather than changing the size."""
    out = []
    idxs = list(range(len(entries)))
    rng.shuffle(idxs)
    for i in idxs[:14]:
        for j in idxs[:14]:
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
    # Screen out decks the engine cannot pilot, exactly as gauntlet.py
    # does. A zero-Basic deck mulligans out and loses on turn 2, so
    # "beating" it is a free 100% -- and a search will happily tune toward
    # whatever wins that matchup fastest. This is the blind-spot farming
    # the gate above exists to prevent, arriving through the sample
    # instead of through the engine.
    playable = []
    for f in sample:
        try:
            if basics_in(f) > 0:
                playable.append(f)
        except Exception:
            continue
    dropped = len(sample) - len(playable)
    if dropped:
        print(f"screened out {dropped} deck(s) with no Basic Pokemon "
              f"(they mulligan out and are a free win)")
    sample = playable
    rng.shuffle(sample)
    sample = sample[:width]
    print(f"field sample ({len(sample)}): "
          f"{', '.join(os.path.basename(s)[:-4] for s in sample)}\n")

    best = render(entries)
    best_score = score(best, folder, games, seed, sample)

    # A fixed +0.5% acceptance threshold is far inside the noise at any
    # sample size this search can afford, so it accepts noise as readily
    # as signal -- and a deck "improved" by noise is exactly the
    # authoritative-looking garbage this whole gate exists to avoid.
    # Require the gain to clear two standard errors of a win rate measured
    # over this many games.
    n_games = max(games * len(sample), 1)
    se = 100.0 * math.sqrt(0.25 / n_games)
    threshold = 2 * se
    print(f"start  {best_score:5.1f}%   "
          f"(n={n_games}, 1 s.e. = {se:.1f}%, accepting gains > {threshold:.1f}%)")
    if threshold > 4:
        print(f"       NOTE: at this sample size nothing smaller than "
              f"{threshold:.1f}% is resolvable.\n"
              f"       Raise --games or --width to see finer differences.")

    for r in range(1, rounds + 1):
        improved = False
        # More candidates per round than the original six. A strict hill
        # climb that gives up after a handful of neighbours reports "no
        # improvement" when it simply has not looked, which is a different
        # claim and a misleading one.
        for cand in neighbours(entries, rng)[:14]:
            text = render(cand)
            res = deckcheck.validate(text)
            if not res.ok:
                continue
            s = score(text, folder, games, seed, sample)
            if s > best_score + threshold:
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
