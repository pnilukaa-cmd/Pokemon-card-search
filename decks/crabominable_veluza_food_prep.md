# Crabominable / Veluza — Food Prep

Analysis of a user-supplied list. The engine is genuinely clever; the
build around it is one attacker too greedy and four Items too dead.

## The engine

**`Food Prep`** (on both `Crabominable` SCR 42 and `Veluza` SCR 45):
*"Attacks used by this Pokémon cost Colorless less **for each Kofu card in
your discard pile**."*

| Attack | Printed cost | With 4 Kofu discarded |
| --- | --- | --- |
| `Haymaker` (Crabominable, 250 dmg) | `W C C C C` | **just `W`** |
| `Sonic Edge` (Veluza, 110, damage unaffected by effects on their Active) | `C C C C` | **free** |

`Kofu` SCR 138 is a genuinely good Supporter on its own — bottom 2, draw
4 — so every copy you play to dig is *also* one Colorless off both
attackers. That is a real, elegant piece of deckbuilding.

**`Brilliant Blender`** SSP 164 (ACE SPEC) is the accelerant: *"search
your deck for up to 5 cards and discard them"* finds all four Kofu at
once and switches the whole engine on with one Item. `Team Rocket's
Petrel` (4 copies) searches any Trainer, so it fetches either Blender or
Kofu — five effective outs to the combo. `Team Rocket's Factory` draws 2
more on a Petrel turn. That chain is well built.

Six Energy in a 60-card deck is *correct* here, not a mistake, precisely
because the discount does the work.

## Set numbers

All eight unresolved lines neighbour-check clean: `Crabominable SCR 42`
(SCR 41 Greninja ex / 43 Chewtle, the Water block — Crabominable is Water
while Crabrawler at 87 is Fighting, which is why the line is split across
two type sections), `Special Red Card CRI 82`, `Sacred Ash DRI 168`,
`Black Belt's Training PRE 96`, `Dudunsparce PRE 80`, plus `Meowth ex
POR 62`, `Night Stretcher ASC 196` and `Buddy-Buddy Poffin ASC 184`
already confirmed previously. Nothing to correct.

Shaymin's three Grass attacks flag as IMPOSSIBLE — correct and irrelevant,
it is in for `Flower Curtain`.

Section headers are off, though: the list says `Pokémon: 8` (actual 18),
`Trainer: 16` (actual 36), `Energy: 2` (actual 6). The deck really is 60,
but PTCGL will reject those counts on import.

## What is actually wrong

**1. ~~Four Buddy-Buddy Poffin can only fetch Dunsparce.~~ — WRONG, see
"Correction" below.** Poffin takes Basics with **70 HP or less**, and the
only Basic in the deck that qualifies is Dunsparce:

| | HP | |
| --- | --- | --- |
| Dunsparce | 70 | eligible |
| Shaymin | 80 | too big |
| Crabrawler | 90 | too big |
| Veluza | 130 | too big |
| Meowth ex | 170 | too big |
| Fezandipiti ex | 210 | too big |

I read that as four redundant Items, since `Poké Pad` also fetches every
non-ex Pokémon in the deck including both attackers. **That conclusion was
wrong** — see the correction below. Fetching only Dunsparce is not a
weakness here, because Dunsparce is where the whole chain starts.

