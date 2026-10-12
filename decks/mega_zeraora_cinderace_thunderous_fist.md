# Mega Zeraora ex / Cinderace Thunderous Fist

Built 2026-10-12 to answer one question: is the Cinderace / big-Basic build
better on an Energy type other than Fighting? The same frame was built on
every Energy type (Fire, Water, Grass, Lightning, Psychic, Darkness, Metal,
Colorless, and Fire + Psychic for Mega Latias ex). Lightning won, then got
three rounds of tuning.

**90.03% against the 86-deck field at 1000 games per opponent** (median
93.3%, 84 of 86 winning). On the same seeds:
- **+6.80 ± 0.74** over the Mega Zygarde ex list as it stood (83.24%).
- **+2.96 ± 0.71** over that list after this round's fix (no Core Memory,
  87.07%; see
  [mega_zygarde_cinderace_gaia_wave.md](mega_zygarde_cinderace_gaia_wave.md)).

**Lines:** Cinderace (opens face down), Mega Zeraora ex, Mega Audino ex.

## Plan

**Cinderace MEG 28**'s Explosiveness puts it face down as your opening
Active from the hand. **Turbo Flare** (C) does 50 and attaches 3 Basic
Energy from your deck to your Benched Pokémon.

**Mega Zeraora ex** (Basic, 270 HP, Retreat 1) turns that Energy straight
into damage:
- **Thunderous Fist** (L): 60 for each Lightning Energy attached. It costs
  one Energy, discards nothing, and grows every turn: 4 Energy is 240, 5 is
  300.
- **Zepto Turn** (LLL): 150, then switch with a Benched Pokémon.

**Voltaic Lightning Energy** adds 20 to a Lightning Pokémon's attacks.

**Mega Audino ex**'s Kaleidowaltz is a second accelerator.

## How to play

1. **Setup.** Put Cinderace face down as the Active whenever you have one.
   Bench Mega Zeraora ex.
2. **First attack.** Turbo Flare: 50 damage and 3 Lightning Energy onto the
   Benched Zeraora.
3. **Next turn.**
   - Cinderace has no Retreat Cost, so retreat it for free.
   - Attach a fourth Energy to Zeraora, or a Voltaic Lightning Energy from
     hand: Turbo Flare only finds Basic Energy.
   - Thunderous Fist for 240-260.
4. **Every turn after.** Attach one more Energy and hit harder. Zeraora
   keeps all its Energy, so it never has to reload.
   - Jumbo Ice Cream heals 80 from it once it has 3+ Energy.
   - When it goes down, Ultra Ball and Canari find the next one, and Turbo
     Flare or Kaleidowaltz loads it.
5. **Boss's Orders** (2) and **Team Rocket's Petrel** (4) take the last
   Prizes.

**Its one real weakness.** Mega Zeraora ex is weak to Fighting. A 200
Gaia Wave becomes 400, more than its 270 HP. It loses to both Mega Zygarde
ex / Cinderace lists in the field (37.1% and 44.6%), its only losing
matchups.

**Matchups (1000 games):**
- **Worst:** Mega Zygarde ex / Cinderace (tuned) 37.1%, Mega Zygarde ex
  (submitted) 44.6%, N's Zoroark 50.6%, Maushold mill 66.6%, Mega
  Chandelure ex 68.0%, Mega Emboar ex 73.1%.
- **Best:** Arbok / Yveltal 100.0%, Mew baby box 99.9%, Wobbuffet /
  Orbeetle 99.6%, Mew / Pikachu box 99.5%.

## How it was found

All runs: 200 games against each of the 86 field decks, paired on the same
seeds. Lists and results are in `runs/2026-10-12/energy_type_screens/`.

**1. Every Energy type, same frame.** Each type list has:
- 4 Cinderace, 2 main hitters, 1 second hitter and Mega Audino ex.
- The same Trainers, with the type's own Special Energy and support where it
  has any.
- 4 Ultra Ball in place of Fighting Gong.

The Fighting list built the same way is the control (86.35%).

