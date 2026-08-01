# Combo patterns worth hunting for deliberately

This file is different from `current_meta_staples.md` — that one is a
snapshot of real cards seen in real decks. This one is *methodology*:
shapes of combo worth actively searching for even without a real decklist
prompting it, because the taxonomy already has the pieces tagged
individually and the only missing step is cross-referencing them.

## Pattern 1: a "drawback" is often an enabler for something else

A card whose own text reads as a downside — self-damage, a self-inflicted
Special Condition, a resource cost, a Bench-size or HP restriction — is
worth checking against every *other* card whose trigger condition that
exact downside could satisfy. The taxonomy tags each side of this
correctly already (see below); the missing step has been actually running
the cross-reference, not a coverage gap in the tags themselves.

### Worked example: Risky Ruins

`Risky Ruins` (Stadium) reads as pure downside: "Whenever any player puts a
Basic non-Darkness Pokémon onto their Bench, place 2 damage counters on
that Pokémon" — 20 free self-damage on your own newly-benched Basic, no
attack involved. Tagged `damage_on_bench_placement` (produce). Cross-
referencing that against consume-role families whose trigger it could
satisfy turned up two real, different payoffs in the same real decklist:

1. **`emergency_evolve_low_hp`** — Pidove's Emergency Evolution ability
   triggers "if this Pokémon's remaining HP is 30 or less." Pidove has
   exactly 50 HP, so Risky Ruins' 20 damage lands it at *exactly* 30 —
   free instant evolution into Unfezant the moment it's benched. This
   only works because the numbers line up exactly; **always check the
   actual arithmetic** (source HP minus the drawback's damage amount
   against the specific threshold text) rather than assuming any
   HP-threshold card combos with any self-damage source.
2. **`transfer_damage_to_opponent`** — Munkidori's Adrena-Brain ability
   (once Darkness Energy is attached to it) moves up to 3 damage counters
   from your own Pokémon to the opponent's — laundering the "wasted"
   self-damage into direct damage on their side instead.

Running `--tags damage_on_bench_placement,transfer_damage_to_opponent,emergency_evolve_low_hp`
against the taxonomy surfaced this immediately once the search was framed
correctly — no new tags needed, no taxonomy gap. **The missing step was
treating a drawback-looking card as worth this cross-reference at all**,
not a search-methodology failure once the right query was run.

### The `transfer_damage_to_opponent` family has more members than any one deck uses

The same search also surfaced **Flutter Mane, Team Rocket's Wobbuffet, and
Cofagrigus** as alternative "damage laundering" pieces alongside Munkidori
and Ninetales (which showed up independently in the Wailord ex/Ninetales
research) — all move damage counters from a Benched Pokémon to the
opponent's. When a real decklist uses one member of a small consume-role
family, check whether the *other* members are worth considering too,
rather than treating the one seen as the only option — they're
interchangeable enablers for the same combo shape, and a different one
might fit a different deck's type/energy base better.

### Second real-world confirmation: Slowking's Drapion/Cofagrigus tech (August 2026)

The same `damage-counter producer + Munkidori's Adrena-Brain` shape showed up
again, independently, in a real August 2026 Standard Slowking build (source:
TCGplayer's "Best Decks Right Now" column, cross-checked card-by-card against
`pokemon_standard_cards.json`) — this time the producers are attacks, not a
Stadium: `Drapion`'s Hazardous Tail (100 damage, "this Pokémon also does 70
damage to itself") and `Cofagrigus`'s Law of the Underworld ("Put 6 damage
counters on each Pokémon that has an Ability — both yours and your
opponent's" — a free board-wide effect that also hits your own Ability-users,
e.g. Munkidori itself). Munkidori's Adrena-Brain launders that self-damage
onto the opponent exactly as it did in the Risky Ruins deck. Two independent
real decklists reaching for the same enabler for two different producer
shapes (a Stadium's passive trigger vs. two Pokémon's own attack costs) is
good evidence this is a genuine known staple package, not a one-off — when a
deck runs any card that damages its own side as a cost or side effect,
checking for Munkidori (or another `transfer_damage_to_opponent` member) is
worth doing by default, not just when a decklist happens to already include it.

## Pattern 2: a generic transfer effect routes around a name/type-restricted ability

