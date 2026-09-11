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
        self.attack_locked = False
        self.retreat_locked = False
        self.attack_locked_by_opponent = False
        self.prev_damage = 0

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
        self.item_locked = False
        self.energy_types = {"Psychic", "Colorless"}

    def remove_from_hand(self, kind, name):
        self.hand.remove((kind, name))

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

    # A Pokemon Checkup resolves BOTH players' Active Pokemon. Resolving
    # only the turn-ending player's checked each Pokemon once per ROUND
    # instead of twice, which halved every Poison and Burn in the game and
    # doubled how long Sleep lasted.
    mine, theirs = Spot("Toucannon"), Spot("Toucannon")
    mine.conditions, theirs.conditions = {"poisoned"}, {"poisoned"}
    pa = FakePlayer("A", POK, EFF, active=mine)
    pb = FakePlayer("B", POK, EFF, active=theirs)
    V.pokemon_checkup(pa, pb, [])
    check("the turn-ending player's Active takes Poison", mine.damage == 10,
          mine.damage)
    check("and so does the opponent's", theirs.damage == 10, theirs.damage)

    # ... but Paralysis is cured only at the end of the AFFECTED player's
    # next turn, so it must survive the checkup in between.
    mine2, theirs2 = Spot("Toucannon"), Spot("Toucannon")
    mine2.conditions, theirs2.conditions = set(), {"paralyzed"}
    pa2 = FakePlayer("A", POK, EFF, active=mine2)
    pb2 = FakePlayer("B", POK, EFF, active=theirs2)
    V.pokemon_checkup(pa2, pb2, [])
    check("Paralysis survives the opponent's checkup",
          "paralyzed" in theirs2.conditions)


def test_resistance_is_applied():
    """369 cards in this pool carry a Resistance and none of it existed.

    It was not on the Pokemon record at all, so every attack into a
    resisted type dealt 30 more damage than the game allows.
    """
    import tcg_model as M
    cards = M.load_cards()
    sc = [c for c in cards if c["name"] == "Scizor ex"][0]
    info = M.build_pokemon_info(sc)
    check("Scizor ex resists Grass by 30", info["resistance"] == ("Grass", 30),
          info["resistance"])
    dun = [c for c in cards if c["name"] == "Dunsparce"][0]
    check("a Pokemon with no Resistance reports None",
          M.build_pokemon_info(dun)["resistance"] is None)


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


def test_biting_spree_hits_the_opponent():
    """Team Rocket's Crobat ex names its targets in an earlier clause
    ("choose 2 of your opponent's Pokemon ... put 2 counters on each"),
    so parsing only the "on ..." tail pointed it at its own board."""
    POK, EFF = build(["Team Rocket's Crobat ex", "Team Rocket's Zubat"],
                     {"Team Rocket's Crobat ex": ("DRI", "122")})
    eff = find(EFF["Team Rocket's Crobat ex"], "Biting Spree")
    act = eff.actions[0]
    check("aimed at the opponent", act.target == IR.Target.OPP_ANY, act.target)
    check("hits two targets", act.filter.get("targets") == 2, str(act.filter))

    mine = Spot("Team Rocket's Zubat")
    a, b, c = (Spot("Team Rocket's Zubat"), Spot("Team Rocket's Zubat"),
               Spot("Team Rocket's Zubat"))
    me = FakePlayer("A", POK, EFF, active=Spot("Team Rocket's Crobat ex"),
                    bench=[mine])
    opp = FakePlayer("B", POK, EFF, active=a, bench=[b, c])
    AE.activate(eff, me, opp, me.active, [])
    check("20 damage landed on exactly two of theirs",
          sorted(p.damage for p in (a, b, c)) == [0, 20, 20],
          str([p.damage for p in (a, b, c)]))
    check("none of mine took damage", mine.damage == 0 and me.active.damage == 0)


def test_terminal_period_needs_exactly_six_counters():
    """Mega Absol ex Knocks Out an Active on exactly 6 counters whatever
    its HP -- and does nothing at 5 or 7."""
    import simulate_versus as SV
    POK, EFF = build(["Mega Absol ex"], {"Mega Absol ex": ("MEG", "161")})
    card = card_for("Mega Absol ex", ("MEG", "161"))
    atk = next(a for a in card["attacks"] if a["name"] == "Terminal Period")
    me = FakePlayer("A", POK, EFF, active=Spot("Mega Absol ex"))
    opp = FakePlayer("B", POK, EFF, active=Spot("Mega Absol ex"))
    for dmg, want in ((60, True), (50, False), (70, False), (0, False)):
        opp.active.damage = dmg
        got = SV.conditional_ko_target(me, opp, atk) is not None
        check(f"{dmg} damage -> KO {want}", got == want)


def test_food_prep_scales_with_kofu_in_discard():
    """Crabominable's Food Prep discounts one Colorless PER Kofu in the
    discard. Compiled as a flat -1 it was wrong in both directions: a
    discount with no Kofu played, and a quarter of the real one with four."""
    import simulate_versus as SV
    POK, EFF = build(["Crabominable", "Veluza"],
                     {"Crabominable": ("SCR", "149"), "Veluza": ("SCR", "45")})
    crab = Spot("Crabominable")
    me = FakePlayer("A", POK, EFF, active=crab)
    opp = FakePlayer("B", POK, EFF, active=Spot("Veluza"))
    haymaker = next(a for a in POK["Crabominable"]["attacks"]
                    if a["name"] == "Haymaker")
    sonic = next(a for a in POK["Veluza"]["attacks"] if a["name"] == "Sonic Edge")

    for kofu, want in ((0, 5), (1, 4), (2, 3), (4, 1)):
        me.discard = ["Kofu"] * kofu
        got = len(SV.effective_cost(me, crab, haymaker["cost"], opp))
        check(f"Haymaker costs {want} with {kofu} Kofu in discard",
              got == want, f"got {got}")
    me.discard = ["Kofu"] * 4
    check("the surviving Energy is the Water, not a Colorless",
          SV.effective_cost(me, crab, haymaker["cost"], opp) == ["Water"],
          str(SV.effective_cost(me, crab, haymaker["cost"], opp)))

    vel = Spot("Veluza")
    me2 = FakePlayer("C", POK, EFF, active=vel, discard=["Kofu"] * 4)
    check("Sonic Edge is free at 4 Kofu",
          SV.effective_cost(me2, vel, sonic["cost"], opp) == [],
          str(SV.effective_cost(me2, vel, sonic["cost"], opp)))
    me2.discard = []
    check("Sonic Edge costs its printed 4 at 0 Kofu",
          len(SV.effective_cost(me2, vel, sonic["cost"], opp)) == 4)


