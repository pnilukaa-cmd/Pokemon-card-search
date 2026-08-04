# Orthworm ex Metal Retaliation

A beefy-attacker deck built around the `counterattack_on_hit` mechanic family
(17 real cards in the pool: Iron Jugulis, Mega Slowbro ex, Mega Scrafty ex,
Bouffalant, Spiky Energy, and others) — cards that punish the opponent for
attacking at all, not just for missing or whiffing a coin flip.

## Centerpieces

1. **Orthworm ex** (Stellar Crown, Basic, 220 HP) — the beefy attacker.
   `Rock Tomb` (4 Colorless) hits for 150 and locks the opponent's retreat.
   Its Ability `Pummeling Payback` is the retaliation engine: *"If this
   Pokémon is damaged by an attack from your opponent's Pokémon (even if
   this Pokémon is Knocked Out), put 2 damage counters on the Attacking
   Pokémon for each Metal Energy attached to this Pokémon."* This is the
   strongest version of the retaliation family in the pool — no "must be
   Active" clause (unlike most of the other 16 members) and no manual
   activation clause either. It just happens, automatically, every time,
   even on the hit that knocks it out. Load it with Metal Energy and every
   attack against it costs the attacker real damage back, guaranteed.

2. **Duraludon → Archaludon** (both Stellar Crown, Basic → Stage 1, Metal) —
   the support line. Archaludon's Ability `Metal Bridge` — *"All of your
   Pokémon that have Metal Energy attached have no Retreat Cost"* — is what
   actually solves Orthworm ex's real problem: a brutal 4-Colorless retreat
   by default. This was found by cross-checking against a real published
   decklist (Limitless TCG, City League Gifu) rather than by database
   mining alone — the pairing isn't obvious from either card's text read in
   isolation. Archaludon's own attack, `Iron Blaster` (160 dmg), locks it
   out of attacking the following turn — treat it as the Ability piece
   first, attacker second.

3. **Cobalion ex** (Chaos Rising, Basic, 210 HP) — added as a third Basic
   specifically to fix the deck's mulligan math (see below). Its Ability
   `Metal Road` only triggers *"when this Pokémon moves from your Bench to
   the Active Spot"* — it does nothing if already Active at the start of a
   turn. Real sequence: retreat your current Active into Cobalion ex, Metal
   Road fires and lets you move any amount of Metal Energy from your other
   Pokémon onto it, then — since it hasn't attacked yet this turn — it can
   swing `Power Tackle` (200 dmg) the same turn with Energy it didn't have
   a moment ago. `Power Tackle` locks it from attacking your next turn, so
   this is a one-turn burst, not a repeatable engine.

## Support

- **Philippe** (Supporter): attach up to 2 Basic Metal Energy from the
  discard pile to one Metal Pokémon — recovers Energy lost to Archaludon's
  or Cobalion ex's own attack costs, straight back onto Orthworm ex.
- **Poké Pad**: searches a Pokémon *without* a Rule Box — real restriction
  worth knowing, it can find Duraludon/Archaludon but **not** Orthworm ex or
  Cobalion ex (both ex cards have Rule Boxes).
- **Deluxe Bomb** (ACE SPEC Tool, 1 copy): one-shot 120-damage retaliation
  burst stacked on top of whatever Pummeling Payback already does, then
  discards itself.
- **Spiky Energy** (2 copies): a verified real synergy piece (already
  logged in `references/current_meta_staples.md`) — a Special Energy that
  adds the identical "retaliate even through a KO" clause to whatever it's
  attached to, on top of providing Colorless for attack costs.

## Known weaknesses (stated plainly)

- All four Pokémon are ×2 Weak to Fire with a small Grass resistance across
  the board — no tech slot in this build hedges that, same tradeoff as
  every other mono-type deck in this project.
- 11 effective Basics (4 Orthworm ex + 4 Duraludon + 3 Cobalion ex) gives a
  **22.2% mulligan rate** (hypergeometric, down from 34.6% before Cobalion
  ex was added) — solidly in this project's healthy range.
- Switch and Judge sit at 2 copies each (down from 4, traded for Philippe/
  Poké Pad/the third Basic line) — less redundancy for repositioning and
  hand disruption than a more generic build would run.
- Verified with `check_energy_support.py`: mono-Metal supply (13 Metal + 2
  Spiky Energy) covers every attack cost with no shortfalls; no
  attack-gating Ability text found; 60 cards total, no card over the
  4-copy limit, ACE SPEC count within the 1-per-deck limit; every card name
  matched `pokemon_standard_cards.json`.

## Pokémon TCG Live Import

```
Pokémon: 14
4 Orthworm ex SCR 110
4 Duraludon SCR 106
3 Archaludon SCR 107
3 Cobalion ex CRI 103

Trainer: 31
4 Ultra Ball MEG 131
4 Boss's Orders MEG 114
4 Lillie's Determination MEG 119
2 Judge POR 76
2 Switch MEG 130
2 Air Balloon BLK 79
3 Rescue Board TEF 159
4 Night Stretcher MEG 173
1 Deluxe Bomb SCR 134
2 Poké Pad ASC 198
3 Philippe CRI 110

Energy: 15
13 Basic Metal Energy
2 Spiky Energy JTG 159

Total Cards: 60
```
