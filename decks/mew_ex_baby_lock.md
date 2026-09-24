# Mew ex "baby attacks" lock

**Not my list.** Supplied 2026-09-24. Basic Energy is written without a set
code (`Basic {P}/{W} Energy MEE` -> `Basic Psychic/Water Energy`).

**17.47% (±0.15) against all 54 field decks at 1000 games each, winning 3.**
Read that as the limit of a one-turn greedy pilot, not a verdict on the
list -- see "Why the number is low".

```
Pokémon: 19
1 Cubchoo BLK 25
1 Latias ex SSP 76
3 Dudunsparce TEF 129
1 Totodile TEF 39
1 Comfey SCR 63
1 Exeggcute 30C 1
3 Dunsparce JTG 120
1 Dedenne SSP 87
1 Elgyem BLK 40
1 Clefairy POR 30
1 Shaymin DRI 10
1 Psyduck ASC 39
3 Mew ex 30C 66

Trainer: 32
2 Accompanying Flute TWM 142
1 Enhanced Hammer TWM 148
1 Miracle Headset SSP 183
1 Xerosic's Machinations SFA 64
2 Battle Cage PFL 85
1 Tool Scrapper ASC 212
4 Poké Pad ASC 198
3 Night Stretcher ASC 196
1 Air Balloon BLK 79
1 Judge POR 76
1 Lana's Aid TWM 155
1 Hilda WHT 84
1 Redeemable Ticket JTG 156
2 Gravity Gemstone SCR 137
2 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination MEG 119
2 Ultra Ball MEG 131
3 Boss's Orders MEG 114

Energy: 8
2 Basic Psychic Energy
4 Prism Energy BLK 86
2 Basic Water Energy

Total Cards: 60
```

## The plan

`Mew ex` (Memory Helix: use any Benched Pokemon's attack; Retreat 0) sits
Active on `Prism Energy` (every type on a Basic) and borrows one-Energy
"baby" attacks: `Cubchoo` Snotted Up (Defending Pokemon can't attack),
`Totodile` Big Bite (can't retreat), `Exeggcute` Hypnosis, `Clefairy` Follow
Me (gust), `Elgyem` Slight Shift, `Dedenne` (a Trainer back). `Gravity
Gemstone` and Big Bite hold the locked Pokemon in place; `Accompanying
Flute` puts fresh Energy-less Basics on the opponent's Bench to drag up.

## What the engine had wrong

Every field run with this list crashed (IndexError in Enhanced Hammer).
Fixed, each with a regression test that fails on 4acbc5d:

- Energy removal kept `energy` and `energy_names` out of step (retreat,
  attack discard costs, Energy-discard effects), and discarded a
  placeholder "Energy" nothing could recover. Enhanced Hammer also aimed
  at the Pokemon with the most Energy rather than one with Special Energy.
- Discard-pile recovery returned Pokemon whatever the card said (Miracle
  Headset's Supporters, Dedenne's Trainer, Lana's Aid's Basic Energy).
- Tool Scrapper was never played, and would have scrapped your own Tools.
- Accompanying Flute had no model.

## Why the number is low

The lock needs a different borrowed attack each turn, chosen against what
the opponent will do next turn. The pilot scores one turn at a time. Two
rules were measured and reverted: pricing "can't attack" riders (-0.27 ±
0.50) and feeding Mew Energy first (+0.31 ± 0.47). Mew ex is in play by
turn 6 in only 56.6% of 1000 baseline trials (3 copies, Ultra Ball the only
Rule Box search), and from turn 5 most idle turns have no Energy anywhere.