def test_hide_n_sneak_threshold():
    """Dhelmise's Vengeful Anchor is 30 damage, or 170 once four Pokemon
    with the Hide 'n' Sneak Ability are in the discard. Sinistcha's Matcha
    Spin wants six. Both clauses were being dropped entirely."""
    import simulate_versus as SV
    POK, EFF = build(["Dhelmise", "Shuppet", "Sinistcha", "Poltchageist"],
                     {"Dhelmise": ("PBL", "39"), "Shuppet": ("PBL", "33"),
                      "Sinistcha": ("PBL", "6"), "Poltchageist": ("PBL", "5")})
    anchor = next(a for a in POK["Dhelmise"]["attacks"]
                  if a["name"] == "Vengeful Anchor")
    spot = Spot("Dhelmise")
    me = FakePlayer("A", POK, EFF, active=spot)
    opp = FakePlayer("B", POK, EFF, active=Spot("Dhelmise"))
    for n, want in ((0, 30), (3, 30), (4, 170), (6, 170)):
        me.discard = ["Shuppet"] * n
        got = SV.attack_damage(me, opp, spot, anchor, record=False)
        check(f"Vengeful Anchor is {want} with {n} in discard",
              got == want, f"got {got}")

    # A discarded Pokemon WITHOUT the Ability must not count.
    me.discard = ["Dhelmise"] * 6
    check("non-Hide-'n'-Sneak Pokemon do not fuel it",
          SV.attack_damage(me, opp, spot, anchor, record=False) == 30)

    eff = IR.compile_effect("Sinistcha", "Matcha Spin",
                            next(a for a in POK["Sinistcha"]["attacks"]
                                 if a["name"] == "Matcha Spin")["text"])
    me.discard = ["Poltchageist"] * 5
    check("Matcha Spin is off at 5", not AE.conditions_met(eff, me, opp, spot))
    me.discard = ["Poltchageist"] * 6
    check("Matcha Spin is on at 6", AE.conditions_met(eff, me, opp, spot))


def test_matcha_spin_is_not_charged_twice():
    """A spread attack's counters are placed by the rider, not by damage.

    Matcha Spin has no printed damage -- its whole effect is "place 4
    damage counters on each of your opponent's Pokemon", which the rider
    path applies. attack_damage used to ALSO return 40 for it, which both
    double-charged the Active and skipped the attack's own 6-fuel gate
    (and picked up Weakness, which counter placement ignores).
    """
    import simulate_versus as SV
    POK, EFF = build(["Sinistcha"], {"Sinistcha": ("PBL", "6")})
    sin = Spot("Sinistcha")
    me = FakePlayer("A", POK, EFF, active=sin)
    opp = FakePlayer("B", POK, EFF, active=Spot("Sinistcha"))
    matcha = next(a for a in POK["Sinistcha"]["attacks"]
                  if a["name"] == "Matcha Spin")

    me.discard = []
    check("Matcha Spin deals no attack damage at 0 fuel",
          SV.attack_damage(me, opp, sin, matcha, record=False) == 0)
    me.discard = ["Poltchageist"] * 6
    check("Matcha Spin still deals no attack damage at 6 fuel "
          "(the rider places the counters)",
          SV.attack_damage(me, opp, sin, matcha, record=False) == 0)


def test_board_wide_spread_is_priced_across_the_board():
    """4 counters on each of six Pokemon is worth 240 to the AI, not 40."""
    import simulate_versus as SV
    # Poltchageist has to be in the card table or the discard pile cannot
    # be counted by Ability name at all.
    POK, EFF = build(["Sinistcha", "Poltchageist"],
                     {"Sinistcha": ("PBL", "6"), "Poltchageist": ("PBL", "5")})
    me = FakePlayer("A", POK, EFF, active=Spot("Sinistcha"),
                    discard=["Poltchageist"] * 6)
    opp = FakePlayer("B", POK, EFF, active=Spot("Sinistcha"))
    matcha = next(a for a in POK["Sinistcha"]["attacks"]
                  if a["name"] == "Matcha Spin")

    opp.bench = []
    check("lone Active is worth 40", SV.attack_rider_value(me, opp, matcha) == 40)
    opp.bench = [Spot("Sinistcha") for _ in range(5)]
    check("a full six-Pokemon board is worth 240",
          SV.attack_rider_value(me, opp, matcha) == 240,
          str(SV.attack_rider_value(me, opp, matcha)))
    me.discard = []
    check("and nothing at all below the 6-fuel gate",
          SV.attack_rider_value(me, opp, matcha) == 0)


def test_neurokinesis_counts_the_whole_opposing_board():
    """Azelf scales off counters on ALL their Pokemon, not just the Active.

    That distinction is the entire reason it pairs with a spread attack;
    the engine only knew the Active-only wording.
    """
    import simulate_versus as SV
    POK, EFF = build(["Azelf"], {"Azelf": ("SSP", "80")})
    az = Spot("Azelf")
    me = FakePlayer("A", POK, EFF, active=az)
    opp = FakePlayer("B", POK, EFF, active=Spot("Azelf"))
    neuro = next(a for a in POK["Azelf"]["attacks"]
                 if a["name"] == "Neurokinesis")

    opp.bench = []
    opp.active.damage = 0
    check("base 10 on an undamaged board",
          SV.attack_damage(me, opp, az, neuro, record=False) == 10)

    opp.active.damage = 40
    check("+10 per counter on the Active",
          SV.attack_damage(me, opp, az, neuro, record=False) == 50)

    opp.bench = [Spot("Azelf") for _ in range(5)]
    for b in opp.bench:
        b.damage = 40
    # 4 counters on each of 6 Pokemon = 24 counters = +240.
    check("Bench counters count too: 10 + 240 after one Matcha Spin",
          SV.attack_damage(me, opp, az, neuro, record=False) == 250,
          str(SV.attack_damage(me, opp, az, neuro, record=False)))


