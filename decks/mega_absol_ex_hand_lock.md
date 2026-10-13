# Mega Absol ex Hand Lock

Built 2026-10-13 for the brief "the most annoying, fastest disruption deck
possible: devolution, hand disruption".

**71.34% against the 88-deck field at 1000 games per opponent** (median
75.6%, 77 of 88 winning). That is **+18.52 ± 0.71** (better on all 88)
over the same deck with an Espathra devolution package (52.82%).

**Lines:** Mega Absol ex, Budew.

## Plan

Every turn costs the opponent something:
- **Turn 1:** **Budew**'s Itchy Pollen costs no Energy. Your opponent can't
  play Items during their next turn: no Ultra Ball, Buddy-Buddy Poffin,
  Rare Candy or Switch.
- **Every attack:** **Mega Absol ex** (Basic, 280 HP) uses **Claw of
  Darkness** (DDC): 200 damage, then your opponent reveals their hand and
  you discard the card you want. Usually their Supporter.
- **Supporters:** **Xerosic's Machinations** cuts their hand to 3, and
  **Eri** strips 2 Items from it. **Unfair Stamp**, after one of your
  Pokémon is Knocked Out, leaves them 2 cards against your 5.
- **Speed:** **Janine's Secret Art** puts a Darkness Energy on each of two
  Mega Absol ex, so Claw of Darkness is ready on turn 2.

## How to play

1. **Setup.** Lead with Budew if you have it (no Retreat Cost).
2. **Turn 1.**
   - If you go second, Itchy Pollen.
   - Play Janine's Secret Art on your Benched Mega Absol ex. Energy it puts
     on your **Active** Pokémon Poisons it, so aim it at the Bench.
   - Or play Xerosic's if their hand is big.
   - If you go first you can't attack: just set up.
3. **Opponent's turn.** No Items. They still have their Supporter and
   Abilities, so draw Supporters and draw Abilities are their way out.
4. **Turn 2.** Retreat Budew for free and Claw of Darkness: 200, plus their
   best card. From here, Claw every turn. Xerosic's first means you're
   picking from 3 cards, and Eri makes sure the Item you take isn't the
   last search card.
5. **Boss's Orders** (2) brings up something Claw can Knock Out.

**Its weaknesses:**
- Mega Absol ex is **weak to Grass**, so it loses badly to Arboliva ex /
  Teal Mask Ogerpon ex (11.2%), Lurantis (33.6%) and Hydrapple (41.3%).
- It also loses to the fast Cinderace decks: Mega Zeraora ex 14.9%, Mega
  Zygarde ex 32.5% and 45.0%.
- 6 Basics is a 45.9% mulligan rate. Adding Budew didn't help (−0.10).

**Matchups (1000 games):**
- **Worst:** Arboliva / Ogerpon 11.2%, Mega Zeraora ex 14.9%, Mega Zygarde
  ex 32.5%, Lurantis 33.6%, Maushold mill 37.1%, N's Zoroark 38.7%.
- **Best:** Arbok / Yveltal 96.3%, Mew / Pikachu box 96.0%, Mew baby box
  94.8%, Wobbuffet / Orbeetle 94.7%, Mew / Hypno 94.4%.

## What about devolution?

The pool's devolution cards, all measured:
- **Espathra** (Mystical Eyes, one Colorless Energy: devolve 1)
- **Espeon** (Miraculous Shine: devolve every evolved Pokémon)
- **Claydol** (Devolution Ray)
- **Archeops** (Ancient Wing: an Ability, a devolve every turn while it's
  Active)

**All of them cost more than they disrupt**, because they spend the attack
(or the Active Spot) on 0 damage. 200 games against the field each:

| Build | Win rate |
|---|---|
| Gothitelle hand lock + Espathra devolution | 25.45% |
| Espeon devolution + Espathra | 23.02% |
| Archeops (fossil) devolution + Espathra | 27.97% |
| Mega Absol ex + 3-3 Espathra | 52.81% |
| Mega Absol ex, Espathra cut | 68.55% (**+15.74 ± 0.79**) |
| Mega Absol ex, Espathra cut, then a 1-1 Espathra added back | 63.05% (−5.51 ± 0.45) |

Devolution is strongest as a finisher: a damaged evolved Pokémon whose lower
Stage has less HP than its damage is Knocked Out. The Absol deck already
takes those with Claw of Darkness itself.

## What the simulator found

Five engine fixes (2026-10-12/13), each with a regression test that fails
on the previous commit:
- **"Devolve 1 of your opponent's evolved Pokémon"** devolved every evolved
  Pokémon. It is now one, the player's pick, a Knock Out first. Claydol's
  Devolution Ray now targets only the Active, as printed.
