---
name: tcg-theorycraft
description: Systematic combo-mining and deck theorycrafting over this repo's Pokémon TCG Standard card database (pokemon_standard_cards.json / mechanic_index.json / analyze_mechanics.py). Use this whenever the user asks to find cards built around a mechanic, ability, or theme ("find Pokémon with X", "what synergizes with Y", "cards that benefit from Z", "build a deck focused on/around W", "theorycraft a deck"), even if they don't name this skill directly. Also use it to sanity-check a proposed deck (Basic count / mulligan odds, energy curve, type coherence) before handing back a decklist. Do not skip straight to inventing a decklist from memory or guessing card names/text — this skill exists specifically because that produces wrong or incomplete answers; always search the actual data first.
---

# TCG Theorycraft

Finding "every card related to mechanic X" in this card pool is deceptively
easy to get wrong by guessing. It has failed in two distinct ways before this
skill existed:

1. Searching only by ability/attack **name** and missing cards that
   *reference* that name elsewhere as a payoff condition (e.g. Dhelmise and
   Spiritomb both scale their damage off "the Hide 'n' Sneak Ability" being
   in the discard pile, without having that Ability themselves — a
   name-only search never finds them).
2. Hand-rolling a fresh keyword search for a general concept instead of
   checking the mechanic taxonomy that already exists — and, when a raw
   sweep *is* needed, either trusting its noise uncritically or dismissing
   it instead of manually triaging the hits.

This skill exists to make the correct process the default path, not
something re-derived under time pressure each time.

## Prerequisites

This only works from the repo root (`pokemon_standard_cards.json`,
`mechanic_index.json`, and `analyze_mechanics.py` need to be in the current
directory). If `mechanic_index.json` looks stale or missing, regenerate it
with `python3 analyze_mechanics.py` first.

## The process

### 1. Classify the ask: named mechanic, or general concept?

- **A specific named Ability/attack** (e.g. "Hide 'n' Sneak", "Tighten Up"):
  run `scripts/search_mechanic.py --sweep-phrase "<exact name>"`. This
  searches both the ability/attack's own name field *and* every card's body
  text in one pass, so it catches both the cards that HAVE it and the cards
  that reference it by name as a scaling condition. This is usually enough
  on its own for a named mechanic — the phrase is specific enough that noise
  is rare.

- **A general concept** (e.g. "card draw", "hand discard", "Confusion",
  "healing", "Stage 2 Pokémon with ability X"): don't invent a regex from
  scratch. First run `scripts/search_mechanic.py --suggest-tags <keyword>`
  to see which of the ~205 hand-verified mechanic families in
  `analyze_mechanics.py` already cover it — these were built and refined
  over many iterations and are far more precise than a fresh guess. Pull
  the ones that look relevant with `--tags tag1,tag2,...`. **Always check
  results in both roles** — `produce` (cards that DO the thing) and
  `consume` (cards that scale with/reward it) are usually on different
  cards, and a request like "find synergy for X" specifically wants the
  `consume` side, which is easy to forget.

### 2. Cross-check with a raw sweep, and actually review the diff

Even when tags exist, run a raw sweep as a completeness check:

```
python3 scripts/search_mechanic.py --tags <tags> --sweep <keyword> --diff
```

The `--diff` output is sweep hits *not* already covered by the tags — this
is the list to manually read through, one by one. Two outcomes:

- **Noise**: generic words produce a lot of this. E.g. sweeping "hand" +
  "discard" together returns ~100 names, but most are coincidental — a card
  that puts a Pokémon "into your hand" and separately "discards the top
  card of your deck" matches both words without being a hand-discard card
  at all. Expect this and don't report noise as findings.
- **A real gap**: sometimes the sweep finds a genuinely on-mechanic card the
  tags missed because the regex was written too narrowly. This has happened
  before — `discard_own_hand_cost` required "in order to use this Ability"
  or an explicit "N other cards" count, and missed the simpler "Discard a
  card from your hand. If you do, draw 2 cards." phrasing on 4 real cards
  (Klefki, Tropius, Iris's Fighting Spirit, Canari).

When it's a real gap, fix it in `analyze_mechanics.py`: find the family's
regex, widen it precisely enough to catch the new phrasing without pulling
in unrelated cards (check what else the widened pattern would match before
committing to it), then:

```
python3 analyze_mechanics.py   # confirm "Untagged effects with real text" is still 0
python3 audit_mechanics.py     # confirm "Flagged mismatches" is still 0
```

Both must stay at 0 — that's the signal nothing regressed. Only after both
pass, tell the user what was found and fixed (briefly — the fix matters
less to them than the corrected finding).

### 3. Report producers and consumers separately, and flag anti-synergies

Don't blend "cards that inflict X" and "cards that benefit from X" into one
list — they usually play different deckbuilding roles (setup vs. payoff).
While reading through results, actively look for anti-synergies worth
calling out explicitly, not just listing cards: e.g. a card whose text says
"both Active Pokémon" without a type restriction will also hurt the user's
own side if their deck doesn't match the required type. These are easy to
miss by only reading a card in isolation.

### 4. If building a decklist from the findings

Pull real stats directly from `pokemon_standard_cards.json` for every card
that goes in the list — types, HP, retreatCost, evolvesFrom/evolvesTo chain,
exact attack costs and damage. Never state a card's stats or text from
memory; multiple printings of the same name can have different attacks, and
guessing has produced wrong answers before.

Check the Basic Pokémon count before finalizing. A 60-card deck needs a
Basic in the opening 7-card hand or it's a mulligan; run
`scripts/search_mechanic.py --mulligan-table <counts>` to see the actual
odds (hypergeometric: `comb(60-basics, 7) / comb(60, 7)`). Four total Basics
is roughly a 60% mulligan rate — a real, easy-to-miss problem, not
theoretical. Aim for roughly 8-12 total Basics unless the user has a reason
to want fewer.

## Script reference

`scripts/search_mechanic.py` has full `--help` text with all flags and
examples (`--suggest-tags`, `--tags`, `--sweep`, `--sweep-phrase`, `--diff`,
`--kind`/`--stage`/`--type` filters, `--mulligan-table`). Run
`python3 .claude/skills/tcg-theorycraft/scripts/search_mechanic.py --help`
if a flag's exact behavior is unclear rather than guessing at it.
