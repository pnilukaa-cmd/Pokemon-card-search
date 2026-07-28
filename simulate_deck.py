"""Single-playthrough simulator for the Psychic Item-Lock deck.

Shuffles the deck, deals an opening hand (with mulligans), then plays turns 1-3
using heuristic priorities: develop the board, evolve when possible, search
with Items, play one Supporter per turn, attach energy where it's needed,
attack if able (respecting the "just evolved" no-attack rule).

This is a single random sample, not a statistical simulation. It's the first
step toward a Monte Carlo version that runs many shuffles and reports
probabilities (e.g. "% of games with Jellicent ex active by turn 3").
"""

import random

POKEMON = {
    "Budew": {"stage": "Basic", "evolves_from": None, "hp": 30, "retreat": 0,
              "rule_box": False, "attack": ("Itchy Pollen", [], 10)},
    "Frillish": {"stage": "Basic", "evolves_from": None, "hp": 80, "retreat": 3,
                 "rule_box": False, "attack": ("Oceanic Gloom", ["Psychic"], 20)},
    "Jellicent ex": {"stage": "Stage 1", "evolves_from": "Frillish", "hp": 270, "retreat": 3,
                      "rule_box": True, "attack": ("Power Press", ["Psychic", "Colorless"], 80)},
    "Eevee": {"stage": "Basic", "evolves_from": None, "hp": 70, "retreat": 1,
              "rule_box": False, "attack": ("Headbutt", ["Colorless", "Colorless"], 20)},
    "Espeon ex": {"stage": "Stage 1", "evolves_from": "Eevee", "hp": 270, "retreat": 1,
                   "rule_box": True, "attack": ("Psych Out", ["Psychic", "Colorless", "Colorless"], 160)},
}

DECKLIST = (
    [("Pokemon", "Budew")] * 3 +
    [("Pokemon", "Frillish")] * 3 +
    [("Pokemon", "Jellicent ex")] * 3 +
    [("Pokemon", "Eevee")] * 3 +
    [("Pokemon", "Espeon ex")] * 3 +
    [("Supporter", "Boss's Orders")] * 4 +
    [("Supporter", "Xerosic's Machinations")] * 3 +
    [("Supporter", "Eri")] * 3 +
    [("Supporter", "Lillie's Determination")] * 4 +
    [("Supporter", "Judge")] * 3 +
    [("Item", "Ultra Ball")] * 3 +
    [("Item", "Poke Pad")] * 3 +
    [("Item", "Buddy-Buddy Poffin")] * 4 +
    [("Item", "Night Stretcher")] * 4 +
    [("Energy", "Basic Psychic Energy")] * 14
)
assert len(DECKLIST) == 60, len(DECKLIST)

BUDDY_POFFIN_ELIGIBLE = ["Budew", "Eevee"]  # HP <= 70
LOAD_PRIORITY = ["Frillish", "Eevee", "Budew"]  # who to lead as Active

# Which Pokemon to search for, in priority order, given what's already in play/hand.
# Each entry: (name, condition function) -- first satisfied entry wins.
SEARCH_PRIORITY = ["Jellicent ex", "Espeon ex", "Frillish", "Eevee", "Budew"]


class GameState:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.active = None       # pokemon name
        self.active_energy = 0
        self.active_evolved_this_turn = False
        self.bench = []          # list of [pokemon name, energy attached]
        self.discard = []
        self.supporter_played = False

    def draw(self, n=1):
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def has_basic_in_hand(self):
        return any(kind == "Pokemon" and POKEMON[name]["stage"] == "Basic"
                   for kind, name in self.hand)

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

    def in_play_names(self):
        names = [name for name, _ in self.bench]
        if self.active:
            names.append(self.active)
        return names

    def hand_names(self):
        return [name for kind, name in self.hand if kind == "Pokemon"]


