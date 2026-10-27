# Aurorus / Mega Kangaskhan ex: Tundra Wall

Built 2026-10-26 on request: a new deck "focused on tankiness, damage
reduction / mitigation". Revised 2026-10-27, on the question: mix in the
Snorlax deck's strategy (Snorlax, its Good Sleep heal, the damage
mitigation), add heals and disruption, and is 27 Energy too much?

**This list: 82.86% against the 98-deck field at 1000 games per opponent**
(median 89.2%, 92 of 98 winning), on the engine as of 2ee4fb9. On the same
seeds and engine it is **+2.85 ± 0.29** over the 2026-10-26 list (80.01%),
better on 82 of 98.

**The changes from the 2026-10-26 list:**
- **−6 Water Energy** (27 → 21).
- **+4 Crushing Hammer** and **+2 Jumbo Ice Cream**.

The 2026-10-26 list read 78.88% against 97 decks on 95007af. It reads
80.01% against these 98 (its own copy added) with the Fossil fix below
(2ee4fb9). The +2.85 compares both lists on the same engine and field.

## The idea

**Aurorus's Tundra Wall** (POR 24, Stage 2 Water, 170 HP, Retreat 3):
- **The wall:** all of your Pokémon with any Water Energy attached take 50
  less damage from attacks. It doesn't stack, so one Aurorus in play is
  the whole effect.
- **Freezing Chill** (Water, Water, Colorless): 150, and the Defending
  Pokémon can't attack next turn.

