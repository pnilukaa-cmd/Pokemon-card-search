# Field results — every deck against every other deck

Full round robin over **55 decks**, **1000 games** per pairing, 1485 pairings, 1,485,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-27. **These supersede every number in the deck files before this date.**

## What changed since the 2026-09-23 table

**The field.** 55 decks: the 54 of the previous run plus the user's
`ditto_tyranitar_gengar_hydreigon`. Same per-pair seeds (`rr1`), so a deck
in both runs faces the same dice against the same opponent.

**The engine** (commit in `ENGINE_COMMIT`). Every number in the previous
table predates all of these, so no deck's old figure is comparable:

- **Rules now enforced:** no Supporter on the first turn going first;
  no evolving on either player's first turn; no Stadium over one of the
  same name; mulligan extra draws.
- **Card conservation:** Knock Outs discard Energy, Tools and the
  Evolution stack; Stadium replacement; attack Bench searches;
  Run Away Draw no longer duplicates Dudunsparce (this inflated the
  Dudunsparce wall).
- **Deck orientation:** Seek Inspiration and the self-mill scalers read
  the top of the deck, not the bottom.
- **No peeking:** choosing an attack no longer reads hidden cards.
- **Every card effect modelled** (`audit_unmodeled.py`: 0): on-play and
  when-damaged Abilities, Prize modifiers, 66 attack texts, situational
  Trainers, Ability locks, 19 Tools, Special Energy and Stadium gaps.
- **Pilot (default greedy):** Basics and Items that reach the hand after
  the Supporter are played that turn; Rare Candy before Stage 1s.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `tauros_risky_ruins` | **73.5%** | 78.1% | 50/54 | study_flygon_sandy_flapping_mill (97%) | lurantis_heal_punish (40%) |
