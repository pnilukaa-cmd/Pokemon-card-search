# Dhelmise / Veluza — Hide 'n' Sneak fuel + Food Prep

Food Prep without Crabominable, paired with the Hide 'n' Sneak discard
package. Mono-Psychic, and the whole deck runs on **filling your own
discard pile on purpose**.

## The two thresholds

`Hide 'n' Sneak` is an Ability on four cards — `Shuppet` PBL 33,
`Banette` PBL 34, `Poltchageist` PBL 5, `Sinistcha` PBL 6 — and three
separate attacks count how many of them are in **your** discard pile:

| Payoff | Needs | Effect |
| --- | --- | --- |
| **`Dhelmise` PBL 39** — Vengeful Anchor `P` | **4+** | 30 → **170 damage for one Energy** |
| **`Sinistcha` PBL 6** — Matcha Spin `C` | **6+** | 4 damage counters on **each** of their Pokémon |
| ~~`Spiritomb` PBL 35~~ — Spiritual End `P` | **13+** | quadruple counters on 2 of their Pokémon |

**Spiritomb is out, and the reason is arithmetic**: there are only four
Hide 'n' Sneak names, so 16 copies is the absolute ceiling, and 13 of them
in the discard leaves three for your deck, hand and board combined. It
cannot coexist with a Food Prep package — or with much of anything.

Dhelmise is the deck. A **Basic** doing **170 for a single Psychic
Energy** is the most efficient attack in any list in this folder.

## Why it is mono-Psychic

Every attack in the deck is payable off one Energy type:

| | cost |
| --- | --- |
| Dhelmise — Vengeful Anchor | `Psychic` |
| Sinistcha — Matcha Spin | `Colorless` |
| Banette — Puppet Pull (80 **+ search your deck for any card**) | `Psychic` |
| Veluza — Sonic Edge | `Colorless ×4` → **free** at 4 Kofu |

`Veluza` is the Food Prep body. Sonic Edge is all-Colorless, so Psychic
Energy pays it, and Kofu discounts it to nothing while also filling the
discard with Kofu. `Crabominable` is gone because `Haymaker` is the only
attack in either package that demands a real **Water** symbol.

**Veluza is at 4, and that is what justifies 4 Kofu.** At 2 Veluza the
discount had nothing to land on often enough — Kofu was a dead Supporter
in a deck that already fights over its Supporter slot. Going to 4 puts a
Veluza in play by turn 6 in **96.8%** of games at avg turn 1.80, so the
Kofu count is paying for itself.

## The problem this deck has to solve, and the card that solves it

**Every natural route puts the fuel into play instead of the discard.**
Playing a Basic is free, so you do it reflexively; a search card that
benches the fuel is actively working against you. Built the obvious way,
the deck never reaches four in the discard: measured, `Vengeful Anchor`
fired at **30 damage, never 170**, and the list came in at **51.2% mean,
10/29 winning**.

**`Naveen` POR 112** is the fix: *"Draw cards until you have 5 cards in
your hand. **Before drawing cards, you may discard any number of cards
from your hand.**"* Controlled discard, then a refill — dump the bodies,
draw back to five. It is the only Supporter in the pool that lets you
choose *what* to discard rather than dumping the whole hand.

**`Night Stretcher` is cut, and it is worth saying why**: it puts a
Pokémon from your discard back into your hand — it runs the engine
*backwards*. `Sacred Ash` and `Lana's Aid` are the same trap.

## Why Buddy-Buddy Poffin is cut

Poffin only fetches Basics with **70 HP or less**. In this list that is
exactly two names — `Shuppet` (50) and `Poltchageist` (30) — and those are
the two cards the deck most wants in the **discard pile**, not on the
Bench. It cannot touch `Dhelmise` (140) or `Veluza` (110), the two Basics
you actually want in play. So the best card in most decks is, here, a
free two-card accelerant pointed at the wrong zone: every fuel body it
benches is one that has to be knocked out before it can count.