**2. Crabominable is the wrong main attacker.** It is a Stage 1 needing
Crabrawler first, and it arrives by turn 6 in only 63.6% of games (avg
turn 3.63). **Veluza is a Basic** with the same Ability, arriving 78.0% by
turn 2.19 — and `Sonic Edge`'s *"damage isn't affected by any effects on
your opponent's Active"* goes straight through `Steven's Carbink`,
`Granite Cave` and every other −30 wall. The 250-damage Haymaker is the
better card in a vacuum and the worse card in this deck.

**3. The deck cannot attack early, by construction.** First attack landed
by turn 6 in **53.1%** of games (avg turn 3.63) — the lowest of any deck
in this folder, where the rest sit at 68–91%. That is inherent: until Kofu
reach the discard, Sonic Edge costs 4 and Haymaker costs 5, against six
Energy in the deck. Turns 1–3 are spent playing Kofu, and there is no
backup plan for the games where they do not show up.

## Correction: keep the Poffin

The original write-up recommended cutting all four `Buddy-Buddy Poffin`
and credited the resulting build's improvement to that change plus the
Veluza change together. **That was a bundled test, and the attribution was
wrong.** Run separately:

| Build | Dunsparce by T6 | Dudunsparce | mean | median | winning |
| --- | --- | --- | --- | --- | --- |
| as sent (3 Veluza, Poffin kept) | 97.3% @ 1.62 | 59.2% | 54.4% | 52.5% | 15/27 |
| 3 Veluza, **Poffin cut** | — | — | 56.2% | 52.5% | 17/27 |
| 4 Veluza, **Poffin cut** | 85.6% @ 2.30 | 41.1% | 57.9% | 55.0% | 22/27 |
| **4 Veluza, Poffin kept** | **95.8% @ 1.67** | **54.8%** | **59.9%** | **58.0%** | 20/27 |

**The Veluza change was carrying the entire improvement.** Cutting Poffin
was a cost being paid alongside it, not a gain: it drops Dunsparce by 10
points and half a turn, and **Dudunsparce by 14 points** — and Dudunsparce
is the draw engine that digs to Petrel, which finds Brilliant Blender,
which loads the discard. Poffin sits at the very start of that chain and
puts **two** Dunsparce on the Bench for one card with no hand cost, which
Poké Pad (one card, to hand) does not replicate.

The winning-matchup counts (20 vs 22) are inside the noise band at 200
games; mean and median both favour keeping the Poffin.

**`Redeemable Ticket` also deserved more credit than it got.** With four
Kofu and a one-of Brilliant Blender in 60 cards, **35.1%** of games prize
at least one Kofu and **10.0%** prize the Blender — **42.1%** of games
prize something the engine needs. Ticket rerolls the whole Prize pile and
puts them back in the deck. That is not a filler slot; it is the answer to
a two-in-five failure mode.

## Suggested changes

One change, not six:

```
-1 Crabrawler SCR 87   (to 2)     +1 Veluza SCR 45      (to 4)
-1 Crabominable SCR 42 (to 2)     +1 Basic Water Energy (to 6)
```

Keep all four Poffin, both Switch, and the Ticket.

Tested across all 27 saved decks, 200 games each:

Veluza goes from 78.0% by turn 2.19 to **98.0% by turn 1.77**, and the
deck's mean win rate from **54.4% to 59.9%** with the median moving
52.5% → 58.0%. Mulligan is unchanged at 19.1% (12 Basics either way).

Keep 2 Crabominable. Haymaker for one Water Energy is still the best
single attack in the deck when the Stage 1 does land; it just should not
be what the deck is *waiting on*.

## Damage boosters and control — the full survey

### Why Shaymin and Black Belt's Training are in there

**`Shaymin` DRI 10** — `Flower Curtain`: *"Prevent all damage done to your
Benched Pokémon that don't have a Rule Box by attacks from your opponent's
Pokémon."* Every attacker in this deck is single-Prize, so the whole Bench
is covered except Fezandipiti ex and Meowth ex. For a deck that does not
attack until turn ~3.5, blanking Bench pressure through the setup turns is
real value. **Two limits worth knowing:** it stops *attacks* only, so it
does nothing against Ability-placed damage (`Dusknoir`'s Cursed Blast,
`Golbat`'s Sneaky Bite), and it does not protect the two ex.

**`Black Belt's Training`** is +40, but **only against a Pokémon ex**, and
it costs the Supporter slot — the same slot Kofu needs to build the
discount and Petrel needs to find the Blender. It is a late-game card in a
deck that spends its early Supporters on the engine.

### Every damage booster in the pool this deck could use

| Card | Boost | Restriction | Slot |
| --- | --- | --- | --- |
| `Brave Bangle` PBL 104 / WHT 80 | +30 | vs **ex only**; holder must have no Rule Box ✓ | Tool |
| `Black Belt's Training` ASC 255 | +40 | vs **ex only** | Supporter |
| `Kieran` TWM 154 | +30 | vs **ex/V only**; other mode is a free switch | Supporter |
| `Maximum Belt` TEF 154 | +50 | vs **ex only** | **ACE SPEC** — conflicts with Brilliant Blender |
| **`Gladion's Final Battle` PBL 108** | **+80** | **any Active**; attacker no Rule Box ✓; **must be your last card** | Supporter |

The headline: **almost every booster in the format is "vs Pokémon ex"
only.** `Gladion's Final Battle` is the single exception and the biggest
number — Sonic Edge 110 → 190, Haymaker 250 → 330, against anything.
`Light Ball`, `Hop's Choice Band`, `Postwick`, `Premium Power Pro`,
`Binding Mochi` and `Future Booster Energy Capsule` are all locked to a
family, type or Special Condition this deck does not have.

### Tested: the boosters do not move the needle here

| Build | mean | median | winning |
| --- | --- | --- | --- |
| 4 Veluza (no new boosters) | **59.4%** | 56.5% | 20/27 |
| + 2 Gladion's Final Battle, −Nighttime Mine, −Special Red Card, −Black Belt's | 58.8% | 56.5% | 21/27 |

