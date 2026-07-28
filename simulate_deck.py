"""Single-playthrough simulator for the Psychic Item-Lock deck.

Shuffles the deck, deals an opening hand (with mulligans), then plays turns 1-3
using simple heuristic priorities: develop the board, evolve when possible,
search/draw with Items and one Supporter per turn, attach energy, attack if able.

This is a single random sample, not a statistical simulation. It's the first
step toward a Monte Carlo version that runs many shuffles and reports
probabilities (e.g. "% of games with Jellicent ex active by turn 3").
"""

import random

POKEMON = {
    "Budew": {"stage": "Basic", "evolves_from": None, "hp": 30, "retreat": 0,
              "attack": ("Itchy Pollen", [], 10)},
    "Frillish": {"stage": "Basic", "evolves_from": None, "hp": 80, "retreat": 3,
                 "attack": ("Oceanic Gloom", ["Psychic"], 20)},
    "Jellicent ex": {"stage": "Stage 1", "evolves_from": "Frillish", "hp": 270, "retreat": 3,
                      "attack": ("Power Press", ["Psychic", "Colorless"], 80)},
    "Eevee": {"stage": "Basic", "evolves_from": None, "hp": 70, "retreat": 1,
              "attack": ("Headbutt", ["Colorless", "Colorless"], 20)},
    "Espeon ex": {"stage": "Stage 1", "evolves_from": "Eevee", "hp": 270, "retreat": 1,
                   "attack": ("Psych Out", ["Psychic", "Colorless", "Colorless"], 160)},
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


class GameState:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.active = None       # pokemon name
        self.active_energy = 0
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
        info = POKEMON[name]
        target = info["evolves_from"]
        if target is None:
            continue
        if state.active == target:
            state.remove_from_hand(kind, name)
            state.active = name
            log.append(f"Evolve {target} -> {name}")
        else:
            slot = next((s for s in state.bench if s[0] == target), None)
            if slot is not None:
                state.remove_from_hand(kind, name)
                slot[0] = name
                log.append(f"Evolve {target} -> {name} (on Bench)")


def play_supporter(state, log):
    if state.supporter_played:
        return
    if ("Supporter", "Lillie's Determination") in state.hand and len(state.hand) < 5:
        state.remove_from_hand("Supporter", "Lillie's Determination")
        state.discard.append("Lillie's Determination")
        state.draw(6)
        state.supporter_played = True
        log.append("Play Lillie's Determination (shuffle hand, draw 6)")


def play_items(state, log):
    # Buddy-Buddy Poffin: bench up to 2 eligible Basics straight from the deck
    if ("Item", "Buddy-Buddy Poffin") in state.hand and len(state.bench) < 4:
        found = []
        remaining_deck = []
        for card in state.deck:
            if len(found) < 2 and card[0] == "Pokemon" and card[1] in BUDDY_POFFIN_ELIGIBLE:
                found.append(card[1])
            else:
                remaining_deck.append(card)
        if found:
            state.remove_from_hand("Item", "Buddy-Buddy Poffin")
            state.discard.append("Buddy-Buddy Poffin")
            state.deck = remaining_deck
            random.shuffle(state.deck)
            for name in found:
                state.bench.append([name, 0])
            log.append(f"Play Buddy-Buddy Poffin -> bench {', '.join(found)} from deck")

    # Ultra Ball: discard 2, search any Pokemon, only if missing a key ex piece and have spare cards
    key_missing = "Jellicent ex" not in state.in_play_names() and "Espeon ex" not in state.in_play_names()
    if ("Item", "Ultra Ball") in state.hand and key_missing and len(state.hand) >= 3:
        discard_candidates = [c for c in state.hand if c != ("Item", "Ultra Ball")][:2]
        if len(discard_candidates) == 2:
            for c in discard_candidates:
                state.remove_from_hand(*c)
                state.discard.append(c[1])
            state.remove_from_hand("Item", "Ultra Ball")
            state.discard.append("Ultra Ball")
            for i, card in enumerate(state.deck):
                if card[0] == "Pokemon":
                    found_card = state.deck.pop(i)
                    random.shuffle(state.deck)
                    state.hand.append(found_card)
                    log.append(f"Play Ultra Ball (discard {discard_candidates[0][1]}, "
                               f"{discard_candidates[1][1]}) -> search {found_card[1]}")
                    break


def attach_energy(state, log):
    if ("Energy", "Basic Psychic Energy") in state.hand:
        state.remove_from_hand("Energy", "Basic Psychic Energy")
        if state.active:
            state.active_energy += 1
            log.append(f"Attach Basic Psychic Energy to {state.active} "
                       f"(now {state.active_energy})")


def try_attack(state, log):
    if not state.active:
        return
    info = POKEMON[state.active]
    name, cost, dmg = info["attack"]
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
    play_basics(state, log)
    try_evolve(state, log)
    play_items(state, log)
    play_supporter(state, log)
    attach_energy(state, log)
    try_evolve(state, log)  # in case a newly drawn/found evolution can go down
    if turn_num > 1 or not going_first:
        try_attack(state, log)
    log.append(f"State: Active={state.active}({state.active_energy} energy), "
               f"Bench={state.bench}, Hand size={len(state.hand)}")


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
