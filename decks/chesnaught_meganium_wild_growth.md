# Chesnaught / Meganium: Wild Growth

Built 2026-10-23 on request: a Chesnaught and Meganium deck, "maybe some
other effects to combine with that". Follow-ups: make sure enough Energy
gets on the board; consider Brambleghast, because Chesnaught's HP is low;
and "maybe even Exeggutor for the health if I can get 6 Energy".

**This list: 71.55% against the 95-deck field at 1000 games per opponent**
(median 75.6%, 87 of 95 winning), on the engine as of f01e13e. On the same
seeds it is **+18.08 ± 0.80** over the first build (53.47%), better on 92
of 95. The Exeggutor version further down is 70.86%: −0.68 ± 0.27 behind
it on the same seeds.

Both numbers are on the same engine, so the +18.08 is all list changes.
The engine fixes found along the way (under "What the simulator found")
moved the first build only from 51.17% to 53.47%.

## Why these two

**Meganium's Wild Growth** (MEG 10, Stage 2, 160 HP): each Basic Grass
Energy attached to your Pokémon provides two Grass Energy. It doesn't
stack, so one Meganium in play is the whole effect. Everything in the deck
counts Energy, so it doubles:
- **Chesnaught** (CRI 7, Stage 2, 180 HP, Retreat 4).
  - Impound (Grass, Grass, Colorless): 160, and the Defending Pokémon
    can't retreat next turn. Under Wild Growth two cards pay it.
  - Needly Armor: when Chesnaught is damaged in the Active Spot, even if
    it's Knocked Out, 3 damage counters go on the attacker for each Grass
    Energy attached. Three Basic Grass are six Grass Energy, so 180 back.
- **Mega Meganium ex** (ASC 10, 360 HP), from the same Bayleef. Giant
  Bouquet (CCC): 70, plus 50 for each Grass Energy attached. Three Basic
  Grass under Wild Growth is 370.
- **Teal Mask Ogerpon ex** (TWM 190, 210 HP).
  - Teal Dance: once a turn, attach a Basic Grass Energy from your hand to
    it and draw a card.
  - Myriad Leaf Shower (GGG): 30, plus 30 for each Energy on both Active
    Pokémon. Yours count double.
- **Alolan Exeggutor** (30C 129, Stage 1, 150 HP, Retreat 4).
  - Scale Up: +250 HP with 6 or more Grass Energy attached. **Under Wild
    Growth that's three Basic Grass Energy, not six**: a 400 HP Pokémon
    that gives up one Prize.
  - Mega Drain (G, C, C, C): 150, and heal 50.
  - Exeggcute (MEG 4), Jam-Packed (C): attaches a Basic Grass Energy from
    the deck to itself.

**Energy acceleration in the deck:**
- the manual attachment, worth double under Wild Growth;
- Teal Dance from the hand;
- Quilladin's Leafy Charge (G) and Exeggcute's Jam-Packed, from the deck;
- Bug Catching Set: up to 2 Grass Pokémon or Basic Grass Energy from the
  top 7.
- **Forest of Vitality** lets a Grass Pokémon evolve on the turn it's
  played, except on your first turn: Chespin to Quilladin, or Exeggcute
  to Exeggutor, the turn it comes down. Rare Candy still can't go on a
  Basic played this turn; that's Rare Candy's own text.

## What the measurements say

**Energy was the whole story.** The first build ran 14 Basic Grass
Energy. Every round, almost any slot turned into an Energy measured
better, until 23. Measured in game (`energy_curve.py`, 10 games against
each field deck, at the end of each of your turns):

| End of your turn | First build: Energy in play | Active can pay its attack | This list: Energy in play | Active can pay its attack |
|---|---|---|---|---|
| 2 | 2.29 | 62.6% | 3.56 | 75.1% |
| 3 | 3.40 | 62.4% | 5.67 | 77.6% |
| 4 | 4.46 | 64.1% | 7.89 | 78.8% |
| 6 | 5.99 | 61.5% | 12.19 | 77.9% |

Energy in play counts what the Pokémon provide, so Wild Growth's double is
included. By turn 6 this list has twice the first build's Energy on the
board. It still ends most turns with about one Energy card in hand
(0.80-1.60), against 0.37-0.80 for the first build. Meganium was in play
by turn 4 in 38.5% of games, and Teal Mask Ogerpon ex in 78.3%.

**Chesnaught's HP, and what was tried for it** (each paired against the
list of that round, 200 games a matchup):

