# Field results — every deck against every other deck

Full round robin over **44 decks**, **200 games** per pairing, 946 pairings, 189,200 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-11. **These supersede every number recorded in the deck files before this date**, and are not comparable with the 2026-09-10 run either: fourteen card effects went from inert to live in between, so the whole field shifted.

What changed since the 2026-09-10 field. A Stadium that matters only because another card NAMES it is now played — `Festival Grounds` gates Festival Lead's double attack and was never put down, so that archetype dealt exactly half its damage. `CONDITION_IMMUNITY` gained a consumer, and blanket immunity ("can't be affected by any Special Conditions") gained a rule, so ten cards stop being decoration. Eight more Trainers compile — `Precious Trolley` (in 7 of these decks), `Xerosic's Machinations` (5), `Dark Bell`, `Hand Trimmer`, `Sacred Ash`, `Energy Recycler`, `Great Haul Net`, `Lumiose Galette` — plus `Secret Box` and `Transformation Tome`. Trainers resolved through the compiled IR now pay their costs, which they never did. And devolving returns the Evolution card to its owner's hand instead of discarding it, which no card in Standard says to do.

> **Read the bottom of the table as a lower bound, not a verdict.** Both sides run the same greedy AI. A list whose edge is in sequencing — holding a Knock Out back, aiming spread damage at a Prize map, choosing when to take the turn off — is piloted by a policy that cannot do any of that, and six measured attempts to make the policy smarter all came out at no detectable difference. Where a deck's placement is known to be an artefact of that, its own file says so.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **73.0%** | 72.0% | 41/43 | feraligatr_munkidori_damage_transfer (98%) | scovillain_salazzle_spicy_rage (44%) |
| 2 | `panic_poison_paralysis` | **72.5%** | 73.5% | 42/43 | team_rockets_wobbuffet_orbeetle_damage_launder (96%) | lurantis_heal_punish (50%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **72.0%** | 73.0% | 41/43 | feraligatr_munkidori_damage_transfer (95%) | lurantis_heal_punish (48%) |
| 4 | `meta_mega_excadrill` | **63.5%** | 61.0% | 37/43 | meta_ns_zoroark (94%) | scovillain_salazzle_spicy_rage (39%) |
| 5 | `meta_raging_bolt` | **62.4%** | 62.0% | 38/43 | meta_ns_zoroark (88%) | arbok_muk_trolley_darkbell (40%) |
| 6 | `toxic_slumber_vileplume_ex` | **61.1%** | 62.5% | 34/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (31%) |
| 7 | `arbok_muk_laser_darkbell` | **60.5%** | 59.0% | 34/43 | meta_ns_zoroark (95%) | lurantis_heal_punish (28%) |
| 8 | `arbok_muk_trolley_darkbell` | **59.6%** | 60.0% | 32/43 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | lurantis_heal_punish (25%) |
| 9 | `water_aggro` | **59.5%** | 58.5% | 30/43 | meta_ns_zoroark (93%) | panic_poison_paralysis (24%) |
| 10 | `scovillain_salazzle_spicy_rage` | **58.7%** | 60.0% | 32/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (32%) |
| 11 | `dhelmise_veluza_hide_n_sneak` | **58.1%** | 57.5% | 30/43 | meta_ns_zoroark (94%) | panic_poison_paralysis (34%) |
| 12 | `krookodile_ex_relicanth_hand_disruption` | **57.9%** | 59.5% | 32/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (20%) |
| 13 | `tr_crobat_absol_bench_snipe` | **57.3%** | 57.0% | 28/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (19%) |
| 14 | `arbok_team_rockets_muk_condition_stack` | **57.1%** | 55.5% | 27/43 | meta_ns_zoroark (94%) | lurantis_heal_punish (30%) |
| 15 | `mega_chandelure_ex_retreat_tax` | **55.8%** | 56.5% | 29/43 | feraligatr_munkidori_damage_transfer (86%) | panic_poison_paralysis (24%) |
| 16 | `orthworm_ex_metal_retaliation` | **55.6%** | 54.0% | 26/43 | meta_festival_lead (88%) | panic_poison_paralysis (24%) |
| 17 | `kyurem_vanilluxe_blizzard` | **55.3%** | 54.5% | 25/43 | meta_ns_zoroark (89%) | panic_poison_paralysis (29%) |
| 18 | `meta_dragapult_pure` | **54.7%** | 54.0% | 28/43 | meta_ns_zoroark (87%) | team_rockets_persian_ex_attack_theft (27%) |
| 19 | `heracross_sinistcha_tea` | **53.1%** | 52.5% | 23/43 | meta_ns_zoroark (90%) | scovillain_salazzle_spicy_rage (24%) |
| 20 | `selective_bloom_cradily` | **52.8%** | 51.5% | 24/43 | feraligatr_munkidori_damage_transfer (88%) | meta_mega_excadrill (15%) |
| 21 | `stevens_carbink_damage_wall` | **52.5%** | 51.0% | 22/43 | meta_ns_zoroark (96%) | panic_poison_paralysis (22%) |
| 22 | `meta_dragapult_blaziken` | **51.3%** | 49.0% | 20/43 | meta_ns_zoroark (88%) | meta_raging_bolt (32%) |
| 23 | `team_rockets_koffing_weezing_bench_swarm` | **51.2%** | 51.5% | 23/43 | meta_ns_zoroark (92%) | toxic_slumber_vileplume_ex (12%) |
| 24 | `meta_dragapult_dusknoir` | **50.0%** | 47.0% | 17/43 | meta_ns_zoroark (84%) | lurantis_heal_punish (26%) |
| 25 | `kangaskhan_tyrantrum_flip_mill` | **49.7%** | 50.0% | 20/43 | meta_ns_zoroark (89%) | panic_poison_paralysis (24%) |
| 26 | `eerie_inferno_ninetales_burn` | **48.9%** | 47.5% | 20/43 | meta_ns_zoroark (90%) | water_aggro (18%) |
| 27 | `decidueye_ex_judge_sniper_lock` | **48.9%** | 48.0% | 19/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (12%) |
| 28 | `mega_lopunny_dusknoir_snipe_finisher` | **48.1%** | 46.0% | 17/43 | feraligatr_munkidori_damage_transfer (84%) | team_rockets_persian_ex_attack_theft (23%) |
| 29 | `mega_scrafty_ex_darkness_tank` | **48.1%** | 48.0% | 15/43 | meta_ns_zoroark (86%) | lurantis_heal_punish (14%) |
| 30 | `ns_zoroark_night_joker_toolbox` | **46.6%** | 45.5% | 13/43 | static_venom_drapion (79%) | lurantis_heal_punish (26%) |
| 31 | `veluza_sinistcha_ex_tea_service` | **46.5%** | 43.5% | 15/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (16%) |
| 32 | `team_rockets_spidops_swarm` | **45.0%** | 41.5% | 13/43 | meta_ns_zoroark (86%) | lurantis_heal_punish (16%) |
| 33 | `tr_arbok_yveltal_snow_coating` | **44.3%** | 44.0% | 14/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (14%) |
| 34 | `hops_snorlax_stacked_buff` | **44.2%** | 41.0% | 12/43 | meta_ns_zoroark (96%) | panic_poison_paralysis (14%) |
| 35 | `darkness_mill_hand_lock` | **43.0%** | 40.0% | 12/43 | feraligatr_munkidori_damage_transfer (84%) | lurantis_heal_punish (10%) |
| 36 | `chandelure_centiskorch_deck_out` | **42.4%** | 40.5% | 11/43 | meta_ns_zoroark (84%) | team_rockets_persian_ex_attack_theft (11%) |
| 37 | `crabominable_veluza_food_prep` | **40.3%** | 38.5% | 7/43 | meta_ns_zoroark (92%) | meta_mega_excadrill (20%) |
| 38 | `meta_slowking` | **40.3%** | 39.0% | 8/43 | meta_ns_zoroark (84%) | arbok_muk_laser_darkbell (16%) |
| 39 | `meta_festival_lead` | **36.0%** | 35.5% | 6/43 | meta_ns_zoroark (82%) | orthworm_ex_metal_retaliation (12%) |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | **34.2%** | 32.0% | 5/43 | meta_ns_zoroark (92%) | team_rockets_persian_ex_attack_theft (12%) |
| 41 | `static_venom_drapion` | **30.9%** | 28.0% | 4/43 | team_rockets_wobbuffet_orbeetle_damage_launder (68%) | lurantis_heal_punish (12%) |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **23.6%** | 19.5% | 2/43 | meta_ns_zoroark (82%) | arbok_muk_trolley_darkbell (3%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **20.6%** | 17.5% | 1/43 | meta_ns_zoroark (77%) | lurantis_heal_punish (2%) |
| 44 | `meta_ns_zoroark` | **12.6%** | 10.5% | 0/43 | static_venom_drapion (42%) | stevens_carbink_damage_wall (4%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|meta_mega_exca|meta_raging_bo|toxic_slumber_|arbok_muk_lase|arbok_muk_trol|water_aggro|scovillain_sal|dhelmise_veluz|krookodile_ex_|tr_crobat_abso|arbok_team_roc|mega_chandelur|orthworm_ex_me|kyurem_vanillu|meta_dragapult|heracross_sini|selective_bloo|stevens_carbin|meta_dragapult|team_rockets_k|meta_dragapult|kangaskhan_tyr|eerie_inferno_|decidueye_ex_j|mega_lopunny_d|mega_scrafty_e|ns_zoroark_nig|veluza_sinistc|team_rockets_s|tr_arbok_yvelt|hops_snorlax_s|darkness_mill_|chandelure_cen|crabominable_v|meta_slowking|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|50|52|51|48|67|72|75|69|44|64|80|81|70|53|65|69|64|70|78|60|67|86|74|70|70|88|65|86|74|69|84|84|82|90|86|80|70|78|84|88|94|98|91|
| **panic_poison_p** |50|—|50|52|56|52|66|72|76|66|66|62|64|66|76|76|71|62|72|73|78|62|80|61|76|77|83|67|76|66|84|74|83|86|84|74|79|81|64|88|86|96|96|90|
| **team_rockets_p** |48|50|—|52|57|69|64|60|65|68|58|71|60|62|64|66|64|73|71|69|66|66|74|73|73|80|80|77|80|66|74|76|86|80|84|89|78|75|78|88|84|94|95|88|
| **meta_mega_exca** |49|48|48|—|43|53|58|56|60|39|66|61|51|60|48|67|70|59|67|85|50|59|54|62|55|52|59|70|61|57|76|78|79|74|68|54|80|66|84|66|78|88|76|94|
| **meta_raging_bo** |52|44|43|57|—|56|42|40|58|48|55|58|52|52|57|61|53|62|62|80|54|68|51|70|57|62|63|69|68|59|66|71|72|64|68|66|76|68|74|73|84|78|80|88|
| **toxic_slumber_** |33|48|31|47|44|—|66|66|52|37|56|64|60|70|48|62|55|54|54|46|67|54|88|55|54|40|52|62|74|64|63|62|78|74|71|63|66|64|62|80|76|88|88|90|
| **arbok_muk_lase** |28|34|36|42|58|34|—|52|56|56|57|36|48|48|66|62|57|58|56|52|58|58|64|56|68|60|66|59|50|70|74|64|60|72|70|68|68|84|61|76|80|94|92|95|
| **arbok_muk_trol** |25|28|40|44|60|34|48|—|60|50|56|38|44|42|62|60|54|56|54|47|60|58|52|60|66|64|68|62|56|68|63|68|62|72|60|70|70|78|65|77|78|97|94|91|
| **water_aggro** |31|24|35|40|42|48|44|40|—|66|43|42|52|52|50|57|54|48|58|58|57|59|60|58|60|82|58|48|60|52|68|70|73|72|69|80|70|70|76|80|76|88|92|93|
| **scovillain_sal** |56|34|32|61|52|63|44|50|34|—|43|58|58|58|45|73|42|54|76|68|65|62|62|60|52|47|50|68|64|60|60|64|68|68|50|42|54|70|65|69|78|82|74|90|
| **dhelmise_veluz** |36|34|42|34|45|44|43|44|57|57|—|47|51|58|48|48|53|50|56|64|49|56|43|59|56|68|61|68|63|58|70|66|62|61|66|64|68|66|83|66|77|80|82|94|
| **krookodile_ex_** |20|38|29|39|42|36|64|62|58|42|53|—|58|65|60|56|61|54|44|36|60|62|70|61|60|66|46|53|59|50|56|56|69|66|55|66|71|66|72|74|72|86|84|93|
| **tr_crobat_abso** |19|36|40|49|48|40|52|56|48|42|49|42|—|50|58|53|46|43|46|42|56|62|53|62|65|60|53|62|57|64|57|60|62|62|68|67|64|71|62|82|80|95|86|93|
| **arbok_team_roc** |30|34|38|40|48|30|52|58|48|42|42|35|50|—|60|58|50|50|48|44|52|60|55|53|60|56|68|57|50|72|62|61|54|74|69|70|63|74|62|72|76|93|92|94|
| **mega_chandelur** |47|24|36|52|43|52|34|38|50|55|52|40|42|40|—|57|64|53|54|50|70|57|42|61|66|58|74|58|50|42|62|56|58|66|54|56|72|61|67|72|64|80|86|83|
| **orthworm_ex_me** |35|24|34|33|39|38|38|40|43|27|52|44|47|42|43|—|60|56|64|58|55|54|70|54|42|54|52|49|56|49|70|68|84|74|67|69|60|52|88|74|78|88|82|88|
| **kyurem_vanillu** |31|29|36|30|47|45|43|46|46|58|47|39|54|50|36|40|—|52|56|48|42|62|46|60|50|71|52|64|50|54|62|74|71|61|62|58|62|64|72|76|72|86|85|89|
| **meta_dragapult** |36|38|27|41|38|46|42|44|52|46|50|46|57|50|47|44|48|—|60|56|46|52|56|54|54|57|58|62|54|52|53|62|66|57|66|60|61|60|70|62|76|85|75|87|
| **heracross_sini** |30|28|29|33|38|46|44|46|42|24|44|56|54|52|46|36|44|40|—|54|38|45|62|52|48|41|49|58|66|60|58|69|60|57|79|57|64|54|78|68|72|88|80|90|
| **selective_bloo** |22|27|31|15|20|54|48|53|42|32|36|64|58|56|50|42|52|44|46|—|36|36|66|51|44|61|60|45|66|42|46|56|78|68|84|76|60|51|64|67|78|83|88|73|
| **stevens_carbin** |40|22|34|50|46|33|42|40|43|35|51|40|44|48|30|45|58|54|62|64|—|56|44|56|53|36|48|54|42|64|66|60|46|56|52|44|70|70|86|60|62|73|82|96|
| **meta_dragapult** |33|38|34|41|32|46|42|42|41|38|44|38|38|40|43|46|38|48|55|64|44|—|49|57|42|54|70|60|51|49|52|62|62|57|60|62|58|50|66|55|76|74|67|88|
| **team_rockets_k** |14|20|26|46|49|12|36|48|40|38|57|30|47|45|58|30|54|44|38|34|56|51|—|49|52|38|53|52|44|60|72|64|54|60|54|61|73|72|64|66|70|89|90|92|
| **meta_dragapult** |26|39|27|38|30|45|44|40|42|40|41|39|38|47|39|46|40|46|48|49|44|43|51|—|46|56|66|64|50|49|48|57|56|56|60|52|54|47|68|66|75|80|76|84|
| **kangaskhan_tyr** |30|24|27|45|43|46|32|34|40|48|44|40|35|40|34|58|50|46|52|56|47|58|48|54|—|42|35|56|52|50|60|54|50|59|50|40|64|66|63|62|72|64|77|89|
| **eerie_inferno_** |30|23|20|48|38|60|40|36|18|53|32|34|40|44|42|46|29|43|59|39|64|46|62|44|58|—|54|45|47|56|38|58|52|48|54|58|50|58|61|68|70|70|82|90|
| **decidueye_ex_j** |12|17|20|41|37|48|34|32|42|50|39|54|47|32|26|48|48|42|51|40|52|30|47|34|65|46|—|55|66|64|52|50|38|54|70|52|62|50|56|74|68|81|88|93|
| **mega_lopunny_d** |35|33|23|30|31|38|41|38|52|32|32|47|38|43|42|51|36|38|42|55|46|40|48|36|44|55|45|—|58|32|50|60|61|56|62|66|50|52|70|63|62|78|84|77|
| **mega_scrafty_e** |14|24|20|39|32|26|50|44|40|36|37|41|43|50|50|44|50|46|34|34|58|49|56|50|48|53|34|42|—|48|48|54|52|59|46|55|62|60|66|70|59|83|79|86|
| **ns_zoroark_nig** |26|34|34|43|41|36|30|32|48|40|42|50|36|28|58|51|46|48|40|58|36|51|40|51|50|44|36|68|52|—|46|46|42|44|52|44|50|68|50|46|79|56|58|77|
| **veluza_sinistc** |31|16|26|24|34|37|26|37|32|40|30|44|43|38|38|30|38|47|42|54|34|48|28|52|40|62|48|50|52|54|—|54|49|42|64|48|57|60|78|56|69|74|84|92|
| **team_rockets_s** |16|26|24|22|29|38|36|32|30|36|34|44|40|39|44|32|26|38|31|44|40|38|36|43|46|42|50|40|46|54|46|—|55|52|67|70|58|52|56|64|66|85|82|86|
| **tr_arbok_yvelt** |16|17|14|21|28|22|40|38|27|32|38|31|38|46|42|16|29|34|40|22|54|38|46|44|50|48|62|39|48|58|51|45|—|54|48|71|67|56|64|68|58|72|86|90|
| **hops_snorlax_s** |18|14|20|26|36|26|28|28|28|32|39|34|38|26|34|26|39|43|43|32|44|43|40|44|41|52|46|44|41|56|58|48|46|—|40|61|62|62|70|70|68|70|88|96|
| **darkness_mill_** |10|16|16|32|32|29|30|40|31|50|34|45|32|31|46|33|38|34|21|16|48|40|46|40|50|46|30|38|54|48|36|33|52|60|—|76|58|52|58|70|60|78|84|79|
| **chandelure_cen** |14|26|11|46|34|37|32|30|20|58|36|34|33|30|44|31|42|40|43|24|56|38|39|48|60|42|48|34|45|56|52|30|29|39|24|—|60|68|48|74|50|62|72|84|
| **crabominable_v** |20|21|22|20|24|34|32|30|30|46|32|29|36|37|28|40|38|39|36|40|30|42|27|46|36|50|38|50|38|50|43|42|33|38|42|40|—|50|62|51|64|62|74|92|
| **meta_slowking** |30|19|25|34|32|36|16|22|30|30|34|34|29|26|39|48|36|40|46|49|30|50|28|53|34|42|50|48|40|32|40|48|44|38|48|32|50|—|56|51|66|52|57|84|
| **meta_festival_** |22|36|22|16|26|38|39|35|24|35|17|28|38|38|33|12|28|30|22|36|14|34|36|32|37|39|44|30|34|50|22|44|36|30|42|52|38|44|—|47|66|55|64|82|
| **salazzle_ex_te** |16|12|12|34|27|20|24|23|20|31|34|26|18|28|28|26|24|38|32|33|40|45|34|34|38|32|26|37|30|54|44|36|32|30|30|26|49|49|53|—|43|52|56|92|
| **static_venom_d** |12|14|16|22|16|24|20|22|24|22|23|28|20|24|36|22|28|24|28|22|38|24|30|25|28|30|32|38|41|21|31|34|42|32|40|50|36|34|34|57|—|68|60|58|
| **team_rockets_w** |6|4|6|12|22|12|6|3|12|18|20|14|5|7|20|12|14|15|12|17|27|26|11|20|36|30|19|22|17|44|26|15|28|30|22|38|38|48|45|48|32|—|74|82|
| **feraligatr_mun** |2|4|5|24|20|12|8|6|8|26|18|16|14|8|14|18|15|25|20|12|18|33|10|24|23|18|12|16|21|42|16|18|14|12|16|28|26|43|36|44|40|26|—|77|
| **meta_ns_zoroar** |9|10|12|6|12|10|5|9|7|10|6|7|7|6|17|12|11|13|10|27|4|12|8|16|11|10|7|23|14|23|8|14|10|4|21|16|8|16|18|8|42|18|23|—|
