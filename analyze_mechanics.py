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
        elif c["supertype"] == "Energy":
            text = " ".join(c.get("rules") or [])
            if not text.strip():
                continue  # Basic Energy: no rules text, nothing to tag
            key = (name, "energy", name, text)
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                {
                    "name": name,
                    "kind": "energy",
                    "effect": name,
                    "text": text,
                    "types": types,
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
    ("self_damage_from_attack", "produce",
     r"also does? \d+ damage to (itself|this Pok[eé]mon)"),
    ("direct_damage_no_attack", "produce",
     r"put \d+ damage counters? on (1 of |each of )?your opponent'?s|place \d+ damage counters? on (1 of |each of )?your opponent|"
     r"put \d+ damage counters? on the Defending Pok[eé]mon|"
     r"put \d+ damage counters? on each of them|"
     r"put \d+ more damage counters? on your opponent'?s Poisoned Pok[eé]mon during Pok[eé]mon Checkup"),
    ("damage_both_sides_ability_havers", "produce",
     r"damage counters? on each Pok[eé]mon that has an Ability"),
    ("transfer_damage_to_opponent", "produce",
     r"move (up to \d+|all|any number of)? ?damage counters? from (1 of your|your) [\w' ]*Pok[eé]mon to (1 of )?your opponent"),
    ("transfer_damage_own", "produce",
     r"move (up to )?\d* ?damage counters? from .*to (another of your|1 of your) Pok[eé]mon"),
    ("damage_move_opponent_side", "produce",
     r"damage counters? from (your opponent'?s|1 of your opponent'?s) Benched Pok[eé]mon to (their|your opponent'?s) Active"),
    ("damage_both_sides_with_counters", "produce",
     r"damage to each Pok[eé]mon that has any damage counters on it|"
     r"damage for each( of your| of your opponent'?s)? Pok[eé]mon.{0,40}that has any damage counters on it"),
    ("damage_counter_move_lock", "consume",
     r"damage counters? on .*can'?t be moved"),
    ("counterattack_on_hit", "consume",
     r"(damaged|Knocked Out) by (damage from )?an attack( from your opponent'?s Pok[eé]mon)?.*(put|place) \d+ damage counters? on the Attacking|"
     r"equal to the damage done to this Pok[eé]mon|"
     r"takes \d+ or more damage from an attack.*place \d+ damage counters? on the Attacking"),
    ("damage_scales_with_counters_on_opponent", "consume",
     r"more damage for each damage counter on|damage for each damage counter on (your opponent|1 of your opponent|all of your opponent)"),
    ("damage_scales_with_own_damage_counters", "consume",
     r"damage for each damage counter (on this Pok[eé]mon|you placed|on all of your)"),
    ("damage_reduces_with_own_damage_counters", "consume",
     r"less damage for each damage counter on this Pok[eé]mon"),
    ("conditional_ohko_effect", "consume",
     r"(it is|that Pok[eé]mon is) Knocked Out\.?\s*$|is Knocked Out\.(?!\s*\()|^Knock Out (\d+|each|1) "),
    ("damage_until_hp_threshold", "produce",
     r"damage counters? on .*until its remaining HP is"),
    ("status_checkup_damage_amp", "produce",
     r"during Pok[eé]mon Checkup, put \d+ more damage counters? on (your opponent'?s |each )?(Burned|Poisoned)"),
    ("mutual_ko", "produce", r"[Bb]oth Active Pok[eé]mon are (now )?Knocked Out"),

    # --- Healing ---
    ("heal_self", "produce",
     r"heal \d+ damage from (this Pok[eé]mon|itself|your Active [A-Za-z]* ?Pok[eé]mon)"),
    ("heal_team", "produce", r"heal \d+ damage from each of (your|their) [A-Za-z]* ?Pok[eé]mon"),
    ("heal_other_target", "produce", r"heal \d+ damage from 1 of your"),
    ("heal_all_damage", "produce", r"heal all damage from"),
    ("heal_equals_damage_dealt", "produce",
     r"heal from this Pok[eé]mon the same amount of damage"),
    ("heal_conditional_bonus", "consume",
     r"if this Pok[eé]mon was healed during this turn"),
    ("heal_both_players", "produce", r"heal \d+ damage from each Pok[eé]mon \(both yours and your opponent"),

    # --- Energy ---
    ("energy_self_discard_cost", "produce",
     r"discard (a|an|\d+) .*Energy.* (from (this Pok[eé]mon|your hand)|card from your hand) in order to use this Ability|discard.*Energy.*from your hand"),
    ("energy_discard_self_all", "produce",
     r"discard (all|up to \d+|any amount of) .*Energy (from|attached to) this Pok[eé]mon|discard all Energy from this"),
    ("energy_discard_on_attack", "produce",
     r"discard (an? |\d+ ?|all )?[A-Za-z]* ?Energy from (this Pok[eé]mon|your)"),
    ("energy_discard_opponent", "produce",
     r"discard (an? |\d+ ?|all )?[A-Za-z]* ?Energy (card )?from (1 of )?your opponent|discard all .*Energy from all of your opponent"),
    ("energy_search", "produce", r"search your deck for (a |an |up to \d+ |any number of )?(Basic )?Energy"),
    ("energy_recursion", "produce",
     r"Energy cards? (from (your|their) discard pile )?into (your|their) hand|Energy .*discard pile into (your|their) hand"),
    ("energy_shuffle_from_discard", "produce",
     r"[Ss]huffle (up to \d+ )?(Basic )?[A-Za-z]* ?Energy cards? from your discard pile into your deck"),
    ("energy_attach_bonus", "produce",
     r"attach (up to \d+ |a |an |any number of )?(Basic )?[A-Za-z]* ?Energy cards? (from your (hand|discard pile)|you find there)|"
     r"attach .*Energy card.*from your hand to your Pok[eé]mon"),
    ("energy_attach_to_opponent", "produce",
     r"[Ee]nergy cards? from your opponent'?s discard pile to their"),
    ("energy_move_between_own", "produce",
     r"move (an? |\d+ |up to \d+ |all |any amount of )?([A-Za-z]+ ){0,2}Energy from .*to (1 of your|another of your|this Pok[eé]mon|your Bench|your Benched|your other|your Active)"),
    ("energy_bounce_self_to_hand", "produce",
     r"[Pp]ut (an?|\d+) [A-Za-z]* ?Energy attached to this Pok[eé]mon into your hand"),
    ("energy_bounce_from_opponent", "produce",
     r"Energy attached to your opponent'?s Active( [\w']+){0,2} Pok[eé]mon into (their|your) hand"),
    ("energy_move_opponent_side", "produce",
     r"[Mm]ove an Energy from (1 of )?your opponent'?s( Active)? Pok[eé]mon to (1 of |another of )?their"),
    ("energy_shuffle_self_into_deck", "produce",
     r"[Ss]huffle (all Energy attached to this Pok[eé]mon|this Pok[eé]mon'?s Energy) into your deck"),
    ("energy_provides_extra_type", "consume",
     r"provides? [A-Za-z]+ ?Energy|provides? \d+ in any combination of"),
    ("restricted_attachment_named_group", "produce",
     r"can only be attached to a [\w' ]+'s Pok[eé]mon"),
    ("damage_scales_with_energy_attached", "consume",
     r"more damage for each [A-Za-z]* ?Energy attached|"
     r"damage for each [A-Za-z]* ?Energy( card)? attached to (this Pok[eé]mon|all)|"
     r"damage for each [A-Za-z]* ?Energy attached to your opponent'?s Active"),
    ("damage_scales_with_energy_in_discard", "consume",
     r"damage for each (Basic )?[A-Za-z]* ?Energy card in your (opponent'?s )?discard pile"),
    ("damage_scales_with_discard_count", "consume",
     r"damage for each card you discarded in this way"),
    ("attack_cost_free_conditional", "consume",
     r"ignore all (Colorless )?Energy in (this attack'?s|the) cost"),

    # --- Status conditions ---
    ("status_inflict", "produce",
     r"(is|are) now (Poisoned|Burned|Asleep|Paralyzed|Confused)|"
     r"make your opponent'?s Active Pok[eé]mon (Asleep|Burned|Confused|Paralyzed|Poisoned)"),
    ("double_attack_conditional", "consume", r"may use an attack it has twice"),
    ("status_cure", "produce", r"recovers? from (all )?Special Condition"),
    ("status_immune", "consume", r"can'?t be (Poisoned|Burned|Asleep|Paralyzed|Confused|Confused)|loses? any Ability that requires"),
    ("damage_scales_with_special_condition", "consume",
     r"damage for each Special Condition affecting"),
    ("conditional_no_effect_attack", "consume", r"this attack does nothing"),
    ("coin_flip_effect", "produce", r"[Ff]lips? (a|\d+|two) coins?"),
    ("attack_whiff_on_coin", "consume", r"flips? (a|\d+|two) coins?\.? ?If (tails|either)"),

    # --- Hand / deck disruption ---
    ("hand_discard_opponent", "produce",
     r"your opponent discards?|from your opponent'?s hand|opponent'?s hand.*shuffles?"),
    ("hand_reveal_opponent", "produce", r"your opponent reveals? their hand"),
    ("hand_shuffle_into_deck_opponent", "produce",
     r"shuffles? (it|that card|those cards|their hand) into (their|your opponent'?s) deck"),
    ("deck_mill_opponent", "produce",
     r"discard (the top|cards? from the top) .*of your opponent'?s deck"),
    ("deck_discard_self_top", "produce",
     r"discard the top( \d+)? cards? of your deck|look at the top card of your deck\. ?You may discard that card"),
    ("deck_search_pokemon", "produce", r"search (your|their) deck for (a |an |up to \d+ )?[A-Za-z].*Pok[eé]mon"),
    ("deck_search_trainer", "produce", r"search (your|their) deck for (a |an |up to \d+ )?(Supporter|Item|Stadium|Trainer)"),
    ("deck_search_generic", "produce",
     r"search (your|their) deck for (a |an |up to \d+ |any number of )?[\w' ]{0,25}cards?\b"),
    ("search_to_bench_generic", "produce", r"put (them|it|those Pok[eé]mon) onto (your|their) Bench"),
    ("recruit_species_to_bench", "produce",
     r"search your deck for up to \d+ [A-Z][\w'’]* and put (them|it) onto (your|their) Bench"),
    ("bench_recruit_from_discard", "produce",
     r"Pok[eé]mon from your discard pile onto (your|their) Bench|"
     r"[A-Z][\w']* from your discard pile onto (your|their) Bench"),
    ("deck_peek_opponent_top", "produce", r"look at the top card of your opponent'?s deck"),
    ("hand_to_deck_top_self", "produce",
     r"put a card from (your|their) hand on top of (your|their) deck"),
    ("deck_peek_keep_any", "produce",
     r"look at the top \d+ cards? of your (deck|opponent'?s deck).*(put|reveal).*(into your hand|onto (your|their) Bench)"),
    ("deck_peek_reorder", "produce", r"put (them|the other cards) back in any order"),
    ("deck_stack_top", "produce", r"put (those|these|them) (cards? )?(on|back on) top of (it|your deck)"),
    ("draw_power", "produce",
     r"draw (a card|\d+ cards?)|draw cards? until (you|they) have"),
    ("draw_scales_with_count", "produce", r"[Dd]raw a card for each"),
    ("mutual_draw", "produce", r"each player draws?"),
    ("discard_own_hand_cost", "produce",
     r"discard (a |an |\d+ |any number of |random )?cards? from your hand in order to use this Ability|discard \d+ (other )?cards? from your hand|discard any number of cards from your hand"),
    ("discard_pile_recursion_pokemon", "produce",
     r"Pok[eé]mon (card )?(from|s from) your discard pile into your hand"),
    ("discard_pile_recursion_supporter", "produce",
     r"Supporter cards? from your discard pile into your hand"),
    ("discard_pile_recursion_trainer", "produce",
     r"Trainer cards? from your discard pile into your hand"),
    ("self_bounce_to_hand", "produce",
     r"[Pp]ut (this Pok[eé]mon|1 of your (Benched )?Pok[eé]mon) and all attached cards into your hand|"
     r"[Pp]ut this Pok[eé]mon into your hand\. \(Discard all cards attached"),
    ("self_shuffle_into_deck", "produce",
     r"[Ss]huffle (it|this Pok[eé]mon|1 of your Benched Pok[eé]mon) and all attached cards into your deck"),
    ("self_discard_no_ko", "produce", r"[Dd]iscard this Pok[eé]mon and all attached cards"),
    ("opponent_pokemon_discard_no_ko", "produce",
     r"[Dd]iscard (your opponent'?s Active Pok[eé]mon|the Defending Pok[eé]mon) and all attached cards"),

    # --- Board control / evasion ---
    ("forced_switch_opponent", "produce",
     r"switch in 1 of your opponent'?s Benched Pok[eé]mon to the Active"),
    ("force_active_to_bench_opponent", "produce",
     r"[Ss]witch out your opponent'?s Active Pok[eé]mon to the Bench"),
    ("self_switch_optional", "produce",
     r"[Ss]witch (this Pok[eé]mon|(your|their) Active( [\w']+)? Pok[eé]mon) with ((1 of |their )?(your|their) Benched( [\w']+)? Pok[eé]mon|(your|their) Active Pok[eé]mon)"),
    ("on_play_switch_to_active", "consume",
     r"you may switch (it|this Pok[eé]mon) with (your|1 of your) Active Pok[eé]mon"),
    ("free_or_reduced_retreat_self", "produce",
     r"(no Retreat Cost|Retreat Cost.{0,60}? is [A-Za-z]* less|has no Retreat Cost)"),
    ("retreat_cost_increase_opponent", "produce",
     r"(opponent'?s Active|Defending Pok[eé]mon|both Active Pok[eé]mon).*Retreat Cost is [A-Za-z]* more|"
     r"Retreat Cost.{0,50}is [A-Za-z]+ more"),
    ("retreat_prevent_opponent", "produce",
     r"(Defending Pok[eé]mon|Active Pok[eé]mon|their [\w']+ Pok[eé]mon) can'?t retreat"),
    ("attack_lock_opponent", "produce", r"can'?t use attacks|this Pok[eé]mon takes? ?can'?t attack|Pok[eé]mon.*can'?t attack"),
    ("attack_lock_specific_opponent", "produce",
     r"that Pok[eé]mon can'?t use that attack|can'?t use [A-Za-z' ]+ during your opponent'?s next turn"),
    ("self_attack_lock_next_turn", "produce",
     r"during your next turn, this Pok[eé]mon can'?t (use|attack)|this attack can'?t be used|can'?t use [A-Za-z' ]+ again"),
    ("ability_lock", "produce",
     r"Pok[eé]mon.*(has|have) no Abilities|lose any Ability"),
    ("item_lock", "produce", r"opponent can'?t play any Item|they can'?t play any Item"),
    ("supporter_lock", "produce", r"opponent can'?t play any Supporter"),
    ("stadium_lock", "produce", r"opponent can'?t play any Stadium"),
    ("evolve_lock_opponent", "produce",
     r"(opponent|they) can'?t play any Pok[eé]mon from their hand to evolve"),
    ("tool_effect_nullify", "produce",
     r"Pok[eé]mon Tools attached to (each|all) Pok[eé]mon.*have no effect"),
    ("acespec_lock", "produce", r"opponent can'?t play any ACE SPEC cards?"),
    ("stadium_discard_effect", "produce", r"[Dd]iscard (a|that) Stadium"),
    ("tool_discard_opponent", "produce",
     r"discard (a |an |up to \d+ |all )?Pok[eé]mon Tools?( and (a |an )?[\w' ]+)? from (1 of )?your opponent|discard.*Pok[eé]mon Tools? from all of your opponent"),
    ("tool_discard_either_side", "produce",
     r"Pok[eé]mon Tools attached to Pok[eé]mon \(yours or your opponent'?s\) and discard them"),
    ("extra_tool_slot_named_group", "produce", r"may have up to \d+ Pok[eé]mon Tool cards attached"),
    ("attack_copy_opponent", "produce",
     r"use it as this attack|use that attack as this attack"),

    # --- Damage math ---
    ("damage_reduction_self", "consume",
     r"(this Pok[eé]mon|it|the Pok[eé]mon this card is attached to|the [A-Za-z]+ Pok[eé]mon this card is attached to) takes \d+ less damage"),
    ("self_damage_increase_next_turn", "consume", r"this Pok[eé]mon takes \d+ more damage from attacks"),
    ("damage_reduction_team", "consume",
     r"(all of your|[\w']+'s|[A-Z][\w]*) [\w' ]*Pok[eé]mon( \([^)]*\))?.*take \d+ less damage"),
    ("attack_damage_reduced_next_turn_opponent", "consume",
     r"attacks used by (the Defending Pok[eé]mon|your opponent'?s Active Pok[eé]mon).{0,45}do \d+ less damage"),
    ("damage_increase_next_turn_opponent", "consume",
     r"Defending Pok[eé]mon takes \d+ more damage from attacks"),
    ("damage_prevention_conditional", "consume", r"prevent all damage"),
    ("effect_prevention_conditional", "consume", r"prevent all effects"),
    ("ko_prevention", "consume", r"is not Knocked Out, and its remaining HP becomes"),
    ("weakness_modify", "produce",
     r"[Ww]eakness of .*is now|has no Weakness|Weakness is now"),
    ("damage_boost_conditional_generic", "consume",
     r"(does|do) \d+ more damage|damage (does|do) \d+ more"),
    ("damage_scales_with_pokemon_count", "consume",
     r"damage for each of your [\w' ]*Pok[eé]mon in play|damage for each of your [\w' ]+ in play|"
     r"damage for each of your Benched Pok[eé]mon|damage for each Pok[eé]mon in play that has"),
    ("damage_on_opponent_energy_attach", "produce",
     r"(opponent attaches|they attach) an Energy card from their hand.*(put|place) \d+ damage counters"),
    ("damage_on_opponent_evolve", "produce",
     r"opponent plays a Pok[eé]mon from their hand to evolve.*put \d+ damage counters"),
    ("damage_on_opponent_retreat", "produce",
     r"opponent'?s Active Pok[eé]mon moves to the Bench.*place \d+ damage counters"),
    ("damage_scales_with_opponent_pokemon_count", "consume",
     r"damage for each of your opponent'?s (Benched )?Pok[eé]mon"),
    ("damage_scales_with_opponent_hand_size", "consume",
     r"damage for each card in your opponent'?s hand"),
    ("damage_scales_with_own_hand_size", "consume",
     r"damage.*for each card in your hand"),
    ("damage_scales_with_prizes_taken_opponent", "consume",
     r"damage for each Prize card your opponent has taken"),
    ("damage_scales_with_prizes_taken_self", "consume",
     r"damage for each Prize card you (have taken|'ve taken)"),
    ("damage_scales_with_tools_attached", "consume",
     r"damage for each Pok[eé]mon Tool attached"),
    ("damage_scales_with_retreat_cost", "consume",
     r"damage for each Colorless in your opponent'?s Active Pok[eé]mon'?s Retreat Cost|less damage for each Colorless in your opponent'?s Active Pok[eé]mon'?s Retreat Cost"),
    ("damage_ignores_weakness_resistance_or_effects", "consume",
     r"isn'?t affected by (Weakness|Resistance|any effects)"),
    ("attack_cost_reduction_scaling", "consume",
     r"attacks? .*cost [A-Za-z]+ less for each|costs? [A-Za-z]+ less for each"),
    ("attack_cost_reduction_flat", "consume", r"attack costs? \d+ Energy less"),
    ("attack_cost_increase_opponent", "produce",
     r"attacks used by (the Defending Pok[eé]mon|your opponent'?s Active Pok[eé]mon|each [\w' ]*Pok[eé]mon in play)( \([^)]*\))? cost [A-Za-z]+ more"),
    ("attack_cost_reduction_flat_conditional", "consume",
     r"attacks used by (the Pok[eé]mon this card is attached to|your [\w' ]+ Pok[eé]mon) cost [A-Za-z]+ less\b"),
    ("hp_scales_with_count", "consume", r"[+–-]\d+ HP for each"),
    ("hp_modify_flat", "produce", r"gets? [+–-]\d+ HP\b"),

    # --- Evolution & prizes ---
    ("evolve_bonus_effect", "consume", r"When you play this Pok[eé]mon from your hand to evolve"),
    ("evolve_skip_stage", "produce", r"skipping the Stage 1|evolve during your first turn"),
    ("auto_evolve_chain", "produce", r"search their deck for a Stage \d Pok[eé]mon that evolves from"),
    ("devolve_opponent", "produce",
     r"devolve (1 of |each of )?your opponent'?s|devolve it by (putting|shuffling)"),
    ("self_devolve", "produce", r"[Dd]evolve 1 of your evolved"),
    ("prize_bonus_self", "produce", r"take \d+ more Prize cards?"),
    ("prize_reduction_opponent", "produce",
     r"takes? 1 fewer Prize card|can'?t take any Prize cards"),
    ("prize_peek", "produce", r"face-down Prize cards?|Prize cards? face up"),

    # --- Self-sacrifice / misc ---
    ("self_ko_for_effect", "produce", r"you use this Ability, this Pok[eé]mon is Knocked Out"),
    ("avoid_discard_on_ko", "produce", r"put it into your hand instead of the discard pile"),
    ("self_evolve_ability", "produce", r"put it onto this Pok[eé]mon to evolve it"),
    ("type_change_self", "produce", r"is [A-Za-z]+ and [A-Za-z]+ type"),
    ("bench_snipe_opponent", "produce",
     r"damage to (each of )?(1 of |2 of )?your opponent'?s (Pok[eé]mon|Benched Pok[eé]mon)"),
    ("bench_snipe_opponent_all", "produce",
     r"damage to each of your opponent'?s (Benched )?Pok[eé]mon"),
    ("own_bench_splash", "produce",
     r"(?<!opponent's )(?<!opponent’s )damage to (1 of |each of )?your Benched Pok[eé]mon"),
    ("bench_damage_spread", "produce", r"damage to each Benched Pok[eé]mon"),
    ("fossil_pseudo_pokemon", "produce",
     r"[Pp]lay this card as if it were a \d+-HP Basic Colorless Pok[eé]mon"),
    ("bench_size_modify", "produce", r"can have up to \d+ Pok[eé]mon on (their|your) Bench"),
    ("alternate_win_condition", "produce", r"you win this game"),
    ("type_specific_damage_reduction_consumable", "consume",
     r"takes \d+ less damage.*and discard this card"),

    # --- Final round: bespoke/rare mechanics found while pushing for full coverage ---
    ("damage_scales_with_named_attack_in_discard", "consume",
     r"damage for each Pok[eé]mon (in your discard pile|you find there) that has the [\w' ]+ attack"),
    ("attack_access_previous_evolution", "produce",
     r"can use any attack from its previous Evolutions"),
    ("emergency_evolve_low_hp", "produce",
     r"if this Pok[eé]mon'?s remaining HP is \d+ or less, you may search"),
    ("opponent_pokemon_shuffle_into_deck", "produce",
     r"[Ss]huffle (1 of |all of )?your opponent'?s (Benched )?Pok[eé]mon.*into (their|your opponent'?s) deck"),
    ("opponent_pokemon_bounce_lock", "produce",
     r"opponent'?s Pok[eé]mon.*can'?t be put into (your opponent'?s|their) hand"),
    ("first_turn_attack_unlock", "produce", r"can use attacks during your first turn"),
    ("attack_type_substitution_conditional", "consume", r"this attack can be used for [A-Za-z]+"),
    ("conditional_attack_type_unlock", "produce",
     r"can use the [\w'\- ]+ attack for [A-Za-z]+"),
    ("opponent_turn_ends_conditional", "produce", r"their turn ends"),
    ("special_play_condition_only", "produce",
     r"can only be put into play (with|only with) the effect of|"
     r"[Pp]ut this Pok[eé]mon into play only with the effect of"),
    ("discard_pile_pokemon_swap_named", "produce",
     r"switch it with 1 of your Pok[eé]mon ex in play"),
    ("attack_base_damage_boost_next_turn", "consume",
     r"attack'?s base damage is \d+"),
    ("conditional_combo_unlock_by_named_card", "consume",
     r"if you have any cards in their discard pile that have \"[\w' ]+\" in the name|"
     r"has \"[\w' ]+\" in its name in your discard pile"),
    ("named_group_evolve_timing_bonus", "produce",
     r"Grass Pok[eé]mon can evolve into Grass Pok[eé]mon during the turn they play those Pok[eé]mon"),
    ("energy_attach_mutual", "produce",
     r"[Ee]ach player may attach up to \d+ .*Energy cards? from their hand"),
    ("bench_swap_from_discard_basic", "produce",
     r"switch it with 1 of your Basic Pok[eé]mon in play"),
    ("play_face_down_setup", "produce", r"put it face down in the Active Spot"),
    ("attack_unlock_by_prior_attack", "consume",
     r"you can use this attack only if this Pok[eé]mon used [\w' ]+ during your last turn"),
    ("discard_energy_on_hit_ability", "consume",
     r"damaged by an attack from your opponent'?s Pok[eé]mon \(even if this Pok[eé]mon is Knocked Out\), discard an Energy"),
    ("tool_swap_condition", "produce", r"Attach a Pok[eé]mon Tool to 1 of your Pok[eé]mon that doesn'?t already have"),
    ("coin_flip_reroll", "consume", r"ignore all results of those coin flips and begin flipping"),
    ("recur_multiple_named_cards_paired", "produce",
     r"you must play \d+ [\w' :]+ cards? at once"),
    ("stack_bench_swap_basic_from_discard", "produce",
     r"Choose a Basic Pok[eé]mon in your discard pile and switch it with 1 of your Basic Pok[eé]mon in play"),
    ("damage_on_bench_placement", "produce",
     r"puts? a Basic( [\w'-]+)? Pok[eé]mon onto (their|your) Bench.{0,20}place \d+ damage counters"),
    ("status_persist_through_evolve", "produce",
     r"don'?t recover from that Special Condition when they evolve or devolve"),
    ("damage_counter_doubler", "produce", r"(double|quadruple) the number of damage counters"),
    ("energy_salvage_on_ko", "produce",
     r"Knocked Out by damage from an attack from your opponent'?s Pok[eé]mon,?.*(move|put) .*Energy.*(to (1 of )?your Benched|into your hand instead of the discard pile)"),
    ("damage_scales_with_revealed_subtype", "consume", r"damage for each [A-Za-z]+ card you find there"),
    ("damage_scales_with_revealed_count", "consume", r"damage for each card you revealed in this way"),
    ("grants_attack_via_tool", "produce", r"can use the attack on this card"),
    ("hand_deck_top_swap", "produce", r"[Ss]witch a card from your hand with the top card of your deck"),
    ("ability_pokemon_play_lock", "produce",
     r"opponent can'?t play any Pok[eé]mon that has an Ability from their hand"),
    ("pokemon_shuffle_from_discard_into_deck", "produce",
     r"[Ss]huffle up to \d+ Pok[eé]mon from your discard pile into your deck"),
    ("deck_peek_bottom", "produce", r"look at the bottom \d+ cards? of your deck"),
    ("hand_count_shuffle_redraw_opponent", "produce",
     r"opponent counts the cards in their hand, shuffles those cards"),
    ("stage2_conditional_bench_play", "produce",
     r"if this Pok[eé]mon is in your hand and your opponent has any Stage 2 Pok[eé]mon in play"),
    ("attack_unlock_by_own_hp", "produce", r"remaining HP is \d+ or less, you may search"),
    ("prize_reshuffle", "produce",
     r"[Cc]ount your Prize cards, shuffle them, and put them on the bottom of your deck"),
    ("retreat_cost_gated_energy_move", "produce",
     r"has a Retreat Cost of exactly \d+.*move up to \d+ Basic Energy cards"),
    ("first_turn_go_second_energy_bounce", "produce",
     r"only if you go second, and only during your first turn.{0,20}Energy attached"),
    ("energy_up_to_amount_attached_opponent", "produce",
     r"[Cc]hoose [\w' ]*Energy cards from your discard pile up to the amount of Energy attached to all of your opponent"),
    ("damage_boost_if_damaged_last_turn", "consume",
     r"if this Pok[eé]mon was damaged by an attack during your opponent'?s last turn"),
    ("damage_scales_with_card_type_in_discard", "consume",
     r"damage for each (Item|Supporter|Stadium|Trainer) card in your opponent'?s discard pile"),
    ("self_reset_via_bottom_discard", "produce",
     r"discard the bottom card of your deck.*put this Pok[eé]mon on top of your deck"),
    ("heal_and_cure_from", "produce",
     r"[Hh]eal \d+ damage and remove a Special Condition from"),
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
