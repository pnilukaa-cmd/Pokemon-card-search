# Team Rocket's Crobat / Mega Absol ex — early bench snipe

Bench damage that costs **no attack at all**, starting turn 2, converting
into a Knock Out that ignores HP entirely.

## Why this shape

Everything that snipes a Bench in Standard is one of three things: an
attack (costs your turn), a Stage 2 payoff (too slow), or an **evolve
trigger** (free, and it fires while you are building your board anyway).
The third is the only one that is genuinely an *early game* plan, and the
Team Rocket's Zubat line is the best version of it:

| Card | Trigger | Effect |
| --- | --- | --- |
| **Team Rocket's Golbat** DRI 121 | on evolving from Zubat | `Sneaky Bite` — 2 counters on **any 1** of their Pokémon |
| **Team Rocket's Crobat ex** DRI 122 | on evolving from Golbat | `Biting Spree` — 2 counters on **each of 2** of their Pokémon |

Neither costs an attack, Energy, or your Supporter. They fire on the same
turn you play the evolution, so damage starts landing **turn 2** and you
still get to attack.

One full chain — Zubat → Golbat → Crobat ex — places **exactly 6 damage
counters**. That number is the whole deck:

**Mega Absol ex** (MEG 161, **Basic**, 280 HP Darkness)
- `Terminal Period` — `Darkness / Colorless`: *"If your opponent's Active
  Pokémon has **exactly 6 damage counters** on it, that Pokémon is
  Knocked Out."*
- `Claw of Darkness` — `D/D/C`, 200, and discard a card from their hand.

Sixty damage worth of counters kills a 350 HP Mega Evolution ex. For two
Energy. Off a **Basic** that needs no evolution line of its own.

Counters only ever arrive in **twos**, so you land on 6 exactly and never
overshoot to 7 — that is why this line and not, say, `Dusclops`, whose
`Cursed Blast` places 5.

**Sableye** TEF 107 (Basic, 70 HP) is the aiming device: `Damage
Collection` (`C/C`, 0 damage) moves **any number** of counters from their
Bench onto their Active. Sprinkle freely, then consolidate exactly what
you need onto whatever you want dead.

## The turn sequence

- **Turn 1.** Zubat or Sableye active, bench a second Zubat. Poffin
  fetches two of them (Zubat 50 HP, Sableye 70 HP — both eligible).
  Nothing has happened yet.
- **Turn 2.** Evolve a Zubat → Golbat: **20 counters placed anywhere**,
  for free. Attack with whatever is Active. *Their out:* KO your 50 HP
  Zubat before it evolves — cheap for them, so bench two.
- **Turn 3.** Second Golbat: another 20 on the same target (40 total). Or
  Golbat → Crobat ex for 20 on each of two. *Their out:* retreat the
  damaged Pokémon to the Bench — which does not help, because your
  targets are on the Bench anyway and the counters stay.
- **Turn 4 — the cash-in.** Third trigger puts a target on exactly 60.
  `Boss's Orders` or `Prime Catcher` drags it Active, `Terminal Period`
  Knocks it Out regardless of HP. *Their out:* healing. `Bianca's
  Devotion` or a heal Ability takes the target off exactly 6 and the
  attack whiffs entirely — this is the deck's real soft spot, and the
  answer is `Claw of Darkness` for 200 instead.

Note the rules detail that makes this work: **retreating and evolving both
clear Special Conditions but neither removes damage counters.** A target
you have marked stays marked wherever it goes.

## Decklist

```
Pokémon: 16
4 Team Rocket's Zubat DRI 120
4 Team Rocket's Golbat DRI 121
2 Team Rocket's Crobat ex DRI 122
3 Mega Absol ex MEG 161
3 Sableye TEF 107

Trainer: 34
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Poké Pad ASC 198
4 Boss's Orders MEG 114
3 Team Rocket's Great Ball ASC 205
3 Janine's Secret Art SFA 59
3 Lillie's Determination MEG 119
2 Team Rocket's Venture Bomb DRI 179
2 Night Stretcher MEG 173
2 Carmine TWM 145
2 Air Balloon MEG 166
1 Prime Catcher TEF 157

Energy: 10
10 Basic Darkness Energy

Total Cards: 60
```

### Card choices worth stating

- **No Rare Candy, deliberately.** Rare Candy skips the Stage 1, which
  skips `Sneaky Bite` — two of the six counters you are trying to place.
  The slow manual line is the *combo*, not a compromise.
- **Prime Catcher TEF 157 as the ACE SPEC.** *Switch in one of their
  Benched Pokémon, then switch your own Active.* It drags the marked
  target up **and** puts Mega Absol ex in the Active Spot, at Item speed,
  for one card. `Boss's Orders` does half of that and costs the Supporter.
- **Janine's Secret Art SFA 59** attaches 2 Darkness from the deck — which
  is exactly what `Terminal Period` costs. Attach to the **Bench**, since
  attaching to your Active Poisons it, then bring it in with Air Balloon.
- **Team Rocket's Venture Bomb DRI 179** is an **Item** that places 2
  counters on a coin flip (tails puts them on your own Active, which a 280
  HP body can absorb). It is the granularity card: the only way to add
  counters without an evolution, when you need a 2 and have run out of
  Zubat.
- **Team Rocket's Great Ball ASC 205** — heads finds an Evolution Team
  Rocket's Pokémon, tails a Basic one. Every Pokémon in the Zubat line is
  a Team Rocket's Pokémon, so it never whiffs entirely.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC, no
