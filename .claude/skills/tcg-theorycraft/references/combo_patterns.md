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

### Third real-world confirmation, and the cleanest one yet: Risky Ruins + Mega Darkrai ex

One of five Mega Darkrai ex build variants a user shared (Version 5, and
notably only that version) already ran `Risky Ruins` alongside `Mega
Darkrai ex` — and the connection is exact and essentially free.
`Mega Darkrai ex`'s Dusk Raid (Darkness+Darkness, 110+): "If your Benched
Pokémon have any damage counters on them, this attack does 110 more
damage" — 220 total for 2 Energy, but only if *something* on the bench has
taken damage. Risky Ruins produces exactly that, automatically, every time
a non-Darkness Basic is benched (2 damage counters, no attack needed) —
and every other Basic in this deck's roster (Latias ex, Fezandipiti ex,
Meowth ex, Mega Kangaskhan ex, Moltres, Chi-Yu, Munkidori, Yveltal is not
Basic-restricted-out since it's Darkness... check each roster's own types)
is non-Darkness, while Mega Darkrai ex itself is Darkness-typed and so
exempt from its own Stadium's damage. This is the cleanest instance of
Pattern 1 found yet: no dedicated combo piece needed beyond a Stadium the
deck plausibly wants for other reasons too, and the "drawback" damages the
support cast, never the payoff attacker. **Caution worth carrying
forward**: if this deck also runs `Chi-Yu`'s Ground Melter ("+60 damage if
a Stadium is in play, then discard that Stadium"), firing it while Risky
Ruins is your own active Stadium destroys your own Dusk Raid enabler —
check for this kind of self-inflicted Stadium removal whenever a deck
pairs a Stadium-dependent engine with a Stadium-discarding attack.

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

## Pattern 5: stack multiple *distinct* Special Conditions on one target, close the retreat escape hatch, then cash in with a per-condition-count scaler

