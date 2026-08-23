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

**Every full deck-build request runs every step below, in order, explicitly
— not just the ones that feel relevant to a fast answer.** Standing user
instruction: when asked for a deck, check every one of these rules, even if
it takes longer. Speed is not the priority on a full build; a clean result
on only some of the checks is not the same as a clean result. Concretely,
before presenting a finished decklist, confirm out loud (briefly, one line
each is fine) that each of the following actually happened for this build,
not just that it usually happens:

1. Searched via tags or sweep-phrase (step 1), checking **both** produce and
   consume roles, not just one. **The results already include every
   supertype — Pokémon, Trainer, and Energy together, not a separate
   pass per card type** — but that only helps if the full result list gets
   re-checked against the *final* build, not just skimmed once at the start.
   Real miss: a `counterattack_on_hit` search surfaced `Deluxe Bomb` (a
   universal, no-type-restriction ACE SPEC Tool doing more damage per hit
   than anything else in the family) in the very first query of a session,
   it got used in one deck built from that search, and then silently
   dropped from a *second*, later deck built from the same mechanic —
   caught only when asked directly whether the Trainer/Item/Stadium/Energy
   side gets the same scrutiny as the Pokémon side. It doesn't, by default:
   the generic support shell (Ultra Ball, Boss's Orders, Switch, Air
   Balloon, Night Stretcher, Lillie's Determination, Judge, Rescue Board)
   gets pulled from a rotation of previously-used staples out of habit, not
   from re-running the mechanic search against this specific build. Before
   finalizing any deck, re-scan the *original* tag-search output
   specifically for Trainer/Energy entries and check each one against the
   list actually being built, even if that search happened earlier in the
   same conversation for a different deck.
2. Ran the raw-sweep `--diff` (step 2) and manually triaged every hit —
   fixed `analyze_mechanics.py` if a real gap turned up, and re-confirmed
   both `python3 analyze_mechanics.py` and `python3 audit_mechanics.py`
   report 0 before moving on.
3. Reported producers and consumers separately and checked for
   anti-synergies (step 3).
4. Pulled every included card's real stats from the JSON, never memory,
   checked the Basic count against the mulligan math, checked every
   attacker's energy-*type* payability (not just total count) with
   `check_energy_support.py`, checked every Ability line for an
   attack-gating clause, and put an exact `SET NUM` on every card line,
   Trainers and Energy included (step 4).
5. Walked the actual turn sequence for the deck's core combo/game plan
   (step 5) — retreat/evolve clearing Special Conditions, one attack per
   turn, Rare Candy's same-turn restriction, and named the opponent's real
   out at each turn boundary rather than presenting the plan as more
   reliable than it is. This applies to any strategy writeup for the deck,
   not only the initial build.
6. For any card with a self-inflicted drawback, searched every mechanical
   *shape* of fix (immunity, switch-not-retreat, flat cost reduction, etc.),
   not just the first one found (step 6).
7. Cross-checked against a real published decklist via web search when
   available, and verified every card name it returned against the JSON
   before trusting it (step 7).
8. Checked `references/current_meta_staples.md` for a known real support
   card or precedent before assuming one doesn't exist (step 8).
9. Actively checked whether any included drawback card has a hidden
   "drawback as enabler" combo partner in the pool, not only when handed a
   decklist that already demonstrates one (step 9).
10. Ran a 1000-trial baseline development-timing simulation with
    `scripts/simulate_baseline.py` and reported the results (step 10) —
    every time a finished decklist is delivered, not only when explicitly
    asked to "test" it.
11. Where a real opponent decklist is available, played it head-to-head
    with `scripts/simulate_versus.py` and reported the win rate along
    with that tool's own list of unmodeled cards (step 11).

Skipping a step because the deck's theme seems simple or narrow is exactly
the situation this list exists to catch — a narrow-seeming theme is often
where a single missed card (an energy-payability gap, an Ability gate, a
Rare Candy timing error) does the most damage, precisely because there's
less redundancy to fall back on.

### 1. Classify the ask: named mechanic, or general concept?

- **A specific named Ability/attack** (e.g. "Hide 'n' Sneak", "Tighten Up"):
  run `scripts/search_mechanic.py --sweep-phrase "<exact name>"`. This
  searches both the ability/attack's own name field *and* every card's body
  text in one pass, so it catches both the cards that HAVE it and the cards
  that reference it by name as a scaling condition. This is usually enough
  on its own for a named mechanic — the phrase is specific enough that noise
  is rare.

- **A named *family* of Pokémon** (e.g. "is there other support for the
  Hop's/Steven's/Ethan's cards?"): searching Trainer cards for the family's
  own name prefix is **not enough** — a support card that boosts or
  protects a named family very often doesn't carry that family's name
  itself. `Postwick` (Stadium, +30 damage to Hop's Pokémon) and
  `Granite Cave` (Stadium, -30 damage taken by Steven's Pokémon) both prove
  this: neither has "Hop's" or "Steven's" anywhere in its own name, only in
  its effect text. A real miss happened here — a Steven's-family deck was
  built and confidently described as having "no equivalent to Postwick,"
  when Granite Cave existed in the pool the whole time and was found only
  because the user pushed back and asked to search for the *effect*
  (similar damage-reduction text) rather than trust the name-prefix search
  that had already run. Search by **effect text mentioning the family name**
  (`--sweep-phrase "Steven's Pokémon"`, `--sweep-phrase "Hop's Pokémon"`,
  etc.) in addition to a name-prefix search before concluding a themed
  family has no supporting cast.

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

Also check that every attacker's energy *type* cost, not just the total
count, is actually payable by what the Energy line provides. Counting total
Energy cards isn't enough — a deck can have "8 Energy" and still be unable
to pay a specific attack if none of them are the right type. Real example:
a user-provided Team Rocket's deck ran `Team Rocket's Articuno`, whose Dark
Frost attack costs Water + Colorless + Colorless, but the deck's only two
Energy cards were `Team Rocket's Energy` (provides Psychic/Darkness only,
and only attaches to Team Rocket's Pokémon) and `Ignition Energy` (provides
Colorless only) — zero Water anywhere in the 60 cards, so that attack is
literally uncastable as built. Read every attacker's attack cost against
the *specific types* the deck's Energy cards actually provide (checking
Special Energy text carefully — many restrict which type(s) they produce,
or which Pokémon they can attach to) before assuming a Pokémon is a
functional attacker rather than an Ability-only or dead include.

The flip side of this check is also real and worth recognizing when it
works rather than only flagging when it doesn't: an attacker whose cost is
entirely **Colorless** accepts *any* Energy type, so a deck's Energy plan
doesn't have to nominally "match" its attackers' type at all. A
user-provided deck ran a Water-Energy-heavy support package (`Misty's
Vitality`, `Dewgong`'s repeatable Wash Out Ability moving Water Energy from
Bench to Active) feeding a trio of Colorless-type ex/Mega attackers (`Mega
Kangaskhan ex`, `Bloodmoon Ursaluna ex`, `Meowth ex`) whose attack costs are
pure Colorless — a real, working plan, not a mismatch, precisely because
Colorless cost doesn't care what type pays it. Combined with a repeatable,
unrestricted Energy-mover like Wash Out, this means a single big Energy
investment (loaded via one Supporter) can keep re-fueling whichever
Colorless-cost attacker rotates into the Active Spot next, rather than
needing its own dedicated Energy line per attacker. When auditing energy
type-payability, check whether the attack cost is Colorless-only before
concluding a color mismatch is a real problem.

Also check every Pokémon's **Ability line**, not just its attack text, for
a condition that gates whether it can attack *at all* — this is a separate
check from energy-payability and easy to skip once the attack cost itself
looks clean. Real example: a from-scratch build included `Team Rocket's
Mewtwo ex` on the strength of its attack (Erasure Ball, a clean 160+ with
no restriction in the attack text itself) without noticing its Ability,
Power Saver: "This Pokémon can't attack unless you have 4 or more Team
Rocket's Pokémon in play." None of the deck's other four Pokémon were
Team Rocket's-named, so the card could never attack at all — caught only
when asked directly to double-check it, not by the original build process.
Read the full card (abilities *and* attacks together) before concluding a
Pokémon is a working attacker, the same discipline already applied to
energy costs above.

**Both of the checks above are now automated** — run
`scripts/check_energy_support.py <decklist file>` (or `-` to read from
stdin) against any finished or user-provided decklist before writing the
review up. It parses the same plain-text decklist format used throughout
this project, cross-references every attacker's attack cost against the
deck's actual Energy-by-type supply (flagging `IMPOSSIBLE` when a type's
total supply is below what a single attack needs simultaneously attached,
and `TIGHT` when supply exactly equals the requirement with no spare
copies), and separately scans every included Pokémon's Ability text for
"can't attack unless..."-style gating language. It caught the Team
Rocket's Articuno, Bastiodon, and Team Rocket's Mewtwo ex cases above
correctly in testing. It matches cards by name only (pooling every
printing's attacks together), so a clean result means "no red flag found
among known printings," not an ironclad guarantee — still worth a manual
skim on anything it flags as borderline.

**It also checks basic deck-construction legality**: total card count is
60, no non-Basic-Energy card exceeds the real 4-copies-per-name limit, and
combined ACE SPEC count across the whole deck is at most 1. Real failure
that motivated adding this: a from-scratch build ran 5 copies of Rhyhorn —
caught only because the user asked "how can there be 5 Rhyhorn," not by the
build process itself, even though every other check (energy payability,
Ability gating, mulligan math) had already run cleanly. The 4-copy limit is
more fundamental than any of those checks and was never being verified at
all before this. Run this check on every finished decklist same as the
others — it's cheap and fully deterministic, there's no reason for this
exact mistake to happen twice.

When outputting a decklist in Pokémon TCG Live's plain-text import format,
**every card line needs an exact `SET NUM` pair, not just the Pokémon
section.** Real failure: a from-scratch build listed Trainer and Energy
cards by bare name only (`4 Ultra Ball`, `14 Darkness Energy`) while the
Pokémon section correctly had set codes — the user reported the import
partially failed, Pokémon matched but nothing else did. PTCGL's importer
apparently can't resolve a Trainer/Supporter/Item card (many of which have
multiple reprints) from name alone the way this project's own
`check_energy_support.py` can. Basic Energy is the one exception — write it
as `14 Basic Darkness Energy` with no set code, matching every previously
working decklist in `decks/`. Look up each Trainer's real `(ptcgoCode,
number)` from `pokemon_standard_cards.json` before finalizing any decklist
meant to be pasted into the actual client, the same discipline already
applied to Pokémon.

### 4b. A missing SET NUM in this repo's index is NOT proof the user is wrong

`pokemon_standard_cards.json` is a Standard-legal **snapshot carrying one
printing per card**, not a complete set list. Every set in it has real
gaps: SFA holds 59 of 66 numbers, TWM 164 of 226, ASC 209 of 289. So when
a user-supplied `SET NUM` does not resolve, there are two possible causes
and they look identical from the index:

1. the user's number is genuinely wrong, or
2. the number is right and this pool just carries a different printing.

Near-miss that motivated writing this down: a user-provided Luxray deck
was checked against the index and **eight** of its lines came back
"mismatch" — `Fezandipiti ex SFA 38`, `Luxray ex TWM 68`, `Battle Cage
PFL 85`, `Night Stretcher ASC 196`, `Buddy-Buddy Poffin ASC 184`, `Boss's
Orders ASC 183`, `Air Balloon ASC 181`, `Rare Candy PAF 89`. Reporting
that list would have been seven false accusations. **Exactly one was
real.**

Before calling any `SET NUM` wrong, run these two checks:

- **Neighbour check.** Print the pool's cards at the surrounding numbers
  in that set. Pokémon are numbered by evolution line and Trainers
  alphabetically, so the gap's identity is usually inferable. `TWM 66
  Shinx / 67 Luxio / [68 gap] / 69 Emolga` puts Luxray ex at exactly 68 —
  the user was right. `ASC 182 Anthea & Concordia / [183, 184 gaps] / 185
  Canari` is precisely where "Boss's Orders" and "Buddy-Buddy Poffin"
  sort — both right. `SFA 36 Okidogi ex / 37 Munkidori ex / [38 gap] / 39
  Pecharunt ex` is the loyal-three block, so Fezandipiti ex 38 is right.
- **Set-legality check.** Is the set code in the pool's set list at all?
  Every card in this pool is regulation mark **H, I or J**. `PAF`
  (Paldean Fates) appears nowhere, so `Rare Candy PAF 89` is the one
  genuine problem in that list — not a typo, a **rotated card**. That is
  the failure worth reporting, and it is a different and more serious one
  than a wrong number.

Report a number as wrong only when both checks fail. When the pool simply
lacks a printing, say so plainly ("this pool carries MEG 173; your ASC 196
is a reprint it doesn't list") instead of correcting the user.

### 5. Walk the actual turn sequence before calling a combo reliable

Listing synergistic cards is not the same as verifying they combo the way
they look like they should. A combo that spans more than one turn gives the
opponent a turn in between to react, and several ordinary game rules quietly
break "setup this turn, cash in next turn" plans if they aren't accounted
for.

**This checklist applies every time a combo or play sequence gets described,
not only while a decklist is first being built.** A real failure: this exact
checklist already correctly listed "retreating cures every Special
Condition" and "only the Active Pokémon attacks, once per turn," but a later
message writing up *how to play* an already-finished deck (not building one)
re-derived a rules claim from memory instead of re-checking this list first,
and stated the opposite — that Burn/Poison survive a retreat to the bench.
The gap wasn't missing knowledge; it was treating "explain the strategy" as
a lighter task than "build the decklist" and skipping the checklist because
of that framing. Re-run this same list before writing any turn-by-turn
strategy explanation, matchup note, or "here's how to pilot this" writeup,
exactly as rigorously as when the decklist itself was assembled.

- **Retreating cures every Special Condition** on the Pokémon that retreats.
  If a combo relies on Poisoned/Confused/Burned/etc. still being present on
  the *following* turn, and nothing prevents the opponent from retreating in
  between, the setup is undone for the cost of their retreat. This is exactly
  what happened when a "Arbok applies 3 conditions, then Muk cashes in next
  turn" plan was first proposed for a Team Rocket deck — it looked clean but
  had a free escape hatch until the sequence was corrected to route through
  Muk's own Gooped Up (which both re-applies a condition *and* locks the
  opponent's retreat for their next turn) before the payoff attack, closing
  most of the window.
- **Evolving also cures Special Conditions** (unless something explicitly
  overrides it, e.g. a card like Dizzying Valley).
- **Only the Active Pokémon attacks, once per turn** — a combo that needs
  Pokémon A to set up and Pokémon B to cash in takes at least two of your
  turns minimum, with an opponent turn in between each. Count the turns
  explicitly rather than describing the combo as if it happens all at once.
- Some conditions self-resolve on their own timeline regardless of anything
  else (Paralyzed clears automatically at the end of the affected player's
  next turn; Asleep requires a coin-flip check each Checkup) — factor this in
  if a combo's timing is tight.
- **Rare Candy can't be used on a Basic Pokémon that was put into play that
  same turn**, and can't be used during your first turn at all — checked
  directly against the card's own text, not assumed. A "play a Basic and
  Rare Candy it straight to Stage 2 the same turn" plan is illegal; the
  Basic has to have already survived to the start of a turn before Rare
  Candy can target it, meaning a from-scratch Rare Candy rush is two turns
  minimum (play the Basic on turn N, Rare Candy it on turn N+1), not one.
  This exact mistake made it into an earlier version of a real combo
  writeup in this skill (a Basic-to-Stage-2 "redeploy" loop) before being
  caught and corrected — worth narrating out loud as its own turn-count
  check whenever a plan leans on Rare Candy for speed.

Before presenting a multi-turn combo as the deck's game plan, narrate it as
actual turns ("your turn N: X. opponent's turn: can they escape here? your
turn N+1: Y.") and explicitly ask, at each opponent turn in between, "what
can they do right now to get out of this." If there's a real window, say so
plainly rather than presenting the combo as more reliable than it is — a
strong combo with a known, disclosed soft spot is a fine, honest answer, and
usually still worth playing; the point is to know it's there rather than
build the whole game plan on an assumption that doesn't survive the
opponent taking a turn.

### 6. When a card has a self-inflicted drawback, search *every* category of fix, not just the first one

A card that hurts itself to do something big (self-damage, self-status,
a brutal retreat cost) usually has more than one real answer in the pool,
and they're mechanically different from each other — finding one doesn't
mean the search is done. This showed up concretely with Wailord ex: its
Falling Down attack does 270 damage but puts *itself* to Sleep, and it
has a 4-cost retreat on top of that. The instinct was to search for
"retreat cost reduction" and stop there. The real decklist for that
Pokémon stacked *three* different answers to the same problem:

- **Immunity effects** — Bubbly Water Energy grants the holder immunity to
  Special Conditions, which can stop the self-inflicted Sleep from landing
  at all if it's already attached. This is the most elegant fix and the
  easiest one to miss, because it doesn't read like a "retreat" card at
  all — check Special Energy and Tool text for "immune to Special
  Conditions" / "can't be [Poisoned/Confused/Asleep/etc.]" whenever a
  self-status drawback is in play.
- **Switch-not-retreat effects** — Surfing Beach (Stadium) lets a Water
  Pokémon swap Active/Bench for free, once per turn each side. It cures
  Sleep the same way retreating does (leaving Active clears Special
  Conditions), but it isn't a retreat, so a "no retreat cost" or "retreat
  cost reduction" keyword search never finds it. Search for "switch...
  Active...Benched" phrasing separately when the goal is "get this
  Pokémon out of the Active Spot," not just "reduce its retreat cost."
- **Flat retreat-cost tools** — the obvious category (Air Balloon, Rescue
  Board, etc.), and worth double-checking with more than one regex pass:
  an ad hoc search for `retreat cost.{0,20}(is|are|becomes).{0,10}(0|Colorless)`
  missed Air Balloon's own text ("Retreat Cost of the Pokémon this card
  **is attached to is** Colorless less") because the intervening clause
  pushed the second "is" outside the character window. If a search for a
  very common, expected card type (retreat tools are a real, well-known
  category) comes back thin or empty, that's a signal to check the search
  itself before concluding the category doesn't exist in the pool.

The general version of this: when hunting for "how do I solve problem X,"
enumerate the different mechanical *shapes* an answer could take (prevent
it, cure it, bypass it via a different game action, reduce its cost) and
search each shape separately, rather than stopping at the first phrasing
that comes to mind.

### 7. Self-validate against real published decklists when possible

The clearest signal that a generated decklist has blind spots doesn't come
from re-reading the same search results harder — it comes from comparing
against a real, currently-played decklist for the same key card(s). When
`WebSearch`/`WebFetch` are available, use them proactively for this rather
than waiting to be handed a decklist to compare against:

1. After building a decklist around specific key Pokémon, search the web
   for real decklists featuring the same cards — Limitless TCG
   (limitlesstcg.com/decks) is the best target, since it indexes real
   tournament and meta decklists with full card lists. A query like
   `site:limitlesstcg.com <Pokémon name> deck` or searching the deck
   archetype name directly usually works.
   **Caveat learned the hard way**: `WebFetch`/direct `curl` to
   limitlesstcg.com (and every other general web domain tested) returned a
   403 policy denial from this session's egress proxy, not a fetchable
   page — check `$HTTPS_PROXY/__agentproxy/status` for
   `recentRelayFailures` before assuming a fetch failure is fixable, and
   don't retry a host that's actually blocked by policy. `WebSearch` still
   works when direct fetch doesn't, but its summaries can contain real
   errors (a decklist summary once had a Pokémon-count header that didn't
   match its own listed contents) — **verify every card name it returns
   against `pokemon_standard_cards.json` individually before trusting
   any of it**, and don't trust card *counts* from a search summary to the
   same standard as card *names*, since names are far easier to verify.
2. Compare card-by-card against the generated list. Don't just note *that*
   something differs — work out *why* the search missed it: was it a
   category of fix not considered (see step 6), a regex that didn't reach
   far enough, a card whose role wasn't obvious from its text alone (e.g.
   Misty's Vitality's "search 4 Energy and attach them" reads as a generic
   Supporter until you connect it to a specific attack's steep energy
   cost), or a card search that was never run at all (searching only
   within the key Pokémon's own kit instead of also looking for standalone
   tech answers, like Moltres's anti-ex attack, that don't reference the
   deck's theme in their own text)?
3. Treat a real, systematic gap (not a one-off stylistic difference — real
   decks vary and there's rarely one "correct" 60) as material to fold
   back into this file or into `analyze_mechanics.py`, the same way a
   taxonomy gap found via the raw-sweep diff in step 2 gets fixed rather
   than just noted once and forgotten.
4. Be honest about the limits of this check: web search results can be
   outdated, Expanded/other-format lists, or just one valid build among
   several — the point is to catch a systematic blind spot in the search
   process (a whole category of card being missed), not to treat someone
   else's exact 60 as ground truth to copy.

### 8. Check `references/current_meta_staples.md` before assuming a support card doesn't exist

This file catalogs real, individually-verified staple cards and mechanics
found by cross-checking actual July 2026 tournament results against the
dataset (see the file for exactly how and its limits). It's a snapshot, not
a live feed — re-verify anything time-sensitive rather than trusting it
blindly as it ages, and treat it as a set of leads to check against the
data, not as ground truth on its own. Notable standing lessons already in
there: some decks legitimately run more than 5 Pokémon on the Bench (Area
Zero Underdepths + a Tera Pokémon raises the cap to 8 — worth checking
before assuming 5 is a hard ceiling), a key Pokémon's own evolution line
sometimes already has draw/selection built in (check before assuming a
bolted-on draw engine is needed), and several real decks run *fewer* total
Energy cards than a first-pass build would suggest because they lean on
search-and-attach Supporters/Items for their steep-cost attacks rather than
raw draw-and-attach over several turns.

### 9. Actively hunt for "drawback as enabler" combos, not just when handed a decklist

A card whose own text reads as a downside — self-damage, a self-inflicted
Special Condition, a Bench/HP restriction, a resource cost — is worth
checking against every *other* card whose trigger condition that exact
downside could satisfy, proactively, not just when a real decklist
happens to demonstrate the combo. This is a distinct skill from steps 1-2
(finding cards *for* a named mechanic): it's finding a mechanic's hidden
*consumer* by starting from something that looks like it has none.

This showed up concretely with `Risky Ruins` (a Stadium that deals 20 free
self-damage to your own newly-benched Basic Pokémon, no attack required) —
it reads as pure downside until cross-referenced against `emergency_evolve_low_hp`
(Pidove's HP hits exactly 30 after the damage, triggering a free instant
evolution) and `transfer_damage_to_opponent` (Munkidori's Adrena-Brain
launders the "wasted" self-damage onto the opponent instead). Both
individual tags already existed correctly in the taxonomy — the missing
step was treating a drawback-looking card as worth the cross-reference at
all, and then actually running `--tags` with the produce tag alongside
candidate consume tags in one call to see them side by side.

Full worked example, the general search recipe (keyword-to-tag-shape
mapping, the "verify the actual numbers, don't assume a tag match is a
confirmed combo" caveat, and checking for sibling members of a small
consume family before treating the first match as the only answer) live in
`references/combo_patterns.md` — read that before starting this kind of
search rather than re-deriving the recipe each time.

### 10. Run a 1000-trial baseline simulation on every finished decklist

`scripts/simulate_baseline.py <decklist file> [trial count] [--verbose]`
runs a deck-agnostic development-timing simulation — it builds its
Pokemon model (stage, evolvesFrom, HP, retreat, types, attacks) straight
from `pokemon_standard_cards.json` for whatever decklist it's handed, so
it works on any build without hand-coding each deck's Pokemon data. It
reports, per Pokémon: what fraction of 1000 opening hands have it in play
by turn 6 and the average turn that happens, plus first-attack timing and
average final hand size at turn 6.

Run this **every time a finished decklist is delivered**, the same
standing requirement as `check_energy_support.py` in step 4 — not only
when the user explicitly asks to "test" or "simulate" the deck. It
answers a different question than the energy/construction checks: not
"can this deck legally do what it claims," but "how fast does it actually
assemble in practice." A deck can pass every legality and payability
check and still turn out to come online too slowly to be worth playing —
this is the check that catches that, quantitatively rather than by feel.

Two stated limitations, matching `simulate_match.py`'s own disclosed
simplifications: no retreating is modeled (so only whatever ends up
Active on turn 1, or what it evolves into, ever attacks in a given
playthrough) and no opponent is modeled (so it measures development
speed, not win rate). Energy type-correctness isn't re-checked here
either — that's `check_energy_support.py`'s job, already covered by step
4. Trainer/Item/Supporter effects are modeled through a hand-authored
registry covering this project's actual staples (Lillie's Determination,
Ultra Ball, Buddy-Buddy Poffin, Poké Pad, Night Stretcher, Energy Search,
Rare Candy, Team Rocket's Petrel, Janine's Secret Art, plus opponent-only
cards like Boss's Orders correctly left un-simulated since they don't
affect any reported metric); a card outside that registry is simply held
in hand rather than misplayed, and the script's own report lists every
such name it hit so a real coverage gap is visible, not silent — extend
the registry in the script when a new staple shows up often enough to be
worth modeling properly, the same way `analyze_mechanics.py` gets
extended when a raw-sweep diff turns up a real taxonomy gap.

### 11. Test against a real opponent deck with `simulate_versus.py`

`scripts/simulate_versus.py <deckA> <deckB> [games] [--verbose]` plays full
games between **any two decklists** and reports a win rate. Unlike the
baseline sim it models knockouts, Prize cards (2 for an ex, 3 for a Mega
Evolution ex, read from the card's own rules text), Weakness, type-correct
Energy payment, retreating, and win conditions. Use it whenever the user
supplies a real meta decklist, or asks "how does this do against X" --
step 10's baseline sim answers "how fast does it assemble," this answers
"does it actually beat that deck."

Both sims share `scripts/tcg_model.py`, which owns decklist parsing, card
resolution by exact SET NUM, and the **Ability parser**. That parser was
built by enumerating every draw Ability in the pool (18 of them) and
asserting the parsed output for each -- run `python3 tcg_model.py` to
re-run those assertions after any change to it. Modeling Abilities matters
more than it sounds: before they were modeled at all, a user's
Alakazam deck (whose attack does 20 damage per card in hand) simulated at
an average hand of 4.95, versus 13.5 once Abilities and the relevant
search Supporters were wired in -- the difference between reading that
deck as a ~99-damage attacker and a ~270-damage one.

Both tools report their own gaps rather than hiding them: Trainers with no
modeled effect, attacks whose text could not be turned into a damage
number, and cards matched by name only. **Read those lines before
trusting a number** -- a deck that leans on an unmodeled card is being
undervalued, and saying so is part of reporting the result.

### 12. Use `search_mechanic.py --help` instead of guessing a flag's behavior

`scripts/search_mechanic.py` has full `--help` text with all flags and
examples (`--suggest-tags`, `--tags`, `--sweep`, `--sweep-phrase`, `--diff`,
`--kind`/`--stage`/`--type` filters, `--mulligan-table`). Run
`python3 .claude/skills/tcg-theorycraft/scripts/search_mechanic.py --help`
if a flag's exact behavior is unclear rather than guessing at it.
