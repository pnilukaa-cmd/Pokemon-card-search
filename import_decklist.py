"""import_decklist.py -- turn a published decklist into one this pool plays.

    python3 import_decklist.py LIST.txt --slug meta_ogerpon_meganium \
        --source "Limitless, Regional Recife 2026, 1st, <player>" [--write]

LIST.txt (or - for stdin) is a PTCGL / Limitless export: "4 Dreepy TWM 128"
lines under Pokemon / Trainer / Energy headers. Every line is resolved
against pokemon_standard_cards.json:

- **exact**: the SET NUM is in this pool under that name.
- **reprint**: a Trainer or Energy whose SET NUM this pool doesn't carry. Same
  name means same card, so it maps to the pool's printing.
- **same card**: a Pokemon whose SET NUM isn't here but whose every pool
  printing has the same attacks and Abilities, so any printing plays the same.
- **AMBIGUOUS**: a Pokemon whose pool printings differ (Pikachu ex) and the
  SET NUM picks none of them. Nothing is guessed; the line must be fixed.
- **NOT IN POOL**: no card of that name is Standard-legal here (rotated, or
  a typo). Nothing is guessed.

This pool carries one printing per card (SKILL.md 4b), so a SET NUM missing
here is not proof the source is wrong: the report says "this pool carries
X" and never "your number is wrong".

Without --write it only reports. With --write, and no AMBIGUOUS or NOT IN
POOL lines, it writes decks/field/<slug>.txt (pool printings) and
decks/<slug>.md (provenance: source, every mapped line, the checks).
"""
import argparse
import json
import re
import sys
from collections import defaultdict

import tcg_model as M

TYPES = ("Grass", "Fire", "Water", "Lightning", "Psychic", "Fighting",
         "Darkness", "Metal")
_ENERGY_RE = re.compile(r"^(?:Basic )?(" + "|".join(TYPES) + r") Energy$")


def _norm(name):
    """Site spellings to the pool's: curly apostrophes, 'Pokemon'."""
    name = name.replace("’", "'").replace("‘", "'").strip()
    name = re.sub(r"\bPokemon\b", "Pokémon", name)
    return re.sub(r"\s+", " ", name)


def _setcode(card):
    s = card.get("set") or {}
    return s.get("ptcgoCode") if isinstance(s, dict) else None


def _version(card):
    """What makes two printings of a Pokemon play differently."""
    return (card.get("hp"),
            tuple((a.get("name"), a.get("text")) for a in card.get("abilities") or []),
            tuple((a.get("name"), tuple(a.get("cost") or []), a.get("damage"),
                   a.get("text")) for a in card.get("attacks") or []))


def _fold(name):
    """Accent- and case-insensitive key: 'Pokegear' finds 'Pokégear 3.0'."""
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFKD", _norm(name))
                   if not unicodedata.combining(ch)).lower()


def index():
    """The pool's own index, which knows every printing of each card."""
    cards = M.load_cards()
    by_name, by_setnum = M.build_card_index(cards)
    by_name = dict(by_name)
    folded = {_fold(n): n for n in by_name}
    sets = {code for (_, code, _) in by_setnum}
    return by_name, by_setnum, sets, folded


def resolve(entries, by_name, by_setnum, sets, folded):
    """[(count, out_line, status, note)] for every parsed entry."""
    rows = []
    for e in entries:
        n, name = e["count"], _norm(e["name"])
        name = folded.get(_fold(name), name)
        code, num = e.get("set"), e.get("number")
        m = _ENERGY_RE.match(name)
        if m and (not code or (name, code, str(num)) not in by_setnum
                  or "Basic" in (by_setnum[(name, code, str(num))].get("subtypes") or [])):
            rows.append((n, f"Basic {m.group(1)} Energy", "exact", ""))
            continue
        if code and num and (name, code, str(num)) in by_setnum:
            rows.append((n, f"{name} {code} {num}", "exact", ""))
            continue
        cands = by_name.get(name, [])
        src = f"{code} {num}" if code else "no SET NUM"
        if not cands:
            why = (f"set {code} is not in this pool (rotated?)" if code and code not in sets
                   else "no card of this name in the pool")
            rows.append((n, f"{name} {src}", "NOT IN POOL", why))
            continue
        pick = cands[0]
        if cands[0]["supertype"] == "Pokémon":
            versions = {_version(c) for c in cands}
            if len(versions) > 1:
                same_set = [c for c in cands if _setcode(c) == code]
                if len(same_set) == 1:
                    pick = same_set[0]
                else:
                    opts = ", ".join(f"{_setcode(c)} {c['number']}" for c in cands)
                    rows.append((n, f"{name} {src}", "AMBIGUOUS",
                                 f"pool printings differ: {opts}"))
                    continue
            status = "same card"
        else:
            status = "reprint"
        out = f"{name} {_setcode(pick)} {pick['number']}"
        gone = " (set not in this pool)" if code and code not in sets else ""
        rows.append((n, out, status,
                     f"{src}{gone} -> this pool carries {_setcode(pick)} {pick['number']}"))
    return rows


