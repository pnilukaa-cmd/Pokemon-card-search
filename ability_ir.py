#!/usr/bin/env python3
"""A structured intermediate representation (IR) for Pokemon card effects.

WHY THIS EXISTS
---------------
The first pass at modeling Abilities hand-wrote one regex per family
(draw, retaliation, damage reduction). That worked for ~40 of the 282
Abilities in the pool and was already becoming unmaintainable: each new
family meant new bespoke parsing code, new bespoke execution code, and no
way to answer "what fraction of the card pool do we actually understand?"

This module replaces that with a compiler. Card text is compiled into a
small, explicit IR, and the game engine executes the IR. Adding support
for a new card shape is then a matter of adding one RULE to a table --
not touching the engine at all.

THE IR
------
Every effect is:

    Effect(
        trigger    = when it fires        (ONCE_PER_TURN, ON_DAMAGED, PASSIVE...)
        conditions = what must be true    (requires Active, a named card in play...)
        costs      = what must be paid    (discard N, shuffle self away...)
        actions    = what actually happens (a list of atomic ops)
    )

An Action is a verb plus a target plus optional amount/filter:

    Action(op=DRAW,           amount=3,  target=SELF)
    Action(op=PLACE_COUNTERS, amount=5,  target=ATTACKING_POKEMON)
    Action(op=REDUCE_DAMAGE,  amount=30, target=YOUR_ALL, filter={'type':'Metal'})

The verb set is deliberately small and closed. Anything that cannot be
expressed in it compiles to an Effect with `unsupported` set, carrying the
original text and a reason -- so coverage is always measurable and gaps
are always visible, never silently dropped.

RUNNING IT
----------
    python3 ability_ir.py            # coverage report over the whole pool
    python3 ability_ir.py --misses   # list what does not compile, grouped
    python3 ability_ir.py --card X   # show the compiled IR for one card
"""
import json
import re
import sys
from collections import Counter, defaultdict

CARDS_PATH = "pokemon_standard_cards.json"


# --------------------------------------------------------------------------
# Vocabulary
# --------------------------------------------------------------------------

class Trigger:
    ONCE_PER_TURN = "once_per_turn"
    ANY_TIMES_PER_TURN = "any_times_per_turn"
    ON_PLAY = "on_play"                  # played from hand to the Bench
    ON_EVOLVE = "on_evolve"              # played from hand to evolve
    ON_DAMAGED = "on_damaged"            # this/your Pokemon took an attack
    ON_KO = "on_ko"                      # something was Knocked Out
    ON_OPPONENT_EVENT = "on_opp_event"   # opponent evolved/retreated/etc.
    PASSIVE = "passive"                  # continuously true, no activation


ALL_SPECIAL_CONDITIONS = frozenset(
    {"asleep", "burned", "confused", "paralyzed", "poisoned"})


class Op:
    # card flow
    DRAW = "draw"
    SEARCH_TO_HAND = "search_to_hand"
    SEARCH_TO_BENCH = "search_to_bench"
    FROM_DISCARD_TO_HAND = "from_discard_to_hand"
    SHUFFLE_SELF_INTO_DECK = "shuffle_self_into_deck"
    LOOK_AT_DECK = "look_at_deck"
    # energy
    ATTACH_ENERGY = "attach_energy"
    MOVE_ENERGY = "move_energy"
    # damage / health
    PLACE_COUNTERS = "place_counters"
    MULTIPLY_COUNTERS = "multiply_counters"
    MOVE_COUNTERS = "move_counters"
    HEAL = "heal"
    PREVENT_DAMAGE = "prevent_damage"
    REDUCE_DAMAGE = "reduce_damage"
    MODIFY_HP = "modify_hp"
    # combat modifiers
    BUFF_DAMAGE = "buff_damage"
    MODIFY_ATTACK_COST = "modify_attack_cost"
    # board control
    SWITCH = "switch"
    APPLY_CONDITION = "apply_condition"
    LOCK = "lock"
    DISCARD_FROM_OPPONENT = "discard_from_opponent"
    MODIFY_RETREAT = "modify_retreat"
    ENDURE = "endure"
    MILL_OPPONENT = "mill_opponent"
    DISCARD_STADIUM = "discard_stadium"
    EVOLVE_EARLY = "evolve_early"
    BUFF_CONDITION_DAMAGE = "buff_condition_damage"
    DEVOLVE = "devolve"
    MODIFY_PRIZE = "modify_prize"
    CONDITION_IMMUNITY = "condition_immunity"
    # Swap a Pokemon in play for one in the discard, in place:
    # attachments, damage, Special Conditions and turns in play all
    # stay on the new Pokemon. Transformation Tome and Ogre's Mask.
    SWAP_IN_PLACE = "swap_in_place"
    ATTACK_FIRST_TURN = "attack_first_turn"
    # Mew ex's Memory Helix: every Benched Pokemon's attacks, not just
    # the pre-evolution chain GRANT_ATTACK_ACCESS already walks.
    GRANT_BENCH_ATTACKS = "grant_bench_attacks"
    SET_WEAKNESS = "set_weakness"
    # "apply Weakness for both Active Pokemon as x3". The engine had no
    # multiplier concept at all -- Weakness was a hard-coded `dmg *= 2`.
    WEAKNESS_MULTIPLIER = "weakness_multiplier"
    REVEAL_OPPONENT_HAND = "reveal_opponent_hand"
    ATTACH_TOOL = "attach_tool"
    SET_TYPE = "set_type"
    SEARCH_TO_DISCARD = "search_to_discard"
    ENERGY_PROVIDES_EXTRA = "energy_provides_extra"
    FORCE_BENCH_OPPONENT = "force_bench_opponent"
    ATTACK_TWICE = "attack_twice"
    RETURN_TO_HAND_ON_KO = "return_to_hand_on_ko"
    IGNORE_OPPONENT_EFFECTS = "ignore_opponent_effects"
    DISCARD_ENERGY_FROM_OPPONENT = "discard_energy_from_opponent"
    SWAP_HAND_WITH_DECK = "swap_hand_with_deck"
    # "Shuffle your hand into your deck. Then, draw N" -- the first half of
    # Lillie's Determination and Lacey, dropped until 2026-09-23.
    SHUFFLE_HAND_INTO_DECK = "shuffle_hand_into_deck"
    # Accompanying Flute: the opponent's Basics from their top 5 onto their
    # Bench -- fresh bodies with no Energy for a gust-and-lock deck.
    FILL_OPPONENT_BENCH = "fill_opponent_bench"
    SET_OPPONENT_HAND = "set_opponent_hand"
    # Discard down to a hand size -- the symmetric half of
    # DISCARD_FROM_OPPONENT, for Hand Trimmer.
    DISCARD_FROM_SELF = "discard_from_self"
    # Shuffle cards from the discard pile back into the deck.
    DISCARD_TO_DECK = "discard_to_deck"
    CLEAR_CONDITIONS = "clear_conditions"
    # Search the deck and put what you find on TOP of it, not into
    # hand -- a turn slower than a search, which is the whole
    # difference between Ciphermaniac's Codebreaking and Ultra Ball.
    SEARCH_TO_TOP_OF_DECK = "search_to_top_of_deck"
    # Put the Prize cards on the bottom of the deck and take that
    # many fresh ones off the top. Redeemable Ticket.
    REROLL_PRIZES = "reroll_prizes"
    # Send the opponent's Active to the Bench -- THEY choose the
    # replacement, which is strictly weaker than a gust.
    FORCE_SWITCH_OPPONENT = "force_switch_opponent"
    DISCARD_TOOL_FROM_OPPONENT = "discard_tool_from_opponent"
    # "This attack also does N damage to each of YOUR Benched Pokemon."
    SELF_BENCH_DAMAGE = "self_bench_damage"
    SELF_ENERGY_TO_HAND = "self_energy_to_hand"
    # "During your opponent's next turn, attacks used by the Defending
    # Pokemon do N less damage."
    WEAKEN_DEFENDER = "weaken_defender"
    # "Heal from this Pokemon the same amount of damage you did."
    HEAL_AS_DEALT = "heal_as_dealt"
    # Bounce / recall shapes.
    SELF_TO_HAND = "self_to_hand"
    SELF_TO_DECK = "self_to_deck"
    SELF_DISCARD = "self_discard"
    BENCH_TO_HAND = "bench_to_hand"
    OPP_BENCH_TO_DECK = "opp_bench_to_deck"
    OPP_ENERGY_TO_HAND = "opp_energy_to_hand"
    DISCARD_TOOL_FROM_ALL_OPPONENT = "discard_tool_from_all_opponent"
    RECOVER_TO_BENCH = "recover_to_bench"
    KO_OUTRIGHT = "ko_outright"
    SELF_KO = "self_ko_now"
    BUFF_NAMED_ATTACK_NEXT_TURN = "buff_named_attack_next_turn"
    DEFENDER_TAKES_MORE = "defender_takes_more"
    SET_BASE_DAMAGE = "set_base_damage"
    BENCH_SPLASH = "bench_splash"
    SELF_TAKES_MORE = "self_takes_more"
    DELAYED_DISCARD_DEFENDER = "delayed_discard_defender"
    EXTRA_PRIZE_ON_KO = "extra_prize_on_ko"
    REMOVE_WEAKNESS = "remove_weakness"
    NO_OP_INFORMATION = "no_op_information"
    RETALIATE_COUNTERS = "retaliate_counters"
    OPP_ATTACH_FROM_DISCARD = "opp_attach_from_discard"
    DISCARD_TOOL_ANY = "discard_tool_any"
    # Rules about deckbuilding or the setup phase, which happen before
    # a game state exists. Modelled as nothing ON PURPOSE.
    NO_OP_SETUP_RULE = "no_op_setup_rule"
    # Grand Tree: evolve straight out of the deck, Stage 1 then Stage 2.
    EVOLVE_FROM_DECK = "evolve_from_deck"
    # Backtrack Badge: re-flip an attack's coins once and keep the
    # better result. A real reroll, not "a second chance at the odds".
    REFLIP_COINS = "reflip_coins"
    # Heavy Baton: on a Knock Out, salvage Energy to the Bench.
    SALVAGE_ENERGY_ON_KO = "salvage_energy_on_ko"
    EXTRA_TOOLS = "extra_tools"
    LOCK_COUNTER_MOVEMENT = "lock_counter_movement"
    WIN_GAME = "win_game"
    CONDITIONAL_KO = "conditional_ko"
    DAMAGE_TO_HP_THRESHOLD = "damage_to_hp_threshold"
    ATTACK_GATE = "attack_gate"
    BENCH_CAP = "bench_cap"
    SELF_DAMAGE = "self_damage"
    DISCARD_SELF_ENERGY = "discard_self_energy"
    # meta
    GRANT_ATTACK_ACCESS = "grant_attack_access"


class Target:
    SELF = "self"
    YOUR_ACTIVE = "your_active"
    YOUR_BENCHED = "your_benched"
    YOUR_ANY = "your_any"
    YOUR_ALL = "your_all"
    OPP_ACTIVE = "opp_active"
    OPP_BENCHED = "opp_benched"
    OPP_ANY = "opp_any"
    OPP_ALL = "opp_all"
    ATTACKING_POKEMON = "attacking_pokemon"
    BOTH_ALL = "both_all"
    PLAYER = "player"          # affects a player, not a Pokemon
    OPPONENT = "opponent"


class Action:
    __slots__ = ("op", "amount", "target", "filter", "note")

    def __init__(self, op, amount=None, target=Target.SELF, filter=None, note=None):
        self.op = op
        self.amount = amount
        self.target = target
        self.filter = filter or {}
        self.note = note

    def __repr__(self):
        bits = [self.op]
        if self.amount is not None:
            bits.append(f"x{self.amount}")
        bits.append(f"-> {self.target}")
        if self.filter:
            bits.append(str(self.filter))
        return "Action(" + " ".join(bits) + ")"

    def to_dict(self):
        return {"op": self.op, "amount": self.amount, "target": self.target,
                "filter": self.filter, "note": self.note}


class Effect:
    __slots__ = ("source", "name", "text", "trigger", "conditions", "costs",
                 "actions", "unsupported", "rules_hit", "chance")

    def __init__(self, source, name, text):
        self.source = source
        self.name = name
        self.text = text
        self.trigger = Trigger.PASSIVE
        self.conditions = []
        self.costs = []
        self.actions = []
        self.unsupported = None
        self.rules_hit = []
        # Probability the effect resolves. Coin flips are real randomness in
        # the game, so they are modeled as such rather than treated as
        # unsupported: "flip a coin, if heads..." is chance=0.5, and
        # "flip 2 coins" style multi-flips set it accordingly.
        self.chance = 1.0

    @property
    def supported(self):
        return bool(self.actions) and not self.unsupported

    def __repr__(self):
        if self.unsupported:
            return f"<Effect {self.source}/{self.name} UNSUPPORTED: {self.unsupported}>"
        return (f"<Effect {self.source}/{self.name} {self.trigger} "
                f"cond={self.conditions} cost={self.costs} {self.actions}>")

    def to_dict(self):
        return {
            "source": self.source, "name": self.name, "trigger": self.trigger,
            "conditions": self.conditions, "costs": self.costs,
            "actions": [a.to_dict() for a in self.actions],
            "unsupported": self.unsupported, "rules_hit": self.rules_hit,
            "chance": self.chance,
        }


# --------------------------------------------------------------------------
# Shared sub-parsers
# --------------------------------------------------------------------------

TYPES = ("Grass|Fire|Water|Lightning|Psychic|Fighting|Darkness|Metal|Fairy|"
         "Dragon|Colorless")

_NUM_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def _num(token, default=1):
    if token is None:
        return default
    token = token.strip().lower()
    if token.isdigit():
        return int(token)
    return _NUM_WORDS.get(token, default)


def parse_trigger(text):
    t = text.lower()
    if "as often as you like during your turn" in t:
        return Trigger.ANY_TIMES_PER_TURN
    if "when you play this pok" in t and "to evolve" in t:
        return Trigger.ON_EVOLVE
    if "when you play this pok" in t:
        return Trigger.ON_PLAY
    if "is damaged by an attack" in t:
        return Trigger.ON_DAMAGED
    if re.search(r"is knocked out|were knocked out", t):
        # "if any of your Pokemon were KO'd during your opponent's last turn"
        # is a CONDITION on a once-per-turn ability, not an ON_KO trigger.
        if "once during your turn" in t:
            return Trigger.ONCE_PER_TURN
        return Trigger.ON_KO
    if "whenever your opponent" in t:
        return Trigger.ON_OPPONENT_EVENT
    if "once during your turn" in t:
        return Trigger.ONCE_PER_TURN
    # Fan Rotom's Fan Call. Read as PASSIVE, so it never fired at all.
    if "once during your first turn" in t:
        return Trigger.ONCE_PER_TURN
    return Trigger.PASSIVE


