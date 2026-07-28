"""Two-player match simulator: our Psychic Item-Lock deck vs. a Dragapult ex
deck modeled on the current meta archetype (Dreepy/Drakloak/Dragapult ex +
Fezandipiti ex for draw).

Both players get simplified heuristic AI. Ours reacts to the opponent's
board/hand state (e.g. Eri when their hand is large, Boss's Orders to snipe
an exposed low-HP threat). The opponent plays a simpler generic heuristic
(develop board, search, attack) without reacting to us.

Simplifications, stated up front:
- Energy is tracked as a plain count per attack, not by type. This matters
  for the opponent's Dragapult ex (Fire+Psychic in the real card) -- here
  any 2 attached energy satisfy it. Good enough for board-development
  timing questions, not for "can they actually pay this specific cost."
- No retreating/switching. The Active Pokemon only changes via evolution.
- Prize cards / knockouts are not modeled -- this simulates board and hand
  development over the first few turns, not a full game to completion.
"""

import random

# ---------------------------------------------------------------- Our deck

OUR_POKEMON = {
    "Budew": {"stage": "Basic", "evolves_from": None, "hp": 30, "retreat": 0,
              "rule_box": False, "attacks": [("Itchy Pollen", 0, 10)]},
    "Frillish": {"stage": "Basic", "evolves_from": None, "hp": 80, "retreat": 3,
                 "rule_box": False, "attacks": [("Oceanic Gloom", 1, 20)]},
    "Jellicent ex": {"stage": "Stage 1", "evolves_from": "Frillish", "hp": 270, "retreat": 3,
                      "rule_box": True, "attacks": [("Power Press", 2, 80)]},
    "Eevee": {"stage": "Basic", "evolves_from": None, "hp": 70, "retreat": 1,
              "rule_box": False, "attacks": [("Headbutt", 2, 20)]},
    "Espeon ex": {"stage": "Stage 1", "evolves_from": "Eevee", "hp": 270, "retreat": 1,
                   "rule_box": True, "attacks": [("Psych Out", 3, 160)]},
}
OUR_DECKLIST = (
    [("Pokemon", "Budew")] * 3 + [("Pokemon", "Frillish")] * 3 +
    [("Pokemon", "Jellicent ex")] * 3 + [("Pokemon", "Eevee")] * 3 +
    [("Pokemon", "Espeon ex")] * 3 +
    [("Supporter", "Boss's Orders")] * 4 + [("Supporter", "Xerosic's Machinations")] * 3 +
    [("Supporter", "Eri")] * 3 + [("Supporter", "Lillie's Determination")] * 4 +
    [("Supporter", "Judge")] * 3 +
    [("Item", "Ultra Ball")] * 3 + [("Item", "Poke Pad")] * 3 +
    [("Item", "Buddy-Buddy Poffin")] * 4 + [("Item", "Night Stretcher")] * 4 +
    [("Energy", "Energy")] * 14
)
assert len(OUR_DECKLIST) == 60, len(OUR_DECKLIST)
OUR_BUDDY_POFFIN_ELIGIBLE = ["Budew", "Eevee"]
OUR_LOAD_PRIORITY = ["Frillish", "Eevee", "Budew"]
OUR_SEARCH_PRIORITY = ["Jellicent ex", "Espeon ex", "Frillish", "Eevee", "Budew"]

# ------------------------------------------------------------- Their deck

