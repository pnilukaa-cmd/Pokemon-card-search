# Field results — every deck against every other deck

Full round robin over **35 decks**, **200 games** per pairing, 595 pairings, 119,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-10, after the ex audit. **These supersede every number recorded in the deck files before this date** — the audit changed damage on a large number of cards (typed Energy scalers counting the wrong Energy, discard-cost attacks that were never charged, attack gates that were never enforced), so older figures are not comparable with these or with each other.

Three changes to the field itself: `selective_bloom_cradily` had been **excluded from every past measurement as unplayable** — the Basic count used by the gauntlet tooling required `supertype == "Pokémon"`, so `Antique Root Fossil` (an Item that plays *as* a 60 HP Basic) did not count and the deck read as having zero Basics. That check was never updated when Fossils were made playable. It measures 5th. `AAA_tr_crobat_absol_snipe` was a byte-identical duplicate of `tr_crobat_absol_bench_snipe` and had been inflating that archetype's presence in every past measurement; `veluza_sinistcha_ex_tea_service` had a deck file but no entry in the field and had never been measured at all.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **73.1%** | 72.5% | 32/34 | team_rockets_wobbuffet_orbeetle_damage_launder (98%) | panic_poison_paralysis (48%) |
| 2 | `panic_poison_paralysis` | **72.1%** | 71.2% | 33/34 | team_rockets_wobbuffet_orbeetle_damage_launder (98%) | toxic_slumber_vileplume_ex (42%) |
| 3 | `toxic_slumber_vileplume_ex` | **63.7%** | 63.0% | 28/34 | team_rockets_wobbuffet_orbeetle_damage_launder (94%) | eerie_inferno_ninetales_burn (41%) |
| 4 | `team_rockets_persian_ex_attack_theft` | **63.4%** | 63.5% | 30/34 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | panic_poison_paralysis (31%) |
| 5 | `selective_bloom_cradily` | **59.0%** | 57.2% | 24/34 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | scovillain_salazzle_spicy_rage (32%) |
| 6 | `water_aggro` | **58.7%** | 55.0% | 25/34 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (30%) |
| 7 | `tr_crobat_absol_bench_snipe` | **58.1%** | 58.8% | 25/34 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | panic_poison_paralysis (32%) |
| 8 | `dhelmise_veluza_hide_n_sneak` | **56.9%** | 54.0% | 24/34 | feraligatr_munkidori_damage_transfer (88%) | lurantis_heal_punish (34%) |
| 9 | `arbok_muk_laser_darkbell` | **56.1%** | 55.5% | 23/34 | feraligatr_munkidori_damage_transfer (92%) | lurantis_heal_punish (24%) |
| 10 | `arbok_team_rockets_muk_condition_stack` | **55.6%** | 53.0% | 19/34 | feraligatr_munkidori_damage_transfer (92%) | lurantis_heal_punish (27%) |
| 11 | `krookodile_ex_relicanth_hand_disruption` | **55.4%** | 55.2% | 23/34 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | lurantis_heal_punish (14%) |
| 12 | `mega_chandelure_ex_retreat_tax` | **55.3%** | 55.0% | 20/34 | feraligatr_munkidori_damage_transfer (86%) | panic_poison_paralysis (28%) |
| 13 | `kangaskhan_tyrantrum_flip_mill` | **55.3%** | 53.0% | 23/34 | feraligatr_munkidori_damage_transfer (83%) | panic_poison_paralysis (36%) |
| 14 | `kyurem_vanilluxe_blizzard` | **54.6%** | 50.8% | 18/34 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | panic_poison_paralysis (27%) |
| 15 | `arbok_muk_trolley_darkbell` | **54.0%** | 52.5% | 21/34 | team_rockets_wobbuffet_orbeetle_damage_launder (91%) | toxic_slumber_vileplume_ex (21%) |
| 16 | `scovillain_salazzle_spicy_rage` | **53.8%** | 52.2% | 21/34 | orthworm_ex_metal_retaliation (80%) | water_aggro (25%) |
| 17 | `heracross_sinistcha_tea` | **52.4%** | 50.8% | 17/34 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | lurantis_heal_punish (28%) |
| 18 | `mega_scrafty_ex_darkness_tank` | **52.4%** | 51.2% | 18/34 | team_rockets_wobbuffet_orbeetle_damage_launder (87%) | lurantis_heal_punish (20%) |
| 19 | `orthworm_ex_metal_retaliation` | **52.1%** | 51.2% | 19/34 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | scovillain_salazzle_spicy_rage (20%) |
| 20 | `decidueye_ex_judge_sniper_lock` | **51.2%** | 49.5% | 16/34 | feraligatr_munkidori_damage_transfer (86%) | lurantis_heal_punish (18%) |
| 21 | `team_rockets_koffing_weezing_bench_swarm` | **51.0%** | 51.8% | 18/34 | feraligatr_munkidori_damage_transfer (90%) | toxic_slumber_vileplume_ex (16%) |
| 22 | `mega_lopunny_dusknoir_snipe_finisher` | **50.0%** | 47.5% | 15/34 | feraligatr_munkidori_damage_transfer (82%) | ns_zoroark_night_joker_toolbox (29%) |
| 23 | `eerie_inferno_ninetales_burn` | **50.0%** | 48.5% | 15/34 | feraligatr_munkidori_damage_transfer (78%) | water_aggro (22%) |
| 24 | `stevens_carbink_damage_wall` | **48.9%** | 46.5% | 15/34 | feraligatr_munkidori_damage_transfer (80%) | lurantis_heal_punish (28%) |
| 25 | `ns_zoroark_night_joker_toolbox` | **45.6%** | 45.8% | 9/34 | static_venom_drapion (80%) | arbok_muk_laser_darkbell (22%) |
| 26 | `veluza_sinistcha_ex_tea_service` | **45.1%** | 41.5% | 10/34 | feraligatr_munkidori_damage_transfer (79%) | panic_poison_paralysis (21%) |
| 27 | `team_rockets_spidops_swarm` | **44.9%** | 41.2% | 11/34 | team_rockets_wobbuffet_orbeetle_damage_launder (85%) | lurantis_heal_punish (18%) |
| 28 | `chandelure_centiskorch_deck_out` | **43.1%** | 41.5% | 9/34 | salazzle_ex_team_rockets_muk_condition_stack (79%) | lurantis_heal_punish (16%) |
| 29 | `darkness_mill_hand_lock` | **42.8%** | 39.8% | 8/34 | chandelure_centiskorch_deck_out (78%) | lurantis_heal_punish (10%) |
| 30 | `hops_snorlax_stacked_buff` | **42.7%** | 40.5% | 8/34 | feraligatr_munkidori_damage_transfer (88%) | panic_poison_paralysis (14%) |
| 31 | `crabominable_veluza_food_prep` | **35.5%** | 34.0% | 4/34 | feraligatr_munkidori_damage_transfer (66%) | panic_poison_paralysis (12%) |
| 32 | `salazzle_ex_team_rockets_muk_condition_stack` | **30.2%** | 27.2% | 4/34 | feraligatr_munkidori_damage_transfer (58%) | lurantis_heal_punish (16%) |
| 33 | `static_venom_drapion` | **28.7%** | 26.8% | 3/34 | team_rockets_wobbuffet_orbeetle_damage_launder (68%) | lurantis_heal_punish (14%) |
| 34 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **19.4%** | 15.5% | 1/34 | feraligatr_munkidori_damage_transfer (66%) | panic_poison_paralysis (2%) |
| 35 | `feraligatr_munkidori_damage_transfer` | **18.9%** | 17.2% | 0/34 | salazzle_ex_team_rockets_muk_condition_stack (42%) | lurantis_heal_punish (4%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|toxic_slumber_|team_rockets_p|selective_bloo|water_aggro|tr_crobat_abso|dhelmise_veluz|arbok_muk_lase|arbok_team_roc|krookodile_ex_|mega_chandelur|kangaskhan_tyr|kyurem_vanillu|arbok_muk_trol|scovillain_sal|heracross_sini|mega_scrafty_e|orthworm_ex_me|decidueye_ex_j|team_rockets_k|mega_lopunny_d|eerie_inferno_|stevens_carbin|ns_zoroark_nig|veluza_sinistc|team_rockets_s|chandelure_cen|darkness_mill_|hops_snorlax_s|crabominable_v|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|48|57|64|64|68|64|66|76|73|86|52|60|58|70|48|72|80|75|82|84|71|72|72|77|69|82|84|90|84|72|84|86|98|96|
| **panic_poison_p** |52|—|42|69|62|70|68|62|73|72|60|72|64|73|72|70|70|62|71|74|74|64|72|68|69|79|78|70|78|86|88|84|86|98|95|
| **toxic_slumber_** |43|58|—|45|50|60|64|50|70|68|66|53|56|62|79|46|66|62|64|56|84|64|41|68|60|62|59|62|66|72|69|80|80|94|87|
| **team_rockets_p** |36|31|55|—|55|54|51|54|52|50|62|52|60|53|50|56|64|66|72|75|53|68|61|66|76|68|74|73|76|75|74|80|82|90|90|
| **selective_bloo** |36|38|50|45|—|47|58|35|67|65|68|58|41|51|70|32|46|73|58|56|76|52|56|56|34|56|57|73|80|74|60|72|80|93|89|
| **water_aggro** |32|30|40|46|53|—|54|43|48|52|48|46|47|55|55|75|52|51|62|57|58|53|78|58|54|66|61|74|60|68|74|79|80|92|94|
| **tr_crobat_abso** |36|32|36|49|42|46|—|47|62|60|50|63|48|52|54|56|50|50|52|60|58|62|56|60|66|62|67|70|63|66|66|78|78|93|88|
| **dhelmise_veluz** |34|38|50|46|65|57|53|—|42|52|40|51|52|49|42|59|52|55|48|62|48|56|64|46|53|64|74|64|60|68|72|66|81|84|88|
| **arbok_muk_lase** |24|27|30|48|33|52|38|58|—|55|46|64|55|58|52|58|51|44|46|52|47|49|57|58|78|64|69|56|58|70|74|78|77|90|92|
| **arbok_team_roc** |27|28|32|50|35|48|40|48|45|—|40|64|56|63|48|48|51|38|50|58|44|55|60|50|72|67|69|56|64|67|76|80|76|92|92|
| **krookodile_ex_** |14|40|34|38|32|52|50|60|54|60|—|53|50|50|54|48|46|52|62|38|66|54|56|56|61|60|58|62|62|64|70|78|74|92|86|
| **mega_chandelur** |48|28|47|48|42|54|37|49|36|36|47|—|58|62|39|63|60|48|56|76|48|54|54|60|44|64|64|64|62|60|67|72|64|84|86|
| **kangaskhan_tyr** |40|36|44|40|59|53|52|48|45|44|50|42|—|52|50|54|58|50|62|53|40|58|56|58|52|64|62|42|56|70|78|74|74|82|83|
| **kyurem_vanillu** |42|27|38|47|49|45|48|51|42|37|50|38|48|—|47|69|66|47|42|48|46|66|66|52|54|62|60|64|61|64|66|72|72|90|78|
| **arbok_muk_trol** |30|28|21|50|30|45|46|58|48|52|46|61|50|53|—|52|43|42|46|54|46|45|53|55|73|62|64|57|58|64|74|78|74|91|87|
| **scovillain_sal** |52|30|54|44|68|25|44|41|42|52|52|37|46|31|48|—|68|53|80|52|52|69|46|61|62|58|75|41|54|58|47|72|78|73|67|
| **heracross_sini** |28|30|34|36|54|48|50|48|49|49|54|40|42|34|57|32|—|62|50|46|62|54|40|48|52|63|62|55|76|54|66|70|73|87|78|
| **mega_scrafty_e** |20|38|38|34|27|49|50|45|56|62|48|52|50|53|58|47|38|—|50|40|56|42|60|60|48|51|52|58|61|60|63|76|72|87|82|
| **orthworm_ex_me** |25|29|36|28|42|38|48|52|54|50|38|44|38|58|54|20|50|50|—|39|66|46|50|60|52|53|65|62|56|78|70|70|75|92|79|
| **decidueye_ex_j** |18|26|44|25|44|43|40|38|48|42|62|24|47|52|46|48|54|60|61|—|54|50|44|50|64|52|48|50|76|55|64|74|72|82|86|
| **team_rockets_k** |16|26|16|47|24|42|42|52|53|56|34|52|60|54|54|48|38|44|34|46|—|52|45|46|59|74|54|63|45|56|80|72|71|90|90|
| **mega_lopunny_d** |29|36|36|32|48|47|38|44|51|45|46|46|42|34|55|31|46|58|54|50|48|—|60|48|29|45|58|67|62|58|60|69|70|78|82|
| **eerie_inferno_** |28|28|59|39|44|22|44|36|43|40|44|46|44|34|47|54|60|40|50|56|55|40|—|68|50|40|61|60|58|58|57|73|71|72|78|
| **stevens_carbin** |28|32|32|34|44|42|40|54|42|50|44|40|42|48|45|39|52|40|40|50|54|52|32|—|58|64|50|40|51|60|73|65|72|72|80|
| **ns_zoroark_nig** |23|31|40|24|66|46|34|47|22|28|39|56|48|46|27|38|48|52|48|36|41|71|50|42|—|50|46|44|59|42|58|43|80|60|66|
| **veluza_sinistc** |31|21|38|32|44|34|38|36|36|33|40|36|36|38|38|42|37|49|47|48|26|55|60|36|50|—|50|50|66|45|59|52|78|73|79|
| **team_rockets_s** |18|22|41|26|43|39|33|26|31|31|42|36|38|40|36|25|38|48|35|52|46|42|39|50|54|50|—|58|70|55|63|64|72|85|80|
| **chandelure_cen** |16|30|38|27|27|26|30|36|44|44|38|36|58|36|43|59|45|42|38|50|37|33|40|60|56|50|42|—|22|42|64|79|60|60|64|
| **darkness_mill_** |10|22|34|24|20|40|37|40|42|36|38|38|44|39|42|46|24|39|44|24|55|38|42|49|41|34|30|78|—|55|52|77|66|78|77|
| **hops_snorlax_s** |16|14|28|25|26|32|34|32|30|33|36|40|30|36|36|42|46|40|22|45|44|42|42|40|58|55|45|58|45|—|66|76|72|77|88|
| **crabominable_v** |28|12|31|26|40|26|34|28|26|24|30|33|22|34|26|53|34|37|30|36|20|40|43|27|42|41|37|36|48|34|—|45|64|53|66|
| **salazzle_ex_te** |16|16|20|20|28|21|22|34|22|20|22|28|26|28|22|28|30|24|30|26|28|31|27|35|57|48|36|21|23|24|55|—|47|56|58|
| **static_venom_d** |14|14|20|18|20|20|22|19|23|24|26|36|26|28|26|22|27|28|25|28|29|30|29|28|20|22|28|40|34|28|36|53|—|68|65|
| **team_rockets_w** |2|2|6|10|7|8|7|16|10|8|8|16|18|10|9|27|13|13|8|18|10|22|28|28|40|27|15|40|22|23|47|44|32|—|66|
| **feraligatr_mun** |4|5|13|10|11|6|12|12|8|8|14|14|17|22|13|33|22|18|21|14|10|18|22|20|34|21|20|36|23|12|34|42|35|34|—|
