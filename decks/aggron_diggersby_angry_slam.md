# Aggron / Diggersby Angry Slam

Built 2026-10-13 for the question "a deck with Aggron's Angry Slam, where
you spread some damage on your own Bench with Diggersby?"

**62.06% against the 89-deck field at 1000 games per opponent** (median
63.9%, 61 of 89 winning). That is **+7.33 ± 0.43** (better on 88 of 89)
over the first build (54.73%). It is level with the existing
[Diggersby / Munkidori deck](diggersby_munkidori_earthquake.md)
(63.49%, −1.43 ± 0.67).

**The same shell with Gourgeist ex in place of Aggron is much stronger:
75.74%, +13.69 ± 0.94.** See
[gourgeist_diggersby_horrifying_rondo.md](gourgeist_diggersby_horrifying_rondo.md).

**Lines:** Aron → Lairon → Aggron (Rare Candy), Bunnelby → Diggersby.

## Plan

- **Diggersby** (Stage 1, 150 HP) uses **Earthquake** (C): 140 damage, and
  30 to each of your own Benched Pokémon.
- **Aggron** (Stage 2, 180 HP) uses **Angry Slam** (M): 50 damage for each
  of your Pokémon with any damage counters on it, Active included. A full
  board of six is 300 for one Energy.

One Earthquake damages your whole Bench, and every damaged Pokémon is
another 50 on Angry Slam. Damage the opponent does to your Active counts
too. Aggron is not an ex, so it gives up only one Prize.

## How to play

1. **Turn 1.**
   - Buddy-Buddy Poffin for Bunnelby and Aron.
   - Attach a Metal Energy.
   - You can't evolve, and Rare Candy can't be played, on your first turn.
2. **Turn 2.**
   - Evolve Bunnelby to Diggersby and Earthquake: 140, plus 30 on each of
     your Benched Pokémon.
   - Rare Candy an Aron that has been in play since last turn into Aggron.
3. **Turn 3.**
   - Switch Aggron in. Diggersby's Retreat Cost is 4, so use Switch.
   - Attach a Metal Energy and Angry Slam. Your Bench is damaged, and
     Diggersby was usually hit as the Active, so this is 250-300.
4. **After that.** Angry Slam every turn; it does no more damage to your
   own side. Go back to Diggersby only when its 140 Knocks Something Out.
   **Don't Earthquake into your own Knock Outs:** each one is a Prize for
   them. Aron and Bunnelby have 70 HP, so a third Earthquake Knocks them
   Out. Whap Down (CCC, 100) has no drawback.

**The opponent's outs:**
- Knock Aggron Out: Fire hits it for double, and 180 HP is small for a
  Stage 2.
- Attack your damaged Bench with Bench damage of their own.
- Diggersby is weak to Fighting.

**Matchups (1000 games):**
- **Worst:** Arboliva / Ogerpon 10.4%, Mega Zeraora ex / Cinderace 13.4%,
  Mega Zygarde ex / Cinderace 16.1% and 30.0%, N's Zoroark 30.6%, Mega
  Absol ex hand lock 31.6%.
- **Best:** Mew / Pikachu box 98.3%, Mew baby box 96.0%, Flygon mill
  95.3%, Chandelure wall 94.9%, Drapion 94.4%.

## What the simulator found

Two engine fixes and one pilot fix (2026-10-13), each with a regression
test that fails on the previous commit:
- **Angry Slam was a flat 50 on every board.** No count rule read "for each
  of your Pokémon that has any damage counters on it", so Aggron's attack
  never scaled at all. It now counts your damaged Pokémon, Active
  included: 0 to 300.
- **Round counted every Pokémon in play** (the same wording family):
  Seismitoad with four Bunnelby hit for 350 instead of 70. No field deck
  plays it.
- **Earthquake's own-Bench damage was free to the pilot.** It used
  Earthquake while it Knocked Out its own Bench, giving away 1.5 Prizes a
  game (one game five). Each own Knock Out now costs what taking a Prize
  is worth, and an Earthquake that hands over the last Prizes is never
  chosen. Measured: +5.41 ± 0.52 for this deck and +3.44 ± 0.57 for
  Diggersby / Munkidori. It is on by default.

Not kept: giving the Energy to a Benched Pokémon it makes ready (so Aggron
gets its Metal while Diggersby is Active). +0.07 / +0.32 alone, +0.63 ±
0.45 on top of the cost.

**Taxonomy:** Angry Slam, Raging Charge and Horrifying Rondo were tagged as
damage *producers*. They are payoffs, now tagged
`damage_scales_with_own_damaged_pokemon`.

## Cards searched

**Damage your own Bench:**
- Diggersby (Earthquake, 30 each)
- Centiskorch SSP (Billowing Heat Wave, 30 each, Fire)
- Hop's Sandaconda and Groudon (Break Ground, 20 each)
- Sandslash TWM and Landorus BLK (Earthquake, 10 each, Fighting)
- Emolga TWM (Sky Wave: 10 to every Bench, both sides)
- Girafarig, Manectric, Zarude (one Benched Pokémon)
- Risky Ruins (2 counters on each Basic benched)
- Team Rocket's Venture Bomb (2 counters on your Active on tails)
- Aron, Lairon (damage to themselves)

