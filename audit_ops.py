#!/usr/bin/env python3
"""Which compiled ops does the runtime actually READ?

The recurring defect in this engine is not a card that fails to parse --
it is a card that parses perfectly into an op nothing ever asks about.
ATTACK_TWICE compiled, sat in apply_action's known-passive list so nothing
reported it as missing, and gated an entire archetype's damage.
CONDITION_IMMUNITY did the same for every "can't be Poisoned" Ability in
the format. Both were found by hand, late.

This finds them mechanically. An op counts as READ if apply_action
executes it, or if some query_* asks _passive_actions for it, or if the
simulator names it directly. Appearing ONLY in apply_action's
acknowledgement tuple -- the "yes, we know, it's a passive" list -- does
NOT count, because that list is exactly where an inert op hides.

Usage:  python3 audit_ops.py [--cards]
        --cards also reports, for each orphan, how many Standard-legal
        cards carry it and which of them appear in this repo's decks.
"""
import collections
import glob
import os
import re
import sys

import ability_ir as IR


def classify():
    names = [a for a in dir(IR.Op) if not a.startswith("_")]
    ae = open("ability_engine.py").read()
    sv = open("simulate_versus.py").read()
    start = ae.index("    if op in (IR.Op.")
    end = ae.index("return False", start) + len("return False")
    ae_noack = ae[:start] + ae[end:]

    executed, read = set(), set()
    for n in names:
        if re.search(r"op == O\.%s\b" % n, ae):
            executed.add(n)
        if re.search(r"_passive_actions\(\s*[^)]*?IR\.Op\.%s\b" % n, ae_noack, re.S):
            read.add(n)
        if re.search(r"(IR\.)?Op\.%s\b" % n, sv):
            read.add(n)
    orphan = sorted(n for n in names if n not in executed and n not in read)
    return names, executed, read, orphan


# Ops that are modelled as nothing ON PURPOSE. They exist so a card whose
# text describes a deckbuilding rule, a setup-phase rule, or hidden
# information the engine has no notion of stops reading as an unhandled gap.
# They are excluded from the orphan list because an orphan means "nobody
# remembered to wire this up", which is a different thing entirely.
DELIBERATE_NO_OPS = {"NO_OP_INFORMATION", "NO_OP_SETUP_RULE"}


def uncalled_queries():
    """query_* functions that read an op but that NOBODY CALLS.

    The orphan check above asks whether an op has a reader. That is not the
    same as the op doing anything: a query_* function can read an op
    perfectly and still be dead code if the simulator never calls it. Adding
    a query and forgetting to wire it is the same defect as never writing
    one, so it gets the same treatment.
    """
    ae = open("ability_engine.py").read()
    sv = open("simulate_versus.py").read()
    out = []
    for m in re.finditer(r"^def (query_\w+)\(", ae, re.M):
        fn = m.group(1)
        body = ae[:m.start()] + ae[m.end():]
        if re.search(r"\b%s\(" % fn, body) or re.search(r"\b%s\(" % fn, sv):
            continue
        out.append(fn)
    return out


def cards_for(ops):
    import tcg_model as M
    hit = collections.defaultdict(set)
    for c in M.load_cards():
        if c.get("set", {}).get("legalities", {}).get("standard") != "Legal":
            continue
        effs = []
        if c.get("supertype") == "Pokémon":
            effs += IR.compile_card_abilities(c)
            for a in c.get("attacks") or []:
                if (a.get("text") or "").strip():
                    effs.append(IR.compile_effect("attack", a["name"], a["text"]))
        else:
            t = " ".join(c.get("rules") or [])
            if t.strip():
                effs.append(IR.compile_effect("trainer", c["name"], t))
        for e in effs:
            if e.unsupported:
                continue
            for act in e.actions:
                nm = (act.op if isinstance(act.op, str) else act.op.name).upper()
                if nm in ops:
                    hit[nm].add(c["name"])
    return hit


def deck_pokemon():
    """Exact card names in this repo's decks.

    Matching on substring instead got this wrong once: "Carbink" is in
    `Steven's Carbink` and "Kyurem" in `Kyurem ex`, which are different
    cards, and two orphans were reported as in-deck when they were not.
    """
    import simulate_versus as S
    out = set()
    for f in sorted(glob.glob("decks/*.md")):
        slug = os.path.basename(f)[:-3]
        if slug in ("FIELD_RESULTS", "snow_coating_verdict"):
            continue
        out |= set(S.load_model(f, slug)[0][1])
    return out


def main():
    names, executed, read, orphan = classify()
    orphan = [n for n in orphan if n not in DELIBERATE_NO_OPS]
    print(f"{len(names)} ops   executed {len(executed)}   "
          f"read as passive {len(read)}   ORPHAN {len(orphan)}\n")
    dead = uncalled_queries()
    if dead:
        print(f"  {len(dead)} query function(s) READ an op but are never "
              f"called -- dead code, same effect as no reader at all:")
        for fn in dead:
            print(f"    {fn}")
        print()
    if not orphan:
        print("  every op has a reader")
        if not dead:
            print("  and every reader is called")
        return
    if "--cards" not in sys.argv:
        for n in orphan:
            print("   ", n)
        return
    hit, in_deck = cards_for(set(orphan)), deck_pokemon()
    print(f"  {'op':26s} {'cards':>5s}  in this repo's decks")
    for n in orphan:
        named = sorted(hit.get(n, ()))
        here = [c for c in named if c in in_deck]
        print(f"  {n:26s} {len(named):5d}  {here if here else '-- none --'}")


if __name__ == "__main__":
    main()
