"""Build a legal 60 from a seed card (B2).

Given one card you want to play, this assembles a deck around it: the
evolution line it needs, the payoff cards that reference its mechanic, an
Energy line that can actually pay its attacks, and a support shell -- then
runs it through deckcheck until it is legal.

    python3 deckbuild.py "Dhelmise" PBL 39
    python3 deckbuild.py "Sinistcha" PBL 6 --out mydeck.txt

It is deliberately NOT an optimiser. It does not measure anything, and it
does not tune counts against a win rate; see the scoping note at the
bottom of this file for why that ordering matters.
"""

import collections
import re
import sys

import ability_ir as IR
import deckcheck
import tcg_model as M

# A support shell that works in any deck: draw, search, recovery, a gust.
# Counts are the conventional ones, trimmed to fit whatever room is left.
SHELL = [
    (4, "Ultra Ball"), (4, "Poké Pad"), (3, "Lillie's Determination"),
    (2, "Boss's Orders"), (2, "Switch"), (2, "Buddy-Buddy Poffin"),
    (2, "Night Stretcher"), (2, "Professor's Research"), (2, "Iono"),
    (2, "Pokégear 3.0"), (1, "Air Balloon"), (1, "Hero's Cape"),
]

MAX_COPIES = 4
DECK_SIZE = 60
TARGET_BASICS = 12


def printing_of(card):
    pr = card.get("printings") or []
    if pr:
        return pr[0][0], pr[0][1]
    st = card.get("set") or {}
    return st.get("ptcgoCode"), str(card.get("number"))


def line(count, card):
    code, num = printing_of(card)
    if code and num:
        return f"{count} {card['name']} {code} {num}"
    return f"{count} {card['name']}"


def evolution_line(card, by_name):
    """The Basic-upward chain this card sits on, lowest stage first."""
    chain, seen = [card], {card["name"]}
    cur = card
    while cur.get("evolvesFrom"):
        prev = (by_name.get(cur["evolvesFrom"]) or [None])[0]
        if prev is None or prev["name"] in seen:
            break
        chain.insert(0, prev)
        seen.add(prev["name"])
        cur = prev
    return chain


def attack_types_needed(cards):
    """Energy types the deck must actually be able to provide."""
    need = collections.Counter()
    for c in cards:
        for atk in c.get("attacks") or []:
            for cost in atk.get("cost") or []:
                if cost != "Colorless":
                    need[cost] += 1
    return need


def mechanic_partners(card, cards, limit=6):
    """Cards that reference this card's own Ability or attack names.

    This is the step a name-only search misses: Dhelmise scales off "the
    Hide 'n' Sneak Ability" without having it, so the payoff and the
    producer never mention each other's card names.
    """
    keys = [a["name"] for a in (card.get("abilities") or [])]
    keys += [a["name"] for a in (card.get("attacks") or [])]
    # And the reverse: whatever named mechanic THIS card is looking for.
    own = " ".join((a.get("text") or "") for a in
                   (card.get("abilities") or []) + (card.get("attacks") or []))
    for m in re.finditer(r"that have the ([\w'’ ]+?) Ability", own):
        keys.append(m.group(1).strip())

    out, seen = [], {card["name"]}
    for other in cards:
        if other["name"] in seen or other.get("supertype") != "Pokémon":
            continue
        text = " ".join((a.get("text") or "") for a in
                        (other.get("abilities") or []) + (other.get("attacks") or []))
        names = [a["name"] for a in (other.get("abilities") or [])]
        if any(k and (k in text or k in names) for k in keys):
            out.append(other)
            seen.add(other["name"])
        if len(out) >= limit:
            break
    return out


def _has_draw_ability(card):
    for ab in (card.get("abilities") or []):
        eff = IR.compile_effect("ability", ab.get("name") or "",
                                ab.get("text") or "")
        if not eff.unsupported and any(a.op == IR.Op.DRAW for a in eff.actions):
            return True
    return False


_DRAW_RE = re.compile(r"\bdraw \d+ cards?\b", re.I)