def checks(rows, by_name):
    """Construction legality on the resolved lines."""
    problems = []
    total = sum(n for n, *_ in rows)
    if total != 60:
        problems.append(f"{total} cards, not 60")
    per_name = defaultdict(int)
    ace = 0
    for n, line, status, _ in rows:
        if line.startswith("Basic "):
            continue
        name = re.sub(r" [A-Z0-9-]+ \d+$", "", line)
        per_name[name] += n
        card = (by_name.get(name) or [{}])[0]
        if "ACE SPEC" in (card.get("subtypes") or []):
            ace += n
    problems += [f"{k}: {v} copies" for k, v in per_name.items() if v > 4]
    if ace > 1:
        problems.append(f"{ace} ACE SPEC cards")
    return problems


def render(rows, by_name):
    sec = {"Pokémon": [], "Trainer": [], "Energy": []}
    for n, line, *_ in rows:
        if line.startswith("Basic "):
            sec["Energy"].append(f"{n} {line}")
            continue
        name = re.sub(r" [A-Z0-9-]+ \d+$", "", line)
        sup = (by_name.get(name) or [{"supertype": "Trainer"}])[0]["supertype"]
        sec[sup].append(f"{n} {line}")
    out = []
    for head, lines in sec.items():
        out.append(f"{head}: {sum(int(x.split()[0]) for x in lines)}")
        out += lines + [""]
    out.append(f"Total Cards: {sum(n for n, *_ in rows)}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--slug")
    ap.add_argument("--source", default="")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dir", default="decks", help="where decks/ is (tests)")
    a = ap.parse_args()
    text = sys.stdin.read() if a.path == "-" else open(a.path).read()
    by_name, by_setnum, sets, folded = index()
    rows = resolve(M.parse_decklist_entries(text), by_name, by_setnum, sets, folded)
    for n, line, status, note in rows:
        print(f"  {status:12s} {n} {line}" + (f"   ({note})" if note else ""))
    bad = [r for r in rows if r[2] in ("AMBIGUOUS", "NOT IN POOL")]
    problems = checks(rows, by_name)
    for p in problems:
        print(f"  ILLEGAL      {p}")
    if not a.write:
        return 1 if bad or problems else 0
    if bad or problems:
        print("not written: fix the lines above first")
        return 1
    if not a.slug:
        print("--slug is required with --write")
        return 1
    deck = render(rows, by_name)
    import os
    os.makedirs(f"{a.dir}/field", exist_ok=True)
    open(f"{a.dir}/field/{a.slug}.txt", "w").write(deck)
    mapped = []
    for n, line, st, note in rows:
        if st in ("reprint", "same card"):
            name = re.sub(r" [A-Z0-9-]+ \d+$", "", line)
            mapped.append(f"- `{n} {name} {note.split(' -> ')[0]}` -> `{line}` ({st})")
    md = [f"# {a.slug}", "", f"**Not my list.** Source: {a.source or 'not given'}.",
          "Reproduced card-for-card; imported with `import_decklist.py`.", ""]
    if mapped:
        md += ["Lines this pool carries under another printing (same card):", ""] + mapped + [""]
    md += ["## PTCGL import", "", "```", deck.rstrip(), "```", ""]
    open(f"{a.dir}/{a.slug}.md", "w").write("\n".join(md))
    print(f"wrote {a.dir}/field/{a.slug}.txt and {a.dir}/{a.slug}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
