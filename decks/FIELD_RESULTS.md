# Field results — every deck against every other deck

Full round robin over **57 decks**, **1000 games** per pairing, 1596 pairings, 1,596,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-29. **These supersede every number in the deck files before this date.**

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

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `tauros_risky_ruins` | **73.0%** | 76.7% | 51/56 | study_flygon_sandy_flapping_mill (97%) | lurantis_heal_punish (39%) |
| 2 | `ns_zoroark_night_joker_toolbox` | **72.3%** | 75.8% | 52/56 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | tauros_risky_ruins (24%) |
| 3 | `ditto_transform_hydreigon` | **69.8%** | 71.0% | 50/56 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | team_rockets_persian_ex_attack_theft (34%) |
| 4 | `team_rockets_persian_ex_attack_theft` | **69.5%** | 70.4% | 53/56 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | ns_zoroark_night_joker_toolbox (43%) |
| 5 | `maushold_gnaw_together_mill` | **68.6%** | 71.1% | 50/56 | static_venom_drapion (91%) | tauros_risky_ruins (34%) |
| 6 | `lurantis_heal_punish` | **68.0%** | 67.9% | 51/56 | darkness_mill_hand_lock (94%) | scovillain_salazzle_spicy_rage (40%) |
| 7 | `ditto_tyranitar_gengar_hydreigon` | **65.7%** | 68.5% | 46/56 | team_rockets_wobbuffet_orbeetle_damage_launder (94%) | lurantis_heal_punish (32%) |
| 8 | `tr_spidops_mewtwo_hammer` | **64.4%** | 65.8% | 50/56 | static_venom_drapion (89%) | tauros_risky_ruins (34%) |
| 9 | `study_mega_excadrill_drill_mill` | **63.5%** | 63.9% | 48/56 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | ditto_transform_hydreigon (23%) |
| 10 | `krookodile_ex_relicanth_hand_disruption` | **60.6%** | 62.2% | 40/56 | team_rockets_wobbuffet_orbeetle_damage_launder (94%) | lurantis_heal_punish (28%) |
| 11 | `wugtrio_paralysis_pin` | **60.5%** | 62.7% | 38/56 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | ns_zoroark_night_joker_toolbox (18%) |
| 12 | `cradily_accelgor_conditions` | **59.4%** | 57.1% | 41/56 | study_flygon_sandy_flapping_mill (96%) | wugtrio_paralysis_pin (36%) |
| 13 | `scovillain_salazzle_spicy_rage` | **59.3%** | 61.5% | 41/56 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | maushold_gnaw_together_mill (23%) |
| 14 | `panic_poison_paralysis` | **59.0%** | 59.2% | 38/56 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | kangaskhan_tyrantrum_flip_mill (21%) |
| 15 | `meta_mega_excadrill` | **58.0%** | 59.4% | 44/56 | static_venom_drapion (87%) | ditto_transform_hydreigon (22%) |
| 16 | `team_rockets_koffing_weezing_bench_swarm` | **57.3%** | 58.0% | 36/56 | static_venom_drapion (91%) | ns_zoroark_night_joker_toolbox (20%) |
| 17 | `mega_lopunny_dusknoir_snipe_finisher` | **57.1%** | 56.4% | 39/56 | static_venom_drapion (86%) | ns_zoroark_night_joker_toolbox (24%) |
| 18 | `cradily_amoonguss_conditions` | **56.6%** | 52.7% | 32/56 | study_flygon_sandy_flapping_mill (97%) | study_mega_excadrill_drill_mill (26%) |
| 19 | `mega_chandelure_ex_retreat_tax` | **55.8%** | 59.5% | 34/56 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | tauros_risky_ruins (15%) |
| 20 | `kangaskhan_tyrantrum_flip_mill` | **55.6%** | 57.8% | 38/56 | static_venom_drapion (89%) | tauros_risky_ruins (11%) |
| 21 | `meta_raging_bolt` | **55.5%** | 56.2% | 42/56 | static_venom_drapion (79%) | maushold_gnaw_together_mill (18%) |
| 22 | `heracross_sinistcha_tea` | **54.2%** | 52.3% | 35/56 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | scovillain_salazzle_spicy_rage (28%) |
| 23 | `meta_slowking` | **53.8%** | 55.0% | 35/56 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | tauros_risky_ruins (15%) |
| 24 | `meta_dragapult_blaziken` | **52.2%** | 53.0% | 35/56 | static_venom_drapion (82%) | ns_zoroark_night_joker_toolbox (22%) |
| 25 | `meta_dragapult_pure` | **51.0%** | 50.8% | 29/56 | team_rockets_wobbuffet_orbeetle_damage_launder (85%) | ns_zoroark_night_joker_toolbox (22%) |
| 26 | `decidueye_ex_judge_sniper_lock` | **50.8%** | 51.8% | 30/56 | static_venom_drapion (86%) | tauros_risky_ruins (11%) |
| 27 | `veluza_sinistcha_ex_tea_service` | **50.8%** | 48.5% | 26/56 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | study_mega_excadrill_drill_mill (17%) |
| 28 | `metal_metang_excadrill` | **50.7%** | 51.5% | 29/56 | static_venom_drapion (82%) | ditto_transform_hydreigon (16%) |
| 29 | `water_aggro` | **50.5%** | 49.6% | 28/56 | chandelure_centiskorch_deck_out (88%) | tauros_risky_ruins (10%) |
| 30 | `kyurem_vanilluxe_blizzard` | **49.3%** | 48.8% | 27/56 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | ns_zoroark_night_joker_toolbox (17%) |
| 31 | `orthworm_ex_metal_retaliation` | **49.2%** | 47.6% | 25/56 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | ns_zoroark_night_joker_toolbox (12%) |
| 32 | `arbok_muk_laser_darkbell` | **48.7%** | 49.1% | 27/56 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | kangaskhan_tyrantrum_flip_mill (20%) |
| 33 | `dhelmise_veluza_hide_n_sneak` | **48.6%** | 48.5% | 24/56 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | study_mega_excadrill_drill_mill (21%) |
| 34 | `toxic_slumber_vileplume_ex` | **48.4%** | 48.1% | 26/56 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | ditto_transform_hydreigon (21%) |
| 35 | `team_rockets_spidops_swarm` | **46.6%** | 43.4% | 20/56 | static_venom_drapion (83%) | tauros_risky_ruins (19%) |
| 36 | `arbok_muk_trolley_darkbell` | **46.2%** | 47.0% | 22/56 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | kangaskhan_tyrantrum_flip_mill (18%) |
| 37 | `mega_scrafty_ex_darkness_tank` | **45.6%** | 44.6% | 23/56 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | lurantis_heal_punish (15%) |
| 38 | `arbok_team_rockets_muk_condition_stack` | **45.2%** | 44.9% | 19/56 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | kangaskhan_tyrantrum_flip_mill (12%) |
| 39 | `meta_dragapult_dusknoir` | **45.0%** | 44.2% | 17/56 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | ns_zoroark_night_joker_toolbox (14%) |
| 40 | `stevens_carbink_damage_wall` | **44.9%** | 43.8% | 20/56 | meta_festival_lead (86%) | ns_zoroark_night_joker_toolbox (16%) |
| 41 | `study_maushold_gnaw_latias` | **44.8%** | 44.0% | 20/56 | study_flygon_sandy_flapping_mill (89%) | tauros_risky_ruins (9%) |
| 42 | `hops_snorlax_stacked_buff` | **44.6%** | 41.3% | 16/56 | study_flygon_sandy_flapping_mill (89%) | ns_zoroark_night_joker_toolbox (17%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **44.2%** | 42.5% | 15/56 | study_flygon_sandy_flapping_mill (87%) | tauros_risky_ruins (9%) |
| 44 | `chandelure_centiskorch_deck_out` | **43.8%** | 44.5% | 21/56 | study_flygon_sandy_flapping_mill (80%) | tauros_risky_ruins (9%) |
| 45 | `tr_crobat_absol_bench_snipe` | **43.5%** | 46.0% | 16/56 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | lurantis_heal_punish (15%) |
| 46 | `eerie_inferno_ninetales_burn` | **39.8%** | 36.5% | 11/56 | study_flygon_sandy_flapping_mill (83%) | wugtrio_paralysis_pin (10%) |
| 47 | `crabominable_veluza_food_prep` | **38.3%** | 36.8% | 10/56 | static_venom_drapion (77%) | ns_zoroark_night_joker_toolbox (13%) |
| 48 | `darkness_mill_hand_lock` | **37.8%** | 35.5% | 11/56 | study_centiskorch_bastiodon_mill (89%) | lurantis_heal_punish (6%) |
| 49 | `tr_arbok_yveltal_snow_coating` | **37.7%** | 34.4% | 13/56 | study_centiskorch_bastiodon_mill (86%) | tauros_risky_ruins (4%) |
| 50 | `meta_ns_zoroark` | **37.0%** | 40.2% | 12/56 | static_venom_drapion (75%) | ditto_transform_hydreigon (10%) |
| 51 | `study_hydreigon_zweilous_mill` | **36.4%** | 34.2% | 9/56 | meta_ns_zoroark (72%) | ditto_transform_hydreigon (11%) |
| 52 | `study_centiskorch_bastiodon_mill` | **35.4%** | 33.5% | 10/56 | meta_ns_zoroark (81%) | ditto_tyranitar_gengar_hydreigon (9%) |
| 53 | `meta_festival_lead` | **29.9%** | 29.1% | 4/56 | static_venom_drapion (63%) | tauros_risky_ruins (6%) |
| 54 | `salazzle_ex_team_rockets_muk_condition_stack` | **28.3%** | 28.2% | 2/56 | meta_festival_lead (58%) | ditto_transform_hydreigon (10%) |
| 55 | `study_flygon_sandy_flapping_mill` | **27.8%** | 22.0% | 5/56 | meta_ns_zoroark (76%) | cradily_amoonguss_conditions (3%) |
| 56 | `static_venom_drapion` | **20.6%** | 17.4% | 4/56 | study_flygon_sandy_flapping_mill (61%) | tauros_risky_ruins (6%) |
| 57 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **19.1%** | 15.4% | 3/56 | study_flygon_sandy_flapping_mill (79%) | ns_zoroark_night_joker_toolbox (4%) |

## Full matrix

Row's win rate against column.

| |tauros_risky_r|ns_zoroark_nig|ditto_transfor|team_rockets_p|maushold_gnaw_|lurantis_heal_|ditto_tyranita|tr_spidops_mew|study_mega_exc|krookodile_ex_|wugtrio_paraly|cradily_accelg|scovillain_sal|panic_poison_p|meta_mega_exca|team_rockets_k|mega_lopunny_d|cradily_amoong|mega_chandelur|kangaskhan_tyr|meta_raging_bo|heracross_sini|meta_slowking|meta_dragapult|meta_dragapult|decidueye_ex_j|veluza_sinistc|metal_metang_e|water_aggro|kyurem_vanillu|orthworm_ex_me|arbok_muk_lase|dhelmise_veluz|toxic_slumber_|team_rockets_s|arbok_muk_trol|mega_scrafty_e|arbok_team_roc|meta_dragapult|stevens_carbin|study_maushold|hops_snorlax_s|feraligatr_mun|chandelure_cen|tr_crobat_abso|eerie_inferno_|crabominable_v|darkness_mill_|tr_arbok_yvelt|meta_ns_zoroar|study_hydreigo|study_centisko|meta_festival_|salazzle_ex_te|study_flygon_s|static_venom_d|team_rockets_w|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **tauros_risky_r** |—|76|40|56|66|39|50|66|48|60|61|58|66|66|48|76|51|61|85|89|78|52|85|61|57|89|56|54|90|57|83|74|57|79|81|76|84|80|65|82|91|77|91|91|70|81|81|88|96|89|87|90|94|83|97|94|89|
| **ns_zoroark_nig** |24|—|60|57|62|42|64|54|41|62|82|57|65|72|68|80|76|66|75|77|59|63|77|78|78|55|79|77|84|83|88|76|76|69|73|80|81|75|86|84|75|83|68|62|85|82|87|87|84|85|78|45|78|88|68|93|96|
| **ditto_transfor** |60|40|—|34|63|37|48|47|77|66|66|53|66|51|78|68|53|55|69|68|60|50|80|71|71|43|57|84|77|76|77|63|69|79|51|68|79|67|72|78|76|83|86|68|77|83|84|87|88|90|89|85|75|90|90|93|95|
| **team_rockets_p** |44|43|66|—|54|58|60|54|44|68|58|63|57|62|56|66|60|71|52|71|57|72|63|61|69|76|68|62|72|70|77|70|74|78|78|70|78|71|72|68|68|76|74|76|78|80|80|90|83|73|82|84|81|82|83|92|95|
| **maushold_gnaw_** |34|38|37|46|—|57|45|43|54|53|68|59|77|68|72|60|50|59|65|65|82|71|77|69|68|75|56|75|65|75|82|75|54|76|64|77|76|82|71|75|65|71|60|77|80|73|71|72|83|84|82|90|82|88|89|91|90|
| **lurantis_heal_** |61|58|63|42|43|—|68|52|46|72|62|61|40|63|52|67|56|63|50|59|48|64|55|51|65|82|64|60|73|69|64|73|76|74|69|72|85|74|68|61|85|71|61|88|85|73|71|94|91|75|88|74|77|80|88|91|92|
| **ditto_tyranita** |50|36|52|40|55|32|—|44|76|57|56|48|60|56|64|65|48|49|60|70|43|36|63|68|68|42|53|71|70|71|68|63|70|65|58|72|73|74|71|71|78|75|80|83|63|79|82|80|91|82|81|91|69|88|84|87|94|
| **tr_spidops_mew** |34|46|53|46|57|48|56|—|36|61|60|59|57|58|55|54|56|66|45|65|60|68|68|61|67|60|72|62|68|62|71|63|73|71|71|68|75|69|72|62|56|71|67|56|72|76|83|74|72|79|72|62|83|76|76|89|85|
| **study_mega_exc** |52|59|23|56|46|54|24|64|—|39|73|58|41|54|60|51|59|74|67|61|54|68|64|59|74|53|83|70|59|78|56|71|79|63|77|77|55|74|74|70|46|74|62|36|71|45|82|51|76|89|72|69|86|84|76|77|89|
| **krookodile_ex_** |40|38|34|32|47|28|43|39|61|—|47|41|50|58|50|60|52|47|63|60|43|41|58|59|62|41|55|54|67|68|67|72|68|52|53|74|68|74|62|75|73|72|77|67|71|76|72|72|73|78|78|71|69|86|81|83|94|
| **wugtrio_paraly** |39|18|34|42|32|38|44|40|27|53|—|64|40|64|37|63|42|65|45|46|48|51|53|51|49|76|64|50|68|61|64|74|65|54|74|73|71|77|63|62|84|73|76|88|69|90|74|83|85|44|60|68|84|87|56|92|96|
| **cradily_accelg** |42|43|47|37|41|39|52|41|42|59|36|—|38|52|46|53|48|50|56|41|56|54|52|49|52|64|52|56|62|59|54|67|60|61|64|68|73|69|54|61|71|67|70|58|79|67|71|85|54|80|85|74|70|74|96|87|90|
| **scovillain_sal** |34|35|34|43|23|60|40|43|59|50|60|62|—|53|67|63|62|70|33|49|59|72|59|55|59|60|61|68|41|35|84|73|65|77|71|71|71|73|66|80|54|65|54|32|75|66|48|64|75|68|67|42|73|82|37|86|87|
| **panic_poison_p** |34|28|49|38|32|37|44|42|46|42|36|48|47|—|48|52|48|42|66|21|49|65|55|51|55|66|60|61|57|57|67|66|64|53|58|69|59|68|64|66|75|72|67|72|67|77|70|80|81|52|76|88|61|82|91|92|92|
| **meta_mega_exca** |52|32|22|44|28|48|36|45|40|50|63|54|33|52|—|49|57|66|32|50|51|69|51|54|61|51|74|61|66|75|68|61|57|61|71|64|66|67|67|56|56|68|60|46|62|59|78|70|78|72|65|51|86|69|55|87|81|
| **team_rockets_k** |24|20|32|34|40|33|35|46|49|40|37|47|37|48|51|—|45|50|64|42|47|51|54|48|49|65|65|61|55|52|58|63|68|64|58|64|58|62|55|63|75|62|65|77|60|70|76|78|79|60|76|84|68|76|89|91|90|
| **mega_lopunny_d** |49|24|47|40|50|44|52|44|41|48|58|52|38|52|43|55|—|53|57|47|46|47|46|48|53|59|48|51|60|54|61|58|54|65|68|61|62|61|59|56|66|62|68|78|62|72|58|74|66|51|59|70|74|70|86|86|86|
| **cradily_amoong** |39|34|45|29|41|37|51|34|26|53|35|50|30|58|34|50|47|—|55|41|48|49|45|46|49|52|46|45|63|51|45|70|50|59|58|72|75|72|55|48|74|67|68|60|76|63|69|87|64|76|83|65|70|78|97|90|93|
| **mega_chandelur** |15|25|31|48|35|50|40|55|33|37|55|44|67|34|68|36|43|45|—|73|49|68|48|58|52|77|68|74|66|68|59|35|62|68|66|37|55|41|60|70|48|64|74|63|49|64|74|64|63|45|60|64|69|80|61|79|84|
| **kangaskhan_tyr** |11|23|32|29|35|41|30|35|39|40|54|59|51|79|50|58|53|59|27|—|44|47|50|59|54|38|62|51|54|59|62|80|54|65|62|82|58|88|63|68|39|63|60|36|58|77|73|54|72|73|62|54|74|82|62|89|81|
| **meta_raging_bo** |22|41|40|43|18|52|57|40|46|57|52|44|41|51|49|53|54|52|51|56|—|50|58|56|56|50|62|60|61|66|58|47|55|67|65|47|65|54|64|60|52|62|59|48|62|64|66|70|76|59|59|53|75|66|63|79|77|
| **heracross_sini** |48|37|50|28|29|36|64|32|32|59|49|46|28|35|31|49|53|51|32|53|50|—|51|45|51|48|52|39|52|62|49|51|50|51|60|54|76|58|58|57|73|60|41|58|70|55|66|82|67|67|76|62|74|68|84|85|89|
| **meta_slowking** |15|23|20|37|23|45|37|32|36|42|47|48|41|45|49|46|54|55|52|50|42|49|—|59|53|45|59|52|64|59|62|56|56|64|64|57|59|63|61|66|49|69|60|45|55|64|67|66|80|68|56|53|83|72|71|83|84|
| **meta_dragapult** |39|22|29|39|31|49|32|39|41|41|49|51|45|49|46|52|52|54|42|41|44|55|41|—|54|66|56|51|58|54|57|54|51|59|68|54|59|58|61|51|49|57|60|52|56|65|60|63|69|56|43|40|73|65|58|82|82|
| **meta_dragapult** |43|22|29|31|32|35|32|33|26|38|51|48|41|45|39|51|47|51|48|46|44|49|47|46|—|58|48|48|61|53|52|52|56|49|64|54|51|57|59|47|54|55|60|52|57|69|64|59|68|64|45|43|80|70|66|81|85|
| **decidueye_ex_j** |11|45|57|24|25|18|58|40|47|59|24|36|40|34|49|35|41|48|23|62|50|52|55|34|42|—|57|54|45|57|60|44|53|66|52|47|73|46|49|54|64|58|51|54|64|62|69|72|40|76|79|22|68|72|55|86|86|
| **veluza_sinistc** |44|21|43|32|44|36|47|28|17|45|36|48|39|40|26|35|52|54|32|38|38|48|41|44|52|43|—|33|48|49|49|55|48|46|59|52|70|57|62|40|66|58|59|55|67|72|61|73|69|58|58|63|85|62|75|84|86|
| **metal_metang_e** |46|23|16|38|25|40|29|38|30|46|50|44|32|39|39|39|49|55|26|49|40|61|48|49|52|46|67|—|57|69|62|48|54|54|63|54|58|53|63|45|48|63|53|42|52|55|67|64|71|63|54|51|81|61|55|82|80|
| **water_aggro** |10|16|23|28|35|27|30|32|41|33|32|38|59|43|34|45|40|37|34|46|39|48|36|42|39|55|52|43|—|48|55|50|48|53|50|54|56|54|49|55|72|52|59|88|54|72|65|76|68|60|70|86|71|78|88|82|80|
| **kyurem_vanillu** |43|17|24|30|25|31|29|38|22|32|39|41|65|43|25|48|46|49|32|41|34|38|41|46|47|43|51|31|52|—|34|52|51|51|67|52|54|56|57|43|68|58|52|70|53|75|64|68|74|47|55|71|76|80|52|87|91|
| **orthworm_ex_me** |17|12|23|23|18|36|32|29|44|33|36|46|16|33|32|42|39|55|41|38|42|51|38|43|48|40|51|38|45|66|—|42|57|49|60|48|47|52|52|58|74|67|52|73|53|55|62|69|86|47|50|80|89|64|84|83|90|
| **arbok_muk_lase** |26|24|37|30|25|27|37|37|29|28|26|33|27|34|39|37|42|30|65|20|53|49|44|46|48|56|45|52|50|48|58|—|48|40|55|51|41|51|54|54|63|66|58|56|53|64|62|65|59|52|74|72|60|72|85|81|93|
| **dhelmise_veluz** |43|24|31|26|46|24|30|27|21|32|35|40|35|36|43|32|46|50|38|46|45|50|44|49|44|47|52|46|52|49|43|52|—|42|55|54|49|58|56|45|58|55|48|52|54|69|71|58|53|66|52|54|81|72|69|84|84|
| **toxic_slumber_** |21|31|21|22|24|26|35|29|37|48|46|39|23|47|39|36|35|41|32|35|33|49|36|41|51|34|54|46|47|49|51|60|58|—|47|64|66|61|54|61|57|55|51|51|54|38|57|72|76|56|71|68|63|67|82|80|84|
| **team_rockets_s** |19|27|49|22|36|31|42|29|23|47|26|36|29|42|29|42|32|42|34|38|35|40|36|32|36|48|41|37|50|33|40|45|45|53|—|48|63|50|42|44|55|52|61|70|56|60|58|74|57|60|66|69|67|65|78|83|82|
| **arbok_muk_trol** |24|20|32|30|23|28|28|32|23|26|27|32|29|31|36|36|39|28|63|18|53|46|43|46|46|53|48|46|46|48|52|49|46|36|52|—|40|52|52|49|60|63|57|48|51|61|60|60|55|48|71|66|58|67|83|79|93|
| **mega_scrafty_e** |16|19|21|22|24|15|27|25|45|32|29|27|29|41|34|42|38|25|45|42|35|24|41|41|49|27|30|42|44|46|53|59|51|34|37|60|—|63|48|59|58|54|54|66|54|68|62|55|54|59|69|74|61|74|85|79|87|
| **arbok_team_roc** |20|25|33|29|18|26|26|31|26|26|23|31|27|32|33|38|39|28|59|12|46|42|37|42|43|54|43|47|46|44|48|49|42|39|50|48|37|—|53|52|60|59|57|50|50|59|55|65|55|49|71|71|59|69|85|83|91|
| **meta_dragapult** |35|14|28|28|29|32|29|28|26|38|37|46|34|36|33|45|41|45|40|37|36|42|39|39|41|51|38|37|51|43|48|46|44|46|58|48|52|47|—|42|53|45|57|56|51|61|50|58|62|49|45|41|70|65|64|79|84|
| **stevens_carbin** |18|16|22|32|25|39|29|38|30|25|38|39|20|34|44|37|44|52|30|32|40|43|34|49|53|46|60|55|45|57|42|46|55|39|56|51|41|48|58|—|44|52|42|40|50|40|65|50|41|56|55|61|86|65|56|72|77|
| **study_maushold** |9|25|24|32|35|15|22|44|54|27|16|29|46|25|44|25|34|26|52|61|48|27|51|51|46|36|34|52|28|32|26|37|42|43|45|40|42|40|47|56|—|42|59|69|45|53|58|46|51|70|73|85|71|81|89|70|81|
| **hops_snorlax_s** |23|17|17|24|29|29|25|29|26|28|27|33|35|28|32|38|38|33|36|37|38|40|31|43|45|42|42|37|48|42|33|34|45|45|48|37|46|41|55|48|58|—|56|66|48|60|62|57|65|59|58|83|75|75|89|83|80|
| **feraligatr_mun** |9|32|14|26|40|39|20|33|38|23|24|30|46|33|40|35|32|32|26|40|41|59|40|40|40|49|41|47|41|48|48|42|52|49|39|43|46|43|43|58|41|44|—|52|51|57|54|44|46|62|59|72|63|72|87|76|75|
| **chandelure_cen** |9|38|32|24|23|12|17|44|64|33|12|42|68|28|54|23|22|40|37|64|52|42|55|48|48|46|45|58|12|30|27|44|48|49|30|52|34|50|44|60|31|34|48|—|51|56|55|17|25|79|66|77|64|79|80|62|71|
| **tr_crobat_abso** |30|15|23|22|20|15|37|28|29|29|31|21|25|33|38|40|38|24|51|42|38|30|45|44|43|36|33|48|46|47|47|47|46|46|44|49|46|50|49|50|55|52|49|49|—|55|60|59|58|56|69|56|54|67|58|80|86|
| **eerie_inferno_** |19|18|17|20|27|27|21|24|55|24|10|33|34|23|41|30|28|37|36|23|36|45|36|35|31|38|28|45|28|25|45|36|31|62|40|39|32|41|39|60|47|40|43|44|45|—|36|55|55|46|65|79|48|69|83|76|74|
| **crabominable_v** |19|13|16|20|29|29|18|17|18|28|26|29|52|30|22|24|42|31|26|27|34|34|33|40|36|31|39|33|35|36|38|38|29|43|42|40|38|45|50|35|42|38|46|45|40|64|—|52|48|52|46|59|76|63|62|77|67|
| **darkness_mill_** |12|13|13|10|28|6|20|26|49|28|17|15|36|20|30|22|26|13|36|46|30|18|34|37|41|28|27|36|24|32|31|35|42|28|26|40|45|35|42|50|54|43|56|83|41|45|48|—|54|56|66|89|40|72|82|70|74|
| **tr_arbok_yvelt** |4|16|12|17|17|9|9|28|24|27|15|46|25|19|22|21|34|36|37|28|24|33|20|31|32|60|31|29|32|26|14|41|47|24|43|45|46|45|38|59|49|35|54|75|42|45|52|46|—|58|59|86|68|58|78|66|72|
| **meta_ns_zoroar** |11|15|10|27|16|25|18|21|11|22|56|20|32|48|28|40|49|24|55|27|41|33|32|44|36|24|42|37|40|53|53|48|34|44|40|52|41|51|51|44|30|41|38|21|44|54|48|44|42|—|28|19|52|54|24|75|66|
| **study_hydreigo** |13|22|11|18|18|12|19|28|28|22|40|15|33|24|35|24|41|17|40|38|41|24|44|57|55|21|42|46|30|45|50|26|48|29|34|29|31|29|55|45|27|42|41|34|31|35|54|34|41|72|—|49|61|59|44|70|68|
| **study_centisko** |10|55|15|16|10|26|9|38|31|29|32|26|58|12|49|16|30|35|36|46|47|38|47|60|57|78|37|49|14|29|20|28|46|32|31|34|26|29|59|39|15|17|28|23|44|21|41|11|14|81|51|—|75|61|44|41|37|
| **meta_festival_** |6|22|25|19|18|23|31|17|14|31|16|30|27|39|14|32|26|30|31|26|25|26|17|27|20|32|15|19|29|24|11|40|19|37|33|42|39|41|30|14|29|25|37|36|46|52|24|60|32|48|39|25|—|42|51|63|49|
| **salazzle_ex_te** |17|12|10|18|12|20|12|24|16|14|13|26|18|18|31|24|30|22|20|18|34|32|28|35|30|28|38|39|22|20|36|28|28|33|35|33|26|31|35|35|19|25|28|21|33|31|37|28|42|46|41|39|58|—|33|47|53|
| **study_flygon_s** |3|32|10|17|11|12|16|24|24|19|44|4|63|9|45|11|14|3|39|38|37|16|29|42|34|45|25|45|12|48|16|15|31|18|22|17|15|15|36|44|11|11|13|20|42|17|38|18|22|76|56|56|49|67|—|39|21|
| **static_venom_d** |6|7|7|8|9|9|13|11|23|17|8|13|14|8|13|9|14|10|21|11|21|15|17|18|19|14|16|18|18|13|17|19|16|20|17|21|21|17|21|28|30|17|24|38|20|24|23|30|34|25|30|59|37|53|61|—|52|
| **team_rockets_w** |11|4|5|5|10|8|6|15|11|6|4|10|13|8|19|10|14|7|16|19|23|11|16|18|15|14|14|20|20|9|10|7|16|16|18|7|13|9|16|23|19|20|25|29|14|26|33|26|28|34|32|63|51|47|79|48|—|
