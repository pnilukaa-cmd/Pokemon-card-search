# Team Rocket's Orbeetle / Morpeko ex (damage laundering)

<!-- field-results -->
> ### Field results — 2026-10-08
> **59.5% mean · 58.8% median · 55 of 76 winning matchups · rank 19 of 77**
>
> Best `mew_baby_box` 95% · worst `ns_zoroark_night_joker_toolbox` 25%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Blipbug → Dottler → Orbeetle, Kangaskhan ex (tank), Morpeko ex (payoff).

## Plan

**Rocket Brain** (Orbeetle): as often as you like, move 1 damage
counter from a Team Rocket's Pokémon to *another of your Pokémon*. Aim it
at **Morpeko ex**, whose Hangry Blaster (DD) does **40 + 40 per counter on
itself**: 5 counters is 240. The counters come from Kangaskhan ex soaking a
hit (Orbeetle heals it in the process) and from **Venture Bomb**: heads puts
2 counters on them, tails puts 2 on your Active, so Morpeko gets +80 either
way. **Janine's Secret Art** attaches 2 Darkness and Poisons your Active,
which gives Morpeko ex a counter every Checkup.

The simulator now pilots this on purpose: load the attacker up to the
Knock Out, never below a third of its HP, else heal the Active.

## How to play

1. **Turn 1.** Poffin: Blipbug ×2. Kangaskhan ex or Morpeko ex Active.
2. **Turn 2.** Rare Candy → Orbeetle. Kangaskhan ex takes the first hit.
3. **Turn 3+.** Switch Morpeko ex in, move Kangaskhan's counters onto it,
   and Hangry Blaster for the Knock Out.

**Their outs.** Knock Out Orbeetle (130 HP, Stage 2) on the Bench. Morpeko ex
gives 2 Prizes and is fragile once loaded.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Draft, old Rocket Brain (moved counters at random) | 54.81% |  |
| **Draft, aimed Rocket Brain** | **60.79%** | +5.98 ± 0.64, now the engine default |
| + Exeggutor line (Double-Edge self-damage as fuel) | 56.72% | worse |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Blipbug | 97.8% | 1.35 |
| Team Rocket's Dottler | 50.1% | 3.30 |
| Team Rocket's Orbeetle | 44.6% | 3.90 |
| Morpeko ex | 85.6% | 1.90 |
| Team Rocket's Kangaskhan ex | 76.5% | 2.16 |

First attack by turn 6 in 88.6% of games (average turn 2.59).

## PTCGL import

```
Pokémon: 13
4 Team Rocket's Blipbug DRI 15
1 Team Rocket's Dottler DRI 88
3 Team Rocket's Orbeetle DRI 198
3 Morpeko ex PBL 102
2 Team Rocket's Kangaskhan ex ASC 162

Trainer: 35
3 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Team Rocket's Venture Bomb DRI 179
3 Janine's Secret Art SFA 59
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Team Rocket's Ariana ASC 202
2 Team Rocket's Proton ASC 208
2 Night Stretcher MEG 173
2 Switch MEG 130
1 Team Rocket's Transceiver ASC 209
2 Air Balloon MEG 166
1 Hero's Cape TEF 152
1 Poké Pad ASC 198

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Darkness Energy

Total Cards: 60
```
