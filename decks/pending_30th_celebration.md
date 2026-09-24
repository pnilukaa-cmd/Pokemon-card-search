# Pending — Maushold mill (30th Celebration)

> **Status 2026-09-24: superseded.** 30th Celebration landed in the pool on
> 2026-09-17 (see `pending_new_sets.md`) and is treated as legal. The
> Maushold mill lists that use it are in the field as
> `maushold_gnaw_together_mill` and `study_maushold_gnaw_latias`. The text
> below is kept as the record of why it was held back.

**This is a research note, not a deck file.** It has no fenced decklist on
purpose: two of its cards do not exist in this repo's pool, so
`check_decks.py` would be right to reject it and the field runner would be
right to skip it. It is here so the work is not lost when the set lands.

## The blocker

`30C` is **Pokémon TCG: 30th Celebration** — a real set, released
worldwide **2026-09-16**, tournament legal for Play! Pokémon from
**2026-09-25**. 199 cards: 128 main set, 33 Secret Rares, 30 Classic
Collection (**not** tournament legal) and 8 foil Basic Energy. `MEE` is
that Basic Energy subset.

It is not in `pokemon_standard_cards.json`, and it cannot be added yet:

- `api.pokemontcg.io` — the source this pool is built from — has not
  indexed it. Its newest set is `PBL` (2026-07-17), the same as ours, and
  its newest `Mew ex` is from Paldean Fates (2024). Regulation marks `K`
  and `L` both return 0 cards.
- Every other card source is refused by the network egress proxy at
  CONNECT: pokemon.com, serebii.net, bulbapedia, limitlesstcg, pokebeach,
  pokemoncard.io, tcgplayer.
- Web-search summaries are the only thing available and they already
  disagree with each other on Maushold's collector number (146 vs 147),
  which is exactly the field a decklist line needs to be right.

Hand-entering card text from a secondary summary into the pool would put
unverified data underneath every measurement in this repo. Not done.

**To finish this:** re-run `python3 fetch_pokemon_cards.py --check` after
the set is indexed. It now reports what would change without writing, and
warns if a regulation mark outside `ACTIVE_REGULATION_MARKS` has acquired
cards — 30C may ship under a new mark, and the silent failure mode is a
fetch that returns the same cards as last time with nothing to indicate
the newest set is missing.

## The two cards, as far as secondary sources agree

| | |
|---|---|
| `Mew ex` **158/128** | Futuristic Rare, Psychic Basic ex, 160 HP, retreat 0. **Memory Helix**: *this Pokémon can use the attacks of any of your Benched Pokémon (you still need the Energy).* **Teleportation Burst** [P] 30, may switch to a Benched Pokémon. |
| `Maushold` **146 or 147/128** | Illustration Rare, Colorless Stage 1, 80 HP. **Gnaw Together** [C]: flip a coin for each Maushold in play; for each heads, discard the top 2 cards of your opponent's deck. |

## The list as submitted

Not mine — supplied by the user. 60 cards; 25 of its 28 lines resolve
against the current pool with valid SET NUMs. The three that do not:

- `4 Maushold 30C` — set not in the pool. The pool's only `Maushold` is
  **SSP 158**, a different card (`Familial March` / `Incessant Incisors`).
- `1 Mew ex 30C` — the pool has **no** `Mew ex` in any printing.
- `3 Psychic Energy MEE 5` — should be written **`3 Basic Psychic Energy`**
  with no set code. The pool holds no Basic Energy cards at all (only 18
  Special Energy); `tcg_model` handles Basic Energy by name. With that one
  line rewritten the deck builds to 55 of 60, the gap being exactly the
  four Maushold and one Mew ex.

```text
Pokémon: 18
4 Tandemaus SSP 157
4 Maushold 30C            <- unresolvable
2 Dunsparce JTG 120
2 Dudunsparce PRE 80
2 Fan Rotom ASC 171
1 Mew ex 30C              <- unresolvable
1 Dedenne SSP 87
1 Shaymin DRI 10
1 Psyduck ASC 39

Trainer: 35
4 Lillie's Determination ASC 192
2 Boss's Orders ASC 183
2 Hassel TWM 151
1 Lana's Aid TWM 155
1 Xerosic's Machinations SFA 64
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
4 Crushing Hammer POR 71
2 Sacred Ash DRI 168
1 Ultra Ball ASC 213
1 Night Stretcher ASC 196
1 Redeemable Ticket JTG 156
3 Backtrack Badge PBL 74
1 Air Balloon ASC 181
1 Handheld Fan TWM 150
2 Nighttime Mine ASC 197
1 Neutralization Zone SFA 60

Energy: 7
4 Mist Energy TEF 161
3 Basic Psychic Energy    <- was "Psychic Energy MEE 5"
```

## What the engine will need

`Memory Helix` is the same shape as `N's Zoroark ex`'s `Night Joker` — use
a Benched Pokémon's attack — but as an **Ability** rather than an attack,
and unrestricted rather than family-scoped. The copy-attack machinery
(`_COPY_OWN_BENCH_RE`, `copied_attack`, `_best_borrowed`, the recursion
guard) is built and exercised; the rule that recognises the text is not.
Worth writing the moment real card text is in hand, and not before.

`Gnaw Together` is a coin-flip mill scaling on a count of your own
Pokémon in play. `mill_scaler_damage` and `parse_chance` both exist; the
"flip a coin for each X" shape needs checking against the real wording.