def parse_conditions(text):
    t = text
    out = []
    # "You can use this card only if you have X in play" (Glass Trumpet:
    # any Tera Pokemon; Anthea & Concordia: six named N's Pokemon). It
    # compiled to a no-op, so the requirement was simply dropped.
    m = re.search(r"you can use this card only if you have ([\w'’ ,]+?"
                  r"(?:, and [\w'’ ]+?)?) in play", t, re.I)
    if m:
        req = m.group(1).strip()
        st = re.match(r"any (\w+) pok[eé]mon$", req, re.I)
        if st:
            out.append({"kind": "have_in_play", "subtype": st.group(1).capitalize()})
        else:
            names = [x.strip() for x in re.split(r",\s*(?:and\s+)?|\s+and\s+", req) if x.strip()]
            out.append({"kind": "have_in_play", "names": names})
    if re.search(r"once during your first turn", t, re.I):
        out.append({"kind": "own_first_turn"})
    if re.search(r"if this pok[eé]mon is in the active spot|as long as this pok[eé]mon is in the active spot", t, re.I):
        out.append({"kind": "self_is_active"})
    if re.search(r"as long as this pok[eé]mon is on your bench|is on your bench", t, re.I):
        out.append({"kind": "self_is_benched"})
    m = re.search(r"were knocked out during your opponent'?s last turn", t, re.I)
    if m:
        out.append({"kind": "lost_pokemon_last_turn"})
    # Case-sensitive on the leading "if" meant this only ever fired when the
    # clause appeared MID-sentence. Three cards put it first -- Illumise,
    # Shelmet and Karrablast -- and a dropped condition is worse than a
    # missed effect: the effect then applies UNCONDITIONALLY. The name
    # capture stays case-sensitive, since a card name is capitalised.
    m = re.search(r"[Ii]f you have ([A-Z][\w'’ -]+?) in play", t)
    if m:
        out.append({"kind": "named_in_play", "name": m.group(1).strip()})
    m = re.search(r"if you played ([A-Z][\w'’ -]+?) from your hand this turn", t)
    if m:
        out.append({"kind": "played_this_turn", "name": m.group(1).strip()})
    m = re.search(r"if this pok[eé]mon has any (" + TYPES + r") energy attached", t, re.I)
    if m:
        out.append({"kind": "self_has_energy_type", "type": m.group(1).capitalize()})
    if re.search(r"if this pok[eé]mon has full hp", t, re.I):
        out.append({"kind": "self_full_hp"})
    # "your Active Pokemon THAT HAS 3 or more Energy attached" is a gate on
    # the target, not decoration. Dropped, it made Jumbo Ice Cream an
    # unconditional Heal 80 for one Item -- strictly better than the card,
    # and exactly the kind of free upgrade a deck gets built around.
    m = re.search(r"(\d+) or more energy (?:cards? )?attached", t, re.I)
    if m:
        out.append({"kind": "active_energy_at_least", "count": int(m.group(1))})
    m = re.search(r"if your opponent has any cards? in their discard pile"
                  r" that have \"([^\"]+)\" in the name", t, re.I)
    if m:
        out.append({"kind": "opponent_discard_has_name", "name": m.group(1)})
    # ---- conditional flat damage bonuses ---------------------------------
    # attack_damage() can already pay "if <condition>, this attack does N
    # more damage", but only when parse_conditions recognised the clause.
    # Nine such bonuses on cards in this repo's decks had no matching
    # condition kind and were silently dropped -- including 130 on Mega
    # Excadrill ex's Maximum Drilling and 100 on Team Rocket's Kangaskhan
    # ex's Wicked Impact, both on top-five decks.
    m = re.search(r"if you have at least (\d+) (" + TYPES + r") energy in play",
                  t, re.I)
    if m:
        out.append({"kind": "energy_in_play_at_least",
                    "count": int(m.group(1)), "type": m.group(2).capitalize()})
    m = re.search(r"if your opponent'?s active pok[eé]mon is an? (" + TYPES
                  + r") pok[eé]mon", t, re.I)
    if m:
        out.append({"kind": "opponent_active_is_type",
                    "type": m.group(1).capitalize()})
    if re.search(r"if this pok[eé]mon has an? pok[eé]mon tool( card)? attached",
                 t, re.I):
        out.append({"kind": "self_has_tool"})
    m = re.search(r"if this pok[eé]mon has at least (\d+) extra energy attached",
                  t, re.I)
    if m:
        out.append({"kind": "self_extra_energy", "count": int(m.group(1))})
    if re.search(r"if this pok[eé]mon moved from your bench to the active spot"
                 r" this turn", t, re.I):
        out.append({"kind": "self_promoted_this_turn"})
    if re.search(r"if a stadium( card)? is in play", t, re.I):
        out.append({"kind": "any_stadium_in_play"})
    m = re.search(r"if this pok[eé]mon used ([\w'’ -]+?) during your last turn",
                  t, re.I)
    if m:
        out.append({"kind": "self_used_attack_last_turn",
                    "name": m.group(1).strip()})
    m = re.search(r"if you played a supporter card that has \"([^\"]+)\" in its"
                  r" name from your hand during this turn", t, re.I)
    if m:
        out.append({"kind": "played_supporter_named", "name": m.group(1)})
    # ---- requirements phrased as "otherwise this attack does nothing" ----
    # Always written as the FAILURE case ("if your opponent's Active isn't
    # Burned, this attack does nothing"), so each is parsed as the positive
    # requirement and attack_damage returns 0 when it is not met.
    m = re.search(r"if your opponent'?s active pok[eé]mon isn'?t"
                  r" (asleep|burned|confused|paralyzed|poisoned)", t, re.I)
    if m:
        out.append({"kind": "opponent_active_has_condition",
                    "condition": m.group(1).lower()})
    if re.search(r"if your opponent'?s active pok[eé]mon isn'?t a pok[eé]mon ex",
                 t, re.I):
        out.append({"kind": "opponent_active_is_ex"})
    if re.search(r"if your opponent'?s active pok[eé]mon has no damage counters"
                 r" on it before this attack does damage", t, re.I):
        out.append({"kind": "opponent_active_has_damage"})
    m = re.search(r"if you don'?t have exactly (\d+) cards? in your hand", t, re.I)
    if m:
        out.append({"kind": "own_hand_size", "count": int(m.group(1))})
    if re.search(r"if you don'?t have the same number of cards in your hand as"
                 r" your opponent", t, re.I):
        out.append({"kind": "hand_size_matches_opponent"})
    if re.search(r"if there is no stadium in play", t, re.I):
        out.append({"kind": "any_stadium_in_play"})
    # re.I is required: the clause starts a sentence, so "If you don't" is
    # capitalised and a case-sensitive pattern silently never matched.
    m = re.search(r"if you don'?t have ([\w'’ -]+?) on your bench", t, re.I)
    if m:
        for nm in re.split(r"\s+and\s+", m.group(1)):
            out.append({"kind": "named_in_play", "name": nm.strip()})
    m = re.search(r"if your opponent doesn'?t have exactly (\d+) or (\d+) prize"
                  r" cards? remaining", t, re.I)
    if m:
        out.append({"kind": "opponent_prizes_exactly",
                    "counts": [int(m.group(1)), int(m.group(2))]})
    m = re.search(r"if you have (\d+) or fewer benched pok[eé]mon", t, re.I)
    if m:
        out.append({"kind": "own_bench_more_than", "count": int(m.group(1))})

    # ---- more conditional flat bonuses -----------------------------------
    # A pool-wide sweep found 85 attacks whose "if <clause>, this attack does
    # N more damage" had no condition kind, so attack_damage had nothing to
    # gate on and every one of them quietly paid base damage. These cover the
    # clauses that appear more than once.
    if re.search(r"if your opponent'?s active pok[eé]mon already has any damage"
                 r" counters on it", t, re.I):
        out.append({"kind": "opponent_active_has_damage"})
    if re.search(r"if your opponent'?s active pok[eé]mon is an evolution"
                 r" pok[eé]mon", t, re.I):
        out.append({"kind": "opponent_active_is_evolution"})
    m = re.search(r"if your opponent'?s active pok[eé]mon is a stage (\d+)"
                  r" pok[eé]mon", t, re.I)
    if m:
        out.append({"kind": "opponent_active_is_stage", "stage": int(m.group(1))})
    if re.search(r"if your benched pok[eé]mon have any damage counters on them",
                 t, re.I):
        out.append({"kind": "your_bench_has_damage"})
    m = re.search(r"if your opponent'?s active pok[eé]mon is"
                  r" (asleep|burned|confused|paralyzed|poisoned)", t, re.I)
    if m:
        out.append({"kind": "opponent_active_has_condition",
                    "condition": m.group(1).lower()})
    if re.search(r"if your opponent'?s active pok[eé]mon is affected by a"
                 r" special condition", t, re.I):
        out.append({"kind": "opponent_active_has_any_condition"})
    m = re.search(r"if your opponent has (\d+) or fewer prize cards remaining",
                  t, re.I)
    if m:
        out.append({"kind": "opponent_prizes_at_most", "count": int(m.group(1))})
    if re.search(r"if you have more prize cards remaining than your opponent",
                 t, re.I):
        out.append({"kind": "more_prizes_than_opponent"})
    m = re.search(r"if you have any (" + TYPES + r") pok[eé]mon on your bench",
                  t, re.I)
    if m:
        out.append({"kind": "bench_has_type", "type": m.group(1).capitalize()})
    if re.search(r"if this pok[eé]mon and your opponent'?s active pok[eé]mon"
                 r" have the same amount of energy attached", t, re.I):
        out.append({"kind": "same_energy_as_opponent_active"})
    if re.search(r"if this pok[eé]mon has no damage counters on it", t, re.I):
        out.append({"kind": "self_no_damage"})
    elif re.search(r"if this pok[eé]mon has any damage counters on it", t, re.I):
        out.append({"kind": "self_has_damage"})
    if re.search(r"if this pok[eé]mon has any special energy attached", t, re.I):
        out.append({"kind": "self_has_special_energy"})
    # Named Energy, e.g. "any Team Rocket's Energy attached". Deliberately
    # NOT the elemental types -- "any Darkness Energy attached" is already
    # self_has_energy_type, which reads the attached card's TYPE rather than
    # its name, and adding a second name-based check for the same clause
    # made Munkidori's Adrena-Brain fail against Basic Darkness Energy.
    m = re.search(r"if this pok[eé]mon has any ([\w'’ ]+?) energy attached",
                  t, re.I)
    if m:
        nm = m.group(1).strip()
        if (nm.lower() not in ("special",)
                and not re.fullmatch(TYPES, nm, re.I)):
            out.append({"kind": "self_has_named_energy", "name": nm})
    if re.search(r"if your opponent'?s active pok[eé]mon has a pok[eé]mon tool"
                 r" attached", t, re.I):
        out.append({"kind": "opponent_active_has_tool"})
    m = re.search(r"if you have (\d+) or more energy in play", t, re.I)
    if m:
        out.append({"kind": "energy_in_play_at_least", "count": int(m.group(1)),
                    "type": None})

    m = re.search(r"if any of your ([\w'’ -]+?) pok[eé]mon were knocked out"
                  r" by damage from an attack during your opponent'?s last turn",
                  t, re.I)
    if m:
        out.append({"kind": "lost_pokemon_last_turn", "family": m.group(1).strip()})
    elif re.search(r"if any of your pok[eé]mon were knocked out by damage from an"
                   r" attack during your opponent'?s last turn", t, re.I):
        out.append({"kind": "lost_pokemon_last_turn"})
    # "If Festival Grounds is in play, this Pokemon may use an attack it
    # has twice." The Stadium clause was dropped entirely, so the gate on
    # an archetype-defining Ability did not exist.
    m = re.search(r"\b[Ii]f ([A-Z][\w'’ -]+?) is in play", t)
    if m:
        out.append({"kind": "stadium_in_play", "name": m.group(1).strip()})
    # Lurantis ex's Lively Cutter is 60 that becomes 260 "if this Pokemon
    # was healed during this turn" -- the payoff the whole heal-punish
    # archetype is built on, and the clause had no condition kind, so
    # attack_damage() had nothing to gate the bonus on and paid the base.
    if re.search(r"was healed during this turn", t, re.I):
        out.append({"kind": "healed_this_turn"})
    # Spiritomb-style: the Ability protects your ACTIVE, gated on its type,
    # and fires from anywhere in play. Without this the type gate is lost and
    # a Darkness-only retaliator wrongly fires for a Psychic Active.
    m = re.search(r"if your active (" + TYPES + r") pok[eé]mon is damaged", t, re.I)
    if m:
        out.append({"kind": "active_is_type", "type": m.group(1).capitalize()})
    m = re.search(r"if this pok[eé]mon'?s remaining hp is (\d+) or less", t, re.I)
    if m:
        out.append({"kind": "self_hp_at_or_below", "hp": int(m.group(1))})
    m = re.search(r"if your opponent has any ([\w' ]+?) in play", t, re.I)
    if m:
        out.append({"kind": "opponent_has_in_play", "what": m.group(1).strip()})
    # Decidueye ex's Sniper's Eye gates its whole effect on the opponent
    # holding an exact number of cards. Without this the cost reduction
    # compiles as unconditional and the card reads as far stronger than it
    # is -- the entire deck around it exists to satisfy this clause.
    # Luxio's Fighting Roar only turns on against an ex Active. Without
    # this the "can evolve the turn you play it" clause reads as
    # unconditional, which is a materially different card.
    if re.search(r"if your opponent'?s active pok[eé]mon is a pok[eé]mon ex", t, re.I):
        out.append({"kind": "opponent_active_is_ex"})
    # "If you have 4 or more Pokemon that have the Hide 'n' Sneak Ability
    # in your discard pile" -- the whole Hide 'n' Sneak archetype is built
    # on this threshold, and it appears on Dhelmise, Sinistcha and
    # Spiritomb at three different counts.
    m = re.search(r"if you have (\d+) or more pok[eé]mon that have the "
                  r"(.+?) ability in your discard pile", t, re.I)
    if m:
        out.append({"kind": "named_ability_in_discard",
                    "ability": m.group(2).strip(), "count": int(m.group(1))})
    # N's Sigilyph's Victory Symbol is the only outright "you win this
    # game" card in the format, and it is gated on an exact Prize count.
    m = re.search(r"when you have exactly (\d+) prize cards? remaining", t, re.I)
    if m:
        out.append({"kind": "own_prizes_equal", "count": int(m.group(1))})
    m = re.search(r"if your opponent has (?:exactly )?(\d+) (?:or (more|fewer) )?cards?"
                  r" in (?:their|your opponent'?s) hand", t, re.I)
    if m:
        cmp_op = {"more": ">=", "fewer": "<="}.get(m.group(2) or "", "==")
        out.append({"kind": "opponent_hand_size", "op": cmp_op,
                    "count": int(m.group(1))})
    return out


def parse_chance(text):
    """Probability the effect resolves, from any coin-flip clause.

    A single "flip a coin. If heads..." is 0.5. "Flip N coins. If all of
    them are heads" is 0.5**N. Flip-until-tails scaling attacks are damage
    calculations, not ability gates, so they are left at 1.0 here.
    """
    t = text.lower()
    # Drasna: the coin picks how many to draw, and both sides draw.
    if re.search(r"if heads, draw \d+ cards?\. if tails, draw \d+", t):
        return 1.0
    # The printed phrasing puts a FULL STOP between the clauses -- "Flip a
    # coin. If heads, ..." -- and [^.] cannot cross one. Every card in this
    # pool written that way (158 of them) parsed as chance 1.0, so EVERY
    # coin flip in the game was a guaranteed success: Ekans always
    # Confused, Crushing Hammer always discarded, and a coin-flip deck in
    # decks/ was measured never missing a flip.
    m = re.search(r"flip (\d+) coins?[^.]{0,40}\.?\s*if all of them are heads", t)
    if m:
        return 0.5 ** int(m.group(1))
    if re.search(r"flip a coin[^.]{0,30}\.?\s*if (heads|tails)", t):
        return 0.5
    m = re.search(r"flip (\d+) coins", t)
    if m and "for each heads" not in t:
        return 1 - 0.5 ** int(m.group(1))     # at least one heads
    return 1.0


def parse_costs(text):
    t = text
    out = []
    m = re.search(r"discard (\d+|a|an|two|three) cards? from your hand in order to use", t, re.I)
    if m:
        out.append({"kind": "discard_hand", "amount": _num(m.group(1))})
    if re.search(r"put a card from your hand on the bottom of your deck in order to use", t, re.I):
        out.append({"kind": "discard_hand", "amount": 1})
    # The Item phrasing of the same cost. "You can use this card only if you
    # discard 3 other cards from your hand" is Secret Box, and it parsed as
    # free -- the card matched no rule at all, so nothing noticed.
    m = re.search(r"only if you discard (\d+|a|an|two|three) other cards?"
                  r" from your hand", t, re.I)
    if m:
        out.append({"kind": "discard_hand", "amount": _num(m.group(1))})
    m = re.search(r"discard a basic (" + TYPES + r") energy card from your hand", t, re.I)
    if m:
        out.append({"kind": "discard_energy_from_hand", "type": m.group(1).capitalize()})
    m = re.search(r"discard a basic (" + TYPES + r") energy from this pok[eé]mon", t, re.I)
    if m:
        out.append({"kind": "discard_energy_from_self", "type": m.group(1).capitalize()})
    if re.search(r"you must play 2 [\w'’ -]+ cards? at once", t, re.I):
        out.append({"kind": "play_two_copies"})
    if re.search(r"shuffle this pok[eé]mon and all attached cards into your deck", t, re.I):
        out.append({"kind": "shuffle_self"})
    if re.search(r"this pok[eé]mon is knocked out", t, re.I) and "if you use this ability" in t.lower():
        out.append({"kind": "self_ko"})
    return out


def parse_target(phrase, default=Target.SELF):
    """Map a natural-language target phrase onto the Target vocabulary."""
    p = (phrase or "").lower()
    if "attacking pok" in p:
        return Target.ATTACKING_POKEMON
    if "both yours and your opponent" in p or "each player" in p:
        return Target.BOTH_ALL
    # "...to THEIR Active Pokemon" -- the possessive refers back to the
    # opponent named earlier in the sentence, so the tail clause on its own
    # has no "opponent" in it. Sableye's Damage Collection moved counters
    # onto the wrong side of the board without this.
    if "your opponent" in p or "opponent's" in p or re.match(r"\s*their\b", p):
        if "active" in p:
            return Target.OPP_ACTIVE
        if "bench" in p:
            return Target.OPP_BENCHED
        if "each of" in p or "all of" in p:
            return Target.OPP_ALL
        return Target.OPP_ANY
    if "this pok" in p:
        return Target.SELF
    if "your active" in p:
        return Target.YOUR_ACTIVE
    if "your bench" in p:
        return Target.YOUR_BENCHED
    if "each of your" in p or "all of your" in p:
        return Target.YOUR_ALL
    if "your pok" in p or "1 of your" in p:
        return Target.YOUR_ANY
    return default


# --------------------------------------------------------------------------
# RULE TABLE -- the extensible part
# --------------------------------------------------------------------------
# Each rule is (name, compiled regex, builder). The builder receives the
# regex match plus the full text and returns a list of Actions. Rules are
# tried in order; every rule that matches contributes its Actions, so a
# card doing two things produces two Actions.

RULES = []


def rule(name, pattern, flags=re.I):
    def deco(fn):
        RULES.append((name, re.compile(pattern, flags), fn))
        return fn
    return deco


# ---- card flow -----------------------------------------------------------

@rule("draw_to_n", r"draw cards until you have (\d+) cards? in your hand")
def _r(m, text):
    return [Action(Op.DRAW, None, Target.SELF, {"up_to_hand_size": int(m.group(1))})]


@rule("draw_n", r"\bdraw (\d+) cards?")
def _r(m, text):
    if re.search(r"draw cards until you have", text, re.I):
        return []
    # "opponent empties their hand, then draws N" is a hand-SIZE set, not a
    # draw -- opponent_hand_reset below owns it. Left here it compiled as
    # "both players draw N", which both handed the user free cards and lost
    # the only thing that matters about the effect: the resulting count.
    if re.search(r"(?:have your opponent shuffle|your opponent shuffles) their hand",
                 text, re.I):
        return []
    # Unfair Stamp's draw is lopsided ("you draw 5, your opponent draws 2")
    # and asymmetric_hand_reset owns it. Left here as well it added a
    # symmetric "both draw 5" on top, handing the opponent three free cards
    # off a card whose entire point is that the draw is one-sided.
    if re.search(r"then, you draw \d+ cards?, and your opponent draws", text, re.I):
        return []
    if re.search(r"each player draw|your opponent .{0,20}draw|they draw", text, re.I):
        return [Action(Op.DRAW, int(m.group(1)), Target.BOTH_ALL)]
    # What happens to the hand FIRST. Both halves of "Shuffle your hand into
    # your deck. Then, draw 6" / "Discard your hand and draw 5" were read as
    # a bare "draw 6": Lillie's Determination, in 46 of 54 field decks, was
    # a free six cards on top of the hand, burning six off the deck a time.
    coin = re.search(r"if heads, draw (\d+) cards?\. if tails, draw (\d+)", text, re.I)
    pre = []
    if re.search(r"shuffle your hand into your deck\. then,? (?:draw \d|flip a coin)", text, re.I):
        pre = [Action(Op.SHUFFLE_HAND_INTO_DECK, None, Target.SELF)]
    elif re.search(r"discard your hand and draw \d", text, re.I):
        pre = [Action(Op.DISCARD_FROM_SELF, 99, Target.SELF)]
    flt = {}
    # "..., draw 8 cards instead" -- a larger draw under a Prize condition.
    # It is not a gate on the card: Lacey without it still draws 4.
    inst = re.search(r"if (you|your opponent) ha(?:ve|s) (exactly )?(\d+)"
                     r"(?: or (fewer))? prize cards? remaining, draw (\d+) cards? instead",
                     text, re.I)
    if inst:
        flt["instead"] = int(inst.group(5))
        flt["instead_if"] = {
            "who": "self" if inst.group(1).lower() == "you" else "opponent",
            "cmp": "<=" if inst.group(4) else "==",
            "count": int(inst.group(3))}
    if coin:
        # Drasna: heads 8, tails 3. Read as a flat 8, gated on the coin.
        flt["coin"] = [int(coin.group(1)), int(coin.group(2))]
    return pre + [Action(Op.DRAW, int(m.group(1)), Target.SELF, flt)]


