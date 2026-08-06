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
  play (1 Active + 5 Bench). This deck runs 4 lines wanting board
  presence (Krookodile ex line, Relicanth, Purrloin/Liepard,
  Dunsparce/Dudunsparce) — an earlier draft also ran Toxtricity as a
  fifth, and was cut once the bench math made clear a 5th permanent line
  couldn't consistently find room alongside the other four.
- **Purrloin/Liepard and Dunsparce/Dudunsparce** are secondary Darkness
  support and a draw engine, respectively — not additional disruption
  pieces, but they round out the curve and keep the hand moving while the
  Krookodile ex line assembles.
- Verified with `check_energy_support.py`: mono-Darkness supply (13 Basic
  Darkness Energy + Enriching Energy) covers every attack in the deck.
  The one flag it raises is expected and intentional: Relicanth's
  `Razor Fin` needs Fighting Energy, which this deck runs none of —
  Relicanth is an Ability-only include and was never meant to attack with
  its own kit.
- Mulligan math: 12 effective Basics (Sandile, Relicanth, Purrloin,
  Dunsparce) -> 19.1% mulligan rate.
- 60 cards, no card over 4 copies, no ACE SPEC in the deck.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Development-timing only — no retreating or opponent modeled, so this
measures how fast the pieces assemble, not win rate:

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Sandile | 95.5% | 1.60 |
| Krokorok | 63.0% | 3.18 |
| Krookodile ex | 34.9% | 3.77 |
| Relicanth | 68.0% | 2.23 |
| Purrloin | 86.3% | 1.92 |
| Liepard | 43.2% | 3.55 |
| Dunsparce | 83.1% | 1.77 |
| Dudunsparce | 38.6% | 3.46 |

First attack landed by turn 6 in 95.5% of trials (avg turn 2.58, almost
always Sandile's or Dunsparce's own Basic-level attack going first while
the real engine is still assembling). Average final hand size at turn 6:
4.68 cards. Full Krookodile ex line online only ~35% of the time by turn
6 — consistent with running two independent lines (the evolution line and
Relicanth) with no dedicated acceleration piece connecting them; this is
the same "hard to get ramped up" read the deck already carried into this
build, now with a number attached to it.

## Pokémon TCG Live Import

```
Pokémon: 22
4 Sandile BLK 135
3 Krokorok BLK 136
3 Krookodile ex CRI 55
2 Relicanth TEF 173
3 Purrloin WHT 136
2 Liepard WHT 137
3 Dunsparce TEF 128
2 Dudunsparce TEF 129

Trainer: 24
4 Lillie's Determination MEG 119
1 Ultra Ball MEG 131
1 Boss's Orders MEG 114
4 Xerosic's Machinations SFA 64
1 Punk Helmet PFL 121
1 Air Balloon BLK 79
1 Rescue Board TEF 159
1 Night Stretcher MEG 173
2 Poké Pad ASC 198
1 Janine's Secret Art SFA 59
2 Team Rocket's Petrel ASC 207
4 Buddy-Buddy Poffin MEG 167
1 Energy Search POR 72

Energy: 14
13 Basic Darkness Energy
1 Enriching Energy SSP 191

Total Cards: 60
```
