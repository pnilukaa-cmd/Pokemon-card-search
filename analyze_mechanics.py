"""Mechanic indexer for combo-mining across the Standard-legal card pool.

Extracts every ability, attack, and Trainer effect, tags each one with the
mechanical "primitive" families it touches (self-damage, damage-transfer,
heal-conditional-bonus, energy discard, hand disruption, etc.), and reports
which cards "produce" each mechanic vs which "consume"/reward it. The
narrowest producer/consumer intersections (few cards on either side) are the
most likely place to find an unused combo, since obvious high-power staples
get discovered by the wider community already -- narrow mechanical overlaps
require this kind of systematic scan instead.

Usage: python3 analyze_mechanics.py
Writes mechanic_index.json (full tagged entry list) and prints a summary
report of every mechanic family with producer/consumer counts, plus the
narrowest candidate combos.
"""
import json
import re
from collections import defaultdict

with open("pokemon_standard_cards.json") as f:
    CARDS = json.load(f)


def extract_entries():
    """One entry per unique (name, kind, effect, text) -- collapses exact
    reprints but keeps genuinely different same-named variants (e.g. the
    Grass-type Applin vs the Dragon-type Applin) since those are
    mechanically different cards."""
    seen = set()
    entries = []
    for c in CARDS:
        name = c["name"]
        types = c.get("types") or []
        if c["supertype"] == "Pokémon":
            for a in c.get("abilities") or []:
                key = (name, "ability", a["name"], a["text"])
                if key in seen:
                    continue
                seen.add(key)
                entries.append(
                    {
                        "name": name,
                        "kind": "ability",
                        "effect": a["name"],
                        "text": a["text"],
                        "types": types,
                        "hp": c.get("hp"),
                    }
                )
            for atk in c.get("attacks") or []:
                text = atk.get("text") or ""
                key = (name, "attack", atk["name"], text)
                if key in seen:
                    continue
                seen.add(key)
                entries.append(
                    {
                        "name": name,
                        "kind": "attack",
                        "effect": atk["name"],
                        "text": text,
                        "damage": atk.get("damage"),
                        "cost": atk.get("cost"),
                        "types": types,
                        "hp": c.get("hp"),
                    }
                )
        elif c["supertype"] == "Trainer":
            text = " ".join(c.get("rules") or [])
            key = (name, "trainer", name, text)
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                {
                    "name": name,
                    "kind": "trainer",
                    "effect": name,
                    "text": text,
                    "types": [],
                    "hp": None,
                }
            )
    return entries


# --- Mechanic taxonomy -------------------------------------------------
# Each family is (tag, role, regex). role is "produce" (creates/triggers the
# condition) or "consume" (rewards/reacts to the condition already being
# true). Some mechanics only have one meaningful role. Order matters where
# patterns overlap -- more specific patterns are listed first within a
# family group so a card can still match multiple distinct families.

