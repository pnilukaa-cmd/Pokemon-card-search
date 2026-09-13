# Field results — every deck against every other deck

Full round robin over **44 decks**, **200 games** per pairing, 946 pairings, 189,200 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-13. **These supersede every number recorded in the deck files before this date**, and are not comparable with any earlier run: the engine changed materially in between.

What changed since the 2026-09-12 field: a pool-wide review of all 1964 card records, not just the ones these decks play. 48 more conditional damage bonuses are gated on a real condition (112 now, up from 64); 20 attacks reading "flip a coin, if tails this attack does nothing" stopped dealing full damage every time; 9 attacks that say their damage ignores Resistance now do; six rider shapes on 41 attacks compile at all (force-switch, defender debuff, Tool discard, own-Bench splash, heal-as-dealt, Energy to hand); `Neo Upper Energy` provides the two Energy it prints instead of one; once-per-turn Stadiums resolve from card text and are worth playing at all. And `hp_tools()` no longer caches an EMPTY registry when reached before the card index loads -- which silently switched off every HP Tool in the format for the life of the process.

> **Read the bottom of the table as a lower bound, not a verdict.** Both sides run the same greedy AI. A list whose edge is in sequencing — holding a Knock Out back, aiming spread damage at a Prize map, choosing when to take the turn off — is piloted by a policy that cannot do any of that, and six measured attempts to make the policy smarter all came out at no detectable difference. Where a deck's placement is known to be an artefact of that, its own file says so.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **72.7%** | 73.5% | 41/43 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | meta_raging_bolt (44%) |
| 2 | `panic_poison_paralysis` | **72.1%** | 71.0% | 41/43 | feraligatr_munkidori_damage_transfer (96%) | lurantis_heal_punish (46%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **70.8%** | 71.5% | 41/43 | meta_ns_zoroark (96%) | panic_poison_paralysis (41%) |
| 4 | `meta_raging_bolt` | **63.6%** | 64.0% | 38/43 | meta_ns_zoroark (93%) | arbok_muk_trolley_darkbell (38%) |
| 5 | `meta_mega_excadrill` | **61.6%** | 61.0% | 36/43 | meta_ns_zoroark (92%) | scovillain_salazzle_spicy_rage (38%) |
| 6 | `scovillain_salazzle_spicy_rage` | **61.2%** | 60.0% | 35/43 | meta_ns_zoroark (90%) | panic_poison_paralysis (37%) |
| 7 | `toxic_slumber_vileplume_ex` | **61.0%** | 61.5% | 35/43 | feraligatr_munkidori_damage_transfer (94%) | team_rockets_persian_ex_attack_theft (28%) |
| 8 | `arbok_muk_laser_darkbell` | **60.8%** | 59.5% | 34/43 | feraligatr_munkidori_damage_transfer (96%) | panic_poison_paralysis (28%) |
| 9 | `krookodile_ex_relicanth_hand_disruption` | **59.0%** | 59.0% | 34/43 | team_rockets_wobbuffet_orbeetle_damage_launder (92%) | lurantis_heal_punish (24%) |
| 10 | `arbok_muk_trolley_darkbell` | **59.0%** | 59.0% | 31/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (24%) |
| 11 | `tr_crobat_absol_bench_snipe` | **58.9%** | 57.5% | 31/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (20%) |
| 12 | `kyurem_vanilluxe_blizzard` | **56.9%** | 56.0% | 29/43 | meta_ns_zoroark (90%) | panic_poison_paralysis (28%) |
| 13 | `team_rockets_koffing_weezing_bench_swarm` | **56.3%** | 53.5% | 28/43 | feraligatr_munkidori_damage_transfer (91%) | lurantis_heal_punish (19%) |
| 14 | `dhelmise_veluza_hide_n_sneak` | **56.3%** | 55.0% | 28/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (32%) |
| 15 | `mega_chandelure_ex_retreat_tax` | **56.3%** | 59.0% | 30/43 | feraligatr_munkidori_damage_transfer (88%) | panic_poison_paralysis (28%) |
| 16 | `arbok_team_rockets_muk_condition_stack` | **55.7%** | 54.5% | 26/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (24%) |
| 17 | `mega_lopunny_dusknoir_snipe_finisher` | **53.7%** | 51.5% | 23/43 | feraligatr_munkidori_damage_transfer (85%) | meta_mega_excadrill (33%) |
| 18 | `heracross_sinistcha_tea` | **53.3%** | 50.5% | 23/43 | team_rockets_wobbuffet_orbeetle_damage_launder (90%) | scovillain_salazzle_spicy_rage (27%) |
| 19 | `meta_dragapult_pure` | **53.2%** | 51.5% | 24/43 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (33%) |
| 20 | `orthworm_ex_metal_retaliation` | **53.1%** | 50.0% | 21/43 | meta_festival_lead (90%) | scovillain_salazzle_spicy_rage (20%) |
| 21 | `stevens_carbink_damage_wall` | **52.5%** | 52.0% | 22/43 | meta_ns_zoroark (92%) | scovillain_salazzle_spicy_rage (30%) |
| 22 | `selective_bloom_cradily` | **52.4%** | 51.0% | 22/43 | feraligatr_munkidori_damage_transfer (86%) | meta_mega_excadrill (15%) |
| 23 | `kangaskhan_tyrantrum_flip_mill` | **51.7%** | 50.5% | 22/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (26%) |
| 24 | `meta_dragapult_blaziken` | **51.3%** | 49.5% | 21/43 | meta_ns_zoroark (86%) | scovillain_salazzle_spicy_rage (32%) |
| 25 | `water_aggro` | **51.0%** | 47.5% | 20/43 | feraligatr_munkidori_damage_transfer (92%) | panic_poison_paralysis (22%) |
| 26 | `ns_zoroark_night_joker_toolbox` | **50.1%** | 48.0% | 18/43 | static_venom_drapion (76%) | arbok_muk_trolley_darkbell (34%) |
| 27 | `mega_scrafty_ex_darkness_tank` | **49.7%** | 49.0% | 21/43 | meta_ns_zoroark (91%) | lurantis_heal_punish (14%) |
| 28 | `eerie_inferno_ninetales_burn` | **49.2%** | 47.0% | 18/43 | meta_ns_zoroark (89%) | panic_poison_paralysis (20%) |
| 29 | `meta_dragapult_dusknoir` | **49.0%** | 46.5% | 14/43 | meta_ns_zoroark (83%) | meta_raging_bolt (27%) |
| 30 | `decidueye_ex_judge_sniper_lock` | **48.2%** | 44.5% | 15/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (16%) |
| 31 | `meta_slowking` | **45.8%** | 47.5% | 19/43 | meta_ns_zoroark (82%) | tr_crobat_absol_bench_snipe (22%) |
| 32 | `hops_snorlax_stacked_buff` | **45.3%** | 43.5% | 14/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (13%) |
| 33 | `veluza_sinistcha_ex_tea_service` | **44.7%** | 44.0% | 13/43 | meta_ns_zoroark (88%) | team_rockets_koffing_weezing_bench_swarm (18%) |
| 34 | `team_rockets_spidops_swarm` | **44.2%** | 39.5% | 14/43 | meta_ns_zoroark (88%) | team_rockets_persian_ex_attack_theft (20%) |
| 35 | `tr_arbok_yveltal_snow_coating` | **42.7%** | 41.5% | 12/43 | meta_ns_zoroark (90%) | panic_poison_paralysis (12%) |
| 36 | `chandelure_centiskorch_deck_out` | **41.7%** | 39.5% | 12/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (14%) |
| 37 | `crabominable_veluza_food_prep` | **40.5%** | 39.0% | 8/43 | meta_ns_zoroark (87%) | meta_mega_excadrill (20%) |
| 38 | `darkness_mill_hand_lock` | **36.6%** | 31.5% | 7/43 | feraligatr_munkidori_damage_transfer (85%) | lurantis_heal_punish (4%) |
| 39 | `meta_festival_lead` | **36.4%** | 35.5% | 6/43 | meta_ns_zoroark (80%) | orthworm_ex_metal_retaliation (10%) |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | **33.9%** | 31.5% | 5/43 | meta_ns_zoroark (90%) | panic_poison_paralysis (10%) |
| 41 | `static_venom_drapion` | **30.4%** | 28.0% | 4/43 | team_rockets_wobbuffet_orbeetle_damage_launder (66%) | panic_poison_paralysis (9%) |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **24.0%** | 22.0% | 3/43 | feraligatr_munkidori_damage_transfer (80%) | lurantis_heal_punish (3%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **19.5%** | 17.5% | 1/43 | meta_ns_zoroark (80%) | arbok_muk_laser_darkbell (4%) |
| 44 | `meta_ns_zoroark` | **13.8%** | 11.0% | 0/43 | static_venom_drapion (42%) | team_rockets_persian_ex_attack_theft (4%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|meta_raging_bo|meta_mega_exca|scovillain_sal|toxic_slumber_|arbok_muk_lase|krookodile_ex_|arbok_muk_trol|tr_crobat_abso|kyurem_vanillu|team_rockets_k|dhelmise_veluz|mega_chandelur|arbok_team_roc|mega_lopunny_d|heracross_sini|meta_dragapult|orthworm_ex_me|stevens_carbin|selective_bloo|kangaskhan_tyr|meta_dragapult|water_aggro|ns_zoroark_nig|mega_scrafty_e|eerie_inferno_|meta_dragapult|decidueye_ex_j|meta_slowking|hops_snorlax_s|veluza_sinistc|team_rockets_s|tr_arbok_yvelt|chandelure_cen|crabominable_v|darkness_mill_|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|54|51|44|53|50|68|69|76|76|80|60|81|61|60|76|60|67|64|71|64|78|69|59|74|65|86|71|68|83|69|82|74|80|86|84|78|96|80|86|89|97|95|92|
| **panic_poison_p** |46|—|59|60|60|63|50|72|56|67|66|72|71|68|72|70|64|70|61|78|69|64|74|54|78|62|68|80|68|84|74|87|80|78|88|83|76|85|63|90|91|94|96|90|
| **team_rockets_p** |49|41|—|55|56|58|72|62|66|52|60|68|61|60|58|66|61|68|67|74|65|72|72|66|77|64|76|74|70|76|73|80|75|80|86|86|74|89|80|84|90|92|94|96|
| **meta_raging_bo** |56|40|45|—|60|46|64|41|65|38|52|56|53|62|60|52|64|66|64|60|50|80|60|66|64|61|68|64|73|57|69|64|71|74|74|72|72|76|76|70|84|76|76|93|
| **meta_mega_exca** |47|40|44|40|—|38|62|54|52|54|50|68|54|60|38|59|67|60|63|61|53|85|54|58|66|64|58|56|66|62|61|68|73|67|80|49|80|76|74|68|77|75|78|92|
| **scovillain_sal** |50|37|42|54|62|—|65|50|49|56|55|44|58|54|44|58|66|73|53|80|70|78|58|68|38|60|60|57|66|65|68|64|59|76|70|38|52|64|69|78|74|84|76|90|
| **toxic_slumber_** |32|50|28|36|38|35|—|68|65|66|51|54|76|61|38|72|52|60|56|66|63|52|55|62|60|62|75|42|58|56|54|72|63|60|76|70|66|80|63|80|75|89|94|90|
| **arbok_muk_lase** |31|28|38|59|46|50|32|—|42|49|46|56|57|55|70|50|58|53|60|65|65|44|64|60|59|64|55|59|63|62|77|71|67|74|59|75|69|78|60|78|80|95|96|92|
| **krookodile_ex_** |24|44|34|35|48|51|35|58|—|67|59|55|68|62|58|60|54|50|58|64|69|36|56|58|58|56|63|58|60|44|54|71|61|68|68|66|62|69|65|76|72|92|82|89|
| **arbok_muk_trol** |24|33|48|62|46|44|34|51|33|—|44|50|45|48|61|56|57|52|58|64|63|42|57|64|59|66|53|64|61|59|71|66|68|70|54|67|76|70|62|74|79|93|92|93|
| **tr_crobat_abso** |20|34|40|48|50|45|49|54|41|56|—|50|55|56|69|51|58|48|54|54|58|43|62|65|68|64|46|56|52|60|78|62|61|64|64|68|70|70|65|80|78|95|82|90|
| **kyurem_vanillu** |40|28|32|44|32|56|46|44|45|50|50|—|52|48|42|53|55|58|58|48|44|54|47|56|62|57|56|71|54|54|61|65|66|61|76|61|64|60|78|78|73|89|87|90|
| **team_rockets_k** |19|29|39|47|46|42|24|43|32|55|45|48|—|62|52|54|46|52|52|46|58|42|64|51|56|52|46|52|57|68|68|63|82|66|68|67|73|70|64|71|84|89|91|86|
| **dhelmise_veluz** |39|32|40|38|40|46|39|45|38|52|44|52|38|—|44|54|59|58|49|52|41|55|44|54|64|57|57|66|60|64|64|54|62|70|60|58|72|68|81|68|80|82|88|92|
| **mega_chandelur** |40|28|42|40|62|56|62|30|42|39|31|58|48|56|—|38|46|60|60|62|57|52|64|54|62|40|48|59|56|70|54|64|68|60|64|60|74|69|70|72|62|82|88|73|
| **arbok_team_roc** |24|30|34|48|41|42|28|50|40|44|49|47|46|46|62|—|56|45|48|54|54|42|51|62|60|62|52|55|57|58|67|71|64|68|54|66|54|70|60|70|80|95|94|92|
| **mega_lopunny_d** |40|36|39|36|33|34|48|42|46|43|42|45|54|41|54|44|—|50|39|62|54|56|50|44|50|38|52|60|52|60|46|58|54|70|76|76|54|71|75|72|76|82|85|74|
| **heracross_sini** |33|30|32|34|40|27|40|47|50|48|52|42|48|42|40|55|50|—|50|42|45|59|46|44|60|50|65|46|60|56|50|56|70|63|58|54|60|82|64|65|78|90|82|89|
| **meta_dragapult** |36|39|33|36|37|47|44|40|42|42|46|42|48|51|40|52|61|50|—|50|45|59|55|49|54|44|52|53|58|64|51|56|52|62|64|60|60|68|70|57|72|82|75|86|
| **orthworm_ex_me** |29|22|26|40|39|20|34|35|36|36|46|52|54|48|38|46|38|58|50|—|55|64|36|51|45|40|49|48|58|56|48|74|70|68|84|74|59|66|90|68|72|88|84|88|
| **stevens_carbin** |36|31|35|50|47|30|37|35|31|37|42|56|42|59|43|46|46|55|55|45|—|64|40|58|53|62|48|34|58|52|70|56|72|64|50|40|72|52|82|68|65|74|77|92|
| **selective_bloo** |22|36|28|20|15|22|48|56|64|58|57|46|58|45|48|58|44|41|41|36|36|—|44|36|51|34|65|56|46|52|46|72|48|64|75|78|61|82|74|70|77|86|86|72|
| **kangaskhan_tyr** |31|26|28|40|46|42|45|36|44|43|38|53|36|56|36|49|50|54|45|64|60|56|—|50|61|50|54|44|60|46|56|66|65|60|55|28|70|44|63|65|72|64|80|92|
| **meta_dragapult** |41|46|34|34|42|32|38|40|42|36|35|44|49|46|46|38|56|56|51|49|42|64|50|—|52|42|50|45|61|65|43|53|56|54|60|58|60|70|64|54|81|75|64|86|
| **water_aggro** |26|22|23|36|34|62|40|41|42|41|32|38|44|36|38|40|50|40|46|55|47|49|39|48|—|44|54|69|45|50|52|54|56|58|58|86|60|68|66|80|67|78|92|84|
| **ns_zoroark_nig** |35|38|36|39|36|40|38|36|44|34|36|43|48|43|60|38|62|50|56|60|38|66|50|58|56|—|58|53|60|48|65|46|47|46|45|48|64|62|51|48|76|66|62|76|
| **mega_scrafty_e** |14|32|24|32|42|40|25|45|37|47|54|44|54|43|52|48|48|35|48|51|52|35|46|50|46|42|—|54|52|34|49|60|52|52|54|54|64|58|66|74|70|88|80|91|
| **eerie_inferno_** |29|20|26|36|44|43|58|41|42|36|44|29|48|34|41|45|40|54|47|52|66|44|56|55|31|47|46|—|40|60|61|51|35|46|57|62|48|65|52|69|66|74|85|89|
| **meta_dragapult** |32|32|30|27|34|34|42|37|40|39|48|46|43|40|44|43|48|40|42|42|42|54|40|39|55|40|48|60|—|54|47|49|49|58|66|56|50|67|72|60|78|78|78|83|
| **decidueye_ex_j** |17|16|24|43|38|35|44|38|56|41|40|46|32|36|30|42|40|44|36|44|48|48|54|35|50|52|66|40|46|—|44|62|56|45|39|51|66|76|60|68|64|78|94|88|
| **meta_slowking** |31|26|27|31|39|32|46|23|46|29|22|39|32|36|46|33|54|50|49|52|30|54|44|57|48|35|51|39|53|56|—|52|54|52|54|38|56|54|64|50|70|60|70|82|
| **hops_snorlax_s** |18|13|20|36|32|36|28|29|29|34|38|35|37|46|36|29|42|44|44|26|44|28|34|47|46|54|40|49|51|38|48|—|60|52|64|60|68|55|69|68|68|70|94|92|
| **veluza_sinistc** |26|20|25|29|27|41|37|33|39|32|39|34|18|38|32|36|46|30|48|30|28|52|35|44|44|53|48|65|51|44|46|40|—|48|45|50|51|72|79|52|72|74|79|88|
| **team_rockets_s** |20|22|20|26|33|24|40|26|32|30|36|39|34|30|40|32|30|37|38|32|36|36|40|46|42|54|48|54|42|55|48|48|52|—|53|68|54|74|52|64|64|79|86|88|
| **tr_arbok_yvelt** |14|12|14|26|20|30|24|41|32|46|36|24|32|40|36|46|24|42|36|16|50|25|45|40|42|55|46|43|34|61|46|36|55|47|—|70|65|52|62|65|59|69|90|90|
| **chandelure_cen** |16|17|14|28|51|62|30|25|34|33|32|39|33|42|40|34|24|46|40|26|60|22|72|42|14|52|46|38|44|49|62|40|50|32|30|—|61|26|47|66|52|62|70|90|
| **crabominable_v** |22|24|26|28|20|48|34|31|38|24|30|36|27|28|26|46|46|40|40|41|28|39|30|40|40|36|36|52|50|34|44|32|49|46|35|39|—|56|67|58|61|58|69|87|
| **darkness_mill_** |4|15|11|24|24|36|20|22|31|30|30|40|30|32|31|30|29|18|32|34|48|18|56|30|32|38|42|35|33|24|46|45|28|26|48|74|44|—|38|65|53|67|85|75|
| **meta_festival_** |20|37|20|24|26|31|37|40|35|38|35|22|36|19|30|40|25|36|30|10|18|26|37|36|34|49|34|48|28|40|36|31|21|48|38|53|33|62|—|46|61|54|63|80|
| **salazzle_ex_te** |14|10|16|30|32|22|20|22|24|26|20|22|29|32|28|30|28|35|43|32|32|30|35|46|20|52|26|31|40|32|50|32|48|36|35|34|42|35|54|—|41|48|59|90|
| **static_venom_d** |11|9|10|16|23|26|25|20|28|21|22|27|16|20|38|20|24|22|28|28|35|23|28|19|33|24|30|34|22|36|30|32|28|36|41|48|39|47|39|59|—|66|64|58|
| **team_rockets_w** |3|6|8|24|25|16|11|5|8|7|5|11|11|18|18|5|18|10|18|12|26|14|36|25|22|34|12|26|22|22|40|30|26|21|31|38|42|33|46|52|34|—|80|79|
| **feraligatr_mun** |5|4|6|24|22|24|6|4|18|8|18|13|9|12|12|6|15|18|25|16|23|14|20|36|8|38|20|15|22|6|30|6|21|14|10|30|31|15|37|41|36|20|—|80|
| **meta_ns_zoroar** |8|10|4|7|8|10|10|8|11|7|10|10|14|8|27|8|26|11|14|12|8|28|8|14|16|24|9|11|17|12|18|8|12|12|10|10|13|25|20|10|42|21|20|—|
