# Deck Hand Odds

Flutter app that computes exact opening-hand odds for a 60-card Pokemon TCG
deck. Paste a decklist export (Pokemon TCG Live, PokemonCard.io, or
Limitless TCG) and it shows odds two ways:

- **By Category** (default): well-differentiated stats like "88% chance of
  at least 1 Pokemon in your opening hand", grouped into Pokemon /
  Supporter / Item / Tool / Stadium / Energy. When a deck has more than one
  Pokemon type (e.g. a Dark/Psychic deck) or more than one Energy type,
  those two categories further split by type ("Pokemon (Darkness)",
  "Pokemon (Psychic)") instead of lumping them together; a mono-type deck
  keeps the simple single bucket. **This is a toggle** ("Split Pokemon/
  Energy by type", on by default) shown above the format dropdown -- turn
  it off to always keep single lumped buckets regardless of type
  diversity. Also includes:
  - **Top 5 most likely hand shapes** by category composition.
  - **Confidence calculator**: pick a target confidence (80/90/95/99%) and
    see how many copies of each category you'd need in the deck to hit
    "at least 1 in opening hand" at that confidence, versus how many you
    currently have.
  - **Optimal-hand comparison**: enter your own target count per category
    for an ideal 7-card hand (pre-filled with the #1 most likely shape as a
    starting point), and see its exact probability compared against the
    single most likely shape.
  - **Deck-building recommendations**: a rule-based check (grounded in
    commonly-cited Standard deck-building ratios) that flags things like too
    few/many Pokemon, Trainers, or Energy, too few Basic Pokemon, thin Stage
    2 evolution lines, no Supporters at all, or an illegal >4-copy count
    (>4 of a non-Basic-Energy card) -- each with a stated reason. Only shows
    up when there's something worth flagging; a well-built list shows none.
    Basic Pokemon and evolution-stage recommendations rely on a per-card
    "stage" field bundled in `assets/card_categories.json`, so they only
    cover cards in the current Standard-legal pool -- older/homebrew/rotated
    Pokemon fall into an "unknown stage" bucket and are silently excluded
    from those specific checks (but still counted normally everywhere else).
- **Exact Hands**: the top 5 most probable exact card-for-card 7-card hands.
  With ~15-25 unique card names in a typical deck these cluster very close
  together (each around 0.02%) since there are tens of thousands of
  possible exact combinations -- useful for precision, but Category mode is
  more actionable for "what will my opener probably look like."

All of this is exact math (multivariate hypergeometric distribution), not
simulation estimates.

## Supported decklist formats

The parser tries every known suffix pattern regardless of a dropdown
selection you make, so pasting works the same either way -- the dropdown
(with a short format example below it) is just there so you know what's
expected:

- **Pokemon TCG Live**: `Pokémon: 14` / `Trainer: 34` / `Energy: 12` section
  headers (colon), cards like `2 Sandile BLK 57` (space-separated set code +
  number).
- **PokemonCard.io**: `// PokemonCard.io Deck List` comment header, no
  section headers, cards like `1 Allister swsh4-146` (hyphenated
  `setcode-number` as one token). Verified against a real export.
- **Limitless TCG**: `Pokémon (17.48)` / `Trainer (34.6)` / `Energy (7.87)`
  section headers (parentheses, not colon), same space-separated
  `SETCODE NUMBER` card shape as PTCG Live. Verified against a real export
  -- though that particular export turned out to be an **"archetype
  average"** view (fractional counts like `1.89` or `0.01`, statistically
  averaged across many tournament decks, not one buildable 60-card deck).
  The parser handles this gracefully: counts round to the nearest integer,
  entries that round to 0 are dropped, and a clear warning fires explaining
  this looks like an aggregate/average list rather than a real decklist. A
  genuine single-player Limitless export (integer counts) should parse
  cleanly with no such warning.

### The "not whole numbers" warning

If you see a warning about card counts not being whole numbers, you've
likely pasted a statistical/meta-analysis view (an archetype's average
build across many real decks) rather than one specific player's decklist.
The app still parses it (rounding each count, dropping anything that rounds
to 0) so you can see an approximate build, but the resulting percentages
aren't meaningful for deck-building the way they are for a real decklist --
look for an individual tournament player's submitted list instead if you
want exact math.

## Status / what's been verified

The full Flutter SDK (3.44.8 stable) was installed and used to actually
verify this project, not just read the code:

- `flutter analyze`: **0 errors** across the whole project.
- `flutter test`: **all tests pass** (6 widget tests), including an
  end-to-end test that loads the sample deck, calculates, and checks
  type-split categories, the confidence calculator, and the optimal-hand
  comparison (including its pre-filled starting values) all render and
  compute correctly, a dedicated test confirming the type-split toggle
  actually keeps a single lumped bucket when turned off, and two tests for
  the recommendations engine -- one pasting a deliberately bad decklist
  (illegal copy count, no Supporters) and confirming the specific warnings
  show up, one confirming a well-built decklist shows no recommendations
  at all.
