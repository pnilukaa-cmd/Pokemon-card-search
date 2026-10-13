# Gourgeist ex / Diggersby Horrifying Rondo

Built 2026-10-13 as the measured alternative to the
[Aggron / Diggersby Angry Slam](aggron_diggersby_angry_slam.md) deck: the
same Diggersby shell, with Gourgeist ex as the payoff instead of Aggron.

**75.74% against the 89-deck field at 1000 games per opponent** (median
79.9%, 84 of 89 winning). On the same seeds:
- **+13.69 ± 0.94** over the tuned Aggron list (62.06%), better on 83.
- **+12.26 ± 0.99** over Diggersby / Munkidori (63.49%), better on 84.
- **+3.75 ± 0.24** over its own first build (71.99%), better on 87.

**Lines:** Pumpkaboo → Gourgeist ex, Bunnelby → Diggersby. No Stage 2 and
no Rare Candy.

## Plan

- **Diggersby** (Stage 1, 150 HP) uses **Earthquake** (C): 140 damage, and
  30 to each of your own Benched Pokémon.
- **Gourgeist ex** (Stage 1, 270 HP) has two attacks:
  - **Horrifying Rondo** (P): 30, plus 50 for each of your *Benched*
    Pokémon with damage counters. Five damaged Benched Pokémon make it 280
    for one Energy.
  - **Ghostly Touch** (PP): 140, and discard a random card from your
    opponent's hand.

**Why it beats Aggron in the same shell:**
- Gourgeist ex is a Stage 1, in play by turn 6 in 75% of games. Aggron, a
  Stage 2 that needs Rare Candy, makes it in 53%.
- Its 270 HP survives where Aggron's 180 doesn't.
- When the Bench isn't damaged yet, Ghostly Touch is a strong attack by
  itself.

The cost is Prizes: Gourgeist ex is an ex and gives up two.

## How to play

1. **Turn 1.** Buddy-Buddy Poffin for Bunnelby and Pumpkaboo, and attach a
   Psychic Energy.
2. **Turn 2.** Evolve both. Earthquake with Diggersby, or Ghostly Touch if
   Gourgeist ex is Active with two Energy.
3. **After that.**
   - Once your Bench is damaged, Horrifying Rondo for one Energy. It counts
     only the **Bench**, so damage to Gourgeist ex itself adds nothing.
   - Use Ghostly Touch when Rondo is smaller than 140.
   - Don't Earthquake into your own Knock Outs. Pumpkaboo has 60 HP, so
     two Earthquakes take it.

**The opponent's outs:**
- Gourgeist ex is weak to Darkness.
- Knocking it Out is two Prizes.
- Diggersby is weak to Fighting.

**Matchups (1000 games):**
- **Worst:** Arboliva / Ogerpon 18.7%, Mega Zeraora ex / Cinderace 27.1%,
  Mega Zygarde ex / Cinderace 29.8%, Mega Absol ex hand lock 40.6%, N's
  Zoroark 42.7%.
- **Best:** Mew / Pikachu box 99.9%, Mew baby box 99.3%, Team Rocket's
  Wobbuffet 98.1%, Chandelure / Centiskorch 97.8%, Drapion 97.6%.

## How it was tuned

200 games against each of the 89 field decks, paired on the same seeds.
Each round is paired against the best list of the round before. Lists and
results are in `runs/2026-10-13/angry_slam_screens/` (`X_`, `g1_`, `g2_`).

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | The tuned Aggron list with Pumpkaboo 4 / Gourgeist ex 3 for Aron 4 / Lairon 1 / Aggron 3; Rare Candy's 4 slots to +1 Poké Pad, Switch, Boss's, Iris's, Night Stretcher; Psychic for Metal | 71.38% | +9.25 ± 1.05 vs Aggron |
| 1 | −2 Energy | 69.66% | −1.71 ± 0.40 |
| 1 | −Hero's Cape, 4th Diggersby, −1 Iris's, −1 Bunnelby | 71.2-71.7% | −0.21 to +0.33 |
| 1 | +2 Energy / −1 Boss's / 2 Risky Ruins / −1 Switch | 72.1-72.5% | +0.70 to +1.12 |
| 1 | **4th Gourgeist ex (−1 Poké Pad)** | **73.35%** | **+1.98 ± 0.45** |
| 2 | +2 Energy / −1 Pumpkaboo / 2 Risky Ruins | 73.4-74.1% | −0.01 to +0.75 |
| 2 | −1 Boss's / −1 Switch, +1 Energy | 74.75% / 75.05% | +1.40 / +1.70 |
| 2 | **−1 Boss's, −1 Switch, +2 Energy (this list)** | **75.47%** | **+2.11 ± 0.50** |
| 1000 games | First build / **this list** | 71.99% / **75.74%** | **+3.75 ± 0.24** |

Logged against random field opponents, it won 47 of 60. Per game it used:
- Ghostly Touch 1.7 times, Earthquake 1.5, Horrifying Rondo 1.5, Whap Down
  0.2.
- Its own Earthquake Knocked Out 0.2 of its Pokémon per game.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Bunnelby | 98.3% | 1.37 |
| Diggersby | 84.2% | 2.72 |
| Pumpkaboo | 98.1% | 1.34 |
| Gourgeist ex | 75.4% | 2.98 |

First attack by turn 6 in 98.7% of games (average turn 2.74). The baseline
doesn't model Iris's Fighting Spirit.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Every attack is payable with Psychic Energy (Diggersby's are Colorless),
  and no Ability gates an attack.
- 8 Basics, 34.6% mulligan.

## PTCGL import

```
Pokémon: 15
4 Bunnelby POR 64
3 Diggersby POR 65
4 Pumpkaboo CRI 40
4 Gourgeist ex CRI 102

Trainer: 28
4 Lillie's Determination MEG 119
3 Iris's Fighting Spirit ASC 190
2 Boss's Orders MEG 114
1 Team Rocket's Petrel ASC 207
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
3 Poké Pad ASC 198
3 Switch MEG 130
3 Night Stretcher MEG 173
1 Hero's Cape TEF 152

Energy: 17
17 Basic Psychic Energy

Total Cards: 60
```
