# Toxic Slumber (Erika's Oddish / Gloom / Vileplume ex)

Third of five decks built around the Special Condition stacking research in this repo (see
`combo_patterns.md` Pattern 5). Where Deck 1 (Panic Poison) leans on the persistent half of the
condition split for a delayed cash-in, this deck leans on the **action-denial** half for
immediate value: a guaranteed same-turn Asleep + Poisoned stack on a single big swing.

## Centerpieces

1. **Erika's Vileplume ex** (Ascended Heroes) — `Bloom Powder` (2 Grass + 1 Colorless) does 160
   damage and inflicts Asleep + Poisoned on the opponent's Active, no coin flip anywhere in the
   chain. Asleep is action-denial (blocks attack and retreat, coin-flip wake each Checkup);
   Poisoned is the persistent chip riding along after it wakes up. `Lovely Fragrance` (Ability,
   once/turn: heal 30 from each of your Pokémon) offsets the self-damage below.

2. **Erika's Gloom** (Ascended Heroes) — `Poison Spray` (1 Grass + 1 Colorless, 50 damage)
   independently inflicts Poisoned, giving the deck a second, cheaper applicator before
   Vileplume ex is online.

3. **Erika's Oddish** (Ascended Heroes) — `Reckless Charge` (1 Grass, 30 damage, 10 self-damage)
   is the early attacker; its self-damage is exactly what Lovely Fragrance later heals back.

## Design notes

- Unlike Deck 2 (Selective Bloom), the full Basic → Stage 1 → Stage 2 line all exist as real
  Pokémon-supertype cards here, so Dawn and Buddy-Buddy Poffin both function at full value —
  Buddy-Buddy Poffin can find Erika's Oddish directly (60 HP, under the 70 HP cap).
- Verified with `check_energy_support.py`: mono-Grass supply (12 Grass Energy) covers every
  attack cost with no shortfalls; no attack-gating Ability text found; every card name in the
  list matched `pokemon_standard_cards.json`.

## Pokémon TCG Live Import

```
Pokémon: 11
4 Erika's Oddish ASC 1
4 Erika's Gloom ASC 2
3 Erika's Vileplume ex ASC 3

Trainer: 37
4 Buddy-Buddy Poffin
4 Rare Candy
4 Ultra Ball
3 Dawn
3 Cheren
3 Boss's Orders
2 Judge
3 Night Stretcher
3 Switch
4 Air Balloon
4 Rescue Board

Energy: 12
12 Grass Energy

Total Cards: 60
```
