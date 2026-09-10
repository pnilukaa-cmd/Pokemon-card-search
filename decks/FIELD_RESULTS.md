# Field results — every deck against every other deck

Full round robin over **38 decks**, **200 games** per pairing, 703 pairings, 140,600 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-10 on a rules-validated engine. **These supersede every number recorded in the deck files before this date.** The engine changed substantially in getting here: Pokémon Checkup now resolves BOTH players' Active (it resolved only one, halving every Poison and Burn and doubling how long Sleep lasted), Resistance now exists at all (369 cards carry one and it was not modelled), every coin flip is actually flipped (all 158 cards phrased "Flip a coin. If heads..." parsed as certain), typed Energy scalers count the type they name, and a long list of attack costs that were never charged now are. Older figures are not comparable with these or with each other.

Four changes to the field itself: the two TCGplayer September 2026 Dragapult lists were added; `selective_bloom_cradily` had been **excluded from every past measurement as unplayable**, because the Basic count required `supertype == "Pokémon"` and `Antique Root Fossil` (an Item that plays *as* a 60 HP Basic) did not count; `AAA_tr_crobat_absol_snipe` was a byte-identical duplicate of `tr_crobat_absol_bench_snipe` and had been inflating that archetype's presence in every past measurement; and `veluza_sinistcha_ex_tea_service` had a deck file but no entry in the field and had never been measured at all.

