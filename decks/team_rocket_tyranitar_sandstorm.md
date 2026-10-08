# Team Rocket's Tyranitar sandstorm

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Larvitar → Pupitar → Tyranitar, Diglett → Dugtrio, Sneasel.

## Plan

**Sand Stream**: during *every* Pokémon Checkup (after your turn **and**
after theirs) while Tyranitar is Active, put **2 damage counters on each of the
opponent's Basic Pokémon**. That is 40 a round on every Basic, Active and Bench.
Tyranitar (180 HP) attacks with Demolition Tackle (FCCC): 180, and discard an
Energy from their Active. **Sneasel's Strike the Sleeper** (DD) does
**20 per counter to one Benched Pokémon**: 80 after two Checkups, 160 after
four. **Dugtrio's Holes** puts 2 more counters on their Active whenever it
retreats or switches to the Bench during their turn. Pupitar's Explosive
Ascension (C) evolves itself into Tyranitar from the deck.

## How to play

1. **Turn 1.** Poffin / Proton: Larvitar ×2, Sneasel, Diglett.
2. **Turn 2.** Rare Candy a Larvitar from last turn → Tyranitar. Put it
   Active (Air Balloon / Giovanni). Sand Stream starts at this turn's Checkup.
   No Candy? Evolve to Pupitar and attack with Explosive Ascension next turn.
3. **Every turn.** Tyranitar swings 180. Each Checkup chips every Basic.
   Sneasel finishes Benched Basics, and Boss's Orders drags up a softened one.

**Their outs.** Sand Stream only hits **Basic** Pokémon; evolved ones are
immune. It also stops the moment Tyranitar leaves the Active Spot. Tyranitar
is Stage 2 and weak to Grass. Retreating out of the Active Spot costs them 20
to Holes.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| **Draft (4-3-4 Tyranitar, 2 Sneasel, 2-1 Dugtrio)** | **64.04%** | this list |
| Mimikyu + 3rd Sneasel instead of Dugtrio line | 62.16% | −1.88 ± 0.58 |
| 3-2 Dugtrio | 61.92% | worse |
| 2 Brave Bangle | 62.73% | worse |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Larvitar | 99.0% | 1.32 |
| Team Rocket's Pupitar | 81.7% | 2.92 |
| Team Rocket's Tyranitar | 71.4% | 3.66 |
| Team Rocket's Sneasel | 89.4% | 2.01 |
| Team Rocket's Diglett | 94.4% | 1.81 |
| Team Rocket's Dugtrio | 46.9% | 3.65 |

First attack by turn 6 in 85.3% of games (average turn 2.73).

## PTCGL import

```
Pokémon: 16
4 Team Rocket's Larvitar DRI 94
3 Team Rocket's Pupitar DRI 95
4 Team Rocket's Tyranitar DRI 96
2 Team Rocket's Sneasel DRI 128
2 Team Rocket's Diglett ASC 100
1 Team Rocket's Dugtrio ASC 101

Trainer: 32
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
2 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
1 Team Rocket's Giovanni ASC 204
2 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
1 Team Rocket's Factory ASC 203
2 Air Balloon MEG 166
1 Hero's Cape TEF 152
1 Poké Pad ASC 198

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Fighting Energy

Total Cards: 60
```
