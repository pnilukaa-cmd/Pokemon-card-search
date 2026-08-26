# Chandelure / Centiskorch — trap-and-deck-out

Rebuild of a user's Chandelure list around its **actual** win condition:
trap a harmless Pokémon in the Active Spot, force draws with `Alluring
Light`, mill with `Controlled Burn`, and win when the opponent cannot draw.

An earlier pass at this list (`mega_chandelure_ex_retreat_tax.md`) read
the retreat tax as a *damage* scaler and recommended cutting the mill
package. That was a misread of the deck: `Binding Flame` and `Gravity
Gemstone` are the **lock**, not the damage, and the mill is the win
condition. This file supersedes that recommendation for this deck.

## The arithmetic that decides everything

After setup both players have **47 cards** left in deck (60 − 7 hand − 6
Prizes). With **N** Chandelure in play and Centiskorch attacking every
turn:

| | per turn cycle |
| --- | --- |
| **Opponent's deck** | −1 their draw, −N `Alluring Light`, −2 `Controlled Burn` = **−(N+3)** |
| **Your deck** | −1 your draw, −N `Alluring Light` = **−(N+1)** |

`Alluring Light` is **symmetric** — it burns both decks equally. The
*entire* asymmetry in the deck is the **+2 from Controlled Burn**. Three
consequences, and they set the whole build:

1. **Centiskorch is the most important card in the deck.** It is the only
   source of edge. The original list ran 2 Sizzlipede / 2 Centiskorch and
   had Centiskorch in play by turn 6 in **20.8%** of games — the win
   condition was absent four games in five.
2. **More Chandelure is strictly better**, even though it burns your own
   deck too. It does not change the *margin* much, but it shortens the
   game, and a shorter game is one you have to survive for fewer turns:

   | N | turns to deck them | your cards left when you win |
   | --- | --- | --- |
   | 0 | 15.7 | 31.3 |
   | 2 | 9.4 | 18.8 |
   | 3 | 7.8 | 15.7 |
   | **4** | **6.7** | **13.5** |

3. **Your own draw engine is your enemy.** Every Supporter that nets you
   cards eats the 13.5-card cushion. This is why the list below runs a
   deliberately thin draw package and two `Sacred Ash`.

A sweep of the whole pool confirms the ceiling is real: **there is no
repeatable non-attack mill in Standard.** Every mill effect is either an
attack (one per turn) or a one-shot on-play/on-evolve trigger
(`Durant ex`, `Flygon`, `Ferrothorn`). 2 per turn is the cap.

## The lock

You cannot survive 7 turns of a real attacker, so the plan is to make sure
there isn't one:

- **Boss's Orders (4)** — drag up a Pokémon with **no Energy attached**.
  This is a damage-free play; the point is *which* Pokémon is Active, not
  hurting it.
- **Jamming Tower (2)** — kills their `Air Balloon` and `Rescue Board`, so
  a gusted 0-Energy Pokémon has to pay its printed Retreat Cost in real
  Energy, one attachment per turn. See the Stadium section below.
- **Crushing Hammer (3)** — an Item, so it strips the Energy they do
  attach without costing you the turn's mill.
- **Xerosic's Machinations (2)** — strips them to 3 cards, taking their
  `Switch` and `Air Balloon` with it. It also forces them to spend draw
  Supporters to refill, which burns their deck *again*. It earns its slot
  twice over in this plan.
- **Team Rocket's Chingling (3)** — free-cost `Chiming Commotion` discards
  a random card from their hand, for **no Energy at all**. Best used the
  turn after `Xerosic's Machinations`: they are already down to 3 cards, so
  a random discard off a 3-card hand is a third of everything they hold,
  and it costs you nothing but the attack on a turn Centiskorch isn't
  online yet. Once Centiskorch is up, Controlled Burn is worth more.

**Do not Knock Out the trapped Pokémon.** Every attack in this deck's plan
deals 0 damage on purpose — a KO just lets them promote something better.
That is the single biggest play-pattern difference from a normal deck.

## Decklist

