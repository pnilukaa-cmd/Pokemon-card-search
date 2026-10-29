# Mega Froslass ex: Resentful Refrain

Reviewed 2026-10-29 from a submitted list: 3 Mega Froslass ex on 3 Snorunt,
a 3-1-3 Chandelure line (TWM 38, Alluring Light) on 3 Rare Candy, 2
Dudunsparce, Meowth ex and Budew, with 6 Energy (4 Water, 2 Fire). Asked
with it: how does this deck win — forcing draws for big Froslass hits? Are
there other win conditions?

**This list: 71.02% against the 102-deck field at 1000 games per
opponent** (median 73.2%, 94 of 102 winning), on the engine as of 51ff3d5.
On the same seeds it is **+14.09 ± 0.51** over the submitted list
(56.93%, 70 winning), better on all 102.

**The changes:**
- **4 Mega Froslass ex on 4 Snorunt** (+1 of each).
- **9 Energy: 7 Water, 2 Fire** (+3 Basic Water Energy).
- **4 Night Stretcher** (+2).
- **Out:** 2 Lucian, 2 Ultra Ball, 2 Team Rocket's Petrel, Pokégear 3.0.

## The short answer

- **It wins with Resentful Refrain, and the hand it hits is mostly the
  opponent's own.** Mega Froslass ex took 83% of the submitted list's
  Prizes with it, against an average of 6.8 cards in hand. Of those, the
  deck had added 0.8 itself that turn; on 128 of 275 hits it added none.
  At 6 cards it is 300 and Knocks Out 93% of the time, at 7 or more every
  time. The opponent came into the turn holding about 6 of their own.
- **Forcing draws matters, but mostly not as damage.** Chandelure's
  Alluring Light ("each player draws a card") fires 3.45 times a game. Used
  only on a turn Resentful Refrain fires it measured −3.23 ± 0.52; never,
  −4.43 ± 0.66. Three quarters of what it is worth comes on other turns:
  it is this deck's draw engine as much as a damage booster.
- **Lucian is not a forced draw.** It sends both hands to the bottom and
  each player draws 3 or 6, so it only grows a hand of 3 or fewer. Two
  Night Stretcher in place of the two Lucian measured +1.34 ± 0.50. The
  simulator used to play it as "each player draws 3", three free cards
  for the opponent, and the list read 2.52 points better for it.
- **The list lost games to Water, not to damage.** With its 6 Energy (on
  the list with the 4th Snorunt and Mega Froslass ex), an Active Mega
  Froslass ex ended 1.00 turn a game without attacking for want of Water,
  and on 0.94 of those there was no Energy in hand at all. With 9 Energy:
  0.19. Resentful Refrain costs one Water and Wally's Compassion
  hands it back, so the deck needs few, but it needs one every turn.
- **The other win conditions are real and small:**
  - Absolute Snow (150 and Asleep) takes the Knock Out when the hand is
    small: 7–11% of Prizes, at an average opposing hand of 2.2–2.6.
  - Chandelure's Mind Ruler (30 a card) takes 9%.
  - The opponent decking out ends about one win in ten (8 of 73 logged
    wins, 9 of 90 for this list): Alluring Light draws them a card each
    turn too.

## How it wins, measured

`attacks.py` (in the archive): every attack the deck made in 120 logged
games, 15 each against the six meta decks, Krookodile ex hand disruption
and Mega Absol ex hand lock. "Added" is the opposing hand at the attack
minus the opposing hand when the turn began.

| | Submitted list | This list |
|---|---|---|
| Wins | 73 / 120 | 90 / 120 |
| Attacks a game | 3.78 | 4.44 |
| Resentful Refrain a game | 2.29 | 2.52 |
| — share of Prizes | 83% | 79% |
| — opposing hand when it fires | 6.8 | 6.3 |
| — of which added that turn | +0.8 | +0.6 |
| Absolute Snow a game (share of Prizes) | 0.27 (7%) | 0.49 (11%) |
| Mind Ruler a game (share of Prizes) | 0.36 (9%) | 0.40 (9%) |
| Wins by the opponent decking out / no Pokémon | 8 / 5 | 9 / 9 |

Resentful Refrain by the size of the hand it hit (submitted list):

| Hand | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8+ |
|---|---|---|---|---|---|---|---|---|
| Hits | 8 | 19 | 22 | 34 | 31 | 30 | 32 | 99 |
| Knocked Out | 50% | 42% | 77% | 65% | 81% | 93% | 100% | 100% |

