# Ditto Transform: Tyranitar / Gengar ex / Hydreigon ex

**Not my list.** Supplied 2026-09-24. The only Basic is Ditto: its
Surprisingly Transform ("flip a coin; on heads search your deck for a
Pokemon and switch it with this Pokemon", keeping every attached card)
puts a Stage 2 into play on turn 2 with no Stage 1 and no Rare Candy.
Backtrack Badge re-flips the tails (a Tool for Colorless Pokemon; Ditto
is Colorless), so the flip lands about 3 times in 4. Crispin loads the
mixed Energy Hydreigon ex's Obsidian wants.

**66.01% (±0.43) under `greedy` against the 55-deck field (itself
included), 200 games each, winning 46 matchups** -- above every meta list
measured on this engine. Under the `lookahead` pilot, paired on the same
engine snapshot: **71.31% vs 65.22%, +6.09 ± 0.64** (it also chooses what
Ditto transforms into: mostly Hydreigon ex, sometimes Gengar ex or
Tyranitar).
Worst: Lurantis heal-punish 26.0, N's Zoroark toolbox 35.0, Heracross tea
37.5, Raging Bolt 39.5. Best: Centiskorch/Bastiodon mill 93.0.

1000-trial development baseline (`simulate_baseline.py`): a Stage 2 in
play by turn 6 in ~95% of games (Hydreigon ex 88.6%, avg turn 2.8); first
attack by turn 6 in 97.1% (avg turn 2.31).

## What the engine was missing (fixed, with regression tests)

- **Surprisingly Transform compiled to nothing** and, as a 0-damage attack
  with no rider value, was never used: the deck never attacked. New op
  `SWAP_FROM_DECK`; the pilot picks what hits hardest next turn, and the
  `lookahead` pilot plays each target out.
- **Backtrack Badge re-flipped damage coins only**, not an attack's effect
  coin -- the Transform flip is the reason it is in the deck.
- **Gengar ex's Fainting Spell** (misprinted "Knocket" in the card data)
  did not compile; it now Knocks Out the attacker on heads.
- The baseline sim did not model the Transform or Crispin.

## Construction notes

- **4 Basics: 60.1% of opening hands have none.** This deck mulligans in
  most games (1.1 mulligans a game measured), each one an extra card for
  the opponent. It still measures as the strongest list here.
- Four printings are outside this Standard pool: Air Balloon SSH 213,
  Pokegear 3.0 UNB 233 (Sun & Moon era), Boss's Orders PAL 265 and Energy
  Search SVI 172 (rotated regulation G). The import below uses legal
  printings of the same cards. Every other SET NUM checked out.
- 60 cards, no card over 4, one ACE SPEC (Secret Box); every attack is
  payable (`check_energy_support.py`).

## PTCGL import

```
Pokémon: 10
4 Ditto 30C 115
2 Tyranitar JTG 95
2 Gengar ex 30C 90
2 Hydreigon ex SSP 240

Trainer: 38
2 Boss's Orders MEG 114
1 Energy Search POR 72
4 Night Stretcher SSP 251
2 Air Balloon MEG 166
1 Xerosic's Machinations SFA 89
1 Special Red Card CRI 113
4 Buddy-Buddy Poffin TWM 223
4 Crispin PRE 171
1 Secret Box TWM 163
4 Backtrack Badge PBL 74
3 Team Rocket's Petrel DRI 226
4 Pokégear 3.0 BLK 84
3 Jumbo Ice Cream CRI 109
4 Lillie's Determination MEG 184

Energy: 12
1 Mist Energy TEF 161
3 Basic Metal Energy
3 Basic Psychic Energy
5 Basic Darkness Energy

Total Cards: 60
```
