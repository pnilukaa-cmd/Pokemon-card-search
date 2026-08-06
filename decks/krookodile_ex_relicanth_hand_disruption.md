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
3. **Team Rocket's Koffing -> Team Rocket's Weezing** (DRI 125 / DRI 126)
   — added after real playtesting surfaced "getting knocked out early with
   an empty bench" as the deck's actual weak point (Purrloin/Liepard
   didn't fix that and were cut). Koffing's Ability, Smog Signals: *"If
   this Pokémon is in the Active Spot and is damaged by an attack (even if
   Knocked Out), search your deck for up to 2 Pokémon that have 'Koffing'
   in their name and put them onto your Bench."* Every hit it takes,
   lethal or not, refills the bench for free instead of leaving it empty.
   Weezing's `Explode Together Now` (Darkness + Colorless) does 40 damage
   for each Koffing/Weezing in play on *either* side, so it directly
   scales off Smog Signals' own refills — a real payoff, not just a
   defensive stopgap. Both run on the same mono-Darkness Energy base as
   the rest of the deck.

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
  (Krookodile ex line, Relicanth, Dunsparce/Dudunsparce, Koffing/Weezing)
  — an earlier draft ran 5 (Toxtricity, then later Purrloin/Liepard on top
  of these four), and both extra lines were cut once it became clear a 5th
  permanent line couldn't consistently find room.
- **Purrloin/Liepard cut entirely** (previously ran 3/2) after real
  playtesting showed the deck getting knocked out early with nothing on
  the bench — Liepard's `Knock Off` wasn't essential, and Purrloin's
  search wasn't fixing the actual problem. Team Rocket's Koffing/Weezing
  replaced them specifically because Smog Signals answers that exact
  complaint (empty bench on a KO) instead of a generic consistency boost
  that didn't touch it. Buddy-Buddy Poffin was already at its legal
  4-copy max, so the fix was adding more Poffin-*eligible* targets
  (Koffing is a 70 HP Basic, well within Poffin's 70-HP-or-less limit)
  rather than more Poffin copies.
- **Dunsparce/Dudunsparce** is the draw-engine line, separate from the
  disruption plan — keeps the hand moving while the other three lines
  assemble. Its own consistency (~35-40% online by turn 6) is a known,
  distinct weak point not touched by the Koffing swap — worth a dedicated
  look if it's still not showing up in games.
- Verified with `check_energy_support.py`: mono-Darkness supply (13 Basic
  Darkness Energy + Enriching Energy) covers every attack in the deck.
  The one flag it raises is expected and intentional: Relicanth's
  `Razor Fin` needs Fighting Energy, which this deck runs none of —
  Relicanth is an Ability-only include and was never meant to attack with
  its own kit.
- Mulligan math: 12 effective Basics (Sandile, Relicanth, Dunsparce, Team
  Rocket's Koffing) -> 19.1% mulligan rate, unchanged from the
  Purrloin/Liepard build — dropping Purrloin to zero (rather than trimming
  it) traded away the small mulligan improvement a partial trim would have
  given, in exchange for the extra Koffing/Weezing slots. Worth knowing
  this is a real tradeoff, not a free upgrade.
- 60 cards, no card over 4 copies, no ACE SPEC in the deck.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Development-timing only — no retreating or opponent modeled, so this
measures how fast the pieces assemble, not win rate. It also can't show
Smog Signals actually *paying off* (it only refills the bench once
something damages Koffing) — it can only confirm Koffing shows up early
and reliably; whether it saves games is a real-match question this tool
doesn't answer:

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Sandile | 95.6% | 1.62 |
| Krokorok | 64.6% | 3.11 |
| Krookodile ex | 37.3% | 3.71 |
| Relicanth | 68.1% | 2.21 |
| Dunsparce | 84.2% | 1.90 |
| Dudunsparce | 39.6% | 3.40 |
| Team Rocket's Koffing | 82.4% | 1.82 |
| Team Rocket's Weezing | 39.6% | 3.34 |

First attack landed by turn 6 in 94.1% of trials (avg turn 2.66). Average
final hand size at turn 6: 4.64 cards. Krookodile ex and Dudunsparce
numbers are essentially unchanged from the Purrloin/Liepard build
(~35-39% either way) — this swap targeted the empty-bench problem
specifically, not the Krookodile ex line's own ramp speed.

## Pokémon TCG Live Import

```
Pokémon: 22
4 Sandile BLK 135
3 Krokorok BLK 136
3 Krookodile ex CRI 55
2 Relicanth TEF 173
3 Dunsparce TEF 128
2 Dudunsparce TEF 129
3 Team Rocket's Koffing DRI 125
2 Team Rocket's Weezing DRI 126

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
