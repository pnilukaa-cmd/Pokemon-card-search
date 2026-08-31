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
    ATTACK_FIRST_TURN = "attack_first_turn"
    SET_WEAKNESS = "set_weakness"
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
    SET_OPPONENT_HAND = "set_opponent_hand"
    EXTRA_TOOLS = "extra_tools"
    LOCK_COUNTER_MOVEMENT = "lock_counter_movement"
    WIN_GAME = "win_game"
    CONDITIONAL_KO = "conditional_ko"
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
    return Trigger.PASSIVE


def parse_conditions(text):
    t = text
    out = []
    if re.search(r"if this pok[eé]mon is in the active spot|as long as this pok[eé]mon is in the active spot", t, re.I):
        out.append({"kind": "self_is_active"})
    if re.search(r"as long as this pok[eé]mon is on your bench|is on your bench", t, re.I):
        out.append({"kind": "self_is_benched"})
    m = re.search(r"were knocked out during your opponent'?s last turn", t, re.I)
    if m:
        out.append({"kind": "lost_pokemon_last_turn"})
    m = re.search(r"if you have ([A-Z][\w'’ -]+?) in play", t)
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
    m = re.search(r"flip (\d+) coins?[^.]{0,40}if all of them are heads", t)
    if m:
        return 0.5 ** int(m.group(1))
    if re.search(r"flip a coin[^.]{0,30}if heads", t):
        return 0.5
    if re.search(r"flip a coin[^.]{0,30}if tails", t):
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
    m = re.search(r"discard a basic (" + TYPES + r") energy card from your hand", t, re.I)
    if m:
        out.append({"kind": "discard_energy_from_hand", "type": m.group(1).capitalize()})
    m = re.search(r"discard a basic (" + TYPES + r") energy from this pok[eé]mon", t, re.I)
    if m:
        out.append({"kind": "discard_energy_from_self", "type": m.group(1).capitalize()})
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
    if re.search(r"each player draw|your opponent .{0,20}draw|they draw", text, re.I):
        return [Action(Op.DRAW, int(m.group(1)), Target.BOTH_ALL)]
    return [Action(Op.DRAW, int(m.group(1)), Target.SELF)]


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


@rule("win_game", r"you win this game")
def _r(m, text):
    """The alternate win condition itself. Its Prize-count gate is parsed
    as a condition, so the action here is unconditional and the engine
    decides whether it is live."""
    return [Action(Op.WIN_GAME, None, Target.SELF)]


@rule("draw_one", r"\bdraw a card")
def _r(m, text):
    # "each player draws a card" belongs to each_player_draws below. Both
    # rules used to fire on Chandelure's Alluring Light, emitting the draw
    # twice -- which doubled the rate of the one engine a deck-out deck
    # actually wins with.
    if re.search(r"each player", text, re.I):
        return []
    return [Action(Op.DRAW, 1, Target.SELF)]


@rule("search_to_bench",
      r"search your deck for (?:up to )?(\d+|a|an) ([\w'’ -]*?)pok[eé]mon[^.]{0,60}?onto your bench")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": m.group(2).strip() or None})]


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
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": species})]


@rule("search_to_hand",
      r"search your deck for (?:up to )?(\d+|a|an)? ?([\w'’ -]*?)(pok[eé]mon|card|supporter|item|stadium|energy)[^.]{0,60}?(?:put (?:it|them) into your hand|into your hand)")
def _r(m, text):
    if "onto your bench" in text.lower():
        return []
    return [Action(Op.SEARCH_TO_HAND, _num(m.group(1)), Target.SELF,
                   {"kind": m.group(3).lower(), "name_contains": (m.group(2) or "").strip() or None})]


@rule("discard_to_hand", r"put (?:up to )?(\d+|a|an) ([\w'’ -]*?)(?:card|pok[eé]mon|energy)[^.]{0,40}from your discard pile into your hand")
def _r(m, text):
    return [Action(Op.FROM_DISCARD_TO_HAND, _num(m.group(1)), Target.SELF)]


@rule("look_at_deck", r"look at the top (\d+) cards? of your deck")
def _r(m, text):
    return [Action(Op.LOOK_AT_DECK, int(m.group(1)), Target.SELF)]


# ---- energy --------------------------------------------------------------

@rule("attach_energy_from_discard",
      r"attach (?:a|an|up to (\d+)) ?(?:basic )?(" + TYPES + r")? ?energy (?:card )?from your discard pile to ([^.]{0,50})")
def _r(m, text):
    return [Action(Op.ATTACH_ENERGY, _num(m.group(1)), parse_target(m.group(3)),
                   {"type": (m.group(2) or "").capitalize() or None, "from": "discard"})]


