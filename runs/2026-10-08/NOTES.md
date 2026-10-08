## What changed since the 2026-09-30 table

**The field.** 57 → 77 decks, same per-pair seeds (`rr1`). Twenty lists
added, none removed:

- **Six user Mew ex lists:** `mew_alex_centiskorch_mill`, `mew_baby_box`,
  `mew_dbc_bastiodon`, `mew_dbc_hypno`, `mew_lonestar_gourgeist_dragapult`,
  `mew_pikachu_box`.
- **User and study lists:** `chandelure_maushold_dudunsparce_wall`,
  `diggersby_munkidori_earthquake`, `trevenant_rapidash_uxie`,
  `golbat_brute_bonnet_punch`.
- **Ten Team Rocket lists from the Team Rocket's study:** `team_rocket_*`
  (see [TEAM_ROCKET_STUDY_2026-10-08.md](TEAM_ROCKET_STUDY_2026-10-08.md)).

**The engine** (commit in `ENGINE_COMMIT`). Every deck can move, mostly
because of the first item:

- **Prize cards now reach the hand** after an attack, Checkup or retaliation
  Knock Out. Before, only the Bench sweep moved them.
- **"Whenever your opponent ..." and Checkup Abilities fire:** Holes, Darkest
  Impulse, Gnawing Curse, Lava Zone, Swirling Prose, Sand Stream, Freezing
  Shroud, Good Sleep.
- **Card texts that resolved wrongly:**
  - "Flip 2 coins. If both of them are tails" was read as 75%.
  - "If <name> is on your Bench" was read as the attacker being Benched.
  - "an Item card" searched for a name containing "n", and search stage
    filters were never read.
  - Poison's "N counters instead of 1" landed on the attacker.
  - Unfair Stamp and Archer kept your hand.
  - Torment was not applied.
  - Rocket Mirror moved from the Active.
- **Earlier in the same window:** Scream, Daydream, Nab 'n' Dash, Eternity
  Bloom; Ability-lock cache; cost Tools; self-Asleep attacks; named Stage 1
  Bench searches; Spiteful Evolution; ex-only spreads; Corrosive Winds.
- **Pilot:** Energy for Ability-gated Pokémon (Munkidori); an aimed Rocket Brain.