energy-type shortfall, no attack-gating Ability text.

Mulligan with 10 Basics: **25.9%**.

1000-trial baseline, in play by turn 6:

| | % | avg turn |
| --- | --- | --- |
| Team Rocket's Zubat | 98.6% | 1.40 |
| Sableye | 95.6% | 1.58 |
| **Team Rocket's Golbat** (the snipe engine) | **88.0%** | **2.84** |
| Mega Absol ex | 77.0% | 2.05 |
| Team Rocket's Crobat ex | 44.8% | 4.18 |

Golbat online at **88% by turn 2.84** is the number that matters for the
brief: counters start landing turn 3 in the large majority of games, and
Mega Absol ex is already there because it is a Basic. Crobat ex at 44.8%
is the Stage 2 bonus, not the plan.

`simulate_versus.py` against **every one of the 26 other saved decks**,
200 games each — mean **58.2%**, median **54.5%**, **19/26** winning
matchups:

| Win rate | Opponent | | Win rate | Opponent |
| --- | --- | --- | --- | --- |
| **87.5%** | T.R. Wobbuffet / Orbeetle | | 54.0% | Arbok / T.R. Muk |
| **81.5%** | Feraligatr / Munkidori | | 53.0% | Krookodile ex / Relicanth |
| **78.0%** | Static Venom Drapion | | 51.0% | T.R. Koffing / Weezing |
| **78.0%** | Eerie Inferno Ninetales | | 50.0% | Orthworm ex metal |
| **71.5%** | Chandelure / Centiskorch mill | | 49.5% | Arbok / Muk (Trolley) |
| **66.0%** | Darkness mill hand lock | | 49.0% | Steven's Carbink wall |
| **65.5%** | Salazzle ex / T.R. Muk | | 45.0% | Toxic Slumber Vileplume ex |
| **65.0%** | Hop's Snorlax | | 42.0% | T.R. Persian ex |
| **61.5%** | T.R. Spidops swarm | | 39.5% | Panic Poison Paralysis |
| **60.0%** | N's Zoroark ex Night Joker | | 36.5% | Lurantis heal punish |
| 57.5% | Water aggro | | | |
| 56.5% | Mega Chandelure ex retreat tax | | | |
| 55.0% | Arbok / Muk (Laser) | | | |
| 54.0% | Mega Scrafty ex darkness tank | | | |
| 54.0% | Decidueye ex / Judge | | | |

The bad matchups share a shape: `lurantis_heal_punish` (36.5%) and
`toxic_slumber_vileplume_ex` (45.0%) both **heal**, which is exactly the
predicted weakness — healing takes a marked target off *exactly* 6
counters and blanks `Terminal Period`. `panic_poison_paralysis` (39.5%)
wins the race before the counters accumulate.

One deck, `selective_bloom_cradily`, is **excluded**: it runs zero Basic
Pokémon (its Lileep arrives via `Antique Root Fossil`, an Item the engine
does not model as a Basic), so it mulligans out and loses on turn 2 every
game. It showed as a 100% matchup in a first pass, which is an artifact of
the harness, not a result.

**Read those with one caveat.** `Terminal Period` fired **zero** times
across those games: the AI has no line for "aim counters at one target,
gust it up, then attack," so the simulator is winning on the free chip
damage and `Claw of Darkness` alone. The combo is upside the numbers do
not contain — which also means the floor is a ~59% deck without ever
executing it.

## Where this deck loses

- **Healing.** Anything that takes a marked target off *exactly* 6
  counters turns `Terminal Period` into a blank. This is the single
  cleanest answer to the deck.
- **Grass weakness ×2** on Mega Absol ex, which also gives up **3 Prizes**.
  Losing it once is half their game.
- **Zubat is 50 HP.** Every trigger depends on Zubat surviving to your
  next turn; a snipe deck on the other side dismantles the engine before
  it starts.
- **Damage-counter lock.** `Patrat`'s `Watchful Eye` (*damage counters
  can't be moved*) shuts off Sableye entirely, though not the placement.
- **Crobat ex is a Stage 2 in a deck with no Rare Candy** — by design, but
  it means the 4-counter trigger arrives late or not at all.

## Simulator work this deck required

Four fixes, three of them general:

1. **`Biting Spree` was aimed at the wrong side of the board.** "Choose 2
   of your opponent's Pokémon and put 2 damage counters on **each** of
   them" names its target in an earlier clause, and `place_counters` only
   parsed the "on ..." tail — so "each of them" resolved to this Pokémon
   and Crobat ex damaged its own team. Now parsed with a target count.
2. **There was no conditional-Knock-Out mechanic.** Adds
   `Op.CONDITIONAL_KO`, a rule for the "exactly N damage counters →
   Knocked Out" shape (this also covers `Glaceon ex`'s `Euclase`),
   valuation as the victim's full HP, and resolution ahead of damage.
3. **`Damage Collection` did not compile**, and `parse_target` read
   "...to **their** Active Pokémon" as the player's own side, because the
   possessive refers back to a subject in an earlier clause. Adds an
   "any number" counter-move rule and fixes the possessive.
4. **Counter placement sprinkled instead of focusing.** The engine now
   tops up whichever target is closest to the 60-counter threshold from
   below — which is what a player does with spread damage, and what makes
   an exact-total payoff reachable at all.

`PLACE_COUNTERS` and `MOVE_COUNTERS` are now executable attack riders too;
previously only Abilities could place counters.
