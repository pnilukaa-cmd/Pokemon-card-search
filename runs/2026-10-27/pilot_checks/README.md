# Pilot checks, 2026-10-27

## `heal_saves_ko` (tried, removed)

**What it did.** The AI tries the draw Supporters before anything else, so
Cook, Fennel and AZ's Tranquility were never played while Lillie's
Determination was in hand. That held even with a Mega Kangaskhan ex one
Okidogi ex attack from giving up three Prizes. The knob played a heal
Supporter first when, tried on a copy of the game, it took the Active out
of the opponent's reach next turn: healed above the hit, or (AZ's) switched
to the Bench.

**The probe** did what it says. At 200 damage, inside Okidogi ex's reach,
each heal was played over Lillie's. At 150, out of reach, Lillie's was
still played.

**Measured** on tag `tk1` (engine 927c086), 200 games against each of the 98
field decks. Each Tundra Wall variant with the heal (round `m1_`) was
paired against itself without the knob:

| Variant | Measured |
|---|---|
| +2 Fennel | −0.48 ± 0.34 |
| +2 Cook | −0.42 ± 0.33 |
| +2 AZ's Tranquility | +0.23 ± 0.39 |

The draw it gave up was worth more than the Knock Out it put off, so the
knob was removed before the field part of the check ran.
