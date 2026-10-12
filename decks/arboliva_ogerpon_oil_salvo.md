# Arboliva ex / Teal Mask Ogerpon ex Oil Salvo

Built 2026-10-12 around Arboliva ex DRI 207, starting from the shape of
real tournament lists. Shun Akita's 4th place at Regional Melbourne 2026
("Ogerpon Meganium") ran Teal Mask Ogerpon ex, Arboliva ex, Meganium,
Meowth ex, Celebi and Fezandipiti ex.

**86.54% against the 87-deck field at 1000 games per opponent.** It wins
all 87 matchups (median 90.1%). On the same seeds:
- **+9.92 ± 0.50** over the Ogerpon / Arboliva start (76.62%), better on
  86 of 87.
- **+11.79 ± 0.55** over the Akita-style list with the Meganium line
  (74.76%), better on all 87.

**Lines:** Smoliv → Dolliv → Arboliva ex (Rare Candy and Forest of
Vitality), Teal Mask Ogerpon ex, Fezandipiti ex.

## Plan

**Arboliva ex** (Stage 2, 310 HP) has two attacks:
- **Oil Salvo** (G): choose an opponent's Pokémon six times and do 20 each
  time, ignoring Weakness and Resistance. That is 120 for one Energy, spread
  to finish damaged Pokémon or take two 60 HP Basics in one attack.
- **Aroma Shot** (CCC): 160, and it recovers from Special Conditions.

**Teal Mask Ogerpon ex** (Basic Tera, 210 HP) is the other attacker:
- **Teal Dance:** once a turn, attach a Basic Grass Energy from your hand to
  it and draw a card.
- **Myriad Leaf Shower** (GGG): 30 plus 30 for each Energy on both Active
  Pokémon, usually 150-210.
- As a Tera Pokémon it takes no damage from attacks while it is on the
  Bench.

The two cover each other:
- Ogerpon hits the Active hard.
- Oil Salvo cleans up what Ogerpon leaves damaged, and the small Basics
  behind it.
- **Fezandipiti ex**'s Flip the Script draws 3 after one of your Pokémon is
  Knocked Out.

## How to play

1. **Turn 1.** Buddy-Buddy Poffin puts two Smoliv (60 HP) on the Bench.
   Ultra Ball finds an Ogerpon. Attach a Grass Energy, and Teal Dance
   another from your hand. Rare Candy can't be played on your first turn.
2. **Opponent's turn.** A Benched Smoliv is an easy Knock Out for a
   Bench-sniper. Forest of Vitality is the way around it.
3. **Turn 2.** Make an Arboliva ex one of two ways:
   - Rare Candy a Smoliv that has been in play since last turn.
   - With Forest of Vitality in play, play a Smoliv from your hand and
     evolve it to Dolliv, then to Arboliva ex, all this turn.

   Then Oil Salvo for one Grass Energy, or Myriad Leaf Shower with the
   Ogerpon.
4. **After that.** Oil Salvo whenever its six hits Knock Out something;
   otherwise Myriad Leaf Shower or Aroma Shot. Boss's Orders (2) brings a
   damaged Pokémon up for the finish.

**Matchups (1000 games):**
- **Worst:** Mega Zeraora ex / Cinderace 54.3%, Tauros 61.1%, Mega Zygarde
  ex / Cinderace 63.0%, then the mill decks (Maushold 65.1%, Mega Excadrill
  65.9%, Flygon 67.2%, Centiskorch 69.2%).
- **Best:** Mew / Hypno 98.5%, Wobbuffet / Orbeetle 97.9%, Mew baby box
  97.8%, Mega Scrafty ex 96.9%.

## What the simulator found

**Two engine fixes** were needed before this deck could be measured at all
(2026-10-12):
- **Oil Salvo's six hits went round the board one at a time.** A Pokémon
  one hit from a Knock Out could get one hit while a fresh 3-Prize Active
  took 40. The six hits are now a budget: spent on the set of Knock Outs
  worth the most Prizes, the rest on the most valuable survivor.
- **Oil Salvo was priced at a flat 120**, so Aroma Shot's 160 always won,
  even with three Benched Knock Outs on offer. It is now worth its damage
  plus those Knock Outs.
- **Meganium's Wild Growth did nothing.** Each Basic Grass Energy should
  provide GrassGrass, but every cost check and every "for each Energy"
  count read one per card. It now counts double, and the Meganium build was
  measured after the fix.

**The Meganium line doesn't pay for itself here.** With Wild Growth working,
the Akita-style list with Chikorita / Bayleef / 2 Meganium measured −1.87 ±
0.41 against the same deck without it. A second Stage 2 line costs more
than doubling Ogerpon's Energy gives.

**The other partner tried, Dusknoir** (Cursed Blast finishes what Oil Salvo
spreads), measured 56.91%, far behind.

## How it was tuned