**Payoffs:** Aggron (Angry Slam), Gourgeist ex (Horrifying Rondo, Benched
only), Paldean Tauros (Raging Charge, Tauros only), Great Tusk (Wrathful
Charge, +80 if your Bench is damaged).

**Anti-synergies:**
- Munkidori, Cofagrigus and Ninetales CRI *move* damage off your Pokémon,
  and Angry Slam counts damaged Pokémon. Moving all 3 counters off a
  Pokémon with 30 damage costs 50.
- Any healing.
- Hippowdon's Super Sandstorm and Raichu's Collateral Bolts hit every
  damaged Benched Pokémon, yours included.

**Measured out:**
- Risky Ruins: −5.02 for three, −1.85 for one. Its 20 makes Earthquake
  Knock Out your 70 HP Basics a turn sooner.
- Emolga's Sky Wave: −5.88.
- Team Rocket's Venture Bomb: −3.52 ± 0.49 for three (in place of Poké Pad).

## How it was tuned

200 games against each of the 89 field decks, paired on the same seeds.
Each round is paired against the best list of the round before. Lists and
results are in `runs/2026-10-13/angry_slam_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Diggersby + 3 Risky Ruins (A) | 54.78% | |
| 0 | No Diggersby: Risky Ruins + Emolga | 50.26% | |
| 0 | Diggersby, Venture Bomb for Ruins | 53.98% | |
| 1 | 2 Emolga (−2 Poké Pad) | 48.89% | −5.88 ± 0.55 |
| 1 | −2 Energy | 49.93% | −4.84 ± 0.57 |
| 1 | No Lairon (4th Aggron) | 49.97% | −4.80 ± 0.51 |
| 1 | −2 Iris's / 4th Switch / 3rd Boss's | 52.3-52.7% | −2.1 to −2.5 |
| 1 | 4th Aggron, 4th Diggersby, +2 or +3 Energy for Poké Pad, −Hero's Cape | 54.8-55.8% | −0.01 to +1.02 |
| 1 | 3 Bunnelby, 2 Diggersby, +2 Energy | 56.60% | +1.83 ± 0.49 |
| 1 | 1 Risky Ruins, +2 Energy | 57.94% | +3.16 ± 0.54 |
| 1 | −2 Air Balloon, +2 Energy | 58.75% | +3.97 ± 0.53 |
| 1 | **No Risky Ruins, +3 Energy** | **59.80%** | **+5.02 ± 0.54** |
| 2 | 1 Risky Ruins back | | −1.85 ± 0.50 |
| 2 | Others (Poké Pad, Lairon, Aggron, Petrel, Cape, Bunnelby/Diggersby) | | −1.19 to +0.87 |
| 2 | **−2 Air Balloon, +2 Energy (this list)** | **62.12%** | **+2.33 ± 0.47** |
| 3 | 2nd Lairon, 4th Aggron, ±1 Energy, −Night Stretcher, −Petrel, −1 Bunnelby, −1 Diggersby | 60.9-62.4% | −1.21 to +0.29 |
| 1000 games | First build / **this list** | 54.73% / **62.06%** | **+7.33 ± 0.43** |

**What made the difference:** fewer things that hurt your own Basics, and
Energy. Risky Ruins and Earthquake together Knock Out your own 70 HP
Basics. Retreating Diggersby (4) and Aggron (3), plus Guard Claw and Whap
Down (3 each), all want Energy.

Logged against random field opponents, it won 37 of 60. Per game it used:
- Earthquake 2.7 times, Angry Slam 0.9, Whap Down 0.7, Guard Claw 0.1.
- Its own Earthquake Knocked Out 0.7 of its Pokémon per game, down from
  1.5 before the pilot fix.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Aron | 98.9% | 1.35 |
| Lairon | 68.6% | 2.87 |
| Aggron | 52.9% | 3.83 |
| Bunnelby | 97.8% | 1.41 |
| Diggersby | 76.4% | 3.00 |

First attack by turn 6 in 98.2% of games (average turn 2.78). The baseline
doesn't model Iris's Fighting Spirit. **Aggron arrives late:** it is a
Stage 2 that needs Rare Candy, which is the main reason Gourgeist ex (a
Stage 1) does better here.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Every attack is payable with Metal Energy, and no Ability gates an
  attack.
- 8 Basics, 34.6% mulligan.

No published list for this pairing was found. The web had card pages only,
plus community Aggron decks on PokemonCard.io, mostly Expanded.

## PTCGL import

```
Pokémon: 15
4 Aron TWM 120
1 Lairon TWM 121
3 Aggron TWM 122
4 Bunnelby POR 64
3 Diggersby POR 65

Trainer: 30
4 Lillie's Determination MEG 119
2 Iris's Fighting Spirit ASC 190
2 Boss's Orders MEG 114
1 Team Rocket's Petrel ASC 207
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Rare Candy MEG 125
3 Poké Pad ASC 198
3 Switch MEG 130
2 Night Stretcher MEG 173
1 Hero's Cape TEF 152

Energy: 15
15 Basic Metal Energy

Total Cards: 60
```
