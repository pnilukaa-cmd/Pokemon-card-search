## What changed since the 2026-10-08 table

**The field.** 77 → 97 decks, same per-pair seeds (`rr1`). Twenty lists
added, none removed:
- **Mega Evolution decks:**
  - `mega_absol_ex_hand_lock`
  - `mega_dragonite_kangaskhan_salazzle_wall`
  - `mega_emboar_oricorio_fire_turbo`, `mega_emboar_oricorio_munkidori`
  - `mega_gengar_ex_toxtricity_chains`
  - `mega_zeraora_cinderace_thunderous_fist`
  - `mega_zygarde_cinderace_gaia_wave`, `mega_zygarde_cinderace_turbo_flare`
- **Builds and reviews since:**
  - `aggron_diggersby_angry_slam`, `gourgeist_diggersby_horrifying_rondo`
  - `alakazam_dudunsparce_powerful_hand`, `alakazam_munkidori_strange_hacking`
  - `arboliva_ogerpon_oil_salvo`
  - `chesnaught_meganium_wild_growth`
  - `hydrapple_hydra_breath_festival`, `hydrapple_seaking_festival_lead`
  - `hydreigon_grafaiai_energy_denial`, `hydreigon_relicanth_hammer_denial`
  - `munkidori_ex_pecharunt_chains`
  - `snorlax_bouffalant_kangaskhan_curly_wall`

**The engine** (commit in `ENGINE_COMMIT`; 54 engine commits since d6badee).
Every deck can move. The changes most likely to move a deck:

- **Pilot, measured and on:**
  - **Switch** waits for a Benched Pokémon that does more this turn, and
    goes to it. It was played on sight into the healthiest body. Measured
    +0.28 to +12.39 on the 10 decks it was tried on.
  - **The manual attachment** goes where the Energy pays part of an attack
    (type-aware), not to whoever is short a number of Energy.
  - **Rare Candy, evolution and searches** go first to an evolved
    whole-side engine (Wild Growth, Metal Bridge).
  - **Searches take the piece that evolves something** (`smart_search`).
  - **Wally's Compassion-style heals** spare an attacker's Energy.
- **Card texts that resolved wrongly:**
  - **Heals** named one Pokémon and healed all of them, or dropped their
    filters and costs: Wally's Compassion, Potion, Super Potion and about
    two dozen more.
  - **HP Abilities** dropped their conditions and scaling: Scale Up,
    Resilient Soul, Craftsmanship, Vibrant Dance, Cynthia's Power Weight,
    Ancient Booster.
  - **Seventeen Tools** were never attached. Curly Wall, Lively Stadium,
    Iron Defender and Attract Customers did nothing or the wrong thing.
  - **Meganium's Wild Growth** did nothing. Retaliation ignored the Energy
    it counts.
  - **Prize modifiers** applied to the wrong side.
  - **"For each heads"** effects happened once.
  - **Devolution and hand disruption** (Judge, Xerosic's) didn't do what
    they print.
  - **Single-target counters, "each" spreads, look-at-the-deck Trainers,
    and attach-from-the-top cards** misread their targets.
  - **Sky Transport** switched to the healthiest body, not the attacker.
  - **Teal Dance** drew whether or not it attached.
  - **Ultra Ball** searched before paying.
  - **Cinderace's Explosiveness and Turbo Flare, Mischievous Painting,
    Handheld Fan, Oil Salvo, Strange Hacking and Angry Slam** each did
    something other than their text.
- **Tried and removed** (measured neutral or negative): coin_expectation,
  denial_weight, gust_needs_attacker, painting_value, hand_cost_hold,
  bench_after_abilities, selfshuffle_keep_bench, overflow_attach.

**What moved.** Twenty strong new decks pull every returning deck's mean
down, so the fair comparison is against the same 76 opponents as the
2026-10-08 table. On that basis 45 of the 77 returning decks are within 3
points (mean shift 3.6). The big movers:
- **Up:**
  - `metal_metang_excadrill` and `meta_mega_excadrill`: +20.8 and +19.1.
  - `salazzle_ex_team_rockets_muk_condition_stack`: +16.7.
  - `kyurem_vanilluxe_blizzard`: +12.1.
  - The three Dragapult meta lists: +7.4 to +10.4.
- **Down:**
  - `orthworm_ex_metal_retaliation`: −10.4.
  - `feraligatr_munkidori_damage_transfer`: −6.7.
  - `study_mega_excadrill_drill_mill`: −6.1.
  - Team Rocket's Porygon-Z, Tyranitar and Honchkrow lists: −4.7 to −5.4.

Which engine change moved which deck was not measured one change at a time.