FAMILIES = [
    # --- Damage counters ---
    ("self_damage_cost", "produce",
     r"put \d+ damage counters? on (this Pok[eé]mon|itself)"),
    ("direct_damage_no_attack", "produce",
     r"put \d+ damage counters? on (1 of your opponent|your opponent'?s)"),
    ("transfer_damage_to_opponent", "produce",
     r"move (up to )?\d* ?damage counters? from 1 of your Pok[eé]mon to (1 of )?your opponent"),
    ("transfer_damage_own", "produce",
     r"move (up to )?\d* ?damage counters? from .*to (another of your|1 of your) Pok[eé]mon"),
    ("damage_counter_move_lock", "consume",
     r"damage counters? on .*can'?t be moved"),
    ("counterattack_on_hit", "consume",
     r"damaged by an attack from your opponent'?s Pok[eé]mon.*put|place \d+ damage counters? on the Attacking"),
    ("damage_scales_with_counters_on_opponent", "consume",
     r"more damage for each damage counter on"),

    # --- Healing ---
    ("heal_self", "produce", r"heal \d+ damage from (this Pok[eé]mon|itself)"),
    ("heal_team", "produce", r"heal \d+ damage from each of your Pok[eé]mon"),
    ("heal_other_target", "produce", r"heal \d+ damage from 1 of your"),
    ("heal_all_damage", "produce", r"heal all damage from"),
    ("heal_equals_damage_dealt", "produce",
     r"heal from this Pok[eé]mon the same amount of damage"),
    ("heal_conditional_bonus", "consume",
     r"if this Pok[eé]mon was healed during this turn"),

    # --- Energy ---
    ("energy_self_discard_cost", "produce",
     r"discard (a|an|\d+) .*Energy.* (from (this Pok[eé]mon|your hand)|card from your hand) in order to use this Ability|discard.*Energy.*from your hand"),
    ("energy_discard_on_attack", "produce",
     r"discard (an? |\d+ ?)Energy from (this Pok[eé]mon|your)"),
    ("energy_discard_opponent", "produce",
     r"discard (an? |\d+ ?)Energy (card )?from your opponent"),
    ("energy_search", "produce", r"search your deck for (a |an |up to \d+ )?(Basic )?Energy"),
    ("energy_recursion", "produce", r"Energy card (from your discard pile )?into your hand"),
    ("energy_attach_bonus", "produce",
     r"attach (up to \d+ |a |an )?(Basic )?[A-Za-z]* ?Energy cards? from your (hand|discard pile)"),
    ("energy_move_between_own", "produce",
     r"move (an? |up to \d+ )?Energy from .*to (1 of your|another of your|this Pok[eé]mon)"),
    ("energy_provides_extra_type", "consume", r"provides? [A-Za-z]+ ?Energy"),
    ("damage_scales_with_energy_attached", "consume",
     r"more damage for each [A-Za-z]* ?Energy attached"),

    # --- Status conditions ---
    ("status_inflict", "produce",
     r"is now (Poisoned|Burned|Asleep|Paralyzed|Confused)"),
    ("status_cure", "produce", r"recovers? from (all )?Special Condition"),
    ("status_immune", "consume", r"can'?t be (Poisoned|Burned|Asleep|Paralyzed|Confused|Confused)|loses? any Ability that requires"),

    # --- Hand / deck disruption ---
    ("hand_discard_opponent", "produce",
     r"your opponent discards? (cards? from their hand|up to)"),
    ("hand_reveal_opponent", "produce", r"your opponent reveals? their hand"),
    ("deck_mill_opponent", "produce",
     r"discard (the top|cards? from the top) .*of your opponent'?s deck"),
    ("deck_search_pokemon", "produce", r"search your deck for (a |an |up to \d+ )?[A-Za-z].*Pok[eé]mon"),
    ("deck_search_trainer", "produce", r"search your deck for (a |an |up to \d+ )?(Supporter|Item|Stadium|Trainer)"),
    ("draw_power", "produce", r"draw \d+ cards?|draw cards? until you have"),
    ("discard_own_hand_cost", "produce",
     r"discard (a |an |\d+ )?cards? from your hand in order to use this Ability|discard \d+ (other )?cards? from your hand"),

    # --- Board control / evasion ---
    ("forced_switch_opponent", "produce",
     r"switch in 1 of your opponent'?s Benched Pok[eé]mon to the Active"),
    ("free_or_reduced_retreat_self", "produce",
     r"(no Retreat Cost|Retreat Cost is [A-Za-z]* less|has no Retreat Cost)"),
    ("retreat_cost_increase_opponent", "produce",
     r"opponent'?s Active .*Retreat Cost is [A-Za-z]* more"),
    ("retreat_prevent_opponent", "produce", r"(Defending Pok[eé]mon|Active Pok[eé]mon) can'?t retreat"),
    ("attack_lock_opponent", "produce", r"can'?t use attacks|this Pok[eé]mon takes? ?can'?t attack"),
    ("ability_lock", "produce", r"(Pok[eé]mon|opponent's Active Pok[eé]mon) has no Abilities|lose any Ability"),
    ("item_lock", "produce", r"opponent can'?t play any Item"),
    ("supporter_lock", "produce", r"opponent can'?t play any Supporter"),
    ("stadium_lock", "produce", r"opponent can'?t play any Stadium"),
    ("evolve_lock_opponent", "produce", r"opponent can'?t play any Pok[eé]mon from their hand to evolve"),

    # --- Damage math ---
    ("damage_reduction_self", "consume", r"this Pok[eé]mon takes \d+ less damage"),
    ("damage_reduction_team", "consume", r"all of your Pok[eé]mon take \d+ less damage"),
    ("damage_prevention_conditional", "consume", r"prevent all damage"),
    ("effect_prevention_conditional", "consume", r"prevent all effects"),
    ("ko_prevention", "consume", r"is not Knocked Out, and its remaining HP becomes"),
    ("weakness_modify", "produce", r"[Ww]eakness of .*is now"),
    ("damage_boost_conditional_generic", "consume",
     r"does \d+ more damage|damage does \d+ more"),

    # --- Evolution & prizes ---
    ("evolve_bonus_effect", "consume", r"When you play this Pok[eé]mon from your hand to evolve"),
    ("evolve_skip_stage", "produce", r"skipping the Stage 1|evolve during your first turn"),
    ("devolve_opponent", "produce", r"devolve 1 of your opponent'?s"),
    ("prize_bonus_self", "produce", r"take 1 more Prize card"),
    ("prize_reduction_opponent", "produce", r"takes? 1 fewer Prize card"),

    # --- Self-sacrifice / misc ---
    ("self_ko_for_effect", "produce", r"you use this Ability, this Pok[eé]mon is Knocked Out"),
    ("coin_flip_effect", "produce", r"[Ff]lip (a|\d+) coins?"),
    ("type_change_self", "produce", r"is [A-Za-z]+ and [A-Za-z]+ type"),
    ("bench_damage_spread", "produce", r"damage to each Benched Pok[eé]mon"),
]

