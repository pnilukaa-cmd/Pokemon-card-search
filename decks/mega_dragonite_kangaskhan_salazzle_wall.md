# Mega Dragonite ex / Mega Kangaskhan ex / Salazzle ex: the wall

Reviewed 2026-10-23 from a submitted list: Mega Dragonite ex, Mega
Kangaskhan ex and Salazzle ex on 6 Fire Energy, with Crushing Hammer,
Handheld Fan, Budew, Gravity Gemstone, Battle Cage and 4 Wally's
Compassion. The question was what the strategy is.

**This list: 71.61% against the 94-deck field at 1000 games per opponent**
(median 74.5%, 82 of 94 winning), on the engine as of e8b2d1a. On the same
seeds it is **+26.21 ± 1.32** over the submitted list (45.39%), better on
93 of 94.

The submitted list measured 20.68% before the engine fixes below and 45-47%
after them; the list changes took it the rest of the way. (It was tuned on
the engine one step earlier, where the same pair measured 72.30% and
46.84%; the type-aware Energy fix since then made the field's multi-type
decks stronger.)

## The strategy, card by card

**Mega Dragonite ex can't attack in this deck.** Ryuno Glide costs Water,
Lightning, Lightning, and the deck runs only Fire Energy. Dratini's and
Dragonair's attacks need Water and Lightning too. What the line is for:
- **A wall.** 370 HP, no Weakness, 470 with Hero's Cape.
- **A free pivot.** Sky Transport (Ability, once a turn): switch your
  Active Pokémon with one of your Benched Pokémon.
- **A free heal.** Wally's Compassion heals all damage from a Mega
  Evolution Pokémon ex and puts its Energy into your hand. Dragonite has
  no Energy worth keeping, so on Dragonite it costs nothing.
- **Dragonair's Evolutionary Guidance** searches an Evolution Pokémon, but
  only with an Energy attached to it.

**The damage comes from two places:**
1. **Mega Kangaskhan ex** (300 HP): Rapid-Fire Combo (CCC) does 200, plus
   50 for each heads until tails: 250 on average. Run Errand draws 2 while
   it's Active.
2. **Salazzle ex** (260 HP): Dire Nails (RR) does 100, Burns and Poisons
   their Active, and then switches Salazzle ex to your Bench. Nasty Plot
   (R) searches any 2 cards.

**The loop the list is built around:**
1. Sky Transport switches the attacker in: Salazzle ex with RR, or
   Kangaskhan with CCC. If Kangaskhan comes in, Run Errand draws 2 first.
2. Dire Nails: 100, Burned and Poisoned, then Salazzle goes to the Bench.
   The Pokémon that comes in to take their attack is the one with the most
   HP left: Mega Dragonite ex.
3. Their turn: they face 370 HP with Burn and Poison ticking between turns
   (Poison 10; Burn 20 and a coin flip to recover).
4. Your turn: Wally's Compassion heals the Dragonite for free, and Sky
   Transport brings the attacker back.

**The control half,** as submitted:
- Crushing Hammer ×4: a coin flip to discard an Energy.
- Handheld Fan ×2: when the holder is hit in the Active Spot, an Energy
  moves off the attacker to their Bench.
- Budew: Itchy Pollen (free) stops Items for a turn.
- Gravity Gemstone: both Actives' Retreat Cost +1 while it's Active, so
  their Burned and Poisoned Pokémon is harder to get out.