def opening_hand(deck):
    while True:
        random.shuffle(deck)
        state = GameState(deck)
        state.draw(7)
        if state.has_basic_in_hand():
            return state
        print("  Mulligan (no Basic Pokemon) -- reshuffling and redrawing 7")
        deck.extend(state.hand)
        state.hand = []


def play_basics(state, log):
    # Lead with the highest-priority Basic if no Active yet
    if state.active is None:
        for name in LOAD_PRIORITY:
            if ("Pokemon", name) in state.hand:
                state.remove_from_hand("Pokemon", name)
                state.active = name
                state.active_energy = 0
                log.append(f"Play {name} as Active Pokemon")
                break
    # Bench every other Basic in hand
    for kind, name in list(state.hand):
        if kind == "Pokemon" and POKEMON[name]["stage"] == "Basic" and len(state.bench) < 5:
            state.remove_from_hand(kind, name)
            state.bench.append([name, 0])
            log.append(f"Bench {name}")


def try_evolve(state, log):
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
            log.append(f"Evolve {target} -> {name} (can't attack this turn)")
        else:
            slot = next((s for s in state.bench if s[0] == target), None)
            if slot is not None:
                state.remove_from_hand(kind, name)
                slot[0] = name
                log.append(f"Evolve {target} -> {name} (on Bench)")


def play_supporter(state, log):
    if state.supporter_played:
        return
    # Priority 1: Lillie's Determination as the main draw engine, when hand is thin
    if ("Supporter", "Lillie's Determination") in state.hand and len(state.hand) < 5:
        state.remove_from_hand("Supporter", "Lillie's Determination")
        state.discard.append("Lillie's Determination")
        state.draw(6)
        state.supporter_played = True
        log.append("Play Lillie's Determination (shuffle hand, draw 6)")
        return
    # Priority 2: Judge as an emergency refill when hand is nearly empty and no
    # Lillie's is available. (Boss's Orders / Xerosic's Machinations / Eri are
    # opponent-reactive and have no clear single-player use, so they're held.)
    if ("Supporter", "Judge") in state.hand and len(state.hand) <= 1:
        state.remove_from_hand("Supporter", "Judge")
        state.discard.append("Judge")
        state.hand = []
        state.draw(4)
        state.supporter_played = True
        log.append("Play Judge (shuffle hand, draw 4)")


def choose_search_target(state, allow_rule_box):
    """Pick the most useful Pokemon to fetch from the deck right now."""
    in_play = state.in_play_names()
    in_hand = state.hand_names()
    for name in SEARCH_PRIORITY:
        if not allow_rule_box and POKEMON[name]["rule_box"]:
            continue
        pre_evo = POKEMON[name]["evolves_from"]
        if name in in_play or name in in_hand:
            continue  # already have one, no need for another right now
        if pre_evo is not None and pre_evo not in in_play:
            continue  # would just sit dead in hand without its pre-evolution
        return name
    return None


def play_items(state, log):
    # Buddy-Buddy Poffin: bench up to 2 eligible Basics straight from the deck.
    # Repeats if multiple copies are in hand and there's still bench room.
    while ("Item", "Buddy-Buddy Poffin") in state.hand and len(state.bench) < 4:
        found = []
        remaining_deck = []
        for card in state.deck:
            if len(found) < 2 and card[0] == "Pokemon" and card[1] in BUDDY_POFFIN_ELIGIBLE:
                found.append(card[1])
            else:
                remaining_deck.append(card)
        if not found:
            break
        state.remove_from_hand("Item", "Buddy-Buddy Poffin")
        state.discard.append("Buddy-Buddy Poffin")
        state.deck = remaining_deck
        random.shuffle(state.deck)
        for name in found:
            state.bench.append([name, 0])
        log.append(f"Play Buddy-Buddy Poffin -> bench {', '.join(found)} from deck")

    # Ultra Ball: discard 2, search any Pokemon (including ex). Repeats while
    # there's a useful target and enough spare cards to pay the discard cost.
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
        log.append(f"Play Ultra Ball (discard {discard_candidates[0][1]}, "
                   f"{discard_candidates[1][1]}) -> search {target}")

    # Poke Pad: search a non-Rule-Box Pokemon (can't fetch Jellicent ex / Espeon ex).
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