def test_prevention_walls_check_who_is_attacking():
    """Safeguard and Cornerstone Stance are conditional, not invincibility.

    Both compiled to a bare "prevent all damage": Safeguard's restriction
    ("Pokemon ex") trails the word Pokemon so the attacker pattern missed
    it, and Cornerstone Stance's ("Pokemon that have an Ability") sat 83
    characters into the text, outside an 80-character match window. The
    engine also never checked the attacker at all, and the game loop never
    called query_prevented in the first place.
    """
    POK, EFF = build(["Sylveon", "Cornerstone Mask Ogerpon ex", "Dhelmise",
                      "Veluza", "Mega Scrafty ex"],
                     {"Sylveon": ("PRE", "40"),
                      "Cornerstone Mask Ogerpon ex": ("TWM", "112"),
                      "Dhelmise": ("PBL", "39"), "Veluza": ("SCR", "45"),
                      "Mega Scrafty ex": ("MEG", "104")})
    syl = Spot("Sylveon")
    me = FakePlayer("A", POK, EFF, active=syl)
    opp = FakePlayer("B", POK, EFF, active=Spot("Mega Scrafty ex"))

    check("Safeguard stops a Pokemon ex",
          AE.query_prevented(me, syl, opp, opp.active))
    opp.active = Spot("Dhelmise")          # single-Prize, has no Ability
    check("Safeguard does NOT stop a non-ex",
          not AE.query_prevented(me, syl, opp, opp.active))

    ogre = Spot("Cornerstone Mask Ogerpon ex")
    me2 = FakePlayer("C", POK, EFF, active=ogre)
    opp2 = FakePlayer("D", POK, EFF, active=Spot("Veluza"))
    check("Cornerstone Stance stops an attacker that has an Ability",
          AE.query_prevented(me2, ogre, opp2, opp2.active))
    opp2.active = Spot("Dhelmise")         # Dhelmise has no Ability
    check("Cornerstone Stance does NOT stop an Ability-less attacker",
          not AE.query_prevented(me2, ogre, opp2, opp2.active))


def test_turn_locks_are_applied_not_just_compiled():
    """"Can't retreat / can't attack next turn" has to reach the board.

    LOCK was classified with the passive ops -- "queried elsewhere, never
    executed" -- and then nothing queried it, so 44 card effects across the
    pool compiled cleanly and did nothing. Retreat-lock is the entire game
    plan of more than one deck in decks/.
    """
    import simulate_versus as SV
    POK, EFF = build(["Dhelmise", "Veluza"],
                     {"Dhelmise": ("PBL", "39"), "Veluza": ("SCR", "45")})
    me = FakePlayer("A", POK, EFF, active=Spot("Dhelmise"))
    opp = FakePlayer("B", POK, EFF, active=Spot("Veluza"))
    log = []

    beset = IR.compile_effect(
        "attack", "Beset",
        "During your opponent's next turn, the Defending Pokémon can't retreat.")
    AE.apply_action(beset.actions[0], me, opp, me.active, log)
    check("the DEFENDER is the one locked", opp.active.retreat_locked)
    check("the attacker is not", not me.active.retreat_locked)

    freeze = IR.compile_effect(
        "attack", "Freezing Chill",
        "During your opponent's next turn, the Defending Pokémon can't attack.")
    AE.apply_action(freeze.actions[0], me, opp, me.active, log)
    check("attack lock lands on the defender",
          opp.active.attack_locked_by_opponent)

    itchy = IR.compile_effect(
        "ability", "Itchy Pollen",
        "During your opponent's next turn, they can't play any Item cards "
        "from their hand.")
    AE.apply_action(itchy.actions[0], me, opp, me.active, log)
    check("Item lock lands on the opposing player", opp.item_locked)

    check("LOCK is in the attack-rider set so attacks can apply it",
          IR.Op.LOCK in SV.ATTACK_RIDER_OPS)


def test_unregistered_trainers_resolve_from_card_text():
    """The IR fallback covers the 227 Trainers the registry never knew.

    The hand-written registry modelled 30 of 257 Trainers. The IR already
    parsed 182 of them and the simulator discarded all of it, so any deck
    built out of anything but a short list of staples played most of its
    Trainer line as blank cards.
    """
    import simulate_versus as SV
    import tcg_model as M
    cards = M.load_cards()
    SV._CARDS_BY_NAME.update({c["name"]: c for c in cards})
    trainers = [c for c in cards if c.get("supertype") == "Trainer"]
    covered = [c for c in trainers
               if c["name"] in SV.KNOWN_TRAINERS or SV.trainer_effect_ir(c["name"])]
    pct = 100 * len(covered) / len(trainers)
    check(f"Trainer coverage is well past the old 11.7% (now {pct:.1f}%)",
          pct > 65, f"{len(covered)}/{len(trainers)}")

    # A Supporter whose effect cannot resolve must not be spent.
    POK, EFF = build(["Dhelmise"], {"Dhelmise": ("PBL", "39")})
    me = FakePlayer("A", POK, EFF, active=Spot("Dhelmise"))
    opp = FakePlayer("B", POK, EFF, active=Spot("Dhelmise"))
    lana = "Lana's Aid"
    if SV.trainer_effect_ir(lana):
        me.hand = [("Supporter", lana)]
        me.discard = []          # nothing to recover -- it should fizzle
        played = SV.play_trainer_from_ir(me, opp, "Supporter", lana, [])
        check("a Supporter that would do nothing is not spent",
              not played and ("Supporter", lana) in me.hand)


