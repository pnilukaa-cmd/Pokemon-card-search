# Team Rocket's Persian ex — Attack Theft (full-toolkit rebuild)

Built around a specific request: punish opponents running strong Pokémon
by stealing their own attacks. Rebuilt after a full survey of all 12
Team Rocket's-named Trainers turned up an engine the first version
missed entirely (Proton, Ariana, Transceiver, Factory), plus two
payoffs that reward leaning into the tribe — `Wicked Impact` and
`Rocket Rush`.

## Centerpiece

**Team Rocket's Meowth -> Persian ex** (ASC 161 / DRI 150, 260 HP) —
`Haughty Order` (Colorless+Colorless): *reveal the top 10 cards of your
opponent's deck, choose an attack from a Pokémon you find there, and use
it as this attack.* Pure Colorless cost, so it never needs a specific
Energy type. Against a deck built on one or two big attackers, this
borrows their best attack regardless of what it costs on their own card.
Backup: `Cruel Slash` (CCC, 140 + Confuse) for when the reveal comes up
dry.

## The three engines this rebuild adds

**1. Team Rocket's Supporter payoffs.** Every "Team Rocket"-named
Supporter you play is worth more than its own text here:
- **Team Rocket's Kangaskhan ex** (ASC 162, 230 HP Basic — no evolution
  needed) — `Wicked Impact` (CCC): 120, **+100 more if you played a
  "Team Rocket" Supporter from hand this turn**. With 10 such Supporters
  in the deck this is live most turns.
- **Team Rocket's Factory** (ASC 203, Stadium) — draw 2 on the same
  trigger.
- **Team Rocket's Transceiver** (ASC 209, Item) — searches a "Team
  Rocket" Supporter, so it both finds the payoff trigger and thins toward
  it.

**2. Board-count payoff.** **Team Rocket's Tarountula -> Spidops**
(ASC 18/19) — `Rocket Rush` (Grass+Colorless): 30 damage **per Team
Rocket's Pokémon in play**. Since every Pokémon in this deck is Team
Rocket's-named, this scales off the whole board. Spidops's `Charging Up`
Ability also re-attaches a Basic Energy from the discard each turn, free.

