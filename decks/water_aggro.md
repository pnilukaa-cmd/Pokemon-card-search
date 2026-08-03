# Water Aggro

Built around three centerpieces from `pokemon_standard_cards_deckbuilding.json` (Standard, regulation marks H/I/J).

## Centerpieces (ranked)

1. **Chien-Pao** (Surging Sparks, Basic, single-prize) — `Icicle Loop` deals 120 damage for 3 energy (Water/Water/Colorless), the best damage-per-energy ratio in the deck, and it's single-prize so trading it never gives up a 2-prize swing. Retreat cost 1.

2. **Barraskewda** (Destined Rivals, Stage 1 from Arrokuda, single-prize) — `Sharp Fin` hits for 40 damage off a single Water energy, providing turn-2 pressure. `Dive` (60 for 2) covers the mid-game. Arrokuda and Barraskewda are both retreat 1 and single-prize.

3. **Palafin ex** (via Palafin's Zero to Hero, Twilight Masquerade) — Evolve Finizen into Palafin, attack, then retreat it (cost 1) to trigger `Zero to Hero`, swapping in Palafin ex with all damage/energy intact. Palafin ex then swings `Giga Impact` for 250 damage off a single Water energy. Costs 2 prizes on KO but requires no extra turn or card to get into play.

## Why they work together

Chien-Pao and Barraskewda apply cheap, single-prize pressure from turn 1-2. Once Palafin has attacked once, retreating it converts a spent attacker into a one-shot 250-damage finisher for free.

## Decklist (60 cards)

### Pokémon (15)

| Qty | Card | Set |
|---|---|---|
| 3 | Chien-Pao | Surging Sparks |
| 2 | Arrokuda | Destined Rivals |
| 2 | Barraskewda | Destined Rivals |
| 3 | Finizen | Twilight Masquerade |
| 3 | Palafin | Twilight Masquerade |
| 2 | Palafin ex | Twilight Masquerade |

### Trainers (33)

| Qty | Card | Type | Effect |
|---|---|---|---|
| 4 | Boss's Orders | Supporter | Gust opponent's benched Pokémon into Active |
| 4 | Crispin | Supporter | Search 2 basic energy, attach 1 |
| 4 | Lacey | Supporter | Shuffle hand, draw 4 (8 if opp has ≤3 prizes) |
| 4 | Ultra Ball | Item | Discard 2, search any Pokémon |
| 4 | Buddy-Buddy Poffin | Item | Bench 2 Basics with ≤70 HP (fetches Finizen/Arrokuda) |
| 3 | Switch | Item | Free retreat (extra Zero to Hero triggers) |
| 3 | Night Stretcher | Item | Recur a KO'd Pokémon or energy |
| 2 | Great Haul Net | Item | Recur up to 3 Water Pokémon + 3 Water Energy from discard |
| 2 | Rescue Board | Tool | -1 retreat cost, free retreat at ≤30 HP |
| 2 | Air Balloon | Tool | -2 retreat cost |
| 1 | Prime Catcher | ACE SPEC | Switch both active Pokémon |

### Energy (12)

| Qty | Card |
|---|---|
| 12 | Basic Water Energy |

Mono-Water energy works throughout since every attack in the deck costs Water + Colorless, and Colorless is payable by any basic energy.

## Pokémon TCG Live Import

```
Pokémon: 15
3 Chien-Pao SSP 56
2 Arrokuda
2 Barraskewda
3 Finizen
3 Palafin
2 Palafin ex

Trainer: 33
4 Boss's Orders
4 Crispin
4 Lacey
4 Ultra Ball
4 Buddy-Buddy Poffin
3 Switch
3 Night Stretcher
2 Great Haul Net
2 Rescue Board
2 Air Balloon
1 Prime Catcher

Energy: 12
12 Basic Water Energy

Total Cards: 60
```

Note on `check_energy_support.py`: the pool also contains a second, unrelated `Chien-Pao`
printing (`me3-54`, Phantasmal Flames) with Darkness-costed attacks. The checker matches by
card name only and pools every printing sharing that name together (a documented limitation of
the tool, not of this deck), so it flags those Darkness attacks as unpayable here. This deck
specifically runs the Surging Sparks printing (`sv8-56`), whose only attack is `Icicle Loop`
(Water/Water/Colorless) — fully covered by the 12 Water Energy above.