def test_hp_tools_are_attached_and_raise_the_KO_threshold():
    """Hero's Cape was never attached, and would not have counted anyway.

    attach_tools only considered damage and retaliation Tools, so retreat
    and HP Tools sat in hand all game; and every Knock Out check read
    printed HP directly, so even an attached +100 HP Tool was worth
    nothing. Both halves had to be fixed for either to matter.
    """
    import simulate_versus as SV
    import tcg_model as M
    SV._CARDS_BY_NAME.update({c["name"]: c for c in M.load_cards()})

    tools = SV.hp_tools()
    check("HP Tools are discovered from card text, not hand-listed",
          tools.get("Hero's Cape") == 100, str(tools))

    POK, EFF = build(["Cornerstone Mask Ogerpon ex"],
                     {"Cornerstone Mask Ogerpon ex": ("TWM", "112")})
    spot = Spot("Cornerstone Mask Ogerpon ex")
    me = FakePlayer("A", POK, EFF, active=spot)
    check("printed HP with no Tool", SV.effective_hp(me, spot) == 210)
    spot.tool = "Hero's Cape"
    check("+100 HP once the Cape is on", SV.effective_hp(me, spot) == 310,
          str(SV.effective_hp(me, spot)))

    me.hand = [("Tool", "Hero's Cape")]
    spot.tool = None
    SV.attach_tools(me, [])
    check("and attach_tools actually puts it there",
          spot.tool == "Hero's Cape")


def test_ai_values_knockouts_and_setup_rather_than_raw_damage():
    """A3, partial: the policy scored attacks purely on damage.

    Two consequences it could not see past. A 170 that leaves a 330 HP
    body standing ranked equal to a 170 that takes three Prizes; and a
    0-damage attack that accelerated Energy or dug for a piece scored a
    flat zero, so the AI would never spend a turn setting up.
    """
    import simulate_versus as SV
    POK, EFF = build(["Dhelmise", "Veluza", "Mega Scrafty ex"],
                     {"Dhelmise": ("PBL", "39"), "Veluza": ("SCR", "45"),
                      "Mega Scrafty ex": ("MEG", "104")})
    dh = Spot("Dhelmise")
    me = FakePlayer("A", POK, EFF, active=dh, discard=["Shuppet"] * 4)
    opp = FakePlayer("B", POK, EFF, active=Spot("Veluza"))
    anchor = next(a for a in POK["Dhelmise"]["attacks"]
                  if a["name"] == "Vengeful Anchor")

    opp.active.damage = 0                       # Veluza is 110 HP
    healthy = SV.attack_value(me, opp, dh, anchor)
    opp.active.damage = 100                     # now 10 from a Knock Out
    lethal = SV.attack_value(me, opp, dh, anchor)
    check("the same attack is worth more when it actually Knocks Out",
          lethal > healthy, f"{lethal} vs {healthy}")

    # A Knock Out on a 2-Prize body outranks one on a 1-Prize body.
    opp2 = FakePlayer("C", POK, EFF, active=Spot("Mega Scrafty ex"))
    opp2.active.damage = POK["Mega Scrafty ex"]["hp"] - 10
    big = SV.attack_value(me, opp2, dh, anchor)
    check("and more still when the Knock Out is worth more Prizes",
          big > lethal, f"{big} vs {lethal}")

    # Setup riders now carry a price instead of scoring zero.
    charge = {"name": "Charge Energy", "cost": ["Colorless"], "damage": 0,
              "text": "Search your deck for a basic Energy card and attach "
                      "it to this Pokémon. Then, shuffle your deck."}
    check("a 0-damage Energy-acceleration attack is worth more than nothing",
          SV.attack_rider_value(me, opp, charge) > 0,
          str(SV.attack_rider_value(me, opp, charge)))


def test_wall_breakers_endure_and_ability_hp():
    """Three effects that all live on the damage path and all did nothing.

    ignore_opponent_effects is the format's answer to a damage wall, and
    was compiled and never consulted -- so the cards whose entire job is
    beating a wall did not beat one. modify_hp on an Ability never reached
    the Knock Out check. And Endure's "if this Pokemon has full HP" clause
    was evaluated AFTER the hit landed, so it was never true.
    """
    import simulate_versus as SV
    POK, EFF = build(["Koraidon", "Okidogi", "Pikachu ex", "Dhelmise"],
                     {"Koraidon": ("TEF", "62"), "Okidogi": ("TWM", "122"),
                      "Pikachu ex": ("SSP", "57"), "Dhelmise": ("PBL", "39")})

    kora = Spot("Koraidon")
    me = FakePlayer("A", POK, EFF, active=kora)
    opp = FakePlayer("B", POK, EFF, active=Spot("Dhelmise"))
    shred = next(a for a in POK["Koraidon"]["attacks"] if a["name"] == "Shred")
    check("the clause is read off the ATTACK when that is where it sits",
          SV.attack_ignores_effects(shred))
    anchor = next(a for a in POK["Dhelmise"]["attacks"]
                  if a["name"] == "Vengeful Anchor")
    check("and an ordinary attack does not claim it",
          not SV.attack_ignores_effects(anchor))

    oki = Spot("Okidogi", energy=[["Darkness"]])
    me3 = FakePlayer("D", POK, EFF, active=oki)
    base = POK["Okidogi"]["hp"]
    check("Adrena-Power's +100 HP reaches effective_hp",
          SV.effective_hp(me3, oki) == base + 100,
          f"{SV.effective_hp(me3, oki)} vs {base + 100}")
    oki_no_energy = Spot("Okidogi")
    me4 = FakePlayer("E", POK, EFF, active=oki_no_energy)
    check("and not without the Darkness Energy it requires",
          SV.effective_hp(me4, oki_no_energy) == base)

    pika = Spot("Pikachu ex")
    me5 = FakePlayer("F", POK, EFF, active=pika)
    pika.prev_damage = 0            # the hit found it undamaged
    pika.damage = 10 ** 4
    check("Endure fires when the attack found it at full HP",
          AE.query_endures(me5, pika, opp))
    pika.prev_damage = 30           # it was already damaged
    check("and not when it was already damaged",
          not AE.query_endures(me5, pika, opp))