| Type | Hitters | Win rate | vs control |
|---|---|---|---|
| **Lightning** | 2 Mega Zeraora ex, Pikachu ex | **87.76%** | **+1.41 ± 0.61** |
| Fire | 2 Gouging Fire ex, Reshiram ex | 85.41% | −0.94 ± 0.85 |
| Metal | 2 Mega Mawile ex, Hop's Zacian ex | 84.11% | −2.24 ± 0.66 |
| Darkness | 2 Mega Absol ex, Yveltal ex | 83.72% | −2.63 ± 0.58 |
| Water | 2 Black Kyurem ex, Dondozo ex | 83.68% | −2.67 ± 0.66 |
| Grass | 2 Mega Heracross ex, Iron Leaves ex | 82.30% | −4.05 ± 0.87 |
| Colorless | 2 Mega Kangaskhan ex, Bloodmoon Ursaluna ex | 82.14% | −4.21 ± 0.94 |
| Psychic | 2 Mega Diancie ex, Mega Floette ex | 80.90% | −5.45 ± 0.79 |
| Fire + Psychic | 2 Mega Latias ex, Gouging Fire ex | 74.47% | −11.88 ± 0.98 |

Thunderous Fist is why Lightning wins. Every other big attack has a fixed
damage number. Thunderous Fist scales with the Energy Turbo Flare and
Kaleidowaltz pour in, for a one-Energy cost and no discard.

**2. Tuning**, each round paired against the best list of the round before:

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 1 | No Ultra Ball (+4 Energy) | 79.00% | −8.76 ± 0.55 |
| 1 | 2 Ultra Ball (+2 Energy) | 84.70% | −3.06 ± 0.37 |
| 1 | No Mega Audino ex (+Zeraora) | 86.93% | −0.83 ± 0.37 |
| 1 | Zekrom ex for Pikachu ex | 86.94% | −0.82 ± 0.33 |
| 1 | Basic Lightning for the 3 Voltaic | 87.22% | −0.53 ± 0.35 |
| 1 | Miraidon ex for Pikachu ex | 87.39% | −0.37 ± 0.37 |
| 1 | Levincia for Lively Stadium | 87.52% | −0.23 ± 0.32 |
| 1 | Canari for 1 Iris's Fighting Spirit | 88.14% | +0.38 ± 0.33 |
| 1 | **3rd Zeraora for Pikachu ex** | **88.40%** | **+0.64 ± 0.39** |
| 2 | 4th Zeraora (−1 Energy) | 88.65% | +0.26 ± 0.38 |
| 2 | Canari for 1 Iris's | 88.78% | +0.39 ± 0.35 |
| 2 | **2 Boss's Orders (+1 Energy)** | **89.07%** | **+0.67 ± 0.32** |
| 3 | 1 Boss's Orders | 89.53% | +0.47 ± 0.30 |
| 3 | **2 Canari for both Iris's** | **89.78%** | **+0.72 ± 0.31** |
| 1000 games | 2 Canari / 2 Canari + 4th Zeraora (this list) | 89.76% / **90.03%** | **+2.96 ± 0.71** vs Fighting |

Ultra Ball is the card the deck can't do without: Fighting Gong has no
Lightning counterpart, and Ultra Ball (with Canari) is how Zeraora is found.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Cinderace | 56.9% | 1.00 |
| Mega Zeraora ex | 94.3% | 1.76 |
| Mega Audino ex | 70.3% | 2.73 |

First attack by turn 6 in 99.9% of games (average turn 2.04). The baseline
doesn't model Turbo Flare's attachment or Canari.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
Every attack is payable with the deck's Energy. Mulligan 30.0% on 5 Basics
+ 4 Cinderace openers.

**Rules assumption:** as with the Zygarde list, the simulator lets
Cinderace open, and stop a mulligan, from a hand with no Basic Pokémon.

## PTCGL import

```
Pokémon: 9
4 Cinderace MEG 28
4 Mega Zeraora ex PBL 114
1 Mega Audino ex ASC 253

Trainer: 25
4 Lillie's Determination MEG 184
4 Team Rocket's Petrel DRI 226
2 Canari ASC 185
2 Boss's Orders MEG 114
4 Ultra Ball MEG 131
4 Jumbo Ice Cream CRI 109
1 Mega Signal MEG 171
1 Switch PFL 123
1 Hero's Cape TEF 152
1 Team Rocket's Factory DRI 173
1 Lively Stadium SSP 180

Energy: 26
23 Basic Lightning Energy
3 Voltaic Lightning Energy PBL 84

Total Cards: 60
```
