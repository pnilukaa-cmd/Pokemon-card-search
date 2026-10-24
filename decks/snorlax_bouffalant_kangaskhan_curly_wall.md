# Snorlax / Bouffalant / Mega Kangaskhan ex: the Curly Wall

Reviewed 2026-10-23 from a submitted list: 4 Snorlax (30C), 4
Bouffalant, 2 Munkidori, 2 Smoochum, Tatsugiri and Lillie's Clefairy ex on
8 Psychic and 3 Darkness Energy, with Heavy Baton, Sacred Charm, Lively
Stadium, Kofu, Crispin, Team Rocket's Petrel and Poké Pad.

**This list: 87.10% against the 95-deck field at 1000 games per opponent**
(median 92.0%, 92 of 95 winning), on the engine as of f01e13e. On the same
seeds it is **+22.22 ± 1.47** over the submitted list (64.89%), better on
93 of 95.

**The changes:**
- **+4 Mega Kangaskhan ex**, −1 Snorlax, −1 Tatsugiri.
- **+7 Energy** (13 Psychic, 5 Darkness).
- **Out:** 2 Team Rocket's Petrel, 2 Boss's Orders, 2 Sacred Charm, 2 Poké
  Pad, Jasmine's Gaze.

The submitted list measured 52.93% before the Switch fix below and 64.89%
after it.

**One caution on the number.** The field's AI aims Boss's Orders at the
Benched Pokémon with the least HP left, not at a Bouffalant to switch
Curly Wall off. A real opponent will, so treat 87% as the ceiling.

## The strategy, card by card

**Two Basic Colorless attackers behind one wall.**
- **Bouffalant** (SCR 119, 100 HP): Curly Wall. While you have another
  Bouffalant in play, all your Basic Colorless Pokémon take 60 less
  damage from attacks. It doesn't stack, so two Bouffalant are the whole
  effect, and it covers Snorlax and Bouffalant. Boundless Power (CCC) does
  130 and can't be used again next turn.
- **Snorlax** (30C 119, 160 HP, Retreat 4): Collapse (CCC) does 130 and
  puts Snorlax to sleep. Good Sleep: if it stays Asleep through Pokémon
  Checkup, heal all its damage.
- **Lively Stadium:** every Basic Pokémon in play gets +30 HP, theirs too.
  Snorlax is 190 behind a 60-point wall; Bouffalant 130.

**The loop:** Snorlax attacks for 130 and falls asleep. Their hit comes in
60 lighter. At Checkup a tails keeps it Asleep and heals it to full. On your
turn it can't attack or retreat, so Switch brings in the other attacker
(Switch clears Asleep), and the healed Snorlax waits on the Bench.

**Support:**
- **Munkidori** (110 HP): Adrena-Brain moves up to 3 damage counters
  from one of your Pokémon to one of theirs, but only with a Darkness
  Energy attached. That is what the 3 Darkness Energy are for.
- **Heavy Baton:** when a Pokémon with Retreat Cost exactly 4 is Knocked
  Out in the Active Spot, up to 3 Basic Energy move to the Bench. Only
  Snorlax qualifies.
- **Smoochum** (30 HP, free retreat): Delightful Kiss (free) attaches 2
  Basic Psychic Energy from the deck to a Benched Pokémon.
- **Crispin:** two Basic Energy of different types, one to hand and one
  attached. With Psychic and Darkness, it gets both.
- **Tatsugiri:** Attract Customers looks at the top 6 for a Supporter
  while Active.
- **Lillie's Clefairy ex:** Fairy Zone makes their Dragon Pokémon weak
  to Psychic.

**Anti-synergies:**
- **Air Balloon on Snorlax** takes its Retreat Cost to 2, so Heavy Baton
  (exactly 4) no longer fires. Both are Tools, so a Snorlax holds one
  anyway.
- **Lively Stadium** gives their Basics +30 too.
- **Boundless Power** locks itself for a turn.
- **Curly Wall needs two Bouffalant in play.** A Boss's Orders on one
  turns it off.
