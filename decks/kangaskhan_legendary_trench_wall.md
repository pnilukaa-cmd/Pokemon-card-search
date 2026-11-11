# Mega Kangaskhan ex / Bouffalant wall with Legendary Trench

A submitted list (2026-11-11), reviewed and tuned: Mega Kangaskhan ex
behind Bouffalant's Curly Wall, with Delta Reign's healing (Legendary
Trench doubles every heal, Tasty Rice Ball) and Legendary Pyroduct.

**This list: 84.57% against the 107-deck field at 1000 games per opponent**
(median 88.2%, 102 winning). The list as submitted reads 65.54% (median
67.5%, 94 winning). On the same seeds this list is **+19.03 ± 0.82**,
better on 106 of 107.

The field's existing Kangaskhan / Bouffalant wall
(`snorlax_bouffalant_kangaskhan_curly_wall`: Snorlax, Lillie's Clefairy ex,
18 Energy, Lively Stadium) reads 84.30% on the same seeds (median 90.6%,
100 winning).

- **This list against it overall:** +0.27 ± 0.71, level.
- **Head to head:** this list wins 67.3% (the submitted list 39.9%).

## How the submitted list plays

`measure_wall.py` (in the archive): 80 logged games, 10 each against the
six meta decks, Krookodile ex hand disruption and Mega Absol ex hand lock.

- **56 wins, nearly all on Prizes.** Rapid-Fire Combo, 2.86 a game for 251
  on average, takes 3.54 Prizes a game.
- **The opponent took 2.29 Prizes a game.** By Pokémon Knocked Out: Mega
  Kangaskhan ex 0.68, Smoochum 0.61, Latias ex 0.38, Bouffalant 0.24,
  Munkidori 0.19.
- **Heals:** Jumbo Ice Cream 0.91 a game (healing 79), Tasty Rice Ball 1.21
  (healing 52 of 92 damage). Legendary Trench was in play for only 55% of
  them; Legendary Pyroduct held the Stadium slot much of the rest.
- **It was short of Energy and draw:** 10 Energy for a three-Energy
  attacker and a three-Energy Jumbo Ice Cream, and no draw Supporter.

## What changed, measured

Each change is paired against the list of its round, at 200 games a
matchup.

| Round | From | Change | Measured |
|---|---|---|---|
| 1 | submitted | 14 Energy (+4 Psychic for Ciphermaniac's ×2, Lucky Helmet ×2) | **+9.18 ± 0.56** |
| 1 | submitted | 4 Lillie's Determination (for Aarune ×2, Ciphermaniac's ×2) | **+5.14 ± 0.44** |
| 1 | submitted | Pyroduct → 2 Lillie's / no Tasty Rice Ball / Lively Stadium for Trench | +0.35 / +0.55 / +0.17 |
| 1 | submitted | No Smoochum / 1 Latias ex / 3 Snorlax | −1.29 / −2.17 / −1.54 |
| 2 | both (`L`) | Trench 4 → 2, +2 Switch | +1.07 ± 0.46 |
| 2 | `L` | 16 or 18 Energy / +2 Darkness / 4th Bouffalant | +0.10, +0.14 / +0.53 / −0.35 |
| 3 | Trench 2 (`M`) | Team Rocket engine 8 → 4 (+2 Kofu, +2 Night Stretcher) | **+2.77 ± 0.37** |
| 3 | `M` | Heavy Baton / Snorlax | −1.38 / −2.46 |
| 4 | engine 4 (`N`) | No Team Rocket engine (Kofu 4, Switch 4): this list | **+2.16 ± 0.30** |
| 4 | `N` | Jumbo Ice Cream 4 → 2 | +0.34 |
| 5 | this list | Lively Stadium for Trench / no Tasty Rice Ball / neither Delta Reign card | +0.53 / −0.47 / +0.04 |

What that says about the build's ideas:

- **Energy and draw were the problem, not the plan.** Four Energy and four
  Lillie's Determination were worth +14 between them.
- **The Team Rocket engine** (4 Transceiver, 4 Petrel: any Trainer, found
  by an Item) lost to plain Kofu and Switch twice: +2.77, then +2.16.
- **Legendary Trench and Tasty Rice Ball are neutral, not strong.**
  Replacing both with Lively Stadium and other cards measured +0.04 in the
  final list. Trench doubles the opponent's heals too, and 4 of them
  crowded out Switch. Two Trench are kept; they cost nothing.
- **Legendary Pyroduct** (Evolution Pokémon have no Abilities) does nothing
  for an all-Basic deck except against Evolution decks: +0.35 to cut.
