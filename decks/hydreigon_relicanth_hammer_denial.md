# Hydreigon / Relicanth hammer denial

Tuned 2026-10-09 from a submitted Hydreigon / Grafaiai Energy-denial list
([hydreigon_grafaiai_energy_denial.md](hydreigon_grafaiai_energy_denial.md)).
**63.56% against the 80-deck field at 1000 games per opponent, against 47.11%
for the list it came from (+16.45 ± 1.00 paired, better on 78 of 80).** That
would place it about 15th of 78 in the 2026-10-08 round robin; the original
sits about 50th. Both numbers come from the engine after the Energy-placement
fix below. The tuning table further down was measured before that fix
(62.88% vs 46.64% then).

**Lines:** Deino → Zweilous → Hydreigon (main), Dunsparce → Dudunsparce (draw),
Relicanth, Pecharunt ex, Shaymin, Psyduck.

## Plan

**Hydreigon 30C 99** (Stage 2, 170 HP) has two attacks:
- **Three-Headed Bite** (D): flip 3 coins and discard an Energy from the
  opponent's Active for each heads.
- **Pitch-Black Fangs** (DC): 140 damage.

**Relicanth's Memory Dive** lets every evolved Pokémon use its previous
Evolutions' attacks. Zweilous and Hydreigon can then use Deino's and
Zweilous's **Stomp Off** (D: discard the top 1 or 2 cards of the opponent's
deck) whenever there is nothing better to do with one Energy.

Four other cards take Energy away from the opponent's attacker:
- **Crushing Hammer**
- **Enhanced Hammer**
- **Rust Syndicate Grunt**
- **Handheld Fan**, which moves an Energy off the attacker every time it hits
  your Active.

While the opponent rebuilds that Energy, Hydreigon trades 140-damage hits.

The support Pokémon:
- **Dudunsparce's Run Away Draw** draws 3 and shuffles Dudunsparce back into
  the deck, so the line is repeatable draw.
- **Shaymin's Flower Curtain** stops attack damage to Benched Pokémon without
  a Rule Box, which covers every Deino and Zweilous.
- **Pecharunt ex's Subjugating Chains** pulls a Benched Darkness Pokémon into
  the Active Spot (Poisoned) as a free pivot.
- **Psyduck's Damp** turns off self-Knock Out Abilities.

## How to play

1. **Turn 1.** Buddy-Buddy Poffin for two Deino (or Deino + Dunsparce). Poké
   Pad finds Deino, Zweilous, Hydreigon, Relicanth or Shaymin. Attach a
   Darkness Energy to the Active Deino.
2. **Turn 2.** Evolve to Zweilous. Rare Candy straight into Hydreigon whenever
   it is in hand. Get Relicanth onto the Bench so Stomp Off stays available.
   Janine's Secret Art puts Darkness Energy on two Darkness Pokémon from the
   deck (it Poisons the Active, so aim it at the Bench). Hilda finds an
   Evolution card and an Energy.
3. **Every turn after.** Pitch-Black Fangs for 140 when it Knocks Out or sets
   up a Boss's Orders / Prime Catcher Knock Out. Otherwise hammer the
   attacker. Three-Headed Bite the Active when it holds 2+ Energy and
   Hydreigon has only one. Put Handheld Fan on whatever stays Active. Use Rust
   Syndicate Grunt the turn after you lose a Pokémon.
4. **Recovery.** Night Stretcher brings back a Hydreigon or a Basic Energy.
   Lana's Aid returns up to 3 non-Rule-Box Pokémon and Basic Energy.

**Their outs.** Lurantis (25%) and Nidoking ex / Nidoqueen (28%) are the worst
matchups. Next are the Ditto Hydreigon decks (29%), Diggersby (31%) and
Raticate rush (32%). These are fast single-Prize
attackers or decks that don't care about losing Energy. The mirror against
Ditto / Hydreigon dropped from 40% to 28% with this tuning; it is the one
matchup that got clearly worse.

## The stall-and-mill plan (and where Grafaiai fits)

The submitter's plan: strip the opponent's Energy, then put it back on their
board where it can't be used. That means a Pokémon that isn't meant to
attack, the wrong type, or a mismatched place. Meanwhile Zweilous's Stomp
Off mills 2 a turn. The simulator agrees that the deck wins by milling. In
120 logged games against eight opponents, 32 of the 1-1 Grafaiai list's 55
wins were deck-outs; the submitted list's were 31 of 47.

