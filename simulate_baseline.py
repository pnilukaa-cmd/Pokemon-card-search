#!/usr/bin/env python3
"""Generic single-deck development-timing simulator.

Reads ANY decklist in this project's plain-text PTCGL format and builds its
Pokemon model from pokemon_standard_cards.json via tcg_model -- stage,
evolvesFrom, HP, retreat, types, attacks, and Abilities all come from the
real card data, matched by exact SET NUM where the decklist provides it.

For head-to-head testing against a real opponent deck (knockouts, Prize
cards, an actual win rate) use simulate_versus.py instead. This tool
answers the narrower question: how fast does one deck assemble, and how
big does its hand get.

What is modeled
  * Board development: playing Basics, evolving (respecting "not the turn
    it entered play"), Rare Candy, and Grand Tree.
  * DRAW ABILITIES -- Toucannon, Dudunsparce, Kadabra/Alakazam,
    N's Zoroark ex, Mega Kangaskhan ex, Fezandipiti ex and the rest of the
    family, including on-evolve triggers, draw-to-N, Active-only and
    after-a-KO conditions, and hand-discard costs. Before this existed the
    simulator read no Abilities at all, which badly understated any
    Ability-driven deck's hand size -- and therefore any attacker that
    scales off hand size.
  * A registry of common Trainer effects. Anything outside it is simply
    never played, and every such name is listed in the report so a gap is
    visible rather than silent.

Stated simplifications
  * No opponent and no retreating. Only whatever ends up Active -- or what
    it evolves into -- ever attacks.
  * Energy is counted, not type-checked (that is check_energy_support.py's
    job), so an Ability whose cost is "discard a Basic <Type> Energy from
    this Pokemon" is skipped rather than guessed at.
  * Pokemon Tools are never attached; Stadiums other than Grand Tree do
    nothing.

Usage:
  python3 simulate_baseline.py decklist.txt          # 1000-trial baseline
  python3 simulate_baseline.py decklist.txt 500      # custom trial count
  python3 simulate_baseline.py decklist.txt --verbose # + one full sample log
"""
import random
import re
import sys
import statistics
from collections import defaultdict

sys.path.insert(0, ".")
from check_energy_support import load_cards, BASIC_ENERGY_RE, SYMBOL_TO_TYPE

# Card model, decklist parsing, and Ability parsing all live in tcg_model
# so this simulator and simulate_versus.py build Pokemon from exactly the
# same code against the same data.
import tcg_model as M
import ability_ir as IR

BASIC_ENERGY_RE = M.BASIC_ENERGY_RE
build_deck_model = M.build_deck_model
build_card_index = M.build_card_index


# ---------------------------------------------------------------------------
# Game engine (deck-agnostic)
# ---------------------------------------------------------------------------

class GameState:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.active = None
        self.active_energy = 0
        self.active_entered_turn = 0
        self.active_evolved_this_turn = False
        self.bench = []  # list of dicts: {"name", "energy", "entered_turn"}
        self.discard = []
        self.supporter_played = False
        self.online_turn = {}       # Pokemon name -> first turn it entered play
        self.first_attack_turn = None
        self.stadium_in_play = None
        self.abilities_used = set()   # (slot_key, ability name) used this turn
        self.lost_pokemon_last_turn = False
        self.played_supporters_this_turn = set()

    def draw(self, n=1):
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def has_basic_in_hand(self, POKEMON):
        return any(k == "Pokemon" and POKEMON[n]["stage"] == "Basic" for k, n in self.hand)

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

    def in_play_names(self):
        names = [s["name"] for s in self.bench]
        if self.active:
            names.append(self.active)
        return names

    def hand_names(self):
        return [n for k, n in self.hand if k == "Pokemon"]

    def note_online(self, name, turn):
        if name not in self.online_turn:
            self.online_turn[name] = turn


def opening_hand(deck, POKEMON):
    while True:
        random.shuffle(deck)
        state = GameState(deck)
        state.draw(7)
        if state.has_basic_in_hand(POKEMON):
            return state
        deck.extend(state.hand)
        state.hand = []


def play_basics(state, POKEMON, turn, log):
    if state.active is None:
        basics_in_hand = [n for k, n in state.hand if k == "Pokemon" and POKEMON[n]["stage"] == "Basic"]
        if basics_in_hand:
            name = basics_in_hand[0]
            state.remove_from_hand("Pokemon", name)
            state.active = name
            state.active_energy = 0
            state.active_entered_turn = turn
            state.note_online(name, turn)
            log.append(f"Play {name} as Active")
    for kind, name in list(state.hand):
        if kind == "Pokemon" and POKEMON[name]["stage"] == "Basic" and len(state.bench) < 5:
            state.remove_from_hand(kind, name)
            state.bench.append({"name": name, "energy": 0, "entered_turn": turn, "evolved_this_turn": False})
            state.note_online(name, turn)
            log.append(f"Bench {name}")


