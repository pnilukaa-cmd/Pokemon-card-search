# Bug Out: Masquerain / Jellicent

A submitted Delta Reign list (2026-11-09), checked against the official
set and tuned.

**This list: 49.12% against the 105-deck field at 1000 games per opponent**
(median 50.1%, 53 winning). The list as submitted reads 30.45% (median
28.8%, 15 winning). On the same seeds this list is **+18.66 ± 0.74** over
it, better on all 105.

## The cards are here

pokemontcg.io carries Delta Reign (set `me6`, code DLR, 141 cards) as of
2026-11-09. It was merged into the pool on its own
(`fetch_pokemon_cards.py --merge-set me6`), replacing the three provisional
cards the Mega Malamar ex deck was built on (same text).

Every line of the submitted list resolves:

- **Spinarak DLR 58, Jellicent DLR 28, Combee DLR 6, Surskit DLR 2,
  Masquerain DLR 3:** the new set.
- **Frillish WHT 44:** the Psychic one (Oceanic Gloom, Retreat 3). Delta
  Reign's own Frillish (DLR 27) is Water.
- **Sizzlipede PBL 9:** the only Bug Out card before Delta Reign.
- **Hilda WHT 84:** a printing of Hilda (WHT 164 / 171 / 84).
- **"Basic {G} Energy MEE 1" and "Telepathic {P} Energy POR 88":** the
  client's export spelling of Basic Grass Energy and Telepathic Psychic
  Energy.

The header counts in the paste (Pokémon: 8, Trainer: 9, Energy: 3) count
lines, not cards. The 60 total is right.

## How Bug Out works, and what the engine got wrong

**Bug Out** (Masquerain: one Grass; Spinarak, Combee, Sizzlipede: three
Colorless): "Reveal the bottom 7 cards of your deck, and this attack does
50 damage for each Pokémon you find there that has the Bug Out attack. Then,
shuffle any revealed Pokémon back into your deck. Discard the other cards."
Sixteen Bug Out Pokémon is the most a deck can run (4 of each). Seven in
the bottom 7 is 350.

The stackers put chosen cards there:

- **Jellicent's Deep Sea Draw:** "Draw a card. If you do, you may put a
  card from your hand on the bottom of your deck."
- **Kofu:** bottom 2, draw 4.
- **Quaquaval's Up-Tempo** and **Lucian:** the other two in the pool.

Before this, the engine read "you find there" as the opponent's revealed
hand: Bug Out did 50 for each Pokémon in *their* hand, and nothing was
shuffled or discarded. Deep Sea Draw was a bare draw, and Kofu bottomed its
two least useful cards. Now:

- Bug Out counts the real bottom 7 when it resolves. Before attacking, the
  pilot counts the Bug Out Pokémon it knows it stacked there, and expects
  the rest at the deck's density.
- Deep Sea Draw, Kofu and Up-Tempo put Bug Out Pokémon on the bottom
  (`stack_bottom`: 20.05% → 28.12% on the submitted list).
- Once two Pokémon are Benched, spare Bug Out Pokémon stay in hand for the
  bottom instead of going to the Bench (`hold_bottom_fuel`: +1.56 ± 0.48).
