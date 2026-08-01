# Current Standard meta staples (verified snapshot)

Gathered by cross-checking real, named cards from actual July 2026 Standard
tournament results (NAIC 2026 and its Top Cut, via web search summaries)
against `pokemon_standard_cards.json`, one card at a time — every name below
was individually confirmed to exist in the dataset before being included
here. This is a snapshot, not a live feed: re-verify anything time-sensitive
(legality, current meta share) rather than trusting this file blindly as it
ages. See the note at the bottom on how this was gathered and its limits.

## Real, confirmed-current archetypes as of this snapshot

- **Dragapult ex** (Dreepy → Drakloak → Dragapult ex) — the most-played deck
  at NAIC 2026 (highest Top Cut representation), though it didn't win the
  event. Commonly paired with Dudunsparce, Blaziken ex, or Dusknoir. A
  Dragapult ex / Charizard ex variant also performed well, leaning on a
  heavy Arven-style Item-search count (though the specific "Arven" and
  "Technical Machine: Evolution" cards referenced for this variant were not
  found in the current dataset — almost certainly rotated out of Standard
  since they're early Scarlet & Violet-era cards, not a data gap; don't
  reintroduce them without checking current `legalities.standard`).
- **Lillie's Clefairy ex** — won NAIC 2026 (James Kowalski). Pairs with
  Latias ex, Wellspring Mask Ogerpon ex, Fezandipiti ex, and a small
  tech package (Moltres, Chien-Pao, Koraidon ex). Notably uses **Area Zero
  Underdepths** (see below) to run past the normal 5-card Bench limit.
- **Drakloak/Unfezant "Risky Ruins" resilience deck** (user-provided,
  verified card-by-card, not sourced from tournament coverage) — no big
  attacker or ex at all; wins through attrition instead. Full mechanic
  writeup and the general search recipe for finding combos shaped like
  this one are in `references/combo_patterns.md`; the short version: Risky
  Ruins' self-damage-on-bench "drawback" is repurposed twice, once by
  Pidove's Emergency Evolution (auto-evolves once the self-damage brings
  it to exactly 30 HP) and once by Munkidori's Adrena-Brain (launders the
  self-damage onto the opponent instead). Backed by Unfezant's Add On
  (draw 4 for 1 Colorless) as the card-advantage engine and Shaymin's
  Flower Curtain protecting the whole fragile-low-HP-Basic plan from being
  sniped. Two cards in the list as pasted (`Poké Pad`, `Rosa's
  Encouragement`) are flagged `standard: Not Legal` in the dataset — worth
  a legality check before playing this as-is in a sanctioned event.
- **Mega Zeraora ex / Iono's Bellibolt ex burst deck** (user-provided,
  verified card-by-card) — see `references/combo_patterns.md` Pattern 2 for
  the full writeup. Short version: Bellibolt ex's Electric Streamer dumps
  unlimited Lightning Energy per turn onto "Iono's" Pokémon, which Mega
  Zeraora ex's name doesn't qualify for — the deck routes around that with
  Scramble Switch (a generic, unrestricted energy-transfer ACE SPEC),
  moving the whole stockpile onto Zeraora for a single huge Thunderous
  Fist. Real weakness: the combo is gated behind that one ACE SPEC copy,
  and the whole core (Zeraora, Bellibolt ex, Voltorb, Tadbulb) shares a
  Fighting ×2 weakness. `Poké Pad` showed up flagged `Not Legal` here too —
  the second of two different user-provided decklists to include it,
  suggesting whatever list-building source these come from hasn't
  accounted for the current rotation boundary.