OPP_POKEMON = {
    "Dreepy": {"stage": "Basic", "evolves_from": None, "hp": 70, "retreat": 1,
               "rule_box": False, "attacks": [("Bite", 2, 40)]},
    "Drakloak": {"stage": "Stage 1", "evolves_from": "Dreepy", "hp": 90, "retreat": 1,
                 "rule_box": False, "attacks": [("Dragon Headbutt", 2, 70)]},
    "Dragapult ex": {"stage": "Stage 2", "evolves_from": "Drakloak", "hp": 320, "retreat": 1,
                       "rule_box": True,
                       "attacks": [("Jet Headbutt", 1, 70), ("Phantom Dive", 2, 200)]},
    "Fezandipiti ex": {"stage": "Basic", "evolves_from": None, "hp": 210, "retreat": 1,
                         "rule_box": True, "attacks": [("Cruel Arrow", 3, 100)]},
}
OPP_DECKLIST = (
    [("Pokemon", "Dreepy")] * 4 + [("Pokemon", "Drakloak")] * 3 +
    [("Pokemon", "Dragapult ex")] * 4 + [("Pokemon", "Fezandipiti ex")] * 4 +
    [("Supporter", "Boss's Orders")] * 4 + [("Supporter", "Lacey")] * 4 +
    [("Supporter", "Crispin")] * 4 +
    [("Item", "Ultra Ball")] * 4 + [("Item", "Rare Candy")] * 4 +
    [("Item", "Buddy-Buddy Poffin")] * 4 + [("Item", "Night Stretcher")] * 4 +
    [("Energy", "Energy")] * 17
)
assert len(OPP_DECKLIST) == 60, len(OPP_DECKLIST)
OPP_BUDDY_POFFIN_ELIGIBLE = ["Dreepy"]  # HP <= 70
OPP_LOAD_PRIORITY = ["Dreepy", "Fezandipiti ex"]
OPP_SEARCH_PRIORITY = ["Dragapult ex", "Drakloak", "Dreepy", "Fezandipiti ex"]


# ------------------------------------------------------------------ Engine

class Player:
    def __init__(self, name, pokemon_defs, decklist, buddy_eligible, load_priority, search_priority):
        self.name = name
        self.defs = pokemon_defs
        self.deck = list(decklist)
        random.shuffle(self.deck)
        self.buddy_eligible = buddy_eligible
        self.load_priority = load_priority
        self.search_priority = search_priority
        self.hand = []
        self.active = None
        self.active_energy = 0
        self.active_evolved_this_turn = False
        self.bench = []  # list of [name, energy]
        self.discard = []
        self.supporter_played = False

    def draw(self, n=1):
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop())

    def has_basic_in_hand(self):
        return any(k == "Pokemon" and self.defs[n]["stage"] == "Basic" for k, n in self.hand)

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

    def in_play_names(self):
        names = [n for n, _, _ in self.bench]
        if self.active:
            names.append(self.active)
        return names

    def hand_names(self):
        return [n for k, n in self.hand if k == "Pokemon"]

    def pre_evolutions(self):
        return {n for n, info in self.defs.items() if info["evolves_from"] is None
                and any(o["evolves_from"] == n for o in self.defs.values())}


def opening_hand(player, log_prefix):
    while not player.has_basic_in_hand():
        if player.hand:
            player.deck.extend(player.hand)
            player.hand = []
            random.shuffle(player.deck)
        player.draw(7)
        if not player.has_basic_in_hand():
            print(f"  {log_prefix}: mulligan (no Basic Pokemon)")


def play_basics(p, log):
    if p.active is None:
        for name in p.load_priority:
            if ("Pokemon", name) in p.hand:
                p.remove_from_hand("Pokemon", name)
                p.active = name
                p.active_energy = 0
                log.append(f"[{p.name}] Play {name} as Active")
                break
    for kind, name in list(p.hand):
        if kind == "Pokemon" and p.defs[name]["stage"] == "Basic" and len(p.bench) < 5:
            p.remove_from_hand(kind, name)
            p.bench.append([name, 0, False])
            log.append(f"[{p.name}] Bench {name}")


def try_evolve(p, log):
    # Only one evolution per Pokemon per turn (without Rare Candy, which
    # evolves Basic -> Stage 2 directly as a single action elsewhere).
    for kind, name in list(p.hand):
        if kind != "Pokemon":
            continue
        target = p.defs[name]["evolves_from"]
        if target is None:
            continue
        if p.active == target and not p.active_evolved_this_turn:
            p.remove_from_hand(kind, name)
            p.active = name
            p.active_evolved_this_turn = True
            log.append(f"[{p.name}] Evolve {target} -> {name} (can't attack this turn)")
        else:
            slot = next((s for s in p.bench if s[0] == target and not s[2]), None)
            if slot is not None:
                p.remove_from_hand(kind, name)
                slot[0] = name
                slot[2] = True
                log.append(f"[{p.name}] Evolve {target} -> {name} (on Bench)")


