# Trevenant / Uxie spread, Rapidash draw

**Not my list.** Supplied 2026-10-07. Import (legal reprints for Switch
and Crushing Hammer): `trevenant_rapidash_uxie.ptcgl.txt`.

**37.39% (±0.18) against the 65-deck field, 1000 games per opponent,
winning 12 of 64.** Worst: N's Zoroark 11, Mega Excadrill mill 13,
Maushold mill 16, Panic Poison 17, Alex's Mew mill 18, Krookodile 18.
Best: Mew Pikachu box 76, Dragapult/Dusknoir 73, Festival Lead 73.
Tauros 20, Ditto Transform 36.

## Plan
- **Spread:** Uxie's Painful Memories (P) puts 2 counters on every opposing Pokemon.
- **Finisher:** Trevenant's Overwhelming Pain (PP) does 60 + 10 per counter on their whole board. It averaged 188 over 36 hits in logged games.
- **Energy lock:** Trevenant's Cursed Roots stops Energy being attached from hand to their Active.
- **Speed:** Phantump's Spiteful Evolution evolves it from hand straight away, at the cost of 2 counters.
- **Draw:** Rapidash's Hurried Gait draws 1 a turn, and Dudunsparce draws 3.
- **Tech:**
  - Mewtwo ex hits every Pokemon ex for 50.
  - Lillie's Clefairy ex makes Dragons weak to Psychic.
  - Nighttime Mine taxes Tera attackers.
  - Patrat's Watchful Eye stops damage-counter movement.

## Why it loses
- **Too slow.** Trevenant is in play by turn 6 in only 56% of games (average turn 3.5); first attack averages turn 2.8.
- **Mill and hand-pressure decks beat it.** Rapidash, Dudunsparce and Lillie's burn through its own deck, so mill decks (Excadrill, Maushold, Alex's Mew) finish the job.
- **The spread needs time.** Each Uxie turn is 20 to everything and doesn't take a Prize by itself.

## Engine fixes this list exposed
- **Phantump's Spiteful Evolution never evolved;** it only put 2 counters on Phantump. Fixed.
- **Ex-only spread attacks hit every Pokemon.** Mewtwo ex's Photon Bullets, Vaporeon ex and Flygon ex hit non-ex Pokemon too. Fixed.

## Spread and multiplier study (2026-10-07)

Every card in the pool that spreads counters, multiplies them, or scales
with them was listed. The fits for a Psychic deck:
- **Spread:** Uxie (2 counters on each, P).
- **Multiplier:** N's Vanilluxe's Snow Coating doubles the counters on each opposing Pokemon, for CC. Spiritomb's Spiritual End needs 13 Hide 'n' Sneak Pokemon in the discard pile.
- **Payoffs:**
  - Trevenant, Azelf: +10 per counter on their whole board.
  - Shedinja: 20 per counter on their Active.
  - Mesprit: 160 if Uxie and Azelf are both Benched.

Paired against the field, greedy pilot, 200 games per opponent:

| Change | Result |
|---|---|
| +2 Azelf (for Patrat, Mewtwo ex) | +2.40 ± 0.85 |
| Vanilluxe line + 2 Rare Candy (for Ponyta/Rapidash, Patrat) | +1.82 ± 1.03 |
| Vanilluxe line + 2 Azelf | +2.86 ± 1.30 |
| Lake trio: +2 Azelf +2 Mesprit | -4.87 ± 0.94 |

Lookahead pilot (50 games): your list 47.4%, Vanilluxe + Azelf 49.4%
(+2.03 ± 1.60). Both gain ~10 points from sequencing alone. The greedy
pilot never used Snow Coating: with 4 counters on each target it values
Snow Coating at 120 against Trevenant's 180 now, and cannot see that
doubling first makes the next Trevenant 300+.

Imports: `trevenant_rapidash_uxie_azelf.ptcgl.txt`, `trevenant_rapidash_uxie_vanilluxe.ptcgl.txt`.
