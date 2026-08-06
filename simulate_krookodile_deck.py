"""Single-playthrough development simulator for the Krookodile ex / Relicanth
hand-disruption deck (decks/krookodile_relicanth... -- see chat history).

Adapted from simulate_deck.py's pattern for a 3-stage evolution line
(Sandile -> Krokorok -> Krookodile ex) plus two support lines (Purrloin ->
Liepard, Dunsparce -> Dudunsparce) and a standalone Ability piece
(Relicanth). This deck deliberately runs no Rare Candy, so every
Krookodile ex that comes online here evolved normally through Krokorok --
meaning Memory Dive (Relicanth's Ability, modeled as "Krookodile ex can use
Tighten Up once Relicanth is in play") is always legally available once
both pieces are down, with no stack-skipping edge case to simulate.

Simplifications, stated up front (same spirit as simulate_match.py's own
list): no opponent, no retreating, Tools/Stadiums/Air Balloon/Rescue
Board/Night Stretcher are not modeled (they don't change board-development
timing questions), Team Rocket's Petrel is modeled as "fetch whichever Item
is most useful right now" rather than simulating a full any-Trainer search,
and attack damage is reported but there's no opposing board to apply it to.
This answers "how fast does the engine come online and how does the hand
hold up," not "who wins the game."
"""

import random

POKEMON = {
    "Sandile": {"stage": "Basic", "evolves_from": None, "hp": 70, "retreat": 1,
                "rule_box": False, "attacks": []},
    "Krokorok": {"stage": "Stage 1", "evolves_from": "Sandile", "hp": 100, "retreat": 2,
                 "rule_box": False, "attacks": [("Tighten Up", ["Darkness", "Colorless"], 40)]},
    "Krookodile ex": {"stage": "Stage 2", "evolves_from": "Krokorok", "hp": 320, "retreat": 3,
                       "rule_box": True,
                       "attacks": [("Corner", ["Darkness", "Colorless"], 80),
                                   ("Strong Bite", ["Darkness", "Darkness", "Colorless"], 140)]},
    "Relicanth": {"stage": "Basic", "evolves_from": None, "hp": 100, "retreat": 1,
                  "rule_box": False, "attacks": []},  # Razor Fin needs Fighting Energy we don't run
    "Purrloin": {"stage": "Basic", "evolves_from": None, "hp": 60, "retreat": 1,
                 "rule_box": False, "attacks": []},
    "Liepard": {"stage": "Stage 1", "evolves_from": "Purrloin", "hp": 110, "retreat": 1,
                "rule_box": False, "attacks": [("Knock Off", ["Darkness"], 50)]},
    "Dunsparce": {"stage": "Basic", "evolves_from": None, "hp": 60, "retreat": 0,
                  "rule_box": False, "attacks": []},
    "Dudunsparce": {"stage": "Stage 1", "evolves_from": "Dunsparce", "hp": 140, "retreat": 3,
                    "rule_box": False, "attacks": [("Land Crush", ["Colorless"] * 3, 90)]},
}

DECKLIST = (
    [("Pokemon", "Sandile")] * 4 +
    [("Pokemon", "Krokorok")] * 3 +
    [("Pokemon", "Krookodile ex")] * 3 +
    [("Pokemon", "Relicanth")] * 2 +
    [("Pokemon", "Purrloin")] * 3 +
    [("Pokemon", "Liepard")] * 2 +
    [("Pokemon", "Dunsparce")] * 3 +
    [("Pokemon", "Dudunsparce")] * 2 +
    [("Supporter", "Lillie's Determination")] * 4 +
    [("Item", "Ultra Ball")] * 1 +
    [("Supporter", "Boss's Orders")] * 1 +
    [("Supporter", "Xerosic's Machinations")] * 4 +
    [("Tool", "Punk Helmet")] * 1 +
    [("Tool", "Air Balloon")] * 1 +
    [("Tool", "Rescue Board")] * 1 +
    [("Item", "Night Stretcher")] * 1 +
    [("Item", "Poke Pad")] * 2 +
    [("Supporter", "Janine's Secret Art")] * 1 +
    [("Supporter", "Team Rocket's Petrel")] * 2 +
    [("Item", "Buddy-Buddy Poffin")] * 4 +
    [("Item", "Energy Search")] * 1 +
    [("Energy", "Basic Darkness Energy")] * 13 +
    [("Energy", "Enriching Energy")] * 1
)
assert len(DECKLIST) == 60, len(DECKLIST)

BUDDY_POFFIN_ELIGIBLE = ["Sandile", "Purrloin", "Dunsparce"]  # HP <= 70; Relicanth (100) doesn't qualify
LOAD_PRIORITY = ["Sandile", "Purrloin", "Relicanth", "Dunsparce"]
SEARCH_PRIORITY = ["Krokorok", "Krookodile ex", "Sandile", "Liepard", "Purrloin",
                   "Dudunsparce", "Dunsparce", "Relicanth"]