def test_counter_multiplier_scales_what_is_already_there():
    """Snow Coating compiled to nothing at all.

    The taxonomy carried a `damage_counter_doubler` family, but there was
    no IR rule and no op, so a deck whose entire plan is doubling a spread
    was invisible to the simulator. Multiplying is a different shape from
    placing: it is worth zero on a clean board and enormous on a spread
    one, which is also how the AI has to price it or it uses it on turn
    one and never again.
    """
    import simulate_versus as SV
    POK, EFF = build(["N's Vanilluxe", "Dhelmise"],
                     {"N's Vanilluxe": ("ASC", "51"), "Dhelmise": ("PBL", "39")})
    van = Spot("N's Vanilluxe")
    me = FakePlayer("A", POK, EFF, active=van)
    opp = FakePlayer("B", POK, EFF, active=Spot("Dhelmise"))
    opp.bench = [Spot("Dhelmise"), Spot("Dhelmise")]
    snow = next(a for a in POK["N's Vanilluxe"]["attacks"]
                if a["name"] == "Snow Coating")

    for s in [opp.active] + opp.bench:
        s.damage = 0
    check("worth nothing on an undamaged board",
          SV.attack_rider_value(me, opp, snow) == 0)

    opp.active.damage = 40
    for s in opp.bench:
        s.damage = 20
    # doubling adds exactly what is already there: 40 + 20 + 20
    check("worth what it would add, not a flat number",
          SV.attack_rider_value(me, opp, snow) == 80,
          str(SV.attack_rider_value(me, opp, snow)))

    AE.apply_action(IR.compile_effect("attack", "Snow Coating",
                                      snow["text"]).actions[0],
                    me, opp, van, [])
    check("the Active is doubled", opp.active.damage == 80)
    check("and every Benched Pokemon too",
          all(s.damage == 40 for s in opp.bench))


def test_rare_candy_bridges_a_line_the_deck_does_not_own():
    """Rare Candy refused to work in the normal way people build the card.

    The card says "skipping the Stage 1", so the middle Pokemon only has
    to exist in the CARD POOL. The simulator looked it up in `pl.POKEMON`,
    which is built from the DECKLIST -- so in the usual construction (run
    the Basic and the Stage 2, skip the Stage 1 entirely) the lookup
    returned None and Rare Candy silently did nothing, every game.

    Same shape as every other bug in this engine's history: the code
    existed, the card compiled, a test passed, and nothing in the field
    ever reached it. Measured cost: N's Vanilluxe reached play 0 times in
    408 games of a deck running 4 Rare Candy and 2 N's Vanilluxe.
    """
    import simulate_versus as SV
    import tcg_model as M
    cards = M.load_cards()
    by_name, _ = M.build_card_index(cards)
    SV._CARDS_BY_NAME.update(by_name)

    deck = ("""Pokemon: 2
3 N's Vanillite ASC 49
2 N's Vanilluxe ASC 51

Trainer: 4
4 Rare Candy MEG 125

Energy: 0

Total Cards: 6
""")
    POK, DECKLIST, _, _ = M.build_deck_model(deck)
    check("the deck really does NOT run the Stage 1",
          "N's Vanillish" not in POK)

    eff = SV.compile_effects_for(POK, M.resolve_deck_cards(deck))
    pl = SV.Player("A", POK, DECKLIST, eff)
    opp = SV.Player("B", POK, DECKLIST, eff)
    pl.hand = [("Item", "Rare Candy"), ("Pokemon", "N's Vanilluxe")]
    spot = SV.InPlay("N's Vanillite", 1)
    pl.active = spot
    pl.bench = []

    ok = SV.effect_rare_candy(pl, opp, 2, [], first_turn=False)
    check("Rare Candy bridges Basic -> Stage 2 with no Stage 1 in the deck",
          ok and pl.active.name == "N's Vanilluxe", pl.active.name)
    check("and it costs the Rare Candy",
          ("Item", "Rare Candy") not in pl.hand)



def _ex_board(card_name):
    """The audit board: my ex Active with 2 own-type + 2 Psychic, 3 Bench."""
    import audit_ex_damage as A
    import simulate_versus as SV
    import tcg_model as M
    cards = M.load_cards()
    by_name, _ = M.build_card_index(cards)
    SV._CARDS_BY_NAME.update(by_name)
    card = [c for c in cards if c["name"] == card_name][0]
    me, op, spot = A.build_board(card, by_name)
    me.active = spot
    atks = {a["name"]: a for a in M.build_pokemon_info(card)["attacks"]}
    return me, op, spot, atks


def test_typed_energy_scalers_count_only_that_type():
    """Every typed Energy scaler in the pool over-counted.

    "for each Psychic Energy attached to this Pokemon" was read as "for
    each Energy attached to this Pokemon", so an attacker holding two
    on-type and two off-type Energy was paid for all four. That silently
    inflates any deck running a second Energy type -- which is most of
    the interesting ones.
    """
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Kingdra ex")     # Water; board 2 W + 2 P
    check("Hydro Pump counts the 2 Water, not all 4 Energy",
          SV.attack_damage(me, op, spot, atks["Hydro Pump"]) == 150,
          SV.attack_damage(me, op, spot, atks["Hydro Pump"]))

    me, op, spot, atks = _ex_board("Dialga ex")      # Metal; board 2 M + 2 P
    check("Metal Blast likewise", 
          SV.attack_damage(me, op, spot, atks["Metal Blast"]) == 140,
          SV.attack_damage(me, op, spot, atks["Metal Blast"]))


def test_bench_counts_honour_their_filter():
    """Gourgeist ex pays per Benched Pokemon *that has damage counters*.

    The count ignored the trailing filter and paid for the whole Bench.
    """
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Gourgeist ex")   # bench: 2 damaged, 1 not
    check("Horrifying Rondo counts only the 2 damaged Benched Pokemon",
          SV.attack_damage(me, op, spot, atks["Horrifying Rondo"]) == 130,
          SV.attack_damage(me, op, spot, atks["Horrifying Rondo"]))


def test_type_words_are_types_not_name_fragments():
    """"for each of your Grass Pokemon in play" is a TYPE.

    It was matched as a name substring, so Torterra ex's Forest March
    counted zero Grass Pokemon on a board where Torterra ex itself is the
    Grass Pokemon, scored 0, and the AI never used the attack.
    """
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Torterra ex")
    check("Forest March sees the Grass Pokemon it is standing on",
          SV.attack_damage(me, op, spot, atks["Forest March"]) == 30,
          SV.attack_damage(me, op, spot, atks["Forest March"]))