- **Snorlax and Bouffalant are weak to Fighting.**

## What the measurements say

**The list as submitted runs short of Energy,** like the Mega Dragonite
list before it. Eleven Energy feed three attackers that each want three,
Munkidori's Darkness, and Heavy Baton. Measured in game
(`energy_curve.py`, 10 games against each field deck, end of your turn
3): the Active could pay its attack 74.7% of the time, with 0.51 Energy
cards left in hand; with four more Energy, 80.7% and 0.94. In round 1
almost every card turned into a Psychic Energy won (paired, 200 games a
matchup, against the submitted list):

| Change | Measured |
|---|---|
| −2 Switch, +2 Energy | +7.94 (before the Switch fix below) |
| −2 Petrel, −2 Kofu, +4 Energy | +7.88 |
| −2 Boss's Orders, +2 Energy | +6.86 |
| −2 Petrel, +2 Energy | +5.68 |
| −2 Sacred Charm, +2 Energy | +5.19 |
| −1 Tatsugiri, +1 Energy | +4.11 |
| −3 Lively Stadium, +3 Energy | +3.88 |
| −1 Energy Recycler, +1 Energy | −0.25 |

**Then the Switch fix changed the picture.** The engine played Switch the
moment it was drawn, into the healthiest Benched Pokémon: a Snorlax with
three Energy, awake and attacking, was swapped for a Munkidori with none.
Fixed, the submitted list went from 52.93% to 65.33% (+12.39 ± 0.71 on the
same seeds), and cutting Switch for Energy fell from +7.94 to +1.30. Switch
is what gets an Asleep Snorlax out: it can't retreat while it sleeps.

**Then Mega Kangaskhan ex.** The Curly Wall precedent in this project's
notes is a Colorless tank squad: Mega Kangaskhan ex and Bloodmoon Ursaluna
ex behind two Bouffalant and Lively Stadium. Mega Kangaskhan ex (MEG 104)
is a Basic Colorless Pokémon, so both apply.
- 300 HP, 330 under Lively Stadium, and it takes 60 less from every hit.
- Rapid-Fire Combo (CCC) does 200, plus 50 for each heads until tails.
- Run Errand draws 2 while it's Active.
- It gives up 3 Prizes.

Two copies measured +6.64 ± 0.87, four +3.34 more.

## Tuning, round by round

All against the 95-deck field, paired on the same seeds within a tag, 200
games a matchup. Tags: sx1 (d6f6f1c), hp1 (a569a0d: Switch), hp2
(f01e13e).

| Round | Base | What won | Result |
|---|---|---|---|
| 1 (sx1) | submitted, 52.46% | every cut for Energy but Energy Recycler (table above) | |
| 2 (hp1) | submitted, 65.16% | −2 Petrel, −2 Kofu, −2 Boss's Orders, −2 Sacred Charm, +8 Psychic (−2 Switch as well: +8.49) | 74.14% (hp2) |
| 3 (hp2) | 74.14% | −1 Tatsugiri +2.07; 2 Kofu back for 2 Energy +1.18; 5 Darkness +0.89 | combined: 77.47% |
| 4 (hp2) | 77.47% | +2 Mega Kangaskhan ex, −1 Poké Pad, −1 Jasmine's Gaze: +6.64 | 84.11% |
| 5 (hp2) | 84.11% | 4 Mega Kangaskhan ex, 3 Snorlax, −1 Poké Pad: +3.34 | **87.45%** |
| 6 (hp2) | 87.45% | nothing: 3rd Crispin +0.23, 2 Snorlax −0.01, 3 Bouffalant −0.54, no Snorlax −0.58 | kept |

What stayed, and why:
- **Smoochum.** Cutting both was −3.93, the largest loss in round 3.
- **Crispin.** Cutting both was −1.86: with Psychic and Darkness it finds one of each.
- **Switch.** −0.63 to cut two once Switch was fixed: it's the way out for an Asleep Snorlax.
- **Kofu.** 2 back for Energy was +1.18; cutting them again in round 4 was −1.17.
- **Heavy Baton, Lively Stadium, Lillie's Clefairy ex, Jasmine's Gaze**
  were all within ±0.3 of an Energy in round 3. Gaze went for Kangaskhan.
