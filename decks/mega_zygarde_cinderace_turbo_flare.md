# Mega Zygarde ex / Cinderace Turbo Flare (submitted list)

A list submitted for study on 2026-10-11. It is in the field as submitted;
the import below uses this pool's printings:
- Boss's Orders RCL 189 → MEG 114
- Super Potion XY 128 → JTG 158
- Pokégear 3.0 UNB 233 → BLK 84
- Cook LOR-TG 25 → TWM 147

**68.23% against the 85-deck field at 1000 games per opponent** (median
68.6%, 80 winning matchups). That's already a top-tier result. The tuned
version,
**[mega_zygarde_cinderace_gaia_wave.md](mega_zygarde_cinderace_gaia_wave.md),
scores 81.63% (+13.77 ± 0.57 paired, better on all 85)**.

## Plan

**Cinderace MEG 28**'s Explosiveness opens it face down as the Active.
Turbo Flare (C) does 50 and attaches 3 Basic Energy from the deck to the
Bench, loading Mega Zygarde ex:
- **Gaia Wave** (FFF): 200 and 30 less damage next turn.
- **Nullifying Zero** (FFFFF): 150 to each opponent's Pokémon on heads.
- **Geobuster** (FFFF, via Core Memory): 350.

Mega Audino ex's Kaleidowaltz accelerates too. A wide Trainer toolbox
handles everything else: healing, hand disruption, late-game Supporters
and searches.

## What the simulator found

**Five engine fixes** (2026-10-11); together worth **+8.07 ± 1.21** for
this list at 200 games (60.90% → 68.97%):
- **Explosiveness** was compiled as a no-op setup rule. The four Cinderace,
  a Stage 2 with no Scorbunny or Raboot, could never be played, and the
  deck mulliganed on its 3 Basics alone. Cinderace now opens and stops a
  mulligan.
- **Turbo Flare** put all three Energy on the first Benched Pokémon, often
  Mega Audino ex; they now go to the Pokémon that needs them.
- **Mega Signal** searched for a card whose NAME contains "Mega Evolution"
  and found nothing; it searches the MEGA subtype now.
- **Fighting Gong** lost its "or a Basic Fighting Pokémon" half, and could
  take the Special Rocky Fighting Energy.
- **Core Memory** was never attached. Any Pokémon holding it could also
  have used Geobuster, since its named holder ("The Mega Zygarde ex this
  card is attached to") didn't match the holder check.

**The list runs out of Energy.** 9 Basic Fighting Energy is too few for
three search-and-attach effects and attacks costing 3-5. Each situational
card swapped for a Basic Fighting Energy measured positive, round after
round: Acerola's Mischief, Cook, Super Potion, Special Red Card, Xerosic's,
Watchtower, Pokégear and Roto-Stick. More Basics (Zygarde 3-4) measured
worse. Full table in the
[tuned list's notes](mega_zygarde_cinderace_gaia_wave.md).

**Matchups (1000 games):**
- **Worst:** N's Zoroark 26.7%, Mega Chandelure ex 38.1%, Spidops / Mewtwo
  48.4%, Ditto Hydreigon 48.6%, Decidueye ex 49.8%, Hydrapple / Seaking
  50.2%, Lurantis 50.2%.
- **Best:** Drapion 90.4%, Mew / Pikachu box 89.2%, Salazzle ex / Muk 88.0%,
  Alakazam 87.9%.

**One rules assumption.** The simulator lets Cinderace open even when the
hand has no Basic Pokémon. I haven't checked this against an official
ruling.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Cinderace | 64.8% | 1.00 |
| Mega Zygarde ex | 50.0% | 1.66 |
| Mega Audino ex | 26.4% | 1.72 |

First attack by turn 6 in 83.6% of games (average turn 2.43).

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
Mulligan 39.9% counting the 4 Cinderace as openers (3 Basics alone would
be 68.5%).

## PTCGL import

```
Pokémon: 7
2 Mega Zygarde ex POR 120
1 Mega Audino ex ASC 253
4 Cinderace MEG 28

Trainer: 41
3 Boss's Orders MEG 114
2 Iris's Fighting Spirit JTG 180
2 Acerola's Mischief MEG 183
1 Team Rocket's Watchtower DRI 180
4 Lillie's Determination MEG 184
1 Lively Stadium SSP 180
4 Fighting Gong MEG 168
2 Roto-Stick PRE 127
4 Jumbo Ice Cream CRI 109
1 Super Potion JTG 158
1 Hero's Cape TEF 152
1 Switch PFL 123
4 Pokégear 3.0 BLK 84
1 Team Rocket's Factory DRI 173
1 Mega Signal MEG 171
1 Premium Power Pro MEG 174
1 Core Memory POR 70
1 Special Red Card CRI 113
1 Xerosic's Machinations SFA 89
4 Team Rocket's Petrel DRI 226
1 Cook TWM 147

Energy: 12
9 Basic Fighting Energy
3 Rocky Fighting Energy POR 87

Total Cards: 60
```
