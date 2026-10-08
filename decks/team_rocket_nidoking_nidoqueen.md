# Team Rocket's Nidoking ex / Nidoqueen

<!-- field-results -->
> ### Field results — 2026-10-08
> **71.5% mean · 73.7% median · 68 of 76 winning matchups · rank 4 of 77**
>
> Best `mew_baby_box` 99% · worst `ns_zoroark_night_joker_toolbox` 31%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Nidoran♀ → Nidorina → Nidoqueen (attacker), Nidoran♂ → Nidorino → Nidoking ex (enabler, backup).

## Plan

**Team Rocket's Nidoqueen** (Stage 2, 170 HP) hits **180 for one Darkness
Energy**: Love Impact is 60 + 120 while any Pokémon with "Nidoking" in its name
is on your **Bench**. **Nidoking ex** (330 HP) sits on the Bench as the enabler.
It is also the backup attacker: Tainted Horn (DDC) does 100 and Poisons for
**8 counters per Checkup**, and Kingly Impact (DDDC) does 240.

**Nidorina's Dark Awakening** (D) evolves up to 2 of your Darkness Pokémon
straight from the deck. **Rare Candy** skips the middle stage. Every Pokémon
is Team Rocket's, so Ariana always draws to 8, and Team Rocket's Energy pays
DD with one card. Hero's Cape takes Nidoqueen to 270 HP.

## How to play

1. **Turn 1.** Poffin (both Nidorans have 70 HP) or Proton: bench two
   Nidoran♀ and a Nidoran♂, attach Darkness.
2. **Turn 2.** Rare Candy can't be used on your first turn or on a Basic
   played this turn. Your Turn-1 Basics are eligible now. Rare Candy
   Nidoran♂ → Nidoking ex on the Bench and Nidoran♀ → Nidoqueen in the Active
   Spot, then attach and Love Impact for 180. With only one Candy, evolve
   Nidoran♀ → Nidorina from hand instead.
3. **Turn 3 (if Nidorina).** Dark Awakening evolves two Pokémon from the deck
   (not ones that already evolved this turn): a Nidorina → Nidoqueen and a
   Nidorino → Nidoking ex.
4. **From then on.** Nidoqueen swings 180 every turn for one Energy. When it
   falls, the next Queen needs one attachment. If they Knock Out the Benched
   Nidoking ex, Love Impact drops to 60. Keep the second Nidoking ex or Night
   Stretcher ready, or promote Nidoking ex itself (Kingly Impact 240).

**Their outs.** A gust onto the Benched Nidoking ex: 330 HP is hard to take
in one hit, but it is the deck's weak point. Fighting Weakness on everything.
Nidoqueen is Stage 2, so a slow start is the usual loss.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Draft: 4-2-3 Queen, 4-1-2 King, Sneasel, Janine's | 71.13% |  |
| v2: 4-2-3 / 4-2-3, 2 Poké Pad, no Janine's or Sneasel | 71.81% | +0.68 ± 0.60 |
| v2 + Hero's Cape | 72.81% | +1.01 ± 0.51 vs v2 |
| v2 + 2 Brave Bangle | 71.51% | level |
| v2, Janine's for Lillie's | 68.74% | worse |
| v2, Queen-heavy 4-3-4 / 4-1-2 | 72.10% | +0.29 |
| **Queen-heavy + Hero's Cape** | **73.34%** | +0.52 ± 0.65 vs Cape |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Nidoran♀ | 99.5% | 1.33 |
| Team Rocket's Nidorina | 86.5% | 2.84 |
| Team Rocket's Nidoqueen | 78.1% | 3.60 |
| Team Rocket's Nidoran♂ | 99.2% | 1.38 |
| Team Rocket's Nidorino | 51.7% | 3.32 |
| Team Rocket's Nidoking ex | 42.5% | 3.86 |

First attack by turn 6 in 93.5% of games (average turn 3.00).

## PTCGL import

```
Pokémon: 18
4 Team Rocket's Nidoran♀ DRI 114
3 Team Rocket's Nidorina DRI 115
4 Team Rocket's Nidoqueen DRI 116
4 Team Rocket's Nidoran♂ DRI 117
1 Team Rocket's Nidorino DRI 118
2 Team Rocket's Nidoking ex DRI 119

Trainer: 30
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Poké Pad ASC 198
1 Hero's Cape TEF 152
2 Team Rocket's Proton ASC 208
4 Team Rocket's Ariana ASC 202
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Team Rocket's Transceiver ASC 209
2 Air Balloon MEG 166

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
