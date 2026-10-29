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
    # Rare Candy before evolving Basics into their Stage 1. Paired, 6 Rare
    # Candy decks x 53 opponents x 200 games: +0.52 +/- 0.24.
    "candy_first": 1,
    # A second Item step after the Supporter (Petrel's search, a draw).
    # Paired, 7 decks x 54 opponents x 200 games: +0.90 +/- 0.24.
    "items_after_supporter": 1,
    # Play a "discard down to N" Supporter (Xerosic's Machinations) first
    # when it strips at least this many cards (0: off). Played only as a
    # fallback, Xerosic's did nothing at all. Paired, 200 games x 78
    # opponents: +0.26 on average across the 16 field decks that run it
    # (better on 13), and +3.6 for Raticate rush against Alakazam.
    "hand_trim_first": int(__import__("os").environ.get("HAND_TRIM_FIRST", 3)),
    # Feed a Pokemon whose Ability needs an Energy type attached (Munkidori).
    # Paired, 200 games x 63 opponents: positive on all 8 Munkidori decks
    # (+0.4 to +10.4; Feraligatr/Munkidori +4.51 +/- 0.62).
    "ability_energy": int(__import__("os").environ.get("ABILITY_ENERGY", 1)),
    # Team Rocket's Orbeetle's Rocket Brain ("move 1 damage counter from 1
    # of your Team Rocket's Pokemon to another of your Pokemon", as often as
    # you like) aimed: onto an Active whose attack grows with its own
    # counters, onto a Benched battery for a Rocket Mirror Active, else off
    # a damaged Active. The generic executor moved one counter from the
    # most damaged Pokemon onto whatever came first. Measured paired, 200
    # games x 67 opponents: Orbeetle / Morpeko ex +5.98 +/- 0.64 (better on
    # 57), Wobbuffet / Orbeetle +3.58 +/- 0.56 (better on 53).
    "counter_mover": int(__import__("os").environ.get("COUNTER_MOVER", 1)),
    # Searches take the Pokemon that evolves something in play (or a Stage 2
    # with Rare Candy in hand), then a Basic with Bench room, never a copy of
    # one already in hand. 0: the first match in the shuffled deck. Paired,
    # 200 games x 83 opponents, on for the measured deck only (PILOT=probe):
    # better on all 10 decks tried, +2.62 on average (Dragapult +5.27, Mega
    # Emboar ex +4.15, Lurantis +4.18, Raging Bolt +0.06). Steering only the
    # Evolution picks was no better.
    "smart_search": int(__import__("os").environ.get("SMART_SEARCH", 1)),
    # Only reset the opponent's hand (Distorted Future) when it takes cards
    # away or sets up an exact-count payoff. Measured on the Gothitelle lock,
    # the only card it changes: +2.22 +/- 0.51 at 200 games x 88 decks.
    "hand_reset_guard": int(__import__("os").environ.get("HAND_RESET_GUARD", 1)),
    # Price "damage to each of your Benched Pokemon" by the Prizes it hands
    # over: each own Benched Pokemon it Knocks Out costs this many times
    # ko_bonus_per_prize per Prize. 0 is off. Measured at 200 games x 89
    # decks, on for the measured deck only: Aggron / Diggersby +5.41 +/- 0.52
    # (0.5x -1.05, 2x -1.28 against 1x), Diggersby / Munkidori +3.44 +/- 0.57.
    # Earthquake is the only such attack in the field.
    "self_bench_ko_cost": float(__import__("os").environ.get("SELF_BENCH_KO_COST", 1)),
    # Count an attack's damage counters ("Place 13 damage counters on 1 of
    # your opponent's Pokemon") toward what it would hit for, when ranking
    # who gets Energy. 0 ranks it at its printed damage (often none).
    "counter_potential": int(__import__("os").environ.get("COUNTER_POTENTIAL", 1)),
    # Rank what an evolve-from-deck effect evolves (Dark Awakening: a
    # Haunter into Gengar ex before a Nidoran into Nidorina). 0 takes the
    # first Pokemon in play with the first card found. Off: it measured
    # noise on every deck it touches (2026-10-16, 200 games a matchup: the
    # submitted Gengar list -0.25 +/- 0.48, Grand Tree / Dark Awakening /
    # Ascension field decks -0.0 to +0.68), because the choice seldom has
    # more than one sensible answer.
    "evolve_pick": int(__import__("os").environ.get("EVOLVE_PICK", 0)),
    # Rank "one each to N of your Benched Pokemon" recipients neediest
    # first (Sinister Surge, Glass Trumpet). 0 is the emptiest first.
    # Measured 2026-10-16, 200 games a matchup: the submitted Gengar list
    # +10.46 +/- 0.53, its tuned Toxtricity list +3.78; the Glass Trumpet
    # field decks +0.27 (Raging Bolt) and +0.64 (Tauros).
    "each_attach_rank": int(__import__("os").environ.get("EACH_ATTACH_RANK", 1)),
    # A heal that costs the healed Pokemon its Energy (Wally's Compassion,
    # Super Potion) goes on a Pokemon with no Energy first, and on one with
    # Energy only when it would otherwise be Knocked Out next turn.
    # Measured 2026-10-23, 200 games a matchup: the submitted Mega Dragonite
    # ex / Kangaskhan ex list +2.43 +/- 0.52, its 12-Energy version +2.54;
    # the two field decks with such a heal +0.93 and -0.28.
    "heal_cost_aware": int(__import__("os").environ.get("HEAL_COST_AWARE", 1)),
    # A manual attachment goes where the Energy in hand pays part of an
    # attack, not just to whoever is short a number of Energy (Fire on a
    # Pokemon that needs Water and Lightning). 0: count only.
    # Measured 2026-10-23, 200 games a matchup, on all 12 field decks with
    # two or more Energy types: +0.23 to +14.99, none worse (the Dragapult
    # lists +7.4 to +9.9, Salazzle ex / Muk +14.99, Raging Bolt +5.06).
    "typed_attach": int(__import__("os").environ.get("TYPED_ATTACH", 1)),
    # Switch (the Item whose only text is the switch) is played when a
    # Benched Pokemon does more this turn than the Active -- an Asleep or
    # Paralyzed Active does nothing -- and goes to that Pokemon. 0: played
    # on sight, to the healthiest body.
    # Measured 2026-10-23, 200 games a matchup: a submitted Snorlax /
    # Bouffalant list +12.39 +/- 0.71, a Chesnaught / Meganium build +2.29;
    # 8 field decks with Switch +0.28 to +5.83, none worse (Crabominable
    # +5.83, Festival Lead +5.62, Trevenant +3.65).
    "switch_pick": int(__import__("os").environ.get("SWITCH_PICK", 1)),
    # Rare Candy, evolution and Pokemon searches go first to the line of an
    # evolved Pokemon whose passive Ability works for your whole side (Wild
    # Growth, Archaludon's Metal Bridge) while none is in play. 0: first match.
    # Measured 2026-10-23, 200 games a matchup: a Meganium / Alolan
    # Exeggutor list +2.27 +/- 0.44, its Chesnaught version +0.03; the
    # field decks it touches +0.92, +0.82, +0.20. With Basic engines
    # included as well, the Raging Bolt list (Latias ex) measured -1.50.
    "engine_first": int(__import__("os").environ.get("ENGINE_FIRST", 1)),
    # Damage per card milled off your own deck (Hammer-lanche): each card
    # costs this much, scaled up as the deck runs down. 0: free.
    # Measured 2026-10-26, 200 games a matchup, on the two Mega Abomasnow
    # ex lists it touches: +9.84 +/- 0.65 and +7.35 +/- 0.64 (10 per card:
    # +9.23, +7.24). No field deck has such an attack.
    "self_mill_cost": float(__import__("os").environ.get("SELF_MILL_COST", 5)),
    # An Energy discarded at the end of your turn (Ignition) is attached
    # only to the Active, and only when it raises the Active's damage this
    # turn. 0: attached like any other Energy.
    # Measured 2026-10-28, 200 games a matchup: a submitted Jellicent ex
    # list with 4 Ignition Energy +1.37 +/- 0.41. No field deck runs it.
    "temp_energy_now": int(__import__("os").environ.get("TEMP_ENERGY_NOW", 1)),
    # Boss's Orders and the gust Trainers only for a Knock Out this turn,
    # worked out against the target itself; otherwise held. 0: the Benched
    # Pokemon with the least HP left, every time.
    # Measured 2026-10-28, 200 games a matchup, on the 11 decks it touches
    # out of 12: +0.97 on average, 9 better. Jellicent ex (4 Boss) +1.75,
    # Mega Chandelure ex +1.30, N's Zoroark +2.39, Raging Bolt +2.19,
    # Dragapult / Blaziken +1.07; Mega Excadrill -0.36 and Dragapult /
    # Dusknoir -0.44 (each about +/- 0.45). Slowking, with no gust, 0.
    "gust_for_ko": int(__import__("os").environ.get("GUST_FOR_KO", 1)),
    # With no Knock Out, gust up a Pokemon that can neither attack nor
    # retreat next turn. 0: hold. Measured 2026-10-28, 200 games a matchup
    # on the seven decks it touches: +0.86 on average, none worse beyond
    # noise (Jellicent ex with 4 Boss's Orders +1.49, Mega Chandelure ex
    # +1.11 / +1.05, Dragapult ex +1.64, N's Zoroark ex +0.68, Raging Bolt
    # ex +0.05, Jellicent ex with 1 Boss +0.01); Slowking, with no gust, 0.
    # Only under an Item lock: +0.74 where always gave +1.49.
    "gust_strand": int(__import__("os").environ.get("GUST_STRAND", 1)),
    # Price "put Pokemon from your discard pile onto your Bench" attacks
    # (King's Order, Come and Get You). 0: no price, never chosen -- 0 uses
    # in 60 games of a Kingdra ex list built on King's Order. On because an
    # attack the AI never picks is an inert card, not because it measured:
    # the submitted Kingdra ex list -0.23 +/- 0.32 at 1000 games a matchup;
    # at 200, the three Duskull decks +0.31 / +0.03 / -0.02.
    "recover_price": int(__import__("os").environ.get("RECOVER_PRICE", 1)),
    # Gwynn, Prism Tower and Brilliant Blender discard what King's Order
    # can bench from the discard (and Energy for Seething Spirit). 0: off,
    # and Brilliant Blender is never played in such a deck. On top of
    # recover_price: +0.33 +/- 0.36 at 1000 games on the same list.
    "recover_fuel": int(__import__("os").environ.get("RECOVER_FUEL", 1)),
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
# "probe": greedy with knobs overridden from PROBE_KNOBS ("smart_search=1,
# other=0.5"), for measuring a knob on ONE deck (vs_field.py PILOT=probe)
# while the field keeps playing greedy. An env knob changes every player,
# so a paired run with it measures the field getting better too.
POLICIES["probe"] = dict(GREEDY, name="probe", **{
    k: float(v) for k, v in (kv.split("=") for kv in
                             __import__("os").environ.get("PROBE_KNOBS", "").split(",") if kv)})
POLICIES["v2"] = GREEDY
POLICIES["v1"] = GREEDY


def get(name):
    """The policy dict for a name, falling back to greedy."""
    return POLICIES.get(name or "greedy", GREEDY)


def knob(pl, key):
    """One knob for whichever pilot this player is running."""
    return get(getattr(pl, "policy", None))[key]
