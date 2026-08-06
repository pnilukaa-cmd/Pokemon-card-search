# Krookodile ex / Relicanth Hand Disruption

Built around a specific request: a Basic-or-Stage-1 attack that strips the
opponent's hand down, paired with a Stage 2/ex-level HP shell to survive
long enough for the disruption to matter. Krokorok's `Tighten Up` (a
Stage 1 attack) discards cards from the opponent's hand; evolving it into
**Krookodile ex** (320 HP) buys the time needed to keep landing hits while
staying alive.

## Centerpieces

1. **Sandile -> Krokorok -> Krookodile ex** (BLK 135 / BLK 136 / CRI 55) —
   the disruption + survivability line itself. Krookodile ex is a Stage 2
   ex, not a Basic-or-Stage-1 attacker on its own; the hand-stripping
   attack lives on Krokorok, and evolving further trades that attack away
   for HP and a bigger attack (`Corner`/`Strong Bite`).
2. **Relicanth** (TEF 173) — Ability-only include. Its Ability lets your
   evolved Pokémon use any attack from their previous Evolutions, meaning
   a fully-evolved Krookodile ex can reach back down and use Krokorok's
   `Tighten Up` again once both pieces are in play, without giving up
   Krookodile ex's HP or its own attacks.
3. **Scraggy -> Mega Scrafty ex** (ASC 134 / ASC 135) — replaced an earlier
   Team Rocket's Koffing/Weezing package once the deck's real weakness
   turned out to be "my one attacker dies too fast," not "empty bench"
   (Koffing/Weezing solved the second problem, not the first). Mega
   Scrafty ex is 330 HP, on par with Krookodile ex itself, and its
   Ability `Counterattacking Crest` places 5 damage counters on whatever
   attacks it while Active — even if that hit is lethal. Paired with a
   Punk Helmet (4 more counters) on the same Pokémon, that's 9 free
   damage counters back per hit, real retaliation rather than just board
   replacement. Its attack `Outlaw Leg` (D+D+C, 160 dmg) discards a random
   hand card **and** the top deck card in one swing. Scraggy's own
   `Knock Off` (D+C, discard random hand card, guaranteed — the ASC 134
   printing specifically; a different 60 HP printing only has a
   coin-flip `Kick Shot`) is Memory Dive-reachable once evolved, same
   role Krokorok's `Tighten Up` plays for the other line.

## Design notes

- **No Rare Candy, deliberately.** Rare Candy explicitly "skips the
  Stage 1" when evolving a Basic straight to Stage 2, meaning the Stage 1
  card is never actually stacked underneath the resulting Pokémon.
  Relicanth's Ability only works for Pokémon that evolved *through* every
  stage normally — a Rare-Candy'd Krookodile ex would never have had
  Krokorok's card underneath it, so it could never reach back for
  `Tighten Up`. This deck's whole plan depends on evolving normally, so
  Rare Candy is excluded on purpose, not by oversight.
- **Bench-slot ceiling respected.** Only 6 Pokémon total can ever be in
  play (1 Active + 5 Bench). This deck runs 4 lines wanting board presence
  (Krookodile ex line, Relicanth, Dunsparce/Dudunsparce, Scraggy/Mega
  Scrafty ex) — earlier drafts ran a 5th (Toxtricity, then Purrloin/Liepard,
  then Team Rocket's Koffing/Weezing on top of these four), and the extra
  line was cut each time once bench math made clear it couldn't
  consistently find room.
- **Koffing/Weezing cut entirely** in favor of Scraggy/Mega Scrafty ex.
  Explicit tradeoff, not a strict upgrade: Koffing/Weezing solved "empty
  bench" (Smog Signals refills 2 free Basics on any hit, live from turn 1
  as a bare 70 HP Basic) but never actually survived a real attacker.
  Mega Scrafty ex solves "my attacker dies too fast" (330 HP + retaliation
  damage) but does nothing for an empty bench — if it goes down, board
  stays down, no auto-refill. It's also a bigger Prize risk: **Mega
  Evolution ex Pokémon give up 3 Prize cards on KO**, one more than a
  normal ex (Krookodile ex) and two more than Weezing.
