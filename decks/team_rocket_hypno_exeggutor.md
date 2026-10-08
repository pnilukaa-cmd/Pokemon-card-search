# Team Rocket's Hypno / Exeggutor / Mewtwo ex

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Exeggcute → Exeggutor, Drowzee → Hypno, Mewtwo ex.

## Plan

The **Exeggutor line's best measured home**. **Exeggutor**
(140 HP): Double-Edge (PCC) 150 and 30 to itself. Tri Kinesis (CC) flips
3 coins, and all heads (12.5%) Knocks Out any one of their Pokémon. Paired
with Hypno's Bench Manipulation and Mewtwo ex as the big finisher.

## How to play

1. **Turn 1.** Bench Exeggcute, Drowzee, Mimikyu.
2. **Turn 2.** Exeggutor Double-Edge 150 (Team Rocket's Energy + Psychic).
3. **Mid-game.** Hypno into a full Bench, Mewtwo ex once 4 Team Rocket's are
   in play.

**Their outs.** Exeggutor's self-damage shortens its life. Darkness Weakness.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| **Hypno + Exeggutor + Mewtwo ex** | **56.99%** | this list |
| Exeggutor-heavy (4-4) | 55.76% | worse |
| Exeggutor as Rocket Brain fuel in Orbeetle / Morpeko | 56.72% | worse than without |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Drowzee | 98.4% | 1.65 |
| Team Rocket's Hypno | 80.8% | 3.24 |
| Team Rocket's Exeggcute | 97.6% | 1.50 |
| Team Rocket's Exeggutor | 72.7% | 3.18 |
| Team Rocket's Mewtwo ex | 71.7% | 2.21 |
| Team Rocket's Mimikyu | 74.7% | 1.94 |

First attack by turn 6 in 88.8% of games (average turn 2.85).

## PTCGL import

```
Pokémon: 16
4 Team Rocket's Drowzee DRI 79
3 Team Rocket's Hypno DRI 80
3 Team Rocket's Exeggcute ASC 77
3 Team Rocket's Exeggutor ASC 78
2 Team Rocket's Mewtwo ex ASC 281
1 Team Rocket's Mimikyu ASC 238

Trainer: 31
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
2 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
1 Team Rocket's Factory ASC 203
2 Switch MEG 130
2 Air Balloon MEG 166
1 Hero's Cape TEF 152
1 Team Rocket's Giovanni ASC 204
2 Poké Pad ASC 198

Energy: 13
4 Team Rocket's Energy ASC 217
9 Basic Psychic Energy

Total Cards: 60
```
