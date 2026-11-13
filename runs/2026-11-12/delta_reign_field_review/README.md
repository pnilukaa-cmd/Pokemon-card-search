# Delta Reign: are the new cards worth adding to the field decks?

Run 2026-11-12, after de65e4e and a845ec3 (the Delta Reign card fixes).
The write-up is in `decks/delta_reign_card_review.md`; this folder holds
the lists, scripts and raw results.

## Method

1. **Fit matrix** (`scripts/profile.py`, `scripts/fit.py`). Every one of
   the 108 field decks gets:
   - **Aarune** ×1 and **Custom Vest** ×2.
   - **Legendary Pyroduct** ×2, if none of its own Evolution Pokémon has
     an Ability (31 decks).
   - The Delta Reign attacker of each Basic Energy type it runs 8+ of:
     Darkrai (Darkness, 26 decks), Giratina (Psychic, 15), Wishiwashi ex
     (Water, 6), Heat Rotom ex (Fire, 6), Raikou ex (Lightning, 1), two
     copies each.

   That makes 300 variants (`lists/variants`).
2. **Standard cuts**, fixed before any game was played:
   - A Supporter replaces the deck's most-played Supporter other than
     Boss's Orders.
   - A Stadium replaces the deck's Stadiums; a Tool replaces its non-ACE
     Tools.
   - Otherwise the cut is its most-played flex Item, in this order: Night
     Stretcher, Switch, Pokégear 3.0, Energy Search, Energy Switch, Energy
     Retrieval, Energy Recycler, Max Rod, Super Rod, Pal Pad. Then a
     Supporter.
3. **Panel screen** (`scripts/batch.py`, `results/screen.jsonl`). Every
   base list and variant played 100 games against each of 16 opponents in
   `results/panel.txt`: the six meta decks, Krookodile ex, Mega Absol ex,
   and eight more, 5 of the 16 Mega ex decks (the field has 32 of 108).
   Seeds are the same as `vs_field.py`'s, so each variant's difference from
   its base is paired.
4. **Full field.** The 40 panel hits of +2.0 or more played 100 games
   against all 107 other field decks, as did their base lists
   (`results/confirm.jsonl`).
5. **Two controls** for the 17 hits of +1.25 or more that were also at
   least 2 SE:
   - The same cut refilled with Basic Energy of the deck's main type
     (`lists/energy_control`). This shows whether the new card beats an
     Energy in that slot, or whether the gain was only the cut.
   - The same new card with a second cut (`lists/second_cut`).

Every ± is the standard error of the mean per-opponent difference.

## Per-card summary (panel, mean change over the decks each card fits)

| Card | Decks | Mean | Median | Above +1.5 | Below −1.5 |
|---|---|---|---|---|---|
| Legendary Pyroduct | 31 | +1.43 | +1.94 | 17 | 2 |
| Wishiwashi ex | 6 | +0.11 | +0.73 | 2 | 1 |
| Darkrai | 26 | −0.29 | −0.31 | 7 | 8 |
| Custom Vest | 108 | −0.38 | −0.56 | 16 | 26 |
| Raikou ex | 1 | −0.69 | | 0 | 0 |
| Aarune | 107 | −1.12 | −1.12 | 9 | 42 |
| Giratina | 15 | −3.79 | −3.81 | 0 | 13 |
| Heat Rotom ex | 6 | −5.83 | −5.25 | 0 | 6 |

## The controls

