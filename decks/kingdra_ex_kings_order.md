# Kingdra ex: King's Order

Reviewed 2026-10-28 from a submitted list: 3 Kingdra ex on a 3-2 Horsea /
Seadra line with 3 Rare Candy, a 2-1-2 Blaziken ex line for Seething
Spirit, and Ludicolo, Aurorus and Carracosta with no line under them. They
get into play through Kingdra ex's King's Order ("Put up to 3 Water Pokémon
from your discard pile onto your Bench") after Gwynn, Ultra Ball, Prism
Tower or Brilliant Blender has discarded them. It ran 10 Energy and 4
Energy Coin. Asked with it: is there more here, maybe a spread-damage mix?

**This list: 64.11% against the 100-deck field at 1000 games per opponent**
(median 69.7%, 76 of 100 winning), on the engine as of e84da63. On the same
seeds it is **+17.48 ± 0.79** over the submitted list (46.42%), better on
99 of 100.

**The changes:**
- **No Blaziken ex line** (−2 Blaziken ex, −1 Combusken, −2 Torchic, −2
  Basic Fire Energy).
- **4 Kingdra ex, 4 Horsea, 3 Seadra** (+1 of each).
- **18 Energy, all Water** (+10 Basic Water Energy).
- **Out:** 4 Energy Coin, Team Rocket's Factory, 1 Ludicolo.

The submitted Kingdra ex PR-SV 131, Buddy-Buddy Poffin ASC 184, Night
Stretcher ASC 196, Prism Tower CRI 80, Poké Pad POR 81 and Gwynn PBL 78 are
real printings this pool doesn't carry (it has SFA 12, MEG 167, MEG 173,
CRI 111, ASC 198 and PBL 109); the import keeps yours.

## The strategy, card by card

- **Kingdra ex** (SFA 12 / PR-SV 131, Stage 2 Water, 310 HP, Retreat 1,
  weak to Lightning):
  - **King's Order** (Water): up to 3 Water Pokémon from your discard pile
    onto your Bench. Any Stage, so a Stage 2 arrives with no line.
  - **Hydro Pump** (Colorless, Colorless): 50, plus 50 for each Water
    Energy attached. Four Water is 250.
- **What King's Order brings back:**
  - **Aurorus** (POR 24): Tundra Wall, −50 damage to every Pokémon of
    yours with Water Energy attached. Doesn't stack.
  - **Ludicolo** (JTG 37): Vibrant Dance, +40 HP to all your Pokémon.
    Doesn't stack.
  - **Carracosta** (SCR 38): Primal Knowledge, +30 to attacks against an
    Active Evolution Pokémon.
- **Feeding the discard:** Gwynn (discard up to 2 Pokémon without a Rule
  Box, draw 3 each), Ultra Ball, Prism Tower, Brilliant Blender (any 5
  cards from the deck).
- **Energy:** Powerglass reattaches a Basic Energy from the discard to the
  Active at the end of each turn. Bubbly Water Energy stops Special
  Conditions on a Water Pokémon. Seadra's Call for Backup finds 3 Pokémon.

## What the measurements say

Each change below is paired against the list of its round, 200 games a
matchup, on e84da63.

| Round | Change | Measured |
|---|---|---|
| 1 | No Blaziken ex line (+1 Horsea, +1 Seadra, +5 Water) | **+12.54 ± 0.71** |
| 1 | 4 Water for the 4 Energy Coin | **+4.73 ± 0.53** |
| 1 | 2 Water for 2 Energy Coin | +3.71 ± 0.51 |
| 1 | Water for Team Rocket's Factory / a 2nd Surfing Beach for it | +1.44 / +0.79 |
| 1 | Water for 2 Ludicolo / 2 Aurorus / Carracosta | +4.29 / +2.76 / +2.27 |
| 1 | A 4th Rare Candy for an Energy Coin | +0.85 ± 0.46 |
| 2 | The three above (no Blaziken, no Coin, no Factory) | **+15.61 ± 0.84** |
| 2 | A 4th Kingdra ex for a Water | **+1.60 ± 0.47** |
| 2 | Water for 2 Ludicolo / 2 Aurorus / Carracosta | −0.04 / −1.09 / +0.76 |
| 2 | 2 Misty's Vitality / Rosa's Encouragement / Boss's Orders for Water | −0.57 / +0.17 / −0.38 |
| 2 | 2 Dewgong POR 19 / 2 Wellspring Mask Ogerpon DRI 67 for Water | −1.34 / −1.98 |
| 2 | Max Rod for Brilliant Blender | −0.47 ± 0.52 |
| 3 | Water for 1 Ludicolo | **+1.11 ± 0.49** |
| 3 | Water for Carracosta / a 4th Rare Candy / a 4th Seadra | +0.24 / +0.29 / +0.38 |
| 3 | Mantine MEG 32 (a 5th Basic) for a Water | −0.49 ± 0.47 |

