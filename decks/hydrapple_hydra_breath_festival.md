# Hydrapple / Hydra Breath Festival (submitted list)

A list submitted for study on 2026-10-09. The plan: get Hydrapple to Knock Out
anything with Hydra Breath. It is in the field as submitted. The import below
uses current printings: Boss's Orders RCL 189 → MEG 114, and Energy Retrieval
CRI 108 → WHT 82 (same text).

**52.05% against the 81-deck field at 1000 games per opponent** (median 50.2%,
41 winning matchups), about 40th of 78 in the 2026-10-08 round robin. The
tuned version,
**[hydrapple_seaking_festival_lead.md](hydrapple_seaking_festival_lead.md),
scores 78.26% (+26.55 ± 0.92 paired, better on all 81)**.

## Plan

**Hydrapple DRI 18's Hydra Breath** (G): discard 6 Basic Grass Energy from
your hand and Knock Out the opponent's Active. **Whip Smash** (GCC) does 140.

With Festival Grounds in play, **Festival Lead** lets Dipplin TWM 18, Seaking
PRE 21 and Goldeen TWM 44 attack twice:
- Do the Wave: 20 per Benched Pokémon.
- Rapid Draw: 60 and draw 2.

**Thwackey's Boom Boom Groove** searches for any card while a Festival Lead
Pokémon is Active. **Forest of Vitality** lets Grass Pokémon evolve the turn
they're played.

## What the simulator found

**Three engine fixes** (2026-10-09; +2.81 ± 0.59 for this list):
- **Bug Catching Set** took the single top card of the 7, of any kind. It now
  takes up to 2 Grass Pokémon or Basic Grass Energy. Drayton, Roto-Stick and
  Tropius's Fruity Aroma had the same bug.
- **Forest of Vitality** let any Pokémon evolve early, even Goldeen into
  Seaking. It now covers only Grass into Grass, and not on your first turn.
- **Hydra Breath** was already modeled.

**Hydra Breath rarely happens.** Hand Energy averaged 1-3 through turn 9,
and 6 or more turned up in about 1 game in 10. Hydra Breath fired 0.15
times per game. With 11 Grass Energy, and Max Rod, Energy Retrieval and
Lana's Aid only able to recover Energy already in the discard pile, the
hand rarely gets to 6.

**Holding Energy in hand doesn't fix it.** Making the pilot keep Grass
Energy in hand instead of attaching measured −3.7 to −16 in every form
tried. It starves the attackers.

**The attackers that win are Seaking and Dipplin.** With Festival Grounds
they attack twice every turn. More of them, more Energy, and no Forest of
Vitality (a second Stadium that knocks out your own Festival Grounds) is
what took the list from 51% to 78%. Full tables are in the
[tuned list's notes](hydrapple_seaking_festival_lead.md).

**Matchups (1000 games):**
- **Worst:** Mega Excadrill drill mill 17.7%, Mew / Lonestar / Dragapult
  23.5%, Moltres / Houndoom 23.5%, Raticate rush 24.2%, Mega Excadrill
  24.7%, Honchkrow 24.9%, Nidoking ex 25.1%.
- **Best:** Drapion 88.2%, Wobbuffet / Orbeetle 87.8%, Flygon mill 86.9%,
  Mew baby box 86.4%.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Applin | 80.2% | 1.78 |
| Dipplin | 46.5% | 3.23 |
| Hydrapple | 19.2% | 4.14 |
| Goldeen | 70.0% | 1.99 |
| Seaking | 32.1% | 3.53 |
| Grookey | 45.9% | 2.25 |
| Thwackey | 11.7% | 3.90 |
| Dudunsparce | 22.1% | 3.64 |

First attack by turn 6 in 88.7% of games (average turn 2.72). The baseline
doesn't model Bug Catching Set, Energy Retrieval, Lana's Aid or Max Rod.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Max Rod),
10 Basics (mulligan 25.9%).

## PTCGL import

```
Pokémon: 20
2 Hydrapple DRI 18
2 Seaking PRE 21
1 Shaymin DRI 10
1 Thwackey TWM 15
3 Dipplin TWM 18
1 Fezandipiti ex ASC 288
1 Dunsparce JTG 120
1 Dunsparce TEF 128
2 Dudunsparce TEF 129
1 Grookey TWM 14
2 Goldeen TWM 44
3 Applin TWM 17

Trainer: 29
1 Forest of Vitality POR 109
2 Night Stretcher MEG 173
4 Lillie's Determination MEG 169
1 Air Balloon MEG 166
3 Buddy-Buddy Poffin MEG 167
1 Max Rod PRE 116
4 Poké Pad POR 113
2 Lana's Aid TWM 207
3 Energy Retrieval WHT 82
4 Bug Catching Set TWM 143
1 Boss's Orders MEG 114
3 Festival Grounds TWM 149

Energy: 11
11 Basic Grass Energy

Total Cards: 60
```
