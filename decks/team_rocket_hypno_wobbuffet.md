# Team Rocket's Hypno / Wobbuffet / Mewtwo ex

<!-- field-results -->
> ### Field results — 2026-10-08
> **56.3% mean · 55.5% median · 50 of 76 winning matchups · rank 29 of 77**
>
> Best `mew_baby_box` 97% · worst `ditto_transform_hydreigon` 16%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 in the Team Rocket's study
([TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).
**Lines:** Drowzee → Hypno, Wobbuffet, Mewtwo ex, Mimikyu, Chingling.

## Plan

**Hypno's Bench Manipulation** (PPP): the *opponent* flips a coin for
each of their Benched Pokémon, and it does **80 per tails**, ignoring Weakness
and Resistance. That averages 40 per Benched Pokémon: 200 into a full Bench,
nothing into an empty one. **Mewtwo ex** (280 HP) attacks only with 4+ Team
Rocket's Pokémon in play. Erasure Ball does 160, +60 per Energy discarded from
your Bench (up to 2), for 280. **Wobbuffet's Rocket Mirror** moves *all* the
counters from one Benched Team Rocket's Pokémon onto their Active: Mewtwo ex
tanks a hit, retreats, and Wobbuffet throws it back.

## How to play

1. **Turn 1.** Poffin: Drowzee ×2, Mimikyu, Chingling. Drowzee's
   Hypnotic Ray (P) does 10 and puts them to Sleep.
2. **Turn 2.** Hypno; Team Rocket's Energy pays PP of PPP. Count their Bench
   first: 4-5 Benched is 160-200 on average.
3. **Against small Benches.** Mewtwo ex (4 Team Rocket's in play is easy here)
   or Wobbuffet's Rocket Mirror.

**Their outs.** Keep their Bench small. Coin variance. Darkness Weakness on
the whole line.

## How it was tuned

200 games against each of the 67 field decks, paired on the same seeds
(screens in `runs/2026-10-08/team_rocket_screens/`).

| Version | Win rate | Paired vs previous best |
|---|---|---|
| Hypno + Exeggutor + Mewtwo ex | 56.99% | → hypno_exeggutor |
| **Hypno-heavy with Wobbuffet** | **58.42%** | this list |
| Exeggutor-heavy | 55.76% | worse |

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Team Rocket's Drowzee | 97.2% | 1.72 |
| Team Rocket's Hypno | 84.2% | 3.20 |
| Team Rocket's Mewtwo ex | 65.2% | 2.03 |
| Team Rocket's Wobbuffet | 85.1% | 2.06 |
| Team Rocket's Mimikyu | 92.8% | 1.66 |
| Team Rocket's Chingling | 71.8% | 1.80 |

First attack by turn 6 in 91.1% of games (average turn 2.94).

## PTCGL import

```
Pokémon: 15
4 Team Rocket's Drowzee DRI 79
4 Team Rocket's Hypno DRI 80
2 Team Rocket's Mewtwo ex ASC 281
2 Team Rocket's Wobbuffet DRI 82
2 Team Rocket's Mimikyu ASC 238
1 Team Rocket's Chingling DRI 85

Trainer: 32
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
3 Poké Pad ASC 198

Energy: 13
4 Team Rocket's Energy ASC 217
9 Basic Psychic Energy

Total Cards: 60
```
