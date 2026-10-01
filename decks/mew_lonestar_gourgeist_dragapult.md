# Lonestar's Mew ex / Gourgeist ex -- playbook

**Not my list.** Supplied 2026-09-30. 59.2% against the 62-deck field
(200 games per opponent, greedy pilot), winning 46 of 62. Import:
`mew_lonestar_gourgeist_dragapult.ptcgl.txt`.

## What the deck does
- **Damage:** Gourgeist ex's Ghostly Touch, 140 for two Psychic Energy plus a random discard from their hand. Mew ex copies it from the Bench.
- **Hand pressure:** Xerosic's Machinations (they discard down to 3), Banette's Cursed Words (they shuffle 3 cards from hand into the deck), Ghostly Touch's discard, and Unfair Stamp after a Knock Out.
- **Item lock:** Mew copies Budew's Itchy Pollen for **0 Energy**.
- **Setup:** Telepathic Psychic Energy benches 2 Basic Psychic Pokémon when attached to a Psychic Pokémon. Drakloak's Recon Directive picks the best of the top 2 cards every turn.

## Turn 1
- **Going first** (no attack, no Supporter, no evolving):
  1. Start Mew ex Active (160 HP, no Retreat Cost).
  2. Attach Telepathic Psychic Energy to Mew and bench 2 Pumpkaboo, or 1 Pumpkaboo and 1 Shuppet.
  3. Play Buddy-Buddy Poffin for Dreepy and Budew (both 70 HP or less).
  4. Use Poké Pad for whatever piece is still missing.
  5. Play Team Rocket's Watchtower if they show a Colorless Pokémon with an Ability.
- **Going second:** the same setup, plus a Supporter and an attack.
  1. Supporter: Xerosic's Machinations to cut their hand to 3. If your own hand is weak, play Hilda for Pumpkaboo plus an Energy instead.
  2. Attack: with Budew on the Bench, Mew uses Itchy Pollen. On their turn 2 they hold 3 cards and can't play Items.

## Turn 2
1. Evolve Pumpkaboo into Gourgeist ex, Dreepy into Drakloak, Shuppet into Banette (Hilda finds Evolutions).
2. Use Recon Directive every turn from now on.
3. Attack:
   - **Ghostly Touch** for 140 is the default.
   - **Cursed Words** (1 Energy) if they rebuilt their hand.
   - **Itchy Pollen** again if their next turn depends on Items.

## Mid and late game
- **Rotate attackers.** Mew has no Retreat Cost, and Latias ex's Skyliner removes it from all your Basics. Pivot freely, and keep Gourgeist ex on the Bench until it's needed.
- **Extra damage options:**
  - Lillie's Clefairy ex: +20 for each Benched Pokémon on both sides.
  - Latias ex: 200, then it can't attack the next turn.
  - Gourgeist ex's Horrifying Rondo: only grows if your own Benched Pokémon are damaged.
- **Comeback and closing tools:**
  - Unfair Stamp after you lose a Pokémon: they draw 2, you draw 5.
  - Special Red Card when they're down to 3 Prizes.
  - Boss's Orders to take the Prize that ends the game.
- **Energy:** Wondrous Patch moves Psychic Energy from the discard pile to a Benched Psychic Pokémon, so a Knocked Out attacker's Energy isn't lost.

## Matchups (simulator, greedy pilot)
- **Best:** Dragapult 60–69% (Lillie's Clefairy ex makes Dragons weak to Psychic), Tauros 58%, Slowking 55%.
- **Worst:**
  - Both Ditto/Hydreigon decks (13% and 26%): Darkness Weakness against a 330-HP attacker that hits for 200.
  - N's Zoroark 22%.
  - Maushold 33%.

## Caveats
- **Measured with a weaker pilot.** The 59% was measured with the simulator's simpler pilot. It rarely has Mew borrow attacks and mostly used Mew's own pivot attack, so a player who uses Itchy Pollen and Cursed Words deliberately should do better.
- **Mulligans:** 19% of opening hands have no Basic (12 Basics).
- **Opening odds:** 78% of opening hands have a setup card (Poffin, Poké Pad or Telepathic).
- **Speed:** the development test gets Gourgeist ex down by turn 6 in 47% of games (average turn 3.4).

## Upgrades tested (2026-10-01)

Paired against the 62-deck field, same dice as the list as supplied:

| Change | 200 games | 1000 games |
|---|---|---|
| **Jacinthe for 1 Xerosic + Hero's Cape for Unfair Stamp** | +2.13 ± 0.63 | **+0.99 ± 0.30** |
| Jacinthe for 1 Xerosic | +1.77 ± 0.52 | +0.24 ± 0.28 (noise) |
| 2 Jacinthe for 2 Xerosic | +1.48 ± 0.63 | |
| Hero's Cape for Unfair Stamp | +0.35 ± 0.61 | |
| Clefairy POR 30 for 1 Boss's Orders | -1.77 ± 0.67 | |
| Clefairy POR 30 for Special Red Card | -2.52 ± 0.59 | |

Clefairy's numbers say nothing about the card: the simulator's pilot used
Follow Me **0 times** in 20 logged games (Mew always preferred Ghostly
Touch), so it measured a dead 70 HP body. Follow Me's real job -- pulling up
a high-Retreat Pokemon and stranding it under Itchy Pollen -- is a human
line the greedy pilot does not see.

Upgraded import: `mew_lonestar_gourgeist_upgraded.ptcgl.txt`.
