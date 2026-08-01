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
  sniped. **Correction (see methodology note below):** this entry
  previously flagged `Poké Pad` and `Rosa's Encouragement` as
  `standard: Not Legal`. That was wrong for Poké Pad specifically — it's a
  real, currently Standard-legal card (Regulation Mark J); the flag was a
  data gap in `fetch_pokemon_cards.py` (it filtered the initial fetch by
  the API's own unreliable `legalities.standard` field before the
  regulation-mark safeguard could apply, silently excluding this and
  ~1,140 other currently-legal cards across nearly every set — root-caused
  and fixed). `Rosa's Encouragement` was not re-checked as part of this fix
  and should be verified directly before trusting either claim about it.
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
  **also corrected**: it's real and Standard-legal, see the note on the
  Risky Ruins entry above and the methodology section below for the actual
  root cause (a data-fetch gap, not a rotation issue).
- **Mega Slowbro ex / Dudunsparce bulky-Psychic control deck**
  (user-provided, verified card-by-card) — a wall/attrition build, not a
  combo deck: two big beefy attackers (Mega Slowbro ex, 330 HP; Latias ex,
  210 HP) backed by an unusually heavy stack of three separate healing
  effects (AZ's Tranquility, Jacinthe, Jumbo Ice Cream) and a
  self-sustaining draw engine (Dudunsparce's Run Away Draw — draw 3, then
  shuffle itself back into the deck, so it never gets stranded as a dead
  card and just keeps getting re-evolved into again). Mega Slowbro ex's
  Shellnado Spin is a genuinely new mechanic shape worth naming — a
  **retaliation/vengeance effect**: "during your opponent's next turn, if
  this Pokémon is damaged by an attack (**even if this Pokémon is Knocked
  Out**), place 12 damage counters on the attacker" — so trading into Mega
  Slowbro ex, even for a clean KO, still costs the opponent 120 damage on
  whatever attacked it next. This is a distinct shape from every damage-
  counter-producer in `combo_patterns.md` Pattern 1 (those trigger from the
  player's own actions; this triggers from the *opponent* choosing to
  attack). **Correction**: this file originally said this shape wasn't
  tagged in the taxonomy and floated adding a new tag for it — checked
  `analyze_mechanics.py` directly and it already exists as
  `counterattack_on_hit` (consume role), with 17 members already matched,
  including `Spiky Energy` (a Special Energy granting the identical "even
  if Knocked Out" property to any Pokémon it's attached to) and
  `Bouffalant`'s (Surging Sparks print) Ready to Ram attack, both of which
  showed up in later user-provided decks — so this is a real, recurring
  design shape in the current pool, already correctly covered, not a gap.
  Lesson: check the taxonomy directly (`--suggest-tags` or grep
  `analyze_mechanics.py`'s `FAMILIES`) before asserting something isn't
  tagged, rather than assuming novelty from not having seen the tag name
  before.
  Latias ex's Skyliner
  Ability (all of your Basic Pokémon have no Retreat Cost) is a
  quality-of-life enabler for the whole low-HP-Basic support package
  (Smoochum, Slowpoke, Dunsparce) to reposition freely. Smoochum's
  Delightful Kiss (Free-cost attack, search 2 Basic Psychic Energy and
  attach both to a Benched Pokémon) is another real instance of the
  "energy-search-and-attach as the primary energy plan" pattern already
  logged in the mechanics section below. `Nighttime Mine` (Stadium: "attacks
  used by each Tera Pokémon in play cost Colorless more," both players) is a
  pure meta call — this deck runs no Tera Pokémon of its own, so it's a
  one-sided tax specifically aimed at Tera-line decks, which includes the
  Dragapult ex archetype logged below (`['Stage 2', 'Tera', 'ex']`).
- **Festival Grounds Goldeen "ex-hate toolbox"** (user-provided, verified
  card-by-card) — a distinct third archetype *shape* worth naming alongside
  the combo decks (Wailord ex, Risky Ruins, Mega Zeraora ex) and the
  wall/control decks (Mega Slowbro ex) already logged here: an all-cheap,
  all-non-Rule-Box roster (every Pokémon in the 60 lacks a Rule Box — no
  ex/V/Mega at all) that stacks *multiple, separate* small bonus-damage-vs-
  opponent's-ex/V effects onto those cheap attackers, specifically to punch
  above their weight against the current ex/Mega-ex-saturated meta (every
  other archetype logged in this file is ex or Mega ex). The stack: `Kieran`
  (+30 to opponent's Active ex/V, or a free switch), `Brave Bangle`
  (Pokémon Tool, +30 to opponent's Active ex, non-Rule-Box holder only),
  `Gladion's Final Battle` (+80 to opponent's Active, but only when it's the
  *last card in your hand* — a hand-emptying finisher, non-Rule-Box
  attacker only), and `Shaymin`'s Pinpoint Dive (60 flat snipe damage
  directly to a Benched ex or V, bypassing the Active-only restriction the
  other three share). None of these alone is a real threat to an ex's HP
  total; stacked together on one attack they add up fast. Two other pieces
  worth naming as their own mechanic shapes: **`Festival Grounds` (Stadium)
  + `Goldeen`'s Festival Lead Ability** ("if Festival Grounds is in play,
  this Pokémon may use an attack it has twice; if the first KOs, attack
  again after the opponent's forced switch-in") is an attack-doubling
  combo gated behind a specific Stadium being in play — check for this
  shape (`X may use an attack twice if [Stadium] is in play`) whenever a
  Stadium and a Pokémon's Ability are both in the same decklist rather than
  assuming they're unrelated pieces; and **`Thwackey`'s Boom Boom Groove**
  ("once per turn, if your Active Pokémon has the Festival Lead Ability,
  search your deck for any card") is gated by *Ability name*, not card name
  or type — the same restriction shape as Pattern 2 in `combo_patterns.md`
  (named-family Abilities), just keyed to an Ability's name instead of a
  Pokémon's; worth checking `--suggest-tags` for other Abilities that key
  off a *named Ability* being present rather than a named Pokémon. Also:
  `Genesect`'s ACE Nullifier Ability ("if this Pokémon has a Pokémon Tool
  attached, opponent can't play ACE SPECs") is turned on for free here by
  `Air Balloon` — the deck was already attaching Air Balloon to reduce
  retreat cost, and that single attachment happens to also satisfy
  Genesect's Ability trigger, a two-birds-one-Tool efficiency worth
  checking for whenever a deck runs both a Tool-gated Ability and a
  generically-useful Tool for unrelated reasons.
- **Mega Kangaskhan ex / Cornerstone Ogerpon ex "ex-immunity wall"**
  (user-provided, verified card-by-card) — the defensive mirror of the
  Festival Grounds Goldeen ex-hate toolbox above: instead of dealing bonus
  damage *to* ex/V Pokémon, this deck stacks several separate, narrowly-
  conditioned damage-**prevention** effects to wall out the ex/Mega-ex/
  Ability-heavy current meta entirely. `Cornerstone Mask Ogerpon ex`
  prevents all damage from opponent's Pokémon *that have an Ability* while
  Active, and all damage period while on the Bench. `Crustle`'s Mysterious
  Rock Inn prevents all damage specifically from opponent's Pokémon **ex**.
  Between those two conditions (Ability-havers, and separately all ex's),
  most of the archetypes already logged in this file are walled out
  entirely — everything catalogued above is either ex, Mega ex, or built
  around a named Ability. `Mist Energy` layers on top, blocking attack
  *effects* (not damage — "damage is not an effect" is explicit in its
  text) from landing on whatever it's attached to, covering the residual
  small non-ex non-Ability attackers the two Abilities above don't stop.
  `Spiky Energy` adds the retaliation property described in the Mega
  Slowbro ex entry above to any Pokémon wearing it. `Psyduck`'s Damp
  Ability is a direct, specific counter to the exact "suicide for a
  free-damage-counter burst" shape `Dusknoir`'s Cursed Blast uses (logged
  under the Dragapult ex/Dusknoir entry below) — "Pokémon in play lose any
  Ability that requires the Pokémon using it to Knock Out itself," which
  reads like a narrow rider until you notice it's aimed at a real, currently
  meta-relevant Ability shape. `Dwebble`'s Ascension attack (free-cost,
  search a card this Pokémon evolves from... into, and evolve immediately)
  is a Rare-Candy-shaped effect built into a Basic's own attack line rather
  than a separate Item — a distinct way to skip a turn of waiting on a slow
  evolution line, worth remembering as its own category next to Rare Candy.
  `Mega Kangaskhan ex` is the actual win condition once the wall is up:
  Run Errand draws 2 every turn it's Active, and Rapid-Fire Combo
  (200+ damage, flip until tails, +50 per heads) is an escalating,
  high-variance burst finisher. **Flagging a real arithmetic problem, not
  just a stylistic note**: this decklist as pasted sums to Pokémon 12 +
  Trainer 33 + Energy 13 = **58 cards, not 60** (verified by adding the
  literal copy counts on every line, which do match the section headers
  exactly here — so the headers aren't lying, the list itself is 2 cards
  short of legal). Worth double-checking with the source for what's
  missing before treating this as a complete, playable 60.
- **Mega Kangaskhan ex Colorless-tank squad** (user-provided, verified
  card-by-card) — a bulky-Colorless variant of the wall archetype: three
  big Colorless-*type* ex/Mega attackers (`Mega Kangaskhan ex`, 300 HP;
  `Bloodmoon Ursaluna ex`, 260 HP; `Meowth ex`, 170 HP) protected by two
  stacking layers of passive defense — `Bouffalant` (Stellar Crown print)'s
  Curly Wall Ability (-60 damage to all of your Basic *Colorless* Pokémon,
  once 2+ Bouffalant are in play — the whole attacker trio qualifies) and
  `Lively Stadium` (+30 HP to every Basic Pokémon, both sides, which is
  most of this roster). A genuinely useful, generalizable insight on the
  Energy side: this deck's actual Energy investment is entirely
  **Water** (`Misty's Vitality` search-and-dump-4, `Dewgong`'s Wash Out
  Ability moving Water Energy from Bench to Active "as often as you like"
  each turn) even though its three main attackers' costs are pure
  Colorless — not a mismatch, because Colorless cost accepts *any* Energy
  type. Paired with a repeatable, unrestricted mover like Wash Out, this
  means a single big Water-Energy dump (loaded once via a Supporter) can
  keep re-fueling whichever Colorless attacker rotates into the Active
  Spot next, rather than needing a dedicated Energy line per attacker —
  see the new note added to SKILL.md step 4 on checking this deliberately
  (it's the positive counterpart to the Team Rocket's Articuno gap logged
  below). `Wally's Compassion` fully heals a Mega Evolution Pokémon ex but
  returns all its attached Energy to hand as the cost of doing so — cheap
  to pay off here specifically because Wash Out makes re-fueling trivial.
  `Precious Trolley` (ACE SPEC) dumps any number of Basic Pokémon onto the
  Bench in one shot — a fast way to get the whole Water-line-plus-Bouffalat
  package into play at once. `Special Red Card` is a late-game safety
  valve, usable only once the opponent is down to 3 or fewer Prizes:
  shuffles their hand away and forces a fresh draw-3, denying a built-up
  hand right as they're about to close out a win.
- **Team Rocket's Honchkrow / Porygon2 Supporter-discard deck**
  (user-provided, verified card-by-card) — the whole Pokémon lineup is
  "Team Rocket's ___"-named (all non-Rule-Box), which feeds two different
  scaling attacks off the same resource: `Team Rocket's Honchkrow`'s Rocket
  Feathers discards any number of "Team Rocket"-named Supporters *from
  hand* for 60 damage each (a burst that wants a full hand of them),
  while `Team Rocket's Porygon2`'s R Command does 20 damage per
  "Team Rocket" Supporter already sitting *in the discard pile* (grows
  passively over the game, no hand cost). The deck runs six different named
  "Team Rocket" Supporters (Ariana, Giovanni, Proton, Petrel, Archer) plus
  `Team Rocket's Transceiver` (an Item, so it doesn't compete for the
  1-per-turn Supporter slot) to fetch more of them — and because the whole
  board really is all Team Rocket's Pokémon, `Team Rocket's Ariana`'s "draw
  to 5, or to 8 if your whole board is Team Rocket's Pokémon" clause is
  effectively always the draw-to-8 mode. `Team Rocket's Factory` (Stadium)
  refunds a card draw every time either player plays a "Team Rocket"
  Supporter that turn, and `Roto-Stick` is worth noting as a distinct
  search-Item shape — most "look at top N, take 1" Items cap at a single
  card, but Roto-Stick lets you take *any number* of the Supporters found
  in the top 4. `Miracle Headset` (ACE SPEC) returns up to 2 Supporters from
  the discard pile, which doubles as recursion for whatever Honchkrow just
  dumped. **Real gap found by checking energy-type payability, not just
  count (see SKILL.md step 4)**: `Team Rocket's Articuno`'s Dark Frost
  attack costs Water + Colorless + Colorless, but the deck's only two
  Energy cards are `Team Rocket's Energy` (Psychic/Darkness only, and only
  attaches to Team Rocket's Pokémon) and `Ignition Energy` (Colorless
  only) — there is no Water source anywhere in the 60 cards, so Dark Frost
  can never actually be paid for as built. Articuno's Repelling Veil
  Ability (blocks attack *effects*, not damage, against your Basic Team
  Rocket's Pokémon) still has standalone defensive value against
  status-heavy matchups, so the card isn't dead, but it's an Ability-only
  include here, not a real attacker — worth stating plainly rather than
  assuming every attack line printed on an included card is actually usable.
- **N's Zoroark ex** (August 2026, TCGplayer "Best Decks Right Now" — see
  methodology note below on how this batch was gathered) — a draw-engine
  deck built around N's Zoroark ex's Trade Ability (discard 1 card, draw 2,
  repeatable every turn) for raw consistency, then attacking with Night
  Joker, which borrows an attack from any Benched "N's" Pokémon rather than
  using a kit of its own — see `combo_patterns.md` Pattern 4 for the full
  writeup on why the real payoff is N's Reshiram's damage-counter-scaling
  Powerful Rage or N's Darmanitan's opponent-discard-scaling Back Draft, not
  anything printed on Zoroark ex itself. Supported by Boss's Orders, Cyrano,
  and Lillie's Determination for setup/utility.
- **Slowking** (August 2026, same source) — an unusually low-attack-count
  deck: Slowking's own attack, Seek Inspiration, discards the top deck card
  and borrows its attack if it's a non-Rule-Box Pokémon (`combo_patterns.md`
  Patterns 3 and 4 — the "randomness" can be engineered away with Academy at
  Night). A common tech package pairs Kyurem (Trifrost — discard all its
  Energy for 110 to 3 of the opponent's Pokémon, a mini board wipe) and
  Metagross (Meteor Mash — windup attack, next turn's copy of the same
  attack hits 60 harder) with Drapion and Cofagrigus, both of which deal
  damage to *your own* side as part of their attack/ability (Hazardous Tail,
  Law of the Underworld) — laundered through Munkidori's Adrena-Brain into
  damage on the opponent instead, a second independent real-decklist
  confirmation of the Pattern 1 shape (full writeup in `combo_patterns.md`).
  Crispin fetches the deck's Basic Energy split.
- **Dragapult ex / Dusknoir** (August 2026, same source — an established
  archetype, "hasn't really changed in two years" per the source material) —
  Budew's Itchy Pollen (Free-cost attack, 10 damage, locks the opponent out
  of playing Item cards next turn) opens the game by denying the
  Item-search-heavy setup most current decks rely on (Ultra Ball, Buddy-
  Buddy Poffin, etc.). Dusknoir's Cursed Blast Ability is a suicide-for-
  value effect — it knocks out Dusknoir itself but puts 13 damage counters
  directly on an opponent's Pokémon, bypassing Weakness/Resistance entirely
  since it's counters, not attack damage. Dragapult ex's Phantom Dive (200
  damage to the Active, plus 6 damage counters spread across the opponent's
  Bench in any distribution) turns one attack into a partial board wipe.
  Drakloak's Recon Directive Ability (look at top 2, keep 1) gives this
  evolution line its own card selection before it even reaches Dragapult ex
  — see the "draw/selection built into a mid-evolution stage" mechanics
  note below, which this deck is the original source of.
- **Mega Excadrill ex** (August 2026, same source, described as the newest
  deck on the list) — a Metal toolbox: Genesect ex's Metallic Signal
  Ability searches up to 2 Evolution Metal Pokémon per turn (a targeted,
  type-restricted search staple worth knowing as its own category, distinct
  from Ultra Ball/Buddy-Buddy Poffin's generic/Basic-only search), setting
  up Mega Excadrill ex's Maximum Drilling (200+, "+130 more damage if this
  Pokémon has at least 2 extra Energy attached beyond the attack's cost" —
  an energy-overkill-payoff attack, worth checking for an
  energy-acceleration engine when a deck runs one of these). Metagross
  offsets the deck's own Prize-trade math on a KO (a Stage-2, high-HP body
  worth more Prizes if traded on curve). Mega Skarmory ex's Sonic Ripper
  ("shuffle all Energy attached to this Pokémon into your deck" + 220
  damage) is a build-it-then-detonate attack, similar in shape to Kyurem's
  Trifrost in the Slowking deck above — a repeatable pattern worth naming:
  **an attack that discards/shuffles away all its own attached Energy as
  part of dealing very high damage is a one-shot burst, not a repeatable
  attacker**, and needs a re-energizing plan (or a second attacker to pivot
  to) for the turns after it fires. Fezandipiti ex's Flip the Script
  (draw 3 once per turn, but only if one of your own Pokémon was KO'd last
  opponent turn) is a comeback-mechanic Ability worth remembering as its
  own named category — a payoff specifically for *being behind*, distinct
  from every other draw-support card catalogued so far in this file, all of
  which are unconditional. **Tech note, not a full archetype of its own**:
  the source material also mentions `Blaziken ex` (Seething Spirit Ability —
  once per turn, reattach a Basic Energy from the discard pile to any of
  your Pokémon, verified real) as a partner/answer piece alongside
  Dragapult ex, since it's Fire-type and super-effective against both
  Hydrapple ex and Mega Excadrill ex — a reminder that a deck's *matchup
  answers* are sometimes covered by a completely different deck's tech
  slot rather than needing to be solved from within the archetype itself.
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

### Update: the N's Zoroark ex / Slowking / Dragapult ex-Dusknoir batch above

Gathered the same way, with the same limits, plus one addition: `tcgplayer.com`
is also blocked at the proxy level for `WebFetch` (confirmed with a direct
403 on the specific source article URL the user provided), joining the
domain list above. That means the source article's exact text — including
any real decklists with counts it contains — was never actually read; only
`WebSearch`'s synthesized summaries of it were available, plus this
project's own `pokemon_standard_cards.json` for verifying every card name
and pulling exact ability/attack text. The three archetype names, and every
individual card name attributed to each, were confirmed in the dataset
before being written above; no card *counts* for these three decks were
sourced or recorded, for the same reliability reason as the July 2026 batch.
The specific combo mechanics described (Munkidori laundering Drapion/
Cofagrigus self-damage; the Academy at Night + Seek Inspiration
determinism trick) were derived directly from the verified card texts, not
from the search summaries — the summaries only supplied which named cards
and archetypes to go look up.