- **A devolved Rare Candy Stage 2 became its printed Stage 1**, not the
  Basic actually under it (Hydreigon ex → Zweilous instead of Deino). It
  crashed the run against a deck without that Stage 1.
- **Claw of Darkness** (and Luxray ex's Piercing Gaze) compiled to the
  reveal alone and never discarded anything.
- **Gothitelle's Distorted Future** put the hand on the bottom of the deck
  where the card says shuffle. It also fired on a 1-card hand, giving the
  opponent two more cards. The guard measured +2.22 ± 0.51.
- **Archen** "evolves from Antiuqe Plume Fossil" in the card data, so the
  Archeops line could never reach play.

## How it was tuned

200 games against each of the 88 field decks, paired on the same seeds.
Each round is paired against the best list of the round before. Lists
and results are in `runs/2026-10-13/disruption_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Mega Absol ex + 3-3 Espathra + Budew | 52.81% | |
| 1 | 2 Scraggy (−2 Hand Trimmer) | 49.64% | −3.16 ± 0.54 |
| 1 | −1 Unfair Stamp / −2 Iris's / −2 Budew, +Energy | 54.0-54.4% | +1.2 to +1.6 |
| 1 | −1 Eri / −1 Xerosic's, +1 Energy | 54.8% | +1.95 / +2.00 |
| 1 | −2 Hand Trimmer, +2 Energy | 56.77% | +3.97 ± 0.57 |
| 1 | 2-2 Espathra (+2 Energy) | 58.43% | +5.62 ± 0.57 |
| 1 | Scraggy / Mega Scrafty ex for Espathra | 58.76% | +5.95 ± 0.73 |
| 1 | **No Espathra: +4 Energy, +2 Janine's Secret Art** | **68.55%** | **+15.74 ± 0.79** |
| 2 | 1-1 Espathra back in (−2 Energy) | 63.05% | −5.51 ± 0.45 |
| 2 | 2-2 Scraggy / Mega Scrafty ex | 66.50% | −2.05 ± 0.60 |
| 2 | No Budew (+2 Energy) | 67.22% | −1.34 ± 0.58 |
| 2 | 4 Budew (−2 Hand Trimmer) | 68.45% | −0.10 ± 0.44 |
| 2 | −1 Eri / −1 Xerosic's, +1 Energy | 69.8% / 70.2% | +1.20 / +1.62 |
| 2 | **−2 Hand Trimmer, +2 Energy** | **70.49%** | **+1.94 ± 0.44** |
| 3 | −2 Iris's / −1 Xerosic's / −1 Eri / −Unfair Stamp, +Energy | 70.3-71.1% | −0.21 to +0.57 |
| 3 | **−1 Team Rocket's Petrel, +1 Energy (this list)** | **71.60%** | **+1.11 ± 0.47** |
| 1000 games | Espathra start / round 2 / **this list** | 52.82% / 70.38% / **71.34%** | **+18.52 ± 0.71** |

Round 3's other cuts measured within noise. The disruption cards stay
because they are the deck you asked for, and none of them measured as
clearly costing games: 4 Xerosic's, 2 Eri, 2 Budew, Unfair Stamp.

Logged against six hard opponents (Raging Bolt, Dragapult, Raticate, N's
Zoroark, Tauros, Lurantis), it won 28 of 60. Per game it used Claw of
Darkness 3.4 times, Xerosic's 1.3, Janine's 1.3, Itchy Pollen 0.9 and Eri
0.7.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Mega Absol ex | 94.2% | 1.39 |
| Budew | 92.4% | 1.63 |

First attack by turn 6 in 99.4% of games (average turn 2.15). The baseline
doesn't model Eri, Unfair Stamp or Iris's Fighting Spirit.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Unfair Stamp).
Every attack is payable with Darkness Energy. 6 Basics, 45.9% mulligan.

## PTCGL import

```
Pokémon: 6
4 Mega Absol ex MEG 161
2 Budew ASC 16

Trainer: 33
4 Lillie's Determination MEG 119
4 Xerosic's Machinations SFA 64
2 Eri TEF 146
4 Janine's Secret Art SFA 59
2 Iris's Fighting Spirit ASC 190
1 Team Rocket's Petrel ASC 207
2 Boss's Orders MEG 114
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
1 Mega Signal MEG 121
2 Night Stretcher MEG 173
2 Switch MEG 130
1 Unfair Stamp TWM 165

Energy: 21
21 Basic Darkness Energy

Total Cards: 60
```