- **Punk Helmet 1 -> 2, Buddy-Buddy Poffin 4 -> 3.** Tested all four
  Helmet/Poffin splits (1/4, 2/3, 3/2, 4/1) via `simulate_baseline.py`.
  Two things came out of it: Scraggy (ASC 134, 80 HP) is **not**
  Buddy-Buddy Poffin-eligible (over its 70-HP-or-less cutoff), so cutting
  Poffin copies never actually helps Scraggy show up faster — it only
  steadily costs Sandile/Dunsparce/Dudunsparce consistency for nothing in
  return. That cost is small and within noise at 2 Helmet/3 Poffin, but
  grows real at 3/2 and 4/1 (Dunsparce online-by-turn-6 drops from 88% to
  75% going from 4 Poffin down to 1). Landed on 2/3 as the balance point —
  it also covers the realistic ceiling on how many Punk Helmets matter at
  once: only one Pokémon is ever Active, and it stays attached once
  placed, so there's rarely a use for more than one per active Darkness
  threat-line (Krookodile ex line + Scraggy line = 2).
- **Dunsparce/Dudunsparce** is the draw-engine line, separate from the
  disruption plan — keeps the hand moving while the other three lines
  assemble. Its own consistency (~33-43% online by turn 6, varying with
  the Poffin count above) is a known, distinct weak point untouched by
  either the Koffing or Scraggy swap — worth a dedicated look if it's
  still not showing up in games.
- Verified with `check_energy_support.py`: mono-Darkness supply (13 Basic
  Darkness Energy + Enriching Energy) covers every attack in the deck.
  The one flag it raises is expected and intentional: Relicanth's
  `Razor Fin` needs Fighting Energy, which this deck runs none of —
  Relicanth is an Ability-only include and was never meant to attack with
  its own kit. (A genuine Darkness/Fighting hybrid was considered and
  explicitly rejected to avoid splitting the Energy base — see chat
  history for the Fighting-side card survey if that direction comes back
  up later.)
- Mulligan math: 12 effective Basics (Sandile, Relicanth, Dunsparce,
  Scraggy) -> 19.1% mulligan rate, unchanged from every prior version of
  this deck — none of the Koffing/Scraggy/Purrloin swaps have touched the
  Basic count.
- 60 cards, no card over 4 copies, no ACE SPEC in the deck.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Development-timing only — no retreating or opponent modeled, so this
measures how fast the pieces assemble, not win rate. It also can't score
Punk Helmet or Counterattacking Crest at all (Tools are out of scope, and
retaliation damage requires an opponent to hit something) — these numbers
only show board-development timing, not whether the deck actually holds
up in a real game:

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Sandile | 95.1% | 1.63 |
| Krokorok | 60.7% | 3.15 |
| Krookodile ex | 35.2% | 3.68 |
| Relicanth | 70.8% | 2.32 |
| Dunsparce | 85.3% | 1.95 |
| Dudunsparce | 39.7% | 3.48 |
| Scraggy | 64.8% | 2.05 |
| Mega Scrafty ex | 28.1% | 3.51 |

First attack landed by turn 6 in 92.2% of trials (avg turn 2.71). Average
final hand size at turn 6: 4.83 cards. Both big-HP payoffs (Krookodile ex,
Mega Scrafty ex) land in the 28-35% range by turn 6 — this deck now runs
two independent Stage-2-equivalent "finisher" lines on top of Relicanth
and the draw engine, four lines total, right at the bench-slot ceiling
discussed above.

## Pokémon TCG Live Import

```
Pokémon: 22
4 Sandile BLK 135
3 Krokorok BLK 136
3 Krookodile ex CRI 55
2 Relicanth TEF 173
3 Dunsparce TEF 128
2 Dudunsparce TEF 129
3 Scraggy ASC 134
2 Mega Scrafty ex ASC 135

Trainer: 24
4 Lillie's Determination MEG 119
1 Ultra Ball MEG 131
1 Boss's Orders MEG 114
4 Xerosic's Machinations SFA 64
2 Punk Helmet PFL 121
1 Air Balloon BLK 79
1 Rescue Board TEF 159
1 Night Stretcher MEG 173
2 Poké Pad ASC 198
1 Janine's Secret Art SFA 59
2 Team Rocket's Petrel ASC 207
3 Buddy-Buddy Poffin MEG 167
1 Energy Search POR 72

Energy: 14
13 Basic Darkness Energy
1 Enriching Energy SSP 191

Total Cards: 60
```
