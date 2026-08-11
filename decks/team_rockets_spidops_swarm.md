# Team Rocket's Spidops — Count-Swarm / Supporter-Discard Blend

Built from a full survey of every "Team Rocket's"-named Pokémon in the
pool (35+ cards, ranked by role before building — see chat history).
Blends the two strongest synergy axes found: `Rocket Rush`'s raw count
of Team Rocket's Pokémon in play, and a separate family of cards that
scale off Team Rocket's-named *Supporters* in hand/discard — both fed by
the same engine card, `Team Rocket's Petrel`.

## Centerpieces

1. **Team Rocket's Tarountula -> Spidops** (ASC 18 / ASC 19, 130 HP) —
   `Rocket Rush` (Grass+Colorless): 30 damage for **each** of your Team
   Rocket's Pokémon in play, Spidops itself included. `Charging Up`
   (Ability) re-attaches a Basic Energy from the discard pile each turn,
   free.
2. **Team Rocket's Kangaskhan ex** (ASC 162, 230 HP Basic ex, no
   evolution needed) — `Wicked Impact` (CCC): 120, +100 more if you
   played a Team Rocket's-named Supporter from hand this turn. A second,
   independent count-swarm-friendly attacker that doubles as a
   Supporter-discard payoff.
3. **Team Rocket's Murkrow -> Honchkrow** (ASC 126 / ASC 127) — Murkrow's
   `Deceit` (free) searches any Supporter; Honchkrow's `Rocket Feathers`
   (CC) discards any number of Team Rocket's Supporters from hand for 60
   damage each.
4. **Team Rocket's Porygon -> Porygon2 -> Porygon-Z** (DRI 153/154/155)
   — `R Command` (both Porygon2 and Porygon-Z) does 20 damage for each
   Team Rocket's Supporter **in your discard pile** — grows all game as
   Petrel gets used. Porygon-Z's Ability also draws a card per turn for
   2 discards.
5. **Team Rocket's Chingling** (DRI 85, 30 HP, standalone) — `Chiming
   Commotion`, **zero Energy cost**, discards a random card from the
   opponent's hand. Pure free value and pure count-padding in one card.
6. **Team Rocket's Meowth** (ASC 161, 70 HP, standalone) — `Paw-cket
   Pilfer`, also free, forces a random hand card face-up and shuffled
   away. Another free-value count-padder.

## Design notes

- **Bench math is inverted here on purpose.** Every other deck built
  this session stayed to 3-4 lines to respect the 6-slot ceiling; this
  deck's entire payoff *is* filling all 6 slots with distinct Team
  Rocket's Pokémon, so running 6 separate lines is the correct call, not
  an oversight.
- **Effectively mono-Grass Energy, no split.** Almost every real attack
  cost in this list is pure Colorless (Kangaskhan ex, Rocket Feathers,
  both R Commands, both free attacks) — only Spidops's own Rocket Rush
  needs a real type (1 Grass), and Colorless accepts any Energy, so
  11 Basic Grass Energy covers the whole deck. `check_energy_support.py`
  flags exactly two attacks as unpayable: Murkrow's `Torment` and
  Honchkrow's `Hammer In`, both needing Darkness — both are secondary
  attacks on Pokémon whose real jobs (Deceit, Rocket Feathers) don't
  need it, so this is intentional, same pattern as every other
  Ability-only/one-dead-attack include this session.
- **Team Rocket's Petrel is doing triple duty**: generic Trainer tutor,
  the discard-fuel for Porygon2/Porygon-Z's R Command, and the thing
  Kangaskhan ex's Wicked Impact checks for. Run at the max 4 copies for
  exactly that reason.
- **Precious Trolley** (ACE SPEC) is an excellent fit — 4 of the 6 lines
  start as Basics, and dumping several onto the Bench in one card
  directly serves the count-swarm plan.
- **Boss's Orders is safe here**, unlike the Arbok/Muk deck — Rocket
  Rush only cares about *your own* board, so there's no equivalent
  anti-synergy risk from gusting the opponent's Bench.
- Mulligan math: **16 effective Basics** (Tarountula, Kangaskhan ex,
  Murkrow, Porygon, Chingling, Meowth) -> **9.9%**, the lowest of any
  deck built this session — a direct, deliberate consequence of running
  6 distinct Basic lines instead of the usual 3-4.
- 60 cards, no card over 4 copies, one ACE SPEC.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Team Rocket's Tarountula | 94.4% | 1.55 |
| Team Rocket's Spidops | 52.2% | 3.29 |
| Team Rocket's Kangaskhan ex | 43.6% | 1.64 |
| Team Rocket's Murkrow | 78.4% | 1.80 |
| Team Rocket's Honchkrow | 38.8% | 3.52 |
| Team Rocket's Porygon | 70.0% | 1.73 |
| Team Rocket's Porygon2 | 34.9% | 3.50 |
| Team Rocket's Porygon-Z | 15.5% | 4.03 |
| Team Rocket's Chingling | 78.5% | 1.64 |
| Team Rocket's Meowth | 58.7% | 1.72 |

First attack landed by turn 6 in 88.6% of trials (avg turn 2.58). Average
final hand size: 4.35.

### The metric that actually matters for this deck: board count

Per-card online rates don't directly show what Rocket Rush cares about
(total Team Rocket's Pokémon simultaneously in play), so a separate
1000-trial run tracked that directly:

| Team Rocket's Pokémon in play, turn 6 | % of trials |
|---|---|
| 6 (max) | **84.5%** |
| 5 | 9.2% |
| 4 | 3.7% |
| 3 or fewer | 2.6% |

Average 5.75 simultaneous Team Rocket's Pokémon by turn 6 — meaning once
Spidops itself is down (52.2% of games by then), Rocket Rush is very
likely already near its 180-damage ceiling (30 x 6) for just 2 Energy.
The 3-stage Porygon-Z line is the slowest piece (15.5% by turn 6) but
isn't load-bearing for Rocket Rush itself — it's a separate payoff that
comes online later.

## Pokémon TCG Live Import

```
Pokémon: 24
4 Team Rocket's Tarountula ASC 18
2 Team Rocket's Spidops ASC 19
2 Team Rocket's Kangaskhan ex ASC 162
3 Team Rocket's Murkrow ASC 126
2 Team Rocket's Honchkrow ASC 127
2 Team Rocket's Porygon DRI 153
2 Team Rocket's Porygon2 DRI 154
2 Team Rocket's Porygon-Z DRI 155
3 Team Rocket's Chingling DRI 85
2 Team Rocket's Meowth ASC 161

Trainer: 25
4 Team Rocket's Petrel ASC 207
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Air Balloon BLK 79
2 Rescue Board TEF 159

Energy: 11
11 Basic Grass Energy

Total Cards: 60
```
