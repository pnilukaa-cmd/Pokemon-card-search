# Maushold mill — Gnaw Together

<!-- field-results -->
> ### Field results — 2026-09-23
> **58.1% mean · 58.0% median · 37 of 53 winning matchups · rank 16 of 54**
>
> Best `meta_ns_zoroark` 92% · worst `lurantis_heal_punish` 28%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-09-23** and was measured against a different field or engine.
<!-- field-results -->


A user list, reviewed 2026-09-21/22. `Maushold 30C 125`'s **Gnaw Together**
(1 Colorless) flips a coin for each Maushold in play and mills 2 per heads;
`Backtrack Badge` re-flips the whole set and keeps the better.

## Two engine bugs had to be fixed before it could be measured

**Gnaw Together milled a flat 2.** It compiled to `MILL_OPPONENT amount=2`
with no flip scaling at all, so the deck's entire win condition ran at
under half rate. Three pieces were missing: `_clause_count` had no rule for
a bare card name ("Maushold you have in play"), the IR rule did not carry
the flip-per-each shape, and the executor neither rolled coins nor
consulted `query_reflip`. Verified against hand-computed truth:

| Maushold in play | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| engine, no badge | 1.02 | 2.03 | 3.04 | 4.05 |
| engine, Backtrack Badge | 1.51 | 2.78 | 3.95 | **5.10** |
| **before the fix** | 2 | 2 | 2 | 2 |

At four Maushold the badge also collapses the whiff rate from 6.2% to
**0.4%** and doubles the chance of the full 8 (6.2% → 12.1%). Gnaw Together
is the best mill attack in the pool; nothing else exceeds 3.

**A RecursionError crash.** `attack_rider_value` guarded a copy-attack with
`borrowed is not atk`, which only stops a direct self-copy. Two copiers
facing each other recurse forever, and `copied_attack`'s depth guard could
not see it — that guard releases its counter in a `finally` before this
function recurses. Found when it killed one shard of a 192-job run while
the other three exited cleanly, so the run reported itself finished.

## As submitted: 27.5%, rank 43 of 44

Reproduced at 26.99%, 27.09% and 27.47% on three seed sets. The plan works
when it works — **35 of 37 wins are deck-outs** — but it mills a mean of
**6.1 cards a game** against the ~50 needed, uses Gnaw Together 2.9 times
in a 21-turn game, and decks itself out in 25 games of 150.

The diagnosis is not the mill card. It is that a deck which only mills
hands over six Prizes for free. The field's best mill deck,
`kangaskhan_tyrantrum_flip_mill` at 52.5%, mills with Tyrantrum's Wreak
Havoc — **160 damage and a mill in the same attack** — on 14 Energy.

## Sixteen variants, 44 opponents, one seed set

| variant | mean | delta | rank |
|---|---|---|---|
| **m7 — 3 Dudunsparce ex, 1 Dudunsparce, 12 Energy** | **56.90%** | **+29.43** | **13** |
| m6 — 4 Dudunsparce ex | 54.59% | +27.12 | 18 |
| m5 — 3 Dudunsparce ex | 52.00% | +24.53 | 26 |
| p1 — Familial March split | 48.50% | +21.03 | 32 |
| m3 — 2 Dudunsparce ex + 10 Energy | 47.99% | +20.52 | 32 |
| p2 — Familial March, lighter | 46.90% | +19.43 | 32 |
| f1 — Accompanying Flute on m3 | 45.10% | +17.64 | 33 |
| f2 — Flute + Zoroark Mind Jack | 35.86% | +8.40 | 40 |
| p3 — Mega Scrafty ex + Punk Helmet | 32.40% | +4.93 | 41 |
| s1 — Mega Scrafty ex | 31.94% | +4.48 | 41 |
| m1 — 10 Energy only | 31.38% | +3.91 | 41 |
| **f3 — Accompanying Flute alone** | 24.45% | **−3.01** | 43 |

`m7` beats every rival head-to-head with a real margin: +2.31 over m6,
+4.90 over m5, +8.40 over the Familial March build.

### What the three user ideas measured

**Familial March works, and still loses.** `Maushold SSP 158` fetches two
Maushold from deck straight onto the Bench, skipping Tandemaus, and both
printings share the name so Gnaw Together counts them all (verified: a
mixed board of four returns a clause count of 4). It is worth **+21.03** —
and `m7` beats it by **+8.40**. Deploying mice costs an attack turn, and
that turn is worth more spent on Tenacious Tail.

**Punk Helmet does not pay.** It is Darkness-only, so it does nothing on a
Colorless mouse; on `Mega Scrafty ex` it stacks with Counterattacking Crest
for 90 back at the attacker. But Mega Scrafty ex is **3 Prizes**, and the
whole Scrafty package measures +4.93 against `m7`'s +29.43.

**Accompanying Flute alone is NEGATIVE: −3.01, better on 5 of 44.** Every
Basic it benches does leave their deck permanently, which is real mill —
but it builds their board for free, and a deck with no threat cannot
afford that. On top of a list that already has a threat it recovers to
+17.64, still well short.

## Recommended list — 56.9%, rank 13 of 44

```text
Pokémon: 19
1 Shaymin DRI 10
4 Maushold 30C 125
4 Dunsparce JTG 120
1 Dudunsparce TEF 129
2 Fan Rotom SCR 118
4 Tandemaus SSP 157
3 Dudunsparce ex JTG 178
Trainer: 29
3 Battle Cage PFL 116
3 Crushing Hammer UPR 166
1 Ultra Ball PLF 122
3 Night Stretcher MEG 173
4 Lillie's Determination MEG 169
3 Backtrack Badge PBL 74
4 Buddy-Buddy Poffin MEG 167
2 Hilda WHT 171
4 Poké Pad POR 113
1 Lana's Aid TWM 207
1 Neutralization Zone SFA 60
Energy: 12
4 Mist Energy TEF 161
8 Basic Psychic Energy
```

Out: 3 Hassel, Sacred Ash, Redeemable Ticket, Xerosic's Machinations,
**2 Dudunsparce**. In: **3 Dudunsparce ex**, 5 Basic Psychic Energy.

The lever is not "more ex" — it is cutting the Stage 1 `Dudunsparce` to a
single copy. It competed for the same evolution slot off the four Dunsparce
while threatening nothing. Mulligan is 22.24% in every top variant, so that
is not the driver either.

`Dudunsparce ex`'s Tenacious Tail costs **one Colorless**, the same as Gnaw
Together, and does 60 per opposing Pokemon ex — 240 against a two-ex board.
The deck goes from milling quietly to milling *and* threatening, which is
the Tyrantrum shape the field's best mill deck already proves out.

## Two caveats

`Crushing Hammer UPR 166` and `Ultra Ball PLF 122` name rotated printings.
Both resolve by name to a single current candidate, so the simulation is
right, but those exact cards are not Standard-legal — use `POR 71` and
`MEG 131`.

Energy stops paying at 10: `m1` (10 Energy) and `m4` (13 Energy) measure
+3.91 and +5.26, statistically the same. That is the third distinct energy
shape across four decks reviewed this session — Tauros wanted 16, Cradily
wanted none, this one wants 12 and no more.
