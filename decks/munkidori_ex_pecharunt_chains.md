# Munkidori ex / Pecharunt ex Chains

Built 2026-10-13 from a random pick. The brief: "a random ex Pokémon with an
Ability; devise a strategy from it. That will be the focus but it will need
supporting win conditions". The roll was among the 40 ex Pokémon with
Abilities that no field deck plays yet: **Munkidori ex SFA 37**.

**82.08% against the 91-deck field at 1000 games per opponent** (median
86.9%, 85 of 91 winning). On the same seeds:
- **+10.04 ± 0.63** over the first build (72.05%), better on 90 of 91.
- **+1.70 ± 0.46** over the same deck with no Munkidori ex at all
  (80.39%).

**Lines:** Munkidori ex, Pecharunt ex, Okidogi ex. All Basic, all Darkness.

## The focus: Munkidori ex

- **Oh No You Don't** (Ability): if it is Knocked Out by an attack while
  you have any **Pecharunt ex** in play, your opponent takes 1 fewer
  Prize. It is a 210 HP ex that gives up one Prize.
- **Dirty Headbutt** (DDC): 190, and it can't use Dirty Headbutt again on
  your next turn.

Two cards make it work:
- **Pecharunt ex**'s **Subjugating Chains** (Ability, once a turn) switches
  a Benched Darkness Pokémon into the Active Spot and Poisons it. Switching
  a Munkidori ex to the Bench ends its Dirty Headbutt lock, so two of them
  trade places and one hits for 190 every turn.
- Pecharunt ex also has to stay in play for the Prize cut, so there are 2.

In 100 logged games Munkidori ex was Knocked Out 49 times:
- 43 times the opponent took 1 Prize.
- 5 times they took 2 (Pecharunt ex was gone).
- Once they took none.

## Supporting win conditions

1. **Okidogi ex** (250 HP) turns the Poison into damage.
   - **Chain-Crazed** (DDC) is 130, plus 130 if Okidogi ex is Poisoned.
   - Subjugating Chains Poisons whatever it brings in, so an Okidogi ex
     switched in by Chains hits for 260.
   - **Poisonous Musculature** (C) attaches 2 Darkness Energy from the deck
     *and* Poisons itself, so it sets up its own 260 for next turn.
   - Okidogi ex gives up 2 Prizes, so it hits hardest but costs most.
2. **Pecharunt ex's Irritated Outburst** (DD): 60 for each Prize your
   opponent has taken. It's the late-game finisher, 240-300 once they have
   taken 4-5.
3. **Janine's Secret Art** puts Darkness Energy on two Darkness Pokémon. On
   your Active it Poisons it, which is a free 260 setup for Okidogi ex.

## How to play