def try_evolve(state, POKEMON, turn, log):
    for kind, name in list(state.hand):
        if kind != "Pokemon":
            continue
        target = POKEMON[name]["evolves_from"]
        if target is None:
            continue
        if (state.active == target and turn > state.active_entered_turn
                and not state.active_evolved_this_turn):
            state.remove_from_hand(kind, name)
            state.active = name
            state.active_evolved_this_turn = True
            state.note_online(name, turn)
            log.append(f"Evolve {target} -> {name} (Active, can't attack this turn)")
            use_draw_abilities(state, POKEMON, log, evolved_name=name)
            continue
        slot = next((s for s in state.bench
                     if s["name"] == target and turn > s["entered_turn"]
                     and not s.get("evolved_this_turn")), None)
        if slot is not None:
            state.remove_from_hand(kind, name)
            slot["name"] = name
            slot["evolved_this_turn"] = True
            state.note_online(name, turn)
            log.append(f"Evolve {target} -> {name} (Bench)")
            use_draw_abilities(state, POKEMON, log, evolved_name=name)


def rare_candy_targets(state, POKEMON, turn):
    if turn <= 1:
        return []
    stage2_in_hand = [n for k, n in state.hand if k == "Pokemon" and POKEMON.get(n, {}).get("stage") == "Stage 2"]
    candidates = []
    if state.active and turn > state.active_entered_turn and POKEMON.get(state.active, {}).get("stage") == "Basic":
        candidates.append(("active", state.active))
    for slot in state.bench:
        if turn > slot["entered_turn"] and POKEMON.get(slot["name"], {}).get("stage") == "Basic":
            candidates.append((slot, slot["name"]))
    results = []
    for loc, basic_name in candidates:
        for s2name in stage2_in_hand:
            s1name = POKEMON.get(s2name, {}).get("evolves_from")
            s1info = POKEMON.get(s1name) if s1name else None
            if s1info and s1info.get("evolves_from") == basic_name:
                results.append((loc, basic_name, s2name))
    return results


def effect_rare_candy(state, POKEMON, turn, log):
    targets = rare_candy_targets(state, POKEMON, turn)
    if not targets:
        return False
    loc, basic_name, s2name = targets[0]
    state.remove_from_hand("Item", "Rare Candy")
    state.discard.append("Rare Candy")
    state.remove_from_hand("Pokemon", s2name)
    if loc == "active":
        state.active = s2name
        state.active_evolved_this_turn = True
    else:
        loc["name"] = s2name
    state.note_online(s2name, turn)
    log.append(f"Play Rare Candy -> {basic_name} skips Stage 1, becomes {s2name}")
    return True


def play_stadium(state, log):
    for kind, name in list(state.hand):
        if kind == "Stadium":
            state.remove_from_hand(kind, name)
            if state.stadium_in_play:
                state.discard.append(state.stadium_in_play)
            state.stadium_in_play = name
            log.append(f"Play Stadium: {name}")
            return


def grand_tree_targets(state, POKEMON, turn):
    if turn <= 1:
        return []
    candidates = []
    if state.active and turn > state.active_entered_turn:
        candidates.append(("active", state.active))
    for slot in state.bench:
        if turn > slot["entered_turn"]:
            candidates.append((slot, slot["name"]))
    results = []
    for loc, name in candidates:
        info = POKEMON.get(name)
        if not info or info["stage"] != "Basic":
            continue
        for s1name, s1info in POKEMON.items():
            if s1info.get("evolves_from") == name and s1info["stage"] == "Stage 1":
                if any(c == ("Pokemon", s1name) for c in state.deck):
                    results.append((loc, name, s1name))
    return results


def effect_grand_tree(state, POKEMON, turn, log):
    """Grand Tree (ACE SPEC Stadium): once per player's turn, evolve a
    Basic already in play straight from the deck (Basic -> Stage 1, then
    chaining to Stage 2 if that's also in the deck) -- no need to have
    drawn the evolution card at all. Real card text also lets the
    opponent use it on their turn, not modeled here since this simulator
    has no opponent."""
    if state.stadium_in_play != "Grand Tree":
        return False
    targets = grand_tree_targets(state, POKEMON, turn)
    if not targets:
        return False
    loc, basic_name, s1name = targets[0]
    state.deck.remove(("Pokemon", s1name))
    if loc == "active":
        state.active = s1name
        state.active_evolved_this_turn = True
    else:
        loc["name"] = s1name
    state.note_online(s1name, turn)
    log.append(f"Grand Tree -> {basic_name} evolves into {s1name} (searched from deck)")
    for s2name, s2info in POKEMON.items():
        if s2info.get("evolves_from") == s1name and s2info["stage"] == "Stage 2":
            if any(c == ("Pokemon", s2name) for c in state.deck):
                state.deck.remove(("Pokemon", s2name))
                if loc == "active":
                    state.active = s2name
                else:
                    loc["name"] = s2name
                state.note_online(s2name, turn)
                log.append(f"Grand Tree chains -> {s1name} evolves into {s2name}")
            break
    random.shuffle(state.deck)
    return True


def energy_need(POKEMON, name, energy_attached):
    attacks = POKEMON.get(name, {}).get("attacks") or []
    if not attacks:
        return 0
    needed = len(attacks[0]["cost"])
    return max(0, needed - energy_attached)


PRE_EVOLUTION_CACHE = {}


def pre_evolution_names(POKEMON):
    return {info["evolves_from"] for info in POKEMON.values() if info["evolves_from"]}