```
Pokémon: 21
4 Litwick PBL 36
4 Lampent PBL 37
4 Chandelure TWM 38
3 Sizzlipede PBL 9
3 Centiskorch PBL 10
3 Team Rocket's Chingling DRI 85

Trainer: 30
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Rare Candy MEG 125
4 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
3 Crushing Hammer POR 71
2 Poké Pad ASC 198
2 Xerosic's Machinations SFA 64
2 Jamming Tower ASC 261
1 Sacred Ash POR 115
1 Grand Tree SCR 136

Energy: 9
2 Telepathic Psychic Energy POR 88
4 Basic Psychic Energy
3 Basic Fire Energy

Total Cards: 60
```

### Card choices worth stating

- **Lampent's `Spreading Light` is the setup engine.** *"Search your deck
  for up to 3 Lampent and put them onto your Bench."* One attack fills the
  Bench with the Stage 1 that becomes four Chandelure. Run **4 Lampent**
  so it can find three.
- **Sacred Ash POR 115** — *"Shuffle up to 5 Pokémon from your discard
  pile into your deck."* Five cards back on your own clock, twice. In a
  deck-out mirror or a long lock this is what wins the race.
- **Grand Tree SCR 136 as the ACE SPEC.** It runs the whole
  Litwick → Lampent → Chandelure chain out of the deck each turn without
  costing you a card off the top, which is exactly what a deck that cannot
  afford to draw wants. Measured: Chandelure by turn 6 goes **44.6% →
  60.2%**. It is symmetric, but the opponent using it pulls **2 more cards
  out of their own deck** every turn — in this matchup that is on your
  side of the ledger.
  - **Swap to `Neutralization Zone` SFA 60 if your meta is ex-heavy**:
    *"Prevent all damage done to Pokémon that don't have a Rule Box (both
    yours and your opponent's) by attacks from the opponent's Pokémon ex
    and Pokémon V."* Every Pokémon in this deck has no Rule Box, so an
    ex-based opponent literally cannot damage you. That is the lock in one
    card — but it does nothing about assembling Chandelure, which is the
    measured weak point.
- **Telepathic Psychic Energy POR 88** — attaching it to a Psychic Pokémon
  searches out **2 Basic Psychic Pokémon onto your Bench**. Litwick
  qualifies, so it is an Energy attachment and a Buddy-Buddy Poffin at
  once.
- **Only 3 Lillie's Determination, only 1 Poké Pad.** Deliberately lean —
  see point 3 of the arithmetic above.
- **Every Pokémon gives up exactly 1 Prize.** In a deck-out deck the
  opponent's clock is six Prizes, so a 2-Prize `Latias ex` or a 3-Prize
  `Mega Chandelure ex` hands them a third or a half of their win for one
  Knock Out. That is what cuts them, not their card quality.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC, no
energy-type shortfall, no attack-gating Ability text.

Mulligan with 10 Basics: **25.9%**.

1000-trial baseline, in play by turn 6 — original list versus this one:

| | original | this build |
| --- | --- | --- |
| Litwick | 86.3% | 96.9% |
| Lampent | 50.1% | 76.3% |
| **Chandelure** (mill engine) | **25.4%** | **61.7%** |
| Sizzlipede | 44.9% | 82.6% |
| **Centiskorch** (the win condition) | **20.8%** | **57.9%** |
| Team Rocket's Chingling | 29.2% | 88.6% |

Mulligan 25.9% (11 Basics). Every utility Basic added on top of these
costs engine consistency directly — a version carrying 3 Chingling **and**
2 Elgyem dropped Chandelure to 50.3% and Centiskorch to 41.7%. Three
Chingling is the most the engine will carry.