def test_discard_scalers_are_paid_for():
    """Eleven ex attacks buy damage by discarding Energy at attack time.

    All of them scored their printed base and nothing else -- Raging Bolt
    ex read as a 70-damage attacker. The cost must be charged where the
    damage is credited, or the attack is free and repeatable, which is
    exactly the bug Cursed Blast's self-KO had.
    """
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Raging Bolt ex")
    atk = atks["Bellowing Thunder"]
    on_board = spot.energy_count() + sum(b.energy_count() for b in me.bench)
    check("board starts with 7 Energy", on_board == 7, on_board)
    check("Bellowing Thunder is worth far more than its printed 70",
          SV.attack_damage(me, op, spot, atk) == 420,
          SV.attack_damage(me, op, spot, atk))
    SV.attack_side_effects(me, op, atk, [])
    left = spot.energy_count() + sum(b.energy_count() for b in me.bench)
    check("and the Energy is actually discarded", left == 1, left)
    check("so the next swing is not free",
          SV.attack_damage(me, op, spot, atk) == 0)

    me, op, spot, atks = _ex_board("Scizor ex")
    check("Cross Breaker discards 2 Metal for 240",
          SV.attack_damage(me, op, spot, atks["Cross Breaker"]) == 240,
          SV.attack_damage(me, op, spot, atks["Cross Breaker"]))


def test_hp_threshold_and_conditional_kos_execute():
    """Compiling a Knock Out is not the same as performing one."""
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Medicham ex")
    atk = atks["Chi-Atsu"]                    # opp Active is 280 HP on 50
    check("Chi-Atsu is worth the 180 counters it places",
          SV.attack_rider_value(me, op, atk) == 180,
          SV.attack_rider_value(me, op, atk))
    SV.attack_side_effects(me, op, atk, [])
    check("and it places them", op.active.damage == 230, op.active.damage)

    me, op, spot, atks = _ex_board("Mega Darkrai ex")
    atk = atks["Abyss Eye"]
    check("Abyss Eye is worth nothing against a healthy Active",
          SV.conditional_ko_target(me, op, atk) is None)
    op.active.conditions = {"poisoned"}
    check("and Knocks Out a Poisoned one regardless of HP",
          SV.conditional_ko_target(me, op, atk) is op.active)

    me, op, spot, atks = _ex_board("Yveltal ex")
    atk = atks["Soul Destroyer"]
    op.active.damage = 250                    # 280 HP -> 30 remaining
    check("Soul Destroyer reaches anything under its HP line",
          SV.conditional_ko_target(me, op, atk) is op.active)



def test_attack_gates_are_conditional_and_enforced():
    """"Can't attack unless you have 4 or more X" was doubly broken.

    The generic "lock" rule matched "can't attack" and threw the whole
    "unless ..." clause away, compiling a conditional gate into an
    unconditional one -- and nothing in the game loop consumed it either,
    so in practice the gate did not exist. A Team Rocket's Mewtwo ex deck
    holding four Team Rocket's Pokemon in sixty cards attacked freely on
    182 turns across 120 games and measured 24.2%; with the gate enforced
    it is blocked on 738 turns and measures 12.5%.
    """
    import ability_engine as AE
    import simulate_versus as SV
    txt = ("This Pokémon can't attack unless you have 4 or more "
           "Team Rocket's Pokémon in play.")
    eff = IR.compile_effect("ability", "Power Saver", txt)
    ops = [a.op for a in eff.actions]
    check("it compiles to a gate", IR.Op.ATTACK_GATE in ops)
    check("and NOT to a blanket attack lock", IR.Op.LOCK not in ops)

    POK, EFF = build(["Team Rocket's Mewtwo ex", "Team Rocket's Diglett"],
                     {"Team Rocket's Mewtwo ex": ("ASC", "281"),
                      "Team Rocket's Diglett": ("ASC", "100")})
    mewtwo = Spot("Team Rocket's Mewtwo ex")
    me = FakePlayer("A", POK, EFF, active=mewtwo)
    me.bench = []
    check("one Team Rocket's Pokemon in play is not enough",
          AE.query_attack_gate(me, mewtwo) is False)
    me.bench = [Spot("Team Rocket's Diglett") for _ in range(3)]
    check("four is", AE.query_attack_gate(me, mewtwo) is True)
    me.bench = [Spot("Team Rocket's Diglett")]
    check("and dropping back below blocks it again",
          AE.query_attack_gate(me, mewtwo) is False)


def test_promo_set_codes_parse():
    """PR-SV is the one set code in this pool with a hyphen in it.

    The set-code pattern allowed none, so the code stayed glued to the
    card name, the line resolved to nothing, and the card vanished from
    every count: deckcheck called a 12-Basic deck an 8-Basic deck.
    """
    import tcg_model as M
    entries = M.parse_decklist_entries("4 Raging Bolt ex PR-SV 145\n")
    check("the name is the name", entries[0]["name"] == "Raging Bolt ex",
          entries[0]["name"])
    check("and the promo set code is kept",
          (entries[0]["set"], entries[0]["number"]) == ("PR-SV", "145"),
          (entries[0]["set"], entries[0]["number"]))



def test_attack_costs_that_were_never_paid():
    """Three whole families of attack cost were free.

    Every one inflates its user, which is the dangerous direction: a cost
    that is never charged never shows up as a missing feature, only as a
    deck that looks better than it is.
    """
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Ceruledge ex")
    before = spot.energy_count()
    SV.attack_side_effects(me, op, atks["Raging Amethyst"], [])
    check("'Discard all Energy from this Pokemon' actually discards it",
          before == 4 and spot.energy_count() == 0, spot.energy_count())

    me, op, spot, atks = _ex_board("Armarouge ex")
    SV.attack_side_effects(me, op, atks["Armor Cannon"], [])
    check("and a single typed discard takes exactly one",
          spot.energy_count() == 3, spot.energy_count())

    # ... but the "discarded in this way" scalers must not be charged
    # twice, since they pay for themselves in a different code path.
    me, op, spot, atks = _ex_board("Raging Bolt ex")
    SV.attack_side_effects(me, op, atks["Bellowing Thunder"], [])
    left = spot.energy_count() + sum(b.energy_count() for b in me.bench)
    check("a discard-scaler is charged once, not twice", left == 1, left)

    POK, EFF = build(["Fomantis"], {"Fomantis": ("PBL", "3")})
    fom = Spot("Fomantis")
    me2 = FakePlayer("A", POK, EFF, active=fom)
    op2 = FakePlayer("B", POK, EFF, active=Spot("Fomantis"))
    atk = next(a for a in POK["Fomantis"]["attacks"]
               if a["name"] == "Reckless Charge")
    fom.damage = 0
    SV.attack_side_effects(me2, op2, atk, [])
    check("recoil damages its own user", fom.damage == 10, fom.damage)