So the deck's real question each turn is not how to make the opponent draw
but whether there is a Mega Froslass ex in the Active Spot with a Water on
it. The changes are all about that:

- **The 4th Snorunt** (+3.99 ± 0.51 once the 4th Mega Froslass ex is in):
  turns from turn 3 with neither a Snorunt nor a Mega Froslass ex in play
  fall from 10.5% to 4.1%, and Resentful Refrain fires 2.44 times a game
  (1.89). A 4th Mega Froslass ex on 3 Snorunt is only +0.38 to +1.30.
- **Water** (the 7th and 8th Energy +4.62 and +2.96, a Fire in the same slot
  only +1.19): the turns lost without Water above.
- **Night Stretcher** brings back a Snorunt, a Mega Froslass ex or a Basic
  Energy; Ultra Ball costs two cards. 2 Night Stretcher for the 2 Ultra
  Ball: +1.63 and +2.49.

## The strategy, card by card

- **Mega Froslass ex** (ASC 265 / 275, Stage 1 Mega Water, 310 HP, Retreat
  1, weak to Metal; gives up **3 Prizes**):
  - **Resentful Refrain** (Water): 50 for each card in the opponent's hand.
  - **Absolute Snow** (Water, Colorless, Colorless): 150, and the
    opponent's Active is Asleep.
- **Chandelure** (TWM 38, Stage 2 Fire, 130 HP, Retreat 2, weak to Water):
  - **Alluring Light**: once during your turn, each player draws a card.
    Each Chandelure in play is one more.
  - **Mind Ruler** (Fire): 30 for each card in the opponent's hand.
- **Getting there:** Salvatore evolves a Snorunt into Mega Froslass ex from
  the deck, even one benched this turn (it takes a card with no
  Abilities, so not Chandelure); Rare Candy takes Litwick to Chandelure;
  Hilda finds an Evolution Pokémon and an Energy; Poké Pad, Buddy-Buddy
  Poffin, Lillie's Determination, Dudunsparce's Run Away Draw, Meowth ex's
  Last-Ditch Catch (a Supporter).
- **Keeping it alive:** Hero's Cape (+100 HP: a 410 HP Mega Froslass ex),
  Wally's Compassion (heal all of a Mega ex's damage; its Energy goes to
  your hand, and one Water re-pays Resentful Refrain the same turn),
  Battle Cage (no damage counters on Benched Pokémon from attacks and
  Abilities).
- **Keeping their hand big:** Budew's Itchy Pollen (no Items next turn:
  they stay in hand).
- **Litwick (PBL 36) is Psychic**, and nothing here pays Will-O-Wisp. It is
  only there to evolve.

Beyond the cuts above, every card tried against a Night Stretcher
measured within about half a point of it (below), so the rest stays as
submitted.

## What the measurements say

