"""Deck validation as a library (B1).

Everything here already existed inside check_energy_support.py's `main`,
tangled up with its printing. A deck builder needs the same answers as
DATA -- to gate a candidate, score it, or show a red underline in a UI --
so this exposes them as one call returning a structured result, with the
CLI left alone as the human-readable front end.

    from deckcheck import validate
    r = validate(open("mydeck.txt").read())
    r.ok                # nothing fatal
    r.errors            # construction-illegal: wrong size, 5th copy, 2 ACE SPEC
    r.warnings          # castable but tight, unresolved SET NUM
    r.mulligan_pct      # opening-hand whiff rate
    r.basics            # Basic Pokemon count
"""

from dataclasses import dataclass, field
from math import comb

import check_energy_support as C
import tcg_model as M


MIN_BASICS_ADVISED = 8


@dataclass
class Result:
    size: int = 0
    basics: int = 0
    mulligan_pct: float = 0.0
    ace_specs: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    unresolved: list = field(default_factory=list)
    energy_supply: dict = field(default_factory=dict)

    @property
    def ok(self):
        return not self.errors

    def summary(self):
        state = "legal" if self.ok else f"{len(self.errors)} error(s)"
        return (f"{self.size} cards, {self.basics} Basics, "
                f"mulligan {self.mulligan_pct:.1f}%, {state}")


def mulligan_pct(basics, size=60, hand=7):
    """Chance the opening hand holds no Basic Pokemon.

    Hypergeometric, and worth stating because it is the check most often
    skipped: four Basics in a 60 is a ~60% mulligan rate, not a rounding
    error.
    """
    if basics >= size or size < hand:
        return 0.0
    return 100.0 * comb(size - basics, hand) / comb(size, hand)


def validate(decklist_text, cards=None):
    cards = cards or C.load_cards()
    by_name, by_setnum = M.build_card_index(cards)
    # Two parsers, deliberately: tcg_model's keeps the SET NUM so a
    # printing can be resolved exactly, check_energy_support's is what its
    # own energy helpers expect.
    lines = M.parse_decklist_entries(decklist_text)
    pairs = C.parse_decklist(decklist_text)
    r = Result()

    resolved = []
    for entry in lines:
        card, exact = M.resolve_card(entry, by_name, by_setnum)
        if card is None:
            if not M.BASIC_ENERGY_RE.match(entry["name"]):
                r.unresolved.append(f"{entry['name']} {entry['set'] or ''} "
                                    f"{entry['number'] or ''}".strip())
                # Still counts toward the 60. A card this pool does not
                # carry is a gap in the data, not a missing card in the
                # deck, and reporting "59 cards" for it is a false error
                # on a legal list.
                r.size += entry["count"]
            continue
        if not exact and entry["set"]:
            r.warnings.append(
                f"{entry['name']} {entry['set']} {entry['number']}: this pool "
                f"carries a different printing; matched by name")
        resolved.append((entry, card))
        r.size += entry["count"]
        if (card.get("supertype") == "Pokémon" or M.fossil_stats(card)) \
                and M.stage_of(card) == "Basic":
            r.basics += entry["count"]
        if "ACE SPEC" in (card.get("subtypes") or []):
            # Per COPY, not per name. Counting distinct names let 3 copies
            # of one ACE SPEC pass as legal, which a generator will
            # produce the moment it tops a deck up to 60.
            r.ace_specs.extend([entry["name"]] * entry["count"])

    resolved_ids = {id(e) for e, _ in resolved}
    for entry in lines:
        # Basic Energy is not in the card data at all, so it never
        # resolves and has to be counted toward the 60 separately.
        if id(entry) not in resolved_ids and M.BASIC_ENERGY_RE.match(entry["name"]):
            r.size += entry["count"]

    # --- construction legality -------------------------------------------
    if r.size != 60:
        r.errors.append(f"deck is {r.size} cards, must be exactly 60")
    for entry, card in resolved:
        if entry["count"] > 4 and not M.BASIC_ENERGY_RE.match(entry["name"]):
            r.errors.append(f"{entry['count']} copies of {entry['name']} "
                            f"(limit is 4)")
    if len(r.ace_specs) > 1:
        shown = ", ".join(sorted(set(r.ace_specs)))
        r.errors.append(f"{len(r.ace_specs)} ACE SPEC cards ({shown}); "
                        f"limit is 1 across the whole deck")

    # --- playability ------------------------------------------------------
    r.mulligan_pct = mulligan_pct(r.basics, r.size or 60)
    if r.basics == 0:
        r.errors.append("no Basic Pokemon: this deck cannot start a game")
    elif r.basics < MIN_BASICS_ADVISED:
        r.warnings.append(f"{r.basics} Basics gives a {r.mulligan_pct:.1f}% "
                          f"mulligan rate; {MIN_BASICS_ADVISED}+ is advised")

    supply = C.energy_type_supply(pairs, by_name)
    r.energy_supply = dict(supply)
    for pkmn, atk_name, cost, per_type in C.attack_requirements(pairs, by_name):
        for t, need in per_type.items():
            have = supply.get(t, 0)
            line = (f"{pkmn} -- {atk_name} ({'/'.join(cost)}) needs {need}x {t}, "
                    f"deck has {have}x")
            if have < need:
                # Not a construction error -- the deck is legal, the attack
                # is simply uncastable. A builder must be able to tell those
                # apart, so it lands in warnings with an explicit label.
                r.warnings.append("UNCASTABLE: " + line)
            elif have == need:
                r.warnings.append("TIGHT: " + line)
    for name, ab_name, text in C.scan_attack_gating_abilities(pairs, by_name):
        r.warnings.append(f"ATTACK-GATED: {name} -- {ab_name}: {text}")

    return r


if __name__ == "__main__":
    import sys
    res = validate(open(sys.argv[1]).read())
    print(res.summary())
    for e in res.errors:
        print(f"  ERROR    {e}")
    for w in res.warnings:
        print(f"  warning  {w}")
    for u in res.unresolved:
        print(f"  ?        {u} did not resolve")