- A Basic the deck evolves (the Centiskorch decks' Sizzlipede) is never
  treated as Bug Out ammo.

## How it wins, measured

`measure.py` (in the archive): 80 logged games, 10 each against the six
meta decks, Krookodile ex hand disruption and Mega Absol ex hand lock.

| | Submitted | This list |
|---|---|---|
| Wins | 28 / 80 | 35 / 80 |
| Attacks a game | 3.29 | 4.64 |
| Prizes from attacks a game | 2.27 | 3.46 |
| Masquerain's Bug Out a game | 1.51 (avg 196, KO 60%) | 2.62 (avg 195, KO 59%) |
| Share of Prizes from Masquerain's Bug Out | 62% | 72% |
| Bug Out Pokémon in the bottom 7 at the attack | 3.07 (0.93 stacked) | 3.16 (0.64 stacked) |
| Bug Out Pokémon in play at the attack | 3.7 | 3.1 |

- **Masquerain is the deck.** Its Bug Out costs one Grass Energy and takes
  most of the Prizes. The three-Colorless Bug Out Basics are mostly ammo,
  and the backup attackers when no Masquerain is ready.
- **The damage mostly comes from density, not stacking.** The bottom 7
  averages 3.2 hits (about 160). When Bug Out fires, 8.8 of the 16 Bug Out
  Pokémon are in a 25-card deck: 2.5 hits by chance alone. Stacking adds
  the rest, about 0.6 cards, because every Bug Out reshuffles the deck.
- **This list wins by attacking more often, not by hitting harder:** more
  Grass Energy for the next Masquerain, and Lana's Aid to bring Pokémon and
  Energy back.

Hits in the bottom 7, this list (285 Bug Outs): 1: 37, 2: 66, 3: 72,
4: 58, 5: 30, 6: 20, 7: 2.

## What changed, measured

Each change is paired against the list of its round, at 200 games a
matchup against the 105-deck field.

| Round | From | Change | Measured |
|---|---|---|---|
| 1 | submitted | 4 Telepathic Psychic Energy → 4 Basic Grass | **+4.31 ± 0.45** |
| 1 | submitted | 2 Telepathic → 2 Grass | +2.15 ± 0.41 |
| 1 | submitted | Latias ex → Kofu | +2.07 ± 0.43 |
| 1 | submitted | Forest of Vitality → Kofu / Poffin 4 (−2 Night Stretcher) | +0.09 / −0.27 |
| 1 | submitted | Hilda 3 (+Kofu) / 4th Kofu (−Lana's Aid) / 2nd Boss's Orders | −0.72 / −1.47 / −2.88 |
| 2 | all Grass | Latias ex → Kofu / → Night Stretcher | **+3.09 ± 0.50** / +2.69 |
| 2 | all Grass | 3-3 Jellicent (+Night Stretcher, +Lana's Aid) | **+2.74 ± 0.47** |
| 2 | all Grass | Frillish DLR 27 for WHT 44 / 10th Energy | −0.16 / −0.70 |
| 2 | all Grass | No Lana's Aid (+2 Night Stretcher) | **−4.02 ± 0.54** |
| 3 | 3-3 line | 2-2 Jellicent (+Lana's Aid, +Night Stretcher) | **+2.35 ± 0.42** |
| 3 | 3-3 line | Boss's Orders → Lana's Aid / Night Stretcher → Lana's Aid | +2.24 / +1.65 |
| 3 | 3-3 line | No Poffin (+Lana's Aid, +Night Stretcher) / Hilda → Lana's Aid | +1.61 / +1.10 |
| 4 | 2-2 line | Boss's Orders → Lillie's Determination | **+1.50 ± 0.47** |
| 4 | 2-2 line | Poffin ×2 → Lillie's + Lucian / Boss's Orders → Lucian | +1.27 / −0.27 |
| 4 | 2-2 line | 1-1 Jellicent / Hilda → Lillie's | −0.70 / −0.05 |
| 4 | 2-2 line | Legacy Energy → Miracle Headset | **−7.57 ± 0.84** |
| 5 | no Boss | Poffin ×2 → 2 Basic Grass: this list | **+4.17 ± 0.51** |
| 5 | no Boss | Poffin ×2 → Lucian ×2 | +0.56 ± 0.46 |
| 6 | this list | Night Stretcher → 12th Energy | +0.32 ± 0.44 |
| 6 | this list | 1 Poffin back / 3-3 Jellicent back (−2 Grass) | −1.56 / −4.22 |

What that says about the submitted list's ideas:

- **Telepathic Psychic Energy** benches Frillish and Latias ex for free,
  but it is not Grass. Masquerain needs Grass, and four more Grass measured
  better than the search.
- **Latias ex** (free retreat for Basics) is a 2-Prize body that does not
  help Masquerain, which is a Stage 1. A Kofu in its slot measured better.
- **Jellicent** earns two copies, not four. Deep Sea Draw stacks the
  bottom, but each Bug Out reshuffles it, and the slots were worth more as
  Lana's Aid and Night Stretcher.
- **Lana's Aid** is the best card in the deck after the Pokémon: it
  returns three Pokémon or Basic Energy. Taking two out cost 4.02.
- **Boss's Orders and Buddy-Buddy Poffin both lost their slots.** Poffin
  benches Spinarak and Combee, the ammo, out of the deck.
- **Legacy Energy stays.** Its one-fewer-Prize clause is worth more than
  Miracle Headset's two Supporters back.

**Energy: 11.** Poffin → Grass is an Energy-for-X swap, the comparison
this simulator overrates (see `decks/mega_froslass_ex_resentful_refrain.md`).
But the next Energy measured flat (+0.32 ± 0.44), and a 10th Energy for a
Lana's Aid lost (−0.70), so it is not the bias alone. A human player could
try 10.

**Basics: 18** (4 Spinarak, 4 Combee, 4 Sizzlipede, 4 Surskit, 2
Frillish): a 7.0% chance of no Basic in the opening hand.

## How it plays, turn by turn

- **First turns:** Surskit and one or two Bug Out Basics down, Frillish
  for Jellicent. Hilda finds Masquerain or Jellicent plus a Grass Energy.
  Forest of Vitality lets a Surskit put down this turn evolve right away
  (not on your first turn).
- **Each turn:** Deep Sea Draw and Kofu put spare Spinarak, Combee,
  Sizzlipede (and spare Masquerain) on the bottom. Then Masquerain attacks
  for one Grass. Keep the rest of the Bug Out Pokémon in hand, not on the
  Bench: one in play is one Bug Out can never find.
- **After each Bug Out:** the Pokémon go back and the deck is shuffled, so
  the stack starts again. The Trainers and Energy among the 7 are
  discarded; Lana's Aid and Night Stretcher bring the Energy back.
- **Their outs:** Fire (Masquerain, Combee and Surskit are weak to it),
  walls that take less damage, and decking. Bug Out discards up to 7 cards
  a turn: 6 of 80 measured games ended on a deck-out, 2 of them won.

## Where it loses

At 1000 games, the submitted list → this list:

| Opponent | Submitted | This list |
|---|---|---|
| Dragapult ex (pure / Dusknoir / Blaziken) | 17.0 / 22.7 / 20.1% | 33.2 / 40.8 / 32.1% |
| Mega Excadrill ex / Raging Bolt ex | 11.0 / 34.2% | 21.3 / 48.7% |
| Slowking / N's Zoroark ex / Festival Lead | 34.8 / 56.1 / 68.7% | 56.4 / 76.1 / 77.0% |
| Mega Malamar ex (Delta Reign) | 16.2% | 39.8% |

Worst for this list: Mega Zeraora ex / Cinderace (2.6%), the Snorlax /
Bouffalant wall (4.9%), Orthworm ex / Archaludon (7.4%), the Aurorus wall
(9.3%), Arboliva ex (9.5%), Munkidori ex / Pecharunt ex (11.7%).

Best: Mew / Pikachu box (93.8%), Drapion (90.7%), Mew / Hypno (88.8%).

The field has one Delta Reign deck (Mega Malamar ex).

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | Submitted | This list |
|---|---|---|
| Masquerain | 72.5% (avg turn 3.09) | 72.6% (3.24) |
| Jellicent | 62.0% (3.09) | 33.8% (3.70) |
| First attack by turn 6 | 96.6% (2.54) | 99.3% (2.28) |

## Import

```
Pokémon: 24
4 Surskit DLR 2
4 Masquerain DLR 3
4 Spinarak DLR 58
4 Combee DLR 6
4 Sizzlipede PBL 9
2 Frillish WHT 44
2 Jellicent DLR 28

Trainer: 25
4 Lillie's Determination MEG 119
4 Kofu SCR 138
4 Lana's Aid TWM 155
4 Hilda WHT 84
4 Poké Pad ASC 198
4 Night Stretcher ASC 196
1 Forest of Vitality MEG 117

Energy: 11
10 Basic Grass Energy
1 Legacy Energy TWM 167

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-11-09/bug_out_screens`. The list is in
the field as `decks/field/bug_out_masquerain_jellicent.txt`.