- **Team Rocket's Mewtwo ex** — also made Top Cut at NAIC 2026, with at
  least one build adding a single copy of Lillie's Clefairy ex as a tech
  inclusion — a reminder that "counter-tech splashes" (running 1-2 copies
  of an otherwise-unrelated archetype's key card) is a normal, real
  deckbuilding pattern worth considering, not just full archetype mixing.

## Mechanics confirmed real and worth checking for, that hadn't come up before

- **Bench-size expansion.** `Area Zero Underdepths` (Stadium): any player
  with a Tera Pokémon in play can have up to **8** Pokémon on their Bench
  instead of the normal 5 (drops back to 5 if the Tera Pokémon leaves play,
  or when the Stadium itself leaves). Every decklist built in this
  project so far implicitly assumed a 5-Bench cap. When a deck's plan
  wants more simultaneous board presence than 5 allows (a toolbox with many
  1-2 pop-per-attacker copies, a resilience deck recurring lots of small
  Basics), check whether a Tera Pokémon + this Stadium is a real option
  before assuming 5 is a hard ceiling.
- **Draw/selection built into a mid-evolution stage, not just the finisher
  or a bolted-on separate Pokémon.** Drakloak's Ability "Recon Directive"
  (look at top 2 of deck, keep 1, bottom the other) gives the Dragapult ex
  line its own card selection *before* it even reaches its final stage —
  meaning that deck doesn't lean as hard on external draw support as it
  otherwise would. Before assuming a deck needs a bolted-on draw engine
  (Dudunsparce, etc.), check whether any card *already in the planned
  evolution line* has its own draw/selection Ability — it's easy to only
  look at the finisher's kit and miss this on an earlier stage.
- **Energy-search-and-attach Supporters/Items as the primary energy plan,
  not raw energy count.** This pattern showed up independently in both the
  Wailord ex reference deck (Misty's Vitality — search up to 4 Basic Water
  Energy, attach them all to one Pokémon) and here (Crispin — search 2
  different Basic Energy types, keep 1 + attach 1; Wondrous Patch — attach
  Basic Psychic Energy from discard to a Benched Psychic Pokémon). Real
  decks with a steep single-attacker energy cost often run *fewer* total
  Energy cards than a first-pass build would assume, because they fetch a
  chunk directly with one Supporter/Item rather than drawing into it over
  several turns. When a key attack has a high energy cost (4-5+), check for
  a search-and-attach Supporter for that type before defaulting to "just
  run more raw Energy."

## Other real staple Trainers worth knowing as named categories (not just "generic draw/search")

- **Cyrano** (Supporter) — search up to 3 Pokémon ex to hand. An ex-search
  staple distinct from generic Pokémon search (Ultra Ball) or Basic-only
  search (Buddy-Buddy Poffin) — reach for this specifically when a deck's
  attacker lines are ex-heavy.
- **Ciphermaniac's Codebreaking** (Supporter) — search 2 cards, put them on
  top of the deck in chosen order. This is deck-*stacking*, not draw — it
  sets up the next 2 draws rather than drawing immediately. A distinct
  category from both "draw power" and "search to hand," worth considering
  when a deck wants to guarantee its next 1-2 topdecks rather than dig
  through the whole deck right now.
- **Lillie's Pearl** (Pokémon Tool) — prize-denial specifically for
  "Lillie's ___"-named Pokémon (1 fewer Prize given up on KO). A reminder
  that named-family restricted Tools are a real card pattern — check
  whether a deck's key Pokémon shares a name-prefix family before assuming
  a generic Tool is the only option.
- **Prime Catcher** (ACE SPEC Item) — switches *both* players' Active
  Pokémon simultaneously (gust the opponent's target up, reposition your
  own). A stronger, ACE-SPEC-gated version of a plain gust effect — worth
  knowing exists even though the 1-ACE-SPEC-per-deck rule means it competes
  with other ACE SPECs already catalogued in this project (Hero's Cape,
  Secret Box, Enriching Energy, etc.).
- **Dusk Ball** (Item) — searches the *bottom* 7 cards of the deck for a
  Pokémon, rather than the whole deck (Ultra Ball) or a Basic-only subset
  (Buddy-Buddy Poffin). A real, distinct search-Item variant.

## How this file was built, and its limits

Built under a 2-hour timebox with `WebSearch` as the *only* working web
access — `WebFetch` and direct `curl` to every tested domain (including
`limitlesstcg.com`, `pokemoncard.io`, `pokemon.com`, `bulbapedia.bulbagarden.net`)
returned a 403 from this session's egress proxy (a policy denial, confirmed
via `$HTTPS_PROXY/__agentproxy/status`'s `recentRelayFailures`, not a
transient or fixable error — per the proxy's own README, that class of
failure should be reported, not routed around). That ruled out the original
plan of fetching literal top-5 decklists from many individual tournament
pages.

`WebSearch` still works and returns synthesized summaries, but those
summaries are not reliable on their own — one decklist summary it returned
had a Pokémon-count header that didn't match its own listed contents (said
22, listed 14), a clear sign of transcription/synthesis error somewhere in
the pipeline. **Every single card name in this file was individually
verified against `pokemon_standard_cards.json` before being included** —
that's what makes the content above trustworthy despite the summary that
produced it not being. Card *counts* in a specific decklist (how many
copies of X) were not verified to the same standard and are deliberately
omitted from this file for exactly that reason — only names, roles, and
confirmed-real mechanics are recorded.

If full-page web access becomes available in a future session, the next
useful expansion here is literal top-5-per-tournament decklists with exact
counts, which this pass could not get to reliably.
