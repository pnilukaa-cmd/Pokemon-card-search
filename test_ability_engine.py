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


def test_apply_condition():
    POK, EFF = build(["Shiinotic"])
    eff = find(EFF["Shiinotic"], "Calming Light")
    mine = Spot("Shiinotic")
    theirs = Spot("Shiinotic")
    theirs.conditions = set()
    me = FakePlayer("A", POK, EFF, active=mine)
    them = FakePlayer("B", POK, EFF, active=theirs)
    ok = AE.activate(eff, me, them, mine, [])
    check("Shiinotic makes the opponent's Active Asleep",
          ok and "asleep" in theirs.conditions, f"ok={ok} conds={theirs.conditions}")


def test_exclusive_conditions():
    """Asleep/Confused/Paralyzed replace each other; Burn/Poison stack."""
    import simulate_versus as V
    spot = V.InPlay("X", 0)
    spot.conditions = {"asleep", "poisoned"}
    # applying Confused must displace Asleep but leave Poisoned
    EXCL = {"asleep", "confused", "paralyzed"}
    spot.conditions -= EXCL
    spot.conditions.add("confused")
    check("Confused displaces Asleep but Poison remains",
          spot.conditions == {"confused", "poisoned"}, f"got {spot.conditions}")


def test_checkup_damage_and_clearing():
    import simulate_versus as V
    POK, EFF = build(["Toucannon"])
    a = Spot("Toucannon")
    p = FakePlayer("A", POK, EFF, active=a)
    o = FakePlayer("B", POK, EFF, active=Spot("Toucannon"))
    a.conditions = {"poisoned"}
    V.pokemon_checkup(p, o, [])
    check("Poison deals 10 at checkup", a.damage == 10, f"got {a.damage}")

    b = Spot("Toucannon")
    b.conditions = {"burned"}
    p2 = FakePlayer("A", POK, EFF, active=b)
    V.pokemon_checkup(p2, o, [])
    check("Burn deals 20 at checkup", b.damage == 20, f"got {b.damage}")

    c = Spot("Toucannon")
    c.conditions = {"paralyzed"}
    p3 = FakePlayer("A", POK, EFF, active=c)
    V.pokemon_checkup(p3, o, [])
    check("Paralysis clears after the turn", "paralyzed" not in c.conditions)


def test_conditions_clear_on_retreat_and_evolve():
    import simulate_versus as V
    spot = V.InPlay("Scraggy", 0)
    spot.conditions = {"poisoned", "asleep"}
    V.clear_conditions(spot, "retreated")
    check("Retreating clears every Special Condition", spot.conditions == set(),
          f"got {spot.conditions}")


def test_condition_blocks_attack():
    import simulate_versus as V
    POK, EFF = build(["Toucannon"])
    a = Spot("Toucannon")
    a.conditions = {"asleep"}
    p = FakePlayer("A", POK, EFF, active=a)
    check("Asleep blocks attacking", V.condition_blocks_attack(p, []))
    a.conditions = {"paralyzed"}
    check("Paralyzed blocks attacking", V.condition_blocks_attack(p, []))
    a.conditions = set()
    check("No condition does not block", not V.condition_blocks_attack(p, []))


def test_opponent_hand_reset():
    """Vivillon's Grand Wing must SET the opponent's hand to exactly 4 --
    not draw 4 for both players, which is what it compiled to before."""
    POK, EFF = build(["Vivillon"], {"Vivillon": ("POR", "9")})
    me = FakePlayer("A", POK, EFF, active=Spot("Vivillon"),
                    hand=[("Item", "Ultra Ball")] * 3)
    opp = FakePlayer("B", POK, EFF, active=Spot("Vivillon"),
                     hand=[("Item", "Ultra Ball")] * 7,
                     deck=[("Item", "Rare Candy")] * 20)
    eff = find(EFF["Vivillon"], "Grand Wing")
    log = []
    fired = AE.activate(eff, me, opp, me.active, log)
    check("Grand Wing fires", fired)
    check("opponent's hand is set to exactly 4", len(opp.hand) == 4,
          f"got {len(opp.hand)}")
    check("own hand is untouched", len(me.hand) == 3, f"got {len(me.hand)}")
    check("the discarded hand went to the bottom of the deck",
          len(opp.deck) == 20 + 7 - 4, f"got {len(opp.deck)}")

    # An opponent already hellbent has nothing to put down, so nothing
    # happens -- Grand Wing cannot turn a 0-card hand into a 4-card one.
    opp2 = FakePlayer("C", POK, EFF, active=Spot("Vivillon"), hand=[],
                      deck=[("Item", "Rare Candy")] * 20)
    check("empty opposing hand is left alone",
          not AE.activate(eff, me, opp2, me.active, []) and not opp2.hand)