_COMPILED = [(tag, role, re.compile(pattern, re.IGNORECASE)) for tag, role, pattern in FAMILIES]


def tag_entry(text):
    return [tag for tag, role, rx in _COMPILED if rx.search(text)]


def role_of(tag):
    for t, role, _ in FAMILIES:
        if t == tag:
            return role
    return None


def main():
    entries = extract_entries()
    for e in entries:
        e["tags"] = tag_entry(e["text"])

    tagged = [e for e in entries if e["tags"]]
    untagged = [e for e in entries if not e["tags"] and e["text"].strip()]

    print(f"Total unique effects scanned: {len(entries)}")
    print(f"Effects with >=1 recognized mechanic tag: {len(tagged)}")
    print(f"Effects with real text but no tag match: {len(untagged)}")
    print()

    by_tag = defaultdict(list)
    for e in entries:
        for t in e["tags"]:
            by_tag[t].append(e)

    print(f"{'Family':38s} {'Role':8s} {'Cards':>6s}  Example")
    print("-" * 110)
    family_rows = []
    for tag, role, _ in FAMILIES:
        members = by_tag.get(tag, [])
        names = sorted(set(m["name"] for m in members))
        example = members[0]["name"] + " (" + members[0]["effect"] + ")" if members else "-"
        family_rows.append((tag, role, len(names), names, example))
        print(f"{tag:38s} {role:8s} {len(names):>6d}  {example}")

    # --- Producer/consumer cross-reference -------------------------------
    # Group families into related pairs by shared root concept (matched by
    # prefix/keyword), then report the intersection size -- narrowest
    # combos are the most interesting (least likely to already be known).
    print()
    print("=" * 110)
    print("NARROWEST PRODUCER/CONSUMER PAIRS (candidates worth a manual look)")
    print("=" * 110)

    pairs = [
        ("self_damage_cost", "transfer_damage_to_opponent"),
        ("self_damage_cost", "damage_boost_conditional_generic"),
        ("heal_self", "heal_conditional_bonus"),
        ("heal_all_damage", "heal_conditional_bonus"),
        ("heal_team", "heal_conditional_bonus"),
        ("energy_discard_on_attack", "damage_scales_with_energy_attached"),
        ("energy_attach_bonus", "damage_scales_with_energy_attached"),
        ("status_inflict", "damage_boost_conditional_generic"),
        ("counterattack_on_hit", "damage_reduction_self"),
        ("prize_bonus_self", "prize_reduction_opponent"),
        ("evolve_bonus_effect", "evolve_skip_stage"),
        ("energy_provides_extra_type", "damage_scales_with_energy_attached"),
        ("bench_damage_spread", "damage_reduction_team"),
        ("self_ko_for_effect", "prize_reduction_opponent"),
        ("weakness_modify", "damage_boost_conditional_generic"),
    ]

    results = []
    for a_tag, b_tag in pairs:
        a_names = set(m["name"] for m in by_tag.get(a_tag, []))
        b_names = set(m["name"] for m in by_tag.get(b_tag, []))
        if not a_names or not b_names:
            continue
        overlap_score = len(a_names) + len(b_names)
        results.append((overlap_score, a_tag, len(a_names), a_names, b_tag, len(b_names), b_names))

    results.sort(key=lambda r: r[0])
    for score, a_tag, a_n, a_names, b_tag, b_n, b_names in results:
        print(f"\n{a_tag} ({a_n} cards)  <->  {b_tag} ({b_n} cards)   [combined size {score}]")
        print(f"  {a_tag}: {sorted(a_names)}")
        print(f"  {b_tag}: {sorted(b_names)}")

    print()
    print("=" * 110)
    print(f"Untagged effects with real text (review candidates for new families): {len(untagged)}")
    print("=" * 110)
    sample = untagged[:25]
    for e in sample:
        print(f"[{e['kind']}] {e['name']} :: {e['effect']} :: {e['text'][:110]}")

    with open("mechanic_index.json", "w") as f:
        json.dump(
            {
                "families": [
                    {"tag": tag, "role": role, "card_count": len(set(m["name"] for m in by_tag.get(tag, [])))}
                    for tag, role, _ in FAMILIES
                ],
                "entries": entries,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print("\nWrote mechanic_index.json")


if __name__ == "__main__":
    main()
