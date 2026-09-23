# Paralysis retreat-lock — "You Are Not Going Anywhere"

Built for the brief: *a deck focused around paralyze to prevent retreating.*

**69.86% (±0.46) across all 45 field decks, 1000 games each, winning 41 of 45.**
Rank 3 in the field, behind lurantis_heal_punish (73.00) and
team_rockets_persian_ex_attack_theft (71.97).

```
Pokémon: 14
4 Wiglett TEF 47
4 Wugtrio ex TEF 190
3 Cryogonal SSP 47
3 Misty's Staryu DRI 46

Trainer: 32
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Boss's Orders MEG 114
4 Lillie's Determination MEG 119
4 Switch MEG 130
4 Night Stretcher MEG 173
2 Poké Pad ASC 198
2 Drayton SSP 174
2 Jumbo Ice Cream PFL 91
2 Iris's Fighting Spirit ASC 190

Energy: 14
14 Basic Water Energy

Total Cards: 60
```

60 cards, 10 Basics, 25.9% mulligan, nothing over four copies, no ACE SPEC,
every line resolving to a real printing, Water covering every attack cost.

## What it does

`Wugtrio ex TEF 190` is the engine. Numbing Hold is two Water for 120 damage
plus *"during your opponent's next turn, the Defending Pokémon can't
retreat"*, on a 250 HP Stage 1 that itself retreats for one. Every turn it
hits hard AND pins.

The Paralysis flips do the other half. `Cryogonal SSP 47`'s Ice Beam and
`Misty's Staryu DRI 46`'s Bubble Beam are one Energy each, and a Paralyzed
Pokémon can neither retreat NOR attack — strictly more than Numbing Hold
buys, half the time, off a one-Prize body.

Four `Boss's Orders` decide who gets stranded. Drag up the support Pokémon
they need to cycle, pin it, and kill it where it stands.

Measured over 160 games against four field decks:

```
  attack used: Numbing Hold                  336    2.10 per game
  attack used: Ice Beam                      241    1.51 per game
  attack used: Bubble Beam                   203    1.27 per game
  opponent DENIED A RETREAT (paralyzed)      179    1.12 per game
  opponent DENIED AN ATTACK  (paralyzed)     179    1.12 per game
  opponent DENIED A RETREAT (Numbing Hold)   134    0.84 per game
```

About two prevented escapes per game, split 57/43 between the two halves.
The retreat denials are counted only on turns the opponent's AI actually
tried to move, not every turn a rider was live.

## What the Paralysis is worth

Against a control that is the SAME 60 cards with the Paralysis deleted and
nothing else changed:

| | mean over 45 decks | winning |
|---|---|---|
| this list | **69.86 ± 0.46** | 41/45 |
| Paralysis deleted | 65.28 ± 0.46 | 37/45 |

**+4.58 points, and four more winning matchups.** At 1000 games over 45
fixed opponents the standard error on the difference is 0.33, so the gap
is about 14 sigma.

This number took four wrong answers to reach, which is worth recording:
+9 and +14.8 and +2.1 all came from an 8-deck sample, and two of them
used a "control" that still ran 3 Misty's Staryu -- whose Bubble Beam is
also a Paralysis flip. Only 3 of the 6 Paralysis cards had been swapped.
Once the control was properly matched and the sample was all 45
opponents, the answer stopped moving: 70.04/65.32 at 200 games and
69.86/65.28 at 1000 agree to within 0.18.

The control swaps six cards for their closest legal twins:

| Paralysis card | replacement | what differs |
|---|---|---|
| `Cryogonal SSP 47` Ice Beam W 30 + flip | `Cryogonal BLK 111` Icicle W 30 | same name, 90 HP, Water, 1 Energy, 30 damage |
| `Misty's Staryu DRI 46` Bubble Beam W 20 + flip | `Staryu POR 20` Water Gun W 20 | same species, 70 HP, retreat 1, 1 Energy, 20 damage |

Paralysis helped in **37 of 45** matchups. It pays most against decks that
need their Active to keep doing a job:

```
  ns_zoroark_night_joker_toolbox     67.5 vs 50.0   +17.5
  arbok_muk_condition_stack          78.0 vs 62.5   +15.5
  krookodile_ex_hand_disruption      60.0 vs 45.0   +15.0
  mega_chandelure_ex_retreat_tax     59.0 vs 45.0   +14.0
```