`Poké Pad` does the opposite job for the same slot. It fetches **any**
Pokémon — Dhelmise and Veluza included — and it puts it in **hand**,
which is precisely where `Gwynn` and `Naveen` can pitch it. One card,
either mode: board when you need board, fuel when you need fuel.

Measured head-to-head, same 60 otherwise (1000-trial baseline):

| in play by turn 6 | 4 Poffin, 2 Poké Pad | **no Poffin, 4 Poké Pad** |
| --- | --- | --- |
| Veluza | 91.6% | **97.6%** |
| Shuppet | 97.1% | 95.6% |
| Poltchageist | 96.7% | 88.8% |
| **Dhelmise** | 69.1% | **76.2%** |
| first attack | 78.3% | 79.4% |

Poffin is *better* at the two things you did not want (Shuppet,
Poltchageist on the Bench) and worse at the two that win games. Full
field, 29 decks, 150 games each: **68.5% with Poffin, 70.5% without.**

**The baseline table above is the load-bearing evidence, not the field
gap.** 1000 trials per row makes those setup numbers tight; the 2-point
field gap on its own sits inside run-to-run noise (below).

The freed slots go to Poké Pad 2 → 4, Gwynn 2 → 3, Brave Bangle 1 → 2.

## Prism Tower over Team Rocket's Factory

Team Rocket's Factory only pays out on a turn you play a Team Rocket
Supporter, and with Petrel trimmed to 3 that is a shrinking number of
turns — the Stadium sat there doing nothing most of the game.

`Prism Tower` CRI 111 — *discard 2 cards from your hand, draw 1* — is a
**repeatable discard outlet that costs no Supporter slot**. That is the
constraint the whole deck lives under: Kofu, Naveen and Gwynn all want
the one Supporter per turn, and Prism Tower fuels the discard around
them. Verified in a verbose trace firing twice in a single game.

It is card disadvantage on paper (2 in, 1 out). It is card *advantage*
here, because the two cards going in are the ones whose job is to be in
the discard.

Two copies, not one — it is also the deck's only way to push an opposing
Stadium off the field.

## The full survey of discard outlets

Everything in Standard that puts **your own** cards into **your own**
discard pile, ranked for this deck:

| Card | | Verdict |
| --- | --- | --- |
| **`Gwynn` PBL 109** | Supporter — *discard up to 2 Pokémon **without a Rule Box** from hand, draw **3 for each*** | **The best card here.** Every Hide 'n' Sneak body is single-Prize, so this is Naveen's fuelling job *plus* a 6-card draw on one card. Now at 3 |
| **`Naveen` POR 112** | Supporter — discard any number from hand, draw to 5 | The flexible one; discards fuel you already hold |
| **`Prism Tower` CRI 111** | Stadium — discard 2 from hand, draw 1 | **In at 2.** Repeatable, and free of the Supporter bottleneck |
| **`Brilliant Blender` SSP 164** | ACE SPEC Item — search 5 cards out of the deck and discard them | Five bodies in one Item. Still the ACE SPEC |
| `Ultra Ball` MEG 131 | Item — discard 2 from hand as its cost | Already in, and the cost is upside here |
| `Raifort` TWM 161 | Supporter — look at top 5, **discard any number** | Selective self-mill, but a third Supporter competing for the slot |
| `Hole-Digging Shovel` POR 74 | Item — discard top 2 of your deck | **Tested and bad — see below** |
| `Larry's Skill` PRE 115 | Supporter — discard hand, search Pokémon + Supporter + Energy | Uncontrolled; dumps what you wanted to keep |
| `Carmine` TWM 145 | Supporter — discard hand, draw 5 | Same problem, no tutor |
| `Secret Box` TWM 163 | ACE SPEC — discard 3, search 4 card types | Competes with Blender for the ACE SPEC |
| `Slowpoke` PBL 29 | Basic, `All-You-Can-Yeet` `P` — discard any number from hand | On-type and free-choice, but it costs your attack for the turn |