**3. The Ability lock.** **Team Rocket's Ekans -> Arbok** (DRI 112/113,
130 HP) — Ability `Potent Glare`: *while this Pokémon is in the Active
Spot, your opponent can't play any Pokémon that has an Ability from
their hand* (except Team Rocket's ones). This is a genuine soft-lock
aimed squarely at Ability-engine decks — N's Zoroark ex's whole draw
engine is its `Trade` Ability, so parking Arbok Active shuts off their
ability to deploy more of them from hand. **Potent Glare costs no
Energy** — Arbok can hold the lock indefinitely without ever attacking,
which is why the deck runs no Darkness Energy for its `Spinning Tail`.

## The Supporter engine, in curve order

- **Team Rocket's Proton** (ASC 208) — search **3 Basic Team Rocket's
  Pokémon** to hand, and it is **legal on your first turn going first**,
  unlike most Supporters. The single best turn-1 play in the deck.
- **Team Rocket's Ariana** (ASC 202) — draw to 5, or **draw to 8 if every
  Pokémon you have in play is Team Rocket's**. Every Pokémon in this
  list is Team Rocket's-named specifically so this is always the 8-card
  mode. **This is the real reason not to splash a generic tech Pokémon
  here** — a single non-Team-Rocket's body on the board silently
  downgrades Ariana to draw-to-5.
- **Team Rocket's Petrel** (ASC 207) x4 — searches any Trainer, so it
  finds Transceiver, Factory, Poffin, or another Supporter as needed.
- **Team Rocket's Giovanni** (ASC 204) — switches your Active Team
  Rocket's Pokémon **and** gusts one of their Benched up. A real
  two-for-one: bring Arbok up to establish the lock while simultaneously
  dragging their weak Pokémon into the Active Spot.

## Design notes

- **Energy is Grass-forward, not Psychic/Darkness.** This is the
  significant change from the first version. Almost every attack here is
  pure Colorless (Persian ex, Kangaskhan ex, Chingling is free), and
  Spidops's `Rocket Rush` is the only cost needing a real type — Grass.
  Basic Grass Energy pays for both, so 8 Grass covers the whole deck.
  **Team Rocket's Energy** (ASC 217) stays at 4 because it provides *2*
  Energy at a time to a Team Rocket's Pokémon, which is exactly what the
  Colorless-cost attackers want.
- Verified with `check_energy_support.py`: no shortfalls anywhere, 60
  cards, no card over 4 copies, one ACE SPEC (`Precious Trolley`).
- Mulligan math: **13 effective Basics** (Meowth, Kangaskhan ex,
  Tarountula, Ekans, Chingling) -> **16.3%**.
- 4 of the 5 Basics are 70 HP or under, so **Buddy-Buddy Poffin** at 4
  copies is genuinely live (Kangaskhan ex at 230 HP is the only one it
  can't fetch).
- **Boss's Orders is safe here** — nothing about this plan cares what the
  opponent's board looks like, unlike the Arbok/Muk deck's real
  anti-synergy with it.
- **Considered and cut for bench pressure**: Honchkrow (`Rocket
  Feathers`, discard Team Rocket's Supporters for 60 each) and the
  Porygon/Porygon2/Porygon-Z line (`R Command`, 20x per Team Rocket's
  Supporter in the discard pile). Both are real Supporter-count payoffs,
  but Honchkrow *discards* the Supporters this deck would rather play
  (turning off Wicked Impact and Factory), and Porygon-Z is a full
  Stage 2 line competing for slots with Persian ex, Spidops, and Arbok.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Proton, Ariana, and Transceiver were added to the simulator's effect
registry for this build, so these numbers reflect the real engine rather
than treating it as a blind spot:

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Team Rocket's Meowth | 95.3% | 1.44 |
| Team Rocket's Persian ex | 61.6% | 3.22 |
| Team Rocket's Kangaskhan ex | 56.0% | 1.80 |
| Team Rocket's Tarountula | 91.7% | 1.61 |
| Team Rocket's Spidops | 52.6% | 3.28 |
| Team Rocket's Ekans | 75.2% | 1.73 |
| Team Rocket's Arbok | 39.0% | 3.49 |
| Team Rocket's Chingling | 71.7% | 1.75 |

First attack landed by turn 6 in 87.4% of trials (avg turn 2.72).
Average final hand size: 4.37.

### Board count — what Rocket Rush actually scales off

| Team Rocket's Pokémon in play, turn 6 | % of trials | Rocket Rush damage |
|---|---|---|
| 6 (max) | **86.6%** | 180 |
| 5 | 6.9% | 150 |
| 4 | 4.2% | 120 |
| 3 or fewer | 2.3% | ≤90 |

Average 5.77 simultaneous Team Rocket's Pokémon by turn 6 — so whenever
Spidops is online (52.6% by then), Rocket Rush is almost always at or
near its 180 ceiling for just 2 Energy.

As always: no retreating and no opponent are modeled, so this measures
how fast the engine assembles, not whether Potent Glare's lock or
Haughty Order's theft actually win games.

## Pokémon TCG Live Import

```
Pokémon: 20
4 Team Rocket's Meowth ASC 161
3 Team Rocket's Persian ex DRI 150
2 Team Rocket's Kangaskhan ex ASC 162
3 Team Rocket's Tarountula ASC 18
2 Team Rocket's Spidops ASC 19
2 Team Rocket's Ekans DRI 112
2 Team Rocket's Arbok DRI 113
2 Team Rocket's Chingling DRI 85

Trainer: 28
4 Team Rocket's Petrel ASC 207
2 Team Rocket's Proton ASC 208
3 Team Rocket's Ariana ASC 202
1 Team Rocket's Giovanni ASC 204
2 Team Rocket's Transceiver ASC 209
2 Team Rocket's Factory ASC 203
4 Buddy-Buddy Poffin MEG 167
3 Ultra Ball MEG 131
1 Precious Trolley SSP 185
2 Night Stretcher MEG 173
2 Air Balloon BLK 79
2 Boss's Orders MEG 114

Energy: 12
4 Team Rocket's Energy ASC 217
8 Basic Grass Energy

Total Cards: 60
```
