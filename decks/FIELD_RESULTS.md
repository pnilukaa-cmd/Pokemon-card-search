# Field results — every deck against every other deck

Full round robin over **97 decks**, **1000 games** per pairing, 4656 pairings, 4,656,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-10-26. **These supersede every number in the deck files before this date.**

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

**Stale since the run.** A fix committed after this table (Basic Energy was
read as Special Energy) changes the 11 field decks that care about Special
Energy, and every pairing against them:
- Enhanced Hammer had been discarding Basic Energy. That's 8 decks:
  `alakazam_dudunsparce_powerful_hand`, `hydreigon_grafaiai_energy_denial`,
  `hydreigon_relicanth_hammer_denial`, `mew_alex_centiskorch_mill`,
  `mew_baby_box`, `mew_dbc_bastiodon`, `mew_dbc_hypno`,
  `trevenant_rapidash_uxie`.
- Tyrantrum's +150 HP had come on with any Energy:
  `kangaskhan_tyrantrum_flip_mill`.
- Farfetch'd and Ruffian also check for Special Energy:
  `ditto_transform_hydreigon`, `mew_pikachu_box`.

Their rows here overstate the Hammer decks and Tyrantrum until the next run.

A second fix after this table (2ee4fb9): a Fossil is an Item outside play,
so Pokémon searches, Night Stretcher and setup no longer treat one as a
Basic Pokémon. It changes the field decks with Fossils:
`cradily_accelgor_conditions`, `cradily_amoonguss_conditions`,
`kangaskhan_tyrantrum_flip_mill`, `mew_dbc_bastiodon`,
`study_centiskorch_bastiodon_mill` (and `aurorus_kangaskhan_tundra_wall`,
added to the field after this run).

A third (aa450cf): "You can use this card only if you discard another card
from your hand" was free, so Morty's Conviction, Canari and Iris's
Fighting Spirit cost nothing, and Morty's drew one card. Ten field decks
run one of them: `aggron_diggersby_angry_slam`, `arboliva_ogerpon_oil_salvo`, `gourgeist_diggersby_horrifying_rondo`, `mega_absol_ex_hand_lock`, `mega_zeraora_cinderace_thunderous_fist`, `mega_zygarde_cinderace_gaia_wave`, `mega_zygarde_cinderace_turbo_flare`, `mew_dbc_bastiodon`, `munkidori_ex_pecharunt_chains`, `wugtrio_paralysis_pin`.

A fourth (4bdff48): Ignition Energy was never discarded at end of turn,
and Prism / Neo Upper Energy kept what they gave a Pokemon before it
evolved. Field decks with those Energy: `mew_baby_box`, `mew_pikachu_box`,
`study_flygon_sandy_flapping_mill`, `study_maushold_gnaw_latias`.

A fifth and sixth (243a582, 27be9e3): Boss's Orders and the other gust
cards had dragged up the Benched Pokémon with the least HP left, Knock Out
or not, so the target was Knocked Out that turn in 29% to 52% of gusts.
They are now played for a Knock Out (+0.97 on average over 11 decks), and
with none, to strand a Pokémon that can neither attack nor retreat (+0.86
over 7). That changes the 91 field decks with a gust card, which is every
deck but `arbok_muk_laser_darkbell`, `arbok_muk_trolley_darkbell`,
`arbok_team_rockets_muk_condition_stack`, `aurorus_kangaskhan_tundra_wall`,
`chesnaught_meganium_wild_growth`, `maushold_gnaw_together_mill`,
`mega_dragonite_kangaskhan_salazzle_wall`, `meta_slowking` and
`snorlax_bouffalant_kangaskhan_curly_wall`; and every pairing.