def choose_search_target(p, allow_rule_box):
    in_play = p.in_play_names()
    in_hand = p.hand_names()
    for name in p.search_priority:
        if not allow_rule_box and p.defs[name]["rule_box"]:
            continue
        pre_evo = p.defs[name]["evolves_from"]
        if name in in_play or name in in_hand:
            continue
        if pre_evo is not None and pre_evo not in in_play:
            continue
        return name
    return None


def discard_value(p, card):
    kind, name = card
    if kind == "Energy":
        return 0 if sum(1 for k, n in p.hand if k == "Energy") > 2 else 2
    if kind == "Pokemon":
        count = sum(1 for k, n in p.hand if k == "Pokemon" and n == name)
        return 1 if (name in p.in_play_names() or count > 1) else 3
    if kind == "Item":
        return 2
    return 4


def play_generic_items(p, log):
    while ("Item", "Buddy-Buddy Poffin") in p.hand and len(p.bench) < 4:
        found, remaining = [], []
        for card in p.deck:
            if len(found) < 2 and card[0] == "Pokemon" and card[1] in p.buddy_eligible:
                found.append(card[1])
            else:
                remaining.append(card)
        if not found:
            break
        p.remove_from_hand("Item", "Buddy-Buddy Poffin")
        p.discard.append("Buddy-Buddy Poffin")
        p.deck = remaining
        random.shuffle(p.deck)
        for name in found:
            p.bench.append([name, 0, False])
        log.append(f"[{p.name}] Buddy-Buddy Poffin -> bench {', '.join(found)}")

    while ("Item", "Ultra Ball") in p.hand:
        target = choose_search_target(p, allow_rule_box=True)
        if target is None:
            break
        eligible = [c for c in p.hand if c != ("Item", "Ultra Ball")]
        if len(eligible) < 2:
            break
        discards = sorted(eligible, key=lambda c: discard_value(p, c))[:2]
        for c in discards:
            p.remove_from_hand(*c)
            p.discard.append(c[1])
        p.remove_from_hand("Item", "Ultra Ball")
        p.discard.append("Ultra Ball")
        p.deck.remove(("Pokemon", target))
        random.shuffle(p.deck)
        p.hand.append(("Pokemon", target))
        log.append(f"[{p.name}] Ultra Ball (discard {discards[0][1]}, {discards[1][1]}) -> search {target}")

    while ("Item", "Poke Pad") in p.hand:
        target = choose_search_target(p, allow_rule_box=False)
        if target is None:
            break
        p.remove_from_hand("Item", "Poke Pad")
        p.discard.append("Poke Pad")
        p.deck.remove(("Pokemon", target))
        random.shuffle(p.deck)
        p.hand.append(("Pokemon", target))
        log.append(f"[{p.name}] Poke Pad -> search {target}")

    # Rare Candy: Basic -> Stage 2 directly (opponent's Dreepy -> Dragapult ex)
    while ("Item", "Rare Candy") in p.hand:
        stage2 = None
        for kind, name in p.hand:
            if kind == "Pokemon" and p.defs[name]["stage"] == "Stage 2":
                mid = p.defs[name]["evolves_from"]
                basic = p.defs[mid]["evolves_from"] if mid in p.defs else None
                active_ok = p.active == basic and not p.active_evolved_this_turn
                bench_slot = next((s for s in p.bench if s[0] == basic and not s[2]), None)
                if active_ok or bench_slot is not None:
                    stage2 = (name, basic, active_ok, bench_slot)
                    break
        if stage2 is None:
            break
        name, basic, active_ok, bench_slot = stage2
        p.remove_from_hand("Item", "Rare Candy")
        p.discard.append("Rare Candy")
        p.remove_from_hand("Pokemon", name)
        if active_ok:
            p.active = name
            p.active_evolved_this_turn = True
        else:
            bench_slot[0] = name
            bench_slot[2] = True
        log.append(f"[{p.name}] Rare Candy: {basic} -> {name}")