def attach_energy(state, POKEMON, pre_evolutions, log):
    energy_card = next((c for c in state.hand if c[0] == "Energy"), None)
    if energy_card is None:
        return
    target = None
    if state.active and energy_need(POKEMON, state.active, state.active_energy) > 0:
        target = "active"
    else:
        for slot in state.bench:
            if slot["name"] in pre_evolutions:
                target = slot
                break
        if target is None:
            for slot in state.bench:
                if energy_need(POKEMON, slot["name"], slot["energy"]) > 0:
                    target = slot
                    break
    if target is None:
        log.append(f"Hold {energy_card[1]} (no useful attachment target)")
        return
    state.remove_from_hand(*energy_card)
    if target == "active":
        state.active_energy += 1
        log.append(f"Attach {energy_card[1]} to {state.active} (Active, now {state.active_energy})")
    else:
        target["energy"] += 1
        log.append(f"Attach {energy_card[1]} to {target['name']} (Bench, now {target['energy']})")
    if energy_card[1] == "Enriching Energy":
        state.draw(4)
        log.append("Enriching Energy attached from hand -> draw 4")


def try_attack(state, POKEMON, turn, log):
    if not state.active or state.active_evolved_this_turn:
        return
    attacks = POKEMON.get(state.active, {}).get("attacks") or []
    if not attacks:
        return
    atk = attacks[0]
    name, cost, dmg = atk["name"], atk["cost"], atk["damage"]
    needed = len(cost) - _cost_discount(state, POKEMON, state.active)
    needed = max(0, needed)
    if state.active_energy >= needed:
        if state.first_attack_turn is None:
            state.first_attack_turn = turn
        log.append(f"Attack: {state.active} uses {name} for {dmg} "
                   f"({state.active_energy} energy, needed {needed})")


_ABILITY_CACHE = {}


def _compiled_abilities(name):
    """Compiled Abilities for a Pokemon name, cached. Matched by name, so
    a printing-specific Ability can be missed -- fine here, since this is
    only used for cost discounts."""
    if name not in _ABILITY_CACHE:
        cards = M.load_cards()
        by_name, _ = M.build_card_index(cards)
        hits = by_name.get(name) or []
        _ABILITY_CACHE[name] = (IR.compile_card_abilities(hits[0])
                                if hits else [])
    return _ABILITY_CACHE[name]


def _cost_discount(state, POKEMON, name):
    """Energy knocked off this Pokemon's attacks by a scaling Ability.

    Crabominable's and Veluza's Food Prep reads "cost Colorless less for
    each Kofu card in your discard pile" -- without this the baseline
    priced Haymaker at its printed five Energy in a deck that runs six,
    and reported a 28% first-attack rate for a deck whose whole point is
    that the attack becomes nearly free.
    """
    total = 0
    for eff in _compiled_abilities(name):
        if eff.unsupported:
            continue
        for act in eff.actions:
            if act.op != IR.Op.MODIFY_ATTACK_COST:
                continue
            named = act.filter.get("per_named_card_in_discard")
            if named:
                total += sum(1 for c in state.discard if c == named)
    return total


def _slots(state):
    """(key, name) for every Pokemon in play. The Active is keyed 'active';
    Bench slots are keyed by identity so two copies of the same Pokemon each
    get their own once-per-turn Ability use."""
    out = []
    if state.active:
        out.append(("active", state.active))
    for slot in state.bench:
        out.append((id(slot), slot["name"]))
    return out


def use_draw_abilities(state, POKEMON, log, evolved_name=None):
    """Fire every legal draw Ability once per turn.

    Abilities are the draw engine for a large share of real decks (Toucannon,
    Dudunsparce, Kadabra/Alakazam, N's Zoroark ex, Mega Kangaskhan ex ...).
    Before this existed the simulator read none of them, which made any
    Ability-driven deck's hand size -- and therefore any hand-size-scaling
    attacker -- read far lower than it really is."""
    for key, name in _slots(state):
        for ab in POKEMON.get(name, {}).get("abilities", []):
            if ab["kind"] != "draw":
                continue
            if ab["trigger"] == "on_evolve" and name != evolved_name:
                continue
            if ab["trigger"] != "on_evolve" and evolved_name is not None:
                continue
            ukey = (key, ab["name"])
            if ukey in state.abilities_used:
                continue
            if ab.get("requires_active") and key != "active":
                continue
            if ab.get("requires_ko_last_turn") and not state.lost_pokemon_last_turn:
                continue
            need = ab.get("requires_in_play")
            if need and need not in state.in_play_names():
                continue
            need_played = ab.get("requires_played_this_turn")
            if need_played and need_played not in state.played_supporters_this_turn:
                continue

            cost_hand = ab.get("cost_discard_hand") or 0
            if cost_hand and len(state.hand) < cost_hand:
                continue
            etype = ab.get("cost_discard_energy_hand")
            eidx = None
            if etype:
                eidx = next((i for i, (k, n) in enumerate(state.hand)
                             if k == "Energy" and n.startswith(etype)), None)
                if eidx is None:
                    continue
            if ab.get("cost_discard_energy_self"):
                # Needs a specific Energy attached to this Pokemon; the
                # baseline sim tracks Energy as a bare count, not by type,
                # so this cost cannot be checked honestly here.
                continue

            target = ab.get("draw_to")
            if target is not None and len(state.hand) >= target:
                continue

            if eidx is not None:
                k, n = state.hand.pop(eidx)
                state.discard.append(n)
            for _ in range(cost_hand):
                if state.hand:
                    k, n = state.hand.pop(0)
                    state.discard.append(n)

            before = len(state.hand)
            if target is not None:
                while len(state.hand) < target and state.deck:
                    state.draw(1)
            else:
                state.draw(ab.get("amount") or 0)
            drew = len(state.hand) - before
            state.abilities_used.add(ukey)
            log.append(f"Ability: {name} uses {ab['name']} -> drew {drew}")

            if ab.get("cost_shuffle_self") and drew > 0:
                state.deck.append(("Pokemon", name))
                if key == "active":
                    state.active = state.bench.pop(0)["name"] if state.bench else None
                else:
                    state.bench = [sl for sl in state.bench if id(sl) != key]
                random.shuffle(state.deck)
                log.append(f"  {name} shuffles itself back into the deck")
                return


