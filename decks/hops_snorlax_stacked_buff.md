# Hop's Snorlax Stacked-Buff

Built to match a real deck the user lost to fast — "two Snorlax, a
Phantump, and a Stadium" before they could get started. That's the
Hop's-named-family archetype already logged in
`references/current_meta_staples.md`: every individual "Hop's ___"
attacker looks weak alone, but three *independent* sources stack the same
+30 damage bonus onto whichever one is swinging, and a second, genuine
two-card lock combo sits alongside it.

## The stacked buff — three separate sources, same number

- **Hop's Snorlax** (JTG 117, 150 HP Basic) — Ability `Extra Helpings`:
  *"Attacks used by your Hop's Pokémon do 30 more damage to your
  opponent's Active Pokémon. Doesn't stack with itself."* No "must be
  Active" clause — it works from the Bench. Running 3 copies is about
  redundancy (only one needs to survive), not stacking the bonus itself.
- **Postwick** (JTG 154, Stadium) — same +30, to *both* players' Hop's
  Pokémon. One real risk: if the opponent also runs Hop's cards, they get
  it too — low-probability but worth knowing.
- **Hop's Choice Band** (JTG 148, Tool) — +30 more **and** −1 Colorless
  cost, on whichever Hop's Pokémon holds it.

All three online turns `Hop's Wooloo`'s unimpressive 50-for-3-Colorless
into **140 damage for 2 Colorless**. None of this touches
**Lillie's Clefairy ex** — she isn't Hop's-named, so she runs on her own
kit entirely (see below).

## The lock combo — not a coincidence

- **Hop's Dubwool**'s Ability `Defiant Horn`: the instant you evolve
  Wooloo into Dubwool during your turn, force one of the opponent's
  Benched Pokémon into the Active Spot.
- **Hop's Trevenant**'s attack `Corner` (Psychic+C+C, 90 dmg): the
  Defending Pokémon can't retreat next turn.

Gust a squishy target up with Dubwool, lock it in with Corner, then swing
with whichever buffed attacker is ready. Trevenant's *other* attack,
`Horrifying Revenge` (Colorless only, 30+100 dmg), jumps from 30 to 130
base if a Hop's Pokémon was KO'd by an attack during the opponent's last
turn — same trigger `Hassel` (Supporter) shares, so this deck deliberately
doesn't mind its cheap Basics (Wooloo, Phantump, both 70 HP) trading
early. That's fuel, not just a loss.

## Lillie's Clefairy ex — the one non-Hop's include

190 HP Basic ex, Psychic. Ability `Fairy Zone` turns opposing Dragon
Pokémon's Weakness to Psychic — direct tech if Dragapult ex shows up.
Attack `Full Moon Rondo` (Psychic+Colorless, 20+20-per-Bench-Pokémon-
both-sides) scales on its own, independent of the Hop's buff stack.
`Telepathic Psychic Energy` doubles as extra search here since Phantump
and Clefairy ex are both Psychic-typed — it fetches 2 Basic Psychic
Pokémon to the Bench when attached, on top of just being Energy.

## Design notes

- **Bench-slot math**: 4 lines want board presence (Snorlax standalone,
  Phantump/Trevenant, Wooloo/Dubwool, Clefairy ex) — within the usual
  6-slot ceiling.
- Verified with `check_energy_support.py`: near-mono Psychic base (12
  Basic Psychic + 2 Telepathic Psychic Energy) covers every attack —
  Trevenant's `Corner` and Clefairy ex's `Full Moon Rondo` are the only
  attacks needing the actual Psychic type; everything else (Snorlax,
  Wooloo/Dubwool, Trevenant's `Horrifying Revenge`) is pure Colorless
  cost, so the same Energy base pays for all of it. No shortfalls, no
  ACE SPEC in the deck, 60 cards, nothing over 4 copies.
- Mulligan math: 11 effective Basics (Snorlax, Phantump, Wooloo, Clefairy
  ex) -> 22.2%, a bit elevated — this deck leans on evolving two separate
  lines plus keeping Snorlax alive, so it wants a slightly bigger Basic
  count than a single-line deck would.
- `Hop's Bag` (search up to 2 Basic Hop's Pokémon to Bench) was added to
  `simulate_baseline.py`'s effect registry while building this — it's the
  same search-to-bench shape Buddy-Buddy Poffin already covers, just
  filtered by name instead of HP, and worth having modeled for any future
  named-family deck (Ethan's, Marnie's, Team Rocket's all have similar
  cards).

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Development-timing only — no retreating or opponent modeled:

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Hop's Snorlax | 85.2% | 1.63 |
| Hop's Phantump | 95.0% | 1.56 |
| Hop's Trevenant | 43.1% | 3.30 |
| Hop's Wooloo | 92.4% | 1.53 |
| Hop's Dubwool | 40.0% | 3.14 |
| Lillie's Clefairy ex | 48.8% | 2.05 |

First attack landed by turn 6 in 73.6% of trials (avg turn 3.12) — lower
than most decks built this session, since none of the Basics attack for
much before evolving or before Snorlax's buff is live; the plan is
patient by design. Average final hand size at turn 6: 4.85. `Hassel`
can't be scored here — it's conditional on an opponent-caused KO, which
this no-opponent simulator can't produce; that's a real gap in what this
tool can tell you about this specific deck, not a bug.

## Pokémon TCG Live Import

```
Pokémon: 15
3 Hop's Snorlax JTG 117
3 Hop's Phantump ASC 95
2 Hop's Trevenant ASC 237
3 Hop's Wooloo JTG 135
2 Hop's Dubwool JTG 136
2 Lillie's Clefairy ex ASC 280

Trainer: 31
2 Postwick JTG 154
3 Hop's Choice Band JTG 148
4 Hop's Bag JTG 147
2 Hassel TWM 151
4 Buddy-Buddy Poffin MEG 167
3 Ultra Ball MEG 131
4 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
2 Night Stretcher MEG 173
1 Air Balloon BLK 79
1 Rescue Board TEF 159
2 Switch MEG 130

Energy: 14
12 Basic Psychic Energy
2 Telepathic Psychic Energy POR 88

Total Cards: 60
```