| Deck | Card | Standard cut | vs base | Energy control vs base | Card − control | Second cut vs base |
|---|---|---|---|---|---|---|
| feraligatr_munkidori_damage_transfer | Wishiwashi ex | 2 Switch | +4.84 ± 0.93 | +0.22 | **+4.62 ± 0.99** | +5.38 ± 0.86 (2 Night Stretcher) |
| kyurem_vanilluxe_blizzard | Wishiwashi ex | 2 Switch | +4.26 ± 0.89 | +1.66 | **+2.60 ± 0.75** | +3.51 ± 0.84 (Night Stretcher, Lillie's) |
| munkidori_ex_pecharunt_chains | Pyroduct | 2 Pokégear 3.0 | +1.82 ± 0.79 | −0.68 | **+2.50 ± 0.72** | +2.76 ± 0.70 (2 Night Stretcher) |
| team_rocket_hypno_exeggutor | Pyroduct | Factory, Night Stretcher | +2.64 ± 0.72 | +1.06 | **+1.59 ± 0.75** | +2.68 ± 0.75 (2 Night Stretcher) |
| mega_absol_ex_hand_lock | Pyroduct | 2 Night Stretcher | +2.40 ± 0.71 | +0.93 | +1.47 ± 0.82 | +0.89 ± 0.72 (2 Switch) |
| mega_malamar_ex_psychic_marionette | Pyroduct | 2 Night Stretcher | +1.76 ± 0.58 | +0.47 | +1.29 ± 0.67 | +0.91 ± 0.68 |
| team_rocket_moltres_houndoom | Pyroduct | Factory, Night Stretcher | +1.99 ± 0.80 | +0.98 | +1.01 ± 0.89 | +1.36 ± 0.71 |
| team_rocket_nidoking_nidoqueen | Pyroduct | 2 Night Stretcher | +2.46 ± 0.65 | +1.43 | +1.03 ± 0.66 | −2.91 ± 0.78 (2 Ariana) |
| aggron_diggersby_angry_slam | Pyroduct | 2 Switch | +3.53 ± 0.70 | +2.84 | +0.69 ± 0.69 | +2.04 ± 0.70 |
| arboliva_ogerpon_oil_salvo | Pyroduct | 2 Forest of Vitality | +1.82 ± 0.64 | +1.27 | +0.55 ± 0.81 | +0.86 ± 0.72 |
| static_venom_drapion | Darkrai | 2 Switch | +3.74 ± 0.66 | +3.62 | +0.12 ± 0.66 | +3.91 ± 0.71 |
| darkness_mill_hand_lock | Darkrai | 2 Night Stretcher | +3.15 ± 0.67 | +2.42 | +0.73 ± 0.62 | +1.29 ± 0.59 |
| decidueye_ex_judge_sniper_lock | Aarune | 1 Judge | +1.45 ± 0.67 | +0.73 | +0.72 ± 0.59 | −1.15 ± 0.66 (Lillie's) |
| arbok_muk_trolley_darkbell | Pyroduct | 2 Night Stretcher | +1.60 ± 0.70 | +1.93 | −0.34 ± 0.78 | −2.60 ± 0.82 (2 Lillie's) |
| arbok_team_rockets_muk_condition_stack | Pyroduct | 2 Night Stretcher | +1.54 ± 0.71 | +2.42 | −0.88 ± 0.77 | −2.11 ± 0.81 (2 Lillie's) |
| mew_dbc_hypno | Pyroduct | 2 Night Stretcher | +1.76 ± 0.62 | +4.23 | −2.48 ± 0.60 | +1.80 ± 0.57 |
| mega_zygarde_cinderace_turbo_flare | Custom Vest | Core Memory, Pokégear | +9.03 ± 0.70 | **+12.01** | −2.98 ± 0.52 | −0.21 ± 0.73 (2 Pokégear) |

Bold in the "Card − control" column marks a new card that beats a Basic
Energy in its slot by 2 SE or more and holds with the second cut.

How the four confirmed additions get used (`scripts/usage.py`: 10 logged
games against each of the eight opponents in `opps8`):

- **Feraligatr list:** Wishiwashi ex attacks 1.04 times a game with Hydro
  Splash and uses Oceanic Gain 2.11 times.
- **Kyurem list:** 1.24 Hydro Splashes and 1.20 Oceanic Gains a game.
- **Legendary Pyroduct:** played 0.62 times a game in the Munkidori ex
  list and 0.89 in Team Rocket Hypno.

Setup baselines (`simulate_baseline.py`, 1000 trials) for the four:

- **Feraligatr list:** Wishiwashi ex is in play by turn 6 in 73.4% of
  games (avg turn 2.22). It slows the Feraligatr line: Croconaw by turn 6
  drops from 63.2% to 50.7%, and the first attack by turn 6 from 88.7% to
  79.1%.
- **Kyurem list:** Wishiwashi ex in play by turn 6 in 54.0%. N's Vanilluxe
  41.6% → 38.9%.
- **The two Pyroduct lists:** setup is unchanged within 2 points.

## Every deck

Panel change for each candidate tested; "field" is the full-field
measurement where one was made. The panel's SE is about 1.3–2.0, so a
panel number alone under about +3 is noise.

| Deck | Panel win % | Candidate: panel change (full field) |
|---|---|---|
| `aggron_diggersby_angry_slam` | 46% | Aarune -4.4; Custom Vest +2.6 (field +0.7); Pyroduct +3.8 (field +3.5) |
| `alakazam_dudunsparce_powerful_hand` | 44% | Aarune -1.6; Custom Vest +0.9 |
| `alakazam_munkidori_strange_hacking` | 59% | Aarune -2.1; Custom Vest -0.4; Giratina -5.9 |
| `arbok_muk_laser_darkbell` | 33% | Aarune -2.3; Custom Vest +0.9; Pyroduct +2.0 (field +0.9); Darkrai +1.5 |
| `arbok_muk_trolley_darkbell` | 29% | Aarune +0.1; Custom Vest +4.4 (field -0.3); Pyroduct +4.6 (field +1.6); Darkrai +1.8 |
| `arbok_team_rockets_muk_condition_stack` | 26% | Aarune -1.1; Custom Vest -0.6; Pyroduct +4.4 (field +1.5); Darkrai +0.8 |
| `arboliva_ogerpon_oil_salvo` | 75% | Aarune +0.5; Custom Vest -0.6; Pyroduct +2.4 (field +1.8) |
| `aurorus_kangaskhan_tundra_wall` | 67% | Aarune +2.5 (field -0.8); Custom Vest +1.1; Wishiwashi ex -1.4 |
| `bug_out_masquerain_jellicent` | 44% | Aarune -2.5; Custom Vest -3.1 |
| `chandelure_centiskorch_deck_out` | 32% | Aarune +1.0; Custom Vest -5.2 |
| `chandelure_maushold_dudunsparce_wall` | 28% | Aarune -1.1; Custom Vest +0.6 |
| `chesnaught_meganium_wild_growth` | 62% | Aarune -0.1; Custom Vest +2.6 (field -1.3) |
| `crabominable_veluza_food_prep` | 26% | Aarune -11.4; Custom Vest -1.3 |
| `cradily_accelgor_conditions` | 42% | Aarune +0.0; Custom Vest -3.8 |
| `cradily_amoonguss_conditions` | 38% | Aarune -2.4; Custom Vest -0.4 |
| `darkness_mill_hand_lock` | 27% | Aarune -0.1; Custom Vest -0.6; Darkrai +3.1 (field +3.1) |
| `decidueye_ex_judge_sniper_lock` | 39% | Aarune +2.4 (field +1.4); Custom Vest +0.2 |
| `dhelmise_veluza_hide_n_sneak` | 38% | Aarune -6.1; Custom Vest -1.0; Giratina -9.9 |
| `diggersby_munkidori_earthquake` | 48% | Aarune -3.5; Custom Vest -4.1; Pyroduct +1.1; Darkrai -2.8 |
| `ditto_transform_hydreigon` | 47% | Aarune -3.3; Custom Vest -2.4; Darkrai -3.6 |
| `ditto_tyranitar_gengar_hydreigon` | 48% | Aarune -4.1; Custom Vest -1.6 |
| `eerie_inferno_ninetales_burn` | 27% | Aarune -0.1; Custom Vest -0.9; Heat Rotom ex -2.8 |
| `feraligatr_munkidori_damage_transfer` | 23% | Aarune -1.2; Custom Vest -1.2; Wishiwashi ex +4.2 (field +4.8) |
| `golbat_brute_bonnet_punch` | 34% | Aarune -3.5; Custom Vest -1.4; Darkrai +1.9 |
| `gothitelle_noivern_distorted_future` | 29% | Aarune -2.2; Custom Vest -1.5; Giratina -3.8 |
| `gourgeist_diggersby_horrifying_rondo` | 63% | Aarune -1.9; Custom Vest -0.4; Pyroduct +1.8; Giratina -4.6 |
| `heracross_sinistcha_tea` | 41% | Aarune -1.1; Custom Vest +1.0 |
| `hops_snorlax_stacked_buff` | 30% | Aarune -0.7; Custom Vest -4.4; Giratina -1.9 |
| `hydrapple_hydra_breath_festival` | 33% | Aarune +0.6; Custom Vest +0.1 |
| `hydrapple_seaking_festival_lead` | 60% | Aarune -1.9; Custom Vest -1.0 |
| `hydreigon_grafaiai_energy_denial` | 34% | Aarune -1.2; Custom Vest -2.0 |
| `hydreigon_relicanth_hammer_denial` | 41% | Aarune -1.2; Custom Vest -2.9; Darkrai +1.0 |
| `jellicent_ex_oceanic_curse` | 58% | Aarune -1.0; Custom Vest +0.1; Giratina -4.4 |
| `kangaskhan_legendary_trench_wall` | 77% | Aarune -3.5; Custom Vest -2.9; Pyroduct +0.5; Giratina -5.5 |
| `kangaskhan_tyrantrum_flip_mill` | 37% | Aarune +0.1; Custom Vest -1.4 |
| `kingdra_ex_kings_order` | 55% | Aarune -3.6; Custom Vest -2.5; Wishiwashi ex -0.4 |
| `krookodile_ex_relicanth_hand_disruption` | 43% | Aarune -2.9; Custom Vest +1.1; Darkrai -0.9 |
| `kyurem_vanilluxe_blizzard` | 34% | Aarune -0.8; Custom Vest -0.8; Wishiwashi ex +2.4 (field +4.3) |
| `lurantis_heal_punish` | 60% | Aarune +0.7; Custom Vest +0.0 |
| `maushold_gnaw_together_mill` | 52% | Aarune +0.6; Custom Vest +0.7; Giratina -3.4 |
| `maushold_mill_legendary_summit` | 64% | Custom Vest -0.1; Pyroduct -10.3; Giratina -2.9 |
| `mega_absol_ex_hand_lock` | 63% | Aarune -3.1; Custom Vest -1.3; Pyroduct +2.5 (field +2.4); Darkrai -0.5 |
| `mega_chandelure_ex_retreat_tax` | 45% | Aarune -1.6; Custom Vest -2.1 |
| `mega_chandelure_ex_telepathic_hilda` | 62% | Aarune -0.5; Custom Vest -1.3; Giratina -2.2 |
| `mega_dragonite_kangaskhan_salazzle_wall` | 60% | Aarune -4.5; Custom Vest -4.6; Heat Rotom ex -6.6 |
| `mega_emboar_oricorio_fire_turbo` | 50% | Aarune -1.2; Custom Vest -6.7; Heat Rotom ex -5.2 |
| `mega_emboar_oricorio_munkidori` | 40% | Aarune -0.9; Custom Vest -0.4; Heat Rotom ex -6.8 |
| `mega_froslass_ex_resentful_refrain` | 74% | Aarune +0.4; Custom Vest -2.9 |
| `mega_gengar_ex_toxtricity_chains` | 62% | Aarune -3.4; Custom Vest -4.9; Darkrai -1.8 |
| `mega_lopunny_dusknoir_snipe_finisher` | 48% | Aarune -3.5; Custom Vest +1.1 |
| `mega_malamar_ex_psychic_marionette` | 72% | Aarune +0.4; Custom Vest -0.7; Pyroduct +2.7 (field +1.8); Darkrai +1.5 |
| `mega_scrafty_ex_darkness_tank` | 33% | Aarune -0.8; Custom Vest -1.0; Darkrai +1.9 |
| `mega_zeraora_cinderace_thunderous_fist` | 80% | Aarune -0.5; Custom Vest +0.1; Raikou ex -0.7 |
| `mega_zygarde_cinderace_gaia_wave` | 80% | Aarune -1.3; Custom Vest +0.0 |
| `mega_zygarde_cinderace_turbo_flare` | 62% | Aarune -1.9; Custom Vest +7.3 (field +9.0) |
| `meta_dragapult_blaziken` | 47% | Aarune +1.4; Custom Vest +4.1 (field +0.8) |
| `meta_dragapult_dusknoir` | 41% | Aarune -1.1; Custom Vest +0.3 |
| `meta_dragapult_pure` | 50% | Aarune -1.9; Custom Vest +4.5 (field -0.1) |
| `meta_festival_lead` | 20% | Aarune -3.4; Custom Vest -3.1 |
| `meta_mega_excadrill` | 67% | Aarune +0.5; Custom Vest -2.1 |
| `meta_ns_zoroark` | 30% | Aarune -2.1; Custom Vest -0.6; Darkrai -1.3 |
| `meta_raging_bolt` | 44% | Aarune +1.0; Custom Vest +1.9; Pyroduct +1.3 |
| `meta_slowking` | 35% | Aarune -1.9; Custom Vest +2.1 (field -2.2); Pyroduct +2.6 (field +1.4) |
| `metal_metang_excadrill` | 60% | Aarune +1.2; Custom Vest -0.3 |
| `mew_alex_centiskorch_mill` | 38% | Aarune +0.6; Custom Vest -1.1; Pyroduct -0.4 |
| `mew_baby_box` | 11% | Aarune -1.2; Custom Vest -1.4 |
| `mew_dbc_bastiodon` | 30% | Aarune -0.2; Custom Vest -0.8; Giratina -1.2 |
| `mew_dbc_hypno` | 12% | Aarune +0.1; Custom Vest -0.6; Pyroduct +2.6 (field +1.8) |
| `mew_lonestar_gourgeist_dragapult` | 46% | Aarune -1.0; Custom Vest -2.8 |
| `mew_pikachu_box` | 18% | Aarune +1.9; Custom Vest +2.3 (field +0.4); Pyroduct +0.8 |
| `munkidori_ex_pecharunt_chains` | 64% | Aarune +3.0 (field -0.8); Custom Vest +3.2 (field -0.9); Pyroduct +3.4 (field +1.8); Darkrai +2.0 (field -2.1) |
| `ns_zoroark_night_joker_toolbox` | 61% | Aarune -1.2; Custom Vest -0.6; Darkrai -3.1 |
| `orthworm_ex_metal_retaliation` | 24% | Aarune -0.9; Custom Vest -1.1 |
| `orthworm_ex_metang_archaludon` | 69% | Aarune -2.2; Custom Vest -0.2 |
| `panic_poison_paralysis` | 42% | Aarune -1.5; Custom Vest +0.1; Pyroduct +2.9 (field +0.4); Darkrai -0.3 |
| `salazzle_ex_team_rockets_muk_condition_stack` | 32% | Aarune -1.5; Custom Vest +0.9; Pyroduct +3.2 (field +1.3) |
| `scovillain_salazzle_spicy_rage` | 51% | Aarune -3.9; Custom Vest -1.1; Heat Rotom ex -8.3 |
| `snorlax_bouffalant_kangaskhan_curly_wall` | 73% | Aarune -0.1; Custom Vest +1.3; Pyroduct +1.5; Giratina -4.9 |
| `static_venom_drapion` | 13% | Aarune -0.5; Custom Vest -1.3; Pyroduct -0.4; Darkrai +2.6 (field +3.7) |
| `stevens_carbink_damage_wall` | 36% | Aarune +3.1 (field -0.1); Custom Vest +2.4 (field -1.7) |
| `study_centiskorch_bastiodon_mill` | 39% | Aarune -1.1; Custom Vest -2.1 |
| `study_flygon_sandy_flapping_mill` | 24% | Aarune +2.2 (field +0.5); Custom Vest -0.6 |
| `study_hydreigon_zweilous_mill` | 30% | Aarune -2.1; Custom Vest -1.9 |
| `study_maushold_gnaw_latias` | 29% | Aarune +1.2; Custom Vest +0.4; Pyroduct -0.3 |
| `study_mega_excadrill_drill_mill` | 46% | Aarune -3.1; Custom Vest -2.2 |
| `tauros_risky_ruins` | 56% | Aarune -2.8; Custom Vest +1.3; Pyroduct -1.0 |
| `team_rocket_honchkrow_kangaskhan` | 46% | Aarune +1.8; Custom Vest +2.9 (field -0.1); Pyroduct +1.1; Darkrai +2.8 (field -0.1) |
| `team_rocket_hypno_exeggutor` | 37% | Aarune +0.2; Custom Vest +3.4 (field +0.6); Pyroduct +2.5 (field +2.6); Giratina -3.4 |
| `team_rocket_hypno_wobbuffet` | 37% | Aarune -0.1; Custom Vest +0.4; Pyroduct +0.9; Giratina -3.9 |
| `team_rocket_moltres_houndoom` | 40% | Aarune +0.6; Custom Vest +0.7; Pyroduct +2.8 (field +2.0); Heat Rotom ex -5.2 |
| `team_rocket_nidoking_nidoqueen` | 50% | Aarune -1.4; Custom Vest +0.9; Pyroduct +4.6 (field +2.5); Darkrai -2.8 |
| `team_rocket_orbeetle_morpeko` | 43% | Aarune -1.8; Custom Vest +0.6; Darkrai -3.7 |
| `team_rocket_porygon_z_kangaskhan` | 44% | Aarune -2.3; Custom Vest +0.3; Darkrai -3.3 |
| `team_rocket_raticate_ampharos` | 48% | Aarune -3.9; Custom Vest -1.7; Darkrai -2.9 |
| `team_rocket_raticate_rush` | 57% | Aarune -1.9; Custom Vest -0.9; Pyroduct -1.9 |
| `team_rocket_tyranitar_sandstorm` | 43% | Aarune -2.9; Custom Vest -1.2 |
| `team_rockets_koffing_weezing_bench_swarm` | 41% | Aarune -0.2; Custom Vest +0.4; Pyroduct +0.9; Darkrai -1.4 |
| `team_rockets_persian_ex_attack_theft` | 51% | Aarune +3.9 (field +1.3); Custom Vest +1.9 |
| `team_rockets_spidops_swarm` | 30% | Aarune -0.1; Custom Vest -1.9 |
| `team_rockets_wobbuffet_orbeetle_damage_launder` | 14% | Aarune +1.3; Custom Vest +0.2; Giratina +1.1 |
| `toxic_slumber_vileplume_ex` | 28% | Aarune +1.9; Custom Vest +1.8 |
| `tr_arbok_yveltal_snow_coating` | 19% | Aarune +0.4; Custom Vest -0.4; Darkrai +1.4 |
| `tr_crobat_absol_bench_snipe` | 35% | Aarune -3.4; Custom Vest -1.8; Darkrai -1.4 |
| `tr_spidops_mewtwo_hammer` | 56% | Aarune -1.9; Custom Vest -2.6 |
| `trevenant_rapidash_uxie` | 31% | Aarune +1.2; Custom Vest -0.9 |
| `veluza_sinistcha_ex_tea_service` | 39% | Aarune -4.8; Custom Vest +1.2 |
| `water_aggro` | 33% | Aarune +0.5; Custom Vest +1.1; Wishiwashi ex +0.7 |
| `wugtrio_paralysis_pin` | 50% | Aarune -2.1; Custom Vest +3.0 (field +1.1); Pyroduct +1.9; Wishiwashi ex -4.9 |
