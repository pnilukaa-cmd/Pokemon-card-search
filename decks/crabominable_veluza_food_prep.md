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

**1. Four Buddy-Buddy Poffin can only fetch Dunsparce.** Poffin takes
Basics with **70 HP or less**, and the only Basic in the deck that
qualifies is Dunsparce:

| | HP | |
| --- | --- | --- |
| Dunsparce | 70 | eligible |
| Shaymin | 80 | too big |
| Crabrawler | 90 | too big |
| Veluza | 130 | too big |
| Meowth ex | 170 | too big |
| Fezandipiti ex | 210 | too big |

Four Items that only ever fetch the draw engine, never an attacker — and
`Poké Pad` (also 4 copies) already fetches every non-ex Pokémon in the
deck including both attackers. The Poffins are redundant *and* narrower.

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

## Suggested changes

```
-4 Buddy-Buddy Poffin ASC 184     +1 Veluza SCR 45  (to 4)
-1 Crabrawler SCR 87   (to 2)     +2 Basic Water Energy (to 7)
-1 Crabominable SCR 42 (to 2)     +2 Switch MEG 130 (to 4)
```

Tested across all 27 saved decks, 200 games each:

| Build | first attack by T6 | mean | median | winning matchups |
| --- | --- | --- | --- | --- |
| as sent | 53.1% | 54.4% | 52.5% | 15/27 |
| −4 Poffin, +2 Switch, +2 Energy | 58.2% | 56.2% | 52.5% | 17/27 |
| **+ Veluza-focused (4 Veluza, 2-2 Crab)** | **57.6%** | **57.9%** | **55.0%** | **22/27** |

Veluza goes from 78.0% by turn 2.19 to **95.8% by turn 1.89**. The
winning-matchup count is the number that moves most: **15 → 22**. Mulligan
is unchanged at 19.1% (12 Basics both ways).

Keep 2 Crabominable. Haymaker for one Water Energy is still the best
single attack in the deck when the Stage 1 does land; it just should not
be what the deck is *waiting on*.

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

Trainer: 35
4 Kofu SCR 138
4 Team Rocket's Petrel ASC 207
4 Poké Pad ASC 198
4 Ultra Ball MEG 131
4 Switch MEG 130
3 Team Rocket's Factory ASC 203
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
1 Brilliant Blender SSP 164
1 Special Red Card CRI 82
1 Night Stretcher ASC 196
1 Sacred Ash DRI 168
1 Black Belt's Training PRE 96
1 Brave Bangle WHT 80
1 Redeemable Ticket JTG 156
1 Nighttime Mine ASC 197

Energy: 8
7 Basic Water Energy
1 Bubbly Water Energy CRI 84

Total Cards: 60
```

## Numbers

Full field, 200 games each — mean **57.9%**, median **55.0%**, **22/27**
winning. Best: Feraligatr/Munkidori 87.0%, T.R. Wobbuffet 80.0%, Eerie
Inferno 77.5%, Salazzle ex 74.5%, Chandelure mill 74.0%. Worst: Panic
Poison Paralysis 37.0%, Lurantis heal punish 39.5%, Mega Chandelure ex
42.5%, Steven's Carbink 43.0%.

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