def attach_energy(p, log):
    if ("Energy", "Energy") not in p.hand:
        return
    pre_evos = p.pre_evolutions()

    def need(name, attached):
        cost = min(a[1] for a in p.defs[name]["attacks"])
        return max(0, cost - attached)

    target = None
    if p.active and need(p.active, p.active_energy) > 0:
        target = "active"
    else:
        for slot in p.bench:
            if slot[0] in pre_evos:
                target = slot
                break
        if target is None:
            for slot in p.bench:
                if need(slot[0], slot[1]) > 0:
                    target = slot
                    break
    if target is None:
        log.append(f"[{p.name}] Hold Energy (no useful target)")
        return
    p.remove_from_hand("Energy", "Energy")
    if target == "active":
        p.active_energy += 1
        log.append(f"[{p.name}] Attach Energy to {p.active} (Active, now {p.active_energy})")
    else:
        target[1] += 1
        log.append(f"[{p.name}] Attach Energy to {target[0]} (Bench, now {target[1]})")


def try_attack(p, log, can_attack):
    if not p.active or p.active_evolved_this_turn or not can_attack:
        return
    best = None
    for atk_name, cost, dmg in p.defs[p.active]["attacks"]:
        if p.active_energy >= cost and (best is None or dmg > best[2]):
            best = (atk_name, cost, dmg)
    if best:
        log.append(f"[{p.name}] Attack: {p.active} uses {best[0]} for {best[2]} "
                   f"({p.active_energy} energy, needed {best[1]})")


def gust(attacker_name, defender, target_name, log):
    """Force target_name from defender's Bench into their Active spot,
    swapping whatever was previously Active onto the Bench."""
    slot = next((s for s in defender.bench if s[0] == target_name), None)
    if slot is None:
        return False
    old_active, old_energy = defender.active, defender.active_energy
    defender.bench.remove(slot)
    if old_active is not None:
        defender.bench.append([old_active, old_energy, defender.active_evolved_this_turn])
    defender.active, defender.active_energy = slot[0], slot[1]
    defender.active_evolved_this_turn = False
    log.append(f"[{attacker_name}] Boss's Orders forces {defender.name}'s "
               f"{target_name} into Active (was {old_active})")
    return True


def play_our_supporter(us, opp, log):
    if us.supporter_played:
        return
    opp_hand_size = len(opp.hand)

    # React to a large opponent hand: strip Items with Eri, or force a big
    # discard with Xerosic's Machinations if it's even bigger.
    if opp_hand_size > 7 and ("Supporter", "Xerosic's Machinations") in us.hand:
        us.remove_from_hand("Supporter", "Xerosic's Machinations")
        us.discard.append("Xerosic's Machinations")
        us.supporter_played = True
        log.append(f"[{us.name}] Play Xerosic's Machinations "
                   f"(opponent hand was {opp_hand_size} -> discard to 3)")
        return
    if opp_hand_size > 5 and ("Supporter", "Eri") in us.hand:
        us.remove_from_hand("Supporter", "Eri")
        us.discard.append("Eri")
        us.supporter_played = True
        log.append(f"[{us.name}] Play Eri (opponent hand was {opp_hand_size} > 5, strip Items)")
        return

    # React to an exposed low-HP threat on their bench worth gusting in with
    # Boss's Orders (only worth it if we could realistically knock it out).
    if ("Supporter", "Boss's Orders") in us.hand:
        weak_bench = [s for s in opp.bench if s[0] == "Fezandipiti ex"]
        if weak_bench and us.active in ("Espeon ex", "Jellicent ex"):
            us.remove_from_hand("Supporter", "Boss's Orders")
            us.discard.append("Boss's Orders")
            us.supporter_played = True
            gust(us.name, opp, "Fezandipiti ex", log)
            return

    if ("Supporter", "Lillie's Determination") in us.hand and len(us.hand) < 5:
        us.remove_from_hand("Supporter", "Lillie's Determination")
        us.discard.append("Lillie's Determination")
        us.draw(6)
        us.supporter_played = True
        log.append(f"[{us.name}] Play Lillie's Determination (draw 6)")
        return
    if ("Supporter", "Judge") in us.hand and len(us.hand) <= 1:
        us.remove_from_hand("Supporter", "Judge")
        us.discard.append("Judge")
        us.hand = []
        us.draw(4)
        us.supporter_played = True
        log.append(f"[{us.name}] Play Judge (draw 4)")


