# Mega Emboar ex / Oricorio ex / Munkidori (submitted list)

A list from a video, submitted for study on 2026-10-11. It is in the field
as submitted; the import below uses this pool's printings:
- Boss's Orders LOR-TG 24 → MEG 114
- Pokégear 3.0 UNB 233 → BLK 84
- Oricorio ex MEP 24 → PFL 18 (same card)

**50.41% against the 84-deck field at 1000 games per opponent** (median
47.4%, 35 winning matchups). The tuned version,
**[mega_emboar_oricorio_fire_turbo.md](mega_emboar_oricorio_fire_turbo.md),
scores 68.22% (+17.81 ± 0.61 paired, better on all 84)**.

## Plan

**Mega Emboar ex** hits for **320 with Crimson Blast** (FFC; 60 to itself).
**Oricorio ex's Excited Turbo** loads it from the hand while a Fire Mega is
in play. **Munkidori's Adrena-Brain** (needs a Darkness Energy) moves the
self-damage onto the opponent. **Latias ex** gives the Basics free retreat,
**Fan Rotom** searches on turn 1 and attacks with a Stadium in play, and
**Dudunsparce** draws.

## What the simulator found

**Three engine fixes** (2026-10-11):
- **Excited Turbo** worked with no Mega in play and attached to any Benched
  Pokémon, giving Latias ex Fire on turn 1. It also ran once a turn instead
  of "as often as you like". It now waits for a Fire Mega, feeds only Fire
  Pokémon, the neediest first, and repeats. **+6.86 ± 0.56** for this list.
  The same missing Mega condition left Seviper's, Ludicolo's and Linoone's
  Excited Abilities always on.
- **Ultra Ball** picked its two discards after the search. A Mega Emboar ex
  whose only Pignite the search had just taken looked unreachable and was
  thrown away. The discards are the cost now, chosen before the search.
- **Pokémon searches** took the first match in the deck: Hilda fetched a
  second Mega Emboar ex with one in hand and no Pignite down. Searches now
  take the piece that evolves something in play. On for the measured deck
  only, that was +4.15 for this list and positive on all 10 decks tried.

**The list is short of Fire Energy.** Nine Fire Energy and four Darkness
Energy (for Munkidori) can't keep Excited Turbo fed. Crimson Blast landed
0.95 times a game. Fan Rotom's 70 did more of the attacking than Emboar.
Each Fire Energy added measured positive, up to 21. Cutting Munkidori and
the Darkness Energy for Fire was worth +7.2 over two rounds, and the
Pokégear, Night Stretcher, Ultra Ball, Fezandipiti ex and one Boss's Orders
went the same way. Full table in the
[tuned list's notes](mega_emboar_oricorio_fire_turbo.md).

**Matchups (1000 games):**
- **Worst:** Hydrapple / Seaking Festival Lead 16.4%, Ditto Hydreigon 26.8%,
  Kyurem / Vanilluxe 30.0%, Nidoking ex 30.2%, Hydreigon / Relicanth 31.0%,
  Maushold mill 31.2%, Raticate rush 31.5%.
- **Best:** Mew baby box 87.8%, Mew / Pikachu box 85.3%, Drapion 82.9%,
  Wobbuffet / Orbeetle 79.0%.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Tepig | 88.8% | 1.92 |
| Pignite | 58.5% | 3.58 |
| Mega Emboar ex | 56.7% | 4.11 |
| Oricorio ex | 55.3% | 2.32 |
| Latias ex | 54.0% | 2.31 |
| Munkidori | 68.1% | 2.37 |
| Fan Rotom | 89.5% | 2.08 |
| Dunsparce | 94.4% | 1.62 |
| Dudunsparce | 73.7% | 3.17 |
| Fezandipiti ex | 27.2% | 2.47 |

First attack by turn 6 in 94.4% of games (average turn 2.90).

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Enriching
Energy), 15 Basics (mulligan 11.8%). Latias ex's and Munkidori's attacks
need Psychic Energy the deck doesn't run. Both are there for their
Abilities.

## PTCGL import

```
Pokémon: 20
3 Dunsparce JTG 120
1 Pignite WHT 97
2 Latias ex SSP 239
2 Fan Rotom ASC 250
2 Munkidori SFA 72
3 Tepig WHT 96
2 Dudunsparce PRE 80
1 Fezandipiti ex SFA 92
2 Mega Emboar ex ASC 273
2 Oricorio ex PFL 18

Trainer: 26
2 Ultra Ball ASC 264
2 Jamming Tower ASC 261
1 Night Stretcher MEG 173
3 Lillie's Determination MEG 169
2 Rare Candy MEG 175
2 Boss's Orders MEG 114
2 Dawn PFL 129
4 Buddy-Buddy Poffin MEG 167
3 Hilda WHT 171
4 Poké Pad POR 113
1 Pokégear 3.0 BLK 84

Energy: 14
1 Enriching Energy SSP 191
9 Basic Fire Energy
4 Basic Darkness Energy

Total Cards: 60
```