- **Bloodmoon Ursaluna ex:** −0.57. Blood Moon costs five, less one per
  Prize they've taken, and can't attack twice in a row.
- **Snorlax is now the small part.** Three copies measured the same as
  none (−0.58 to cut all three with the Heavy Batons). Good Sleep still
  heals all damage, but Kangaskhan and Bouffalant do the attacking.

## What the simulator found

Engine fixes, each with a regression test that fails on the commit
before:
1. **Curly Wall protected nothing** (e8b2d1a). It read "Basic Colorless" as
   a card name. Its "at least 1 other Bouffalant" condition and
   no-stacking were dropped too.
2. **Lively Stadium's +30 HP went on the Stadium itself** (e8b2d1a).
3. **Attract Customers took the top card, whatever it was** (e8b2d1a).
4. **Heavy Baton crashed the game** when its holder was Knocked Out
   (e8b2d1a). It now moves only Basic Energy.
5. **Seventeen Tools were never attached**, Sacred Charm and Heavy Baton
   among them (e8b2d1a).
6. **Switch was played the moment it was drawn,** into the healthiest
   Benched Pokémon (a569a0d). +12.39 here, +0.28 to +5.83 on 8 field decks.
7. **An Asleep Active was rated at its full damage** (a569a0d). Sky
   Transport and the switch-in Abilities wouldn't move it.

## How to play the final list

1. **Turn 1.** Bench two Bouffalant first: Curly Wall needs both.
   Buddy-Buddy Poffin (70 HP or less) finds only Smoochum here; Precious
   Trolley puts the rest down at once. Lively Stadium down.
2. **Turn 2.** Smoochum's Delightful Kiss puts 2 Psychic on a Benched
   Kangaskhan or Snorlax. Crispin for one Psychic and one Darkness: the
   Darkness goes on Munkidori for Adrena-Brain.
3. **Every turn after.**
   - Kangaskhan in the Active Spot: Run Errand, then Rapid-Fire Combo.
   - Munkidori moves 3 damage counters off whoever is hurt onto their
     Pokémon.
   - Snorlax's Collapse when you want the heal. Switch it out if it's
     still asleep on your turn.

**The opponent's outs:**
- **Fighting.** Snorlax, Bouffalant and Kangaskhan are all weak to it.
- **A Boss's Orders on a Bouffalant.** With one Bouffalant in play, Curly
  Wall is off. Keep three in play when you can.
- **Kangaskhan gives up 3 Prizes.** Two Knock Outs on Kangaskhan are six.
- **Ability lock** shuts off Curly Wall, Run Errand and Adrena-Brain.

## Matchups (1000 games each)

**Best:** Mew / Hypno 99.8%, Team Rocket's Arbok / Yveltal 99.6%, Mew baby
box 99.6%, Wobbuffet / Orbeetle 98.8%, Arbok / Team Rocket's Muk 98.5%.

**Worst:**

| Opponent | This list | Submitted |
|---|---|---|
| Mega Zygarde ex / Cinderace, Gaia Wave | 26.2% | 3.8% |
| Tauros, Risky Ruins | 34.8% | 35.2% |
| Arboliva / Ogerpon | 47.2% | 14.2% |
| Mega Zygarde ex / Cinderace, Turbo Flare | 50.6% | 29.9% |
| N's Zoroark toolbox | 56.3% | 24.3% |
| **Mew / Pikachu box** | **58.1%** | **85.0%** |
| Mega Gengar ex / Toxtricity | 61.3% | 32.0% |

**The two that got worse** are Tauros (−0.4) and the Mew / Pikachu box
(−26.9). The box runs Cornerstone Mask Ogerpon ex: Fighting, so it hits
everything here for Weakness, and Cornerstone Stance prevents all damage
from Pokémon that have an Ability. Snorlax, Bouffalant, Kangaskhan,
Munkidori and Clefairy ex all have one, so only Munkidori's moved damage
counters get through. Four 3-Prize Kangaskhan give it an easy race.
Fighting decks (Zygarde, Tauros) are the deck's real problem.

