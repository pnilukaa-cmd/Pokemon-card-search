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
- **Gravity Gemstone (2)** — +1 Retreat Cost to both Actives. A gusted
  0-Energy Pokémon with retreat 2 now needs two turns of attachments just
  to leave, and they can only attach one Energy per turn.
- **Xerosic's Machinations (2)** — strips them to 3 cards, taking their
  `Switch` and `Air Balloon` with it. It also forces them to spend draw
  Supporters to refill, which burns their deck *again*. It earns its slot
  twice over in this plan.
- **Team Rocket's Chingling (3)** — free-cost `Chiming Commotion` discards
  a random card from their hand. Mostly a Poffin-able opener; use it only
  on turns Centiskorch isn't ready, since Controlled Burn is worth more.

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

Trainer: 29
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Rare Candy MEG 125
4 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
2 Xerosic's Machinations SFA 64
2 Gravity Gemstone SCR 137
2 Sacred Ash POR 115
2 Night Stretcher MEG 173
1 Poké Pad ASC 198
1 Grand Tree SCR 136

Energy: 10
2 Telepathic Psychic Energy POR 88
4 Basic Psychic Energy
4 Basic Fire Energy

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
| Litwick | 86.3% | 96.5% |
| Lampent | 50.1% | 76.3% |
| **Chandelure** (mill engine) | **25.4%** | **60.2%** |
| Sizzlipede | 44.9% | 77.9% |
| **Centiskorch** (the win condition) | **20.8%** | **51.1%** |

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

## What was cut, and why

| Cut | Why |
| --- | --- |
| 2 Mega Chandelure ex | competes with Chandelure for the same Lampent, and **3 Prizes** is half the opponent's clock for one KO. `Gravity Gemstone` supplies the retreat tax for one card instead of a Stage 2 line |
| 1 Latias ex | 2 Prizes, and `Skyliner` frees your *Basics* — irrelevant to a Stage 1 attacker that never wants to move |
| 1 Comfey | `Flower Shower` draws **each** player 3 — symmetric, so it buys no edge, and it costs you 3 off your own cushion in one shot |
| 1 Maractus | `Corner` stops retreat for one turn but is an *attack*, so it costs you the 2-card Controlled Burn that turn. The lock is cheaper via Gravity Gemstone + hand denial |
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