**So every Pokémon here carries Water Energy, and the attackers are the
biggest Basics that pay with it:**
- **Mega Kangaskhan ex** (MEG 104, Basic, 300 HP, Retreat 3).
  - Rapid-Fire Combo (CCC): 200, plus 50 for each heads until tails.
  - Run Errand: draw 2 while it's Active.
  - Under Tundra Wall, 300 HP taking 50 less (400 with Hero's Cape).
  - It gives up 3 Prizes.
- **Bouffalant ex** (WHT 162, Basic, 220 HP).
  - Bouffer: takes 30 less, so 80 less under Tundra Wall.
  - Gold Breaker (CCC): 100, or 200 against a Pokémon ex.
- **Articuno** (JTG 161, Basic, 110 HP, Retreat 1).
  - Frigid Fluttering (C): search 2 Basic Water Energy and attach them to
    itself.
  - Ice Blast (Water, Water, Colorless): 110.

**Getting Aurorus out:** Aurorus evolves from Amaura, which evolves from
**Antique Sail Fossil**, an Item played as a 60 HP Basic Colorless Pokémon
(it can't retreat, and can be discarded from play at any time during your
turn).
- **Fossil Quarry** (Stadium, once each player's turn): search up to 2
  "Antique" cards onto the Bench. That's the Fossils without spending a
  card each.
- **Rare Candy** goes straight from the Fossil to Aurorus, the turn after
  it was put down.
- **Poké Pad** finds Amaura, Aurorus or Articuno. It can't find a Fossil:
  in the deck a Fossil is an Item.

**The utility (2026-10-27):**
- **Jumbo Ice Cream** (PFL 91, Item): heal 80 from your Active Pokémon if
  it has 3 or more Energy attached. Every attack here costs three.
- **Crushing Hammer** (POR 71, Item): flip a coin; if heads, discard an
  Energy from one of your opponent's Pokémon.

## 2026-10-27: Snorlax, heals, disruption and fewer Energy

**The short answers:**
- **Snorlax doesn't fit here.** No version gained (−0.49 to −2.56), and
  moving the Water wall into the Snorlax deck lost 8.60. Good Sleep heals rarely, even
  in its own deck.
- **Heals and Energy disruption win.** Jumbo Ice Cream (heal 80 from an
  Active with 3 or more Energy; every attacker here runs three) and
  Crushing Hammer took the deck from 80.0% to 82.9%.
- **27 Energy was too many.** The six cut Energy were sitting in hand: the
  same Energy reaches the board with 21. But the Energy count itself is
  close to neutral. The gain is in what replaces them.

**Round 1** (`m1_`, engine 927c086), each against the 2026-10-26 list,
each new pair for 2 Water Energy unless noted. 200 games a matchup:

| Change | Measured |
|---|---|
| +2 Jumbo Ice Cream, +2 Crushing Hammer (−4 Energy) | **+1.99 ± 0.43** |
| +2 Cook | +1.46 ± 0.42 |
| +2 Jumbo Ice Cream | +1.31 ± 0.34 |
| +2 Xerosic's Machinations | +0.95 ± 0.38 |
| +2 Fennel | +0.93 ± 0.41 |
| +2 Crushing Hammer | +0.48 ± 0.37 |
| +2 Snorunt, +2 Mega Froslass ex (Absolute Snow puts the Active to sleep; −4 Energy) | +0.08 ± 0.52 |
| +2 Judge | −0.26 ± 0.39 |
| +4 Snorlax, +2 Heavy Baton, −2 Bouffalant ex (−4 Energy) | −0.49 ± 0.43 |
| +2 Pokémon Catcher | −0.54 ± 0.41 |
| Poké Vital A for Hero's Cape | −0.60 ± 0.36 |
| +2 Budew (Itchy Pollen, Item lock) | −0.85 ± 0.37 |
| +2 Snorlax | −1.12 ± 0.41 |
| +2 AZ's Tranquility | −1.12 ± 0.41 |
| +3 Snorlax, +1 Heavy Baton (−4 Energy) | −2.56 ± 0.41 |

**Round 2** (`m3_`, engine 2ee4fb9), each against the round-1 winner (23
Energy, 2 Jumbo Ice Cream, 2 Crushing Hammer), which is itself +2.43 ±
0.37 over the 2026-10-26 list on this engine:

| Change | Measured |
|---|---|
| +2 Crushing Hammer for 2 Energy (21) | **+0.99 ± 0.33** |
| +1 Cook, +1 Xerosic's for 2 Energy | +0.88 ± 0.37 |
| +2 Cook for 2 Energy | +0.81 ± 0.38 |
| +2 Cook for 2 Poké Pad | +0.70 ± 0.39 |
| +2 Jumbo Ice Cream for 2 Energy | +0.65 ± 0.38 |
| +2 Xerosic's for 2 Energy | +0.37 ± 0.38 |
| +2 Energy Search for 2 Energy | +0.27 ± 0.32 |
| +2 Poké Pad for 2 Energy (21) | +0.13 ± 0.36 |
| +2 Xerosic's for 2 Poké Pad | +0.04 ± 0.37 |
| +2 Energy Retrieval for 2 Energy | −0.25 ± 0.32 |
| +2 Energy for 2 Poké Pad (25) | −0.31 ± 0.38 |
| +2 Night Stretcher for 2 Energy | −0.46 ± 0.36 |

**Round 3** (`m4_`), each against this list. Nothing beat it:

| Change | Measured |
|---|---|
| Cook for a Poké Pad | +0.19 ± 0.30 |
| +2 Cook for 2 Energy (19) | +0.13 ± 0.28 |
| Cook and Xerosic's for 2 Poké Pad | +0.08 ± 0.31 |
| 2 Cook for 2 Poké Pad | +0.05 ± 0.32 |
| 2 Jumbo Ice Cream for 2 Poké Pad | −0.18 ± 0.28 |
| 2 Xerosic's for 2 Poké Pad | −0.20 ± 0.34 |
| 2 Energy for 2 Poké Pad (23) | −0.48 ± 0.35 |
| Cook for a Switch | −0.96 ± 0.33 |
| Cook for a Lillie's Determination | −0.97 ± 0.31 |

**Mixing with the Snorlax deck,** both ways:
- **Snorlax into this deck:** −0.49 to −2.56 (round 1).
- **This deck's wall into the Snorlax deck,** each against the Snorlax /
  Bouffalant / Kangaskhan list (86.51% on this engine):
  - Water Energy for Psychic, Articuno for Smoochum and Lillie's
    Clefairy ex, and an Aurorus line (2 Antique Sail Fossil, 2 Rare Candy,
    1 Amaura, 2 Aurorus): **−8.60 ± 0.56**. With Fossil Quarry for a
    Lively Stadium: −9.26 ± 0.66.
  - Its Pokémon take 110 less with Curly Wall on top of Tundra Wall, and
    it still measured 8.6 points worse.
- **Heals and disruption into the Snorlax deck,** for its 2 Kofu: Jumbo Ice
  Cream −0.02, Xerosic's −0.32, Cook −0.60, Crushing Hammer −0.72 (each
  about ± 0.3). Jumbo Ice Cream for Psychic Energy instead: +0.47 ± 0.33
  for two, +0.67 ± 0.34 for three (with one Kofu); see that deck's page.
- **The Snorlax deck is still the stronger deck:** +3.47 ± 0.49 over this
  list, 200 games a matchup.

**Why Snorlax loses here** (`goodsleep.py`, 2 games against each field
deck):

| | Snorlax deck | This deck with 4 Snorlax |
|---|---|---|
| Snorlax attacks per game | 1.49 | 2.56 |
| Good Sleep heals per game | 0.20 (91 HP each) | 0.41 (67 HP each) |
| Snorlax Knocked Out per game | 0.12 | 0.33 |

Good Sleep needs Snorlax to stay asleep through the Checkup after your
turn and the one after the hit, one chance in four. Even in its own deck it
heals about once every five games. Collapse does 130 for three Energy;
Rapid-Fire Combo does 200, plus 50 a heads, for the same three.

**What the new cards do in play** (`mitigation.py`, 5 games against each
field deck):

| | 2026-10-26 list | This list |
|---|---|---|
| Share of incoming damage mitigated | 17.3% | 17.4% |
| HP healed per game | 0 | 37.2 |
| Opponent's Energy removed per game | 0 | 0.90 |
| Damaging attacks taken (490 games) | 1620 | 1530 |

The wall takes off the same share. On top of it the list heals 37 HP and
removes 0.90 of the opponent's Energy a game, and it was hit 6% fewer times
over the same 490 games.

**27 Energy was too many** (`energy_curve.py`, 10 games against each field
deck, at the end of your turn):

| Turn | 27 Energy: in play / Active can attack / Energy in hand | 21 Energy: in play / Active can attack / Energy in hand |
|---|---|---|
| 2 | 2.38 / 19.8% / 3.11 | 2.37 / 20.6% / 2.17 |
| 3 | 3.23 / 78.5% / 3.56 | 3.22 / 76.6% / 2.43 |
| 4 | 3.89 / 79.3% / 3.95 | 3.88 / 77.9% / 2.60 |
| 6 | 5.22 / 85.2% / 4.62 | 5.28 / 81.9% / 2.90 |

The board gets the same Energy. With 27, an extra one to two Energy cards
sat in hand every turn. The Active can attack slightly less often with 21
(81.9% against 85.2% at turn 6); the list as a whole is still +2.85.

## The 2026-10-26 build

### What the measurements said

**The first build was a Water wall built from Stage 1 tanks**, and it
measured 39.68% (49.45% after the engine fix below):
- Cetitan (Solid Body, −30; 80 less under Tundra Wall);
- Mega Abomasnow ex (Frost Barrier: 200, and 30 less next turn);
- Aurorus.

Every round said the same thing: the Stage 1 lines and the support
Pokémon cost more than their reductions saved, and Energy was short.
Each change below is paired against the list of its round, 200 games a
matchup:

| Round | Change | Measured |
|---|---|---|
| 1 | +2 Mega Kangaskhan ex | **+7.34** |
| 1 | Bastiodon (Ancient Bulwark) / Bronzong (Protective Bell) / Dewgong (Wash Out) | −3.63 / −4.94 / −4.36 |
| 1 | Neutralization Zone for Hero's Cape | +0.37 |
| 2 | Mega Abomasnow ex line out, 4 Kangaskhan, +3 Energy | **+15.29** |
| 2 | Cetitan line out, +4 Energy, Articuno, Kangaskhan, Bouffalant ex | **+14.77** |
| 2 | Wally's Compassion / Pokémon Center Lady / Lively Stadium | +0.11 / +0.70 / +0.06 |
| 3 | both lines out (the shell above), 23 Energy | 73.24% |
| 3 | −2 Ultra Ball, +2 Energy | +2.29 |
| 3 | no Aurorus (Regice ex, Bouffalant ex, Energy instead) | −2.82 |
| 3 | Bouffalant's Curly Wall on top (2 or 3 Bouffalant) | −2.94 / −2.57 |
| 3 | Regice ex / Black Kyurem ex | −5.41 / −5.48 |
| 4 | −2 more Ultra Ball, +2 Energy (27) | +1.87 |
| 4 | Neutralization Zone for Hero's Cape | **−11.03** |
| 4 | Survival Brace for Hero's Cape | −2.63 |
| 4 | Mega Abomasnow ex back, with the mill fix | −1.11 |
| 4 | Cetitan back | −6.44 |
| 5-6 | −Boss's Orders, −Night Stretcher, +2 Poké Pad | +1.31 |

What it adds up to:
- **Tundra Wall earns its place,** +2.82 over the same shell without it.
  But the mitigation that wins is the one on the attacker. A Kangaskhan
  that hits for 200+ and takes 50 less beat every Pokémon that only
  reduces damage.
- **Curly Wall** (another −60 to Basic Colorless) measured worse on top.
  Two Bouffalant that don't attack cost more than the extra 60.
- **Neutralization Zone** prevents all damage from Pokémon ex to Pokémon
  without a Rule Box. It's also a Stadium, so it pushes out Fossil Quarry,
  and Kangaskhan and Bouffalant ex have Rule Boxes: −11.03.
- **Energy:** 27 Basic Water Energy is not a typo. Every Pokémon needs
  Water for the wall, and every attack costs three.

**Measured mitigation in play** (`mitigation.py`, 5 games against each
field deck, 95007af): 17.1% of incoming damage is taken off, 69.5 taken
per damaging hit against 83.8 before mitigation. For comparison, the
Snorlax / Bouffalant / Kangaskhan Curly Wall deck: 14.2%. Hits are counted
up to the HP the Active had left.

**Energy on the board** (`energy_curve.py`, 10 games against each field
deck, 95007af):

| End of your turn | First build: Energy in play / Active can attack | 2026-10-26 list: Energy in play / Active can attack |
|---|---|---|
| 2 | 1.93 / 45.2% | 2.30 / 18.0% |
| 3 | 2.46 / 40.1% | 3.18 / 70.6% |
| 4 | 2.80 / 46.4% | 3.83 / 74.8% |
| 6 | 3.27 / 49.3% | 5.02 / 78.8% |

Turn 2 is slower (Rapid-Fire Combo costs three), and from turn 3 the
Active can attack three turns in four. With the Fossil fix in (this list,
2ee4fb9), Mega Kangaskhan ex is in play by turn 4 in 77.8% of games and
Aurorus in 49.0%.

## How to play it

1. **Turn 1.**
   - Mega Kangaskhan ex or Articuno Active.
   - Fossil Quarry for two Antique Sail Fossils.
   - Water Energy on the Active.
   - Articuno's Frigid Fluttering is a good first attack: two Water
     from the deck. The player going first can't attack on turn 1.
2. **Turn 2.**
   - Rare Candy a Fossil into Aurorus. It can't go on a Fossil put down
     this turn, or on your first turn.
   - Give Aurorus a Water Energy too: Tundra Wall covers it as well.
3. **Every turn after.**
   - Kangaskhan Active: Run Errand, then Rapid-Fire Combo.
   - Keep one Water on every Benched attacker so the wall covers whoever
     comes in.
   - Aurorus's Freezing Chill when their attacker needs to stop for a
     turn.
   - Jumbo Ice Cream on a damaged Kangaskhan with its three Energy, before
     it attacks again.
   - Crushing Hammer on the Pokémon about to attack you, or the one
     closest to its attack cost.

**The opponent's outs:**
- **Fighting.** Kangaskhan and Bouffalant ex are weak to it. The two worst
  matchups are Fighting decks: Mega Zygarde ex / Cinderace (Gaia Wave)
  22.1%, Tauros 27.4%.
- **Knock Out Aurorus.** A Boss's Orders on the Benched Aurorus (170 HP,
  weak to Metal) turns the wall off.