**The meta decks:**

| Opponent | This list | Submitted |
|---|---|---|
| Festival Lead | 97.6% | 94.9% |
| Slowking | 90.4% | 55.5% |
| N's Zoroark | 90.2% | 63.4% |
| Dragapult / Dusknoir | 90.1% | 65.1% |
| Dragapult | 88.1% | 52.8% |
| Dragapult / Blaziken | 83.2% | 51.6% |
| Raging Bolt | 82.6% | 53.6% |
| Mega Excadrill | 70.5% | 27.0% |

## Cards searched

- **Basic Colorless attackers** (Curly Wall covers them): Mega Kangaskhan
  ex, Bloodmoon Ursaluna ex, from the Curly Wall precedent in
  `references/current_meta_staples.md`.
- **Energy:** Crispin is already the best fit (two types). Energy Recycler
  measured −0.25 to cut, so it stays.
- **Other printings:** the pool carries Snorlax TWM 136 and SSP 144, and
  Bouffalant SSP 151 (130 HP, no Curly Wall).

**Anti-synergies:**
- **Air Balloon on Snorlax** takes its Retreat Cost to 2, so Heavy Baton
  (exactly 4) no longer fires.
- **Lively Stadium** gives their Basics +30 too.
- **Boundless Power** can't be used two turns running.
- **Mega Kangaskhan ex** gives up 3 Prizes behind a wall built for
  1-Prize Basics.

## 1000-trial setup baseline

| Pokémon | Submitted list, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Snorlax | 91.1% | 74.3% | 1.91 |
| Smoochum | 82.3% | 74.5% | 1.83 |
| Munkidori | 63.3% | 55.3% | 2.09 |
| Lillie's Clefairy ex | 29.1% | 29.7% | 2.03 |
| Bouffalant | 80.0% | 78.9% | 1.81 |
| Mega Kangaskhan ex | | 73.7% | 1.76 |

First attack by turn 6: **98.0%** of trials (average turn 2.65), against
86.3% for the submitted list (2.81).

In game (`energy_curve.py`, end of your turn 3): the Active can pay its
attack 87.2% of the time, against 77.5% for the submitted list, and
there are 2.13 Energy cards in hand, against 0.57.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Precious Trolley).
- Every attack is payable: Snorlax, Bouffalant and Kangaskhan cost
  Colorless, and Munkidori and Clefairy are Psychic. No Ability gates an
  attack.
- 16 Basics: a mulligan in about 10% of hands.
- **Four printings in the submitted list are from rotated sets this pool
  doesn't carry:** Energy Recycler FLI 143, Air Balloon SSH 213, Boss's
  Orders RCL 189 and Switch MEW 206. The import below uses the pool's
  printings of the same cards: Energy Recycler POR 108, Air Balloon MEG
  166, Switch MEG 130. "Basic {P} Energy MEE 13" is written as Basic
  Psychic Energy.

**Real lists:** none found with Snorlax and Bouffalant together.
Limitless shows Snorlax 30C 119 in no decklist in its main database:
- [Limitless: Snorlax 30C 119](https://limitlesstcg.com/cards/30C/119)

## PTCGL import

```
Pokémon: 16
3 Snorlax 30C 119
2 Smoochum SSP 75
2 Munkidori SFA 72
1 Lillie's Clefairy ex ASC 280
4 Bouffalant SCR 119
4 Mega Kangaskhan ex MEG 104

Trainer: 26
2 Heavy Baton TEF 151
3 Night Stretcher MEG 173
1 Energy Recycler POR 108
1 Air Balloon MEG 166
2 Buddy-Buddy Poffin TWM 223
2 Crispin PRE 171
1 Poké Pad POR 113
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 184
4 Switch MEG 130
3 Lively Stadium SSP 180
2 Kofu SCR 165

Energy: 18
13 Basic Psychic Energy
5 Basic Darkness Energy

Total Cards: 60
```