...and it costs points against decks that only ever want to attack from the
Active, where the slots would rather hold a real attacker:

```
  lurantis_heal_punish               38.5 vs 42.5    -4.0
  meta_dragapult_pure                51.5 vs 55.5    -4.0
```

It is not the missed attack that wins the game. It is the Pokémon that
cannot leave.

## Cheap Paralysis beats guaranteed Paralysis

This was the counterintuitive result, and it reversed my prior. Paralysis is
cured at the end of the opponent's next turn, so it buys exactly one turn and
has to be re-applied EVERY turn to be a lock. Packages tried on a common
chassis:

| package | mean, 8-deck sample |
|---|---|
| cheap one-Energy flips (this list) | 59.4 / 57.7 |
| loose control, no Paralysis | 50.4 |
| `Regice ex ASC 48` — guaranteed, WCCC, discards 2 | 48.8 |
| `Weavile ASC 228` — guaranteed, discards ALL its Energy | 42.3 |

A four-Energy guarantee fires roughly three turns in four and takes until
turn four to come online; Weavile locks once and then spends two turns
reloading. Both measured at or BELOW playing no Paralysis at all. A 50% flip
you can throw from turn one delivers more locked turns than either — and on a
one-Prize body instead of a two-Prize one.

The field's own Paralysis deck, `static_venom_drapion`, is built on the
guaranteed-but-expensive plan. This list beats it 89.0.

## Development baseline, 1000 trials

```
  Wiglett          95.8%  avg turn 1.46
  Wugtrio ex       73.1%  avg turn 2.91
  Cryogonal        84.6%  avg turn 1.87
  Misty's Staryu   90.0%  avg turn 1.72
  First attack landed by turn 6: 97.3%   avg final hand 5.05
```

(simulate_baseline's "no modeled play effect" note for Drayton, Iris's
Fighting Spirit and Jumbo Ice Cream refers to that tool's own narrower
registry — all three are modelled and fire in simulate_versus.)

## Matchups

| worst | | best | |
|---|---|---|---|
| lurantis_heal_punish | 38.5 | selective_bloom_cradily | 100.0 |
| team_rockets_persian_ex | 44.5 | wobbuffet_orbeetle | 97.0 |
| scovillain_salazzle | 46.0 | feraligatr_munkidori | 96.0 |
| heracross_sinistcha | 47.5 | meta_ns_zoroark | 95.5 |
| toxic_slumber_vileplume_ex | 48.5 | static_venom_drapion | 89.0 |

It dismantles anything that needs time to assemble and loses to decks that
out-heal 120 a turn (`lurantis_heal_punish` heals 70+) or punish it directly
(`team_rockets_persian_ex` steals the attack it is hit with).

## Cards considered and rejected

- `Pawmot PFL 34` — Voltaic Fist, two Lightning for 130 AND guaranteed
  Paralysis, no discard. The best rate in the pool, but 60 self-damage a turn
  on a 140 HP Stage 2 caps it at two locks per copy, and `Clemont's Quick Wit`
  heals exactly the 60 back only once per turn for one Supporter.
- `Mega Eelektross ex ASC 266` — 350 HP, 190 + guaranteed Paralysis, but it
  discards two Lightning per attack and `Eelektrik`'s Dynamotor only attaches
  to the BENCH, so it cannot refuel itself in the Active Spot.
- `Powerglass SFA 63` — would make `Regice ex` lock every single turn
  (+1 Energy at end of turn, Ice Prison nets −1). It is one of 26 Pokémon
  Tools the engine never attaches, and implementing it alone would have been
  a buff written for this deck while 25 others stayed inert.
- `Dawn PFL 118` — would fetch Wiglett and Wugtrio ex in one card, but it is
  unmodelled and would sit in hand as a dead slot.

## Known engine caveats

Measured on this branch, after six fixes made while building this deck. Three
loose searches remain, affecting 12 field decks and none of this list:
`Crispin`'s "of different types", `Cyrano`'s "Pokémon ex", and the Ascension
family's "a card that evolves from" (currently a universal tutor). All three
make those field decks STRONGER than printed, so this deck's number is
conservative.

`Wugtrio ex` is a Tera Pokémon, and the Tera rule (no damage while Benched)
is not modelled — also conservative here.