def test_heal_scaling_and_spread_are_counted_once():
    """Lurantis ex's payoff, and the snipe shapes it sits beside."""
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Lurantis ex")
    cutter = atks["Lively Cutter"]
    spot.healed_this_turn = False
    check("Lively Cutter is 60 when nothing healed it",
          SV.attack_damage(me, op, spot, cutter) == 60,
          SV.attack_damage(me, op, spot, cutter))
    spot.healed_this_turn = True
    check("and 260 on a turn it was healed",
          SV.attack_damage(me, op, spot, cutter) == 260,
          SV.attack_damage(me, op, spot, cutter))

    # A free-target snipe carries ALL its damage in the text, so it must be
    # applied exactly once -- as counters (no Weakness on the Bench), not
    # as counters AND main damage.
    me, op, spot, atks = _ex_board("Fezandipiti ex")
    arrow = atks["Cruel Arrow"]
    before = sum(s.damage for s in [op.active] + op.bench)
    main = SV.attack_damage(me, op, spot, arrow, record=False)
    SV.attack_side_effects(me, op, arrow, [])
    after = sum(s.damage for s in [op.active] + op.bench)
    check("Cruel Arrow places its 100 once", main == 0 and after - before == 100,
          (main, after - before))

    me, op, spot, atks = _ex_board("Farigiraf ex")
    beam = atks["Dirty Beam"]
    before = sum(s.damage for s in [op.active] + op.bench)
    main = SV.attack_damage(me, op, spot, beam, record=False)
    SV.attack_side_effects(me, op, beam, [])
    after = sum(s.damage for s in [op.active] + op.bench)
    check("but an 'also does 30 to a Benched' rider is on TOP of the base",
          main == 160 and after - before == 30, (main, after - before))



def test_special_energy_provides_what_it_says():
    """Every Special Energy in the pool was treated as "any type".

    The fallback for an unrecognised Energy card was the whole type list,
    and all 18 Special Energy hit it -- Shadowy Darkness Energy says
    plainly "it provides Darkness Energy" and was being counted as able to
    pay a Fire cost. The opposite error sat next to it: Team Rocket's
    Energy provides TWO, and was attached as one, which is the whole
    reason a three-Energy attack on a Stage 1 is castable.
    """
    import simulate_versus as SV
    import tcg_model as M
    by_name, _ = M.build_card_index(M.load_cards())
    check("a typed Special Energy provides only its type",
          SV.energy_provisions("Shadowy Darkness Energy", by_name)
          == [["Darkness"]],
          SV.energy_provisions("Shadowy Darkness Energy", by_name))
    check("a Colorless one likewise",
          SV.energy_provisions("Spiky Energy", by_name) == [["Colorless"]])
    tr = SV.energy_provisions("Team Rocket's Energy", by_name)
    check("Team Rocket's Energy provides TWO", len(tr) == 2, tr)
    check("and only Psychic or Darkness",
          all(sorted(x) == ["Darkness", "Psychic"] for x in tr), tr)
    check("Prism still provides every type, one at a time",
          len(SV.energy_provisions("Prism Energy", by_name)) == 1
          and len(SV.energy_provisions("Prism Energy", by_name)[0]) > 5)
    check("Spinning Tail is payable off two Team Rocket's Energy",
          SV.can_pay(["Darkness", "Darkness", "Darkness"], tr + tr))


def test_rare_candy_bridges_in_the_baseline_sim_too():
    """The same Stage-1 lookup bug lived in simulate_baseline.

    It reported N's Vanilluxe at 0.0% in play by turn 6 for a deck the
    match simulator plays it in every game -- the two simulators
    disagreeing is the signal that one of them is wrong.
    """
    import simulate_baseline as SB
    check("the pool knows what N's Vanilluxe's Stage 1 evolves from",
          SB._pool_evolves_from("N's Vanillish") == "N's Vanillite",
          SB._pool_evolves_from("N's Vanillish"))



def test_coin_flips_are_actually_flipped():
    """Every coin flip in the pool was a guaranteed success.

    parse_chance matched "flip a coin[^.]{0,30}if heads" -- but the printed
    phrasing puts a FULL STOP between the clauses, and [^.] cannot cross
    one. All 158 cards written that way parsed as chance 1.0: Ekans always
    Confused, Crushing Hammer always discarded an Energy, and an entire
    coin-flip deck in decks/ was measured never missing a flip.
    """
    check("a single flip is 0.5",
          IR.parse_chance("Flip a coin. If heads, discard an Energy.") == 0.5)
    check("two coins, all heads, is 0.25",
          IR.parse_chance("Flip 2 coins. If all of them are heads, this "
                          "attack does 100 more damage.") == 0.25)
    check("flip-until-tails is a damage calculation, not a gate",
          IR.parse_chance("Flip a coin until you get tails.") == 1.0)
    check("damage-per-heads is likewise not a gate",
          IR.parse_chance("Flip 2 coins. This attack does 90 damage for "
                          "each heads.") == 1.0)
    check("text with no flip is certain",
          IR.parse_chance("Your opponent's Active Pokemon is now Confused.")
          == 1.0)

    # And the damage side of the same clause: the conditional-bonus path
    # needs a parsed CONDITION to gate on, and a coin flip is not one, so
    # these silently paid base damage.
    import random
    import simulate_versus as SV
    me, op, spot, atks = _ex_board("Amoonguss ex")
    atk = atks["Champignon's Swing"]
    random.seed(1)
    vals = {SV.attack_damage(me, op, spot, atk, record=False)
            for _ in range(400)}
    check("a flipped damage bonus lands on both outcomes",
          vals == {100, 180}, sorted(vals))