| Change | Measured |
|---|---|
| Hero's Cape (+100 HP) for Deluxe Bomb | +0.64, +0.81; Deluxe Bomb back later −1.60, −1.34 |
| Survival Brace (lives at 10 HP from full) for Deluxe Bomb | −1.26 |
| Shuckle (heal 30 a turn) | −1.89 |
| Brambleghast 2-2 (Resilient Soul, Powerful Needles) | −4.75; −3.93 at 18 Energy |
| Alolan Exeggutor 2-2 next to Chesnaught | −3.85; −3.78 at 18 Energy; 1-1 −3.14 |
| Exeggutor 3-3 and a second Mega Meganium ex in place of the Chesnaught line | +2.55, +2.63, +2.12 |

What it adds up to:
- **Hero's Cape is the ACE SPEC.** Chesnaught at 280 HP measured better
  than Deluxe Bomb's 120 back in all four comparisons.
- **A third attacking line costs more than it adds.** Brambleghast and
  Exeggutor both lost as additions. The deck can't power three lines and
  Meganium at once.
- **Brambleghast** (TEF 21, Stage 1) starts at 100 HP: Resilient Soul adds
  50 only per Prize you've already given up. Powerful Needles flips a coin
  per Energy (240 on average with three Basic Grass under Wild Growth),
  but it was the worst addition in both rounds.
- **Chesnaught is the weakest piece.** Each copy traded for an Energy has
  measured better: 3 to 2 Chesnaught was part of the +6.30 round, and 2 to
  1 measured +1.33 more. The list below keeps 2, so it's still a
  Chesnaught deck. If you'd rather not, the Exeggutor version is the
  other way to go.

**Exeggutor, as you suggested, works best in place of Chesnaught.** Under
Wild Growth three Basic Grass cards make it 400 HP for one Prize. The
Exeggutor version and the Chesnaught version finished within a point of
each other at 200 games (71.18% and 71.46%); the 1000-game numbers are
below.

**Other cards tried** (each against the list of its round):
- **2 Waitress / Energy Search / Powerglass, for Pokégear and a Switch:**
  −0.38, −0.75, −0.89.
- **Rosa's Encouragement:** −0.99.
- **Hydrapple ex 2-1-2:** −2.68.
- **A 2nd Mega Meganium ex:** −2.24, −2.46, −1.16.
- **Boss's Orders:** cutting both for Energy was +4.59; adding 2 back
  later was −3.22.

## How to play it

1. **Turn 1.** Bench Chikorita and Chespin (Poffin, Ultra Ball for a
   Basic). Teal Mask Ogerpon ex is the opener: Teal Dance an Energy onto it
   and draw.
2. **Turn 2.** Rare Candy into **Meganium first**, before Chesnaught or
   Mega Meganium ex. Wild Growth is the engine; everything else is twice as
   expensive without it. Keep Meganium on the Bench: 160 HP, and its own
   attack isn't the plan.
3. **Every turn after.**
   - Ogerpon swings Myriad Leaf Shower while the Stage 2s come up.
   - Chesnaught goes Active with three Basic Grass and Hero's Cape: 280
     HP, Impound for 160, and 180 back on whatever hits it.
   - Mega Meganium ex's Giant Bouquet is the finisher: 370 with three
     Basic Grass under Wild Growth.

**The opponent's outs:**
- **Fire.** Everything in the deck is weak to it.
- **Knock Out Meganium.** A Boss's Orders on the Bench Meganium switches
  every cost back to normal. The second Meganium and Night Stretcher are
  the backup.
- **Ability lock** shuts off Wild Growth and Teal Dance.
- **Energy removal** costs double: each Basic Grass discarded was two
  Energy.

## Matchups (1000 games each)

**Best:** Static Venom Drapion 95.2%, Team Rocket's Arbok / Yveltal 93.8%,
Wobbuffet / Orbeetle 93.0%, Mew / Hypno 92.6%, Mew baby box 91.7%.

**Worst:**

| Opponent | This list | First build | Exeggutor version |
|---|---|---|---|
| Mega Zeraora ex / Cinderace | 31.4% | 12.1% | 30.4% |
| Tauros, Risky Ruins | 35.5% | 25.4% | 30.3% |
| Arboliva / Ogerpon | 37.3% | 16.1% | 35.2% |
| Mega Dragonite ex / Kangaskhan ex / Salazzle ex | 39.8% | 22.1% | 34.2% |
| Mega Zygarde ex / Cinderace | 42.3% | 23.2% | 37.5% |
| Mega Gengar ex / Toxtricity | 45.0% | 25.8% | 45.0% |

Three of the six bring a Fire attacker (Cinderace's Turbo Flare,
Salazzle ex), and everything here is weak to Fire.

**The meta decks:**

| Opponent | This list | First build |
|---|---|---|
| N's Zoroark | 85.7% | 74.1% |
| Festival Lead | 84.0% | 72.2% |
| Slowking | 76.7% | 55.5% |
| Dragapult / Dusknoir | 73.1% | 49.3% |
| Dragapult | 67.0% | 40.2% |
| Raging Bolt | 66.4% | 50.1% |
| Dragapult / Blaziken | 63.8% | 43.5% |
| Mega Excadrill | 51.7% | 26.6% |

