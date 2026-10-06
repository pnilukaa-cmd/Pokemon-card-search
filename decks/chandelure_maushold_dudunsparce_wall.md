# Mega Chandelure ex / Maushold / Dudunsparce

**Not my list.** Supplied 2026-10-06. Import: `chandelure_maushold_dudunsparce_wall.ptcgl.txt`.

**39.44% (±0.18) against the 63-deck field, 1000 games per opponent,
winning 15 of 63.** Worst: Tauros 2, Team Rocket's Koffing 8, Cradily
decks 12-14, Maushold mill 14. Best: Mew Pikachu box 86, Scovillain 77.

## Plan
- **Main win condition: mill.** Gnaw Together, from 4 Maushold, flips a coin for each Maushold in play and discards 2 cards from the top of their deck per heads.
- **Walls:**
  - Mist Energy: blocks effects of attacks on the Pokémon it's attached to.
  - Neutralization Zone: no damage from ex/V attackers to Pokémon without a Rule Box.
  - Shaymin: protects Benched Pokémon without a Rule Box.
  - Battle Cage: no damage counters placed on the Bench.
- **Mega Chandelure ex: the late attacker.** Binding Flame raises their Retreat Cost by 1, and Gravity Gemstone raises both Actives' by 1 more. Phantom Maze does 130 + 50 per Colorless in their Retreat Cost.
- **Card flow:** Dudunsparce draws 3; Sacred Ash and Lana's Aid recover Pokémon.

## In 20 logged games
- **Gnaw Together:** 47 uses. It's the deck.
- **Run Away Draw:** 28 uses.
- **Phantom Maze:** only 5 uses, so Chandelure rarely got online.
- **Spreading Light:** never used. The pilot evolves Lampent into Chandelure instead of using it to bench more Lampent.
- **Game endings:** 5 of the 20 games ended in a deck-out.

## Engine fixes this list exposed
- **Spreading Light and Familial March benched nothing.** The Bench search refused every non-Basic, even when the card names its Stage 1. Fixing it moved three field decks: chandelure_centiskorch +2.4, mega_chandelure_ex +1.8, study_maushold_gnaw_latias +1.3.
- **Ethan's Sudowoodo's Try to Imitate skipped its coin flip,** so it always copied the opponent's attack.

## Upgrades tested (2026-10-06)

Paired against the 63-deck field, 200 games per opponent (a 1000-game
confirmation was stopped before it finished):

| Change | Result |
|---|---|
| +2 Fan Rotom, +1 Maushold 30C (-Sudowoodo, -Elgyem, -Prism Tower) | **+7.32 ± 0.93** |
| +3 Backtrack Badge (-2 Gravity Gemstone, -Tool Scrapper) | +3.16 ± 0.68 |
| +3 Crushing Hammer (-Prism Tower, -Redeemable Ticket, -Air Balloon) | +1.79 ± 0.68 |
| +2 Budew (-Sudowoodo, -Elgyem) | -0.15 ± 0.66 |
| Rotom + Maushold + Badge | +9.40 ± 0.90 |
| **All three (Rotom + Maushold, Badge, Hammer)** | **+12.95 ± 1.04 (39.7 -> 52.6%)** |

All three come from the 68.6% maushold_gnaw_together_mill list, which
beat this deck 86-14. Import: `chandelure_maushold_dudunsparce_wall_upgraded.ptcgl.txt`
(Basic Fighting Energy becomes a third Psychic once Sudowoodo is cut).

## Delay cards tested on the upgraded list (2026-10-06, 200 games, paired)

Each in place of Sacred Ash + Battle Cage (Scream Tail ex for a Dunsparce):

| Addition | Result |
|---|---|
| **2 Enhanced Hammer TWM 148** | **+4.75 ± 0.68** (now in the upgraded import) |
| 2 Xerosic's Machinations | -0.32 ± 0.74 |
| 2 Eri | -0.55 ± 0.65 |
| 1 Scream Tail ex | -0.56 ± 0.65 |
| 2 Energy Swatter | -1.88 ± 0.52 |

Enhanced Hammer always hits (no coin), and most of the field leans on
Special Energy.

## Other milling Pokemon (2026-10-06, 200 games, paired vs the upgraded list)

Every Pokemon in the pool that discards from the top of the opponent's
deck was listed; the ones payable with this deck's Psychic/Colorless
Energy were tested.

| Change | Result |
|---|---|
| +2 Durant ex (for Lana's Aid + 1 Night Stretcher) | -3.38 ± 0.70 |
| +1 Drilbur +1 Excadrill SSP (same cuts) | -2.52 ± 0.65 |
| +2 Team Rocket's Larvitar (same cuts) | -3.48 ± 0.69 |
| Chandelure line -> 2 Durant ex, 2 Drilbur, 2 Excadrill | +1.73 ± 0.77 |
| **Chandelure line -> 2 Drilbur, 2 Excadrill, 2 TR Larvitar** | **+3.66 ± 0.85 (57.5 -> 61.2%)** |

The pure-mill version is `maushold_pure_mill_variant.ptcgl.txt`. One-card
millers only pay off in the Chandelure slots, which attacked 5 times in 20
games; taking recursion slots for them loses.
