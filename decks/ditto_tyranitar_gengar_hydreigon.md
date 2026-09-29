# Ditto Transform: Tyranitar / Gengar ex / Hydreigon ex

<!-- field-results -->
> ### Field results — 2026-09-29
> **65.7% mean · 68.5% median · 46 of 56 winning matchups · rank 7 of 57**
>
> Best `team_rockets_wobbuffet_orbeetle_damage_launder` 94% · worst `lurantis_heal_punish` 32%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-09-29** and was measured against a different field or engine.
<!-- field-results -->




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

## Tested 2026-09-28: a second Basic to cut the mulligans

1000 games against each of the 54 other field decks, paired (same dice),
engine after the Fan Call / Backtrack Badge / Impromptu Carrier fixes:

| Variant | Basics | Mulligan % | Win % | vs original |
|---|---|---|---|---|
| original | 4 | 60.1 | 65.86 | -- |
| +1 Farfetch'd TWM 132, -1 Jumbo Ice Cream | 5 | 52.5 | 66.93 | **+1.07 ± 0.50** |
| +1 Farfetch'd, +1 Fan Rotom, -1 Jumbo, -1 Energy Search | 6 | 45.9 | 66.88 | +1.02 ± 0.52 |
| +1 Fan Rotom ASC 171, -1 Jumbo Ice Cream | 5 | 52.5 | 65.92 | -0.07 ± 0.38 |
| +2 Fan Rotom, -2 Jumbo Ice Cream | 6 | 45.9 | 66.16 | +0.17 ± 0.51 |

Fan Rotom (Fan Call fetches 3 Ditto on turn 1) looks like the natural
fix and measures as nothing: as the opener it has no live attack (Assault
Landing needs a Stadium, and this deck plays none) and costs a retreat
before Ditto can Transform. Before the pilot fixes it measured -2.9,
because the greedy pilot fed it the Energy and the Backtrack Badge that
Ditto needed. Farfetch'd is the better fifth Basic: 70 HP (Poffin finds
it), Mach Cut strips Special Energy, and Impromptu Carrier thins a Tool.
About two standard errors -- a likely small gain, not a proven one.

1000-trial baseline of the Farfetch'd list: Ditto in play 98.3% (avg turn
1.19), first attack by turn 6 in 98.1% (avg 2.28), Hydreigon ex by turn 6
72.7% (original: 88.7%). The baseline sim cannot retreat, so a Farfetch'd
opener never lets Ditto attack there; the versus sim retreats, and that is
where the +1.07 comes from.

```
Pokémon: 11
4 Ditto 30C 115
2 Tyranitar JTG 95
2 Gengar ex 30C 90
2 Hydreigon ex SSP 240
1 Farfetch'd TWM 132

Trainer: 37
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
2 Jumbo Ice Cream CRI 109
4 Lillie's Determination MEG 184

Energy: 12
1 Mist Energy TEF 161
3 Basic Metal Energy
3 Basic Psychic Energy
5 Basic Darkness Energy

Total Cards: 60
```
