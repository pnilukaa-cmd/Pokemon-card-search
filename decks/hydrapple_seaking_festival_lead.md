# Hydrapple / Seaking Festival Lead

Tuned 2026-10-09 from a submitted Hydrapple list
([hydrapple_hydra_breath_festival.md](hydrapple_hydra_breath_festival.md)).
**78.26% against the 82-deck field at 1000 games per opponent, against 52.05%
for the list it came from (+26.55 ± 0.92 paired, better on all 81 shared
opponents).** It would rank first of 78 in the 2026-10-08 round robin
(Raticate rush led with 72.8%); the submitted list sits about 40th.

**Lines:** Applin → Dipplin → Hydrapple, Goldeen → Seaking. Nothing else.

## Plan

**Festival Grounds** turns on **Festival Lead**, which Dipplin TWM 18, Seaking
PRE 21 and Goldeen TWM 44 all have: "this Pokémon may use an attack it has
twice". The Stadium also stops Special Conditions on any Pokémon with
Energy attached.

- **Seaking — Rapid Draw** (C): 60 damage and draw 2. Twice, that's 120
  damage and 4 cards for one Energy of any type.
- **Dipplin — Do the Wave** (G): 20 for each of your Benched Pokémon. Twice
  with a full Bench, that's 200.
- **Hydrapple DRI 18 — Hydra Breath** (G): discard 6 Basic Grass Energy from
  your hand and Knock Out the opponent's Active, whatever it is.
- **Hydrapple — Whip Smash** (GCC): 140.

Seaking and Dipplin do the damage turn after turn. Hydrapple is the closer
for the one thing they can't Knock Out. Bug Catching Set, Energy Retrieval,
Lana's Aid and Max Rod keep the Grass Energy flowing for Hydra Breath and
for re-attaching.

## How to play

1. **Turn 1.** Buddy-Buddy Poffin for Goldeen and Applin; Poké Pad for more.
   Fill the Bench: every Benched Pokémon is 40 more Do the Wave damage
   (20, twice). Play Festival Grounds.
2. **Turn 2 on.** Evolve into Seaking and Dipplin. One Energy on whichever is
   Active, then attack twice. Use Seaking's Rapid Draw when you need cards,
   and Do the Wave when the Bench is full and you need the damage.
3. **Hydrapple** comes in when the Active is too big for 120-200, such as a
   big ex or a healed tank. With 6 Grass Energy in hand, Hydra Breath Knocks
   it Out. Otherwise Whip Smash for 140. Energy Retrieval, Lana's Aid and
   Max Rod refill the hand after a Hydra Breath.
4. **Keep Festival Grounds in play.** Four copies are there so you can put it
   back after the opponent plays their own Stadium. Without it, everything
   attacks once.

**Their outs.** The worst matchups:

| Opponent | Win rate |
|---|---|
| Mega Excadrill drill mill | 41.7% |
| The mirror | 50.3% |
| Lurantis | 53.4% |
| Tauros | 55.6% |
| Raticate rush | 57.0% |
| Moltres / Houndoom | 57.1% |
| Honchkrow / Kangaskhan | 60.6% |

Everything else is above 60%. The best are Flygon mill (97.9%), Mew baby box
(97.8%), Wobbuffet / Orbeetle (97.4%) and Mew / Hypno (95.8%). The deck
mulligans 34.6% of the time with 8 Basics. The win rates include that.

## How it was tuned