@rule("draw_per_opponent_hand",
      r"draw a card for each card in your opponent'?s hand")
def _r(m, text):
    """Mr. Mime: read as "draw a card" -- one, whatever their hand held."""
    pre = []
    if re.search(r"shuffle your hand into your deck", text, re.I):
        pre = [Action(Op.SHUFFLE_HAND_INTO_DECK, None, Target.SELF)]
    return pre + [Action(Op.DRAW, 1, Target.SELF, {"per_opp_hand": True})]


@rule("opponent_hand_reset",
      r"(?:have your opponent shuffle|your opponent shuffles) their hand"
      r"[^.]*?(?:into their deck|on the bottom of their deck)")
def _r(m, text):
    """Vivillon's Grand Wing / Gothitelle's Distorted Future.

    The opponent's hand goes away and is replaced by exactly N fresh cards.
    The number, not the drawing, is the effect: it is the only repeatable
    way in the format to put an opponent on an exact hand count, which is
    what Decidueye ex's Sniper's Eye reads.
    """
    n = re.search(r"(?:they |and )draw (\d+) cards?", text[m.start():], re.I)
    if not n:
        return []
    return [Action(Op.SET_OPPONENT_HAND, int(n.group(1)), Target.OPPONENT)]


# "Your opponent discards cards from their hand until they have N cards"
# -- Xerosic's Machinations, in five decks here, and Hand Trimmer, which
# does it to both players. Distinct from the shuffle-and-redraw hand
# resets: nothing is drawn back.
@rule("discard_opponent_hand_down_to",
      r"(your opponent|each player) discards? cards? from their hand"
      r" until they have (\d+) cards?")
def _r(m, text):
    acts = [Action(Op.DISCARD_FROM_OPPONENT, None, Target.OPPONENT,
                   {"down_to": int(m.group(2))})]
    if m.group(1).lower() == "each player":
        acts.append(Action(Op.DISCARD_FROM_SELF, None, Target.SELF,
                           {"down_to": int(m.group(2))}))
    return acts


# Shuffle cards back out of the discard pile. Three shapes of the same
# effect -- Sacred Ash (Pokemon), Energy Recycler (Basic Energy), Great
# Haul Net (either or both, Water only) -- and none compiled. Against a
# mill deck this is the difference between decking out and not.
@rule("shuffle_discard_into_deck",
      r"shuffle up to (\d+) (" + TYPES + r")? ?(pok[eé]mon|basic energy|energy)"
      r"(?: cards?)? from your discard pile into your deck")
def _r(m, text):
    kind = "Pokemon" if m.group(3).lower().startswith("pok") else "Energy"
    f = {"kind": kind}
    if m.group(2):
        f["type"] = m.group(2).capitalize()
    return [Action(Op.DISCARD_TO_DECK, int(m.group(1)), Target.SELF, f)]


# Lumiose Galette: 20 HP back and one Special Condition off the Active.
# Two actions from one sentence; the heal rules read the number and the
# condition-clearing half was dropped.
@rule("heal_and_clear_condition",
      r"heal (\d+) damage and remove a special condition from your active")
def _r(m, text):
    return [Action(Op.HEAL, int(m.group(1)), Target.YOUR_ACTIVE),
            Action(Op.CLEAR_CONDITIONS, None, Target.YOUR_ACTIVE)]


# Dark Bell: "Both Active non-Darkness Pokemon are now Confused." The
# type exclusion is the whole card -- it reads as symmetric and is not,
# because the deck playing it is mono-Darkness.
@rule("condition_both_actives_except_type",
      r"both active non-(" + TYPES + r") pok[eé]mon are now"
      r" (asleep|burned|confused|paralyzed|poisoned)")
def _r(m, text):
    return [Action(Op.APPLY_CONDITION, None, Target.BOTH_ALL,
                   {"conditions": [m.group(2).lower()],
                    "type_not": m.group(1).capitalize(),
                    "active_only": True})]


@rule("conditional_ko_on_counters",
      r"(?:if your opponent'?s active pok[eé]mon has exactly (\d+) damage counters"
      r" on it, that pok[eé]mon is knocked out"
      r"|knock out 1 of your opponent'?s pok[eé]mon that has exactly (\d+)"
      r" damage counters on it)")
def _r(m, text):
    """Mega Absol ex's Terminal Period and Glaceon ex's Euclase: a Knock
    Out that ignores HP entirely and keys off an exact counter total.
    Scoring these on damage alone read them as 0-damage attacks."""
    n = int(m.group(1) or m.group(2))
    tgt = Target.OPP_ACTIVE if m.group(1) else Target.OPP_ANY
    return [Action(Op.CONDITIONAL_KO, n, tgt, {"exact_counters": n})]


@rule("ko_on_special_condition",
      r"if your opponent'?s active pok[eé]mon is affected by a special "
      r"condition, it is knocked out")
def _r(m, text):
    """Mega Darkrai ex's Abyss Eye. A 0-damage attack that takes Prizes,
    and the payoff for every Special Conditions deck in the pool."""
    return [Action(Op.CONDITIONAL_KO, 0, Target.OPP_ACTIVE,
                   {"needs_special_condition": True})]


@rule("ko_below_remaining_hp",
      r"knock out each of your opponent'?s pok[eé]mon that has (\d+) hp or "
      r"less remaining")
def _r(m, text):
    """Yveltal ex's Soul Destroyer: a board wipe on anything already
    softened. Worth every Pokemon it removes, not zero."""
    return [Action(Op.CONDITIONAL_KO, int(m.group(1)), Target.OPP_ALL,
                   {"max_remaining_hp": int(m.group(1))})]


@rule("damage_until_remaining_hp",
      r"put damage counters on (each of your opponent'?s benched pok[eé]mon|"
      r"your opponent'?s active pok[eé]mon) until (?:its|their) remaining "
      r"hp is (\d+)")
def _r(m, text):
    """Medicham ex's Chi-Atsu and Palossand ex's Barite Jail. These place
    counters up to a fixed remaining HP, so on a big target they are the
    largest single hit in the pool -- Chi-Atsu is 230 against a 280 HP
    Active. Both read as 0-damage attacks."""
    tgt = (Target.OPP_BENCHED if "benched" in m.group(1).lower()
           else Target.OPP_ACTIVE)
    return [Action(Op.DAMAGE_TO_HP_THRESHOLD, int(m.group(2)), tgt, {})]


@rule("win_game", r"you win this game")
def _r(m, text):
    """The alternate win condition itself. Its Prize-count gate is parsed
    as a condition, so the action here is unconditional and the engine
    decides whether it is live."""
    return [Action(Op.WIN_GAME, None, Target.SELF)]


@rule("draw_one", r"\bdraw a card")
def _r(m, text):
    if re.search(r"draw a card for each card in your opponent", text, re.I):
        return []          # draw_per_opponent_hand owns it
    # "each player draws a card" belongs to each_player_draws below. Both
    # rules used to fire on Chandelure's Alluring Light, emitting the draw
    # twice -- which doubled the rate of the one engine a deck-out deck
    # actually wins with.
    if re.search(r"each player", text, re.I):
        return []
    return [Action(Op.DRAW, 1, Target.SELF)]


# Words that qualify WHICH Pokemon a search may take, but are not part of
# any card's name. Dumping them into name_contains produced filters like
# "a Pokemon whose name contains 'Basic'", which matches nothing -- so all
# 88 Bench-search attacks in the pool silently found zero cards.
STAGE_WORDS = {"basic", "stage 1", "stage 2", "evolution"}
TYPE_WORDS = {"grass", "fire", "water", "lightning", "psychic", "fighting",
              "darkness", "metal", "dragon", "colorless", "fairy"}


def _search_filter(qualifier):
    """Split a search's qualifier into stage / type / name-fragment."""
    q = (qualifier or "").strip()
    filt = {}
    low = q.lower()
    for word in sorted(STAGE_WORDS, key=len, reverse=True):
        if low.startswith(word):
            filt["stage"] = "Stage 1" if word == "stage 1" else (
                "Stage 2" if word == "stage 2" else word.title())
            low = low[len(word):].strip()
            break
    if low in TYPE_WORDS:
        filt["type"] = low.title()
        low = ""
    if low:
        filt["name_contains"] = q[-len(low):].strip() if len(low) <= len(q) else q
    return filt


@rule("search_to_bench",
      r"search your deck for (?:up to )?(\d+|a|an|any number of)"
      r" ([\w'’ -]*?)pok[eé]mon[^.]{0,60}?onto your bench")
def _r(m, text):
    # "any number of" is Precious Trolley, an ACE SPEC that fills the Bench
    # in one card and appears in seven decks here. The count alternation
    # only knew digits and articles, so it matched nothing.
    n = m.group(1).lower()
    amount = 5 if n == "any number of" else _num(n)
    return [Action(Op.SEARCH_TO_BENCH, amount, Target.YOUR_BENCHED,
                   _bench_name_filter(m))]


def _bench_name_filter(m):
    """The qualifier before the noun, plus a name restriction after it.

    "up to 2 Pokemon that have "Koffing" in their name": the restriction
    sits after the noun and was dropped, so Smog Signals and Rotom's Roto
    Call benched any Basic at all.
    """
    f = _search_filter(m.group(2))
    nm = re.search(r"that have [\"“']([^\"”']+)[\"”'] in their names?",
                   m.group(0))
    if nm and not f.get("name_contains"):
        f["name_contains"] = nm.group(1)
    return f


# Fossil Quarry: "search your deck for up to 2 Item cards that have
# "Antique" in their name and put them onto your Bench". The Fossils are
# Items that PLAY AS Basic Pokemon, and build_deck_model already files them
# under kind "Pokemon", so the ordinary Bench-search handler can place them
# -- the wording just never matched a rule, because it says "Item cards"
# where every other Bench search says "Pokemon".
@rule("search_named_item_to_bench",
      r"search your deck for (?:up to )?(\d+|a|an) item cards? that have"
      r" [\"“']([^\"”']+)[\"”'] in their name and put them onto your bench")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": m.group(2)})]


@rule("recruit_species_to_bench",
      r"search your deck for (?:up to )?(\d+|a|an) ([\w'’ .-]+?) and put (?:it|them) onto your bench")
def _r(m, text):
    """Species-named Bench search: "search your deck for up to 3 Lampent".

    search_to_bench above only matches text containing the word "Pokemon",
    so a card that names the species instead compiled to nothing at all.
    Lampent's Spreading Light is a whole deck's setup engine -- one attack
    fills the Bench with the Stage 1 that becomes the mill engine.

    The species is the capitalised token, checked against the ORIGINAL text
    rather than the case-folded match, so "3 Basic Energy cards" and other
    lowercase nouns don't get mistaken for a species name.
    """
    species = m.group(2).strip()
    if not species[:1].isupper():
        return []
    # "Basic Pokemon" / "Stage 2 Pokemon" is a category, not a species, and
    # search_to_bench above already handles it -- matching here as well
    # emitted the same action two and three times over.
    low = species.lower()
    # endswith() was too narrow: Buddy-Buddy Poffin captures "Basic Pokemon
    # WITH 70 HP OR LESS", which ends in "less", so the category slipped
    # through and the card compiled to two Bench searches. It benched the
    # right number only by luck -- the junk name_contains filter matched no
    # card name, so the second action silently no-opped. A species name
    # never contains the word "Pokemon" anywhere, so test the whole phrase.
    if "pokémon" in low or "pokemon" in low or low in STAGE_WORDS:
        return []
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": species})]


@rule("search_to_hand",
      r"search your deck for (?:up to )?(\d+|a|an)? ?([\w'’ -]*?)(pok[eé]mon|card|supporter|item|stadium|energy)[^.]{0,60}?(?:put (?:it|them) into your hand|into your hand)")
def _r(m, text):
    # A search that puts onto the Bench is search_to_bench's. The trigger
    # "when you play this Pokemon from your hand onto your Bench" is not:
    # it blocked Meowth ex's Supporter search outright.
    if "onto your bench" in re.sub(r"from your hand onto your bench", "",
                                   text.lower()):
        return []
    # Crispin searches TWO and puts only ONE in hand, attaching the other.
    # search_energy_split owns that shape; matching here as well put both
    # into hand and then attached a third.
    if re.search(r"put 1 of them into your hand\. attach the other", text, re.I):
        return []
    return [Action(Op.SEARCH_TO_HAND, _num(m.group(1)), Target.SELF,
                   dict(_search_filter(m.group(2)), kind=m.group(3).lower()))]


# Secret Box: one sentence naming four different kinds of card. The
# general search_to_hand rule reads a single kind, so this shape compiled
# to nothing at all -- an ACE SPEC that fetches an Item, a Tool, a
# Supporter AND a Stadium did nothing in any deck running it.
@rule("search_multi_kind",
      r"search your deck for an item card, a pok[eé]mon tool card,"
      r" a supporter card, and a stadium card")
def _r(m, text):
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": k})
            for k in ("item", "tool", "supporter", "stadium")]


# In-place swap: the Pokemon in the discard takes over the board position
# of one in play, keeping everything attached to it. Two cards in Standard
# do this -- Transformation Tome (four copies in N's Zoroark, where it is
# the deck's whole engine) and Ogre's Mask -- and neither compiled.
@rule("swap_in_place",
      r"choose a [\w'’ -]{0,40}?pok[eé]mon[^.]{0,60}?in your discard pile"
      r"[^.]{0,60}?switch it with 1 of your [^.]{0,60}?in play")
def _r(m, text):
    t = text.lower()
    f = {}
    if "basic pok" in t:
        f["stage"] = "Basic"
    # The name restriction is quoted, and the quoted phrase is the same on
    # both halves of the sentence -- read it off the whole text rather than
    # trying to capture it twice inside an already long pattern.
    fam = re.search(r"has [\"“']([^\"”']+)[\"”'] in its name", text)
    if fam:
        f["family"] = fam.group(1)
    if re.search(r"pok[eé]mon ex", t):
        f["rule_box"] = True
    return [Action(Op.SWAP_IN_PLACE, 1, Target.YOUR_ANY, f)]


@rule("discard_to_hand", r"put (?:up to )?(\d+|a|an) ([\w'’ -]*?)(?:card|pok[eé]mon|energy)[^.]{0,40}from your discard pile into your hand")
def _r(m, text):
    # WHICH cards. The executor used to return Pokemon whatever the card
    # said: Miracle Headset ("2 Supporter cards") handed back two Pokemon,
    # Dedenne's Electromagnetic Sonar ("a Trainer card") a Pokemon, and
    # Lana's Aid never returned the Basic Energy it names.
    seg = m.group(0).lower()
    kinds = []
    if "supporter" in seg:
        kinds.append("Supporter")
    if "trainer" in seg:
        kinds += ["Supporter", "Item", "Tool", "Stadium"]
    if re.search(r"pok[eé]mon(?! ex| v\b)", seg.split("from your discard")[0]):
        kinds.append("Pokemon")
    et = re.search(r"basic (\w+ )?energy", seg)
    if et:
        kinds.append("Energy")
    f = {"kinds": kinds} if kinds else {}
    if et and et.group(1) and et.group(1).strip() not in ("energy",):
        f["energy_type"] = et.group(1).strip().capitalize()
    return [Action(Op.FROM_DISCARD_TO_HAND, _num(m.group(1)), Target.SELF, f)]


@rule("look_at_deck", r"look at the top (\d+) cards? of your deck")
def _r(m, text):
    return [Action(Op.LOOK_AT_DECK, int(m.group(1)), Target.SELF)]


# ---- energy --------------------------------------------------------------

@rule("attach_to_each_benched_type",
      r"choose up to (\d+) of your benched (" + TYPES + r") pok[eé]mon and attach a basic"
      r" energy card from your discard pile to each of them")
def _r(m, text):
    """Glass Trumpet: one Basic Energy from the discard to EACH of up to 2
    Benched Pokemon of a type. The generic rule read "to each of them" as a
    target and attached a single Energy to "self"."""
    return [Action(Op.ATTACH_ENERGY, 1, Target.YOUR_BENCHED,
                   {"from": "discard", "type": None, "each_of": int(m.group(1)),
                    "recipient_type": m.group(2).capitalize()})]


@rule("attach_energy_from_discard",
      r"attach (?:a|an|up to (\d+)) ?(?:basic )?(" + TYPES + r")? ?energy (?:cards? )?from your discard pile to ([^.]{0,50})")
def _r(m, text):
    if m.group(3).strip().lower().startswith("each of them"):
        return []          # attach_to_each_benched_type owns it
    return [Action(Op.ATTACH_ENERGY, _num(m.group(1)), parse_target(m.group(3)),
                   {"type": (m.group(2) or "").capitalize() or None, "from": "discard"})]


@rule("attach_energy_from_hand",
      r"attach (?:a|an|up to (\d+)) ?(?:basic )?(" + TYPES + r")? ?energy (?:cards? )?from your hand to ([^.]{0,50})")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, _num(m.group(1)), parse_target(m.group(3)),
                   {"type": (m.group(2) or "").capitalize() or None, "from": "hand"})]


@rule("attach_energy_from_deck",
      r"search your deck for (?:up to )?(\d+|a|an) ?(?:basic )?(" + TYPES + r")? ?energy[^.]{0,40}attach")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, _num(m.group(1)), Target.YOUR_ANY,
                   {"type": (m.group(2) or "").capitalize() or None, "from": "deck"})]


@rule("move_energy", r"move (?:a|an|(\d+)) ?(" + TYPES + r")? ?energy from ([^.]{0,40}?) to ([^.]{0,40})")
def _r(m, text):
    f = {"type": (m.group(2) or "").capitalize() or None,
         "from": parse_target(m.group(3))}
    # Elgyem's Slight Shift moves an Energy between the OPPONENT's own
    # Pokemon ("to another of their Pokemon"). It compiled as a move onto
    # your own Active -- and the executor ignored `from` anyway.
    if re.search(r"your opponent'?s pok[eé]mon to another of their", text, re.I):
        f["opp_internal"] = True
    return [Action(Op.MOVE_ENERGY, _num(m.group(1)), parse_target(m.group(4)), f)]


