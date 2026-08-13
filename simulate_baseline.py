#!/usr/bin/env python3
"""Generic baseline development-timing simulator + Monte Carlo runner.

Unlike simulate_deck.py / simulate_krookodile_deck.py (both hand-coded for
one specific decklist each), this reads ANY decklist in this project's
plain-text PTCGL format and builds its Pokemon model directly from
pokemon_standard_cards.json -- stage, evolvesFrom, HP, retreat cost, types,
and attacks are all pulled from the real card data, matched by exact
SET NUM when the decklist provides it (falling back to name-only pooling,
same fallback check_energy_support.py uses, if it doesn't).

Trainer/Item/Supporter effects are modeled through a hand-authored
registry (see EFFECT registries below) covering the staples this project
has actually used across decks/ so far. A card with no registered handler
is simply held in hand -- it's never misplayed, and every such name is
reported once at the end of a run so a gap is visible rather than silent.
Pokemon Tools and Stadiums are deliberately out of scope entirely (never
attached/played) since they don't change board-development timing
questions, the same simplification simulate_krookodile_deck.py already
disclosed.

Same stated simplifications as simulate_deck.py/simulate_match.py: no
retreating (so only whatever ends up Active on turn 1 -- or what it
evolves into -- ever attacks in a run) and no opponent modeled. Energy
type-correctness is NOT re-checked here (that's check_energy_support.py's
job); this only counts total attached Energy against total attack-cost
length. This answers "how fast does the engine come online, and how does
the hand hold up," not "who wins."

Usage:
  python3 simulate_baseline.py decklist.txt          # 1000-trial baseline
  python3 simulate_baseline.py decklist.txt 500       # custom trial count
  python3 simulate_baseline.py decklist.txt --verbose # + one full sample log
"""
import random
import re
import sys
import statistics
from collections import defaultdict

sys.path.insert(0, ".")
from check_energy_support import load_cards, BASIC_ENERGY_RE, SYMBOL_TO_TYPE

LINE_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")


def parse_decklist_entries(text):
    """Like check_energy_support.parse_decklist, but keeps the SET/NUM
    tokens (when present) instead of discarding them, so cards can be
    resolved to their exact printing."""
    out = []
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if not m:
            continue
        count, rest = int(m.group(1)), m.group(2)
        tokens = rest.split()
        set_code = number = None
        if tokens and tokens[-1].isdigit():
            number = tokens[-1]
            tokens = tokens[:-1]
            if tokens and re.fullmatch(r"[A-Za-z0-9]{2,6}", tokens[-1]) and tokens[-1].isupper():
                set_code = tokens[-1]
                tokens = tokens[:-1]
        name = " ".join(tokens).strip()
        if not name:
            continue

        def expand(mm):
            return SYMBOL_TO_TYPE.get(mm.group(1).upper(), mm.group(0))
        name = re.sub(r"\{(\w)\}", expand, name)
        name = re.sub(r"^Basic (\w+) Energy$", r"\1 Energy", name)
        out.append({"count": count, "name": name, "set": set_code, "number": number})
    return out


def build_card_index(cards):
    by_name = defaultdict(list)
    by_setnum = {}
    for c in cards:
        by_name[c["name"]].append(c)
        code = (c.get("set") or {}).get("ptcgoCode")
        num = c.get("number")
        if code and num:
            by_setnum[(c["name"], code, num)] = c
    return by_name, by_setnum


def resolve_card(entry, by_name, by_setnum):
    """Returns (card_or_None, matched_exact_printing: bool)."""
    if entry["set"] and entry["number"]:
        c = by_setnum.get((entry["name"], entry["set"], entry["number"]))
        if c:
            return c, True
    matches = by_name.get(entry["name"])
    if matches:
        return matches[0], False
    return None, False


def stage_of(card):
    subtypes = card.get("subtypes") or []
    if "Basic" in subtypes:
        return "Basic"
    if "Stage 1" in subtypes:
        return "Stage 1"
    if "Stage 2" in subtypes:
        return "Stage 2"
    return "Basic" if not card.get("evolvesFrom") else "Stage 1"


def is_rule_box(card):
    subtypes = set(card.get("subtypes") or [])
    return bool(subtypes - {"Basic", "Stage 1", "Stage 2", "Restored"})


DAMAGE_RE = re.compile(r"^\D*(\d+)")


def parse_damage(dmg):
    if not dmg:
        return 0
    m = DAMAGE_RE.match(dmg)
    return int(m.group(1)) if m else 0


def build_pokemon_info(card):
    attacks = []
    for atk in card.get("attacks") or []:
        cost = atk.get("cost") or []
        attacks.append((atk["name"], cost, parse_damage(atk.get("damage"))))
    retreat = card.get("convertedRetreatCost")
    if retreat is None:
        retreat = len(card.get("retreatCost") or [])
    return {
        "stage": stage_of(card),
        "evolves_from": card.get("evolvesFrom"),
        "hp": int(card.get("hp") or 0),
        "retreat": retreat,
        "rule_box": is_rule_box(card),
        "types": card.get("types") or [],
        "attacks": attacks,
    }