200 games against each field deck, paired on the same seeds. Each round
is paired against the best list of the round before. Rounds 0-2 ran on
the 86-deck field. Rounds 3-5 ran on the 87-deck field that went in with
the Lightning Cinderace list (base rerun). Lists and results are in
`runs/2026-10-12/arboliva_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Dusknoir spread build | 56.91% | |
| 0 | Ogerpon / Meganium (Akita-style) | 74.48% | |
| 0 | **Ogerpon, no Meganium** | **77.23%** | |
| 1 | 3rd Boss's Orders (−Iris's) | 75.46% | −1.77 ± 0.40 |
| 1 | 2nd Celebi (−Iris's) | 75.73% | −1.49 ± 0.43 |
| 1 | 2 Jumbo Ice Cream (−Iris's, −Night Stretcher) | 76.46% | −0.77 ± 0.42 |
| 1 | 3rd Dolliv (−Iris's) | 76.77% | −0.46 ± 0.40 |
| 1 | 4th Arboliva ex (−Iris's) | 77.20% | −0.02 ± 0.43 |
| 1 | −Iris's, +1 Energy | 78.17% | +0.95 ± 0.41 |
| 1 | −Fezandipiti ex, +1 Energy | 78.76% | +1.53 ± 0.43 |
| 1 | −Night Stretcher, +1 Energy | 78.98% | +1.76 ± 0.43 |
| 1 | −Forest of Vitality, +1 Energy | 79.34% | +2.11 ± 0.38 |
| 1 | −Meowth ex, +1 Energy | 79.50% | +2.27 ± 0.38 |
| 1 | **−Ogerpon, +1 Energy** | **80.15%** | **+2.92 ± 0.45** |
| 2 | 2 Ogerpon (+1 Energy) | 78.69% | −1.45 ± 0.48 |
| 2 | −Forest, −Meowth ex, +Arboliva ex, +1 Energy | 81.76% | +1.62 ± 0.42 |
| 2 | −Forest, −Meowth ex, +2 Energy | 82.41% | +2.27 ± 0.45 |
| 2 | **−Forest, −Meowth ex, −Night Stretcher, +3 Energy** | **83.59%** | **+3.44 ± 0.46** |
| 3 | 87-deck field: base | 82.37% | |
| 3 | −1 Forest, +1 Energy | 82.98% | +0.60 ± 0.42 |
| 3 | −Switch, +1 Energy | 83.09% | +0.72 ± 0.40 |
| 3 | −Celebi, +1 Energy | 83.74% | +1.36 ± 0.40 |
| 3 | **−last Meowth ex, +1 Energy** | **84.21%** | **+1.84 ± 0.42** |
| 4 | Bloodmoon Ursaluna ex for Celebi | 81.12% | −3.09 ± 0.47 |
| 4 | Mega Kangaskhan ex for Celebi | 82.49% | −1.72 ± 0.39 |
| 4 | 4th Ogerpon for Celebi | 85.37% | +1.16 ± 0.42 |
| 4 | **−Celebi, −Switch, +2 Energy** | **85.57%** | **+1.36 ± 0.43** |
| 5 | −Fezandipiti ex, +1 Energy | 84.75% | −0.82 ± 0.44 |
| 5 | 4th Arboliva ex (−1 Energy) | 86.14% | +0.57 ± 0.40 |
| 5 | **4th Ogerpon (−1 Energy) (this list)** | **86.59%** | **+1.02 ± 0.42** |
| 1000 games | Akita-style / Ogerpon start / this list | 74.76% / 76.62% / **86.54%** | **+9.92 ± 0.50** |
| 1000 games | This list + 4th Arboliva ex (−1 Energy) | 86.51% | −0.03 ± 0.20 |

**What made the difference:** Energy, again. Teal Dance wants a Grass
Energy in hand every turn. Myriad Leaf Shower counts every Energy attached,
and Oil Salvo and Aroma Shot need theirs too. The start ran 14 Grass Energy.
Every round's best change traded a situational card for one:
- Meowth ex (2)
- Celebi
- Night Stretcher
- Switch
- a Forest of Vitality

That took it to 20. Ogerpon went to 3 and back to 4 along the way.

Logged against six hard opponents (Raging Bolt, Dragapult, Raticate, N's
Zoroark, Tauros, Lurantis), this list won 41 of 60. Per game it used Oil
Salvo 1.7 times, Myriad Leaf Shower 2.1 and Aroma Shot 0.3.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Teal Mask Ogerpon ex | 89.1% | 1.62 |
| Smoliv | 94.3% | 1.59 |
| Dolliv | 48.3% | 3.28 |
| Arboliva ex | 41.9% | 3.76 |
| Fezandipiti ex | 53.2% | 2.43 |

First attack by turn 6 in 88.4% of games (average turn 3.23). The baseline
doesn't model Bug Catching Set, Teal Dance or Forest of Vitality's
same-turn evolution, so Arboliva ex comes down sooner in real games than
this shows.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
Every attack is payable with Grass Energy. 8 Basics (mulligan 34.6%); the
win rates include it.

## PTCGL import

```
Pokémon: 13
3 Smoliv DRI 21
2 Dolliv DRI 22
3 Arboliva ex DRI 207
4 Teal Mask Ogerpon ex TWM 190
1 Fezandipiti ex ASC 142

Trainer: 27
4 Lillie's Determination MEG 184
2 Iris's Fighting Spirit JTG 180
2 Boss's Orders MEG 114
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
3 Bug Catching Set TWM 143
1 Night Stretcher MEG 173
1 Hero's Cape TEF 152
2 Forest of Vitality MEG 117

Energy: 20
20 Basic Grass Energy

Total Cards: 60
```

Sources for the real lists:
- [Ogerpon Meganium by Shun Akita (Limitless)](https://limitlesstcg.com/decks/list/27434)
- [Arboliva ex decklists (Limitless)](https://limitlesstcg.com/cards/DRI/23/decklists)
- [Arboliva ex decks (PokemonCard.io)](https://pokemoncard.io/category/pokemon/arboliva-ex-sv10-23)
- [Best Arboliva ex deck (Deltia's Gaming)](https://deltiasgaming.com/?p=255777)

The real lists' exact counts come from search summaries, not the pages
themselves.
