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
