# Team Rocket's Raticate / Ampharos (evolution tax)

<!-- field-results -->
> ### Field results — 2026-10-08
> **63.6% mean · 61.7% median · 67 of 76 winning matchups · rank 11 of 77**
>
> Best `mew_baby_box` 94% · worst `ns_zoroark_night_joker_toolbox` 38%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Mareep → Flaaffy → Ampharos (Ability only), Rattata → Raticate, Meowth → Persian ex.

## Plan

The **Ampharos line's best home**. **Darkest Impulse**: whenever the
opponent plays a Pokémon from their hand to evolve, put 4 damage counters on
it (doesn't stack). It needs no Energy, so Ampharos sits on the Bench taxing
every evolution while the Raticate rush (90 for one Energy) takes Prizes.
The deck runs no Lightning, so Head Bolt is never used. That is intentional.

## How to play

1. **Turn 1.** Bench Rattata, Mareep (Procurement, C, searches an Item)
   and Meowth.
2. **Turn 2-3.** Raticate attacks every turn. Evolve Mareep → Flaaffy →
   Ampharos when there is a spare turn. Every Stage 1 / Stage 2 the opponent
   evolves from hand then starts with 40 damage.

**Their outs.** Against Basic-only decks Ampharos is 6 dead cards. Costs
10 points against plain Raticate rush (75.0%).

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Standalone Ampharos / Zapdos (Head Bolt 140, Wicked Thunder 120) | 51.93% |  |
| standalone + extra Flaaffy | 50.90% |  |
| standalone + 2 Brave Bangle | 52.31% | → `team_rocket_ampharos_zapdos.ptcgl.txt` |
| **Ampharos as a tax in the Raticate shell** | **65.12%** | this list |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Rattata | 99.5% | 1.36 |
| Team Rocket's Raticate | 86.3% | 2.82 |
| Team Rocket's Mareep | 94.0% | 1.90 |
| Team Rocket's Flaaffy | 46.4% | 3.80 |
| Team Rocket's Ampharos | 22.6% | 4.72 |
| Team Rocket's Meowth | 92.9% | 1.95 |
| Team Rocket's Persian ex | 54.7% | 3.66 |

First attack by turn 6 in 94.2% of games (average turn 2.73).

## PTCGL import

```
Pokémon: 14
4 Team Rocket's Rattata DRI 147
4 Team Rocket's Raticate DRI 148
2 Team Rocket's Mareep DRI 72
1 Team Rocket's Flaaffy DRI 73
2 Team Rocket's Ampharos DRI 74
2 Team Rocket's Meowth ASC 161
2 Team Rocket's Persian ex DRI 150

Trainer: 34
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
2 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
2 Team Rocket's Petrel ASC 207
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
2 Team Rocket's Factory ASC 203
2 Brave Bangle PBL 104
2 Air Balloon MEG 166
1 Maximum Belt TEF 154

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
