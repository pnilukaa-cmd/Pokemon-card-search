#!/usr/bin/env python3
"""Every deck file must be legal, resolvable, and match the measured field.

Three ways a deck file has silently gone wrong in this project:

  1. A line with no SET NUM. The simulator falls back to the FIRST printing
     of that name, which can be a different card -- water_aggro resolved
     `Palafin` to TEF 49, a printing with no Zero to Hero, so its Palafin ex
     had no legal way into play in any game it ever played.
  2. A set code that is not in this pool at all (a rotated card, or a typo
     like `MEE 7` on a Basic Energy line, which takes no set code).
  3. The decklist in decks/<name>.md drifting away from the copy that was
     actually measured.

Usage:  python3 check_decks.py [field-dir]
"""
import glob
import os
import re
import sys

import deckcheck
import tcg_model as M


def decklist_in(md_text):
    for b in re.findall(r"```\n(.*?)```", md_text, re.S):
        if "Total Cards:" in b:
            return b
    return None


def main():
    field = sys.argv[1] if len(sys.argv) > 1 else None
    cards = M.load_cards()
    by_name, by_setnum = M.build_card_index(cards)
    pool_sets = {p[0] for c in cards for p in (c.get("printings") or [])}

    problems = []
    for md in sorted(glob.glob(os.path.join("decks", "*.md"))):
        slug = os.path.basename(md)[:-3]
        text = open(md).read()
        deck = decklist_in(text)
        if deck is None:
            continue                      # a research note, not a deck
        res = deckcheck.validate(deck)
        for e in res.errors:
            problems.append((slug, "ILLEGAL", e))
        for entry in M.parse_decklist_entries(deck):
            nm, code, num = entry["name"], entry["set"], entry["number"]
            if "Energy" in nm and not code:
                continue                  # Basic Energy carries no set code
            if not code:
                problems.append((slug, "NO SET NUM", nm))
            elif code not in pool_sets:
                problems.append((slug, "SET NOT IN POOL", f"{nm} {code} {num}"))
            elif not by_setnum.get((nm, code, str(num))):
                have = (by_name.get(nm) or [None])[0]
                problems.append((slug, "PRINTING NOT IN POOL",
                                 f"{nm} {code} {num}; pool has "
                                 f"{have.get('printings') if have else None}"))
        if field:
            twin = os.path.join(field, slug + ".txt")
            if not os.path.exists(twin):
                problems.append((slug, "NOT IN FIELD",
                                 "has a decklist but was never measured"))
            else:
                def bag(t):
                    # Compare CONTENTS, not line order -- the Trainer
                    # section gets reordered by hand all the time and that
                    # is not a drift.
                    return sorted((e["count"], e["name"], e["set"], e["number"])
                                  for e in M.parse_decklist_entries(t))
                if bag(open(twin).read()) != bag(deck):
                    problems.append((slug, "DRIFT",
                                     "decks/*.md does not match the measured "
                                     "copy"))

    if field:
        for t in sorted(glob.glob(os.path.join(field, "*.txt"))):
            slug = os.path.basename(t)[:-4]
            if not os.path.exists(os.path.join("decks", slug + ".md")):
                problems.append((slug, "NO DECK FILE",
                                 "measured but has no decks/*.md"))

    for slug, kind, detail in problems:
        print(f"  {kind:22s} {slug:46s} {detail}")
    print(f"\n{len(problems)} problem(s) across "
          f"{len(glob.glob(os.path.join('decks', '*.md')))} deck files")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