# --- Trainer/Item/Supporter effect registry -------------------------------

def discard_value(state, card):
    kind, name = card
    if kind == "Energy":
        energy_in_hand = sum(1 for k, n in state.hand if k == "Energy")
        return 0 if energy_in_hand > 2 else 2
    if kind == "Pokemon":
        count_in_hand = sum(1 for k, n in state.hand if k == "Pokemon" and n == name)
        return 1 if (name in state.in_play_names() or count_in_hand > 1) else 3
    if kind == "Item":
        return 2
    return 4


def stage_rank(POKEMON, name):
    return {"Basic": 0, "Stage 1": 1, "Stage 2": 2}.get(POKEMON[name]["stage"], 1)


def search_priority(POKEMON):
    return sorted(POKEMON.keys(), key=lambda n: (stage_rank(POKEMON, n), POKEMON[n]["rule_box"]))


def choose_search_target(state, POKEMON, priority, allow_rule_box):
    in_play = set(state.in_play_names())
    in_hand = set(state.hand_names())
    in_deck = {n for k, n in state.deck if k == "Pokemon"}
    for name in priority:
        if not allow_rule_box and POKEMON[name]["rule_box"]:
            continue
        if name in in_play or name in in_hand or name not in in_deck:
            continue
        pre = POKEMON[name]["evolves_from"]
        if pre is not None and pre not in in_play:
            continue
        return name
    return None


def buddy_poffin_eligible(POKEMON):
    return [n for n, info in POKEMON.items() if info["stage"] == "Basic" and info["hp"] <= 70]


# Cards shaped like "search up to N Basic <Family> Pokemon and put them onto
# your Bench" (Hop's Bag, and the same pattern used by other named-family
# Trainers in this format) -- keyed by exact card name -> the substring its
# own text restricts to and how many it fetches. An empty substring matches
# every Basic, which covers unrestricted versions like Precious Trolley
# ("search for any number of Basic Pokemon") -- 99 stands in for "any
# number," since the bench-space check already caps the real limit.
FAMILY_BENCH_SEARCH_ITEMS = {
    "Hop's Bag": ("Hop's", 2),
    "Precious Trolley": ("", 99),
}


def family_bench_eligible(POKEMON, family_substring):
    return [n for n, info in POKEMON.items() if info["stage"] == "Basic" and family_substring in n]