**Spread damage.** Two rounds, first for Energy Coin, then like for like in
the King's Order slots on the round-2 list:

| Change | Measured |
|---|---|
| 2 Frosmoth MEG 43 for 2 Aurorus (Chilling Wings: 20 to each, Asleep) | −3.54 ± 0.53 |
| 2 Seaking PBL 14 for 2 Aurorus (Hydro Jet: 30 per Water to any one) | −3.46 ± 0.53 |
| 2 Vaporeon ex PRE 149 for 2 Ludicolo (Severe Squall: 60 to each ex) | −2.25 ± 0.47 |
| 2 Frosmoth + Greninja ex 30C 148 for 2 Aurorus + Carracosta | −3.04 ± 0.50 |
| Greninja ex 30C 148 for Carracosta (Stealthy Slash: 30 per counter) | +0.58 ± 0.47; round 3 −0.38 ± 0.46 |
| Mega Starmie ex POR 102 for Carracosta (Jetting Blow: 120, 50 to the Bench) | +0.24 ± 0.50 |
| 2 Cynthia's Milotic / 2 Articuno 30C 132, for Energy Coin on the submitted list | −2.65 / −2.49 |

Under the greedy pilot the spread Pokémon reached play through King's
Order (Frosmoth on 10% of turns, Greninja ex 11%) but never attacked: every
Energy went to the Active Kingdra ex. So the round-3 list was also played
by the lookahead pilot (`PILOT=lookahead`, which chooses the Energy target,
the retreat and the attack against the opponent's reply), 50 games a
matchup. Greninja ex for Carracosta: +0.50 ± 0.87. 2 Frosmoth and Greninja
ex for 2 Aurorus and Carracosta: −0.80 ± 0.90, where greedy said −3.04.
Better piloted, spread comes out even, not ahead.

**What it adds up to:**
- **The deck is Kingdra ex, and it was short of it and of Energy.** The
  Blaziken ex line took 5 Pokémon and 2 Fire Energy, for Seething Spirit
  1.63 times a game and Smolder-sault 0.70 times. Without it, Kingdra ex
  is in play on 90% of turns from turn 3 (75% before), and Hydro Pump
  fires 3.52 times a game (2.03). Both lists on e84da63, 60 logged games
  against six strong decks.
- **Energy Coin is a 1-in-4 Energy:** tails 1.58 times a game, an Energy
  0.53 times. Four Water in their place: +4.73.
- **King's Order works, and is worth little here.** In the submitted list
  the simulator never used it: the executor took Basic Pokémon only, and
  the attack had no price (see below). Fixed, Aurorus is in play on 59% of
  turns from turn 3, Carracosta 43%, Ludicolo 29%. But at 1000 games the
  fixes moved the submitted list −0.23 ± 0.32 and +0.33 ± 0.36: the
  package costs nearly what it gives. Aurorus earns its slots (−1.09 to
  cut both); one Ludicolo is enough, since Vibrant Dance doesn't stack.
- **Spread didn't earn a slot.** Every spread Pokémon tried lost to the
  Stage 2 it replaced or was even with it. The cheap spreaders (Frosmoth,
  Seaking, Milotic) do 20–90, where Hydro Pump does 250 to the Active.
- **This simulator's AI runs short of Energy** (see
  `jellicent_ex_oceanic_curse.md`, *Boss's Orders, re-measured*), so
  "Water for X" rows lean toward the Water. The Blaziken, Energy Coin and
  Kingdra ex results don't depend on that.

## How to play it

1. **Turn 1.**
   - Horsea Active; Buddy-Buddy Poffin for two more (60 HP fits its 70 HP
     limit).
   - Gwynn or Ultra Ball to discard Aurorus, Ludicolo or Carracosta.
   - No evolving on either player's first turn, and no Rare Candy.
2. **Turn 2.**
   - Rare Candy a Horsea that was in play last turn into Kingdra ex.
   - King's Order (one Water) if two or more support Pokémon are in the
     discard; otherwise Water Energy on Kingdra ex.
3. **Turn 3 and after.**
   - Hydro Pump: 50 plus 50 per Water Energy. Powerglass on the Active
     Kingdra ex adds one from the discard each turn.
   - Surfing Beach switches a damaged Kingdra ex for a fresh one for free.
   - Keep Aurorus on the Bench and Water Energy on whatever is Active:
     Tundra Wall only covers Pokémon with Water Energy attached.

**The opponent's outs:**
- **Lightning.** Horsea, Seadra, Kingdra ex, Ludicolo and Carracosta are
  all weak to it.
- **Knocking out Horsea before Rare Candy**, and Bench damage on Horsea
  and Seadra (60 and 90 HP).
- **A Kingdra ex gives up 2 Prizes.**
- **4 Basics: a 60.1% mulligan.** Every 5th Basic tried (Mantine,
  Ogerpon) measured worse.

## Matchups (1000 games each)

Both lists on e84da63, the same seeds.

**Best:** Mew baby box 94.5%, Mew / Pikachu box 93.3%, Team Rocket's
Wobbuffet / Orbeetle 92.8%, Team Rocket's Arbok / Yveltal 92.1%, Arbok /
Team Rocket's Muk 91.2%.

**Worst:**

| Opponent | This list | Submitted |
|---|---|---|
| Mega Zeraora ex / Cinderace (Lightning) | 1.4% | 2.7% |
| Snorlax / Bouffalant / Mega Kangaskhan ex | 9.7% | 6.8% |
| Aurorus / Kangaskhan, Tundra Wall | 13.1% | 6.7% |
| Arboliva / Ogerpon | 17.2% | 15.7% |
| Mega Zygarde ex / Cinderace, Gaia Wave | 20.6% | 7.6% |
| Munkidori ex / Pecharunt ex | 21.7% | 15.4% |
| Chesnaught / Meganium | 26.4% | 25.3% |
| Mega Chandelure ex / Telepathic / Hilda | 28.7% | 15.7% |

**The meta decks:**

| Opponent | This list | Submitted |
|---|---|---|
| Festival Lead | 81.9% | 71.4% |
| N's Zoroark | 79.1% | 63.1% |
| Slowking | 71.1% | 50.9% |
| Dragapult / Dusknoir | 60.9% | 46.5% |
| Dragapult | 59.4% | 39.1% |
| Dragapult / Blaziken | 59.1% | 44.8% |
| Raging Bolt | 57.0% | 41.6% |
| Mega Excadrill | 34.5% | 23.6% |

## What the simulator found

Each fix has a regression test that fails on the commit before.
1. **King's Order could never bench a Stage 2** (e84da63). The executor for
   "put Pokémon from your discard pile onto your Bench" took Basics only.
   Only Ho-Oh's Flames of Revival says Basic; King's Order and Salamence
   ex's Booming Call take any Stage.
2. **King's Order had no price**, so the AI never chose it: 0 uses in 60
   games. Priced now (`recover_price`); Gwynn, Prism Tower and Brilliant
   Blender now discard what it can bench (`recover_fuel`). Brilliant
   Blender had never been played in this deck.
3. **Carracosta's Primal Knowledge did nothing.** "Attacks used by your
   Pokémon do 30 more damage to your opponent's Active Evolution Pokémon"
   read as a family named "Pokémon do 30 more damage to … Evolution".
   Serperior ex, Garganacl, Lilligant, Victini and Iron Crown ex were
   misread the same way.
4. **Bench-only attacks hit the Active.** "This attack does 70 damage to 1
   of your opponent's Benched Pokémon" (Prinplup, Lopunny, Turtonator,
   Shaymin TEF, Salamence ex's Wide Blast) put the damage on the Active.
5. **Misty's Vitality didn't end the turn**: four Water Energy came with
   that turn's attack. Field: `kyurem_vanilluxe_blizzard`.
6. **The setup baseline held Gwynn and Energy Coin in hand.** The
   submitted list read Kingdra ex in play by turn 6 in 39.3% of trials;
   with them played, 52.0%.

## Cards searched

- **Spread** (`bench_snipe_opponent`, `bench_snipe_opponent_all`,
  `bench_damage_spread`, Water): Frosmoth, Seaking, Cynthia's Milotic,
  Greninja ex (30C 148 is Water; TWM 106 is Fighting, so King's Order
  can't take it), Vaporeon ex, Mega Starmie ex, Articuno, Kyurem ex,
  Regice, Prinplup, Mantine, Glaceon ex, Suicune, Keldeo, Glastrier.
- **Recruit from the discard** (`bench_recruit_from_discard`): Kingdra ex,
  Alomomola (Basics of 70 HP or less), Ho-Oh, Duskull, Salamence ex.
- **Water Energy loaders** (raw sweep, "attach … Water Energy"): Misty's
  Vitality, Rosa's Encouragement, Dewgong's Wash Out, Clawitzer, Gorebyss,
  Regice ex, Wellspring Mask Ogerpon; measured above where they fit.

**Anti-synergies:**
- Team Rocket's Factory draws only after a Team Rocket's Supporter; the
  submitted list had none.
- Bubbly Water Energy's immunity is for Water Pokémon: on Blaziken ex it
  was only an Energy.
- Tundra Wall covers only Pokémon with Water Energy attached.

## 1000-trial setup baseline

| Pokémon | Submitted, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Horsea | 94.8% | 100.0% | 1.00 |
| Seadra | 61.6% | 80.2% | 2.55 |
| Kingdra ex | 52.0% | 65.6% | 3.54 |

First attack by turn 6: **99.6%** of trials (average turn 3.00), against
90.6% (2.96). The baseline has no King's Order, so Ludicolo, Aurorus and
Carracosta read 0% there; in played games they are in play on 29%, 59% and
43% of turns from turn 3.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Brilliant Blender)
  (`check_energy_support.py`).
- Every attack is payable with Water Energy. No Ability gates an attack.
- **4 Basics: a 60.1% mulligan.**

**Real lists:** no current Standard Kingdra ex list with its contents
turned up. The search confirmed the SV Promo 131 printing.
- [Limitless: Kingdra ex SVP 131](https://www.limitlesstcg.com/cards/SVP/131)
- [Limitless: Kingdra ex SFA 12](https://limitlesstcg.com/cards/SFA/12)
- [20cards: Kingdra ex meta page](https://20cards.com/meta/kingdra-ex)

## PTCGL import

```
Pokémon: 15
4 Kingdra ex PR-SV 131
3 Seadra SFA 11
4 Horsea SFA 10
2 Aurorus POR 24
1 Ludicolo JTG 37
1 Carracosta SCR 38

Trainer: 27
4 Lillie's Determination MEG 119
4 Gwynn PBL 78
1 Boss's Orders MEG 114
3 Poké Pad POR 81
3 Rare Candy MEG 125
2 Ultra Ball ASC 213
2 Buddy-Buddy Poffin ASC 184
2 Powerglass SFA 63
1 Night Stretcher ASC 196
1 Brilliant Blender SSP 164
1 Air Balloon BLK 79
1 Switch MEG 130
1 Prism Tower CRI 80
1 Surfing Beach MEG 129

Energy: 18
4 Bubbly Water Energy CRI 84
14 Basic Water Energy

Total Cards: 60
```
