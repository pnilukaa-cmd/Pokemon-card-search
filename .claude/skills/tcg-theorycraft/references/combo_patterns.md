# Combo patterns worth hunting for deliberately

This file is different from `current_meta_staples.md` — that one is a
snapshot of real cards seen in real decks. This one is *methodology*:
shapes of combo worth actively searching for even without a real decklist
prompting it, because the taxonomy already has the pieces tagged
individually and the only missing step is cross-referencing them.

## The pattern: a "drawback" is often an enabler for something else

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

## How to run this search proactively (not just when handed a decklist)

1. When any card's own text is a downside on its face (self-damage,
   self-status, discards a resource, restricts something about the user's
   own board), treat that as a signal to check it against consume-role
   families, not just skip past it as "why would anyone run this."
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