A seventh (e84da63): King's Order now benches any Stage and is chosen at
all, Gwynn, Prism Tower and Brilliant Blender feed it, and Misty's
Vitality ends the turn. Field decks it changes: `kyurem_vanilluxe_blizzard`
(Misty's Vitality) and the three with Duskull's Come and Get You, now
priced (`alakazam_dudunsparce_powerful_hand`,
`mega_lopunny_dusknoir_snipe_finisher`, `meta_dragapult_dusknoir`:
+0.03, +0.31, −0.02 at 200 games). The team damage-buff and Bench-only
attack fixes touch no field deck. `kingdra_ex_kings_order` was added to
the field after this run.

`orthworm_ex_metang_archaludon` was added to the field after this run too
(2026-10-29); b6759de changes only the setup baseline.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `mega_zeraora_cinderace_thunderous_fist` | **87.2%** | 90.8% | 93/96 | tr_arbok_yveltal_snow_coating (100%) | mega_zygarde_cinderace_gaia_wave (32%) |
| 2 | `snorlax_bouffalant_kangaskhan_curly_wall` | **87.1%** | 91.8% | 94/96 | mew_dbc_hypno (100%) | mega_zygarde_cinderace_gaia_wave (27%) |
| 3 | `mega_zygarde_cinderace_gaia_wave` | **85.9%** | 89.0% | 95/96 | tr_arbok_yveltal_snow_coating (100%) | arboliva_ogerpon_oil_salvo (42%) |
| 4 | `arboliva_ogerpon_oil_salvo` | **82.0%** | 86.0% | 94/96 | tr_arbok_yveltal_snow_coating (98%) | mega_zeraora_cinderace_thunderous_fist (44%) |
| 5 | `munkidori_ex_pecharunt_chains` | **78.5%** | 81.7% | 86/96 | mew_baby_box (100%) | mega_zygarde_cinderace_gaia_wave (21%) |
| 6 | `mega_gengar_ex_toxtricity_chains` | **73.6%** | 77.4% | 86/96 | mew_baby_box (99%) | mega_zygarde_cinderace_gaia_wave (17%) |
| 7 | `meta_mega_excadrill` | **71.9%** | 73.8% | 86/96 | mew_pikachu_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (29%) |
| 8 | `gourgeist_diggersby_horrifying_rondo` | **71.8%** | 76.1% | 82/96 | mew_pikachu_box (100%) | munkidori_ex_pecharunt_chains (17%) |
| 9 | `chesnaught_meganium_wild_growth` | **71.4%** | 75.3% | 87/96 | tr_arbok_yveltal_snow_coating (96%) | tauros_risky_ruins (31%) |
| 10 | `hydrapple_seaking_festival_lead` | **70.6%** | 74.8% | 84/96 | mew_baby_box (98%) | mega_zeraora_cinderace_thunderous_fist (12%) |
| 11 | `mega_dragonite_kangaskhan_salazzle_wall` | **70.1%** | 73.0% | 83/96 | mew_baby_box (98%) | mega_zygarde_cinderace_gaia_wave (13%) |
| 12 | `mega_absol_ex_hand_lock` | **69.5%** | 73.2% | 78/96 | mew_pikachu_box (98%) | mega_zeraora_cinderace_thunderous_fist (16%) |
| 13 | `alakazam_munkidori_strange_hacking` | **69.2%** | 73.4% | 79/96 | team_rockets_wobbuffet_orbeetle_damage_launder (98%) | mega_zygarde_cinderace_gaia_wave (16%) |
| 14 | `mega_zygarde_cinderace_turbo_flare` | **67.5%** | 68.8% | 90/96 | static_venom_drapion (93%) | arboliva_ogerpon_oil_salvo (26%) |
| 15 | `metal_metang_excadrill` | **66.1%** | 67.0% | 83/96 | mew_pikachu_box (97%) | mega_zeraora_cinderace_thunderous_fist (25%) |
| 16 | `ns_zoroark_night_joker_toolbox` | **66.1%** | 70.1% | 80/96 | mew_dbc_hypno (96%) | arboliva_ogerpon_oil_salvo (12%) |
| 17 | `team_rocket_raticate_rush` | **66.0%** | 67.9% | 81/96 | mew_baby_box (97%) | mega_zygarde_cinderace_gaia_wave (16%) |
| 18 | `lurantis_heal_punish` | **65.9%** | 68.1% | 76/96 | mew_pikachu_box (99%) | snorlax_bouffalant_kangaskhan_curly_wall (14%) |
| 19 | `tauros_risky_ruins` | **63.7%** | 64.5% | 68/96 | study_flygon_sandy_flapping_mill (99%) | mega_zygarde_cinderace_gaia_wave (10%) |
| 20 | `team_rocket_nidoking_nidoqueen` | **63.5%** | 67.6% | 73/96 | mew_baby_box (99%) | mega_zeraora_cinderace_thunderous_fist (6%) |
| 21 | `team_rockets_persian_ex_attack_theft` | **62.9%** | 63.9% | 76/96 | mew_baby_box (96%) | snorlax_bouffalant_kangaskhan_curly_wall (20%) |
| 22 | `ditto_transform_hydreigon` | **62.2%** | 63.7% | 69/96 | mew_pikachu_box (98%) | mega_zeraora_cinderace_thunderous_fist (5%) |
| 23 | `mega_emboar_oricorio_fire_turbo` | **60.8%** | 61.7% | 71/96 | mew_baby_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (14%) |
| 24 | `tr_spidops_mewtwo_hammer` | **60.7%** | 61.5% | 70/96 | mew_dbc_hypno (94%) | snorlax_bouffalant_kangaskhan_curly_wall (13%) |
| 25 | `maushold_gnaw_together_mill` | **59.6%** | 61.0% | 67/96 | mew_baby_box (97%) | snorlax_bouffalant_kangaskhan_curly_wall (9%) |
| 26 | `team_rocket_honchkrow_kangaskhan` | **59.4%** | 60.2% | 67/96 | mew_pikachu_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (11%) |
| 27 | `diggersby_munkidori_earthquake` | **59.2%** | 58.2% | 64/96 | mew_pikachu_box (99%) | snorlax_bouffalant_kangaskhan_curly_wall (6%) |
| 28 | `wugtrio_paralysis_pin` | **58.6%** | 58.0% | 62/96 | mew_baby_box (99%) | snorlax_bouffalant_kangaskhan_curly_wall (6%) |
| 29 | `meta_dragapult_pure` | **57.6%** | 59.3% | 65/96 | mew_baby_box (94%) | mega_zeraora_cinderace_thunderous_fist (12%) |
| 30 | `ditto_tyranitar_gengar_hydreigon` | **57.3%** | 57.9% | 62/96 | mew_pikachu_box (95%) | mega_zeraora_cinderace_thunderous_fist (8%) |
| 31 | `aggron_diggersby_angry_slam` | **56.9%** | 57.0% | 57/96 | mew_pikachu_box (99%) | snorlax_bouffalant_kangaskhan_curly_wall (8%) |
| 32 | `meta_dragapult_blaziken` | **56.7%** | 57.0% | 66/96 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | mega_zeraora_cinderace_thunderous_fist (14%) |
| 33 | `team_rocket_raticate_ampharos` | **56.4%** | 56.9% | 63/96 | mew_baby_box (94%) | mega_zeraora_cinderace_thunderous_fist (14%) |
| 34 | `mega_lopunny_dusknoir_snipe_finisher` | **55.9%** | 55.5% | 64/96 | mew_pikachu_box (93%) | snorlax_bouffalant_kangaskhan_curly_wall (17%) |
| 35 | `kyurem_vanilluxe_blizzard` | **55.9%** | 57.4% | 59/96 | mew_pikachu_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (6%) |
| 36 | `scovillain_salazzle_spicy_rage` | **55.3%** | 55.3% | 59/96 | mew_baby_box (94%) | munkidori_ex_pecharunt_chains (14%) |
| 37 | `hydreigon_relicanth_hammer_denial` | **53.9%** | 55.5% | 57/96 | mew_pikachu_box (99%) | mega_zeraora_cinderace_thunderous_fist (2%) |
| 38 | `panic_poison_paralysis` | **53.3%** | 54.8% | 55/96 | mew_baby_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (4%) |
| 39 | `team_rocket_porygon_z_kangaskhan` | **53.2%** | 55.4% | 58/96 | static_venom_drapion (90%) | mega_zeraora_cinderace_thunderous_fist (10%) |
| 40 | `krookodile_ex_relicanth_hand_disruption` | **53.0%** | 52.5% | 52/96 | mew_pikachu_box (94%) | mega_zeraora_cinderace_thunderous_fist (7%) |
| 41 | `alakazam_dudunsparce_powerful_hand` | **52.5%** | 56.7% | 57/96 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | mega_zygarde_cinderace_gaia_wave (10%) |
| 42 | `team_rockets_koffing_weezing_bench_swarm` | **52.5%** | 51.8% | 51/96 | mew_baby_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (3%) |
| 43 | `team_rocket_orbeetle_morpeko` | **51.8%** | 51.8% | 53/96 | mew_baby_box (96%) | arboliva_ogerpon_oil_salvo (9%) |
| 44 | `team_rocket_tyranitar_sandstorm` | **51.4%** | 50.8% | 49/96 | mew_pikachu_box (96%) | mega_zeraora_cinderace_thunderous_fist (2%) |
| 45 | `study_mega_excadrill_drill_mill` | **51.0%** | 51.8% | 51/96 | mew_pikachu_box (93%) | snorlax_bouffalant_kangaskhan_curly_wall (8%) |
| 46 | `cradily_accelgor_conditions` | **50.2%** | 50.0% | 46/96 | mew_pikachu_box (98%) | arboliva_ogerpon_oil_salvo (9%) |
| 47 | `meta_raging_bolt` | **50.1%** | 49.8% | 47/96 | mew_baby_box (83%) | maushold_gnaw_together_mill (15%) |
| 48 | `mew_lonestar_gourgeist_dragapult` | **50.1%** | 51.0% | 48/96 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | mega_zeraora_cinderace_thunderous_fist (4%) |
| 49 | `mega_chandelure_ex_retreat_tax` | **49.8%** | 50.5% | 49/96 | mew_baby_box (90%) | tauros_risky_ruins (12%) |
| 50 | `team_rocket_moltres_houndoom` | **49.7%** | 48.2% | 46/96 | mew_pikachu_box (97%) | mega_zeraora_cinderace_thunderous_fist (3%) |
| 51 | `meta_dragapult_dusknoir` | **49.2%** | 48.0% | 45/96 | mew_baby_box (90%) | mega_zeraora_cinderace_thunderous_fist (5%) |
| 52 | `mega_emboar_oricorio_munkidori` | **49.1%** | 47.5% | 42/96 | mew_pikachu_box (92%) | snorlax_bouffalant_kangaskhan_curly_wall (8%) |
| 53 | `kangaskhan_tyrantrum_flip_mill` | **48.2%** | 46.5% | 44/96 | arbok_team_rockets_muk_condition_stack (91%) | mega_zygarde_cinderace_gaia_wave (7%) |
| 54 | `cradily_amoonguss_conditions` | **47.9%** | 46.3% | 41/96 | mew_pikachu_box (98%) | snorlax_bouffalant_kangaskhan_curly_wall (5%) |
| 55 | `team_rocket_hypno_wobbuffet` | **47.6%** | 46.5% | 43/96 | mew_baby_box (96%) | mega_zeraora_cinderace_thunderous_fist (6%) |
| 56 | `decidueye_ex_judge_sniper_lock` | **46.8%** | 46.8% | 41/96 | mew_baby_box (94%) | mega_zeraora_cinderace_thunderous_fist (8%) |
| 57 | `team_rocket_hypno_exeggutor` | **46.4%** | 45.7% | 41/96 | mew_baby_box (94%) | munkidori_ex_pecharunt_chains (6%) |
| 58 | `veluza_sinistcha_ex_tea_service` | **45.9%** | 44.2% | 36/96 | mew_pikachu_box (93%) | mega_zeraora_cinderace_thunderous_fist (5%) |
| 59 | `water_aggro` | **45.8%** | 44.4% | 35/96 | mew_baby_box (94%) | mega_zeraora_cinderace_thunderous_fist (4%) |
| 60 | `heracross_sinistcha_tea` | **45.0%** | 43.9% | 34/96 | mew_pikachu_box (96%) | arboliva_ogerpon_oil_salvo (8%) |
| 61 | `hydrapple_hydra_breath_festival` | **44.9%** | 41.5% | 39/96 | static_venom_drapion (88%) | mega_zeraora_cinderace_thunderous_fist (2%) |
| 62 | `meta_slowking` | **44.7%** | 43.8% | 35/96 | mew_baby_box (87%) | mega_zeraora_cinderace_thunderous_fist (5%) |
| 63 | `mega_scrafty_ex_darkness_tank` | **44.6%** | 41.4% | 37/96 | mew_pikachu_box (94%) | mega_zeraora_cinderace_thunderous_fist (4%) |
| 64 | `golbat_brute_bonnet_punch` | **44.1%** | 40.4% | 38/96 | mew_baby_box (95%) | mega_zeraora_cinderace_thunderous_fist (4%) |
| 65 | `mew_alex_centiskorch_mill` | **43.9%** | 41.4% | 33/96 | mew_pikachu_box (98%) | hydrapple_seaking_festival_lead (4%) |
| 66 | `dhelmise_veluza_hide_n_sneak` | **43.3%** | 43.8% | 36/96 | static_venom_drapion (85%) | mega_zeraora_cinderace_thunderous_fist (6%) |
| 67 | `arbok_muk_laser_darkbell` | **42.9%** | 40.0% | 37/96 | mew_baby_box (96%) | snorlax_bouffalant_kangaskhan_curly_wall (3%) |
| 68 | `stevens_carbink_damage_wall` | **42.9%** | 41.5% | 34/96 | mew_pikachu_box (82%) | snorlax_bouffalant_kangaskhan_curly_wall (7%) |
| 69 | `arbok_muk_trolley_darkbell` | **40.8%** | 40.0% | 27/96 | mew_baby_box (96%) | snorlax_bouffalant_kangaskhan_curly_wall (4%) |
| 70 | `hops_snorlax_stacked_buff` | **39.8%** | 35.8% | 23/96 | mew_pikachu_box (94%) | snorlax_bouffalant_kangaskhan_curly_wall (4%) |
| 71 | `salazzle_ex_team_rockets_muk_condition_stack` | **39.8%** | 39.8% | 26/96 | mew_pikachu_box (85%) | mega_zygarde_cinderace_gaia_wave (3%) |
| 72 | `hydreigon_grafaiai_energy_denial` | **39.4%** | 37.1% | 32/96 | mew_pikachu_box (94%) | mega_zeraora_cinderace_thunderous_fist (1%) |
| 73 | `tr_crobat_absol_bench_snipe` | **39.3%** | 37.2% | 26/96 | mew_baby_box (89%) | mega_zeraora_cinderace_thunderous_fist (2%) |
| 74 | `toxic_slumber_vileplume_ex` | **39.0%** | 36.8% | 29/96 | mew_pikachu_box (92%) | mega_zeraora_cinderace_thunderous_fist (1%) |
| 75 | `team_rockets_spidops_swarm` | **38.9%** | 36.8% | 26/96 | mew_baby_box (87%) | snorlax_bouffalant_kangaskhan_curly_wall (1%) |
| 76 | `arbok_team_rockets_muk_condition_stack` | **38.2%** | 36.5% | 25/96 | mew_baby_box (95%) | snorlax_bouffalant_kangaskhan_curly_wall (1%) |
| 77 | `meta_ns_zoroark` | **37.6%** | 39.7% | 22/96 | mew_dbc_hypno (81%) | tauros_risky_ruins (8%) |
| 78 | `mew_dbc_bastiodon` | **36.7%** | 30.3% | 29/96 | meta_festival_lead (87%) | mega_zeraora_cinderace_thunderous_fist (1%) |
| 79 | `eerie_inferno_ninetales_burn` | **36.4%** | 31.7% | 22/96 | mew_pikachu_box (92%) | snorlax_bouffalant_kangaskhan_curly_wall (2%) |
| 80 | `chandelure_centiskorch_deck_out` | **36.1%** | 36.2% | 22/96 | mew_pikachu_box (90%) | gourgeist_diggersby_horrifying_rondo (2%) |
| 81 | `study_centiskorch_bastiodon_mill` | **35.2%** | 34.0% | 18/96 | meta_ns_zoroark (86%) | snorlax_bouffalant_kangaskhan_curly_wall (6%) |
| 82 | `trevenant_rapidash_uxie` | **35.2%** | 31.8% | 20/96 | mew_pikachu_box (87%) | snorlax_bouffalant_kangaskhan_curly_wall (3%) |
| 83 | `feraligatr_munkidori_damage_transfer` | **34.3%** | 31.4% | 20/96 | mew_baby_box (92%) | snorlax_bouffalant_kangaskhan_curly_wall (2%) |
| 84 | `darkness_mill_hand_lock` | **34.3%** | 29.5% | 18/96 | mew_pikachu_box (88%) | mega_zeraora_cinderace_thunderous_fist (1%) |
| 85 | `study_hydreigon_zweilous_mill` | **33.7%** | 34.0% | 15/96 | mew_pikachu_box (75%) | snorlax_bouffalant_kangaskhan_curly_wall (4%) |
| 86 | `orthworm_ex_metal_retaliation` | **33.4%** | 28.4% | 20/96 | static_venom_drapion (88%) | snorlax_bouffalant_kangaskhan_curly_wall (2%) |
| 87 | `chandelure_maushold_dudunsparce_wall` | **32.9%** | 30.6% | 12/96 | mew_pikachu_box (87%) | tauros_risky_ruins (3%) |
| 88 | `study_maushold_gnaw_latias` | **32.8%** | 29.6% | 20/96 | mew_pikachu_box (94%) | snorlax_bouffalant_kangaskhan_curly_wall (2%) |
| 89 | `crabominable_veluza_food_prep` | **32.5%** | 27.9% | 15/96 | mew_pikachu_box (77%) | mega_zeraora_cinderace_thunderous_fist (4%) |
| 90 | `meta_festival_lead` | **29.7%** | 26.4% | 10/96 | static_venom_drapion (72%) | mega_zeraora_cinderace_thunderous_fist (2%) |
| 91 | `tr_arbok_yveltal_snow_coating` | **23.3%** | 18.8% | 9/96 | mew_pikachu_box (83%) | mega_zeraora_cinderace_thunderous_fist (0%) |
| 92 | `study_flygon_sandy_flapping_mill` | **22.9%** | 18.2% | 5/96 | mew_pikachu_box (71%) | tauros_risky_ruins (1%) |
| 93 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **19.5%** | 13.6% | 7/96 | study_flygon_sandy_flapping_mill (87%) | mega_zeraora_cinderace_thunderous_fist (1%) |
| 94 | `mew_dbc_hypno` | **18.4%** | 13.8% | 6/96 | mew_pikachu_box (92%) | snorlax_bouffalant_kangaskhan_curly_wall (0%) |
| 95 | `static_venom_drapion` | **17.6%** | 12.4% | 6/96 | mew_pikachu_box (81%) | mega_zygarde_cinderace_gaia_wave (2%) |
| 96 | `mew_pikachu_box` | **12.1%** | 8.1% | 2/96 | meta_festival_lead (61%) | mega_zeraora_cinderace_thunderous_fist (0%) |
| 97 | `mew_baby_box` | **11.3%** | 6.9% | 2/96 | mew_pikachu_box (76%) | mega_zeraora_cinderace_thunderous_fist (0%) |

## Full matrix

Row's win rate against column.

| |mega_zeraora_c|snorlax_bouffa|mega_zygarde_c|arboliva_ogerp|munkidori_ex_p|mega_gengar_ex|meta_mega_exca|gourgeist_digg|chesnaught_meg|hydrapple_seak|mega_dragonite|mega_absol_ex_|alakazam_munki|mega_zygarde_c|metal_metang_e|ns_zoroark_nig|team_rocket_ra|lurantis_heal_|tauros_risky_r|team_rocket_ni|team_rockets_p|ditto_transfor|mega_emboar_or|tr_spidops_mew|maushold_gnaw_|team_rocket_ho|diggersby_munk|wugtrio_paraly|meta_dragapult|ditto_tyranita|aggron_diggers|meta_dragapult|team_rocket_ra|mega_lopunny_d|kyurem_vanillu|scovillain_sal|hydreigon_reli|panic_poison_p|team_rocket_po|krookodile_ex_|alakazam_dudun|team_rockets_k|team_rocket_or|team_rocket_ty|study_mega_exc|cradily_accelg|meta_raging_bo|mew_lonestar_g|mega_chandelur|team_rocket_mo|meta_dragapult|mega_emboar_or|kangaskhan_tyr|cradily_amoong|team_rocket_hy|decidueye_ex_j|team_rocket_hy|veluza_sinistc|water_aggro|heracross_sini|hydrapple_hydr|meta_slowking|mega_scrafty_e|golbat_brute_b|mew_alex_centi|dhelmise_veluz|arbok_muk_lase|stevens_carbin|arbok_muk_trol|hops_snorlax_s|salazzle_ex_te|hydreigon_graf|tr_crobat_abso|toxic_slumber_|team_rockets_s|arbok_team_roc|meta_ns_zoroar|mew_dbc_bastio|eerie_inferno_|chandelure_cen|study_centisko|trevenant_rapi|feraligatr_mun|darkness_mill_|study_hydreigo|orthworm_ex_me|chandelure_mau|study_maushold|crabominable_v|meta_festival_|tr_arbok_yvelt|study_flygon_s|team_rockets_w|mew_dbc_hypno|static_venom_d|mew_pikachu_bo|mew_baby_box|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **mega_zeraora_c** |—|36|32|56|60|72|69|76|66|88|69|84|81|47|75|52|82|85|89|94|80|95|72|86|67|89|90|89|88|92|90|86|86|77|90|77|98|89|90|93|89|94|81|98|90|91|83|96|70|97|95|83|92|94|94|92|94|95|96|89|98|95|96|96|91|94|89|88|91|96|89|99|98|99|98|91|87|99|97|98|93|96|93|99|96|98|88|97|96|98|100|91|99|99|98|100|100|
| **snorlax_bouffa** |64|—|27|51|61|65|71|83|64|80|74|76|78|51|73|56|82|86|37|91|80|88|86|87|91|89|94|94|86|88|92|83|86|83|94|86|95|96|88|92|83|97|87|81|92|91|82|91|70|97|91|92|87|95|93|90|94|95|92|90|95|92|93|96|90|92|97|93|96|96|97|97|93|98|99|99|91|98|98|94|94|97|98|97|96|98|96|98|96|98|100|96|99|100|97|63|99|
| **mega_zygarde_c** |68|73|—|42|79|83|61|73|59|74|87|70|84|60|70|62|84|64|90|88|76|84|72|77|82|85|85|88|80|83|88|82|85|80|86|82|95|92|88|89|90|88|82|97|89|80|78|93|69|88|90|82|93|80|91|75|92|80|91|73|92|91|93|92|90|91|93|90|94|96|97|97|93|95|91|96|90|98|96|96|92|94|94|96|94|97|85|97|93|93|100|94|99|99|98|99|99|
| **arboliva_ogerp** |44|49|58|—|70|63|61|77|58|82|59|82|70|74|70|88|68|70|58|83|71|83|69|80|62|77|86|82|78|90|89|77|75|74|90|67|85|82|79|92|83|85|91|89|71|91|81|89|73|70|83|77|89|93|90|89|89|89|86|92|92|86|96|93|68|90|88|89|90|91|79|89|91|87|93|91|90|93|86|89|66|85|93|96|94|96|72|94|90|92|98|69|98|98|94|93|98|
| **munkidori_ex_p** |40|39|21|30|—|52|50|83|46|70|62|57|69|44|58|48|67|71|61|78|72|72|75|77|29|72|82|83|71|74|82|69|74|72|81|86|94|94|71|81|75|86|88|82|78|82|72|95|78|92|80|81|78|84|94|72|94|89|81|90|94|86|90|90|73|89|94|78|96|94|92|96|85|96|96|96|71|98|95|91|68|94|94|96|84|96|58|96|93|94|99|48|99|99|98|94|100|
| **mega_gengar_ex** |28|35|17|37|48|—|48|60|53|46|60|37|63|43|57|60|60|66|32|67|62|64|70|72|61|73|67|74|68|59|69|70|68|72|74|77|77|83|70|71|70|73|79|68|79|78|72|87|79|78|77|80|77|82|86|80|90|83|88|86|78|78|81|88|75|82|88|82|91|82|90|88|82|86|88|92|84|72|84|81|60|84|89|87|81|94|78|92|87|87|92|73|97|98|92|89|99|
| **meta_mega_exca** |31|29|39|39|50|52|—|58|48|58|53|51|44|49|59|56|60|70|80|65|62|62|49|65|53|65|75|75|67|66|76|67|65|72|82|64|75|75|68|68|68|73|72|67|70|79|70|80|46|72|73|62|77|86|77|76|80|88|83|91|86|73|82|84|60|79|80|79|83|85|77|79|83|86|88|83|82|94|74|64|69|82|88|86|84|94|67|83|89|91|91|71|93|97|91|98|97|
| **gourgeist_digg** |24|17|27|23|17|40|42|—|46|58|46|38|61|47|49|42|61|56|86|53|64|49|72|71|68|66|69|66|62|63|75|57|66|65|70|64|77|77|70|66|79|80|66|82|63|81|67|76|62|84|72|76|78|84|79|82|85|83|78|81|85|78|80|74|86|86|84|75|82|88|81|92|74|90|90|84|63|57|93|98|76|89|92|89|84|92|78|97|91|93|95|76|99|98|98|100|99|
| **chesnaught_meg** |34|36|41|42|54|47|52|54|—|53|41|70|48|60|56|80|57|59|31|70|61|82|56|64|67|62|71|65|64|87|66|61|63|60|75|47|81|71|67|86|65|73|79|87|70|71|69|75|60|58|74|71|83|78|78|76|79|77|72|76|80|79|88|81|70|81|79|76|81|80|63|80|82|86|86|86|86|85|82|76|66|78|81|93|90|88|78|84|84|85|96|81|93|94|93|64|92|
| **hydrapple_seak** |12|20|26|18|30|54|42|42|47|—|58|56|58|49|44|61|56|50|60|61|56|64|74|57|75|64|69|47|52|69|61|52|65|57|60|75|81|88|64|78|64|81|68|82|42|87|61|58|79|59|61|81|76|88|81|75|80|61|79|73|79|73|86|82|96|64|94|61|95|75|84|93|82|89|84|95|86|70|93|91|84|88|94|92|87|81|91|86|78|82|85|97|96|95|92|94|98|
| **mega_dragonite** |31|26|13|41|38|40|47|54|59|42|—|52|51|36|54|38|54|65|45|65|57|75|58|64|40|66|76|84|65|66|74|66|61|64|59|62|77|82|71|66|62|80|70|71|83|81|66|70|48|84|70|69|72|86|82|78|78|82|80|76|75|71|82|80|61|83|88|84|87|85|82|88|80|92|88|89|79|89|84|81|59|74|84|88|88|95|58|90|88|88|92|51|93|97|95|71|98|
| **mega_absol_ex_** |16|24|30|18|43|63|49|62|30|44|48|—|53|47|51|42|50|37|82|75|44|65|80|47|39|56|69|54|69|80|72|70|63|61|66|50|86|65|60|78|84|75|76|86|88|50|58|84|65|77|74|86|79|55|87|67|85|64|74|53|73|83|84|72|69|80|71|82|75|87|72|93|77|79|73|77|77|96|87|95|74|85|86|93|91|91|60|91|88|73|96|62|92|93|94|98|96|
| **alakazam_munki** |19|22|16|30|31|37|56|39|52|42|49|47|—|32|64|46|44|45|75|50|64|62|76|29|51|64|61|58|64|51|72|61|67|60|67|64|74|82|73|57|68|72|77|73|74|87|72|62|83|79|69|85|39|86|84|80|81|73|79|84|79|78|69|81|82|49|86|79|87|82|79|87|82|77|88|90|59|84|89|74|79|90|94|85|72|94|70|89|86|85|95|92|98|98|89|93|97|
| **mega_zygarde_c** |53|49|40|26|56|57|51|53|40|51|64|53|68|—|62|30|69|56|69|70|62|50|55|52|67|68|63|68|65|65|70|67|70|68|65|60|63|74|74|68|84|64|73|69|62|62|59|73|38|68|72|65|77|59|67|53|66|64|66|63|74|75|74|75|74|71|75|73|76|75|83|71|78|85|69|82|71|80|82|59|75|73|70|81|72|83|71|69|75|81|90|83|84|82|93|92|91|
| **metal_metang_e** |25|27|30|30|42|43|41|51|44|56|46|49|36|38|—|50|50|60|73|57|55|53|51|60|62|61|67|59|60|57|62|58|59|66|75|61|65|64|61|64|71|60|65|57|68|72|64|75|42|65|68|61|71|80|66|67|67|83|75|86|85|73|80|80|63|70|72|67|74|81|72|72|77|80|82|74|77|90|65|59|72|77|81|78|78|90|71|75|84|89|83|78|88|94|90|97|95|
| **ns_zoroark_nig** |48|44|38|12|52|40|44|58|20|39|62|58|54|70|50|—|59|32|19|71|52|60|48|54|58|69|65|74|68|66|70|66|58|70|71|67|70|66|70|59|72|74|76|50|43|54|65|79|73|83|72|62|77|62|79|53|81|74|81|63|66|79|76|82|68|75|72|79|75|82|82|81|82|71|70|76|83|32|82|61|37|86|73|82|70|91|64|76|89|76|79|71|95|96|94|74|96|
| **team_rocket_ra** |18|18|16|32|33|40|40|39|43|44|46|50|56|31|50|41|—|50|50|57|56|69|53|53|56|56|59|57|60|66|64|54|58|55|59|58|67|77|58|67|75|71|56|65|54|71|59|65|60|68|68|61|69|73|68|70|70|66|69|74|73|70|78|79|78|68|82|73|84|77|80|81|77|85|83|90|61|86|86|80|80|78|81|88|84|89|81|85|80|81|94|83|94|95|93|97|97|
| **lurantis_heal_** |15|14|36|30|29|34|30|44|41|50|35|63|55|44|40|68|50|—|72|57|50|73|34|59|49|58|63|64|56|77|61|52|57|55|68|40|80|63|63|82|53|70|69|88|58|68|61|67|52|49|67|47|66|73|74|79|71|78|76|75|72|70|85|82|58|79|76|59|78|77|64|92|85|80|79|82|80|52|74|89|62|79|74|92|93|81|68|91|78|84|95|88|91|94|90|99|98|
| **tauros_risky_r** |11|63|10|42|39|68|20|14|69|40|55|18|25|31|27|81|50|28|—|48|54|37|44|69|66|49|33|53|43|53|47|44|56|45|42|51|60|59|58|61|43|72|50|51|49|58|83|43|88|50|56|58|92|61|73|90|68|54|89|56|71|88|72|70|92|57|70|75|73|76|57|85|66|77|84|78|92|76|77|90|86|76|95|87|85|91|97|94|82|94|97|99|86|90|96|96|98|
| **team_rocket_ni** |6|9|12|17|22|33|35|47|30|39|35|25|50|30|43|29|43|43|52|—|44|43|54|61|75|50|56|53|52|47|56|49|51|61|54|53|74|62|54|57|64|68|60|70|55|68|53|77|75|68|64|64|60|75|80|72|80|72|71|66|77|63|71|71|86|76|76|69|82|78|74|89|68|77|76|80|69|81|76|88|74|86|89|78|80|87|90|90|84|80|94|84|98|96|94|98|99|
| **team_rockets_p** |20|20|24|29|28|38|38|36|39|44|43|56|36|38|45|48|44|50|46|56|—|69|46|54|58|57|60|51|55|63|62|51|54|54|55|47|66|62|57|69|58|63|61|54|48|67|62|56|52|62|66|57|68|70|62|74|64|71|66|69|72|70|79|73|77|73|69|63|70|74|65|80|76|76|82|73|70|81|79|80|80|68|81|87|84|84|75|71|84|81|89|84|93|91|94|92|96|
| **ditto_transfor** |5|12|16|17|28|36|38|51|18|36|25|35|38|50|47|40|31|27|63|57|31|—|52|42|67|59|59|54|59|50|63|58|40|43|58|58|73|44|70|62|62|64|65|59|86|48|56|83|70|68|60|70|68|49|83|43|86|56|75|48|69|79|73|64|68|72|65|74|65|83|85|58|74|79|53|70|90|90|78|81|86|56|92|84|90|88|84|86|87|72|94|95|95|94|95|98|97|
| **mega_emboar_or** |28|14|28|31|25|30|51|28|44|26|42|20|24|45|49|52|47|66|56|46|54|48|—|57|53|51|52|48|53|52|50|57|60|52|43|56|60|54|51|50|43|55|59|60|87|64|64|48|46|69|64|64|66|74|64|63|66|62|48|81|63|66|63|66|74|48|62|76|65|77|71|76|72|90|81|71|75|87|73|75|81|68|71|77|78|89|80|83|59|78|89|87|93|91|93|97|98|
| **tr_spidops_mew** |14|13|23|20|23|28|35|29|36|43|36|53|71|48|40|46|47|41|31|39|46|58|43|—|56|53|56|47|54|55|51|48|53|47|49|60|56|82|56|64|81|56|64|55|45|69|62|60|44|65|63|56|69|71|60|58|61|70|67|76|71|69|75|76|75|71|80|61|80|70|71|67|74|73|73|85|75|79|81|56|59|79|77|78|72|80|72|66|84|84|83|83|88|94|91|83|93|
| **maushold_gnaw_** |33|9|18|38|71|39|47|32|33|25|60|61|49|33|38|42|44|51|34|25|42|33|47|44|—|60|39|67|48|44|31|50|44|43|61|70|39|67|62|47|64|54|64|45|53|56|85|59|59|74|54|63|63|54|56|70|59|58|58|60|58|78|67|73|63|53|74|68|75|65|76|64|75|73|63|82|83|82|65|75|85|78|63|64|84|82|82|68|70|78|82|89|83|86|90|97|97|
| **team_rocket_ho** |11|11|15|23|28|27|35|34|38|36|34|44|36|32|39|31|44|42|51|50|43|41|49|47|40|—|56|48|51|57|55|49|53|52|51|44|49|52|53|60|59|55|49|71|44|61|57|65|57|66|62|64|60|64|66|56|70|59|62|70|72|68|71|76|67|71|64|66|66|77|65|71|71|78|75|69|60|87|78|68|74|72|76|84|66|85|84|83|79|83|94|86|96|97|94|98|97|
| **diggersby_munk** |10|6|15|14|18|33|25|31|29|31|24|31|39|37|33|35|41|37|67|44|40|41|48|44|61|44|—|57|44|56|54|41|53|50|46|44|67|64|48|59|58|75|43|58|53|55|44|60|57|66|61|61|53|57|62|56|68|53|72|56|72|50|69|70|92|66|73|63|70|77|72|86|72|83|67|78|56|71|86|91|92|66|77|86|78|80|94|94|76|81|93|96|95|94|97|99|97|
| **wugtrio_paraly** |11|6|12|18|17|26|25|34|35|53|16|46|42|32|41|26|43|36|47|47|49|46|52|53|33|52|43|—|49|53|57|47|55|47|55|41|57|55|62|60|63|65|56|47|37|76|59|67|46|78|61|55|55|78|55|79|59|67|70|62|75|61|70|83|63|75|72|63|75|74|73|46|79|69|86|80|50|44|92|97|64|48|82|84|69|85|60|93|78|82|94|61|95|97|96|97|99|
| **meta_dragapult** |12|14|20|22|29|32|33|38|36|48|35|31|36|35|40|32|40|44|57|48|45|41|47|46|52|49|56|51|—|46|61|51|51|52|62|62|42|62|53|53|59|63|53|56|55|72|59|39|58|58|59|56|64|72|59|63|65|66|74|72|73|63|61|69|50|69|70|68|73|64|79|48|72|70|76|76|72|54|77|64|46|40|80|71|60|82|71|70|80|80|81|84|90|86|90|91|94|
| **ditto_tyranita** |8|12|17|10|26|41|34|37|13|31|34|20|49|35|43|34|34|23|47|53|37|50|48|45|56|43|44|47|54|—|53|62|51|42|58|56|70|48|51|60|68|55|56|69|79|45|44|71|59|50|55|62|71|43|75|42|75|49|65|35|58|68|63|55|72|62|62|64|63|70|77|75|60|60|57|71|82|89|75|83|85|72|84|74|81|75|77|81|79|61|93|79|89|87|87|95|95|
| **aggron_diggers** |10|8|12|11|18|31|24|25|34|39|26|28|28|30|38|30|36|39|53|44|38|37|50|49|69|45|46|43|39|47|—|34|49|45|52|33|63|59|44|54|55|67|42|61|42|68|47|50|57|50|54|57|56|66|58|64|62|60|69|60|71|54|66|64|91|65|70|54|70|72|57|84|62|76|75|74|49|70|79|89|87|72|79|77|76|76|94|88|80|85|85|96|92|91|94|99|96|
| **meta_dragapult** |14|17|18|23|31|30|33|43|39|48|34|30|39|33|42|34|46|48|56|51|49|42|43|52|50|51|59|53|49|38|66|—|54|50|54|61|51|60|53|48|64|63|57|57|55|70|56|50|46|60|57|56|60|75|59|71|63|67|64|70|74|58|62|70|51|65|70|63|71|69|71|52|70|70|79|74|65|44|72|65|41|38|76|69|49|78|59|61|76|75|82|71|89|88|88|84|88|
| **team_rocket_ra** |14|14|15|25|26|32|35|34|37|35|39|37|33|30|41|42|42|43|44|49|46|60|40|47|56|47|47|45|49|49|51|46|—|52|50|47|59|53|48|56|50|61|50|52|45|57|56|54|57|54|59|50|59|60|57|65|58|56|69|64|62|61|67|68|61|57|61|60|62|68|67|72|69|71|73|67|54|71|74|69|65|74|73|79|74|81|74|72|72|72|82|84|87|88|92|90|94|
| **mega_lopunny_d** |23|17|20|26|28|28|28|35|40|43|36|39|40|32|34|30|45|45|55|39|46|57|48|53|57|48|50|53|48|58|55|50|48|—|51|42|55|49|52|55|46|56|49|49|56|56|49|54|56|53|59|55|58|62|59|64|59|56|64|49|58|56|60|66|79|57|53|52|54|65|61|69|64|69|70|57|52|72|73|85|82|57|70|76|66|74|89|78|59|75|80|92|85|81|86|93|90|
| **kyurem_vanillu** |10|6|14|10|19|26|18|30|25|40|41|34|33|35|25|29|41|32|58|46|45|42|57|51|39|49|54|45|38|42|48|46|50|49|—|77|50|56|53|52|51|62|51|48|39|65|48|30|46|68|53|66|58|71|62|54|64|62|64|65|70|58|60|68|61|76|67|50|69|74|84|67|72|66|77|74|58|89|80|82|67|68|77|72|68|57|60|82|78|80|92|58|91|90|91|98|96|
| **scovillain_sal** |23|14|18|33|14|23|36|36|53|25|38|50|36|40|39|33|42|60|49|47|53|42|44|40|30|56|56|59|38|44|67|39|53|58|23|—|33|55|58|51|48|62|61|55|77|69|57|56|32|76|51|49|53|77|63|66|62|66|46|80|54|68|71|70|26|70|76|73|76|70|73|47|75|86|79|76|63|29|69|46|40|64|64|71|68|89|33|70|51|70|82|50|86|87|88|89|94|
| **hydreigon_reli** |2|5|5|15|6|23|25|23|19|19|23|14|26|37|35|30|33|20|40|26|34|27|40|44|61|51|33|43|58|30|37|49|41|45|50|67|—|54|55|54|48|55|55|41|65|40|55|66|72|56|57|65|62|36|67|49|69|47|50|58|50|69|62|62|63|64|73|66|75|63|85|78|76|64|50|73|77|77|74|73|78|84|79|61|80|60|82|73|71|62|89|95|91|96|91|99|97|
| **panic_poison_p** |11|4|8|18|6|17|25|23|29|12|18|35|18|26|36|34|23|37|41|38|38|56|46|18|33|48|36|45|38|52|41|40|47|51|44|45|46|—|48|50|45|55|51|60|58|56|54|59|71|63|52|58|19|50|65|66|61|72|60|69|26|64|47|45|79|63|68|61|70|72|63|77|62|62|64|67|55|84|76|77|89|84|71|79|77|79|68|88|74|50|93|93|89|94|91|92|98|
| **team_rocket_po** |10|12|12|21|29|30|32|30|33|36|29|40|27|26|39|30|42|37|42|46|43|30|49|44|38|47|52|38|47|49|56|47|52|48|47|42|45|52|—|56|56|50|50|46|42|56|56|56|36|57|59|62|59|63|52|56|55|56|57|55|70|62|65|68|64|60|54|57|55|69|59|56|62|73|72|59|53|77|72|58|59|63|70|75|54|83|66|67|77|79|81|65|87|85|90|87|88|
| **krookodile_ex_** |7|8|11|8|19|29|32|34|14|22|34|22|43|32|36|41|33|18|39|43|31|38|50|36|53|40|41|40|47|40|46|52|44|45|48|49|46|50|44|—|75|55|50|53|63|41|42|55|58|53|52|59|58|43|70|42|68|48|64|43|47|58|58|64|46|68|70|64|70|69|71|68|67|52|54|72|75|82|72|72|68|75|75|69|74|75|70|76|73|62|81|79|91|91|86|94|94|
| **alakazam_dudun** |11|17|10|17|25|30|32|21|35|36|38|16|32|16|29|28|25|47|57|36|42|38|57|19|36|41|42|37|41|32|45|36|50|54|49|52|52|55|44|25|—|57|58|68|48|69|54|28|63|65|52|70|24|65|55|43|58|64|68|66|68|63|59|64|60|41|60|61|61|68|67|58|64|73|68|63|57|75|76|55|68|74|81|66|64|70|65|64|77|82|74|82|90|82|87|87|90|
| **team_rockets_k** |6|3|12|15|14|27|27|20|27|19|20|25|28|36|40|26|29|30|28|32|37|36|45|44|46|45|25|35|37|45|33|37|39|44|38|38|45|45|50|45|43|—|52|60|62|50|51|60|70|58|47|57|48|52|64|63|64|71|58|55|52|60|54|51|93|63|59|59|58|63|52|72|60|71|63|62|59|44|63|90|79|76|74|72|80|72|96|87|83|66|90|90|88|92|93|96|98|
| **team_rocket_or** |19|13|18|9|12|21|28|34|21|32|30|24|23|27|35|24|44|31|50|40|39|35|41|36|36|51|57|44|47|44|58|43|50|51|49|39|45|49|50|50|42|48|—|48|53|47|43|53|36|64|55|52|49|52|54|51|55|57|53|62|63|56|62|66|40|67|61|55|66|69|66|67|66|70|70|64|50|71|74|68|60|58|67|74|58|80|54|77|75|74|86|57|89|88|88|95|96|
| **team_rocket_ty** |2|19|3|11|18|32|33|18|13|18|29|14|27|31|43|50|35|12|49|30|46|41|40|45|55|29|42|53|44|31|39|43|48|51|52|45|59|40|54|47|32|40|52|—|56|38|49|40|59|55|47|53|65|37|56|52|44|44|56|42|47|52|65|65|58|78|82|69|88|65|65|75|64|36|62|88|70|88|48|69|79|78|72|55|61|72|67|65|75|47|87|85|92|95|75|96|91|
| **study_mega_exc** |10|8|11|29|22|21|30|37|30|58|17|12|26|38|32|57|46|42|51|45|52|14|13|55|47|56|47|63|45|21|58|45|55|44|61|23|35|42|58|37|52|38|47|44|—|59|52|58|66|30|48|27|54|70|54|41|58|75|48|66|81|60|39|48|24|78|66|62|70|65|60|49|63|56|77|68|86|73|34|36|63|80|64|46|65|54|63|49|73|84|75|81|84|79|79|93|86|
| **cradily_accelg** |9|9|20|9|18|22|21|19|29|13|19|50|13|38|28|46|29|32|42|32|33|52|36|31|44|39|45|24|28|55|32|30|43|44|35|31|60|44|44|59|31|50|53|62|41|—|53|40|59|40|38|49|42|49|48|61|50|56|56|54|36|56|68|60|56|54|62|50|67|62|46|79|70|64|63|68|72|41|64|62|68|72|73|84|88|63|88|78|72|67|70|97|86|90|90|98|97|
| **meta_raging_bo** |17|18|22|19|28|28|30|33|31|39|34|42|28|41|36|35|41|39|17|47|38|44|36|38|15|43|56|41|41|56|53|44|44|51|52|43|45|46|44|58|46|49|57|51|48|47|—|45|49|53|53|45|52|54|45|46|49|57|56|60|62|57|62|64|54|56|49|50|49|63|58|50|62|66|67|55|61|75|62|52|60|43|64|72|59|68|64|64|65|70|77|70|76|73|83|72|83|
| **mew_lonestar_g** |4|9|7|11|5|13|20|24|25|42|30|16|38|27|25|21|35|33|57|23|44|17|52|40|41|35|40|33|61|29|50|50|46|46|70|44|34|41|44|45|72|40|47|60|42|60|55|—|45|48|66|60|57|64|53|57|56|64|60|70|71|63|53|62|50|60|49|47|54|68|59|56|60|58|77|56|43|35|75|61|40|71|71|64|44|74|68|67|80|78|84|78|91|86|84|81|88|
| **mega_chandelur** |30|30|31|27|22|21|54|38|40|21|52|35|17|62|58|27|40|48|12|25|48|30|54|56|41|43|43|54|42|41|43|54|43|44|54|68|28|29|64|42|37|30|64|41|34|41|51|55|—|60|54|59|74|48|59|77|59|65|62|67|46|50|49|42|38|59|37|64|37|60|62|41|46|66|71|41|38|29|60|64|53|46|78|57|58|69|51|51|74|68|71|55|81|66|79|86|90|
| **team_rocket_mo** |3|3|12|30|8|22|28|16|42|41|16|23|21|32|35|17|32|51|50|32|38|32|31|35|26|34|34|22|42|50|50|40|46|47|32|24|44|37|43|47|35|42|36|45|70|60|47|52|40|—|55|41|39|66|41|64|41|56|53|75|69|46|56|59|54|42|52|69|54|63|53|65|63|84|72|58|52|67|68|55|70|64|62|78|60|94|70|78|49|80|87|87|89|90|93|97|94|
| **meta_dragapult** |5|9|10|17|20|23|27|28|26|39|30|26|31|28|32|28|32|33|44|36|34|40|36|37|46|38|39|39|41|45|46|43|41|41|47|49|43|48|41|48|48|53|45|53|52|62|47|34|46|45|—|46|56|65|52|57|54|53|63|57|63|52|57|60|51|52|56|56|59|57|66|48|63|63|66|62|56|46|72|72|48|27|73|67|54|67|70|70|63|73|75|80|84|82|85|88|90|
| **mega_emboar_or** |17|8|18|23|19|20|38|24|29|19|31|14|15|35|39|38|39|53|42|36|43|30|36|44|37|36|39|45|44|38|43|44|50|45|34|51|35|42|38|41|30|43|48|47|73|51|55|40|41|59|54|—|55|58|50|44|50|48|44|73|52|56|51|56|50|40|55|64|51|60|63|47|66|76|71|56|65|74|59|52|60|48|53|65|59|83|70|66|45|73|82|79|83|81|87|92|92|
| **kangaskhan_tyr** |8|13|7|11|22|23|23|22|17|24|28|21|61|23|29|23|31|34|8|40|32|32|34|31|37|40|47|45|36|29|44|40|41|42|42|47|38|81|41|42|76|52|51|35|46|58|48|43|26|61|44|45|—|53|42|38|45|51|52|48|59|53|51|60|38|55|83|63|84|62|70|46|58|63|55|91|70|73|77|43|57|53|66|54|62|68|59|50|72|69|75|69|79|83|89|77|88|
| **cradily_amoong** |6|5|20|7|16|18|14|16|22|12|14|45|14|41|20|38|27|27|39|25|30|51|26|29|46|36|43|22|28|57|34|25|40|38|29|23|64|50|37|57|35|48|48|63|30|51|46|36|52|34|35|42|47|—|42|50|44|47|60|51|32|46|67|61|61|49|67|39|70|67|45|82|72|60|56|74|71|34|59|59|58|75|75|82|85|58|87|78|74|64|76|98|86|94|92|98|98|
| **team_rocket_hy** |6|7|9|10|6|14|23|21|22|19|18|13|16|33|34|21|32|26|27|20|38|17|36|40|44|34|38|45|41|25|42|41|43|41|38|37|33|35|48|30|45|36|46|44|46|52|55|47|41|59|48|50|58|58|—|55|52|64|55|64|59|58|41|49|52|59|45|59|50|70|58|51|52|58|70|53|45|84|66|71|74|63|64|59|55|78|75|79|81|79|89|85|88|89|80|89|96|
| **decidueye_ex_j** |8|10|25|11|28|20|24|18|24|25|22|33|20|47|33|47|30|21|10|28|26|57|37|42|30|44|44|21|37|58|36|29|35|36|46|34|51|34|44|58|57|37|49|48|59|39|54|43|23|36|43|56|62|50|45|—|49|59|46|48|60|58|72|53|43|46|43|53|48|57|52|76|66|66|54|46|75|58|61|63|22|59|58|73|82|72|53|68|73|63|63|60|78|83|88|66|94|
| **team_rocket_hy** |6|6|8|11|6|10|20|15|21|20|22|15|19|34|33|19|30|29|32|20|36|14|34|39|41|30|32|41|35|25|38|37|42|41|36|38|31|39|45|32|42|36|45|56|42|50|51|44|41|59|46|50|55|56|48|51|—|61|54|61|56|58|45|46|58|62|45|59|51|65|58|46|47|61|66|53|47|82|64|66|75|61|62|57|54|73|74|75|80|76|87|82|88|86|82|90|94|
| **veluza_sinistc** |5|5|20|11|11|17|12|17|23|39|18|36|27|36|17|26|34|22|46|28|29|44|38|30|42|41|47|33|34|51|40|33|44|44|38|34|53|28|44|52|36|29|43|56|25|44|43|36|35|44|47|52|49|53|36|41|39|—|49|52|62|46|64|64|60|47|40|35|44|56|41|70|58|48|62|52|60|46|69|53|60|67|71|77|59|60|72|71|66|82|72|79|81|87|88|93|85|
| **water_aggro** |4|8|9|14|19|12|17|22|28|21|20|26|21|34|25|19|31|24|11|29|34|25|52|33|42|38|28|30|26|35|31|36|31|36|36|54|50|40|43|36|32|42|47|44|52|44|44|40|38|47|37|56|48|40|45|54|46|51|—|48|49|43|47|50|81|48|46|47|53|51|64|70|50|57|54|55|58|37|73|89|82|59|63|70|72|64|78|80|69|63|76|89|76|82|82|89|94|
| **heracross_sini** |11|10|27|8|10|14|9|19|24|27|24|47|16|37|14|37|26|25|44|34|31|52|19|24|40|30|44|38|28|65|40|30|36|51|35|20|42|31|45|57|34|45|38|58|34|46|40|30|33|25|43|27|52|49|36|52|39|48|52|—|64|47|68|57|42|44|49|43|51|56|41|68|65|44|68|56|58|52|49|66|52|46|46|81|70|46|77|76|61|69|78|89|86|81|88|96|93|
| **hydrapple_hydr** |2|5|8|8|6|22|14|15|20|21|25|27|21|26|15|34|27|28|29|23|28|31|37|29|42|28|28|25|27|42|29|26|38|42|30|46|50|74|30|53|32|48|37|53|19|64|38|29|54|31|37|48|41|68|41|40|44|38|51|36|—|37|65|64|68|38|75|34|78|45|57|64|64|57|59|82|67|51|74|60|59|60|67|77|62|51|73|60|55|69|76|83|84|82|88|83|86|
| **meta_slowking** |5|8|9|14|14|22|27|22|21|27|29|17|22|25|27|21|30|30|12|37|30|21|34|31|22|32|50|39|37|32|46|42|39|44|42|32|31|36|38|42|37|40|44|48|40|44|43|37|50|54|48|44|47|54|42|42|42|54|57|53|63|—|55|53|43|53|47|53|50|65|50|37|52|63|62|57|58|68|57|47|54|46|68|62|55|71|70|57|70|79|84|75|83|83|83|65|87|
| **mega_scrafty_e** |4|7|7|4|10|19|18|20|12|14|18|16|31|26|20|24|22|15|28|29|21|27|37|25|33|29|31|30|39|37|34|38|33|40|40|29|38|53|35|42|41|46|38|35|61|32|38|47|51|44|43|49|49|33|59|28|55|36|53|32|35|45|—|57|48|54|71|58|71|59|56|62|59|46|42|74|55|76|71|78|78|68|60|61|68|69|69|73|62|60|76|89|83|86|82|94|86|
| **golbat_brute_b** |4|4|8|7|10|12|16|26|19|18|20|28|19|25|20|18|21|18|30|29|27|36|34|24|27|24|30|17|31|45|36|30|32|34|32|30|38|55|32|36|36|49|34|35|52|40|36|38|58|41|40|44|40|39|51|47|54|36|50|43|36|47|43|—|59|51|72|51|74|56|57|61|56|54|55|72|43|64|68|74|70|60|64|73|69|65|73|76|62|50|84|78|87|85|90|94|95|
| **mew_alex_centi** |9|10|10|32|27|25|40|14|30|4|39|31|18|26|37|32|22|42|8|14|23|32|26|25|37|33|8|37|50|28|9|49|39|21|39|74|37|21|36|54|40|7|60|42|76|44|46|50|62|46|49|50|62|39|48|57|42|40|19|58|32|57|52|41|—|33|42|65|48|41|68|67|58|59|24|49|71|81|32|73|82|78|48|37|73|35|76|56|48|54|70|90|62|78|54|98|92|
| **dhelmise_veluz** |6|8|9|10|11|18|21|14|19|36|17|20|51|29|30|25|32|21|43|24|27|28|52|29|47|29|34|25|31|38|35|35|43|43|24|30|36|37|40|32|59|37|33|22|22|46|44|40|41|58|48|60|45|51|41|54|38|53|52|56|62|47|46|49|67|—|51|39|52|56|48|56|50|44|56|54|52|29|69|55|48|73|52|57|48|50|65|62|76|79|58|70|79|79|85|75|80|
| **arbok_muk_lase** |11|3|7|12|6|12|20|16|21|6|12|29|14|25|28|28|18|24|30|24|31|35|38|20|26|36|27|28|30|38|30|30|39|47|33|24|27|32|46|30|40|41|39|18|34|38|51|51|63|48|44|45|17|33|55|57|55|60|54|51|25|53|29|28|58|49|—|51|53|69|47|53|47|42|56|54|45|79|63|55|65|80|60|64|61|72|62|73|67|50|81|87|87|92|84|93|96|
| **stevens_carbin** |12|7|10|11|22|18|21|25|24|39|16|18|21|27|33|21|27|41|25|31|37|26|24|39|32|34|37|37|32|36|46|37|40|48|50|27|34|39|43|36|39|41|45|31|38|50|50|53|36|31|44|36|37|61|41|47|41|65|53|57|66|47|42|49|35|61|49|—|52|55|42|44|52|51|61|55|56|62|46|38|52|62|59|56|56|53|44|52|72|82|59|54|69|65|78|82|81|
| **arbok_muk_trol** |9|4|6|10|4|9|17|18|19|5|13|25|13|24|26|25|16|22|27|18|30|35|35|20|25|34|30|25|27|37|30|29|38|46|31|24|25|30|45|30|39|42|34|12|30|33|51|46|63|46|41|49|16|30|50|52|49|56|47|49|22|50|29|26|52|48|47|48|—|64|44|47|44|41|57|50|44|77|63|50|65|77|59|59|56|68|59|69|67|50|73|85|87|92|84|92|96|
| **hops_snorlax_s** |4|4|4|9|6|18|15|12|20|25|15|13|18|25|19|18|23|23|24|22|26|17|23|30|35|23|23|26|36|30|28|31|32|35|26|30|37|28|31|31|32|37|31|35|35|38|37|32|40|37|43|40|38|33|30|43|35|44|49|44|55|35|41|44|59|44|31|45|36|—|49|62|47|54|55|40|46|46|59|72|80|60|62|59|60|43|82|72|65|74|81|92|77|79|83|94|92|
| **salazzle_ex_te** |11|3|3|21|8|10|23|19|37|16|18|28|21|17|28|18|20|36|43|26|35|15|29|29|24|35|28|27|21|23|43|29|33|39|16|27|15|37|41|29|33|48|34|35|40|54|42|41|38|47|34|37|30|55|42|48|42|59|36|59|43|50|44|43|32|52|53|58|56|51|—|26|49|61|60|57|52|47|57|36|46|53|47|52|47|76|50|47|59|60|78|58|73|66|76|85|81|
| **hydreigon_graf** |1|3|3|11|4|12|21|8|20|7|12|7|13|29|28|19|19|8|15|11|20|42|24|33|36|29|14|54|52|25|16|48|28|31|33|53|22|23|44|32|42|28|33|25|51|21|50|44|59|35|52|53|54|18|49|24|54|30|30|32|36|63|38|39|33|44|47|56|53|38|74|—|66|43|30|50|69|60|57|44|65|74|56|44|71|36|68|46|57|52|72|86|80|81|80|94|89|
| **tr_crobat_abso** |2|7|7|9|15|18|17|26|18|18|20|23|18|22|23|18|23|15|34|32|24|26|28|26|25|29|28|21|28|40|38|30|31|36|28|25|24|38|38|33|36|40|34|36|37|30|38|40|54|37|37|34|42|28|48|34|53|42|50|35|36|48|41|44|42|50|53|48|56|53|51|34|—|44|47|56|50|56|54|54|50|50|54|59|57|59|57|60|60|52|74|59|85|76|81|88|89|
| **toxic_slumber_** |1|2|5|13|4|14|14|10|14|11|8|21|23|15|20|29|15|20|23|23|24|21|10|27|27|22|17|31|30|40|24|30|29|31|34|14|36|38|27|48|27|29|30|64|44|36|34|42|34|16|37|24|37|40|42|34|39|52|43|56|43|37|54|46|41|56|58|49|59|46|39|57|56|—|44|64|63|70|31|58|62|64|50|65|70|61|54|67|52|53|78|83|73|76|80|92|90|
| **team_rockets_s** |2|1|9|7|4|12|12|10|14|16|12|27|12|31|18|30|17|21|16|24|18|47|19|27|37|25|33|14|24|43|25|21|27|30|23|21|50|36|28|46|32|37|30|38|23|37|33|23|29|28|34|29|45|44|30|46|34|38|46|32|41|38|58|45|76|44|44|39|43|45|40|70|53|56|—|48|53|50|56|69|70|52|65|71|69|51|70|60|65|63|71|77|77|78|86|80|87|
| **arbok_team_roc** |9|1|4|9|4|8|17|16|14|5|11|23|10|18|26|24|10|18|22|20|27|30|29|15|18|31|22|20|24|29|26|26|33|43|26|24|27|33|41|28|37|38|36|12|32|32|45|44|59|42|38|44|9|26|47|54|47|48|45|44|18|43|26|28|51|46|46|45|50|60|43|50|44|36|52|—|42|70|61|48|66|73|56|60|59|62|51|67|64|48|76|84|87|87|86|84|95|
| **meta_ns_zoroar** |13|9|10|10|29|16|18|37|14|14|21|23|41|29|23|17|39|20|8|31|30|10|25|25|17|40|44|50|28|18|51|35|46|48|42|37|23|45|47|25|43|41|50|30|14|28|39|57|62|48|44|35|30|29|55|25|53|40|42|42|33|42|45|57|29|48|55|44|56|54|48|31|50|37|47|58|—|17|53|26|14|55|47|45|28|58|38|41|54|50|55|30|76|81|77|48|66|
| **mew_dbc_bastio** |1|2|2|7|2|28|6|43|15|30|11|4|16|20|10|68|14|48|24|19|19|10|13|21|18|13|29|56|46|11|30|56|29|28|11|71|23|16|23|18|25|56|29|12|27|59|25|65|71|33|54|26|27|66|16|42|18|54|63|48|49|32|24|36|19|71|21|38|23|54|53|40|44|30|50|30|83|—|47|33|55|72|70|31|55|29|47|37|51|87|50|82|55|69|71|84|77|
| **eerie_inferno_** |3|2|4|14|5|16|26|7|18|7|16|13|11|18|35|18|14|26|23|24|21|22|27|19|35|22|14|8|23|25|21|28|26|27|20|31|26|24|28|28|24|37|26|52|66|36|38|25|40|32|28|41|23|41|34|39|36|31|27|51|26|43|29|32|68|31|37|54|37|41|43|43|46|69|44|39|47|53|—|59|84|53|49|59|65|63|85|60|37|45|78|86|69|64|82|92|85|
| **chandelure_cen** |2|6|4|11|9|19|36|2|24|9|19|5|26|41|41|39|20|11|10|12|20|19|25|44|25|32|9|3|36|17|11|35|31|15|18|54|27|23|42|28|45|10|32|31|64|38|48|39|36|45|28|48|57|41|29|37|34|47|11|34|40|53|22|26|27|45|45|62|50|28|64|56|46|42|31|52|74|67|41|—|67|71|49|12|63|38|52|38|58|53|36|81|55|69|64|90|79|
| **study_centisko** |7|6|8|34|32|40|31|24|34|16|41|26|21|25|28|63|20|38|14|26|20|14|19|41|15|26|8|36|54|15|13|59|35|18|33|60|22|11|41|32|32|21|40|21|37|32|40|60|47|30|52|40|43|42|26|78|25|40|18|48|41|46|22|30|18|52|35|48|35|20|54|35|50|38|30|34|86|45|16|33|—|72|42|14|53|24|39|23|44|75|28|52|31|58|47|72|55|
| **trevenant_rapi** |4|3|6|15|6|16|18|11|22|12|26|15|10|27|23|14|22|21|24|14|32|44|32|21|22|28|34|52|60|28|28|62|26|43|32|36|16|16|37|25|26|24|42|22|20|28|57|29|54|36|73|52|47|25|37|41|39|33|41|54|40|54|32|40|22|27|20|38|23|40|47|26|50|36|48|27|45|28|47|29|28|—|57|51|54|58|40|27|47|61|51|45|70|80|69|87|65|
| **feraligatr_mun** |7|2|6|7|6|11|12|8|19|6|16|14|6|30|19|27|19|26|5|11|19|8|29|23|37|24|23|18|20|16|21|24|27|30|23|36|21|29|30|25|19|26|33|28|36|27|36|29|22|38|27|47|34|25|36|42|38|29|37|54|33|32|40|36|52|48|40|41|41|38|53|44|46|50|35|44|53|30|51|51|58|43|—|44|57|60|60|47|54|59|60|90|70|73|79|84|92|
| **darkness_mill_** |1|3|4|4|4|13|14|11|7|8|12|7|15|19|22|18|12|8|13|22|13|16|23|22|36|16|14|16|29|26|23|31|21|24|28|29|39|21|25|31|34|28|26|45|54|16|28|36|43|22|33|35|46|18|41|27|43|23|30|19|23|38|39|27|63|43|36|44|41|41|48|56|41|35|29|40|55|69|41|88|86|49|56|—|64|43|74|62|48|36|67|85|67|68|69|88|88|
| **study_hydreigo** |4|4|6|6|16|19|16|16|10|13|12|9|28|28|22|30|16|7|15|20|16|10|22|28|16|34|22|31|40|19|24|51|26|34|32|32|20|23|46|26|36|20|42|39|35|12|41|56|42|40|46|41|38|15|45|18|46|41|28|30|38|45|32|31|27|52|39|44|44|40|53|29|43|30|31|41|72|45|35|37|47|46|43|36|—|56|44|35|60|55|56|54|65|57|71|75|66|
| **orthworm_ex_me** |2|2|3|4|4|6|6|8|12|19|5|9|6|17|10|9|11|19|9|13|16|12|11|20|18|15|20|15|18|25|24|22|19|26|43|11|40|21|17|25|30|28|20|28|46|37|32|26|31|6|33|17|32|42|22|28|27|40|36|54|49|29|31|35|65|50|28|47|32|57|24|64|41|39|49|38|42|71|37|62|76|42|40|57|44|—|62|68|53|84|85|85|78|76|88|86|82|
| **chandelure_mau** |12|4|15|28|42|22|33|22|22|9|42|40|30|29|29|36|19|32|3|10|25|16|20|28|18|16|6|40|29|23|6|41|26|11|40|67|18|32|34|30|35|4|46|33|37|12|36|32|49|30|30|30|41|13|25|47|26|28|22|23|27|30|31|27|24|35|38|56|41|18|50|32|43|46|30|49|62|53|15|48|61|60|40|26|56|38|—|29|37|52|36|72|44|47|35|87|76|
| **study_maushold** |3|2|3|6|4|8|17|3|16|14|10|9|11|31|25|24|15|9|6|10|29|14|17|34|32|17|6|7|30|19|12|39|28|22|18|30|27|12|33|24|36|13|23|35|51|22|36|33|49|22|30|34|50|22|21|32|25|29|20|24|40|43|27|24|44|38|27|48|31|28|53|54|40|33|40|33|59|63|40|62|77|73|53|38|65|32|71|—|51|57|52|91|69|68|60|94|90|
| **crabominable_v** |4|4|7|10|7|13|11|9|16|22|12|12|14|25|16|11|20|22|18|16|16|13|41|16|30|21|24|22|20|21|20|24|28|41|22|49|29|26|23|27|23|17|25|25|27|28|35|20|26|51|37|55|28|26|19|27|20|34|31|39|45|30|38|38|52|24|33|28|33|35|41|43|40|48|35|36|46|49|63|42|56|53|46|52|40|47|63|49|—|74|50|62|62|72|77|77|68|
| **meta_festival_** |2|2|7|8|6|13|9|7|15|18|12|27|15|19|11|24|19|16|6|20|19|28|22|16|22|17|19|18|20|39|15|25|28|25|20|30|38|50|21|38|18|34|26|53|16|33|30|22|32|20|27|27|31|36|21|37|24|18|37|31|31|21|40|50|46|21|50|18|50|26|40|48|48|47|37|52|50|13|55|47|25|39|41|64|45|16|48|43|26|—|47|62|55|54|72|39|55|
| **tr_arbok_yvelt** |0|0|0|2|1|8|9|5|4|15|8|4|5|10|17|21|6|5|3|6|11|6|11|17|18|6|7|6|19|7|15|18|18|20|8|18|11|7|19|19|26|10|14|13|25|30|23|16|29|13|25|18|25|24|11|37|13|28|24|22|24|16|24|16|30|42|19|41|27|19|22|28|26|22|29|24|45|50|22|64|72|49|40|33|44|15|64|48|50|53|—|68|38|41|56|83|77|
| **study_flygon_s** |9|4|6|31|52|27|29|24|19|3|49|38|8|17|22|29|17|12|1|16|16|5|13|17|11|14|4|39|16|21|4|29|16|8|42|50|5|7|35|21|18|10|43|15|19|3|30|22|45|13|20|21|31|2|15|40|18|21|11|11|17|25|11|22|10|30|13|46|15|8|42|14|41|17|23|16|70|18|14|19|48|55|10|15|46|15|28|9|38|38|32|—|13|27|34|71|46|
| **team_rockets_w** |1|1|1|2|1|3|7|1|7|4|7|8|2|16|12|5|6|9|14|2|7|5|7|12|17|4|5|5|10|11|8|11|13|15|9|14|9|11|13|9|10|12|11|8|16|14|24|9|19|11|16|17|21|14|12|22|12|19|24|14|16|17|17|13|38|21|13|31|13|23|27|20|15|27|23|13|24|45|31|45|69|30|30|33|35|22|56|31|38|45|62|87|—|43|54|83|72|
| **mew_dbc_hypno** |1|0|1|2|1|2|3|2|6|5|3|7|2|18|6|4|5|6|10|4|9|6|9|6|14|3|6|3|14|13|9|12|12|19|10|13|4|6|15|9|18|8|12|5|21|10|27|14|34|10|18|19|17|6|11|17|14|13|18|19|18|17|14|15|22|21|8|35|8|21|34|19|24|24|22|13|19|31|36|31|42|20|27|32|43|24|53|32|28|46|59|73|57|—|45|92|71|
| **static_venom_d** |2|3|2|6|2|8|9|2|7|8|5|6|11|7|10|6|7|10|4|6|6|5|7|9|10|6|3|4|10|13|6|12|8|14|9|12|9|9|10|14|13|7|12|25|21|10|17|16|21|7|15|13|11|8|20|12|18|12|18|12|12|17|18|10|46|15|16|22|16|17|24|20|19|20|14|14|23|29|18|36|53|31|21|31|29|12|65|40|23|28|44|66|46|55|—|81|76|
| **mew_pikachu_bo** |0|37|1|7|6|11|2|0|36|6|29|2|7|8|3|26|3|1|4|2|8|2|3|17|3|2|1|3|9|5|1|16|10|7|2|11|1|8|13|6|13|4|5|4|7|2|28|19|14|3|12|8|23|2|11|34|10|7|11|4|17|35|6|6|2|25|7|18|8|6|15|6|12|8|20|16|52|16|8|10|28|13|16|12|25|14|13|6|23|61|17|29|17|8|19|—|24|
| **mew_baby_box** |0|1|1|2|0|1|3|1|8|2|2|4|3|9|5|4|3|2|2|1|4|3|2|7|3|3|3|1|6|5|4|12|6|10|4|6|3|2|12|6|10|2|4|9|14|3|17|12|10|6|10|8|12|2|4|6|6|15|6|7|14|13|14|5|8|20|4|19|4|8|19|11|11|10|13|5|34|23|15|21|45|35|8|12|34|18|24|10|32|45|23|54|28|29|24|76|—|
