# Mega Malamar ex: Psychic Marionette

Built 2026-11-06 from a request: a Darkness deck around Inkay and Mega
Malamar ex from Delta Reign, with Sableye to disrupt, and maybe Toxtricity
for Energy acceleration.

**This list: 77.50% against the 104-deck field at 1000 games per
opponent** (median 81.1%, 97 of 104 winning), on the engine as of b2d5545.
The list as asked (`M0` in the archive: Inkay / Mega Malamar ex, 2 Sableye,
a Toxel / Toxtricity line, a Vullaby / Mandibuzz line, 4 Accompanying
Flute) reads 61.68% (median 63.2%, 83 winning). On the same seeds this list
is **+15.82 ± 0.58** over it, better on all 104.

**Read this first: the Delta Reign cards are provisional.** The English set
came out today and neither card API this project reads (pokemontcg.io,
TCGdex) carries it yet. Sableye, Inkay and Mega Malamar ex are in the pool
from the Japanese Storm Emeralda (TCGdex, M6-046 to 048): HP, costs and
damage as printed, English text written in the template of the pool's card
with the same effect, names and numbers (DLR 60, 68, 69) from retailers.
Two attack names (Ominous Lick, Eerie Wave) are placeholders. Check the
cards in PTCGL; when the card API carries the set, they are replaced (a
copy is in `provisional_cards_delta_reign.json`).

## The cards

- **Mega Malamar ex** (DLR 69, Stage 1 Darkness from Inkay, 320 HP, Retreat
  2, **weak to Grass**, 3 Prizes):
  - **Psychic Marionette** (Darkness, Darkness): 70 damage for each of
    the opponent's Benched Pokémon. A full Bench is 350.
  - **(Eerie Wave)** (Darkness ×3): 200, and the opponent's Active is
    Confused.
- **Inkay** (DLR 68, Basic, 60 HP): **Knock Off** (Darkness), 10, and
  discard a random card from the opponent's hand. This, not Sableye, is
  the set's hand disruption.
- **Sableye** (DLR 60, Basic, 80 HP): **Lure Out** (Darkness), reveal the
  top 5 of the opponent's deck and put any Basic Pokémon there onto their
  Bench; **(Ominous Lick)** (Darkness, Colorless), 5 damage counters on
  any of their Pokémon.
- **Pecharunt ex** (SFA 39): Subjugating Chains, switch a Benched Darkness
  Pokémon into the Active Spot (it is Poisoned): a free way to bring a
  charged Mega Malamar ex up.
- **Fezandipiti ex** (ASC 142): Flip the Script, draw 3 after a Knock Out.
- **Janine's Secret Art**: a Basic Darkness Energy onto each of 2 Darkness
  Pokémon from the deck.

## How it wins, measured

`attacks_bench.py` (in the archive), 80 logged games, 10 each against the
six meta decks, Krookodile ex hand disruption and Mega Absol ex hand lock:
60 wins.

- **Psychic Marionette takes 74% of the Prizes,** 2.38 times a game, into
  an average opposing Bench of 4.3. On a full Bench of 5 it Knocks Out 99%
  of the time; on 3, 74%.
- **The 200 attack takes the other 24%,** when their Bench is small
  (average 1.8): the deck doesn't need the Bench to be full.
- **Inkay's Knock Off** goes 0.54 times a game, from Inkay waiting to
  evolve.

| Their Bench | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Psychic Marionette | 70 | 140 | 210 | 280 | 350 |
| Hits | 4 | 15 | 23 | 47 | 88 |
| Knocked Out | 50% | 60% | 74% | 85% | 99% |

Opponents fill their own Benches. That is why every card spent on filling
it for them measured as a loss.

## What the measurements say

Your two suggestions:

- **Sableye** doesn't earn more than one slot. Lure Out benches whatever
  Basics sit in their top 5, at the cost of the attack: 2 Sableye for a
  Poké Pad and a Night Stretcher +3.09 ± 0.40, 3 down to 1 +4.36 ± 0.43.
  The last one measured +1.97 to cut, but only against a 19th Energy, the
  comparison this simulator overrates, and it keeps the Basics at 7.
- **Toxtricity** (PFL 68, Sinister Surge) doesn't either: Pecharunt ex,
  Fezandipiti ex and 2 Energy for the 2-2 line +3.91 ± 0.54, and the line
  back into the final list −2.00 ± 0.55.

Every change is paired against the list of its round, 200 games a
matchup.

| Round | From | Change | Measured |
|---|---|---|---|
| 1 | as asked | No Vullaby / Mandibuzz (+Mega Malamar ex, Sableye, Poké Pad, Night Stretcher) | **+6.96 ± 0.51** |
| 1 | as asked | No Toxtricity line (+2 Energy, Ultra Ball, Poké Pad) | +3.68 ± 0.54 |
| 1 | as asked | No Sableye / no Accompanying Flute / no Xerosic's | +3.09 / +1.92 / +1.33 |
| 1 | as asked | 4th Mega Malamar ex / no Janine's | +1.18 / −0.21 |
| 1 | as asked | Flute played and Lure Out priced for Psychic Marionette (engine) | −0.27 ± 0.46 |
| 2 | 4 Malamar | 1 Sableye of 3 / no Flute | **+4.36** / **+3.32** |
| 2 | 4 Malamar | Pecharunt ex + Fezandipiti ex + 2 Energy for the Toxtricity line | **+3.91 ± 0.54** |
| 2 | 4 Malamar | Pecharunt ex / Fezandipiti ex / Meowth ex alone | +1.55 / +1.11 / −0.68 |
| 2 | 4 Malamar | No Xerosic's / 15 Energy | +1.38 / +2.18 |
| 3 | 4 Malamar | Round 2's gains together, Xerosic's kept | **+8.37 ± 0.57** |
| 3 | 4 Malamar | The same, no Xerosic's: this list | **+8.81 ± 0.56** |
| 3 | 4 Malamar | Round 2's gains with Xerosic's and a 2nd Sableye | +6.88 ± 0.54 |
| 4 | this list | No Sableye (+1 Energy) | +1.97 ± 0.38 |
| 4 | this list | Toxtricity 2-2 back (−4 Energy) | −2.00 ± 0.55 |
| 4 | this list | 16 / 14 Energy (Petrel, Munkidori, Pokégear in) | −1.76 / −2.28 |
| 4 | this list | No Janine's (+2 Petrel) / Munkidori | −1.96 / −0.19 |