PRE_EVOLUTIONS = {name for name, info in POKEMON.items() if info["evolves_from"] is None
                   and any(other["evolves_from"] == name for other in POKEMON.values())}


class GameState:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.active = None
        self.active_energy = 0
        self.active_evolved_this_turn = False
        self.bench = []  # list of [name, energy]
        self.discard = []
        self.supporter_played = False
        self.krookodile_ex_online_turn = None
        self.relicanth_online_turn = None
        self.tighten_up_available_turn = None

    def draw(self, n=1):
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def has_basic_in_hand(self):
        return any(k == "Pokemon" and POKEMON[n]["stage"] == "Basic" for k, n in self.hand)

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

    def in_play_names(self):
        names = [n for n, _ in self.bench]
        if self.active:
            names.append(self.active)
        return names

    def hand_names(self):
        return [n for k, n in self.hand if k == "Pokemon"]


def opening_hand(deck):
    while True:
        random.shuffle(deck)
        state = GameState(deck)
        state.draw(7)
        if state.has_basic_in_hand():
            return state
        deck.extend(state.hand)
        state.hand = []


def play_basics(state, log):
    if state.active is None:
        for name in LOAD_PRIORITY:
            if ("Pokemon", name) in state.hand:
                state.remove_from_hand("Pokemon", name)
                state.active = name
                state.active_energy = 0
                log.append(f"Play {name} as Active")
                break
    for kind, name in list(state.hand):
        if kind == "Pokemon" and POKEMON[name]["stage"] == "Basic" and len(state.bench) < 5:
            state.remove_from_hand(kind, name)
            state.bench.append([name, 0])
            log.append(f"Bench {name}")


def try_evolve(state, turn, log):
    for kind, name in list(state.hand):
        if kind != "Pokemon":
            continue
        target = POKEMON[name]["evolves_from"]
        if target is None:
            continue
        if state.active == target:
            state.remove_from_hand(kind, name)
            state.active = name
            state.active_evolved_this_turn = True
            log.append(f"Evolve {target} -> {name} (Active, can't attack this turn)")
            if name == "Krookodile ex" and state.krookodile_ex_online_turn is None:
                state.krookodile_ex_online_turn = turn
        else:
            slot = next((s for s in state.bench if s[0] == target), None)
            if slot is not None:
                state.remove_from_hand(kind, name)
                slot[0] = name
                log.append(f"Evolve {target} -> {name} (Bench)")
                if name == "Krookodile ex" and state.krookodile_ex_online_turn is None:
                    state.krookodile_ex_online_turn = turn


def note_relicanth(state, turn):
    if state.relicanth_online_turn is None and "Relicanth" in state.in_play_names():
        state.relicanth_online_turn = turn
    if (state.tighten_up_available_turn is None
            and "Krookodile ex" in state.in_play_names()
            and "Relicanth" in state.in_play_names()):
        state.tighten_up_available_turn = turn


def play_supporter(state, log):
    if state.supporter_played:
        return
    if ("Supporter", "Lillie's Determination") in state.hand and len(state.hand) < 5:
        state.remove_from_hand("Supporter", "Lillie's Determination")
        state.discard.append("Lillie's Determination")
        state.draw(6)
        state.supporter_played = True
        log.append("Play Lillie's Determination (shuffle hand, draw 6)")
        return
    if ("Supporter", "Janine's Secret Art") in state.hand and state.in_play_names():
        targets = [n for n in state.in_play_names()][:2]
        state.remove_from_hand("Supporter", "Janine's Secret Art")
        state.discard.append("Janine's Secret Art")
        for t in targets:
            if t == state.active:
                state.active_energy += 1
            else:
                for slot in state.bench:
                    if slot[0] == t:
                        slot[1] += 1
        state.supporter_played = True
        log.append(f"Play Janine's Secret Art -> attach Darkness Energy to {', '.join(targets)}")
        return
    if ("Supporter", "Team Rocket's Petrel") in state.hand:
        want_energy = not any(k == "Energy" for k, _ in state.hand)
        fetch = ("Item", "Energy Search") if want_energy else ("Item", "Ultra Ball")
        if fetch in state.deck:
            state.remove_from_hand("Supporter", "Team Rocket's Petrel")
            state.discard.append("Team Rocket's Petrel")
            state.deck.remove(fetch)
            random.shuffle(state.deck)
            state.hand.append(fetch)
            state.supporter_played = True
            log.append(f"Play Team Rocket's Petrel -> search {fetch[1]}")
            return
    if ("Supporter", "Boss's Orders") in state.hand and len(state.hand) <= 2:
        # No opponent modeled; treat as a discard-for-nothing fallback only when desperate.
        pass


