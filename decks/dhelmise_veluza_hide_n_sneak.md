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

## The problem this deck has to solve, and the card that solves it

**Every natural route puts the fuel into play instead of the discard.**
`Buddy-Buddy Poffin` benches it, `Poké Pad` puts it in hand, and playing a
Basic is free so you do it reflexively. Built the obvious way, the deck
never reaches four in the discard: measured, `Vengeful Anchor` fired at
**30 damage, never 170**, and the list came in at **51.2% mean, 10/29
winning**.

**`Naveen` POR 112** is the fix: *"Draw cards until you have 5 cards in
your hand. **Before drawing cards, you may discard any number of cards
from your hand.**"* Controlled discard, then a refill — dump the bodies,
draw back to five. It is the only Supporter in the pool that lets you
choose *what* to discard rather than dumping the whole hand.

With Naveen in and the fuel deliberately held back from the Bench:

| | mean | median | winning |
| --- | --- | --- | --- |
| built the obvious way | 51.2% | 46.0% | 10/29 |
| **+ 4 Naveen, fuel held for the discard** | **60.9%** | **58.0%** | **21/29** |

**`Night Stretcher` is cut, and it is worth saying why**: it puts a
Pokémon from your discard back into your hand — it runs the engine
*backwards*. `Sacred Ash` and `Lana's Aid` are the same trap.

## Decklist

```
Pokémon: 17
4 Shuppet PBL 33
4 Poltchageist PBL 5
3 Dhelmise PBL 39
2 Banette PBL 34
2 Sinistcha PBL 6
2 Veluza SCR 45

Trainer: 35
4 Kofu SCR 138
4 Naveen POR 112
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Team Rocket's Petrel ASC 207
3 Poké Pad ASC 198
3 Team Rocket's Factory ASC 203
2 Boss's Orders MEG 114
2 Switch MEG 130
2 Brave Bangle WHT 80
1 Brilliant Blender SSP 164
1 Lillie's Determination MEG 119
1 Redeemable Ticket JTG 156

Energy: 8
8 Basic Psychic Energy

Total Cards: 60
```

### Card choices worth stating

- **`Brilliant Blender` searches five cards out of the deck and discards
  them** — five Hide 'n' Sneak bodies at once clears the 4-threshold
  instantly and nearly clears the 6. It is the single best turn the deck
  has, and `Team Rocket's Petrel` (×4) searches any Trainer to find it.
- **`Ultra Ball` is a fuel line, not just search** — its cost is
  discarding 2 from hand, and the fuel is a legal discard.
- **`Poltchageist` PBL 5, not TWM 21 or TWM 171.** Only the PBL printing
  carries the Ability the payoffs count. TWM 21's `Tea Server` actively
  pulls Grass Energy back out of the discard.
- **`Banette` PBL 34** is fuel *and* a tutor: `Puppet Pull` is 80 damage
  and searches your deck for **any card**.
- **Kofu and Naveen both want the Supporter slot**, and you only get one a
  turn. Early turns are Naveen (fuel), later turns Kofu (discount) — the
  discount only matters once Veluza is the one attacking.

## Numbers

60 cards, no card over 4 copies, 1 ACE SPEC, no energy-type shortfall.
Mulligan **16.3%** (13 Basics). *`check_energy_support.py` flags 8 Grass
costs as IMPOSSIBLE — all false positives from name-pooling other Dhelmise
and Poltchageist printings; every attack in the exact list above is
Psychic- or Colorless-costed.*

1000-trial baseline, in play by turn 6: Shuppet 97.4%, Poltchageist 95.9%,
**Dhelmise 90.9% @ turn 1.92**, Veluza 60.5%, Banette 56.3%, Sinistcha
45.6%. First attack by turn 6: **75.4%**.

Full field, 29 decks, 150 games each — mean **60.9%**, median **58.0%**,
**21/29** winning. Best: T.R. Wobbuffet 90.0%, Eerie Inferno 86.0%,
Chandelure mill 80.7%, Static Venom 77.3%, Salazzle ex 76.0%. Worst:
Steven's Carbink 38.7%, Lurantis 40.0%, Panic Poison 42.0%.

## Where it loses

- **Flat damage reduction** (Steven's Carbink 38.7%). Vengeful Anchor is
  one number with no scaling headroom — a −30 wall takes 170 to 140 and
  there is nothing to add. Brave Bangle only helps against an ex.
- **Healing** (Lurantis 40.0%) undoes Matcha Spin's spread counters.
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

Covered by firing tests asserting Vengeful Anchor at 30/30/170/170 for
0/3/4/6 fuel, that a discarded Pokémon **without** the Ability does not
count, and that Matcha Spin is off at 5 and on at 6.