def build_deck_model(text):
    """Returns (POKEMON dict, DECKLIST list-of-(kind,name), fallback_pooled
    set of names matched by name only, unresolved list of names not found
    at all)."""
    entries = parse_decklist_entries(text)
    cards = load_cards()
    by_name, by_setnum = build_card_index(cards)
    POKEMON = {}
    DECKLIST = []
    fallback_pooled = set()
    unresolved = []
    for entry in entries:
        name, count = entry["name"], entry["count"]
        if BASIC_ENERGY_RE.match(name):
            DECKLIST += [("Energy", name)] * count
            continue
        card, exact = resolve_card(entry, by_name, by_setnum)
        if card is None:
            unresolved.append(name)
            continue
        if not exact:
            fallback_pooled.add(name)
        supertype = card.get("supertype")
        if supertype == "Pokémon":
            if name not in POKEMON:
                POKEMON[name] = build_pokemon_info(card)
            DECKLIST += [("Pokemon", name)] * count
        elif supertype == "Energy":
            DECKLIST += [("Energy", name)] * count
        else:  # Trainer
            subtypes = set(card.get("subtypes") or [])
            if "Supporter" in subtypes:
                kind = "Supporter"
            elif "Pokémon Tool" in subtypes:
                kind = "Tool"
            elif "Stadium" in subtypes:
                kind = "Stadium"
            else:
                kind = "Item"
            DECKLIST += [(kind, name)] * count
    return POKEMON, DECKLIST, fallback_pooled, unresolved


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
            state.bench.append({"name": name, "energy": 0, "entered_turn": turn})
            state.note_online(name, turn)
            log.append(f"Bench {name}")


def try_evolve(state, POKEMON, turn, log):
    for kind, name in list(state.hand):
        if kind != "Pokemon":
            continue
        target = POKEMON[name]["evolves_from"]
        if target is None:
            continue
        if state.active == target and turn > state.active_entered_turn:
            state.remove_from_hand(kind, name)
            state.active = name
            state.active_evolved_this_turn = True
            state.note_online(name, turn)
            log.append(f"Evolve {target} -> {name} (Active, can't attack this turn)")
            continue
        slot = next((s for s in state.bench if s["name"] == target and turn > s["entered_turn"]), None)
        if slot is not None:
            state.remove_from_hand(kind, name)
            slot["name"] = name
            state.note_online(name, turn)
            log.append(f"Evolve {target} -> {name} (Bench)")


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
    needed = len(attacks[0][1])
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
    name, cost, dmg = attacks[0]
    needed = len(cost)
    if state.active_energy >= needed:
        if state.first_attack_turn is None:
            state.first_attack_turn = turn
        log.append(f"Attack: {state.active} uses {name} for {dmg} "
                   f"({state.active_energy} energy, needed {needed})")


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
                state.bench.append({"name": name, "energy": 0, "entered_turn": turn})
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
            state.bench.append({"name": name, "energy": 0, "entered_turn": turn})
            state.note_online(name, turn)
        log.append(f"Play Buddy-Buddy Poffin -> bench {', '.join(found)}")

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


def effect_lillies_determination(state, POKEMON, log):
    if len(state.hand) >= 5:
        return False
    state.remove_from_hand("Supporter", "Lillie's Determination")
    state.discard.append("Lillie's Determination")
    state.draw(6)
    log.append("Play Lillie's Determination (shuffle hand, draw 6)")
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


SUPPORTER_PRIORITY = ["Lillie's Determination", "Janine's Secret Art", "Team Rocket's Petrel"]
SUPPORTER_EFFECTS = {
    "Lillie's Determination": effect_lillies_determination,
    "Janine's Secret Art": effect_janines_secret_art,
    "Team Rocket's Petrel": effect_petrel,
}
# Real cards whose whole effect targets the opponent's side (or a
# Prize-count condition we don't track) -- correctly left unplayed rather
# than misrepresented as "unmodeled gap," since they have zero effect on
# any metric this simulator reports.
NO_SELF_EFFECT_SUPPORTERS = {"Boss's Orders", "Xerosic's Machinations", "Rosa's Encouragement"}


def play_supporter(state, POKEMON, log):
    if state.supporter_played:
        return
    for name in SUPPORTER_PRIORITY:
        if ("Supporter", name) in state.hand:
            handler = SUPPORTER_EFFECTS[name]
            if handler(state, POKEMON, log):
                state.supporter_played = True
                return


KNOWN_ITEM_NAMES = ({"Rare Candy", "Buddy-Buddy Poffin", "Ultra Ball", "Poké Pad", "Night Stretcher", "Energy Search"}
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
    play_basics(state, POKEMON, turn_num, log)
    try_evolve(state, POKEMON, turn_num, log)
    play_stadium(state, log)
    effect_grand_tree(state, POKEMON, turn_num, log)
    play_items(state, POKEMON, priority, turn_num, log)
    play_supporter(state, POKEMON, log)
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