200 games against each of the 81 field decks, paired on the same seeds, on
the engine after the fixes in the submitted list's notes. Each round is
paired against the best list of the round before. Lists and results are in
`runs/2026-10-09/hydrapple_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Submitted list | 51.35% | |
| 1 | +1 Hydrapple (−Air Balloon) | 51.40% | +0.05 ± 0.48 |
| 1 | +2 Energy Search | 51.31% | −0.04 ± 0.48 |
| 1 | +2 Rare Candy | 51.09% | −0.25 ± 0.50 |
| 1 | 2-2 Thwackey (−Dunsparce, −Dudunsparce) | 47.91% | −3.43 ± 0.57 |
| 1 | 14 Energy (−Lana's Aid, −Energy Retrieval, −Air Balloon) | 55.94% | +4.59 ± 0.53 |
| 1 | **14 Energy (−Fezandipiti ex, −Air Balloon, −Night Stretcher)** | **58.64%** | **+7.30 ± 0.61** |
| 2 | 16 Energy | 58.80% | +0.15 ± 0.49 |
| 2 | −Dunsparce TEF −Dudunsparce, +2 Energy | 60.31% | +1.67 ± 0.54 |
| 2 | −Shaymin, +Goldeen | 61.59% | +2.94 ± 0.51 |
| 2 | −Grookey −Thwackey, +2 Energy | 62.06% | +3.42 ± 0.60 |
| 2 | **3-3 Seaking for the Thwackey line** | **65.09%** | **+6.45 ± 0.60** |
| 3 | 16 Energy | 65.31% | +0.22 ± 0.51 |
| 3 | 4-4 Seaking (−Lana's Aid, −Energy Retrieval) | 67.01% | +1.92 ± 0.43 |
| 3 | −Shaymin, +Goldeen | 67.94% | +2.85 ± 0.50 |
| 3 | 4-4 Seaking (−Dunsparce TEF, −Dudunsparce) | 69.33% | +4.24 ± 0.53 |
| 3 | **4-4 Seaking (−Shaymin, −Dunsparce TEF)** | **71.20%** | **+6.10 ± 0.58** |
| 4 | 3 Hydrapple (−Lana's Aid) | 69.63% | −1.57 ± 0.50 |
| 4 | 4-4 Dipplin (−Lana's Aid, −Energy Retrieval) | 70.52% | −0.67 ± 0.53 |
| 4 | −1 Dudunsparce, +1 Energy | 71.91% | +0.72 ± 0.50 |
| 4 | 4th Festival Grounds (−Night Stretcher) | 72.41% | +1.21 ± 0.46 |
| 4 | **No Dunsparce / Dudunsparce: +Applin +Dipplin +Hydrapple** | **72.94%** | **+1.74 ± 0.47** |
| 5 | 2 Hydrapple, +1 Energy | 74.28% | +1.35 ± 0.51 |
| 5 | 4th Festival Grounds (−Night Stretcher) | 74.40% | +1.46 ± 0.42 |
| 5 | 2 Hydrapple, +1 Poffin | 74.99% | +2.05 ± 0.47 |
| 5 | **2 Hydrapple +1 Energy, 4th Festival Grounds** | **75.97%** | **+3.03 ± 0.50** |
| 6 | 2nd Boss's Orders (−Lana's Aid) | 74.28% | −1.69 ± 0.44 |
| 6 | 16 Energy (−Energy Retrieval) | 76.19% | +0.22 ± 0.47 |
| 6 | 4th Poffin (−Lana's Aid) | 76.65% | +0.69 ± 0.46 |
| 6 | **No Forest of Vitality, +1 Poffin (this list)** | **78.47%** | **+2.50 ± 0.48** |
| 1000 games | Submitted list / this list | 52.05% / **78.26%** | **+26.55 ± 0.92** |

**What made the difference:**

1. **Energy.** Hydra Breath needs 6 Grass Energy in hand, and every attacker
   needs one on the board. 11 was too few. Hand Energy averaged 1-3 through
   turn 9, and 6 or more turned up in about 1 game in 10. 14-15 is where
   it stops paying.
2. **Festival Lead attackers over support Pokémon.** Thwackey, Dudunsparce,
   Shaymin and Fezandipiti ex each measured worse than another Goldeen,
   Seaking, Applin or Dipplin. Thwackey's Boom Boom Groove searches only
   while a Festival Lead Pokémon is Active, and Seaking's Rapid Draw already
   draws 4 a turn.
3. **Forest of Vitality is a Stadium too.** Playing it replaces your own
   Festival Grounds and switches off every double attack. Cutting it gained
   +2.5.

Holding Energy in hand for Hydra Breath, instead of attaching, measured
worse in every form tried (−3.7 to −16). The deck wins by attacking every
turn with Seaking and Dipplin, and Hydra Breath comes when the hand has the
Energy anyway. In 60 logged games against six hard opponents (Raging Bolt,
Dragapult, Raticate, N's Zoroark, Tauros, Lurantis) this list won 36. It
used Do the Wave 3.3 times a game, Rapid Draw 2.9, Whip Smash 1.0 and
Hydra Breath 0.4. The submitted list won 6 of the same 60.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Applin | 95.8% | 1.46 |
| Dipplin | 76.0% | 2.75 |
| Hydrapple | 37.8% | 4.03 |
| Goldeen | 95.0% | 1.37 |
| Seaking | 72.0% | 2.84 |

First attack by turn 6 in 98.0% of games (average turn 2.85). The baseline
doesn't model Bug Catching Set, Energy Retrieval, Lana's Aid or Max Rod, so
these numbers measure setup speed only.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Max Rod), no
Energy-type shortfall.

## PTCGL import

```
Pokémon: 18
4 Applin TWM 17
4 Dipplin TWM 18
2 Hydrapple DRI 18
4 Goldeen TWM 44
4 Seaking PRE 21

Trainer: 27
4 Lillie's Determination MEG 169
1 Boss's Orders MEG 114
2 Lana's Aid TWM 207
4 Buddy-Buddy Poffin MEG 167
4 Poké Pad POR 113
4 Bug Catching Set TWM 143
3 Energy Retrieval WHT 82
1 Max Rod PRE 116
4 Festival Grounds TWM 149

Energy: 15
15 Basic Grass Energy

Total Cards: 60
```
