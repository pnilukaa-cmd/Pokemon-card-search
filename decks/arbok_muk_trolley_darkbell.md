# Arbok / Team Rocket's Muk — Precious Trolley + Dark Bell variant

One of two sibling variants branching from `arbok_team_rockets_muk_condition_stack.md`
after adding `Dark Bell` and testing the ACE SPEC slot (`Precious Trolley`
vs `Dangerous Laser`) head to head. This is the **Trolley** branch — see
`arbok_muk_laser_darkbell.md` for the other. Same Pokémon core as the
original (Ekans/Arbok, Venipede/Whirlipede, Team Rocket's Grimer/Muk); the
change is entirely in the Trainer line.

## What changed from the original build

- **+3 Dark Bell** (PBL 106, Item): *"Both Active non-Darkness Pokémon
  are now Confused."* Since this whole deck is mono-Darkness, your own
  Active is immune to its own effect — functionally a free, guaranteed
  Confuse on the opponent (barring a mirror match), no attack or Energy
  needed.
- **Ultra Ball 3 -> 4**, and **Air Balloon / Rescue Board both 4 -> 2**
  to make room. This alone measurably helped board development in
  testing, independent of Dark Bell.
- **Kept Precious Trolley** as the ACE SPEC (search any number of Basic
  Pokémon onto the Bench) rather than switching to Dangerous Laser.

## Why Trolley over Dangerous Laser here — the real tradeoff

Both are legitimate; this is the higher-consistency pick. Precious
Trolley is a modeled, measurable board-development boost (see the sim
table below). Dangerous Laser (Burn + Confused on the opponent's Active,
guaranteed, no attack needed) would let Dark Bell + Whirlipede's Poison
Ring cover all 3 stackable Special Conditions and the retreat-lock
without ever needing Arbok's own turn — a real de-risking of the kill
sequence that this simulator can't score, since it has no opponent board
to apply Special Conditions to. Trolley wins on raw consistency; Laser
wins on reducing how much has to go right to land Hazardous Venom. Pick
based on whether you'd rather have a faster board or a shorter combo
chain — see `arbok_muk_laser_darkbell.md` for that version.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Ekans | 98.1% | 1.44 |
| Arbok | 68.2% | 3.18 |
| Venipede | 95.1% | 1.71 |
| Whirlipede | 53.4% | 3.50 |
| Team Rocket's Grimer | 82.1% | 1.90 |
| Team Rocket's Muk | 42.0% | 3.76 |

First attack landed by turn 6 in 94.4% of trials (avg turn 2.65). Average
final hand size at turn 6: 3.54. All figures improved over the original
saved build (e.g. Arbok 62.2% -> 68.2%, Muk 39.2% -> 42.0%) — most of
that gain traces to the extra Ultra Ball, not Dark Bell itself (Dark Bell
scores as zero-effect here, correctly, since its whole effect targets a
board this simulator doesn't model).

Verified with `check_energy_support.py`: 60 cards, no card over 4
copies, ACE SPEC within limit, mono-Darkness Energy covers every attack
with no shortfalls. Mulligan math unchanged from the original build (11
effective Basics -> 22.2%), since the Pokémon line didn't change.

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
1 Precious Trolley SSP 185
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