| 2 | `ns_zoroark_night_joker_toolbox` | **72.7%** | 75.7% | 50/54 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | tauros_risky_ruins (25%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **69.6%** | 70.4% | 50/54 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | tauros_risky_ruins (41%) |
| 4 | `maushold_gnaw_together_mill` | **69.2%** | 70.2% | 50/54 | static_venom_drapion (90%) | tauros_risky_ruins (33%) |
| 5 | `lurantis_heal_punish` | **68.4%** | 68.7% | 49/54 | darkness_mill_hand_lock (94%) | scovillain_salazzle_spicy_rage (40%) |
| 6 | `ditto_tyranitar_gengar_hydreigon` | **66.0%** | 68.3% | 46/54 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | lurantis_heal_punish (28%) |
| 7 | `study_mega_excadrill_drill_mill` | **64.1%** | 65.5% | 47/54 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | ditto_tyranitar_gengar_hydreigon (25%) |
| 8 | `krookodile_ex_relicanth_hand_disruption` | **61.4%** | 62.6% | 40/54 | team_rockets_wobbuffet_orbeetle_damage_launder (94%) | lurantis_heal_punish (28%) |
| 9 | `wugtrio_paralysis_pin` | **61.3%** | 62.7% | 38/54 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | ns_zoroark_night_joker_toolbox (18%) |
| 10 | `cradily_accelgor_conditions` | **59.8%** | 57.1% | 40/54 | study_flygon_sandy_flapping_mill (96%) | wugtrio_paralysis_pin (36%) |
| 11 | `scovillain_salazzle_spicy_rage` | **59.7%** | 61.0% | 41/54 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | maushold_gnaw_together_mill (21%) |
| 12 | `panic_poison_paralysis` | **59.2%** | 57.5% | 38/54 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | kangaskhan_tyrantrum_flip_mill (21%) |
| 13 | `meta_mega_excadrill` | **58.8%** | 60.5% | 44/54 | static_venom_drapion (87%) | maushold_gnaw_together_mill (30%) |
| 14 | `team_rockets_koffing_weezing_bench_swarm` | **57.6%** | 58.3% | 36/54 | static_venom_drapion (91%) | ns_zoroark_night_joker_toolbox (20%) |
| 15 | `mega_lopunny_dusknoir_snipe_finisher` | **57.4%** | 56.5% | 39/54 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | ns_zoroark_night_joker_toolbox (24%) |
| 16 | `cradily_amoonguss_conditions` | **57.0%** | 54.2% | 31/54 | study_flygon_sandy_flapping_mill (97%) | study_mega_excadrill_drill_mill (26%) |
| 17 | `mega_chandelure_ex_retreat_tax` | **56.1%** | 59.7% | 33/54 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | tauros_risky_ruins (15%) |
| 18 | `kangaskhan_tyrantrum_flip_mill` | **56.0%** | 57.8% | 38/54 | static_venom_drapion (89%) | tauros_risky_ruins (10%) |
| 19 | `meta_raging_bolt` | **55.6%** | 56.1% | 42/54 | static_venom_drapion (79%) | maushold_gnaw_together_mill (16%) |
| 20 | `meta_slowking` | **54.6%** | 55.0% | 35/54 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | tauros_risky_ruins (17%) |
| 21 | `heracross_sinistcha_tea` | **54.5%** | 52.5% | 34/54 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | scovillain_salazzle_spicy_rage (28%) |
| 22 | `veluza_sinistcha_ex_tea_service` | **53.6%** | 52.5% | 32/54 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | study_mega_excadrill_drill_mill (23%) |
| 23 | `meta_dragapult_blaziken` | **53.0%** | 53.7% | 36/54 | static_venom_drapion (82%) | ns_zoroark_night_joker_toolbox (22%) |
| 24 | `dhelmise_veluza_hide_n_sneak` | **52.2%** | 51.7% | 30/54 | static_venom_drapion (87%) | study_mega_excadrill_drill_mill (24%) |
| 25 | `meta_dragapult_pure` | **51.4%** | 50.5% | 28/54 | team_rockets_wobbuffet_orbeetle_damage_launder (85%) | ns_zoroark_night_joker_toolbox (22%) |
| 26 | `metal_metang_excadrill` | **51.3%** | 51.5% | 29/54 | static_venom_drapion (82%) | ns_zoroark_night_joker_toolbox (23%) |
| 27 | `water_aggro` | **51.2%** | 49.6% | 27/54 | chandelure_centiskorch_deck_out (88%) | tauros_risky_ruins (12%) |
| 28 | `decidueye_ex_judge_sniper_lock` | **50.5%** | 51.2% | 28/54 | static_venom_drapion (86%) | tauros_risky_ruins (11%) |
| 29 | `kyurem_vanilluxe_blizzard` | **49.8%** | 48.8% | 25/54 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | ns_zoroark_night_joker_toolbox (17%) |
| 30 | `orthworm_ex_metal_retaliation` | **49.7%** | 47.6% | 24/54 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | ns_zoroark_night_joker_toolbox (12%) |
| 31 | `arbok_muk_laser_darkbell` | **48.8%** | 49.7% | 26/54 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | kangaskhan_tyrantrum_flip_mill (20%) |
| 32 | `toxic_slumber_vileplume_ex` | **48.8%** | 48.7% | 23/54 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | tauros_risky_ruins (21%) |
| 33 | `team_rockets_spidops_swarm` | **46.6%** | 43.0% | 20/54 | static_venom_drapion (83%) | tauros_risky_ruins (17%) |
| 34 | `arbok_muk_trolley_darkbell` | **46.5%** | 47.0% | 21/54 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | kangaskhan_tyrantrum_flip_mill (18%) |
| 35 | `mega_scrafty_ex_darkness_tank` | **46.5%** | 44.9% | 23/54 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | lurantis_heal_punish (15%) |
| 36 | `meta_dragapult_dusknoir` | **45.5%** | 44.7% | 17/54 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | ns_zoroark_night_joker_toolbox (14%) |
| 37 | `arbok_team_rockets_muk_condition_stack` | **45.4%** | 45.8% | 18/54 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | kangaskhan_tyrantrum_flip_mill (12%) |
| 38 | `hops_snorlax_stacked_buff` | **45.3%** | 41.5% | 16/54 | study_flygon_sandy_flapping_mill (89%) | ns_zoroark_night_joker_toolbox (17%) |
| 39 | `study_maushold_gnaw_latias` | **45.2%** | 45.5% | 19/54 | study_flygon_sandy_flapping_mill (91%) | tauros_risky_ruins (11%) |
| 40 | `stevens_carbink_damage_wall` | **44.9%** | 44.4% | 19/54 | meta_festival_lead (81%) | ns_zoroark_night_joker_toolbox (16%) |
| 41 | `feraligatr_munkidori_damage_transfer` | **44.8%** | 42.7% | 14/54 | study_flygon_sandy_flapping_mill (87%) | tauros_risky_ruins (10%) |
| 42 | `tr_crobat_absol_bench_snipe` | **44.1%** | 46.0% | 16/54 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | lurantis_heal_punish (15%) |
| 43 | `chandelure_centiskorch_deck_out` | **44.0%** | 46.0% | 21/54 | study_flygon_sandy_flapping_mill (80%) | tauros_risky_ruins (10%) |
| 44 | `crabominable_veluza_food_prep` | **40.4%** | 39.6% | 11/54 | static_venom_drapion (79%) | ns_zoroark_night_joker_toolbox (15%) |
| 45 | `eerie_inferno_ninetales_burn` | **40.3%** | 38.2% | 11/54 | study_flygon_sandy_flapping_mill (83%) | wugtrio_paralysis_pin (10%) |
| 46 | `darkness_mill_hand_lock` | **38.2%** | 35.5% | 11/54 | study_centiskorch_bastiodon_mill (89%) | lurantis_heal_punish (6%) |
| 47 | `tr_arbok_yveltal_snow_coating` | **38.0%** | 35.4% | 13/54 | study_centiskorch_bastiodon_mill (86%) | tauros_risky_ruins (5%) |
| 48 | `meta_ns_zoroark` | **37.7%** | 40.5% | 12/54 | static_venom_drapion (75%) | tauros_risky_ruins (11%) |
| 49 | `study_hydreigon_zweilous_mill` | **36.7%** | 34.9% | 9/54 | meta_ns_zoroark (72%) | lurantis_heal_punish (12%) |
| 50 | `study_centiskorch_bastiodon_mill` | **35.7%** | 33.5% | 10/54 | meta_ns_zoroark (81%) | tauros_risky_ruins (9%) |
| 51 | `meta_festival_lead` | **34.8%** | 33.6% | 8/54 | static_venom_drapion (69%) | tauros_risky_ruins (7%) |
| 52 | `salazzle_ex_team_rockets_muk_condition_stack` | **28.5%** | 28.8% | 2/54 | team_rockets_wobbuffet_orbeetle_damage_launder (53%) | ditto_tyranitar_gengar_hydreigon (10%) |
| 53 | `study_flygon_sandy_flapping_mill` | **28.1%** | 22.0% | 5/54 | meta_ns_zoroark (76%) | cradily_amoonguss_conditions (3%) |
| 54 | `static_venom_drapion` | **20.8%** | 17.5% | 4/54 | study_flygon_sandy_flapping_mill (61%) | tauros_risky_ruins (4%) |
| 55 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **19.3%** | 15.4% | 2/54 | study_flygon_sandy_flapping_mill (79%) | ns_zoroark_night_joker_toolbox (4%) |

## Full matrix

Row's win rate against column.

| |tauros_risky_r|ns_zoroark_nig|team_rockets_p|maushold_gnaw_|lurantis_heal_|ditto_tyranita|study_mega_exc|krookodile_ex_|wugtrio_paraly|cradily_accelg|scovillain_sal|panic_poison_p|meta_mega_exca|team_rockets_k|mega_lopunny_d|cradily_amoong|mega_chandelur|kangaskhan_tyr|meta_raging_bo|meta_slowking|heracross_sini|veluza_sinistc|meta_dragapult|dhelmise_veluz|meta_dragapult|metal_metang_e|water_aggro|decidueye_ex_j|kyurem_vanillu|orthworm_ex_me|arbok_muk_lase|toxic_slumber_|team_rockets_s|arbok_muk_trol|mega_scrafty_e|meta_dragapult|arbok_team_roc|hops_snorlax_s|study_maushold|stevens_carbin|feraligatr_mun|tr_crobat_abso|chandelure_cen|crabominable_v|eerie_inferno_|darkness_mill_|tr_arbok_yvelt|meta_ns_zoroar|study_hydreigo|study_centisko|meta_festival_|salazzle_ex_te|study_flygon_s|static_venom_d|team_rockets_w|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **tauros_risky_r** |—|75|59|67|40|49|45|59|61|57|62|66|47|78|50|61|85|90|82|83|53|52|56|54|58|55|88|89|58|84|73|79|83|77|81|64|79|77|89|82|90|70|90|78|82|91|95|89|87|91|93|83|97|96|90|
| **ns_zoroark_nig** |25|—|57|59|42|67|41|62|82|57|65|72|68|80|76|66|75|77|59|77|63|76|78|75|78|77|84|55|83|88|76|69|73|80|81|86|75|83|76|84|68|85|62|85|82|87|84|85|78|45|75|88|68|93|96|
| **team_rockets_p** |41|43|—|50|58|60|44|68|58|63|57|62|56|66|60|71|52|71|57|63|72|66|61|70|69|62|72|76|70|77|70|78|78|70|78|72|71|76|70|68|74|78|76|78|80|90|83|73|82|84|82|82|83|92|95|
| **maushold_gnaw_** |33|41|50|—|58|42|55|50|67|59|79|67|70|58|52|55|63|68|84|79|70|56|67|52|66|74|62|74|75|82|73|77|63|78|77|70|81|73|64|76|59|78|78|69|72|69|82|87|86|88|77|88|87|90|89|
| **lurantis_heal_** |60|58|42|42|—|72|46|72|62|61|40|63|52|67|56|63|50|59|48|55|64|63|51|70|65|60|73|82|69|64|73|74|69|72|85|68|74|71|86|61|61|85|88|68|73|94|91|75|88|74|79|80|88|91|92|
| **ditto_tyranita** |51|33|40|58|28|—|75|58|54|48|60|56|63|65|48|51|61|70|45|65|35|50|69|65|69|71|69|44|71|68|66|64|60|69|70|70|75|73|78|76|77|64|82|80|79|79|91|81|81|91|63|90|86|88|92|
| **study_mega_exc** |55|59|56|45|54|25|—|39|73|58|41|54|60|51|59|74|67|61|54|64|68|77|59|76|74|70|59|53|78|56|71|63|77|77|55|74|74|74|43|70|62|71|36|81|45|51|76|89|72|69|85|84|76|77|89|
| **krookodile_ex_** |41|38|32|50|28|42|61|—|47|41|50|58|50|60|52|47|63|60|43|58|41|52|59|64|62|54|67|41|68|67|72|52|53|74|68|62|74|72|72|75|77|71|67|73|76|72|73|78|78|71|67|86|81|83|94|
| **wugtrio_paraly** |39|18|42|33|38|46|27|53|—|64|40|64|37|63|42|65|45|46|48|53|51|61|51|65|49|50|68|76|61|64|74|54|74|73|71|63|77|73|85|62|76|69|88|73|90|83|85|44|60|68|78|87|56|92|96|
| **cradily_accelg** |43|43|37|41|39|52|42|59|36|—|38|52|46|53|48|50|56|41|56|52|54|46|49|54|52|56|62|64|59|54|67|61|64|68|73|54|69|67|71|61|70|79|58|72|67|85|54|80|85|74|66|74|96|87|90|
| **scovillain_sal** |38|35|43|21|60|40|59|50|60|62|—|53|67|63|62|70|33|49|59|59|72|53|55|60|59|68|41|60|35|84|73|77|71|71|71|66|73|65|52|80|54|75|32|48|66|64|75|68|67|42|69|82|37|86|87|
| **panic_poison_p** |34|28|38|33|37|44|46|42|36|48|47|—|48|52|48|42|66|21|49|55|65|56|51|58|55|61|57|66|57|67|66|53|58|69|59|64|68|72|76|66|67|67|72|69|77|80|81|52|76|88|51|82|91|92|92|
| **meta_mega_exca** |53|32|44|30|48|37|40|50|63|54|33|52|—|49|57|66|32|50|51|51|69|70|54|53|61|61|66|51|75|68|61|61|71|64|66|67|67|68|55|56|60|62|46|76|59|70|78|72|65|51|82|69|55|87|81|
| **team_rockets_k** |22|20|34|42|33|35|49|40|37|47|37|48|51|—|45|50|64|42|47|54|51|61|48|58|49|61|55|65|52|58|63|64|58|64|58|55|62|62|75|63|65|60|77|71|70|78|79|60|76|84|64|76|89|91|90|
| **mega_lopunny_d** |50|24|40|48|44|52|41|48|58|52|38|52|43|55|—|53|57|47|46|46|47|48|48|53|53|51|60|59|54|61|58|65|68|61|62|59|61|62|67|56|68|62|78|56|72|74|66|51|59|70|69|70|86|86|86|
| **cradily_amoong** |39|34|29|45|37|49|26|53|35|50|30|58|34|50|47|—|55|41|48|45|49|44|46|48|49|45|63|52|51|45|70|59|58|72|75|55|72|67|70|48|68|76|60|67|63|87|64|76|83|65|65|78|97|90|93|
| **mega_chandelur** |15|25|48|37|50|39|33|37|55|44|67|34|68|36|43|45|—|73|49|48|68|68|58|59|52|74|66|77|68|59|35|68|66|37|55|60|41|64|49|70|74|49|63|73|64|64|63|45|60|64|66|80|61|79|84|
| **kangaskhan_tyr** |10|23|29|32|41|30|39|40|54|59|51|79|50|58|53|59|27|—|44|50|47|55|59|53|54|51|54|38|59|62|80|65|62|82|58|63|88|63|41|68|60|58|36|67|77|54|72|73|62|54|69|82|62|89|81|
| **meta_raging_bo** |18|41|43|16|52|55|46|57|52|44|41|51|49|53|54|52|51|56|—|58|50|56|56|53|56|60|61|50|66|58|47|67|65|47|65|64|54|62|51|60|59|62|48|62|64|70|76|59|59|53|70|66|63|79|77|
| **meta_slowking** |17|23|37|21|45|35|36|42|47|48|41|45|49|46|54|55|52|50|42|—|49|56|59|53|53|52|64|45|59|62|56|64|64|57|59|61|63|69|50|66|60|55|45|67|64|66|80|68|56|53|79|72|71|83|84|
| **heracross_sini** |47|37|28|30|36|65|32|59|49|46|28|35|31|49|53|51|32|53|50|51|—|52|45|49|51|39|52|48|62|49|51|51|60|54|76|58|58|60|71|57|41|70|58|63|55|82|67|67|76|62|71|68|84|85|89|
| **veluza_sinistc** |48|24|34|44|37|50|23|48|39|54|47|44|30|39|52|56|32|45|44|44|48|—|43|50|51|37|53|42|51|53|54|50|62|54|69|62|59|59|64|45|62|66|53|64|73|78|74|59|64|63|80|67|76|87|87|
| **meta_dragapult** |44|22|39|33|49|31|41|41|49|51|45|49|46|52|52|54|42|41|44|41|55|57|—|50|54|51|58|66|54|57|54|59|68|54|59|61|58|57|52|51|60|56|52|61|65|63|69|56|43|40|68|65|58|82|82|
| **dhelmise_veluz** |46|25|30|48|30|35|24|36|35|46|40|42|47|42|47|52|41|47|47|47|51|50|50|—|52|49|54|54|54|47|55|51|56|57|50|59|61|58|57|51|55|54|54|74|70|61|59|67|54|53|79|71|71|87|85|
| **meta_dragapult** |42|22|31|34|35|31|26|38|51|48|41|45|39|51|47|51|48|46|44|47|49|49|46|48|—|48|61|58|53|52|52|49|64|54|51|59|57|55|50|47|60|57|52|60|69|59|68|64|45|43|76|70|66|81|85|
| **metal_metang_e** |45|23|38|26|40|29|30|46|50|44|32|39|39|39|49|55|26|49|40|48|61|63|49|51|52|—|57|46|69|62|48|54|63|54|58|63|53|63|46|45|53|52|42|67|55|64|71|63|54|51|76|61|55|82|80|
| **water_aggro** |12|16|28|38|27|31|41|33|32|38|59|43|34|45|40|37|34|46|39|36|48|47|42|46|39|43|—|55|48|55|50|53|50|54|56|49|54|52|73|55|59|54|88|64|72|76|68|60|70|86|65|78|88|82|80|
| **decidueye_ex_j** |11|45|24|26|18|56|47|59|24|36|40|34|49|35|41|48|23|62|50|55|52|58|34|46|42|54|45|—|57|60|44|66|52|47|73|49|46|58|62|54|51|64|54|67|62|72|40|76|79|22|61|72|55|86|86|
| **kyurem_vanillu** |42|17|30|25|31|29|22|32|39|41|65|43|25|48|46|49|32|41|34|41|38|49|46|46|47|31|52|43|—|34|52|51|67|52|54|57|56|58|66|43|52|53|70|63|75|68|74|47|55|71|72|80|52|87|91|
| **orthworm_ex_me** |16|12|23|18|36|32|44|33|36|46|16|33|32|42|39|55|41|38|42|38|51|47|43|53|48|38|45|40|66|—|42|49|60|48|47|52|52|67|72|58|52|53|73|59|55|69|86|47|50|80|86|64|84|83|90|
| **arbok_muk_lase** |27|24|30|27|27|34|29|28|26|33|27|34|39|37|42|30|65|20|53|44|49|46|46|45|48|52|50|56|48|58|—|40|55|51|41|54|51|66|64|54|58|53|56|58|64|65|59|52|74|72|50|72|85|81|93|
| **toxic_slumber_** |21|31|22|23|26|36|37|48|46|39|23|47|39|36|35|41|32|35|33|36|49|50|41|49|51|46|47|34|49|51|60|—|47|64|66|54|61|55|58|61|51|54|51|49|38|72|76|56|71|68|57|67|82|80|84|
| **team_rockets_s** |17|27|22|37|31|40|23|47|26|36|29|42|29|42|32|42|34|38|35|36|40|38|32|44|36|37|50|48|33|40|45|53|—|48|63|42|50|52|54|44|61|56|70|57|60|74|57|60|66|69|62|65|78|83|82|
| **arbok_muk_trol** |23|20|30|22|28|31|23|26|27|32|29|31|36|36|39|28|63|18|53|43|46|46|46|43|46|46|46|53|48|52|49|36|52|—|40|52|52|63|62|49|57|51|48|58|61|60|55|48|71|66|49|67|83|79|93|
| **mega_scrafty_e** |19|19|22|23|15|30|45|32|29|27|29|41|34|42|38|25|45|42|35|41|24|31|41|50|49|42|44|27|46|53|59|34|37|60|—|48|63|54|58|59|54|54|66|58|68|55|54|59|69|74|62|74|85|79|87|
| **meta_dragapult** |36|14|28|30|32|30|26|38|37|46|34|36|33|45|41|45|40|37|36|39|42|38|39|41|41|37|51|51|43|48|46|46|58|48|52|—|47|45|53|42|57|51|56|50|61|58|62|49|45|41|66|65|64|79|84|
| **arbok_team_roc** |21|25|29|19|26|25|26|26|23|31|27|32|33|38|39|28|59|12|46|37|42|41|42|39|43|47|46|54|44|48|49|39|50|48|37|53|—|59|60|52|57|50|50|55|59|65|55|49|71|71|48|69|85|83|91|
| **hops_snorlax_s** |23|17|24|27|29|27|26|28|27|33|35|28|32|38|38|33|36|37|38|31|40|41|43|42|45|37|48|42|42|33|34|45|48|37|46|55|41|—|62|48|56|48|66|61|60|57|65|59|58|83|70|75|89|83|80|
| **study_maushold** |11|24|30|36|14|22|57|28|15|29|48|24|45|25|33|30|51|59|49|50|29|36|48|43|50|54|27|38|34|28|36|42|46|38|42|47|40|38|—|53|58|49|68|58|53|50|52|72|71|84|64|79|91|67|79|
| **stevens_carbin** |18|16|32|24|39|24|30|25|38|39|20|34|44|37|44|52|30|32|40|34|43|55|49|49|53|55|45|46|57|42|46|39|56|51|41|58|48|52|47|—|42|50|40|55|40|50|41|56|55|61|81|65|56|72|77|
| **feraligatr_mun** |10|32|26|41|39|23|38|23|24|30|46|33|40|35|32|32|26|40|41|40|59|38|40|45|40|47|41|49|48|48|42|49|39|43|46|43|43|44|42|58|—|51|52|54|57|44|46|62|59|72|60|72|87|76|75|
| **tr_crobat_abso** |30|15|22|22|15|36|29|29|31|21|25|33|38|40|38|24|51|42|38|45|30|34|44|46|43|48|46|36|47|47|47|46|44|49|46|49|50|52|51|50|49|—|49|58|55|59|58|56|69|56|51|67|58|80|86|
| **chandelure_cen** |10|38|24|22|12|18|64|33|12|42|68|28|54|23|22|40|37|64|52|55|42|47|48|46|48|58|12|46|30|27|44|49|30|52|34|44|50|34|32|60|48|51|—|57|56|17|25|79|66|77|57|79|80|62|71|
| **crabominable_v** |22|15|22|31|32|20|19|27|27|28|52|31|24|29|44|33|27|33|38|33|37|36|39|26|40|33|36|33|37|41|42|51|43|42|42|50|45|39|42|45|46|42|43|—|62|55|50|53|47|60|69|63|60|79|69|
| **eerie_inferno_** |18|18|20|28|27|21|55|24|10|33|34|23|41|30|28|37|36|23|36|36|45|27|35|30|31|45|28|38|25|45|36|62|40|39|32|39|41|40|47|60|43|45|44|38|—|55|55|46|65|79|41|69|83|76|74|
| **darkness_mill_** |9|13|10|31|6|21|49|28|17|15|36|20|30|22|26|13|36|46|30|34|18|22|37|39|41|36|24|28|32|31|35|28|26|40|45|42|35|43|50|50|56|41|83|45|45|—|54|56|66|89|34|72|82|70|74|
| **tr_arbok_yvelt** |5|16|17|18|9|9|24|27|15|46|25|19|22|21|34|36|37|28|24|20|33|26|31|41|32|29|32|60|26|14|41|24|43|45|46|38|45|35|48|59|54|42|75|50|45|46|—|58|59|86|62|58|78|66|72|
| **meta_ns_zoroar** |11|15|27|13|25|19|11|22|56|20|32|48|28|40|49|24|55|27|41|32|33|41|44|33|36|37|40|24|53|53|48|44|40|52|41|51|51|41|28|44|38|44|21|47|54|44|42|—|28|19|54|54|24|75|66|
| **study_hydreigo** |13|22|18|14|12|19|28|22|40|15|33|24|35|24|41|17|40|38|41|44|24|36|57|46|55|46|30|21|45|50|26|29|34|29|31|55|29|42|29|45|41|31|34|53|35|34|41|72|—|49|60|59|44|70|68|
| **study_centisko** |9|55|16|12|26|9|31|29|32|26|58|12|49|16|30|35|36|46|47|47|38|37|60|47|57|49|14|78|29|20|28|32|31|34|26|59|29|17|16|39|28|44|23|40|21|11|14|81|51|—|70|61|44|41|37|
| **meta_festival_** |7|25|18|23|21|37|15|33|22|34|31|49|18|36|31|35|34|31|30|21|29|20|32|21|24|24|35|39|28|14|50|43|38|51|38|34|52|30|36|19|40|49|43|31|59|66|38|46|40|30|—|48|55|69|57|
| **salazzle_ex_te** |17|12|18|12|20|10|16|14|13|26|18|18|31|24|30|22|20|18|34|28|32|33|35|29|30|39|22|28|20|36|28|33|35|33|26|35|31|25|21|35|28|33|21|37|31|28|42|46|41|39|52|—|33|47|53|
| **study_flygon_s** |3|32|17|13|12|14|24|19|44|4|63|9|45|11|14|3|39|38|37|29|16|24|42|29|34|45|12|45|48|16|15|18|22|17|15|36|15|11|9|44|13|42|20|40|17|18|22|76|56|56|45|67|—|39|21|
| **static_venom_d** |4|7|8|10|9|12|23|17|8|13|14|8|13|9|14|10|21|11|21|17|15|13|18|13|19|18|18|14|13|17|19|20|17|21|21|21|17|17|33|28|24|20|38|21|24|30|34|25|30|59|31|53|61|—|52|
| **team_rockets_w** |10|4|5|11|8|8|11|6|4|10|13|8|19|10|14|7|16|19|23|16|11|13|18|15|15|20|20|14|9|10|7|16|18|7|13|16|9|20|21|23|25|14|29|31|26|26|28|34|32|63|43|47|79|48|—|