# ---- damage / health -----------------------------------------------------

@rule("multiply_counters",
      r"(double|triple|quadruple) the number of damage counters on "
      r"(each of your opponent'?s pok[eé]mon|each of them)")
def _r(m, text):
    """N's Vanilluxe's Snow Coating and Spiritomb's Spiritual End.

    The taxonomy had a `damage_counter_doubler` family for these, but no
    IR rule and no op, so the text compiled to nothing at all -- a deck
    whose whole plan is doubling a spread was invisible to the simulator.
    Multiplying is not the same shape as placing: it scales whatever is
    already there, which is what makes it exponential across turns.
    """
    factor = {"double": 2, "triple": 3, "quadruple": 4}[m.group(1).lower()]
    # "choose 2 of your opponent's Pokemon and quadruple ... each of them"
    mm = re.search(r"choose (\d+) of your opponent'?s pok[eé]mon", text, re.I)
    filt = {"targets": int(mm.group(1))} if mm else {}
    tgt = Target.OPP_ANY if mm else Target.OPP_ALL
    return [Action(Op.MULTIPLY_COUNTERS, factor, tgt, filt)]



@rule("place_counters_per_discard",
      r"put (\d+) damage counters? on ([^.]{0,45}?) for each (basic (?:" + TYPES +
      r") energy) card in your discard pile")
def _r(m, text):
    """Sinistcha ex's Re-Brew: 2 counters per Basic Grass Energy in the
    discard. The count is the card -- flattened to a plain 2 it reads as a
    20-damage attack instead of a 100+ one. The trailing "shuffle those
    Energy cards into your deck" is carried as `consumes_fuel`, because it
    makes Re-Brew a burst rather than a repeatable engine."""
    return [Action(Op.PLACE_COUNTERS, int(m.group(1)), parse_target(m.group(2)),
                   {"per_discard_card": m.group(3).lower(),
                    "consumes_fuel": bool(
                        re.search(r"shuffle those energy cards into your deck",
                                  text, re.I))})]


@rule("place_counters", r"(?:place|put) (\d+) damage counters? on ([^.]{0,60})")
def _r(m, text):
    if re.search(r"for each .{0,30}card in your discard pile", text, re.I):
        return []          # place_counters_per_discard above owns this
    # "Choose 2 of your opponent's Pokemon and put 2 damage counters on
    # EACH of them" -- the target lives in the *earlier* clause, so
    # parsing only the "on ..." tail read "each of them" as this Pokemon
    # and pointed Crobat ex's Biting Spree at its own side of the board.
    mm = re.search(r"choose (\d+) of your opponent'?s pok[eé]mon[^.]{0,40}?"
                   r"(?:place|put) (\d+) damage counters? on each", text, re.I)
    if mm:
        return [Action(Op.PLACE_COUNTERS, int(mm.group(2)), Target.OPP_ANY,
                       {"targets": int(mm.group(1))})]
    # "... in any way you like" is a BUDGET to split, not N counters on
    # each target. Carried through so the engine can allocate it to take
    # an actual Knock Out instead of dumping the lot on one Pokemon.
    filt = {}
    if re.search(r"in any way you like", text, re.I):
        filt["distribute"] = True
    return [Action(Op.PLACE_COUNTERS, int(m.group(1)),
                   parse_target(m.group(2)), filt)]


@rule("move_counters", r"move (?:up to )?(\d+) damage counters? from ([^.]{0,40}?) to ([^.]{0,40})")
def _r(m, text):
    return [Action(Op.MOVE_COUNTERS, int(m.group(1)), parse_target(m.group(3)),
                   {"from": parse_target(m.group(2))})]


@rule("move_counters_any",
      r"move any number of damage counters from ([^.]{0,45}?) to ([^.]{0,45})")
def _r(m, text):
    """Sableye's Damage Collection. "Any number" is what makes an exact
    counter total reachable on demand, so the amount is left open (None)
    rather than pinned to a number the card never states."""
    return [Action(Op.MOVE_COUNTERS, None, parse_target(m.group(2)),
                   {"from": parse_target(m.group(1)), "any_number": True})]


@rule("heal", r"heal (\d+) damage from ([^.]{0,50})")
def _r(m, text):
    return [Action(Op.HEAL, int(m.group(1)), parse_target(m.group(2)))]


# Window widened from 80 to 140: Cornerstone Stance's restriction ("by
# your opponent's Pokemon that have an Ability") sits 83 characters in,
# so the clause that made the card conditional fell outside the match
# and it compiled as flat, unconditional invincibility.
@rule("prevent_damage", r"prevent all (?:damage|effects of attacks)[^.]{0,140}")
def _r(m, text):
    seg = m.group(0)
    tgt = Target.SELF
    if "your benched" in seg.lower():
        tgt = Target.YOUR_BENCHED
    elif "each of your" in seg.lower() or "all of your" in seg.lower():
        tgt = Target.YOUR_ALL
    filt = {}
    mm = re.search(r"from your opponent's ([\w' ]+?) pok", seg, re.I)
    if mm and "done to" not in mm.group(1).lower():
        filt["attacker_is"] = mm.group(1).strip()
    # The restriction on WHO is being blocked usually trails the word
    # "Pokemon" rather than preceding it, so the pattern above missed it
    # entirely and these Abilities compiled to "prevent all damage,
    # unconditionally" -- Sylveon's Safeguard and Cornerstone Mask
    # Ogerpon ex's Cornerstone Stance both became flat invincibility.
    if re.search(r"pok[eé]mon ex\b", seg, re.I):
        filt["attacker_is_ex"] = True
    if re.search(r"pok[eé]mon that ha(?:ve|s) an ability", seg, re.I):
        filt["attacker_has_ability"] = True
    # Shaymin's Flower Curtain shields only the Pokemon WITHOUT a Rule Box.
    # Dropping this clause made it protect the benched ex it is played
    # alongside, which is the exact opposite of how the card plays.
    if re.search(r"don'?t have a rule box", seg, re.I):
        filt["no_rule_box"] = True
    # Terapagos ex's Crown Opal: "by attacks from Basic non-Colorless
    # Pokemon". Dropped, it read as total immunity.
    mm = re.search(r"by attacks from (basic )?(?:non-(\w+) )?pok[eé]mon", seg, re.I)
    if mm and mm.group(1):
        filt["attacker_stage"] = "Basic"
    if mm and mm.group(2):
        filt["attacker_type_not"] = mm.group(2).capitalize()
    # Bastiodon's Ancient Bulwark stops only attackers holding 2 or less
    # Energy -- a wall against early aggression, not a wall. Dropped, it
    # read as total immunity for the whole board for the rest of the game,
    # which is the single largest over-count a passive can produce.
    mm = re.search(r"that ha(?:ve|s) (\d+) or (?:less|fewer) energy attached",
                   seg, re.I)
    if mm:
        filt["attacker_energy_at_most"] = int(mm.group(1))
    # "Prevent all EFFECTS of attacks ... (Damage is not an effect.)" is
    # not a damage wall: Skeledirge and Empoleon ex compiled as immune to
    # all damage. "Damage from AND effects of attacks" is both.
    if re.search(r"prevent all effects of attacks", seg, re.I):
        filt["effects_only"] = True
    elif re.search(r"prevent all damage from and effects of attacks", seg, re.I):
        filt["and_effects"] = True
    # Battle Cage: not damage at all -- damage COUNTERS put on a Benched
    # Pokemon by the opponent's attack or Ability effects. It compiled to a
    # bare "prevent all damage", which nothing that plays Stadiums reads.
    if re.search(r"prevent all damage counters from being placed on benched", seg, re.I):
        return [Action(Op.PREVENT_DAMAGE, None, Target.YOUR_BENCHED,
                       {"bench_counters": True})]
    return [Action(Op.PREVENT_DAMAGE, None, tgt, filt)]


@rule("reduce_damage", r"takes? (\d+) less damage from attacks")
def _r(m, text):
    tgt = Target.SELF
    mm = re.search(r"all of your ([\w'’ -]*?)pok[eé]mon take", text, re.I)
    filt = {}
    if mm:
        tgt = Target.YOUR_ALL
        fam = (mm.group(1) or "").strip()
        if fam:
            filt["family"] = fam
    mm2 = re.search(r"([\w'’]+) pok[eé]mon \(both yours and your opponent", text, re.I)
    if mm2:
        tgt = Target.BOTH_ALL
        filt["type"] = mm2.group(1).capitalize()
    return [Action(Op.REDUCE_DAMAGE, int(m.group(1)), tgt, filt)]


@rule("modify_hp", r"gets? \+(\d+) hp")
def _r(m, text):
    return [Action(Op.MODIFY_HP, int(m.group(1)), Target.SELF)]


# ---- combat modifiers ----------------------------------------------------

@rule("buff_damage", r"do (\d+) more damage")
def _r(m, text):
    tgt = Target.YOUR_ALL if re.search(r"attacks used by your", text, re.I) else Target.SELF
    filt = {}
    mm = re.search(r"attacks used by your ([\w'’ -]+?) pok[eé]mon", text, re.I)
    if mm:
        filt["family"] = mm.group(1).strip()
    return [Action(Op.BUFF_DAMAGE, int(m.group(1)), tgt, filt)]


@rule("attack_cost_scales_by_named_card_in_discard",
      r"cost (" + TYPES + r") less for each ([A-Z][\w'\u2019 .-]*?) card in your discard pile")
def _r(m, text):
    """Crabominable's and Veluza's Food Prep: "cost Colorless less for each
    Kofu card in your discard pile."

    The scaling is the card. Compiled as a flat -1 it is wrong in both
    directions -- a discount before any Kofu has been played, and a
    quarter of the real discount once four have. Haymaker goes from five
    Energy to one, and Sonic Edge from four to free.
    """
    return [Action(Op.MODIFY_ATTACK_COST, -1, Target.SELF,
                   {"type": m.group(1).capitalize(),
                    "per_named_card_in_discard": m.group(2).strip()})]


@rule("attack_cost_scales_by_opponent_bench",
      r"cost (" + TYPES + r") less for each of your opponent'?s benched pok[eé]mon")
def _r(m, text):
    """Incineroar ex's Hustle Play -- same shape as Food Prep, counting
    their Bench instead of your discard."""
    return [Action(Op.MODIFY_ATTACK_COST, -1, Target.SELF,
                   {"type": m.group(1).capitalize(),
                    "per_opponent_benched": True})]


@rule("modify_attack_cost", r"cost (" + TYPES + r") less")
def _r(m, text):
    # The scaling variants above own their own phrasings; without this the
    # flat rule fires as well and doubles the reduction.
    if re.search(r"less for each", text, re.I):
        return []
    return [Action(Op.MODIFY_ATTACK_COST, -1, Target.SELF, {"type": m.group(1).capitalize()})]


# ---- board control -------------------------------------------------------

@rule("fill_opponent_bench",
      r"reveal the top (\d+) cards of your opponent'?s deck\. you may choose any"
      r" number of basic pok[eé]mon you find there and put those pok[eé]mon onto"
      r" their bench")
def _r(m, text):
    return [Action(Op.FILL_OPPONENT_BENCH, int(m.group(1)), Target.OPPONENT)]


@rule("switch_opponent", r"switch (?:in )?1 of your opponent's benched (basic )?pok[eé]mon")
def _r(m, text):
    # Lisia's Appeal gusts only a BASIC Pokemon, and "Benched Basic
    # Pokemon" did not match at all, so the card only Confused.
    f = {"gust": True}
    if m.group(1):
        f["basic_only"] = True
    return [Action(Op.SWITCH, 1, Target.OPP_ACTIVE, f)]


@rule("switch_benched_type_in",
      r"switch 1 of your benched (\w+) pok[eé]mon(?:, except any ([^,]+),)? with your"
      r" active pok[eé]mon\.(?: if you do, the new active pok[eé]mon is now (\w+))?")
def _r(m, text):
    """Pecharunt ex's Subjugating Chains. Read as "the opponent's Active is
    now Poisoned" with no switch at all: a free Poison on the opponent every
    turn, and none of the card's real job -- bringing up a paid-up Benched
    attacker, whose own Poison is what switches Binding Mochi on."""
    f = {"gust": False, "choose": True, "type": m.group(1).capitalize()}
    if m.group(2):
        f["exclude"] = m.group(2).strip()
    if m.group(3):
        f["then_condition"] = m.group(3).lower()
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, f)]


@rule("switch_own", r"switch (?:this pok[eé]mon|your active pok[eé]mon) with 1 of your benched"
      r"(?: (" + TYPES + r"))?")
def _r(m, text):
    f = {"gust": False}
    if re.search(r"you may switch (?:this pok[eé]mon|your active pok[eé]mon) with", text, re.I):
        f["optional"] = True
    if m.group(1):
        f["type"] = m.group(1).capitalize()
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, f)]


@rule("apply_condition", r"is now (asleep|burned|confused|paralyzed|poisoned)")
def _r(m, text):
    # "the NEW Active Pokemon is now Poisoned" is your own, after a switch;
    # switch_benched_type_in owns it.
    # (Florges and Lisia's Appeal say the same about the OPPONENT's new
    # Active after a gust, and keep it.)
    if re.search(r"switch 1 of your benched .{0,80}the new active pok[eé]mon is now",
                 text, re.I | re.S):
        return []
    conds = re.findall(r"(asleep|burned|confused|paralyzed|poisoned)", text, re.I)
    tgt = Target.ATTACKING_POKEMON if "attacking pok" in text.lower() else Target.OPP_ACTIVE
    return [Action(Op.APPLY_CONDITION, None, tgt,
                   {"conditions": sorted({c.lower() for c in conds})})]


@rule("attack_bench_spread",
      r"this attack also does (\d+) damage to (each|\d+) of your opponent'?s "
      r"benched pok[eé]mon")
def _r(m, text):
    """17 attacks carry a Bench spread rider and none of them compiled --
    Dragapult ex aside, every "also does 30 to a Benched Pokemon" in the
    pool was doing nothing. Modelled as counters, not attack damage,
    because the printed reminder says Weakness and Resistance do not
    apply on the Bench."""
    amt = int(m.group(1)) // 10
    who = m.group(2).lower()
    if who == "each":
        return [Action(Op.PLACE_COUNTERS, amt, Target.OPP_BENCHED,
                       {"attack_damage": True})]
    return [Action(Op.PLACE_COUNTERS, amt, Target.OPP_BENCHED,
                   {"targets": int(who), "attack_damage": True})]


@rule("attack_snipe_any",
      r"this attack does (\d+) damage to (each|\d+) of your opponent'?s "
      r"pok[eé]mon")
def _r(m, text):
    """Free-target snipes -- Fezandipiti ex's Cruel Arrow, Electivire ex's
    Dual Bolt, Cinderace ex's Garnet Volley. Their printed damage field is
    empty because ALL of the damage is in this clause, so scored on the
    damage field alone they read as 0-damage attacks."""
    amt = int(m.group(1)) // 10
    who = m.group(2).lower()
    if who == "each":
        return [Action(Op.PLACE_COUNTERS, amt, Target.OPP_ALL,
                       {"attack_damage": True})]
    return [Action(Op.PLACE_COUNTERS, amt, Target.OPP_ANY,
                   {"targets": int(who), "attack_damage": True})]


@rule("asymmetric_hand_reset",
      r"each player shuffles their hand into their deck\. then, you draw "
      r"(\d+) cards?, and your opponent draws (\d+) cards?")
def _r(m, text):
    """Unfair Stamp. The generic "each player draws N" rule read this as
    BOTH players drawing 5, handing the opponent three free cards off a
    card whose whole point is that the draw is lopsided in your favour."""
    return [Action(Op.DRAW, int(m.group(1)), Target.SELF),
            Action(Op.SET_OPPONENT_HAND, int(m.group(2)), Target.OPPONENT)]


@rule("coin_flip_discard_opponent_energy",
      r"flip a coin\. if heads, discard an energy from 1 of your "
      r"opponent'?s pok[eé]mon")
def _r(m, text):
    """Crushing Hammer -- four copies in both of the current top meta
    Dragapult lists, and it compiled to nothing at all."""
    eff = [Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 1, Target.OPP_ANY)]
    return eff


@rule("search_energy_split",
      r"search your deck for up to 2 basic energy cards of different types,"
      r" reveal them, and put 1 of them into your hand\. attach the other")
def _r(m, text):
    """Crispin. Only the search half compiled, so the card fetched Energy
    and never accelerated any -- and acceleration is the entire reason the
    current Dragapult lists play it, to pay Phantom Dive's two colours."""
    # "of DIFFERENT types" is a real restriction: in a mono-Energy deck the
    # card can only ever find one, so it yields one Energy and not two.
    # Unflagged, water_aggro (12 Basic Water and nothing else) got both
    # halves off a card that cannot pay for them.
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF,
                   {"stage": "Basic", "kind": "energy", "records_type": True}),
            Action(Op.ATTACH_ENERGY, 1, Target.YOUR_ANY,
                   {"from": "deck", "different_type": True})]


@rule("discard_own_energy_cost",
      r"discard (all|a|an|\d+) (?:(grass|fire|water|lightning|psychic|fighting|"
      r"darkness|metal|dragon|fairy|colorless) )?energy (?:cards? )?from this "
      r"pok[eé]mon")
def _r(m, text):
    """59 attacks pay for themselves by dumping their own Energy and none
    of them did. Ceruledge ex's Raging Amethyst and Cynthia's Garchomp
    ex's Draconic Buster are supposed to discard ALL Energy and rebuild;
    instead they fired at full price every turn, forever.

    Attacks worded "... for each card you discarded in this way" are a
    different shape -- the amount is chosen at attack time and both the
    damage and the payment are handled together in simulate_versus -- so
    they are left alone here to avoid charging twice.
    """
    if re.search(r"discarded in this way", text, re.I):
        return []
    n = m.group(1).lower()
    amount = None if n == "all" else (1 if n in ("a", "an") else int(n))
    filt = {"type": m.group(2).capitalize()} if m.group(2) else {}
    return [Action(Op.DISCARD_SELF_ENERGY, amount, Target.SELF, filt)]


@rule("self_damage_recoil",
      r"this pok[eé]mon (?:also )?do(?:es)? (\d+) damage to itself")