Many of the strongest resource-generation Abilities are restricted to a
named family — "your Iono's Pokémon," "your Team Rocket's Pokémon," "your
Cynthia's Pokémon," and so on. That restriction looks like it walls off any
payoff card that doesn't share the family name, and it's tempting to
conclude the combo just doesn't work. Check for a **generic transfer
effect** before concluding that — one with no name/type restriction can
move the resource the restricted ability generated onto the excluded
payoff card anyway.

### Worked example: Mega Zeraora ex + Iono's Bellibolt ex

`Iono's Bellibolt ex`'s Electric Streamer Ability attaches unlimited Basic
Lightning Energy per turn, but only to "your Iono's Pokémon" — and
`Mega Zeraora ex` (whose Thunderous Fist does 60 damage per Lightning
Energy attached to it) isn't Iono's-prefixed at all, so Electric Streamer
can't target it directly. The bridge is `Scramble Switch` (ACE SPEC):
"Switch your Active with a Benched Pokémon. If you do, move any amount of
Energy from the Pokémon you moved to the Bench to the new Active
Pokémon" — completely generic, no name restriction. Stack a large energy
pool onto Bellibolt ex (fully legal target for Electric Streamer), then
Scramble Switch moves all of it onto Mega Zeraora ex in one shot for a
massive Thunderous Fist off a 1-energy attack cost. Verify this kind of
bridge is real by checking the *exact* wording of the transfer effect for
any restriction of its own — Scramble Switch has none, which is what makes
it work; a differently-worded transfer effect might still carry a
restriction that blocks the same trick.

**Caveat worth flagging when this pattern shows up**: if the bridge card is
a single-copy ACE SPEC (as it is here), the combo is a precious, largely
one-per-game event, not a repeatable engine — say so plainly rather than
presenting it as reliably available turn after turn.

### The toolkit: generic energy-movement cards (no name/type restriction)

Tagged `energy_move_between_own` in the taxonomy (25 cards total; the ones
below have no Basic-type or name restriction, making them the most
flexible bridges — several other family members are restricted to a
specific Energy type, e.g. Metal- or Water-only, and are situational
bridges only for that color):

- **Scramble Switch** (Item, ACE SPEC) — switch-gated, moves any amount
- **Energy Switch** (Item) — no switch required, moves 1 Basic Energy,
  unlimited copies allowed (not ACE SPEC) — the most accessible generic
  bridge in the pool since it isn't gated behind the 1-ACE-SPEC rule
- **Delcatty** (attack, Energy Blender) — "any amount... in any way you
  like," fully generic
- **Blissey ex** (ability, Happy Switch) — repeatable every turn, moves 1
  Basic Energy between any two of your Pokémon
- **Azumarill ex** (ability, Bubble Gathering) — repeatable, pulls energy
  from any other Pokémon onto itself specifically
- **N's Plan** (Supporter) — moves up to 2 Energy from Bench to Active

## Pattern 3: a "random" resolution can be made deterministic by controlling what it looks at

Some effects read as pure gambling — "discard the top card of your deck and
use its attack if applicable" (Slowking's Seek Inspiration), "flip a coin,"
"reveal the top card." Before writing an effect like this off as unreliable
filler, check whether anything else in the pool can *set or know* the exact
card the random effect will act on. If so, the "randomness" is cosmetic —
the deck can engineer the outcome every time.

### Worked example: Slowking + Academy at Night

`Slowking`'s Seek Inspiration attack discards the top card of the deck and,
if it's a non-Rule-Box Pokémon, borrows one of its attacks. Taken alone this
is a coin flip on deck order. `Academy at Night` (Stadium) lets *each*
player, once per their own turn, "put a card from their hand on top of their
deck" — completely generic, no restriction on which card. Play Academy at
Night, then on a later turn place a spare copy of whatever powerful
non-Rule-Box attacker's attack you want (e.g., a big Trainer-Stage Pokémon
with a strong attack) face-up from hand onto the top of the deck, then
immediately attack with Seek Inspiration — the "randomly discarded" card is
the exact one you just placed, so the "random" attack-copy is fully
deterministic that turn. This is inference from the two cards' literal text
verified against the dataset, not sourced from any deck guide — worth
double-checking turn-order legality (both effects need to resolve within the
same turn, stadium ability before the attack) before relying on it, but the
game-text math checks out.

### The general shape to search for

