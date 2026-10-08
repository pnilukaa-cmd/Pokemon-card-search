# Team Rocket's Moltres ex / Houndoom

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Moltres ex, Houndour → Houndoom.

## Plan

**Moltres ex** (220 HP Basic): Flame Screen (FCC) 110, and it takes
50 less damage next turn. **Evil Incineration** (FCCC): discard a Team
Rocket's Energy from Moltres ex to **discard the opponent's Active and
everything attached**. That is not a Knock Out, so no Prize, but their best
attacker and its Energy are gone. **Houndoom** (130 HP): Scorching Fire (FC)
120, or Cruel Coal (F) Burns and Confuses.

## How to play

1. **Turn 1.** Moltres ex and Houndour ×2 down. Fire Energy on Moltres.
2. **Turn 2.** Houndoom online: Scorching Fire 120. Or Moltres Flame Screen 110
   while hiding behind the 50 reduction.
3. **The big threat.** When they power up a 300-HP ex, Moltres ex with a Team
   Rocket's Energy plus Fire throws it away with Evil Incineration. That costs
   one of your 4 Team Rocket's Energy each time.

**Their outs.** Evil Incineration takes no Prize, so the deck still has to
win the race with 120s and 110s. Moltres ex is weak to Lightning,
Houndoom to Water.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Draft: 4-4 Houndoom, 3 Moltres ex, 2 Sneasel | 57.31% |  |
| **4 Moltres ex, no Sneasel** | **61.34%** | +4.0 |
| 3-3 Houndoom, 4 Moltres ex | 61.63% | level, but 40% mulligan |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Houndour | 99.7% | 1.30 |
| Team Rocket's Houndoom | 93.5% | 2.63 |
| Team Rocket's Moltres ex | 98.1% | 1.66 |

First attack by turn 6 in 91.9% of games (average turn 3.14).

## PTCGL import

```
Pokémon: 13
4 Team Rocket's Houndour DRI 37
4 Team Rocket's Houndoom DRI 191
4 Team Rocket's Moltres ex DRI 208

Trainer: 33
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
3 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
1 Team Rocket's Giovanni ASC 204
2 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
1 Team Rocket's Factory ASC 203
2 Switch MEG 130
2 Air Balloon MEG 166
2 Poké Pad ASC 198
1 Hero's Cape TEF 152
1 Energy Search POR 72

Energy: 14
4 Team Rocket's Energy ASC 217
11 Basic Fire Energy

Total Cards: 60
```
