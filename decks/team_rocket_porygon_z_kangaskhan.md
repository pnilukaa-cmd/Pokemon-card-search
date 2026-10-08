# Team Rocket's Porygon-Z / Kangaskhan ex

<!-- field-results -->
> ### Field results — 2026-10-08
> **63.1% mean · 62.8% median · 65 of 76 winning matchups · rank 14 of 77**
>
> Best `static_venom_drapion` 91% · worst `ditto_transform_hydreigon` 32%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Porygon → Porygon2 → Porygon-Z, Kangaskhan ex, Chingling.

## Plan

**Porygon-Z** (Stage 2, 140 HP) hits 20 for every Team Rocket Supporter
in your **discard pile** (R Command, CC). Its Ability **Reconstitute** discards
2 cards from your hand to draw 1 each turn, a way to bin spare Supporters on
purpose. Every Supporter you play also adds one. Mid-game the discard holds 8+
and R Command does 160+. **Kangaskhan ex** carries the early game (220 after a
Team Rocket Supporter). Rare Candy gets Porygon-Z out on turn 2.

## How to play

1. **Turn 1.** Proton for Porygon ×2 and Kangaskhan ex.
2. **Turn 2.** Team Rocket Supporter → Kangaskhan ex Wicked Impact 220.
   Rare Candy a Porygon (played last turn) → Porygon-Z.
3. **Turn 3+.** Reconstitute dumps spare Supporters. When Kangaskhan ex falls,
   Porygon-Z attacks for 20 × (Team Rocket Supporters in the discard).

**Their outs.** Porygon-Z needs time for the count to build, so a fast deck
can race it. It is 1-Prize and weak to Fighting.
It measured 6.5 points under the Honchkrow build in the same shell:
Honchkrow cashes the Supporters straight from hand.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Honchkrow + Porygon-Z + Kangaskhan ex | 64.75% |  |
| **Porygon-Z + Kangaskhan ex (4-1-3, 3 Rare Candy)** | **64.16%** | this list |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Porygon | 99.6% | 1.32 |
| Team Rocket's Porygon2 | 69.4% | 3.27 |
| Team Rocket's Porygon-Z | 67.3% | 4.04 |
| Team Rocket's Kangaskhan ex | 98.0% | 1.68 |
| Team Rocket's Chingling | 83.3% | 1.96 |

First attack by turn 6 in 90.0% of games (average turn 2.91).

## PTCGL import

```
Pokémon: 13
4 Team Rocket's Porygon DRI 153
1 Team Rocket's Porygon2 DRI 154
3 Team Rocket's Porygon-Z DRI 155
4 Team Rocket's Kangaskhan ex ASC 162
1 Team Rocket's Chingling DRI 85

Trainer: 35
3 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
3 Ultra Ball MEG 131
2 Poké Pad ASC 198
3 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
3 Team Rocket's Petrel ASC 207
2 Team Rocket's Archer ASC 201
2 Team Rocket's Giovanni ASC 204
4 Team Rocket's Transceiver ASC 209
2 Team Rocket's Factory ASC 203
1 Night Stretcher MEG 173
2 Air Balloon MEG 166

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