def consistency_basics(cards, prefer_types=()):
    """Low-cost Basics whose Ability draws cards, best first.

    Every real decklist runs something like this, and a generator that
    does not will produce lists that mulligan out of the game.
    """
    out = []
    for c in cards:
        if c.get("supertype") != "Pokémon" or M.stage_of(c) != "Basic":
            continue
        # Single-Prize only. Sorting the whole pool by HP put Mega
        # Kangaskhan ex at the top of the "filler" list -- a 3-Prize
        # liability handed to the opponent to fix a mulligan rate.
        if {"ex", "V", "MEGA", "Tera"} & set(c.get("subtypes") or []):
            continue
        # Ask the IR whether the Ability draws, instead of pattern-matching
        # the text here. A hand-rolled regex found exactly one card in the
        # whole pool; the compiler that already parses these finds the
        # real set.
        for ab in (c.get("abilities") or []):
            eff = IR.compile_effect("ability", ab.get("name") or "",
                                    ab.get("text") or "")
            if not eff.unsupported and any(a.op == IR.Op.DRAW
                                           for a in eff.actions):
                out.append(c)
                break
    # Basics with their own draw Ability are almost nonexistent in this
    # format -- the real engines (Dudunsparce, Bibarel) are Stage 1. So
    # fall through to the Basic that EVOLVES into one, which is what a
    # real list actually runs, and finally to any cheap single-Prize body.
    draw_evolutions = {c["name"] for c in cards
                       if c.get("supertype") == "Pokémon"
                       and M.stage_of(c) != "Basic"
                       and _has_draw_ability(c)}
    tier2, tier3 = [], []
    for c in cards:
        if c.get("supertype") != "Pokémon" or M.stage_of(c) != "Basic":
            continue
        if {"ex", "V", "MEGA", "Tera"} & set(c.get("subtypes") or []):
            continue
        if any(c["name"] == o.get("evolvesFrom") for o in cards
               if o.get("name") in draw_evolutions):
            tier2.append(c)
        elif int(c.get("convertedRetreatCost") or 9) <= 1:
            tier3.append(c)

    # Cheap to retreat first, then durable: this body is support, not an
    # attacker, and one that gets stuck in the Active Spot is a liability.
    def rank(c):
        # On-type first: an off-type filler drags UNCASTABLE warnings into
        # an otherwise clean list and cannot share the Energy line.
        off = 0 if set(c.get("types") or []) & set(prefer_types) else 1
        return (off, int(c.get("convertedRetreatCost") or 9),
                -int(c.get("hp") or 0))

    out.sort(key=rank)
    tier2.sort(key=rank)
    tier3.sort(key=rank)
    return out + tier2 + tier3


