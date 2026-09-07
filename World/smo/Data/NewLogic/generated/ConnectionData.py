from rule_builder.rules import *
from .TokenNames import SMOTokenNames as tokens
from .RegionData import SMORegionData as regions
from ....Rules import CanCapture, HasStoryProgress

region_connection_data: dict[str, dict[str, Rule]] = {
    regions.region_names["jizos_great_adventure_substage_near_side_jizo01"]: {
        regions.region_names["jizos_great_adventure_substage_far_side_jizo02"]: Or(
            And(CanCapture(tokens.jizo), HasAll(tokens.wall_jump, tokens.p_switches)),
            And(
                CanCapture(tokens.jizo),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.p_switches, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.jizo),
                HasAll(
                    tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.p_switches, tokens.intermediate_tricks
                ),
            ),
        ),
    },
    regions.region_names["jizos_great_adventure_substage_far_side_jizo02"]: {
        regions.region_names["jizos_great_adventure_substage_near_side_jizo01"]: True_(),
    },
    regions.region_names["spinning_tower_substage_near_side_tukkun000_enter"]: {
        regions.region_names["spinning_tower_substage_far_side_tukkun000_exit"]: Or(
            CanCapture(tokens.pokio),
            HasAll(
                tokens.ground_pound,
                tokens.roll,
                tokens.roll_boost,
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
        ),
    },
    regions.region_names["spinning_tower_substage_far_side_tukkun000_exit"]: {
        regions.region_names["spinning_tower_substage_near_side_tukkun000_enter"]: True_(),
    },
    regions.region_names["wooden_tower_substage_near_side_tukkun001_enter"]: {
        regions.region_names["wooden_tower_substage_far_side_tukkun001_exit"]: Or(
            CanCapture(tokens.pokio),
            HasAll(
                tokens.backflip, tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks
            ),
        ),
    },
    regions.region_names["wooden_tower_substage_far_side_tukkun001_exit"]: {
        regions.region_names["wooden_tower_substage_near_side_tukkun001_enter"]: True_(),
    },
    regions.region_names["bowsers_kingdom_stage_change_come"]: {
        regions.region_names["bowsers_kingdom_island_in_the_sky_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["bowsers_kingdom_third_courtyard_rear_checkpoint"]: {
        regions.region_names["bowsers_kingdom_third_coutyward_end"]: Or(
            And(
                CanCapture(tokens.pokio),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            Has(tokens.ground_pound),
            And(
                CanCapture(tokens.pokio),
                HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.pokio),
                HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["bowsers_kingdom_island_in_the_sky_checkpoint"]: False_(),
        regions.region_names["bowsers_kingdom_third_courtyard_link"]: True_(),
    },
    regions.region_names["bowsers_kingdom_third_coutyward_end"]: {
        regions.region_names["bowsers_kingdom_third_courtyard_rear_checkpoint"]: Or(
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.bowsers_kingdom_access)),
            And(HasStoryProgress("bowsers", [0]), HasAll(tokens.cap_return_jump, tokens.intermediate_tricks)),
        ),
        regions.region_names["bowsers_kingdom_second_courtyard_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_island_in_the_sky_checkpoint"]: False_(),
    },
    regions.region_names["bowsers_kingdom_sky_world_wall_zone"]: {
        regions.region_names["bowsers_kingdom_second_courtyard_checkpoint"]: True_(),
    },
    regions.region_names["bowsers_kingdom_second_courtyard_checkpoint"]: {
        regions.region_names["bowsers_kingdom_souvenir_shop_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_second_courtyard_link"]: True_(),
    },
    regions.region_names["bowsers_kingdom_souvenir_shop_checkpoint"]: {
        regions.region_names["bowsers_kingdom_home_entrance_byoubu"]: True_(),
        regions.region_names["bowsers_kingdom_home_entrance_shop"]: True_(),
        regions.region_names["bowsers_kingdom_main_courtyard_entrance_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_shop_link"]: True_(),
        regions.region_names["bowsers_kingdom_bowser_peach"]: True_(),
    },
    regions.region_names["bowsers_kingdom_main_courtyard_checkpoint"]: {
        regions.region_names["bowsers_kingdom_moon_rock"]: True_(),
        regions.region_names["bowsers_kingdom_home_entrance_tukkun001_enter"]: True_(),
        regions.region_names["bowsers_kingdom_main_courtyard_entrance_checkpoint"]: Or(
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.jump)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.cap_return_jump)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.dive, tokens.intermediate_tricks)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.vault, tokens.intermediate_tricks)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.long_jump)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.backflip)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.side_flip)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), Has(tokens.spin)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.wall_jump, tokens.intermediate_tricks)),
            And(CanCapture(tokens.pokio), HasStoryProgress("bowsers", [1, 2, 3])),
        ),
        regions.region_names["bowsers_kingdom_home_entrance_patakaron02"]: True_(),
        regions.region_names["bowsers_kingdom_outer_wall_area"]: Or(
            CanCapture(tokens.pokio),
            HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.spin_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["bowsers_kingdom_sky_world_castle_zone"]: True_(),
    },
    regions.region_names["bowsers_kingdom_outer_wall_checkpoint"]: {
        regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: CanCapture(tokens.pokio),
        regions.region_names["bowsers_kingdom_home_entrance_sora001"]: False_(),
    },
    regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: {
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: CanCapture(tokens.pokio),
        regions.region_names["bowsers_kingdom_ogre_area"]: Or(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.hard_tricks),
        ),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_floor"]: True_(),
        regions.region_names["bowsers_kingdom_outer_wall_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_top"]: False_(),
    },
    regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: {
        regions.region_names["bowsers_kingdom_showdown_arena_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_ogre_area"]: True_(),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_floor"]: True_(),
        regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_slingshot_area"]: And(
            Or(
                CanCapture(tokens.lakitu),
                HasAll(tokens.bowsers_kingdom_access, tokens.hard_tricks),
                And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
            ),
            HasStoryProgress("bowsers", [1, 2, 3]),
        ),
        regions.region_names["bowsers_kingdom_mech_fight"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_top"]: True_(),
        regions.region_names["bowsers_kingdom_knocking_down_the_nice_frame"]: Or(
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks
            ),
            HasAll(tokens.side_flip, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["bowsers_kingdom_past_the_moving_wall_area"]: Or(
            CanCapture(tokens.pokio),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["bowsers_kingdom_bowsers_kfr"]: And(
            Has(tokens.talk_to_npcs), HasStoryProgress("bowsers", [1, 2, 3])
        ),
    },
    regions.region_names["bowsers_kingdom_showdown_arena_checkpoint"]: {
        regions.region_names["bowsers_kingdom_home_entrance_jizo01"]: True_(),
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_slingshot_area"]: True_(),
    },
    regions.region_names["bowsers_kingdom_treasure_vault_substage_near_side_shop_dress"]: {
        regions.region_names["bowsers_kingdom_treasure_vault_substage_far_side_shop_dress"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_shop"]: {
        regions.region_names["crazy_cap_store_substage_far_side_shop"]: True_(),
    },
    regions.region_names["dashing_above_the_clouds_substage_near_side_sora001"]: {
        regions.region_names["dashing_above_the_clouds_substage_far_side_sora001"]: True_(),
    },
    regions.region_names["dashing_above_the_clouds_substage_far_side_sora001"]: {
        regions.region_names["dashing_above_the_clouds_substage_near_side_sora001"]: False_(),
    },
    regions.region_names["hexagon_tower_substage_near_side_patakaron02"]: {
        regions.region_names["hexagon_tower_substage_far_side_patakaron02"]: True_(),
    },
    regions.region_names["scene_in_the_folding_screen_substage_near_side_byoubu"]: {
        regions.region_names["scene_in_the_folding_screen_substage_far_side_byoubu"]: True_(),
    },
    regions.region_names["bowsers_kingdom_island_in_the_sky_checkpoint"]: {
        regions.region_names["bowsers_kingdom_third_courtyard_rear_checkpoint"]: HasAll(
            tokens.side_flip, tokens.easy_glitches
        ),
        regions.region_names["bowsers_kingdom_exterminate_the_ogres_island"]: True_(),
        regions.region_names["bowsers_kingdom_third_coutyward_end"]: HasAll(tokens.side_flip, tokens.easy_glitches),
    },
    regions.region_names["bowsers_kingdom_main_courtyard_entrance_checkpoint"]: {
        regions.region_names["bowsers_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["bowsers_kingdom_main_courtyard_checkpoint"]: Or(
            And(CanCapture(tokens.pokio), CanCapture(tokens.spark_pylon)),
            And(CanCapture(tokens.spark_pylon), Has(tokens.ground_pound)),
        ),
        regions.region_names["bowsers_kingdom_exterminate_the_ogres_island"]: CanCapture(tokens.spark_pylon),
    },
    regions.region_names["bowsers_kingdom_ogre_area"]: {
        regions.region_names["bowsers_kingdom_home_entrance_tukkun000_enter"]: Has(tokens.ground_pound),
        regions.region_names["bowsers_kingdom_home_entrance_sora001"]: Or(
            HasAll(tokens.climb, tokens.grab),
            And(CanCapture(tokens.pokio), HasAll(tokens.grab, tokens.intermediate_tricks)),
        ),
        regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: HasAll(
            tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks
        ),
        regions.region_names["bowsers_kingdom_past_the_moving_wall_area"]: Or(
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks), HasAll(tokens.dive, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["bowsers_kingdom_home_entrance_tukkun000_enter"]: {
        regions.region_names["bowsers_kingdom_ogre_area"]: True_(),
    },
    regions.region_names["bowsers_kingdom_home_entrance_sora001"]: {
        regions.region_names["bowsers_kingdom_ogre_area"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
        ),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_floor"]: True_(),
        regions.region_names["bowsers_kingdom_outer_wall_checkpoint"]: True_(),
    },
    regions.region_names["bowsers_kingdom_bowsers_treasure_vault_floor"]: {
        regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
        ),
        regions.region_names["bowsers_kingdom_home_entrance_sora001"]: Or(
            HasAll(tokens.climb, tokens.grab),
            And(CanCapture(tokens.pokio), HasAll(tokens.grab, tokens.intermediate_tricks)),
        ),
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: False_(),
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_top"]: And(
            CanCapture(tokens.pokio), HasStoryProgress("bowsers", [1, 2, 3])
        ),
    },
    regions.region_names["bowsers_kingdom_third_courtyard_front_checkpoint"]: {
        regions.region_names["bowsers_kingdom_top_of_third_courtyard"]: Or(
            CanCapture(tokens.pokio),
            HasAll(tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["bowsers_kingdom_top_of_third_courtyard"]: {
        regions.region_names["bowsers_kingdom_third_courtyard_rear_checkpoint"]: CanCapture(tokens.spark_pylon),
    },
    regions.region_names["bowsers_kingdom_slingshot_area"]: {
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_knocking_down_the_nice_frame"]: True_(),
    },
    regions.region_names["bowsers_kingdom_default_start"]: {
        regions.region_names["bowsers_kingdom_behind_the_big_doors"]: Or(
            And(HasStoryProgress("bowsers", [0]), Has(tokens.bowsers_kingdom_access)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.vault, tokens.intermediate_tricks)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.dive, tokens.intermediate_tricks)),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.wall_jump, tokens.intermediate_tricks)),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(HasStoryProgress("bowsers", [1, 2, 3]), HasAll(tokens.triple_jump, tokens.hard_tricks)),
            And(
                HasStoryProgress("bowsers", [1, 2, 3]),
                HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: True_(),
    },
    regions.region_names["bowsers_kingdom_behind_the_big_doors"]: {
        regions.region_names["bowsers_kingdom_small_bird_in_bowsers_kingdom"]: Or(
            CanCapture(tokens.goomba),
            HasAll(tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.bowsers_kingdom_access, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            Has(tokens.ground_pound_jump),
            Has(tokens.side_flip),
            HasAll(tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["bowsers_kingdom_third_courtyard_front_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["bowsers_kingdom_default_start"]: True_(),
    },
    regions.region_names["bowsers_kingdom_exterminate_the_ogres_island"]: {
        regions.region_names["bowsers_kingdom_island_in_the_sky_checkpoint"]: False_(),
    },
    regions.region_names["bowsers_kingdom_outer_wall_area"]: {
        regions.region_names["bowsers_kingdom_outer_wall_checkpoint"]: True_(),
        regions.region_names["bowsers_kingdom_main_courtyard_checkpoint"]: True_(),
    },
    regions.region_names["bowsers_kingdom_bowsers_treasure_vault_top"]: {
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_floor"]: True_(),
        regions.region_names["bowsers_kingdom_home_entrance_shop_dress"]: True_(),
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: Or(
            CanCapture(tokens.pokio),
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["bowsers_kingdom_inner_wall_checkpoint"]: And(
            Or(
                Has(tokens.bowsers_kingdom_access),
                HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.down_throw, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            HasStoryProgress("bowsers", [1, 2, 3]),
        ),
        regions.region_names["bowsers_kingdom_past_the_moving_wall_area"]: Or(
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks), HasAll(tokens.dive, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["bowsers_kingdom_shop_link"]: {
        regions.region_names["bowsers_kingdom_souvenir_shop_checkpoint"]: False_(),
    },
    regions.region_names["bowsers_kingdom_third_courtyard_link"]: {
        regions.region_names["bowsers_kingdom_third_courtyard_rear_checkpoint"]: False_(),
    },
    regions.region_names["bowsers_kingdom_second_courtyard_link"]: {
        regions.region_names["bowsers_kingdom_second_courtyard_checkpoint"]: False_(),
    },
    regions.region_names["bowsers_kingdom_home_entrance_patakaron02"]: {
        regions.region_names["bowsers_kingdom_main_courtyard_checkpoint"]: Or(
            Has(tokens.dive),
            HasAll(tokens.bowsers_kingdom_access, tokens.intermediate_tricks),
            And(HasStoryProgress("bowsers", [3]), Has(tokens.bowsers_kingdom_access)),
        ),
    },
    regions.region_names["bowsers_kingdom_home_entrance_tukkun001_enter"]: {
        regions.region_names["bowsers_kingdom_main_courtyard_checkpoint"]: Or(
            Has(tokens.dive),
            HasAll(tokens.bowsers_kingdom_access, tokens.intermediate_tricks),
            And(HasStoryProgress("bowsers", [3]), Has(tokens.bowsers_kingdom_access)),
        ),
    },
    regions.region_names["bowsers_kingdom_past_the_moving_wall_area"]: {
        regions.region_names["bowsers_kingdom_bowsers_treasure_vault_top"]: False_(),
        regions.region_names["bowsers_kingdom_ogre_area"]: False_(),
    },
    regions.region_names["bowsers_kingdom_knocking_down_the_nice_frame"]: {
        regions.region_names["bowsers_kingdom_beneath_the_keep_checkpoint"]: False_(),
    },
    regions.region_names["poison_tides_substage_near_side_poison_wave_ex_ent"]: {
        regions.region_names["poison_tides_substage_far_side_poison_wave_ex_exit"]: CanCapture(tokens.paragoomba),
    },
    regions.region_names["precision_rolling_substage_near_side_rollingstart"]: {
        regions.region_names["precision_rolling_substage_far_side_rollinggoal"]: True_(),
    },
    regions.region_names["precision_rolling_substage_far_side_rollinggoal"]: {
        regions.region_names["precision_rolling_substage_near_side_rollingstart"]: False_(),
    },
    regions.region_names["push_block_peril_substage_near_side_push_block_ex_stage_ent"]: {
        regions.region_names["push_block_peril_substage_far_side_push_block_ex_stage_ent_dokan"]: CanCapture(
            tokens.spark_pylon
        ),
    },
    regions.region_names["push_block_peril_substage_far_side_push_block_ex_stage_ent_dokan"]: {
        regions.region_names["push_block_peril_substage_near_side_push_block_ex_stage_ent"]: Or(
            CanCapture(tokens.spark_pylon), HasAll(tokens.jump, tokens.intermediate_tricks)
        ),
        regions.region_names["push_block_peril_push_block_peril_purples_1_3"]: Or(
            CanCapture(tokens.spark_pylon),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
        ),
    },
    regions.region_names["cap_kingdom_central_plaza_checkpoint"]: {
        regions.region_names["cap_kingdom_home_entrance_rollingstart"]: True_(),
        regions.region_names["cap_kingdom_home_entrance_frog_search_ex_stage_ent"]: True_(),
        regions.region_names["cap_kingdom_fly_to_the_edge_of_the_fog"]: Or(
            CanCapture(tokens.paragoomba), And(CanCapture(tokens.frog), Has(tokens.easy_glitches))
        ),
        regions.region_names["cap_kingdom_hidden_in_a_sunken_hat"]: Or(
            CanCapture(tokens.paragoomba),
            HasAll(tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.frog), Has(tokens.easy_glitches)),
        ),
        regions.region_names["cap_kingdom_moon_rock"]: And(
            Or(
                CanCapture(tokens.paragoomba),
                HasAll(tokens.long_jump, tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                And(CanCapture(tokens.frog), Has(tokens.easy_glitches)),
            ),
            HasStoryProgress("cap", [1, 2, 3]),
        ),
        regions.region_names["cap_kingdom_home_entrance_ex"]: True_(),
        regions.region_names["cap_kingdom_home_return_rollinggoal"]: False_(),
        regions.region_names["cap_kingdom_home_entrance_poison_wave_ex_ent"]: CanCapture(tokens.paragoomba),
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: False_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_1234"]: And(
            Or(
                HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.spin_throw, tokens.intermediate_tricks),
                HasAll(tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.dive, tokens.down_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.down_throw, tokens.intermediate_tricks),
                CanCapture(tokens.paragoomba),
            ),
            HasStoryProgress("cap", [1, 2, 3]),
        ),
        regions.region_names["cap_kingdom_cap_kingdom_purples_5678"]: And(
            Or(
                CanCapture(tokens.paragoomba),
                HasAll(tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.dive, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
                HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
                And(CanCapture(tokens.frog), Has(tokens.intermediate_tricks)),
            ),
            HasStoryProgress("cap", [1, 2, 3]),
        ),
        regions.region_names["cap_kingdom_cap_kingdom_purples_9101112"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_13141516"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_171819"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_202122"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_232425"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_262728"]: True_(),
        regions.region_names["cap_kingdom_cap_kingdom_purples_293031"]: True_(),
        regions.region_names["cap_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["cap_kingdom_cap_peach"]: True_(),
    },
    regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: {
        regions.region_names["cap_kingdom_home_entrance_poison_wave_ex_ent"]: True_(),
        regions.region_names["cap_kingdom_home_entrance_push_block_ex_stage_ent"]: True_(),
        regions.region_names["cap_kingdom_home_return_push_block_ex_stage_ent_dokan"]: False_(),
        regions.region_names["cap_kingdom_fly_to_the_edge_of_the_fog"]: HasAll(tokens.dive, tokens.intermediate_tricks),
        regions.region_names["cap_kingdom_hidden_in_a_sunken_hat"]: HasAll(
            tokens.dive, tokens.vault, tokens.intermediate_tricks
        ),
        regions.region_names["cap_kingdom_central_plaza_checkpoint"]: True_(),
        regions.region_names["cap_kingdom_stage_change_come"]: Has(tokens.paintings),
        regions.region_names["cap_kingdom_cap_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["cap_kingdom_home_return_push_block_ex_stage_ent_dokan"]: {
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: True_(),
    },
    regions.region_names["cap_kingdom_default_start"]: {
        regions.region_names["cap_kingdom_central_plaza_checkpoint"]: True_(),
    },
    regions.region_names["cap_kingdom_home_return_goal"]: {
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: True_(),
    },
    regions.region_names["cap_kingdom_home_return_rollinggoal"]: {
        regions.region_names["cap_kingdom_central_plaza_checkpoint"]: True_(),
    },
    regions.region_names["cap_kingdom_home_entrance_poison_wave_ex_ent"]: {
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: False_(),
    },
    regions.region_names["cap_kingdom_fly_to_the_edge_of_the_fog"]: {
        regions.region_names["cap_kingdom_central_plaza_checkpoint"]: False_(),
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: False_(),
    },
    regions.region_names["inside_cap_tower_default_start"]: {
        regions.region_names["inside_cap_tower_bottom"]: True_(),
    },
    regions.region_names["inside_cap_tower_bottom"]: {
        regions.region_names["inside_cap_tower_top"]: Or(
            CanCapture(tokens.frog),
            HasAll(
                tokens.ground_pound_jump,
                tokens.vault,
                tokens.wall_jump,
                tokens.dive,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.backflip, tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks
            ),
            HasAll(
                tokens.side_flip, tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks
            ),
            HasAll(tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.ground_pound_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
        ),
    },
    regions.region_names["inside_cap_tower_top"]: {
        regions.region_names["inside_cap_tower_bottom"]: True_(),
        regions.region_names["inside_cap_tower_substage_far_side_goal"]: True_(),
    },
    regions.region_names["inside_cap_tower_substage_near_side_ex"]: {
        regions.region_names["inside_cap_tower_bottom"]: True_(),
        regions.region_names["inside_cap_tower_tht_purples_1_4"]: And(
            Or(
                CanCapture(tokens.frog),
                HasAll(tokens.wall_jump, tokens.dive, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.neutral_throw, tokens.ledge_grab, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.up_throw, tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.backflip,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.neutral_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks
                ),
                HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.backflip, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.side_flip,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.neutral_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.side_flip, tokens.wall_jump, tokens.up_throw, tokens.ledge_grab, tokens.intermediate_tricks
                ),
                HasAll(tokens.side_flip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.side_flip, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.ground_pound_jump,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.neutral_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.ground_pound_jump,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.up_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.ground_pound_jump, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.spin, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.spin, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.triple_jump,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.neutral_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.triple_jump, tokens.wall_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks
                ),
                HasAll(tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.triple_jump, tokens.hard_tricks),
                HasAll(tokens.up_throw, tokens.vault, tokens.triple_jump, tokens.hard_tricks),
                HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.side_flip, tokens.wall_jump, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.wall_jump, tokens.hard_tricks),
            ),
            HasStoryProgress("cap", [1, 2, 3]),
        ),
    },
    regions.region_names["cap_kingdom_hidden_in_a_sunken_hat"]: {
        regions.region_names["cap_kingdom_top_hat_tower_checkpoint"]: False_(),
        regions.region_names["cap_kingdom_central_plaza_checkpoint"]: False_(),
    },
    regions.region_names["inside_cap_tower_substage_far_side_goal"]: {
        regions.region_names["inside_cap_tower_tht_purples_5_9"]: And(
            Or(
                CanCapture(tokens.frog),
                HasAll(tokens.dive, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("cap", [1, 2, 3]),
        ),
    },
    regions.region_names["poison_tides_substage_far_side_poison_wave_ex_exit"]: {
        regions.region_names["poison_tides_poison_tides_purples_1_3"]: Or(
            CanCapture(tokens.paragoomba),
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
        ),
    },
    regions.region_names["frog_pond_substage_near_side_frog_search_ex_stage_ent"]: {
        regions.region_names["frog_pond_frog_pond_purples_1_4"]: Or(
            CanCapture(tokens.frog),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump,
                tokens.vault,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.up_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.side_flip, tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(tokens.triple_jump, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.up_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.spin, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["frog_pond_substage_far_side_frog_search_ex_stage_ent"]: True_(),
    },
    regions.region_names["8_bit_chasm_lifts_substage_near_side_lift2d"]: {
        regions.region_names["8_bit_chasm_lifts_substage_far_side_lift2dexit"]: Has(tokens.enter_2d_pipes),
    },
    regions.region_names["gusty_bridges_substage_near_side_wind_blow_ex_start"]: {
        regions.region_names["gusty_bridges_substage_far_side_wind_blow_ex_goal"]: True_(),
    },
    regions.region_names["gusty_bridges_substage_far_side_wind_blow_ex_goal"]: {
        regions.region_names["gusty_bridges_substage_near_side_wind_blow_ex_start"]: False_(),
    },
    regions.region_names["mysterious_clouds_substage_near_side_cap_appear_ex_ent"]: {
        regions.region_names["mysterious_clouds_substage_far_side_cap_appear_ex_exit"]: True_(),
    },
    regions.region_names["nice_shots_with_chain_chomps_substage_near_side_wanwan_ex_start"]: {
        regions.region_names["nice_shots_with_chain_chomps_substage_far_side_wanwan_ex_goal"]: CanCapture(
            tokens.chain_chomp
        ),
    },
    regions.region_names["nice_shots_with_chain_chomps_substage_far_side_wanwan_ex_goal"]: {
        regions.region_names["nice_shots_with_chain_chomps_substage_near_side_wanwan_ex_start"]: False_(),
    },
    regions.region_names["cascade_kingdom_default_start"]: {
        regions.region_names["cascade_kingdom_waterfall_basin_checkpoint"]: True_(),
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
        regions.region_names["cascade_kingdom_first_moon"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_789"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_161718"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_192021"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_222324"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_252627"]: Or(
            Has(tokens.swim), HasAll(tokens.down_throw, tokens.intermediate_tricks)
        ),
        regions.region_names["cascade_kingdom_stage_change_go"]: Or(
            HasAll(tokens.swim, tokens.paintings),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.paintings, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: {
        regions.region_names["cascade_kingdom_fossil_falls_heights_checkpoint"]: Or(
            And(CanCapture(tokens.big_chain_chomp), HasStoryProgress("cascade", [0]), Has(tokens.enter_2d_pipes)),
            HasAll(tokens.triple_jump, tokens.dive, tokens.wall_jump, tokens.backflip, tokens.hard_tricks),
            HasAll(
                tokens.backflip,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.side_flip,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound_jump,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            And(CanCapture(tokens.t_rex), HasStoryProgress("cascade", [0]), Has(tokens.enter_2d_pipes)),
            And(HasStoryProgress("cascade", [1, 2, 3]), Has(tokens.enter_2d_pipes)),
            And(CanCapture(tokens.t_rex), CanCapture(tokens.spark_pylon), HasStoryProgress("cascade", [1, 2, 3])),
        ),
        regions.region_names["cascade_kingdom_home_entrance_lift2d"]: True_(),
        regions.region_names["cascade_kingdom_home_return_lift2dexit"]: False_(),
        regions.region_names["cascade_kingdom_home_entrance_wanwan_ex_start"]: True_(),
        regions.region_names["cascade_kingdom_home_return_wanwan_ex_goal"]: False_(),
        regions.region_names["cascade_kingdom_top_of_the_big_stump_checkpoint"]: And(
            Or(
                Has(tokens.cascade_kingdom_access),
                HasAll(tokens.neutral_throw, tokens.hard_tricks),
                HasAll(tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.neutral_throw, tokens.ledge_grab, tokens.intermediate_tricks),
                HasAll(tokens.triple_jump, tokens.intermediate_tricks),
                HasAll(tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
                HasAll(
                    tokens.double_jump,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.neutral_throw,
                    tokens.intermediate_tricks,
                ),
                HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.wall_jump, tokens.down_throw, tokens.intermediate_tricks),
                HasAll(tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.intermediate_tricks),
            ),
            HasStoryProgress("cascade", [1, 2, 3]),
        ),
        regions.region_names["cascade_kingdom_island_in_the_sky_checkpoint"]: False_(),
        regions.region_names["cascade_kingdom_home_entrance_wind_blow_ex_start"]: True_(),
        regions.region_names["cascade_kingdom_home_return_wind_blow_ex_goal"]: False_(),
        regions.region_names["cascade_kingdom_home_entrance_cap_appear_ex_ent"]: True_(),
        regions.region_names["cascade_kingdom_home_return_cap_appear_ex_exit"]: False_(),
        regions.region_names["cascade_kingdom_first_moon"]: Or(
            CanCapture(tokens.chain_chomp), And(CanCapture(tokens.t_rex), Has(tokens.intermediate_tricks))
        ),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_123"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_456"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_101112"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_131415"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_323334"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_353637"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_383940"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_414243"]: True_(),
        regions.region_names["cascade_kingdom_stage_change_go"]: And(
            Or(
                HasAll(tokens.dive, tokens.paintings),
                HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.paintings, tokens.hard_tricks),
            ),
            HasStoryProgress("cascade", [1, 2, 3]),
        ),
        regions.region_names["cascade_kingdom_cascade_kfr"]: Has(tokens.talk_to_npcs),
        regions.region_names["cascade_kingdom_madame_broode_arena"]: And(
            CanCapture(tokens.t_rex), Has(tokens.intermediate_tricks)
        ),
    },
    regions.region_names["cascade_kingdom_home_return_lift2dexit"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_return_wanwan_ex_goal"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_island_in_the_sky_checkpoint"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
        regions.region_names["cascade_kingdom_top_of_the_big_stump_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_top_of_the_big_stump_checkpoint"]: {
        regions.region_names["cascade_kingdom_island_in_the_sky_checkpoint"]: False_(),
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
        regions.region_names["cascade_kingdom_home_entrance_rex_poppun_ex"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_28293031"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_return_wind_blow_ex_goal"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_return_cap_appear_ex_exit"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_fossil_falls_heights_checkpoint"]: {
        regions.region_names["cascade_kingdom_moon_rock"]: True_(),
        regions.region_names["cascade_kingdom_dark_side_hint_art_cascade"]: True_(),
        regions.region_names["cascade_kingdom_cascade_kingdom_purples_444546"]: True_(),
        regions.region_names["cascade_kingdom_cascade_peach"]: True_(),
        regions.region_names["cascade_kingdom_madame_broode_arena"]: True_(),
    },
    regions.region_names["cascade_kingdom_stage_change_come"]: {
        regions.region_names["cascade_kingdom_island_in_the_sky_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["cascade_kingdom_waterfall_basin_checkpoint"]: {
        regions.region_names["cascade_kingdom_first_moon"]: And(
            Or(CanCapture(tokens.chain_chomp), HasAll(tokens.jump, tokens.easy_glitches)),
            HasStoryProgress("cascade", [0]),
        ),
    },
    regions.region_names["cascade_kingdom_first_moon"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_entrance_lift2d"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_entrance_wanwan_ex_start"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_entrance_cap_appear_ex_ent"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["cascade_kingdom_home_entrance_wind_blow_ex_start"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
    },
    regions.region_names["8_bit_chasm_lifts_substage_far_side_lift2dexit"]: {
        regions.region_names["8_bit_chasm_lifts_cascade_kingdom_purples_47484950"]: Or(
            Has(tokens.enter_2d_pipes),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["cascade_kingdom_madame_broode_arena"]: {
        regions.region_names["cascade_kingdom_stone_bridge_checkpoint"]: True_(),
        regions.region_names["cascade_kingdom_fossil_falls_heights_checkpoint"]: True_(),
    },
    regions.region_names["cloud_kingdom_default_start"]: {
        regions.region_names["cloud_kingdom_moon_rock"]: True_(),
        regions.region_names["cloud_kingdom_home_entrance_fukuwarai"]: True_(),
        regions.region_names["cloud_kingdom_home_entrance_cube"]: True_(),
        regions.region_names["cloud_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["cloud_kingdom_stage_change_come"]: And(
            Has(tokens.paintings), HasStoryProgress("cloud", [3])
        ),
        regions.region_names["cloud_kingdom_cloud_peach"]: True_(),
    },
    regions.region_names["2d_cube_substage_near_side_cube"]: {
        regions.region_names["2d_cube_substage_far_side_cube"]: True_(),
    },
    regions.region_names["picture_match_substage_near_side_fukuwarai"]: {
        regions.region_names["picture_match_substage_far_side_fukuwarai"]: True_(),
    },
    regions.region_names["cloud_kingdom_stage_change_come"]: {
        regions.region_names["cloud_kingdom_default_start"]: Has(tokens.paintings),
    },
    regions.region_names["yoshi_on_the_sinking_island_substage_near_side_sea_world_ex3a"]: {
        regions.region_names["yoshi_on_the_sinking_island_start_of_subarea"]: True_(),
    },
    regions.region_names["yoshi_on_the_sinking_island_start_of_subarea"]: {
        regions.region_names["yoshi_on_the_sinking_island_substage_far_side_sea_world_ex3b"]: Or(
            CanCapture(tokens.yoshi),
            HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
        ),
        regions.region_names["yoshi_on_the_sinking_island_substage_far_side_senobi_tower_yoshi_ex_exit"]: CanCapture(
            tokens.yoshi
        ),
    },
    regions.region_names["yoshi_on_the_sinking_island_substage_far_side_sea_world_ex3b"]: {
        regions.region_names["yoshi_on_the_sinking_island_start_of_subarea"]: HasAll(
            tokens.vault, tokens.neutral_throw, tokens.hard_tricks
        ),
    },
    regions.region_names["yoshi_under_siege_substage_near_side_taxi"]: {
        regions.region_names["yoshi_under_siege_substage_far_side_taxireturn"]: True_(),
    },
    regions.region_names["dark_side_default_start"]: {
        regions.region_names["dark_side_main_land"]: Or(
            CanCapture(tokens.spark_pylon),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.moon_kingdom_low_gravity,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.triple_jump,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.moon_kingdom_low_gravity,
                tokens.hard_tricks,
            ),
            HasAll(tokens.triple_jump, tokens.long_jump, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
        ),
        regions.region_names["dark_side_home_entrance_killer_road_no_cap_ex"]: Has(tokens.scarecrows),
        regions.region_names["dark_side_stage_change_come"]: And(CanCapture(tokens.spark_pylon), Has(tokens.paintings)),
        regions.region_names["dark_side_stage_change_go"]: False_(),
    },
    regions.region_names["dark_side_main_land"]: {
        regions.region_names["dark_side_home_entrance_lava_world_up_down_yoshi_ex"]: True_(),
        regions.region_names["dark_side_home_entrance_senobi_tower_yoshi_ex"]: True_(),
        regions.region_names["dark_side_default_start"]: CanCapture(tokens.spark_pylon),
        regions.region_names["dark_side_lower_area"]: True_(),
        regions.region_names["dark_side_1st_ledge"]: Or(
            Has(tokens.moon_kingdom_low_gravity), HasAll(tokens.dark_side_access, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["dark_side_home_entrance_killer_road_no_cap_ex"]: {
        regions.region_names["dark_side_default_start"]: True_(),
    },
    regions.region_names["dark_side_home_entrance_stacker_room_start"]: {
        regions.region_names["dark_side_home_entrance_bomb_tail_room_start"]: True_(),
    },
    regions.region_names["dark_side_home_entrance_bomb_tail_room_start"]: {
        regions.region_names["dark_side_home_entrance_fire_blower_room_start"]: True_(),
    },
    regions.region_names["dark_side_home_entrance_cap_thrower_room_start"]: {
        regions.region_names["dark_side_home_entrance_fire_blower_room_start"]: True_(),
        regions.region_names["dark_side_dark_side_mech_fight"]: True_(),
        regions.region_names["dark_side_dark_side_captain_toad"]: True_(),
    },
    regions.region_names["breakdown_road_capless_substage_near_side_killer_road_no_cap_ex"]: {
        regions.region_names["breakdown_road_capless_substage_far_side_killer_road_no_cap_ex"]: True_(),
    },
    regions.region_names["invisible_road_capless_substage_near_side_packun_poison_no_cap_ex"]: {
        regions.region_names["invisible_road_capless_substage_far_side_packun_poison_no_cap_ex_exit"]: Or(
            HasAll(tokens.dive, tokens.jump), And(HasHP(2), HasAll(tokens.jump, tokens.intermediate_tricks))
        ),
    },
    regions.region_names["rabbit_ridge_tower_hariet_battle_substage_far_side_bomb_tail_room_goal"]: {
        regions.region_names["rabbit_ridge_tower_hariet_battle_substage_near_side_bomb_tail_room_start"]: True_(),
    },
    regions.region_names["rabbit_ridge_tower_rango_battle_substage_near_side_cap_thrower_room_start"]: {
        regions.region_names["rabbit_ridge_tower_rango_battle_substage_far_side_cap_thrower_room_goal"]: True_(),
    },
    regions.region_names["rabbit_ridge_tower_spewart_battle_substage_near_side_fire_blower_room_start"]: {
        regions.region_names["rabbit_ridge_tower_spewart_battle_substage_far_side_fire_blower_room_goal"]: True_(),
    },
    regions.region_names["rabbit_ridge_tower_topper_battle_substage_far_side_stacker_room_goal"]: {
        regions.region_names["rabbit_ridge_tower_topper_battle_substage_near_side_stacker_room_start"]: True_(),
    },
    regions.region_names["vanishing_road_capless_substage_near_side_bike_steel_no_cap_ex"]: {
        regions.region_names["vanishing_road_capless_substage_far_side_bike_steel_no_cap_ex_exit"]: Or(
            HasAll(tokens.long_jump, tokens.roll_boost, tokens.p_switches),
            HasAll(tokens.roll_boost, tokens.p_switches, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.p_switches, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.p_switches, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["yoshi_on_the_sinking_island_substage_near_side_senobi_tower_yoshi_ex"]: {
        regions.region_names["yoshi_on_the_sinking_island_start_of_subarea"]: True_(),
    },
    regions.region_names["yoshi_under_siege_substage_near_side_shooting_city_yoshi_ex"]: {
        regions.region_names["yoshi_under_siege_substage_far_side_taxireturn"]: True_(),
    },
    regions.region_names["yoshi_under_siege_substage_far_side_shooting_city_yoshi_ex_exit"]: {
        regions.region_names["yoshi_under_siege_substage_near_side_shooting_city_yoshi_ex"]: True_(),
    },
    regions.region_names["yoshis_magma_swamp_substage_near_side_lava_world_up_down_yoshi_ex"]: {
        regions.region_names["yoshis_magma_swamp_substage_far_side_lava_world_up_down_yoshi_ex_exit"]: True_(),
    },
    regions.region_names["vanishing_road_capless_substage_far_side_bike_steel_no_cap_ex_exit"]: {
        regions.region_names["vanishing_road_capless_substage_near_side_bike_steel_no_cap_ex"]: False_(),
    },
    regions.region_names["dark_side_stage_change_come"]: {
        regions.region_names["dark_side_default_start"]: True_(),
        regions.region_names["dark_side_dark_side_captain_toad"]: True_(),
        regions.region_names["dark_side_dark_side_mech_fight"]: True_(),
    },
    regions.region_names["dark_side_stage_change_go"]: {
        regions.region_names["dark_side_default_start"]: True_(),
        regions.region_names["dark_side_lower_area"]: Has(tokens.paintings),
    },
    regions.region_names["dark_side_lower_area"]: {
        regions.region_names["dark_side_main_land"]: Has(tokens.moon_kingdom_low_gravity),
        regions.region_names["dark_side_home_entrance_packun_poison_no_cap_ex"]: Has(tokens.scarecrows),
        regions.region_names["dark_side_home_entrance_shooting_city_yoshi_ex"]: True_(),
    },
    regions.region_names["dark_side_home_entrance_packun_poison_no_cap_ex"]: {
        regions.region_names["dark_side_lower_area"]: True_(),
    },
    regions.region_names["dark_side_home_entrance_senobi_tower_yoshi_ex"]: {
        regions.region_names["dark_side_main_land"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["dark_side_1st_ledge"]: {
        regions.region_names["dark_side_upper_area"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["dark_side_upper_area"]: {
        regions.region_names["dark_side_dark_side_mech_fight"]: CanCapture(tokens.spark_pylon),
        regions.region_names["dark_side_home_entrance_stacker_room_start"]: CanCapture(tokens.spark_pylon),
        regions.region_names["dark_side_home_entrance_bike_steel_no_cap_ex"]: Has(tokens.scarecrows),
        regions.region_names["dark_side_dark_side_captain_toad"]: CanCapture(tokens.spark_pylon),
    },
    regions.region_names["dark_side_home_entrance_bike_steel_no_cap_ex"]: {
        regions.region_names["dark_side_upper_area"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.cap_return_jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["dark_side_dark_side_mech_fight"]: {
        regions.region_names["dark_side_upper_area"]: Or(
            CanCapture(tokens.spark_pylon), HasAll(tokens.dark_side_access, tokens.intermediate_tricks)
        ),
        regions.region_names["dark_side_stage_change_come"]: False_(),
    },
    regions.region_names["dark_side_dark_side_captain_toad"]: {
        regions.region_names["dark_side_dark_side_mech_fight"]: True_(),
        regions.region_names["dark_side_upper_area"]: Or(
            CanCapture(tokens.spark_pylon), HasAll(tokens.dark_side_access, tokens.intermediate_tricks)
        ),
        regions.region_names["dark_side_stage_change_come"]: Has(tokens.paintings),
    },
    regions.region_names["darker_side_default_start"]: {
        regions.region_names["darker_side_home_entrance_cp_entrance"]: CanCapture(tokens.frog),
    },
    regions.region_names["culmina_crater_bowser_escape_default_start"]: {
        regions.region_names["culmina_crater_bowser_escape_home_entrance_room3_goal"]: True_(),
    },
    regions.region_names["culmina_crater_pokio_section_home_entrance_room2_start"]: {
        regions.region_names["culmina_crater_pokio_section_default_start"]: True_(),
        regions.region_names["culmina_crater_pokio_section_substage_near_side_room2_start"]: True_(),
    },
    regions.region_names["inside_culmina_crater_substage_near_side_room2_start"]: {
        regions.region_names["inside_culmina_crater_substage_near_side_room3_start"]: True_(),
    },
    regions.region_names["inside_culmina_crater_substage_near_side_room3_start"]: {
        regions.region_names["inside_culmina_crater_substage_far_side_room2_start"]: True_(),
    },
    regions.region_names["inside_culmina_crater_substage_far_side_room2_start"]: {
        regions.region_names["inside_culmina_crater_substage_far_side_room3_start"]: True_(),
    },
    regions.region_names["inside_culmina_crater_substage_far_side_room3_start"]: {
        regions.region_names["inside_culmina_crater_substage_far_side_moon_goal"]: True_(),
    },
    regions.region_names["inside_culmina_crater_substage_far_side_moon_goal"]: {
        regions.region_names["inside_culmina_crater_substage_near_side_cp_entrance"]: True_(),
    },
    regions.region_names["culmina_crater_bowser_escape_home_entrance_room3_goal"]: {
        regions.region_names["culmina_crater_bowser_escape_substage_far_side_room3_goal"]: True_(),
    },
    regions.region_names["culmina_crater_bowser_escape_substage_far_side_room3_goal"]: {
        regions.region_names["culmina_crater_bowser_escape_substage_near_side_room3_goal"]: True_(),
    },
    regions.region_names["culmina_crater_pokio_section_substage_near_side_room2_start"]: {
        regions.region_names["culmina_crater_pokio_section_substage_far_side_room2_start"]: True_(),
    },
    regions.region_names["inside_culmina_crater_home_entrance_room2_start"]: {
        regions.region_names["inside_culmina_crater_home_entrance_room3_start"]: True_(),
        regions.region_names["inside_culmina_crater_substage_near_side_room2_start"]: True_(),
    },
    regions.region_names["darker_side_home_entrance_cp_entrance"]: {
        regions.region_names["darker_side_default_start"]: True_(),
    },
    regions.region_names["jump_grab_cling_climb_substage_near_side_cap_trampoline_a"]: {
        regions.region_names["jump_grab_cling_climb_substage_far_side_cap_trampoline_b"]: Or(
            Has(tokens.ledge_grab),
            HasAll(tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.wall_jump, tokens.hard_tricks),
        ),
        regions.region_names["jump_grab_cling_climb_jump_grab_cling_and_climb_purples_1_3"]: Or(
            Has(tokens.ledge_grab),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["jump_grab_cling_climb_substage_far_side_cap_trampoline_b"]: {
        regions.region_names["jump_grab_cling_climb_substage_near_side_cap_trampoline_a"]: HasAll(
            tokens.neutral_throw,
            tokens.ground_pound,
            tokens.roll_boost,
            tokens.vault,
            tokens.dive,
            tokens.wall_jump,
            tokens.hard_tricks,
        ),
    },
    regions.region_names["waves_of_poison_substage_near_side_lake_world_moon_ex1a"]: {
        regions.region_names["waves_of_poison_substage_far_side_lake_world_moon_ex1b"]: Or(
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            CanCapture(tokens.frog),
        ),
    },
    regions.region_names["waves_of_poison_substage_far_side_lake_world_moon_ex1b"]: {
        regions.region_names["waves_of_poison_substage_near_side_lake_world_moon_ex1a"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            And(CanCapture(tokens.big_chain_chomp), HasAll(tokens.spin, tokens.intermediate_tricks)),
            HasAll(tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            CanCapture(tokens.frog),
        ),
    },
    regions.region_names["lake_kingdom_lake_world_town_zone"]: {
        regions.region_names["lake_kingdom_underwater_entrance_checkpoint"]: Has(tokens.swim),
    },
    regions.region_names["lake_kingdom_underwater_entrance_checkpoint"]: {
        regions.region_names["lake_kingdom_courtyard_checkpoint"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_water_plaza_entrance_checkpoint"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_viewing_balcony_checkpoint"]: False_(),
        regions.region_names["lake_kingdom_lake_kingdom_purples_424344"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_underwater_moons"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_behind_the_floodgate"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_lake_kingdom_purples_394041"]: Has(tokens.swim),
    },
    regions.region_names["lake_kingdom_water_plaza_entrance_checkpoint"]: {
        regions.region_names["lake_kingdom_water_plaza_display_window_checkpoint"]: True_(),
        regions.region_names["lake_kingdom_water_plaza_terrace_checkpoint"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_lake_kingdom_purples_323334"]: True_(),
        regions.region_names["lake_kingdom_lake_kingdom_purples_212223"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_underwater_moons"]: Or(
            Has(tokens.swim), And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks))
        ),
        regions.region_names["lake_kingdom_lake_world2dzone"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_captain_toad_area"]: Or(
            HasAll(tokens.ground_pound, tokens.swim, tokens.intermediate_tricks),
            HasAll(tokens.swim, tokens.hard_tricks),
            And(CanCapture(tokens.cheep_cheep), Has(tokens.swim)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
    },
    regions.region_names["lake_kingdom_viewing_balcony_checkpoint"]: {
        regions.region_names["lake_kingdom_underwater_entrance_checkpoint"]: Has(tokens.swim),
        regions.region_names["lake_kingdom_stage_change_come"]: Has(tokens.paintings),
        regions.region_names["lake_kingdom_courtyard_checkpoint"]: Or(
            HasAll(tokens.long_jump, tokens.dive),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.long_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["lake_kingdom_water_plaza_terrace_checkpoint"]: Or(
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive),
            HasAll(tokens.long_jump, tokens.dive),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.long_jump, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.hard_tricks),
        ),
        regions.region_names["lake_kingdom_underwater_moons"]: Or(
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)), Has(tokens.swim)
        ),
    },
    regions.region_names["lake_kingdom_default_start"]: {
        regions.region_names["lake_kingdom_lake_town"]: Or(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            And(CanCapture(tokens.zipper), Has(tokens.swim)),
            And(HasStoryProgress("lake", [1, 2, 3]), Has(tokens.lake_kingdom_access)),
            And(CanCapture(tokens.goomba), HasAll(tokens.up_throw, tokens.hard_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.neutral_throw, tokens.backflip, tokens.hard_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.neutral_throw, tokens.double_jump, tokens.hard_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.hard_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.neutral_throw, tokens.side_flip, tokens.hard_tricks)),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["lake_kingdom_moon_rock"]: Or(
            Has(tokens.swim),
            And(HasStoryProgress("lake", [1, 2, 3]), HasAll(tokens.lake_kingdom_access, tokens.intermediate_tricks)),
        ),
        regions.region_names["lake_kingdom_home_entrance_lake_world_moon_ex1a"]: True_(),
        regions.region_names["lake_kingdom_home_return_lake_world_moon_ex1b"]: False_(),
        regions.region_names["lake_kingdom_lake_kingdom_purples_567"]: And(CanCapture(tokens.zipper), Has(tokens.swim)),
        regions.region_names["lake_kingdom_lake_kingdom_purples_121314"]: True_(),
        regions.region_names["lake_kingdom_lake_kingdom_purples_151617"]: Or(
            And(CanCapture(tokens.zipper), HasAll(tokens.wall_jump, tokens.swim)),
            And(CanCapture(tokens.zipper), HasAll(tokens.neutral_throw, tokens.swim, tokens.intermediate_tricks)),
            And(CanCapture(tokens.zipper), HasAll(tokens.up_throw, tokens.swim, tokens.intermediate_tricks)),
            And(CanCapture(tokens.zipper), HasAll(tokens.down_throw, tokens.swim, tokens.intermediate_tricks)),
            And(CanCapture(tokens.zipper), HasAll(tokens.dive, tokens.swim, tokens.intermediate_tricks)),
            And(CanCapture(tokens.zipper), HasAll(tokens.triple_jump, tokens.swim, tokens.intermediate_tricks)),
            And(CanCapture(tokens.zipper), HasAll(tokens.long_jump, tokens.swim)),
            And(
                CanCapture(tokens.zipper),
                HasAll(tokens.spin, tokens.ledge_grab, tokens.swim, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.up_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.down_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.long_jump, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.zipper),
                HasStoryProgress("lake", [1, 2, 3]),
                HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["lake_kingdom_lake_kingdom_purples_181920"]: Or(
            Has(tokens.swim),
            HasAll(tokens.lake_kingdom_access, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["lake_kingdom_behind_the_floodgate"]: And(
            Or(
                And(CanCapture(tokens.zipper), Has(tokens.intermediate_tricks)),
                And(CanCapture(tokens.zipper), Has(tokens.swim)),
            ),
            HasStoryProgress("lake", [3]),
        ),
        regions.region_names["lake_kingdom_lake_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["lake_kingdom_home_return_lake_world_moon_ex1b"]: {
        regions.region_names["lake_kingdom_default_start"]: True_(),
    },
    regions.region_names["lake_kingdom_lake_town"]: {
        regions.region_names["lake_kingdom_home_entrance_goton"]: And(
            Has(tokens.swim), HasStoryProgress("lake", [1, 2, 3])
        ),
        regions.region_names["lake_kingdom_home_return_cap_trampoline_b"]: True_(),
        regions.region_names["lake_kingdom_home_entrance_fastener_ex"]: And(
            CanCapture(tokens.zipper), Has(tokens.swim)
        ),
        regions.region_names["lake_kingdom_lake_world_town_zone"]: True_(),
        regions.region_names["lake_kingdom_courtyard_checkpoint"]: True_(),
    },
    regions.region_names["lake_kingdom_home_return_cap_trampoline_b"]: {
        regions.region_names["lake_kingdom_lake_town"]: False_(),
    },
    regions.region_names["lake_kingdom_courtyard_checkpoint"]: {
        regions.region_names["lake_kingdom_stage_change_go"]: HasAll(tokens.swim, tokens.paintings),
        regions.region_names["lake_kingdom_lake_kingdom_purples_35363738"]: Or(
            CanCapture(tokens.goomba),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["lake_kingdom_viewing_balcony_checkpoint"]: False_(),
        regions.region_names["lake_kingdom_lake_world2dzone"]: Or(
            Has(tokens.swim), HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks)
        ),
        regions.region_names["lake_kingdom_water_plaza_terrace_checkpoint"]: HasAll(
            tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks
        ),
        regions.region_names["lake_kingdom_underwater_moons"]: Or(
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)), Has(tokens.swim)
        ),
    },
    regions.region_names["lake_kingdom_water_plaza_terrace_checkpoint"]: {
        regions.region_names["lake_kingdom_lake_world_timer_athletic000zone"]: Has(tokens.scarecrows),
        regions.region_names["lake_kingdom_lake_kingdom_purples_24252627"]: True_(),
        regions.region_names["lake_kingdom_lake_kingdom_purples_28293031"]: CanCapture(tokens.zipper),
        regions.region_names["lake_kingdom_home_entrance_cap_trampoline_a"]: True_(),
        regions.region_names["lake_kingdom_lake_world2dzone"]: Or(
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.down_throw, tokens.intermediate_tricks),
            Has(tokens.swim),
        ),
        regions.region_names["lake_kingdom_lake_kingdom_purples_212223"]: HasAll(
            tokens.lake_kingdom_access, tokens.intermediate_tricks
        ),
        regions.region_names["lake_kingdom_lake_kingdom_purples_424344"]: Or(
            Has(tokens.swim),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["lake_kingdom_lake_kingdom_purples_454647"]: True_(),
        regions.region_names["lake_kingdom_courtyard_checkpoint"]: Or(
            Has(tokens.swim), HasAll(tokens.dive, tokens.intermediate_tricks)
        ),
        regions.region_names["lake_kingdom_viewing_balcony_checkpoint"]: And(
            Or(
                HasAll(
                    tokens.neutral_throw,
                    tokens.triple_jump,
                    tokens.ground_pound,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.roll,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.scarecrows,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.vault,
                    tokens.cap_return_jump,
                    tokens.neutral_throw,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.scarecrows,
                    tokens.backflip,
                    tokens.long_jump,
                    tokens.dive,
                    tokens.vault,
                    tokens.neutral_throw,
                    tokens.cap_return_jump,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.scarecrows,
                    tokens.vault,
                    tokens.long_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.ground_pound_jump,
                    tokens.jump,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.scarecrows,
                    tokens.vault,
                    tokens.long_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.side_flip,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.scarecrows,
                    tokens.vault,
                    tokens.long_jump,
                    tokens.triple_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.scarecrows,
                    tokens.triple_jump,
                    tokens.vault,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.hard_tricks,
                ),
            ),
            HasStoryProgress("lake", [1, 2, 3]),
        ),
        regions.region_names["lake_kingdom_lake_peach"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_lake_world_shop"]: {
        regions.region_names["crazy_cap_store_substage_far_side_lake_world_shop"]: True_(),
    },
    regions.region_names["unzipping_the_chasm_substage_near_side_fastener_ex"]: {
        regions.region_names["unzipping_the_chasm_substage_far_side_fastener_ex"]: True_(),
    },
    regions.region_names["lake_kingdom_home_entrance_goton"]: {
        regions.region_names["lake_kingdom_underwater_moons"]: Or(CanCapture(tokens.cheep_cheep), Has(tokens.swim)),
        regions.region_names["lake_kingdom_captain_toad_area"]: And(
            CanCapture(tokens.cheep_cheep), Has(tokens.intermediate_tricks)
        ),
        regions.region_names["lake_kingdom_behind_the_floodgate"]: And(
            CanCapture(tokens.cheep_cheep), Has(tokens.intermediate_tricks)
        ),
    },
    regions.region_names["lake_kingdom_water_plaza_display_window_checkpoint"]: {
        regions.region_names["lake_kingdom_home_entrance_lake_world_shop"]: True_(),
    },
    regions.region_names["lake_kingdom_underwater_moons"]: {
        regions.region_names["lake_kingdom_home_entrance_goton"]: Or(CanCapture(tokens.cheep_cheep), Has(tokens.swim)),
        regions.region_names["lake_kingdom_lake_kingdom_purples_891011"]: True_(),
        regions.region_names["lake_kingdom_underwater_entrance_checkpoint"]: Or(
            Has(tokens.swim), CanCapture(tokens.cheep_cheep)
        ),
        regions.region_names["lake_kingdom_water_plaza_entrance_checkpoint"]: Or(
            Has(tokens.swim), CanCapture(tokens.cheep_cheep)
        ),
        regions.region_names["lake_kingdom_viewing_balcony_checkpoint"]: False_(),
        regions.region_names["lake_kingdom_courtyard_checkpoint"]: Or(Has(tokens.swim), CanCapture(tokens.cheep_cheep)),
    },
    regions.region_names["lake_kingdom_behind_the_floodgate"]: {
        regions.region_names["lake_kingdom_home_entrance_goton"]: False_(),
    },
    regions.region_names["lake_kingdom_captain_toad_area"]: {
        regions.region_names["lake_kingdom_home_entrance_goton"]: False_(),
    },
    regions.region_names["lake_kingdom_lake_world2dzone"]: {
        regions.region_names["lake_kingdom_lake_kingdom_purples_1234"]: Has(tokens.enter_2d_pipes),
    },
    regions.region_names["stretch_and_traverse_the_jungle_substage_near_side_imomu_01"]: {
        regions.region_names["stretch_and_traverse_the_jungle_substage_far_side_imomu_02"]: Or(
            And(CanCapture(tokens.tropical_wiggler), Has(tokens.p_switches)),
            HasAll(tokens.p_switches, tokens.jump, tokens.hard_tricks),
            HasAll(tokens.p_switches, tokens.long_jump, tokens.intermediate_tricks),
            HasAll(tokens.p_switches, tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["stretch_and_traverse_the_jungle_substage_far_side_imomu_02"]: {
        regions.region_names["stretch_and_traverse_the_jungle_substage_near_side_imomu_01"]: False_(),
    },
    regions.region_names["lost_kingdom_default_start"]: {
        regions.region_names["lost_kingdom_swamp_hill_checkpoint"]: Or(
            Has(tokens.ground_pound), HasAll(tokens.lost_kingdom_access, tokens.intermediate_tricks), Has(tokens.dive)
        ),
        regions.region_names["lost_kingdom_home_return_imomu_02"]: True_(),
        regions.region_names["lost_kingdom_moon_rock"]: True_(),
        regions.region_names["lost_kingdom_tn_t"]: Or(
            CanCapture(tokens.tropical_wiggler),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            And(CanCapture(tokens.binoculars), HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.binoculars), HasAll(tokens.down_throw, tokens.dive, tokens.intermediate_tricks)),
            HasAll(tokens.long_jump, tokens.down_throw, tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["lost_kingdom_mountainside_platform_checkpoint"]: True_(),
        regions.region_names["lost_kingdom_lost_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["lost_kingdom_swamp_hill_checkpoint"]: {
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: HasAll(
            tokens.ground_pound, tokens.wall_jump, tokens.p_switches
        ),
        regions.region_names["lost_kingdom_mountainside_platform_checkpoint"]: True_(),
        regions.region_names["lost_kingdom_on_a_tree_in_the_swamp"]: Or(
            HasAll(tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.lost_kingdom_access, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            And(CanCapture(tokens.tropical_wiggler), Has(tokens.ground_pound)),
            HasAll(tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound, tokens.intermediate_tricks),
        ),
        regions.region_names["lost_kingdom_butterfly_area"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive),
            HasAll(tokens.backflip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.cap_return_jump, tokens.hard_tricks),
        ),
        regions.region_names["lost_kingdom_stage_change_go"]: Has(tokens.paintings),
    },
    regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: {
        regions.region_names["lost_kingdom_home_entrance_kinopio"]: True_(),
        regions.region_names["lost_kingdom_swamp_hill_checkpoint"]: True_(),
        regions.region_names["lost_kingdom_home_entrance_clash_world_moon_ex2"]: True_(),
        regions.region_names["lost_kingdom_a_butterflys_treasure"]: True_(),
        regions.region_names["lost_kingdom_on_a_tree_in_the_swamp"]: True_(),
        regions.region_names["lost_kingdom_butterfly_area"]: True_(),
        regions.region_names["lost_kingdom_tn_t"]: Or(
            And(CanCapture(tokens.glydon), HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.glydon), HasAll(tokens.down_throw, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.glydon), HasAll(tokens.up_throw, tokens.dive, tokens.hard_tricks)),
        ),
        regions.region_names["lost_kingdom_lost_peach"]: True_(),
    },
    regions.region_names["lost_kingdom_home_return_imomu_02"]: {
        regions.region_names["lost_kingdom_default_start"]: True_(),
    },
    regions.region_names["lost_kingdom_a_butterflys_treasure"]: {
        regions.region_names["lost_kingdom_butterfly_area"]: True_(),
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: False_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_kinopio"]: {
        regions.region_names["crazy_cap_store_substage_far_side_kinopio"]: True_(),
    },
    regions.region_names["klepto_2_lava_boogaloo_substage_far_side_clash_world_moon_ex2"]: {
        regions.region_names["klepto_2_lava_boogaloo_substage_near_side_clash_world_moon_ex2"]: True_(),
    },
    regions.region_names["lost_kingdom_butterfly_area"]: {
        regions.region_names["lost_kingdom_home_entrance_clash_world_moon_ex2"]: True_(),
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: Or(
            HasAll(tokens.ground_pound, tokens.wall_jump, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
        ),
        regions.region_names["lost_kingdom_swamp_hill_checkpoint"]: True_(),
    },
    regions.region_names["lost_kingdom_on_a_tree_in_the_swamp"]: {
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: False_(),
        regions.region_names["lost_kingdom_swamp_hill_checkpoint"]: False_(),
    },
    regions.region_names["lost_kingdom_home_entrance_clash_world_moon_ex2"]: {
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: False_(),
    },
    regions.region_names["lost_kingdom_stage_change_come"]: {
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["lost_kingdom_tn_t"]: {
        regions.region_names["lost_kingdom_rocky_mountain_summit_checkpoint"]: False_(),
    },
    regions.region_names["blazing_above_the_gears_substage_far_side_gabuzou_clock_exdokan"]: {
        regions.region_names["blazing_above_the_gears_substage_near_side_gabuzou_clock_ex"]: True_(),
    },
    regions.region_names["lava_island_fly_by_substage_near_side_fence_lift_ex"]: {
        regions.region_names["lava_island_fly_by_substage_far_side_fence_lift_exdokan"]: CanCapture(tokens.lava_bubble),
    },
    regions.region_names["lava_island_fly_by_substage_far_side_fence_lift_exdokan"]: {
        regions.region_names["lava_island_fly_by_substage_near_side_fence_lift_ex"]: False_(),
    },
    regions.region_names["magma_swamp_substage_near_side_key_move_ex"]: {
        regions.region_names["magma_swamp_substage_far_side_key_move_ex_dokan"]: True_(),
    },
    regions.region_names["narrow_magma_path_substage_near_side_pecho_bubble_ex"]: {
        regions.region_names["narrow_magma_path_substage_far_side_pecho_bubble_ex_dokan"]: Or(
            CanCapture(tokens.lava_bubble),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["simmering_in_the_kitchen_substage_near_side_costume_event_world_lava"]: {
        regions.region_names["simmering_in_the_kitchen_substage_far_side_costume_out"]: True_(),
    },
    regions.region_names["spinning_athletics_substage_near_side_bbqex"]: {
        regions.region_names["spinning_athletics_substage_far_side_bbqex_dokan"]: Or(
            HasAll(tokens.dive, tokens.jump), HasAll(tokens.jump, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["volcano_cave_cruising_substage_near_side_lava_lift_ex"]: {
        regions.region_names["volcano_cave_cruising_substage_far_side_lava_lift_exdokan"]: True_(),
    },
    regions.region_names["volcano_cave_cruising_substage_far_side_lava_lift_exdokan"]: {
        regions.region_names["volcano_cave_cruising_substage_near_side_lava_lift_ex"]: HasAll(
            tokens.vault, tokens.wall_jump, tokens.neutral_throw
        ),
    },
    regions.region_names["luncheon_kingdom_default_start"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza_checkpoint"]: And(
            Or(CanCapture(tokens.lava_bubble), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)),
            HasStoryProgress("luncheon", [0, 2]),
        ),
        regions.region_names["luncheon_kingdom_floating_sky_island_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: And(
            Or(CanCapture(tokens.lava_bubble), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            HasStoryProgress("luncheon", [1, 2]),
        ),
        regions.region_names["luncheon_kingdom_peronza_plaza"]: And(
            Or(CanCapture(tokens.lava_bubble), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)),
            HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
        ),
    },
    regions.region_names["luncheon_kingdom_peronza_plaza_checkpoint"]: {
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: True_(),
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
    },
    regions.region_names["luncheon_kingdom_path_to_the_meat_plateau_checkpoint"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: True_(),
        regions.region_names["luncheon_kingdom_the_rooftop_lantern"]: False_(),
    },
    regions.region_names["luncheon_kingdom_start_of_the_peak_climb_checkpoint"]: {
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: CanCapture(tokens.lava_bubble),
        regions.region_names["luncheon_kingdom_captain_toad"]: True_(),
        regions.region_names["luncheon_kingdom_top_of_the_peak_climb_checkpoint"]: Or(
            CanCapture(tokens.volbonan),
            HasAll(tokens.luncheon_kingdom_access, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.ground_pound_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw, tokens.triple_jump, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
        ),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_luncheon_kfr"]: Has(tokens.talk_to_npcs),
        regions.region_names["luncheon_kingdom_tall_tall_roof"]: HasAll(
            tokens.neutral_throw,
            tokens.cap_return_jump,
            tokens.dive,
            tokens.vault,
            tokens.wall_jump,
            tokens.intermediate_tricks,
        ),
    },
    regions.region_names["luncheon_kingdom_remote_island_in_the_lava_checkpoint"]: {
        regions.region_names["luncheon_kingdom_lava_world_island_zone"]: True_(),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: CanCapture(tokens.lava_bubble),
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
    },
    regions.region_names["luncheon_kingdom_lava_world_timer_athletic000zone"]: {
        regions.region_names["luncheon_kingdom_default_start"]: And(
            Or(
                CanCapture(tokens.volbonan),
                HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks),
                CanCapture(tokens.lava_bubble),
            ),
            HasStoryProgress("luncheon", [1, 2, 6, 7]),
        ),
    },
    regions.region_names["luncheon_kingdom_home_entrance_costume_event_world_lava"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_fork_ex"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza"]: Or(
            CanCapture(tokens.lava_bubble), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["luncheon_kingdom_home_entrance_key_move_ex"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_shop"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
    },
    regions.region_names["luncheon_kingdom_floating_sky_island_checkpoint"]: {
        regions.region_names["luncheon_kingdom_stage_change_come"]: Has(tokens.paintings),
        regions.region_names["luncheon_kingdom_default_start"]: True_(),
    },
    regions.region_names["luncheon_kingdom_lava_world_timer_athletic001zone"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
    },
    regions.region_names["luncheon_kingdom_captain_toad"]: {
        regions.region_names["luncheon_kingdom_start_of_the_peak_climb_checkpoint"]: CanCapture(tokens.lava_bubble),
        regions.region_names["luncheon_kingdom_top_of_the_peak_climb_checkpoint"]: False_(),
    },
    regions.region_names["luncheon_kingdom_peronza_plaza"]: {
        regions.region_names["luncheon_kingdom_home_entrance_town"]: True_(),
        regions.region_names["luncheon_kingdom_peronza_plaza_checkpoint"]: True_(),
        regions.region_names["luncheon_kingdom_salt_pile_isle_checkpoint"]: Or(
            CanCapture(tokens.lava_bubble), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)
        ),
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: Or(
            CanCapture(tokens.lava_bubble),
            HasAll(tokens.neutral_throw, tokens.cap_return_jump, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: True_(),
        regions.region_names["luncheon_kingdom_lava_world_timer_athletic000zone"]: True_(),
        regions.region_names["luncheon_kingdom_home_entrance_fork_ex"]: Or(
            CanCapture(tokens.lava_bubble),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.hard_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.vault, tokens.up_throw, tokens.hard_tricks),
        ),
        regions.region_names["luncheon_kingdom_iminluncheon_peach"]: True_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_fence_lift_ex"]: {
        regions.region_names["luncheon_kingdom_peronza_plaza_checkpoint"]: True_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_lava_lift_ex"]: {
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: Or(
            Has(tokens.enter_2d_pipes), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["luncheon_kingdom_the_rooftop_lantern"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau_checkpoint"]: CanCapture(tokens.fire_bro),
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: False_(),
        regions.region_names["luncheon_kingdom_top_of_the_peak_climb_checkpoint"]: False_(),
    },
    regions.region_names["luncheon_kingdom_lava_world_cave_zone"]: {
        regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: And(
            Or(Has(tokens.enter_2d_pipes), HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks)),
            HasStoryProgress("luncheon", [1, 2, 6, 7]),
        ),
    },
    regions.region_names["fork_flickin_to_the_summit_substage_near_side_fork_ex"]: {
        regions.region_names["fork_flickin_to_the_summit_substage_far_side_fork_ex"]: CanCapture(tokens.volbonan),
    },
    regions.region_names["fork_flickin_to_the_summit_substage_far_side_fork_ex"]: {
        regions.region_names["fork_flickin_to_the_summit_substage_near_side_fork_ex"]: True_(),
    },
    regions.region_names["luncheon_kingdom_slots_substage_near_side_town"]: {
        regions.region_names["luncheon_kingdom_slots_substage_far_side_town"]: True_(),
    },
    regions.region_names["luncheon_treasure_vault_substage_near_side_treasure_event_world_lava"]: {
        regions.region_names["luncheon_treasure_vault_substage_far_side_treasure_event_world_lava"]: True_(),
    },
    regions.region_names["shards_in_the_cheese_rocks_substage_far_side_martin_cube_ex"]: {
        regions.region_names["shards_in_the_cheese_rocks_substage_near_side_martin_cube_ex"]: True_(),
    },
    regions.region_names["luncheon_kingdom_top_of_the_peak_climb_checkpoint"]: {
        regions.region_names["luncheon_kingdom_captain_toad"]: True_(),
        regions.region_names["luncheon_kingdom_the_rooftop_lantern"]: And(
            CanCapture(tokens.lava_bubble), Has(tokens.intermediate_tricks)
        ),
        regions.region_names["luncheon_kingdom_meat_multi"]: And(
            CanCapture(tokens.lava_bubble), HasStoryProgress("luncheon", [2])
        ),
        regions.region_names["luncheon_kingdom_tall_tall_roof"]: Or(
            CanCapture(tokens.volbonan),
            Has(tokens.long_jump),
            HasAll(tokens.vault, tokens.neutral_throw),
            Has(tokens.dive),
            Has(tokens.wall_jump),
            CanCapture(tokens.lava_bubble),
            Has(tokens.roll_boost),
            Has(tokens.triple_jump),
            HasAll(tokens.down_throw, tokens.vault, tokens.jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: {
        regions.region_names["luncheon_kingdom_remote_island_in_the_lava_checkpoint"]: Or(
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.triple_jump,
                tokens.dive,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
            HasAll(tokens.long_jump, tokens.triple_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["luncheon_kingdom_start_of_the_peak_climb_checkpoint"]: And(
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks), HasStoryProgress("luncheon", [1, 2])
        ),
        regions.region_names["luncheon_kingdom_under_the_meat_plateau"]: True_(),
        regions.region_names["luncheon_kingdom_meat_multi"]: Or(
            And(CanCapture(tokens.meat), CanCapture(tokens.lava_bubble), CanCapture(tokens.hammer_bro)),
            And(
                CanCapture(tokens.meat),
                CanCapture(tokens.hammer_bro),
                HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["luncheon_kingdom_home_entrance_gabuzou_clock_ex"]: True_(),
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
        regions.region_names["luncheon_kingdom_spinning_athletics_island"]: Or(
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.triple_jump,
                tokens.dive,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
            HasAll(tokens.long_jump, tokens.triple_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            And(
                HasHP(3),
                HasAll(
                    tokens.jump,
                    tokens.ground_pound,
                    tokens.roll,
                    tokens.cap_return_jump,
                    tokens.dive,
                    tokens.hard_tricks,
                ),
            ),
        ),
        regions.region_names["luncheon_kingdom_meat_plateau_at_sea_level"]: True_(),
    },
    regions.region_names["luncheon_kingdom_volcano_cave_entrance_checkpoint"]: {
        regions.region_names["luncheon_kingdom_start_of_the_peak_climb_checkpoint"]: CanCapture(tokens.lava_bubble),
    },
    regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau_checkpoint"]: Or(
            And(CanCapture(tokens.hammer_bro), HasStoryProgress("luncheon", [0])),
            And(HasStoryProgress("luncheon", [2]), Has(tokens.luncheon_kingdom_access)),
        ),
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: Or(
            And(CanCapture(tokens.hammer_bro), HasStoryProgress("luncheon", [0, 1])),
            And(HasStoryProgress("luncheon", [2, 6, 7]), Has(tokens.luncheon_kingdom_access)),
        ),
        regions.region_names["luncheon_kingdom_captain_toad"]: And(
            CanCapture(tokens.lava_bubble), HasStoryProgress("luncheon", [6, 7])
        ),
        regions.region_names["luncheon_kingdom_the_rooftop_lantern"]: CanCapture(tokens.fire_bro),
        regions.region_names["luncheon_kingdom_peronza_plaza"]: True_(),
        regions.region_names["luncheon_kingdom_jutting_crag"]: Or(
            And(
                CanCapture(tokens.hammer_bro),
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                Has(tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.fire_bro), HasStoryProgress("luncheon", [1, 2, 6, 7]), Has(tokens.intermediate_tricks)
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            ),
            And(CanCapture(tokens.lava_bubble), HasStoryProgress("luncheon", [1, 2, 6, 7])),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.side_flip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(
                    tokens.up_throw,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.intermediate_tricks,
                ),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(
                    tokens.up_throw, tokens.ground_pound_jump, tokens.vault, tokens.dive, tokens.intermediate_tricks
                ),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(
                    tokens.up_throw,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.ledge_grab,
                    tokens.intermediate_tricks,
                ),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(
                    tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks
                ),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.ground_pound_jump, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.spin, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.triple_jump, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.backflip, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(
                    tokens.down_throw, tokens.ground_pound_jump, tokens.vault, tokens.ledge_grab, tokens.hard_tricks
                ),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.side_flip, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.spin, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.down_throw, tokens.triple_jump, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
            ),
        ),
        regions.region_names["luncheon_kingdom_surrounded_by_tall_mountains"]: HasAll(
            tokens.vault, tokens.dive, tokens.neutral_throw, tokens.hard_tricks
        ),
        regions.region_names["luncheon_kingdom_home_entrance_martin_cube_ex"]: CanCapture(tokens.hammer_bro),
        regions.region_names["luncheon_kingdom_home_entrance_pecho_bubble_ex"]: HasAll(
            tokens.vault, tokens.dive, tokens.neutral_throw, tokens.hard_tricks
        ),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: And(
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
        ),
        regions.region_names["luncheon_kingdom_remote_island_in_the_lava_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_spinning_athletics_island"]: False_(),
    },
    regions.region_names["luncheon_kingdom_salt_pile_isle_checkpoint"]: {
        regions.region_names["luncheon_kingdom_moon_rock"]: CanCapture(tokens.lava_bubble),
    },
    regions.region_names["luncheon_kingdom_stage_change_come"]: {
        regions.region_names["luncheon_kingdom_floating_sky_island_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["luncheon_kingdom_under_the_meat_plateau"]: {
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
    },
    regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: {
        regions.region_names["luncheon_kingdom_surrounded_by_tall_mountains"]: And(
            Or(
                And(CanCapture(tokens.hammer_bro), Has(tokens.ground_pound)),
                And(CanCapture(tokens.fire_bro), Has(tokens.ground_pound)),
                HasAll(tokens.ground_pound, tokens.intermediate_tricks),
                And(CanCapture(tokens.lava_bubble), Has(tokens.ground_pound)),
                HasAll(tokens.vault, tokens.dive, tokens.ground_pound, tokens.neutral_throw),
            ),
            HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
        ),
        regions.region_names["luncheon_kingdom_home_entrance_pecho_bubble_ex"]: True_(),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: Or(
            CanCapture(tokens.volbonan),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.down_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.up_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
        ),
        regions.region_names["luncheon_kingdom_home_entrance_treasure_event_world_lava"]: True_(),
        regions.region_names["luncheon_kingdom_under_the_meat_plateau"]: Or(
            And(CanCapture(tokens.hammer_bro), HasStoryProgress("luncheon", [0, 1, 2])),
            And(CanCapture(tokens.fire_bro), HasStoryProgress("luncheon", [1, 2])),
            And(CanCapture(tokens.lava_bubble), HasStoryProgress("luncheon", [0, 1, 2, 6, 7])),
            And(HasStoryProgress("luncheon", [0, 1, 2, 6, 7]), HasAll(tokens.vault, tokens.intermediate_tricks)),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.luncheon_kingdom_access, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("luncheon", [0, 1, 2, 6, 7]),
                HasAll(tokens.spin, tokens.dive, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["luncheon_kingdom_remote_island_in_the_lava_checkpoint"]: CanCapture(tokens.lava_bubble),
        regions.region_names["luncheon_kingdom_spinning_athletics_island"]: CanCapture(tokens.lava_bubble),
    },
    regions.region_names["luncheon_kingdom_home_entrance_martin_cube_ex"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: True_(),
    },
    regions.region_names["luncheon_kingdom_jutting_crag"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: True_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_treasure_event_world_lava"]: {
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: True_(),
    },
    regions.region_names["luncheon_kingdom_surrounded_by_tall_mountains"]: {
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: False_(),
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
    },
    regions.region_names["narrow_magma_path_substage_far_side_pecho_bubble_ex_dokan"]: {
        regions.region_names["narrow_magma_path_substage_near_side_pecho_bubble_ex"]: False_(),
    },
    regions.region_names["luncheon_kingdom_tall_tall_roof"]: {
        regions.region_names["luncheon_kingdom_top_of_the_peak_climb_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_start_of_the_peak_climb_checkpoint"]: False_(),
    },
    regions.region_names["luncheon_kingdom_home_entrance_pecho_bubble_ex"]: {
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: False_(),
    },
    regions.region_names["luncheon_kingdom_spinning_athletics_island"]: {
        regions.region_names["luncheon_kingdom_post_2nd_story_moon"]: False_(),
        regions.region_names["luncheon_kingdom_path_to_the_meat_plateau"]: CanCapture(tokens.lava_bubble),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: False_(),
        regions.region_names["luncheon_kingdom_meat_plateau_at_sea_level"]: Or(
            CanCapture(tokens.lava_bubble),
            And(
                HasHP(3),
                HasAll(tokens.vault, tokens.dive, tokens.cap_return_jump, tokens.neutral_throw, tokens.hard_tricks),
            ),
        ),
        regions.region_names["luncheon_kingdom_home_entrance_bbqex"]: Has(tokens.scarecrows),
    },
    regions.region_names["luncheon_kingdom_meat_plateau_at_sea_level"]: {
        regions.region_names["luncheon_kingdom_spinning_athletics_island"]: And(
            CanCapture(tokens.lava_bubble), HasStoryProgress("luncheon", [1, 2, 6, 7])
        ),
        regions.region_names["luncheon_kingdom_meat_plateau_checkpoint"]: Or(
            CanCapture(tokens.volbonan),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.down_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.backflip,
                tokens.wall_jump,
                tokens.up_throw,
                tokens.spin_throw,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
        ),
        regions.region_names["luncheon_kingdom_home_entrance_pecho_bubble_ex"]: True_(),
    },
    regions.region_names["bullet_billding_substage_near_side_bou"]: {
        regions.region_names["bullet_billding_substage_far_side_boureturn"]: Or(
            Has(tokens.climb),
            HasAll(tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
            And(
                CanCapture(tokens.bullet_bill),
                HasAll(
                    tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.ledge_grab, tokens.intermediate_tricks
                ),
            ),
            HasAll(tokens.backflip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.up_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.cap_return_jump, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.jump, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
        ),
        regions.region_names["bullet_billding_one_mans_trash"]: Or(
            Has(tokens.climb),
            HasAll(tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
            And(
                CanCapture(tokens.bullet_bill),
                HasAll(
                    tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.ledge_grab, tokens.intermediate_tricks
                ),
            ),
            HasAll(tokens.backflip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.up_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.cap_return_jump, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.jump, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["crazy_cap_store_substage_near_side_shop_coin"]: {
        regions.region_names["crazy_cap_store_substage_near_side_shop_corect"]: True_(),
    },
    regions.region_names["crowded_alleyway_substage_near_side_gunsyu"]: {
        regions.region_names["crowded_alleyway_substage_far_side_gunsyudokan"]: True_(),
    },
    regions.region_names["rewiring_the_neighborhood_substage_near_side_densen"]: {
        regions.region_names["rewiring_the_neighborhood_substage_far_side_densendokan"]: CanCapture(tokens.spark_pylon),
    },
    regions.region_names["scooter_daredevil_substage_near_side_bike"]: {
        regions.region_names["scooter_daredevil_substage_far_side_bikereturn"]: Or(
            HasAll(tokens.scooter_riding, tokens.p_switches),
            HasAll(tokens.roll_boost, tokens.triple_jump, tokens.p_switches, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.p_switches, tokens.jump, tokens.hard_tricks),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.long_jump,
                tokens.cap_return_jump,
                tokens.jump,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.long_jump, tokens.jump, tokens.dive, tokens.p_switches, tokens.neutral_throw, tokens.hard_tricks
            ),
            HasAll(tokens.down_throw, tokens.p_switches, tokens.dive, tokens.hard_tricks),
            HasAll(
                tokens.spin_throw,
                tokens.long_jump,
                tokens.p_switches,
                tokens.jump,
                tokens.cap_return_jump,
                tokens.hard_tricks,
            ),
        ),
    },
    regions.region_names["scooter_daredevil_substage_far_side_bikereturn"]: {
        regions.region_names["scooter_daredevil_substage_near_side_bike"]: False_(),
    },
    regions.region_names["scooter_escape_substage_near_side_bike02"]: {
        regions.region_names["scooter_escape_substage_far_side_bike02return"]: Or(
            Has(tokens.scooter_riding), HasAll(tokens.roll_boost, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["scooter_escape_substage_far_side_bike02return"]: {
        regions.region_names["scooter_escape_substage_near_side_bike02"]: False_(),
    },
    regions.region_names["swinging_scaffolding_substage_near_side_gragra"]: {
        regions.region_names["swinging_scaffolding_substage_far_side_gragrareturn"]: True_(),
    },
    regions.region_names["metro_kingdom_default_start"]: {
        regions.region_names["metro_kingdom_city_outskirts_checkpoint"]: And(
            Or(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.neutral_throw,
                    tokens.triple_jump,
                    tokens.ground_pound,
                    tokens.cap_return_jump,
                    tokens.dive,
                    tokens.roll,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.up_throw,
                    tokens.ground_pound,
                    tokens.triple_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.roll,
                    tokens.hard_tricks,
                ),
            ),
            HasStoryProgress("metro", [0]),
        ),
        regions.region_names["metro_kingdom_isolated_rooftop_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: And(
            Or(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(
                    tokens.ground_pound,
                    tokens.triple_jump,
                    tokens.neutral_throw,
                    tokens.cap_return_jump,
                    tokens.dive,
                    tokens.roll,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.ground_pound,
                    tokens.roll,
                    tokens.triple_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.up_throw,
                    tokens.hard_tricks,
                ),
            ),
            HasStoryProgress("metro", [1, 3, 4, 7]),
        ),
        regions.region_names["metro_kingdom_moon_rock"]: True_(),
        regions.region_names["metro_kingdom_stage_change_go"]: Has(tokens.paintings),
    },
    regions.region_names["metro_kingdom_city_outskirts_checkpoint"]: {
        regions.region_names["metro_kingdom_construction_site_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_default_start"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("metro", [0])
        ),
    },
    regions.region_names["metro_kingdom_construction_site_checkpoint"]: {
        regions.region_names["metro_kingdom_construction_access_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_inside_an_iron_girder"]: True_(),
    },
    regions.region_names["metro_kingdom_construction_access_checkpoint"]: {
        regions.region_names["metro_kingdom_heliport_checkpoint"]: And(
            Or(CanCapture(tokens.spark_pylon), Has(tokens.wall_jump)), HasStoryProgress("metro", [0])
        ),
        regions.region_names["metro_kingdom_girder_sandwich"]: And(
            Has(tokens.wall_jump), HasStoryProgress("metro", [0])
        ),
    },
    regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: {
        regions.region_names["metro_kingdom_heliport_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_mayor_pauline_commemorative_park_checkpoint"]: And(
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasStoryProgress("metro", [1, 3, 4, 7]),
        ),
        regions.region_names["metro_kingdom_glittering_above_the_pool"]: Or(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
        ),
        regions.region_names["metro_kingdom_home_return_gunsyudokan"]: And(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasStoryProgress("metro", [1, 3, 4]),
        ),
        regions.region_names["metro_kingdom_girder_sandwich"]: HasAll(
            tokens.cap_return_jump, tokens.intermediate_tricks
        ),
        regions.region_names["metro_kingdom_left_at_the_cafe"]: Has(tokens.ground_pound),
        regions.region_names["metro_kingdom_hint_art"]: HasAll(tokens.cap_return_jump, tokens.intermediate_tricks),
        regions.region_names["metro_kingdom_hanging_between_buildings"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.roll, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.intermediate_tricks),
            And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
            HasAll(tokens.metro_kingdom_access, tokens.hard_tricks),
        ),
        regions.region_names["metro_kingdom_metro_kfr"]: HasAll(tokens.talk_to_npcs, tokens.intermediate_tricks),
        regions.region_names["metro_kingdom_night_metro_multi"]: CanCapture(tokens.sherm),
        regions.region_names["metro_kingdom_home_entrance_bike"]: True_(),
    },
    regions.region_names["metro_kingdom_heliport_checkpoint"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: Or(
            Has(tokens.climb),
            HasAll(tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_donsuke"]: True_(),
        regions.region_names["metro_kingdom_dark_side_hint_art_metro"]: True_(),
    },
    regions.region_names["metro_kingdom_isolated_rooftop_checkpoint"]: {
        regions.region_names["metro_kingdom_default_start"]: True_(),
        regions.region_names["metro_kingdom_stage_change_come"]: Has(tokens.paintings),
    },
    regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: {
        regions.region_names["metro_kingdom_construction_site_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_rooftop_garden_checkpoint"]: And(
            Or(
                And(CanCapture(tokens.spark_pylon), Has(tokens.dive)),
                And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
                CanCapture(tokens.pole),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            HasStoryProgress("metro", [1, 3, 4, 7]),
        ),
        regions.region_names["metro_kingdom_home_entrance_shop_corect"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_shop_coin"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_kaitendokan"]: And(
            CanCapture(tokens.manhole), HasStoryProgress("metro", [1, 3, 4])
        ),
        regions.region_names["metro_kingdom_home_entrance_onpu"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_taxi"]: And(
            CanCapture(tokens.taxi), HasStoryProgress("metro", [1, 3, 4])
        ),
        regions.region_names["metro_kingdom_home_return_taxireturn"]: False_(),
        regions.region_names["metro_kingdom_seaside_hint_art_metro"]: True_(),
        regions.region_names["metro_kingdom_metro_kfr"]: Or(
            And(CanCapture(tokens.spark_pylon), Has(tokens.talk_to_npcs)),
            HasAll(
                tokens.neutral_throw, tokens.vault, tokens.dive, tokens.talk_to_npcs, tokens.jump, tokens.hard_tricks
            ),
            HasAll(
                tokens.double_jump, tokens.up_throw, tokens.vault, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks
            ),
            HasAll(
                tokens.up_throw, tokens.side_flip, tokens.vault, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks
            ),
            HasAll(
                tokens.up_throw, tokens.backflip, tokens.dive, tokens.vault, tokens.talk_to_npcs, tokens.hard_tricks
            ),
            HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.jump,
                tokens.ground_pound_jump,
                tokens.dive,
                tokens.vault,
                tokens.talk_to_npcs,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.vault,
                tokens.talk_to_npcs,
                tokens.cap_return_jump,
                tokens.hard_tricks,
            ),
            HasAll(tokens.wall_jump, tokens.talk_to_npcs),
        ),
        regions.region_names["metro_kingdom_default_start"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("metro", [1, 3, 4, 7])
        ),
    },
    regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: {
        regions.region_names["metro_kingdom_heliport_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_outdoor_cafe_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_mayor_pauline_commemorative_park_checkpoint"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("metro", [1, 3, 4, 7])
        ),
        regions.region_names["metro_kingdom_home_return_taxireturn"]: False_(),
        regions.region_names["metro_kingdom_home_entrance_taxi"]: CanCapture(tokens.taxi),
        regions.region_names["inside_new_donk_city_tower_stage_change_main_enter"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_under001enter"]: CanCapture(tokens.manhole),
        regions.region_names["metro_kingdom_trumpeter"]: Or(
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.p_switches)),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.climb, tokens.intermediate_tricks),
            And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
            CanCapture(tokens.pole),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.jump, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.backflip,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.side_flip,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.backflip,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.vault,
                tokens.dive,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.spin,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound_jump,
                tokens.ground_pound,
                tokens.jump,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.vault,
                tokens.cap_return_jump,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["metro_kingdom_girder_sandwich"]: Or(
            Has(tokens.wall_jump),
            And(CanCapture(tokens.spark_pylon), HasStoryProgress("metro", [1, 3, 4, 7])),
            And(
                CanCapture(tokens.pole),
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.up_throw, tokens.double_jump, tokens.dive, tokens.vault, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(
                    tokens.up_throw,
                    tokens.jump,
                    tokens.ground_pound_jump,
                    tokens.dive,
                    tokens.vault,
                    tokens.hard_tricks,
                ),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("metro", [1, 3, 4, 7]),
                HasAll(
                    tokens.neutral_throw, tokens.cap_return_jump, tokens.triple_jump, tokens.vault, tokens.hard_tricks
                ),
            ),
        ),
        regions.region_names["metro_kingdom_glittering_above_the_pool"]: Or(
            And(CanCapture(tokens.volbonan), Has(tokens.wall_jump)),
            And(CanCapture(tokens.pole), CanCapture(tokens.volbonan)),
            And(
                CanCapture(tokens.volbonan),
                HasAll(tokens.wall_jump, tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["metro_kingdom_left_at_the_cafe"]: Or(
            HasAll(tokens.wall_jump, tokens.ground_pound),
            And(CanCapture(tokens.spark_pylon), Has(tokens.ground_pound)),
            And(CanCapture(tokens.pole), Has(tokens.ground_pound)),
        ),
        regions.region_names["metro_kingdom_hint_art"]: Or(
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.p_switches)),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.p_switches),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.dive, tokens.intermediate_tricks)),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            CanCapture(tokens.pole),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.jump, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.double_jump,
                tokens.dive,
                tokens.vault,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.backflip,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.side_flip,
                tokens.dive,
                tokens.vault,
                tokens.p_switches,
                tokens.ground_pound,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.spin,
                tokens.vault,
                tokens.dive,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.ground_pound_jump,
                tokens.ground_pound,
                tokens.jump,
                tokens.vault,
                tokens.dive,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.cap_return_jump,
                tokens.vault,
                tokens.ground_pound,
                tokens.p_switches,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["metro_kingdom_hanging_between_buildings"]: Or(
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.backflip, tokens.p_switches)),
            And(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.ground_pound, tokens.dive, tokens.p_switches, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.ground_pound_jump, tokens.p_switches)
            ),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.side_flip, tokens.p_switches)),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.triple_jump, tokens.p_switches)),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.spin, tokens.p_switches)),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.vault, tokens.p_switches)),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.backflip, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.dive, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.ground_pound_jump, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.side_flip, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.spin, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.triple_jump, tokens.p_switches),
            HasAll(tokens.wall_jump, tokens.ground_pound, tokens.p_switches, tokens.neutral_throw, tokens.vault),
            And(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            HasAll(tokens.wall_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.jump, tokens.hard_tricks),
        ),
        regions.region_names["metro_kingdom_crossing_lines"]: Or(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            CanCapture(tokens.pole),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.dive,
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.hard_tricks,
            ),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.backflip, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.vault,
                tokens.wall_jump,
                tokens.dive,
                tokens.ground_pound_jump,
                tokens.hard_tricks,
            ),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.side_flip, tokens.hard_tricks),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.triple_jump, tokens.hard_tricks
            ),
        ),
        regions.region_names["metro_kingdom_metro_kfr"]: Or(
            And(CanCapture(tokens.spark_pylon), Has(tokens.talk_to_npcs)),
            HasAll(tokens.wall_jump, tokens.talk_to_npcs),
            HasAll(
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.talk_to_npcs,
                tokens.intermediate_tricks,
            ),
        ),
        regions.region_names["metro_kingdom_home_entrance_bike02"]: True_(),
        regions.region_names["metro_kingdom_home_return_bike02return"]: False_(),
        regions.region_names["metro_kingdom_home_entrance_bonus"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_bou"]: True_(),
        regions.region_names["metro_kingdom_home_return_boureturn"]: False_(),
        regions.region_names["metro_kingdom_home_entrance_densen"]: True_(),
        regions.region_names["metro_kingdom_home_return_densendokan"]: False_(),
        regions.region_names["metro_kingdom_home_return_gunsyudokan"]: Or(
            And(CanCapture(tokens.pole), HasStoryProgress("metro", [0, 1, 3, 4])),
            And(
                CanCapture(tokens.volbonan),
                HasStoryProgress("metro", [4]),
                HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            ),
            And(CanCapture(tokens.spark_pylon), HasStoryProgress("metro", [1, 3, 4])),
        ),
        regions.region_names["metro_kingdom_home_entrance_theater"]: True_(),
        regions.region_names["metro_kingdom_home_return_bikereturn"]: And(
            Or(
                CanCapture(tokens.pole),
                HasAll(tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.intermediate_tricks),
                HasAll(tokens.ledge_grab, tokens.intermediate_tricks),
                And(CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
            ),
            HasStoryProgress("metro", [7]),
        ),
        regions.region_names["metro_kingdom_night_metro_multi"]: True_(),
        regions.region_names["metro_kingdom_inside_an_iron_girder"]: True_(),
        regions.region_names["metro_kingdom_metro_peach"]: True_(),
    },
    regions.region_names["metro_kingdom_rooftop_garden_checkpoint"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_home_entrance_tenjo"]: And(
            CanCapture(tokens.mini_rocket), Has(tokens.long_jump)
        ),
        regions.region_names["metro_kingdom_crossing_lines"]: CanCapture(tokens.spark_pylon),
    },
    regions.region_names["metro_kingdom_moon_rock"]: {
        regions.region_names["metro_kingdom_default_start"]: True_(),
    },
    regions.region_names["metro_kingdom_trumpeter"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_metro_kfr"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_home_return_gragrareturn"]: False_(),
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_left_at_the_cafe"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_girder_sandwich"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_construction_access_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_hanging_between_buildings"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: CanCapture(tokens.spark_pylon),
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_home_entrance_gragra"]: False_(),
    },
    regions.region_names["metro_kingdom_hint_art"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_crossing_lines"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_rooftop_garden_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_glittering_above_the_pool"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: Has(tokens.long_jump),
    },
    regions.region_names["metro_kingdom_home_entrance_gragra"]: {
        regions.region_names["metro_kingdom_hanging_between_buildings"]: Has(tokens.p_switches),
    },
    regions.region_names["metro_kingdom_home_entrance_donsuke"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world_timer_athletic003zone"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_theater"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world_timer_athletic002zone"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign004zone"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_return_taxireturn"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_taxi"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_shop_corect"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_bike02"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_bonus"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_bou"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_densen"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_gunsyu"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_kaitendokan"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: CanCapture(tokens.manhole),
    },
    regions.region_names["metro_kingdom_home_entrance_onpu"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_tenjo"]: {
        regions.region_names["metro_kingdom_rooftop_garden_checkpoint"]: False_(),
        regions.region_names["metro_kingdom_home_return_gunsyudokan"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_shop_coin"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign001zone"]: {
        regions.region_names["metro_kingdom_city_world2dsign000zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign000zone"]: {
        regions.region_names["metro_kingdom_city_world2dsign006zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign006zone"]: {
        regions.region_names["metro_kingdom_city_world2dsign005zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign005zone"]: {
        regions.region_names["metro_kingdom_city_world2dsign003zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign003zone"]: {
        regions.region_names["metro_kingdom_city_world2dsign002zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world2dsign002zone"]: {
        regions.region_names["metro_kingdom_city_world_timer_athletic000zone"]: True_(),
    },
    regions.region_names["metro_kingdom_city_world_timer_athletic000zone"]: {
        regions.region_names["metro_kingdom_default_start"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_far_side_shop_coin"]: {
        regions.region_names["crazy_cap_store_substage_far_side_shop_corect"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_far_side_shop_corect"]: {
        regions.region_names["crazy_cap_store_substage_near_side_shop_corect"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_main_enter"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_under001enter"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["inside_new_donk_city_tower_substage_near_side_main_enter"]: {
        regions.region_names["inside_new_donk_city_tower_substage_far_side_main_exit"]: Or(
            Has(tokens.climb),
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["metro_kingdom_slots_substage_near_side_bonus"]: {
        regions.region_names["metro_kingdom_slots_substage_far_side_bonus"]: True_(),
    },
    regions.region_names["on_the_big_screen_substage_near_side_theater"]: {
        regions.region_names["on_the_big_screen_substage_far_side_theater"]: True_(),
    },
    regions.region_names["pitchblack_mountain_substage_near_side_donsuke"]: {
        regions.region_names["pitchblack_mountain_substage_far_side_donsuke"]: True_(),
    },
    regions.region_names["rainbow_notes_substage_far_side_onpu"]: {
        regions.region_names["rainbow_notes_substage_near_side_onpu"]: True_(),
    },
    regions.region_names["metro_kingdom_home_entrance_car"]: {
        regions.region_names["metro_kingdom_main_street_entrance_checkpoint"]: True_(),
    },
    regions.region_names["rc_race_substage_far_side_car"]: {
        regions.region_names["rc_race_substage_near_side_car"]: True_(),
    },
    regions.region_names["rotating_maze_shards_substage_near_side_kaitendokan"]: {
        regions.region_names["rotating_maze_shards_substage_far_side_kaitendokan"]: True_(),
    },
    regions.region_names["sewers_substage_near_side_under001enter"]: {
        regions.region_names["sewers_city_world_factory01zone"]: True_(),
    },
    regions.region_names["sewers_substage_far_side_under001enter"]: {
        regions.region_names["sewers_substage_near_side_under001enter"]: True_(),
    },
    regions.region_names["swinging_along_the_high_rises_substage_far_side_tenjo"]: {
        regions.region_names["swinging_along_the_high_rises_substage_near_side_tenjo"]: True_(),
    },
    regions.region_names["inside_new_donk_city_tower_stage_change_main_enter"]: {
        regions.region_names["inside_new_donk_city_tower_default_start"]: True_(),
    },
    regions.region_names["metro_kingdom_home_return_gragrareturn"]: {
        regions.region_names["metro_kingdom_metro_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["metro_kingdom_home_return_bike02return"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_return_boureturn"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_home_return_densendokan"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_outdoor_cafe_checkpoint"]: {
        regions.region_names["metro_kingdom_home_entrance_gunsyu"]: True_(),
    },
    regions.region_names["metro_kingdom_home_return_gunsyudokan"]: {
        regions.region_names["metro_kingdom_home_entrance_tenjo"]: And(
            CanCapture(tokens.mini_rocket), HasStoryProgress("metro", [1, 3, 4])
        ),
    },
    regions.region_names["metro_kingdom_home_return_bikereturn"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_plaza_checkpoint"]: True_(),
    },
    regions.region_names["metro_kingdom_stage_change_come"]: {
        regions.region_names["metro_kingdom_isolated_rooftop_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["shards_under_siege_substage_near_side_taxi"]: {
        regions.region_names["shards_under_siege_moon_free_space"]: True_(),
    },
    regions.region_names["shards_under_siege_moon_free_space"]: {
        regions.region_names["shards_under_siege_substage_near_side_taxi"]: CanCapture(tokens.taxi),
        regions.region_names["shards_under_siege_substage_far_side_taxireturn"]: CanCapture(tokens.taxi),
    },
    regions.region_names["shards_under_siege_substage_far_side_taxireturn"]: {
        regions.region_names["shards_under_siege_moon_free_space"]: True_(),
    },
    regions.region_names["metro_kingdom_mayor_pauline_commemorative_park_checkpoint"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
    },
    regions.region_names["metro_kingdom_home_entrance_bike"]: {
        regions.region_names["metro_kingdom_new_donk_city_hall_rooftop_checkpoint"]: False_(),
    },
    regions.region_names["inside_new_donk_city_tower_substage_far_side_main_exit"]: {
        regions.region_names["inside_new_donk_city_tower_substage_near_side_main_enter"]: True_(),
    },
    regions.region_names["bullet_billding_substage_far_side_boureturn"]: {
        regions.region_names["bullet_billding_substage_near_side_bou"]: Or(
            Has(tokens.climb),
            HasAll(tokens.jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin_throw, tokens.intermediate_tricks),
            HasAll(tokens.cap_return_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["bullet_billding_one_mans_trash"]: Or(
            And(CanCapture(tokens.bullet_bill), Has(tokens.climb)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.jump, tokens.intermediate_tricks)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.up_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.spin_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.cap_return_jump, tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.long_jump, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
        ),
    },
    regions.region_names["bullet_billding_one_mans_trash"]: {
        regions.region_names["bullet_billding_substage_near_side_bou"]: False_(),
        regions.region_names["bullet_billding_substage_far_side_boureturn"]: False_(),
    },
    regions.region_names["moon_kingdom_default_start"]: {
        regions.region_names["moon_kingdom_home_entrance_ddd"]: True_(),
        regions.region_names["moon_kingdom_home_entrance_dot00"]: Has(tokens.moon_kingdom_low_gravity),
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.cap_return_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.jump),
            Has(tokens.long_jump),
            Has(tokens.triple_jump),
        ),
        regions.region_names["moon_kingdom_moon_world_home2dzone"]: True_(),
        regions.region_names["moon_kingdom_home_entrance_moon"]: Or(
            HasAll(
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
        ),
        regions.region_names["moon_kingdom_shining_above_the_moon"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
        ),
        regions.region_names["moon_kingdom_moon_timer_1"]: Or(
            HasAll(tokens.long_jump, tokens.moon_kingdom_low_gravity, tokens.scarecrows),
            HasAll(tokens.neutral_throw, tokens.moon_kingdom_low_gravity, tokens.scarecrows, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.dive, tokens.scarecrows, tokens.hard_tricks),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.scarecrows, tokens.dive, tokens.intermediate_tricks),
            HasAll(
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.side_flip,
                tokens.roll,
                tokens.jump,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.backflip,
                tokens.roll,
                tokens.jump,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.jump,
                tokens.ledge_grab,
                tokens.roll,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.jump,
                tokens.wall_jump,
                tokens.roll,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.moon_kingdom_low_gravity, tokens.scarecrows, tokens.double_jump, tokens.roll, tokens.hard_tricks
            ),
            HasAll(
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.spin,
                tokens.jump,
                tokens.roll,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.spin_throw,
                tokens.moon_kingdom_low_gravity,
                tokens.jump,
                tokens.scarecrows,
                tokens.backflip,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.spin_throw,
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.wall_jump,
                tokens.jump,
                tokens.hard_tricks,
            ),
            HasAll(
                tokens.spin_throw,
                tokens.moon_kingdom_low_gravity,
                tokens.scarecrows,
                tokens.side_flip,
                tokens.jump,
                tokens.hard_tricks,
            ),
        ),
    },
    regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: {
        regions.region_names["moon_kingdom_quiet_wall_checkpoint"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            Has(tokens.rocket_flower),
            HasAll(tokens.roll, tokens.intermediate_tricks),
            Has(tokens.dive),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.long_jump, tokens.wall_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["moon_kingdom_stage_change_go"]: False_(),
        regions.region_names["moon_kingdom_bunny_area"]: Or(
            HasAll(tokens.moon_kingdom_low_gravity, tokens.dive),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.wall_jump),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.backflip),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.ground_pound_jump),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.side_flip),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.spin),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.double_jump),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.vault, tokens.neutral_throw),
            HasAll(tokens.up_throw, tokens.vault, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.down_throw, tokens.vault, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(
                tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
            ),
            HasAll(tokens.up_throw, tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.backflip, tokens.ledge_grab, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw, tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.ledge_grab, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(
                tokens.down_throw, tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.down_throw,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.spin, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.wall_jump, tokens.spin, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.triple_jump, tokens.hard_tricks),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.moon_kingdom_low_gravity, tokens.jump, tokens.cap_return_jump, tokens.hard_tricks),
        ),
        regions.region_names["moon_kingdom_moon_rock_area"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.spin, tokens.intermediate_tricks),
        ),
        regions.region_names["moon_kingdom_cliffside_treasure_chest"]: Or(
            HasAll(tokens.rocket_flower, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.rocket_flower, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.triple_jump, tokens.hard_tricks),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.long_jump,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.roll_boost,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.moon_kingdom_low_gravity, tokens.long_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.long_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.moon_kingdom_low_gravity, tokens.long_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["moon_kingdom_quiet_wall_checkpoint"]: {
        regions.region_names["moon_kingdom_home_entrance_ggg"]: Has(tokens.talk_to_npcs),
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: Or(
            HasAll(
                tokens.ground_pound_jump,
                tokens.neutral_throw,
                tokens.wall_jump,
                tokens.dive,
                tokens.vault,
                tokens.moon_kingdom_low_gravity,
            ),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks
            ),
            HasAll(tokens.wall_jump, tokens.side_flip, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
        ),
        regions.region_names["moon_kingdom_home_entrance_bbb"]: True_(),
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["moon_kingdom_home_entrance_ggg"]: {
        regions.region_names["moon_kingdom_quiet_wall_checkpoint"]: True_(),
    },
    regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: {
        regions.region_names["moon_kingdom_wedding_hall_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_home_entrance_aaa"]: True_(),
        regions.region_names["moon_kingdom_shining_above_the_moon"]: CanCapture(tokens.frog),
        regions.region_names["moon_kingdom_moon_rock_area"]: CanCapture(tokens.frog),
        regions.region_names["moon_kingdom_bunny_area"]: CanCapture(tokens.frog),
        regions.region_names["moon_kingdom_stage_change_go"]: And(
            CanCapture(tokens.frog), HasAll(tokens.moon_kingdom_low_gravity, tokens.paintings)
        ),
        regions.region_names["moon_kingdom_quiet_wall_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_cliffside_treasure_chest"]: And(
            CanCapture(tokens.frog), Has(tokens.moon_kingdom_low_gravity)
        ),
    },
    regions.region_names["moon_kingdom_wedding_hall_checkpoint"]: {
        regions.region_names["wedding_room_moon_world_wedding_room_zone"]: True_(),
        regions.region_names["moon_kingdom_home_entrance_aaa"]: True_(),
        regions.region_names["moon_kingdom_stage_change_come"]: Or(
            And(CanCapture(tokens.frog), Has(tokens.paintings)),
            HasAll(tokens.wall_jump, tokens.paintings, tokens.moon_kingdom_low_gravity),
        ),
        regions.region_names["moon_kingdom_roof_of_chapel"]: Or(
            And(CanCapture(tokens.frog), Has(tokens.moon_kingdom_low_gravity)),
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.ground_pound, tokens.moon_kingdom_low_gravity, tokens.hard_tricks
            ),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.backflip,
                tokens.moon_kingdom_low_gravity,
                tokens.vault,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.side_flip,
                tokens.vault,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["moon_kingdom_moon_shards_at_chapel"]: Or(
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.frog), Has(tokens.moon_kingdom_low_gravity)),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.ground_pound, tokens.moon_kingdom_low_gravity, tokens.hard_tricks
            ),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.dive, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.up_throw,
                tokens.vault,
                tokens.backflip,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.vault,
                tokens.side_flip,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.spin, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks
            ),
        ),
        regions.region_names["moon_kingdom_moon_kfr"]: Has(tokens.talk_to_npcs),
        regions.region_names["moon_kingdom_moon_peach"]: Or(
            And(CanCapture(tokens.frog), Has(tokens.moon_kingdom_low_gravity)),
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.moon_kingdom_low_gravity, tokens.intermediate_tricks),
            HasAll(
                tokens.up_throw, tokens.vault, tokens.ground_pound, tokens.moon_kingdom_low_gravity, tokens.hard_tricks
            ),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
            HasAll(
                tokens.up_throw,
                tokens.backflip,
                tokens.moon_kingdom_low_gravity,
                tokens.vault,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.up_throw,
                tokens.side_flip,
                tokens.vault,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
        ),
        regions.region_names["moon_kingdom_moon_timer_1"]: Or(
            And(
                CanCapture(tokens.frog),
                HasAll(
                    tokens.moon_kingdom_low_gravity,
                    tokens.scarecrows,
                    tokens.jump,
                    tokens.roll,
                    tokens.up_throw,
                    tokens.hard_tricks,
                ),
            ),
            And(
                CanCapture(tokens.frog),
                HasAll(
                    tokens.spin_throw,
                    tokens.moon_kingdom_low_gravity,
                    tokens.scarecrows,
                    tokens.jump,
                    tokens.hard_tricks,
                ),
            ),
        ),
    },
    regions.region_names["8_bit_galaxy_substage_near_side_dot00"]: {
        regions.region_names["8_bit_galaxy_substage_far_side_dot01"]: Or(
            HasAll(tokens.enter_2d_pipes, tokens.moon_kingdom_low_gravity),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.moon_kingdom_low_gravity,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.hard_tricks),
        ),
    },
    regions.region_names["crazy_cap_store_substage_near_side_ddd"]: {
        regions.region_names["crazy_cap_store_substage_far_side_ddd"]: True_(),
    },
    regions.region_names["giant_swings_substage_near_side_moon"]: {
        regions.region_names["giant_swings_substage_far_side_moon_exit"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.ledge_grab, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.dive),
            HasAll(tokens.ground_pound_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.dive, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["giant_swings_a_swing_on_top_of_a_swing"]: Or(
            HasAll(tokens.ledge_grab, tokens.intermediate_tricks),
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["moon_cave_escape_moon_world_basement004zone"]: {
        regions.region_names["moon_cave_escape_default_start"]: True_(),
        regions.region_names["moon_cave_escape_moon_world_basement003zone"]: True_(),
    },
    regions.region_names["moon_cave_escape_moon_world_basement000zone"]: {
        regions.region_names["moon_cave_escape_moon_world_basement002zone"]: True_(),
    },
    regions.region_names["moon_cave_escape_moon_world_basement001zone"]: {
        regions.region_names["moon_cave_escape_moon_world_basement002zone"]: True_(),
        regions.region_names["moon_cave_escape_moon_world_basement003zone"]: True_(),
    },
    regions.region_names["moon_kingdom_treasure_vault_substage_near_side_ggg"]: {
        regions.region_names["moon_kingdom_treasure_vault_substage_far_side_ggg"]: True_(),
    },
    regions.region_names["underground_caverns_substage_near_side_bbb"]: {
        regions.region_names["underground_caverns_moon_world_capture_parade_lava_pillar_zone"]: True_(),
        regions.region_names["underground_caverns_moon_world_capture_parade_lift_zone"]: Or(
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.vault, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.vault, tokens.hard_tricks)),
        ),
    },
    regions.region_names["underground_caverns_moon_world_capture_parade_megane_zone"]: {
        regions.region_names["underground_caverns_moon_world_capture_parade_bull_zone"]: Or(
            And(CanCapture(tokens.spark_pylon), HasAll(tokens.ground_pound, tokens.p_switches)),
            And(
                CanCapture(tokens.spark_pylon),
                HasAll(
                    tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
                ),
            ),
            And(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
        ),
    },
    regions.region_names["wedding_room_substage_near_side_aaa"]: {
        regions.region_names["wedding_room_moon_world_wedding_room_zone"]: True_(),
        regions.region_names["wedding_room_substage_far_side_aaa"]: True_(),
    },
    regions.region_names["underground_caverns_moon_world_capture_parade_lava_pillar_zone"]: {
        regions.region_names["underground_caverns_moon_world_capture_parade_lift_zone"]: And(
            CanCapture(tokens.parabones), CanCapture(tokens.spark_pylon)
        ),
    },
    regions.region_names["underground_caverns_moon_world_capture_parade_lift_zone"]: {
        regions.region_names["underground_caverns_moon_world_capture_parade_killer_zone"]: Or(
            HasAll(tokens.moon_kingdom_access, tokens.hard_tricks),
            And(CanCapture(tokens.hammer_bro), CanCapture(tokens.tropical_wiggler), Has(tokens.ground_pound)),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["underground_caverns_moon_world_capture_parade_killer_zone"]: {
        regions.region_names["underground_caverns_moon_world_capture_parade_megane_zone"]: Or(
            CanCapture(tokens.banzai_bill),
            And(
                CanCapture(tokens.bullet_bill),
                HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.bullet_bill),
                HasAll(
                    tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
                ),
            ),
            HasAll(
                tokens.vault,
                tokens.wall_jump,
                tokens.dive,
                tokens.ground_pound,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["underground_caverns_moon_world_capture_parade_bull_zone"]: Or(
            And(CanCapture(tokens.banzai_bill), CanCapture(tokens.spark_pylon), Has(tokens.intermediate_tricks)),
            And(CanCapture(tokens.banzai_bill), HasAll(tokens.wall_jump, tokens.intermediate_tricks)),
            And(
                CanCapture(tokens.bullet_bill),
                CanCapture(tokens.spark_pylon),
                HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.bullet_bill),
                HasAll(
                    tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks
                ),
            ),
        ),
    },
    regions.region_names["underground_caverns_moon_world_capture_parade_bull_zone"]: {
        regions.region_names["underground_caverns_substage_far_side_bbb"]: And(
            CanCapture(tokens.spark_pylon), CanCapture(tokens.broodes_chain_chomp)
        ),
    },
    regions.region_names["moon_kingdom_stage_change_come"]: {
        regions.region_names["moon_kingdom_wedding_hall_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_the_tip_of_a_white_spire"]: True_(),
        regions.region_names["moon_kingdom_roof_of_chapel"]: True_(),
        regions.region_names["moon_kingdom_moon_shards_at_chapel"]: True_(),
        regions.region_names["moon_kingdom_moon_peach"]: True_(),
    },
    regions.region_names["moon_kingdom_stage_change_go"]: {
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_bunny_area"]: True_(),
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: False_(),
    },
    regions.region_names["moon_kingdom_roof_of_chapel"]: {
        regions.region_names["moon_kingdom_stage_change_come"]: False_(),
        regions.region_names["moon_kingdom_the_tip_of_a_white_spire"]: True_(),
    },
    regions.region_names["moon_kingdom_the_tip_of_a_white_spire"]: {
        regions.region_names["moon_kingdom_stage_change_come"]: False_(),
    },
    regions.region_names["moon_kingdom_bunny_area"]: {
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_home_entrance_moon"]: Or(
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["moon_kingdom_stage_change_go"]: Or(
            HasAll(tokens.wall_jump, tokens.moon_kingdom_low_gravity, tokens.paintings),
            HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.paintings, tokens.hard_tricks),
        ),
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: False_(),
    },
    regions.region_names["moon_kingdom_home_entrance_moon"]: {
        regions.region_names["moon_kingdom_bunny_area"]: True_(),
        regions.region_names["moon_kingdom_default_start"]: True_(),
    },
    regions.region_names["moon_kingdom_moon_rock_area"]: {
        regions.region_names["moon_kingdom_moon_rock"]: True_(),
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: True_(),
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: False_(),
    },
    regions.region_names["moon_kingdom_moon_shards_at_chapel"]: {
        regions.region_names["moon_kingdom_stage_change_come"]: False_(),
    },
    regions.region_names["moon_kingdom_moon_peach"]: {
        regions.region_names["moon_kingdom_stage_change_come"]: False_(),
        regions.region_names["moon_kingdom_wedding_hall_checkpoint"]: False_(),
    },
    regions.region_names["8_bit_galaxy_substage_far_side_dot01"]: {
        regions.region_names["8_bit_galaxy_substage_near_side_dot00"]: True_(),
    },
    regions.region_names["giant_swings_substage_far_side_moon_exit"]: {
        regions.region_names["giant_swings_substage_near_side_moon"]: Or(
            Has(tokens.moon_kingdom_low_gravity),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
        ),
        regions.region_names["giant_swings_a_swing_on_top_of_a_swing"]: Or(
            Has(tokens.dive), HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["giant_swings_a_swing_on_top_of_a_swing"]: {
        regions.region_names["giant_swings_substage_far_side_moon_exit"]: False_(),
    },
    regions.region_names["moon_kingdom_home_entrance_dot00"]: {
        regions.region_names["moon_kingdom_default_start"]: True_(),
    },
    regions.region_names["moon_kingdom_shining_above_the_moon"]: {
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: False_(),
    },
    regions.region_names["moon_kingdom_cliffside_treasure_chest"]: {
        regions.region_names["moon_kingdom_ringing_bells_plateau_checkpoint"]: Has(tokens.rocket_flower),
        regions.region_names["moon_kingdom_ever_after_hill_checkpoint"]: False_(),
    },
    regions.region_names["moon_kingdom_moon_timer_1"]: {
        regions.region_names["moon_kingdom_wedding_hall_checkpoint"]: False_(),
        regions.region_names["moon_kingdom_default_start"]: False_(),
    },
    regions.region_names["mushroom_kingdom_default_start"]: {
        regions.region_names["mushroom_kingdom_peachs_castle_main_entrance_checkpoint"]: True_(),
        regions.region_names["mushroom_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["mushroom_kingdom_mushroom_pond_checkpoint"]: True_(),
        regions.region_names["mushroom_kingdom_home_return_peach_world_shop_a"]: True_(),
        regions.region_names["mushroom_kingdom_home_entrance_peach_world_shop_a"]: True_(),
        regions.region_names["mushroom_kingdom_home_entrance_mofumofu_a"]: True_(),
        regions.region_names["mushroom_kingdom_yoshis_house_checkpoint"]: False_(),
        regions.region_names["mushroom_kingdom_home_entrance_peach_world_ex1a"]: False_(),
    },
    regions.region_names["mushroom_kingdom_stage_change_come"]: {
        regions.region_names["mushroom_kingdom_yoshis_house_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["mushroom_kingdom_yoshis_house_checkpoint"]: {
        regions.region_names["mushroom_kingdom_default_start"]: True_(),
    },
    regions.region_names["mushroom_kingdom_mushroom_pond_checkpoint"]: {
        regions.region_names["mushroom_kingdom_home_entrance_boss_magma_a"]: True_(),
        regions.region_names["mushroom_kingdom_home_return_giant_wander_boss_b"]: False_(),
        regions.region_names["mushroom_kingdom_home_entrance_giant_wander_boss_a"]: Has(tokens.swim),
        regions.region_names["mushroom_kingdom_home_entrance_boss_knuckle_a"]: True_(),
        regions.region_names["mushroom_kingdom_mushroom_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["mushroom_kingdom_home_entrance_giant_wander_boss_a"]: {
        regions.region_names["mushroom_kingdom_mushroom_pond_checkpoint"]: True_(),
    },
    regions.region_names["mushroom_kingdom_peachs_castle_main_entrance_checkpoint"]: {
        regions.region_names["mushroom_kingdom_home_entrance_peach_castle_gate"]: True_(),
        regions.region_names["mushroom_kingdom_home_return_peach_castle_gate"]: True_(),
        regions.region_names["mushroom_kingdom_home_entrance_boss_forest_a"]: Or(
            HasAll(tokens.climb, tokens.grab),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            And(CanCapture(tokens.yoshi), Has(tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.vault, tokens.rocket_flower, tokens.hard_tricks),
        ),
        regions.region_names["mushroom_kingdom_home_return_costume_event_world_peach"]: True_(),
        regions.region_names["mushroom_kingdom_home_entrance_costume_event_world_peach"]: True_(),
        regions.region_names["mushroom_kingdom_home_return_boss_raid_b"]: False_(),
        regions.region_names["mushroom_kingdom_home_entrance_boss_raid_a"]: Or(
            And(CanCapture(tokens.yoshi), Has(tokens.swim)),
            And(CanCapture(tokens.yoshi), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.swim, tokens.hard_tricks),
        ),
        regions.region_names["mushroom_kingdom_goomba_woods_checkpoint"]: True_(),
        regions.region_names["mushroom_kingdom_home_entrance_peach_world_ex2a"]: True_(),
        regions.region_names["mushroom_kingdom_castle_roof"]: Or(
            Has(tokens.scarecrows),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.ground_pound_jump, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.ground_pound_jump, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
        ),
    },
    regions.region_names["mushroom_kingdom_home_return_boss_raid_b"]: {
        regions.region_names["mushroom_kingdom_peachs_castle_main_entrance_checkpoint"]: True_(),
    },
    regions.region_names["mushroom_kingdom_home_entrance_boss_forest_a"]: {
        regions.region_names["mushroom_kingdom_peachs_castle_main_entrance_checkpoint"]: True_(),
    },
    regions.region_names["mushroom_kingdom_home_entrance_boss_raid_a"]: {
        regions.region_names["mushroom_kingdom_peachs_castle_main_entrance_checkpoint"]: True_(),
    },
    regions.region_names["mushroom_kingdom_goomba_woods_checkpoint"]: {
        regions.region_names["mushroom_kingdom_home_entrance_fukuwarai2"]: CanCapture(tokens.mini_rocket),
        regions.region_names["mushroom_kingdom_home_return_fukuwarai2"]: False_(),
        regions.region_names["mushroom_kingdom_home_return_peach_world_ex2a"]: True_(),
        regions.region_names["mushroom_kingdom_mushroom_timer_challenge"]: Has(tokens.scarecrows),
    },
    regions.region_names["mushroom_kingdom_home_entrance_fukuwarai2"]: {
        regions.region_names["mushroom_kingdom_goomba_woods_checkpoint"]: True_(),
    },
    regions.region_names["mushroom_kingdom_home_return_fukuwarai2"]: {
        regions.region_names["mushroom_kingdom_goomba_woods_checkpoint"]: True_(),
    },
    regions.region_names["painting_room_lord_of_lightning_substage_near_side_boss_raid_b"]: {
        regions.region_names["painting_room_lord_of_lightning_substage_far_side_boss_raid_b"]: True_(),
        regions.region_names["painting_room_lord_of_lightning_stage_change_boss_raid_a"]: True_(),
    },
    regions.region_names["painting_room_lord_of_lightning_painting_to_lord_of_lightning_boss_re_fight"]: {
        regions.region_names["painting_room_lord_of_lightning_substage_near_side_boss_raid_b"]: True_(),
        regions.region_names["lord_of_lightning_boss_re_fight_default_start"]: True_(),
    },
    regions.region_names["painting_room_mechawiggler_substage_near_side_mofumofu_a"]: {
        regions.region_names["painting_room_mechawiggler_substage_far_side_mofumofu_a"]: True_(),
        regions.region_names["painting_room_mechawiggler_painting_to_mechawiggler_boss_re_fight"]: True_(),
    },
    regions.region_names["painting_room_mollusque_lanceur_substage_near_side_giant_wander_boss_b"]: {
        regions.region_names["painting_room_mollusque_lanceur_substage_far_side_giant_wander_boss_b"]: True_(),
        regions.region_names["painting_room_mollusque_lanceur_stage_change_giant_wander_boss_a"]: True_(),
        regions.region_names["painting_room_mollusque_lanceur_painting_to_mollusque_lanceur_boss_re_fight"]: True_(),
    },
    regions.region_names["painting_room_torkdrift_substage_near_side_boss_forest_a"]: {
        regions.region_names["painting_room_torkdrift_substage_far_side_boss_forest_a"]: True_(),
        regions.region_names["painting_room_torkdrift_painting_to_torkdrift_boss_re_fight"]: True_(),
    },
    regions.region_names["painting_room_lord_of_lightning_home_entrance_picture_boss_raid"]: {
        regions.region_names["painting_room_lord_of_lightning_substage_near_side_boss_raid_b"]: True_(),
    },
    regions.region_names["painting_room_mechawiggler_home_entrance_picture_mofumofu"]: {
        regions.region_names["painting_room_mechawiggler_substage_near_side_mofumofu_a"]: True_(),
    },
    regions.region_names["painting_room_mollusque_lanceur_home_entrance_picture_giant_wander_boss"]: {
        regions.region_names["painting_room_mollusque_lanceur_substage_near_side_giant_wander_boss_b"]: True_(),
    },
    regions.region_names["painting_room_torkdrift_home_entrance_picture_boss_forest"]: {
        regions.region_names["painting_room_torkdrift_substage_near_side_boss_forest_a"]: True_(),
    },
    regions.region_names["painting_room_cookatiel_substage_near_side_boss_magma_a"]: {
        regions.region_names["painting_room_cookatiel_substage_far_side_boss_magma_a"]: True_(),
    },
    regions.region_names["painting_room_cookatiel_substage_far_side_boss_magma_a"]: {
        regions.region_names["painting_room_cookatiel_painting_to_cookatiel_boss_re_fight"]: True_(),
    },
    regions.region_names["painting_room_cookatiel_home_entrance_picture_boss_magma"]: {
        regions.region_names["painting_room_cookatiel_substage_near_side_boss_magma_a"]: True_(),
    },
    regions.region_names["painting_room_knucklotec_substage_near_side_boss_knuckle_a"]: {
        regions.region_names["painting_room_knucklotec_substage_far_side_boss_knuckle_a"]: True_(),
    },
    regions.region_names["painting_room_knucklotec_substage_far_side_boss_knuckle_a"]: {
        regions.region_names["painting_room_knucklotec_painting_to_knucklotec_boss_re_fight"]: True_(),
    },
    regions.region_names["painting_room_knucklotec_home_entrance_picture_boss_knuckle"]: {
        regions.region_names["painting_room_knucklotec_substage_near_side_boss_knuckle_a"]: True_(),
    },
    regions.region_names["mushroom_kingdom_home_return_giant_wander_boss_b"]: {
        regions.region_names["mushroom_kingdom_mushroom_pond_checkpoint"]: True_(),
    },
    regions.region_names["8_bit_bullet_bills_substage_near_side_peach_world_ex2a"]: {
        regions.region_names["8_bit_bullet_bills_substage_far_side_peach_world_ex2a"]: True_(),
    },
    regions.region_names["castle_courtyard_64_substage_near_side_costume_event_world_peach"]: {
        regions.region_names["castle_courtyard_64_substage_far_side_costume_event_world_peach"]: True_(),
    },
    regions.region_names["cookatiel_boss_re_fight_substage_near_side_picture_boss_magma"]: {
        regions.region_names["cookatiel_boss_re_fight_substage_far_side_picture_boss_magma"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_peach_world_shop_a"]: {
        regions.region_names["crazy_cap_store_substage_far_side_peach_world_shop_a"]: True_(),
    },
    regions.region_names["knucklotec_boss_re_fight_substage_far_side_picture_boss_knuckle"]: {
        regions.region_names["knucklotec_boss_re_fight_substage_near_side_picture_boss_knuckle"]: True_(),
    },
    regions.region_names["lord_of_lightning_boss_re_fight_substage_near_side_picture_boss_raid"]: {
        regions.region_names["lord_of_lightning_boss_re_fight_substage_far_side_picture_boss_raid"]: True_(),
    },
    regions.region_names["lord_of_lightning_boss_re_fight_substage_far_side_picture_boss_raid"]: {
        regions.region_names["lord_of_lightning_boss_re_fight_substage_near_side_picture_boss_raid"]: False_(),
    },
    regions.region_names["mechawiggler_boss_re_fight_substage_near_side_picture_mofumofu"]: {
        regions.region_names["mechawiggler_boss_re_fight_substage_far_side_picture_mofumofu"]: True_(),
    },
    regions.region_names["mollusque_lanceur_boss_re_fight_substage_near_side_picture_giant_wander_boss"]: {
        regions.region_names["mollusque_lanceur_boss_re_fight_substage_far_side_picture_giant_wander_boss"]: True_(),
    },
    regions.region_names["mollusque_lanceur_boss_re_fight_substage_far_side_picture_giant_wander_boss"]: {
        regions.region_names["mollusque_lanceur_boss_re_fight_substage_near_side_picture_giant_wander_boss"]: False_(),
    },
    regions.region_names["peachs_castle_substage_near_side_peach_castle_gate"]: {
        regions.region_names["peachs_castle_substage_far_side_peach_castle_gate"]: True_(),
    },
    regions.region_names["picture_match_substage_near_side_fukuwarai2"]: {
        regions.region_names["picture_match_substage_far_side_fukuwarai2"]: CanCapture(tokens.mini_rocket),
    },
    regions.region_names["torkdrift_boss_re_fight_substage_near_side_picture_boss_forest"]: {
        regions.region_names["torkdrift_boss_re_fight_substage_far_side_picture_boss_forest"]: True_(),
    },
    regions.region_names["yoshi_in_the_sea_of_clouds_substage_near_side_peach_world_ex1a"]: {
        regions.region_names["yoshi_in_the_sea_of_clouds_substage_far_side_peach_world_ex1a"]: True_(),
    },
    regions.region_names["mushroom_kingdom_castle_roof"]: {
        regions.region_names["mushroom_kingdom_home_entrance_peach_world_ex1a"]: CanCapture(tokens.yoshi),
    },
    regions.region_names["mushroom_kingdom_home_entrance_peach_world_ex1a"]: {
        regions.region_names["mushroom_kingdom_default_start"]: True_(),
        regions.region_names["mushroom_kingdom_castle_roof"]: False_(),
    },
    regions.region_names["mummy_army_substage_near_side_boss_raid_world_moon_ex02_enter"]: {
        regions.region_names["mummy_army_substage_far_side_boss_raid_world_moon_ex02_exit"]: True_(),
    },
    regions.region_names["mummy_army_substage_far_side_boss_raid_world_moon_ex02_exit"]: {
        regions.region_names["mummy_army_substage_near_side_boss_raid_world_moon_ex02_enter"]: Or(
            Has(tokens.wall_jump),
            Has(tokens.vault),
            HasAll(tokens.backflip, tokens.ledge_grab),
            Has(tokens.dive),
            Has(tokens.climb),
            HasAll(tokens.ground_pound_jump, tokens.ledge_grab),
            HasAll(tokens.side_flip, tokens.ledge_grab),
            HasAll(tokens.spin, tokens.ledge_grab),
            Has(tokens.triple_jump),
        ),
    },
    regions.region_names["ruined_kingdom_default_start"]: {
        regions.region_names["ruined_kingdom_arena"]: CanCapture(tokens.spark_pylon),
        regions.region_names["ruined_kingdom_moon_rock"]: True_(),
        regions.region_names["ruined_kingdom_home_entrance_boss_raid_world_moon_ex02_enter"]: True_(),
        regions.region_names["ruined_kingdom_home_return_boss_raid_world_moon_ex02_exit"]: False_(),
    },
    regions.region_names["ruined_kingdom_arena"]: {
        regions.region_names["ruined_kingdom_home_entrance_boss_raid_world_ex01_eixt"]: CanCapture(tokens.mini_rocket),
        regions.region_names["ruined_kingdom_stage_change_come"]: False_(),
        regions.region_names["ruined_kingdom_ruined_peach"]: True_(),
    },
    regions.region_names["ruined_kingdom_home_entrance_boss_raid_world_ex01_eixt"]: {
        regions.region_names["ruined_kingdom_arena"]: True_(),
    },
    regions.region_names["roulette_tower_substage_near_side_boss_raid_world_ex01_eixt"]: {
        regions.region_names["roulette_tower_substage_far_side_boss_raid_world_ex01_eixt"]: Or(
            And(CanCapture(tokens.mini_rocket), HasAll(tokens.enter_2d_pipes, tokens.p_switches, tokens.ground_pound)),
            And(
                CanCapture(tokens.mini_rocket),
                HasAll(tokens.enter_2d_pipes, tokens.p_switches, tokens.intermediate_tricks),
            ),
        ),
    },
    regions.region_names["ruined_kingdom_home_return_boss_raid_world_moon_ex02_exit"]: {
        regions.region_names["ruined_kingdom_default_start"]: True_(),
    },
    regions.region_names["ruined_kingdom_home_entrance_boss_raid_world_moon_ex02_enter"]: {
        regions.region_names["ruined_kingdom_default_start"]: True_(),
    },
    regions.region_names["ruined_kingdom_stage_change_go"]: {
        regions.region_names["ruined_kingdom_default_start"]: Has(tokens.paintings),
    },
    regions.region_names["ruined_kingdom_stage_change_come"]: {
        regions.region_names["ruined_kingdom_arena"]: True_(),
    },
    regions.region_names["bullet_bill_maze_substage_near_side_doukutu1"]: {
        regions.region_names["bullet_bill_maze_substage_far_side_doukutu2"]: CanCapture(tokens.bullet_bill),
        regions.region_names["bullet_bill_maze_rooftop"]: Or(
            HasAll(tokens.backflip, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.backflip, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.side_flip, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.backflip, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.side_flip, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["bullet_bill_maze_bullet_bill_side_path"]: CanCapture(tokens.bullet_bill),
        regions.region_names["bullet_bill_maze_bullet_bill_maze_purples_1_6"]: CanCapture(tokens.bullet_bill),
    },
    regions.region_names["bullet_bill_maze_substage_far_side_doukutu2"]: {
        regions.region_names["bullet_bill_maze_substage_near_side_doukutu1"]: False_(),
        regions.region_names["bullet_bill_maze_rooftop"]: Or(
            HasAll(tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["crazy_cap_store_substage_near_side_bar1"]: {
        regions.region_names["crazy_cap_store_substage_near_side_bar2"]: False_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_bar2"]: {
        regions.region_names["crazy_cap_store_substage_near_side_bar1"]: False_(),
    },
    regions.region_names["freezing_waterway_substage_near_side_ex_2dhosui"]: {
        regions.region_names["freezing_waterway_substage_far_side_ex_2dhosui_exit"]: CanCapture(tokens.gushen),
    },
    regions.region_names["freezing_waterway_substage_far_side_ex_2dhosui_exit"]: {
        regions.region_names["freezing_waterway_substage_near_side_ex_2dhosui"]: False_(),
    },
    regions.region_names["ice_cave_substage_near_side_arijigoku"]: {
        regions.region_names["ice_cave_substage_far_side_arijigoku2"]: True_(),
        regions.region_names["ice_cave_substage_far_side_arijigoku1"]: True_(),
        regions.region_names["ice_cave_icy_cave_purples_1_4"]: True_(),
    },
    regions.region_names["jaxi_driving_substage_near_side_run00"]: {
        regions.region_names["jaxi_driving_substage_near_side_aaa"]: True_(),
    },
    regions.region_names["jaxi_driving_substage_near_side_aaa"]: {
        regions.region_names["jaxi_driving_substage_near_side_run00"]: False_(),
        regions.region_names["jaxi_driving_substage_far_side_run00return"]: Has(tokens.jaxi_riding),
        regions.region_names["jaxi_driving_jaxi_drivingi_purples_1_8"]: HasAll(tokens.jaxi_riding, tokens.wallet),
        regions.region_names["jaxi_driving_substage_near_side_run00return"]: False_(),
        regions.region_names["jaxi_driving_substage_far_side_aaa"]: False_(),
        regions.region_names["jaxi_driving_substage_far_side_run00"]: False_(),
    },
    regions.region_names["jaxi_driving_substage_far_side_run00return"]: {
        regions.region_names["jaxi_driving_substage_near_side_aaa"]: False_(),
    },
    regions.region_names["transparent_lifts_substage_near_side_meganelift01"]: {
        regions.region_names["transparent_lifts_substage_far_side_meganelift02"]: True_(),
        regions.region_names["transparent_lifts_transparent_lifts_purples_1_4"]: True_(),
    },
    regions.region_names["transparent_lifts_substage_far_side_meganelift02"]: {
        regions.region_names["transparent_lifts_substage_near_side_meganelift01"]: True_(),
    },
    regions.region_names["strange_neighborhood_substage_far_side_birureturn"]: {
        regions.region_names["strange_neighborhood_free_space"]: True_(),
    },
    regions.region_names["strange_neighborhood_free_space"]: {
        regions.region_names["strange_neighborhood_substage_far_side_birureturn"]: CanCapture(tokens.mini_rocket),
        regions.region_names["strange_neighborhood_substage_near_side_biru"]: Or(
            And(
                CanCapture(tokens.mini_rocket),
                HasAll(
                    tokens.neutral_throw,
                    tokens.ground_pound,
                    tokens.roll_boost,
                    tokens.vault,
                    tokens.dive,
                    tokens.hard_tricks,
                ),
            ),
            And(
                CanCapture(tokens.mini_rocket),
                HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
        ),
        regions.region_names["strange_neighborhood_strange_neighborhood_purples_1_4"]: True_(),
    },
    regions.region_names["strange_neighborhood_substage_near_side_biru"]: {
        regions.region_names["strange_neighborhood_free_space"]: Or(
            Has(tokens.scarecrows), HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks)
        ),
    },
    regions.region_names["the_invisible_maze_substage_near_side_anki2"]: {
        regions.region_names["the_invisible_maze_substage_near_side_wall"]: True_(),
    },
    regions.region_names["sand_kingdom_default_start"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_entrance_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_southwestern_floating_island_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_desert_oasis_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_bar2"]: Has(tokens.crouch),
        regions.region_names["sand_kingdom_home_entrance_town"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_bar1"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_abc"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_shindo"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_biru"]: And(
            CanCapture(tokens.mini_rocket), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_home_return_birureturn"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_wall"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_anki2"]: False_(),
        regions.region_names["sand_kingdom_moon_rock"]: True_(),
        regions.region_names["sand_kingdom_jaxi_access"]: And(
            HasAll(tokens.talk_to_npcs, tokens.wallet), HasStoryProgress("sand", [1, 2, 3, 4])
        ),
        regions.region_names["sand_kingdom_sand_kingdom_purples_323334"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_353637"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_383940"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_4142"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_434445464748"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_495051"]: True_(),
        regions.region_names["sand_kingdom_moe_eye_habitat_checkpoint"]: HasAll(
            tokens.neutral_throw, tokens.vault, tokens.dive
        ),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [1, 2, 3, 4])
        ),
    },
    regions.region_names["sand_kingdom_tostarena_ruins_entrance_checkpoint"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_rocket"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_456"]: True_(),
        regions.region_names["sand_kingdom_on_top_of_the_stone_archway"]: Or(
            And(CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [1, 2, 3, 4])),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            ),
            And(HasStoryProgress("sand", [0, 1]), HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks)),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.hard_tricks,
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.neutral_throw, tokens.backflip, tokens.vault, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.neutral_throw, tokens.side_flip, tokens.vault, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.neutral_throw, tokens.spin, tokens.jump, tokens.vault, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(
                    tokens.neutral_throw,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.jump,
                    tokens.intermediate_tricks,
                ),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.up_throw, tokens.vault, tokens.backflip, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(
                    tokens.up_throw, tokens.vault, tokens.ground_pound_jump, tokens.jump, tokens.intermediate_tricks
                ),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.up_throw, tokens.side_flip, tokens.vault, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(tokens.up_throw, tokens.spin, tokens.vault, tokens.intermediate_tricks),
            ),
        ),
        regions.region_names["sand_kingdom_moe_eye_habitat_checkpoint"]: And(
            CanCapture(tokens.bullet_bill), Has(tokens.intermediate_tricks)
        ),
    },
    regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: Or(
            And(CanCapture(tokens.bullet_bill), HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks)),
            HasAll(tokens.wall_jump, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["sand_kingdom_home_entrance_run00"]: False_(),
        regions.region_names["sand_kingdom_home_entrance_hide"]: Has(tokens.talk_to_npcs),
        regions.region_names["sand_kingdom_home_entrance_ex_2dhosui"]: True_(),
        regions.region_names["sand_kingdom_home_return_ex_2dhosui_exit"]: False_(),
        regions.region_names["sand_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["sand_kingdom_sand_world_killer_tower_zone"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_arijigoku"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_101112"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_131415"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_16171819"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_232425"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_60616263"]: True_(),
        regions.region_names["sand_kingdom_home_return_arijigoku1"]: False_(),
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_under01"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_pyramid01"]: True_(),
        regions.region_names["sand_kingdom_tostarena_ruins_above_small_2d_wall"]: Or(
            Has(tokens.enter_2d_pipes),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.ledge_grab, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.ledge_grab, tokens.down_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.up_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.down_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.ground_pound_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.backflip, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.grab, tokens.ground_pound, tokens.ledge_grab, tokens.hard_tricks),
            And(CanCapture(tokens.goomba), HasStoryProgress("sand", [2, 3, 4]), Has(tokens.intermediate_tricks)),
        ),
        regions.region_names["sand_kingdom_home_entrance_run00return"]: False_(),
        regions.region_names["sand_kingdom_on_the_leaning_pillar"]: Or(
            CanCapture(tokens.bullet_bill),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw),
            HasAll(tokens.long_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.sand_kingdom_access, tokens.hard_tricks),
        ),
    },
    regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: {
        regions.region_names["sand_kingdom_moe_eye_habitat_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_on_the_lone_pillar"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_home_entrance_pyramid01"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_under01"]: True_(),
        regions.region_names["sand_kingdom_home_entrance_out"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_293031"]: True_(),
        regions.region_names["sand_kingdom_on_top_of_the_stone_archway"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_tostarena_ruins_above_small_2d_wall"]: True_(),
        regions.region_names["sand_kingdom_on_the_leaning_pillar"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("sand", [2, 3, 4])
        ),
    },
    regions.region_names["sand_kingdom_southwestern_floating_island_checkpoint"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_home_return_arijigoku2"]: False_(),
        regions.region_names["sand_kingdom_jaxi_access"]: HasAll(tokens.wallet, tokens.talk_to_npcs),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: False_(),
    },
    regions.region_names["sand_kingdom_home_return_birureturn"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_home_entrance_run00"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_home_entrance_anki2"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: {
        regions.region_names["sand_kingdom_home_entrance_doukutu1"]: True_(),
        regions.region_names["sand_kingdom_home_return_doukutu2"]: False_(),
        regions.region_names["sand_kingdom_home_entrance_meganelift01"]: True_(),
        regions.region_names["sand_kingdom_home_return_meganelift02"]: False_(),
        regions.region_names["sand_kingdom_on_the_north_pillar"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_poster_cleanup"]: Or(
            And(HasStoryProgress("sand", [4]), Has(tokens.neutral_throw)), Has(tokens.up_throw), Has(tokens.spin_throw)
        ),
        regions.region_names["sand_kingdom_timer_challenge_1"]: Or(
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump),
        ),
        regions.region_names["sand_kingdom_sand_kingdom_purples_202122"]: True_(),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: Has(tokens.enter_2d_pipes),
        regions.region_names["sand_kingdom_home_entrance_out"]: True_(),
        regions.region_names["sand_kingdom_sand_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["sand_kingdom_home_return_doukutu2"]: {
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
        regions.region_names["sand_kingdom_poster_cleanup"]: And(Has(tokens.down_throw), HasStoryProgress("sand", [4])),
        regions.region_names["sand_kingdom_timer_challenge_1"]: True_(),
    },
    regions.region_names["sand_kingdom_home_return_meganelift02"]: {
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_home_return_ex_2dhosui_exit"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_home_return_arijigoku2"]: {
        regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_top_of_the_pyramid"]: {
        regions.region_names["sand_kingdom_on_the_lone_pillar"]: Or(
            And(
                HasStoryProgress("sand", [0]),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            And(HasStoryProgress("sand", [2, 3, 4]), HasAll(tokens.sand_kingdom_access, tokens.intermediate_tricks)),
            And(HasStoryProgress("sand", [2, 3, 4]), HasAll(tokens.talk_to_npcs, tokens.jaxi_riding)),
        ),
        regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: And(
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
            HasStoryProgress("sand", [0, 2, 3, 4]),
        ),
        regions.region_names["sand_kingdom_on_the_north_pillar"]: And(
            Or(
                HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw),
                HasAll(tokens.ground_pound, tokens.roll_boost, tokens.vault, tokens.dive, tokens.neutral_throw),
            ),
            HasStoryProgress("sand", [2, 3, 4]),
        ),
        regions.region_names["sand_kingdom_poster_cleanup"]: And(
            And(CanCapture(tokens.spark_pylon), Has(tokens.down_throw)), HasStoryProgress("sand", [4])
        ),
        regions.region_names["sand_kingdom_timer_challenge_1"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [2, 3, 4])
        ),
        regions.region_names["sand_kingdom_home_entrance_pyramid04"]: True_(),
        regions.region_names["sand_kingdom_sand_kingdom_purples_262728"]: True_(),
        regions.region_names["sand_kingdom_sand_peach"]: True_(),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: And(
            CanCapture(tokens.spark_pylon), HasStoryProgress("sand", [2, 3, 4])
        ),
    },
    regions.region_names["sand_kingdom_timer_challenge_1"]: {
        regions.region_names["sand_kingdom_home_return_doukutu2"]: False_(),
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_poster_cleanup"]: {
        regions.region_names["sand_kingdom_home_return_doukutu2"]: False_(),
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: False_(),
    },
    regions.region_names["sand_kingdom_stage_change_come"]: {
        regions.region_names["sand_kingdom_southwestern_floating_island_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["colossal_ruins_substage_near_side_rocket"]: {
        regions.region_names["colossal_ruins_substage_far_side_rocket"]: True_(),
    },
    regions.region_names["costume_room_substage_near_side_abc"]: {
        regions.region_names["costume_room_substage_far_side_abc"]: True_(),
    },
    regions.region_names["deepest_underground_substage_near_side_yadokari00"]: {
        regions.region_names["deepest_underground_deepest_underground_arena"]: Or(
            CanCapture(tokens.bullet_bill),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["deepest_underground_substage_far_side_yadokari00"]: True_(),
    },
    regions.region_names["underground_ruins_substage_near_side_under01"]: {
        regions.region_names["underground_ruins_underground_ruins_start"]: True_(),
    },
    regions.region_names["underground_ruins_underground_ruins_start"]: {
        regions.region_names["underground_ruins_substage_near_side_under01"]: False_(),
        regions.region_names["underground_ruins_underground_ruins_end"]: CanCapture(tokens.bullet_bill),
        regions.region_names["underground_ruins_underground_purples_1_3"]: True_(),
        regions.region_names["underground_ruins_underground_purples_4_7"]: Or(
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin_throw, tokens.intermediate_tricks),
            Has(tokens.up_throw),
            CanCapture(tokens.goomba),
            CanCapture(tokens.bullet_bill),
        ),
        regions.region_names["underground_ruins_underground_treasure_chest"]: Or(
            And(CanCapture(tokens.bullet_bill), Has(tokens.dive)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.ledge_grab)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.backflip)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.ground_pound_jump)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.side_flip)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.spin)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.triple_jump)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.wall_jump)),
            And(CanCapture(tokens.bullet_bill), Has(tokens.vault)),
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
        ),
    },
    regions.region_names["underground_ruins_substage_far_side_under01"]: {
        regions.region_names["underground_ruins_underground_ruins_start"]: True_(),
    },
    regions.region_names["underground_ruins_underground_ruins_end"]: {
        regions.region_names["underground_ruins_home_entrance_yadokari00"]: True_(),
        regions.region_names["underground_ruins_underground_treasure_chest"]: Or(
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.hard_tricks),
        ),
    },
    regions.region_names["sand_kingdom_jaxi_access"]: {
        regions.region_names["sand_kingdom_home_entrance_run00return"]: Has(tokens.jaxi_riding),
        regions.region_names["sand_kingdom_jaxi_ruins_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_home_entrance_aaa"]: Has(tokens.jaxi_riding),
    },
    regions.region_names["the_invisible_maze_substage_near_side_wall"]: {
        regions.region_names["the_invisible_maze_substage_far_side_wall"]: True_(),
    },
    regions.region_names["the_invisible_maze_substage_far_side_wall"]: {
        regions.region_names["the_invisible_maze_substage_near_side_wall"]: HasAll(
            tokens.neutral_throw, tokens.hard_tricks
        ),
    },
    regions.region_names["bullet_bill_maze_rooftop"]: {
        regions.region_names["bullet_bill_maze_substage_near_side_doukutu1"]: True_(),
        regions.region_names["bullet_bill_maze_substage_far_side_doukutu2"]: True_(),
        regions.region_names["bullet_bill_maze_bullet_bill_side_path"]: True_(),
        regions.region_names["bullet_bill_maze_bullet_bill_maze_purples_1_6"]: True_(),
    },
    regions.region_names["sand_kingdom_home_entrance_run00return"]: {
        regions.region_names["sand_kingdom_jaxi_access"]: False_(),
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_moe_eye_habitat_checkpoint"]: {
        regions.region_names["sand_kingdom_sand_kingdom_purples_123"]: True_(),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: Has(tokens.enter_2d_pipes),
        regions.region_names["sand_kingdom_tostarena_ruins_entrance_checkpoint"]: False_(),
    },
    regions.region_names["inverted_pyramid_lower_interior_substage_near_side_pyramid01"]: {
        regions.region_names["inverted_pyramid_lower_interior_substage_far_side_pyramid01"]: Or(
            And(CanCapture(tokens.bullet_bill), Has(tokens.enter_2d_pipes)),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.enter_2d_pipes, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.enter_2d_pipes, tokens.hard_tricks),
            HasAll(tokens.dive, tokens.enter_2d_pipes, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.triple_jump, tokens.enter_2d_pipes, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.triple_jump, tokens.enter_2d_pipes, tokens.hard_tricks),
            HasAll(tokens.long_jump, tokens.enter_2d_pipes, tokens.hard_tricks),
        ),
    },
    regions.region_names["inverted_pyramid_upper_interior_substage_near_side_pyramid04"]: {
        regions.region_names["inverted_pyramid_upper_interior_upper_inverted_pyramid_start"]: True_(),
        regions.region_names["inverted_pyramid_upper_interior_inverted_pyramid_2d_purples_1_3"]: True_(),
    },
    regions.region_names["inverted_pyramid_upper_interior_upper_inverted_pyramid_start"]: {
        regions.region_names["inverted_pyramid_upper_interior_substage_far_side_pyramid04"]: Or(
            CanCapture(tokens.bullet_bill),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.down_throw, tokens.dive, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.dive, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["sand_kingdom_home_entrance_aaa"]: {
        regions.region_names["sand_kingdom_jaxi_access"]: False_(),
    },
    regions.region_names["sand_kingdom_home_return_arijigoku1"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["deepest_underground_deepest_underground_arena"]: {
        regions.region_names["deepest_underground_substage_near_side_yadokari00"]: True_(),
        regions.region_names["deepest_underground_substage_far_side_out"]: True_(),
    },
    regions.region_names["deepest_underground_substage_far_side_out"]: {
        regions.region_names["deepest_underground_substage_near_side_out"]: False_(),
        regions.region_names["deepest_underground_deepest_underground_arena"]: True_(),
    },
    regions.region_names["deepest_underground_substage_near_side_out"]: {
        regions.region_names["deepest_underground_substage_far_side_out"]: True_(),
    },
    regions.region_names["sand_kingdom_on_the_lone_pillar"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_tostarena_ruins_above_small_2d_wall"]: False_(),
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: False_(),
    },
    regions.region_names["sand_kingdom_home_entrance_under01"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: Has(tokens.enter_2d_pipes),
    },
    regions.region_names["sand_kingdom_home_entrance_out"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: Has(tokens.enter_2d_pipes),
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: True_(),
    },
    regions.region_names["sand_kingdom_home_entrance_pyramid01"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: And(
            Has(tokens.enter_2d_pipes), HasStoryProgress("sand", [0, 2, 3, 4])
        ),
    },
    regions.region_names["sand_kingdom_tostarena_ruins_above_small_2d_wall"]: {
        regions.region_names["sand_kingdom_on_top_of_the_stone_archway"]: CanCapture(tokens.bullet_bill),
        regions.region_names["sand_kingdom_on_the_lone_pillar"]: CanCapture(tokens.bullet_bill),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: Or(
            Has(tokens.enter_2d_pipes),
            And(
                HasStoryProgress("sand", [0, 1]),
                HasAll(
                    tokens.backflip,
                    tokens.wall_jump,
                    tokens.vault,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.hard_tricks,
                ),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.up_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.down_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("sand", [2, 3, 4]),
                HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            ),
        ),
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["jaxi_driving_substage_near_side_run00return"]: {
        regions.region_names["jaxi_driving_substage_near_side_aaa"]: Has(tokens.jaxi_riding),
    },
    regions.region_names["tostarena_slots_substage_near_side_town"]: {
        regions.region_names["tostarena_slots_substage_far_side_town"]: True_(),
    },
    regions.region_names["sand_kingdom_home_entrance_hide"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: True_(),
    },
    regions.region_names["jaxi_driving_substage_far_side_aaa"]: {
        regions.region_names["jaxi_driving_substage_near_side_aaa"]: True_(),
    },
    regions.region_names["jaxi_driving_substage_far_side_run00"]: {
        regions.region_names["jaxi_driving_substage_near_side_aaa"]: True_(),
    },
    regions.region_names["sand_kingdom_on_the_leaning_pillar"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_on_top_of_the_stone_archway"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_above_small_2d_wall"]: False_(),
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
        regions.region_names["sand_kingdom_tostarena_ruins_entrance_checkpoint"]: True_(),
    },
    regions.region_names["inverted_pyramid_lower_interior_substage_far_side_pyramid01"]: {
        regions.region_names["inverted_pyramid_lower_interior_substage_near_side_pyramid01"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_123"]: {
        regions.region_names["sand_kingdom_moe_eye_habitat_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_456"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_entrance_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_789"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_101112"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_131415"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_16171819"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_202122"]: {
        regions.region_names["sand_kingdom_tostarena_northwest_reaches_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_232425"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_262728"]: {
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_293031"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_round_tower_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_323334"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_353637"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_383940"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_4142"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_434445464748"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_495051"]: {
        regions.region_names["sand_kingdom_tostarena_town_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_sand_kingdom_purples_60616263"]: {
        regions.region_names["sand_kingdom_tostarena_ruins_sand_pillar_checkpoint"]: False_(),
    },
    regions.region_names["sand_kingdom_on_the_north_pillar"]: {
        regions.region_names["sand_kingdom_top_of_the_pyramid"]: False_(),
    },
    regions.region_names["flying_through_the_narrow_valley_substage_near_side_sea_world_ex1a"]: {
        regions.region_names["flying_through_the_narrow_valley_substage_far_side_sea_world_ex1b"]: CanCapture(
            tokens.gushen
        ),
    },
    regions.region_names["flying_through_the_narrow_valley_substage_far_side_sea_world_ex1b"]: {
        regions.region_names["flying_through_the_narrow_valley_substage_near_side_sea_world_ex1a"]: False_(),
    },
    regions.region_names["seaside_kingdom_sea_world_lighthouse_zone"]: {
        regions.region_names["seaside_kingdom_lighthouse_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_sea_world_under_glass_zone"]: {
        regions.region_names["seaside_kingdom_glass_palace_checkpoint"]: True_(),
    },
    regions.region_names["stop_poke_and_roll_substage_near_side_sea_world_moon_ex1a"]: {
        regions.region_names["stop_poke_and_roll_substage_far_side_sea_world_moon_ex1b"]: Or(
            CanCapture(tokens.pokio), HasAll(tokens.jump, tokens.hard_tricks)
        ),
    },
    regions.region_names["stop_poke_and_roll_substage_far_side_sea_world_moon_ex1b"]: {
        regions.region_names["stop_poke_and_roll_substage_near_side_sea_world_moon_ex1a"]: False_(),
    },
    regions.region_names["underwater_tunnel_substage_near_side_pukupuku_cave_start"]: {
        regions.region_names["underwater_tunnel_substage_far_side_pukupuku_cave_goal"]: Or(
            And(CanCapture(tokens.cheep_cheep), Has(tokens.swim)),
            HasAll(tokens.swim, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.swim, tokens.hard_tricks),
        ),
    },
    regions.region_names["seaside_kingdom_sea_world_lava_zone"]: {
        regions.region_names["seaside_kingdom_hot_spring_island_checkpoint"]: True_(),
    },
    regions.region_names["a_sea_of_clouds_substage_near_side_sea_world_ex2"]: {
        regions.region_names["a_sea_of_clouds_free_space"]: True_(),
    },
    regions.region_names["a_sea_of_clouds_free_space"]: {
        regions.region_names["a_sea_of_clouds_substage_near_side_sea_world_ex2"]: CanCapture(tokens.mini_rocket),
        regions.region_names["a_sea_of_clouds_substage_far_side_sea_world_ex2return"]: CanCapture(tokens.mini_rocket),
    },
    regions.region_names["a_sea_of_clouds_substage_far_side_sea_world_ex2return"]: {
        regions.region_names["a_sea_of_clouds_free_space"]: True_(),
    },
    regions.region_names["seaside_kingdom_default_start"]: {
        regions.region_names["seaside_kingdom_rolling_canyon_checkpoint"]: True_(),
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_ocean_trench_west_checkpoint"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: True_(),
        regions.region_names["seaside_kingdom_lighthouse"]: Or(
            And(HasStoryProgress("seaside", [1, 2, 3]), HasAll(tokens.climb, tokens.rocket_flower)),
            And(CanCapture(tokens.gushen), Has(tokens.intermediate_tricks)),
            And(HasStoryProgress("seaside", [1, 2, 3]), HasAll(tokens.swim, tokens.climb)),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.triple_jump, tokens.dive, tokens.climb, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.climb, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.dive, tokens.climb, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.climb, tokens.hard_tricks),
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.climb, tokens.hard_tricks),
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.dive, tokens.climb, tokens.hard_tricks),
            ),
        ),
        regions.region_names["seaside_kingdom_home_entrance_shindo_lv2"]: True_(),
        regions.region_names["seaside_kingdom_sea_world_wall_cave_center_zone"]: True_(),
        regions.region_names["seaside_kingdom_on_the_cliff_overlooking_the_beach"]: Or(
            CanCapture(tokens.gushen),
            HasAll(tokens.vault, tokens.dive, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.up_throw,
                tokens.dive,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.vault,
                tokens.hard_tricks,
            ),
            HasAll(tokens.up_throw, tokens.dive, tokens.side_flip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.dive, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
            HasAll(
                tokens.triple_jump,
                tokens.neutral_throw,
                tokens.vault,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["seaside_kingdom_stage_change_go"]: And(
            Has(tokens.paintings), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_hot_spring_island_checkpoint"]: Or(
            HasAll(tokens.neutral_throw, tokens.cap_return_jump, tokens.hard_tricks),
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            CanCapture(tokens.gushen),
        ),
        regions.region_names["seaside_kingdom_underwater_moons"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_underwater_ground_pound_moons"]: Or(
            HasAll(tokens.swim, tokens.ground_pound),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_glass_palace_checkpoint"]: Or(
            Has(tokens.swim),
            HasAll(tokens.neutral_throw, tokens.hard_tricks),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            CanCapture(tokens.gushen),
            And(HasStoryProgress("seaside", [1, 2, 3]), Has(tokens.seaside_kingdom_access)),
        ),
        regions.region_names["seaside_kingdom_home_entrance_pukupuku_cave_start"]: False_(),
        regions.region_names["seaside_kingdom_home_entrance_treasure_event_world_sea"]: False_(),
        regions.region_names["seaside_kingdom_home_entrance_sea_world_moon_ex2"]: False_(),
        regions.region_names["seaside_kingdom_home_entrance_sea_world_ex3a"]: False_(),
        regions.region_names["seaside_kingdom_home_entrance_room_event_world_sea"]: False_(),
        regions.region_names["seaside_kingdom_home_entrance_sea_world_ex1a"]: False_(),
        regions.region_names["seaside_kingdom_seaside_peach"]: True_(),
    },
    regions.region_names["seaside_kingdom_diving_platform_checkpoint"]: {
        regions.region_names["seaside_kingdom_stage_change_come"]: Has(tokens.paintings),
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_beach_house_checkpoint"]: {
        regions.region_names["seaside_kingdom_home_entrance_costume_event_sea_world"]: True_(),
        regions.region_names["seaside_kingdom_diving_platform_checkpoint"]: And(
            CanCapture(tokens.gushen), Has(tokens.intermediate_tricks)
        ),
        regions.region_names["seaside_kingdom_home_entrance_sea_world_ex2"]: CanCapture(tokens.mini_rocket),
        regions.region_names["seaside_kingdom_bonjour_dorrie"]: And(
            CanCapture(tokens.gushen), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_moon_rock"]: True_(),
        regions.region_names["seaside_kingdom_seed_moons"]: Or(
            CanCapture(tokens.gushen),
            HasAll(tokens.rocket_flower, tokens.hard_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.side_flip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.goomba), Has(tokens.hard_tricks)),
        ),
        regions.region_names["seaside_kingdom_narrow_vallet_alcove"]: And(
            Or(
                Has(tokens.seaside_kingdom_access),
                And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
                And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
                CanCapture(tokens.gushen),
                Has(tokens.swim),
                HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
                HasAll(tokens.triple_jump, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.hard_tricks),
            ),
            HasStoryProgress("seaside", [0]),
        ),
        regions.region_names["seaside_kingdom_taking_notes_ocean_surface_dash"]: Or(
            HasAll(tokens.rocket_flower, tokens.notes),
            HasAll(tokens.swim, tokens.notes, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.gushen), HasAll(tokens.notes, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.notes, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.notes, tokens.intermediate_tricks)),
            HasAll(tokens.swim, tokens.notes, tokens.hard_tricks),
            And(CanCapture(tokens.gushen), HasAll(tokens.notes, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_shopping"]: Or(
            And(HasStoryProgress("seaside", [1, 2, 3]), HasAll(tokens.swim, tokens.talk_to_npcs, tokens.wallet)),
            And(HasStoryProgress("seaside", [0]), HasAll(tokens.talk_to_npcs, tokens.wallet)),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.talk_to_npcs, tokens.rocket_flower, tokens.wallet, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.triple_jump, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
            And(
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.neutral_throw, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("seaside", [1, 2, 3]),
                HasAll(tokens.dive, tokens.talk_to_npcs, tokens.hard_tricks),
            ),
        ),
    },
    regions.region_names["seaside_kingdom_ocean_trench_west_checkpoint"]: {
        regions.region_names["seaside_kingdom_home_entrance_sea_world_moon_ex2"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_home_entrance_treasure_event_world_sea"]: HasAll(
            tokens.swim, tokens.talk_to_npcs
        ),
        regions.region_names["seaside_kingdom_lighthouse"]: Or(
            HasAll(tokens.dive, tokens.swim),
            And(CanCapture(tokens.cheep_cheep), Has(tokens.swim)),
            HasAll(tokens.swim, tokens.hard_tricks),
        ),
    },
    regions.region_names["seaside_kingdom_home_entrance_sea_world_ex2"]: {
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_lighthouse_checkpoint"]: {
        regions.region_names["seaside_kingdom_lighthouse_top"]: True_(),
        regions.region_names["seaside_kingdom_rapid_ascent_on_hot_springs_island"]: And(
            And(CanCapture(tokens.glydon), HasAll(tokens.dive, tokens.hard_tricks)),
            HasStoryProgress("seaside", [1, 2, 3]),
        ),
    },
    regions.region_names["seaside_kingdom_sea_world_beach_volley_ball_zone"]: {
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_above_rolling_canyon_checkpoint"]: {
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_sea_world_bottom_hollow_zone"]: {
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_room_event_world_sea"]: {
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_sea_world_ex3a"]: {
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_glass_palace_checkpoint"]: {
        regions.region_names["seaside_kingdom_default_start"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_what_the_waves_left_behind"]: Has(tokens.rocket_flower),
    },
    regions.region_names["seaside_kingdom_hot_spring_island_checkpoint"]: {
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_rapid_ascent_on_hot_springs_island"]: Or(
            CanCapture(tokens.gushen),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["seaside_kingdom_sea_world_long_reef_zone"]: {
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_sea_world_wall_cave_west_zone"]: {
        regions.region_names["seaside_kingdom_sea_world_under_glass_zone"]: True_(),
    },
    regions.region_names["costume_room_substage_near_side_costume_event_sea_world"]: {
        regions.region_names["costume_room_substage_far_side_costume_event_sea_world"]: True_(),
    },
    regions.region_names["rumbling_floor_cave_substage_near_side_shindo_lv2"]: {
        regions.region_names["rumbling_floor_cave_substage_far_side_shindo_lv2"]: True_(),
    },
    regions.region_names["sphynx_treasure_vault_substage_near_side_treasure_event_world_sea"]: {
        regions.region_names["sphynx_treasure_vault_substage_far_side_treasure_event_world_sea"]: Has(tokens.swim),
    },
    regions.region_names["spinning_maze_substage_near_side_sea_world_moon_ex2"]: {
        regions.region_names["spinning_maze_substage_far_side_sea_world_moon_ex2"]: True_(),
    },
    regions.region_names["stretching_up_the_sinking_island_substage_near_side_sea_world_ex3a"]: {
        regions.region_names["stretching_up_the_sinking_island_substage_far_side_sea_world_ex3b"]: Or(
            CanCapture(tokens.uproot),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["stretching_up_the_sinking_island_substage_far_side_sea_world_ex3b"]: {
        regions.region_names["stretching_up_the_sinking_island_substage_near_side_sea_world_ex3a"]: HasAll(
            tokens.vault, tokens.neutral_throw, tokens.hard_tricks
        ),
    },
    regions.region_names["wriggling_power_moon_substage_near_side_room_event_world_sea"]: {
        regions.region_names["wriggling_power_moon_substage_far_side_room_event_world_sea"]: Has(tokens.swim),
    },
    regions.region_names["seaside_kingdom_lighthouse"]: {
        regions.region_names["seaside_kingdom_bonjour_dorrie"]: And(
            Or(HasAll(tokens.seaside_kingdom_access, tokens.intermediate_tricks), CanCapture(tokens.glydon)),
            HasStoryProgress("seaside", [1, 2, 3]),
        ),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
        regions.region_names["seaside_kingdom_lighthouse_top"]: True_(),
        regions.region_names["seaside_kingdom_ocean_trench_west_checkpoint"]: Has(tokens.swim),
    },
    regions.region_names["seaside_kingdom_rolling_canyon_checkpoint"]: {
        regions.region_names["seaside_kingdom_home_entrance_sea_world_moon_ex1a"]: Or(
            Has(tokens.swim),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_home_return_sea_world_moon_ex1b"]: False_(),
        regions.region_names["seaside_kingdom_sea_world_damage_ball_zone"]: True_(),
        regions.region_names["seaside_kingdom_what_the_waves_left_behind"]: Or(
            Has(tokens.swim),
            CanCapture(tokens.gushen),
            HasAll(tokens.seaside_kingdom_access, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
        ),
        regions.region_names["seaside_kingdom_back_canyon"]: Or(
            Has(tokens.swim),
            CanCapture(tokens.gushen),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.neutral_throw, tokens.side_flip, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            And(CanCapture(tokens.goomba), Has(tokens.hard_tricks)),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.hard_tricks),
            And(HasStoryProgress("seaside", [1, 2, 3]), HasAll(tokens.rocket_flower, tokens.intermediate_tricks)),
        ),
    },
    regions.region_names["seaside_kingdom_home_return_sea_world_moon_ex1b"]: {
        regions.region_names["seaside_kingdom_rolling_canyon_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: {
        regions.region_names["seaside_kingdom_home_entrance_sea_world_ex3a"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_home_return_sea_world_ex3b"]: False_(),
    },
    regions.region_names["seaside_kingdom_home_return_sea_world_ex3b"]: {
        regions.region_names["seaside_kingdom_ocean_trench_east_checkpoint"]: Has(tokens.swim),
    },
    regions.region_names["seaside_kingdom_lighthouse_top"]: {
        regions.region_names["seaside_kingdom_on_the_cliff_overlooking_the_beach"]: And(
            And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_what_the_waves_left_behind"]: And(
            And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_back_canyon"]: And(
            And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_glass_palace_checkpoint"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("seaside", [1, 2, 3])
        ),
        regions.region_names["seaside_kingdom_taking_notes_ocean_surface_dash"]: And(
            CanCapture(tokens.glydon), HasAll(tokens.notes, tokens.swim)
        ),
        regions.region_names["seaside_kingdom_shopping"]: And(CanCapture(tokens.glydon), Has(tokens.talk_to_npcs)),
    },
    regions.region_names["seaside_kingdom_on_the_cliff_overlooking_the_beach"]: {
        regions.region_names["seaside_kingdom_lighthouse_top"]: False_(),
    },
    regions.region_names["seaside_kingdom_stage_change_go"]: {
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_sea_world_moon_ex1a"]: {
        regions.region_names["seaside_kingdom_rolling_canyon_checkpoint"]: Has(tokens.swim),
    },
    regions.region_names["seaside_kingdom_underwater_moons"]: {
        regions.region_names["seaside_kingdom_sea_world2dlarge_zone"]: Has(tokens.enter_2d_pipes),
        regions.region_names["seaside_kingdom_sea_world_sphinx_quiz_zone"]: True_(),
        regions.region_names["seaside_kingdom_sea_world_utsubo_den_zone"]: True_(),
        regions.region_names["seaside_kingdom_sea_world_cove_cave_zone"]: True_(),
        regions.region_names["seaside_kingdom_sea_world2dsmall_zone"]: True_(),
        regions.region_names["seaside_kingdom_home_entrance_pukupuku_cave_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_narrow_vallet_alcove"]: {
        regions.region_names["seaside_kingdom_home_entrance_sea_world_ex1a"]: Or(
            CanCapture(tokens.gushen),
            HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.down_throw, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks
            ),
            HasAll(tokens.backflip, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.ground_pound_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_sea_world_ex1a"]: {
        regions.region_names["seaside_kingdom_narrow_vallet_alcove"]: True_(),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_seed_moons"]: {
        regions.region_names["seaside_kingdom_canyon_seed"]: Or(
            Has(tokens.swim),
            CanCapture(tokens.gushen),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.cheep_cheep), HasAll(tokens.down_throw, tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.spin_throw, tokens.vault, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.side_flip, tokens.spin_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.backflip, tokens.vault, tokens.spin_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ground_pound_jump, tokens.spin_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.spin, tokens.spin_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.triple_jump, tokens.vault, tokens.spin_throw, tokens.hard_tricks),
            HasAll(tokens.spin_throw, tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.spin_throw, tokens.backflip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.spin_throw, tokens.up_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.spin_throw, tokens.side_flip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.spin_throw, tokens.side_flip, tokens.wall_jump, tokens.hard_tricks),
            HasAll(
                tokens.neutral_throw, tokens.spin_throw, tokens.ground_pound_jump, tokens.wall_jump, tokens.hard_tricks
            ),
            HasAll(tokens.up_throw, tokens.spin_throw, tokens.ground_pound_jump, tokens.wall_jump, tokens.hard_tricks),
            HasAll(
                tokens.triple_jump,
                tokens.wall_jump,
                tokens.ledge_grab,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(
                tokens.triple_jump, tokens.up_throw, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks
            ),
            HasAll(tokens.spin_throw, tokens.triple_jump, tokens.wall_jump, tokens.hard_tricks),
            And(
                CanReachRegion(regions.region_names["seaside_kingdom_lighthouse_top"]),
                CanCapture(tokens.glydon),
                HasStoryProgress("seaside", [1, 2, 3]),
                Has(tokens.intermediate_tricks),
            ),
        ),
    },
    regions.region_names["seaside_kingdom_back_canyon"]: {
        regions.region_names["seaside_kingdom_lighthouse_top"]: False_(),
    },
    regions.region_names["seaside_kingdom_what_the_waves_left_behind"]: {
        regions.region_names["seaside_kingdom_glass_palace_checkpoint"]: False_(),
        regions.region_names["seaside_kingdom_lighthouse_top"]: False_(),
    },
    regions.region_names["seaside_kingdom_canyon_seed"]: {
        regions.region_names["seaside_kingdom_seed_moons"]: False_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_treasure_event_world_sea"]: {
        regions.region_names["seaside_kingdom_ocean_trench_west_checkpoint"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_sea_world_moon_ex2"]: {
        regions.region_names["seaside_kingdom_ocean_trench_west_checkpoint"]: Has(tokens.swim),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_home_entrance_pukupuku_cave_start"]: {
        regions.region_names["seaside_kingdom_underwater_moons"]: False_(),
        regions.region_names["seaside_kingdom_default_start"]: True_(),
    },
    regions.region_names["seaside_kingdom_taking_notes_ocean_surface_dash"]: {
        regions.region_names["seaside_kingdom_lighthouse_top"]: False_(),
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: False_(),
    },
    regions.region_names["seaside_kingdom_shopping"]: {
        regions.region_names["seaside_kingdom_beach_house_checkpoint"]: False_(),
        regions.region_names["seaside_kingdom_lighthouse_top"]: False_(),
    },
    regions.region_names["snow_kingdom_home_entrance_byugo_puzzle"]: {
        regions.region_names["snow_kingdom_default_start"]: And(
            CanCapture(tokens.ty_foo), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
    },
    regions.region_names["snow_kingdom_home_entrance_ex_ice_water"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["snow_kingdom_home_entrance_ex_ice_water_dash"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["snow_kingdom_default_start"]: {
        regions.region_names["snow_kingdom_home_entrance_moon_race"]: True_(),
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
        regions.region_names["snow_kingdom_snow_kingdom_clifftop_checkpoint"]: HasAll(
            tokens.ground_pound,
            tokens.crouch,
            tokens.roll_boost,
            tokens.roll,
            tokens.vault,
            tokens.dive,
            tokens.neutral_throw,
            tokens.intermediate_tricks,
        ),
        regions.region_names["snow_kingdom_corner_of_the_freezing_sea_checkpoint"]: True_(),
        regions.region_names["snow_kingdom_stage_change_go"]: And(
            And(CanCapture(tokens.ty_foo), Has(tokens.paintings)), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_home_entrance_ex_ice_water_dash"]: True_(),
        regions.region_names["snow_kingdom_home_entrance_ex_sky_bonus"]: True_(),
        regions.region_names["snow_kingdom_home_entrance_ex_ice_water"]: And(
            Has(tokens.scarecrows), HasStoryProgress("snow", [1, 2, 3])
        ),
    },
    regions.region_names["snow_kingdom_home_entrance_ex_rail_col2"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["snow_kingdom_home_entrance_ex_sky_bonus"]: {
        regions.region_names["snow_kingdom_default_start"]: And(
            HasAll(tokens.climb, tokens.grab), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
    },
    regions.region_names["snow_kingdom_moon_rock"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["shiveria_town_snow_world_town_zone"]: {
        regions.region_names["shiveria_town_substage_near_side_snow_ugent"]: True_(),
        regions.region_names["shiveria_town_home_entrance_shop_door"]: True_(),
        regions.region_names["shiveria_town_home_entrance_snow_costume_ex"]: Or(
            Has(tokens.climb),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.down_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.spin_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.hard_tricks),
        ),
        regions.region_names["shiveria_town_race_room_access"]: Or(
            CanCapture(tokens.ty_foo),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["shiveria_town_snow_world_byugo_zone"]: {
        regions.region_names["shiveria_town_snow_world_town_zone"]: True_(),
    },
    regions.region_names["shiveria_town_snow_world_gabuzou_zone"]: {
        regions.region_names["shiveria_town_snow_world_town_zone"]: True_(),
    },
    regions.region_names["shiveria_town_snow_world_icicle_zone"]: {
        regions.region_names["shiveria_town_snow_world_town_zone"]: True_(),
    },
    regions.region_names["shiveria_town_snow_world_balcony_zone"]: {
        regions.region_names["shiveria_town_snow_world_town_zone"]: True_(),
    },
    regions.region_names["shiveria_town_home_entrance_snow_costume_ex"]: {
        regions.region_names["shiveria_town_snow_world_town_zone"]: True_(),
    },
    regions.region_names["class_s_lobby_substage_far_side_moon_race"]: {
        regions.region_names["class_s_lobby_substage_near_side_moon_race"]: True_(),
    },
    regions.region_names["cold_room_substage_near_side_snow_costume_ex"]: {
        regions.region_names["cold_room_substage_far_side_snow_costume_ex"]: True_(),
    },
    regions.region_names["crazy_cap_store_substage_near_side_shop_door"]: {
        regions.region_names["crazy_cap_store_substage_far_side_shop_door"]: True_(),
    },
    regions.region_names["koopa_walking_in_snow_substage_near_side_figure_walker"]: {
        regions.region_names["koopa_walking_in_snow_substage_far_side_figure_walker"]: True_(),
    },
    regions.region_names["shiveria_town_substage_far_side_snow_ugexit"]: {
        regions.region_names["shiveria_town_substage_near_side_snow_ugent"]: True_(),
    },
    regions.region_names["spinning_above_the_clouds_substage_near_side_ex_sky_bonus"]: {
        regions.region_names["spinning_above_the_clouds_substage_far_side_ex_sky_bonus"]: True_(),
    },
    regions.region_names["ty_foo_sliding_puzzle_substage_far_side_byugo_puzzle"]: {
        regions.region_names["ty_foo_sliding_puzzle_substage_near_side_byugo_puzzle"]: True_(),
    },
    regions.region_names["snow_kingdom_stage_change_go"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["snow_kingdom_snow_kingdom_clifftop_checkpoint"]: {
        regions.region_names["snow_kingdom_default_start"]: True_(),
    },
    regions.region_names["dashing_over_cold_water_substage_near_side_ex_ice_water_dash"]: {
        regions.region_names["dashing_over_cold_water_substage_far_side_ex_ice_water_dash_exit"]: Or(
            HasAll(tokens.swim, tokens.rocket_flower),
            HasAll(tokens.neutral_throw, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.down_throw, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.dive, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.backflip, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.ledge_grab, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.rocket_flower, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["freezing_water_substage_near_side_ex_ice_water"]: {
        regions.region_names["freezing_water_substage_far_side_ex_ice_water_exit"]: Or(
            Has(tokens.swim),
            HasAll(tokens.ground_pound, tokens.roll_boost, tokens.triple_jump, tokens.dive, tokens.hard_tricks),
        ),
    },
    regions.region_names["wintery_flower_road_substage_near_side_ex_rail_col2"]: {
        regions.region_names["wintery_flower_road_substage_far_side_ex_rail_col2_exit"]: Or(
            Has(tokens.scarecrows),
            And(
                CanCapture(tokens.banzai_bill),
                HasAll(
                    tokens.neutral_throw,
                    tokens.vault,
                    tokens.dive,
                    tokens.wall_jump,
                    tokens.cap_return_jump,
                    tokens.jump,
                    tokens.hard_tricks,
                ),
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.cap_return_jump,
                tokens.ground_pound,
                tokens.jump,
                tokens.roll,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["wintery_flower_road_looking_back_on_flower_road"]: Or(
            Has(tokens.scarecrows),
            And(
                CanCapture(tokens.banzai_bill),
                HasAll(
                    tokens.neutral_throw,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.cap_return_jump,
                    tokens.jump,
                    tokens.hard_tricks,
                ),
            ),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.wall_jump,
                tokens.dive,
                tokens.cap_return_jump,
                tokens.ground_pound,
                tokens.roll,
                tokens.jump,
                tokens.hard_tricks,
            ),
        ),
    },
    regions.region_names["wintery_flower_road_substage_far_side_ex_rail_col2_exit"]: {
        regions.region_names["wintery_flower_road_substage_near_side_ex_rail_col2"]: CanCapture(tokens.banzai_bill),
        regions.region_names["wintery_flower_road_looking_back_on_flower_road"]: HasAll(
            tokens.neutral_throw, tokens.jump, tokens.vault, tokens.dive, tokens.cap_return_jump, tokens.hard_tricks
        ),
    },
    regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: {
        regions.region_names["snow_kingdom_moon_rock"]: True_(),
        regions.region_names["snow_kingdom_home_entrance_byugo_puzzle"]: And(
            CanCapture(tokens.ty_foo), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_home_entrance_ex_ice_water_dash"]: True_(),
        regions.region_names["snow_kingdom_home_return_ex_ice_water_dash_exit"]: False_(),
        regions.region_names["snow_kingdom_home_entrance_ex_ice_water"]: And(
            Has(tokens.scarecrows), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_home_return_ex_ice_water_exit"]: False_(),
        regions.region_names["snow_kingdom_home_entrance_ex_sky_bonus"]: And(
            HasAll(tokens.climb, tokens.grab), HasStoryProgress("snow", [1, 2, 3])
        ),
        regions.region_names["snow_kingdom_home_entrance_ex_rail_col2"]: True_(),
        regions.region_names["snow_kingdom_home_return_ex_rail_col2_exit"]: False_(),
        regions.region_names["snow_kingdom_home_entrance_figure_walker"]: True_(),
        regions.region_names["snow_kingdom_home_entrance_moon_race"]: True_(),
        regions.region_names["snow_kingdom_stage_change_go"]: And(
            Or(
                And(CanCapture(tokens.ty_foo), Has(tokens.paintings)),
                HasAll(
                    tokens.backflip,
                    tokens.neutral_throw,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.side_flip,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.vault,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.paintings,
                    tokens.cap_return_jump,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.triple_jump,
                    tokens.vault,
                    tokens.dive,
                    tokens.wall_jump,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.down_throw,
                    tokens.backflip,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.down_throw,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.down_throw,
                    tokens.side_flip,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.down_throw,
                    tokens.triple_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.up_throw,
                    tokens.backflip,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.up_throw,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.up_throw,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.side_flip,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
                HasAll(
                    tokens.up_throw,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.dive,
                    tokens.triple_jump,
                    tokens.paintings,
                    tokens.hard_tricks,
                ),
            ),
            HasStoryProgress("snow", [1, 2, 3]),
        ),
        regions.region_names["snow_kingdom_home_entrance_snow_ugent"]: True_(),
        regions.region_names["snow_kingdom_swim_moons_snow_kingdom"]: Or(
            Has(tokens.swim), And(CanCapture(tokens.cheep_cheep_snow_kingdom), Has(tokens.intermediate_tricks))
        ),
        regions.region_names["snow_kingdom_snow_kfr"]: Has(tokens.talk_to_npcs),
    },
    regions.region_names["snow_kingdom_home_return_ex_ice_water_dash_exit"]: {
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
    },
    regions.region_names["snow_kingdom_home_return_ex_ice_water_exit"]: {
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
    },
    regions.region_names["snow_kingdom_home_return_ex_rail_col2_exit"]: {
        regions.region_names["snow_kingdom_above_the_ice_well_checkpoint"]: True_(),
    },
    regions.region_names["snow_kingdom_stage_change_come"]: {
        regions.region_names["snow_kingdom_snow_kingdom_clifftop_checkpoint"]: Has(tokens.paintings),
    },
    regions.region_names["class_a_lobby_substage_near_side_race_entrance"]: {
        regions.region_names["class_a_lobby_race_room"]: True_(),
    },
    regions.region_names["class_a_lobby_race_room"]: {
        regions.region_names["class_a_lobby_substage_near_side_race_entrance"]: False_(),
        regions.region_names["class_a_lobby_substage_far_side_race_track_exit"]: True_(),
        regions.region_names["class_a_lobby_dark_side_snow_hint_art"]: Or(
            HasAll(tokens.wall_jump, tokens.dive, tokens.ground_pound),
            HasAll(tokens.triple_jump, tokens.ground_pound),
            HasAll(tokens.ground_pound_jump, tokens.ground_pound),
            HasAll(tokens.backflip, tokens.ground_pound),
            HasAll(tokens.side_flip, tokens.ground_pound),
            HasAll(tokens.ground_pound, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.ground_pound, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ground_pound, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound, tokens.dive, tokens.intermediate_tricks),
            And(CanCapture(tokens.shiverian_racer), HasAll(tokens.ground_pound, tokens.hard_tricks)),
        ),
    },
    regions.region_names["snow_world_lobby001stage_default_start"]: {
        regions.region_names["snow_world_lobby001stage_lobby_win"]: True_(),
    },
    regions.region_names["shiveria_town_race_room_access"]: {
        regions.region_names["shiveria_town_home_entrance_race_entrance"]: True_(),
    },
    regions.region_names["dashing_over_cold_water_substage_far_side_ex_ice_water_dash_exit"]: {
        regions.region_names["dashing_over_cold_water_substage_near_side_ex_ice_water_dash"]: Or(
            HasAll(tokens.swim, tokens.rocket_flower),
            HasAll(tokens.rocket_flower, tokens.intermediate_tricks),
            HasAll(tokens.swim, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["freezing_water_substage_far_side_ex_ice_water_exit"]: {
        regions.region_names["freezing_water_substage_near_side_ex_ice_water"]: Or(
            HasAll(tokens.swim, tokens.jump),
            HasAll(tokens.long_jump, tokens.ground_pound_jump, tokens.jump, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.roll_boost, tokens.ground_pound, tokens.dive, tokens.jump, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.backflip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.ground_pound_jump, tokens.dive, tokens.jump, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.side_flip, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.wall_jump, tokens.spin, tokens.dive, tokens.hard_tricks),
            And(HasHP(2), HasAll(tokens.swim, tokens.dive, tokens.hard_tricks)),
        ),
    },
    regions.region_names["wintery_flower_road_looking_back_on_flower_road"]: {
        regions.region_names["wintery_flower_road_substage_near_side_ex_rail_col2"]: False_(),
        regions.region_names["wintery_flower_road_substage_far_side_ex_rail_col2_exit"]: False_(),
    },
    regions.region_names["shiveria_town_substage_near_side_snow_ugent"]: {
        regions.region_names["shiveria_town_snow_peach"]: True_(),
    },
    regions.region_names["crowded_elevator_substage_near_side_ex_tankuro"]: {
        regions.region_names["crowded_elevator_substage_far_side_ex_tankuro_exit"]: Has(tokens.p_switches),
        regions.region_names["crowded_elevator_crowded_elevator_purples_1_3"]: Or(
            HasAll(tokens.jump, tokens.p_switches, tokens.intermediate_tricks),
            And(CanCapture(tokens.sherm), Has(tokens.p_switches)),
            And(CanCapture(tokens.fire_bro), Has(tokens.p_switches)),
        ),
    },
    regions.region_names["crowded_elevator_substage_far_side_ex_tankuro_exit"]: {
        regions.region_names["crowded_elevator_substage_near_side_ex_tankuro"]: False_(),
    },
    regions.region_names["flooding_pipeway_substage_near_side_ex_water"]: {
        regions.region_names["flooding_pipeway_substage_far_side_ex_water_exit"]: Or(
            Has(tokens.swim),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.vault, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["flooding_pipeway_flooding_pipeway_purples_1_3"]: Or(
            Has(tokens.swim),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.wall_jump, tokens.hard_tricks),
        ),
    },
    regions.region_names["flower_road_substage_near_side_ex_rail_collision"]: {
        regions.region_names["flower_road_substage_far_side_ex_rail_collision_exit"]: Or(
            HasAll(tokens.p_switches, tokens.wall_jump),
            And(CanCapture(tokens.goomba), HasAll(tokens.p_switches, tokens.ledge_grab, tokens.intermediate_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.p_switches, tokens.dive, tokens.intermediate_tricks)),
        ),
        regions.region_names["flower_road_flower_road_purples_1_3"]: Or(
            HasAll(tokens.p_switches, tokens.wall_jump),
            And(CanCapture(tokens.goomba), HasAll(tokens.p_switches, tokens.ledge_grab, tokens.intermediate_tricks)),
            And(CanCapture(tokens.goomba), HasAll(tokens.p_switches, tokens.dive, tokens.intermediate_tricks)),
        ),
    },
    regions.region_names["flower_road_substage_far_side_ex_rail_collision_exit"]: {
        regions.region_names["flower_road_substage_near_side_ex_rail_collision"]: Or(
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.neutral_throw,
                tokens.dive,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.triple_jump, tokens.dive, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
        regions.region_names["flower_road_flower_road_purples_1_3"]: Or(
            HasAll(
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.neutral_throw,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["invisible_road_substage_near_side_poison_ex"]: {
        regions.region_names["invisible_road_substage_far_side_poison_ex_exit"]: True_(),
    },
    regions.region_names["spinning_platforms_treasure_vault_substage_near_side_bonus"]: {
        regions.region_names["spinning_platforms_treasure_vault_substage_far_side_bonus2"]: True_(),
    },
    regions.region_names["spinning_platforms_treasure_vault_substage_far_side_bonus2"]: {
        regions.region_names["spinning_platforms_treasure_vault_substage_near_side_bonus"]: False_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai001"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai002"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai001v"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai003"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai003v"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_substage_near_side_jyukai004"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["shards_in_the_fog_substage_near_side_ex_mist"]: {
        regions.region_names["shards_in_the_fog_free_space"]: True_(),
    },
    regions.region_names["shards_in_the_fog_free_space"]: {
        regions.region_names["shards_in_the_fog_substage_near_side_ex_mist"]: CanCapture(tokens.mini_rocket),
        regions.region_names["shards_in_the_fog_substage_far_side_ex_mist"]: CanCapture(tokens.mini_rocket),
    },
    regions.region_names["wooded_kingdom_default_start"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: Or(
            And(HasStoryProgress("wooded", [0]), Has(tokens.talk_to_npcs)),
            And(HasStoryProgress("wooded", [1, 2, 3, 4]), Has(tokens.wooded_kingdom_access)),
            And(CanCapture(tokens.fire_bro), HasStoryProgress("wooded", [0])),
            And(CanCapture(tokens.uproot), HasStoryProgress("wooded", [0])),
        ),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_moon_rock"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_383940"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_414243"]: Or(
            HasAll(tokens.neutral_throw, tokens.intermediate_tricks),
            CanCapture(tokens.uproot),
            Has(tokens.up_throw),
            HasAll(tokens.spin_throw, tokens.wall_jump, tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin_throw, tokens.wall_jump, tokens.backflip, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin_throw, tokens.wall_jump, tokens.side_flip, tokens.dive, tokens.intermediate_tricks),
            HasAll(
                tokens.ground_pound_jump, tokens.wall_jump, tokens.dive, tokens.spin_throw, tokens.intermediate_tricks
            ),
            HasAll(tokens.wall_jump, tokens.spin, tokens.dive, tokens.spin_throw, tokens.intermediate_tricks),
            HasAll(tokens.wooded_kingdom_access, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_515253"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_686970"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_717273"]: True_(),
        regions.region_names["wooded_kingdom_home_entrance_jyukai003"]: True_(),
        regions.region_names["wooded_kingdom_taking_notes_stretching"]: Or(
            CanCapture(tokens.uproot),
            CanCapture(tokens.fire_bro),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.triple_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
        ),
        regions.region_names["wooded_kingdom_painting_access"]: False_(),
    },
    regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: {
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: Or(
            CanCapture(tokens.uproot),
            HasAll(tokens.triple_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.long_jump, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
            And(CanCapture(tokens.fire_bro), HasAll(tokens.dive, tokens.intermediate_tricks)),
            HasAll(tokens.wall_jump, tokens.cap_return_jump, tokens.hard_tricks),
            And(
                CanCapture(tokens.fire_bro), HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks)
            ),
            And(CanCapture(tokens.fire_bro), HasAll(tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.fire_bro), HasAll(tokens.wall_jump, tokens.down_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.fire_bro), Has(tokens.hard_tricks)),
            HasAll(tokens.down_throw, tokens.vault, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: Or(
            And(CanCapture(tokens.sherm), HasStoryProgress("wooded", [1, 2, 3, 4]), HasAll(tokens.climb, tokens.grab)),
            And(
                HasStoryProgress("wooded", [1, 2, 3, 4]), HasAll(tokens.climb, tokens.grab, tokens.intermediate_tricks)
            ),
            And(
                HasStoryProgress("wooded", [1, 2, 3, 4]),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            HasAll(tokens.neutral_throw, tokens.dive, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_nut_round_the_corner"]: Or(
            CanCapture(tokens.uproot),
            And(CanCapture(tokens.fire_bro), Has(tokens.intermediate_tricks)),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.wooded_kingdom_access, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_climb_the_cliff_to_get_the_nut"]: Or(
            CanCapture(tokens.uproot),
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            CanCapture(tokens.fire_bro),
            HasAll(tokens.wooded_kingdom_access, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_the_nut_in_the_red_maze"]: CanCapture(tokens.uproot),
        regions.region_names["wooded_kingdom_the_nut_in_the_robot_storeroom"]: And(
            Or(
                HasAll(tokens.backflip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.dive, tokens.wall_jump, tokens.intermediate_tricks),
                HasAll(tokens.side_flip, tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.dive, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.ground_pound_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.spin, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.triple_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.dive, tokens.triple_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.backflip, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.ground_pound_jump, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.side_flip, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.spin, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.spin, tokens.down_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.triple_jump, tokens.intermediate_tricks),
                Has(tokens.climb),
                CanCapture(tokens.uproot),
                CanCapture(tokens.fire_bro),
                HasAll(tokens.wooded_kingdom_access, tokens.hard_tricks),
            ),
            HasStoryProgress("wooded", [4]),
        ),
        regions.region_names["wooded_kingdom_moon_shards_in_the_forest"]: And(
            CanCapture(tokens.uproot), HasStoryProgress("wooded", [4])
        ),
        regions.region_names["wooded_kingdom_home_entrance_ex_water"]: Has(tokens.swim),
        regions.region_names["wooded_kingdom_home_return_ex_water_exit"]: False_(),
        regions.region_names["wooded_kingdom_home_entrance_killer_road"]: True_(),
        regions.region_names["wooded_kingdom_home_entrance_jyukai003v"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_456"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_1011"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_16171819"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_30313233"]: CanCapture(tokens.uproot),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_44454647"]: Or(
            CanCapture(tokens.uproot),
            Has(tokens.up_throw),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.neutral_throw, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.wall_jump, tokens.intermediate_tricks),
            And(CanCapture(tokens.fire_bro), HasAll(tokens.neutral_throw, tokens.intermediate_tricks)),
            And(CanCapture(tokens.fire_bro), HasAll(tokens.wall_jump, tokens.intermediate_tricks)),
            And(CanCapture(tokens.sherm), HasStoryProgress("wooded", [1])),
        ),
        regions.region_names["wooded_kingdom_high_up_on_a_rock_wall"]: Or(
            CanCapture(tokens.uproot),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.backflip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.ground_pound_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.spin, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.triple_jump, tokens.hard_tricks),
        ),
        regions.region_names["wooded_kingdom_charging_station_area"]: False_(),
        regions.region_names["wooded_kingdom_painting_access"]: False_(),
    },
    regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: {
        regions.region_names["wooded_kingdom_sky_garden_tower_checkpoint"]: Or(
            Has(tokens.p_switches),
            HasAll(
                tokens.neutral_throw,
                tokens.ground_pound,
                tokens.roll_boost,
                tokens.vault,
                tokens.dive,
                tokens.intermediate_tricks,
            ),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.vault, tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["wooded_kingdom_the_nut_in_the_red_maze"]: HasAll(
            tokens.wall_jump, tokens.intermediate_tricks
        ),
        regions.region_names["wooded_kingdom_moon_shards_in_the_forest"]: And(
            Or(
                HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.vault, tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [4]),
        ),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_home_entrance_tower001"]: False_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_123"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_26272829"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_30313233"]: And(
            Or(
                HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.up_throw, tokens.wall_jump, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.dive, tokens.spin_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [0, 2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_home_entrance_bonus"]: And(
            Or(
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
                HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
                HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
                And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.hard_tricks)),
            ),
            HasStoryProgress("wooded", [1, 2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: And(
            Or(
                CanCapture(tokens.sherm),
                HasAll(tokens.vault, tokens.wall_jump, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
                HasAll(
                    tokens.backflip,
                    tokens.neutral_throw,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.neutral_throw,
                    tokens.side_flip,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.intermediate_tricks,
                ),
                HasAll(tokens.neutral_throw, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.hard_tricks),
                HasAll(
                    tokens.neutral_throw,
                    tokens.spin,
                    tokens.ground_pound_jump,
                    tokens.vault,
                    tokens.wall_jump,
                    tokens.ledge_grab,
                    tokens.hard_tricks,
                ),
                And(CanCapture(tokens.goomba), HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks)),
                And(
                    CanCapture(tokens.goomba),
                    HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
                ),
            ),
            HasStoryProgress("wooded", [1, 2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_nut_round_the_corner"]: True_(),
        regions.region_names["wooded_kingdom_inside_a_rock_in_the_forest"]: And(
            CanCapture(tokens.sherm), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_lost_in_the_tall_trees"]: And(
            CanCapture(tokens.sherm), HasStoryProgress("wooded", [4])
        ),
        regions.region_names["wooded_kingdom_the_nut_in_the_robot_storeroom"]: And(
            Or(
                And(CanCapture(tokens.goomba), Has(tokens.intermediate_tricks)),
                HasAll(tokens.wooded_kingdom_access, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [4]),
        ),
        regions.region_names["wooded_kingdom_painting_access"]: Or(
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.backflip, tokens.ledge_grab, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.spin, tokens.ledge_grab, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.ground_pound_jump, tokens.ledge_grab, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.wall_jump, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.triple_jump, tokens.ledge_grab, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.backflip, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.ground_pound_jump, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.side_flip, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            And(
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.triple_jump, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            ),
            HasAll(
                tokens.triple_jump,
                tokens.vault,
                tokens.dive,
                tokens.wall_jump,
                tokens.neutral_throw,
                tokens.hard_tricks,
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("wooded", [1, 2, 3, 4]),
                HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("wooded", [1, 2, 3, 4]),
                HasAll(tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            ),
            HasAll(tokens.spin, tokens.scarecrows, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.spin, tokens.scarecrows, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.scarecrows, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(tokens.backflip, tokens.wall_jump, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(tokens.ground_pound_jump, tokens.wall_jump, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(tokens.side_flip, tokens.wall_jump, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.scarecrows, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw, tokens.backflip, tokens.vault, tokens.wall_jump, tokens.dive, tokens.hard_tricks
            ),
            HasAll(
                tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.dive, tokens.side_flip, tokens.hard_tricks
            ),
            And(
                CanCapture(tokens.goomba),
                HasStoryProgress("wooded", [1, 2, 3, 4]),
                HasAll(tokens.wall_jump, tokens.neutral_throw, tokens.cap_return_jump, tokens.hard_tricks),
            ),
        ),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_414243"]: And(
            CanCapture(tokens.sherm), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_44454647"]: And(
            And(CanCapture(tokens.sherm), Has(tokens.intermediate_tricks)), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_over_the_cliffs_edge_area"]: Or(
            Has(tokens.swing), HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks)
        ),
        regions.region_names["wooded_kingdom_wooded_kfr"]: Has(tokens.talk_to_npcs),
        regions.region_names["wooded_kingdom_charging_station_area"]: True_(),
        regions.region_names["wooded_kingdom_thanks_for_the_charge"]: Has(tokens.ground_pound),
    },
    regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_the_nut_that_grew_on_the_tall_fence"]: True_(),
        regions.region_names["wooded_kingdom_painting_access"]: True_(),
        regions.region_names["wooded_kingdom_stage_change_come"]: Has(tokens.paintings),
        regions.region_names["wooded_kingdom_default_start"]: True_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: And(
            HasAll(tokens.vault, tokens.dive, tokens.neutral_throw), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_looking_down_on_goombas"]: And(
            Or(
                HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
                HasAll(
                    tokens.neutral_throw,
                    tokens.triple_jump,
                    tokens.ground_pound,
                    tokens.roll,
                    tokens.cap_return_jump,
                    tokens.dive,
                    tokens.hard_tricks,
                ),
            ),
            HasStoryProgress("wooded", [1, 2, 3, 4]),
        ),
    },
    regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: {
        regions.region_names["wooded_kingdom_secret_flower_field_entrance_checkpoint"]: And(
            CanCapture(tokens.sherm), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: And(
            Has(tokens.p_switches), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_climb_the_cliff_to_get_the_nut"]: True_(),
        regions.region_names["wooded_kingdom_the_nut_that_grew_on_the_tall_fence"]: Or(
            CanCapture(tokens.uproot), HasAll(tokens.wooded_kingdom_access, tokens.intermediate_tricks)
        ),
        regions.region_names["wooded_kingdom_inside_a_rock_in_the_forest"]: And(
            And(CanCapture(tokens.coin_coffer), Has(tokens.wallet)), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_painting_access"]: Or(
            And(HasStoryProgress("wooded", [4]), HasAll(tokens.scarecrows, tokens.swing)),
            HasAll(tokens.wooded_kingdom_access, tokens.intermediate_tricks),
            And(CanCapture(tokens.uproot), HasStoryProgress("wooded", [1, 2, 3, 4])),
        ),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_12131415"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_30313233"]: And(
            Or(
                HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.up_throw, tokens.intermediate_tricks),
                HasAll(tokens.wall_jump, tokens.dive, tokens.spin_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [1, 2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_taking_notes_stretching"]: Or(
            And(CanCapture(tokens.goomba), Has(tokens.hard_tricks)),
            And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)),
        ),
        regions.region_names["wooded_kingdom_high_up_on_a_rock_wall"]: True_(),
        regions.region_names["wooded_kingdom_above_the_iron_mountain_path"]: Or(
            Has(tokens.p_switches),
            HasAll(tokens.neutral_throw, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
        ),
        regions.region_names["wooded_kingdom_thanks_for_the_charge"]: And(
            CanCapture(tokens.uproot), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_looking_down_on_goombas"]: Or(
            HasAll(tokens.vault, tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.rocket_flower, tokens.hard_tricks),
            And(CanCapture(tokens.uproot), HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.hard_tricks)),
            HasAll(
                tokens.neutral_throw,
                tokens.triple_jump,
                tokens.ground_pound,
                tokens.cap_return_jump,
                tokens.dive,
                tokens.roll,
                tokens.hard_tricks,
            ),
        ),
        regions.region_names["wooded_kingdom_home_entrance_bonus"]: Or(
            And(HasStoryProgress("wooded", [1, 2, 3, 4]), HasAll(tokens.enter_2d_pipes, tokens.jump)),
            And(HasStoryProgress("wooded", [3, 4]), HasAll(tokens.climb, tokens.jump)),
        ),
    },
    regions.region_names["wooded_kingdom_summit_path_checkpoint"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: And(
            Has(tokens.rocket_flower), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_captain_toad"]: And(
            Or(
                HasAll(tokens.rocket_flower, tokens.hard_tricks),
                HasAll(tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_home_entrance_ex_rail_collision"]: True_(),
        regions.region_names["wooded_kingdom_home_return_ex_rail_collision_exit"]: False_(),
        regions.region_names["wooded_kingdom_home_return_ex_tankuro_exit"]: And(
            Has(tokens.rocket_flower), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_over_the_cliffs_edge_area"]: True_(),
        regions.region_names["wooded_kingdom_painting_access"]: HasAll(
            tokens.neutral_throw,
            tokens.ground_pound,
            tokens.roll_boost,
            tokens.vault,
            tokens.dive,
            tokens.wall_jump,
            tokens.hard_tricks,
        ),
    },
    regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_captain_toad"]: And(
            Or(
                CanCapture(tokens.glydon),
                HasAll(tokens.roll_boost, tokens.intermediate_tricks),
                HasAll(tokens.long_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
                HasAll(tokens.triple_jump, tokens.vault, tokens.dive, tokens.neutral_throw, tokens.intermediate_tricks),
            ),
            HasStoryProgress("wooded", [2, 3, 4]),
        ),
        regions.region_names["wooded_kingdom_lost_in_the_tall_trees"]: And(
            Or(
                And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)),
                HasAll(
                    tokens.ground_pound,
                    tokens.roll_boost,
                    tokens.vault,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.wall_jump,
                    tokens.intermediate_tricks,
                ),
                HasAll(
                    tokens.ground_pound,
                    tokens.roll_boost,
                    tokens.vault,
                    tokens.dive,
                    tokens.neutral_throw,
                    tokens.climb,
                    tokens.intermediate_tricks,
                ),
                HasAll(tokens.ground_pound, tokens.hard_tricks),
            ),
            HasStoryProgress("wooded", [4]),
        ),
        regions.region_names["wooded_kingdom_invader_in_the_sky_garden"]: And(
            And(CanCapture(tokens.glydon), Has(tokens.intermediate_tricks)), HasStoryProgress("wooded", [4])
        ),
        regions.region_names["wooded_kingdom_home_entrance_excloud"]: And(
            HasAll(tokens.climb, tokens.grab), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_sky_garden_tower_checkpoint"]: Or(
            Has(tokens.dive), HasAll(tokens.wooded_kingdom_access, tokens.intermediate_tricks)
        ),
        regions.region_names["wooded_kingdom_home_entrance_bonus"]: True_(),
        regions.region_names["wooded_kingdom_climb_the_cliff_to_get_the_nut"]: True_(),
        regions.region_names["wooded_kingdom_above_the_iron_mountain_path"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_looking_down_on_goombas"]: And(
            CanCapture(tokens.glydon), HasStoryProgress("wooded", [2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_home_entrance_ex_rail_collision"]: True_(),
        regions.region_names["wooded_kingdom_home_entrance_ex_tankuro"]: True_(),
        regions.region_names["wooded_kingdom_wooded_peach"]: True_(),
    },
    regions.region_names["wooded_kingdom_sky_garden_tower_checkpoint"]: {
        regions.region_names["wooded_kingdom_invader_in_the_sky_garden"]: And(
            Or(CanCapture(tokens.goomba), CanCapture(tokens.uproot), HasAll(tokens.grab, tokens.hard_tricks)),
            HasStoryProgress("wooded", [4]),
        ),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_home_entrance_tower002"]: True_(),
        regions.region_names["wooded_kingdom_wooded_kingdom_purples_12131415"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_return_ex_rail_collision_exit"]: {
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_return_ex_tankuro_exit"]: {
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_return_ex_water_exit"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_excloud"]: {
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_secret_flower_field_entrance_checkpoint"]: {
        regions.region_names["wooded_kingdom_home_entrance_poison_ex"]: True_(),
        regions.region_names["wooded_kingdom_home_return_poison_ex_exit"]: False_(),
        regions.region_names["secret_flower_field_flower_field"]: True_(),
        regions.region_names["wooded_kingdom_secret_flower_field_roof"]: Or(
            Has(tokens.enter_2d_pipes),
            And(HasStoryProgress("wooded", [3, 4]), Has(tokens.climb)),
            And(
                CanCapture(tokens.coin_coffer),
                HasStoryProgress("wooded", [2, 3, 4]),
                HasAll(tokens.dive, tokens.grab, tokens.hard_tricks),
            ),
        ),
    },
    regions.region_names["wooded_kingdom_home_return_poison_ex_exit"]: {
        regions.region_names["wooded_kingdom_secret_flower_field_entrance_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_painting_access"]: {
        regions.region_names["wooded_kingdom_stage_change_go"]: Has(tokens.paintings),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_default_start"]: True_(),
        regions.region_names["wooded_kingdom_looking_down_on_goombas"]: HasAll(
            tokens.neutral_throw,
            tokens.ground_pound,
            tokens.roll,
            tokens.vault,
            tokens.dive,
            tokens.cap_return_jump,
            tokens.hard_tricks,
        ),
    },
    regions.region_names["deep_woods_free_space"]: {
        regions.region_names["deep_woods_substage_near_side_jyukai001"]: HasAll(tokens.climb, tokens.grab),
        regions.region_names["deep_woods_substage_near_side_jyukai002"]: Has(tokens.climb),
        regions.region_names["deep_woods_substage_near_side_jyukai001v"]: Has(tokens.climb),
        regions.region_names["deep_woods_substage_near_side_jyukai003"]: HasAll(tokens.climb, tokens.grab),
        regions.region_names["deep_woods_substage_near_side_jyukai003v"]: Has(tokens.climb),
        regions.region_names["deep_woods_substage_near_side_jyukai004"]: Has(tokens.climb),
        regions.region_names["deep_woods_home_entrance_explorer_bonus"]: True_(),
        regions.region_names["deep_woods_home_entrance_treasure_tree"]: True_(),
        regions.region_names["deep_woods_substage_far_side_jyukai003"]: HasAll(tokens.climb, tokens.grab),
        regions.region_names["deep_woods_deep_woods_purples_7_9"]: CanCapture(tokens.boulder),
        regions.region_names["deep_woods_deep_woods_purples_1_6"]: True_(),
        regions.region_names["deep_woods_substage_far_side_jyukai001"]: HasAll(tokens.climb, tokens.grab),
    },
    regions.region_names["secret_flower_field_flower_field"]: {
        regions.region_names["secret_flower_field_default_start"]: True_(),
    },
    regions.region_names["wooded_kingdom_forest_world2droad_zone"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_jyukai001"]: {
        regions.region_names["wooded_kingdom_default_start"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_boss001"]: {
        regions.region_names["wooded_kingdom_secret_flower_field_entrance_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_tower001"]: {
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_forest_world_timer_athletic001zone"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: And(
            CanCapture(tokens.sherm), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
    },
    regions.region_names["sky_garden_tower_substage_far_side_tower002"]: {
        regions.region_names["sky_garden_tower_substage_near_side_tower002"]: Or(
            Has(tokens.p_switches),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.vault, tokens.wall_jump, tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.ledge_grab, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.spin, tokens.wall_jump, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.wall_jump, tokens.dive, tokens.backflip, tokens.hard_tricks),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.hard_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.hard_tricks)),
        ),
        regions.region_names["sky_garden_tower_tower_nut"]: True_(),
    },
    regions.region_names["wooded_kingdom_forest_world_athletic_zone"]: {
        regions.region_names["wooded_kingdom_forest_world_timer_athletic001zone"]: True_(),
    },
    regions.region_names["breakdown_road_substage_near_side_killer_road"]: {
        regions.region_names["breakdown_road_substage_far_side_killer_road"]: True_(),
    },
    regions.region_names["costume_room_substage_near_side_explorer_bonus"]: {
        regions.region_names["costume_room_default_start"]: True_(),
    },
    regions.region_names["deep_woods_home_entrance_explorer_bonus"]: {
        regions.region_names["deep_woods_home_return_explorer_bonus"]: True_(),
    },
    regions.region_names["deep_woods_substage_far_side_jyukai003"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["deep_woods_treasure_vault_substage_near_side_treasure_tree"]: {
        regions.region_names["deep_woods_treasure_vault_substage_far_side_treasure_tree"]: True_(),
    },
    regions.region_names["secret_flower_field_substage_near_side_boss001"]: {
        regions.region_names["secret_flower_field_substage_far_side_boss001"]: True_(),
        regions.region_names["secret_flower_field_flower_field"]: True_(),
    },
    regions.region_names["shards_in_the_fog_substage_far_side_ex_mist"]: {
        regions.region_names["shards_in_the_fog_free_space"]: True_(),
    },
    regions.region_names["walking_on_clouds_substage_near_side_excloud"]: {
        regions.region_names["walking_on_clouds_substage_far_side_excloud"]: True_(),
        regions.region_names["walking_on_clouds_walking_on_clouds_purples_1_3"]: Or(
            CanCapture(tokens.uproot),
            HasAll(tokens.neutral_throw, tokens.hard_tricks),
            HasAll(tokens.up_throw, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["wooded_kingdom_the_nut_that_grew_on_the_tall_fence"]: {
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_charging_station_area"]: False_(),
    },
    regions.region_names["wooded_kingdom_captain_toad"]: {
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_invader_in_the_sky_garden"]: {
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_sky_garden_tower_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_lost_in_the_tall_trees"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_inside_a_rock_in_the_forest"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_killer_road"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_nut_round_the_corner"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_over_the_cliffs_edge_area"]: False_(),
        regions.region_names["wooded_kingdom_charging_station_area"]: False_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_ex_rail_collision"]: {
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_climb_the_cliff_to_get_the_nut"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_bonus"]: {
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_over_the_cliffs_edge_area"]: HasAll(
            tokens.neutral_throw, tokens.intermediate_tricks
        ),
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_poison_ex"]: {
        regions.region_names["wooded_kingdom_secret_flower_field_entrance_checkpoint"]: True_(),
    },
    regions.region_names["sky_garden_tower_substage_near_side_tower002"]: {
        regions.region_names["sky_garden_tower_sky_garden_tower_purples_1_3"]: Has(tokens.p_switches),
        regions.region_names["sky_garden_tower_tower_nut"]: Or(
            And(CanCapture(tokens.uproot), Has(tokens.p_switches)),
            HasAll(tokens.p_switches, tokens.intermediate_tricks),
            HasAll(tokens.wall_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.wall_jump, tokens.intermediate_tricks),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.hard_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.hard_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.wall_jump, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.dive, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.vault, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.backflip, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.backflip, tokens.intermediate_tricks)),
            And(
                CanCapture(tokens.uproot),
                HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.intermediate_tricks),
            ),
            And(
                CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.ground_pound_jump, tokens.intermediate_tricks)
            ),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.side_flip, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.side_flip, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.spin, tokens.intermediate_tricks)),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.spin, tokens.intermediate_tricks)),
            And(
                CanCapture(tokens.uproot), HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.intermediate_tricks)
            ),
            And(CanCapture(tokens.uproot), HasAll(tokens.up_throw, tokens.triple_jump, tokens.intermediate_tricks)),
            HasAll(tokens.neutral_throw, tokens.vault, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.vault, tokens.dive, tokens.hard_tricks),
            HasAll(tokens.triple_jump, tokens.dive, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.spin, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.up_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.down_throw, tokens.spin, tokens.wall_jump, tokens.hard_tricks),
            HasAll(tokens.neutral_throw, tokens.backflip, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.ground_pound_jump, tokens.wall_jump, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.wall_jump, tokens.side_flip, tokens.intermediate_tricks),
            HasAll(tokens.neutral_throw, tokens.triple_jump, tokens.wall_jump, tokens.intermediate_tricks),
        ),
    },
    regions.region_names["wooded_kingdom_over_the_cliffs_edge_area"]: {
        regions.region_names["wooded_kingdom_summit_path_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_home_entrance_bonus"]: False_(),
        regions.region_names["wooded_kingdom_nut_round_the_corner"]: True_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_charging_station_area"]: True_(),
    },
    regions.region_names["flower_road_flower_road_purples_1_3"]: {
        regions.region_names["flower_road_substage_near_side_ex_rail_collision"]: False_(),
        regions.region_names["flower_road_substage_far_side_ex_rail_collision_exit"]: False_(),
    },
    regions.region_names["wooded_kingdom_high_up_on_a_rock_wall"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
    },
    regions.region_names["wooded_kingdom_the_nut_in_the_robot_storeroom"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_the_nut_in_the_red_maze"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_moon_shards_in_the_forest"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_charging_station_area"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_home_entrance_ex_mist"]: And(
            CanCapture(tokens.mini_rocket), HasStoryProgress("wooded", [1, 2, 3, 4])
        ),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: True_(),
        regions.region_names["wooded_kingdom_home_entrance_ex_animal_chase"]: True_(),
        regions.region_names["wooded_kingdom_nut_round_the_corner"]: True_(),
        regions.region_names["wooded_kingdom_the_nut_that_grew_on_the_tall_fence"]: Or(
            HasAll(tokens.neutral_throw, tokens.vault, tokens.wall_jump, tokens.long_jump, tokens.intermediate_tricks),
            HasAll(
                tokens.neutral_throw,
                tokens.vault,
                tokens.wall_jump,
                tokens.dive,
                tokens.roll,
                tokens.intermediate_tricks,
            ),
        ),
    },
    regions.region_names["wooded_kingdom_home_entrance_ex_mist"]: {
        regions.region_names["wooded_kingdom_charging_station_area"]: True_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_ex_animal_chase"]: {
        regions.region_names["wooded_kingdom_charging_station_area"]: True_(),
    },
    regions.region_names["wooded_kingdom_above_the_iron_mountain_path"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["herding_sheep_substage_near_side_ex_animal_chase"]: {
        regions.region_names["herding_sheep_2nd_sheep"]: Or(
            Has(tokens.p_switches), HasAll(tokens.ground_pound, tokens.hard_tricks)
        ),
    },
    regions.region_names["sky_garden_tower_tower_nut"]: {
        regions.region_names["sky_garden_tower_substage_far_side_tower002"]: False_(),
        regions.region_names["sky_garden_tower_substage_near_side_tower002"]: False_(),
    },
    regions.region_names["wooded_kingdom_thanks_for_the_charge"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_looking_down_on_goombas"]: {
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_cage_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_painting_access"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_414243"]: {
        regions.region_names["wooded_kingdom_forest_charging_station_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_default_start"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_123"]: {
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_456"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_383940"]: {
        regions.region_names["wooded_kingdom_default_start"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_26272829"]: {
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_44454647"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_1011"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_30313233"]: {
        regions.region_names["wooded_kingdom_iron_road_halfway_point_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_12131415"]: {
        regions.region_names["wooded_kingdom_sky_garden_tower_checkpoint"]: False_(),
        regions.region_names["wooded_kingdom_iron_mountain_path_station_8_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_16171819"]: {
        regions.region_names["wooded_kingdom_iron_road_entrance_checkpoint"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_686970"]: {
        regions.region_names["wooded_kingdom_default_start"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_515253"]: {
        regions.region_names["wooded_kingdom_default_start"]: False_(),
    },
    regions.region_names["wooded_kingdom_wooded_kingdom_purples_717273"]: {
        regions.region_names["wooded_kingdom_default_start"]: False_(),
    },
    regions.region_names["wooded_kingdom_home_entrance_ex_tankuro"]: {
        regions.region_names["wooded_kingdom_observation_deck_checkpoint"]: False_(),
    },
    regions.region_names["deep_woods_substage_far_side_jyukai001"]: {
        regions.region_names["deep_woods_free_space"]: True_(),
    },
    regions.region_names["painting_room_torkdrift_painting_to_torkdrift_boss_re_fight"]: {
        regions.region_names["torkdrift_boss_re_fight_default_start"]: True_(),
    },
    regions.region_names["painting_room_knucklotec_painting_to_knucklotec_boss_re_fight"]: {
        regions.region_names["knucklotec_boss_re_fight_default_start"]: True_(),
    },
    regions.region_names["painting_room_cookatiel_painting_to_cookatiel_boss_re_fight"]: {
        regions.region_names["cookatiel_boss_re_fight_default_start"]: True_(),
    },
    regions.region_names["painting_room_mollusque_lanceur_painting_to_mollusque_lanceur_boss_re_fight"]: {
        regions.region_names["mollusque_lanceur_boss_re_fight_default_start"]: True_(),
    },
    regions.region_names["painting_room_mechawiggler_painting_to_mechawiggler_boss_re_fight"]: {
        regions.region_names["mechawiggler_boss_re_fight_default_start"]: True_(),
    },
}
