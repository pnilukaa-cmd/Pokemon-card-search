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
- **Mega Zeraora ex "energy burst" build, no Iono's-Bellibolt bridge**
  (user-provided, verified card-by-card) — a second, independent real deck
  reaching for the same Thunderous Fist payoff as the entry above (60
  damage per Lightning Energy attached, for a 1-Energy attack cost), but
  fueling it a completely different way — no Iono's Bellibolt ex, no
  Scramble Switch, just direct energy-dumping. `Magneton`'s Overvolt
  Discharge attaches up to 3 Basic Energy from the discard pile to any
  Lightning Pokémon in one shot, at the cost of KO'ing Magneton itself —
  the deck runs 3 copies specifically to get multiple activations, backed
  by `Explorer's Guidance` and `Canari` (whose own discard costs help seed
  the discard pile with Basic Energy for Magneton to later grab). Cinderace's
  Turbo Flare is a second, independent burst-loader (search 3 Basic Energy,
  attach to a Benched Pokémon) that doesn't need discard-pile setup at all.
  Worth generalizing: when a "per-Energy-attached" scaling attack shows up,
  check for *multiple different* burst-loading pieces rather than assuming
  one Supporter/Ability is the whole plan — this deck stacks at least three
  independent loaders (Magneton, Cinderace, `Powerglass`'s slow 1-per-turn
  trickle). `Voltaic Lightning Energy` is worth flagging as a real
  "double-dip" Special Energy: it counts as a Lightning Energy for
  Thunderous Fist's per-Energy multiplier *and* separately adds a flat +20
  to whatever attacks off it — when checking a scaling attack's Energy
  count, verify whether any attached Special Energy is also stacking a flat
  bonus on top, not just contributing to the count. `Hero's Cape` (ACE
  SPEC, +100 HP) protects the single big investment (Zeraora ex, 270→370
  HP) from being sniped down before it unloads. `Cinderace`'s Explosiveness
  Ability is a distinct setup-time mechanic worth remembering exists: its
  text allows putting it face-down in the Active Spot during setup while
  still in hand, bypassing the normal Basic-Pokémon-only opening-Active
  rule — quote the exact wording rather than assuming how it resolves if
  this comes up again, since it's an unusual enough interaction to double
  check against current rulings before relying on it.
- **Six-deck batch (Wailord ex, Relicanth, Rampardos ex, Vikavolt, Slowbro,
  Lurantis ex)** — all user-provided, all verified card-by-card, all
  clean at 60/60 with no illegal counts. A few standout, exact-number
  findings worth remembering as reusable checks:
  - `Heavy Baton` requires the holder to have a Retreat Cost of *exactly*
    4, be Active, and get Knocked Out by an opponent's attack, to salvage
    3 Basic Energy onto the bench. `Wailord ex`'s retreat cost is exactly
    4 — checked, not assumed — so this is a real, precisely-tuned
    insurance policy for a deck that invests 3-5 Water Energy per swing.
  - `Antique Skull Fossil`'s Spiny Skull Ability is a **fourth** independent
    real-decklist instance of the `counterattack_on_hit`/"retaliate even
    through a KO" family (after Mega Slowbro ex's Shellnado Spin,
    Bouffalant's Ready to Ram, and Spiky Energy) — this shape is
    thoroughly confirmed as a real, recurring design pattern in the
    current pool, not a rarity.
  - `Vikavolt` (PBL print, `me5-26`)'s Giga Railgun (260 damage, 2
    Lightning) is a hard on/off gate, not a scaling bonus: "If this
    Pokémon has no Voltaic Lightning Energy attached, this attack does
    nothing" — worth distinguishing from scaling attacks when auditing an
    energy line, since the deck needs *at least one* specific Special
    Energy, not just "more energy is better."
  - `Slowbro`'s All Out (50+, "+160 more damage if you have no cards in
    hand") is a third independent instance of "empty hand as a resource
    state, not just a risk" — alongside `Gladion's Final Battle` (usable
    only as your last card) and `Cassiopeia` (usable only as your last
    card) already logged elsewhere in this project. Already correctly
    tagged in the taxonomy (`damage_scales_with_own_hand_size`), no gap —
    worth actively checking for a hand-dumping Trainer suite (multiple
    Ultra Ball/Poké Pad/Buddy-Buddy Poffin copies) as a *deliberate* setup
    for this kind of attack rather than assuming a thin hand is accidental.
  - `Lurantis ex`'s Lively Cutter (60+, "+200 more damage if this Pokémon
    was healed this turn") pairs with `Community Center` (Stadium: heal 10
    from every one of your Pokémon once per turn, if you played a
    Supporter that turn) in the same decklist — a real combo shape, but
    flagged as worth double-checking against actual rulings rather than
    assumed: it's not fully certain from text alone whether a 0-effect
    heal (Lurantis ex already at full HP) still counts as "was healed"
    for Lively Cutter's trigger, the same category of edge case as
    Cinderace's Explosiveness Ability logged earlier in this file.
