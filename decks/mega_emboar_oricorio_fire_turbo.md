# Mega Emboar ex / Oricorio ex Fire Turbo

Tuned 2026-10-11 from a submitted Mega Emboar ex list
([mega_emboar_oricorio_munkidori.md](mega_emboar_oricorio_munkidori.md)).
**68.22% against the 84-deck field at 1000 games per opponent, against 50.41%
for the list it came from (+17.81 ± 0.61 paired, better on all 84).**

**Lines:** Tepig → Pignite → Mega Emboar ex (main), Oricorio ex, Latias ex,
Fan Rotom, Dunsparce → Dudunsparce.

## Plan

**Mega Emboar ex** (Stage 2, 380 HP) hits for **320 with Crimson Blast**
(FFC; 60 to itself).

**Oricorio ex's Excited Turbo** attaches a Basic Fire Energy from your hand
to a Benched Fire Pokémon, as often as you like, while a Fire Mega
Evolution Pokémon ex is in play. A Benched Mega Emboar ex goes from zero to
Crimson Blast in one turn, and so does the next one after a Knock Out.

The support Pokémon:
- **Latias ex's Skyliner:** your Basics have no Retreat Cost, so the Active
  Basic retreats for free into Mega Emboar ex.
- **Fan Rotom:** searches Colorless Pokémon on turn 1 and attacks for 70
  with Jamming Tower in play.
- **Dudunsparce:** draws.

The deck is built around having Fire Energy in hand every turn. 21 Basic
Fire Energy feed Excited Turbo and Crimson Blast, and the 3 Mega Emboar ex
and 2 Rare Candy make sure there is something to feed.

## How to play

1. **Turn 1.** Buddy-Buddy Poffin for Tepig. Fan Rotom's Fan Call finds
   Dunsparce and Fan Rotom. Attach Fire to a Tepig.
2. **Turn 2.** Rare Candy Tepig → Mega Emboar ex, or Tepig → Pignite.
   With a Mega Emboar ex in play, Excited Turbo every Fire Energy in hand onto
   it. Retreat the Active Basic for free (Latias ex) and Crimson Blast for
   320.
3. **Every turn after.** Keep a second Tepig or Pignite going on the Bench.
   When the Active Emboar is Knocked Out, Excited Turbo loads the next one.
   Dawn and Hilda find the missing Evolution, and Hilda an Energy too.
4. **Their outs.** The 60 self-damage and 3-Prize Mega rule mean an Emboar
   that doesn't Knock Out is a liability. One Boss's Orders is enough for
   the late-game target.

**Matchups (1000 games):**
- **Worst:** Hydrapple / Seaking Festival Lead 24.4%. Then Mega Chandelure
  ex, Mew / Lonestar / Dragapult, Nidoking ex, Kyurem / Vanilluxe, Mega
  Zygarde ex / Cinderace and Water aggro, all 46-49%.
- **Best:** Mew baby box 97.7%, Mew / Pikachu box 97.0%, Wobbuffet /
  Orbeetle 94.9%, Toxic Slumber Vileplume ex 92.7%.

Median matchup 69.0%; 74 of 84 winning.

## How it was tuned

