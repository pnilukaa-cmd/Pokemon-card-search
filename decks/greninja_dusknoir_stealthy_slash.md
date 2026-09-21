# Greninja ex / Dusknoir — Cursed Blast into Stealthy Slash

A user list, reviewed 2026-09-21. `Dusknoir`'s Cursed Blast puts **13
damage counters** on any one of the opponent's Pokémon and Knocks Dusknoir
out; `Greninja ex` 30C 21's **Stealthy Slash** then does 30 damage per
damage counter on that Pokémon — 390 — and can aim at the Bench. Two cards,
anything dead.

## The list holds two DIFFERENT cards called Greninja ex

`2 Greninja ex TWM 106` and `2 Greninja ex 30C 21` is legal: the four-copy
rule is per name, and that is exactly four. But they share nothing else:

| | TWM 106 | 30C 21 |
|---|---|---|
| HP | 310 | 300 |
| Type | Fighting | Water |
| Attacks | Shinobi Blade W 170 + search; Mirage Barrage | **Stealthy Slash**; Aqua Edge WW 160 |

`build_deck_model` keyed `POKEMON` by name with "first one wins", so the
model held four copies of the TWM card and the 30C one was **absent** —
and nothing warned: `unresolved` empty, `unmodeled` empty. The engine was
deleting the half of the deck that wins the game.

`meta_festival_lead` hits the same bug with `2 Applin TWM 17` (Grass) and
`2 Applin TWM 126` (Dragon). Fixed for both; see the commit. Re-measuring
`meta_festival_lead` moved it **+0.43 [−0.95, +1.81]** — the bug was real,
its impact was not.

## Three more gaps the list walked into

- **Stealthy Slash dealt 0** at every counter count. `_clause_count` had no
  rule for "damage counter on *that* Pokémon", and `_DOES_DMG_RE` wants
  "does N damage for each" adjacent — the interposed target phrase broke
  it. Now 0/3/7/13/20 counters → 0/90/210/390/600.
- **Ignition Energy provided one Colorless on everything.** It provides
  `CCC` on an Evolution Pokémon, so in a Stage 2 deck it was supplying a
  third of its value.
