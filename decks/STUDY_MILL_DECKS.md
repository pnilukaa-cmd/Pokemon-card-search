# Five mill decks, measured

All five against the same 45-deck field, 1000 games per opponent
(45,000 games each). 95% CI on each mean is +/-0.46.

| deck | field mean | would rank | mills/game | win/45 |
|------|-----------:|-----------:|-----------:|-------:|
| `study_mega_excadrill_drill_mill` | **56.51** | ~13 | 7.28 | 29/45 |
| `study_hydreigon_zweilous_mill`   | 43.08 | ~37 | 5.59 | 10/45 |
| `study_maushold_gnaw_latias`      | 36.50 | ~40 | 4.29 |  9/45 |
| `study_flygon_sandy_flapping_mill`| 23.24 | ~43 | 2.20 |  2/45 |
| `study_centiskorch_bastiodon_mill`| 14.84 | ~44 | 5.10 |  2/45 |

## Mill is not a win condition in this field

The best of the five discards **7.28 cards a game** over ~21 turns. Decking
a 60-card opponent needs roughly 53. Nothing here is within a factor of
five of its stated plan, and the ranking tracks DAMAGE, not mill rate --
Centiskorch mills more than Maushold and finishes 21 points lower.

The engine is not the reason. Gnaw Together was verified over 2000 trials
at exactly its printed rate: 4 Maushold in play gives 4.04 cards per use,
3 gives 2.95, 1 gives 1.01. The decks simply never assemble. Maushold
averages ~1.6 Maushold in play at the moment it attacks.

## What separates the one that works

`Mega Excadrill ex` wins because its mill is stapled to an attack worth
making anyway, and because Relicanth's Memory Dive gives it a curve:

| attack | cost | effect |
|--------|------|--------|
| Burrow (borrowed via Memory Dive) | 1 Colorless | discard 1 |
| Undermine | MM | 90 damage + discard 2 |
| Maximum Drilling | MMM + 2 extra | 330 damage |

A one-Energy play on turn one that still advances the mill, scaling into
90-plus-mill, then a 330-damage finisher, all on a 340 HP body. Observed
usage per game: Undermine 2.70, Burrow 1.43, Maximum Drilling 0.86.

Relicanth is a combo piece, not an attacker -- Memory Dive is verified to
grant `Burrow` and `Mud-Slap` only while Relicanth is benched. Its own
Razor Fin is uncastable (no Fighting Energy) and that does not matter.

Hydreigon ex has the same shape -- 200 damage plus discard 3 on a 330 HP
Stage 2 -- but fires only 1.14 times a game off a 7-card Energy base.

## Construction faults found

**`study_centiskorch_bastiodon_mill`** -- 8 real Basics, **34.6% mulligan**.
The 3 Antique Armor Fossil are Items and do not stop a mulligan; the list
reads as 11 Basics / 22%. No Psychic Energy at all, so the whole
Dreepy/Drakloak line is uncastable, and Bastiodon's Hammer In needs 2
Metal against 1 in the deck. Controlled Burn does **zero damage**: the
deck spends every turn removing two cards while threatening nothing, and
hands over six Prizes. Across 200 games it loses 185 in 17 turns with
Bastiodon in play 71% of the time.

**`study_hydreigon_zweilous_mill`** -- 7 Energy total. N's Zekrom's
Rampaging Thunder is uncastable, and Hydreigon ex's Obsidian needs 1
Psychic and 1 Metal, both satisfied only by the single Legacy Energy.

## Can a devolve loop re-trigger Flygon's Sandy Flapping?

No. `Strange Timepiece MEG 128` is the only card in Standard that devolves
your OWN Pokemon and it only targets **Psychic** Pokemon; Flygon is
Fighting. Every other devolve effect in the pool targets the opponent.

Even with matching types the arithmetic fails: Strange Timepiece says the
Pokemon can't evolve that turn, so the loop is one extra trigger every two
turns, for one Item each time -- +1 card milled per turn against a ~53
card requirement. `Scoop Up Cyclone` physically works but picks up the
whole stack, so it costs an ACE SPEC, a Rare Candy and two turns for 2
cards.

Sandy Flapping already self-loops: it fires on evolution AND again when
Flygon is Knocked Out in the Active Spot.