**On Tools specifically: there are none.** Every Pokémon Tool in the
format whose text contains "discard" is discarding *itself* (the Berries,
Deluxe Bomb, Tremendous Bomb, Powerglass). No Tool is a discard outlet.

### Tested

| Build | mean | median | winning |
| --- | --- | --- | --- |
| built the obvious way | 51.2% | 46.0% | 10/29 |
| 4 Naveen, fuel held for the discard | 60.9% | 58.0% | 21/29 |
| 2 Naveen + 2 Gwynn | 61.7% | 59.3% | 25/29 |
| + 3 Hole-Digging Shovel (−Poké Pad, −Lillie's, −Switch) | 56.8% | 52.7% | 16/29 |
| 4 Veluza, 3 Lillie's, 3 Petrel, Prism Tower, **Poffin kept** | 68.5% | 66.7% | 26/29 |
| **same, Poffin cut for Poké Pad / Gwynn / Bangle** | **70.5%** | **70.0%** | **27/29** |
| *(identical list, second run — see the variance note)* | 71.6% | 70.7% | 28/29 |

`Gwynn` was a small mean gain but moved winning matchups **21 → 25**, and
the reason is that it is the only outlet that pays you for discarding
rather than charging you.

**`Hole-Digging Shovel` is a trap.** Milling the top 2 blind is only ~20%
fuel per card in this list — the other 80% of the time it is throwing away
Dhelmise, Energy or your search. Random self-mill is not the same thing as
selective self-mill; `Raifort` does the same job while letting you look
first.

## Decklist

```
Pokémon: 19
4 Veluza SCR 45
4 Shuppet PBL 33
4 Poltchageist PBL 5
3 Dhelmise PBL 39
2 Banette PBL 34
2 Sinistcha PBL 6

Trainer: 33
4 Kofu SCR 138
4 Ultra Ball MEG 131
4 Poké Pad ASC 198
3 Team Rocket's Petrel ASC 207
3 Lillie's Determination MEG 119
3 Gwynn PBL 109
2 Naveen POR 112
2 Prism Tower CRI 111
2 Boss's Orders MEG 114
2 Switch MEG 130
2 Brave Bangle WHT 80
1 Brilliant Blender SSP 164
1 Redeemable Ticket JTG 156

Energy: 8
8 Basic Psychic Energy

Total Cards: 60
```

### Card choices worth stating

- **`Brilliant Blender` searches five cards out of the deck and discards
  them** — five Hide 'n' Sneak bodies at once clears the 4-threshold
  instantly and nearly clears the 6. It is the single best turn the deck
  has, and `Team Rocket's Petrel` searches any Trainer to find it.
- **Petrel is at 3, not 4.** It is a tutor, not a payoff — the fourth copy
  was the one you drew after already finding Blender. The slot went to
  `Lillie's Determination`, which is at **3** because a mono-Psychic deck
  of 30–140 HP bodies needs an actual out to a bad board, not one copy of
  one.
- **`Ultra Ball` is a fuel line, not just search** — its cost is
  discarding 2 from hand, and the fuel is a legal discard.
- **`Poltchageist` PBL 5, not TWM 21 or TWM 171.** Only the PBL printing
  carries the Ability the payoffs count. TWM 21's `Tea Server` actively
  pulls Grass Energy back out of the discard.
- **`Banette` PBL 34** is fuel *and* a tutor: `Puppet Pull` is 80 damage
  and searches your deck for **any card**.
- **Kofu, Naveen and Gwynn all want the Supporter slot**, and you only get
  one a turn. Early turns are Naveen/Gwynn (fuel), later turns Kofu
  (discount) — the discount only matters once Veluza is the one attacking.
  Prism Tower exists to fuel on the turns the Supporter is spent elsewhere.

## Numbers

60 cards, no card over 4 copies, 1 ACE SPEC, no energy-type shortfall.
Mulligan **11.8%** (15 Basics — down from 16.3%, because Veluza 2 → 4 added
two more Basics than Poffin's cut removed). *`check_energy_support.py`
flags 8 Grass costs as IMPOSSIBLE — all false positives from name-pooling
other Dhelmise, Poltchageist and Sinistcha printings; every attack in the
exact list above is Psychic- or Colorless-costed.*

1000-trial baseline, in play by turn 6: **Veluza 96.8% @ turn 1.80**,
Shuppet 94.9%, Poltchageist 92.6%, **Dhelmise 79.8% @ turn 2.31**,
Banette 61.3%, Sinistcha 45.8%. First attack by turn 6: **77.8%**.
(The baseline sim does not model Gwynn, Naveen or Redeemable Ticket —
their effect shows up in the full-field numbers, not these.)

Full field, 29 decks, 150 games each — mean **70.5%**, median **70.0%**,
**27/29** winning. Best: Feraligatr/Munkidori 96.0%, T.R. Wobbuffet 92.0%,
Chandelure mill 92.0%, Eerie Inferno 86.7%, Darkness Mill 85.3%. Worst:
Steven's Carbink 48.0%, N's Zoroark 49.3%, Panic Poison 51.3%.

**Variance note.** This exact list run a second time against the same
field gave **71.6% mean, 70.7% median, 28/29**. At 150 games per matchup
the mean carries roughly **±1 point**, and a single matchup swings much
more than that — Steven's Carbink read 48.0% and then 41.3%. So read the
field mean to one significant figure: this deck is a **~70%** list, and
any two builds inside 2 points of each other are not separated by these
numbers alone. Per-matchup rows are directional, not precise.

## Where it loses

- **Flat damage reduction** (Steven's Carbink 48.0%). Vengeful Anchor is
  one number with no scaling headroom — a −30 wall takes 170 to 140 and
  there is nothing to add. Brave Bangle only helps against an ex.
- **Toolbox attackers** (N's Zoroark 49.3%) copy your own 170 back at you
  off a body that outlives yours.
- **170 does not one-shot the big tier.** Most Mega ex sit at 300+, so
  the deck trades rather than races, and its own bodies are 30–140 HP.
- **The fuel is also the board.** Twelve Hide 'n' Sneak Pokémon have two
  incompatible jobs — being discarded, and being the Sinistcha line. Every
  Poltchageist you discard is one you cannot evolve.

## Simulator work this deck required

1. **The threshold clause did not exist.** *"If you have N or more Pokémon
   that have the Hide 'n' Sneak Ability in your discard pile"* compiled to
   nothing on `Dhelmise` (so Vengeful Anchor was a flat 30) and was
   silently dropped on `Sinistcha` (so Matcha Spin fired unconditionally).
   Adds a `named_ability_in_discard` condition that counts the discard by
   Ability name.
2. **Attack riders ignored their own conditions.** `attack_side_effects`
   applied every action regardless, and `attack_rider_value` priced them
   the same way — a gated attack read as always-on to both the engine and
   the AI.
3. **Conditional flat damage bonuses were unreadable.** "*If <condition>,
   this attack does N more damage*" had no path at all; only the "for
   each" scaling shape did.
4. **The AI benched every Basic on sight**, so a deck whose payoff counts
   its own Pokémon in the discard could never turn its payoff on. It now
   holds back a Basic that is worth more as fuel, once a board exists.
5. **No Stadium did anything.** `Stadium` cards were tracked but never
   executed, so the Factory-vs-Prism-Tower question could not be asked.
   Adds `use_stadium`, with Prism Tower as a repeatable fuel outlet and
   Team Rocket's Factory gated on a Team Rocket Supporter that turn.

Covered by firing tests asserting Vengeful Anchor at 30/30/170/170 for
0/3/4/6 fuel, that a discarded Pokémon **without** the Ability does not
count, and that Matcha Spin is off at 5 and on at 6.
