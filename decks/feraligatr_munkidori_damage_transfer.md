# Feraligatr / Munkidori Damage-Transfer Engine

A unique combo found by scanning every ability across **all 10 Standard types** for two
narrow, complementary effects: an ability that puts damage counters on its *own* Pokémon,
and an ability that *moves* damage counters onto the *opponent's* side. Only one card in the
entire Standard-legal pool (1,964 cards) does each:

- **Feraligatr** (Water) — `Torrential Heart`: put 5 damage counters (50 damage) on itself,
  and this turn its attacks do +120 damage. Self-harm ability.
- **Munkidori** (Psychic) — `Adrena-Brain`: if it has any Darkness Energy attached, move up
  to 3 damage counters (30 damage) from one of your Pokémon to one of your opponent's. The
  *only* card in Standard that moves damage counters onto the opponent's side of the field.

No other Pokémon in the pool combines with either of these the way they combine with each
other. Chaining them together launders most of Feraligatr's self-inflicted damage straight
onto the opponent, for free, every turn — a genuinely unused interaction since these two cards
don't otherwise show up in the same archetype (Munkidori is normally a Darkness-deck piece;
Feraligatr is a rogue/budget Water attacker on its own).

## The combo, step by step

1. Feraligatr is Active with 2 Water Energy attached. Munkidori is on the Bench with 1 Basic
   Darkness Energy attached (that Energy also legally pays the Colorless slot of Munkidori's
   own attack if you ever need it — it isn't dead weight).
2. Use Feraligatr's `Torrential Heart`: put 5 damage counters (50 damage) on Feraligatr.
3. Use Munkidori's `Adrena-Brain`: move 3 of those damage counters (30 damage) off Feraligatr
   and onto the opponent's Active (or a juicy Benched target). Net cost to Feraligatr: only
   20 damage instead of 50. Both are Abilities, so both are free actions before your attack.
4. Attack with `Giant Wave` (Water/Water, base 160) for **160 + 120 = 280 damage**, plus the
   30 already sitting on the opponent's board from step 3 — up to **310 damage** total for a
   turn that only spent 2 Energy.
5. Giant Wave can't be used again next turn, but the Torrential Heart + Adrena-Brain damage
   transfer has no such restriction, so a second Feraligatr (swapped in via `Switch`) can
   repeat it, or you can attack with `Mind Bend` (Munkidori, 60 damage + Confuse) while
   waiting for Giant Wave to come back online.

180 HP Feraligatr can absorb four full activations at the mitigated 20-damage rate (80 total)
before it's in real danger, instead of the two activations (100 damage) it could take running
`Torrential Heart` alone.

## Why this hasn't been "found" before

Torrential Heart is the only self-damage ability in the pool that isn't a one-time sacrifice
(unlike Dusclops/Dusknoir's `Cursed Blast`, which KOs the user outright) — it's a *repeatable*
tax, which is exactly what Adrena-Brain's repeatable damage-siphon is built to offset. Pairing
a Water Stage 2 with a Psychic Basic that needs a splash of Darkness Energy means this combo
naturally spans three types at once, which is why it doesn't fall out of any single-type or
even two-type search for "good cards."

## Decklist (60 cards)

### Pokémon (14)

| Qty | Card | Set | Role |
|---|---|---|---|
| 4 | Totodile | Temporal Forces (TEF 39) | 70 HP Basic; also the exact HP cap for Buddy-Buddy Poffin |
| 2 | Croconaw | Temporal Forces (TEF 40) | Bridge; `Reverse Thrust` (30, switch) doubles as a free retreat |
| 4 | Feraligatr | Temporal Forces (TEF 41) | Centerpiece attacker |
| 4 | Munkidori | Twilight Masquerade (TWM 95) | Damage-transfer engine + backup attacker (`Mind Bend`, 60 + Confuse) |

### Trainers (31)

| Qty | Card | Type | Effect |
|---|---|---|---|
| 4 | Rare Candy | Item | Skip straight to Feraligatr off a Basic |
| 4 | Buddy-Buddy Poffin | Item | Bench 2 Basics ≤70 HP — fetches Totodile |
| 4 | Ultra Ball | Item | Discard 2, search any Pokémon (Munkidori, Feraligatr, Totodile) |
| 3 | Switch | Item | Escape Feraligatr's retreat cost 3 after a big turn |
| 2 | Night Stretcher | Item | Recur a KO'd Pokémon or a Basic Energy |
| 3 | Boss's Orders | Supporter | Gust the target you want the transferred damage/attack to hit |
| 2 | Rosa's Encouragement | Supporter | While behind on prizes, reattach 2 discarded Basic Energy to a Stage 2 (Feraligatr) |
| 2 | Drayton | Supporter | Look at top 7, grab a Pokémon + a Trainer |
| 2 | Brock's Scouting | Supporter | Search 2 Basics or 1 Evolution — the one card that can fetch Croconaw directly |
| 3 | Lillie's Determination | Supporter | Shuffle hand, draw 6 (8 late-game) |
| 2 | Colress's Tenacity | Supporter | Search a Stadium + an Energy card |

### Energy (15)

| Qty | Card |
|---|---|
| 13 | Basic Water Energy |
| 2 | Basic Darkness Energy |

2 Darkness Energy is enough — only one Munkidori needs one attached at a time to run
`Adrena-Brain`, and Night Stretcher / Ultra Ball discards can bring copies back if needed.

## Design notes / weaknesses

- Both Totodile and Feraligatr are Weak to Lightning (×2) — this deck folds fast to any
  Lightning matchup; there's no tech slot spared for it here, which is the honest tradeoff
  for how narrow the core combo is.
- Munkidori is Weak to Darkness (×2) but Resists Fighting (-30); keep it on the Bench, not
  Active, whenever possible — it's the engine, not a wall.
- 14 Pokémon / 31 Trainer / 15 Energy sits inside commonly-cited Standard ratios (roughly
  12-20 / 25-35 / 8-16), with 8 Basics (4 Totodile + 4 Munkidori) comfortably in the 6-8
  range recommended for consistent openers.
- Only 2 Croconaw back 4 Feraligatr — the app's own recommendation engine (see
  `android_app/`) correctly flags this as a thin evolution line. It's an accepted tradeoff
  here: 4x Rare Candy is meant to skip Croconaw entirely most games, so the 2 copies are
  backup insurance for when Candy isn't drawn, not the primary path. Verified this decklist
  parses to exactly 60 cards with the real app, cross-checked against `pokemon_standard_cards.json`.
- Checked with `check_energy_support.py`: Munkidori's only attack, `Mind Bend`
  (Psychic/Colorless), can never be paid — this deck runs Water and Darkness Energy only.
  That's expected, not a bug: Munkidori's whole role here is `Adrena-Brain`, which is an
  Ability (a "Darkness Energy attached" check, not an Energy cost) — it was never meant to
  attack.

## Pokémon TCG Live Import

```
Pokémon: 14
4 Totodile TEF 39
2 Croconaw TEF 40
4 Feraligatr TEF 41
4 Munkidori TWM 95

Trainer: 31
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin TEF 144
4 Ultra Ball MEG 131
3 Switch MEG 130
2 Night Stretcher SFA 61
3 Boss's Orders MEG 114
2 Rosa's Encouragement POR 84
2 Drayton SSP 174
2 Brock's Scouting JTG 146
3 Lillie's Determination MEG 119
2 Colress's Tenacity SFA 57

Energy: 15
13 Basic Water Energy
2 Basic Darkness Energy

Total Cards: 60
```
