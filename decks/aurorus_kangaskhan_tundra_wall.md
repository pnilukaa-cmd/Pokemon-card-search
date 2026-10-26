# Aurorus / Mega Kangaskhan ex: Tundra Wall

Built 2026-10-26 on request: a new deck "focused on tankiness, damage
reduction / mitigation".

**This list: 78.88% against the 97-deck field at 1000 games per opponent**
(median 85.3%, 89 of 97 winning), on the engine as of 95007af. On the same
seeds it is **+29.42 ± 1.39** over the first build (49.45%), better on 95
of 97.

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
- **Poké Pad** finds Amaura, Aurorus or Articuno.

## What the measurements say

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
field deck): 17.1% of incoming damage is taken off, 69.5 taken per
damaging hit against 83.8 before mitigation. For comparison, the
Snorlax / Bouffalant / Kangaskhan Curly Wall deck: 14.2%. Hits are counted
up to the HP the Active had left.

**Energy on the board** (`energy_curve.py`, 10 games against each field
deck):

| End of your turn | First build: Energy in play / Active can attack | This list: Energy in play / Active can attack |
|---|---|---|
| 2 | 1.93 / 45.2% | 2.30 / 18.0% |
| 3 | 2.46 / 40.1% | 3.18 / 70.6% |
| 4 | 2.80 / 46.4% | 3.83 / 74.8% |
| 6 | 3.27 / 49.3% | 5.02 / 78.8% |

Turn 2 is slower (Rapid-Fire Combo costs three), and from turn 3 the
Active can attack three turns in four. Mega Kangaskhan ex is in play by
turn 4 in 77.6% of games, Aurorus in 36.9%.

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

**The opponent's outs:**
- **Fighting.** Kangaskhan and Bouffalant ex are weak to it. The two worst
  matchups are Fighting decks: Mega Zygarde ex / Cinderace (Gaia Wave)
  15.4%, Tauros 24.2%.
- **Knock Out Aurorus.** A Boss's Orders on the Benched Aurorus (170 HP,
  weak to Metal) turns the wall off.
- **Kangaskhan gives up 3 Prizes.** Two Knock Outs on it are six.
- **Ability lock** stops Tundra Wall and Run Errand.
- **A promoted Fossil can't retreat.** After a Knock Out, don't promote a
  Fossil unless you have Switch; it can be discarded from play on your
  turn.

## Matchups (1000 games each)

**Best:** Mew baby box 99.9%, Mew / Hypno 99.7%, Team Rocket's Arbok /
Yveltal 98.0%, Mew / Bastiodon 97.3%, Wobbuffet / Orbeetle 97.1%.

**Worst:**

| Opponent | This list | First build |
|---|---|---|
| Mega Zygarde ex / Cinderace, Gaia Wave | 15.4% | 12.7% |
| Tauros, Risky Ruins | 24.2% | 43.5% |
| Arboliva / Ogerpon | 31.8% | 8.8% |
| Snorlax / Bouffalant / Mega Kangaskhan ex | 34.5% | 6.9% |
| Mega Zeraora ex / Cinderace | 37.5% | 8.8% |
| Mega Zygarde ex / Cinderace, Turbo Flare | 38.4% | 36.8% |
| N's Zoroark toolbox | 47.1% | 24.4% |
| Chesnaught / Meganium | 49.1% | 18.8% |

Tauros got worse: 43.5% to 24.2%. Weakness to Fighting is the price of
the Colorless attackers.

**The meta decks:**

| Opponent | This list | First build |
|---|---|---|
| Festival Lead | 96.1% | 84.0% |
| N's Zoroark | 84.7% | 64.4% |
| Dragapult / Dusknoir | 82.2% | 50.8% |
| Slowking | 80.5% | 47.6% |
| Dragapult | 76.6% | 39.1% |
| Dragapult / Blaziken | 76.2% | 43.0% |
| Raging Bolt | 72.9% | 46.2% |
| Mega Excadrill | 53.1% | 15.4% |

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

**Anti-synergies:**
- Tundra Wall needs Water Energy on the Pokémon it covers. A Kangaskhan
  powered by anything else isn't covered.
- Neutralization Zone and Lively Stadium compete with Fossil Quarry for
  the Stadium.
- Mega Abomasnow ex's Hammer-lanche mills your deck in a deck built to go
  long.
- Bouffalant ex isn't a "Bouffalant" for Curly Wall.

## 1000-trial setup baseline

| Pokémon | First build, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Antique Sail Fossil | 74.8% | 83.3% | 2.00 |
| Amaura | 29.7% | 42.6% | 3.51 |
| Aurorus | 29.6% | 44.5% | 3.99 |
| Articuno | 57.0% | 80.1% | 2.06 |
| Mega Kangaskhan ex | | 70.1% | 1.87 |
| Bouffalant ex | | 51.2% | 2.44 |

First attack by turn 6: **84.0%** of trials (average turn 2.94), against
68.6% for the first build.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Every attack is payable with Water Energy (Kangaskhan's and Bouffalant
  ex's cost Colorless). No Ability gates an attack.
- **9 Basics: a 30.0% mulligan.** Fossils don't count. A 4th Articuno for
  an Energy measured −0.46.
- The card file's legality flags (fetched 2026-09-24) mark Perfect Order
  cards as not yet Standard: Amaura, Aurorus, Antique Sail Fossil and
  Poké Pad POR here. That looks like the snapshot predating the set's
  Standard date; check it in PTCGL.

**Real lists:** no Aurorus / Kangaskhan list was found. The public
Aurorus decks pair it with Antique Sail Fossil, Amaura, Rare Candy and
Poké Pad, as this one does:
- [pokemoncard.io: Aurorus (Perfect Order) decks](https://pokemoncard.io/category/pokemon/aurorus-me3-24)
- [pokemoncard.io: Aurorus (Perfect Order 92) decks](https://pokemoncard.io/category/pokemon/aurorus-me3-92)

## PTCGL import

```
Pokémon: 14
2 Amaura POR 23
3 Aurorus POR 24
3 Articuno JTG 161
4 Mega Kangaskhan ex MEG 104
2 Bouffalant ex WHT 162

Trainer: 19
4 Antique Sail Fossil POR 69
2 Fossil Quarry PBL 76
4 Rare Candy MEG 125
4 Lillie's Determination MEG 119
2 Switch MEG 130
1 Hero's Cape TEF 152
2 Poké Pad POR 113

Energy: 27
27 Basic Water Energy

Total Cards: 60
```
