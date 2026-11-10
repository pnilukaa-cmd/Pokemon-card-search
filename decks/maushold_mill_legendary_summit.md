# Maushold mill with Legendary Summit and Tauros

A submitted Maushold mill list (2026-11-09), studied as a mill deck, then
checked against the newest cards (Delta Reign, Pitch Black, 30th
Celebration) for new combinations.

**This list: 66.55% against the 106-deck field at 1000 games per opponent**
(median 70.2%, 82 winning). The list as submitted reads 58.96% (median
63.3%, 75 winning). On the same seeds this list is **+7.59 ± 0.83**, better
on 87 of 106.

The field already had a Maushold mill build from before Delta Reign
(`maushold_gnaw_together_mill`: Battle Cage, Dudunsparce ex, Mist Energy,
Crushing Hammer). Against the same seeds it reads 56.23% (median 57.8%,
68 winning):

- **The submitted list:** +2.73 ± 1.83 over it.
- **This list:** **+10.32 ± 1.73** over it, better on 70.

Legendary Summit and Tauros are what the Delta Reign version adds.

## The submitted list is a real mill deck

How it wins, from `measure_mill.py` (80 logged games, 10 each against the
six meta decks, Krookodile ex hand disruption and Mega Absol ex hand lock):

- **Every win was a deck-out:** 51 wins, all 51 by the opponent running
  out of cards. The losses: 26 on Prizes, 2 to its own deck running out,
  1 with no Pokémon left.
- **The opponent can barely take Prizes:** 1.91 a game on average.
  - Legendary Summit (Delta Reign): "Whenever a Colorless Pokémon (yours or
    your opponent's) is Knocked Out by damage from an attack ..., that
    player takes 1 fewer Prize card." Every Pokémon in the list but Comfey
    is a single-Prize Colorless Pokémon, so it is worth 0.
  - Neutralization Zone: attacks from Pokémon ex and V do no damage to a
    Pokémon without a Rule Box. None of the list's Pokémon has one.
- **The mill:** Maushold's Gnaw Together, 4.44 a game, 2.36 cards each.
  Comfey's Flower Shower makes the opponent draw 3. Together they take
  13.9 cards a game off the opponent's deck, on top of their own draws.
- **The leak is Maushold in play:** Gnaw Together flips one coin per
  Maushold, and there were only 2.0 in play on average when it fired.

| Maushold in play | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Gnaw Together fired (submitted list) | 106 | 140 | 101 | 8 |
| Cards milled each | 1.33 | 2.44 | 3.26 | 3.38 |

**What the two walls are worth.** Each was tested by removing it from the
list being tuned:

- **No Legendary Summit:** −12.65 ± 1.27.
- **Battle Cage for Neutralization Zone:** −15.83 ± 1.69.

They are the deck. Gnaw Together only has to keep milling while the
opponent cannot finish the game.

### Engine fixes this needed

- **Legendary Summit** was never played: the pilot's "is this Stadium
  worth putting down" check did not know a Prize modifier. When it was in
  play, it cut a Prize on *every* Knock Out by an attack, the opponent's ex
  included. Now it is played while you have as many Colorless Pokémon in
  play as they do, and it covers Colorless Pokémon only.
- **Aarune** ("up to 3 in any combination of Supporter and Stadium cards")
  searched for a card *named* "in any combination of …" and found nothing.
  So did Celebi, Heatmor and Ethan's Adventure. It now takes a Stadium and
  Supporters.
- **The setup baseline** plays Aarune, and lists Pokémon Catcher as
  opponent-only.

### Set numbers

Pokégear 3.0 SVI 186 and Pokémon Catcher SVI 187 are printings from the
rotated Scarlet & Violet base set, which this pool does not carry. The
same cards are Standard-legal as **Pokégear 3.0 BLK 84** and **Pokémon
Catcher POR 82 / DLR 129**; the import below uses those. "Basic {P} Energy
MEE 5" is the client's export spelling of Basic Psychic Energy. Legendary
Summit DLR 96 and DLR 97 are two printings of one card (4 in all, legal).

## The newest cards for mill

Searched by mechanic family (mill, forced draws, hand disruption, Prize
reduction, damage prevention and reduction, healing, locks) over Delta
Reign, Pitch Black, 30th Celebration, Chaos Rising and Perfect Order. The
ones that could fit, each tested in the list as a single change:

| Card (set) | What it does for mill | Measured |
|---|---|---|
| **Tauros** (DLR 77) | Colorless Basic, 130 HP: worth 0 Prizes under Summit; Raging Horns hits harder as it takes damage | **+3.09, then +2.30 at 4 copies** |
| Legendary Summit (DLR) | already in the list | **−12.65 to take out** |
| Custom Vest (DLR) | 60 less from Mega ex attacks | −2.36 |
| Legendary Pyroduct (DLR) | Evolution Pokémon have no Abilities | −2.73 (for 1 Summit) |
| Grisham (DLR) | heal 50 from every Pokémon in play (both sides) | −2.99 |
| Tasty Rice Ball (DLR) | heal 30, +30 for each in the discard | −3.23 |
| Swablu / Altaria (DLR) | Colorless; Basics have no Retreat Cost | −3.75 |
| Eevee (DLR 78) | Colorless Basic, Nap heals 20 | −2.80 (Tauros is not just "more Basics") |

Not tested, and why:

- **Sandslash DLR** mills one card but costs Fighting Energy.
- **Mantine DLR's Make Waves** shuffles the opponent's hand *back into*
  their deck: the opposite of mill.
- **Inkay DLR's Knock Off** discards from the hand, not the deck, and
  needs Darkness Energy.
- (Corrected 2026-11-10: this list first named Rotom's Astonish and
  Sharpedo's Chew Off and Liepard's Knock Off as Delta Reign cards. Those
  attacks are on older printings; Delta Reign's Rotom, Sharpedo and
  Liepard have Thunder Shock, Crunch and Follow-Up Claw.)
- **Legendary Trench** would double heals, but it is a Stadium and would
  push Summit out.

From the published list (the PokéBeach "Maushold Mill (30th Anni)" thread:
Salvatore, Battle Cage, Lisia's Appeal, Mist Energy):

| Change | Measured |
|---|---|
| Salvatore for an Aarune | −0.90 |
| Lisia's Appeal for a Catcher | −0.55 |
| Mist Energy ×3 for 3 Psychic | +0.70, +0.75, +0.49 (three rounds, each within noise) |
| Battle Cage for Neutralization Zone | −15.83 |

## Newer Supporters (2026-11-10)

None replaces what is there. Two Lillie's Determination for two of Emma,
Tate & Liza's Training, Emcee's Hype, Judge, Lucian or more Xerosic's cost
5.5 to 7.6. Tate & Liza's Training for Aarune and Pokégear (it returns to
the hand while Legendary Summit is in play) cost 2.34, and Eri 2.84. Full
table: `runs/2026-11-10/delta_reign_mill_cards/README.md`.

## What changed, measured

Each change is paired against the list of its round, at 200 games a matchup.