- **A regression I introduced fixing the first one.** The loose damage
  regex then matched `Kyurem ex`'s Blizzard Burst and `Palafin`'s Vanguard
  Punch, where the scaling clause belongs to a *secondary* sentence
  ("this attack ALSO does 10 damage to each Benched Pokémon FOR EACH Prize
  card taken"). Main damage is the printed 130. The old code scored it
  `base × count` = **390**; my regex then scored it **30**. Both wrong.
  Caught because a 15-point swing on `kyurem_vanilluxe_blizzard` was not
  plausible for a regex tweak.

`Grand Tree` is **not** inert, contrary to a claim made during this review:
`trainer_effect_ir` returns None for it, which is the wrong accessor —
`stadium_turn_effect_ir` compiles it to `evolve_from_deck` and it fires 11
times in six logged games.

## As submitted: 52.2%, rank 23 of 46

95% CI [48.1, 56.3], 26/45 winning matchups. A second independent seed set
read 53.7%. Best `meta_ns_zoroark` 87.5%; worst `lurantis_heal_punish`
20.5%, `meta_mega_excadrill` 30.0%.

## Ignition Energy is nearly dead here, and it is the whole finding

It provides **Colorless**. The only attack in the deck with a Colorless in
its cost is `Mirage Barrage` (WCC) — and that one discards 2 Energy to use.
`Stealthy Slash` (W), `Aqua Edge` (WW) and `Shinobi Blade` (W) get nothing
from it, and it discards itself at the end of your turn.

Swapping the three for Basic Water at the same count, changing nothing
else, is worth **+13.26** held out.

`Gravity Mountain` gives every Stage 2 in play −30 HP — including your four
Greninja ex and two Dusknoir. Cutting it is worth **+3.58**.

## What was tested

Every variant paired against the field, same CRN seed per pairing, two
independent seed sets.

| change | selection Δ | held-out Δ | 95% CI |
|---|---|---|---|
| −3 Ignition, −Gravity Mountain, +4 Water | +13.38 | **+15.08** | [+13.35, +16.81] |
| −3 Ignition, +3 Water | +10.47 | **+13.26** | [+11.81, +14.70] |
| −2 Meowth ex, +2 Water | +8.72 | **+10.54** | [+9.23, +11.86] |
| −Gravity Mountain, +1 Water | +1.96 | **+3.58** | [+2.54, +4.62] |

Every one survived. Then the Energy curve was walked out, because the
Tauros review had shown one that kept climbing past where the first edits
landed. **This one plateaus immediately.** Every jump past the recommended
list is noise, tested as cumulative sums rather than single steps:

```
 +1 Water and −Latias ex   +0.40  [−0.94, +1.74]  noise
 12 Water                  +1.01  [−0.17, +2.19]  noise
 13 Water                  +0.49  [−1.00, +1.98]  noise
```

So stop at 10. The lists that go further also drop to 10 Basics and a
25.86% mulligan for nothing.

## Recommended list — 67.1%, rank 4 of 46

**−3 Ignition Energy, −1 Gravity Mountain, +4 Basic Water Energy.** Two
lines. Keeps all 11 Basics and the 22.24% mulligan.

```text
Pokémon: 21
1 Latias ex SSP 76
1 Budew ASC 16
2 Frogadier CRI 21
2 Dusknoir PRE 37
2 Greninja ex TWM 106
2 Greninja ex 30C 21
4 Froakie CRI 20
2 Dusclops PRE 36
1 Fezandipiti ex ASC 142
2 Meowth ex POR 62
2 Duskull PRE 35
Trainer: 29
1 Surfer SSP 187
3 Poké Pad POR 81
3 Rare Candy MEG 125
2 Night Stretcher ASC 196
3 Hilda WHT 84
2 Colress's Tenacity SFA 57
1 Grand Tree SCR 136
4 Buddy-Buddy Poffin TEF 144
4 Lillie's Determination MEG 119
4 Ultra Ball MEG 131
2 Boss's Orders MEG 114
Energy: 10
1 Bubbly Water Energy CRI 84
9 Basic Water Energy
```

First attack by turn 6: 75.6% → **81.7%** on the 1000-trial baseline.

## What this measurement does not establish

**Stealthy Slash's Bench targeting is not modelled.** The card chooses any
of the opponent's Pokémon; the engine resolves damage against the Active.
Since Cursed Blast can load up a Benched threat and Stealthy Slash is meant
to shoot it, the attack's real value is **higher** than measured here —
this is a floor.

**Five Pokémon in this deck can never attack.** There is no Psychic Energy,
so `Latias ex` (Eon Blade PPC), `Dusknoir` (Shadow Bind PPC), `Dusclops`
and both `Duskull` attacks are uncastable. That is deliberate — they are
there for Skyliner and Cursed Blast, which are Abilities — but anything
from that line dragged into the Active Spot is a passed turn, and `Boss's
Orders` exists.

## Under the pilot team: greedy wins, and `setup` is measurably worse

The recommended list against the whole field under each pilot. **Field
deltas, not mirror deltas** — a mirror gain overstates by roughly 3x and
correlates only +0.27 with the field, so this varies the pilot on the
Greninja side, leaves every opponent on greedy, and keeps the CRN seed per
pairing. Two independent seed sets, because max-of-4 is biased upward.

| pilot | selection Δ | held-out Δ | held-out 95% CI |
|---|---|---|---|
| aggro | +0.92 | **−0.08** | [−1.38, +1.22] |
| control | −1.13 | **−1.46** | [−2.70, −0.21] |
| prizewise | −0.98 | **−1.47** | [−2.57, −0.37] |
| setup | −1.71 | **−1.70** | [−2.99, −0.41] |

`aggro` looked like +0.92 on the selection seeds — an interval already
spanning zero — and measured **−0.08** held out. Nothing beats greedy.

Picking the best pilot per OPPONENT reads **+2.67** on the selection seeds
and **−0.50** held out. All of it was noise, again.

**A prediction stated before the run, and wrong.** `setup` is the only
pilot that has ever converted a mirror gain into a field gain, and it did
so for decks that must assemble a board before they threaten anything —
which is exactly what a Stage 2 deck with Rare Candy, Grand Tree and a
six-card Duskull line looks like. `setup` is the **worst** pilot here, by
−1.70 held out, and significantly so on both seed sets.

The plausible reason, offered as speculation rather than measurement: this
deck's assembly is bought with Trainers — Rare Candy, Grand Tree,
Buddy-Buddy Poffin, Ultra Ball — not with attack turns. A pilot that
trades tempo for board development has nothing left to buy, and only gives
up the tempo.

The list's own number reproduced across three independent seed sets:
**67.08%**, **67.11%**, **67.87%**, rank 4 of 46 every time.
