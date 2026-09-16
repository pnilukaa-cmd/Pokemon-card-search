# Mega Heracross ex / Sinistcha — Spill the Tea

<!-- field-results -->
> ### Field results — 2026-09-16
> **59.6% mean · 59.0% median · 33 of 44 winning matchups · rank 9 of 45**
>
> Best `meta_ns_zoroark` 92% · worst `scovillain_salazzle_spicy_rage` 27%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the Stadium-passive fix and is not comparable**: 20 Stadiums had inert passives, Stadiums a deck wanted but did not name by text were never played at all, and blind discard costs pitched arbitrary cards instead of ranking them.
<!-- field-results -->
















> **CORRECTION (re-measured after the ex audit).** The numbers first
> recorded here — 66.4% mean, 32 of 34 winning — were measured on an
> engine in which **`Spill the Tea` never paid its cost.** The attack
> reads "discard up to 3 Grass Energy cards from your Pokémon. This
> attack does 70 damage for each card **you discarded in this way**",
> and the simulator credited the damage without performing the discard.
> It was free 210 every turn.
>
> With the cost charged, this deck measures **49.3% mean / 49.0% median /
> 15 of 33 winning**. It is a fine deck, not the strongest in the folder,
> and the recycling engine below is what keeps it playable rather than
> what makes it dominant: `Tea Server` returning one Basic Grass Energy
> per turn does not refill three.
>
> Everything below this line is the original write-up. The card reasoning
> stands; the numbers in it do not.

It arrived by accident, and the honest version of how is worth more than
the list: the deck was built to test `Munkidori` laundering damage off a
big-HP soaker into a `Snow Coating` doubler, and **the two cards it was
built around both measured as costs.** What was left is what wins.

## The engine is `Spill the Tea`, and it recycles itself

`Sinistcha` **TWM 22** — Stage 1 from Poltchageist, 70 HP.

> **`Grass` Spill the Tea 70× — discard up to 3 Grass Energy cards from
> your Pokémon. This attack does 70 damage for each card discarded.**

**Up to 210 damage for a single Grass Energy.** Traced over 15 games it is
the deck's most-used attack by a wide margin (25 uses, against 16
Mountain Ramming and 14 Juggernaut Horn).

The discard is not a cost here, because of the Basic it evolves from:

`Poltchageist` **TWM 21** — **`Grass` Tea Server: put a Basic Grass Energy
card from your discard pile into your hand.**

Spill the Tea throws Grass Energy away; Tea Server picks it back up. Four
Poltchageist and fourteen Grass Energy is what makes a 210-damage attack
repeatable rather than a one-off.

**Note the printing.** `Poltchageist` TWM 21 is the one with Tea Server.
TWM 20 has `Storehouse Hideaway` and PBL 5 has `Hide 'n' Sneak` — neither
recycles anything.

## The counter-puncher

`Mega Heracross ex` **PFL 108** — a **Basic** with **280 HP**.

> `Grass``Grass` **Juggernaut Horn 100+** — *if this Pokémon was damaged
> by an attack during your opponent's last turn, this attack does that
> much more damage.*

Not "50 more" — **exactly what it took**. Hit for 150, swing for 250. Hit
for 200, swing for 300. And `Grass``Grass``Grass` Mountain Ramming is a
flat 170 with a two-card mill when they have not attacked into it.

A 280 HP **Basic** is the whole reason this deck is fast: no line to
assemble, and it is out by turn 2 in 63.8% of games.

The cost is honest: it is a Mega Evolution ex, so **it gives up 3 Prizes**.

## The two cards it was built around, and why both are gone

### Munkidori: −4.9 points

The plan was sound on paper — a big body soaks a hit, and
`Adrena-Brain` moves 3 damage counters off it onto the opponent, turning
damage taken into damage dealt.