def _r(m, text):
    """Recoil. 75 attacks in the pool say this and not one of them
    compiled, so every recoil attacker in the format was swinging for
    free -- Koraidon ex's Kaiser Tackle took 60 a turn it never paid.
    """
    return [Action(Op.SELF_DAMAGE, int(m.group(1)), Target.SELF)]


@rule("bench_cap",
      r"can have up to (\d+) pok[eé]mon on their bench")
def _r(m, text):
    """Area Zero Underdepths. The Bench limit was a hard constant of 5, so
    the Stadium that raises it to 8 for a player with a Tera Pokemon in
    play did nothing at all -- in a deck built on a Tera attacker, three
    Bench slots is a third of the board."""
    filt = {}
    mm = re.search(r"each player who has any ([\w' -]+?) pok[eé]mon in play",
                   text, re.I)
    if mm:
        filt["requires_subtype"] = mm.group(1).strip().title()
    return [Action(Op.BENCH_CAP, int(m.group(1)), Target.BOTH_ALL, filt)]


@rule("attack_gate",
      r"this pok[eé]mon can'?t attack unless you have (\d+) or more "
      r"([\w'’ -]+?) pok[eé]mon in play")
def _r(m, text):
    """Team Rocket's Mewtwo ex's Power Saver and friends.

    This MUST sit above the generic "lock" rule, which matched "can't
    attack" and threw the whole "unless ..." clause away -- compiling a
    conditional gate into an unconditional one. Nothing consumed it
    either, so in practice the gate simply did not exist and a deck with
    four Team Rocket's Pokemon in sixty cards attacked freely.
    """
    return [Action(Op.ATTACK_GATE, int(m.group(1)), Target.SELF,
                   {"family": m.group(2).strip()})]


@rule("lock", r"can'?t (attack|retreat|play|use)")
def _r(m, text):
    # "can't attack UNLESS ..." is a conditional gate, owned by the
    # attack_gate rule above. Falling through to here as well stapled an
    # unconditional attack lock onto the same card, which would stop it
    # attacking even with the requirement met.
    if re.search(r"can'?t attack unless", text, re.I):
        return []
    # "You can't use more than 1 Last-Ditch Catch Ability each turn" is a
    # once-per-turn limit on the card's own Ability, not a lock: it
    # compiled Meowth ex as a self-lock and dropped its Supporter search.
    if re.match(r"can'?t use more than", m.group(0) + text[m.end():m.end() + 12], re.I):
        return []
    what = m.group(1).lower()
    # "the Defending Pokemon can't USE ATTACKS" is an attack lock. It
    # compiled as what="use", which the executor does not know, so every
    # one of these (Cubchoo's Snotted Up, N's Vanillish, Cobalion ex; 16
    # cards) did nothing at all.
    if what == "use" and re.match(r"\s+attacks", text[m.end():], re.I):
        what = "attack"
    tgt = Target.OPPONENT if "your opponent" in text.lower() else Target.SELF
    return [Action(Op.LOCK, None, tgt, {"what": what})]


@rule("discard_from_opponent", r"discard[^.]{0,40}from your opponent's hand")
def _r(m, text):
    mm = re.search(r"discard (\d+|a|an) ", m.group(0), re.I)
    return [Action(Op.DISCARD_FROM_OPPONENT, _num(mm.group(1) if mm else "a"), Target.OPPONENT)]


# ---- second pass: shapes found by auditing what the first pass missed ----

@rule("heal_all", r"heal all damage from ([^.]{0,50})")
def _r(m, text):
    return [Action(Op.HEAL, None, parse_target(m.group(1)), {"all": True})]


@rule("search_bench_loose",
      r"search your deck for (?:up to )?(\d+|a|an) ([\w'’ -]*?)pok[eé]mon[^.]{0,80}?put (?:it|them) onto your bench")
def _r(m, text):
    # Wider window than search_to_bench, for phrasings that put more words
    # between the noun and "onto your Bench". Shares the qualifier parser
    # so it does not re-emit the same action with a junk name filter.
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   _bench_name_filter(m))]


@rule("move_energy_between_yours",
      r"move (?:a|an|(\d+)) ?(?:basic )?(" + TYPES + r")? ?energy from 1 of your pok[eé]mon to another")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, _num(m.group(1)), Target.YOUR_ANY,
                   {"type": (m.group(2) or "").capitalize() or None, "from": Target.YOUR_ANY})]


@rule("ability_lock", r"(?:has|have) no abilities")
def _r(m, text):
    tgt = Target.OPP_ALL
    seg = text.lower()
    if "your opponent's active" in seg:
        tgt = Target.OPP_ACTIVE
    elif "both yours and your opponent" in seg:
        tgt = Target.BOTH_ALL
    filt = {}
    mm = re.search(r"(" + TYPES + r") pok[eé]mon in play", text, re.I)
    if mm:
        filt["type"] = mm.group(1).capitalize()
    if "rule box" in seg:
        filt["rule_box_only"] = True
    return [Action(Op.LOCK, None, tgt, dict(filt, what="abilities"))]


@rule("modify_retreat", r"retreat cost[^.]{0,40}?is (" + TYPES + r") (more|less)")
def _r(m, text):
    sign = 1 if m.group(2).lower() == "more" else -1
    tgt = Target.OPP_ACTIVE if "your opponent" in text.lower() else Target.SELF
    filt = {}
    # Ariados's Big Net taxes only an "Active Evolution Pokemon" -- it does
    # nothing against the Basic attackers a lot of the format runs, so the
    # restriction has to survive compilation.
    if re.search(r"active evolution pok[eé]mon", text, re.I):
        filt["stage_not"] = "Basic"
    return [Action(Op.MODIFY_RETREAT, sign, tgt, filt)]


@rule("no_retreat_cost", r"(?:has|have) no retreat cost")
def _r(m, text):
    tgt = Target.YOUR_ALL if re.search(r"all of your|your basic", text, re.I) else Target.SELF
    filt = {}
    # Latias ex's Skyliner frees your BASIC Pokemon only.
    if re.search(r"your basic pok[eé]mon", text, re.I):
        filt["stage"] = "Basic"
    return [Action(Op.MODIFY_RETREAT, -99, tgt, filt)]


@rule("opponent_attack_cost", r"attacks used by your opponent's ([\w' ]*?)pok[eé]mon cost (" + TYPES + r") more")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, 1, Target.OPP_ALL,
                   {"type": m.group(2).capitalize(), "family": m.group(1).strip() or None})]


@rule("look_top_and_discard", r"look at the top card of your deck")
def _r(m, text):
    return [Action(Op.LOOK_AT_DECK, 1, Target.SELF,
                   {"may_discard": bool(re.search(r"discard that card", text, re.I))})]


@rule("shuffle_self_effect",
      r"you may shuffle (?:it|this pok[eé]mon) and all attached cards into your deck")
def _r(m, text):
    return [Action(Op.SHUFFLE_SELF_INTO_DECK, 1, Target.SELF)]


@rule("endure_ko", r"(?:it|this pok[eé]mon) is not knocked out")
def _r(m, text):
    return [Action(Op.ENDURE, None, Target.SELF)]


@rule("switch_self_in", r"switch it with your active pok[eé]mon")
def _r(m, text):
    f = {"gust": False}
    # Iron Leaves ex's Rapid Vernier: "switch IT" is the Pokemon just
    # played, not a Benched Pokemon of your choice.
    if re.search(r"when you play this pok[eé]mon from your hand", text, re.I):
        f["self_in"] = True
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, f)]


@rule("prevent_card_effects",
      r"prevent all effects of that card done to ([^.]{0,50})")
def _r(m, text):
    return [Action(Op.PREVENT_DAMAGE, None, parse_target(m.group(1)),
                   {"effects_only": True, "source": "trainer_card"})]


@rule("cannot_be_returned_to_hand", r"can'?t be put into your opponent'?s hand")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.OPPONENT, {"what": "return_to_hand"})]


@rule("attach_multi_type_energy",
      r"attach (?:up to )?(\d+|a|an) basic (" + TYPES + r") energy card[^.]{0,80}?from your (discard pile|hand|deck)")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, _num(m.group(1)), Target.YOUR_ANY,
                   {"type": m.group(2).capitalize(), "from": m.group(3).split()[0]})]


# ---- third pass ----------------------------------------------------------

@rule("make_condition", r"make your opponent'?s active pok[eé]mon (asleep|burned|confused|paralyzed|poisoned)")
def _r(m, text):
    return [Action(Op.APPLY_CONDITION, None, Target.OPP_ACTIVE,
                   {"conditions": [m.group(1).lower()]})]


@rule("prevent_effects_of_attacks_abilities",
      r"prevent all effects of your opponent'?s pok[eé]mon'?s (?:attacks and abilities|abilities|attacks)[^.]{0,40}done to ([^.(]{0,40})")
def _r(m, text):
    return [Action(Op.PREVENT_DAMAGE, None, parse_target(m.group(1)),
                   {"effects_only": True})]


@rule("opponent_attacks_do_less",
      r"attacks used by your opponent'?s ([\w' ]*?)pok[eé]mon[^.]{0,60}?do (\d+) less damage")
def _r(m, text):
    return [Action(Op.REDUCE_DAMAGE, int(m.group(2)), Target.SELF,
                   {"applies_to_opponent_attacks": True,
                    "family": (m.group(1) or "").strip() or None})]


@rule("mill_opponent", r"discard the (?:top|bottom) (?:(\d+) )?cards? of your opponent'?s deck")
def _r(m, text):
    # "Flip a coin for each Maushold you have in play. FOR EACH HEADS,
    # discard the top 2 cards of your opponent's deck." The mill is not a
    # flat amount -- it happens once per heads, and the number of coins is
    # itself a board count. Maushold's Gnaw Together is the only card in
    # the pool with this shape; the other seven "flip a coin for each X ...
    # for each heads" attacks all scale DAMAGE, which attack_damage owns.
    per = re.search(r"flip a coin for each ([^.]+)\.", text, re.I)
    if per and re.search(r"for each heads", text, re.I):
        return [Action(Op.MILL_OPPONENT, _num(m.group(1)), Target.OPPONENT,
                       {"per_heads": per.group(1).strip()})]
    return [Action(Op.MILL_OPPONENT, _num(m.group(1)), Target.OPPONENT)]


@rule("discard_stadium", r"discard a stadium in play")
def _r(m, text):
    return [Action(Op.DISCARD_STADIUM, 1, Target.BOTH_ALL)]


@rule("search_energy_attach_loose",
      r"search your deck for[^.]{0,90}?energy cards?[^.]{0,60}?attach")
def _r(m, text):
    mm = re.search(r"up to (\d+)", m.group(0))
    return [Action(Op.ATTACH_ENERGY, _num(mm.group(1) if mm else "a"), Target.YOUR_ANY,
                   {"from": "deck"})]


@rule("attach_energy_from_discard_loose",
      r"attach up to (\d+) basic energy cards? from your discard pile")
def _r(m, text):
    # attach_named_energy_from_discard matches the same sentence and
    # produces its own attach, so emitting one here too doubled the
    # acceleration -- Rosa's Encouragement attached FOUR Energy off a card
    # that says up to two.
    if re.search(r"attach up to \d+ basic energy cards? from your discard "
                 r"pile to 1 of your", text, re.I):
        return []
    return [Action(Op.ATTACH_ENERGY, int(m.group(1)), Target.YOUR_ANY, {"from": "discard"})]


@rule("evolve_early", r"can evolve during your first turn or the turn you play it")
def _r(m, text):
    return [Action(Op.EVOLVE_EARLY, None, Target.SELF)]


@rule("checkup_bonus_counters",
      r"put (\d+) more damage counters on your opponent'?s (\w+) pok[eé]mon during pok[eé]mon checkup")
def _r(m, text):
    return [Action(Op.BUFF_CONDITION_DAMAGE, int(m.group(1)), Target.OPP_ALL,
                   {"condition": m.group(2).lower()})]


@rule("devolve",
      r"devolve (1|each) of your opponent'?s evolved pok[eé]mon"
      r"|if your opponent'?s active pok[eé]mon is an evolved pok[eé]mon,"
      r" (devolve) it")
def _r(m, text):
    """Espeon ex's Amazez devolves the WHOLE board, not one Pokemon --
    the "each" wording had no rule and the attack compiled to nothing."""
    # Where the Evolution card goes is printed on every one of these
    # cards, and it is never the discard pile: five say "into your
    # opponent's hand", Espeon ex says "shuffling ... into your opponent's
    # deck".
    to = "deck" if re.search(r"shuffl\w+ the highest stage evolution card"
                             r"[^.]{0,40}into your opponent'?s deck",
                             text, re.I) else "hand"
    if (m.group(1) or "").lower() == "each":
        return [Action(Op.DEVOLVE, 99, Target.OPP_ALL, {"to": to})]
    return [Action(Op.DEVOLVE, 1, Target.OPP_ANY, {"to": to})]


@rule("ko_active_outright",
      r"discard your opponent'?s active pok[eé]mon and all attached cards")
def _r(m, text):
    """Team Rocket's Moltres ex's Evil Incineration removes the Active
    outright. Scored on damage it read as a 0-damage attack."""
    return [Action(Op.CONDITIONAL_KO, 0, Target.OPP_ACTIVE,
                   {"unconditional": True})]


@rule("flip_ko_a_basic",
      r"flip a coin\. if heads, knock out your opponent'?s active basic "
      r"pok[eé]mon")
def _r(m, text):
    """Alolan Exeggutor ex's Swinging Sphene. Either side of the flip is a
    Knock Out -- heads the Active, tails a Benched one -- so it is a
    guaranteed Knock Out on a Basic, which is not a 0-damage attack."""
    return [Action(Op.CONDITIONAL_KO, 0, Target.OPP_ANY,
                   {"basic_only": True})]


@rule("spread_choose_n_times",
      r"choose 1 of your opponent'?s pok[eé]mon (\d+) times.*?"
      r"do (\d+) damage to it")
def _r(m, text):
    """Arboliva ex's Oil Salvo: six separate 20s aimed anywhere. Worth 120
    spread across the board, and it compiled to nothing."""
    return [Action(Op.PLACE_COUNTERS, int(m.group(2)) // 10, Target.OPP_ANY,
                   {"targets": int(m.group(1)), "attack_damage": True})]


@rule("flip_per_opponent_pokemon",
      r"for each of your opponent'?s pok[eé]mon, flip a coin\. if heads, "
      r"this attack does (\d+) damage to that pok[eé]mon")
def _r(m, text):
    """Mega Zygarde ex's Nullifying Zero: a coin per opposing Pokemon, 150
    on each heads. Expected value across a full board is the biggest
    single attack in the pool, and it scored zero."""
    return [Action(Op.PLACE_COUNTERS, int(m.group(1)) // 10, Target.OPP_ALL,
                   {"chance_each": 0.5, "attack_damage": True})]


@rule("each_player_draws", r"each player draws? (?:a card|(\d+) cards?)")
def _r(m, text):
    return [Action(Op.DRAW, _num(m.group(1)), Target.BOTH_ALL)]


@rule("retreat_multi_less", r"retreat cost is (?:colorless){2,} less")
def _r(m, text):
    tgt = Target.YOUR_ACTIVE if "your active" in text.lower() else Target.SELF
    return [Action(Op.MODIFY_RETREAT, -2, tgt)]


@rule("modify_prizes", r"(?:takes? 1 fewer prize card|can'?t take any prize cards)")
def _r(m, text):
    fewer = -99 if "can't take any" in m.group(0).lower() else -1
    return [Action(Op.MODIFY_PRIZE, fewer, Target.OPPONENT)]


@rule("condition_immunity", r"can'?t be (asleep|burned|confused|paralyzed|poisoned)")
def _r(m, text):
    return [Action(Op.CONDITION_IMMUNITY, None, Target.SELF,
                   {"conditions": [m.group(1).lower()]})]


# Blanket immunity. Ten Standard-legal cards say "can't be affected by any
# Special Conditions" rather than naming one, and the narrow rule above
# matched none of them -- the seven Antique Fossils, Ancient Booster Energy
# Capsule, Bubbly Water Energy and Festival Grounds.
@rule("condition_immunity_all",
      r"can'?t be affected by (?:any )?special conditions")
def _r(m, text):
    t = text.lower()
    if "both yours and your opponent" in t:
        tgt = Target.BOTH_ALL
    elif re.search(r"\byour pok[eé]mon\b", t):
        tgt = Target.YOUR_ALL
    else:
        tgt = Target.SELF
    f = {"conditions": sorted(ALL_SPECIAL_CONDITIONS)}
    # Festival Grounds only shelters a Pokemon with Energy on it, which is
    # the whole cost of the effect.
    if re.search(r"has any energy attached", t):
        f["requires_energy"] = True
    return [Action(Op.CONDITION_IMMUNITY, None, tgt, f)]


@rule("move_energy_any_amount",
      r"move any amount of (" + TYPES + r")? ?energy from ([^.]{0,40}?) to ([^.]{0,40})")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, None, parse_target(m.group(3)),
                   {"type": (m.group(1) or "").capitalize() or None,
                    "from": parse_target(m.group(2)), "any_amount": True})]


@rule("evolve_from_deck_ascension",
      r"search your deck for a card that evolves from (?:this|that|1 of your)"
      r" [^.]{0,30}?pok[eé]mon and put it onto (?:this|that) pok[eé]mon to evolve it")
def _r(m, text):
    """Ascension, Cellular Evolution, Evo-Powder and the rest of that family.

    These used to fall through to search_any_card and compile to "search
    your deck for a card, any card, into your hand" -- verified by
    execution to pull an Ultra Ball out of a deck holding no Pokemon at
    all. That is a universal tutor AND it skipped the evolution the card
    is entirely about. EVOLVE_FROM_DECK already exists with an executor
    that matches on evolves_from and respects evolved_this_turn.

    "For each of your Benched Pokemon" (Reuniclus, Vivillon) evolves the
    whole Bench, so the amount is the Bench cap rather than one.
    """
    each = bool(re.search(r"for each of your benched pok[eé]mon", text, re.I))
    f = {}
    if each:
        f["bench_only"] = True
    elif re.search(r"evolves from this pok[eé]mon", text, re.I):
        f["self"] = True                  # Ascension: this Pokemon only
    return [Action(Op.EVOLVE_FROM_DECK, 5 if each else 1,
                   Target.SELF if f.get("self") else Target.YOUR_ANY, f)]