## What the simulator found

Engine fixes, each with a regression test that fails on the commit before:
1. **HP Abilities ignored their conditions** (be34d64).
   - Alolan Exeggutor's Scale Up was +250 with nothing attached. The type
     between "more" and "Energy" hid the clause, and it now counts Energy
     provided, Wild Growth included.
   - Brambleghast's Resilient Soul and Conkeldurr's Craftsmanship were a
     flat +50 and +40.
   - Ludicolo's Vibrant Dance went to Ludicolo alone.
   - Cynthia's Power Weight and Ancient Booster Energy Capsule gave HP to
     any holder.
   - "N or more Grass Energy" attack bonuses counted cards, not Energy.
2. **Teal Dance drew before attaching** (be34d64). With no Grass Energy in
   hand it still drew, and attached what it drew.
3. **Switch was played the moment it was drawn**, into the healthiest
   Benched Pokémon (a569a0d). It now waits until a Benched Pokémon does
   more this turn than the Active. +2.29 on this deck, +0.28 to +5.83 on 8
   field decks with Switch, and +12.39 on a submitted Snorlax list. An
   Asleep or Paralyzed Active now counts as doing nothing, for Sky
   Transport too.
4. **Rare Candy took the first Stage 2 in hand** (f01e13e). With
   Chesnaught ahead of Meganium in hand, the Candy went to Chesnaught;
   Meganium was in play by turn 4 in 23% of games. Rare Candy, evolution
   and searches now go to an evolved whole-side engine first: 34% by
   turn 4. +2.27 on the Exeggutor version, +0.03 on the Chesnaught
   version, +0.20 to +0.92 on the field decks it touches.

**Tried and taken back out:**
- Putting the spare attachment where one more Energy adds HP or damage
  (an Exeggutor one card short of 400): −0.38 to +0.76.
- Skipping Teal Dance when the only Energy in hand is wanted elsewhere:
  −0.50 to +0.02. Teal Dance's draw pays for itself.

## Cards searched

- **HP:** every "+N HP" card (`hp_modify_flat`, `hp_scales_with_count`),
  plus a raw "HP" sweep, triaged by hand.
  - Grass-usable: Hero's Cape, Growing Grass Energy (a Special Energy, so
    Wild Growth doesn't double it), Lively Stadium (Basics only),
    Brambleghast, Alolan Exeggutor.
  - Survive-a-Knock-Out shapes from the sweep: Survival Brace (ACE SPEC),
    and Pokémon-specific Abilities (Crustle, Mega Hawlucha ex) that don't
    fit.
- **Healing** (`heal_self`, `heal_other_target`, `heal_team`): Shuckle,
  Ludicolo PFL (needs a Grass Mega ex), Whimsicott (discards the
  Energy), Hydrapple ex's Ripening Charge, Leafeon, Pokémon Center Lady,
  Super Potion.
- **Energy** (`energy_search`, `energy_attach_bonus`,
  `energy_recursion`): Energy Search, Waitress, Rosa's Encouragement,
  Powerglass, Energy Retrieval, Crispin (needs two types).
- **Retaliation partners:** Deluxe Bomb, Spiky Energy, Punk Helmet
  (Darkness only).

**Anti-synergies:**
- Growing Grass Energy and Spiky Energy aren't Basic, so Wild Growth
  doesn't double them.
- Hero's Cape, Deluxe Bomb and Survival Brace are all ACE SPECs: one only.
- Chesnaught and Alolan Exeggutor both have Retreat 4. With one Switch,
  whatever is Active usually stays there.

## Tuning, round by round

All against the 95-deck field, paired on the same seeds within a tag, 200
games a matchup. Each engine fix that changed play got a new tag, and the
round's base was re-run on it: hp0 (be34d64), hp1 (a569a0d: Switch), hp2
(f01e13e: Rare Candy to the engine).

| Round | Base | What won | Result |
|---|---|---|---|
| 1 (hp0) | first build, 51.17% | −2 Boss's Orders, +2 Energy: +4.59 | 55.76% |
| 2 (hp1) | that list, 57.08% | 3rd Ogerpon +1.57, 18 Energy +1.01, 3 Rare Candy +0.87, Hero's Cape +0.81 | combined: 61.94% |
| 3 (hp1) | 61.94% | −2 Shaymin, +2 Energy: +2.87 | 64.82% |
| 4 (hp2) | 65.16% | one each of Chesnaught, Chespin, Poffin, Forest, Night Stretcher, Rare Candy for an Energy: +0.88 to +1.45 | |
| 5 (hp2) | 65.16% | −1 Chesnaught, −1 Chespin, −1 Poffin, −1 Forest, +1 Ogerpon, +3 Energy: +6.30 | **71.46%** |
| 6 (hp2) | 71.46% | 1 Chesnaught +1.33, 1 Quilladin +1.09; 24th Energy, 2 Rare Candy within noise | kept |

