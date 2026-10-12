# Mega Zygarde ex / Cinderace Gaia Wave

Tuned 2026-10-11 from a submitted Mega Zygarde ex / Cinderace list
([mega_zygarde_cinderace_turbo_flare.md](mega_zygarde_cinderace_turbo_flare.md)),
updated 2026-10-12 with a Cornerstone Mask Ogerpon ex.

**83.30% against the 86-deck field at 1000 games per opponent.** It wins
85 of 86 matchups (median 86.0%), the highest field result in the repo.
- Against the 2026-10-11 list (no Ogerpon, one more Energy) on the same
  seeds: 81.48%, so **+1.83 ± 0.41 paired**, better on 57 and worse on 27.
- Against the submitted list: 68.23%.

**Lines:** Cinderace (opens face down), Mega Zygarde ex, Mega Audino ex,
Cornerstone Mask Ogerpon ex.

## Plan

**Cinderace MEG 28** is a Stage 2, but its **Explosiveness** puts it face
down as your opening Active straight from the hand. Its **Turbo Flare** (C)
does 50 and attaches 3 Basic Energy from your deck to your Benched Pokémon.
On turn 1 or 2 that loads a Benched Mega Zygarde ex.

**Mega Zygarde ex** (Basic, 310 HP) has three attacks:
- **Gaia Wave** (FFF): 200, and it takes 30 less damage next turn.
- **Nullifying Zero** (FFFFF): 150 to each of the opponent's Pokémon on
  heads.
- **Geobuster** (FFFF, from **Core Memory**): 350, discarding all its
  Energy.

**Mega Audino ex**'s Kaleidowaltz (2 Basic Energy per heads, 3 coins) is a
second accelerator, and its Ear Force punishes a loaded Active.

**Cornerstone Mask Ogerpon ex** (Basic, 210 HP, 2 Prizes, Retreat 1) is the
second attacker:
- **Demolish** (FCC): 140, ignoring Weakness, Resistance and effects on the
  Defending Pokémon.
- **Cornerstone Stance:** no damage from attackers that have an Ability.

It is a 2-Prize attacker the Ability decks can't touch: N's Zoroark ex,
Spidops, the Mega Chandelure ex list.

The tuning turned almost every tech card into Basic Fighting Energy.
Turbo Flare, Kaleidowaltz and Fighting Gong all pull Basic Energy from the
deck, and Gaia Wave and Geobuster spend a lot of it. With 21 in the deck
every search hits.

## How to play

1. **Setup.** Put Cinderace face down as the Active whenever you have one.
   It also saves you from a mulligan with no Basic in hand. Bench Mega
   Zygarde ex.
2. **Turns 1-2.** Turbo Flare: 50 damage and 3 Energy onto the Benched
   Zygarde. Fighting Gong finds Zygarde or Ogerpon (both Basic Fighting), or
   a Basic Fighting Energy. Mega Signal finds whichever Mega you are missing.
   Attach Core Memory to a Zygarde.
3. **Then.** Switch or retreat into Mega Zygarde ex and Gaia Wave for 200
   (230 with Premium Power Pro). Geobuster the 300+ HP targets. Jumbo Ice
   Cream heals 80 off an Active with 3+ Energy. Rocky Fighting Energy stops
   attack effects on it.
4. **Ogerpon.** Put it in front of an attacker with an Ability, which then
   can't damage it, and to take 2-Prize Knock Outs without giving up 3.
5. **Boss's Orders** (3) and **Team Rocket's Petrel** (4, any Trainer) take
   the Prizes that end the game.

**Matchups (1000 games):**
- **Worst:**
  - the 2026-10-11 list 49.3%
  - Lurantis 54.0%
  - N's Zoroark 56.9%
  - the submitted list 61.3%
  - Mega Chandelure ex 63.4%
  - Mega Emboar ex Fire Turbo 64.7%
  - Hydrapple / Seaking 65.9%
- **Best:** Mew baby box 99.0%, Mew / Pikachu box 98.3%, Mew / Hypno 97.0%,
  Mew / Bastiodon 96.6%.
- **Ogerpon's biggest gains:** N's Zoroark +14.3, Raging Bolt +13.5, Mega
  Chandelure ex +12.6, Spidops / Mewtwo +11.5.