- `flutter build web`: **builds successfully** to `build/web/`.
- `lib/deck_parser.dart`, `lib/hand_odds.dart`, and `lib/card_categories.dart`
  were also independently run as plain Dart scripts
  (`test/verify_hand_odds.dart`, `test/verify_categories.dart`):
  - Exact-hand math confirmed against a Python prototype (109,000 hand
    compositions, probabilities summing to exactly 1.000000).
  - Diacritic-insensitive matching confirmed (e.g. "Poke Pad" typed without
    the accent still resolves to the real "Poké Pad"'s category).
  - Type-splitting confirmed: a real Dark/Psychic mixed-type fixture splits
    into separate buckets; a genuinely mono-type fixture does not.
  - `minimumCountForConfidence()` confirmed to return the actual minimum
    (one fewer copy provably falls below the target confidence) at 80/90/
    95/99% targets.
  - `compositionProbability()` confirmed to match direct hypergeometric
    computation and to never exceed the enumerated maximum.
- The `android/` and `web/` native project folders (generated by
  `flutter create .`) are committed, so you don't need to generate them
  yourself -- Android SDK/toolchain wasn't available in the environment that
  built this, so the Android build itself is unverified, but the Dart/
  Flutter layer underneath it is the same code that passed analyze/test/web
  build.

A real PokemonCard.io export was also tested during development (not one of
the automated tests, but worth knowing): a user-provided decklist mixing
cards from many old, long-rotated sets parsed 60/60 cards correctly once the
PokemonCard.io suffix format was added, though most of those specific old
cards fell into the "Trainer (unspecified)" / "Unrecognized" fallback
buckets since the category lookup only covers the current Standard-legal
pool, not historical cards -- expected behavior, not a bug, for an
Expanded/old-format decklist.

## Setup

1. Install Flutter: https://docs.flutter.dev/get-started/install (this also
   walks you through installing Android Studio, which gives you the Android
   SDK and an emulator -- needed to actually run on Android, not just to
   build the Dart/Flutter code)
2. From this directory: `flutter pub get`
3. Run it:
   - `flutter run -d chrome` to see it in a browser immediately, no
     emulator/device needed
   - `flutter run` with an Android emulator running (via Android Studio) or
     a physical device connected (USB debugging enabled) to run it as a
     real Android app
4. If anything complains, run `flutter doctor` -- it diagnoses exactly
   what's missing on your machine (e.g. unaccepted Android licenses) and
   usually tells you the fix directly.

## Project layout

```
lib/
  deck_parser.dart      -- parses decklist paste text -> {name: count},
                            supports PTCG Live / PokemonCard.io / Limitless
  hand_odds.dart         -- exact hand-probability math (hypergeometric)
  card_categories.dart   -- categorization, type-splitting, marginal odds,
                            confidence calculator, composition probability
  main.dart               -- Flutter UI (paste box, mode toggle, results,
                            confidence calculator, optimal-hand comparison)
assets/
  card_categories.json  -- name -> {category, types}, generated from
                            pokemon_standard_cards.json
test/
  verify_hand_odds.dart   -- standalone verification script (see Status above)
  verify_categories.dart  -- standalone verification script (see Status above)
  widget_test.dart        -- Flutter widget tests (see Status above)
```

To regenerate `assets/card_categories.json` after the card database
updates, see the Python snippet in this file's git history, or ask for it
to be regenerated from `pokemon_standard_cards.json` in the repo root.

## Known limitations / next steps

- Only computes the **opening 7-card hand**. Turn 2/3 draws depend on what
  you actually played turn 1 (which cards you searched, evolved, etc.), so
  they need the turn-by-turn simulation logic from this repo's
  `simulate_match.py` ported over, not the pure-combinatorics approach.
- The parser strips the trailing set-code + number and only keys on card
  name. Two different prints of the same-named card are treated
  identically, which is correct for hand-odds math but means the app has no
  card metadata (HP, attacks, images) beyond what's typed in.
- The opening-hand odds themselves still treat all Pokemon as one category
  (Basic vs. evolution isn't split into separate hand-odds buckets) -- "at
  least 1 Pokemon" isn't the same as "hand is legal to start with." The
  deck-building recommendations feature does use per-card stage data (see
  above) for its Basic-count and evolution-line checks, but that's a
  separate, coarser check than the exact hand-odds math.
- The category lookup only covers the current Standard-legal card pool.
  Older/Expanded-format cards fall back to a generic "Trainer
  (unspecified)"/"Unrecognized" bucket instead of being properly typed and
  categorized. Broadening this to the full historical card pool was
  considered but deliberately deferred -- ask for it if Expanded support
  becomes a priority.
- No manual card picker yet -- paste-only, per the initial scope.
- Limitless TCG's per-player decklist export (integer counts, not the
  "archetype average" view) hasn't been tested against a real single-deck
  export yet -- only the average/aggregate format has been confirmed so far.