def play_items(state, POKEMON, priority, turn, log):
    for item_name, (family, max_count) in FAMILY_BENCH_SEARCH_ITEMS.items():
        eligible = family_bench_eligible(POKEMON, family)
        while ("Item", item_name) in state.hand and len(state.bench) < 5:
            found, remaining = [], []
            for card in state.deck:
                if len(found) < max_count and card[0] == "Pokemon" and card[1] in eligible:
                    found.append(card[1])
                else:
                    remaining.append(card)
            if not found:
                break
            state.remove_from_hand("Item", item_name)
            state.discard.append(item_name)
            state.deck = remaining
            random.shuffle(state.deck)
            for name in found[: max(0, 5 - len(state.bench))]:
                state.bench.append({"name": name, "energy": 0, "entered_turn": turn, "evolved_this_turn": False})
                state.note_online(name, turn)
            log.append(f"Play {item_name} -> bench {', '.join(found)}")

    while ("Item", "Rare Candy") in state.hand:
        if not effect_rare_candy(state, POKEMON, turn, log):
            break

    eligible_basics = buddy_poffin_eligible(POKEMON)
    while ("Item", "Buddy-Buddy Poffin") in state.hand and len(state.bench) < 5:
        found, remaining = [], []
        for card in state.deck:
            if len(found) < 2 and card[0] == "Pokemon" and card[1] in eligible_basics:
                found.append(card[1])
            else:
                remaining.append(card)
        if not found:
            break
        state.remove_from_hand("Item", "Buddy-Buddy Poffin")
        state.discard.append("Buddy-Buddy Poffin")
        state.deck = remaining
        random.shuffle(state.deck)
        for name in found[: max(0, 5 - len(state.bench))]:
            state.bench.append({"name": name, "energy": 0, "entered_turn": turn, "evolved_this_turn": False})
            state.note_online(name, turn)
        log.append(f"Play Buddy-Buddy Poffin -> bench {', '.join(found)}")

    # Brilliant Blender: search up to 5 cards out of the deck and discard
    # them -- here, the Kofu that Food Prep counts.
    while ("Item", "Brilliant Blender") in state.hand:
        wanted = [c for c in state.deck if c[1] == "Kofu"][:5]
        if not wanted:
            break
        state.remove_from_hand("Item", "Brilliant Blender")
        state.discard.append("Brilliant Blender")
        for card in wanted:
            state.deck.remove(card)
            state.discard.append(card[1])
        random.shuffle(state.deck)
        log.append(f"Play Brilliant Blender -> discard {len(wanted)} Kofu")

    while ("Item", "Ultra Ball") in state.hand:
        target = choose_search_target(state, POKEMON, priority, allow_rule_box=True)
        if target is None:
            break
        eligible = [c for c in state.hand if c != ("Item", "Ultra Ball")]
        if len(eligible) < 2:
            break
        discard_candidates = sorted(eligible, key=lambda c: discard_value(state, c))[:2]
        for c in discard_candidates:
            state.remove_from_hand(*c)
            state.discard.append(c[1])
        state.remove_from_hand("Item", "Ultra Ball")
        state.discard.append("Ultra Ball")
        state.deck.remove(("Pokemon", target))
        random.shuffle(state.deck)
        state.hand.append(("Pokemon", target))
        log.append(f"Play Ultra Ball -> search {target}")

    while ("Item", "Poké Pad") in state.hand:
        target = choose_search_target(state, POKEMON, priority, allow_rule_box=False)
        if target is None:
            break
        state.remove_from_hand("Item", "Poké Pad")
        state.discard.append("Poké Pad")
        state.deck.remove(("Pokemon", target))
        random.shuffle(state.deck)
        state.hand.append(("Pokemon", target))
        log.append(f"Play Poké Pad -> search {target}")

    # Pokegear 3.0: look at the top 7 cards of the deck and take a
    # Supporter from among them. Like Team Rocket's Transceiver above, it
    # only takes a Supporter the registry can actually resolve, so the
    # measured value stays honest rather than counting a fetch that would
    # then sit inert in hand.
    while ("Item", "Pokégear 3.0") in state.hand:
        top7 = state.deck[-7:]
        pick = next((c for c in reversed(top7)
                     if c[0] == "Supporter" and c[1] in SUPPORTER_EFFECTS), None)
        if pick is None:
            break
        state.remove_from_hand("Item", "Pokégear 3.0")
        state.discard.append("Pokégear 3.0")
        state.deck.remove(pick)
        random.shuffle(state.deck)
        state.hand.append(pick)
        log.append(f"Play Pokégear 3.0 -> reveal {pick[1]}")

    while ("Item", "Night Stretcher") in state.hand:
        pkmn_in_discard = next((n for n in state.discard if n in POKEMON), None)
        basic_energy_in_discard = next((n for n in state.discard if BASIC_ENERGY_RE.match(n)), None)
        pick = pkmn_in_discard or basic_energy_in_discard
        if pick is None:
            break
        state.remove_from_hand("Item", "Night Stretcher")
        state.discard.append("Night Stretcher")
        state.discard.remove(pick)
        kind = "Pokemon" if pick in POKEMON else "Energy"
        state.hand.append((kind, pick))
        log.append(f"Play Night Stretcher -> retrieve {pick} from discard")

    if ("Item", "Energy Search") in state.hand:
        basic_e = next((c for c in state.deck if c[0] == "Energy" and BASIC_ENERGY_RE.match(c[1])), None)
        if basic_e:
            state.remove_from_hand("Item", "Energy Search")
            state.discard.append("Energy Search")
            state.deck.remove(basic_e)
            random.shuffle(state.deck)
            state.hand.append(basic_e)
            log.append(f"Play Energy Search -> get {basic_e[1]}")

    # Team Rocket's Transceiver: search the deck for a Supporter whose name
    # contains "Team Rocket" and put it into hand. Only fetches Supporters
    # the registry can actually play, so the simulated value stays honest.
    while ("Item", "Team Rocket's Transceiver") in state.hand:
        fetch = next((c for c in state.deck
                      if c[0] == "Supporter" and "Team Rocket" in c[1]
                      and c[1] in SUPPORTER_EFFECTS), None)
        if fetch is None:
            break
        state.remove_from_hand("Item", "Team Rocket's Transceiver")
        state.discard.append("Team Rocket's Transceiver")
        state.deck.remove(fetch)
        random.shuffle(state.deck)
        state.hand.append(fetch)
        log.append(f"Play Team Rocket's Transceiver -> search {fetch[1]}")


def effect_lillies_determination(state, POKEMON, log):
    if len(state.hand) >= 5:
        return False
    state.remove_from_hand("Supporter", "Lillie's Determination")
    state.discard.append("Lillie's Determination")
    state.draw(6)
    log.append("Play Lillie's Determination (shuffle hand, draw 6)")
    return True


def effect_kofu(state, POKEMON, log):
    """Kofu: bottom 2 cards of your hand, draw 4. In a Food Prep deck each
    copy played is also one Colorless off Haymaker and Sonic Edge, so it
    is worth the Supporter slot even from a comfortable hand."""
    rest = [c for c in state.hand if c != ("Supporter", "Kofu")]
    if len(rest) < 2:
        return False
    state.remove_from_hand("Supporter", "Kofu")
    state.discard.append("Kofu")
    for _ in range(2):
        state.deck.insert(0, state.hand.pop(0))
    state.draw(4)
    log.append("Play Kofu (bottom 2, draw 4)")
    return True


