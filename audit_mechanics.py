"""Independent, exhaustive audit of mechanic_index.json.

Rather than re-sample, this scans every single tagged entry (not a subset)
and cross-checks it against a second, independent set of keyword/phrase
sentinels -- each sentinel names the tag families that MUST be present if
that phrase appears in the card's text. Any entry where a sentinel phrase
is found but none of its expected families are present gets printed for
manual review. This is the practical way to check "every card" rather than
literally reading 2,161 lines one at a time.
"""
import json
import re

with open("mechanic_index.json") as f:
    DATA = json.load(f)

ENTRIES = DATA["entries"]

# Universal reminder/boilerplate text that appears verbatim on every card of
# a given kind, unrelated to that specific card's actual effect -- stripped
# before running sentinels so e.g. every Tool card doesn't false-positive
# the "Pokemon Tool mechanic" check just because it IS a Tool card.
BOILERPLATE = [
    r"You may attach any number of Pok[eé]mon Tools to your Pok[eé]mon during your turn\.?"
    r" You may attach only 1 Pok[eé]mon Tool to each Pok[eé]mon,? and it stays attached\.?",
    r"You may play only 1 Stadium card during your turn\.? Put it (next to|into) the Active Spot,?"
    r" and discard it if another Stadium comes into play\.? A Stadium with the same name can[’']?t be played\.?",
    r"ACE SPEC: You can'?t have more than 1 ACE SPEC card in your deck\.?",
    r"You can'?t have more than 1 ACE SPEC card in your deck\.?",
    r"You may play (any number of Item|only 1 Supporter) cards? during your turn\.?",
    r"Any attached cards, damage counters, Special Conditions, turns in play, and any other effects remain on the new Pok[eé]mon\.?",
]


def strip_boilerplate(text):
    for pattern in BOILERPLATE:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text

