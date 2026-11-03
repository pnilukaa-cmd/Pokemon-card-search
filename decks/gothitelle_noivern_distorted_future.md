# Gothitelle / Noivern: Distorted Future

Built 2026-11-02 from a request: a deck around Gothitelle's Distorted
Future (the opponent's hand to 3), paired with an easy hand discard
(Talonflame's Sky Hunt), Rare Candy, and Fletchling's Chirp to find the
Pokémon with Fighting Resistance.

**This list: 39.19% against the 103-deck field at 1000 games per
opponent** (median 37.3%, 31 of 103 winning), on the engine as of bfb7a80.
The list as asked (Gothitelle, a 4-2-2 Fletchling / Talonflame line, Rare
Candy; `V0` in the archive) reads 24.56% (median 20.9%, 10 winning). On the
same seeds this list is **+14.64 ± 0.82** over it, better on 102 of 103.

## What makes the deck work

- **Gothitelle** (WHT 43, Stage 2 Psychic, 150 HP, Retreat 2, weak to
  Darkness, Fighting Resistance):
  - **Distorted Future**: once during your turn, **while it is in the
    Active Spot**, the opponent shuffles their hand into their deck and
    draws 3.
  - **Synchro Shot** (Psychic, Colorless): 90, plus 90 if you have the same
    number of cards in your hand as your opponent. So Distorted Future is
    half of a 180: it sets their hand to 3, and your hand has to be 3 too.
- **Noivern** (JTG 128, Stage 1 Colorless, 110 HP, **no Retreat Cost**):
  Tuning Echo makes Frightening Howl (110, and the Defending Pokémon is
  Confused) cost nothing while the hands match. With 3 Energy it is a
  plain 110 attacker, and with no Retreat Cost it is also the pivot that
  lets Gothitelle come back to the Active Spot.
- **Noibat** (JTG 127): Rapid Draw (Colorless): draw a card. The one way
  this deck has to grow its own hand when it is the short one.
- **Team Rocket's Chingling** (DRI 85, Basic, 30 HP, no Retreat Cost):
  Chiming Commotion costs nothing and discards a random card from the
  opponent's hand. The easy hand discard, on a Basic.
- **Xerosic's Machinations**: the opponent discards down to 3, whoever is
  in your Active Spot.

Their hand was 3 or fewer on 97% of this list's Synchro Shots.

## What the measurements say

Every change is paired against the list of its round, 200 games a
matchup. Your three suggested pieces:

- **Talonflame's Sky Hunt doesn't earn its slots.** It is a coin flip for
  one card, on a Stage 2 Fire line whose attacks the Psychic Energy can't
  pay. The 2-2 line against a 4th Gothitelle, a 3rd Gothorita and 2 Hilda:
  −3.64 ± 0.46. A 1-1 line: −2.22 ± 0.49. A 3rd line on the first list:
  −0.07.
- **Fletchling's Chirp doesn't either.** Everything in the deck has
  Fighting Resistance, so Chirp finds any of it, but only as the Active's
  attack. Noibat (also Fighting Resistance) is the better Basic: 4 Noibat
  for 2 Fletchling +3.18 ± 0.45, no Fletchling +4.61 ± 0.60, 2 Fletchling
  back −4.76 ± 0.51.
- **Rare Candy stays at 4** (not varied), for a 4-3-4 Gothitelle line.

| Round | From | Change | Measured |
|---|---|---|---|
| 1 | as asked | Matching hands before Synchro Shot (engine) | **+1.17 ± 0.36**, +1.80 ± 0.45 |
| 1 | as asked | 2 Iron Boulder (Adjusted Horn: 170, nothing on unequal hands) | −4.10 ± 0.47 |
| 1 | as asked | 2 Hand Trimmer | +0.40 ± 0.34 |
| 2 | as asked | Noivern 2-2 | +1.42 ± 0.50, +0.31 ± 0.57 |
| 2 | as asked | 2 fewer Lillie's Determination | −2.09 ± 0.46 |
| 2 | as asked | Xerosic's: none / 4 | −0.77 / +0.54 |
| 3 | as asked | Krookodile 2-1-2 (Cursed Slug, 240 on 3 or fewer) | −0.83 ± 0.56 |
| 3 | as asked | 12 Energy (for 2 Petrel) | **+2.22 ± 0.44** |
| 4 | 12 Energy | Noivern 2-2, no Talonflame line, 14 Energy | **+4.89 ± 0.55** |
| 4 | 12 Energy | 14 Energy, Talonflame kept | −0.03 ± 0.41 |
| 5 | round 4's best | 4 Noibat for 2 Fletchling | **+3.18 ± 0.45** |
| 5 | round 4's best | back to 12 Energy / a 2nd Switch / a 3rd Xerosic's | −3.21 / −0.88 / −1.59 |
| 6 | 4 Noibat | No Fletchling (+ a 3rd Noivern, a 15th Energy) | **+4.61 ± 0.60** |
| 6 | 4 Noibat | 4th Noivern / 16 Energy | −2.64 / +1.32 |
| 7 | no Fletchling | 2 Chingling (for a Hilda and a Night Stretcher) | −0.08 ± 0.45 |
| 7 | no Fletchling | Budew / 16 Energy | −0.15 / −0.30 |

The last round left two lists level: this one and the same list without
Chingling. This one has 10 Basic Pokémon against 8: a 25.9% chance of no
Basic in the opening hand, against 34.6%.

**Energy.** 12 beat 10 (+2.22). In the Noivern lists 14 beat 12 (going
back cost 3.21), and 16 read +1.32 once and −0.30 once, so the list stops
at 15. With Talonflame kept, 14 was no better than 12 (−0.03). Read Energy
gains with the usual caution, since this simulator overrates Energy (see
`decks/mega_froslass_ex_resentful_refrain.md`); here every attacker pays
it: Synchro Shot 2, Frightening Howl 3 on unequal hands, Gothitelle's
retreat 2.

## How it plays, turn by turn

- **Your first turns:** Gothita, Noibat and Chingling to the Bench
  (Buddy-Buddy Poffin takes any two). Chingling's free Chiming Commotion
  from the Active Spot strips a card while the board builds. Rare Candy
  can't be used on your first turn or on a Gothita played that turn, so
  Gothitelle comes on your second turn at the earliest, from a Gothita that was
  already down.
- **Each turn with Gothitelle Active:** Distorted Future sets their hand
  to 3, Synchro Shot hits for 180 if your hand is 3 too, else 90. The
  simulator now holds Distorted Future until just before the attack and
  sheds cards to match (a Basic to the Bench, Ultra Ball for two). Doing
  it by hand: count the cards you will have left after the turn's
  attachment and plays, and use Distorted Future last.
- **Their turn, and their outs:** they start it with 4 cards (3 and the
  draw), and a draw Supporter refills them. Gothitelle has 150 HP (250
  with Hero's Cape) and is weak to Darkness, so most ex attackers Knock it
  Out in one hit, and the next one needs Rare Candy again. Distorted
  Future only works from the Active Spot; a gust that drags up a Benched
  Pokémon turns it off until Gothitelle comes back (Noivern's free retreat
  or Switch).
- **Noivern** swings on the turns Gothitelle can't, Confusing the
  Defending Pokémon, and costs nothing on matched hands.

## Engine changes made for this deck

- **Matching hands** (`hand_match`, on): a deck with a payoff for equal
  hands holds Distorted Future and Sky Hunt until just before the attack,
  picks the count it can reach, sheds cards to it and fires what it
  takes. Synchro Shot matched 18% → 38% of the time on the first lists.
  No field deck has such a payoff.
- **Tuning Echo and Synchro Pulse** ("If you have the same number of cards
  in your hand as your opponent, ...") compiled with no condition:
  Noivern attacked for free on any hand. They are gated now. No field
  deck runs either.
- **Fletchling's Chirp** found any 2 Pokémon; searches read "with Fighting
  Resistance" now.
- **The mechanic index** has `hand_size_match_payoff` (Gothitelle, Iron
  Boulder, Noivern, Ampharos) and `opponent_small_hand_payoff`
  (Krookodile, Mienshao, Decidueye ex), which sat under unrelated tags.

## Where it loses

At 1000 games, the list as asked → this list:

| Opponent | As asked | This list |
|---|---|---|
| Snorlax / Bouffalant / Mega Kangaskhan ex wall | 0.4% | 1.1% |
| Mega Zygarde ex / Cinderace | 0.7% | 1.9% |
| Aurorus / Mega Kangaskhan ex (Tundra Wall) | 0.7% | 2.3% |
| Mega Zeraora ex / Cinderace | 0.4% | 2.7% |
| Munkidori ex / Pecharunt ex | 0.7% | 3.8% |
| Orthworm ex / Metang / Archaludon ex | 2.7% | 6.6% |
| Arboliva ex / Ogerpon | 4.8% | 8.5% |
| Dragapult ex (pure / Dusknoir / Blaziken) | 16.6 / 26.3 / 18.0% | 27.4 / 38.3 / 26.8% |
| Mega Excadrill ex | 9.8% | 20.4% |
| Raging Bolt ex / Slowking / N's Zoroark ex | 20.2 / 20.9 / 29.1% | 36.9 / 38.3 / 37.4% |
| Festival Lead | 58.6% | 62.3% |

The two Mega Kangaskhan ex walls, both Cinderace decks and Munkidori ex /
Pecharunt ex beat it almost every game. It beats mill and lock decks: Flygon mill
96.5%, Chandelure / Maushold / Dudunsparce 91.5%, Mew ex baby box 90.5%.

It is a Stage 2 deck whose attacker has 150 HP and hits for 180 at best,
in a field of 230–340 HP ex: a 180 needs two hits on most of them. The
simulated opponents don't keep their hand at a count that dodges the
match, but they don't need to: they lose 3 or more cards a turn and still
win most games. Gothitelle's value is the disruption; the damage is the
weak half.

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | As asked | This list |
|---|---|---|
| Gothitelle | 66.7% (avg turn 3.73) | 56.7% (3.79) |
| Talonflame / Noivern | 50.3% (3.91) | 61.0% (3.22) |
| First attack by turn 6 | 88.0% (3.10) | 93.2% (2.67) |

Slower to its first Gothitelle (it gave up Chirp, Petrel and Poké Pad),
faster to an attack: Noivern and Chingling attack while Gothitelle is
still coming.

## Import

```
Pokémon: 20
4 Gothita WHT 124
3 Gothorita WHT 125
4 Gothitelle WHT 43
4 Noibat JTG 127
3 Noivern JTG 128
2 Team Rocket's Chingling DRI 85

Trainer: 25
4 Lillie's Determination MEG 119
2 Hilda WHT 164
2 Xerosic's Machinations SFA 64
2 Boss's Orders MEG 114
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Night Stretcher MEG 173
1 Switch MEG 130
1 Hero's Cape TEF 152

Energy: 15
15 Basic Psychic Energy

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-11-02/gothitelle_screens`. The list is
in the field as `decks/field/gothitelle_noivern_distorted_future.txt`.