Each change below is paired against the list of its round, 200 games a
matchup. Round 1 used Ultra Ball as the card that comes in. Ultra Ball is
weak here (it costs two cards), so that read every cut as a loss (round 2:
2 Wally's for 2 Ultra Ball −2.73, for 2 Night Stretcher −0.29), and from
round 3 the card that comes in is Night Stretcher.

| Round | List | Change | Measured |
|---|---|---|---|
| 1 | submitted | Lucian as printed (engine fix) | −2.52 ± 0.59 |
| 1 | submitted | 4th Mega Froslass ex for Pokégear 3.0 | **+1.30 ± 0.47** |
| 1 | submitted | Ultra Ball in for: Hero's Cape / 2 Wally's | −3.35 / −2.50 |
| 1 | submitted | Ultra Ball in for: Salvatore / 2 Battle Cage | −2.27 / −2.27 |
| 1 | submitted | Ultra Ball in for: 2 Lucian / Budew / a Chandelure | −1.38 / −1.19 / −1.11 |
| 1 | submitted | Ultra Ball in for: 2 Petrel / a Lucian | −0.66 / −0.48 |
| 1 | submitted | 4th Chandelure for Pokégear 3.0 | −0.53 ± 0.43 |
| 2 | submitted | Alluring Light only on a Resentful Refrain turn / never | −3.23 / −4.43 |
| 2 | 4 Froslass | 4th Snorunt for a Petrel | **+3.99 ± 0.51** |
| 2 | 4 Froslass | 5th Water for a Petrel | **+3.62 ± 0.44** |
| 2 | 4 Froslass | 4th Wally's / 3rd Lucian / 3rd Ultra Ball for a Petrel | +0.76 / +0.66 / +0.21 |
| 3 | + Snorunt | 5th Water / 3rd Fire for the last Petrel | **+4.62** / +1.19 |
| 3 | + Snorunt | 2 Night Stretcher for: 2 Ultra Ball / 2 Lucian / 2 Wally's | **+1.63** / **+1.34** / −0.56 |
| 3 | + Snorunt | Night Stretcher for: Budew / a Battle Cage / a Boss's Orders | +0.02 / +0.09 / +0.01 |
| 3 | + Snorunt | Night Stretcher for: Salvatore / a Chandelure | −0.12 / −0.61 |
| 3 | + Snorunt | 4th Litwick for the last Petrel | +0.49 ± 0.52 |
| 4 | + Water | 2 Night Stretcher + 2 Water for 2 Ultra Ball + 2 Lucian | **+5.72 ± 0.48** |
| 4 | + Water | 2 Water for 2 Lucian / Water for a Lucian | +4.63 / +2.96 |
| 4 | + Water | 2 Night Stretcher for 2 Ultra Ball / 2 Lucian | +2.49 / +1.01 |
| 5 | this list | 10th Energy (Water) for Budew / a Battle Cage / a Boss's Orders / a Wally's | +1.65 / +1.20 / +1.86 / +1.21 |
| 5 | this list | 10th Energy (Water) for Salvatore | −0.14 ± 0.44 |
| 5 | this list | 8 Energy (a Water out for an Ultra Ball / a Lucian) | −1.55 / −1.54 |
| 5 | this list | 3rd Fire for a Water | −1.15 ± 0.47 |

Standard errors are about ±0.45–0.55 throughout.

**Why this stops at 9 Energy.** Swapping an Energy in for anything reads
well in this simulator, whose AI is Energy-hungry (see the Boss's Orders
re-measure in `decks/jellicent_ex_oceanic_curse.md`): here it also puts
Water on Dunsparce and Meowth ex 0.65–0.82 times a game. Up to 9 the gain has a
cause measured directly (the turns an Active Mega Froslass ex sat without
Water, 1.00 → 0.19 a game), and Water beats Fire by 3.4 points in the same
slot. A 10th Energy has at most 0.19 turns a game left to win back, so most
of its +1.2 to +1.9 is the bias, and it would cost a Boss's Orders, a
Battle Cage or Budew.

## Where it loses

At 1000 games, submitted list → this list:

| Opponent | Submitted | This list |
|---|---|---|
| Orthworm ex / Metang / Archaludon ex (Metal) | 29.7% | 39.4% |
| Arboliva ex / Ogerpon | 32.1% | 44.6% |
| Chesnaught / Meganium | 36.0% | 44.7% |
| Mega Gengar ex / Toxtricity | 31.3% | 46.1% |
| Mega Zeraora ex / Cinderace | 34.8% | 47.4% |
| Gourgeist / Diggersby | 32.5% | 49.2% |
| Mega Absol ex hand lock | 32.7% | 49.5% |
| Mew ex / Alex / Centiskorch mill | 35.3% | 50.5% |
| Jellicent ex Item lock | 30.0% | 51.0% |
| Dragapult ex (pure / Dusknoir / Blaziken) | 57.2 / 58.7 / 66.7% | 69.2 / 72.2 / 74.9% |
| Mega Excadrill ex | 42.9% | 53.8% |
| Raging Bolt ex | 71.3% | 77.3% |
| Slowking / Festival Lead / N's Zoroark ex | 77.2 / 83.1 / 84.6% | 84.7 / 86.0 / 89.3% |

The 8 it still loses: the Metal list (Mega Froslass ex is weak to Metal),
Arboliva ex, Chesnaught / Meganium, Mega Gengar ex, Mega Zeraora ex,
Hydrapple / Seaking Festival Lead (47.6%), Gourgeist and the Mega Absol ex
hand lock. Against a hand lock or a mill deck the opposing hand stays
small, and against mill Alluring Light costs this deck a card of its own
deck too.

**A caveat that matters for this deck in particular.** The simulator's
opponents do not play around a hand-counting attacker: they draw and keep
cards the way they would against anything. A human opponent facing Mega
Froslass ex will bench, attach and play Items out, skip a draw Supporter,
or keep a hand reset for the turn it attacks. The measured hand of 6–7 is
an upper end, and Absolute Snow and Mind Ruler matter more against a
careful opponent than here.

## Engine changes made for this review

- **Lucian** compiled as "each player draws 3". It is hand-written now:
  each player puts their hand on the bottom of their deck and draws 6 on
  heads, 3 on tails, and the card-text fallback no longer plays it. It is
  played to refill a hand of 3 or fewer when the Active's attack counts
  the opponent's hand, and as disruption against 7 or more otherwise. No
  field deck runs it.
- **Tried and taken out:** Alluring Light gated to attack turns (above);
  keeping Lucian off a big hand while a hand-counting attacker waits on
  the Bench (+0.42 ± 0.49).
- **Also taken out:** counting Wally's Compassion as free on an Active
  whose one-Energy attack the returned Energy re-pays the same turn. Four
  200-game screens read +0.30 to +0.75; at 1000 games, +0.21 ± 0.22.
- **The setup baseline** matched "evolves from" against the deck's own key
  for a card, so Dudunsparce never evolved from "Dunsparce (JTG 120)", the
  second printing; it plays Salvatore and Lucian now.
- **`search_mechanic.py --sweep-phrase`** matched case-sensitively and
  missed Frosmoth's "Each player draws a card." The pool has three
  mutual-draw cards (`mutual_draw`): Chandelure's Alluring Light,
  Frosmoth's Alluring Wings (ASC 53, Active only) and Comfey's Flower
  Shower (an attack).

## Other ways to grow their hand

The search for cards that grow the opponent's hand finds little that
doesn't cost the attack:
- **Frosmoth** (ASC 53) Alluring Wings is the same draw, but only from the
  Active Spot, where Mega Froslass ex needs to be.
- **Dustox** (ASC 15, Boisterous Wind, an Energy to their hand on heads)
  and **Archeops** (WHT 132, Ancient Wing, devolve from the Active Spot)
  are Abilities on Stage 2 lines.
- Espathra, Espeon, Slowking, Octillery, Unfezant and Paldean Tauros put
  cards into their hand with an **attack**, which is the turn's attack.
- Judge sets each hand to 4 (200 for Resentful Refrain); Lucian to 3 or 6.

## Setup baseline

`simulate_baseline.py`, 1000 trials, in play by turn 6:

| | Submitted | This list |
|---|---|---|
| Mega Froslass ex | 79.1% (avg turn 3.08) | 76.5% (2.92) |
| Chandelure | 47.8% (4.01) | 38.1% (3.96) |
| Dudunsparce | 48.2% (3.57) | 34.8% (3.64) |
| First attack by turn 6 | 91.1% (2.74) | 93.0% (2.61) |

Without the Ultra Ball, Petrel and Pokégear 3.0 it is a little slower to
its first Mega Froslass ex and Chandelure. The baseline has no opponent and
no Knock Outs, so the second and third Mega Froslass ex, and the Water to
attack with each turn, are what it can't see. 11 Basic Pokémon (10
submitted): a 22.2% chance of no Basic in the opening 7 (25.9%).