> **On the two meta lists.** `meta_dragapult_pure` places 17th and `meta_dragapult_dusknoir` 25th, and that is a statement about this simulator, not about the decks. Both sides here run the same greedy AI, which does not aim Phantom Dive's six counters at a prize map, does not hold a knockout back to deny Fezandipiti ex and Unfair Stamp, and does not sequence Crushing Hammer. Those are exactly the skills the article says the archetype wins on. A real list piloted by a policy that cannot pilot it is a lower bound. `AAA_tr_crobat_absol_snipe` was a byte-identical duplicate of `tr_crobat_absol_bench_snipe` and had been inflating that archetype's presence in every past measurement; `veluza_sinistcha_ex_tea_service` had a deck file but no entry in the field and had never been measured at all.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `panic_poison_paralysis` | **73.8%** | 73.0% | 36/37 | feraligatr_munkidori_damage_transfer (97%) | team_rockets_persian_ex_attack_theft (50%) |
| 2 | `lurantis_heal_punish` | **72.7%** | 73.0% | 35/37 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | scovillain_salazzle_spicy_rage (39%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **71.0%** | 70.0% | 35/37 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | lurantis_heal_punish (50%) |
| 4 | `toxic_slumber_vileplume_ex` | **61.7%** | 59.5% | 30/37 | feraligatr_munkidori_damage_transfer (91%) | team_rockets_persian_ex_attack_theft (36%) |
| 5 | `water_aggro` | **60.5%** | 56.0% | 32/37 | feraligatr_munkidori_damage_transfer (92%) | team_rockets_persian_ex_attack_theft (30%) |
| 6 | `scovillain_salazzle_spicy_rage` | **58.9%** | 61.0% | 30/37 | team_rockets_wobbuffet_orbeetle_damage_launder (84%) | panic_poison_paralysis (32%) |
| 7 | `arbok_muk_laser_darkbell` | **57.7%** | 56.0% | 27/37 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | toxic_slumber_vileplume_ex (26%) |
| 8 | `tr_crobat_absol_bench_snipe` | **57.1%** | 55.5% | 26/37 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (24%) |
| 9 | `arbok_team_rockets_muk_condition_stack` | **56.9%** | 54.0% | 24/37 | feraligatr_munkidori_damage_transfer (94%) | lurantis_heal_punish (28%) |
| 10 | `dhelmise_veluza_hide_n_sneak` | **56.7%** | 56.0% | 24/37 | feraligatr_munkidori_damage_transfer (86%) | team_rockets_persian_ex_attack_theft (35%) |
| 11 | `arbok_muk_trolley_darkbell` | **56.0%** | 57.5% | 24/37 | team_rockets_wobbuffet_orbeetle_damage_launder (93%) | toxic_slumber_vileplume_ex (25%) |
| 12 | `kyurem_vanilluxe_blizzard` | **56.0%** | 53.0% | 24/37 | feraligatr_munkidori_damage_transfer (84%) | panic_poison_paralysis (27%) |
| 13 | `mega_chandelure_ex_retreat_tax` | **55.7%** | 56.0% | 25/37 | feraligatr_munkidori_damage_transfer (86%) | panic_poison_paralysis (22%) |
| 14 | `krookodile_ex_relicanth_hand_disruption` | **55.2%** | 55.5% | 27/37 | team_rockets_wobbuffet_orbeetle_damage_launder (88%) | lurantis_heal_punish (22%) |
| 15 | `selective_bloom_cradily` | **54.8%** | 52.0% | 20/37 | darkness_mill_hand_lock (88%) | scovillain_salazzle_spicy_rage (30%) |
| 16 | `orthworm_ex_metal_retaliation` | **54.7%** | 51.5% | 19/37 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | scovillain_salazzle_spicy_rage (20%) |
| 17 | `meta_dragapult_pure` | **52.8%** | 50.5% | 19/37 | static_venom_drapion (80%) | panic_poison_paralysis (30%) |
| 18 | `heracross_sinistcha_tea` | **51.4%** | 50.0% | 18/37 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | lurantis_heal_punish (26%) |
| 19 | `stevens_carbink_damage_wall` | **51.4%** | 50.0% | 18/37 | feraligatr_munkidori_damage_transfer (74%) | panic_poison_paralysis (31%) |
| 20 | `team_rockets_koffing_weezing_bench_swarm` | **50.5%** | 50.0% | 17/37 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | toxic_slumber_vileplume_ex (11%) |
| 21 | `decidueye_ex_judge_sniper_lock` | **49.8%** | 49.5% | 17/37 | feraligatr_munkidori_damage_transfer (86%) | lurantis_heal_punish (16%) |
| 22 | `kangaskhan_tyrantrum_flip_mill` | **49.8%** | 48.0% | 15/37 | crabominable_veluza_food_prep (76%) | team_rockets_persian_ex_attack_theft (20%) |
| 23 | `mega_lopunny_dusknoir_snipe_finisher` | **49.4%** | 48.0% | 15/37 | feraligatr_munkidori_damage_transfer (84%) | panic_poison_paralysis (27%) |
| 24 | `eerie_inferno_ninetales_burn` | **49.0%** | 47.5% | 18/37 | feraligatr_munkidori_damage_transfer (84%) | water_aggro (21%) |
| 25 | `meta_dragapult_dusknoir` | **48.9%** | 48.0% | 16/37 | team_rockets_wobbuffet_orbeetle_damage_launder (81%) | panic_poison_paralysis (28%) |
| 26 | `ns_zoroark_night_joker_toolbox` | **46.7%** | 46.0% | 11/37 | static_venom_drapion (83%) | lurantis_heal_punish (27%) |
| 27 | `mega_scrafty_ex_darkness_tank` | **46.3%** | 46.0% | 11/37 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | lurantis_heal_punish (14%) |
| 28 | `veluza_sinistcha_ex_tea_service` | **45.0%** | 42.5% | 14/37 | feraligatr_munkidori_damage_transfer (82%) | panic_poison_paralysis (20%) |
| 29 | `team_rockets_spidops_swarm` | **44.1%** | 40.5% | 12/37 | feraligatr_munkidori_damage_transfer (84%) | lurantis_heal_punish (14%) |
| 30 | `hops_snorlax_stacked_buff` | **43.5%** | 40.0% | 9/37 | feraligatr_munkidori_damage_transfer (92%) | panic_poison_paralysis (10%) |
| 31 | `tr_arbok_yveltal_snow_coating` | **43.2%** | 44.0% | 11/37 | feraligatr_munkidori_damage_transfer (92%) | lurantis_heal_punish (14%) |
| 32 | `darkness_mill_hand_lock` | **41.5%** | 36.0% | 10/37 | feraligatr_munkidori_damage_transfer (85%) | lurantis_heal_punish (9%) |
| 33 | `chandelure_centiskorch_deck_out` | **41.3%** | 40.5% | 10/37 | salazzle_ex_team_rockets_muk_condition_stack (71%) | lurantis_heal_punish (11%) |
| 34 | `crabominable_veluza_food_prep` | **36.3%** | 34.5% | 3/37 | feraligatr_munkidori_damage_transfer (72%) | panic_poison_paralysis (18%) |
| 35 | `salazzle_ex_team_rockets_muk_condition_stack` | **31.0%** | 29.0% | 3/37 | ns_zoroark_night_joker_toolbox (57%) | lurantis_heal_punish (14%) |
| 36 | `static_venom_drapion` | **30.0%** | 27.5% | 3/37 | team_rockets_wobbuffet_orbeetle_damage_launder (68%) | panic_poison_paralysis (11%) |
| 37 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **20.9%** | 18.0% | 2/37 | feraligatr_munkidori_damage_transfer (80%) | lurantis_heal_punish (3%) |
| 38 | `feraligatr_munkidori_damage_transfer` | **18.1%** | 16.0% | 0/37 | salazzle_ex_team_rockets_muk_condition_stack (45%) | panic_poison_paralysis (3%) |

## Full matrix

Row's win rate against column.

| |panic_poison_p|lurantis_heal_|team_rockets_p|toxic_slumber_|water_aggro|scovillain_sal|arbok_muk_lase|tr_crobat_abso|arbok_team_roc|dhelmise_veluz|arbok_muk_trol|kyurem_vanillu|mega_chandelur|krookodile_ex_|selective_bloo|orthworm_ex_me|meta_dragapult|heracross_sini|stevens_carbin|team_rockets_k|decidueye_ex_j|kangaskhan_tyr|mega_lopunny_d|eerie_inferno_|meta_dragapult|ns_zoroark_nig|mega_scrafty_e|veluza_sinistc|team_rockets_s|hops_snorlax_s|tr_arbok_yvelt|darkness_mill_|chandelure_cen|crabominable_v|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **panic_poison_p** |—|54|50|52|67|68|70|66|71|64|72|73|78|62|64|77|70|70|69|76|79|77|73|78|72|70|73|80|74|90|84|80|78|82|85|89|96|97|
| **lurantis_heal_** |46|—|50|60|67|39|73|76|72|56|71|58|63|78|68|62|62|74|64|84|84|74|68|69|68|73|86|72|86|86|86|91|89|78|86|86|97|90|
| **team_rockets_p** |50|50|—|64|70|61|56|62|56|65|67|59|58|61|66|78|64|69|66|70|76|80|72|74|68|70|80|74|82|72|85|82|82|82|84|86|96|90|
| **toxic_slumber_** |48|40|36|—|52|39|74|56|66|54|75|58|48|70|42|52|56|60|64|89|54|52|54|38|65|53|73|66|63|78|76|76|58|68|80|69|89|91|
| **water_aggro** |33|33|30|48|—|68|48|52|55|54|50|53|55|51|56|56|57|54|56|60|62|53|54|79|56|54|68|68|68|70|76|69|81|74|82|78|88|92|
| **scovillain_sal** |32|61|39|61|32|—|55|58|52|54|61|38|42|58|70|80|61|72|61|58|56|54|72|49|64|68|64|58|74|65|68|56|35|56|68|70|84|69|
| **arbok_muk_lase** |30|27|44|26|52|45|—|50|52|52|56|54|60|39|40|59|58|52|56|50|67|62|50|60|54|70|54|62|68|66|62|66|64|74|79|84|97|96|
| **tr_crobat_abso** |34|24|38|44|48|42|50|—|44|50|54|51|65|53|40|53|58|48|54|56|56|68|58|53|60|61|56|70|64|59|62|64|64|70|81|80|95|86|
| **arbok_team_roc** |29|28|44|34|45|48|48|56|—|49|54|49|64|43|48|53|50|50|52|59|62|60|52|59|50|68|54|64|62|67|59|64|69|74|73|79|92|94|
| **dhelmise_veluz** |36|44|35|46|46|46|48|50|51|—|43|52|44|46|59|50|56|59|46|44|65|49|60|66|62|56|56|67|68|62|56|64|66|74|72|84|83|86|
| **arbok_muk_trol** |28|29|33|25|50|39|44|46|46|57|—|48|60|42|42|54|54|47|62|53|62|60|58|66|58|64|58|60|63|64|55|66|68|74|72|80|93|90|
| **kyurem_vanillu** |27|42|41|42|47|62|46|49|51|48|52|—|44|46|57|44|50|56|42|53|56|53|65|68|62|52|53|65|65|66|72|59|58|64|75|76|80|84|
| **mega_chandelur** |22|37|42|52|45|58|40|35|36|56|40|56|—|48|49|52|54|61|68|47|76|64|66|60|56|43|55|65|59|66|62|59|63|72|70|60|82|86|
| **krookodile_ex_** |38|22|39|30|49|42|61|47|57|54|58|54|52|—|40|58|52|40|58|62|38|53|51|56|59|54|58|56|56|66|66|64|60|68|78|73|88|86|
| **selective_bloo** |36|32|34|58|44|30|60|60|52|41|58|43|51|60|—|36|44|44|38|66|48|45|50|56|45|42|71|44|64|67|78|88|76|58|70|72|84|83|
| **orthworm_ex_me** |23|38|22|48|44|20|41|47|47|50|46|56|48|42|64|—|54|66|58|68|52|38|48|49|52|44|42|72|72|74|80|68|70|66|71|75|90|81|
| **meta_dragapult** |30|38|36|44|43|39|42|42|50|44|46|50|46|48|56|46|—|60|36|50|62|50|62|60|58|54|48|51|60|56|67|66|59|56|62|80|74|78|
| **heracross_sini** |30|26|31|40|46|28|48|52|50|41|53|44|39|60|56|34|40|—|38|56|49|46|60|41|52|55|72|67|60|46|56|78|44|72|60|73|86|74|
| **stevens_carbin** |31|36|34|36|44|39|44|46|48|54|38|58|32|42|62|42|64|62|—|46|47|54|48|38|65|54|50|68|64|53|55|54|40|70|67|70|72|74|
| **team_rockets_k** |24|16|30|11|40|42|50|44|41|56|47|47|53|38|34|32|50|44|54|—|50|58|58|42|46|59|44|70|66|60|53|50|60|78|72|68|90|89|
| **decidueye_ex_j** |21|16|24|46|38|44|33|44|38|35|38|44|24|62|52|48|38|51|53|50|—|60|50|42|46|62|69|53|51|64|39|70|50|66|79|74|82|86|
| **kangaskhan_tyr** |23|26|20|48|47|46|38|32|40|51|40|47|36|47|55|62|50|54|46|42|40|—|62|42|58|50|50|64|56|60|55|46|40|76|66|76|74|76|
| **mega_lopunny_d** |27|32|28|46|46|28|50|42|48|40|42|35|34|49|50|52|38|40|52|42|50|38|—|56|48|36|53|43|62|60|62|68|73|56|65|70|81|84|
| **eerie_inferno_** |22|31|26|62|21|51|40|47|41|34|34|32|40|44|44|51|40|59|62|58|58|58|44|—|48|54|48|43|46|52|54|59|60|56|71|69|72|84|
| **meta_dragapult** |28|32|32|35|44|36|46|40|50|38|42|38|44|41|55|48|42|48|35|54|54|42|52|52|—|44|54|46|56|54|61|59|58|54|64|74|81|74|
| **ns_zoroark_nig** |30|27|30|47|46|32|30|39|32|44|36|48|57|46|58|56|46|45|46|41|38|50|64|46|56|—|57|44|46|41|46|62|45|52|43|83|60|59|
| **mega_scrafty_e** |27|14|20|27|32|36|46|44|46|44|42|47|45|42|29|58|52|28|50|56|31|50|47|52|46|43|—|38|48|56|48|46|54|66|76|66|86|76|
| **veluza_sinistc** |20|28|26|34|32|42|38|30|36|33|40|35|35|44|56|28|49|33|32|30|47|36|57|57|54|56|62|—|54|40|44|64|52|59|56|70|72|82|
| **team_rockets_s** |26|14|18|37|32|26|32|36|38|32|37|35|41|44|36|28|40|40|36|34|49|44|38|54|44|54|52|46|—|50|56|64|60|63|66|68|78|84|
| **hops_snorlax_s** |10|14|28|22|30|35|34|41|33|38|36|34|34|34|33|26|44|54|47|40|36|40|40|48|46|59|44|60|50|—|46|46|58|67|72|62|76|92|
| **tr_arbok_yvelt** |16|14|15|24|24|32|38|38|41|44|45|28|38|34|22|20|33|44|45|47|61|45|38|46|39|54|52|56|44|54|—|44|68|66|67|57|72|92|
| **darkness_mill_** |20|9|18|24|31|44|34|36|36|36|34|41|41|36|12|32|34|22|46|50|30|54|32|41|41|38|54|36|36|54|56|—|76|58|70|62|78|85|
| **chandelure_cen** |22|11|18|42|19|65|36|36|31|34|32|42|37|40|24|30|41|56|60|40|50|60|27|40|42|55|46|48|40|42|32|24|—|58|71|50|58|68|
| **crabominable_v** |18|22|18|32|26|44|26|30|26|26|26|36|28|32|42|34|44|28|30|22|34|24|44|44|46|48|34|41|37|33|34|42|42|—|48|68|64|72|
| **salazzle_ex_te** |15|14|16|20|18|32|21|19|27|28|28|25|30|22|30|29|38|40|33|28|21|34|35|29|36|57|24|44|34|28|33|30|29|52|—|44|49|55|
| **static_venom_d** |11|14|14|31|22|30|16|20|21|16|20|24|40|27|28|25|20|27|30|32|26|24|30|31|26|17|34|30|32|38|43|38|50|32|56|—|68|68|
| **team_rockets_w** |4|3|4|11|12|16|3|5|8|17|7|20|18|12|16|10|26|14|28|10|18|26|19|28|19|40|14|28|22|24|28|22|42|36|51|32|—|80|
| **feraligatr_mun** |3|10|10|9|8|31|4|14|6|14|10|16|14|14|17|19|22|26|26|11|14|24|16|16|26|41|24|18|16|8|8|15|32|28|45|32|20|—|