**Engine fix (2026-10-09).** Mischievous Painting and Handheld Fan both let
the player GIVING the Energy choose where it goes, and the simulator chose
badly:
- **Painting** put every Energy on the opponent's Active, their attacker, and
  turned it into Colorless Energy.
- **The Fan** took the last Energy attached and gave it to the first Benched
  Pokémon, often the next attacker.

Both now put each Energy on the opponent's Pokémon that can use it least.
That's one with no attack, on it or anything it evolves into, that the type
can pay part of, and no Ability that wants it (Munkidori). So against
Dragapult, the Energy goes on Budew, not Dreepy. The Fan now takes the Energy
the attacker most needs: it leaves Dragapult ex without Fire + Psychic for
Phantom Dive. Worth +1.27 ± 0.51 to the submitted list and +0.75 ± 0.46 to
this one.

**Mischievous Painting itself doesn't pay for the attack.** It was tried at
several values, paired on the submitted list:

| What a Painting attack was worth | Paired change |
|---|---|
| 20 / 40 / 80 per discarded Energy | −2.02 / −1.90 / −3.69 |
| 40 / 120 per Energy that lands where nothing can use it | −0.04 ± 0.30 / −0.52 ± 0.32 |

**Fewer Grafaiai measures better.** 1000 games x 80 decks:

| Build | Win rate | Paired vs submitted |
|---|---|---|
| Submitted list | 47.11% | |
| 2-2 Grafaiai, 10 Energy, 4-4-2 Hydreigon, no Psyduck | 57.08% | +9.97 ± 0.90 |
| **1-1 Grafaiai, 10 Energy, 4-4-3 Hydreigon** ([import](hydreigon_grafaiai_stall_mill.ptcgl.txt)) | **61.19%** | **+14.08 ± 1.00** |
| No Grafaiai (this list) | 63.56% | +16.45 ± 1.00; +2.37 ± 0.30 vs 1-1 |

The stall that measures comes from the 4 Crushing Hammers, Handheld Fan
parking Energy on dead Benched Pokémon, and enough Energy (10) to Stomp Off
every turn. If you want Painting available, the 1-1 Grafaiai list costs about
2.4 points. Its worst matchups are Lurantis 21%, Nidoking ex 24%, Raticate 26%
and Ditto Hydreigon 27%. In the 1000-trial baseline it has Hydreigon in play
by turn 6 in 47.9% of games and its first attack by turn 6 in 91.5%.

Tried and removed in the same pass, neither measured:
- Not using Run Away Draw when it would leave one Pokémon in play: +0.21 at
  200 games; −0.04 / +0.25 at 1000.
- Benching Basics an Ability drew the same turn: −0.30.

## How it was tuned

200 games against each of the 79 field decks, paired on the same seeds; the
last three rows are 1000 games. Lists and results are in
`runs/2026-10-09/hydreigon_screens/`.

