# Mega Kangaskhan ex / Tyrantrum — flip-until-tails

Built from the four cards asked for: `Team Rocket's Diglett`,
`Mega Kangaskhan ex`, `Tyrantrum`, `Houndstone`. All four share the
"flip a coin until you get tails" mechanic, and three of them mill.

## The coin-flip maths, first, because it governs everything

Heads count is geometric: `P(H = k) = (1/2)^(k+1)`.

| | |
| --- | --- |
| **E[H]** | **1.00 — on every card in the family** |
| **median H** | **0** |
| sd | 1.41 |
| P(H=0) / ≥1 / ≥2 / ≥3 | 50% / 50% / 25% / 12.5% |

Each individual flip pays the printed number **half** the time, the next a
**quarter**, the next an **eighth** — summing to exactly one. The long
streaks that make the card feel good contribute almost nothing to the
average. **Flipping more coins does not raise your mean, only your
variance.**

The important consequence for deckbuilding: an attack worded *"does N
damage for each heads"* has **no floor and whiffs to zero 50% of the
time**, while *"does N **more** damage for each heads"* keeps its printed
base. Every card in this deck is deliberately the second kind or a
non-damage rider.

## Why the mill is not the win condition

Say it plainly rather than building toward it: after setup the opponent
has ~47 cards and draws 1 per turn. One flip-miller removes E[1] more.

**Time to deck them out: ~23 turns. Time to lose on Prizes: ~12.**

`Relentless Burrowing` and `Wreak Havoc` are chip and information, not a
clock. The deck wins on Prizes.

## What each card actually does

| Card | | |
| --- | --- | --- |
| **`Mega Kangaskhan ex` MEG 104** | Basic, **300 HP**, `C``C``C` Rapid-Fire Combo **200+50/heads** (E = 250) | **This is the deck.** Colorless cost takes any Energy, and `Run Errand` draws 2 every turn it is Active |
| **`Tyrantrum` POR 45** | Stage 2, 180 HP, `F``C` Wreak Havoc 160 + mill | `Tyrannically Gutsy`: **+150 HP with any Special Energy attached → 330 HP** |
| **`Houndstone` MEG 145** | Stage 1, 140 HP, `P` Horrifying Bite 30 + shuffle random cards from their hand | Pairs with `Judge`: shrink their hand first, then take from what is left |
| **`Team Rocket's Diglett` ASC 100** | Basic, 60 HP, `F` Relentless Burrowing | 0 damage. Mill only. In at 2 because it was asked for — it is the weakest card here |

## The card that makes it work, and the one that nearly broke it

**`Rocky Fighting Energy` POR 87 is a three-way fit on Tyrantrum**:
it pays the `F`, it is a **Special** Energy so it switches on the +150 HP,
and it *prevents all effects of attacks* on the Fighting Pokémon holding
it. A 330 HP attacker immune to Special Conditions, gusts and retreat
locks, hitting for 160.

**But it says "the Fighting Pokémon this card is attached to"** — and
`Mega Kangaskhan ex` is **Colorless**. The deck's main attacker had no
protection at all, and the gauntlet said so precisely: the worst matchups
were all status and effect decks (Panic Poison 26.5%, T.R. Persian 27.0%,
AAA Crobat 31.0%, Arbok Laser 33.0%).

**`Mist Energy` TEF 161 is the same effect with no type restriction** —
Colorless, so it pays Rapid-Fire Combo outright, and still Special, so it
still turns on Tyrantrum's HP. Four copies in over the plain Fighting
Energy:

| | mean | median | winning |
| --- | --- | --- | --- |
| Basic Fighting Energy | 46.1% | 43.5% | 12/31 |
| **4 Mist Energy** | **54.1%** | **52.0%** | **16/31** |
| *same swap, independent seed* | 46.4% → **52.9%** | 43.5% → **53.0%** | 12 → **18** |

**+8.0% and +6.5% on two independent seeds, all three metrics both times.**
Paired comparison (common random numbers), 200 games per matchup.

## The cost nobody can design around

`Tyrantrum` does not start from a Basic Pokémon. Its line is
**`Antique Jaw Fossil` (an Item played as a 60 HP Basic) → `Tyrunt`
(Stage 1) → `Tyrantrum` (Stage 2)** — three steps.

