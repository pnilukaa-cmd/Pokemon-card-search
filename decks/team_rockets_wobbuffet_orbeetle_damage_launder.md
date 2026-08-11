# Team Rocket's Wobbuffet / Orbeetle Damage-Laundering Control

A different shape than every other deck built this session: instead of
applying Special Conditions or scaling off a count, this one turns
**damage your own Pokémon take** into offense. Found while ranking the
full Team Rocket's roster — flagged then as "a real 2-card combo," built
out here.

## The engine

- **Team Rocket's Orbeetle** (DRI 198, 130 HP, Stage 2) — Ability
  `Rocket Brain`: *"As often as you like during your turn, you may move
  1 damage counter from 1 of your Team Rocket's Pokémon to another of
  your Pokémon."* No "must be Active" restriction — confirmed directly
  against the card text before building around it, since that clause is
  exactly the kind of thing worth checking rather than assuming. Usable
  from the Bench, unlimited times per turn.
- **Team Rocket's Wobbuffet** (DRI 82, 110 HP, Basic, no evolution) —
  `Rocket Mirror` (Psychic+Colorless): *"Move all damage counters from 1
  of your Benched Team Rocket's Pokémon to your opponent's Active
  Pokémon."*

## The actual turn sequence, walked out — not just asserted

1. **Wobbuffet sits Active and takes hits** over several of the
   opponent's turns, accumulating damage counters normally.
2. **Each of your turns, Orbeetle (from the Bench) sweeps those counters
   off Wobbuffet onto a third Pokémon** — a "battery," any other Team
   Rocket's Pokémon sitting on your Bench. This simultaneously **heals
   Wobbuffet** (damage counters removed = effective HP restored) and
   **loads the battery** with ammo. Repeat turn after turn; there's no
   per-turn cap on Rocket Brain, so a single turn can sweep everything
   Wobbuffet has accumulated in one go.
3. **On the turn you want to cash in**: use Rocket Brain one last time to
   top off the battery, *then* attack with Wobbuffet's `Rocket Mirror` to
   dump the battery's entire accumulated damage-counter total onto the
   opponent's Active in one shot — for just 1 Psychic Energy. Using the
   Ability doesn't consume your one attack for the turn, so both happen
   on the same turn.

## The real vulnerability — named plainly, not glossed over

The loaded battery is a Bench Pokémon sitting there holding a large,
visible pile of stored damage. **Any bench-snipe effect the opponent has
(several exist in this format — cards that deal damage directly to a
Benched Pokémon) can simply knock it out before you cash in**, destroying
everything stored on it with no compensation — Rocket Mirror only works
on a Benched Team Rocket's Pokémon that's still alive. This isn't
something the deck can fully protect against; it's a genuine soft spot to
play around (don't over-load a single battery past what it can survive,
and consider cashing in before the pile gets too tempting a target).

## Why the baseline simulator can't validate this deck's actual plan

Every other deck built this session got at least partial signal from
`simulate_baseline.py` on its core mechanic. This one doesn't — the
combo depends entirely on the opponent damaging your Pokémon, and this
simulator has **no opponent at all**, by design (same stated
simplification as `simulate_match.py`). It can tell you how fast
Wobbuffet, Orbeetle, and the rest show up on board; it cannot tell you
whether the damage-laundering loop, the healing side-benefit, or the
eventual burst actually plays out well in a real game. Treat the table
below as "can this deck assemble its pieces," not "does the combo work."

## Design notes

- **Team Rocket's Exeggcute -> Exeggutor** is the backup plan and a real
  attacker in its own right: `Double-Edge` (Psychic+C+C, 150 dmg) also
  does 30 guaranteed self-damage — a proactive, controllable damage
  source for the Orbeetle engine that doesn't require waiting on the
  opponent, on top of just being a strong attack on its own.
- **Team Rocket's Chingling** (30 HP, free `Chiming Commotion`) serves
  double duty here: free hand disruption if it ever attacks, and a cheap,
  disposable battery candidate — low HP means it holds less before
  dying, but it's also the least costly piece to risk losing to a
  bench-snipe.
- Mono-Psychic Energy, no split — every real attack cost in the deck
  (Rocket Mirror, Orbeetle's own `Psychic`, Exeggutor's `Double-Edge`,
  Dottler's `Super Psy Bolt`) needs Psychic or is Colorless-only.
  `check_energy_support.py`: 12 Basic Psychic Energy, no shortfalls, 60
  cards, no card over 4 copies, one ACE SPEC.
- **Boss's Orders is safe here**, same reasoning as the Spidops deck —
  nothing about this combo cares what the opponent's board looks like,
  so there's no equivalent anti-synergy risk.
- Mulligan math: 12 effective Basics (Blipbug, Wobbuffet, Exeggcute,
  Chingling) -> 19.1%.
- Bench-slot math: 4 lines (Blipbug/Dottler/Orbeetle,
  Wobbuffet, Exeggcute/Exeggutor, Chingling) — the usual ceiling for a
  combo-focused build this session, not a swarm build like the Spidops
  deck.

## Baseline simulation (1000 trials, `simulate_baseline.py`) — development timing only

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Team Rocket's Blipbug | 94.6% | 1.64 |
| Team Rocket's Dottler | 58.3% | 3.40 |
| Team Rocket's Orbeetle | 24.2% | 4.13 |
| Team Rocket's Wobbuffet | 81.6% | 1.92 |
| Team Rocket's Exeggcute | 87.1% | 1.81 |
| Team Rocket's Exeggutor | 46.1% | 3.46 |
| Team Rocket's Chingling | 87.4% | 1.65 |

First attack landed by turn 6 in 87.6% of trials (avg turn 2.54). Average
final hand size: 4.25. **The real weak point this table does show**:
Orbeetle — the piece the whole engine depends on — is only online by
turn 6 in 24.2% of games, the slowest of any piece in this deck. Since
the combo doesn't function at all without Orbeetle in play, this is
worth taking seriously even though the combo's *payoff* itself can't be
simulated — its *setup speed* can be, and it's slow.

## Pokémon TCG Live Import

```
Pokémon: 18
3 Team Rocket's Blipbug DRI 15
2 Team Rocket's Dottler DRI 88
2 Team Rocket's Orbeetle DRI 198
3 Team Rocket's Wobbuffet DRI 82
3 Team Rocket's Exeggcute ASC 77
2 Team Rocket's Exeggutor ASC 78
3 Team Rocket's Chingling DRI 85

Trainer: 30
4 Team Rocket's Petrel ASC 207
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 119
3 Boss's Orders MEG 114
4 Night Stretcher MEG 173
2 Air Balloon BLK 79
2 Rescue Board TEF 159
2 Switch MEG 130

Energy: 12
12 Basic Psychic Energy

Total Cards: 60
```
