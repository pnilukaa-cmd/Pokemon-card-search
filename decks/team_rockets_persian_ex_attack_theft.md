# Team Rocket's Persian ex — Attack Theft

Built around a specific request: a deck that punishes opponents running
strong Pokémon by stealing their own attacks against them, backed by a
Psychic/Darkness Team Rocket's support core fed by Team Rocket's Energy.

## Centerpiece

**Team Rocket's Meowth -> Persian ex** (ASC 161 / DRI 150, 260 HP) —
`Haughty Order` (Colorless+Colorless, no fixed damage): *reveal the top
10 cards of your opponent's deck, choose an attack from a Pokémon you
find there, and use it as this attack.* Pure Colorless cost — it doesn't
need Team Rocket's Energy or any specific type to fire. Against a deck
built around one or two big attackers, this can borrow their own best
attack and use it against them, no matter what it costs on their card.
Backup attack `Cruel Slash` (Colorless+Colorless+Colorless, 140 dmg):
guaranteed Confuse, reliable when Haughty Order doesn't find anything
worth taking.

## Support core — why Team Rocket's Energy matters here

Persian ex itself needs no specific type, so **Team Rocket's Energy**
(ASC 217: provides 2 Energy in any combination of Psychic/Darkness, but
only attaches to Team Rocket's Pokémon) is doing its work on the rest of
the roster instead:

- **Team Rocket's Mewtwo ex** (ASC 281, 280 HP, Psychic) — `Erasure
  Ball` (Psychic+Psychic+Colorless): 160, up to +120 more by discarding
  Bench Energy. Its Ability, `Power Saver` ("can't attack unless you
  have 4+ Team Rocket's Pokémon in play"), was flagged as a real trap in
  a different, non-tribal deck earlier in this project — here it's a
  non-issue, since **every single Pokémon in this decklist is Team
  Rocket's-named**.
- **Team Rocket's Zubat -> Golbat -> Crobat ex** (DRI 120/121/122,
  Darkness) — Zubat's `Poison Spray` and Golbat's `Confuse Ray` are
  cheap, guaranteed early disruption; Crobat ex (310 HP) can return
  itself to hand after attacking via `Assassin's Return`, protecting a
  big investment from retaliation.
- **Team Rocket's Chingling** (DRI 85, 30 HP) — `Chiming Commotion`,
  zero Energy cost, discards a random card from the opponent's hand.
  Pure free value and cheap board count.

## Design notes

- Real Psychic/Darkness split, softened by Team Rocket's Energy's
  flexibility: 4 Team Rocket's Energy + 5 Basic Psychic + 5 Basic
  Darkness = 14 total, verified with `check_energy_support.py` to cover
  Mewtwo ex's double-Psychic and Crobat ex's double-Darkness
  requirements with no shortfalls.
- **Team Rocket's Petrel (x4) + Team Rocket's Transceiver (x2) +
  Team Rocket's Factory (x1)** form the same search-and-draw chain
  found while ranking the full Team Rocket's roster earlier: Transceiver
  fetches a "Team Rocket"-named Supporter (only Petrel qualifies here),
  Petrel fetches any Trainer, and Factory draws 2 more if a Team
  Rocket's Supporter was played from hand that turn — one Trainer play
  can chain into two more actions.
- **Precious Trolley** (ACE SPEC) fits well — 3 of the 4 Pokémon lines
  start as Basics.
- **Boss's Orders is safe here** — Persian ex's plan doesn't care what
  the opponent's board looks like, so there's no equivalent to the
  Arbok/Muk deck's anti-synergy with it.
- Mulligan math: 12 effective Basics (Meowth, Mewtwo ex, Zubat,
  Chingling) -> 19.1%.
- Bench-slot math: 4 lines (Meowth/Persian ex, Mewtwo ex standalone,
  Zubat/Golbat/Crobat ex, Chingling standalone) — the usual ceiling for
  a combo-focused build.
- 60 cards, no card over 4 copies, one ACE SPEC.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Team Rocket's Meowth | 96.7% | 1.47 |
| Team Rocket's Persian ex | 62.9% | 3.20 |
| Team Rocket's Mewtwo ex | 60.0% | 1.95 |
| Team Rocket's Zubat | 90.5% | 1.72 |
| Team Rocket's Golbat | 56.2% | 3.41 |
| Team Rocket's Crobat ex | 29.4% | 4.16 |
| Team Rocket's Chingling | 89.6% | 1.73 |

First attack landed by turn 6 in 90.4% of trials (avg turn 2.62). Average
final hand size: 3.90. Crobat ex, the deepest investment (Stage 2), is
predictably the slowest piece at 29.4% — Persian ex and Mewtwo ex are
both real, faster options for whenever it isn't out yet.
`Team Rocket's Transceiver`'s search effect isn't modeled (only Petrel's
search is currently in the registry) — a disclosed gap, not a flaw in
the card.

## Pokémon TCG Live Import

```
Pokémon: 19
4 Team Rocket's Meowth ASC 161
3 Team Rocket's Persian ex DRI 150
2 Team Rocket's Mewtwo ex ASC 281
3 Team Rocket's Zubat DRI 120
2 Team Rocket's Golbat DRI 121
2 Team Rocket's Crobat ex DRI 122
3 Team Rocket's Chingling DRI 85

Trainer: 27
4 Team Rocket's Petrel ASC 207
2 Team Rocket's Transceiver ASC 209
1 Team Rocket's Factory ASC 203
4 Buddy-Buddy Poffin MEG 167
3 Ultra Ball MEG 131
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Switch MEG 130
2 Air Balloon BLK 79

Energy: 14
4 Team Rocket's Energy ASC 217
5 Basic Psychic Energy
5 Basic Darkness Energy

Total Cards: 60
```
