#!/usr/bin/env python3
"""Deterministic search helpers for TCG combo-mining/theorycrafting.

This exists so the tag lookup, raw-text sweep, and gap-detection steps are
run the same way every time instead of being re-derived by hand. It does
the mechanical retrieval; deciding what's a real combo vs. noise, and
building an actual decklist, is still a judgment call for whoever's using
this (see SKILL.md).

Run from the repo root (needs pokemon_standard_cards.json, mechanic_index.json,
and analyze_mechanics.py in the current directory).

Modes (pick one or more):
  --suggest-tags KEYWORD     Grep family tag names in analyze_mechanics.py for
                              KEYWORD, print each match's role + card_count.
                              Use this first to find candidate tags before
                              pulling full entries.

  --tags TAG1,TAG2,...       Print every mechanic_index.json entry carrying
                              any of these tags, grouped by role (produce vs
                              consume), with name/effect/text.

  --sweep KEYWORD            Raw full-text search over every card's
                              abilities+attacks+trainer rules for KEYWORD
                              (case-insensitive substring), independent of
                              any tag. Prints unique (name, effect) hits.
                              Expect noise for generic words -- this is a
                              completeness cross-check, not a final answer.

  --sweep-phrase "exact phrase"
                              Same as --sweep but for a literal multi-word
                              phrase (e.g. an exact Ability name like
                              "Hide 'n' Sneak") -- use this to find cards
                              that reference a *named* mechanic elsewhere in
                              their own text without owning it themselves.

  --diff                     When used with both --tags and --sweep/--sweep-phrase,
                              prints only the sweep hits NOT already covered
                              by the tag results -- the actual candidates to
                              manually review for taxonomy gaps.

Filters (apply to any mode):
  --kind ability|attack|trainer|energy
  --stage "Basic"|"Stage 1"|"Stage 2"|ex|MEGA   (matches subtypes)
  --type Grass|Fire|Water|...                    (matches Pokemon types)

Utility:
  --mulligan-table N1,N2,...   Print P(zero Basics in opening 7 of 60) for
                                 each given Basic count. Rule of thumb: aim
                                 for ~8-12 total Basics; 4 alone is ~60%.

Examples:
  python3 search_mechanic.py --suggest-tags heal
  python3 search_mechanic.py --tags heal_self,heal_team --kind ability --stage "Stage 2"
  python3 search_mechanic.py --sweep confus
  python3 search_mechanic.py --sweep-phrase "Hide 'n' Sneak"
  python3 search_mechanic.py --tags discard_own_hand_cost --sweep "hand" --diff
  python3 search_mechanic.py --mulligan-table 4,6,8,10,12
"""
import argparse
import json
import re
import sys
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4] if False else Path.cwd()


def load_cards():
    with open("pokemon_standard_cards.json") as f:
        return json.load(f)


def load_index():
    with open("mechanic_index.json") as f:
        return json.load(f)


def load_families_source():
    with open("analyze_mechanics.py") as f:
        return f.read()


def suggest_tags(keyword):
    src = load_families_source()
    index = load_index()
    fam_lookup = {f["tag"]: f for f in index["families"]}
    # Match the tag-definition lines: ("tag_name", "role", r"regex"...)
    matches = re.findall(r'\(\s*"([a-zA-Z0-9_]+)"\s*,\s*"(produce|consume)"', src)
    seen = set()
    hits = []
    for tag, role in matches:
        if tag in seen:
            continue
        seen.add(tag)
        if keyword.lower() in tag.lower():
            count = fam_lookup.get(tag, {}).get("card_count", "?")
            hits.append((tag, role, count))
    hits.sort(key=lambda x: (x[1], -x[2] if isinstance(x[2], int) else 0))
    print(f"Family tags matching {keyword!r} ({len(hits)} found):\n")
    for tag, role, count in hits:
        print(f"  {tag:45s} {role:8s} {count} cards")
    if not hits:
        print("  (none -- try a shorter/different substring, or use --sweep instead)")


def entry_matches_filters(e, cards_by_name, kind, stage, ptype):
    if kind and e["kind"] != kind:
        return False
    if stage or ptype:
        printings = cards_by_name.get(e["name"], [])
        if stage and not any(stage in (c.get("subtypes") or []) for c in printings):
            return False
        if ptype and not any(ptype in (c.get("types") or []) for c in printings):
            return False
    return True


def build_name_index(cards):
    by_name = {}
    for c in cards:
        by_name.setdefault(c["name"], []).append(c)
    return by_name


