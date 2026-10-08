# Team Rocket's Raticate rush

<!-- field-results -->
> ### Field results — 2026-10-08
> **72.8% mean · 72.0% median · 74 of 76 winning matchups · rank 1 of 77**
>
> Best `mew_baby_box` 98% · worst `ns_zoroark_night_joker_toolbox` 43%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Rattata → Raticate (main), Meowth → Persian ex, Kangaskhan ex.

## Plan

Single-Prize aggression. **Team Rocket's Raticate** (Stage 1, 90 HP) attacks
for **90 with one Energy of any type** (Reckless Abandon, C). Flip 2 coins: on
two tails (25%) it also does 90 to itself, which usually Knocks it Out. With
**Brave Bangle** (no Rule Box: +30 against an Active ex) it hits an ex for 120,
and **Maximum Belt** (+50 against an ex) for 140. Every Raticate the opponent
Knocks Out gives up one Prize while it takes two from their ex.

**Persian ex** borrows an attack from the top 10 cards of the opponent's deck
(Haughty Order, CC) or hits 140 and Confuses (Cruel Slash, CCC).
**Kangaskhan ex** hits 220 (Wicked Impact, CCC) on any turn you played a Team
Rocket Supporter. Every Pokémon is Team Rocket's, so **Ariana** always draws
to 8.

## How to play

1. **Turn 1.** Proton (legal on turn 1 going first) or Buddy-Buddy Poffin
   for 2-3 Rattata and a Meowth. Attach any Energy to a Rattata. Going second,
   Rattata's Dangerous Incisors (C) does 10 and Poisons.
2. **Turn 2.** Evolve Rattata → Raticate (no evolving on either player's first
   turn). Attach Energy, Brave Bangle or Maximum Belt, then Reckless Abandon
   for 90 / 120 / 140.
3. **Every turn after.** Keep the next Raticate on the Bench with its Energy
   so it can step in after a Knock Out. Night Stretcher brings Raticate back.
   Boss's Orders / Giovanni drag up a damaged or low-HP two-Prize Pokémon.
4. **Late game.** Persian ex or Kangaskhan ex finish what Raticate can't one-shot.

**Their outs.** Raticate has 90 HP, so expect to lose one every turn; that is
the trade. It's weak to Fighting (every Colorless Team Rocket's Pokémon is),
and the 25% self-Knock Out gives them a free Prize when it happens.
N's Zoroark is the worst matchup (43% in the full run).

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Draft: 4-4 Raticate, 2-2 Persian ex, 2 Kangaskhan ex, 2 Brave Bangle | 73.68% |  |
| No Persian ex (4 Kangaskhan ex) | 71.93% | worse |
| **+ Maximum Belt (−1 Poké Pad)** | **75.01%** | +1.34 ± 0.62 vs draft |
| 4 Brave Bangle (−2 Poké Pad) | 74.25% | +0.57 |
| Maximum Belt + 4 Brave Bangle | 74.66% | −0.36 ± 0.44 vs Belt |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Rattata | 99.6% | 1.31 |
| Team Rocket's Raticate | 88.0% | 2.87 |
| Team Rocket's Kangaskhan ex | 86.7% | 2.21 |
| Team Rocket's Meowth | 95.8% | 1.76 |
| Team Rocket's Persian ex | 63.7% | 3.55 |

First attack by turn 6 in 94.0% of games (average turn 2.84).

## PTCGL import

```
Pokémon: 14
4 Team Rocket's Rattata DRI 147
4 Team Rocket's Raticate DRI 148
2 Team Rocket's Kangaskhan ex ASC 162
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
1 Team Rocket's Giovanni ASC 204
3 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
2 Team Rocket's Factory ASC 203
2 Brave Bangle PBL 104
2 Air Balloon MEG 166
1 Poké Pad ASC 198
1 Maximum Belt TEF 154

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