| Round | From | Change | Measured |
|---|---|---|---|
| 1 | submitted | 2 Tauros for 2 Pokémon Catcher | **+3.09 ± 0.71** |
| 1 | submitted | No Catcher (+Lana's Aid, Night Stretcher, Xerosic's) | −1.27 ± 0.53 |
| 2 | +2 Tauros | Dunsparce line 2-2 → 1-1, for 2 more Tauros | **+2.30 ± 0.57** |
| 2 | +2 Tauros | 4 Tauros for Catcher and Lana's Aid | −0.69 |
| 3 | 4 Tauros | No Dunsparce line (+Lana's Aid, +Night Stretcher): this list | **+2.96 ± 0.44** |
| 3 | 4 Tauros | 3rd Comfey / 3rd Xerosic's / 4th Backtrack Badge | +0.72 / −0.45 / −1.02 |
| 4 | this list | 3rd Comfey / Mist ×3 / both / Comfey for an Aarune | +0.21 / +0.49 / +0.85 / +0.25 |

Round 4 is flat: the list has stopped improving. Mist Energy came out
slightly positive in every round it was tried, but never by more than its
error. By the rules it also stops Phantom Dive's damage counters on the
Pokémon holding it (placing counters is an effect), which could matter
against Dragapult. That was not measured by matchup.

## How this list wins

`measure_mill.py`, 80 logged games, the same eight opponents:

- **53 wins:** 43 by deck-out, 10 on Prizes.
- **The opponent took 2.08 Prizes a game;** this list took 1.25.
- **Gnaw Together:** 3.00 a game, 2.50 cards each.
- **Tauros's Raging Horns:** 2.73 a game, Knocking Out 32% of the time.
  It gives the deck a second way to win and costs nothing to lose under
  Summit.
- **Games run long:** 21.4 turns on average.

## How it plays, turn by turn

- **First turns:** Tandemaus (and Tauros, Comfey) to the Bench with
  Buddy-Buddy Poffin. Evolve every Tandemaus into Maushold you can.
  Backtrack Badge goes on a Maushold: it re-flips all of Gnaw Together's
  coins.
- **One Stadium at a time:** Summit and Neutralization Zone replace each
  other.
  - Against Pokémon ex attackers, Neutralization Zone: they cannot damage
    your Pokémon at all.
  - Against single-Prize attackers, Legendary Summit: your Colorless
    Pokémon are worth 0.
  - Aarune finds either.
- **Each turn:** Gnaw Together with as many Maushold as possible. Three
  is 3 a turn on average; four is the most. Flower Shower when the
  opponent is close to empty: 3 more cards off their deck. Xerosic's cuts
  a big hand down to 3. A Tauros in the Active Spot soaks damage and hits
  back.
- **Their outs:**
  - A Stadium that replaces Summit, or one that replaces Neutralization
    Zone against ex attackers.
  - Damage counters, which neither wall stops: Dragapult ex's Phantom
    Dive.
  - Non-Colorless attackers taking Comfey (Psychic) for Prizes.
  - Running the deck out of cards itself: 5 of 80 measured losses.

## Where it loses

At 1000 games, the submitted list → this list:

| Opponent | Submitted | This list |
|---|---|---|
| Dragapult ex (pure / Dusknoir / Blaziken) | 41.0 / 34.8 / 51.8% | 39.0 / 38.1 / 49.4% |
| Raging Bolt ex / Mega Excadrill ex | 65.6 / 63.8% | 65.5 / 67.0% |
| Slowking / Festival Lead / N's Zoroark ex | 71.1 / 72.0 / 90.9% | 76.5 / 88.3 / 94.0% |
| Mega Malamar ex / Bug Out (Delta Reign) | 75.8 / 68.7% | 81.4 / 81.6% |

Worst for this list:

- Tauros / Risky Ruins: 16.1%
- Team Rocket's Tyranitar: 20.3%
- Diggersby / Munkidori: 28.8%
- Mew / Alex / Centiskorch mill: 30.4%
- Jellicent ex: 31.3%
- The field's other Maushold mill (`maushold_gnaw_together_mill`, Battle
  Cage and Dudunsparce ex): 35.0%

It lost ground to the Ditto / Hydreigon decks (−10.6 and −6.1) and to the
other mill decks (−3.5 to −7.0).

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | Submitted | This list |
|---|---|---|
| Maushold | 75.9% (avg turn 2.89) | 75.0% (2.85) |
| Tandemaus | 94.9% (1.44) | 96.6% (1.46) |
| Comfey | 82.2% (1.94) | 86.0% (1.85) |
| Tauros | — | 84.7% (1.87) |

**Basics:** 10 (4 Tandemaus, 4 Tauros, 2 Comfey), a 25.9% chance of no
Basic in the opening hand. The submitted list's 8 was 34.6%.

## Import

```
Pokémon: 14
4 Tandemaus SSP 157
4 Maushold 30C 146
4 Tauros DLR 77
2 Comfey SCR 63

Trainer: 37
4 Lillie's Determination MEG 119
2 Xerosic's Machinations SFA 64
4 Lana's Aid TWM 155
2 Aarune DLR 89
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad ASC 198
4 Night Stretcher ASC 196
4 Pokégear 3.0 BLK 84
1 Pokémon Catcher POR 82
3 Backtrack Badge PBL 74
4 Legendary Summit DLR 96
1 Neutralization Zone SFA 60

Energy: 9
9 Basic Psychic Energy

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-11-09/maushold_mill_screens`. The list
is in the field as `decks/field/maushold_mill_legendary_summit.txt`.