def choose_search_target(state, allow_rule_box):
    in_play = state.in_play_names()
    in_hand = state.hand_names()
    for name in SEARCH_PRIORITY:
        if not allow_rule_box and POKEMON[name]["rule_box"]:
            continue
        pre_evo = POKEMON[name]["evolves_from"]
        if name in in_play or name in in_hand:
            continue
        if pre_evo is not None and pre_evo not in in_play:
            continue
        return name
    return None


def play_items(state, log):
    while ("Item", "Buddy-Buddy Poffin") in state.hand and len(state.bench) < 4:
        found = []
        remaining = []
        for card in state.deck:
            if len(found) < 2 and card[0] == "Pokemon" and card[1] in BUDDY_POFFIN_ELIGIBLE:
                found.append(card[1])
            else:
                remaining.append(card)
        if not found:
            break
        state.remove_from_hand("Item", "Buddy-Buddy Poffin")
        state.discard.append("Buddy-Buddy Poffin")
        state.deck = remaining
        random.shuffle(state.deck)
        for name in found:
            state.bench.append([name, 0])
        log.append(f"Play Buddy-Buddy Poffin -> bench {', '.join(found)}")

    while ("Item", "Ultra Ball") in state.hand:
        target = choose_search_target(state, allow_rule_box=True)
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

    while ("Item", "Poke Pad") in state.hand:
        target = choose_search_target(state, allow_rule_box=False)
        if target is None:
            break
        state.remove_from_hand("Item", "Poke Pad")
        state.discard.append("Poke Pad")
        state.deck.remove(("Pokemon", target))
        random.shuffle(state.deck)
        state.hand.append(("Pokemon", target))
        log.append(f"Play Poke Pad -> search {target}")

    if ("Item", "Energy Search") in state.hand:
        if ("Energy", "Basic Darkness Energy") in state.deck:
            state.remove_from_hand("Item", "Energy Search")
            state.discard.append("Energy Search")
            state.deck.remove(("Energy", "Basic Darkness Energy"))
            random.shuffle(state.deck)
            state.hand.append(("Energy", "Basic Darkness Energy"))
            log.append("Play Energy Search -> get Basic Darkness Energy")


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


def energy_need(name, energy_attached):
    if not POKEMON[name]["attacks"]:
        return 0
    needed = len(POKEMON[name]["attacks"][0][1])
    return max(0, needed - energy_attached)


def attach_energy(state, log):
    energy_card = next((c for c in state.hand if c[0] == "Energy"), None)
    if energy_card is None:
        return
    target = None
    if state.active and energy_need(state.active, state.active_energy) > 0:
        target = "active"
    else:
        for slot in state.bench:
            if slot[0] in PRE_EVOLUTIONS:
                target = slot
                break
        if target is None:
            for slot in state.bench:
                if energy_need(slot[0], slot[1]) > 0:
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
        target[1] += 1
        log.append(f"Attach {energy_card[1]} to {target[0]} (Bench, now {target[1]})")


def try_attack(state, log):
    if not state.active or state.active_evolved_this_turn:
        return
    info = POKEMON[state.active]
    if not info["attacks"]:
        return
    name, cost, dmg = info["attacks"][0]
    needed = len(cost)
    if state.active_energy >= needed:
        log.append(f"Attack: {state.active} uses {name} for {dmg} "
                   f"({state.active_energy} energy, needed {needed})")


def play_turn(turn_num, state, going_first, log):
    log.append(f"--- Turn {turn_num} ---")
    if not (turn_num == 1 and going_first):
        state.draw(1)
        log.append("Draw 1 for turn")
    state.supporter_played = False
    state.active_evolved_this_turn = False
    play_basics(state, log)
    try_evolve(state, turn_num, log)
    play_items(state, log)
    play_supporter(state, log)
    attach_energy(state, log)
    try_evolve(state, turn_num, log)
    note_relicanth(state, turn_num)
    if turn_num > 1 or not going_first:
        try_attack(state, log)
    bench_str = ", ".join(f"{n}({e})" for n, e in state.bench)
    log.append(f"State: Active={state.active}({state.active_energy}e), "
               f"Bench=[{bench_str}], Hand={len(state.hand)}")


def run_playthrough(num_turns=6, going_first=True, verbose=True):
    random.seed()
    deck = list(DECKLIST)
    state = opening_hand(deck)
    if verbose:
        print("=== Opening Hand ===")
        print("Hand:", sorted(n for _, n in state.hand))
        print()
    log = []
    for turn in range(1, num_turns + 1):
        play_turn(turn, state, going_first, log)
    if verbose:
        print("\n".join(log))
    return {
        "krookodile_ex_round": state.krookodile_ex_online_turn,
        "relicanth_round": state.relicanth_online_turn,
        "tighten_up_round": state.tighten_up_available_turn,
        "final_hand": len(state.hand),
    }


if __name__ == "__main__":
    run_playthrough()