- **Kangaskhan gives up 3 Prizes.** Two Knock Outs on it are six.
- **Ability lock** stops Tundra Wall and Run Errand.
- **A promoted Fossil can't retreat.** After a Knock Out, don't promote a
  Fossil unless you have Switch; it can be discarded from play on your
  turn.

## Matchups (1000 games each)

Both lists on 2ee4fb9, the same seeds.

**Best:** Mew baby box 100.0%, Mew / Hypno 99.6%, Team Rocket's Arbok /
Yveltal 98.9%, Wobbuffet / Orbeetle 98.8%, Mew / Bastiodon 97.8%.

**Worst:**

| Opponent | This list | 2026-10-26 list |
|---|---|---|
| Mega Zygarde ex / Cinderace, Gaia Wave | 22.1% | 17.4% |
| Tauros, Risky Ruins | 27.4% | 26.2% |
| Snorlax / Bouffalant / Mega Kangaskhan ex | 41.4% | 34.7% |
| Mega Zeraora ex / Cinderace | 45.9% | 40.6% |
| Mega Zygarde ex / Cinderace, Turbo Flare | 46.0% | 44.2% |
| Arboliva / Ogerpon | 47.2% | 38.7% |
| N's Zoroark toolbox | 53.2% | 51.0% |
| Chesnaught / Meganium | 54.9% | 48.3% |