@rule("attach_energy_from_hand",
      r"attach (?:a|an|up to (\d+)) ?(?:basic )?(" + TYPES + r")? ?energy (?:card )?from your hand to ([^.]{0,50})")
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
    return [Action(Op.MOVE_ENERGY, _num(m.group(1)), parse_target(m.group(4)),
                   {"type": (m.group(2) or "").capitalize() or None,
                    "from": parse_target(m.group(3))})]


# ---- damage / health -----------------------------------------------------

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
    return [Action(Op.PLACE_COUNTERS, int(m.group(1)), parse_target(m.group(2)))]


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


@rule("prevent_damage", r"prevent all (?:damage|effects of attacks)[^.]{0,80}")
def _r(m, text):
    seg = m.group(0)
    tgt = Target.SELF
    if "your benched" in seg.lower():
        tgt = Target.YOUR_BENCHED
    elif "each of your" in seg.lower() or "all of your" in seg.lower():
        tgt = Target.YOUR_ALL
    filt = {}
    mm = re.search(r"from your opponent's ([\w' ]+?) pok", seg, re.I)
    if mm:
        filt["attacker_is"] = mm.group(1).strip()
    # Shaymin's Flower Curtain shields only the Pokemon WITHOUT a Rule Box.
    # Dropping this clause made it protect the benched ex it is played
    # alongside, which is the exact opposite of how the card plays.
    if re.search(r"don'?t have a rule box", seg, re.I):
        filt["no_rule_box"] = True
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

@rule("switch_opponent", r"switch (?:in )?1 of your opponent's benched pok[eé]mon")
def _r(m, text):
    return [Action(Op.SWITCH, 1, Target.OPP_ACTIVE, {"gust": True})]


@rule("switch_own", r"switch (?:this pok[eé]mon|your active pok[eé]mon) with 1 of your benched")
def _r(m, text):
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, {"gust": False})]


@rule("apply_condition", r"is now (asleep|burned|confused|paralyzed|poisoned)")
def _r(m, text):
    conds = re.findall(r"(asleep|burned|confused|paralyzed|poisoned)", text, re.I)
    tgt = Target.ATTACKING_POKEMON if "attacking pok" in text.lower() else Target.OPP_ACTIVE
    return [Action(Op.APPLY_CONDITION, None, tgt,
                   {"conditions": sorted({c.lower() for c in conds})})]


@rule("lock", r"can'?t (attack|retreat|play|use)")
def _r(m, text):
    what = m.group(1).lower()
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
    return [Action(Op.SEARCH_TO_BENCH, _num(m.group(1)), Target.YOUR_BENCHED,
                   {"name_contains": (m.group(2) or "").strip() or None})]


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
    return [Action(Op.SWITCH, 1, Target.YOUR_ACTIVE, {"gust": False})]


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
    return [Action(Op.ATTACH_ENERGY, int(m.group(1)), Target.YOUR_ANY, {"from": "discard"})]


@rule("evolve_early", r"can evolve during your first turn or the turn you play it")
def _r(m, text):
    return [Action(Op.EVOLVE_EARLY, None, Target.SELF)]


@rule("checkup_bonus_counters",
      r"put (\d+) more damage counters on your opponent'?s (\w+) pok[eé]mon during pok[eé]mon checkup")
def _r(m, text):
    return [Action(Op.BUFF_CONDITION_DAMAGE, int(m.group(1)), Target.OPP_ALL,
                   {"condition": m.group(2).lower()})]


@rule("devolve", r"devolve 1 of your opponent'?s evolved pok[eé]mon")
def _r(m, text):
    return [Action(Op.DEVOLVE, 1, Target.OPP_ANY)]


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


@rule("move_energy_any_amount",
      r"move any amount of (" + TYPES + r")? ?energy from ([^.]{0,40}?) to ([^.]{0,40})")
def _r(m, text):
    return [Action(Op.MOVE_ENERGY, None, parse_target(m.group(3)),
                   {"type": (m.group(1) or "").capitalize() or None,
                    "from": parse_target(m.group(2)), "any_amount": True})]


@rule("search_any_card", r"search your deck for a card\b")
def _r(m, text):
    return [Action(Op.SEARCH_TO_HAND, 1, Target.SELF, {"kind": "card"})]


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
    return [Action(Op.GRANT_ATTACK_ACCESS, None, Target.SELF,
                   {"attack": m.group(1).strip()})]


@rule("search_named_to_bench",
      r"search your deck for an? ([A-Z][\w'’ -]+?) and put it onto your bench")
def _r(m, text):
    return [Action(Op.SEARCH_TO_BENCH, 1, Target.YOUR_BENCHED,
                   {"name_contains": m.group(1).strip()})]


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


def compile_effect(source, name, text):
    eff = Effect(source, name, text)
    if not text.strip():
        eff.unsupported = "no text"
        return eff

    eff.trigger = parse_trigger(text)
    eff.conditions = parse_conditions(text)
    eff.costs = parse_costs(text)
    eff.chance = parse_chance(text)

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
            eff.actions.extend(acts)
            eff.rules_hit.append(rname)

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