def effect_janines_secret_art(state, POKEMON, log):
    targets = [n for n in state.in_play_names() if "Darkness" in POKEMON.get(n, {}).get("types", [])][:2]
    if not targets:
        return False
    if not any(c[0] == "Energy" and c[1] == "Darkness Energy" for c in state.deck):
        return False
    state.remove_from_hand("Supporter", "Janine's Secret Art")
    state.discard.append("Janine's Secret Art")
    attached = []
    for t in targets:
        e = next((c for c in state.deck if c == ("Energy", "Darkness Energy")), None)
        if e is None:
            break
        state.deck.remove(e)
        if t == state.active:
            state.active_energy += 1
        else:
            for slot in state.bench:
                if slot["name"] == t:
                    slot["energy"] += 1
        attached.append(t)
    random.shuffle(state.deck)
    log.append(f"Play Janine's Secret Art -> search+attach Darkness Energy to {', '.join(attached)}"
               f" (Special Condition on Active not modeled)")
    return True


def effect_petrel(state, POKEMON, log):
    trainer_cards = [c for c in state.deck if c[0] in ("Item", "Supporter", "Tool", "Stadium")]
    if not trainer_cards:
        return False
    want_energy = not any(k == "Energy" for k, _ in state.hand)
    preferred = ["Energy Search"] if want_energy else ["Ultra Ball", "Poké Pad", "Buddy-Buddy Poffin", "Rare Candy"]
    fetch = None
    for want_name in preferred:
        cand = next((c for c in trainer_cards if c[1] == want_name), None)
        if cand:
            fetch = cand
            break
    if fetch is None:
        fetch = trainer_cards[0]
    state.remove_from_hand("Supporter", "Team Rocket's Petrel")
    state.discard.append("Team Rocket's Petrel")
    state.deck.remove(fetch)
    random.shuffle(state.deck)
    state.hand.append(fetch)
    log.append(f"Play Team Rocket's Petrel -> search {fetch[1]}")
    return True


def effect_proton(state, POKEMON, log):
    """Team Rocket's Proton: search up to 3 Basic Team Rocket's Pokemon
    and put them into your hand. (The real card is also legal on your own
    first turn going first, unlike most Supporters -- that exception
    isn't modeled here because this simulator lets any Supporter be played
    from turn 1 anyway, so modeling it would overstate nothing.)"""
    found = []
    remaining = []
    for card in state.deck:
        if (len(found) < 3 and card[0] == "Pokemon"
                and POKEMON.get(card[1], {}).get("stage") == "Basic"
                and card[1].startswith("Team Rocket's")):
            found.append(card)
        else:
            remaining.append(card)
    if not found:
        return False
    state.remove_from_hand("Supporter", "Team Rocket's Proton")
    state.discard.append("Team Rocket's Proton")
    state.deck = remaining
    random.shuffle(state.deck)
    state.hand.extend(found)
    log.append(f"Play Team Rocket's Proton -> search {', '.join(c[1] for c in found)}")
    return True


def effect_ariana(state, POKEMON, log):
    """Team Rocket's Ariana: draw until you have 5 cards in hand -- or 8
    instead if EVERY Pokemon you have in play is a Team Rocket's Pokemon.
    The all-Team-Rocket's check is the real deckbuilding constraint here:
    a single non-Team-Rocket's Pokemon on the board silently downgrades
    this to the 5-card mode."""
    in_play = state.in_play_names()
    all_tr = bool(in_play) and all(n.startswith("Team Rocket's") for n in in_play)
    target = 8 if all_tr else 5
    if len(state.hand) >= target:
        return False
    state.remove_from_hand("Supporter", "Team Rocket's Ariana")
    state.discard.append("Team Rocket's Ariana")
    drew = 0
    while len(state.hand) < target and state.deck:
        state.draw(1)
        drew += 1
    mode = "all Team Rocket's in play" if all_tr else "mixed board"
    log.append(f"Play Team Rocket's Ariana -> draw to {target} ({mode}), drew {drew}")
    return True


def _search_pokemon_to_hand(state, POKEMON, pred):
    for i, (k, n) in enumerate(state.deck):
        if k == "Pokemon" and pred(n):
            state.deck.pop(i)
            random.shuffle(state.deck)
            state.hand.append(("Pokemon", n))
            return n
    return None


def effect_dawn(state, POKEMON, log):
    """Dawn: search for a Basic, a Stage 1, and a Stage 2 -- three cards
    straight into hand."""
    got = []
    for stage in ("Basic", "Stage 1", "Stage 2"):
        n = _search_pokemon_to_hand(state, POKEMON,
                                    lambda x, st=stage: POKEMON[x]["stage"] == st)
        if n:
            got.append(n)
    if not got:
        return False
    state.remove_from_hand("Supporter", "Dawn")
    state.discard.append("Dawn")
    log.append(f"Play Dawn -> search {', '.join(got)}")
    return True