@rule("search_any_card", r"search your deck for a card\b")
def _r(m, text):
    # "a card that evolves from ..." is handled above as an evolution; if
    # this fired too the card would ALSO tutor something unrelated.
    if re.search(r"a card that evolves from", text, re.I):
        return []
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "card"})]


# Ciphermaniac's Codebreaking. Modelled exactly rather than as a search:
# the cards go on TOP of the deck, so they arrive next turn's draw, and
# treating that as "into your hand" would make the card a strictly faster
# Ultra Ball than the one that is printed.
@rule("search_to_top_of_deck",
      r"search your deck for (\d+|a|an) cards?[^.]{0,60}?"
      r"put (?:those|that) cards? on top of it")
def _r(m, text):
    return [Action(Op.SEARCH_TO_TOP_OF_DECK, _num(m.group(1)), Target.SELF)]


# Redeemable Ticket. Prize cards are real cards in this engine -- dealt off
# the deck at setup and taken into hand on a Knock Out -- so re-rolling
# them genuinely changes which cards the deck can still reach. A deck that
# prized its one copy of something gets another roll at it.
@rule("reroll_prizes",
      r"count your prize cards, shuffle them, and put them on the bottom"
      r" of your deck")
def _r(m, text):
    return [Action(Op.REROLL_PRIZES, None, Target.SELF)]


# Seven rider shapes that compiled to nothing at all. Counts are attacks in
# the pool carrying each.
@rule("force_switch_opponent",                                  # 11
      r"switch out your opponent'?s active pok[eé]mon to the bench")
def _r(m, text):
    return [Action(Op.FORCE_SWITCH_OPPONENT, None, Target.OPPONENT)]


@rule("discard_tool_from_opponent",                             # 6
      r"discard (?:all|a|any) pok[eé]mon tools? from your opponent'?s active")
def _r(m, text):
    return [Action(Op.DISCARD_TOOL_FROM_OPPONENT, None, Target.OPP_ACTIVE)]


@rule("self_bench_damage",                                      # 5
      r"this attack also does (\d+) damage to each of your benched pok[eé]mon")
def _r(m, text):
    return [Action(Op.SELF_BENCH_DAMAGE, int(m.group(1)), Target.YOUR_BENCHED)]


@rule("self_energy_to_hand",                                    # 4
      r"put an energy attached to this pok[eé]mon into your hand")
def _r(m, text):
    return [Action(Op.SELF_ENERGY_TO_HAND, 1, Target.SELF)]


@rule("weaken_defender",                                        # 10
      r"during your opponent'?s next turn, attacks used by the defending"
      r" pok[eé]mon do (\d+) less damage")
def _r(m, text):
    return [Action(Op.WEAKEN_DEFENDER, int(m.group(1)), Target.OPP_ACTIVE)]


@rule("heal_as_dealt",                                          # 5
      r"heal from this pok[eé]mon the same amount of damage you did")
def _r(m, text):
    return [Action(Op.HEAL_AS_DEALT, None, Target.SELF)]


# ---- the long tail of one-off attack riders -------------------------------
# Each of these appears on one to three attacks. They are here because the
# alternative is a pool where 6% of attacks silently do half of what they
# say, and because the shapes recur in every new set.

@rule("self_to_hand",
      r"put this pok[eé]mon and all attached cards into your hand"
      r"|you may put this pok[eé]mon into your hand")
def _r(m, text):
    return [Action(Op.SELF_TO_HAND, 1, Target.SELF)]


@rule("self_to_deck",
      r"shuffle this pok[eé]mon and all attached cards into your deck")
def _r(m, text):
    return [Action(Op.SELF_TO_DECK, 1, Target.SELF)]


@rule("self_discard_now", r"discard this pok[eé]mon and all attached cards")
def _r(m, text):
    return [Action(Op.SELF_DISCARD, 1, Target.SELF)]


@rule("bench_to_hand",
      r"put (\d+) of your benched pok[eé]mon and all attached cards into your hand")
def _r(m, text):
    return [Action(Op.BENCH_TO_HAND, int(m.group(1)), Target.YOUR_BENCHED)]


@rule("bench_to_deck",
      r"shuffle (\d+) of your benched pok[eé]mon and all attached cards into"
      r" your deck")
def _r(m, text):
    return [Action(Op.SELF_TO_DECK, int(m.group(1)), Target.YOUR_BENCHED)]


# NOTE the [^.] -> [\s\S] here. "Choose 2 of your opponent's Benched
# Pokemon. Shuffle those Pokemon ... into your opponent's deck." puts a FULL
# STOP between the two halves, and a [^.] bridge cannot cross it. That is
# the third time this exact mistake has cost a card in this project
# (parse_chance's coin flips, and the flat-bonus bridge before it).
@rule("opp_bench_to_deck",
      r"choose (\d+) of your opponent'?s benched pok[eé]mon[\s\S]{0,60}?shuffle"
      r"[\s\S]{0,60}?into your opponent'?s deck"
      r"|shuffle (\d+) of your opponent'?s benched pok[eé]mon and all attached"
      r" cards into their deck")
def _r(m, text):
    n = m.group(1) or m.group(2) or 1
    return [Action(Op.OPP_BENCH_TO_DECK, int(n), Target.OPP_BENCHED)]


@rule("opp_energy_to_hand",
      r"you may put (\d+) energy attached to your opponent'?s active"
      r"[\w ]*? pok[eé]mon into their hand")
def _r(m, text):
    return [Action(Op.OPP_ENERGY_TO_HAND, int(m.group(1)), Target.OPP_ACTIVE)]


@rule("discard_special_energy_from_opponent",
      r"discard (?:a|all) special energy from (?:your opponent'?s active"
      r" pok[eé]mon|all of your opponent'?s pok[eé]mon)")
def _r(m, text):
    board = "all of your opponent" in text.lower()
    return [Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 99 if board else 1,
                   Target.OPP_ALL if board else Target.OPP_ACTIVE,
                   {"special": True})]


@rule("discard_tools_and_special_energy",
      r"discard all pok[eé]mon tools and special energy from"
      r" (?:your opponent'?s active pok[eé]mon|all of your opponent'?s pok[eé]mon)")
def _r(m, text):
    board = "all of your opponent" in text.lower()
    return [Action(Op.DISCARD_TOOL_FROM_ALL_OPPONENT if board
                   else Op.DISCARD_TOOL_FROM_OPPONENT, None,
                   Target.OPP_ALL if board else Target.OPP_ACTIVE),
            Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 99 if board else 1,
                   Target.OPP_ALL if board else Target.OPP_ACTIVE,
                   {"special": True})]


@rule("discard_tools_from_opponent_pokemon",
      r"discard up to (\d+) pok[eé]mon tools? from your opponent'?s pok[eé]mon")
def _r(m, text):
    return [Action(Op.DISCARD_TOOL_FROM_ALL_OPPONENT, int(m.group(1)),
                   Target.OPP_ALL)]


@rule("recover_to_bench",
      r"put up to (\d+) ([\w'’ -]*?) ?(?:pok[eé]mon )?from your discard pile"
      r" onto your bench")
def _r(m, text):
    f = {}
    what = (m.group(2) or "").strip()
    if what and what.lower() not in ("basic", ""):
        if re.fullmatch(TYPES, what, re.I):
            f["type"] = what.capitalize()
        else:
            f["name_contains"] = what
    return [Action(Op.RECOVER_TO_BENCH, int(m.group(1)), Target.YOUR_BENCHED, f)]


@rule("search_combination_to_bench",
      r"search your deck for up to (\d+) in any combination of ([\w'’ ]+?) and"
      r" [\w'’ ]+? and put them onto your bench")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, int(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": m.group(2).strip()})]


@rule("ko_by_property",
      r"if your opponent'?s active pok[eé]mon (?:has any special energy attached|"
      r"is a basic pok[eé]mon), it is knocked out")
def _r(m, text):
    f = ({"requires_special_energy": True}
         if "special energy" in text.lower() else {"stage": "Basic"})
    return [Action(Op.KO_OUTRIGHT, 1, Target.OPP_ACTIVE, f)]


# Team Rocket's Exeggutor's Tri Kinesis: "Flip 3 coins. If all of them are
# heads, Knock Out 1 of your opponent's Pokemon." The flip is the effect's
# chance (parse_chance); the target is any of theirs, so the best Prize.
@rule("ko_any_opponent", r"knock out 1 of your opponent'?s pok[eé]mon")
def _r(m, text):
    # "...1 of your opponent's Pokemon that has exactly 6 damage counters"
    # is conditional_ko's (Glaceon ex's Euclase).
    if re.match(r"\s+that ", text[m.end():]):
        return []
    return [Action(Op.KO_OUTRIGHT, 1, Target.OPP_ANY, {"choose": True})]


@rule("ko_both_actives", r"both active pok[eé]mon are knocked out")
def _r(m, text):
    return [Action(Op.KO_OUTRIGHT, 1, Target.OPP_ACTIVE),
            Action(Op.SELF_KO, 1, Target.SELF)]


@rule("ko_lowest_hp",
      r"choose a pok[eé]mon in play \(yours or your opponent'?s\) that has the"
      r" least hp remaining, except for this pok[eé]mon, and it is knocked out")
def _r(m, text):
    return [Action(Op.KO_OUTRIGHT, 1, Target.BOTH_ALL, {"lowest_hp": True})]


@rule("buff_named_attack_next_turn",
      r"during your next turn, this pok[eé]mon'?s ([\w'’ -]+?) attack"
      r"(?:'?s base damage is (\d+)| does (\d+) more damage)")
def _r(m, text):
    if m.group(2):
        return [Action(Op.BUFF_NAMED_ATTACK_NEXT_TURN, int(m.group(2)),
                       Target.SELF, {"attack": m.group(1).strip(),
                                     "absolute": True})]
    return [Action(Op.BUFF_NAMED_ATTACK_NEXT_TURN, int(m.group(3)),
                   Target.SELF, {"attack": m.group(1).strip()})]


@rule("defender_takes_more",
      r"during your next turn, the defending pok[eé]mon takes (\d+) more damage"
      r" from attacks")
def _r(m, text):
    return [Action(Op.DEFENDER_TAKES_MORE, int(m.group(1)), Target.OPP_ACTIVE)]


@rule("set_base_damage_on_condition",
      r"this attack'?s base damage is (\d+)")
def _r(m, text):
    return [Action(Op.SET_BASE_DAMAGE, int(m.group(1)), Target.SELF)]


@rule("self_clear_conditions", r"this pok[eé]mon recovers from all special conditions")
def _r(m, text):
    return [Action(Op.CLEAR_CONDITIONS, None, Target.SELF)]


@rule("opponent_hand_to_deck_random",
      r"choose a random card from your opponent'?s hand[,.]? (?:and )?your"
      r" opponent reveals that card and shuffles it into their deck")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_OPPONENT, 1, Target.OPPONENT,
                   {"to": "deck"})]


@rule("opponent_chooses_to_deck",
      r"your opponent chooses (\d+) cards? from their hand and shuffles those"
      r" cards into their deck")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_OPPONENT, int(m.group(1)), Target.OPPONENT,
                   {"to": "deck"})]


@rule("opponent_discards_n",
      r"your opponent discards (\d+|a) cards? from their hand")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_OPPONENT, _num(m.group(1)), Target.OPPONENT)]


@rule("trade_a_discard",
      r"discard a card from your hand\. if you do, your opponent discards a"
      r" card from their hand")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_SELF, 1, Target.SELF),
            Action(Op.DISCARD_FROM_OPPONENT, 1, Target.OPPONENT)]


@rule("may_discard_any_hand", r"you may discard any number of cards from your hand")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_SELF, 0, Target.SELF)]


@rule("bench_splash",
      r"this attack also does (\d+) damage to (each|\d+) benched pok[eé]mon"
      r"(?: that has any damage counters on it)? \(both yours and your"
      r" opponent'?s\)"
      r"|this attack also does (\d+) damage to (\d+) of your benched pok[eé]mon")
def _r(m, text):
    t = text.lower()
    if m.group(1):
        amount, who = int(m.group(1)), m.group(2)
        n = None if who == "each" else int(who)
        f = {"side": "both"}
        if "damage counters on it" in t:
            f["damaged_only"] = True
    else:
        amount, n, f = int(m.group(3)), int(m.group(4)), {"side": "yours"}
    return [Action(Op.BENCH_SPLASH, amount, Target.BOTH_ALL,
                   dict(f, count=n))]


@rule("defender_attack_may_fail",
      r"during your opponent'?s next turn, if the defending pok[eé]mon tries to"
      r" use an attack, your opponent flips (a coin|\d+ coins)")
def _r(m, text):
    odds = 0.5 if m.group(1) == "a coin" else 0.75   # "if either is tails"
    return [Action(Op.LOCK, None, Target.OPP_ACTIVE,
                   {"what": "attack", "chance_to_block": odds})]


@rule("no_energy_attach_to_defender",
      r"during your opponent'?s next turn, energy can'?t be attached from your"
      r" opponent'?s hand to the defending pok[eé]mon"
      r"|during your opponent'?s next turn, if they attach an energy card from"
      r" their hand to the defending pok[eé]mon, their turn ends")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.OPP_ACTIVE, {"what": "attach_energy"})]


@rule("delayed_discard_defender",
      r"at the end of your opponent'?s next turn, discard the defending"
      r" pok[eé]mon and all attached cards")
def _r(m, text):
    return [Action(Op.DELAYED_DISCARD_DEFENDER, 1, Target.OPP_ACTIVE)]


@rule("extra_prize_on_ko",
      r"during your next turn, if the defending pok[eé]mon is knocked out,"
      r" take (\d+) more prize cards?")
def _r(m, text):
    return [Action(Op.EXTRA_PRIZE_ON_KO, int(m.group(1)), Target.OPP_ACTIVE)]


@rule("self_takes_more",
      r"during your opponent'?s next turn, this pok[eé]mon takes (\d+) more"
      r" damage from attacks")
def _r(m, text):
    return [Action(Op.SELF_TAKES_MORE, int(m.group(1)), Target.SELF)]


@rule("remove_own_weakness",
      r"during your opponent'?s next turn, this pok[eé]mon has no weakness")
def _r(m, text):
    return [Action(Op.REMOVE_WEAKNESS, None, Target.SELF)]


@rule("set_defender_weakness_colorless",
      r"the defending pok[eé]mon'?s weakness is now colorless")
def _r(m, text):
    return [Action(Op.SET_WEAKNESS, None, Target.OPP_ACTIVE,
                   {"to_type": "Colorless"})]


@rule("move_all_energy_to_bench",
      r"move all energy from this pok[eé]mon to (?:(\d+) of )?your benched"
      r" pok[eé]mon")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, 99, Target.YOUR_BENCHED,
                   {"from": Target.SELF})]


@rule("move_basic_energy_to_bench",
      r"move a basic energy from this pok[eé]mon to (\d+) of your benched"
      r" pok[eé]mon")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, 1, Target.YOUR_BENCHED,
                   {"from": Target.SELF})]


@rule("attach_any_basic_from_hand",
      r"(?:you|each player) may attach (?:any number of|up to \d+) basic energy"
      r" cards? from (?:your|their) hand to (?:your|their) pok[eé]mon")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, 2, Target.YOUR_ANY, {"from": "hand"})]


@rule("move_counters_bench_to_opponent",
      r"move all damage counters from (\d+) of your benched ([\w'’ ]*?) ?"
      r"pok[eé]mon to (?:your opponent'?s active pok[eé]mon|\d+ of your"
      r" opponent'?s pok[eé]mon)")
def _r(m, text):
    f = {}
    fam = (m.group(2) or "").strip()
    if fam:
        f["family"] = fam
    return [Action(Op.MOVE_COUNTERS, 99, Target.OPP_ACTIVE,
                   dict(f, **{"from": Target.YOUR_BENCHED}))]


@rule("information_only",
      r"look at the top (?:\d+ cards?|card) of your opponent'?s deck"
      r"|look at \d+ of your opponent'?s face-down prize cards")
def _r(m, text):
    # Deliberately a no-op with a name: the engine has no hidden information
    # for a player to act on, so there is nothing to model -- but leaving it
    # UNSUPPORTED made these read as gaps in every audit.
    return [Action(Op.NO_OP_INFORMATION, None, Target.SELF)]


@rule("keep_n_of_opponent_bench",
      r"choose (\d+) of your opponent'?s benched pok[eé]mon\. if you do,"
      r" shuffle all of your opponent'?s benched pok[eé]mon that you didn'?t"
      r" choose")
def _r(m, text):
    # Shiftry's Expelling Tornado keeps N and shuffles the REST away, which
    # is the inverse of every other Bench-bounce in the pool.
    # KEEPS N and shuffles the REST away -- the inverse of every other
    # Bench-bounce in the pool, so the count is a keep, not a take.
    return [Action(Op.OPP_BENCH_TO_DECK, None, Target.OPP_BENCHED,
                   {"keep": int(m.group(1))})]


@rule("free_cost_when_conditioned",
      r"if this pok[eé]mon is affected by a special condition, ignore all"
      r" energy in this attack'?s cost")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, -99, Target.SELF)]


@rule("cost_becomes_type_when_damaged",
      r"if this pok[eé]mon has any damage counters on it, this attack can be"
      r" used for (" + TYPES + r")")
def _r(m, text):
    # "can be used for Fighting" means the printed cost is replaced by a
    # single Energy of that type.
    return [Action(Op.MODIFY_ATTACK_COST, -99, Target.SELF,
                   {"cost_becomes": 1, "type": m.group(1).capitalize()})]


@rule("opponent_attaches_from_their_discard",
      r"attach up to (\d+) energy cards? from your opponent'?s discard pile to"
      r" their pok[eé]mon")
def _r(m, text):
    return [Action(Op.OPP_ATTACH_FROM_DISCARD, int(m.group(1)), Target.OPP_ANY)]


@rule("damaged_last_turn_reflects_damage",
      r"if this pok[eé]mon was damaged by an attack during your opponent'?s"
      r" last turn, this attack does that much more damage")
def _r(m, text):
    # The bonus is the damage this Pokemon took, so there is no number in
    # the text for the flat-bonus path to read. attack_damage resolves it.
    return [Action(Op.NO_OP_INFORMATION, None, Target.SELF,
                   {"handled_by": "damage_model"})]


@rule("retaliate_counters",
      r"during your opponent'?s next turn, if this pok[eé]mon is damaged by an"
      r" attack[\s\S]{0,40}?, put (?:(\d+) damage counters?|damage counters)"
      r" on the attacking pok[eé]mon"
      r"(?: equal to the damage done to this pok[eé]mon)?")