SKILL.md step 5 already flags the general danger here in passing (an
"Arbok applies 3 conditions, then Muk cashes in next turn" plan that looked
clean but had a free retreat escape hatch) but never worked the combo all
the way through with real numbers, and — checked directly against the
dataset for this pass — the "Muk" in that anecdote is `Team Rocket's Muk`,
whose own Gooped Up attack (the fix SKILL.md's anecdote actually used) only
adds *one* condition (Confused) and can't be the attack that also cashes in,
since a Pokémon only gets one attack per turn. Below is the sequence
actually checked card-by-card, with the real fix identified (a Supporter,
not Gooped Up) and the real ceiling checked against real Special-Condition
rules rather than assumed.

### The scaler: a two-member family that pays per *distinct* condition, not per counter

`damage_scales_with_special_condition` (consume role) has exactly two
members, and both count the number of *different* Special Conditions
currently affecting the opponent's Active Pokémon, not damage counters:

- **Team Rocket's Muk**'s Hazardous Venom (Darkness+Darkness+Colorless, 3
  Energy): "This attack does 100 damage for each Special Condition
  affecting your opponent's Active Pokémon."
- **Cradily**'s Miasma Wind (Grass, 1 Energy): identical wording, "100
  damage for each Special Condition affecting your opponent's Active
  Pokémon."

One Confused Pokémon is only worth 100 — a fine rate but nothing special.
The real payoff is stacking 2-3 *different* conditions (Confused, Poisoned,
Burned all count separately) onto the same target before this attack fires.

### The setup: Arbok's Panic Poison applies all three at once for 1 Energy

`Arbok` (Darkness, Stage 1, retreat cost 2 Colorless) has Panic Poison
(Darkness ×1, 0 damage): "Your opponent's Active Pokémon is now Burned,
Confused, and Poisoned." — all three Special Conditions, in one attack, for
the cheapest possible cost. This is the cheapest way to load the scaler's
counter in the whole pool (no other card in `status_inflict` applies more
than one condition per use, let alone three for one Energy).

### Closing the actual escape hatch: `Roxie's Performance`, not Gooped Up

The obvious next step — attack with Panic Poison this turn, attack with
Hazardous Venom/Miasma Wind next turn — is exactly the plan SKILL.md warns
about: retreating cures every Special Condition, and nothing in Panic
Poison's own text stops the opponent from just retreating away on their
turn in between, undoing all three conditions for the cost of one retreat.
`Roxie's Performance` (Supporter) is the actual fix, checked directly: "During
your opponent's next turn, their Poisoned Pokémon can't retreat. (This
includes newly Poisoned Pokémon.)" Play it the same turn as Panic Poison —
the parenthetical confirms it applies even though the Poison itself lands
from the same turn's attack, so there's no ordering trap. (Team Rocket's
Muk's own Gooped Up also locks retreat, but only adds Confused, and using it
this turn instead of Panic Poison would mean giving up the 3-condition stack
for a 1-condition one — it's the wrong tool for this specific line, useful
only as a same-Pokémon 2-condition backup, see below.)

### Full turn-by-turn (numbers and timing checked, not assumed)

1. **Your turn N** (Arbok Active, Team Rocket's Muk on the Bench with
   Hazardous Venom's 3 Energy already attached from prior turns): play
   Roxie's Performance, then attack with Panic Poison. Opponent's Active is
   now Burned + Confused + Poisoned, and can't retreat next turn.
2. **Opponent's turn N**: locked out of retreating. Checkup happens once at
   the end of this turn: Poison chips its usual amount with no self-cure;
   Confused only matters if they try to attack (coin flip risk, doesn't
   expire either way); **Burn gets its own coin flip at Checkup to clear
   itself, in addition to dealing damage** — this is the one condition of
   the three that isn't guaranteed to survive.
3. **Your turn N+1**: retreat Arbok (2 Colorless, legal same turn as an
   attack), Team Rocket's Muk is promoted, attack with Hazardous Venom.

### The honest ceiling: 200 guaranteed, 300 only if Burn survives two coin flips

Poisoned and Confused have no self-cure mechanic at all in the rules — once
applied and not retreated/evolved away, they're still there next turn, full
stop. Burned gets an independent coin-flip cure check at **every** Checkup,
and two Checkups happen between Panic Poison landing and Hazardous Venom
resolving (end of your turn N, end of the opponent's turn N) — each an
independent ~50% chance to clear it, so Burn survives to the payoff turn
only ~25% of the time. **The reliable number to plan around is 200 damage
(Confused + Poisoned, both guaranteed once applied and retreat-locked), not
300** — 300 is a real but minority-chance bonus, not the deck's expected
output. Report it that way rather than quoting the theoretical 3-condition
maximum as if it were the normal case.

### Simpler 2-condition fallback that doesn't need Arbok or a Supporter slot

Team Rocket's Muk can generate its own second condition without any other
piece: Gooped Up (Darkness+Colorless, 40 damage) confuses and locks retreat
in the same attack, no Supporter needed. Pair it with `Cradily` sitting on
the Bench (Grass, no Active-Spot restriction on its own ability): "Once
during your turn, you may flip a coin. If heads, choose Burned, Confused,
or Poisoned. Your opponent's Active Pokémon is now affected by that Special
Condition" — choose Poisoned. Turn N: Muk attacks with Gooped Up
(Confused + retreat lock). Turn N+1: before attacking, activate Cradily's
ability choosing Poisoned; on heads, Muk's own Hazardous Venom now hits for
200 (2 conditions); on tails, it's a 100 floor. This route needs one fewer
card, doesn't cost a Supporter for the turn, and never risks Burn's
self-cure — but its own upside is capped at 200 (no route to 300) and is
gated behind Cradily's 50% coin flip rather than a guaranteed effect. It
also mixes Darkness (Muk) with Grass (Cradily) in one deck, same as the
Arbok line mixing Darkness (Arbok, Muk) with a Supporter slot instead of a
second color — worth weighing which tradeoff a real 60 would rather make.

### Real-world confirmation with a third Burn source: Magmar/Magmortar

A user-provided decklist independently ran `Cradily` paired with the
`Magmar`/`Magmortar` line instead of Team Rocket's Muk — a third distinct
way to reach the same 2-condition Miasma Wind payoff, worth recording since
it changes which conditions are actually reliable. Magmortar's own Searing
Flame (Fire+Fire+Colorless, 90 damage) inflicts Burn on a coin flip, not
guaranteed — so this variant leans on Cradily's own coin-flip Ability for
the *second* condition too, meaning both halves of the 2-condition stack
are independently ~50% here, a real step down in reliability from the
Muk/Gooped-Up route (which locks Confused for free, no flip). Magmortar's
Magma Surge Ability ("during Pokémon Checkup, put 3 more damage counters on
your opponent's Burned Pokémon") is worth noting as a separate, independent
reason to want Burn active on the target regardless of whether Miasma Wind
ever fires — it's pulling double duty as both a condition-count contributor
and its own damage-over-time source.

## Pattern 6: seed flat damage across the *whole* opposing board, then double it — no retreat escape hatch to design around at all

`damage_counter_doubler` (produce role) has two members; the generally
usable one is **`N's Vanilluxe`**'s Snow Coating (Colorless+Colorless, 0
base damage): "Double the number of damage counters on each of your
opponent's Pokémon." Unlike Pattern 5's Special-Condition stack, this
pairs with a category of card that's structurally safer to combo with: an
attack that spreads a small, *flat* amount of damage across **every** one
of the opponent's Pokémon — Active and Bench simultaneously — rather than
a single target. `bench_snipe_opponent_all` and `direct_damage_no_attack`
both contain several: `Uxie`'s Painful Memories (Psychic ×1, 0 base
damage): "Put 2 damage counters on each of your opponent's Pokémon";
`Frosmoth`'s Chilling Wings (me1 print, Water ×1, 20 damage): "This attack
does 20 damage to each of your opponent's Pokémon... Your opponent's Active
Pokémon is now Asleep"; `Team Rocket's Arbok`'s Spinning Tail (Darkness
×3, 30 damage): "This attack does 30 damage to each of your opponent's
Pokémon."

### Why this is more reliable than Pattern 5, checked against the actual rules

Special Conditions are cured by retreating or evolving — that's the whole
reason Pattern 5 needs a dedicated retreat-lock piece to make the 2-turn
setup-then-cash-in sequence hold up. **Damage counters have no such
escape.** Retreating moves a Pokémon to the Bench with every damage counter
it already had still on it; evolving does the same. The only ways to remove
a damage counter are a healing effect or the Pokémon being Knocked Out.
That means a "seed now, double next turn" plan built on this family needs
**no** protective piece at all — the opponent can freely retreat, evolve,
or reposition their whole board in between and the counters (and the
doubler's payoff) are completely unaffected either way.

### Worked example, numbers checked

1. **Turn N**: `Frosmoth` (me1 print) attacks with Chilling Wings for 1
   Water Energy — every one of the opponent's Pokémon in play (Active and
   however many are Benched) takes 20 damage (2 counters), and their Active
   is Asleep as a bonus.
2. **Opponent's turn**: free to retreat, evolve, attack, whatever they want
   — none of it removes the damage counters just placed, regardless of
   which of their Pokémon ends up in which position by the time your next
   turn starts.
3. **Turn N+1**: switch `N's Vanilluxe` into the Active Spot and attack with
   Snow Coating for 2 Colorless Energy — every opponent Pokémon that still
   has those counters (all of them, unless healed) now has them **doubled**:
   20 → 40 damage, again spread across their entire board, for a total
   outlay of 3 Energy across two turns.

40 flat, unavoidable damage to literally everything the opponent has in
play is a serious chunk of HP against the many 60-90 HP support Basics that
show up throughout `current_meta_staples.md` (Smoochum, Slowpoke, Dunsparce,
Voltorb, Tadbulb, etc.) and sets up an easy follow-up KO from any ordinary
attack or snipe effect the turn after — check the specific target's real HP
before calling it a guaranteed KO on its own, since 40 alone won't finish a
150+ HP attacker, but as a board-wide softening pass it's strictly better
than a single-target snipe of the same total Energy cost.

### Toolkit: other flat, no-condition, whole-board seeders worth swapping in

Any of these work as the "seed" half in place of Frosmoth, chosen for
whichever Energy type fits the rest of the deck — all hit every one of the
opponent's Pokémon (not just their Active) with a flat, unscaled amount:

- **Uxie** — Painful Memories, Psychic ×1, 20 damage everywhere, no
  attached-Pokémon requirement at all (works from turn one)
- **Team Rocket's Arbok** — Spinning Tail, Darkness ×3, 30 damage everywhere
- **Regice** — Blizzard, Water+Colorless×2, 90 to the Active plus 10 to each
  Benched Pokémon (asymmetric — Bench-only portion is what feeds the doubler
  evenly; the Active already took its big hit directly)
- **N's Vanilluxe**'s own other attack, Blizzard (same text as Regice's) —
  meaning a single copy of N's Vanilluxe can seed its own Bench-wide damage
  one turn and double it the next, at the cost of needing 3 Energy (Water +
  Colorless ×2) for the seed turn before switching to the 2-Colorless
  double turn

## Pattern 7: a board-wide status-immunity Stadium is a 4th real fix for self-inflicted Special Conditions — and a direct anti-synergy against Pattern 5

SKILL.md step 6 lists three real answers to a self-inflicted Special
Condition drawback (immunity Energy/Tools, switch-not-retreat Stadiums,
flat retreat-cost reduction), using Wailord ex's Falling Down (270 damage,
"This Pokémon is now Asleep") as the running example fixed there by
`Bubbly Water Energy`. Checked directly against the taxonomy for this pass:
`status_cure`'s `Festival Grounds` (Stadium) is a fourth real fix, more
general than any of the three already logged, and it wasn't cross-checked
against Wailord ex before now.

**Festival Grounds**' actual text: "Each Pokémon that has any Energy
attached (both yours and your opponent's) recovers from all Special
Conditions and can't be affected by any Special Conditions." Wailord ex's
own Falling Down costs 5 Water Energy, so by the time it's used, Wailord ex
already trivially satisfies "has any Energy attached" — once Festival
Grounds is in play, Wailord ex simply **never becomes Asleep from its own
attack at all**, and is also immune to anything the opponent tries to
inflict on it. Unlike Bubbly Water Energy, this doesn't cost an Energy-line
slot (every attached card can be a plain Basic Water Energy) and doesn't
only cover Sleep — it blanket-covers every Special Condition, from any
source, for the whole game once it's in play.

**The real tradeoff, checked rather than assumed**: the immunity is
explicitly "both yours and your opponent's" — symmetric. Any deck running
Festival Grounds for this reason gives up its own ability to inflict
Special Conditions on the opponent for as long as the Stadium stays in
play, since the opponent's own energied attacker becomes equally immune.
This is a **direct, concrete anti-synergy with Pattern 5 above** (the
Arbok/Muk/Cradily Special-Condition-stacking combo) — a deck can't
meaningfully run both game plans at once, since Festival Grounds would
neutralize its own Panic Poison/Gooped Up/Selective Slime the moment any of
them tries to land on an opponent's Pokémon holding any Energy at all
(true of essentially every attacker by the time it's attacking). Worth
checking for this specific clash whenever a decklist pairs a self-status
attacker (wanting the immunity) with a status-inflicting subplan (wanting
the opposite) — the two want opposite things from the same Stadium slot,
and only one can be in play at a time under the normal 1-Stadium rule.

Also worth noting as a practical fragility, not just for this card but for
any Stadium-based fix: Stadiums are directly contestable — a single
opposing Stadium played later discards Festival Grounds outright (both
players' Stadium slots are shared, "discard it if another Stadium comes
into play" applies regardless of who played either one), so a plan that
depends on Festival Grounds staying in play indefinitely has a real,
opponent-controlled failure mode that Bubbly Water Energy (attached
directly to the Pokémon, not contestable) doesn't share.

## Pattern 8: check whether a "Tool count" scaler is scoped to your side only — the wording isn't always identical between near-duplicate attacks

`damage_scales_with_tools_attached` has 5 members, 4 of which are the
Rotom line's Gadget Show — "This attack does 30 damage for each Pokémon
Tool attached to all of **your** Pokémon" — explicitly your-side-only. The
5th, `Bronzong` (me2 print)'s Tool Drop, reads differently, checked against
the literal dataset text rather than assumed identical: "This attack does
40 damage for each Pokémon Tool attached to **all** Pokémon" — no "your."
As printed, that counts Tools on both sides of the board, not just the
caster's own — a real, verified textual difference from its closest
taxonomy sibling, not a transcription artifact (cross-checked, no other
printing of "Tool Drop" exists in the dataset to compare against, but the
wording is internally consistent with itself and clearly distinct from
Gadget Show's explicit "your Pokémon" phrasing).

Practically: Bronzong (me2-72; Colorless×1 Triple Draw for a 3-card hand
refill, Colorless×3 for Tool Drop) doesn't need its own deck to be
Tool-heavy to hit a real number — Pokémon Tools like `Air Balloon` are
common enough across the current pool (`current_meta_staples.md` logs it as
a default retreat-cost fixer in more than one archetype) that an opponent's
own unrelated Tool choices can passively feed this attack's damage without
Bronzong's pilot doing anything to cause it. **Don't take this as a
guaranteed source of damage** — it depends entirely on what both players
happen to have attached at the moment Tool Drop is used, and a Tool-light
matchup gives it nothing — but when auditing a Tool Drop deck's real
output, count Tools on both sides of the table, not just the caster's own,
since that's what the actual printed text says to do. This is exactly the
kind of near-identical-wording gap worth checking literally rather than
assuming from a family's dominant pattern (4 of 5 members say "your," the
5th doesn't) — general lesson: when several members of the same taxonomy
family look interchangeable, check each one's exact text before treating
the majority phrasing as universal.

## Pattern 9: a shared unusual trigger across several cards doesn't mean any of them natively satisfy it — check the *holder's* type separately from the *condition's* type

Several different cards can share an oddly-specific trigger condition
("if this Pokémon has any [X] attached/attribute") as a deliberate family
identity, without any of them actually being built to satisfy that
condition on their own. Don't assume a shared trigger implies a
type-restricted searcher for that trigger will work on all of them —
check the *searcher's* restriction against each *holder's own type*
separately, since those are two independent facts that can easily conflict.

### Worked example: Okidogi's "Adrena-" family and why type-restricted Darkness search doesn't feed it

Studying `Okidogi` surfaces three real cards, all worth separating clearly
by printing since two share the name:

- **`Okidogi` (sv6-111, Fighting-type)**: Adrena-Power — "If this Pokémon
  has any Darkness Energy attached, it gets +100 HP, and the attacks it
  uses do 100 more damage to your opponent's Active Pokémon." A huge
  passive, but Okidogi's own attack (Good Punch, Fighting+Fighting) has
  nothing to do with Darkness — the Darkness Energy is purely there to
  flip the condition, not to pay a cost.
- **`Okidogi` (me2pt5-122, Fighting-type)**: a different card entirely —
  Settle the Score does 80+ damage, "+60 more damage for each Prize card
  your opponent took during their last turn." A revenge attacker: it wants
  the opponent to have just KO'd one of your Pokémon (2 Prizes from an ex
  KO = +120, for 200 total off a 3-Energy attack). Same disposable-Basics
  philosophy as `Hop's Trevenant`/`Hassel`'s shared "a Hop's Pokémon was
  KO'd last turn" trigger (`current_meta_staples.md`) — not something you
  can force, but a real payoff for a deck willing to trade a big Pokémon on
  purpose rather than only trying to protect its board.
- **`Okidogi ex` (sv6pt5-36, Darkness-type)**: a self-contained 2-turn
  combo with itself — Poisonous Musculature searches up to 2 Basic
  Darkness Energy and attaches them to itself, *and* self-inflicts
  Poison as a side effect of doing so; Chain-Crazed does 130+130=260 if
  Poisoned. No external card needed — it's Pattern 1's shape (a drawback
  enabling a payoff) except both halves are printed on the same card, one
  turn apart. **Anti-synergy worth flagging explicitly**: `Festival
  Grounds` (Stadium — "Each Pokémon that has any Energy attached recovers
  from all Special Conditions and can't be affected by any Special
  Conditions," both players) directly erases this combo the instant
  Poisonous Musculature attaches Energy, the same way Pattern 7 already
  flagged it against Wailord ex's self-Sleep. Don't run both in the same
  deck without noticing.

The interesting cross-card finding: `Munkidori`'s Adrena-Brain and
`Fezandipiti`'s Adrena-Pheromone share Adrena-Power's exact "any Darkness
Energy attached" trigger — clearly a deliberate shared family identity
(these three are the Loyal Three legendary trio) — but **checking their
actual types**, Munkidori and Fezandipiti (non-ex) are both **Psychic**,
and the base Okidogi above is **Fighting**. None of the three
Adrena-ability holders is Darkness-typed. That matters because the
obvious-looking feeders are type-restricted and can't reach them:
`Toxtricity`'s Sinister Surge only attaches to "your Benched **Darkness**
Pokémon," and `Janine's Secret Art` only targets "your **Darkness**
Pokémon" — both walled off from all three Adrena- holders. The real
bridge has to be a **generic, type-unrestricted** Energy mover — exactly
the `energy_move_between_own` toolkit from Pattern 2 (`Energy Switch`,
`Delcatty`, `Blissey ex`, `N's Plan`, etc.). `Energy Switch` in particular
is the cleanest fit here: not gated behind the 1-ACE-SPEC rule, and since
none of the three Adrena- Pokémon's own attacks need Darkness Energy for
cost, a single Darkness Energy card can be shuffled between whichever of
the three needs its passive on right now — Okidogi before it attacks,
Fezandipiti before the opponent's turn (its bonus only matters when it's
about to take a hit), Munkidori before using Adrena-Brain — rather than
needing one dedicated Darkness Energy per Pokémon.

### Independent confirmation: a Mega Darkrai ex deck runs straight into the same gap

A different user-provided deck (several Mega Darkrai ex build variants,
none related to the Okidogi research above) ran both `Munkidori` and
`Janine's Secret Art` — and would have hit exactly this wall: Janine's
Secret Art only attaches Basic Darkness Energy to "your Darkness
Pokémon," and Munkidori is Psychic-typed, so it can never be a legal
target for it. The deck already happened to run `Energy Switch` (2-3
copies across its variants) for unrelated-looking generic utility — which
is, unnoticed by the builder or not, the only thing in the list actually
capable of getting a Darkness Energy onto Munkidori to turn on
Adrena-Brain. Worth calling out plainly when this shows up again: a deck
can already contain its own fix for a gap like this without the fix being
labeled as one — check every generic mover already in a decklist against
every type-restricted trigger before assuming a gap needs a new card added.

### Third independent confirmation, and the most fragile version yet: a Marnie's Grimmsnarl ex deck

A third, unrelated user-provided deck (a Marnie's Grimmsnarl ex evolution
line plus `Munkidori` and `Yveltal`) ran straight into the identical gap —
its only Darkness Energy source that could reach a non-Darkness Pokémon
is `Marnie's Grimmsnarl ex`'s Punk Up Ability, which is itself restricted
to "your **Marnie's** Pokémon," so it can't feed Munkidori either.
This deck's only generic bridge is a single copy of `Energy Switch` — even
more precious than the 2-3 copies the Mega Darkrai ex deck ran, so
Adrena-Brain coming online at all is a real one-shot-per-game event here,
not a repeatable plan. Three independent decks hitting this exact wall is
strong confirmation this is a common, easy-to-miss deckbuilding trap
whenever Munkidori is paired with *any* named-family-restricted Darkness
search, not just Janine's Secret Art specifically.