def effect_hilda(state, POKEMON, log):
    """Hilda: search an Evolution Pokemon and an Energy card into hand."""
    got = []
    n = _search_pokemon_to_hand(state, POKEMON, lambda x: POKEMON[x]["stage"] != "Basic")
    if n:
        got.append(n)
    i = next((i for i, (k, _) in enumerate(state.deck) if k == "Energy"), None)
    if i is not None:
        card = state.deck.pop(i)
        random.shuffle(state.deck)
        state.hand.append(card)
        got.append(card[1])
    if not got:
        return False
    state.remove_from_hand("Supporter", "Hilda")
    state.discard.append("Hilda")
    log.append(f"Play Hilda -> search {', '.join(got)}")
    return True


def effect_judge(state, POKEMON, log):
    """Judge: each player shuffles their hand into their deck and draws 4.

    Only the player's own half is modeled -- there is no opponent board
    here, so the half that actually matters to a Decidueye ex deck
    (setting the OPPONENT to exactly 4 cards, which is what switches
    Sniper's Eye on) cannot be scored by this simulator at all. Read a
    Judge deck's numbers here as development speed only, never as a
    measure of how often the combo is live.
    """
    rest = [c for c in state.hand if c != ("Supporter", "Judge")]
    if len(rest) >= 4:
        return False
    state.remove_from_hand("Supporter", "Judge")
    state.discard.append("Judge")
    state.deck.extend(rest)
    state.hand = []
    random.shuffle(state.deck)
    state.draw(4)
    log.append(f"Play Judge (shuffle {len(rest)} back, draw 4; opponent side not modeled)")
    return True


def effect_carmine(state, POKEMON, log):
    """Carmine: discard your hand and draw 5."""
    rest = [c for c in state.hand if c != ("Supporter", "Carmine")]
    if len(rest) >= 5:
        return False
    state.remove_from_hand("Supporter", "Carmine")
    state.discard.append("Carmine")
    for kind, name in rest:
        state.discard.append(name)
    state.hand = []
    state.draw(5)
    log.append(f"Play Carmine (discard {len(rest)}, draw 5)")
    return True


SUPPORTER_PRIORITY = ["Team Rocket's Proton", "Team Rocket's Ariana", "Kofu", "Dawn", "Hilda",
                      "Lillie's Determination", "Carmine", "Judge",
                      "Janine's Secret Art", "Team Rocket's Petrel"]
SUPPORTER_EFFECTS = {
    "Lillie's Determination": effect_lillies_determination,
    "Kofu": effect_kofu,
    "Janine's Secret Art": effect_janines_secret_art,
    "Team Rocket's Petrel": effect_petrel,
    "Team Rocket's Proton": effect_proton,
    "Team Rocket's Ariana": effect_ariana,
    "Dawn": effect_dawn,
    "Hilda": effect_hilda,
    "Judge": effect_judge,
    "Carmine": effect_carmine,
}
# Real cards whose whole effect targets the opponent's side (or a
# Prize-count condition we don't track) -- correctly left unplayed rather
# than misrepresented as "unmodeled gap," since they have zero effect on
# any metric this simulator reports.
NO_SELF_EFFECT_SUPPORTERS = {"Boss's Orders", "Xerosic's Machinations", "Rosa's Encouragement",
                             "Team Rocket's Giovanni", "Black Belt's Training"}


def play_supporter(state, POKEMON, log):
    if state.supporter_played:
        return
    for name in SUPPORTER_PRIORITY:
        if ("Supporter", name) in state.hand:
            handler = SUPPORTER_EFFECTS[name]
            if handler(state, POKEMON, log):
                state.supporter_played = True
                return


KNOWN_ITEM_NAMES = ({"Rare Candy", "Buddy-Buddy Poffin", "Ultra Ball", "Poké Pad", "Night Stretcher",
                      "Energy Search", "Team Rocket's Transceiver", "Pokégear 3.0",
                      "Brilliant Blender"}
                     | set(FAMILY_BENCH_SEARCH_ITEMS))
# "Switch" repositions Active/Bench with no other effect (retreating isn't
# modeled at all, so this can't move any tracked metric either way).
# "Dangerous Laser" and "Dark Bell" apply Special Conditions, and
# "Special Red Card" resets the opponent's hand -- all real, strong
# effects in an actual game, but this simulator has no opponent board to
# apply them to, so they correctly score as having zero effect on any
# metric reported here. That's a real limit on what this tool can tell
# you about those cards specifically, not evidence they're weak.
NO_SELF_EFFECT_ITEMS = {"Switch", "Dangerous Laser", "Dark Bell", "Special Red Card"}


def collect_unmodeled(DECKLIST):
    unmodeled = set()
    for kind, name in DECKLIST:
        if kind == "Supporter" and name not in SUPPORTER_EFFECTS and name not in NO_SELF_EFFECT_SUPPORTERS:
            unmodeled.add(name)
        elif kind == "Item" and name not in KNOWN_ITEM_NAMES and name not in NO_SELF_EFFECT_ITEMS:
            unmodeled.add(name)
    return unmodeled