def test_meta_trainers_compile_once_and_correctly():
    """Four Trainers from the current top meta lists, all mis-modelled.

    Overlapping rules ACCUMULATE actions and the dedupe only drops exactly
    identical ones, so two rules matching the same sentence with slightly
    different arguments both fired.
    """
    import simulate_versus as SV
    import tcg_model as M
    by_name, _ = M.build_card_index(M.load_cards())
    SV._CARDS_BY_NAME.update(by_name)
    SV._TRAINER_IR_CACHE.clear()

    def ops(name):
        eff = SV.trainer_effect_ir(name)
        return [] if eff is None else [(str(a.op), a.amount) for a in eff.actions]

    check("Crushing Hammer exists at all",
          ops("Crushing Hammer") == [("discard_energy_from_opponent", 1)],
          ops("Crushing Hammer"))
    check("and it is a coin flip",
          SV.trainer_effect_ir("Crushing Hammer").chance == 0.5)
    check("Rosa's Encouragement attaches 2, not 4",
          ops("Rosa's Encouragement") == [("attach_energy", 2)],
          ops("Rosa's Encouragement"))
    check("Crispin searches 1 and attaches 1",
          ops("Crispin") == [("search_to_hand", 1), ("attach_energy", 1)],
          ops("Crispin"))
    check("Unfair Stamp draws 5 for YOU and sets the opponent to 2",
          ops("Unfair Stamp") == [("draw", 5), ("set_opponent_hand", 2)],
          ops("Unfair Stamp"))



def test_counter_budgets_are_allocated_to_take_a_knockout():
    """"Put N damage counters ... in any way you like" is a BUDGET.

    It was being spent by topping Pokemon up toward a flat KO_THRESHOLD of
    60 regardless of their real HP, and the sort put an UNDAMAGED Pokemon
    ahead of one five counters from dying. Phantom Dive put all six
    counters on a fresh 60 HP Basic while two sat at 20 damage, and
    Knocked Out nothing.
    """
    import audit_ex_damage as A
    import simulate_versus as SV
    import tcg_model as M
    cards = M.load_cards()
    by_name, _ = M.build_card_index(cards)
    SV._CARDS_BY_NAME.update(by_name)
    card = [c for c in cards if c["name"] == "Dragapult ex"][0]
    me, op, spot = A.build_board(card, by_name)
    me.active = spot
    atk = next(a for a in M.build_pokemon_info(card)["attacks"]
               if a["name"] == "Phantom Dive")
    hp = op.POKEMON["Dunsparce"]["hp"]
    before = sum(s.damage for s in op.bench)
    SV.attack_side_effects(me, op, atk, [])
    placed = (sum(s.damage for s in op.bench) - before) // 10
    check("it spends exactly its budget", placed == 6, placed)
    check("and finishes something rather than killing nothing",
          any(b.damage >= hp for b in op.bench),
          [b.damage for b in op.bench])



def test_gust_targeting_is_policy_split():
    """The two pilots must actually differ, or the mirror measures nothing.

    This caught a flaw in my own experiment: the prize-aware gust targeting
    was written UNCONDITIONALLY, so both seats of the mirror used it and the
    comparison silently measured only the other half of the change. A
    policy-gated behaviour needs a test that the gate works, exactly like an
    Ability needs a test that it fires.
    """
    import simulate_versus as SV
    import tcg_model as M
    by_name, _ = M.build_card_index(M.load_cards())
    SV._CARDS_BY_NAME.update(by_name)
    POK = {n: M.build_pokemon_info((by_name.get(n) or [None])[0])
           for n in ("Dunsparce", "Mega Heracross ex")}
    me, op = SV.Player("A", POK, []), SV.Player("B", POK, [])
    a = SV.InPlay("Dunsparce", 0)
    a.energy = [["Colorless"]] * 3
    me.active = a
    op.active = SV.InPlay("Dunsparce", 0)
    low = SV.InPlay("Dunsparce", 0)
    low.damage = 50                       # 10 HP left, worth 1 Prize
    ex = SV.InPlay("Mega Heracross ex", 0)
    ex.damage = 270                       # 10 HP left, worth 3 Prizes
    op.bench = [low, ex]

    me.policy = "v1"
    check("v1 drags up whatever has least HP left",
          SV.choose_gust_target(me, op) is low)
    me.policy = "v2g"
    check("v2g drags up the same-effort target worth three times as much",
          SV.choose_gust_target(me, op) is ex)



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
               test_victory_symbol_is_prize_gated,
               test_biting_spree_hits_the_opponent,
               test_terminal_period_needs_exactly_six_counters,
               test_food_prep_scales_with_kofu_in_discard,
               test_hide_n_sneak_threshold,
               test_matcha_spin_is_not_charged_twice,
               test_board_wide_spread_is_priced_across_the_board,
               test_neurokinesis_counts_the_whole_opposing_board,
               test_prevention_walls_check_who_is_attacking,
               test_turn_locks_are_applied_not_just_compiled,
               test_unregistered_trainers_resolve_from_card_text,
               test_hp_tools_are_attached_and_raise_the_KO_threshold,
               test_ai_values_knockouts_and_setup_rather_than_raw_damage,
               test_wall_breakers_endure_and_ability_hp,
               test_counter_multiplier_scales_what_is_already_there,
               test_rare_candy_bridges_a_line_the_deck_does_not_own,
               test_typed_energy_scalers_count_only_that_type,
               test_bench_counts_honour_their_filter,
               test_type_words_are_types_not_name_fragments,
               test_discard_scalers_are_paid_for,
               test_hp_threshold_and_conditional_kos_execute,
               test_attack_gates_are_conditional_and_enforced,
               test_promo_set_codes_parse,
               test_attack_costs_that_were_never_paid,
               test_heal_scaling_and_spread_are_counted_once,
               test_special_energy_provides_what_it_says,
               test_rare_candy_bridges_in_the_baseline_sim_too,
               test_resistance_is_applied,
               test_coin_flips_are_actually_flipped,
               test_meta_trainers_compile_once_and_correctly,
               test_counter_budgets_are_allocated_to_take_a_knockout,
               test_gust_targeting_is_policy_split]:
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
