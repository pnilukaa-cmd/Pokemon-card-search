#!/usr/bin/env python3
"""Firing tests for the ability IR runtime.

ability_ir.py's own test suite proves that card text COMPILES to the right
IR. This file proves the separate, and previously untested, claim that the
compiled IR actually EXECUTES -- that activating an Ability really changes
game state in the expected direction.

That distinction is not academic. The first attempt to wire the runtime
into simulate_versus.py shipped a Player whose EFFECTS map was never
populated, so every Ability silently no-opped: the compiler was perfect,
coverage looked great, and not one Ability fired. Nothing in the existing
tests could catch that, because nothing tested execution.

Run:  python3 test_ability_engine.py
"""
import sys

sys.path.insert(0, ".")
import ability_ir as IR
import ability_engine as AE
import tcg_model as M


# --------------------------------------------------------------------------
# Minimal board doubles (same duck-typed shape the simulator uses)
# --------------------------------------------------------------------------

class Spot:
    def __init__(self, name, damage=0, energy=None):
        self.name = name
        self.damage = damage
        self.energy = list(energy or [])
        self.energy_names = ["X Energy"] * len(self.energy)
        self.entered_turn = 0
        self.evolved_this_turn = False
        self.tool = None

    def energy_count(self):
        return len(self.energy)


class FakePlayer:
    def __init__(self, name, POKEMON, EFFECTS, active=None, bench=None,
                 hand=None, deck=None, discard=None):
        self.name = name
        self.POKEMON = POKEMON
        self.EFFECTS = EFFECTS
        self.active = active
        self.bench = list(bench or [])
        self.hand = list(hand or [])
        self.deck = list(deck or [])
        self.discard = list(discard or [])
        self.prizes = 6
        self.lost_pokemon_last_turn = False
        self.played_supporters_this_turn = set()
        self.abilities_used = set()
        self.deck_out = False

    def draw(self, n=1):
        for _ in range(n):
            if not self.deck:
                self.deck_out = True
                return
            self.hand.append(self.deck.pop())

    def in_play(self):
        return ([self.active] if self.active else []) + self.bench

    def in_play_names(self):
        return [p.name for p in self.in_play()]


_CARDS = M.load_cards()
_BY_NAME, _BY_SETNUM = M.build_card_index(_CARDS)


def card_for(name, setnum=None):
    if setnum:
        c = _BY_SETNUM.get((name, setnum[0], setnum[1]))
        if c:
            return c
    return _BY_NAME[name][0]


def effects_for(name, setnum=None):
    c = card_for(name, setnum)
    return [e for e in IR.compile_card_abilities(c)]


def info_for(name, setnum=None):
    return M.build_pokemon_info(card_for(name, setnum))


def build(names, setnums=None):
    """POKEMON + EFFECTS maps for a set of card names."""
    setnums = setnums or {}
    POK, EFF = {}, {}
    for n in names:
        POK[n] = info_for(n, setnums.get(n))
        EFF[n] = effects_for(n, setnums.get(n))
    return POK, EFF


def find(effs, ability_name):
    for e in effs:
        if e.name == ability_name:
            return e
    raise AssertionError(f"ability {ability_name!r} not found")


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

FAILURES = []


def check(label, cond, detail=""):
    if cond:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}  {detail}")
        FAILURES.append(label)


def test_draw_fires():
    POK, EFF = build(["Toucannon"])
    p = FakePlayer("A", POK, EFF, active=Spot("Toucannon"),
                   deck=[("Pokemon", "Toucannon")] * 10)
    eff = find(EFF["Toucannon"], "Aerial Draw")
    ok = AE.activate(eff, p, p, p.active, [])
    check("Toucannon Aerial Draw draws 1", ok and len(p.hand) == 1,
          f"ok={ok} hand={len(p.hand)}")


def test_draw_with_discard_cost():
    POK, EFF = build(["N's Zoroark ex"])
    p = FakePlayer("A", POK, EFF, active=Spot("N's Zoroark ex"),
                   hand=[("Item", "Ultra Ball")],
                   deck=[("Pokemon", "N's Zorua")] * 10)
    eff = find(EFF["N's Zoroark ex"], "Trade")
    ok = AE.activate(eff, p, p, p.active, [])
    # discard 1 from hand, draw 2  ->  net +1
    check("N's Zoroark ex Trade is net +1 card", ok and len(p.hand) == 2,
          f"ok={ok} hand={len(p.hand)}")
    check("N's Zoroark ex Trade discarded the cost", len(p.discard) == 1,
          f"discard={p.discard}")


