# Water Aggro

<!-- field-results -->
> ### Field results — 2026-09-13
> **51.0% mean · 47.5% median · 20 of 43 winning matchups · rank 25 of 44**
>
> Best `feraligatr_munkidori_damage_transfer` 92% · worst `panic_poison_paralysis` 22%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->












> **Decklist corrected.** Every line in this list originally carried a bare card name with no `SET NUM`. The simulator resolves a bare name to the *first* printing in the pool, which for `Palafin` is **TEF 49** — a printing with no `Zero to Hero` Ability. `Palafin ex`'s rule is "put this Pokémon into play **only** with the effect of Palafin's Zero to Hero", so the deck's 250-damage finisher had no legal route into play in any game this deck ever played. The line is now pinned to `Finizen TWM 59 / Palafin TWM 60 / Palafin ex TWM 61` and every card carries an exact set number.


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
2 Arrokuda DRI 62
2 Barraskewda DRI 63
3 Finizen TWM 59
3 Palafin TWM 60
2 Palafin ex TWM 61

Trainer: 33
4 Boss's Orders MEG 114
4 Crispin SCR 133
4 Lacey SCR 139
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
3 Switch MEG 130
3 Night Stretcher MEG 173
2 Great Haul Net CRI 78
2 Rescue Board TEF 159
2 Air Balloon ASC 181
1 Prime Catcher TEF 157

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
