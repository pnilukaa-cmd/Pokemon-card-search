# Jellicent ex: Oceanic Curse Item lock

Reviewed 2026-10-28 from a submitted list: a 4-4 Frillish / Jellicent ex
line with 4 Ignition Energy, 4 Boss's Orders, and a disruption package of
Crushing Hammer, Enhanced Hammer, Handheld Fan, Eri, Xerosic's, Ruffian,
Rust Syndicate Grunt and Special Red Card. Asked with it: can it be mixed
with the Mega Chandelure ex deck (`mega_chandelure_ex_telepathic_hilda`),
keeping a simple line of Pokémon and the Item lock? The submitted
Pokégear 3.0 SVI 186 is a rotated printing; this pool carries BLK 84.

**This list: 66.83% against the 99-deck field at 1000 games per opponent**
(median 74.7%, 77 of 99 winning), on the engine as of 94c272f. On the same
seeds it is **+4.67 ± 0.43** over the submitted list (62.16%), better on
91 of 99.

**The changes:** −4 Ignition Energy, −3 Boss's Orders, +7 Basic Psychic
Energy. Everything else is the submitted list.

## The strategy, card by card

- **Jellicent ex** (WHT 45, Stage 1 Psychic, 270 HP, Retreat 3, weak to
  Darkness):
  - **Oceanic Curse:** while it's in the Active Spot, your opponent can't
    play Item cards or Pokémon Tool cards from their hand.
  - **Power Press** (Psychic, Colorless): 80, or 160 with 2 extra Energy
    attached.
- **Frillish** (WHT 44, Basic, 80 HP): Oceanic Gloom (Psychic) does 20,
  and the opponent can't play Items during their next turn. The lock
  starts before Jellicent ex is out.
- **The rest takes away what Items would have fixed:**
  - Energy: Crushing Hammer, Enhanced Hammer, Rust Syndicate Grunt, and
    Handheld Fan (moves an Energy off the attacker that hit it);
  - their hand: Eri (discard 2 Items), Xerosic's (down to 3), Special Red
    Card (to 3, late);
  - Tools and Special Energy: Ruffian;
  - Jellicent ex stays up with Jacinthe and Poké Vital A (heal 150), and
    Mist Energy stops attack effects on it.
- **Telepathic Psychic Energy** benches 2 Frillish when attached to a
  Psychic Pokémon; Hilda finds Jellicent ex and an Energy; Pokégear 3.0
  finds Supporters.

## What the measurements say

Each change below is paired against the list of its round, 200 games a
matchup.

**Mixing it with Mega Chandelure ex** (engine 4bdff48), both ways:

| Change | Measured |
|---|---|
| Chandelure list + 2 Frillish (for a Boss's Orders, a Poffin) | −5.37 ± 0.51 |
| Chandelure list + 2 Frillish + 2 Jellicent ex | −3.94 ± 0.57 |
| Chandelure list + 3 Frillish + 2 Jellicent ex | −5.01 ± 0.65 |
| Chandelure list + 2 Frillish + Eri | −5.09 ± 0.54 |
| Chandelure list + 2 Budew (Itchy Pollen) | −4.78 ± 0.48 |
| This list + a 3-3-3 Chandelure line, 2 Rare Candy (for the Fans, Hammers, Pokégear, Ruffian, Grunt, Red Card) | −2.41 ± 0.93 |

Neither deck wants the other's engine. In the Chandelure list with 2
Frillish and 2 Jellicent ex, the Energy went to Jellicent ex, whose Power
Press does 80–160 where Phantom Maze does 230 or more. Phantom Maze fell
from 3.78 uses a game to 2.47, and the wins against six strong decks from
43 to 31 of 60 (`tally.py`). The Chandelure list is also the stronger of
the two (73.3% to this list's 66.8%) and wins the matchup 75.6% to 24.4%.

**Tuning this list** (each against the round before; rounds 1–2 on
4bdff48, 3–5 on 94c272f):

| Round | Change | Measured |
|---|---|---|
| 1 | 4 Basic Psychic Energy for the 4 Ignition Energy | **+3.04 ± 0.46** |
| 1 | 2 Energy for 2 Pokégear / 2 Handheld Fan / 2 Watchtower / 2 Jacinthe | +1.11 / +1.06 / +0.90 / +0.75 |
| 1 | 2 Basic Psychic for the 2 Mist Energy | −0.42 ± 0.52 |
| 1 | 2 Budew for 2 Handheld Fan | −8.51 ± 0.65 |
| 2 | Energy for a Boss's Orders (4 → 3) | **+1.52 ± 0.40** |
| 2 | 2 Mystery Garden for the Watchtowers | −0.51 ± 0.44 |
| 2 | 2 Ignition back | −1.39 ± 0.46 |
| 3 | Energy for a Boss's Orders (3 → 2) | **+1.10 ± 0.44** |
| 3 | Energy for Ruffian / Special Red Card / Eri / Grunt / Xerosic's | +0.84 / +0.67 / +0.25 / +0.20 / +0.07 |
| 3 | 2 or 4 Ignition back, with the Ignition fix below | −0.08 / −0.72 |
| 3 | Prime Catcher for Poké Vital A | −1.11 ± 0.44 |
| 4 | Energy for a Boss's Orders (2 → 1) | **+1.48 ± 0.44** |
| 5 | Energy for the last Boss's Orders | +0.72 ± 0.49 |
| 5 | Energy for Ruffian / Special Red Card | −0.10 / −0.15 |

**What it adds up to:**
- **The Item lock works,** and keeping it is right: Oceanic Curse stops
  Switch, Rare Candy, Ultra Ball, Tools and the heals the opponent's
  attackers rely on. The disruption cards around it are each roughly
  neutral for an Energy, so they stay.
- **Energy was short.** At the end of turn 4 the submitted list's Active
  could attack in 68.6% of games; this list, 83.9% (`energy_curve.py`).
  Power Press wants 4 Energy for 160.
- **Ignition Energy doesn't fit.** On Jellicent ex it is three Energy for
  one turn, then it is discarded; on Frillish it is one Colorless that
  can't pay Oceanic Gloom. With the AI playing it only where it's spent
  that turn, 2 Ignition measured even with 2 Basic Psychic, and 4 lost.
- **Boss's Orders measured worse than Energy here,** one copy at a time,
  down to one (and the last one about even). Under the lock their Active
  can't play Switch or Air Balloon to leave either.

## How to play it

1. **Turn 1.**
   - Frillish Active, Telepathic Psychic Energy on a Frillish for two more.
   - Oceanic Gloom if you're going second: no Items for them next turn.
     The player going first can't attack on turn 1.
2. **Turn 2.**
   - Evolve the Active Frillish into Jellicent ex: the lock is on from
     now as long as it stays Active.
   - Power Press for 80; Hammers on their attacker.
3. **Every turn after.**
   - Four Energy on Jellicent ex for 160.
   - Jacinthe or Poké Vital A when it is damaged: a healed Jellicent ex is
     another turn of lock.
   - Eri and Xerosic's when their hand holds the Items they're waiting to
     play.

**The opponent's outs:**
- **Darkness.** Jellicent ex and Frillish are weak to it. The worst
  matchups: Munkidori ex / Pecharunt ex 3.7%, Mega Absol ex 11.2%.
- **Supporters, Abilities and Stadiums aren't locked.** Boss's Orders on a
  Benched Frillish, switching Abilities, and Stadium-based switches all
  work.
- **Knocking out the Active Jellicent ex** turns the lock off until the
  next one is promoted. It gives up 2 Prizes.
- **Retreat 3:** once Jellicent ex is Active it stays there.
- **4 Basics: a 60.1% mulligan.** Telepathic Energy only helps after
  setup.

## Matchups (1000 games each)

Both lists on 94c272f, the same seeds.

**Best:** Mew baby box 99.5%, Mew / Hypno 97.4%, Trevenant / Rapidash /
Uxie 96.1%, Wobbuffet / Orbeetle 95.6%, Team Rocket's Tyranitar 95.5%.

**Worst:**

| Opponent | This list | Submitted |
|---|---|---|
| Munkidori ex / Pecharunt ex | 3.7% | 3.6% |
| Mega Zeraora ex / Cinderace | 8.0% | 7.4% |
| Mega Absol ex hand lock | 11.2% | 11.5% |
| Mega Zygarde ex / Cinderace, Gaia Wave | 13.5% | 15.5% |
| Arboliva / Ogerpon | 19.9% | 16.1% |
| Mega Gengar ex / Toxtricity | 20.4% | 17.9% |
| N's Zoroark toolbox | 21.6% | 15.7% |
| Snorlax / Bouffalant / Mega Kangaskhan ex | 22.4% | 19.6% |
| Mega Chandelure ex / Telepathic / Hilda | 24.4% | 17.3% |

**The meta decks:**

| Opponent | This list | Submitted |
|---|---|---|
| Festival Lead | 93.6% | 90.6% |
| Slowking | 86.8% | 85.6% |
| Dragapult / Dusknoir | 83.0% | 75.3% |
| Dragapult | 78.7% | 72.3% |
| Dragapult / Blaziken | 75.0% | 66.7% |
| Raging Bolt | 61.3% | 65.9% |
| N's Zoroark | 49.8% | 44.0% |
| Mega Excadrill | 41.7% | 32.2% |

## What the simulator found

Each fix has a regression test that fails on the commit before.
1. **Ignition Energy was never discarded** (4bdff48). "Discard it at the
   end of your turn" had no reader for Energy, so on an Evolution Pokémon
   it was three permanent Colorless. The submitted list read 65.58% with
   that and 60.35% without it (200 games).
2. **Energy that depends on its holder's Stage didn't follow it**
   (4bdff48). Ignition attached to a Frillish stayed one Colorless on the
   Jellicent ex it became; Neo Upper Energy on a Lampent stayed Colorless
   on Mega Chandelure ex. It is now recomputed when a Pokémon evolves,
   devolves or is swapped. Field decks with Prism or Neo Upper Energy:
   `mew_baby_box`, `mew_pikachu_box`, `study_flygon_sandy_flapping_mill`,
   `study_maushold_gnaw_latias`.
3. **Ignition went where it was thrown away** (94c272f, a pilot rule,
   `temp_energy_now`): to a bare Frillish or a Benched Pokémon. It now goes
   only to the Active, and only when it raises the Active's damage this
   turn: +1.37 ± 0.41 on the submitted list.
4. **The inert-card guard misread Mystery Garden** as never played (it is
   put down once two Psychic Pokémon are in play), and the setup baseline
   listed Eri, Ruffian, Rust Syndicate Grunt, Jacinthe and Poké Vital A as
   unmodelled; they have no effect on development there.

## Cards searched

- **Item lock** (`item_lock`, plus raw sweeps for "can't play any Item"
  and "Item cards from their hand": no gaps): Jellicent ex, Frillish,
  Budew (−8.51 here, −4.78 in the Chandelure list), Tyranitar's Daunting
  Gaze (Darkness, Stage 2), Flaaffy's Disconnect (Lightning), Galvantula
  ex's Fulgurite (Lightning, discards its Energy).
- **Stadium lock** (`stadium_lock`): Copperajah, Chi-Yu, neither Psychic.

**Anti-synergies:**
- Mist Energy and Ignition Energy provide Colorless only: neither pays
  Oceanic Gloom's Psychic, or the Psychic half of Power Press.
- The list has no Switch, and Jellicent ex has Retreat 3: a Frillish
  promoted in front of it is stuck there.

## 1000-trial setup baseline

| Pokémon | Submitted, by turn 6 | This list, by turn 6 | This list, average turn |
|---|---|---|---|
| Frillish | 100.0% | 100.0% | 1.00 |
| Jellicent ex | 90.7% | 88.8% | 2.35 |

First attack by turn 6: **96.9%** of trials (average turn 2.86), against
96.0% (2.92).

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Poké Vital A)
  (`check_energy_support.py`).
- Every attack is payable with Psychic Energy. No Ability gates an attack.
- **4 Basics: a 60.1% mulligan.**

**Real lists:** the published Jellicent ex decks pair it with Gardevoir ex
(Ralts, Kirlia), Munkidori and Scream Tail. Gardevoir ex isn't in this
pool. Frillish's Oceanic Gloom as an early lock is common to them.
- [Deltia's Gaming: Jellicent ex deck guide](https://deltiasgaming.com/?p=288369)
- [Limitless: Jellicent ex decklists](https://limitlesstcg.com/cards/en/WHT/45/decklists)
- [pokemoncard.io: Jellicent ex decks](https://pokemoncard.io/category/pokemon/jellicent-ex-rsv10pt5-45)

## PTCGL import

```
Pokémon: 8
4 Jellicent ex WHT 45
4 Frillish WHT 44

Trainer: 35
4 Lillie's Determination MEG 119
4 Hilda WHT 84
4 Jacinthe POR 75
1 Xerosic's Machinations SFA 64
1 Eri TEF 146
1 Rust Syndicate Grunt PBL 81
1 Ruffian JTG 157
1 Boss's Orders MEG 114
4 Pokégear 3.0 BLK 84
4 Crushing Hammer POR 71
2 Enhanced Hammer TWM 148
4 Handheld Fan TWM 150
1 Special Red Card CRI 82
1 Poké Vital A SFA 62
2 Team Rocket's Watchtower DRI 180

Energy: 17
4 Telepathic Psychic Energy POR 88
2 Mist Energy TEF 161
11 Basic Psychic Energy

Total Cards: 60
```