def _r(m, text):
    # "equal to the damage done to this Pokemon" has no number of its own;
    # -1 is the sentinel for "however much it took", resolved on the board.
    return [Action(Op.RETALIATE_COUNTERS,
                   int(m.group(1)) if m.group(1) else -1, Target.SELF)]


# ---- Trainers: the last of the tail --------------------------------------

@rule("berry_type_damage_reduction",
      r"if the pok[eé]mon this card is attached to is damaged by an attack from"
      r" your opponent'?s (" + TYPES + r") pok[eé]mon, it takes (\d+) less damage")
def _r(m, text):
    return [Action(Op.REDUCE_DAMAGE, int(m.group(2)), Target.SELF,
                   {"attacker_type": m.group(1).capitalize()})]


@rule("discard_tools_any_side",
      r"choose up to (\d+) pok[eé]mon tools? attached to pok[eé]mon \(yours or"
      r" your opponent'?s\) and discard them")
def _r(m, text):
    return [Action(Op.DISCARD_TOOL_ANY, int(m.group(1)), Target.BOTH_ALL)]


@rule("discard_tool_and_special_energy_one",
      r"discard a pok[eé]mon tool and a special energy from 1 of your"
      r" opponent'?s pok[eé]mon")
def _r(m, text):
    return [Action(Op.DISCARD_TOOL_FROM_ALL_OPPONENT, 1, Target.OPP_ALL),
            Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 1, Target.OPP_ANY,
                   {"special": True})]


@rule("discard_special_energy_one_opponent",
      r"discard a special energy from 1 of your opponent'?s pok[eé]mon")
def _r(m, text):
    return [Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 1, Target.OPP_ANY,
                   {"special": True})]


@rule("discard_energy_one_opponent",
      r"discard an energy from 1 of your opponent'?s pok[eé]mon")
def _r(m, text):
    return [Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 1, Target.OPP_ANY)]


@rule("scoop_up_own_pokemon",
      r"put 1 of your pok[eé]mon and all attached cards into your hand")
def _r(m, text):
    return [Action(Op.SELF_TO_HAND, 1, Target.YOUR_ANY)]


@rule("stadium_tools_have_no_effect",
      r"pok[eé]mon tools attached to each pok[eé]mon \(both yours and your"
      r" opponent'?s\) have no effect")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.BOTH_ALL, {"what": "tools"})]


@rule("stadium_stage2_hp_penalty",
      r"each stage (\d+) pok[eé]mon in play \(both yours and your opponent'?s\)"
      r" gets ([+-]\d+) hp")
def _r(m, text):
    return [Action(Op.MODIFY_HP, int(m.group(2)), Target.BOTH_ALL,
                   {"stage": f"Stage {m.group(1)}"})]


@rule("stadium_extra_poison",
      r"during pok[eé]mon checkup, put (\d+) more damage counters? on each"
      r" poisoned non-(" + TYPES + r") pok[eé]mon")
def _r(m, text):
    return [Action(Op.BUFF_CONDITION_DAMAGE, int(m.group(1)) * 10,
                   Target.BOTH_ALL, {"condition": "poisoned",
                                     "type_not": m.group(2).capitalize()})]


@rule("stadium_tera_cost_more",
      r"attacks used by each ([\w]+) pok[eé]mon in play \(both yours and your"
      r" opponent'?s\) cost colorless more")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, 1, Target.BOTH_ALL,
                   {"requires_subtype": m.group(1).capitalize()})]


@rule("search_named_tools_to_hand",
      r"search your deck for up to (\d+) pok[eé]mon tool cards? that have"
      r" [\"“']([^\"”']+)[\"”'] in their name, reveal them, and put them into"
      r" your hand")
def _r(m, text):
    return [Action(Op.SEARCH_TO_HAND, int(m.group(1)), Target.SELF,
                   {"kind": "tool", "name_contains": m.group(2)})]


@rule("look_at_bottom_for_pokemon",
      r"look at the bottom (\d+) cards of your deck\. you may reveal a"
      r" pok[eé]mon you find there and put it into your hand")
def _r(m, text):
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "pokémon"})]


@rule("discard_hand_then_search_three",
      r"discard your hand and search your deck for a pok[eé]mon, a supporter"
      r" card, and a basic energy card")
def _r(m, text):
    return [Action(Op.DISCARD_FROM_SELF, 99, Target.SELF),
            Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "pokémon"}),
            Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "supporter"}),
            Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "energy"})]


@rule("move_energy_bench_to_active",
      r"move up to (\d+) energy from your benched pok[eé]mon to your active"
      r" pok[eé]mon")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, int(m.group(1)), Target.YOUR_ACTIVE,
                   {"from": Target.YOUR_BENCHED})]


@rule("opponent_hand_to_bottom_redraw",
      r"your opponent counts the cards in their hand, shuffles those cards, and"
      r" puts them on the bottom of their deck")
def _r(m, text):
    return [Action(Op.SET_OPPONENT_HAND, None, Target.OPPONENT,
                   {"redraw_same": True})]


@rule("tool_grants_its_own_attack",
      r"the [\w'’ ]+ this card is attached to can use the attack on this card")
def _r(m, text):
    return [Action(Op.GRANT_ATTACK_ACCESS, None, Target.SELF,
                   {"from_tool": True})]


@rule("tera_attack_costs_less",
      r"when the tera pok[eé]mon this card is attached to uses an attack, that"
      r" attack costs (\d+) energy less")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, -int(m.group(1)), Target.SELF,
                   {"type": "Colorless"})]


@rule("setup_or_deckbuilding_rule",
      r"put this pok[eé]mon into play only with the effect of"
      r"|if this pok[eé]mon is in your hand when you are setting up to play"
      r"|this pok[eé]mon can evolve into any pok[eé]mon ex that evolves from")
def _r(m, text):
    # Deckbuilding and setup-phase rules. There is no turn on which these
    # "happen", so they are modelled as nothing ON PURPOSE rather than
    # falling out of the audit as unhandled gaps. Zero to Hero, which is the
    # half of Palafin that DOES happen during a turn, compiles separately.
    return [Action(Op.NO_OP_SETUP_RULE, None, Target.SELF)]


@rule("zero_to_hero",
      r"when this pok[eé]mon moves from the active spot to the bench, you may"
      r" search your deck for an? ([\w'’ ]+?) and switch it with this pok[eé]mon")
def _r(m, text):
    return [Action(Op.SWAP_IN_PLACE, 1, Target.SELF,
                   {"name_contains": m.group(1).strip(), "from": "deck"})]


@rule("heavy_baton",
      r"if the pok[eé]mon this card is attached to has a retreat cost of exactly"
      r" (\d+)[\s\S]{0,90}?is knocked out by damage from an attack"
      r"[\s\S]{0,60}?move up to (\d+) basic energy")
def _r(m, text):
    # Fires ON A KNOCK OUT, which MOVE_ENERGY's ordinary path never checks
    # -- it was compiled with an on_ko flag nothing read, so the Tool did
    # nothing. Its own op, resolved where Knock Outs are resolved.
    return [Action(Op.SALVAGE_ENERGY_ON_KO, int(m.group(2)), Target.YOUR_BENCHED,
                   {"retreat_exactly": int(m.group(1))})]


@rule("first_turn_energy_bounce",
      r"put an energy attached to 1 of your opponent'?s pok[eé]mon into their"
      r" hand")
def _r(m, text):
    return [Action(Op.OPP_ENERGY_TO_HAND, 1, Target.OPP_ANY)]


@rule("stadium_type_evolve_early",
      r"each player'?s (" + TYPES + r") pok[eé]mon can evolve into \1 pok[eé]mon"
      r" during the turn they play those pok[eé]mon")
def _r(m, text):
    return [Action(Op.EVOLVE_EARLY, None, Target.BOTH_ALL,
                   {"type": m.group(1).capitalize()})]


@rule("devolve_own",
      r"devolve (\d+) of your evolved (" + TYPES + r")? ?pok[eé]mon by putting"
      r" any number of evolution cards on it into your hand")
def _r(m, text):
    f = {"to": "hand", "own": True}
    if m.group(2):
        f["type"] = m.group(2).capitalize()
    return [Action(Op.DEVOLVE, int(m.group(1)), Target.YOUR_ANY, f)]


@rule("stadium_confusion_sticks",
      r"confused pok[eé]mon \(both yours and your opponent'?s\) don'?t recover"
      r" from that special condition when they evolve or devolve")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.BOTH_ALL,
                   {"what": "clear_confusion_on_evolve"})]


@rule("named_team_required",
      r"you can use this card only if you have ([\w'’ ,]+?(?:, and [\w'’ ]+?)?)"
      r" in play")
def _r(m, text):
    # The requirement is the card; whatever it then does is compiled by the
    # other rules matching the rest of the text.
    return [Action(Op.NO_OP_SETUP_RULE, None, Target.SELF,
                   {"requires": m.group(1)})]


@rule("reveal_prize_and_hand",
      r"turn (\d+) of your opponent'?s face-down prize cards? face up and choose"
      r" a random card from your opponent'?s hand")
def _r(m, text):
    return [Action(Op.NO_OP_INFORMATION, None, Target.SELF),
            Action(Op.DISCARD_FROM_OPPONENT, 1, Target.OPPONENT, {"to": "deck"})]


@rule("reflip_coins",
      r"after you flip any coins for an attack[\s\S]{0,80}?you may ignore all"
      r" results of those coin flips")
def _r(m, text):
    # "You MAY ignore the results and flip again" -- you only re-flip when
    # the first result was bad, so it is take-the-better-of-two, not a
    # second roll at the same odds. It was a NO_OP placeholder, which
    # counted as "accounted for" while doing nothing.
    m2 = re.search(r"of the ([\w]+) pok[eé]mon this card is attached to", text,
                   re.I)
    f = {"type": m2.group(1).capitalize()} if m2 else {}
    return [Action(Op.REFLIP_COINS, 1, Target.SELF, f)]


@rule("evolve_from_deck",
      r"search your deck for a stage 1 pok[eé]mon that evolves from 1 of your"
      r" basic pok[eé]mon and put it onto that pok[eé]mon to evolve it")
def _r(m, text):
    # Grand Tree. The second sentence chains a Stage 2 onto whatever was
    # just evolved, so this is up to two stages in one activation.
    chain = bool(re.search(r"search your deck for a stage 2 pok[eé]mon", text,
                           re.I))
    return [Action(Op.EVOLVE_FROM_DECK, 2 if chain else 1, Target.YOUR_ANY,
                   {"chain": True, "basic_first": True} if chain else {"basic_first": True})]


@rule("discard_to_bench",
      r"put a basic pok[eé]mon[^.]{0,40}from your discard pile onto")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, 1, Target.YOUR_BENCHED, {"from": "discard"})]


@rule("ignore_energy_cost", r"ignore all (" + TYPES + r")? ?energy in the costs? of")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, -99, Target.SELF,
                   {"type": (m.group(1) or "").capitalize() or None})]


@rule("attack_first_turn", r"can use attacks during your first turn")
def _r(m, text):
    return [Action(Op.ATTACK_FIRST_TURN, None, Target.SELF)]


@rule("grant_bench_attacks",
      r"can use the attacks of any of your benched pok[e\u00e9]mon")
def _r(m, text):
    return [Action(Op.GRANT_BENCH_ATTACKS, None, Target.SELF)]


@rule("weakness_multiplier",
      r"apply weakness for both active pok[e\u00e9]mon as\s*[x\u00d7]\s*(\d+)")
def _r(m, text):
    # Applies to BOTH Active Pokemon, so it cuts in both directions -- the
    # opponent attacking into your Weakness gets the same multiplier.
    return [Action(Op.WEAKNESS_MULTIPLIER, int(m.group(1)), Target.BOTH_ALL)]


@rule("set_weakness", r"weakness of each of your opponent'?s (\w+) pok[eé]mon in play is now (\w+)")
def _r(m, text):
    return [Action(Op.SET_WEAKNESS, None, Target.OPP_ALL,
                   {"from_type": m.group(1).capitalize(), "to_type": m.group(2).capitalize()})]


@rule("suppress_self_ko_abilities", r"lose any ability that requires the pok[eé]mon using it to knock out itself")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.BOTH_ALL, {"what": "self_ko_abilities"})]


@rule("reveal_opponent_hand", r"your opponent reveals their hand")
def _r(m, text):
    return [Action(Op.REVEAL_OPPONENT_HAND, None, Target.OPPONENT)]


@rule("discard_kind_from_revealed_hand",
      r"you discard up to (\d+) (item|supporter|pok[eé]mon tool|trainer) cards? you find there")
def _r(m, text):
    """Eri: the discard was dropped; only "reveals their hand" compiled."""
    kind = {"pokémon tool": "Tool", "pokemon tool": "Tool"}.get(
        m.group(2).lower(), m.group(2).capitalize())
    return [Action(Op.DISCARD_FROM_OPPONENT, int(m.group(1)), Target.OPPONENT,
                   {"kind": kind})]


@rule("attach_tool_from_deck", r"search your deck for a pok[eé]mon tool card and attach")
def _r(m, text):
    return [Action(Op.ATTACH_TOOL, 1, Target.YOUR_ANY, {"from": "deck"})]


@rule("prevent_that_damage", r"prevent that damage")
def _r(m, text):
    return [Action(Op.PREVENT_DAMAGE, None, Target.SELF)]


@rule("apply_chosen_condition",
      r"choose (?:burned|confused|poisoned)[\s\S]{0,80}affected by that special condition")
def _r(m, text):
    return [Action(Op.APPLY_CONDITION, None, Target.OPP_ACTIVE,
                   {"conditions": ["burned", "confused", "poisoned"], "choose_one": True})]


@rule("checkup_bonus_any_order",
      r"during pok[eé]mon checkup, put (\d+) more damage counters on your opponent'?s (\w+)")
def _r(m, text):
    return [Action(Op.BUFF_CONDITION_DAMAGE, int(m.group(1)), Target.OPP_ALL,
                   {"condition": m.group(2).lower()})]


@rule("discard_opponent_energy",
      r"(?:put|discard) an energy (?:attached to|from) (your opponent'?s active|the attacking)")
def _r(m, text):
    tgt = (Target.ATTACKING_POKEMON if "attacking" in m.group(1).lower()
           else Target.OPP_ACTIVE)
    return [Action(Op.DISCARD_ENERGY_FROM_OPPONENT, 1, tgt)]


@rule("extra_prize", r"take 1 more prize card")
def _r(m, text):
    return [Action(Op.MODIFY_PRIZE, 1, Target.SELF)]


@rule("set_type", r"it is (" + TYPES + r") and (" + TYPES + r") type")
def _r(m, text):
    return [Action(Op.SET_TYPE, None, Target.SELF,
                   {"types": [m.group(1).capitalize(), m.group(2).capitalize()]})]


@rule("attack_twice", r"may use an attack it has twice")
def _r(m, text):
    return [Action(Op.ATTACK_TWICE, None, Target.SELF)]


@rule("return_to_hand_on_ko", r"put it into your hand instead of")
def _r(m, text):
    return [Action(Op.RETURN_TO_HAND_ON_KO, None, Target.SELF)]


@rule("ignore_opponent_effects",
      r"isn'?t affected by any effects on your opponent'?s active")
def _r(m, text):
    return [Action(Op.IGNORE_OPPONENT_EFFECTS, None, Target.SELF)]


@rule("swap_hand_with_deck", r"switch a card from your hand with the top card of your deck")
def _r(m, text):
    return [Action(Op.SWAP_HAND_WITH_DECK, 1, Target.SELF)]


@rule("extra_tools", r"may have up to (\d+) pok[eé]mon tool cards attached")
def _r(m, text):
    return [Action(Op.EXTRA_TOOLS, int(m.group(1)), Target.YOUR_ALL)]


@rule("lock_counter_movement", r"damage counters[^.]{0,60}can'?t be moved")
def _r(m, text):
    return [Action(Op.LOCK_COUNTER_MOVEMENT, None, Target.BOTH_ALL)]


@rule("search_named_evolution",
      r"search your deck for an? ([A-Z][\w'’ -]+?) or ([A-Z][\w'’ -]+?) and put it")
def _r(m, text):
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF,
                   {"kind": "pokemon", "one_of": [m.group(1).strip(), m.group(2).strip()]})]


@rule("attach_named_energy_from_discard",
      r"attach up to (\d+) ([A-Z][\w'’ ]*?energy) cards? from your discard pile")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, int(m.group(1)), Target.SELF,
                   {"from": "discard", "card_name": m.group(2).strip()})]


@rule("move_energy_on_ko", r"move up to (\d+) basic ([\w]+) energy")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, int(m.group(1)), Target.YOUR_ANY,
                   {"type": m.group(2).capitalize(), "from": Target.SELF})]


@rule("conditional_attack_access", r"this pok[eé]mon can use the ([\w'’ -]+?) attack")
def _r(m, text):
    # "...can use the Trifrost attack for [C]" is a COST OVERRIDE, not
    # access: Kyurem already has Trifrost. Compiled as GRANT_ATTACK_ACCESS
    # it named an op with no consumer, so the ability was inert -- and had
    # it been implemented as written it would have granted an attack the
    # card already has, for free, with the "if your opponent has a Colress
    # card in their discard pile" gate missing entirely.
    cost = re.search(r"attack for ((?:" + TYPES + r")(?:\s*(?:" + TYPES
                     + r"))*)\b", text, re.I)
    if cost:
        n = len(re.findall(TYPES, cost.group(1), re.I))
        return [Action(Op.MODIFY_ATTACK_COST, -99, Target.SELF,
                       {"attack": m.group(1).strip(), "cost_becomes": n})]
    return [Action(Op.GRANT_ATTACK_ACCESS, None, Target.SELF,
                   {"attack": m.group(1).strip()})]


@rule("search_named_to_bench",
      r"search your deck for an? ([A-Z][\w'’ -]+?) and put it onto your bench")
def _r(m, text):
    named = m.group(1).strip()
    low = named.lower()
    # Same category-vs-species trap as recruit_species_to_bench above.
    if low.endswith("pokémon") or low.endswith("pokemon") or low in STAGE_WORDS:
        return []
    return [Action(Op.SEARCH_TO_BENCH, 1, Target.YOUR_BENCHED,
                   {"name_contains": named})]


@rule("search_energy_and_discard",
      r"search your deck for up to (\d+) basic (" + TYPES + r") energy cards? and discard them")