**Energy: 18 is a lot, and the simulator overrates Energy** (see
`decks/mega_froslass_ex_resentful_refrain.md`). Going down to 16 or 14 with
Team Rocket's Petrel, Munkidori and Pokégear in its place lost each time,
so the list keeps 18; a human player could well run fewer.

**Basics: 7** (4 Inkay, Sableye, Pecharunt ex, Fezandipiti ex): a 39.9%
chance of no Basic in the opening hand. The simulator plays the mulligans
out and still measures this list best; with 10 Basics it would be 25.9%.

## How it plays, turn by turn

- **First turns:** Inkay (and the others) to the Bench with Buddy-Buddy
  Poffin. An Inkay in the Active Spot can Knock Off a card while the rest
  set up. Mega Malamar ex is a Stage 1: evolve from an Inkay that has been
  down since an earlier turn, not on your first turn.
- **Energy:** 2 Darkness for Psychic Marionette. Janine's Secret Art puts
  one on each of two Darkness Pokémon from the deck, so a Benched Mega
  Malamar ex is ready the turn Pecharunt ex's Subjugating Chains brings it
  up. It arrives Poisoned, which 320 HP can carry for a few turns.
- **Each turn:** count their Bench. 4 or 5 Benched Pokémon is 280–350 for
  two Energy; with 2 or fewer, the 200 attack and its Confusion are
  better. Boss's Orders drags up the Benched Pokémon the hit can Knock Out.
- **Their outs:** a small Bench (a deck that keeps 1–2 Benched Pokémon
  takes Psychic Marionette down to 70–140), Grass attackers (Mega Malamar
  ex is weak to Grass: Chesnaught / Meganium, Arboliva ex, Lurantis,
  Hydrapple all beat it), and Knocking Out a 3-Prize Mega ex.

## Where it loses

At 1000 games, the list as asked → this list:

| Opponent | As asked | This list |
|---|---|---|
| Chesnaught / Meganium (Grass) | 21.6% | 25.9% |
| Mega Zygarde ex / Cinderace (Gaia Wave) | 15.8% | 26.8% |
| Arboliva ex / Ogerpon (Grass) | 18.6% | 28.4% |
| Mega Zeraora ex / Cinderace | 16.8% | 29.7% |
| Lurantis (Grass) | 30.7% | 38.3% |
| Hydrapple / Seaking Festival Lead (Grass) | 26.5% | 39.3% |
| Mega Zygarde ex / Cinderace (Turbo Flare) | 27.9% | 40.6% |
| Dragapult ex (pure / Dusknoir / Blaziken) | 64.5 / 68.6 / 65.3% | 78.3 / 83.3 / 82.7% |
| Mega Excadrill ex / Raging Bolt ex | 54.1 / 61.6% | 71.3 / 76.9% |
| Festival Lead / Slowking / N's Zoroark ex | 71.9 / 74.6 / 79.4% | 76.7 / 91.5 / 94.0% |

The field predates Delta Reign: none of its decks run the new set, so a
real Delta Reign field (Mega Rayquaza ex, Talonflame ex, the Legendary
Stadiums) is untested here.

## Engine changes made for this deck

- **Provisional Delta Reign cards** in the pool (above).
- **Lure Out did nothing as an attack:** fill_opponent_bench (Accompanying
  Flute's effect) was not an attack rider. It is now.
- **Tried and taken out:** playing Accompanying Flute for, and pricing
  Lure Out by, an attack that counts the opponent's Bench (−0.27 ± 0.46).
- **The mechanic index** has `fill_opponent_bench` (Accompanying Flute,
  Lure Out, Lickitung, Mandibuzz, Lillie's Ribombee).
- **The setup baseline** lists Accompanying Flute as an opponent-only Item.

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | As asked | This list |
|---|---|---|
| Inkay | 96.2% (avg turn 1.46) | 98.5% (1.25) |
| Mega Malamar ex | 67.7% (2.97) | 89.1% (2.63) |
| First attack by turn 6 | 94.1% (2.62) | 98.0% (2.76) |

## Import

The Delta Reign set code is written DLR, as retailers list it; check it
imports.

```
Pokémon: 11
4 Inkay DLR 68
4 Mega Malamar ex DLR 69
1 Sableye DLR 60
1 Pecharunt ex SFA 39
1 Fezandipiti ex ASC 142

Trainer: 31
4 Lillie's Determination MEG 119
4 Hilda WHT 164
3 Boss's Orders MEG 114
2 Janine's Secret Art SFA 59
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Night Stretcher MEG 173
4 Poké Pad ASC 198
1 Switch MEG 130
1 Hero's Cape TEF 152

Energy: 18
18 Basic Darkness Energy

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-11-06/malamar_screens`. The list is in
the field as `decks/field/mega_malamar_ex_psychic_marionette.txt`.