- **Smoochum and Latias ex earn their slots.** Smoochum gives up Prizes
  (0.47 a game), but cutting it measured −1.29. Latias ex's free retreat
  for an all-Basic deck measured −2.17 to cut one.

## How this list plays

`measure_wall.py`, 80 logged games, the same eight opponents:

- **71 wins: 70 on Prizes, 1 by deck-out.**
- **The opponent took 1.51 Prizes a game;** this list took 5.79. Games
  run 14.9 turns.
- **Rapid-Fire Combo:** 3.46 a game for 249 on average, 4.40 Prizes a
  game. Latias ex's Eon Blade adds 0.72.
- **Heals:** Jumbo Ice Cream 0.97 a game (healing 72), Tasty Rice Ball 0.88
  (healing 54), Trench up for about half of them.

## How it plays, turn by turn

- **Setup:** Precious Trolley or Poké Pad for the Basics. Two Bouffalant
  in play switch Curly Wall on: 60 less damage to every Basic Colorless
  Pokémon (Kangaskhan, Bouffalant), not stacking. Smoochum's Delightful
  Kiss (no Energy) puts 2 Psychic Energy on a Benched Pokémon.
- **Each turn:** Mega Kangaskhan ex's Run Errand draws 2 in the Active
  Spot. Attach toward Rapid-Fire Combo (200, plus 50 a heads until tails).
  Munkidori with a Darkness Energy moves 3 damage counters off your
  Pokémon onto theirs every turn.
- **Healing:** Jumbo Ice Cream needs 3 Energy on the Active; Tasty Rice
  Ball grows with each copy in the discard. Legendary Trench doubles both,
  for the opponent as well.
- **Their outs:**
  - Fighting attackers: Kangaskhan, Bouffalant and Snorlax are weak to
    Fighting.
  - Damage that is not "from attacks": counters.
  - Knocking out Smoochum or Latias ex for cheap Prizes.

## Where it loses

At 1000 games, the submitted list → this list:

| Opponent | Submitted | This list |
|---|---|---|
| Dragapult ex (pure / Dusknoir / Blaziken) | 61.1 / 69.5 / 68.8% | 85.3 / 87.3 / 86.0% |
| Raging Bolt ex / Mega Excadrill ex | 61.0 / 50.1% | 81.9 / 68.2% |
| Slowking / N's Zoroark ex / Festival Lead | 74.8 / 80.1 / 87.7% | 93.1 / 87.9 / 97.7% |
| The field's Kangaskhan / Bouffalant wall | 39.9% | 67.3% |
| Delta Reign decks: Mega Malamar ex / Bug Out / Maushold mill | 30.5 / 73.9 / 63.1% | 52.7 / 95.0 / 31.2% |

Worst for this list:

- Tauros / Risky Ruins: 31.0%
- The Maushold mill list: 31.2%. Kangaskhan's attacks are no use against
  Pokémon that give up no Prizes, and the heal deck runs out of cards first.
- Mega Froslass ex: 33.6%
- Mega Zygarde ex / Cinderace (Gaia Wave): 34.5%
- N's Zoroark ex toolbox: 47.2%

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | Submitted | This list |
|---|---|---|
| Mega Kangaskhan ex | 79.5% (avg turn 1.86) | 81.9% (1.79) |
| Bouffalant | 83.4% (2.32) | 80.8% (2.13) |
| First attack by turn 6 | 88.6% (2.95) | 96.3% (2.75) |

**Basics:** all 13 Pokémon are Basics, a 16.3% chance of no Basic in the
opening hand. The baseline now plays Ciphermaniac's Codebreaking, and lists
Tasty Rice Ball as heal-only; both were unmodeled.

## Import

```
Pokémon: 13
4 Mega Kangaskhan ex MEG 104
3 Bouffalant PR-SV 136
2 Latias ex SSP 76
2 Munkidori TWM 95
2 Smoochum SSP 75

Trainer: 33
4 Lillie's Determination MEG 119
4 Kofu SCR 138
2 Crispin SCR 133
2 Boss's Orders ASC 183
4 Jumbo Ice Cream PFL 91
4 Tasty Rice Ball DLR 101
4 Switch MEG 130
3 Poké Pad ASC 198
3 Night Stretcher ASC 196
1 Precious Trolley SSP 185
2 Legendary Trench DLR 98

Energy: 14
9 Basic Psychic Energy
3 Basic Darkness Energy
2 Mist Energy TEF 161

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-11-11/kangaskhan_trench_screens`. The
list is in the field as `decks/field/kangaskhan_legendary_trench_wall.txt`.
