# Field results — every deck against every other deck

Full round robin over **45 decks**, **200 games** per pairing, 990 pairings, 198,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-16, after the Stadium-passive fix. **These supersede every number in the deck files before this date** and are not comparable with the 2026-09-15 field: the engine changed materially in between.

What changed since 2026-09-15. Three engine bugs, each of which had been silently suppressing real card text:
- **20 Stadium passives were inert.** `_passive_actions` only ever walked Pokemon Abilities, so a Stadium's own compiled effect reached nothing. Stadiums now contribute their actions with `holder=None`, and third-person Stadium text ("that player may search *their* deck") is normalised to first person before it compiles.
- **Stadiums a deck wanted but did not name were never played.** `_stadium_has_effect` asked only whether the Stadium’s own text compiled. A Stadium that any of your cards *names* is now worth playing, which is why `Festival Grounds` had never once hit the table.
- **Blind discards threw away the wrong cards.** Costs that discard from hand picked arbitrarily; they now rank by `pitch_rank`.

One new deck joined the field: `metal_metang_excadrill`, the list reviewed on 2026-09-16. Every other deck is unchanged, so a like-for-like delta against the previous field is in the section below the table.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **72.4%** | 71.0% | 43/44 | feraligatr_munkidori_damage_transfer (95%) | scovillain_salazzle_spicy_rage (46%) |
| 2 | `panic_poison_paralysis` | **71.1%** | 70.2% | 41/44 | feraligatr_munkidori_damage_transfer (96%) | lurantis_heal_punish (46%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **70.6%** | 69.8% | 42/44 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (44%) |
| 4 | `scovillain_salazzle_spicy_rage` | **63.8%** | 64.2% | 37/44 | meta_ns_zoroark (94%) | team_rockets_persian_ex_attack_theft (38%) |
| 5 | `krookodile_ex_relicanth_hand_disruption` | **63.5%** | 64.0% | 37/44 | meta_ns_zoroark (92%) | lurantis_heal_punish (28%) |
| 6 | `meta_raging_bolt` | **63.0%** | 62.8% | 37/44 | meta_ns_zoroark (93%) | arbok_muk_laser_darkbell (36%) |
| 7 | `meta_mega_excadrill` | **61.0%** | 61.2% | 36/44 | meta_ns_zoroark (89%) | scovillain_salazzle_spicy_rage (36%) |
| 8 | `toxic_slumber_vileplume_ex` | **59.9%** | 62.0% | 34/44 | feraligatr_munkidori_damage_transfer (94%) | lurantis_heal_punish (32%) |
| 9 | `heracross_sinistcha_tea` | **59.6%** | 59.0% | 33/44 | meta_ns_zoroark (92%) | scovillain_salazzle_spicy_rage (27%) |
| 10 | `arbok_muk_laser_darkbell` | **58.7%** | 59.0% | 31/44 | feraligatr_munkidori_damage_transfer (96%) | panic_poison_paralysis (28%) |
| 11 | `arbok_muk_trolley_darkbell` | **56.7%** | 56.0% | 31/44 | meta_ns_zoroark (94%) | lurantis_heal_punish (24%) |
| 12 | `mega_chandelure_ex_retreat_tax` | **56.6%** | 59.0% | 31/44 | feraligatr_munkidori_damage_transfer (88%) | panic_poison_paralysis (28%) |
| 13 | `kyurem_vanilluxe_blizzard` | **55.8%** | 55.0% | 27/44 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | team_rockets_persian_ex_attack_theft (29%) |
| 14 | `metal_metang_excadrill` | **55.5%** | 55.2% | 27/44 | meta_ns_zoroark (90%) | scovillain_salazzle_spicy_rage (28%) |
| 15 | `team_rockets_koffing_weezing_bench_swarm` | **54.7%** | 54.0% | 28/44 | feraligatr_munkidori_damage_transfer (91%) | lurantis_heal_punish (19%) |
| 16 | `arbok_team_rockets_muk_condition_stack` | **54.5%** | 53.0% | 27/44 | feraligatr_munkidori_damage_transfer (94%) | lurantis_heal_punish (24%) |
| 17 | `meta_dragapult_pure` | **54.0%** | 51.5% | 25/44 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (28%) |
| 18 | `mega_lopunny_dusknoir_snipe_finisher` | **53.4%** | 52.2% | 24/44 | feraligatr_munkidori_damage_transfer (85%) | meta_mega_excadrill (33%) |
| 19 | `dhelmise_veluza_hide_n_sneak` | **53.4%** | 51.2% | 24/44 | meta_ns_zoroark (96%) | lurantis_heal_punish (22%) |
| 20 | `water_aggro` | **53.2%** | 50.2% | 22/44 | feraligatr_munkidori_damage_transfer (95%) | panic_poison_paralysis (27%) |
| 21 | `decidueye_ex_judge_sniper_lock` | **52.7%** | 51.2% | 23/44 | feraligatr_munkidori_damage_transfer (90%) | team_rockets_persian_ex_attack_theft (16%) |
| 22 | `tr_crobat_absol_bench_snipe` | **52.5%** | 51.2% | 25/44 | meta_ns_zoroark (90%) | lurantis_heal_punish (14%) |
| 23 | `orthworm_ex_metal_retaliation` | **51.8%** | 49.8% | 19/44 | meta_festival_lead (90%) | scovillain_salazzle_spicy_rage (12%) |
| 24 | `meta_dragapult_blaziken` | **51.2%** | 49.2% | 21/44 | meta_ns_zoroark (86%) | meta_raging_bolt (32%) |
| 25 | `selective_bloom_cradily` | **51.1%** | 48.0% | 20/44 | team_rockets_wobbuffet_orbeetle_damage_launder (86%) | meta_mega_excadrill (15%) |
| 26 | `stevens_carbink_damage_wall` | **51.0%** | 47.5% | 18/44 | meta_ns_zoroark (93%) | scovillain_salazzle_spicy_rage (26%) |
| 27 | `kangaskhan_tyrantrum_flip_mill` | **50.1%** | 49.8% | 21/44 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (26%) |
| 28 | `ns_zoroark_night_joker_toolbox` | **50.0%** | 48.0% | 18/44 | static_venom_drapion (76%) | arbok_muk_trolley_darkbell (34%) |
| 29 | `mega_scrafty_ex_darkness_tank` | **49.9%** | 49.8% | 21/44 | meta_ns_zoroark (93%) | lurantis_heal_punish (13%) |
| 30 | `eerie_inferno_ninetales_burn` | **48.9%** | 48.0% | 20/44 | meta_ns_zoroark (90%) | panic_poison_paralysis (20%) |
| 31 | `meta_dragapult_dusknoir` | **48.6%** | 45.2% | 14/44 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (24%) |
| 32 | `veluza_sinistcha_ex_tea_service` | **48.6%** | 47.2% | 20/44 | meta_ns_zoroark (92%) | panic_poison_paralysis (20%) |
| 33 | `hops_snorlax_stacked_buff` | **44.2%** | 42.0% | 13/44 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (13%) |
| 34 | `chandelure_centiskorch_deck_out` | **44.1%** | 44.8% | 14/44 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (14%) |
| 35 | `team_rockets_spidops_swarm` | **43.7%** | 40.5% | 13/44 | meta_ns_zoroark (93%) | lurantis_heal_punish (16%) |
| 36 | `meta_slowking` | **43.6%** | 43.5% | 11/44 | meta_ns_zoroark (80%) | team_rockets_persian_ex_attack_theft (17%) |
| 37 | `crabominable_veluza_food_prep` | **43.5%** | 41.0% | 10/44 | meta_ns_zoroark (94%) | team_rockets_persian_ex_attack_theft (21%) |
| 38 | `tr_arbok_yveltal_snow_coating` | **41.1%** | 40.2% | 11/44 | feraligatr_munkidori_damage_transfer (90%) | panic_poison_paralysis (12%) |
| 39 | `darkness_mill_hand_lock` | **37.6%** | 36.0% | 8/44 | feraligatr_munkidori_damage_transfer (86%) | lurantis_heal_punish (6%) |
| 40 | `meta_festival_lead` | **35.3%** | 33.5% | 4/44 | meta_ns_zoroark (82%) | orthworm_ex_metal_retaliation (10%) |
| 41 | `salazzle_ex_team_rockets_muk_condition_stack` | **33.8%** | 30.8% | 4/44 | meta_ns_zoroark (87%) | panic_poison_paralysis (13%) |
| 42 | `static_venom_drapion` | **28.6%** | 25.5% | 4/44 | team_rockets_wobbuffet_orbeetle_damage_launder (65%) | panic_poison_paralysis (9%) |
| 43 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **25.0%** | 21.5% | 4/44 | meta_ns_zoroark (82%) | lurantis_heal_punish (5%) |
| 44 | `feraligatr_munkidori_damage_transfer` | **18.6%** | 15.0% | 1/44 | meta_ns_zoroark (80%) | arbok_muk_laser_darkbell (4%) |
| 45 | `meta_ns_zoroark` | **13.0%** | 10.2% | 0/44 | static_venom_drapion (41%) | dhelmise_veluza_hide_n_sneak (4%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|scovillain_sal|krookodile_ex_|meta_raging_bo|meta_mega_exca|toxic_slumber_|heracross_sini|arbok_muk_lase|arbok_muk_trol|mega_chandelur|kyurem_vanillu|metal_metang_e|team_rockets_k|arbok_team_roc|meta_dragapult|mega_lopunny_d|dhelmise_veluz|water_aggro|decidueye_ex_j|tr_crobat_abso|orthworm_ex_me|meta_dragapult|selective_bloo|stevens_carbin|kangaskhan_tyr|ns_zoroark_nig|mega_scrafty_e|eerie_inferno_|meta_dragapult|veluza_sinistc|hops_snorlax_s|chandelure_cen|team_rockets_s|meta_slowking|crabominable_v|tr_arbok_yvelt|darkness_mill_|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|54|50|46|72|54|53|68|58|69|76|60|64|57|81|76|64|60|78|69|81|86|71|60|78|64|69|65|87|71|70|68|82|86|84|70|74|86|94|80|78|89|95|95|91|
| **panic_poison_p** |46|—|56|58|46|56|60|50|68|72|67|72|68|66|71|70|59|64|68|73|77|68|78|61|64|69|74|62|73|80|64|80|87|75|74|80|76|88|86|63|87|91|93|96|90|
| **team_rockets_p** |50|44|—|62|60|56|56|66|60|64|56|58|71|64|68|58|72|61|70|67|84|62|77|64|62|66|74|64|70|74|76|73|80|86|80|83|79|74|87|78|86|84|94|94|92|
| **scovillain_sal** |54|42|38|—|49|53|64|66|73|59|61|41|43|72|66|64|57|60|58|46|58|66|88|64|75|74|54|64|70|58|68|64|69|39|76|64|54|73|72|67|80|82|88|78|94|
| **krookodile_ex_** |28|54|40|51|—|39|56|47|44|68|69|65|68|62|69|69|66|60|73|60|38|63|72|61|40|72|63|58|63|72|62|59|74|74|62|59|71|74|76|66|84|76|87|88|92|
| **meta_raging_bo** |46|44|44|47|61|—|60|64|56|36|44|60|58|62|53|50|62|66|62|60|55|61|67|68|80|56|64|56|72|58|71|64|70|64|74|64|68|75|70|78|72|86|75|77|93|
| **meta_mega_exca** |47|40|44|36|44|40|—|62|59|54|54|38|65|60|54|59|59|67|52|72|60|54|61|62|85|53|54|64|62|56|62|70|68|46|68|70|73|80|70|74|64|77|78|78|89|
| **toxic_slumber_** |32|50|34|34|53|36|38|—|64|68|66|38|57|46|76|72|55|52|70|62|48|64|66|52|52|63|55|62|71|42|58|62|72|55|56|55|66|76|78|66|75|75|87|94|83|
| **heracross_sini** |42|32|40|27|56|44|41|36|—|58|60|48|46|47|61|59|58|60|56|68|53|66|57|47|68|54|62|59|74|51|55|64|68|50|73|62|67|64|84|80|76|81|87|90|92|
| **arbok_muk_lase** |31|28|36|41|32|64|46|32|42|—|49|70|50|52|57|50|52|58|60|57|60|50|65|61|44|65|64|64|50|59|59|68|71|62|73|68|66|59|71|59|76|80|92|96|92|
| **arbok_muk_trol** |24|33|44|39|31|56|46|34|40|51|—|61|56|56|45|56|48|57|52|52|54|48|64|60|42|63|57|66|42|64|56|62|66|56|71|80|62|54|62|60|68|79|94|92|94|
| **mega_chandelur** |40|28|42|59|35|40|62|62|52|30|39|—|63|62|48|38|52|46|58|60|74|38|62|56|52|57|64|40|48|59|60|64|64|68|58|57|72|64|62|70|76|62|78|88|82|
| **kyurem_vanillu** |36|32|29|57|32|42|35|43|54|50|44|37|—|35|49|55|52|56|47|60|50|56|43|58|64|45|55|50|55|70|64|56|69|52|69|56|68|76|62|68|83|78|89|88|86|
| **metal_metang_e** |43|34|36|28|38|38|40|54|53|48|44|38|65|—|41|57|56|58|52|62|49|56|58|53|79|48|44|44|57|47|58|60|64|42|70|55|68|72|62|78|62|83|78|78|90|
| **team_rockets_k** |19|29|32|34|31|47|46|24|39|43|55|52|51|59|—|54|49|46|60|56|56|45|46|50|42|58|64|52|46|52|54|70|63|64|70|64|62|68|64|62|73|84|86|91|90|
| **arbok_team_roc** |24|30|42|36|31|50|41|28|41|50|44|62|45|43|46|—|52|56|45|54|52|48|54|56|42|54|51|62|52|55|52|63|71|57|66|68|59|54|78|56|70|80|90|94|93|
| **meta_dragapult** |36|41|28|43|34|38|41|45|42|48|52|48|48|44|51|48|—|60|46|52|62|52|50|50|58|51|62|53|58|58|60|46|46|54|64|57|61|65|70|70|62|78|79|82|90|
| **mega_lopunny_d** |40|36|39|40|40|34|33|48|40|42|43|54|44|42|54|44|40|—|58|55|52|50|62|46|56|54|50|38|53|60|50|50|58|77|60|54|58|76|68|75|72|76|79|85|72|
| **dhelmise_veluz** |22|32|30|42|27|38|48|30|44|40|48|42|53|48|40|55|54|42|—|47|52|48|45|48|58|50|53|60|50|58|62|68|52|62|62|71|68|50|56|83|71|74|79|86|96|
| **water_aggro** |31|27|33|54|40|40|28|38|32|43|48|40|40|38|44|46|48|45|53|—|50|47|50|48|51|53|43|42|57|76|60|52|57|84|62|52|62|70|66|76|77|74|80|95|88|
| **decidueye_ex_j** |19|23|16|42|62|45|40|52|47|40|46|26|50|51|44|48|38|48|48|50|—|58|57|34|54|54|68|58|69|46|44|54|67|54|52|60|67|44|72|67|71|74|82|90|90|
| **tr_crobat_abso** |14|32|38|34|37|39|46|36|34|50|52|62|44|44|55|52|48|50|52|53|42|—|50|53|45|52|62|52|49|49|48|48|56|64|58|70|58|51|64|55|75|76|83|86|90|
| **orthworm_ex_me** |29|22|23|12|28|33|39|34|43|35|36|38|57|42|54|46|50|38|55|50|43|50|—|48|64|55|36|40|45|48|59|64|74|68|70|50|58|84|67|90|66|72|88|84|86|
| **meta_dragapult** |40|39|36|36|39|32|38|48|53|39|40|44|42|47|50|44|50|54|52|52|66|47|52|—|60|36|46|40|52|44|62|45|58|54|66|46|49|69|64|63|53|78|74|71|86|
| **selective_bloo** |22|36|38|25|60|20|15|48|32|56|58|48|36|21|58|58|42|44|42|49|46|55|36|40|—|36|44|34|70|56|48|44|72|81|59|45|56|75|81|70|69|77|86|86|73|
| **stevens_carbin** |36|31|34|26|28|44|47|37|46|35|37|43|55|52|42|46|49|46|50|47|46|48|45|64|64|—|40|62|43|34|60|59|56|36|70|68|62|50|52|79|68|65|73|77|93|
| **kangaskhan_tyr** |31|26|26|46|37|36|46|45|38|36|43|36|45|56|36|49|38|50|47|57|32|38|64|54|56|60|—|50|51|44|50|54|66|32|60|61|66|55|50|63|68|72|68|80|90|
| **ns_zoroark_nig** |35|38|36|36|42|44|36|38|41|36|34|60|50|56|48|38|47|62|40|58|42|48|60|60|66|38|50|—|60|53|52|48|46|45|47|70|59|45|66|51|50|76|60|62|75|
| **mega_scrafty_e** |13|27|30|30|37|28|38|29|26|50|58|52|45|43|54|48|42|47|50|43|31|51|55|48|30|57|49|40|—|58|51|40|71|70|50|56|64|60|52|68|78|70|86|80|93|
| **eerie_inferno_** |29|20|26|42|28|42|44|58|49|41|36|41|30|53|48|45|42|40|42|24|54|51|52|56|44|66|56|47|42|—|46|38|51|48|54|58|52|57|67|52|74|66|68|85|90|
| **meta_dragapult** |30|36|24|32|38|29|38|42|45|41|44|40|36|42|46|48|40|50|38|40|56|52|41|38|52|40|50|48|49|54|—|42|45|62|58|50|49|64|63|70|63|74|75|76|86|
| **veluza_sinistc** |32|20|27|36|41|36|30|38|36|32|38|36|44|40|30|37|54|50|32|48|46|52|36|55|56|41|46|52|60|62|58|—|41|54|50|51|51|54|73|79|56|72|75|86|92|
| **hops_snorlax_s** |18|13|20|31|26|30|32|28|32|29|34|36|31|36|37|29|54|42|48|43|33|44|26|42|28|44|34|54|29|49|55|59|—|58|50|48|56|64|50|69|74|68|75|94|94|
| **chandelure_cen** |14|25|14|61|26|36|54|45|50|38|44|32|48|58|36|43|46|23|38|16|46|36|32|46|19|64|68|55|30|52|38|46|42|—|36|68|48|32|23|62|78|57|61|74|86|
| **team_rockets_s** |16|26|20|24|38|26|32|44|27|27|29|42|31|30|30|34|36|40|38|38|48|42|30|34|41|30|40|53|50|46|42|50|50|64|—|54|57|58|72|60|57|68|74|84|93|
| **meta_slowking** |30|20|17|36|41|36|30|45|38|32|20|43|44|45|36|32|43|46|29|48|40|30|50|54|55|32|39|30|44|42|50|49|52|32|46|—|53|60|58|61|48|74|64|62|80|
| **crabominable_v** |26|24|21|46|29|32|27|34|33|34|38|28|32|32|38|41|39|42|32|38|33|42|42|51|44|38|34|41|36|48|51|49|44|52|43|47|—|46|60|78|58|72|64|78|94|
| **tr_arbok_yvelt** |14|12|26|27|26|25|20|24|36|41|46|36|24|28|32|46|35|24|50|30|56|49|16|31|25|50|45|55|40|43|36|46|36|68|42|40|54|—|48|58|62|59|76|90|84|
| **darkness_mill_** |6|14|13|28|24|30|30|22|16|29|38|38|38|38|36|22|30|32|44|34|28|36|33|36|19|48|50|34|48|33|37|27|50|77|28|42|40|52|—|40|64|51|60|86|74|
| **meta_festival_** |20|37|22|33|34|22|26|34|20|41|40|30|32|22|38|44|30|25|17|24|33|45|10|37|30|21|37|49|32|48|30|21|31|38|40|39|22|42|60|—|38|66|49|63|82|
| **salazzle_ex_te** |22|13|14|20|16|28|36|25|24|24|32|24|17|38|27|30|38|28|29|23|29|25|34|47|31|32|32|50|22|26|37|44|26|22|43|52|42|38|36|62|—|48|47|62|87|
| **static_venom_d** |11|9|16|18|24|14|23|25|19|20|21|38|22|17|16|20|22|24|26|26|26|24|28|22|23|35|28|24|30|34|26|28|32|43|32|26|28|41|49|34|52|—|65|64|59|
| **team_rockets_w** |5|7|6|12|13|25|22|13|13|8|6|22|11|22|14|10|21|21|21|20|18|17|12|26|14|27|32|40|14|32|25|25|25|39|26|36|36|24|40|51|53|35|—|80|82|
| **feraligatr_mun** |5|4|6|22|12|23|22|6|10|4|8|12|12|22|9|6|18|15|14|5|10|14|16|29|14|23|20|38|20|15|24|14|6|26|16|38|22|10|14|37|38|36|20|—|80|
| **meta_ns_zoroar** |9|10|8|6|8|7|11|17|8|8|6|18|14|10|10|7|10|28|4|12|10|10|14|14|27|7|10|25|7|10|14|8|6|14|7|20|6|16|26|18|13|41|18|20|—|

## Like-for-like delta against the 2026-09-15 field

The new field has 45 decks, the old one 44, so the mean columns above are not directly comparable. This table restricts both runs to the **43 opponents they share** and is therefore an honest before/after.

Noise floor: each pairing is 200 games (SE ≈ 3.5 points), and the seed stream diverges the moment engine behaviour changes, so a per-deck mean over 43 opponents carries SE ≈ **0.76 points**. Rows inside ±1.5 are noise; only the rows outside that are claims. Across the whole matrix the mean absolute per-pairing move is 5.63 points against 3.99 expected from divergence alone, so there is real signal on top of the churn — but it lives in the aggregates, not in any single cell.

| deck | old | new | delta |
|---|---|---|---|
| `meta_festival_lead` | 20.6% | 35.6% | **+15.06** |
| `krookodile_ex_relicanth_hand_disruption` | 56.5% | 63.5% | **+7.00** |
| `heracross_sinistcha_tea` | 54.4% | 59.9% | **+5.51** |
| `crabominable_veluza_food_prep` | 38.9% | 43.8% | **+4.86** |
| `team_rockets_koffing_weezing_bench_swarm` | 51.1% | 54.6% | **+3.51** |
| `mega_lopunny_dusknoir_snipe_finisher` | 50.3% | 53.7% | **+3.45** |
| `scovillain_salazzle_spicy_rage` | 60.2% | 63.6% | **+3.41** |
| `decidueye_ex_judge_sniper_lock` | 49.8% | 52.7% | **+2.90** |
| `mega_scrafty_ex_darkness_tank` | 47.2% | 50.1% | **+2.90** |
| `veluza_sinistcha_ex_tea_service` | 46.1% | 48.8% | **+2.67** |
| `team_rockets_wobbuffet_orbeetle_damage_launder` | 23.2% | 25.1% | **+1.87** |
| `ns_zoroark_night_joker_toolbox` | 48.7% | 49.9% | +1.16 |
| `chandelure_centiskorch_deck_out` | 42.8% | 43.8% | +1.02 |
| `mega_chandelure_ex_retreat_tax` | 56.0% | 56.5% | +0.55 |
| `arbok_muk_trolley_darkbell` | 56.5% | 56.7% | +0.26 |
| `lurantis_heal_punish` | 72.6% | 72.7% | +0.08 |
| `meta_slowking` | 43.4% | 43.5% | +0.08 |
| `meta_raging_bolt` | 63.1% | 63.0% | -0.10 |
| `kyurem_vanilluxe_blizzard` | 56.7% | 56.3% | -0.36 |
| `arbok_muk_laser_darkbell` | 59.4% | 58.9% | -0.55 |
| `meta_ns_zoroark` | 13.6% | 13.1% | -0.57 |
| `kangaskhan_tyrantrum_flip_mill` | 50.7% | 50.0% | -0.66 |
| `meta_mega_excadrill` | 61.7% | 61.0% | -0.71 |
| `team_rockets_spidops_swarm` | 44.8% | 44.0% | -0.74 |
| `team_rockets_persian_ex_attack_theft` | 71.7% | 70.8% | -0.87 |
| `toxic_slumber_vileplume_ex` | 61.2% | 60.2% | -1.01 |
| `salazzle_ex_team_rockets_muk_condition_stack` | 34.9% | 33.7% | -1.21 |
| `static_venom_drapion` | 30.2% | 28.9% | -1.28 |
| `hops_snorlax_stacked_buff` | 45.7% | 44.4% | -1.31 |
| `meta_dragapult_blaziken` | 52.8% | 51.3% | -1.50 |
| `panic_poison_paralysis` | 72.8% | 71.2% | **-1.58** |
| `eerie_inferno_ninetales_burn` | 50.8% | 48.8% | **-1.98** |
| `feraligatr_munkidori_damage_transfer` | 20.7% | 18.5% | **-2.16** |
| `meta_dragapult_dusknoir` | 51.0% | 48.7% | **-2.30** |
| `stevens_carbink_damage_wall` | 53.3% | 50.9% | **-2.40** |
| `tr_arbok_yveltal_snow_coating` | 43.9% | 41.4% | **-2.50** |
| `meta_dragapult_pure` | 56.8% | 54.3% | **-2.53** |
| `selective_bloom_cradily` | 54.4% | 51.8% | **-2.69** |
| `arbok_team_rockets_muk_condition_stack` | 58.0% | 54.8% | **-3.23** |
| `dhelmise_veluza_hide_n_sneak` | 56.8% | 53.5% | **-3.30** |
| `orthworm_ex_metal_retaliation` | 55.7% | 52.0% | **-3.67** |
| `darkness_mill_hand_lock` | 43.2% | 37.6% | **-5.58** |
| `tr_crobat_absol_bench_snipe` | 58.2% | 52.7% | **-5.58** |
| `water_aggro` | 59.5% | 53.6% | **-5.90** |

`meta_festival_lead` is the headline: **+15.1 points**. That deck is built around `Festival Grounds`, and the Stadium had never once been played in any measurement before this one — `_stadium_has_effect` asked whether the Stadium's own text compiled, and Festival Grounds' text does nothing on its own; the payoff is on the Pokemon that name it. It is still a losing deck at 35.6%, but it had been scored at 20.6% for a mechanic that was switched off.