def _r(m, text):
    # Thins the deck and stocks the discard pile; the Energy never lands
    # in play, so this is deck manipulation, not acceleration.
    return [Action(Op.SEARCH_TO_DISCARD, int(m.group(1)), Target.SELF,
                   {"kind": "energy", "type": m.group(2).capitalize()})]


@rule("shuffle_opponent_hand_cards",
      r"choose a random card from your opponent'?s hand[\s\S]{0,80}shuffles? them into their deck")
def _r(m, text):
    n = 2 if re.search(r"flip 2 coins", text, re.I) else 1
    return [Action(Op.DISCARD_FROM_OPPONENT, n, Target.OPPONENT,
                   {"to": "deck", "per_heads": bool(re.search(r"for each heads", text, re.I))})]


@rule("switch_self_with_active", r"switch this pok[eé]mon with your active pok[eé]mon")
def _r(m, text):
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, {"gust": False, "promote_self": True})]


@rule("energy_provides_more",
      r"each basic (" + TYPES + r") energy attached to all of your pok[eé]mon provides")
def _r(m, text):
    return [Action(Op.ENERGY_PROVIDES_EXTRA, 1, Target.YOUR_ALL,
                   {"type": m.group(1).capitalize()})]


@rule("self_to_top_of_deck",
      r"put this pok[eé]mon on top of your deck")
def _r(m, text):
    return [Action(Op.SHUFFLE_SELF_INTO_DECK, 1, Target.SELF, {"to_top": True})]


@rule("bench_opponent_basics",
      r"put any number of basic pok[eé]mon you find there onto their bench")
def _r(m, text):
    return [Action(Op.FORCE_BENCH_OPPONENT, None, Target.OPPONENT)]


@rule("attack_cost_scales_by_prizes",
      r"costs (" + TYPES + r") less for each prize card your opponent has taken")
def _r(m, text):
    return [Action(Op.MODIFY_ATTACK_COST, -1, Target.SELF,
                   {"type": m.group(1).capitalize(), "per_opponent_prize_taken": True})]


@rule("retreat_may_fail",
      r"if tails, energy for its retreat cost is not discarded, and they don'?t switch")
def _r(m, text):
    return [Action(Op.LOCK, None, Target.OPPONENT,
                   {"what": "retreat", "chance_to_block": 0.5})]


@rule("put_self_onto_bench_from_hand",
      r"you may put this pok[eé]mon onto your bench")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, 1, Target.YOUR_BENCHED, {"from": "hand", "self": True})]


@rule("move_energy_on_own_ko",
      r"put all basic (" + TYPES + r") energy attached to that pok[eé]mon")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, None, Target.YOUR_ANY,
                   {"type": m.group(1).capitalize(), "any_amount": True, "on_ko": True})]


# ---- meta ----------------------------------------------------------------

@rule("grant_attack_access", r"can use any attack from its previous evolutions")
def _r(m, text):
    return [Action(Op.GRANT_ATTACK_ACCESS, None, Target.YOUR_ALL)]


# --------------------------------------------------------------------------
# Compiler
# --------------------------------------------------------------------------

# Phrases that mark an effect as genuinely outside the verb set. Recorded as
# a reason rather than silently producing an empty Effect.
_KNOWN_UNSUPPORTED = [
    # These are structural rules about how a card enters play or what it may
    # evolve into -- not effects that happen during a turn. There is nothing
    # for the runtime to execute, so they are named precisely rather than
    # left as a vague "no rule matched".
    (r"put this pok[eé]mon into play only with", "deckbuilding/put-into-play rule, not a turn action"),
    (r"when you are setting up to play", "setup-phase rule, before the game starts"),
    (r"can evolve into any pok[eé]mon ex that evolves from",
     "evolution-legality rule, not a turn action"),
    (r"moves from the active spot to the bench[\s\S]{0,120}switch it with this pok",
     "in-place transform (Palafin <-> Palafin ex) keeping all attached state"),
    (r"instead of", "replacement effect"),
    (r"put this pok[eé]mon into play only with", "special put-into-play rule"),
    (r"choose an attack|use it as this attack", "copies another attack"),
    (r"it is .{0,20}type", "changes a Pokemon's type"),
    (r"twice", "repeats an attack"),
    (r"take a prize card|take 1 more prize", "modifies Prize taking"),
]


def _collapse_duplicate_attachments(eff, spans):
    """One "attach Energy" sentence must produce exactly ONE attach.

    Several rules deliberately overlap to catch different phrasings, and
    the generic ones (attach_multi_type_energy, search_energy_attach_loose,
    attach_named_energy_from_discard) match the same sentence as the
    destination-aware ones. The existing dedupe keys on the whole Action,
    so two attaches that differ only in target or filter both survived --
    and both EXECUTE. Measured: Teal Dance attached 2 Energy off a card
    that says one, Dynamotor 2 off a card that says one, and 55 effects in
    the Standard pool accelerated at double their printed rate. That is
    the largest single distortion the simulator had: every accelerator in
    the format was twice as fast as its card said.

    Collapse is per SOURCE ("from": hand / deck / discard), because one
    card really can attach from two different places. Within a source the
    survivor is the action whose rule matched the WIDEST span of text --
    the rule that read the destination clause understood the sentence
    better than the one that stopped at "from your discard pile". Ties
    keep the first, which is rule order.
    """
    attaches = [a for a in eff.actions if a.op == Op.ATTACH_ENERGY]
    if len(attaches) < 2:
        return eff.actions
    best = {}
    for a in attaches:
        src = (a.filter or {}).get("from")
        width, _rname = spans.get(id(a), (0, ""))
        if src not in best or width > best[src][0]:
            best[src] = (width, a)
    keep = {id(a) for _w, a in best.values()}
    return [a for a in eff.actions
            if a.op != Op.ATTACH_ENERGY or id(a) in keep]


_HP_CAP_RE = re.compile(r"with (\d+) HP or less", re.I)
_NO_RULE_BOX_RE = re.compile(
    r"(?:that )?(?:doesn'?t|don'?t) have a rule box|without a rule box", re.I)
_RESTRICTED_OPS = (Op.SEARCH_TO_BENCH, Op.SEARCH_TO_HAND, Op.RECOVER_TO_BENCH,
                   Op.FROM_DISCARD_TO_HAND)


_EX_ONLY_RE = re.compile(r"search your deck for[^.]{0,40}?pok[eé]mon ex\b", re.I)


def _stamp_target_restrictions(eff):
    """"a Basic Pokemon WITH 70 HP OR LESS", "a Pokemon THAT DOESN'T HAVE A
    RULE BOX" -- both are restrictions on what the search may take, and
    both sit AFTER the noun.

    _search_filter only reads the qualifier that comes BEFORE it (stage,
    type, name fragment), so both were dropped. Buddy-Buddy Poffin fetched
    any Basic at all, a 230 HP Regice ex included; Poke Pad tutored a
    Pokemon ex, which is the one thing the card exists not to do. 36 and
    23 of the 45 decks in this repo's field run those two cards.

    A dropped restriction never weakens a card. It makes it unconditional,
    which is how both of these went unnoticed while looking like working
    search.
    """
    cap = _HP_CAP_RE.search(eff.text or "")
    no_box = _NO_RULE_BOX_RE.search(eff.text or "")
    # Cyrano searches for "up to 3 Pokemon ex". Unrestricted it took three
    # one-Prize support Pokemon instead, which is a different and better
    # card -- verified by execution against a deck holding no ex at all.
    ex_only = _EX_ONLY_RE.search(eff.text or "")
    if not cap and not no_box and not ex_only:
        return
    for a in eff.actions:
        if a.op not in _RESTRICTED_OPS:
            continue
        a.filter = dict(a.filter or {})
        if cap:
            a.filter["hp_at_most"] = int(cap.group(1))
        if no_box:
            a.filter["no_rule_box"] = True
        if ex_only:
            a.filter["ex_only"] = True


def compile_effect(source, name, text):
    eff = Effect(source, name, text)
    if not text.strip():
        eff.unsupported = "no text"
        return eff

    eff.trigger = parse_trigger(text)
    eff.conditions = parse_conditions(text)
    eff.costs = parse_costs(text)
    eff.chance = parse_chance(text)

    spans = {}                    # action id -> how much text its rule read
    for rname, rx, builder in RULES:
        m = rx.search(text)
        if not m:
            continue
        try:
            acts = builder(m, text)
        except Exception as exc:                       # a rule must never crash the run
            eff.unsupported = f"rule {rname} raised {exc!r}"
            return eff
        if acts:
            for a in acts:
                spans[id(a)] = (m.end() - m.start(), rname)
            eff.actions.extend(acts)
            eff.rules_hit.append(rname)

    # Several rules deliberately overlap to catch different phrasings of
    # the same sentence, so one card text can produce the identical Action
    # more than once. That is harmless while an action is only inspected,
    # and actively wrong once it is EXECUTED -- a duplicated
    # "search 2 Basic Pokemon onto your Bench" benched four.
    seen, unique = set(), []
    for a in eff.actions:
        key = (a.op, a.amount, a.target,
               tuple(sorted((str(k), str(v)) for k, v in (a.filter or {}).items())))
        if key in seen:
            continue
        seen.add(key)
        unique.append(a)
    eff.actions = unique
    # A Prize clause that only picks the larger draw ("draw 8 cards
    # instead") was ALSO parsed as a condition on the whole card, so Lacey
    # could not be played at all until the opponent was down to 3 Prizes.
    for a in eff.actions:
        ii = (a.filter or {}).get("instead_if")
        if ii and ii["who"] == "opponent":
            eff.conditions = [c for c in eff.conditions
                              if not (c.get("kind") == "opponent_prizes_at_most"
                                      and c.get("count") == ii["count"])]
        if ii and ii["who"] == "self":
            eff.conditions = [c for c in eff.conditions
                              if not (c.get("kind") == "own_prizes_equal"
                                      and c.get("count") == ii["count"])]
    eff.actions = _collapse_duplicate_attachments(eff, spans)
    _stamp_target_restrictions(eff)

    if not eff.actions:
        for pat, reason in _KNOWN_UNSUPPORTED:
            if re.search(pat, text, re.I):
                eff.unsupported = reason
                return eff
        eff.unsupported = "no rule matched"
    return eff


def compile_card_abilities(card):
    return [compile_effect(card["name"], ab.get("name") or "", ab.get("text") or "")
            for ab in (card.get("abilities") or [])]


# --------------------------------------------------------------------------
# Coverage reporting
# --------------------------------------------------------------------------

def load_cards(path=CARDS_PATH):
    with open(path) as f:
        return json.load(f)


def all_effects(cards):
    seen, out = set(), []
    for c in cards:
        for ab in c.get("abilities") or []:
            key = (c["name"], ab.get("name"))
            if key in seen:
                continue
            seen.add(key)
            out.append(compile_effect(c["name"], ab.get("name") or "", ab.get("text") or ""))
    return out


def coverage_report(effects, show_misses=False):
    total = len(effects)
    ok = [e for e in effects if e.supported]
    bad = [e for e in effects if not e.supported]
    print(f"Abilities compiled : {len(ok)}/{total}  ({100*len(ok)/total:.1f}%)")
    print(f"Not compiled       : {len(bad)}")

    print("\nBy trigger:")
    for k, v in Counter(e.trigger for e in ok).most_common():
        print(f"  {v:4d}  {k}")
    print("\nBy op:")
    ops = Counter(a.op for e in ok for a in e.actions)
    for k, v in ops.most_common():
        print(f"  {v:4d}  {k}")

    print("\nUncompiled, by reason:")
    for k, v in Counter(e.unsupported for e in bad).most_common():
        print(f"  {v:4d}  {k}")

    if show_misses:
        print("\n--- uncompiled abilities ---")
        for e in bad:
            print(f"  [{e.unsupported}] {e.source} / {e.name}")
            print(f"      {e.text[:150]}")
    return len(ok), total


def main():
    cards = load_cards()
    if "--card" in sys.argv:
        want = sys.argv[sys.argv.index("--card") + 1].lower()
        for c in cards:
            if want in c["name"].lower():
                for e in compile_card_abilities(c):
                    print(f"\n{c['name']} / {e.name}")
                    print(f"  text     : {e.text}")
                    print(f"  trigger  : {e.trigger}")
                    print(f"  conditions: {e.conditions}")
                    print(f"  costs    : {e.costs}")
                    print(f"  actions  : {e.actions}")
                    print(f"  rules    : {e.rules_hit}")
                    if e.unsupported:
                        print(f"  UNSUPPORTED: {e.unsupported}")
        return 0
    if "--test" in sys.argv:
        return 0 if _self_test() else 1
    effects = all_effects(cards)
    coverage_report(effects, show_misses="--misses" in sys.argv)
    print()
    ok = _self_test()
    return 0 if ok else 1




# --------------------------------------------------------------------------
# Correctness self-test
# --------------------------------------------------------------------------
# Coverage alone is a bad metric: a rule that MATCHES but produces the wrong
# IR is worse than one that does not match, because it silently feeds the
# engine a lie. These assertions pin the compiled output for a spread of
# real cards -- one per rule family, plus the tricky ones -- so a future
# regex tweak that breaks an existing card fails loudly.

_EXPECT = {
    # (card, ability): dict of fields to assert on the compiled Effect
    ("Toucannon", "Aerial Draw"): {
        "trigger": Trigger.ONCE_PER_TURN,
        "ops": [(Op.DRAW, 1, Target.SELF)],
    },
    ("Alakazam", "Psychic Draw"): {
        "trigger": Trigger.ON_EVOLVE,
        "ops": [(Op.DRAW, 3, Target.SELF)],
    },
    ("N's Zoroark ex", "Trade"): {
        "trigger": Trigger.ONCE_PER_TURN,
        "ops": [(Op.DRAW, 2, Target.SELF)],
        "costs": [{"kind": "discard_hand", "amount": 1}],
    },
    ("Dudunsparce", "Run Away Draw"): {
        "ops": [(Op.DRAW, 3, Target.SELF)],
        "costs": [{"kind": "shuffle_self"}],
    },
    ("Fezandipiti ex", "Flip the Script"): {
        "conditions_contain": {"kind": "lost_pokemon_last_turn"},
        "ops": [(Op.DRAW, 3, Target.SELF)],
    },
    ("Mega Kangaskhan ex", "Run Errand"): {
        "conditions_contain": {"kind": "self_is_active"},
        "ops": [(Op.DRAW, 2, Target.SELF)],
    },
    ("Mega Scrafty ex", "Counterattacking Crest"): {
        "trigger": Trigger.ON_DAMAGED,
        "ops": [(Op.PLACE_COUNTERS, 5, Target.ATTACKING_POKEMON)],
    },
    ("Spiritomb", "Spiteful Swirl"): {
        "trigger": Trigger.ON_DAMAGED,
        "ops": [(Op.PLACE_COUNTERS, 1, Target.ATTACKING_POKEMON)],
    },
    ("Munkidori", "Adrena-Brain"): {
        "trigger": Trigger.ONCE_PER_TURN,
        "conditions_contain": {"kind": "self_has_energy_type", "type": "Darkness"},
        "ops": [(Op.MOVE_COUNTERS, 3, Target.OPP_ANY)],
    },
    ("Steven's Carbink", "Stone Palace"): {
        "ops": [(Op.REDUCE_DAMAGE, 30, Target.YOUR_ALL)],
    },
    ("Bronzong", "Protective Bell"): {
        "ops": [(Op.REDUCE_DAMAGE, 10, Target.YOUR_ALL)],
    },
    ("Hop's Snorlax", "Extra Helpings"): {
        "ops": [(Op.BUFF_DAMAGE, 30, Target.YOUR_ALL)],
    },
    ("Team Rocket's Arbok", "Potent Glare"): {
        "conditions_contain": {"kind": "self_is_active"},
        "ops_contain": Op.LOCK,
    },
    ("Relicanth", "Memory Dive"): {
        "ops": [(Op.GRANT_ATTACK_ACCESS, None, Target.YOUR_ALL)],
    },
    ("Shuppet", "Hide 'n' Sneak"): {
        "ops_contain": Op.PREVENT_DAMAGE,
    },
    ("Bastiodon", "Ancient Bulwark"): {
        "conditions_contain": {"kind": "self_is_benched"},
        "ops_contain": Op.PREVENT_DAMAGE,
    },
    ("Lillie's Clefairy ex", "Fairy Zone"): {
        "ops": [(Op.SET_WEAKNESS, None, Target.OPP_ALL)],
    },
    ("Pecharunt", "Toxic Subjugation"): {
        "ops": [(Op.BUFF_CONDITION_DAMAGE, 5, Target.OPP_ALL)],
    },
    ("Team Rocket's Spidops", "Charging Up"): {
        "ops_contain": Op.ATTACH_ENERGY,
    },
}


def _self_test():
    cards = load_cards()
    by_key = {}
    for c in cards:
        for ab in c.get("abilities") or []:
            by_key.setdefault((c["name"], ab.get("name")), ab)

    failures = []
    for key, want in _EXPECT.items():
        ab = by_key.get(key)
        if ab is None:
            failures.append(f"{key}: not present in dataset")
            continue
        eff = compile_effect(key[0], key[1], ab.get("text") or "")
        if eff.unsupported:
            failures.append(f"{key}: did not compile ({eff.unsupported})")
            continue
        if "trigger" in want and eff.trigger != want["trigger"]:
            failures.append(f"{key}: trigger={eff.trigger}, expected {want['trigger']}")
        if "ops" in want:
            got = [(a.op, a.amount, a.target) for a in eff.actions]
            for exp in want["ops"]:
                if exp not in got:
                    failures.append(f"{key}: missing action {exp}; got {got}")
        if "ops_contain" in want:
            if want["ops_contain"] not in [a.op for a in eff.actions]:
                failures.append(f"{key}: no {want['ops_contain']} in {[a.op for a in eff.actions]}")
        if "costs" in want:
            for c_ in want["costs"]:
                if c_ not in eff.costs:
                    failures.append(f"{key}: missing cost {c_}; got {eff.costs}")
        if "conditions_contain" in want:
            if want["conditions_contain"] not in eff.conditions:
                failures.append(f"{key}: missing condition {want['conditions_contain']};"
                                f" got {eff.conditions}")

    print(f"Correctness assertions: {len(_EXPECT)} cards checked")
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print("  " + f)
        return False
    print("All correctness assertions passed.")
    return True


if __name__ == "__main__":
    sys.exit(main())