def build(seed_name, set_code=None, number=None, cards=None):
    cards = cards or M.load_cards()
    by_name, by_setnum = M.build_card_index(cards)
    seed = None
    if set_code and number:
        seed = by_setnum.get((seed_name, set_code, str(number)))
    if seed is None:
        seed = (by_name.get(seed_name) or [None])[0]
    if seed is None:
        raise SystemExit(f"no card named {seed_name!r} in the pool")

    pokemon, notes = [], []
    chain = evolution_line(seed, by_name)
    # An evolution needs at least as many of its pre-evolution, or the line
    # is dead cards. A Stage 1 payoff at 3 wants 4 of its Basic.
    for i, c in enumerate(chain):
        want = MAX_COPIES if i < len(chain) - 1 else 3
        pokemon.append((want, c))
    if len(chain) > 1:
        notes.append(f"evolution line: {' -> '.join(c['name'] for c in chain)}")

    for partner in mechanic_partners(seed, cards, limit=3):
        pchain = evolution_line(partner, by_name)
        for i, c in enumerate(pchain):
            if any(c["name"] == p["name"] for _, p in pokemon):
                continue
            pokemon.append((2 if i == len(pchain) - 1 else 3, c))
        notes.append(f"mechanic partner: {partner['name']}")

    # Basics floor: a deck that mulligans is not a deck. Four Basics is a
    # ~60% mulligan rate, which is what a naive build lands on whenever the
    # seed card has no evolution line to pad it out.
    def count_basics():
        return sum(n for n, c in pokemon if M.stage_of(c) == "Basic")

    for idx, (n, c) in enumerate(list(pokemon)):
        if count_basics() >= TARGET_BASICS:
            break
        if M.stage_of(c) == "Basic" and n < MAX_COPIES:
            pokemon[idx] = (min(MAX_COPIES, n + TARGET_BASICS - count_basics()), c)

    # Still short means the deck simply has too few Basic species, and no
    # amount of raising counts fixes it -- it needs another body. Prefer a
    # Basic that draws cards, which is what a real list would reach for.
    if count_basics() < TARGET_BASICS:
        have = {c["name"] for _, c in pokemon}
        deck_types = {t for _, c in pokemon for t in (c.get('types') or [])}
        for filler in consistency_basics(cards, deck_types):
            if filler["name"] in have:
                continue
            take = min(MAX_COPIES, TARGET_BASICS - count_basics())
            pokemon.append((take, filler))
            notes.append(f"consistency Basic added for the mulligan floor: "
                         f"{filler['name']}")
            if count_basics() >= TARGET_BASICS:
                break

    poke_count = sum(n for n, _ in pokemon)

    # Energy: cover every non-Colorless cost the chosen Pokemon demand.
    needed = attack_types_needed([c for _, c in pokemon])
    types = [t for t, _ in needed.most_common(2)] or ["Psychic"]
    energy_total = 8 if len(types) == 1 else 10
    energy = []
    per = energy_total // len(types)
    for i, t in enumerate(types):
        n = per + (energy_total - per * len(types) if i == 0 else 0)
        energy.append((n, f"Basic {t} Energy"))

    # Trainers fill whatever is left.
    room = DECK_SIZE - poke_count - energy_total
    trainers = []
    for n, name in SHELL:
        if room <= 0:
            break
        card = (by_name.get(name) or [None])[0]
        if card is None:
            continue
        take = min(n, room)
        # One ACE SPEC in the whole deck, ever.
        if "ACE SPEC" in (card.get("subtypes") or []):
            take = min(take, 1)
        trainers.append((take, card))
        room -= take
    # Top up whatever room is left by raising existing counts toward 4,
    # cheapest-to-justify first. Dumping the remainder onto one card was
    # the obvious shortcut and it produces 21 Ultra Ball.
    i = 0
    while room > 0 and trainers:
        n, card = trainers[i % len(trainers)]
        cap = 1 if "ACE SPEC" in (card.get("subtypes") or []) else MAX_COPIES
        if n < cap:
            trainers[i % len(trainers)] = (n + 1, card)
            room -= 1
        elif all(n >= (1 if "ACE SPEC" in (c.get("subtypes") or [])
                       else MAX_COPIES) for n, c in trainers):
            break
        i += 1
    if room > 0:
        # Nothing legal left to add: give the slots to Energy rather than
        # emit an illegal list.
        energy[0] = (energy[0][0] + room, energy[0][1])
        energy_total += room
        room = 0

    out = [f"Pokémon: {poke_count}"]
    out += [line(n, c) for n, c in pokemon]
    out.append("")
    out.append(f"Trainer: {sum(n for n, _ in trainers)}")
    out += [line(n, c) for n, c in trainers]
    out.append("")
    out.append(f"Energy: {energy_total}")
    out += [f"{n} {name}" for n, name in energy]
    out.append("")
    out.append(f"Total Cards: {DECK_SIZE}")
    return "\n".join(out), notes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    name = args[0]
    code = args[1] if len(args) > 1 else None
    num = args[2] if len(args) > 2 else None

    text, notes = build(name, code, num)
    res = deckcheck.validate(text)

    print(text)
    print()
    print(f"# {res.summary()}")
    for n in notes:
        print(f"# {n}")
    for e in res.errors:
        print(f"# ERROR   {e}")
    for w in res.warnings[:6]:
        print(f"# warning {w}")

    out = next((a for a in sys.argv if a.startswith("--out=")), None)
    if out:
        path = out.split("=", 1)[1]
        open(path, "w").write(text + "\n")
        print(f"# written to {path}")


# Scoping note. This stops at "a legal, coherent 60 built around one
# card". It deliberately does not search for the BEST 60, because an
# optimiser maximises whatever the simulator reports, and the simulator's
# blind spots are the cheapest thing for it to find. Automated deck
# search waits on the coverage bar in the scoping doc.
if __name__ == "__main__":
    main()