**`Rare Candy` cannot bridge it.** Rare Candy needs a Stage 2 that evolves
from the Basic it targets; Tyrantrum evolves from Tyrunt, not from the
Fossil. Checked against the card text, not assumed.

`Fossil Quarry` PBL 76 searches two Antique Items straight onto the Bench
and is what makes the line playable at all — but note it is **symmetric**,
so it helps a Fossil opponent too.

Measured, 1200 openings with Prizes set aside:

| | T1 | T2 | T3 | T4 | T5 | T6 |
| --- | --- | --- | --- | --- | --- | --- |
| Mega Kangaskhan ex | 51.9% | 59.7% | 66.2% | 70.9% | 74.2% | 78.2% |
| Antique Jaw Fossil | 39.8% | 76.2% | 85.2% | 90.2% | 93.0% | 95.2% |
| Tyrunt | 0% | 17.5% | 43.3% | 55.8% | 64.4% | 71.2% |
| **Tyrantrum** | 0% | 0% | **6.2%** | 19.2% | 28.7% | **36.1%** |
| Houndstone | 0% | 11.9% | 25.2% | 35.5% | 46.2% | 54.1% |

**Tyrantrum arrives on turn 4.6 and shows up in a third of games.** Treat
it as a late-game wall you sometimes get, not a plan. Kangaskhan is out by
turn 2 in 60% of games and is what actually plays the match.

## Decklist

```
Pokémon: 19
4 Mega Kangaskhan ex MEG 104
3 Antique Jaw Fossil POR 68
3 Tyrunt POR 44
3 Greavard SCR 70
2 Tyrantrum POR 45
2 Houndstone MEG 145
2 Team Rocket's Diglett ASC 100

Trainer: 27
4 Ultra Ball MEG 131
4 Night Stretcher MEG 173
3 Poké Pad ASC 198
3 Fossil Quarry PBL 76
3 Lillie's Determination ASC 192
2 Judge POR 76
2 Boss's Orders ASC 183
2 Switch MEG 130
2 Air Balloon ASC 181
2 Eri PRE 136

Energy: 14
4 Rocky Fighting Energy POR 87
4 Mist Energy TEF 161
3 Basic Fighting Energy
2 Telepathic Psychic Energy POR 88
1 Enriching Energy SSP 191

Total Cards: 60
```

- **`Poké Pad` cannot fetch Mega Kangaskhan ex** — it searches a Pokémon
  *without a Rule Box*. `Ultra Ball` is the only tutor here that reaches
  the deck's best card, which is why it is at 4.
- **`Switch` and `Air Balloon` are not optional.** Kangaskhan and
  Tyrantrum both retreat for 3, and the Fossil **cannot retreat at all**.
- **`Enriching Energy` SSP 191** is the ACE SPEC: Colorless, and draws 4
  when attached. It goes on Kangaskhan.

## Numbers

60 cards, no card over 4, one ACE SPEC. Mulligan **19.1%** (12 Basics,
counting the Fossil, which really is a Basic once played). One TIGHT
energy flag: Houndstone's secondary `Hammer In` wants 2 Psychic and the
deck runs exactly 2 — its primary attack needs only 1.

Full field, 31 decks, 200 games each, paired — mean **54.1%**, median
**52.0%**, **16/31** winning. Best: Feraligatr 87.0%, T.R. Wobbuffet
74.5%, Crabominable 73.5%. Worst: T.R. Crobat snipe 33.0%, Panic Poison
38.0%, Arbok conditions 39.0%.

*`Energy Swatter` and `Eri` have no modeled effect in the simulator, so
their disruption is not counted in that figure.*

## Simulator work this deck required

**Fossils were not playable at all.** They are Item cards whose own text
says to play them as a Basic Pokémon, and the engine treated them as
Items — so a Fossil deck had **zero Basics**, mulliganed out and lost on
turn 2. That is why `selective_bloom_cradily` sat in the gauntlet's
"unplayable" list for this entire project, silently excluded from every
field measurement. Fossils now resolve as 60 HP Colorless Basics that
cannot retreat and carry no attacks, and Cradily plays a real game (45%
against Water Aggro rather than an automatic loss). Every deck's field
figure now includes one more opponent than it did before.