- Battle Cage: no damage counters on either Bench from attacks and
  Abilities (Phantom Dive, Dragapult's spread).
- Nighttime Mine: Tera Pokémon's attacks cost one more.
- Ciphermaniac's Codebreaking puts 2 cards on top of the deck. Run Errand
  then draws them.

## What the measurements say

**The list as submitted runs out of Energy.** Six Fire Energy feed
Kangaskhan's CCC, Salazzle ex's RR, the Energy Dragonair needs for its
search, and whatever Wally's Compassion sends back to the hand. In logged
games most turns without an attack had no Energy in hand, and the deck
attacked about twice a game. Every card turned into an Energy won, and the
control cards measured no better than the Energy that replaced them.

| Change | Measured (200 games a matchup, paired) |
|---|---|
| +6 Energy for 2 Pokégear, 2 Ciphermaniac's, 2 Battle Cage | **+18.55 ± 1.18** |
| −1 Gravity Gemstone, −2 Handheld Fan, −2 Wally's Compassion, +5 Energy | +4.05 ± 0.58 |
| −2 Boss's Orders, +2 Energy | +1.51 ± 0.45, then +1.38 ± 0.37 |

What stayed, and why:
- **The Dragonite line.** Cutting it for 8 Energy and a 3rd Salandit and
  Salazzle ex measured −1.06 against the 12-Energy list. It's a wall and a
  pivot, and both matter.
- **Crushing Hammer.** Cutting all four for Energy was +1.77 at 12 Energy
  but −0.10 at 17: by then they're as good as an Energy.
- **2 Wally's Compassion, Budew, Nighttime Mine, 3 Kangaskhan,** each
  within ±0.8 of an Energy at the end.

**Giving Dragonite its attack doesn't pay here.** 3 Lightning and 2 Water
in place of 5 Fire, so Ryuno Glide (330) is payable, measured **−4.66 ±
0.49** on the current engine (worse on 78 of 94). Water, Lightning and
Lightning on one Pokémon rarely come together without Eelektrik's
Dynamotor, and every off-type Energy is one Salazzle ex and the
Kangaskhan can't use as well. The first measurement, −22.80, was mostly
the AI's fault: it put Fire Energy on Dragonite, where it pays nothing.
That is engine fix 5.

**Boss's Orders measured below an Energy,** twice. My reading, not a
measurement: the plan stacks Burn and Poison on their Active, and a fresh
Pokémon dragged up starts clean.

## How to play the final list

1. **Turn 1.** Poffin for Salandit and Dratini (Budew too). Mega
   Kangaskhan ex is a fine opener: Run Errand draws 2 every turn it's
   Active.
2. **Turn 2.** Evolve Salandit; Rare Candy a Dratini into Mega Dragonite ex
   (not on your first turn, and not on a Dratini played this turn). Load
   Kangaskhan or Salazzle.
3. **Every turn after.**
   - Sky Transport whoever can attack into the Active Spot. Don't switch
     for its own sake: a Kangaskhan with no Energy in the Active Spot does
     nothing.
   - Kangaskhan's Rapid-Fire Combo for the Knock Outs; Salazzle ex's Dire
     Nails to Burn and Poison and get out.
   - Wally's Compassion on the Dragonite, or on a Kangaskhan only to save
     it from a Knock Out: it puts all its Energy back in your hand.

**The opponent's outs:**
- **Kangaskhan is weak to Fighting** (Salazzle ex and Salandit to Water).
  Dragonite has no Weakness.
- **Three Megas on the Bench are 9 Prizes.** A Boss's Orders on a Benched
  Kangaskhan with no Energy is their cleanest 3.
- **Ability lock** shuts off Sky Transport and Run Errand, and the deck
  falls back to retreating.
- **Their own heals or switching** undo Burn and Poison.

**Matchups (1000 games, current engine):**
- **Worst:** Mega Zygarde ex / Cinderace 16.7% (Fighting, Kangaskhan's
  Weakness) and 40.9%, Mega Zeraora ex / Cinderace 33.3%, Arboliva /
  Ogerpon 35.3%, Munkidori ex / Pecharunt ex 35.9%, Mega Gengar ex /
  Toxtricity 37.4%, N's Zoroark 39.3%, Maushold mill 40.9%.
- **Best:** Mew baby box 98.9%, Mew / Hypno 96.6%, Drapion and Team
  Rocket's Wobbuffet 94.2%, Vileplume ex 94.1%.
- Against the field's meta lists: Dragapult ex 67.3%, Raging Bolt 62.4%.

## What the simulator found

Five engine changes, each with a regression test that fails on the
commit before:
1. **Sky Transport switched to the healthiest body, not the attacker.** It
   compiled like Dire Nails' "switch this Pokémon out". Two Dragonite
   switched back and forth 13 times a game, and a loaded Salazzle ex or
   Kangaskhan on the Bench rarely came up. It now brings up the Benched
   Pokémon that does the most this turn, and only if that beats the
   Active. **20.68% → 44.05%** on the submitted list (+23.37 ± 1.46). Two
   Abilities that switch themselves in from the Bench (Meowscarada's
   Showtime, Linoone's Excited Dash) now do.
2. **"Heal ... from 1 of your Pokémon" healed every Pokémon you had.**
   Wally's Compassion healed the whole board, Mega or not, and returned no
   Energy. 26 heal effects in all were wrong: Potion, Super Potion and
   Jacinthe healed everything too, others dropped who they heal (Psychic
   only, Basic only, 30 HP or less remaining) or what the heal costs
   (discard the Energy).
3. **Evolutionary Guidance ran with no Energy on Dragonair** (and Regirock's
   Rock Armor with none on Regirock).
4. **Wally's Compassion went on whatever was most damaged,** often a
   Kangaskhan with three Energy that wasn't in danger. The AI now heals a
   Pokémon with no Energy to lose first, and one with Energy only when it
   would otherwise be Knocked Out next turn. +2.43 ± 0.52 on the submitted
   list, +2.54 on the 12-Energy list; noise on the two field decks it
   touches.
5. **The AI attached Energy by count, not type.** Any Energy went to the
   hardest hitter still short a number of Energy, so in the Ryuno Glide
   test Fire went onto Dragonite. It now goes where the Energy in hand
   pays part of an attack. Measured on all 12 field decks with two or more
   Energy types: +0.23 to +14.99, none worse (the Dragapult lists +7.4 to
   +9.9).

Fixes 2, 4 and 5 change field decks too: anything with Potion, Super
Potion, Jacinthe, Comfey, Applin, Dolliv, Poké Vital A or Wally's
Compassion, and every deck with two Energy types. Their own notes keep their
older numbers until the next full field run.

## Cards searched

- **Mega Evolution support** (every card naming "Mega Evolution Pokémon"):
  Mega Signal (search a Mega Evolution ex; measured ±0 for a Pokégear),
  Linoone, Oricorio ex (needs a Fire Mega; neither Mega here is Fire),
  Seviper and Ludicolo (Darkness and Grass Megas), Tremendous Bomb, Jett.
- **Energy:** Fire acceleration in the pool comes on its own Stage 1 or 2
  lines (Emboar, Infernape, Blaziken ex). Night Stretcher is already here.

**Anti-synergies:**
- Wally's Compassion empties the healed Pokémon's Energy. Fine on
  Dragonite, three turns of attacks on Kangaskhan.
- Salandit's Ember discards its own Energy, for 30.
- Three Mega Kangaskhan ex on the Bench give up 3 Prizes each.
- Dire Nails' switch isn't optional: if your Bench is all low HP, the
  Pokémon taking the next hit is a small one.

## How it was tuned

200 games against each of the 94 field decks, paired on the same seeds.
Each round is paired against the best list of the round before. Lists and
results are in `runs/2026-10-23/dragonite_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | The submitted list, before the Sky Transport fix | 20.68% | |
| 0 | After it | 44.05% | +23.37 ± 1.46 |
| 1 | **+6 Energy for 2 Pokégear, 2 Ciphermaniac's, 2 Battle Cage** | **62.93%** | **+18.55 ± 1.18** |
| 1 | −4 Pokégear / −4 Crushing Hammer / −2 Battle Cage and Nighttime Mine / −2 Wally's, for Energy | 55.7-58.1% | +11.30 to +13.71 |
| 1 | Cut the Dragonite line for 8 Energy, a 3rd Salandit and Salazzle ex | 56.41% | +12.03 |
| 1 | −2 Ciphermaniac's / −2 Pokégear / −2 Fan / −1 Kangaskhan / −Budew, for Energy | 50.1-53.5% | +5.69 to +9.15 |
| 2 | −2 Wally's, +2 Energy | 67.10% | +4.17 ± 0.57 |
| 2 | −Gemstone / −2 Fan / −4 Hammer / −1 Kangaskhan / −Budew / −2 Pokégear, for Energy | 64.2-65.2% | +1.29 to +2.23 |
| 2 | Cut the Dragonite line / 3rd Salazzle ex / −Nighttime Mine | 61.9-63.2% | −1.06 to +0.26 |
| 2 | The cost-aware Wally's pick (engine fix 4) | 65.47% | +2.54 ± 0.51 |
| 3 | After fix 4, the singles again | 66.4-67.8% | +0.67 to +2.02 |
| 3 | **−Gemstone, −2 Fan, −2 Wally's, +5 Energy** | **69.81%** | **+4.05 ± 0.58** |
| 3 | −Gemstone, −2 Fan, with −2 Hammer / −1 Kangaskhan / alone | 68.4-69.4% | +2.67 to +3.65 |
| 4 | **−1 Boss's Orders, +1 Energy** | **71.31%** | **+1.51 ± 0.45** |
| 4 | Hammers, Pokégear, Budew, Nighttime Mine, Mega Signal, Kangaskhan, Wally's count | 69.3-70.6% | −0.47 to +0.77 |
| 4 | 3 Lightning and 2 Water for 5 Fire (Ryuno Glide); −4.66 after fix 5 | 47.01% | −22.80 ± 0.75 |
| 5 | **−the other Boss's Orders, +1 Energy (this list)** | **72.69%** | **+1.38 ± 0.37** |
| 5 | −Budew / −1 Wally's / Pokégear for an Energy | 71.3-72.0% | −0.05 to +0.67 |
| 1000 games | Submitted / round 3 / **this list** | 46.84% / 70.04% / **72.30%** | **+2.26 ± 0.29** over round 3 |
| 1000 games, current engine | Submitted / **this list** | 45.39% / **71.61%** | **+26.21 ± 1.32** |

In 60 logged games against random field opponents, it won 44. Per game:
- Rapid-Fire Combo 2.8, Dire Nails 1.5, Sky Transport 1.9, Run Errand 3.5.
- Wally's Compassion 0.5, Crushing Hammer 1.9 (0.8 heads).

## 1000-trial setup baseline

| Pokémon | Submitted list, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Salandit | 95.4% | 95.6% | 1.75 |
| Salazzle ex | 50.4% | 52.1% | 3.45 |
| Dratini | 87.4% | 86.5% | 2.08 |
| Dragonair | 52.3% | 51.8% | 3.60 |
| Mega Dragonite ex | 38.5% | 41.3% | 4.37 |
| Mega Kangaskhan ex | 69.0% | 66.9% | 1.94 |
| Budew | 65.2% | 64.0% | 2.53 |

First attack by turn 6: **98.2%** of games (average turn 2.74), against
59.2% for the submitted list (turn 3.23).

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Mega Dragonite ex, Dratini and Dragonair have no payable attack (Water
  and Lightning), as in the submitted list. Kangaskhan, Salazzle ex,
  Salandit and Budew are all payable. No Ability gates an attack.
- 10 Basics: a 25.9% mulligan.
- **Two printings in the submitted list are from Scarlet & Violet base
  (SVI), which this pool doesn't carry:** Pokégear 3.0 SVI 186 and Rare
  Candy SVI 191. The import below uses the pool's printings, Pokégear 3.0
  BLK 84 and Rare Candy MEG 125. "6 Basic {R} Energy MEE 10" is written as
  Basic Fire Energy.
- The card file's legality flags (fetched 2026-09-24) still mark Perfect
  Order cards, Salazzle ex POR 16 among them, as not yet Standard. That
  looks like the snapshot predating the set's Standard date; check it in
  PTCGL.

**Real lists:** no Mega Kangaskhan ex / Salazzle ex version found. The
published Mega Dragonite ex lists play it as an attacker, on Lightning and
Water Energy with Eelektrik's Dynamotor, and pair it with other attackers:
- [Limitless: Mega Dragonite ex City League decklists (Japan)](https://limitlesstcg.com/cards/ASC/152/decklists/jp)
- [Limitless: 10th place, City League Tokyo](https://limitlesstcg.com/decks/list/jp/52698)
- [Mega Dragonite ex deck list and guide (pairs it with Mega Kangaskhan ex)](https://www.josephwriteranderson.com/blog/mega-dragonite-ex-deck-list-and-guide)
- [Deltia's Gaming: Mega Dragonite ex deck guide](https://deltiasgaming.com/pokemon-tcg-mega-dragonite-ex-deck-guide-ascended-heroes/)

## PTCGL import

```
Pokémon: 17
3 Salandit SCR 23
3 Mega Dragonite ex ASC 152
3 Dratini ASC 150
2 Dragonair ASC 151
3 Mega Kangaskhan ex MEG 104
2 Salazzle ex POR 16
1 Budew PRE 4

Trainer: 24
4 Crushing Hammer POR 71
1 Hero's Cape TEF 152
2 Pokégear 3.0 BLK 84
2 Poké Pad ASC 198
1 Night Stretcher ASC 196
1 Nighttime Mine ASC 197
2 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination MEG 119
3 Ultra Ball MEG 131
2 Wally's Compassion MEG 132
2 Rare Candy MEG 125

Energy: 19
19 Basic Fire Energy

Total Cards: 60
```