**A caveat that matters more than the win rates below.** The simulator's
AI cannot play this deck's actual plan: its `Boss's Orders` drags up the
opponent's *weakest* Pokémon by remaining HP rather than the most
*harmless* one, and it has no concept of deliberately declining a Knock
Out to keep a target trapped. So the lock — the half of the deck that
keeps you alive for seven turns — is simply not being executed. Read the
setup table above as the real evidence, and the win rates as a floor:

| Opponent | original | this build |
| --- | --- | --- |
| Mega Scrafty ex darkness tank | 32.0% | 34.0% |
| Hop's Snorlax stacked buff | 33.6% | 40.8% |
| Decidueye ex / Judge | 45.2% | 48.0% |

## Every mill effect in Standard

A full sweep of the pool turns up **25** effects that discard cards off
the opponent's deck. **None of them is a Trainer** — there is no mill Item
or Supporter in the format at all — and none is a repeatable Ability.
That is why 2-per-turn is the ceiling.

### Repeatable, 0 damage (these keep the lock intact)

| Card | Cost | Mill | Notes |
| --- | --- | --- | --- |
| **Centiskorch** PBL 10 | `F` | **2** | Stage 1, 140 HP, retreat 3. The build's pick |
| **Zweilous** SSP 118 | `D` | **2** | Stage 1, 100 HP, retreat 2 — off a **70 HP Poffin-eligible** Deino |
| **Great Tusk** TEF 97 | `CC` | 1, or **4** | Basic, 140 HP, retreat 3. The 4 needs an Ancient Supporter that turn |
| **Drilbur** SSP 108 | `C` | 1 | 70 HP Basic, **Colorless cost** — runs off any Energy, Poffin-eligible |
| **Deino** SSP 117 | `D` | 1 | 70 HP Basic, retreat 1 |
| **Sizzlipede** PBL 9 | `F` | 1 | 80 HP — **too big for Buddy-Buddy Poffin** |
| **T.R. Diglett** ASC 100 | `F` | flip until tails | 60 HP Basic. Averages 1, spikes to 3–4 |

### Repeatable but deals damage (breaks the lock)

`Hydreigon ex` (200 dmg + mill 3), `Tyranitar` JTG 95 (150 + 2),
`Coalossal` TEF 95 (150 + 2), `Mega Excadrill ex` PBL 103 (90 + 2),
`Mega Heracross ex` PFL 108 (170 + 2), `Tyrantrum` POR 45 (160 + flips),
`Mega Scrafty ex` and `Scovillain ex` (mill 1 + a hand discard).

These are all better cards; none of them belongs in a trap deck, because
Knocking the trapped Pokémon out just lets the opponent promote a real
attacker. They belong in a Prize-race deck that mills as a bonus.

### One-shot bursts

| Card | Burst | Trigger |
| --- | --- | --- |
| **Ferrothorn** CRI 63 | **8** | *Only* if the opponent discards it **from your deck**. The largest single mill in the format, and near-dead outside the mill mirror — but it triggers from the deck, so it costs no Bench slot |
| **Great Tusk + Explorer's Guidance** | 4 in one turn | `Land Collapse` goes 1 → 4 if you played an Ancient Supporter. `Explorer's Guidance` TEF 147 is the only one |
| **Flygon** PFL 101 | 2 | On evolving into it, **and again** if it is KO'd in the Active Spot |
| **Durant ex** SSP 215 | 1 | When played from hand to the Bench. 2 Prizes, so not here |

**On the late one-time mill specifically.** `Great Tusk` + `Explorer's
Guidance` is the only real burst available, and it is a *finisher only*,
never an engine — Explorer's Guidance is *"look at the top 6 of your deck,
put 2 into your hand, discard the other cards,"* which costs **you 6 cards
to mill them 4**. Running it as the plan loses the race outright:

| | per turn |
| --- | --- |
| them | 1 + N + 4 = N+5 |
| you | 1 + N + 6 = **N+7** |

At N=2 you deck yourself on turn 7 with 13 of their cards still to go. As
a single pair of cards held for the turn they sit at 4 or fewer, it
converts "two more turns" into "I win now" — worth it only if you can
afford Great Tusk's **retreat 3** in the Active Spot. Tested as a maindeck
package it cost more than it gave: Chandelure by turn 6 dropped
60.2% → 54.2% and Centiskorch 51.1% → 46.5%.

### The Deino line: better on paper, worse in practice

`Deino` SSP 117 is 70 HP where `Sizzlipede` is 80 — the difference between
Buddy-Buddy Poffin fetching your win condition and not. Swapping the whole
line in did exactly what the maths predicted: **Zweilous by turn 6
51.1% → 60.0%**, Deino 77.9% → 90.8%.

It then lost the head-to-head against the Fire version **32% to 68%**, and
every gauntlet matchup fell (34.0% → 20.0%, 40.8% → 17.2%, 48.0% → 16.4%).
The reason is not the mill at all: dropping Fire Energy makes
**`Mind Ruler` uncastable**, and Mind Ruler is the deck's only source of
damage anywhere. Zweilous is also 100 HP against Centiskorch's 140. A deck
whose every attack deals 0 damage needs one card that can actually kill
something when the lock breaks — the Fire Energy is in the list for
Chandelure, not for Centiskorch.