## Printings

The submitted Boss's Orders RCL 189, Rare Candy PLB 105, Energy Search SVI
172, Ultra Ball PLF 122 and Pokégear 3.0 UNB 233 are older printings, from
sets this Standard pool (regulation marks H–J) doesn't carry; the cards are
legal through their current printings, and the import uses Boss's Orders
MEG 114, Rare Candy MEG 125 and Energy Search POR 72. Every other number
checks out: the Pokémon this pool lists at other numbers (Snorunt ASC 227,
Dudunsparce TEF 129, Lampent WHT 102, Meowth ex POR 107, Budew ASC 16) are
the same cards. Basic Energy is written the way PTCGL imports it ("7 Basic
Water Energy"), not "4 Basic W".

```
Pokémon: 21
4 Snorunt ASC 46
2 Mega Froslass ex ASC 275
2 Mega Froslass ex ASC 265
3 Litwick PBL 36
1 Lampent WHT 17
3 Chandelure TWM 38
1 Dunsparce TEF 128
1 Dunsparce JTG 120
2 Dudunsparce PRE 80
1 Meowth ex POR 121
1 Budew ASC 221

Trainer: 30
3 Lillie's Determination MEG 169
2 Hilda WHT 171
3 Wally's Compassion MEG 186
2 Boss's Orders MEG 114
1 Salvatore TEF 202
4 Buddy-Buddy Poffin MEG 167
4 Poké Pad POR 113
4 Night Stretcher MEG 173
3 Rare Candy MEG 125
1 Energy Search POR 72
1 Hero's Cape TEF 152
2 Battle Cage PFL 116

Energy: 9
7 Basic Water Energy
2 Basic Fire Energy

Total Cards: 60
```

Runs, lists and scripts: `runs/2026-10-29/froslass_screens`. The list is in
the field as `decks/field/mega_froslass_ex_resentful_refrain.txt`.
