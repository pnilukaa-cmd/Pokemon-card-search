# Tauros / Risky Ruins — Raging Charge

A user list, reviewed 2026-09-20. Four Tauros CRI 69 and four Paldean
Tauros PFL 48 both scale off how many "Tauros" you have in play; Risky
Ruins damages every Basic as it is benched, which is what arms Paldean
Tauros's Raging Charge; Area Zero Underdepths lifts the Bench cap to 8 off
Cornerstone Mask Ogerpon ex's Tera; Backtrack Badge re-flips Target
Together's coins.

## The list could not be measured until three engine bugs were fixed

Each was found by MEASURING an attack against a hand-computed truth, not
by reading whether it compiled. All three are committed.

1. **`Target Together` dealt zero damage, always.** Its printed damage
   field is empty — the number lives entirely in "flip a coin for each of
   your Pokémon that has 'Tauros' in its name … 50 damage for each heads",
   and no rule read that shape. The deck's headline attacker was a 130 HP
   body the AI never once selected. The fix reaches **8 attacks in the
   pool**, which were being scored at the all-heads figure (double the
   true mean) or at base: Brambleghast, Exeggutor, Heliolisk, Scrafty,
   Larry's Dudunsparce ex, Volcanion, Maushold and Tauros.
2. **`Raging Charge` was a flat 40 at every board state.** It scales per
   damaged Tauros; `_clause_count` had no rule for a quoted NAME fragment
   plus a damage filter.
3. **`Risky Ruins` was played and then did nothing.** Its trigger is a
   Pokémon being put onto the Bench, which the Ability IR has no trigger
   for, so it compiled to a passive `PLACE_COUNTERS` no consumer reads.

Re-measuring the three field decks that run Risky Ruins found **no
significant change** (`meta_dragapult_pure` +1.34, `blaziken` +0.22,
`dusknoir` +0.38, every interval spanning zero). It is a one-of tech
Stadium for them, not an engine.

## As submitted: 45.5%, rank 33 of 46

95% CI [40.9, 50.2], 15/45 winning matchups. Reproduced to the decimal on
a second independent run of the same seeds.

The spread is unusually wide — 85.5% into `static_venom_drapion`, 19.0%
into `meta_raging_bolt`. It beats the bottom of the field and is crushed
by the top, with no tech either way.

## The problem is Energy starvation, and it is measurable

The list attaches Energy on only **0.61 of its turns**. Nearly four turns
in ten there is nothing in hand to attach, in a deck whose costs are `F`,
`FF`, `FCC` and `CC`.

Three of the nine Energy are **Darkness**, which pays no `F` cost anywhere
in the deck — its only real job is giving Crispin a second type to fetch.
Swapping those three for Fighting, changing nothing else, is worth
**+3.37** on held-out seeds.

`Tatsugiri` cannot attack at all: Surf costs Fire+Water and the deck runs
neither. It is there for Attract Customers, but it is a 70 HP body that
Boss's Orders can strand in the Active Spot.

## What was tested

Every variant paired against the field: same CRN seed per pairing, only
the list changing. Five seed sets in total.

| change | held-out delta | 95% CI |
|---|---|---|
| −3 Darkness → +3 Fighting | +3.37 | [+2.11, +4.62] |
| −1 Sacred Ash → +1 Fighting | +2.76 | [+1.20, +4.31] |
| −1 Tatsugiri → +1 Fighting | +4.02 | [+2.52, +5.52] |
| −3 Area Zero, +2 Fighting, +1 Poké Pad | +6.47 | [+4.89, +8.05] |
| −1 Tatsugiri, −3 Darkness, +4 Fighting | +7.39 | [+5.86, +8.92] |

Selection mean +5.56 → held-out +5.12, an **8% shrink**. That is not luck:
these are paired over 45 opponents (n=45 per estimate), not the single
mirror matchup the pilot programme used, so there was far less noise to
select on.

### Walking out the Energy curve

Each count paired against the one below it, holding the mulligan rate
constant at 22.24%:

| Fighting Energy | mean | vs the submitted list |
|---|---|---|
| 9 (as submitted) | 45.5% | — |
| 12 | 57.6% | +11.13 |
| 13 | 60.0% | +13.49 |
| 15 | 61.4% | +14.98 |
| **16** | **63.2%** | **+16.77** |
| 17 | 63.6% | +17.19 |
| 18 | 64.3% | +17.83 |

**A trap worth recording.** Single steps 13→14 and 14→15 both read as
noise, and the first conclusion drawn was "13 is the last justified step."
That was wrong: `e15 − e13` measured **+1.99 [+0.61, +3.36]**, real. The
individual steps were underpowered, not absent. Always test the cumulative
jump before declaring a plateau.

The genuine plateau is at 16: `e18 − e16` is **+1.07 [−0.33, +2.46]**,
noise, and getting past 16 means cutting Area Zero Underdepths.

## Recommended list — 63.2%, rank 6 of 46

−10 cards, all replaced by Basic Fighting Energy: `Tatsugiri`,
3 `Darkness Energy`, `Sacred Ash`, `Special Red Card`, `Lucky Helmet`,
`Hassel`, `Premium Power Pro`, `Lana's Aid`.

```text
Pokémon: 11
1 Shaymin DRI 10
4 Paldean Tauros PFL 48
2 Cornerstone Mask Ogerpon ex TWM 112
4 Tauros CRI 69
Trainer: 33
3 Risky Ruins MEG 127
2 Crispin PRE 105
3 Poké Pad ASC 198
3 Area Zero Underdepths SCR 131
4 Lillie's Determination MEG 119
3 Glass Trumpet SCR 135
2 Backtrack Badge PBL 74
2 Air Balloon BLK 79
2 Boss's Orders MEG 114
3 Fighting Gong MEG 116
3 Night Stretcher SFA 61
2 Team Rocket's Petrel ASC 207
1 Precious Trolley SSP 185
Energy: 16
16 Basic Fighting Energy
```

Attachments per turn 0.61 → **0.84**. Attacks per game 4.18 → **5.09**.
Games two turns shorter. The 1000-trial baseline agrees from a completely
separate tool: **first attack landed by turn 6 goes from 68.3% to 93.3%**.

## Two things this measurement does NOT establish

**Target Together's value is understated here.** The card says "choose 1
of your opponent's Pokémon" — its real power is sniping the Bench, and the
engine computes damage against the Active only. Whatever this list is
worth, it is worth at least this much.

**16 Basic Energy in a 60-card deck is very high for real play.** The
starvation is mechanically real and shows up in two independent tools, so
the direction is not in doubt. But the simulator's pilot attaches on
every legal turn and never holds a card back, which flatters Energy
density; a human sequences better and the true optimum is probably lower.
**12–13 captures most of the gain** (+11.13 to +13.49 of the +16.77) in a
list that looks like a deck someone would actually build. Treat 16 as the
engine's answer, not a deckbuilding instruction.

The parts that are mechanically explicable and safe either way: the three
Darkness Energy pay no `F` cost, and Tatsugiri cannot attack.