1. **Turn 1.**
   - Bench Pecharunt ex first: no Pecharunt ex, no Prize cut.
   - Bench a Munkidori ex and an Okidogi ex (Ultra Ball, Brock's Scouting).
   - Janine's Secret Art on two of them; attach.
2. **Turn 2.**
   - Subjugating Chains the attacker in: an Okidogi ex with DDC (260,
     Poisoned) or a Munkidori ex (190).
   - Or Okidogi ex in the Active uses Poisonous Musculature to load itself.
3. **Every turn after.**
   - Chains brings in the attacker that's ready. The one that just attacked
     goes to the Bench, where its Poison and its Headbutt lock both end.
   - Munkidori ex is the default attacker, because losing it costs 1 Prize.
     Use Okidogi ex for the 260 Knock Outs.
   - Irritated Outburst once the opponent has taken 4 Prizes.

**The opponent's outs:**
- **Knock Out or Boss's Orders the Pecharunt ex** (190 HP, 2 Prizes). That
  doubles the next Munkidori ex Prize. Keep the second one.
- **Fighting.** Munkidori ex, Okidogi ex and Pecharunt ex are all weak to
  Fighting.
- **Their own Poison cure or a Stadium** that blocks Special Conditions
  turns Okidogi ex back into a 130.
- **Poison on your Active** is 10 a turn. Chains moves it off the next turn.

**Matchups (1000 games):**
- **Worst:** Arboliva / Ogerpon 23.0%, Mega Zygarde ex / Cinderace 29.5%
  and 44.0% (Fighting), Maushold mill 30.2%, Mega Zeraora ex / Cinderace
  37.4%, N's Zoroark 48.3%.
- **Best:** Mew baby box 99.8%, Mew / Hypno 99.4%, Arbok / Yveltal 99.3%,
  Team Rocket's Wobbuffet 98.9%.
- Against the other new decks: Gourgeist ex / Diggersby 83.1%, Mega Absol
  ex 61.3%.

## What the simulator found

**Four engine fixes** (2026-10-13). Each of the first three has a regression
test that fails on the previous commit:
- **Poisonous Musculature Poisoned the opponent.** "If you attached Energy
  ..., this Pokémon is now Poisoned": the subject came after an "If"
  clause the rule didn't read. So Chain-Crazed's +130 never followed it,
  and the opponent got a free Poison.
- **Janine's Secret Art's "it is now Poisoned"** (your own Active) compiled
  to a Poison on theirs. Its Supporter play is hand-written and was
  already right, so the field's Darkness decks were unaffected.
- **"During your next turn, this Pokémon can't use <attack>" locked
  nothing** (23 Pokémon). Munkidori ex hit for 190 every turn from the
  same spot. So did the field's Feraligatr (Giant Wave), Annihilape
  (Impact Blow) and Crabominable (Haymaker). It now holds for that turn.
  Gouging Fire ex's "until it leaves the Active Spot" holds until it does.
- **Not fixed, noted:** the AI's damage estimate leaves out Tool bonuses
  (Binding Mochi's +40 while Poisoned). They're applied when the attack
  resolves.

## Cards searched

- **Names Pecharunt ex:** only Munkidori ex.
- **Prize cuts:** Munkidori ex, Legacy Energy, Mega Gengar ex, Shedinja,
  Lillie's Pearl.
- **Darkness acceleration:** Janine's Secret Art, Okidogi ex, Toxtricity,
  Marnie's Grimmsnarl ex.
- **Poison payoffs:** Okidogi ex, Binding Mochi, Pecharunt PR-SV (opponent's
  Poisoned only), Venoshock (Glimmora / Scolipede, the opponent's Poison).

**Anti-synergies:**
- Festival Grounds and any Special Condition blocker switch off Okidogi
  ex's Poison bonus.
- The plain Munkidori (ASC 99) is Psychic. Janine's can't reach it, and
  its attack is unpayable here. Two of them, with Energy Switch and Poké
  Pad to support Adrena-Brain, measured −3.17 against a 3rd Okidogi ex, a
  2nd Fezandipiti ex and 4 Energy in those slots.

**Measured out:**
- Fezandipiti ex: cutting the last one was +1.05. Cruel Arrow's 100 to any Pokémon didn't pay for the slot.
- Binding Mochi: no better than the Energy it replaced.
- Legacy Energy for Hero's Cape: −0.61.
- A 3rd Pecharunt ex: ±0.

## How it was tuned

200 games against each of the 91 field decks, paired on the same seeds.
Each round is paired against the best list of the round before. Lists and
results are in `runs/2026-10-13/munkidori_ex_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | 4 Munkidori ex, 2 Pecharunt ex, 2 Okidogi ex, Fezandipiti ex, 2 Munkidori (A) | 72.25% | −3.17 vs C |
| 0 | No Okidogi ex (2 Fezandipiti ex) | 60.53% | −14.90 vs C |
| 0 | A with Legacy Energy for Hero's Cape | 72.21% | −3.21 vs C |
| 0 | **3 Okidogi ex, 2 Fezandipiti ex, no Munkidori (C)** | **75.42%** | |
| 1 | −2 Energy for a Pokégear and a Boss's / 1 Pecharunt ex / 3rd Boss's for a Pokégear | 73.8-74.6% | −1.67 to −0.78 |
| 1 | −2 Brock's, −1 Janine's, 3rd Pecharunt ex, −2 Energy Retrieval, −2 Iris's | 75.6-76.4% | +0.14 to +0.95 |
| 1 | −Petrel / −2 Switch / −1 Fezandipiti ex, +Energy | 76.7-78.0% | +1.24 to +2.52 |
| 1 | 3 Munkidori ex, 4 Okidogi ex | 78.69% | +3.26 ± 0.41 |
| 1 | **4th Okidogi ex for a Fezandipiti ex** | **79.25%** | **+3.82 ± 0.43** |
| 2 | Binding Mochi ×2 (for Energy Retrieval / Iris's / Switch) | 78.6-80.2% | −0.68 to +0.94 |
| 2 | Legacy Energy, 3rd Pecharunt ex, −Energy Retrieval, −Iris's, −Petrel, −Fezandipiti ex, −2 Switch | 78.6-80.3% | −0.61 to +1.04 |
| 2 | **−2 Switch, −Petrel, +3 Energy** | **81.04%** | **+1.80 ± 0.39** |
| 3 | −Hero's Cape, −2 Energy, −1 Janine's | 80.0% | −1.07 to −0.99 |
| 3 | −1 Brock's, −Iris's, −Energy Retrieval, −Night Stretcher, 3rd Pecharunt ex, 2 Mochi for 2 Energy | 80.7-81.4% | −0.40 to +0.37 |
| 3 | **−Fezandipiti ex, +1 Energy (this list)** | **82.09%** | **+1.05 ± 0.39** |
| Control | 2 Munkidori ex / no Munkidori ex | 81.24% / 80.45% | −0.85 / −1.65 |
| 1000 games | First build / no Munkidori ex / **this list** | 72.05% / 80.39% / **82.08%** | **+10.04 ± 0.63** |

**What made the difference:**
- **Okidogi ex.** The deck without it measured 60.5%, and every round
  wanted more of it.
- **Energy.** Every Pokémon's attack costs 2-3 Darkness, and Chains wants a
  loaded attacker on the Bench every turn.

Logged against random field opponents, it won 52 of 60. Per game it used:
- Dirty Headbutt 2.6 times, Chain-Crazed 1.9, Subjugating Chains 1.8.
- Janine's Secret Art 1.8, Poisonous Musculature 1.2, Irritated Outburst
  0.1.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Munkidori ex | 89.5% | 1.79 |
| Pecharunt ex | 71.1% | 2.29 |
| Okidogi ex | 82.6% | 1.82 |

First attack by turn 6 in 98.6% of games (average turn 2.41). The baseline
doesn't model Brock's Scouting, Energy Retrieval or Iris's Fighting Spirit,
so Pecharunt ex lands sooner in real games than this shows.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Every attack is payable with Darkness Energy, and no Ability gates an
  attack.
- 10 Basics, 25.9% mulligan.

**Real lists:** no tournament results found. The closest is a guide's list,
not a tournament list: Munkidori ex 2, Pecharunt ex 2, Okidogi ex 2,
Fezandipiti ex 1, with Binding Mochi and Janine's Secret Art. It's the same
plan, and every card in it was checked against the pool and measured here.
- [Okidogi ex Loyal Three guide](https://www.josephwriteranderson.com/blog/loyal-three-deck-from-shrouded-fable-looks-broken)
- [Deltia's Gaming Munkidori ex guide](https://deltiasgaming.com/?p=295241)
- [PokemonCard.io Munkidori ex decks](https://pokemoncard.io/category/pokemon/munkidori-ex-sv6pt5-91)

## PTCGL import

```
Pokémon: 10
4 Munkidori ex SFA 37
2 Pecharunt ex SFA 39
4 Okidogi ex SFA 36

Trainer: 26
4 Lillie's Determination MEG 119
4 Janine's Secret Art SFA 59
2 Boss's Orders MEG 114
2 Brock's Scouting JTG 146
4 Ultra Ball MEG 131
3 Pokégear 3.0 BLK 84
2 Night Stretcher MEG 173
2 Energy Retrieval CRI 108
1 Hero's Cape TEF 152
2 Iris's Fighting Spirit ASC 190

Energy: 24
24 Basic Darkness Energy

Total Cards: 60
```
