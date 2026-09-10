#!/usr/bin/env python3
"""Audit every ex / Mega ex Pokemon in the pool, card by card.

Three questions, kept separate because they fail independently:
  1. Does the card's text COMPILE to IR at all?
  2. Does the simulator's damage model read a real number off the attack?
  3. Is the Prize value right (ex = 2, Mega ex = 3)?

Usage: python3 audit_ex.py [--bucket] [--show REASON] [--name NAME]
"""
import collections
import json
import sys

import ability_ir as IR
import tcg_model as M


def is_ex(card):
    st = card.get("subtypes") or []
    return "ex" in st or "MEGA" in st


def load():
    cards = M.load_cards()
    return [c for c in cards if c.get("supertype") == "Pokémon" and is_ex(c)]


def prizes_for(card):
    """What the sim will award for KOing this card."""
    text = " ".join(card.get("rules") or [])
    st = card.get("subtypes") or []
    if "MEGA" in st:
        return 3, ("3 Prize cards" in text)
    if "ex" in st:
        return 2, ("2 Prize cards" in text or "3 Prize cards" in text)
    return 1, True


def audit():
    ex = load()
    seen = {}
    for c in ex:
        seen.setdefault(c["name"], c)          # one entry per name
    rows = []
    for name, card in sorted(seen.items()):
        effs = []
        for ab in card.get("abilities") or []:
            e = IR.compile_effect("ability", ab.get("name") or "", ab.get("text") or "")
            effs.append(("ability", ab.get("name"), ab.get("text") or "", e))
        for at in card.get("attacks") or []:
            txt = at.get("text") or ""
            e = IR.compile_effect("attack", at.get("name") or "", txt) if txt.strip() else None
            effs.append(("attack", at.get("name"), txt, e))
        rows.append((name, card, effs))
    return rows


def main():
    rows = audit()
    show = None
    if "--show" in sys.argv:
        show = sys.argv[sys.argv.index("--show") + 1]
    only = None
    if "--name" in sys.argv:
        only = sys.argv[sys.argv.index("--name") + 1]

    reasons = collections.Counter()
    dead_by_card = collections.defaultdict(list)
    n_eff = n_bad = 0
    prize_bad = []
    no_damage = []

    for name, card, effs in rows:
        if only and only.lower() not in name.lower():
            continue
        p, ok = prizes_for(card)
        if not ok:
            prize_bad.append((name, p, " ".join(card.get("rules") or [])[:70]))
        for kind, ename, text, e in effs:
            if kind == "attack" and not text.strip():
                dmg = card_damage(card, ename)
                if dmg is None:
                    no_damage.append((name, ename))
                continue
            n_eff += 1
            if e is None or e.unsupported:
                n_bad += 1
                why = e.unsupported if e else "not compiled"
                reasons[why] += 1
                dead_by_card[name].append((kind, ename, why, text))

    print(f"===== ex / Mega ex cards audited: "
          f"{len([r for r in rows if not only or only.lower() in r[0].lower()])} "
          f"unique names =====")
    print(f"effects with text: {n_eff}   compiled: {n_eff-n_bad} "
          f"({100*(n_eff-n_bad)/max(n_eff,1):.1f}%)   dead: {n_bad}\n")

    print("===== dead effects, by reason =====")
    for why, k in reasons.most_common():
        print(f"  {k:4d}  {why}")

    if prize_bad:
        print(f"\n===== Prize-value text mismatch: {len(prize_bad)} =====")
        for n, p, t in prize_bad[:20]:
            print(f"  {n:38s} expected {p}  rules: {t}")

    if show:
        print(f"\n===== cards failing with reason containing '{show}' =====")
        for name in sorted(dead_by_card):
            for kind, ename, why, text in dead_by_card[name]:
                if show.lower() in why.lower():
                    print(f"  {name} / {kind} {ename}\n      [{why}] {text[:150]}")

    if only:
        print(f"\n===== detail for '{only}' =====")
        for name, card, effs in rows:
            if only.lower() not in name.lower():
                continue
            print(f"\n{name}  HP {card.get('hp')}  {card.get('types')} "
                  f"{card.get('subtypes')}  from {card.get('evolvesFrom')}  "
                  f"{card.get('printings')}")
            for kind, ename, text, e in effs:
                mark = "ok " if (e and e.ok()) else ("-- " if text.strip() else "raw")
                print(f"   {mark} {kind:7s} {ename}")
                if text.strip():
                    print(f"        {text[:150]}")
                if e and e.unsupported:
                    print(f"        UNSUPPORTED: {e.unsupported}")


def card_damage(card, attack_name):
    for a in card.get("attacks") or []:
        if a.get("name") == attack_name:
            return a.get("damage")
    return None


if __name__ == "__main__":
    main()