def test_cost_unaffordable_blocks():
    POK, EFF = build(["N's Zoroark ex"])
    p = FakePlayer("A", POK, EFF, active=Spot("N's Zoroark ex"),
                   hand=[], deck=[("Pokemon", "N's Zorua")] * 5)
    eff = find(EFF["N's Zoroark ex"], "Trade")
    ok = AE.activate(eff, p, p, p.active, [])
    check("Trade blocked with an empty hand (cost unpayable)", not ok, f"ok={ok}")


def test_active_only_condition():
    POK, EFF = build(["Mega Kangaskhan ex"])
    eff = find(EFF["Mega Kangaskhan ex"], "Run Errand")
    benched = Spot("Mega Kangaskhan ex")
    p = FakePlayer("A", POK, EFF, active=Spot("Mega Kangaskhan ex"),
                   bench=[benched], deck=[("Item", "Ultra Ball")] * 6)
    check("Run Errand fires from the Active Spot",
          AE.activate(eff, p, p, p.active, []) and len(p.hand) == 2)
    p2 = FakePlayer("A", POK, EFF, active=Spot("Toucannon") if False else None,
                    bench=[benched], deck=[("Item", "Ultra Ball")] * 6)
    check("Run Errand blocked from the Bench",
          not AE.activate(eff, p2, p2, benched, []))


def test_ko_condition():
    POK, EFF = build(["Fezandipiti ex"])
    eff = find(EFF["Fezandipiti ex"], "Flip the Script")
    p = FakePlayer("A", POK, EFF, active=Spot("Fezandipiti ex"),
                   deck=[("Item", "Ultra Ball")] * 6)
    check("Flip the Script blocked with no KO last turn",
          not AE.activate(eff, p, p, p.active, []))
    p.lost_pokemon_last_turn = True
    check("Flip the Script fires after a KO",
          AE.activate(eff, p, p, p.active, []) and len(p.hand) == 3,
          f"hand={len(p.hand)}")


def test_energy_type_condition_and_counter_move():
    POK, EFF = build(["Munkidori"])
    eff = find(EFF["Munkidori"], "Adrena-Brain")
    mine = Spot("Munkidori", damage=30, energy=[["Darkness"]])
    opp_spot = Spot("Munkidori", damage=0)
    me = FakePlayer("A", POK, EFF, active=mine)
    them = FakePlayer("B", POK, EFF, active=opp_spot)
    ok = AE.activate(eff, me, them, mine, [])
    check("Munkidori moves counters with Darkness attached",
          ok and mine.damage == 0 and opp_spot.damage == 30,
          f"ok={ok} mine={mine.damage} opp={opp_spot.damage}")

    bare = Spot("Munkidori", damage=30, energy=[])
    me2 = FakePlayer("A", POK, EFF, active=bare)
    check("Munkidori blocked without Darkness Energy",
          not AE.activate(eff, me2, them, bare, []))


def test_passive_damage_reduction():
    POK, EFF = build(["Steven's Carbink", "Steven's Metagross ex"])
    carbink = Spot("Steven's Carbink")
    metagross = Spot("Steven's Metagross ex")
    p = FakePlayer("A", POK, EFF, active=metagross, bench=[carbink])
    red = AE.query_damage_reduction(p, metagross)
    check("Steven's Carbink gives team -30", red == 30, f"got {red}")

    POK2, EFF2 = build(["Steven's Carbink", "Toucannon"])
    outsider = Spot("Toucannon")
    p2 = FakePlayer("A", POK2, EFF2, active=outsider,
                    bench=[Spot("Steven's Carbink")])
    red2 = AE.query_damage_reduction(p2, outsider)
    check("Carbink does NOT protect a non-Steven's Pokemon", red2 == 0, f"got {red2}")


