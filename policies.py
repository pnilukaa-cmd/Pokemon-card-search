#!/usr/bin/env python3
"""Named pilots: the decisions a player makes, held apart from the rules.

The engine has always had exactly one pilot -- greedy, maximise damage now
-- and every deck in this repo has been measured under it. That is fine
until the pilot's blind spots start deciding the standings, which they do:
a search-toolbox deck reads low here because the pilot cannot hold a card
back for the turn it matters, and a deck whose edge is sequencing reads low
for the same reason. Calling that "a lower bound" is true and useless. A
TEAM of pilots turns it into a measurement -- run the same deck under
several styles and the spread tells you how much of its placement is the
deck and how much is the driver.

Every knob below is read at the decision point, never baked in. The rule
that matters: `greedy` reproduces the engine's historical behaviour
EXACTLY, so ai_selfplay.py reading +0.00 for greedy-vs-greedy is a live
self-test that the plumbing changed nothing. Any pilot that reads non-zero
against itself is broken, not interesting.

Knobs, and what each one is really asking:

  ko_bonus_per_prize    how much is taking a Prize worth against raw damage
  overkill_penalty      how much does damage past a Knock Out cost you
  prize_liability       do you avoid exposing a 2- or 3-Prize attacker
  rider_scale           how much are non-damage riders worth
  setup_scale           ... and specifically the ones that build your board
  retreat_per_energy    how dearly you hold the Energy a retreat discards
  retreat_flat          the fixed tempo cost of retreating at all
  self_lock_divisor     how much an attack that locks you out next turn costs
  promote               after a Knock Out: "healthy" body or best "attacker"
  gust                  "prize" (aware) or "weakest" target
  energy_to_active      attach to the Active first, or to the best body
  pitch_energy_guard    how hard to protect Energy when paying a hand cost
"""

GREEDY = {
    "name": "greedy",
    "blurb": "maximise damage and Prizes this turn. The engine's historical pilot.",
    "ko_bonus_per_prize": 120,
    "overkill_penalty": 0.5,
    "prize_liability": 0,
    "rider_scale": 1.0,
    "setup_scale": 1.0,
    "retreat_per_energy": 30,
    "retreat_flat": 10,
    "self_lock_divisor": 2.0,
    "promote": "healthy",
    "gust": "prize",
    "energy_to_active": True,
    "pitch_energy_guard": 1.0,
    # One-turn lookahead on the attack choice: 0 is off (greedy).
    "lookahead_samples": 0,
    "lookahead_margin": 0.0,
    # Bench the Basics that reach the hand after the Supporter (Ultra Ball,
    # draw), not a turn later. Paired, 6 meta decks x 53 opponents x 200
    # games: +0.97 +/- 0.27 (every deck positive).
    "bench_after_supporter": 1,
    # A second pass of once-per-turn Abilities after attach/evolve, and
    # moved damage counters aimed at a Knock Out. Under measurement.
    "abilities_late": 0,
    "counter_ko_target": 0,
}

# Prizes are the win condition, so chase them: a Knock Out is worth far
# more than the damage that produced it, overkill is cheap, and a retreat
# that gets a real attacker into the Active Spot is worth paying for.
AGGRO = dict(GREEDY, **{
    "name": "aggro",
    "blurb": "chase Knock Outs; overkill is cheap and tempo is worth Energy.",
    "ko_bonus_per_prize": 240,
    "overkill_penalty": 0.1,
    "rider_scale": 0.5,
    "setup_scale": 0.4,
    "retreat_per_energy": 12,
    "retreat_flat": 0,
    "promote": "attacker",
})

# Damage is a means, not the point. Value disruption and denial, keep the
# investment on the board, and do not hand over Prizes cheaply.
CONTROL = dict(GREEDY, **{
    "name": "control",
    "blurb": "value disruption and board investment over raw damage.",
    "ko_bonus_per_prize": 70,
    "overkill_penalty": 0.9,
    "prize_liability": 45,
    "rider_scale": 2.0,
    "setup_scale": 1.3,
    "retreat_per_energy": 45,
    "retreat_flat": 20,
    "self_lock_divisor": 3.0,
    "pitch_energy_guard": 1.8,
})

# The first turns decide the game for a deck that has to assemble
# something. Pay for board development up front and accept a slower clock.
SETUP = dict(GREEDY, **{
    "name": "setup",
    "blurb": "build the board first; a 0-damage developing turn is fine.",
    "ko_bonus_per_prize": 100,
    "rider_scale": 1.4,
    "setup_scale": 2.5,
    "retreat_per_energy": 35,
    "energy_to_active": False,
    "pitch_energy_guard": 1.5,
})

# Both players are racing to six. Weigh a Knock Out by how much of that
# race it actually finishes, and price what you are exposing in return.
PRIZEWISE = dict(GREEDY, **{
    "name": "prizewise",
    "blurb": "weigh every trade against the Prize map, both directions.",
    "ko_bonus_per_prize": 120,
    "overkill_penalty": 0.7,
    "prize_liability": 70,
    "rider_scale": 1.1,
    "promote": "healthy",
    "gust": "prize",
})

# Greedy in everything but the attack: each payable attack is played out
# through the opponent's whole reply turn, N times, and the best position
# wins. Built for decks whose attacks pay off on the OPPONENT's turn (locks,
# Sleep, "can't retreat") -- which greedy can only guess at.
LOOKAHEAD = dict(GREEDY, **{
    "name": "lookahead",
    "blurb": "greedy, but each attack is played out through the opponent's reply.",
    "lookahead_samples": 4,
    "lookahead_margin": 10.0,
})

POLICIES = {p["name"]: p for p in (GREEDY, AGGRO, CONTROL, SETUP, PRIZEWISE, LOOKAHEAD)}
# The engine's historical pilot answers to its old name too, so existing
# callers and recorded measurements keep working.
POLICIES["v2"] = GREEDY
POLICIES["v1"] = GREEDY


def get(name):
    """The policy dict for a name, falling back to greedy."""
    return POLICIES.get(name or "greedy", GREEDY)


def knob(pl, key):
    """One knob for whichever pilot this player is running."""
    return get(getattr(pl, "policy", None))[key]