| | mean | median | winning |
| --- | --- | --- | --- |
| with 4 Munkidori + 4 Prism Energy | 60.4% | 60.0% | 26/34 |
| **without** (Dunsparce line + 4 more Grass) | **65.3%** | **65.5%** | **30/34** |
| *independent seed* | 59.9% → **66.4%** | → 65.0% | 26 → **32/34** |

**It is redundant with Juggernaut Horn.** Both cards convert damage-taken
into damage-dealt, and Heracross does it at *100 plus the full amount* per
turn where Munkidori does *30*. Paying a second card — and four Prism
Energy diluting the Grass line, because Adrena-Brain needs Darkness
attached — to do a worse version of what the deck already does was a
straight loss.

### Snow Coating: −3.1 points

| | mean | median | winning |
| --- | --- | --- | --- |
| this deck's Grass core | **60.4%** | 60.0% | **26/34** |
| + 3 Vanillite / 2 Vanilluxe / 1 Vanillish / 3 Rare Candy | 57.3% | 55.2% | 25/34 |

That is the **fourth** shell in which `N's Vanilluxe` has been built and
measured, and the fourth in which it does not earn its slots. The record:

| shell | with | without |
| --- | --- | --- |
| N's Zoroark toolbox | 17.5% | — (archetype was 36%) |
| Palossand ex | 35.4% | **35.3%** |
| Kyurem ex / Water | **46.4%** | 40.5% |
| this Grass core | 57.3% | **60.4%** |

It works in exactly one place — the Kyurem shell — and there it earns its
keep as a `Blizzard` attacker rather than as a doubler.

## Decklist

```
Pokémon: 17
4 Poltchageist TWM 21
4 Mega Heracross ex PFL 108
4 Dunsparce JTG 120
3 Sinistcha TWM 22
2 Dudunsparce TEF 129

Trainer: 29
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Poké Pad ASC 198
3 Lillie's Determination MEG 119
3 Boss's Orders MEG 114
3 Switch MEG 130
2 Cyrano SSP 170
2 Night Stretcher MEG 173
2 Judge POR 76
1 Air Balloon ASC 181
1 Hero's Cape TEF 152

Energy: 14
14 Basic Grass Energy

Total Cards: 60
```

- **Fourteen Grass Energy is the attack, not the support.** Spill the Tea
  discards up to three per swing. This is one of the few decks where
  running out of Energy is the failure mode rather than drawing too much.
- **`Buddy-Buddy Poffin` reaches every Basic here** — Poltchageist (40 HP)
  and Dunsparce (70) are both under the cap. It cannot fetch Heracross;
  `Ultra Ball` and `Cyrano` do that.
- **`Cyrano` searches three Pokémon ex at once.** `Poké Pad` cannot touch
  Heracross (Rule Box), so it is there for the Sinistcha line.
- **`Hero's Cape`** (+100 HP → **380**) is the ACE SPEC, on Heracross.
  More HP is more turns absorbing hits, and Juggernaut Horn is paid in
  exactly the damage it absorbs.

## Numbers

60 cards, no card over 4, one ACE SPEC. Mulligan **19.1%** (12 Basics).

1200-opening curve: Poltchageist 88.0% by T2, **Mega Heracross ex 63.8% by
T2 and 85.5% by T6**, Sinistcha 42.9% by T2 and 85.9% by T6.

Full field, 34 decks, 200 games each — mean **66.4%**, median **65.0%**,
**32/34** winning. Independent seed: 65.3% / 65.5% / 30-34.

## Where it loses

Only two matchups, and they are the same two that beat most things in
this folder: `panic_poison_paralysis` and `toxic_slumber_vileplume_ex` —
**Special Conditions**. A 280 HP Basic that wants to sit in the Active
Spot and absorb hits is exactly what Paralysis and Sleep punish, because
the counter-punch never gets to happen.

`Switch` at 3 and `Air Balloon` are the partial answer already in the
list; a Special-Condition immunity Tool or Energy would be the real one,
and is the first thing to test if you take this to a table.