- **Its biggest losses:** Nidoking / Nidoqueen −4.9, Lurantis −4.5.

## How it was tuned

200 games against each field deck (84-86), paired on the same seeds. Each
round is paired against the best list of the round before. Rounds 0-5 ran
on the engine after the fixes in the submitted list's notes. Their lists
and results are in `runs/2026-10-11/zygarde_screens/`; round 6 is in
`runs/2026-10-12/big_basic_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Submitted list | 68.97% | |
| 1 | 3 Zygarde + 2 Audino (−Cook, −Super Potion, −Special Red Card) | 67.26% | −1.71 ± 0.56 |
| 1 | 4 Mega Zygarde ex (−Cook, −Super Potion) | 67.58% | −1.39 ± 0.52 |
| 1 | 3 Mega Zygarde ex (−Cook) | 67.86% | −1.11 ± 0.48 |
| 1 | 2 Mega Audino ex (−Special Red Card) | 69.12% | +0.15 ± 0.47 |
| 1 | −2 Acerola's Mischief, +Zygarde, +1 Energy | 70.98% | +2.01 ± 0.48 |
| 1 | **+2 Fighting Energy (−Xerosic's, −Watchtower)** | **71.43%** | **+2.46 ± 0.53** |
| 2 | 3 Basic Fighting for the 3 Rocky | 70.70% | −0.73 ± 0.58 |
| 2 | −Special Red Card, +1 Energy | 73.55% | +2.12 ± 0.44 |
| 2 | −Cook, −Super Potion, +2 Energy | 74.54% | +3.11 ± 0.54 |
| 2 | −2 Acerola's Mischief, +2 Energy | 75.52% | +4.09 ± 0.46 |
| 2 | **−2 Pokégear 3.0, +2 Energy** | **75.83%** | **+4.40 ± 0.47** |
| 3 | −Cook, −Super Potion, +2 Energy | 77.10% | +1.27 ± 0.43 |
| 3 | −2 more Pokégear, +2 Energy | 78.19% | +2.48 ± 0.45 |
| 3 | −2 Acerola's Mischief, +2 Energy | 78.66% | +2.83 ± 0.44 |
| 3 | −2 Acerola's, −Special Red Card, +3 Energy | 79.08% | +3.26 ± 0.46 |
| 3 | **−2 Acerola's, −Cook, −Super Potion, +4 Energy** | **79.14%** | **+3.31 ± 0.47** |
| 4 | −Lively Stadium, +1 Energy | 79.59% | +0.62 ± 0.45 |
| 4 | −Special Red Card, +1 Energy | 79.63% | +0.67 ± 0.43 |
| 4 | −2 Pokégear, +2 Energy | 80.72% | +1.79 ± 0.44 |
| 4 | −2 Roto-Stick, +2 Energy | 80.78% | +1.83 ± 0.44 |
| 4 | **−Special Red Card, −2 Pokégear, +3 Energy** | **80.91%** | **+1.92 ± 0.44** |
| 5 | −1 Petrel, +1 Energy | 81.34% | +0.42 ± 0.45 |
| 5 | −2 Roto-Stick, −Lively Stadium, +3 Energy | 81.84% | +0.92 ± 0.41 |
| 5 | −2 Roto-Stick, +Zygarde, +1 Energy | 82.53% | +1.62 ± 0.39 |
| 5 | **−2 Roto-Stick, +2 Energy (2026-10-11 list)** | **82.83%** | **+1.92 ± 0.40** |
| 6 | 86-deck field, 2026-10-12 engine: 2026-10-11 list | 82.00% | |
| 6 | Mega Hawlucha ex added (−1 Energy) | 81.90% | −0.10 ± 0.47 |
| 6 | 3rd Mega Zygarde ex added (−1 Energy) | 82.36% | +0.36 ± 0.41 |
| 6 | Cornerstone Mask Ogerpon ex added (−1 Energy) | 82.67% | +0.67 ± 0.52 |
| 6 | **Mega Kangaskhan ex added (−1 Energy)** | **82.69%** | **+0.69 ± 0.45** |
| 1000 games | 2026-10-11 list | 81.48% | |
| 1000 games | Mega Kangaskhan ex added | 82.51% | +1.03 ± 0.28 |
| 1000 games | Kangaskhan and Ogerpon added (−2 Energy) | 83.50% | +2.02 ± 0.44 |
| 1000 games | **Cornerstone Mask Ogerpon ex added (this list)** | **83.30%** | **+1.83 ± 0.41** |

Adding both is +0.19 ± 0.26 over Ogerpon alone, a tie, and it loses the
mirror against the 2026-10-11 list (44.2%, against 49.3% for this list).
So this list adds only Ogerpon. Mega Kangaskhan ex (Run Errand draws 2 while
it's Active) is the next card to add.

**What made the difference:**

1. **Energy in the deck.** Turbo Flare, Kaleidowaltz and Fighting Gong
   search Basic Energy, and Gaia Wave (3), Nullifying Zero (5) and Geobuster
   (4, then discarded) burn through it. 9 Basic Fighting Energy ran dry.
   Every round, trading a situational card for one measured positive, up
   to 22.
2. **The situational cards cost more than they gave.** Acerola's Mischief
   only works at 2 Prizes or fewer, and Special Red Card at 3 or fewer.
   Cook, Super Potion, Xerosic's, Watchtower, Pokégear and Roto-Stick each
   measured worse than an Energy. Petrel, Lillie's, Iris, Boss's Orders,
   Fighting Gong and Jumbo Ice Cream stay.
3. **A different Basic, not more of the same.** A 3rd or 4th Zygarde lowers
   the mulligan rate but adds nothing new (+0.36 at best). Ogerpon covers
   what Zygarde can't: attackers with Abilities, and a 2-Prize target in
   place of a 3-Prize one.
4. **Mega Audino ex stays.** Swapped out for each of 18 other big Basics,
   the list got worse every time (best: Cornerstone Mask Ogerpon ex
   −0.07). Its second accelerator is worth more than a second hitter; see
   `runs/2026-10-12/big_basic_screens/`.

Logged against six hard opponents (Raging Bolt, Dragapult, Raticate, N's
Zoroark, Tauros, Lurantis), the 2026-10-11 list won 40 of 60, against 36
for the submitted list. It used Gaia Wave 2.4 times a game, Turbo Flare 1.5,
Nullifying Zero 0.7 and Geobuster 0.4. With Kangaskhan and Ogerpon both
added it won 44 of 60; Ogerpon used Demolish 0.6 times a game.

**One rules assumption.** The simulator lets Cinderace open, and stop a
mulligan, even when the hand has no Basic Pokémon, as Explosiveness reads.
I haven't checked this against an official ruling. If a Basic is required
too, the deck's real mulligan rate is higher (4 Basics: 60.1% of hands).

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Cinderace | 61.4% | 1.00 |
| Mega Zygarde ex | 46.0% | 1.67 |
| Mega Audino ex | 26.2% | 2.04 |
| Cornerstone Mask Ogerpon ex | 27.6% | 1.88 |

First attack by turn 6 in 98.1% of games (average turn 2.39). The baseline
doesn't model Turbo Flare's attachment.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
Mulligan 34.6% on 4 Basics + 4 Cinderace openers. Every attack is payable
with Fighting Energy. That mulligan rate is the deck's real weakness, and
the win rates include it.

## PTCGL import

```
Pokémon: 8
4 Cinderace MEG 28
2 Mega Zygarde ex POR 120
1 Mega Audino ex ASC 253
1 Cornerstone Mask Ogerpon ex TWM 112

Trainer: 28
4 Lillie's Determination MEG 184
4 Team Rocket's Petrel DRI 226
2 Iris's Fighting Spirit JTG 180
3 Boss's Orders MEG 114
4 Fighting Gong MEG 168
4 Jumbo Ice Cream CRI 109
1 Mega Signal MEG 171
1 Switch PFL 123
1 Premium Power Pro MEG 174
1 Core Memory POR 70
1 Hero's Cape TEF 152
1 Team Rocket's Factory DRI 173
1 Lively Stadium SSP 180

Energy: 24
21 Basic Fighting Energy
3 Rocky Fighting Energy POR 87

Total Cards: 60
```
