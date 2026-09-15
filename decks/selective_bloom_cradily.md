# Selective Bloom (Antique Root Fossil / Lileep / Cradily)

<!-- field-results -->
> ### Field results — 2026-09-15
> **51.9% mean · 49.0% median · 21 of 43 winning matchups · rank 22 of 44**
>
> Best `feraligatr_munkidori_damage_transfer` 86% · worst `meta_mega_excadrill` 15%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->














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
4 Rare Candy MEG 125
4 Ultra Ball MEG 131
4 Poké Ball POR 80
3 Dawn PFL 118
3 Cheren ASC 258
3 Boss's Orders MEG 114
3 Night Stretcher MEG 173
3 Judge POR 76
3 Switch MEG 130
4 Air Balloon MEG 166
4 Rescue Board TEF 159

Energy: 10
10 Basic Grass Energy

Total Cards: 60
```