Whenever a card's effect depends on "the top card of the deck," "a random
card," or a coin flip, check the pool for:
1. **Top-of-deck setters** — anything that lets a player choose a card and
   place it on top (Academy at Night above; `Ciphermaniac's Codebreaking`
   also stacks 2 chosen cards on top, already catalogued in
   `current_meta_staples.md` as deck-stacking, not draw).
2. **Rerolls / look-and-choose variants of the same effect family** — a
   different card that does a similar thing but lets you choose instead of
   relying on chance, which might replace the "random" card entirely rather
   than feed it.
Either one turns a nominally-random payoff into a reliable one, which
meaningfully changes how strong the effect actually is compared to reading
its text in isolation.

## How to run these searches proactively (not just when handed a decklist)

1. When any card's own text is a downside on its face (self-damage,
   self-status, discards a resource, restricts something about the user's
   own board) — Pattern 1 — treat that as a signal to check it against
   consume-role families, not just skip past it as "why would anyone run
   this." When a powerful resource-generation Ability is restricted to a
   named family and a payoff card falls outside that family — Pattern 2 —
   check for a generic transfer effect (search `--suggest-tags` for
   `move`, `transfer`, `switch`) before concluding the combo doesn't work,
   and check the transfer effect's own wording carefully for whether it
   carries a restriction of its own.
2. Use `--suggest-tags` with keywords describing the *shape* of the
   drawback (`damage_counter`, `bench_placement`, `hp_threshold`,
   `transfer`, `self_damage`, etc.) to find candidate produce/consume tag
   pairs, then pull them together with a single `--tags tag1,tag2,tag3`
   call — the script already supports listing multiple tags' members
   side by side in one pass, which is the whole trick.
3. Verify the actual numbers by hand for anything HP- or damage-counter-
   threshold-based — the taxonomy tags the *shape* of an effect correctly,
   but not whether a specific pair of cards' numbers actually align. A
   correct tag match is a candidate to check, not a confirmed combo.
4. When a produce/consume pair is confirmed, check for other members of
   the same consume family (see the `transfer_damage_to_opponent`
   example above) before treating the first match as the only answer.

Other shapes worth the same treatment, not yet worked through in detail
but following the identical pattern: self-status-inflicting attacks paired
against `status_cure`/`status_immune` families (does something in the pool
turn a self-inflicted Special Condition into a non-issue the way Bubbly
Water Energy did for Wailord ex's self-Sleep — see the main SKILL.md step 6
for that specific case); resource-discard costs (Ultra Ball-style) paired
against discard-pile recursion or discard-count payoffs; retreat-cost
increases on the *opponent* paired against anything that benefits from the
opponent being stuck Active.

## Pattern 4: an attack-copying attacker is only as good as what it can copy — check the source's best attack, not the copier's own kit

Tagged `attack_copy_generic` in the taxonomy (Clefable's Metronome, Slowking's
Seek Inspiration, N's Zoroark ex's Night Joker, Team Rocket's Mimikyu's
Gemstone Mimicry, Ethan's Sudowoodo's Try to Imitate, Team Rocket's Persian
ex's Haughty Order, Zoroark's Foul Play, Thievul's Skill Thief) — a card
whose own attack is "use one of [some other Pokémon]'s attacks instead."
These attackers are frequently cheap-to-activate (Night Joker costs just 2
Darkness regardless of what it copies) and deliberately weak or blank on
their own, so their real ceiling is whichever attack they can reach, not
anything printed on their own attack line. When one shows up:

1. Identify what it's allowed to copy (own Bench only, opponent's Active
   only, own discard pile, etc. — the restriction varies by card and matters
   a lot for how reliably it's usable).
2. Look up the actual best-in-slot attack among the eligible sources and
   check whether the deck can set up that attack's own trigger condition —
   e.g. N's Zoroark ex's Night Joker can borrow N's Reshiram's Powerful Rage
   ("20 damage for each damage counter on this Pokémon," scales with however
   much damage N's Reshiram has already taken) or N's Darmanitan's Back
   Draft ("30 damage for each Basic Energy in your opponent's discard pile,"
   scales with the deck's own Energy-discard/disruption count, e.g. Crushing
   Hammer). The attack-copier's real damage ceiling depends on which of
   those setup conditions the rest of the decklist is actually feeding.
3. Cross-check against Pattern 3 above — if the copy source is
   randomly-determined (Seek Inspiration's top-of-deck discard) rather than
   a chosen Bench Pokémon (Night Joker), check for a way to make that
   randomness deterministic before assuming the attack is unreliable.