Keep the Fire line. If you want a Poffin-eligible early miller without a
third colour, **`Drilbur` SSP 108** is the one: `Burrow` costs a single
**Colorless**, so the Psychic Energy already in the deck pays for it.

## The Stadium slot

The lock lives and dies on Retreat Cost, and **the cards that break it are
Tools**: `Air Balloon` (−2), `Rescue Board` (−1), `Future Booster Energy
Capsule` (no Retreat Cost at all). That points at one Stadium.

**Jamming Tower ASC 261** — *"Pokémon Tools attached to each Pokémon (both
yours and your opponent's) have no effect."* It answers every retreat Tool
in the format at once, and at **2 copies** you always have a Stadium to
push theirs out with.

It does turn off your own `Gravity Gemstone`, so it is Jamming Tower **or**
Gemstone, not both. On a gusted Pokémon with printed Retreat Cost 2:

| | their retreat |
| --- | --- |
| Gemstone, they attach Air Balloon | 2 + 1 − 2 = **1** |
| Gemstone, no Balloon | 2 + 1 = **3** |
| **Jamming Tower** (Balloon dead) | **2** |

Gemstone has the higher ceiling and folds completely to a single Air
Balloon. Jamming Tower has the lower ceiling and no answer. For a deck
whose survival *is* the lock, take the floor.

The other Stadiums worth knowing about:

| Stadium | Verdict |
| --- | --- |
| **Team Rocket's Watchtower** ASC 210 | *Colorless Pokémon have no Abilities.* **Costs this deck literally nothing** — nothing in it is Colorless — and switches off `Dudunsparce`, `Mega Kangaskhan ex`, `Fan Rotom`, `Noctowl`. The free-roll bump if you would rather keep Gravity Gemstone. Mild anti-synergy: killing their draw also slows their own deck burn |
| **Neutralization Zone** SFA 60 | ACE SPEC. Nothing here has a Rule Box, so an ex deck **cannot damage you at all**. The strongest single lock card available — but it costs you Grand Tree, and it is 1 copy, so it cannot be replayed after a bump |
| **Academy at Night** SFA 54 | Puts a card from hand back on **top of your deck** each turn, which extends your own clock. Symmetric, so it helps whoever is closer to decking out — that is *them*. Skip |
| **Gravity Mountain** SSP 177 | −30 HP to every Stage 2. Your Chandelure is 130. No |
| **Risky Ruins** MEG 127 | 2 damage counters on every Basic non-Darkness Pokémon benched. You bench 10+ Basics. No |
| **Lumiose City** POR 111 | Searching with it **ends your turn**. No |

Note that **Grand Tree is itself a Stadium**, so running it alongside two
Jamming Tower means sequencing them: Grand Tree early while you are still
assembling, Jamming Tower once the lock is what matters. Playing your own
Jamming Tower discards your own Grand Tree — that is the intended line,
not a mistake.

## The energy-denial half of the lock

Raising Retreat Cost only works while they cannot pay it, and they attach
one Energy a turn. Denial is the other half:

| Card | Speed | Effect |
| --- | --- | --- |
| **Crushing Hammer** POR 71 | **Item** | Flip; heads discards an Energy from **any** of their Pokémon. Costs no attack and no Supporter, and you can throw several a turn |
| **Elgyem** BLK 40 | attack, `P`, **0 dmg** | `Slight Shift` — move an Energy from one of their Pokémon to another. Guaranteed, no flip |
| **Enhanced Hammer** TWM 148 | Item | No flip, but **Special Energy only** |
| **Dustox** ASC 15 | **Ability** | `Boisterous Wind` — flip, bounce an Energy off their Active to hand. Repeatable and free, but a third Stage 2 line |

`Elgyem` is the right card for turns 1–3 specifically. Centiskorch is not
online until turn ~3.3, so those attacks are doing nothing anyway, and
`Slight Shift` costs one **Psychic** — a colour already in the deck — deals
**0 damage** so it never breaks the trap, and is a 60 HP Poffin-eligible
Basic. It undoes a turn of their retreat progress for free. Once
Centiskorch is up, hand the job to `Crushing Hammer`, which does the same
work at Item speed without costing you the 2-card mill.