Every one of the worst eight moved up. Against the 2026-10-26 list itself
(the field's copy) this list wins 62.8%.

**The meta decks:**

| Opponent | This list | 2026-10-26 list |
|---|---|---|
| Festival Lead | 96.1% | 97.0% |
| N's Zoroark | 89.9% | 86.5% |
| Dragapult / Dusknoir | 87.9% | 85.0% |
| Slowking | 87.7% | 84.9% |
| Dragapult / Blaziken | 86.2% | 77.4% |
| Dragapult | 83.8% | 80.4% |
| Raging Bolt | 77.4% | 73.9% |
| Mega Excadrill | 62.8% | 62.0% |

## What the simulator found

Each fix has a regression test that fails on the commit before.
1. **Damage walls dropped their conditions** (f117148):
   - **Tundra Wall and Klinklang's Gear Coating** ("all of your Pokémon
     that have any Water / Metal Energy attached") protected only
     themselves.
   - **Dewgong's Thick Fat** took 30 off every attack, not just Fire and
     Water.
   - **Drednaw's Impervious Shell** (200 or more) and **Carracosta's
     Mighty Shell** (attackers with Special Energy) were total immunity.
   - **Granite Cave** protected nobody.
2. **Every Basic Energy in play read as Special Energy** (f117148).
   Enhanced Hammer discarded Basic Energy, and Tyrantrum's +150 HP came
   on with any Energy. That's 11 field decks; the 2026-10-26 field table
   notes them as stale.
3. **Hammer-lanche milled for free** (95007af). Discarding the top 6 of
   your own deck was priced at nothing, so it tied Frost Barrier at 200
   and was used every turn. The round-1 Kangaskhan list decked itself out
   in 36 of 291 games. Each milled card now costs damage, more as the
   deck runs down: +9.84 ± 0.65 and +7.35 ± 0.64 on the two Abomasnow
   lists. Abomasnow was cut in round 2, before this fix. Put back in
   round 4 with the fix in, it still measured −1.11.
4. **Fossils were Pokémon in the deck** (2ee4fb9). A Fossil is an Item
   played "as if it were" a Basic Pokémon, and only in play is it one.
   Poké Pad, Ultra Ball and Buddy-Buddy Poffin fetched Fossils, Night
   Stretcher returned one, and setup put one down as the opening Active,
   where it can't attack or retreat. This list's Poké Pads were finding
   Fossils. It touches the 6 field decks with Fossils.
5. **The setup baseline had the same bug, and no Fossil Quarry**
   (bbf7b1b). This list's "first attack by turn 6" read 81% and is 98%.
6. **Tried and removed:** a heal Supporter played before the draw
   Supporters when it takes the Active out of the opponent's reach. Cook,
   Fennel and AZ's Tranquility were never played while Lillie's
   Determination was in hand. Measured −0.48, −0.42 and +0.23 on the three
   heal lists (`runs/2026-10-27/pilot_checks`), so the AI still draws
   first.

## Cards searched

- **Mitigation** (`damage_reduction_self`, `damage_reduction_team`,
  `damage_prevention_conditional`, `ko_prevention`,
  `attack_damage_reduced_next_turn_opponent`, the type Berries), plus raw
  sweeps for "less damage" and "prevent all damage", triaged by hand:
  noise only.
- **Whole-team reductions:**
  - Tundra Wall (−50, Water Energy);
  - Curly Wall (−60, Basic Colorless, needs two Bouffalant);
  - Gear Coating (−20, Metal Energy);
  - Protective Bell (−10);
  - Antique Armor Fossil (−10 while Active);
  - Full Metal Lab and Iron Defender (Metal);
  - Granite Cave and Stone Palace (Steven's);
  - Jasmine's Gaze (−30 for one turn).
- **Walls:**
  - Ancient Bulwark (attackers with 2 or fewer Energy);
  - Neutralization Zone (ex attackers, no-Rule-Box defenders);
  - Mysterious Rock Inn, Safeguard and Armor Tail (ex attackers);
  - Cornerstone Stance (attackers with Abilities);
  - Impervious Shell (200+).
- **Self reductions:** Solid Body, Diamond Coat, Bouffer, Mud Coat,
  Thicket Body, Soft Wool (−30); Fur Coat and Exoskeleton (−20).
- **Energy:**
  - Articuno, Regice ex, Dewgong's Wash Out, Chansey, Blissey ex;
  - Crispin (needs two types);
  - Energy Switch, Waitress.
- **2026-10-27, heals** (all nine `heal_*` tags plus a raw "heal" sweep;
  the sweep's diff against the tags is 0):
  - Trainers: Jumbo Ice Cream, Cook, Fennel, AZ's Tranquility, Pokémon
    Center Lady, Wally's Compassion, Bianca's Devotion, Jacinthe, Potion,
    Super Potion, Poké Vital A, Arven's Sandwich, Dragon Elixir,
    Clemont's Quick Wit, Lumiose Galette, Community Center.
  - Snorlax's Good Sleep; Magearna's Auto Heal (Active only).
- **2026-10-27, disruption** (`energy_discard_opponent`,
  `hand_discard_opponent`, plus a raw "discard an energy" sweep: its 28
  extra hits are self-discard costs, noise):
  - Crushing Hammer, Enhanced Hammer (Special Energy only), Megaton
    Blower, Rust Syndicate Grunt;
  - Xerosic's Machinations, Judge, Hand Trimmer, Team Rocket's Bother-Bot;
  - Pokémon Catcher; Budew's Itchy Pollen.
- **2026-10-27, Energy in place of Energy cards** (`energy_search`,
  `energy_recursion`, `energy_shuffle_from_discard`,
  `energy_salvage_on_ko`): Energy Search, Energy Retrieval, Night
  Stretcher, Energy Recycler, Waitress, Huntail's Diver's Catch
  (Water-type only; Kangaskhan is Colorless), Snorlax's Gormandizer.

**Anti-synergies:**
- Tundra Wall needs Water Energy on the Pokémon it covers. A Kangaskhan
  powered by anything else isn't covered.
- Neutralization Zone and Lively Stadium compete with Fossil Quarry for
  the Stadium.
- Mega Abomasnow ex's Hammer-lanche mills your deck in a deck built to go
  long.
- Bouffalant ex isn't a "Bouffalant" for Curly Wall.
- Jumbo Ice Cream heals only an Active with 3 or more Energy: Articuno
  after one Frigid Fluttering doesn't qualify.
- Good Sleep wants Snorlax left Asleep; Switch, which this list needs,
  wakes it.

## 1000-trial setup baseline

With the baseline's Fossil fix (bbf7b1b). Unseeded, so about ±1.5 between
runs.

| Pokémon | 2026-10-26 list, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Antique Sail Fossil | 85.1% | 85.8% | 1.96 |
| Amaura | 51.9% | 53.5% | 3.55 |
| Aurorus | 52.9% | 54.4% | 3.97 |
| Articuno | 82.4% | 83.6% | 2.02 |
| Mega Kangaskhan ex | 74.4% | 75.6% | 1.65 |
| Bouffalant ex | 53.0% | 52.3% | 2.12 |

First attack by turn 6: **98.3%** of trials (average turn 2.78), against
99.9% (2.68) with 27 Energy. Crushing Hammer and Jumbo Ice Cream do
nothing in this simulator (no opponent, no damage).

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape)
  (`check_energy_support.py`).
- Every attack is payable with Water Energy (Kangaskhan's and Bouffalant
  ex's cost Colorless). No Ability gates an attack.
- **9 Basics: a 30.0% mulligan.** Fossils don't count. A 4th Articuno for
  an Energy measured −0.46.
- The card file's legality flags (fetched 2026-09-24) mark Perfect Order
  cards as not yet Standard: Amaura, Aurorus, Antique Sail Fossil and
  Poké Pad POR here. That looks like the snapshot predating the set's
  Standard date; check it in PTCGL.

**Real lists:** no Aurorus / Kangaskhan list was found, and no Aurorus
list with Jumbo Ice Cream or Crushing Hammer (searched 2026-10-27). The
public Aurorus decks pair it with Antique Sail Fossil, Amaura, Rare Candy
and Poké Pad, as this one does. Most also run Boss's Orders; this list
cut it and Night Stretcher for 2 Poké Pad (+1.31, rounds 5-6 above):
- [pokemoncard.io: Aurorus (Perfect Order) decks](https://pokemoncard.io/category/pokemon/aurorus-me3-24)
- [pokemoncard.io: Aurorus (Perfect Order 92) decks](https://pokemoncard.io/category/pokemon/aurorus-me3-92)

**The Fossil rule:** no published ruling on Antique Fossils at setup or
with Pokémon searches was found. The Rulings Compendium answers a related
question for Antique Dome / Helix Fossil: in hand it is an Item, and can't
be used as a Pokémon.
- [Pokémon Rulings Compendium: Antique Dome Fossil](https://compendium.pokegym.net/category/5-trainers/antique-dome-fossil/)
- [Bulbapedia: Antique Sail Fossil](https://bulbapedia.bulbagarden.net/wiki/Antique_Sail_Fossil_(TCG))

## PTCGL import

```
Pokémon: 14
2 Amaura POR 23
3 Aurorus POR 24
3 Articuno JTG 161
4 Mega Kangaskhan ex MEG 104
2 Bouffalant ex WHT 162

Trainer: 25
4 Antique Sail Fossil POR 69
2 Fossil Quarry PBL 76
4 Rare Candy MEG 125
4 Lillie's Determination MEG 119
2 Switch MEG 130
1 Hero's Cape TEF 152
2 Poké Pad POR 113
2 Jumbo Ice Cream PFL 91
4 Crushing Hammer POR 71

Energy: 21
21 Basic Water Energy

Total Cards: 60
```
