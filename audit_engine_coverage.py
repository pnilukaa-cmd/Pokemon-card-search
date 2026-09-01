"""Does the engine actually USE what it compiles?

Every deck-invalidating bug in this project so far has had the same shape:
something existed, parsed correctly, had a passing unit test -- and was
never reached in a real game.

  * `query_prevented` was written when Abilities were first wired in, had
    a passing test, and NO code path in simulate_versus ever called it. So
    every damage-prevention Ability in the pool did nothing, and a deck
    built out of them measured as if it had no defence at all.
  * Cursed Blast's `self_ko` cost was compiled and never paid, so the
    Ability was free forever -- worth 11 points of win rate to one deck.
  * Prize cards were tracked as a counter and never removed from the deck.

Compilation coverage (ability_ir: 98.6%) does not measure any of this.
This audit measures two different things:

  STATIC   every public query_* in ability_engine, and whether any
           simulator actually calls it.
  DYNAMIC  every IR Op that appears in the compiled card pool, and
           whether it ever fires across a corpus of real games.

An Op that compiles on real cards but never executes is either dead code
or an unwired feature, and that is precisely the bug class above.
"""

import glob
import os
import random
import re
import sys
from collections import Counter

import ability_ir as IR
import ability_engine as AE
import tcg_model as M

SIMS = ["simulate_versus.py", "simulate_baseline.py"]
COVERAGE_FILE = "engine_coverage.json"


def all_ops():
    return {v for k, v in vars(IR.Op).items()
            if not k.startswith("_") and isinstance(v, str)}


def static_unwired():
    """Engine queries nothing reachable from a simulator ever calls.

    Reachability is transitive: query_retreat_modifier is never named in
    either simulator, but effective_retreat calls it and the simulators
    call that, so it is wired. Only report a query that nothing reachable
    consults.
    """
    src = open("ability_engine.py").read()
    names = re.findall(r"^def (query_\w+|effective_retreat)\(", src, re.M)
    bodies = dict(re.findall(r"^def (\w+)\(.*?\):\n(.*?)(?=\n^def |\Z)",
                             src, re.M | re.S))
    sim_src = "".join(open(f).read() for f in SIMS if os.path.exists(f))

    reachable = {n for n in bodies if re.search(rf"\b{n}\s*\(", sim_src)}
    changed = True
    while changed:                       # transitive closure
        changed = False
        for caller in list(reachable):
            for callee in bodies:
                if callee in reachable:
                    continue
                if re.search(rf"\b{callee}\s*\(", bodies.get(caller, "")):
                    reachable.add(callee)
                    changed = True
    return [n for n in names if n not in reachable]


def ops_present_in_pool():
    """Ops that real cards in the pool actually compile to."""
    cards = M.load_cards()
    seen = Counter()
    for c in cards:
        for kind, entries in (("ability", c.get("abilities") or []),
                              ("attack", c.get("attacks") or [])):
            for e in entries:
                text = e.get("text") or ""
                if not text:
                    continue
                eff = IR.compile_effect(kind, e.get("name") or "", text)
                if eff.unsupported:
                    continue
                for a in eff.actions:
                    seen[a.op] += 1
    return seen


def ops_fired_in_games(folder, games_per_pair, pairs):
    """Ops that actually execute when games are played."""
    import simulate_versus as SV
    fired = Counter()
    real_apply = AE.apply_action

    def spy(act, *a, **kw):
        out = real_apply(act, *a, **kw)
        if out is not False:
            fired[act.op] += 1
        return out

    # Passive Abilities never go through apply_action -- they are read out
    # of _passive_actions by the query_* helpers. Instrumenting only
    # apply_action reported every wall and buff in the pool as dead code.
    real_passive = AE._passive_actions

    def passive_spy(pl, op, *a, **kw):
        got = list(real_passive(pl, op, *a, **kw))
        for _holder, _eff, act in got:
            fired[act.op] += 1
        return got

    AE.apply_action = spy
    SV.AE.apply_action = spy
    AE._passive_actions = passive_spy
    decks = sorted(glob.glob(os.path.join(folder, "*.txt")))
    random.shuffle(decks)
    try:
        for i in range(min(pairs, len(decks) // 2)):
            a, b = decks[2 * i], decks[2 * i + 1]
            try:
                mA = SV.load_model(a, os.path.basename(a)[:-4])[0]
                mB = SV.load_model(b, os.path.basename(b)[:-4])[0]
                for _ in range(games_per_pair):
                    SV.run_game(mA, mB)
            except Exception as exc:      # one broken deck file must not
                print(f"  (skipped {os.path.basename(a)} vs "        # abort the audit
                      f"{os.path.basename(b)}: {exc})")
    finally:
        AE.apply_action = real_apply
        SV.AE.apply_action = real_apply
        AE._passive_actions = real_passive
    return fired


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "decks"
    pairs = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    print("===== STATIC: engine queries no simulator calls =====")
    unwired = static_unwired()
    if unwired:
        for n in unwired:
            print(f"  UNWIRED  {n}  -- exists, compiles, never consulted")
    else:
        print("  none -- every engine query is reachable from a simulator")

    print("\n===== DYNAMIC: ops that compile on real cards but never fire =====")
    present = ops_present_in_pool()
    fired = ops_fired_in_games(folder, games, pairs)
    dead = sorted((op for op in present if not fired.get(op)),
                  key=lambda o: -present[o])
    for op in dead:
        print(f"  NEVER FIRES  {op:34} on {present[op]:4} card effects")
    if not dead:
        print("  none -- every op present in the pool executed at least once")

    firing = len(present) - len(dead)
    print(f"\n  {len(present)} of {len(all_ops())} ops appear on real cards; "
          f"{firing} of those fired in play.")

    # Written so other tools can gate on it without re-running a corpus.
    # deckopt.py refuses to search for decks until this clears its bar,
    # because an optimiser maximises whatever the simulator reports and
    # the simulator's blind spots are the cheapest thing for it to find.
    import json
    with open(COVERAGE_FILE, "w") as fh:
        json.dump({"ops_present": len(present), "ops_firing": firing,
                   "ops_total": len(all_ops()),
                   "unwired_queries": unwired,
                   "dead_ops": [str(o) for o in dead]}, fh, indent=2)
    print(f"  wrote {COVERAGE_FILE}")
    print("\nA NEVER FIRES line is not automatically a bug -- an op can be rare\n"
          "enough that a short corpus misses it. Raise the game count before\n"
          "concluding, then go look at whether the game loop asks for it.")
    return 1 if unwired else 0


if __name__ == "__main__":
    sys.exit(main())