def play_opp_supporter(opp, us, log):
    if opp.supporter_played:
        return
    # Simple generic heuristic: draw when hand is thin, otherwise accelerate
    # energy with Crispin, otherwise gust with Boss's Orders if we have an
    # exposed low-retreat piece worth it. No reaction to our specific cards.
    if ("Supporter", "Lacey") in opp.hand and len(opp.hand) < 4:
        opp.remove_from_hand("Supporter", "Lacey")
        opp.discard.append("Lacey")
        opp.hand = []
        opp.draw(4)
        opp.supporter_played = True
        log.append(f"[{opp.name}] Play Lacey (draw 4)")
        return
    if ("Supporter", "Crispin") in opp.hand and ("Energy", "Energy") not in opp.hand:
        opp.remove_from_hand("Supporter", "Crispin")
        opp.discard.append("Crispin")
        opp.hand.append(("Energy", "Energy"))
        opp.supporter_played = True
        log.append(f"[{opp.name}] Play Crispin (fetch Energy)")
        return
    if ("Supporter", "Boss's Orders") in opp.hand and us.bench:
        # Target our lowest-HP benched Pokemon -- easiest to threaten next
        # turn. Never force Jellicent ex active: its item lock is passive,
        # so pulling it up would just turn our own lock on for us.
        candidates = [s for s in us.bench if s[0] != "Jellicent ex"]
        if not candidates:
            return
        target = min(candidates, key=lambda s: OUR_POKEMON[s[0]]["hp"])[0]
        opp.remove_from_hand("Supporter", "Boss's Orders")
        opp.discard.append("Boss's Orders")
        opp.supporter_played = True
        gust(opp.name, us, target, log)


def play_turn(p, other, log, turn_num, going_first, supporter_fn):
    if not (turn_num == 1 and going_first):
        p.draw(1)
        log.append(f"[{p.name}] Draw 1 card")
    p.supporter_played = False
    p.active_evolved_this_turn = False
    for slot in p.bench:
        slot[2] = False
    play_basics(p, log)
    try_evolve(p, log)
    play_generic_items(p, log)
    supporter_fn(p, other, log)
    attach_energy(p, log)
    try_evolve(p, log)
    can_attack = turn_num > 1 or not going_first
    try_attack(p, log, can_attack)
    bench_str = ", ".join(f"{n}({e})" for n, e, _ in p.bench)
    log.append(f"[{p.name}] State: Active={p.active}({p.active_energy}), "
               f"Bench=[{bench_str}], Hand={len(p.hand)}")


def main():
    random.seed()
    us = Player("US", OUR_POKEMON, OUR_DECKLIST, OUR_BUDDY_POFFIN_ELIGIBLE,
                OUR_LOAD_PRIORITY, OUR_SEARCH_PRIORITY)
    opp = Player("OPPONENT", OPP_POKEMON, OPP_DECKLIST, OPP_BUDDY_POFFIN_ELIGIBLE,
                 OPP_LOAD_PRIORITY, OPP_SEARCH_PRIORITY)

    us.draw(7)
    opening_hand(us, "US")
    opp.draw(7)
    opening_hand(opp, "OPPONENT")

    print("US opening hand:      ", sorted(n for _, n in us.hand))
    print("OPPONENT opening hand:", sorted(n for _, n in opp.hand))
    print()

    log = []
    for turn in (1, 2, 3):
        log.append(f"=== Round {turn} ===")
        log.append(f"--- {turn}: US turn (US goes first) ---")
        play_turn(us, opp, log, turn, going_first=True, supporter_fn=play_our_supporter)
        log.append(f"--- {turn}: OPPONENT turn ---")
        play_turn(opp, us, log, turn, going_first=False, supporter_fn=play_opp_supporter)

    print("\n".join(log))


if __name__ == "__main__":
    main()