def print_tags(tags, kind, stage, ptype):
    index = load_index()
    cards = load_cards()
    by_name = build_name_index(cards)
    fam_lookup = {f["tag"]: f for f in index["families"]}

    produce_hits, consume_hits = [], []
    for e in index["entries"]:
        matched = tags & set(e["tags"])
        if not matched:
            continue
        if not entry_matches_filters(e, by_name, kind, stage, ptype):
            continue
        role = fam_lookup.get(next(iter(matched)), {}).get("role", "?")
        (produce_hits if role == "produce" else consume_hits).append((e, matched))

    for label, bucket in [("PRODUCE (cards that DO it)", produce_hits),
                           ("CONSUME (cards that benefit from / scale with it)", consume_hits)]:
        print(f"\n===== {label}: {len(bucket)} =====")
        for e, matched in bucket:
            print(f"{e['name']} | {e['kind']} | {e['effect']}  [{', '.join(sorted(matched))}]")
            if e["text"].strip():
                print(f"   {e['text']}")
    return {(e["name"], e["effect"]) for e, _ in produce_hits + consume_hits}


def sweep(keyword_or_phrase, kind, stage, ptype, exact_phrase=False):
    cards = load_cards()
    by_name = build_name_index(cards)
    hits = []
    seen = set()
    needle = keyword_or_phrase if exact_phrase else keyword_or_phrase.lower()
    for c in cards:
        blobs = []
        if c["supertype"] == "Pokémon":
            for a in c.get("abilities") or []:
                blobs.append(("ability", a["name"], a["text"]))
            for atk in c.get("attacks") or []:
                blobs.append(("attack", atk["name"], atk.get("text") or ""))
        elif c["supertype"] in ("Trainer", "Energy"):
            blobs.append((c["supertype"].lower(), c["name"], " ".join(c.get("rules") or [])))
        for kind_, effect, text in blobs:
            # Search both the effect/ability/attack NAME and its body text --
            # a card that just IS the named mechanic (e.g. an Ability whose
            # own name is the phrase) won't repeat that name in its body text.
            combined = f"{effect} {text}"
            haystack = combined if exact_phrase else combined.lower()
            if needle not in haystack:
                continue
            fake_entry = {"name": c["name"], "kind": kind_, "effect": effect, "text": text}
            if not entry_matches_filters(fake_entry, by_name, kind, stage, ptype):
                continue
            key = (c["name"], effect)
            if key in seen:
                continue
            seen.add(key)
            hits.append(fake_entry)
    print(f"\n===== RAW SWEEP for {keyword_or_phrase!r}: {len(hits)} unique hits =====")
    print("(Independent of tags -- expect noise for generic words. Cross-check")
    print(" against --tags output; review sweep-only hits by hand.)\n")
    for e in hits:
        print(f"{e['name']} | {e['kind']} | {e['effect']}")
        if e["text"].strip():
            print(f"   {e['text']}")
    return {(e["name"], e["effect"]) for e in hits}


def mulligan_table(counts):
    deck, hand = 60, 7
    print("Basics -> P(zero Basics in opening 7-card hand)")
    for n in counts:
        p = comb(deck - n, hand) / comb(deck, hand)
        flag = "  <-- risky, aim for 8-12" if n < 8 else ""
        print(f"  {n:3d}  ->  {p:.1%}{flag}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--suggest-tags", metavar="KEYWORD")
    p.add_argument("--tags", metavar="TAG1,TAG2,...")
    p.add_argument("--sweep", metavar="KEYWORD")
    p.add_argument("--sweep-phrase", metavar="PHRASE")
    p.add_argument("--diff", action="store_true")
    p.add_argument("--kind", choices=["ability", "attack", "trainer", "energy"])
    p.add_argument("--stage", metavar="SUBTYPE")
    p.add_argument("--type", metavar="POKEMON_TYPE")
    p.add_argument("--mulligan-table", metavar="N1,N2,...")
    args = p.parse_args()

    if not any([args.suggest_tags, args.tags, args.sweep, args.sweep_phrase, args.mulligan_table]):
        p.print_help()
        sys.exit(1)

    if args.mulligan_table:
        mulligan_table([int(x) for x in args.mulligan_table.split(",")])

    if args.suggest_tags:
        suggest_tags(args.suggest_tags)

    tag_keys = None
    sweep_keys = None
    if args.tags:
        tag_keys = print_tags(set(args.tags.split(",")), args.kind, args.stage, args.type)

    if args.sweep:
        sweep_keys = sweep(args.sweep, args.kind, args.stage, args.type, exact_phrase=False)
    elif args.sweep_phrase:
        sweep_keys = sweep(args.sweep_phrase, args.kind, args.stage, args.type, exact_phrase=True)

    if args.diff and tag_keys is not None and sweep_keys is not None:
        gap = sweep_keys - tag_keys
        print(f"\n===== DIFF: sweep hits NOT covered by --tags: {len(gap)} =====")
        print("(Review these by hand -- each is either a real taxonomy gap in")
        print(" analyze_mechanics.py, or coincidental noise from generic words.)\n")
        for name, effect in sorted(gap):
            print(f"  {name} -- {effect}")


if __name__ == "__main__":
    main()
