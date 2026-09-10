# Dragapult ex / Dusknoir — TCGplayer, September 2026

**Not my list.** Taken from Natalie Millar's *The Best Pokémon TCG Decks
Right Now (September 2026)* on TCGplayer, published 2026-08-25, and
reproduced here card-for-card. The Dusknoir variant: `extra knockout potential at the cost of giving your opponent prize cards`, and per the article better than the straight build against Zoroark and single-Prize decks.

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
Pokémon: 20
4 Dreepy TWM 128
4 Drakloak TWM 129
3 Dragapult ex PRE 73
2 Duskull SFA 18
2 Dusclops PRE 36
1 Dusknoir SFA 20
1 Munkidori TWM 95
1 Meowth ex POR 62
1 Fezandipiti ex ASC 142
1 Budew PRE 4

Trainer: 32
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad ASC 198
4 Crushing Hammer POR 71
4 Lillie's Determination ASC 192
4 Ultra Ball ASC 213
3 Boss's Orders MEG 114
2 Night Stretcher ASC 196
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