`Crushing Hammer` is maindecked at 3 above. **`Elgyem` is a 1-of swap**
(over the third `Lillie's Determination`) if you want the guaranteed,
no-flip version for turns 1–3; every utility Basic past the third
Chingling measurably costs engine consistency, so it is a real trade
rather than a free include.

**A limitation to read the win rates against.** `Crushing Hammer` has no
modeled effect in the simulator, and **no Stadium does anything at all in
`simulate_versus.py`** (`Player.stadium` is assigned and never read), so
Jamming Tower is invisible there too. The AI also has no concept of
denying a retreat. Those three together mean the versus numbers score
this build's *costs* and none of its payoff — while the earlier
Gravity Gemstone version did get its +1 counted, because Tools feed the
retreat query. Judge the lock on the arithmetic: a trapped Pokémon on
Retreat Cost 2 whose Air Balloon is dead and who loses an Energy a turn
never leaves.

## What was cut, and why

| Cut | Why |
| --- | --- |
| 2 Mega Chandelure ex | competes with Chandelure for the same Lampent, and **3 Prizes** is half the opponent's clock for one KO. `Jamming Tower` protects the retreat lock for one card instead of a Stage 2 line |
| 1 Latias ex | 2 Prizes, and `Skyliner` frees your *Basics* — irrelevant to a Stage 1 attacker that never wants to move |
| 1 Comfey | `Flower Shower` draws **each** player 3 — symmetric, so it buys no edge, and it costs you 3 off your own cushion in one shot |
| 1 Maractus | `Corner` stops retreat for one turn but is an *attack*, so it costs you the 2-card Controlled Burn that turn. The lock is cheaper via Jamming Tower + Crushing Hammer + hand denial |
| 1 Eevee / 1 Sylveon | `Safeguard` walls one Pokémon; `Neutralization Zone` walls the whole board for one card if you want that effect |
| 1 Elgyem, 1 Dedenne, 1 Team Rocket's Watchtower, 1 Lana's Aid, 2 Air Balloon | singleton utility with no line to it; the deck cannot afford cards that don't advance the clock or the lock |

Added: **Chandelure 2 → 4**, **Centiskorch 2 → 3**, **Sizzlipede 2 → 3**,
**Lampent 3 → 4**, **Rare Candy 2 → 4**, **Buddy-Buddy Poffin 1 → 4**,
**4 Ultra Ball** (the original ran none), **2 Sacred Ash**, **Grand Tree**.

## Where this deck loses

- **Anything that KOs through the lock.** A gusted Pokémon that still hits
  for 100+ ends you; Centiskorch is 140 HP and has to stand there for
  ~7 turns.
- **Their own Switch / Air Balloon / free-retreat Ability.** The trap is
  only as good as their inability to leave. This is what the Xerosic's and
  Chingling hand denial is protecting, and two Xerosic's is not many.
- **Decks that draw hard on their own.** Ironically these are *good*
  matchups for the clock (they burn their deck faster) but bad for the
  lock (they find the out).
- **Fire weakness on Chandelure**, ×2 on a 130 HP Bench sitter, and
  `Boss's Orders` on the other side digs it out.
- **The cushion is 13.5 cards.** Two greedy Supporters and a bad Ultra
  Ball turn can genuinely flip which player decks out first.

## Simulator work this deck required

The deck-out plan could not be scored at all before this pass:

1. **Deck-out was never a loss.** The check was `deck_out and not hand`,
   so a player with an empty deck but cards in hand took turns forever. No
   mill deck could ever be recorded as winning. Now you lose the moment
   you must draw and cannot, which is the actual rule.
2. **`Alluring Light` compiled to two draws, not one.** `draw_one` and
   `each_player_draws` both matched "each player draw a card", doubling
   the rate of the one engine this deck wins with.
3. **Mill was priced as a rider at 5 damage-equivalent per card**, so a
   0-damage mill attack lost every comparison to any attack that dealt
   damage and the AI never played the plan. Now priced as what it is: a
   whole win is six Prizes, so milling N of their D remaining cards is
   N/D of the way there.
4. **`Spreading Light` did not compile at all** — `search_to_bench` only
   matches text containing the word "Pokémon", and this card names the
   species ("up to 3 Lampent"). A new `recruit_species_to_bench` rule
   covers it, and `SEARCH_TO_BENCH` is now an executable attack rider.
