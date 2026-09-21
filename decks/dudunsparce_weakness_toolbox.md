# Illumise ×3 Weakness — the combo is the problem, not the payoff

A user list, sent 2026-09-21 with the question "it seems to be focused on
3x weakness?" It is, and that focus costs it more than thirty points.

## The engine could not see the deck's thesis

`Illumise` 30C 4 — **Supereffective Pheromones**: "If you have Volbeat in
play, apply Weakness for both Active Pokémon as ×3". Three things were
wrong, all fixed before anything was measured:

1. **The engine had no Weakness multiplier concept.** `do_attack` did
   `dmg *= 2` inline. Illumise is the only card in the pool that changes
   it, so the ability compiled to `no rule matched` and did nothing.
   Added `Op.WEAKNESS_MULTIPLIER` and `query_weakness_multiplier`, read by
   both damage sites. It says BOTH Active Pokémon, so both boards are
   checked — the opponent attacking into **your** Weakness gets ×3 too.
2. **`parse_conditions` matched "if you have X in play" case-sensitively**,
   so the clause only registered mid-sentence. Three cards put it first:
   Illumise, `Shelmet` and `Karrablast`. A dropped condition is worse than
   a missed effect — the effect then applies **unconditionally**, and
   Shelmet and Karrablast's Stimulated Evolution had been evolving without
   the partner they require.
3. **`Mew ex`'s Memory Helix** was the rule still missing after 30th
   Celebration landed. Added `Op.GRANT_BENCH_ATTACKS`; Mew ex now borrows
   the whole Bench, copy-attacks excluded so a borrow cannot borrow a
   borrow.

No field deck runs Illumise, Volbeat, Shelmet, Karrablast or Mew ex, so
none of this disturbs the recorded field.

## As submitted: 31.2%, rank 42 of 46, 1 of 45 winning matchups

Reproduced at 30.9% and 31.0% on two further seed sets. Its one winning
matchup is `meta_ns_zoroark` at 84.0%. Under the pilot team greedy wins
again (aggro +0.86 held out, spanning zero); `setup` reads **−6.84** and
wins 1 of 45 — the worst pilot result recorded in this repo.

## The ×3 fires on about one attack every three games

Instrumented directly over 150 games:

```
Weakness multiplier queried on this deck's side   153 times (~1 per game)
   returned x2   103  (67.3%)
   returned x3    50  (32.7%)
Illumise AND Volbeat both in play at that moment   50 of 153 (32.7%)
```

Two things stack against it. **Weakness comes up about once a game at
all** — the multiplier is only consulted when the defender's Weakness
already matches the Active's type, and these thirteen Pokémon span seven
types with no way to choose which is Active when it matters. Of those rare
moments, the ×3 is live a third of the time, because it needs two specific
70–80 HP Basics alive at once.

## Cutting the combo is worth more than thirty points

Every variant paired against the field, three independent seed sets.

| change | selection Δ | held-out Δ | 95% CI |
|---|---|---|---|
| **more** combo (3 Volbeat / 3 Illumise) | −0.51 | **−0.86** | [−2.19, +0.48] |
| combo + Energy | +1.91 | +0.79 | [−0.59, +2.17] |
| Energy only | +5.68 | +4.66 | [+3.19, +6.12] |
| cut combo, 2 Dudunsparce ex | +21.66 | +20.49 | [+18.36, +22.62] |
| cut combo, 3 Dudunsparce ex, 14 Energy | — | **+31.38** | [+28.71, +34.04] |

Committing harder to the ×3 is worth nothing. Removing it is worth twenty
points, and the freed slots are worth ten more.

Pushed further on a third seed set, against the best of those as anchor:

```
 +1 Dunsparce +1 Dudunsparce ex  +3.49 [+1.96, +5.01]  REAL
 more Energy                     -0.24 [-1.86, +1.37]  noise
 both of the above               +4.71 [+3.23, +6.19]  REAL
```

More of the **Dudunsparce ex line** pays; more Energy does not. That is the
opposite of what the last two decks reviewed here wanted, and worth
remembering before assuming Energy is always the answer.

## Recommended list — 66.7%, rank 4 of 46

The 7-Basic version measured 67.9% — **+1.22 against this one, 95% CI
[−0.35, +2.79], noise** — while taking the mulligan from 29.98% to
**39.91%**. Statistically tied, so the safer opening wins the tie.

```text
Pokémon: 16
3 Dudunsparce TEF 129
1 Lillie's Clefairy ex ASC 280
4 Dunsparce JTG 120
2 Mew ex 30C 158
4 Dudunsparce ex JTG 178
1 Shaymin DRI 10
1 Moltres PFL 14
Trainer: 31
2 Boss's Orders RCL 189
1 Lana's Aid TWM 207
2 Crispin SCR 164
4 Lillie's Determination MEG 169
1 Air Balloon MEG 166
3 Buddy-Buddy Poffin MEG 167
3 Ultra Ball PLF 122
1 Counter Gain ASC 259
3 Night Stretcher MEG 173
2 Gwynn PBL 119
1 Tool Scrapper CRI 115
4 Poké Pad POR 113
1 Special Red Card CRI 113
2 Brave Bangle WHT 80
1 Battle Cage PFL 116
Energy: 13
1 Basic Fire Energy
1 Legacy Energy TWM 167
1 Basic Fighting Energy
1 Basic Lightning Energy
4 Prism Energy ASC 216
5 Basic Psychic Energy
```

Gone: 2 Volbeat, 2 Illumise, 1 Unown, 1 Stunfisk, 1 Marnie's Purrloin,
1 Passimian. In: 3 Dudunsparce ex, 1 Dunsparce, 4 Basic Psychic Energy.

First attack by turn 6: 75.6% → **96.0%**. What wins games is
`Dudunsparce ex`'s Tenacious Tail — 60 per opposing Pokémon ex in play,
which reads 240 against a two-ex board — and `Mew ex` borrowing it through
the Memory Helix implemented for this review.

**The mulligan is still 29.98%**, up from the submitted list's excellent
9.92%. That is the real price of this rebuild and it is not small: nearly
one opening hand in three is a free card for the opponent. The win rate
already includes that cost, since the simulator models mulligans — but if
you want the original's opening back, the 2-Dudunsparce-ex version at
51.7% and 19.06% mulligan is the compromise.

## Two caveats

**`Boss's Orders RCL 189` and `Ultra Ball PLF 122` name rotated
printings.** Both resolve by name to current cards and only one candidate
exists, so the simulation is right — but RCL and PLF are long out of
Standard. Use `MEG 114` and `MEG 131`.

**None of this says the ×3 is a bad card.** It says it is a bad card *in a
deck that cannot choose which type attacks*. A list built to put a
specific attacker Active against a known Weakness would measure
differently, and was not tested here.
