# Decidueye ex / Vivillon — "exactly 4" cost lock

A deck whose entire job is to keep the opponent's hand at exactly four
cards, because that is the switch on `Decidueye ex`'s Ability.

## The engine

**Decidueye ex** (POR 100, Stage 2 Grass, 320 HP, retreat 2)

- Ability **Sniper's Eye** — *"If your opponent has exactly 4 cards in
  their hand, ignore all Colorless Energy in the costs of attacks used by
  this Pokémon."*
- Attack **Crushing Arrow** — `Grass / Colorless / Colorless / Colorless`,
  **240 damage**, *"Discard an Energy from your opponent's Active
  Pokémon."*

Sniper's Eye turns Crushing Arrow from a four-Energy attack into a
**one-Grass-Energy** attack. That is the whole deck: 240 damage plus
Energy denial off a single manual attachment, repeatable from turn 3 —
but only on turns where the opponent is holding exactly 4.

## Why Judge, and why Judge is not enough on its own

**Judge** (POR 76, Supporter) — *"Each player shuffles their hand into
their deck and draws 4 cards."*

A sweep of the whole Standard pool for effects that set an opponent's
hand to a fixed number confirms **Judge is the only Supporter that lands
on exactly 4**. The near misses set the wrong number and are dead here:

| Card | Sets opponent to | Verdict |
| --- | --- | --- |
| Judge (POR 76) | **4** | the card |
| Team Rocket's Archer (ASC 201) | 3 | wrong number, plus needs TR Pokémon |
| Harlequin (WHT 163) | 3 or 5 on a flip | wrong either way |
| Lucian (TWM 157) | flip-dependent | unusable |
| Meddling Memo (PRE 120) | same count they had | no |
| **Unfair Stamp** (TWM 165) | **2** | **anti-synergy — actively switches Sniper's Eye off** |

Judge alone has two problems, though, and both are structural:

1. **One Supporter per turn.** Judging every turn means never playing
   Boss's Orders, never playing a draw Supporter, never playing a damage
   boost. The deck stalls out doing exactly one thing.
2. **It is symmetric.** Judge caps *your* hand at 4 too, so it wants to be
   played after you have dumped your hand, not before.

## The fix — Vivillon POR 9

**Vivillon** (POR 9, Stage 2 Grass, 120 HP, retreat 1)

- Ability **Grand Wing** — *"Once during your turn, you may use this
  Ability. Your opponent shuffles their hand and puts it on the bottom of
  their deck. If they put any cards on the bottom of their deck in this
  way, they draw 4 cards."*

This is Judge as an **Ability**: same number, every turn, free, and it
does not touch your own hand or your Supporter slot. It is also *stronger*
disruption than Judge — their cards go to the **bottom of the deck**
rather than being shuffled in, so what they were holding is gone for the
rest of the game rather than redrawable.

Both are in the deck because they fail in opposite directions:

- Grand Wing has a hole — *"if they put any cards on the bottom"*. An
  opponent who has emptied their hand stays at 0, and Sniper's Eye stays
  off.
- Judge has no such clause. Against a hellbent opponent, Judge is the card
  that forces them back up to exactly 4.

Vivillon doing the hand-setting is also what frees the Supporter slot for
`Black Belt's Training` — see the damage math below.

## The damage math

Crushing Arrow is 240. Most ex attackers in the format sit at 260–330 HP,
so 240 on its own is a two-hit KO on the things that matter.

- **Black Belt's Training** (ASC 255, Supporter): *"During this turn,
  attacks used by your Pokémon do 40 more damage to your opponent's Active
  Pokémon ex."* → **280**, which one-shots the 260–280 HP tier.
- This only works on a turn Vivillon is setting the hand, because Judge
  and Black Belt's Training both want the same Supporter slot. That
  trade — Ability sets the hand, Supporter adds the damage — is the deck's
  best turn.

## Decklist

```
Pokémon: 19
4 Rowlet SFA 3
2 Dartrix SFA 4
3 Decidueye ex POR 100
4 Scatterbug POR 7
1 Spewpa POR 8
3 Vivillon POR 9
2 Budew ASC 16

Trainer: 32
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Rare Candy MEG 125
2 Pokégear 3.0 BLK 84
2 Switch MEG 130
1 Night Stretcher MEG 173
1 Grand Tree SCR 136
4 Judge POR 76
3 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Black Belt's Training ASC 255
2 Dawn PFL 118
1 Carmine TWM 145

Energy: 9
9 Basic Grass Energy

Total Cards: 60
```