def test_passive_damage_buff():
    POK, EFF = build(["Hop's Snorlax", "Hop's Wooloo"])
    snorlax = Spot("Hop's Snorlax")
    wooloo = Spot("Hop's Wooloo")
    p = FakePlayer("A", POK, EFF, active=wooloo, bench=[snorlax])
    buff = AE.query_damage_buff(p, wooloo)
    check("Hop's Snorlax gives team +30 from the Bench", buff == 30, f"got {buff}")


def test_retaliation():
    POK, EFF = build(["Mega Scrafty ex"])
    me = FakePlayer("A", POK, EFF, active=Spot("Mega Scrafty ex"))
    attacker = Spot("Mega Scrafty ex")
    them = FakePlayer("B", POK, EFF, active=attacker)
    back = AE.query_retaliation(me, attacker, them)
    check("Mega Scrafty ex retaliates 50", back == 50, f"got {back}")


def test_spiritomb_team_retaliation_type_gate():
    POK, EFF = build(["Spiritomb", "Scraggy", "Munkidori"],
                     setnums={"Spiritomb": ("MEG", "148")})
    attacker = Spot("Scraggy")
    them = FakePlayer("B", POK, EFF, active=attacker)

    dark_active = FakePlayer("A", POK, EFF, active=Spot("Scraggy"),
                             bench=[Spot("Spiritomb")])
    check("Spiritomb retaliates for a Darkness Active",
          AE.query_retaliation(dark_active, attacker, them) == 10,
          f"got {AE.query_retaliation(dark_active, attacker, them)}")

    psy_active = FakePlayer("A", POK, EFF, active=Spot("Munkidori"),
                            bench=[Spot("Spiritomb")])
    check("Spiritomb does NOT retaliate for a Psychic Active",
          AE.query_retaliation(psy_active, attacker, them) == 0,
          f"got {AE.query_retaliation(psy_active, attacker, them)}")


def test_search_to_hand():
    # Crobat has several printings with different Abilities; pin the one
    # that actually has Nighttime Maneuvers rather than taking [0].
    sn = None
    for c in _CARDS:
        if c["name"] == "Crobat" and any(
                a["name"] == "Nighttime Maneuvers" for a in c.get("abilities") or []):
            sn = (c["set"]["ptcgoCode"], c["number"])
            break
    POK, EFF = build(["Crobat"], setnums={"Crobat": sn})
    eff = find(EFF["Crobat"], "Nighttime Maneuvers")
    p = FakePlayer("A", POK, EFF, active=Spot("Crobat"),
                   deck=[("Item", "Ultra Ball"), ("Pokemon", "Zubat")])
    ok = AE.activate(eff, p, p, p.active, [])
    check("Crobat searches a card into hand", ok and len(p.hand) == 1,
          f"ok={ok} hand={p.hand}")


def test_shuffle_self_cost():
    POK, EFF = build(["Dudunsparce"])
    eff = find(EFF["Dudunsparce"], "Run Away Draw")
    dud = Spot("Dudunsparce")
    bench_mon = Spot("Dudunsparce")
    p = FakePlayer("A", POK, EFF, active=dud, bench=[bench_mon],
                   deck=[("Item", "Ultra Ball")] * 8)
    ok = AE.activate(eff, p, p, dud, [])
    check("Dudunsparce draws 3", ok and len(p.hand) == 3, f"hand={len(p.hand)}")
    check("Dudunsparce shuffles itself away and promotes",
          p.active is bench_mon, f"active={p.active.name if p.active else None}")


def main():
    print("Ability runtime firing tests\n")
    for fn in [test_draw_fires, test_draw_with_discard_cost,
               test_cost_unaffordable_blocks, test_active_only_condition,
               test_ko_condition, test_energy_type_condition_and_counter_move,
               test_passive_damage_reduction, test_passive_damage_buff,
               test_retaliation, test_spiritomb_team_retaliation_type_gate,
               test_search_to_hand, test_shuffle_self_cost]:
        print(f"{fn.__name__}:")
        try:
            fn()
        except Exception as exc:
            print(f"  ERROR {fn.__name__}: {exc!r}")
            FAILURES.append(fn.__name__)
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES: {FAILURES}")
        return 1
    print("All ability runtime firing tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
