# Cradily / Amoonguss — Special Conditions, Grass

The Cradily condition deck, rebuilt across 2026-09-21/22. `Cradily SCR 6`'s
**Miasma Wind** costs one Grass and does 100 per Special Condition on the
opponent's Active, capped at 3 by the Asleep/Confused/Paralyzed exclusivity.

## Where it started and where it ended

| list | mean | rank |
|---|---|---|
| as submitted | 44.3% | 37 of 45 |
| d1 — `Glimmora TWM 109` -> `SSP 115` | 50.5% | 29 |
| gr1 — + Foongus / Amoonguss | 57.0% | 13 |
| gr6 — cut the Glimmet/Glimmora line | 60.9% | 8 |
| **gb1 — Fighting Energy -> Grass** | **64.9%** | **4** |
| ac3 — Accelgor in, Tangela out | 65.0% | 4 |

**44.3% to 64.9%.** Every step validated on held-out seeds.

## What each step actually was

**The Glimmora swap (+5.51).** `Stun Poison` is a coin flip for 0 damage;
`Corrosive Shards` is the same Colorless cost for 20 damage and *guaranteed*
Poison. Miasma Wind whiffed on 30% of swings before this.

**Foongus / Amoonguss (+6.50).** `Amoonguss BLK 11`'s Dangerous Reaction is
30, +120 if the Active has any condition — **150 for one Colorless**, a
second payoff that needs no Fossil line. `Foongus BLK 10` sets it up for one
Colorless.

**Cutting the Glimmora line entirely (+10.88, and +4.38 over keeping it).**
This REVERSES the first step: once Amoonguss exists, the Fighting package is
a worse version of the same job. The earlier recommendation was not wrong
when it was made; it was superseded.

**Fighting Energy -> Grass (+4.01).** After the Glimmora cut, nothing in the
deck costs Fighting — verified by enumerating every remaining attack cost.
Four cards that could only pay Colorless, replaced by four that also pay
Miasma Wind.

## What was tested and rejected

| idea | result |
|---|---|
| **Bastiodon** (Ancient Bulwark wall) | **−30.91** |
| Bastiodon + Accelgor | −23.33 |
| Vileplume (two conditions per attack) | −1.03 |
| **Scovillain ex** (the only repeatable Burned source) | +0.90, noise |
| 3 Switch restored | −1.91 |
| Accelgor bolted onto Tangela builds | −4.82 |
| **Dark Bell** (put back to price it) | **−6.69** |

**Bastiodon is the biggest miss.** Every argument for it was true — Ancient
Bulwark works from the Bench so it needs no Energy, its Metal type is free,
and `Fossil Quarry` already fetches its Antique Armor Fossil. Measured:
Bastiodon reaches play in 50% of games, but **Cradily's rate falls from 89%
to 61%**, attacks per game roughly halve (Dangerous Reaction 173 -> 94) and
games shorten from 21.3 to 17.4 turns. A second Fossil Stage 2 line fights
the first for Fossil Quarry, Rare Candy and Bench space.

**Dark Bell was the user's catch, and it is the most expensive card in the
original list.** "Both Active non-Darkness Pokémon are now Confused" —
Cradily is Grass, so it confuses itself, and the engine models that
correctly: 50% the attack fails AND you take 30.

**Energy acceleration: not needed.** Every attack in the deck costs one
Energy (Miasma Wind `G`, Bind Down `G`, Poison Powder `G`, Toxic Spore `C`,
Dangerous Reaction `C`). You attach one per turn by rule.

## Accelgor, measured properly

Accelgor lost by 4-5 points every time it was added *on top of* Tangela. Cut
Tangela and run a full 3-3 line and it comes out level: on identical seeds,
across 88 paired matchups, **Accelgor minus gb1 = −0.76 [−1.86, +0.33],
noise**, better on 39 of 88. One seed set had it +0.14 and the other −1.66,
which is what a real tie looks like.

It also has the better opening — **29.98% mulligan against 34.64%** — since
Shelmet is a Basic and Tangela was doing less than assumed.

## Pilots

Greedy wins, as on every other deck this session. On the Accelgor build all
four alternatives span zero on both seed sets; per-opponent best pilot reads
+2.74 on selection seeds and **+0.06** held out.

## Caveat

Real mulligan is **29.98–34.64%**, not the 16-19% a naive count gives: the 4
`Antique Root Fossil` are Items and cannot be an opening Pokémon.