- **Fossil "mass-evolve" toolbox** (user-provided, verified card-by-card
  — one real discrepancy found: `Reuniclus PR-SV 212` doesn't match any of
  the 11 real Reuniclus printings checked live against the API, none of
  which are from a `svp`/PR-SV promo set at all; the deck's other cards
  (`Duosion`, `Solosis`) specify the `BLK` set code, and the `zsv10pt5-39`
  Reuniclus printing — the one already in the local dataset — fits the
  deck's whole theme exactly (see below), so that's almost certainly what
  was meant; worth a direct correction with the source rather than
  guessing silently) — the headline mechanic here hasn't come up before
  in this file: **attacks that evolve multiple Pokémon at once**, not just
  one. `Duosion` (BLK print)'s Cellular Evolution evolves one target;
  `Reuniclus` (BLK print, `zsv10pt5-39`)'s Cellular Ascension goes further
  — "for each of your Benched Pokémon, search your deck for a card that
  evolves from that Pokémon and put it onto that Pokémon to evolve it" —
  potentially completing 4+ separate evolution lines in a single attack,
  a Rare-Candy-for-the-whole-bench effect gated behind one Pokémon's turn
  rather than one Item card per target. `Rare Candy` is still run
  alongside it, most likely to fast-track Reuniclus itself online first,
  with Cellular Ascension mass-completing everything else afterward.
  Feeding that engine: `Antique Root Fossil` and `Antique Armor Fossil`
  (Item cards played as if 60-HP Basic Colorless Pokémon — no retreat, no
  Special Conditions, discardable any time) that `Lileep` and `Shieldon`
  literally evolve *from*, letting the deck open a Basic-count-free board
  position via Trainer search instead of needing real Basics in the
  opening hand, then evolve the Fossil directly into a real attacker.
  `Fossil Quarry` (Stadium) searches up to 2 "Antique"-named Fossils to
  bench per player per turn, symmetric but functionally this deck's own
  Fossil-flooding engine. Real payoff pieces once evolved: `Cradily`'s
  Miasma Wind is the exact scaler documented in `combo_patterns.md`
  Pattern 5 (100 damage per distinct Special Condition on the opponent's
  Active) — this deck reaches it via `Magmar`/`Magmortar`'s own coin-flip
  Burn plus Cradily's own coin-flip Ability rather than the Pattern 5
  worked example's Arbok/Muk line, a real independent confirmation this
  scaler shows up across more than one build (now logged in that Pattern's
  entry too). `Bastiodon`'s Ancient Bulwark (while Benched, not Active —
  easy to misread) zeroes damage from any opponent attacker with 2 or
  fewer Energy attached, a slow-start-denial wall while this evolution
  engine sets up. `Togekiss`'s Wonder Kiss is a coin-flip bonus-Prize
  effect on KO-ing the opponent's Active, worth naming as its own small
  category distinct from the direct-damage-scaling payoffs elsewhere in
  this file.
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
  Ability-heavy current meta entirely. **Precision worth being exact
  about**: both of these are self-protection, not team-wide shields —
  `Cornerstone Mask Ogerpon ex`'s Ability reads "prevent all damage done
  to **this Pokémon**," and `Crustle`'s Mysterious Rock Inn reads
  "prevent all damage done to **this Pokémon** by attacks from your
  opponent's Pokémon ex" (checked literally, not paraphrased from memory)
  — each protects only the single card holding the Ability, while it's
  the one being attacked. The wall works because whichever of these two
  is sitting Active becomes unkillable by the matching attacker type, not
  because the whole board is immune; anything else on the field is still
  as vulnerable as normal. Between those two self-protections (Ability-
  havers, and separately all ex's) most of the archetypes already
  catalogued in this file still can't touch whichever wall-piece is
  Active — everything logged above is either ex, Mega ex, or built around
  a named Ability. `Mist Energy` layers on top, blocking attack
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
- **Hop's-named-family stacked-buff deck** (user-provided, verified
  card-by-card against literal card IDs, not just names — a `pokemoncard.io`
  export lists exact IDs like `me2pt5-96`, and a couple of those didn't
  match the printing that survived dedup locally; confirmed live via the
  API that they're identical reprints, e.g. `sv9-56` and the local
  `Lillie's Clefairy ex` entry match exactly on HP/Ability/attack text) —
  every named "Hop's ___" attacker looks weak alone (`Hop's Wooloo`: 50
  damage for 3 Colorless), but three *independent* sources stack the same
  bonus onto them at once: `Hop's Snorlax`'s Extra Helpings Ability (+30,
  doesn't stack with itself but only needs one Snorlax in play),
  `Postwick` (Stadium, +30, both players' Hop's Pokémon), and `Hop's
  Choice Band` (Tool, +30 and −1 Colorless cost). All three online turns
  Wooloo into 110 damage for 2 Colorless. This is the positive-buff mirror
  of the ex-hate toolbox's damage-tax stack logged above — same "several
  independently-sourced conditional bonuses for one named family, stacked"
  shape, just aimed at your own side instead of the opponent's.
  **A genuine two-card lock combo, not a coincidence**: `Hop's Dubwool`'s
  Defiant Horn forces one of the opponent's Benched Pokémon into the
  Active Spot the instant you evolve into Dubwool, and `Hop's Trevenant`'s
  Corner attack stops the Defending Pokémon from retreating next turn —
  gust a squishy bench target up, lock it in place, then swing with
  whichever buffed Hop's attacker is ready. The deck also actively *wants*
  its own cheap Basics to die: Trevenant's own attack jumps from 30 to 130
  base if a Hop's Pokémon was KO'd by an attack during the opponent's last
  turn, and `Hassel` (look at top 8, take up to 3) shares that exact same
  trigger condition — a disposable-Basics-as-fuel philosophy, not a
  wall/attrition plan like the earlier logged decks. The one non-Hop's
  card, `Lillie's Clefairy ex`, is real tech, not filler: Fairy Zone turns
  opposing Dragon Pokémon's Weakness to Psychic — direct tech against the
  Dragapult ex archetype (Tera/Dragon, logged above) — and Full Moon Rondo
  scales off *total* Benched Pokémon on both sides, which this
  bench-heavy deck (`Hop's Bag` fetches 2 Basic Hop's Pokémon at once)
  naturally inflates on its own. `Telepathic Psychic Energy` (attach to a
  Psychic Pokémon, search 2 Basic Psychic Pokémon to bench) doubles as a
  second Hop's-Basic tutor here specifically because `Hop's Phantump` is
  Psychic-typed — worth checking a Special Energy's search clause against
  a deck's actual type lineup rather than assuming it only fuels, since it
  can moonlight as extra search.
- **Mega Kangaskhan ex / Crustle, stripped-down and refined (user reports
  this build "making some noise" competitively)** — verified card-by-card,
  same core two cards as the ex-immunity wall entry above but with
  `Cornerstone Mask Ogerpon ex` and `Psyduck` cut entirely, replaced by a
  much heavier disruption and healing suite. The real strategic read,
  given the self-protection correction above: `Crustle` isn't walling the
  *team*, it's turning whichever single Active slot it holds into
  something the entire ex-saturated current meta (see this whole file)
  functionally cannot touch — an opposing ex attacker can never damage
  Crustle specifically, full stop, for the rest of the game, no matter
  how much HP or damage it has. `Mega Kangaskhan ex` behind it is the
  actual engine: Run Errand drawing 2 cards *every* turn it's Active is
  enormous sustained card advantage over a long grind, and Rapid-Fire
  Combo's escalating coin-flip damage is the eventual finisher once the
  opponent's board has been worn down. The disruption package attacks the
  opponent's ability to ever find an answer, not their board directly:
  `Eri` strips 2 Items from a revealed hand, `Xerosic's Machinations`
  caps their hand at 3, `Hand Trimmer` caps *both* hands at 5 but the
  opponent discards first (so it's asymmetric in the pilot's favor if
  played after already committing their own hand down). `Handheld Fan`
  is worth noting as the deck's answer to Crustle's one real gap: since
  Mysterious Rock Inn only blocks *ex* attackers, a non-ex attacker can
  still damage Crustle — Handheld Fan (redirect Energy from whatever hits
  the holder onto the *opponent's own* Bench) specifically punishes that
  exact edge case rather than being a generic inclusion. Three separate
  heal effects (`Jumbo Ice Cream`, `Pokémon Center Lady`, `Bianca's
  Devotion`) plus `Hero's Cape` (+100 HP on Kangaskhan ex, 300→400) keep
  the non-immune half of the team alive through the long game this build
  is built to win. Running both `Community Center` and `Festival Grounds`
  (only one Stadium can ever be in play at once) is a real, deliberate
  toolbox choice, not redundancy — pick whichever passive effect actually
  matters for the matchup in front of you. **Honest weak points, not
  glossed over**: this is a grindy, reactive plan with no fast kill, so a
  genuinely explosive aggressive deck can beat it to the punch before the
  disruption/heal engine gets rolling; and any deck built entirely around
  non-ex attackers (several toolbox decks already logged in this file —
  the Team Rocket Supporter-discard deck, the Fossil mass-evolve deck —
  sidestep Crustle's protection completely, since it's ex-specific, not
  universal.
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