def discard_value(state, card):
    """Lower score = safer to discard for a cost like Ultra Ball."""
    kind, name = card
    if kind == "Energy":
        # Keep at least a couple of energy in hand to keep attaching each turn.
        energy_in_hand = sum(1 for k, n in state.hand if k == "Energy")
        return 0 if energy_in_hand > 2 else 2
    if kind == "Pokemon":
        # Redundant copy (already have one in play or elsewhere in hand) is cheap to lose.
        count_in_hand = sum(1 for k, n in state.hand if k == "Pokemon" and n == name)
        return 1 if (name in state.in_play_names() or count_in_hand > 1) else 3
    if kind == "Item":
        return 2
    return 4  # Supporter: protect these, discard last


def energy_need(name, energy_attached):
    needed = len(POKEMON[name]["attack"][1])
    return max(0, needed - energy_attached)


PRE_EVOLUTIONS = {name for name, info in POKEMON.items() if info["evolves_from"] is None
                   and any(other["evolves_from"] == name for other in POKEMON.values())}


def attach_energy(state, log):
    if ("Energy", "Basic Psychic Energy") not in state.hand:
        return
    # 1. Power up the Active if it isn't yet at its own attack's threshold.
    # 2. Otherwise pre-load a benched pre-evolution (Frillish/Eevee) even if it
    #    doesn't need energy yet -- it carries over when evolved into the ex.
    # 3. Otherwise any other benched Pokemon that still needs energy.
    # 4. Otherwise hold the energy rather than stranding it on a dead-end
    #    Pokemon (e.g. Budew, which never evolves and needs 0 to attack).
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
        log.append("Hold Basic Psychic Energy (no useful attachment target this turn)")
        return

    state.remove_from_hand("Energy", "Basic Psychic Energy")
    if target == "active":
        state.active_energy += 1
        log.append(f"Attach Basic Psychic Energy to {state.active} (Active, now {state.active_energy})")
    else:
        target[1] += 1
        log.append(f"Attach Basic Psychic Energy to {target[0]} (Bench, now {target[1]})")


def try_attack(state, log):
    if not state.active or state.active_evolved_this_turn:
        return
    name, cost, dmg = POKEMON[state.active]["attack"]
    needed = len(cost)
    if state.active_energy >= needed:
        log.append(f"Attack: {state.active} uses {name} for {dmg} damage "
                   f"({state.active_energy} energy attached, needed {needed})")


def play_turn(turn_num, state, going_first, log):
    log.append(f"--- Turn {turn_num} ---")
    if not (turn_num == 1 and going_first):
        state.draw(1)
        log.append("Draw 1 card for turn")
    state.supporter_played = False
    state.active_evolved_this_turn = False
    play_basics(state, log)
    try_evolve(state, log)
    play_items(state, log)
    play_supporter(state, log)
    attach_energy(state, log)
    try_evolve(state, log)  # in case a newly drawn/found evolution can go down
    if turn_num > 1 or not going_first:
        try_attack(state, log)
    bench_str = ", ".join(f"{n}({e})" for n, e in state.bench)
    log.append(f"State: Active={state.active}({state.active_energy} energy), "
               f"Bench=[{bench_str}], Hand size={len(state.hand)}")


def main():
    random.seed()
    deck = list(DECKLIST)
    print("=== Opening Hand ===")
    state = opening_hand(deck)
    print("Hand:", sorted(name for _, name in state.hand))
    print()

    going_first = True
    log = []
    for turn in (1, 2, 3):
        play_turn(turn, state, going_first, log)

    print("\n".join(log))


if __name__ == "__main__":
    main()
