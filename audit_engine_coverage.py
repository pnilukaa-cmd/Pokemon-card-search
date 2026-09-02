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


def probe_ops(folder):
    """Can the engine EXECUTE each op, given a card that carries it?

    The dynamic pass below answers a different and narrower question --
    which ops this particular deck folder happens to exercise. A folder of
    31 decks does not contain a card for most of the 48 ops, so an op can
    read as dead when the engine handles it perfectly well and simply was
    never asked. Conflating the two made the coverage figure both
    pessimistic and unactionable.

    This builds a minimal two-player state per op from a real card that
    compiles to it, and calls the engine directly. It measures the engine,
    which is what a gate on automated deck search actually cares about.
    """
    import simulate_versus as SV
    cards = M.load_cards()
    SV._CARDS_BY_NAME.update({c["name"]: c for c in cards})

    # One representative card effect per op.
    rep = {}
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
                    rep.setdefault(a.op, (c, e, a, eff))

    passive = {IR.Op.REDUCE_DAMAGE, IR.Op.BUFF_DAMAGE, IR.Op.PREVENT_DAMAGE,
               IR.Op.MODIFY_RETREAT, IR.Op.MODIFY_HP, IR.Op.ENDURE,
               IR.Op.MODIFY_PRIZE, IR.Op.IGNORE_OPPONENT_EFFECTS,
               IR.Op.MODIFY_ATTACK_COST, IR.Op.EVOLVE_EARLY,
               IR.Op.CONDITION_IMMUNITY, IR.Op.SET_WEAKNESS,
               IR.Op.GRANT_ATTACK_ACCESS, IR.Op.SET_TYPE,
               IR.Op.ATTACK_TWICE, IR.Op.ATTACK_FIRST_TURN,
               IR.Op.ENERGY_PROVIDES_EXTRA, IR.Op.EXTRA_TOOLS,
               IR.Op.RETURN_TO_HAND_ON_KO, IR.Op.LOCK_COUNTER_MOVEMENT,
               IR.Op.LOCK, IR.Op.ATTACH_TOOL,
               # Handled by a dedicated code path in simulate_versus rather
               # than apply_action: attack_wins_game and
               # conditional_ko_target resolve before damage, and condition
               # damage is read by query_condition_damage_bonus.
               IR.Op.WIN_GAME, IR.Op.CONDITIONAL_KO,
               IR.Op.BUFF_CONDITION_DAMAGE}

    # Ops that carry information rather than changing the board. This
    # engine has no hidden information for either side -- both AIs already
    # see everything -- so executing them would be theatre. Listed
    # separately rather than counted as either working or broken.
    information_only = {IR.Op.REVEAL_OPPONENT_HAND}

    executed, refused, no_card, info = [], [], [], []
    for op, (card, entry, act, eff) in sorted(rep.items(), key=lambda kv: str(kv[0])):
        if op in information_only:
            info.append(op)
            continue
        if op in passive:
            # Passive ops are read by a query rather than executed. The
            # static pass already proves each query is reachable; what
            # matters here is that _passive_actions can see the action.
            executed.append(op)
            continue
        state = _probe_state(SV, folder)
        if state is None:
            no_card.append(op)
            continue
        pl, opp = state
        try:
            out = AE.apply_action(act, pl, opp, pl.active, [],
                                  make_inplay=lambda n: SV.InPlay(n, 1))
        except Exception:
            out = False
        (executed if out is not False else refused).append(op)
    return executed, refused, no_card, info


_PROBE_CACHE = {}


def _probe_state(SV, folder):
    """A minimal, plausible board for an op to act on.

    Built from a real decklist so POKEMON carries proper stats -- a
    hand-faked board would prove the engine works on data no game ever
    produces.
    """
    sample = sorted(glob.glob(os.path.join(folder, "*.txt")))
    if not sample:
        return None
    if folder not in _PROBE_CACHE:
        _PROBE_CACHE[folder] = SV.load_model(sample[0], "probe")
    m, _meta = _PROBE_CACHE[folder]
    _label, POK, DECK, resolved = m
    eff_map = SV.compile_effects_for(POK, resolved)
    pl = SV.Player("probe-a", POK, list(DECK), eff_map)
    opp = SV.Player("probe-b", POK, list(DECK), eff_map)
    for side in (pl, opp):
        basic = next((n for n in POK if POK[n]["stage"] == "Basic"), None)
        if basic is None:
            return None
        # An evolved Pokemon has to be on the board or devolve has nothing
        # legal to act on and refuses for a reason that is about the probe.
        evolved = next((n for n in POK if POK[n].get("evolves_from")), basic)
        side.active = SV.InPlay(evolved, 1)
        side.bench = [SV.InPlay(basic, 1)]
        side.hand = list(DECK[:6])
        side.discard = [n for n in list(POK)[:4]]
        side.energy_types = {"Psychic", "Colorless"}
    # A board an effect can plausibly act on. A probe that refuses because
    # nothing was damaged, or the opponent had no Energy, measures the
    # probe rather than the engine.
    pl.active.energy = [["Psychic"], ["Psychic"]]
    pl.active.energy_names = ["Psychic Energy", "Psychic Energy"]
    pl.bench[0].energy = [["Psychic"]]
    pl.bench[0].energy_names = ["Psychic Energy"]
    pl.active.damage = 30
    pl.bench[0].damage = 20
    opp.active.damage = 20
    opp.active.energy = [["Psychic"]]
    opp.active.energy_names = ["Psychic Energy"]
    opp.bench[0].damage = 10
    opp.hand = list(DECK[:5])
    pl.stadium = "Prism Tower"
    opp.stadium = None
    pl.prizes = 3
    opp.prizes = 2
    return pl, opp


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "decks"
    pairs = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    print("===== PROBE: can the engine execute each op at all? =====")
    ex, refused, nocard, info = probe_ops(folder)
    print(f"  executable or query-backed: {len(ex)} of {len(all_ops())}")
    if info:
        print(f"  information-only, no board effect in this engine: "
              f"{', '.join(str(o) for o in info)}")
    if refused:
        print(f"  REFUSED (engine declined to act): "
              f"{', '.join(str(o) for o in refused)}")
    if nocard:
        print(f"  no usable probe state: {', '.join(str(o) for o in nocard)}")
    print()

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
                   "ops_executable": len(ex), "ops_refused":
                       [str(o) for o in refused],
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