### Card choices worth stating

- **Rowlet SFA 3 (70 HP), not POR 10 (80 HP)** — and **Scatterbug POR 7
  (40 HP)**, **Budew ASC 16 (30 HP)**. Every Basic in the deck is at or
  under 70 HP, so `Buddy-Buddy Poffin` can fetch **any two of them**. The
  80 HP Rowlet printing would be Poffin-ineligible and quietly break the
  opening.
- **Grand Tree SCR 136 as the ACE SPEC.** Two Stage 2 lines in one deck is
  the deck's real risk, and Grand Tree is the only card in the pool that
  fixes it: it searches a Stage 1 onto a Basic *and then* the matching
  Stage 2 onto that, once per turn, free, from the deck. In simulation it
  is worth about +11 points of Decidueye ex consistency and +13 of
  Vivillon (see below). It is symmetric — the opponent gets the same
  evolution every turn — which is a real cost, but this deck has more to
  gain from it than almost any deck does. `Maximum Belt` (+50 vs ex) was
  the tested alternative and lost: without Grand Tree, Decidueye ex landed
  by turn 6 in only 58% of games.
- **2 Dartrix / 1 Spewpa.** They are mostly skipped by Rare Candy, but
  Grand Tree searches the *Stage 1* out of the deck, so the middle stages
  cannot be cut to zero.
- **Budew ASC 16** — free-cost `Itchy Pollen` Item-locks the opponent for a
  turn and it retreats for free. It is a Basic that buys the turns a
  double-Stage-2 deck needs.
- **9 Grass Energy** is deliberately high for a deck that usually attacks
  off one. It is insurance for the turns Sniper's Eye is *off*, where
  Crushing Arrow costs the full four.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC, no
energy-type shortfall on any attack, no attack-gating Ability text.

Mulligan rate with 10 Basics: **25.9%** (`comb(50,7)/comb(60,7)`).

`simulate_baseline.py`, 1000 trials — in play by turn 6:

| | % | avg turn |
| --- | --- | --- |
| Rowlet | 95.9% | 1.51 |
| Scatterbug | 95.7% | 1.59 |
| Budew | 82.4% | 1.95 |
| Dartrix | 80.1% | 2.96 |
| **Decidueye ex** | **68.3%** | 3.65 |
| Spewpa | 62.8% | 3.29 |
| **Vivillon** | **59.6%** | 3.63 |

First attack landed by turn 6: 78.6% (avg turn 2.67).

Builds tested along the way, by Decidueye ex / Vivillon on turn 6:

| Build | Decidueye ex | Vivillon |
| --- | --- | --- |
| Maximum Belt ACE SPEC | 52.5% | 39.6% |
| Grand Tree ACE SPEC | 66.3% | 53.4% |
| + 2 Dawn (−1 Pokégear) | 69.5% | 53.0% |
| + 3rd Vivillon (−1 Switch) | 67.5% | 64.0% |
| **final (−1 Night Stretcher, +2nd Black Belt's)** | **68.0%** | **59.9%** |

A no-Vivillon variant (Dunsparce/Dudunsparce as the draw engine, Judge as
the only hand-setter) was built and tested too: it reached Decidueye ex
62.0% by turn 6, no better than the two-line build, and had no way to set
the opponent's hand without spending the Supporter slot. Dropped.

`simulate_versus.py`, 300 games each:

| Opponent | Win rate |
| --- | --- |
| Mega Scrafty ex darkness tank | 62.0% |
| Eerie Inferno Ninetales burn | 52.7% |
| Hop's Snorlax stacked buff | 44.0% |
| Steven's Carbink damage wall | 36.3% |
| Team Rocket's Persian ex attack theft | 35.3% |

*(Every number on this page was re-measured after a later fix to evolution
timing — the simulators had been letting one Pokémon evolve twice in a
single turn, which flattered every Stage 2 deck by about a turn. The
figures above are the post-fix ones.)*

## Turn sequence — what actually has to happen

- **Turn 1.** Ideally Budew or Rowlet active. Poffin for Rowlet +
  Scatterbug. `Carmine` is legal on your own first turn going first.
  You cannot Rare Candy this turn, and you cannot evolve a Basic put into
  play this turn. *Their out:* a fast attacker that KOs a 30–70 HP Basic
  and puts you a prize behind immediately.
- **Turn 2.** Rare Candy a Rowlet into Decidueye ex, or let Grand Tree run
  the Scatterbug → Spewpa → Vivillon chain. Attach a Grass to Decidueye.
  Judge here is usually a refill, not a combo enabler, since you cannot
  attack profitably yet. *Their out:* their own Stadium bumping Grand
  Tree, which costs you the free evolution every subsequent turn.
- **Turn 3 — the first real combo turn.** Grand Wing (if Vivillon is
  down) or Judge → opponent at exactly 4 → Sniper's Eye is on → Crushing
  Arrow for **one Grass Energy**, 240 damage, and an Energy off their
  Active. *Their out:* Boss's Orders on your Vivillon, or any bench snipe
  — Vivillon is 120 HP and dies to a lot.
- **Turn 4 onward.** Grand Wing every turn keeps the discount live and the
  Supporter slot open. Spend it on `Black Belt's Training` for the 280 vs
  ex, or `Boss's Orders` to drag something out, or `Lillie's
  Determination` to refuel. Crushing Arrow strips an Energy every single
  turn, so a slow opponent never re-arms.

Order-of-operations note: play your Items **before** Judge. Judge shuffles
your hand away, so Rare Candy, Ultra Ball and Poffin should already be
spent when it resolves.

## Where this deck loses

- **Fire.** Every Pokémon in the deck is Grass with **Fire ×2 weakness**,
  Decidueye ex included. A 160-damage Fire attack is a clean one-shot on a
  320 HP Stage 2.
- **Flat damage reduction.** `Steven's Carbink` / `Granite Cave`-style
  team-wide −30 turns 240 into 210 and 280 into 250, which is exactly the
  wrong side of the ex HP breakpoints. 35.3% in simulation.
- **Anything that empties its own hand.** A hellbent opponent switches
  Sniper's Eye off, and Grand Wing cannot fix it because they have nothing
  to put on the bottom of their deck. This is what the 4 Judge are for —
  Judge draws them 4 unconditionally.
- **Prize math.** Decidueye ex gives up 2 prizes and needs two attacks to
  KO a big ex without Black Belt's Training. Trading 2-for-2 while needing
  two turns per KO is a losing race against a deck that one-shots you.
- **Getting Grand Tree bumped.** It is your only Stadium and your only
  ACE SPEC; once another Stadium replaces it, the evolution engine is gone
  and you are back to drawing into Rare Candy.

## Simulator work this deck required

Two genuine engine bugs surfaced while testing this list, both fixed in
`ability_ir.py` / `ability_engine.py` with firing tests in
`test_ability_engine.py`:

1. **Sniper's Eye compiled without its condition.** `parse_conditions`
   had no rule for *"if your opponent has exactly N cards in their hand"*,
   so the Colorless-ignore compiled as a **permanent, unconditional**
   discount. Every deck built on this card would have simulated as far
   stronger than it is. Added the `opponent_hand_size` condition (`==`,
   `>=`, `<=`), wired into `conditions_met`, and made it fail closed when
   no opponent is in view rather than reading the player's own hand.
2. **Grand Wing compiled to the wrong effect entirely.** The `draw_n` rule
   matched *"they draw 4 cards"* and produced `draw 4 -> both_all` — free
   cards for the Vivillon player, and no hand-size change on the opponent
   at all, which is the only part that matters. Added `Op.SET_OPPONENT_HAND`
   and an `opponent_hand_reset` rule that owns this shape (Gothitelle's
   `Distorted Future` was mis-compiling the same way and is now correct
   too), and taught `draw_n` to stand down for it.

Also modeled, since they were being scored as blanks: `Judge`, `Carmine`,
`Pokégear 3.0` and `Black Belt's Training` in both simulators. Before
those landed the versus sim had this deck at 34.0% against Mega Scrafty;
with them it is 62.0%.
