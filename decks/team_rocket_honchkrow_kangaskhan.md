# Team Rocket's Honchkrow / Kangaskhan ex (Supporter engine)

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Murkrow → Honchkrow, Kangaskhan ex.

## Plan

Everything is fed by Team Rocket Supporters. **Kangaskhan ex**
(230 HP Basic) hits **220 for CCC** on any turn you played a Team Rocket
Supporter (Wicked Impact 120 + 100). **Honchkrow** turns spare Team Rocket
Supporters in hand into damage: Rocket Feathers (CC) discards any number of
them for **60 each**, so 3 is 180 and 4 is 240. **Murkrow's Deceit** (C)
searches any Supporter.

The engine: 4 Ariana (draw to 8, all Team Rocket's), 4 Petrel, 3 Proton,
2 Archer, 2 Giovanni, 4 Transceiver (finds a Team Rocket Supporter) and
2 Factory (draw 2 after one).

## How to play

1. **Turn 1.** Proton: Kangaskhan ex plus two Murkrow. Attach (Team
   Rocket's Energy pays 2 of the 3).
2. **Turn 2.** Play a Team Rocket Supporter (Ariana or Petrel), draw 2 off
   Factory, and Wicked Impact for 220. Evolve Murkrow → Honchkrow on the Bench.
3. **When Kangaskhan ex falls.** Honchkrow comes up and cashes the Supporters
   you couldn't play (you play only one per turn) at 60 each. Archer (only if a
   Team Rocket's Pokémon was Knocked Out last turn) resets both hands, 5 for
   you and 3 for them.
4. **Giovanni** switches your Active Team Rocket's Pokémon with a Benched one,
   *then* gusts. Use it to bring Kangaskhan ex up and pick the target.

**Their outs.** Kangaskhan ex gives up 2 Prizes and is weak to Fighting.
Honchkrow (130 HP) is weak to Lightning. Hand disruption (Iono-type resets)
strips Honchkrow's fuel.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Draft: Honchkrow + Porygon-Z + Kangaskhan ex | 64.75% |  |
| **Honchkrow + Kangaskhan ex only (4/4/4)** | **70.71%** | +6.0 (Porygon-Z was dead weight) |
| Porygon-Z + Kangaskhan ex only | 64.16% | → own deck |
| Honchkrow version + Maximum Belt | 70.63% | −0.08 ± 0.48 |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Murkrow | 99.4% | 1.57 |
| Team Rocket's Honchkrow | 94.2% | 2.94 |
| Team Rocket's Kangaskhan ex | 98.7% | 1.52 |

First attack by turn 6 in 89.9% of games (average turn 2.95).

## PTCGL import

```
Pokémon: 12
4 Team Rocket's Murkrow ASC 126
4 Team Rocket's Honchkrow ASC 127
4 Team Rocket's Kangaskhan ex ASC 162

Trainer: 36
4 Buddy-Buddy Poffin MEG 167
3 Ultra Ball MEG 131
1 Poké Pad ASC 198
3 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
4 Team Rocket's Petrel ASC 207
2 Team Rocket's Archer ASC 201
2 Team Rocket's Giovanni ASC 204
4 Team Rocket's Transceiver ASC 209
2 Team Rocket's Factory ASC 203
2 Lillie's Determination MEG 119
1 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Air Balloon MEG 166

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