def test_sniper_eye_cost_reduction_is_conditional():
    """Sniper's Eye may only discount the cost while the opponent holds
    exactly 4 cards. Compiled without its condition it read as a permanent
    discount, which silently overrated every deck built on it."""
    POK, EFF = build(["Decidueye ex"], {"Decidueye ex": ("POR", "100")})
    me = FakePlayer("A", POK, EFF, active=Spot("Decidueye ex", energy=[["Grass"]]))
    opp = FakePlayer("B", POK, EFF, active=Spot("Decidueye ex"))

    opp.hand = [("Item", "Ultra Ball")] * 4
    on = AE.query_ignored_cost_types(me, me.active, opp)
    check("Colorless is ignored at exactly 4 cards", on == {"Colorless"}, str(on))

    for n in (3, 5, 0):
        opp.hand = [("Item", "Ultra Ball")] * n
        off = AE.query_ignored_cost_types(me, me.active, opp)
        check(f"no discount at {n} cards", off == set(), str(off))


def test_fighting_roar_needs_an_ex_active():
    """Luxio may evolve the turn it is played only while the opponent's
    Active is a Pokemon ex. Compiled without that gate it read as a free
    turn of evolution speed in every matchup."""
    POK, EFF = build(["Luxio", "Luxray ex", "Shinx"],
                     {"Luxio": ("POR", "27")})
    me = FakePlayer("A", POK, EFF, active=Spot("Luxio"))
    opp = FakePlayer("B", POK, EFF, active=Spot("Luxray ex"))   # 310 HP ex
    check("Fighting Roar is on against an ex Active",
          AE.query_evolves_early(me, me.active, opp))
    opp.active = Spot("Shinx")                                   # 70 HP Basic
    check("Fighting Roar is off against a non-ex Active",
          not AE.query_evolves_early(me, me.active, opp))
    check("no opponent in view means off, not on",
          not AE.query_evolves_early(me, me.active, me))


def test_flower_curtain_skips_rule_box_pokemon():
    """Shaymin protects benched Pokemon that DON'T have a Rule Box. The
    clause was being dropped, so it shielded the benched ex too."""
    POK, EFF = build(["Shaymin", "Fezandipiti ex", "Shinx"],
                     {"Shaymin": ("DRI", "10")})
    plain, boxed = Spot("Shinx"), Spot("Fezandipiti ex")
    me = FakePlayer("A", POK, EFF, active=Spot("Shaymin"),
                    bench=[plain, boxed])
    opp = FakePlayer("B", POK, EFF, active=Spot("Shinx"))
    check("benched non-Rule-Box Pokemon is protected",
          AE.query_prevented(me, plain, opp))
    check("benched Pokemon ex is NOT protected",
          not AE.query_prevented(me, boxed, opp))


def test_retreat_tax_reaches_across_the_table():
    """Mega Chandelure ex's Binding Flame taxes the OPPONENT's Active. The
    retreat query only ever read the owner's own passives, so the tax --
    and every attack that prices itself off the resulting number -- scored
    as zero."""
    POK, EFF = build(["Mega Chandelure ex", "Litwick", "Ariados", "Latias ex"],
                     {"Mega Chandelure ex": ("PBL", "38"), "Ariados": ("TWM", "5")})
    defender_active = Spot("Litwick")                 # Basic, printed retreat 1
    me = FakePlayer("A", POK, EFF, active=defender_active)
    opp = FakePlayer("B", POK, EFF, active=Spot("Mega Chandelure ex"))
    check("one Binding Flame adds 1",
          AE.effective_retreat(me, defender_active, opp) == 2,
          str(AE.effective_retreat(me, defender_active, opp)))

    opp.bench = [Spot("Mega Chandelure ex")]          # Binding Flame stacks
    check("a benched second copy stacks to 2",
          AE.effective_retreat(me, defender_active, opp) == 3,
          str(AE.effective_retreat(me, defender_active, opp)))

    # Big Net taxes only an Active EVOLUTION Pokemon, so it misses a Basic.
    opp.bench.append(Spot("Ariados"))
    check("Big Net does not tax a Basic Active",
          AE.effective_retreat(me, defender_active, opp) == 3,
          str(AE.effective_retreat(me, defender_active, opp)))
    me.active = Spot("Ariados")                        # Stage 1 Active
    check("Big Net does tax an Evolution Active",
          AE.effective_retreat(me, me.active, opp) == 1 + 2 + 1,
          str(AE.effective_retreat(me, me.active, opp)))


