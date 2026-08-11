# Arbok / Team Rocket's Muk Condition Stack (Pure Darkness)

Replaces an earlier Fire/Darkness draft (Salazzle ex + Team Rocket's Muk)
with an all-Darkness version once research turned up a strictly stronger,
type-clean core: `Arbok` alone hits the 3-condition, 300-damage ceiling
on Team Rocket's Muk's `Hazardous Venom`, and `Whirlipede` closes the
retreat-escape gap that the Salazzle version couldn't — both native
Darkness, no Energy split required.

## Centerpieces

1. **Ekans -> Arbok** (TEF 100 / TEF 101, 130 HP) — `Panic Poison` (1
   Darkness, 0 base dmg): Burned, Confused, **and** Poisoned, all three,
   guaranteed, no coin flip. One card hits the real ceiling — only one of
   Asleep/Confused/Paralyzed can affect a Pokémon at a time, so 3 total
   Special Conditions is the actual maximum, not something more stacking
   pushes past.
2. **Venipede -> Whirlipede** (TWM 115 / TWM 116, 100 HP) — `Poison Ring`
   (1 Darkness): Poisoned **and** the opponent can't retreat during their
   next turn, guaranteed. This is the fix for the escape hatch: it locks
   exactly the one opponent turn that sits between your setup and Team
   Rocket's Muk's cash-in turn, so there's no window left for them to
   retreat away and clear everything for free.
3. **Team Rocket's Grimer -> Team Rocket's Muk** (DRI 123 / DRI 124,
   150 HP) — `Hazardous Venom` (Darkness+Darkness+Colorless): 100 damage
   per Special Condition on the opponent's Active. With Arbok's 3 already
   down (and Whirlipede's lock making sure they're still down), this is a
   deterministic 300, not a conditional bonus.

## A real anti-synergy, not simulator-testable — found by reading the cards, not running trials

**Boss's Orders is cut entirely from this build.** It gusts one of the
opponent's *Benched* Pokémon into the Active Spot — which, applied here,
would drag a completely fresh, condition-free target into the spot
Hazardous Venom is aimed at, destroying your own setup instead of helping
it. This is the opposite of Boss's Orders' usual role as an auto-include
staple, and it's not something `simulate_baseline.py` can catch on its
own — the simulator has no opponent board to gust incorrectly, so this
finding came from reading what Boss's Orders and Hazardous Venom actually
do to each other, not from a trial count. Testing confirmed cutting it for
more Team Rocket's Petrel measurably helped anyway (see table below), so
the simulated numbers and the rules-reading point the same direction.

## Supporter comparison — 5 configs, 1000 trials each (5,000 total)

You called it — the Supporter mix was the single biggest lever tested.
Every variant below kept Pokémon (17), Energy (13 Darkness), and the core
Item suite (Poffin/Ultra Ball/Trolley) identical, varying only
Lillie's Determination / Janine's Secret Art / Team Rocket's Petrel /
Boss's Orders:

| Variant | Grimer online T6 | Muk online T6 | Whirlipede T6 | Avg hand size |
|---|---|---|---|---|
| Lillie's-heavy (4/2/2, 2 Boss's) | 80.2% | 36.9% | 43.8% | 4.37 |
| Balanced (3/3/3, 2 Boss's) | 80.3% | 35.6% | 42.8% | 3.60 |
| Petrel-heavy (2/2/4, 2 Boss's) | 78.8% | 35.0% | 44.1% | 3.43 |
| Janine's-heavy (2/4/2, 2 Boss's) | 75.9% | 30.7% | 38.6% | 3.60 |
| **No Boss's (4/2/4, 0 Boss's) — winner** | **80.7%** | **39.2%** | **46.7%** | 4.03 |

Two clear findings, not just noise:
- **Janine's Secret Art is the weakest Supporter here**, worst on every
  metric — it attaches Energy but never puts a new Pokémon into play, so
  leaning on it slows board development even though it looks like
  "ramp." Kept at 2 copies (not 0) since it still has a real job:
  searching Darkness Energy onto a Benched piece that needs it, just not
  as the deck's primary engine.
- **Cutting Boss's Orders for more Team Rocket's Petrel beat every other
  config**, including the 4-Lillie's-heavy one — Petrel searches any
  Trainer card, which in this deck usually means fetching another
  Buddy-Buddy Poffin or Ultra Ball, compounding the search chain in a way
  the other Supporters don't.

## Design notes

- Verified with `check_energy_support.py`: mono-Darkness (13 Basic
  Darkness Energy) covers every attack, including Hazardous Venom's
  double-Darkness cost. No shortfalls, 60 cards, no card over 4 copies,
  one ACE SPEC (`Precious Trolley` — fits well since Ekans, Venipede, and
  Team Rocket's Grimer are all Basics).
- Mulligan math: 11 effective Basics (Ekans, Venipede, Team Rocket's
  Grimer) -> 22.2%.
- Bench-slot math: 3 lines want board presence (Ekans/Arbok,
  Venipede/Whirlipede, Grimer/Muk) — comfortably within the usual
  6-slot ceiling.
- Real turn sequence for the combo: Turn N, Whirlipede applies Poison +
  locks the opponent's next-turn retreat. Opponent's Turn N+1: forced to
  stay put. Your Turn N+2: bring in Arbok (or have it already down) for
  Panic Poison to stack Burn+Confuse on top of the still-active Poison,
  or if Arbok already fired earlier and conditions are already at 3, just
  swap Team Rocket's Muk in and fire Hazardous Venom for the full 300 —
  the lock from Whirlipede is what guarantees this lands rather than
  whiffing on an empty board state.
- `Ekans`'s own attack (`Poison Blend`, coin-flip Confuse+Poison) is a
  weak seed attack — not relied on; the deck wants Ekans in play mainly
  to evolve into Arbok.

## Baseline simulation, final build (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Ekans | 97.0% | 1.54 |
| Arbok | 62.2% | 3.42 |
| Venipede | 92.4% | 1.81 |
| Whirlipede | 46.7% | 3.47 |
| Team Rocket's Grimer | 80.7% | 1.95 |
| Team Rocket's Muk | 39.2% | 3.70 |

First attack landed by turn 6 in 94.4% of trials (avg turn 2.63). Average
final hand size at turn 6: 4.03. As always: no retreating or opponent
modeled, so this measures development speed, not whether the Boss's
Orders anti-synergy or the Whirlipede lock actually play out the way
described above — that's a real-match question, not a simulator one.

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
3 Ultra Ball MEG 131
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 119
2 Janine's Secret Art SFA 59
4 Team Rocket's Petrel ASC 207
4 Night Stretcher MEG 173
4 Air Balloon BLK 79
4 Rescue Board TEF 159

Energy: 13
13 Basic Darkness Energy

Total Cards: 60
```