def play_turn(turn_num, state, going_first, POKEMON, priority, pre_evolutions, log):
    log.append(f"--- Turn {turn_num} ---")
    if not (turn_num == 1 and going_first):
        state.draw(1)
        log.append("Draw 1 for turn")
    state.supporter_played = False
    state.active_evolved_this_turn = False
    for _slot in state.bench:
        _slot["evolved_this_turn"] = False
    state.abilities_used = set()
    state.played_supporters_this_turn = set()
    play_basics(state, POKEMON, turn_num, log)
    try_evolve(state, POKEMON, turn_num, log)
    play_stadium(state, log)
    effect_grand_tree(state, POKEMON, turn_num, log)
    play_items(state, POKEMON, priority, turn_num, log)
    play_supporter(state, POKEMON, log)
    use_draw_abilities(state, POKEMON, log)
    attach_energy(state, POKEMON, pre_evolutions, log)
    try_evolve(state, POKEMON, turn_num, log)
    if turn_num > 1 or not going_first:
        try_attack(state, POKEMON, turn_num, log)
    bench_str = ", ".join(f"{s['name']}({s['energy']})" for s in state.bench)
    log.append(f"State: Active={state.active}({state.active_energy}e), "
               f"Bench=[{bench_str}], Hand={len(state.hand)}")


def run_playthrough(POKEMON, DECKLIST, num_turns=6, going_first=True, verbose=False):
    random.seed()
    deck = list(DECKLIST)
    priority = search_priority(POKEMON)
    pre_evolutions = pre_evolution_names(POKEMON)
    state = opening_hand(deck, POKEMON)
    log = []
    if verbose:
        print("=== Opening Hand ===")
        print("Hand:", sorted(n for _, n in state.hand))
        print()
    for turn in range(1, num_turns + 1):
        play_turn(turn, state, going_first, POKEMON, priority, pre_evolutions, log)
    if verbose:
        print("\n".join(log))
    return {
        "online_turn": dict(state.online_turn),
        "first_attack_turn": state.first_attack_turn,
        "final_hand": len(state.hand),
    }


def run_baseline(decklist_text, n=1000, num_turns=6, verbose_sample=False):
    POKEMON, DECKLIST, fallback_pooled, unresolved = build_deck_model(decklist_text)
    if verbose_sample:
        run_playthrough(POKEMON, DECKLIST, num_turns=num_turns, verbose=True)
        print()

    results = [run_playthrough(POKEMON, DECKLIST, num_turns=num_turns, verbose=False) for _ in range(n)]

    report = {
        "n": n,
        "deck_size": len(DECKLIST),
        "pokemon_names": list(POKEMON.keys()),
        "online_pct": {},
        "online_avg_turn": {},
        "first_attack_pct": 0.0,
        "first_attack_avg_turn": None,
        "avg_final_hand": statistics.mean(r["final_hand"] for r in results),
        "fallback_pooled": sorted(fallback_pooled),
        "unresolved": sorted(unresolved),
        "unmodeled_cards": sorted(collect_unmodeled(DECKLIST)),
    }
    for name in POKEMON:
        turns = [r["online_turn"][name] for r in results if name in r["online_turn"]]
        report["online_pct"][name] = 100 * len(turns) / n
        report["online_avg_turn"][name] = statistics.mean(turns) if turns else None

    attack_turns = [r["first_attack_turn"] for r in results if r["first_attack_turn"] is not None]
    report["first_attack_pct"] = 100 * len(attack_turns) / n
    report["first_attack_avg_turn"] = statistics.mean(attack_turns) if attack_turns else None
    return report


def print_report(report):
    print(f"===== Baseline simulation: {report['n']} trials, deck size {report['deck_size']} =====\n")
    print("Pokemon in play by turn 6 (% of trials, avg turn when it happened):")
    for name in report["pokemon_names"]:
        pct = report["online_pct"][name]
        avg = report["online_avg_turn"][name]
        avg_str = f"turn {avg:.2f}" if avg is not None else "n/a"
        print(f"  {name:<28} {pct:5.1f}%   avg {avg_str}")
    print()
    fa_avg = f"turn {report['first_attack_avg_turn']:.2f}" if report["first_attack_avg_turn"] is not None else "n/a"
    print(f"First attack landed by turn 6: {report['first_attack_pct']:.1f}% of trials (avg {fa_avg})")
    print(f"Average final hand size (turn 6): {report['avg_final_hand']:.2f}")
    if report["fallback_pooled"]:
        print(f"\nMatched by name only (no exact SET NUM in decklist or no exact printing found),"
              f" pooling every printing with that name: {', '.join(report['fallback_pooled'])}")
    if report["unresolved"]:
        print(f"\nNOT FOUND in pokemon_standard_cards.json (excluded from simulation): "
              f"{', '.join(report['unresolved'])}")
    if report["unmodeled_cards"]:
        print(f"\nNo modeled play effect (held in hand only, doesn't affect these numbers -- "
              f"review before trusting a deck that leans on these): {', '.join(report['unmodeled_cards'])}")
    print("\nNote: no retreating and no opponent are modeled (same as simulate_match.py's stated"
          " simplifications) -- these numbers measure development speed, not win rate.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    n = 1000
    verbose_sample = False
    for arg in sys.argv[2:]:
        if arg == "--verbose":
            verbose_sample = True
        else:
            n = int(arg)
    text = sys.stdin.read() if path == "-" else open(path).read()
    report = run_baseline(text, n=n, verbose_sample=verbose_sample)
    print_report(report)


if __name__ == "__main__":
    main()