**Statistically indistinguishable.** The reason is structural, not a
numbers problem: `Gladion's Final Battle` needs you hellbent, and this
deck refills to 4+ cards every time it plays Kofu. The two fight each
other. The Supporter slot is already fully committed — Kofu is the
discount, Petrel is the search, and there is not a third turn spare for a
damage buff.

**So the honest answer on damage is: no, and the one card that looked like
it would fix it does not.** The existing single `Brave Bangle` is the
right shape, because it is a **Tool** — it costs no Supporter turn at all.
A second copy is the only boost worth adding.

### Control options that do fit

| Card | Effect | Fit |
| --- | --- | --- |
| **`Psyduck` ASC 226** | `Damp` — *Pokémon in play lose any Ability that requires the user to Knock Out itself* | **Basic, 70 HP, Water — Poffin-eligible.** A hard shutdown of every `Cursed Blast` deck (Dusclops/Dusknoir), which is a real archetype |
| `Golduck` ASC 40 | same Ability, Stage 1 | slower version of the above |
| `Budew` ASC 16 | free-cost attack, Item lock for a turn | buys a setup turn, but Grass and off-plan |
| `Walrein` SSP 45 | *Pokémon with 2 or less Energy attached can't attack* | brutal lock, but a Stage 2 — too slow for a deck already starting turn 3 |
| `Frillish` WHT 126 | Item lock | Psychic, off-type |

`Psyduck` is the one genuinely worth a slot, and it is a sideboard-style
answer rather than a maindeck improvement — it is dead against everything
that is not built on a self-Knock-Out Ability.

### One anti-synergy in the current list

`Nighttime Mine` taxes **Tera** Pokémon, and this deck has none — it is
pure opponent tech. But it is a Stadium, and playing it **discards your
own `Team Rocket's Factory`**, which is the card drawing you 2 on every
Petrel turn. Four Stadiums competing for one slot, three of which you
actually want out.

## Revised list

```
Pokémon: 17
4 Veluza SCR 45
2 Crabrawler SCR 87
2 Crabominable SCR 42
3 Dunsparce JTG 120
3 Dudunsparce PRE 80
1 Fezandipiti ex ASC 142
1 Meowth ex POR 62
1 Shaymin DRI 10

Trainer: 36
4 Kofu SCR 138
4 Team Rocket's Petrel ASC 207
4 Poké Pad ASC 198
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin ASC 184
3 Team Rocket's Factory ASC 203
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Switch MEG 130
1 Brilliant Blender SSP 164
1 Special Red Card CRI 82
1 Night Stretcher ASC 196
1 Sacred Ash DRI 168
1 Black Belt's Training PRE 96
1 Redeemable Ticket JTG 156
1 Brave Bangle WHT 80

Energy: 7
6 Basic Water Energy
1 Bubbly Water Energy CRI 84

Total Cards: 60
```

## Numbers

Full field, 200 games each — mean **59.9%**, median **58.0%**, **20/27**
winning, against 54.4% / 52.5% / 15-27 for the list as sent.

The losses are all speed or attrition — decks that punish a turn-3 start.
`panic_poison_paralysis` and `lurantis_heal_punish` both win the race
before Food Prep is online, and Mega Chandelure ex's retreat tax strands
whatever is Active while the discount is still building.

`selective_bloom_cradily` excluded (zero Basic Pokémon the engine can put
into play).

## Simulator work this deck required

`Food Prep` is the deck, and the engine had it wrong in both directions:

1. **The scaling was being dropped.** *"cost Colorless less for each Kofu
   card in your discard pile"* compiled to a **flat −1**, so the engine
   gave a discount before any Kofu had been played and only a quarter of
   the real one once four had. Adds an
   `attack_cost_scales_by_named_card_in_discard` rule and a
   `query_cost_reduction` runtime that counts the named card in the
   discard pile every time an attack is priced. Its sibling shape
   (`Incineroar ex`'s Hustle Play, counting the opponent's Bench) is now
   covered too, and the flat rule stands down when a "for each" clause is
   present rather than double-firing.
2. **`Kofu` and `Brilliant Blender` were unmodeled** in both simulators,
   so the combo could not happen at all. With them wired in, the baseline
   first-attack rate went from 28.1% to 53.1% — the earlier figure was
   measuring a deck that was never allowed to use its engine.

Both are covered by firing tests asserting Haymaker at 5/4/3/1 Energy for
0/1/2/4 Kofu in the discard, that the surviving symbol is the **Water**
and not a Colorless, and that Sonic Edge reaches free.
