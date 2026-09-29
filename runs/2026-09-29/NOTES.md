## What changed since the 2026-09-27 table

**The field.** 57 decks: the 55 of the previous run plus
`ditto_transform_hydreigon` (built this session) and the user's
`tr_spidops_mewtwo_hammer`. Same per-pair seeds (`rr1`), so a deck in both
runs faces the same dice against the same opponent. The Ditto list's field
copy now carries legal reprints (resolved by name before; no game changes).

**The engine** (commit in `ENGINE_COMMIT`):

- **Brave Bangle** added 60 instead of 30 and ignored its ex-only clause
  (priced by both DAMAGE_TOOLS and the generic Tool reader). Four field
  decks run it: expect crabominable/dhelmise/festival_lead/veluza lower.
- **Pilot:** Backtrack Badge goes on a Pokemon that flips for an attack;
  Energy skips an Active whose attacks all do nothing; name-limited
  Abilities ("can't use more than 1 Fan Call") are limited per name.
- **Cards:** Impromptu Carrier (once, on play, optional), Born to Slack
  (gates Slaking, not the opponent), Crobat CRI 51 (top of deck, not
  hand), Toxtricity, Mandibuzz, Lickitung, Tricky Steps / Jamming Wing
  (the opponent's Energy to their Bench).
- Mechanic taxonomy: nine 30C effects tagged (no effect on games).