def test_skyliner_frees_only_basics():
    """Latias ex's Skyliner reads 'your BASIC Pokemon'. The Basic clause was
    being dropped, which zeroed the Retreat Cost of Stage 2s too."""
    POK, EFF = build(["Latias ex", "Litwick", "Mega Chandelure ex"],
                     {"Mega Chandelure ex": ("PBL", "38")})
    basic, stage2 = Spot("Litwick"), Spot("Mega Chandelure ex")
    me = FakePlayer("A", POK, EFF, active=Spot("Latias ex"), bench=[basic, stage2])
    opp = FakePlayer("B", POK, EFF, active=Spot("Litwick"))
    check("a Basic retreats for free", AE.effective_retreat(me, basic, opp) == 0,
          str(AE.effective_retreat(me, basic, opp)))
    check("a Stage 2 keeps its printed cost",
          AE.effective_retreat(me, stage2, opp) == 2,
          str(AE.effective_retreat(me, stage2, opp)))


def test_alluring_light_draws_one_each():
    """Chandelure's Alluring Light draws each player exactly ONE card.
    Two overlapping compiler rules were both firing, doubling the rate of
    the engine a deck-out deck wins with."""
    POK, EFF = build(["Chandelure"], {"Chandelure": ("TWM", "38")})
    eff = find(EFF["Chandelure"], "Alluring Light")
    check("exactly one draw action compiles", len(eff.actions) == 1,
          str(eff.actions))
    me = FakePlayer("A", POK, EFF, active=Spot("Chandelure"),
                    deck=[("Item", "Ultra Ball")] * 20)
    opp = FakePlayer("B", POK, EFF, active=Spot("Chandelure"),
                     deck=[("Item", "Ultra Ball")] * 20)
    AE.activate(eff, me, opp, me.active, [])
    check("each player drew 1, not 2",
          len(me.hand) == 1 and len(opp.hand) == 1,
          f"me={len(me.hand)} opp={len(opp.hand)}")
    check("one card left each deck", len(me.deck) == 19 and len(opp.deck) == 19)


def test_victory_symbol_is_prize_gated():
    """N's Sigilyph's Victory Symbol is the format's only outright win
    condition, and it is live at exactly 1 Prize remaining -- not 2, and
    not 0."""
    POK, EFF = build(["N's Sigilyph"], {"N's Sigilyph": ("JTG", "64")})
    card = card_for("N's Sigilyph", ("JTG", "64"))
    atk = next(a for a in card["attacks"] if a["name"] == "Victory Symbol")
    eff = IR.compile_effect("N's Sigilyph", atk["name"], atk["text"])
    check("Victory Symbol compiles to a win", 
          any(a.op == IR.Op.WIN_GAME for a in eff.actions), str(eff.actions))
    me = FakePlayer("A", POK, EFF, active=Spot("N's Sigilyph"))
    opp = FakePlayer("B", POK, EFF, active=Spot("N's Sigilyph"))
    for prizes, want in ((1, True), (2, False), (0, False), (6, False)):
        me.prizes = prizes
        got = AE.conditions_met(eff, me, opp, me.active)
        check(f"live at {prizes} Prize(s): {want}", got == want)


def main():
    print("Ability runtime firing tests\n")
    for fn in [test_draw_fires, test_draw_with_discard_cost,
               test_cost_unaffordable_blocks, test_active_only_condition,
               test_ko_condition, test_energy_type_condition_and_counter_move,
               test_passive_damage_reduction, test_passive_damage_buff,
               test_retaliation, test_spiritomb_team_retaliation_type_gate,
               test_search_to_hand, test_shuffle_self_cost,
               test_apply_condition, test_exclusive_conditions,
               test_checkup_damage_and_clearing,
               test_conditions_clear_on_retreat_and_evolve,
               test_condition_blocks_attack,
               test_opponent_hand_reset,
               test_sniper_eye_cost_reduction_is_conditional,
               test_fighting_roar_needs_an_ex_active,
               test_flower_curtain_skips_rule_box_pokemon,
               test_retreat_tax_reaches_across_the_table,
               test_skyliner_frees_only_basics,
               test_alluring_light_draws_one_each,
               test_victory_symbol_is_prize_gated]:
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