200 games against each of the 84 field decks, paired on the same seeds,
on the engine after the fixes in the submitted list's notes. Each round is
paired against the best list of the round before. Lists and results are in
`runs/2026-10-11/emboar_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Submitted list | 50.81% | |
| 1 | **11 Fire Energy (−Pokégear 3.0, −Night Stretcher)** | **54.27%** | **+3.46 ± 0.49** |
| 2 | 3 Rare Candy (−Hilda) | 54.19% | −0.08 ± 0.51 |
| 2 | 2 Pignite + 3 Rare Candy (−Hilda, −Lillie's) | 53.09% | −1.18 ± 0.54 |
| 2 | 2 Pignite (−Hilda) | 54.64% | +0.37 ± 0.53 |
| 2 | 3 Mega Emboar ex (−Fezandipiti ex) | 55.29% | +1.02 ± 0.55 |
| 2 | **13 Fire Energy (−Ultra Ball, −Hilda)** | **57.39%** | **+3.11 ± 0.47** |
| 3 | No Jamming Tower (+2 Fire) | 56.70% | −0.69 ± 0.63 |
| 3 | 3 Mega Emboar ex | 58.77% | +1.38 ± 0.48 |
| 3 | No Fezandipiti ex (+1 Fire) | 59.03% | +1.64 ± 0.54 |
| 3 | 15 Fire (−Ultra Ball, −Dawn) | 59.77% | +2.38 ± 0.55 |
| 3 | **15 Fire + 3 Mega Emboar ex (−Fezandipiti ex)** | **60.87%** | **+3.49 ± 0.52** |
| 4 | 17 Fire (−Hilda, −Lillie's) | 58.28% | −2.59 ± 0.63 |
| 4 | No Dudunsparce line (+Tepig, +2 Fire) | 58.99% | −1.88 ± 0.56 |
| 4 | 2 Pignite (−Hilda) | 60.09% | −0.78 ± 0.50 |
| 4 | 1 Latias ex (+Tepig) | 60.92% | +0.05 ± 0.57 |
| 4 | **1 Munkidori (−1 Darkness, +2 Fire)** | **63.47%** | **+2.60 ± 0.52** |
| 5 | 1 Fan Rotom (+Tepig) | 62.95% | −0.52 ± 0.58 |
| 5 | 4 Mega Emboar ex (−Hilda) | 63.16% | −0.31 ± 0.51 |
| 5 | 1 Latias ex (+Tepig) | 64.08% | +0.61 ± 0.51 |
| 5 | 2 Darkness Energy | 65.02% | +1.55 ± 0.51 |
| 5 | **No Munkidori, no Darkness Energy (+Tepig, +3 Fire)** | **68.02%** | **+4.55 ± 0.50** |
| 6 | 19 Fire (+Ultra Ball) | 65.93% | −2.08 ± 0.47 |
| 6 | 1 Latias ex (+Fire) | 67.64% | −0.37 ± 0.48 |
| 6 | 1 Dudunsparce (+Pignite) | 68.08% | +0.06 ± 0.46 |
| 6 | **21 Fire (−1 Boss's Orders) (this list)** | **69.25%** | **+1.23 ± 0.54** |
| 1000 games | Submitted / no Munkidori / this list | 50.41% / 67.19% / **68.22%** | **+17.81 ± 0.61**; +1.03 ± 0.22 vs no Munkidori |

**What made the difference:**

1. **Fire Energy in hand is the engine.** Excited Turbo attaches as many as
   you hold, so every Fire in hand is Crimson Blast damage. Going from 9 to
   21 Fire was worth about 12 points.
2. **Munkidori didn't pay for its slots.** Adrena-Brain moves Mega Emboar
   ex's 60 self-damage onto the opponent, but it needs Darkness Energy that
   does nothing else here. Cutting it for Fire gained +2.6, then +4.6. The
   simulator aims Adrena-Brain simply, always taking counters off the most
   damaged Pokémon and putting them on their Active. Treat this as a floor,
   but it is a big gap to make up.
3. **A third Mega Emboar ex** helps once the Energy is there to feed it.

Crimson Blast lands 2.4 times a game in this list against 0.95 in the
submitted one. Logged against six hard opponents (Raging Bolt, Dragapult,
Raticate, N's Zoroark, Tauros, Lurantis), it won 35 of 60 against 23.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Tepig | 96.1% | 1.65 |
| Pignite | 54.4% | 3.32 |
| Mega Emboar ex | 60.4% | 3.86 |
| Oricorio ex | 54.0% | 2.35 |
| Latias ex | 50.0% | 2.36 |
| Fan Rotom | 84.1% | 2.12 |
| Dunsparce | 86.0% | 1.93 |
| Dudunsparce | 57.8% | 3.36 |

First attack by turn 6 in 99.3% of games (average turn 2.71). The setup
baseline doesn't model Excited Turbo.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Enriching
Energy), 13 Basics (mulligan 16.3%). Latias ex's Eon Blade (Psychic) can
never be paid; Latias ex is there for Skyliner.

## PTCGL import

Oricorio ex MEP 24 (the promo in the submitted list) is listed as PFL 18,
the printing this pool carries; it is the same card.

```
Pokémon: 19
4 Tepig WHT 96
1 Pignite WHT 97
3 Mega Emboar ex ASC 273
2 Oricorio ex PFL 18
2 Latias ex SSP 239
2 Fan Rotom ASC 250
3 Dunsparce JTG 120
2 Dudunsparce PRE 80

Trainer: 19
3 Lillie's Determination MEG 169
2 Hilda WHT 171
1 Dawn PFL 129
1 Boss's Orders MEG 114
4 Buddy-Buddy Poffin MEG 167
4 Poké Pad POR 113
2 Rare Candy MEG 175
2 Jamming Tower ASC 261

Energy: 22
1 Enriching Energy SSP 191
21 Basic Fire Energy

Total Cards: 60
```
