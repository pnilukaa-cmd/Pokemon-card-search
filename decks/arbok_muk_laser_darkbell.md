# Arbok / Team Rocket's Muk — Dangerous Laser + Dark Bell variant

The other of two sibling variants branching from
`arbok_team_rockets_muk_condition_stack.md` — see
`arbok_muk_trolley_darkbell.md` for the Precious Trolley branch. Same
Pokémon core (Ekans/Arbok, Venipede/Whirlipede, Team Rocket's
Grimer/Muk); the ACE SPEC slot is the one real difference between the
two files.

## What changed from the original build

- **+3 Dark Bell** (PBL 106, Item): *"Both Active non-Darkness Pokémon
  are now Confused."* Mono-Darkness deck, so this only ever lands on the
  opponent — free, guaranteed Confuse, no attack or Energy needed.
- **ACE SPEC swapped: Precious Trolley -> Dangerous Laser** (SFA 58):
  *"Your opponent's Active Pokémon is now Burned and Confused."* Two of
  the three stackable Special Conditions, guaranteed, straight from an
  Item card — no Pokémon attack required. Paired with Whirlipede's
  `Poison Ring` (Poison + retreat-lock, also guaranteed), that's all 3
  conditions and the lock from just two cards, without ever needing
  Arbok's own turn to fire `Panic Poison`. Shortens the actual kill
  sequence for Team Rocket's Muk's `Hazardous Venom`.
- **Ultra Ball 3 -> 4**, **Air Balloon / Rescue Board both 4 -> 2** —
  same trim as the Trolley variant, made room for both changes above.

## Why this version over the Trolley one — and the real cost

This version doesn't build the board as fast (see the sim numbers below,
which are worse across the line than the Trolley variant) — Dangerous
Laser doesn't put any Pokémon into play, so it can't help board
development the way Precious Trolley's "search any number of Basics to
Bench" does. What it buys instead is real but **can't be shown by this
simulator**: removing 2 of the 3 needed conditions from ever requiring an
attack means a thinner board can still land the full combo, since
Dangerous Laser + Whirlipede alone cover everything Hazardous Venom
needs. The simulator has no opponent board to apply Special Conditions
to, so it can only score what it can see — Trolley's board-development
edge is real and measured; Dangerous Laser's combo-derisking edge is real
and unmeasured. Don't read the numbers below as this version being worse
overall, only slower to assemble a board.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Ekans | 97.8% | 1.50 |
| Arbok | 59.9% | 3.30 |
| Venipede | 90.0% | 1.88 |
| Whirlipede | 47.6% | 3.60 |
| Team Rocket's Grimer | 79.1% | 2.03 |
| Team Rocket's Muk | 37.9% | 3.53 |

First attack landed by turn 6 in 93.2% of trials (avg turn 2.68). Average
final hand size at turn 6: 3.61. Dangerous Laser and Dark Bell both score
as zero-effect in this table — correctly, per the reasoning above, not
because they're weak cards.

Verified with `check_energy_support.py`: 60 cards, no card over 4
copies, ACE SPEC within limit, mono-Darkness Energy covers every attack
with no shortfalls. Mulligan math unchanged from the original build (11
effective Basics -> 22.2%).

## Pokémon TCG Live Import

```
Pokémon: 17
4 Ekans TEF 100
2 Arbok TEF 101
4 Venipede TWM 115
2 Whirlipede TWM 116
3 Team Rocket's Grimer DRI 123
2 Team Rocket's Muk DRI 124

Trainer: 30
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Dangerous Laser SFA 58
4 Lillie's Determination MEG 119
2 Janine's Secret Art SFA 59
4 Team Rocket's Petrel ASC 207
4 Night Stretcher MEG 173
2 Air Balloon BLK 79
2 Rescue Board TEF 159
3 Dark Bell PBL 106

Energy: 13
13 Basic Darkness Energy

Total Cards: 60
```
