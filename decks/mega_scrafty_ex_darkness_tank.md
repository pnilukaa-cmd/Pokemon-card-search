# Mega Scrafty ex Darkness Tank — Playbook

The final landing point of a long iteration chain this session: started as
a Krookodile ex/Relicanth hand-disruption deck, pivoted through a
Koffing/Weezing bench-refill package, settled on Scraggy/Mega Scrafty ex
as the core, then added a retaliation stack, a Brute Bonnet finisher
combo, and tuned Trainer counts against a specific real threat (fast
N's Zoroark ex decks). This file is both the decklist and the how-to-pilot
guide — the design notes below are load-bearing for actually playing it,
not just background.

## The game plan in one paragraph

Get a Darkness Pokémon into the Active Spot holding as much passive
retaliation as possible (Punk Helmet, Spiritomb's team-wide Ability,
Spiky Energy), let the opponent hit it, then either grind them down with
Mega Scrafty ex's own `Outlaw Leg` or — if the retaliation stack got big
enough — swing in Brute Bonnet on your very next turn for a one-shot
`Relentless Punches` kill. Janine's Secret Art and Absol's Darkfall keep
the early game from stalling out while the retaliation pieces assemble.

## Centerpieces (recap, verified against real card text)

- **Scraggy -> Mega Scrafty ex** (ASC 134/135, 330 HP): Ability
  `Counterattacking Crest` — 5 damage counters on any attacker that hits
  it while Active, even lethally. `Outlaw Leg` (D+D+C, 160 dmg) discards a
  random hand card **and** the top deck card in the same swing.
- **Spiritomb** (MEG 148, 80 HP) — Ability `Spiteful Swirl`: 1 more damage
  counter on any attacker that hits **whichever** Darkness Pokémon of
  yours is Active, from the Bench, no restriction. Stacks with Mega
  Scrafty ex's own Ability rather than replacing it.
- **Punk Helmet** (PFL 121, Tool, x3) + **Spiky Energy** (JTG 159,
  Special Energy, x2) — both add more retaliation damage counters and,
  critically, **don't compete with each other's slot** (one Tool + one
  Energy per Pokémon), so a single Active can stack both plus
  Counterattacking Crest for up to 11 damage counters on one hit taken.
- **Brute Bonnet** (TWM 118, 120 HP) — `Relentless Punches` (3 Darkness):
  50 + 50 per damage counter already on the opponent's Active. The
  cash-in for everything above.
- **Munkidori** (ASC 99, 110 HP) — Ability `Adrena-Brain`: needs Darkness
  Energy attached to itself (works from the Bench), moves up to 3 damage
  counters from your own Pokémon onto the opponent's — heals your side
  and adds more fuel for Relentless Punches at once. Its own attack
  (`Mind Bend`, Psychic-cost) is unusable in this mono-Darkness build —
  Ability-only include, same pattern as Relicanth in an earlier deck.
- **Absol** (SFA 30, 110 HP, no evolution) — `Darkfall` (1 Colorless): 20
  dmg, +50 more with 3+ Darkness Energy in play. Cheap early damage that
  scales for free off Energy you're already running.
- **Dunsparce -> Dudunsparce** — the draw-and-tempo line, separate from
  the combat plan.

## The core combo, walked out turn by turn

1. **Turn N (opponent's turn)**: they attack your Active — ideally Mega
   Scrafty ex holding Punk Helmet + Spiky Energy, with Spiritomb also in
   play. Damage counters (up to 11+) land on **their** attacker as part
   of resolving their own attack.
2. **Turn N+1 (your very next turn — no opponent turn happens in
   between)**: if Brute Bonnet is Active, `Relentless Punches` fires
   immediately for 50 + 50-per-counter. Because this happens on the turn
   right after the hit, **the opponent never gets a window to retreat and
   erase the counters** — unlike the delayed, retreat-vulnerable combos
   in some other decks built this session, this one is naturally safe
   from that escape hatch.
3. **If Brute Bonnet wasn't already Active**: use **Switch** (free, no
   retreat cost paid, x4 in the deck) to bring it in during your main
   phase before attacking. This is *why* the deck runs 4 Switch — it's
   not generic consistency, it's the enabler for this exact swap.
4. **Munkidori**, if online, adds more counters to the opponent's Active
   on the turns in between, independent of whether they're attacking you
   that turn — a second income stream for the same finisher.

## Turn-by-turn priorities

- **Opening hand**: 15 effective Basics (Dunsparce, Scraggy, Absol, Brute
  Bonnet, Munkidori all count) -> 11.8% mulligan. You should almost
  always have a real choice of what to lead.
- **Turns 1-2**: get Scraggy or Absol down as your attacker, bench
  whatever else you drew. Play **Janine's Secret Art** early if you have
  2+ Darkness Pokémon down — it's your best early Energy-acceleration,
  and unlike Grand Tree (deliberately cut from this build — see below)
  it's entirely one-sided.
- **Turns 2-4**: evolve Scraggy into Mega Scrafty ex as soon as legal
  (can't evolve the same turn a Basic entered play). Start attaching
  Punk Helmet/Spiky Energy to whichever Pokémon is holding the Active
  Spot long-term.
- **Turns 4+**: once the retaliation stack is real, start planning the
  Brute Bonnet swing described above. Use **AZ's Tranquility** to pull
  Mega Scrafty ex back to the Bench and heal it (only triggers the heal
  if the moved Pokémon is an ex, which Mega Scrafty ex is) when it's
  taken real damage, buying it more turns to keep tanking.

## Why Grand Tree was cut — a specific, disclosed matchup call

Grand Tree (ACE SPEC Stadium, evolve a Basic straight from the deck) was
tested and gave a real, measured boost (Mega Scrafty ex online-by-turn-6
rose from 37.0% to 48.8% with it in an earlier build). It was cut anyway
because **the effect is symmetric** — "once during each player's turn" —
and this deck was being tuned specifically against fast N's Zoroark ex
decks that are already fully online by turn 2. N's Zoroark ex itself is a
Stage 1 (evolves from N's Zorua), so Grand Tree would very plausibly
accelerate the exact opponent this build is trying to out-pace. **Maximum
Belt** (ACE SPEC Tool, +50 dmg vs. opposing ex) replaced it — no
symmetric downside, and it buffs Mega Scrafty ex/Brute Bonnet's real
damage output directly. The cost of this swap is real and was measured,
not hidden: Mega Scrafty ex's own online rate dropped back to ~37-39%
without Grand Tree's assist.

## Matchup notes: fast, high-draw decks (N's Zoroark ex and similar)

- **Eri** (discard up to 2 Items from their revealed hand) and
  **Xerosic's Machinations** (cap their hand at 3) are your answers to
  "they're drawing fast and setting up by turn 2" — both deny the
  resources that get them there before they can spend them. Xerosic's
  runs at 2 copies (see below); Eri at 1.
- Don't expect to out-race a deck like this. The plan is to survive their
  early tempo advantage using the retaliation stack (every hit they land
  on you is fuel for your own comeback), not to match their speed
  directly.
- N's Zoroark ex's own Ability (`Trade`: discard 1, draw 2) means a long
  game favors *them* on raw card advantage if the retaliation plan stalls
  — this is a real risk of the matchup, not something this build
  neutralizes outright.

## Trainer-count tuning, tested via `simulate_baseline.py`

Xerosic's Machinations was tested at 1/2/3 copies (trimming Energy
Search, then also Poké Pad, to make room):

| Xerosic's count | First attack by T6 | Mega Scrafty ex T6 | Spiritomb T6 |
|---|---|---|---|
| 1 (cut nothing) | 91.6% | 37.0% | 64.8% |
| **2 (cut Energy Search)** | 88.2% | 39.0% | 66.4% |
| 3 (also cut Poké Pad) | 86.8% | 37.0% | 59.9% |

**Locked in at 2** — going from 1 to 2 is essentially free (Energy Search
was doing little on its own), but 3 has a real, measured cost. Worth
remembering the simulator can't score Xerosic's own effect at all (it
only touches the opponent's hand) — this table only shows what got cut
to make room for it, not its actual value, which has to be judged from
real games.

## Known real risks (not simulator-visible)

- **Munkidori can't be fed by Janine's Secret Art** — Janine's only
  targets "your Darkness Pokémon," and Munkidori is Psychic-typed despite
  needing Darkness Energy attached. Feed it via normal draw/attach or
  Energy Search instead.
- **Shadowy Darkness Energy's damage-prevention only applies while its
  holder is Benched** — if that Pokémon is your Active (e.g. mid-combo),
  it's just a plain Darkness Energy card with no protection.
- Verified with `check_energy_support.py`: mono-Darkness (12 Basic + 2
  Spiky + 2 Shadowy Darkness Energy) covers everything except Spiritomb's
  and Munkidori's own attacks — both intentionally unused, Ability-only
  includes.

## Pokémon TCG Live Import

```
Pokémon: 20
3 Dunsparce TEF 128
2 Dudunsparce TEF 129
2 Spiritomb MEG 148
4 Scraggy ASC 134
3 Mega Scrafty ex ASC 135
2 Absol SFA 30
2 Brute Bonnet TWM 118
2 Munkidori ASC 99

Trainer: 26
3 Punk Helmet PFL 121
2 Xerosic's Machinations SFA 64
2 AZ's Tranquility CRI 106
1 Poké Pad ASC 198
1 Night Stretcher MEG 173
2 Janine's Secret Art SFA 59
4 Lillie's Determination MEG 119
1 Team Rocket's Petrel ASC 207
3 Ultra Ball MEG 131
1 Boss's Orders MEG 114
4 Switch MEG 130
1 Maximum Belt TEF 154
1 Eri TEF 146

Energy: 14
2 Spiky Energy JTG 159
2 Shadowy Darkness Energy PBL 83
10 Basic Darkness Energy MEE 7

Total Cards: 60
```
