# Pure Dragapult ex — TCGplayer, September 2026

<!-- field-results -->
> ### Field results — 2026-09-13
> **53.2% mean · 51.5% median · 24 of 43 winning matchups · rank 19 of 44**
>
> Best `meta_ns_zoroark` 86% · worst `team_rockets_persian_ex_attack_theft` 33%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->








**Not my list.** Taken from Natalie Millar's *The Best Pokémon TCG Decks
Right Now (September 2026)* on TCGplayer, published 2026-08-25, and
reproduced here card-for-card. The straight build. Per the article this is `slightly better in the mirror match`, and runs a 1/1 Dunsparce/Dudunsparce line for extra cards plus a lone `Moltres` tech.

The article's own summary of the archetype: Phantom Dive "does relevant
damage and sets up for multi-Prize turns while also delaying knockouts to
avoid activating Fezandipiti ex and Unfair Stamp", fuelled by Drakloak's
`Recon Directive` and `Crispin` for Phantom Dive's two colours.

## Provenance and what I changed

The published list gives set codes but **no collector numbers**, so every
line was resolved against this repo's card pool. Two lines needed a
different printing, and neither is an error in the original:

- `Crushing Hammer SVI` — this pool has no SVI. It carries **POR 71** and
  PBL 105; the article's own Dusknoir list uses POR, so POR 71 is used in
  both.
- `Judge DRI` — this pool carries only **POR 76**.
- Basic Energy was printed as `MEE`; Basic Energy takes no set code and is
  written without one here, as everywhere else in this repo.

Everything else resolved exactly as published.

## Decklist

```
Pokémon: 19
4 Dreepy PRE 71
4 Drakloak ASC 159
3 Dragapult ex TWM 130
2 Munkidori ASC 99
1 Meowth ex POR 62
1 Fezandipiti ex ASC 142
1 Dunsparce JTG 120
1 Dudunsparce PRE 80
1 Moltres PFL 14
1 Budew PRE 4

Trainer: 33
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad ASC 198
4 Crushing Hammer POR 71
4 Lillie's Determination ASC 192
4 Ultra Ball ASC 213
3 Night Stretcher ASC 196
3 Boss's Orders MEG 114
2 Risky Ruins MEG 127
2 Crispin PRE 105
1 Rosa's Encouragement POR 84
1 Judge POR 76
1 Unfair Stamp TWM 165

Energy: 8
3 Basic Psychic Energy
3 Basic Fire Energy
2 Basic Darkness Energy

Total Cards: 60
```

## Modelling note

Four of this deck's Trainers had no working model in this simulator until
the day it was added — `Crushing Hammer` compiled to nothing at all,
`Crispin` fetched Energy without attaching any, `Rosa's Encouragement`
attached four Energy off a card that says two, and `Unfair Stamp` let the
opponent draw five when the card gives them two. Against
`heracross_sinistcha_tea` this deck measured **40.0%** with all four inert
and **63.3%** with them working. Any number recorded for it before that
fix is meaningless.
