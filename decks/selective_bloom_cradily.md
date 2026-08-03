# Selective Bloom (Antique Root Fossil / Lileep / Cradily)

Second of five decks built around the Special Condition stacking research in this repo (see
`combo_patterns.md` Pattern 5). Unlike the other four, this one is a **self-contained
single-Pokémon engine** — Cradily can inflict a Special Condition and cash it in for damage
without needing a second attacker to set it up.

## Centerpieces

1. **Cradily** (Stellar Crown) — `Selective Slime` (Ability, once/turn): flip a coin; if heads,
   choose Burned, Confused, or Poisoned and inflict it on the opponent's Active. `Miasma Wind`
   (1 Grass) then does 100 damage for each *distinct* Special Condition currently on the
   opponent's Active — the same narrow "counts distinct conditions" family as Team Rocket's
   Muk's Hazardous Venom (Pattern 5's 2-member `damage_scales_with_special_condition` list).

2. **Lileep** (Stellar Crown) — `Bind Down` (1 Grass, 50 damage): the opponent's Active can't
   retreat during their next turn. Not itself a Special Condition, so it doesn't feed Miasma
   Wind's multiplier, but it buys time for Selective Slime's coin flip to land more than once.

3. **Antique Root Fossil** (Stellar Crown) — played as a 60 HP Basic Colorless Pokémon; Lileep
   evolves *only* from this specific card, not from any generic Basic. Its own Ability taxes
   the opponent's Basic Pokémon attacks while Active.

## Real structural weakness (flagged honestly)

**Antique Root Fossil can't be tutored.** It's Trainer-supertype in the deck, so Ultra Ball
and Poké Ball — which search specifically for Pokémon-supertype cards — can't find it, and it
stays Trainer-supertype in the discard pile too, so Night Stretcher can't recur it either.
You're drawing into all 4 copies naturally or not at all, which is why the trainer line leans
this hard on raw draw (Cheren/Dawn/Judge) instead of tutoring. Dawn's search for a Basic +
Stage 1 + Stage 2 also only partially resolves here — there's no Pokémon-supertype Basic in
this deck for the "Basic" clause to find, only the Stage 1 (Lileep) and Stage 2 (Cradily).

## Design notes

- Rare Candy skips straight from the Fossil to Cradily when drawn together.
- Verified with `check_energy_support.py`: mono-Grass supply (10 Grass Energy) covers every
  attack cost with no shortfalls; no attack-gating Ability text found; every card name in the
  list matched `pokemon_standard_cards.json`.

## Pokémon TCG Live Import

```
Pokémon: 8
4 Lileep SCR 145
4 Cradily SCR 6

Trainer: 42
4 Antique Root Fossil SCR 130
4 Rare Candy
4 Ultra Ball
4 Poké Ball
3 Dawn
3 Cheren
3 Boss's Orders
3 Night Stretcher
3 Judge
3 Switch
4 Air Balloon
4 Rescue Board

Energy: 10
10 Grass Energy

Total Cards: 60
```