# (sentinel regex, description, set of tag families where at least one
# must be present for the entry to pass)
SENTINELS = [
    (r"damage counters?", "damage counter mechanic", {
        "self_damage_cost", "self_damage_from_attack", "direct_damage_no_attack",
        "transfer_damage_to_opponent", "transfer_damage_own", "damage_counter_move_lock",
        "counterattack_on_hit", "damage_scales_with_counters_on_opponent",
        "damage_scales_with_own_damage_counters", "damage_reduces_with_own_damage_counters",
        "damage_until_hp_threshold", "damage_both_sides_ability_havers",
        "damage_both_sides_with_counters", "damage_move_opponent_side",
        "damage_on_opponent_energy_attach", "damage_on_opponent_evolve",
        "damage_on_opponent_retreat", "damage_counter_doubler", "status_checkup_damage_amp",
        "damage_on_bench_placement", "conditional_ohko_effect",
        "damage_boost_if_damage_counters_present", "status_checkup_damage_multiplier",
        "damage_on_self_energy_attach", "bench_snipe_opponent", "bench_damage_spread",
        "attack_type_substitution_conditional", "attack_base_damage_boost_next_turn",
        "damage_prevention_conditional", "self_evolve_ability",
    }),
    (r"[Hh]eal \d+ damage|heal all damage", "heal mechanic", {
        "heal_self", "heal_team", "heal_other_target", "heal_all_damage",
        "heal_equals_damage_dealt", "heal_both_players", "heal_and_cure_from",
        "damage_on_self_energy_attach", "energy_attach_bonus", "status_inflict",
        "self_switch_optional",
    }),
    (r"(Poisoned|Burned|Asleep|Paralyzed|Confused)", "status condition mechanic", {
        "status_inflict", "status_cure", "status_immune", "damage_scales_with_special_condition",
        "status_persist_through_evolve", "attack_whiff_on_coin", "double_attack_conditional",
        "damage_boost_conditional_generic", "conditional_no_effect_attack",
        "retreat_prevent_opponent", "damage_both_sides_with_counters",
        "status_checkup_damage_amp", "status_checkup_damage_multiplier", "direct_damage_no_attack",
        "damage_prevention_conditional",
    }),
    (r"Prize cards?", "prize mechanic", {
        "prize_bonus_self", "prize_reduction_opponent", "prize_peek", "prize_reshuffle",
        "damage_scales_with_prizes_taken_opponent", "damage_scales_with_prizes_taken_self",
        "attack_cost_reduction_flat_conditional", "attack_cost_reduction_scaling",
        "prize_count_threshold_conditional", "hp_scales_with_count", "draw_power",
        "damage_prevention_conditional", "energy_attach_bonus", "bench_snipe_opponent",
        "bench_snipe_opponent_all", "status_inflict", "conditional_no_effect_attack",
        "alternate_win_condition", "damage_boost_conditional_generic",
    }),
    (r"Retreat Cost", "retreat-cost mechanic", {
        "free_or_reduced_retreat_self", "retreat_cost_increase_opponent",
        "retreat_prevent_opponent", "damage_scales_with_retreat_cost",
        "attack_cost_reduction_flat_conditional", "retreat_cost_gated_energy_move",
        "damage_boost_conditional_generic", "retreat_negate_on_coin",
    }),
    (r"search (your|their) deck", "deck search mechanic", {
        "deck_search_pokemon", "deck_search_trainer", "deck_search_generic",
        "recruit_species_to_bench", "auto_evolve_chain", "search_to_bench_generic",
        "emergency_evolve_low_hp", "coin_flip_effect",
    }),
    (r"[Ff]lips? .*coins?", "coin flip mechanic", {
        "coin_flip_effect", "attack_whiff_on_coin", "coin_flip_reroll",
    }),
    (r"Pok[eé]mon Tool", "Pokemon Tool mechanic", {
        "tool_discard_opponent", "tool_discard_either_side", "tool_effect_nullify",
        "extra_tool_slot_named_group", "grants_attack_via_tool", "damage_scales_with_tools_attached",
        "restricted_attachment_named_group", "tool_swap_condition", "tool_attached_conditional_trigger",
        "deck_search_pokemon", "deck_search_generic", "item_lock", "energy_discard_opponent",
        "acespec_lock", "hand_reveal_opponent", "attack_damage_reduced_next_turn_opponent",
        "tool_discard_self", "conditional_no_effect_attack",
    }),
    (r"\bStadium\b", "Stadium-interaction mechanic", {
        "stadium_lock", "stadium_discard_effect", "damage_scales_with_card_type_in_discard",
        "damage_boost_if_stadium_in_play", "deck_search_trainer", "deck_search_generic",
        "deck_search_pokemon", "conditional_no_effect_attack", "draw_power", "heal_team",
        "status_cure", "tool_effect_nullify", "ability_lock", "damage_reduction_team",
        "self_switch_optional", "hp_modify_flat", "bench_size_modify",
        "named_group_evolve_timing_bonus", "status_persist_through_evolve",
        "damage_on_bench_placement", "attack_cost_increase_opponent",
        "opponent_turn_ends_conditional", "free_or_reduced_retreat_self",
        "retreat_cost_increase_opponent", "energy_recursion", "energy_discard_self_all",
        "stadium_discard_effect",
    }),
    (r"discards? .{0,25}(from your opponent'?s hand|their hand)", "hand-discard mechanic", {
        "hand_discard_opponent", "energy_recursion", "draw_power",
    }),
    (r"discard (the top|cards? from the top)", "deck-mill mechanic", {
        "deck_mill_opponent", "deck_discard_self_top", "mutual_deck_mill",
    }),
]

failures = []
for e in ENTRIES:
    raw_text = e["text"]
    if not raw_text.strip():
        continue
    text = strip_boilerplate(raw_text)
    tagset = set(e["tags"])
    for pattern, desc, expected in SENTINELS:
        if re.search(pattern, text, re.IGNORECASE) and not (tagset & expected):
            failures.append((e, desc, pattern))

print(f"Scanned {len([e for e in ENTRIES if e['text'].strip()])} entries with text "
      f"against {len(SENTINELS)} independent sentinel checks.")
print(f"Flagged mismatches: {len(failures)}\n")
for e, desc, pattern in failures:
    print(f"[{e['kind']}] {e['name']} :: {e['effect']}  (missing: {desc})")
    print(f"   text: {e['text']}")
    print(f"   current tags: {e['tags']}")
    print()
