# One-Energy attacks for Mew ex, 2026-10-27

The question: which attacks costing a single Energy are the strongest for
Mew ex to borrow with Memory Helix ("this Pokémon can use the attacks of
any of your Benched Pokémon"), especially from Pokémon that are hard to
get onto the board.

`copy_attack_scan.py` (repo root) scores every attack in the pool with
exactly one Energy in its cost, 1163 of them, as Mew ex would use it:
- Mew ex Active, one Energy of the attack's type on it (Colorless: Psychic).
- The donor and two others on the Bench.
- Against a field deck's Active with 3 Energy and 6 cards in hand, its own
  list as the cards we can't see.
- Damage is the mean of 40 seeds, so coin flips read as their expected
  value. "+rider" is the engine's value for the rest of the attack.

One board each, engine as of this commit:
- `vs_dragapult.*`: `meta_dragapult_pure`, Dragapult ex Active.
- `vs_raging_bolt.*`: `meta_raging_bolt`, Raging Bolt ex Active.

**Found on the way** (both fixed, with tests that fail on 0ecb7af):
- "N less damage for each X" multiplied instead of subtracting (Tinkaton's
  Windup Swing read 720 against a 3-Energy Active; it's 60). Six attacks,
  no field deck.
- Coalossal's Tar Cannon ignored "if you don't have 10 or more Basic
  Fighting Energy in your discard pile, this attack does nothing". No field
  deck.