Round 6 is where it stops: what's left is within about 1.5 points, and
going to one Chesnaught would leave a Chesnaught deck with one Chesnaught.

**The Exeggutor branch,** the same shell with the Chesnaught line swapped
for 3 Exeggcute, 3 Alolan Exeggutor and a second Mega Meganium ex:
- 64.06% in round 3, 69.48% in round 4 (where Rare Candy going to
  Meganium first was worth +2.27 to it).
- Round 5, −1 Forest, −1 Mega Meganium ex, −1 Rare Candy for 3 Energy:
  +1.70, to 71.18%.
- 4 Exeggutor (−4.29), 2 Ogerpon (−3.67) and a 4th Chikorita (−2.10)
  were all worse.

## 1000-trial setup baseline

| Pokémon | First build, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Chespin | 91.3% | 87.2% | 1.88 |
| Quilladin | 43.1% | 44.0% | 3.45 |
| Chesnaught | 37.1% | 25.7% | 4.00 |
| Chikorita | 84.0% | 83.5% | 1.83 |
| Bayleef | 36.1% | 36.3% | 3.55 |
| Meganium | 22.6% | 21.0% | 4.10 |
| Mega Meganium ex | 12.3% | 10.3% | 3.98 |
| Teal Mask Ogerpon ex | 53.6% | 81.6% | 1.82 |

First attack by turn 6: **92.9%** of trials (average turn 2.93), against
82.9% for the first build (2.84).

This tool plays no opponent and models no Abilities, so Teal Dance,
Leafy Charge and Bug Catching Set don't show here. The full engine has
Meganium in play by turn 6 in 52.6% of games and Chesnaught in 41.7%
(`energy_curve.py TRACK=`).

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Hero's Cape).
- Every attack is payable with Grass Energy. No Ability gates an attack.
- 10 Basics: a 25.9% mulligan. The Exeggutor version has 9 (30.0%); a 4th
  Chikorita or Exeggcute for an Energy measured −2.10 and −2.37 there.
- The card file's legality flags (fetched 2026-09-24) still mark
  Ascended Heroes cards as not yet Standard: Mega Meganium ex ASC 10 and
  Chikorita ASC 8 here. That looks like the snapshot predating the
  set's Standard date, as with Perfect Order in the Dragonite notes.
  Check it in PTCGL. Alolan Exeggutor is a 30C card.

**Real lists:** no published Chesnaught list was found. The Meganium lists
that exist build Wild Growth around Hydrapple ex and Teal Mask Ogerpon ex,
which agrees with Ogerpon going to 4 here:
- [Deltia's Gaming: Meganium deck guide (Mega Evolution)](https://deltiasgaming.com/?p=358447)
- [pokemoncard.io: Mega Venusaur and Mega Meganium deck](https://pokemoncard.io/deck/ever-green-forest-mvenusaur-and-mmeganium-148708)
- [pokemoncard.io: Mega Meganium ex (Ascended Heroes) decks](https://pokemoncard.io/category/pokemon/mega-meganium-ex-me2pt5-10)

## PTCGL import

```
Pokémon: 19
3 Chespin CRI 5
2 Quilladin CRI 6
2 Chesnaught CRI 7
3 Chikorita ASC 8
2 Bayleef MEG 9
2 Meganium MEG 10
1 Mega Meganium ex ASC 10
4 Teal Mask Ogerpon ex TWM 190

Trainer: 18
3 Rare Candy MEG 125
4 Ultra Ball MEG 131
1 Buddy-Buddy Poffin ASC 184
1 Forest of Vitality MEG 117
4 Lillie's Determination MEG 119
1 Night Stretcher MEG 173
1 Switch MEG 130
2 Bug Catching Set TWM 143
1 Hero's Cape TEF 152

Energy: 23
23 Basic Grass Energy

Total Cards: 60
```

**The Exeggutor version** (70.86%; decks/meganium_alolan_exeggutor_wild_growth.ptcgl.txt):

```
Pokémon: 17
3 Chikorita ASC 8
2 Bayleef MEG 9
2 Meganium MEG 10
1 Mega Meganium ex ASC 10
3 Teal Mask Ogerpon ex TWM 190
3 Exeggcute MEG 4
3 Alolan Exeggutor 30C 129

Trainer: 18
2 Rare Candy MEG 125
4 Ultra Ball MEG 131
2 Buddy-Buddy Poffin ASC 184
1 Forest of Vitality MEG 117
4 Lillie's Determination MEG 119
1 Night Stretcher MEG 173
1 Switch MEG 130
2 Bug Catching Set TWM 143
1 Hero's Cape TEF 152

Energy: 25
25 Basic Grass Energy

Total Cards: 60
```