| Change | Win rate | Paired vs |
|---|---|---|
| Submitted list (Rare Candy MEG 125 for the rotated SVI 191) | 46.65% | |
| +1 Rare Candy (−Nighttime Mine) | 46.40% | −0.25 ± 0.80 vs submitted |
| +1 Hydreigon (−Air Balloon) | 47.46% | +0.81 ± 0.48 |
| +1 Rare Candy +1 Hydreigon | 48.30% | +1.65 ± 0.80 |
| 8 Darkness Energy (−Nighttime Mine, −Air Balloon) | 50.82% | +4.18 ± 0.81 |
| 9 Darkness Energy | 51.52% | +4.87 ± 0.85 |
| **No Grafaiai:** −2 Shroodle −2 Grafaiai, +Deino +Hydreigon +Rare Candy +Dunsparce | **53.68%** | **+7.04 ± 0.51** (better on 76) |
| No Grafaiai, 8 Energy | 56.93% | +3.25 ± 0.81 vs No Grafaiai |
| No Grafaiai, 9 Energy | 57.51% | +3.82 ± 0.89 |
| **No Grafaiai, 10 Energy** (−Mine −Balloon −Xerosic's −Petrel) | **58.22%** | **+4.54 ± 0.92** |
| 11 Energy (−Enhanced Hammer) | 56.97% | −1.25 ± 0.61 vs 10 Energy |
| 12 Energy (−Rust Syndicate Grunt too) | 56.55% | −1.67 ± 0.67 |
| 3 Rare Candy | 56.63% | −1.59 ± 0.53 |
| **3 Zweilous** (−Dunsparce TEF) | **61.91%** | **+3.69 ± 0.53** |
| 4 Zweilous (−the last Dunsparce TEF) | 62.77% | +0.85 ± 0.47 vs 3 Zweilous |
| 4 Hydreigon (−Rust Syndicate Grunt) | 61.98% | +0.07 ± 0.54 |
| No Psyduck (+Dunsparce JTG) | 61.78% | −0.13 ± 0.48 |
| No Pecharunt ex (+Dunsparce JTG) | 59.38% | −2.53 ± 0.53 |
| Submitted list, 1000 games | 46.64% | |
| 3 Zweilous, 1000 games | 61.20% | +14.56 ± 0.90 vs submitted |
| **4 Zweilous, 1000 games (this list)** | **62.88%** | **+16.24 ± 0.91**; +1.68 ± 0.24 vs 3 Zweilous |

**Three findings, in order of size:**

1. **Grafaiai works against the rest of the deck.** Energized Graffiti does 40
   for each Energy on the opponent's side, and every hammer takes those
   Energy away. Its four slots are worth more as Stage 2 consistency. With
   them, Hydreigon evolves 1.73 times per game instead of 1.10, and Pitch-Black
   Fangs lands 1.20 times per game instead of 0.63 (60 logged games against
   six opponents).
2. **Six Energy is too few** for attackers that need two. In a logged game
   against Dragapult, Pecharunt ex sat Active for three turns with at most one
   Energy and Hydreigon never attacked. Win rate climbs to 10 Energy and falls
   after. The 4 cards cut for Energy (Nighttime Mine, Air Balloon, Xerosic's
   Machinations, Petrel) were rarely the difference.
3. **Zweilous count over Dunsparce.** The third and fourth Zweilous make
   Hydreigon reliable without a Rare Candy in hand. A third Rare Candy didn't
   help.

The trade-off is 10 Basic Pokémon instead of 12, so the deck mulligans 25.9%
of the time instead of 19.1%; the numbers above include that.

Two pilot ideas tried during this study measured negative and were reverted:
- **Valuing Energy denial by how much it cuts the opponent's best attack:**
  −1.43 for this deck, worse on 7 of 10 decks.
- **Holding Boss's Orders when nothing can attack:** −0.35 on average across
  10 decks.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Deino | 95.6% | 1.47 |
| Zweilous | 71.0% | 2.91 |
| Hydreigon | 49.7% | 3.71 |
| Dunsparce | 80.1% | 1.78 |
| Dudunsparce | 35.9% | 3.21 |
| Relicanth | 36.1% | 2.42 |
| Shaymin | 47.2% | 2.51 |
| Pecharunt ex | 28.0% | 2.26 |
| Psyduck | 48.9% | 2.26 |

First attack by turn 6 in 89.3% of games (average turn 2.79). The submitted
list had Hydreigon by turn 6 in 23-27% of games across four baseline runs,
and its first attack by turn 6 in 77-79%. The
baseline doesn't model Crushing Hammer, Enhanced Hammer, Lana's Aid, Prime
Catcher or Rust Syndicate Grunt, so these numbers measure setup speed only.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Prime Catcher).
The one warning is Relicanth's Razor Fin (Fighting), which can never be
paid. Relicanth is in the deck for Memory Dive, not to attack.

## PTCGL import

```
Pokémon: 19
4 Deino SSP 117
4 Zweilous SSP 118
3 Hydreigon 30C 99
2 Dunsparce JTG 120
2 Dudunsparce TEF 129
1 Relicanth TEF 84
1 Pecharunt ex SFA 39
1 Shaymin DRI 10
1 Psyduck ASC 39

Trainer: 31
1 Enhanced Hammer TWM 148
4 Crushing Hammer POR 71
1 Prime Catcher TEF 157
4 Poké Pad ASC 198
2 Night Stretcher ASC 196
2 Handheld Fan TWM 150
1 Lana's Aid TWM 155
1 Hilda WHT 84
1 Rust Syndicate Grunt PBL 81
1 Janine's Secret Art SFA 59
4 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination MEG 119
3 Boss's Orders MEG 114
2 Rare Candy MEG 125

Energy: 10
10 Basic Darkness Energy

Total Cards: 60
```
