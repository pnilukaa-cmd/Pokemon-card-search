# Salazzle ex / Team Rocket's Muk Condition Stack

Built from a card-name lookup ("Slazzle ex" -> Salazzle ex), then a search
for a real synergy piece rather than just packing the best individual
Salazzle cards. Salazzle ex's own attack applies two Special Conditions in
one hit; the pool has exactly two cards whose damage scales directly with
*how many* Special Conditions are on the opponent's Active — this deck
pairs them.

## Centerpieces

1. **Salandit -> Salazzle ex** (POR 15 / POR 101, 260 HP) — `Nasty Plot`
   (1 Fire) searches your deck for **up to 2 cards, any cards**, a
   genuinely flexible tutor. `Dire Nails` (Fire+Fire, 100 dmg) Burns
   **and** Poisons the opponent's Active in one hit, then switches
   Salazzle ex itself to the Bench (you choose which Benched Pokémon
   comes up) — hit-and-run, not a card that sits and tanks.
2. **Salandit -> Salazzle** (ASC 224, 120 HP) — the same Basic also
   supports this second Stage 1: `Sudden Scorching` (Colorless+Colorless,
   0 base dmg) makes the opponent discard a card from hand, guaranteed,
   every attack. **Design note, checked directly against the rules, not
   assumed**: the card's text has a second clause — 2 more discards "if
   this Pokémon evolved from Salandit during this turn" — but a
   Pokémon can't attack the same turn it evolves under the normal game
   rules, and a full sweep of this dataset found no card in the current
   Standard pool that grants an exception. Treat this as a reliable
   1-card-discard attack; the 3-card mode doesn't appear to be reachable
   as this deck is built.
3. **Team Rocket's Grimer -> Team Rocket's Muk** (DRI 123 / DRI 124,
   150 HP) — `Hazardous Venom` (Darkness+Darkness+Colorless): **100 damage
   for each Special Condition on the opponent's Active.** Since Dire Nails
   already guarantees exactly 2 conditions in one hit, this isn't a
   conditional "if Poisoned" bonus like most cards in this shape — it's a
   deterministic 200 damage follow-up once both pieces are down.

## The real gap in this combo, not glossed over

Dire Nails and Hazardous Venom can't happen the same turn — Salazzle ex
already used its one attack for the turn applying the conditions, so Muk
has to wait until your *next* turn to cash in. That leaves the opponent's
turn in between, and **retreating cures every Special Condition** — if
they simply retreat their Burned/Poisoned Active before your next turn,
both conditions are gone and Hazardous Venom hits for 0 (it has no base
damage of its own, purely the per-condition multiplier). Nothing in this
build locks their retreat during that window. If this turns out to matter
in practice, Team Rocket's Muk's *other* attack, `Gooped Up`
(Darkness+Colorless, 40 dmg, Confuse + can't-retreat-next-turn), is a real
answer — but using it costs you the turn you'd otherwise spend setting up
or cashing in, so it's a genuine tradeoff, not a free fix.

## Design notes

- **Real Fire/Darkness Energy split, not a mono-type deck.** Both payoff
  attacks need their actual type (Dire Nails: 2 Fire; Hazardous Venom: 2
  Darkness), so this isn't a "Colorless cost accepts anything" situation
  like several other decks built this session — 7 Basic Fire + 7 Basic
  Darkness Energy, verified with `check_energy_support.py` to cover both
  sides with no shortfalls.
- **Mulligan math is a real weak point**: 8 effective Basics (4 Salandit,
  4 Team Rocket's Grimer — both already at the 4-copy legal max) ->
  **34.6%**, elevated compared to most decks built this session (which
  targeted 12+ Basics for ~19%). Buddy-Buddy Poffin (4x) and Ultra Ball
  (4x) help find pieces on turn 2+ but don't touch the opening 7-card
  check itself. Worth knowing going in, not something the support suite
  actually fixes.
- Bench-slot math: 3 lines want board presence (Salandit feeding two
  different Stage 1 targets counts as roughly one slot's worth of
  pressure since only one evolves per copy drawn; Grimer/Muk is the
  second full line) — comfortably within the usual ceiling.
- Checked `current_meta_staples.md` for existing precedent on this
  archetype — found none, this looks like a genuinely new pairing for
  this project rather than a known meta list to cross-check against.
- `Precious Trolley` (ACE SPEC: search any number of Basic Pokémon onto
  the Bench) fits well here since both Salandit and Team Rocket's Grimer
  are Basics — one card can put a real chunk of the board down at once.
  Added it to `simulate_baseline.py`'s effect registry while building
  this (same search-to-bench shape as Buddy-Buddy Poffin/Hop's Bag, just
  unrestricted).
- 60 cards, no card over 4 copies, one ACE SPEC.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

Development-timing only — no retreating or opponent modeled (so it can't
show the retreat-escape gap above in action either way):

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Salandit | 97.7% | 1.37 |
| Salazzle | 68.9% | 2.97 |
| Salazzle ex | 58.2% | 3.23 |
| Team Rocket's Grimer | 94.1% | 1.63 |
| Team Rocket's Muk | 52.6% | 3.24 |

First attack landed by turn 6 in 93.9% of trials (avg turn 2.94, almost
always Salandit or Grimer's own weak Basic-level attack while the real
combo assembles). Average final hand size at turn 6: 3.83 — noticeably
thinner than other decks this session, a real cost of running fewer draw
Supporters in favor of the dual-type search suite. `Pokégear 3.0` isn't
modeled (its dig-for-a-Supporter shape doesn't match the registry's
search-to-bench/hand patterns).

## Pokémon TCG Live Import

```
Pokémon: 15
4 Salandit POR 15
2 Salazzle ASC 224
3 Salazzle ex POR 101
4 Team Rocket's Grimer DRI 123
2 Team Rocket's Muk DRI 124

Trainer: 31
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Boss's Orders MEG 114
4 Lillie's Determination MEG 119
2 Night Stretcher MEG 173
2 Switch MEG 130
3 Team Rocket's Petrel ASC 207
1 Air Balloon BLK 79
2 Rescue Board TEF 159
2 Energy Search POR 72
2 Pokégear 3.0 BLK 84
1 Precious Trolley SSP 185

Energy: 14
7 Basic Fire Energy
7 Basic Darkness Energy

Total Cards: 60
```
