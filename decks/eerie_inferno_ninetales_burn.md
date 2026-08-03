# Eerie Inferno (Vulpix / Ninetales + Numel + Magmar / Magmortar)

Fifth of five decks built around the Special Condition stacking research in this repo (see
`combo_patterns.md` Pattern 5). Unlike the four Grass/Darkness decks above, this one pairs a
guaranteed condition-applicator with a card that mechanically *amplifies* one of the two
conditions applied, rather than just scaling off the count.

## Centerpieces

1. **Ninetales** (Twilight Masquerade) — `Eerie Glow` (2 Fire, 90 damage) inflicts Burned +
   Confused on the opponent's Active, no coin flip.

2. **Magmortar** (Journey Together) — `Magma Surge` (Ability): during Pokémon Checkup, put 3
   *more* damage counters on the opponent's Burned Pokémon, on top of the normal Burn tick.
   This isn't just thematically paired with Ninetales — it mechanically multiplies the exact
   condition Eerie Glow guarantees. `Searing Flame` (2 Fire + 1 Colorless, 90 damage) also has
   a coin-flip chance to inflict Burned, but that's a bonus, not the deck's reliable Burn
   source — Ninetales is doing that job alone.

3. **Numel** (Ascended Heroes, the `me2pt5-223` printing specifically — the other Numel
   printing in the pool has no Ability at all) — `Incandescent Body`: any attack that damages
   Numel while it's Active burns the attacker back. A bench-safe piece that punishes the
   opponent for attacking through it.

## Design notes

- Larry's Staraptor was researched and deliberately cut: its 3-stage evolution cost doesn't fit
  this deck's low curve, and its payoff triggers off *your own* Pokémon's conditions rather
  than the opponent's — backwards from what this deck is trying to do.
- Firebreather (search up to 7 Basic Fire Energy) keeps the mono-Fire base flowing without
  competing with the deck's other Item slots.
- Verified with `check_energy_support.py`: mono-Fire supply (11 Fire Energy) covers every
  attack cost with no shortfalls; no attack-gating Ability text found; every card name in the
  list matched `pokemon_standard_cards.json`.

## Pokémon TCG Live Import

```
Pokémon: 16
4 Vulpix TWM 26
4 Ninetales TWM 27
3 Magmar JTG 20
3 Magmortar JTG 21
2 Numel ASC 223

Trainer: 33
4 Ultra Ball
4 Buddy-Buddy Poffin
4 Boss's Orders
4 Cheren
3 Judge
3 Switch
3 Night Stretcher
3 Air Balloon
3 Rescue Board
2 Firebreather

Energy: 11
11 Fire Energy

Total Cards: 60
```
