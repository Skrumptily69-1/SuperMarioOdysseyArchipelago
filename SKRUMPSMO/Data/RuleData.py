from enum import IntEnum, StrEnum
from .ItemData import SMOItemData
from .LocationData import SMOLocationData
from .RegionData import SMORegion
from .EntranceData import SMOEntranceData

class SMORuleCondition(IntEnum):
    """
    Enumeration of Super Mario Odyssey access rule conditions.
    """
    REGION = 0
    ITEM = 1
    MOONS = 2
    TOTAL_MOONS = 3
    CAPTURE = 4
    REGIONAL_COINS = 5
    ENTRANCE = 6
    TRICK_EASY = 7
    TRICK_INTERMEDIATE= 8
    TRICK_HARD = 9
    GLITCH_EASY = 10
    GLITCH_INTERMEDIATE = 11
    GLITCH_HARD = 12
    ABILITY = 13
    LOCATION = 14
    PARENTHESIS_OPEN = 98
    PARENTHESIS_CLOSE = 99

class SMORuleOperation(IntEnum):
    NONE = -1
    AND = 0
    OR = 1
    PARENTHESIS_NONE = 2
    PARENTHESIS_AND = 3
    PARENTHESIS_OR = 4

class SMOEntranceDataType(StrEnum):
    ENTER = "Entrance"
    EXIT = "End"
    UNIQUE_EXIT = "Unique Exit End"
    START = "Beginning"

class SMOKingdoms(StrEnum):
    CAP = "Cap"
    CASCADE = "Cascade"
    SAND = "Sand"
    WOODED = "Wooded"
    LAKE = "Lake"
    CLOUD = "Cloud"
    LOST = "Lost"
    METRO = "Metro"
    SEASIDE = "Seaside"
    SNOW = "Snow"
    LUNCHEON = "Luncheon"
    RUINED = "Ruined"
    BOWSER = "Bowser's"
    MOON = "Moon"
    MUSHROOM = "Mushroom"
    DARK = "Dark Side"
    DARKER = "Darker Side"

kingdom_name_to_id = {
    SMOKingdoms.CAP : 0,
    SMOKingdoms.CASCADE: 1,
    SMOKingdoms.SAND: 2,
    SMOKingdoms.WOODED: 3,
    SMOKingdoms.LAKE: 4,
    SMOKingdoms.CLOUD: 5,
    SMOKingdoms.LOST: 6,
    SMOKingdoms.METRO: 7,
    SMOKingdoms.SEASIDE: 8,
    SMOKingdoms.SNOW: 9,
    SMOKingdoms.LUNCHEON: 10,
    SMOKingdoms.RUINED: 11,
    SMOKingdoms.BOWSER: 12,
    SMOKingdoms.MOON: 13,
    SMOKingdoms.MUSHROOM: 14,
    SMOKingdoms.DARK: 15,
    SMOKingdoms.DARKER: 16,
}
moon_rule_data : dict[str, list] = {
    #region Cap Moons 
    SMOLocationData.frog_jumping_above_the_fog: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.NONE),
    ],
    SMOLocationData.frog_jumping_from_the_top_deck: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.NONE),
    ],
    SMOLocationData.cap_kingdom_timer_challenge_1: [],
    SMOLocationData.shopping_in_bonneton: [],
    SMOLocationData.the_forgotten_treasure: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE),
    ],
    SMOLocationData.taxi_flying_through_bonneton: [
        (SMORuleCondition.CAPTURE, [SMOItemData.binoculars], SMORuleOperation.NONE),
    ],
    SMOLocationData.bonnetter_blockade: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    SMOLocationData.peach_in_the_cap_kingdom: [
        (SMORuleCondition.REGION, SMORegion.mushroom_kingdom, SMORuleOperation.NONE)
    ],
    SMOLocationData.found_with_cap_kingdom_art: [
        (SMORuleCondition.REGION, SMORegion.moon_kingdom, SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cap Moons Top of Top Hat Tower
    SMOLocationData.good_evening_captain_toad: [],
    SMOLocationData.cap_kingdom_regular_cup: [],
    #endregion

    #region Cap Moons Moon Rock
    SMOLocationData.next_to_glasses_bridge: [],
    SMOLocationData.danger_sign: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    SMOLocationData.under_the_big_ones_brim: [],
    SMOLocationData.fly_to_the_edge_of_the_fog: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.spin_the_hat_get_a_prize: [],
    SMOLocationData.hidden_in_a_sunken_hat: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.fog_shrouded_platform: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE),
    ],
    SMOLocationData.bird_traveling_in_the_fog: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, None, SMORuleOperation.NONE),
    ],
    SMOLocationData.caught_hopping_near_the_ship: [],
    SMOLocationData.taking_notes_in_the_fog: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    SMOLocationData.cap_kingdom_timer_challenge_2: [],
    #endregion

    #region Cap Moons Top of Top Hat Tower Moon Rock
    SMOLocationData.cap_kingdom_master_cup: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [SMOItemData.long_jump], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [SMOItemData.roll], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [SMOItemData.triple_jump], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Moons Poson Tide
    SMOLocationData.skimming_the_poison_tide: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    SMOLocationData.slipping_through_the_poison_tide: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Moons Push Block
    SMOLocationData.push_block_peril: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR), 

    ],
    SMOLocationData.hidden_among_the_push_blocks: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR), 
    ],
    #endregion

    #region Cap Moons Frog Pond
    SMOLocationData.searching_the_frog_pond: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY,
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.vault, SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE,
        [SMOItemData.backflip, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.NONE),
        ],

    SMOLocationData.secrets_of_the_frog_pond: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY,
         [SMOItemData.vault, SMOItemData.dive, SMOItemData.wall_jump], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cap Moons Rolling Lane
    SMOLocationData.roll_on_and_on: [],
    SMOLocationData.precision_rolling: [],
    #endregion

    #region Cascade Moons
    SMOLocationData.our_first_power_moon: [
    (SMORuleCondition.CAPTURE, [SMOItemData.chain_chomp], SMORuleOperation.NONE)
    ],
    SMOLocationData.chomp_through_the_rocks: [
        (SMORuleCondition.CAPTURE, [SMOItemData.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.chain_chomp], SMORuleOperation.NONE)

    ],
    SMOLocationData.behind_the_waterfall: [
        (SMORuleCondition.CAPTURE, [SMOItemData.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.big_chain_chomp], SMORuleOperation.NONE),      
    ],
    SMOLocationData.multi_moon_atop_the_falls: [
        (SMORuleCondition.CAPTURE, [SMOItemData.broodes_chain_chomp, SMOItemData.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.broodes_chain_chomp, SMOItemData.big_chain_chomp], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.broodes_chain_chomp, SMOItemData.backflip, SMOItemData.dive, SMOItemData.wall_jump, SMOItemData.vault], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cascade Moons Post Peace Moons
    SMOLocationData.treasure_of_the_waterfall_basin: [],
    SMOLocationData.on_top_of_the_rubble: [],
    SMOLocationData.cascade_kingdom_timer_challenge_1: [],
    SMOLocationData.cascade_kingdom_regular_cup:[
        (SMORuleCondition.ABILITY, [SMOItemData.roll_boost], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.long_jump], [SMOItemData.triple_jump], [SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spin], [SMOItemData.triple_jump], [SMOItemData.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [], SMORuleOperation.NONE),
    ],
    SMOLocationData.shopping_in_fossil_falls:[],
    SMOLocationData.sphynx_traveling_to_the_waterfall: [
        (SMORuleCondition.CAPTURE, [SMOItemData.binoculars], SMORuleOperation.NONE),
    ],
    SMOLocationData.above_a_high_cliff: [],
    SMOLocationData.across_the_floating_isles: [],
    SMOLocationData.cascade_kingdom_timer_challenge_2: [
        (SMORuleCondition.ABILITY, [SMOItemData.triple_jump], [SMOItemData.backflip], [SMOItemData.side_flip], 
        [SMOItemData.ground_pound_jump],[SMOItemData.spin],[SMOItemData.double_jump, SMOItemData.dive], [SMOItemData.wall_jump, SMOItemData.dive], SMORuleOperation.NONE),
    ],
    SMOLocationData.good_morning_captain_toad:[],
    SMOLocationData.caveman_cave_fan:[
        (SMORuleCondition.ITEM, [SMOItemData.caveman_headwear, SMOItemData.caveman_outfit], SMORuleOperation.NONE)
    ],
    SMOLocationData.peach_in_the_cascade_kingdom: [
        (SMORuleCondition.REGION, SMORegion.mushroom_kingdom, SMORuleOperation.NONE)
    ],
    SMOLocationData.secret_path_to_fossil_falls: [
        (SMORuleCondition.REGION, SMORegion.seaside_kingdom_peace, SMORuleOperation.AND),
        (SMORuleCondition.REGION, SMORegion.snow_kingdom_peace, SMORuleOperation.NONE),
    ],
    SMOLocationData.a_tourist_in_the_cascade_kingdom: [
        (SMORuleCondition.REGION, SMORegion.sand_kingdom_peace, SMORuleOperation.AND),
        (SMORuleCondition.REGION, SMORegion.metro_kingdom_peace, SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Moons Moon Revisit Moons
    SMOLocationData.rolling_rock_by_the_falls: [],
    #endregion

    #region Cascade Moons Moon Rock Moons
    SMOLocationData.taking_notes_hurry_upward: [],
    SMOLocationData.bottom_of_the_waterfall_basin: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.under_the_old_electrical_pole: [
        (SMORuleCondition.CAPTURE, [SMOItemData.t_rex], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.caught_hopping_at_the_waterfall: [],
    SMOLocationData.cascade_kingdom_master_cup: [
        (SMORuleCondition.ABILITY, [SMOItemData.long_jump], [SMOItemData.triple_jump], [SMOItemData.dive], [SMOItemData.roll_boost], SMORuleOperation.NONE)
    ],
    SMOLocationData.next_to_the_stone_arch: [],
    SMOLocationData.guarded_by_a_colossal_fossil: [],
    SMOLocationData.inside_the_busted_fossil:[
        
    ],
    SMOLocationData.treasure_under_the_cliff: [],
    SMOLocationData.under_the_ground: [
        (SMORuleCondition.CAPTURE, [SMOItemData.t_rex], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.PARENTHESIS_NONE)
    ],
    #endregion

    #region Cascade Kingdom T-Rex Nest Moons
    SMOLocationData.dinosaur_nest_big_cleanup: [],
    SMOLocationData.dinosaur_nest_running_wild: [
        (SMORuleCondition.CAPTURE, [SMOItemData.t_rex], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Kingdom Chain Chomp Cave Moons
    SMOLocationData.nice_shot_with_the_chain_chomp: [
        (SMORuleCondition.CAPTURE, [SMOItemData.chain_chomp], SMORuleOperation.NONE)
    ],
    SMOLocationData.very_nice_shot_with_the_chain_chomp:[
        (SMORuleCondition.CAPTURE, [SMOItemData.chain_chomp], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Kingdom Chasm Lifts Moons
    SMOLocationData.past_the_chasm_lifts:[],
    SMOLocationData.hidden_chasm_passage:[],
    #endregion

    #region Cascade Kingdom Gusty Bridges Moons
    SMOLocationData.across_the_gusty_bridges: [],
    SMOLocationData.flying_far_away_from_gusty_bridges: [],
    #endregion

    #region Cascade Kingdom Mysterious Clouds Moons
    SMOLocationData.across_the_mysterious_clouds: [],
    SMOLocationData.atop_a_wall_among_the_clouds: [],
    #endregion

    #region Sand Kingdom Moons
    SMOLocationData.atop_the_highest_tower: [],
    SMOLocationData.moon_shards_in_the_sand: [],
    SMOLocationData.overlooking_the_desert_town: [],
    SMOLocationData.alcove_in_the_ruins: [],
    SMOLocationData.on_the_leaning_pillar: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [], SMORuleOperation.NONE),
    ],
    SMOLocationData.hidden_room_in_the_flowing_sands: [],
    SMOLocationData.secret_of_the_mural: [],
    SMOLocationData.on_top_of_stone_archway: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.spark_pylon], SMORuleOperation.NONE),
    ],
    SMOLocationData.from_a_crate_in_the_ruins: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.long_jump], [SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], [SMOItemData.triple_jump], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [], SMORuleOperation.NONE)
    ],  
    SMOLocationData.where_the_birds_gather: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.top_of_a_dune: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.lost_in_the_luggage: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.inside_a_block_is_a_hard_place: [],
    SMOLocationData.the_treasure_of_jaxi_ruins: [],
    SMOLocationData.bird_traveling_the_desert: [],
    SMOLocationData.desert_gardening_plaza_seed: [],
    SMOLocationData.desert_gardening_ruins_seed: [],
    SMOLocationData.desert_gardening_seed_on_the_cliff: [],
    SMOLocationData.taking_notes_jump_on_the_palm: [
        (SMORuleCondition.ABILITY, [SMOItemData.climb], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [], SMORuleOperation.NONE)
    ],
    SMOLocationData.among_the_five_cactuses: [],
    SMOLocationData.wandering_cactus: [
        SMORuleCondition.CAPTURE, [SMOItemData.cactus], SMORuleOperation.NONE
    ],
    SMOLocationData.found_with_bowsers_kingdom_art: [
        (SMORuleCondition.REGION, [SMORegion.bowsers_kingdom], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound],  SMORuleOperation.PARENTHESIS_NONE)
    ],
    #endregion

    #region Sand Kingdom Inverted Pyramid Mural
    SMOLocationData.secret_of_the_inverted_mural: [],
    #endregion

    #region Sand Kingdom Inverted Pyramid Upper
    SMOLocationData.hidden_room_in_the_inverted_pyramid: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        #needs to be tested with people
    ],
    #endregion

    #region Sand Kingdom Inverted Pyramid Top
    SMOLocationData.showdown_on_the_inverted_pyramid: [],
    SMOLocationData.on_the_statues_tail: [],
    SMOLocationData.on_the_lone_pillar: [],
    #waiting for kgamer
    #endregion

    #region Sand Kingdom Night Sand
    SMOLocationData.bullet_bill_breakthrough: [],
    SMOLocationData.secret_path_to_new_donk_city: [],
    #endregion

    #region Sand Kingdom Underground Ruins
    SMOLocationData.underground_treasure_chest: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.dive], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.vault], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.backflip], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.ground_pound_jump], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.ledge_grab], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.spin], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.side_flip], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD,  [SMOItemData.ground_pound_jump, SMOItemData.vault, SMOItemData.dive, SMOItemData.roll, SMOItemData.up_throw, SMOItemData.down_throw], SMORuleOperation.NONE)
    ],
    SMOLocationData.goomba_tower_assembly: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ground_pound, SMOItemData.vault, SMOItemData.dive, SMOItemData.roll], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Deepest Underground
    SMOLocationData.the_hole_in_the_desert: [
        (SMORuleCondition.CAPTURE, [SMOItemData.knucklotecs_fist, SMOItemData.bullet_bill], SMORuleOperation.OR,),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ground_pound_jump, SMOItemData.vault, SMOItemData.dive, SMOItemData.roll, SMOItemData.up_throw, SMOItemData.down_throw, SMOItemData.knucklotecs_fist], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Post Peace
    SMOLocationData.hang_your_hat_on_the_fountain: [],
    SMOLocationData.bird_traveling_wastes: [],
    SMOLocationData.sand_kingdom_timer_challenge_2: [],
    SMOLocationData.sand_kingdom_timer_challenge_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.spark_pylon], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [SMOItemData.roll, SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.crouch, SMOItemData.wall_jump, SMOItemData.dive, SMOItemData.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump, SMOItemData.dive, SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.sand_kingdom_timer_challenge_3: [],
    SMOLocationData.found_in_the_sand_good_dog: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.herding_sheep_in_the_dunes: [],
    SMOLocationData.fishing_in_the_oasis: [
        (SMORuleCondition.CAPTURE, [SMOItemData.lakitu], SMORuleOperation.NONE)
    ],
    SMOLocationData.love_in_the_heart_of_the_desert: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.youre_quite_a_catch_captain_toad: [
        (SMORuleCondition.CAPTURE, [SMOItemData.lakitu], SMORuleOperation.NONE)
    ],
    SMOLocationData.jaxi_reunion: [],
    SMOLocationData.walking_the_desert: [],
    #endregion

    #region Sand Kingdom Top of Top hat Tower Post Peace
    SMOLocationData.the_lurker_under_the_stone: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.welcome_back_jaxi: [],
    #endregion

    #region Sand Kingdom Sand Shop
    SMOLocationData.shopping_in_tostarena: [],
    #endregion

    #region Sand Kingdom Slots
    SMOLocationData.sand_kingdom_slots: [],
    #endregion

    #region Sand Kingdom Moe Eye Sub Area
    SMOLocationData.the_invisible_maze: [],
    SMOLocationData.skull_sign_in_the_transparent_maze: [],
    #endregion

    #region Sand Kingdom Bullet Bill Maze
    SMOLocationData.the_bullet_bill_maze_break_through: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.the_bullet_bill_maze_side_path: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE),
    ],
    #endregion

    #region Sand Kingdom Jaxi Ruins
    SMOLocationData.jaxi_driver: [],
    SMOLocationData.jaxi_stunt_driving: [],
    #endregion
    
    #region Sand Kingdom Strange Neighborhood
    SMOLocationData.strange_neighborhood: [],
    SMOLocationData.above_a_strange_neighborhood: [],
    #endregion

    #region Sand Kingdom Sand Rumble
    SMOLocationData.a_rumble_from_the_sandy_floor: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Employees Only
    SMOLocationData.employees_only: [],
    #endregion

    #region Sand Kingdom Ice Cave
    SMOLocationData.ice_cave_treasure: [
        (SMORuleCondition.ABILITY, [SMOItemData.wall_jump], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Sphynx Vault
    SMOLocationData.sphynxs_hidden_vault: [],
    #endregion

    #region Sand Kingdom Deepest Underground Peace
    SMOLocationData.under_the_mummys_curse: [],
    #endregion

    #region Sand Kingdom Deepest Underground Post Game
    SMOLocationData.binding_band_returned: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE) 
    ],
    #endregion

    #region Sand Kingdom Moe Eye Floor
    SMOLocationData.where_the_transparent_platforms_end: [],
    SMOLocationData.jump_onto_the_transparent_lift: [],
    #endregion

    #region Sand Kingdom Colassal Ruins
    SMOLocationData.colossal_ruins_dash_jump: [
        (SMORuleCondition.CAPTURE, [SMOItemData.spark_pylon], SMORuleOperation.NONE)
    ],
    SMOLocationData.sinking_colossal_ruins_hurry: [
        (SMORuleCondition.CAPTURE, [SMOItemData.spark_pylon], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Sand Outfit
    SMOLocationData.dancing_with_new_friends: [],
    #endregion

    #region Sand Kingdom Sand Kingdom Moon Rock
    SMOLocationData.jammin_in_the_sand_kingdom: [],
    SMOLocationData.hat_and_seek_in_the_sand: [],
    SMOLocationData.sand_kingdom_regular_cup: [],
    SMOLocationData.sand_kingdom_master_cup: [],
    SMOLocationData.round_the_world_tourist: [],
    SMOLocationData.peach_in_the_sand_kingdom: [],
    SMOLocationData.mighty_leap_from_the_palm_tree: [],
    SMOLocationData.on_the_north_pillar: [
        (SMORuleCondition.CAPTURE, [SMOItemData.spark_pylon], SMORuleOperation.NONE)
    ],
    SMOLocationData.into_the_flowing_sands: [],
    SMOLocationData.in_the_skies_above_the_canyon: [],
    SMOLocationData.island_in_the_poison_swamp: [],
    SMOLocationData.an_invisible_gleam: [
        (SMORuleCondition.ABILITY, [SMOItemData.ground_pound], SMORuleOperation.NONE)
    ],
    SMOLocationData.on_the_eastern_pillar: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.NONE)
    ],
    SMOLocationData.caught_hopping_in_the_desert: [],
    SMOLocationData.poster_cleanup: [],
    SMOLocationData.taking_notes_running_down: [],
    SMOLocationData.taking_notes_in_the_wall_painting: [],
    SMOLocationData.love_at_the_edge_of_the_desert: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.more_walking_in_the_desert: [],
    #endregion

    #region Sand Kingdom Freezing Waterway
    SMOLocationData.through_the_freezing_waterway: [
        (SMORuleCondition.CAPTURE, [SMOItemData.gushen], SMORuleOperation.NONE)
    ],
    SMOLocationData.freezing_waterway_hidden_room: [
        (SMORuleCondition.CAPTURE, [SMOItemData.gushen], SMORuleOperation.NONE)
    ]
    #endregion

}

regional_rule_data : dict[str, list] = {
    #region Cap Kingdom Regional Coins
    SMOLocationData.cap_kingdom_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE),
    ],
    SMOLocationData.cap_kingdom_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_8: [
        (SMORuleCondition.CAPTURE, [SMOItemData.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    SMOLocationData.cap_kingdom_regional_coin_group_3: [],
    SMOLocationData.cap_kingdom_regional_coin_9: [],
    SMOLocationData.cap_kingdom_regional_coin_10: [],
    SMOLocationData.cap_kingdom_regional_coin_11: [],
    SMOLocationData.cap_kingdom_regional_coin_12: [],
    SMOLocationData.cap_kingdom_regional_coin_group_4: [],
    SMOLocationData.cap_kingdom_regional_coin_13: [],
    SMOLocationData.cap_kingdom_regional_coin_14: [],
    SMOLocationData.cap_kingdom_regional_coin_15: [],
    SMOLocationData.cap_kingdom_regional_coin_16: [],
    SMOLocationData.cap_kingdom_regional_coin_group_5: [],
    SMOLocationData.cap_kingdom_regional_coin_17: [],
    SMOLocationData.cap_kingdom_regional_coin_18: [],
    SMOLocationData.cap_kingdom_regional_coin_19: [],
    SMOLocationData.cap_kingdom_regional_coin_group_6: [],
    SMOLocationData.cap_kingdom_regional_coin_20: [],
    SMOLocationData.cap_kingdom_regional_coin_21: [],
    SMOLocationData.cap_kingdom_regional_coin_22: [],
    SMOLocationData.cap_kingdom_regional_coin_group_7: [],
    SMOLocationData.cap_kingdom_regional_coin_23: [],
    SMOLocationData.cap_kingdom_regional_coin_24: [],
    SMOLocationData.cap_kingdom_regional_coin_25: [],
    SMOLocationData.cap_kingdom_regional_coin_group_8: [],
    SMOLocationData.cap_kingdom_regional_coin_26: [],
    SMOLocationData.cap_kingdom_regional_coin_27: [],
    SMOLocationData.cap_kingdom_regional_coin_28: [],
    SMOLocationData.cap_kingdom_regional_coin_group_9: [],
    SMOLocationData.cap_kingdom_regional_coin_29: [],
    SMOLocationData.cap_kingdom_regional_coin_30: [],
    SMOLocationData.cap_kingdom_regional_coin_31: [],
    #endregion

    #region Top Hat Tower Regional Coins
    SMOLocationData.top_hat_tower_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.top_hat_tower_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.top_hat_tower_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.top_hat_tower_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.top_hat_tower_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    SMOLocationData.top_hat_tower_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    SMOLocationData.top_hat_tower_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    SMOLocationData.top_hat_tower_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    SMOLocationData.top_hat_tower_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    SMOLocationData.top_hat_tower_regional_coin_8: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    SMOLocationData.top_hat_tower_regional_coin_9: [
        (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    #endregion

    #region Cap Kingdom Frog Pond Regional Coins
    SMOLocationData.frog_pond_regional_coin_group_1: [
    (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.dive, SMOItemData.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [SMOItemData.backflip, SMOItemData.wall_jump, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [SMOItemData.vault, SMOItemData.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    SMOLocationData.frog_pond_regional_coin_1: [
    (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.dive, SMOItemData.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [SMOItemData.backflip, SMOItemData.wall_jump, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [SMOItemData.vault, SMOItemData.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    SMOLocationData.frog_pond_regional_coin_2: [
    (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.dive, SMOItemData.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [SMOItemData.backflip, SMOItemData.wall_jump, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [SMOItemData.vault, SMOItemData.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    SMOLocationData.frog_pond_regional_coin_3: [
    (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.dive, SMOItemData.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [SMOItemData.backflip, SMOItemData.wall_jump, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [SMOItemData.vault, SMOItemData.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    SMOLocationData.frog_pond_regional_coin_4: [    
    (SMORuleCondition.CAPTURE, [SMOItemData.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [SMOItemData.dive, SMOItemData.backflip, SMOItemData.vault],
        [SMOItemData.ground_pound_jump, SMOItemData.dive, SMOItemData.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [SMOItemData.backflip, SMOItemData.wall_jump, SMOItemData.dive],
        [SMOItemData.ground_pound_jump, SMOItemData.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [SMOItemData.vault, SMOItemData.wall_jump],
    ], SMORuleOperation.NONE),
    ],    
    #endregion

    #region Cap Kingdom Poison Tides Regional Coins
    SMOLocationData.poison_tides_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE,[SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.poison_tides_regional_coin_1: [
        (SMORuleCondition.CAPTURE,[SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.poison_tides_regional_coin_2: [
        (SMORuleCondition.CAPTURE,[SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    SMOLocationData.poison_tides_regional_coin_3: [
        (SMORuleCondition.CAPTURE,[SMOItemData.paragoomba], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cap Kingdom Push Block Regional Coins
    SMOLocationData.pushblocks_regional_coin_group_1: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR),  
    ],
    SMOLocationData.pushblocks_regional_coin_1: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR), 
    ],
    SMOLocationData.pushblocks_regional_coin_2: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR),         
    ],
    SMOLocationData.pushblocks_regional_coin_3: [
        (SMORuleCondition.ABILITY,
        [SMOItemData.spark_pylon, SMOItemData.double_jump], 
        [SMOItemData.spark_pylon, SMOItemData.vault], 
        [SMOItemData.spark_pylon, SMOItemData.wall_jump],
        [SMOItemData.spark_pylon, SMOItemData.dive],
        [SMOItemData.spark_pylon, SMOItemData.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,    
        [SMOItemData.spark_pylon, SMOItemData.ledge_grab], SMORuleOperation.NONE),        
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMOItemData.spark_pylon], SMORuleOperation.OR), 
    ],
    #endregion

    #region Cascade Kingdom Regional Coins
    SMOLocationData.cascade_kingdom_regional_coin_group_1: [],
    SMOLocationData.cascade_kingdom_regional_coin_1: [],
    SMOLocationData.cascade_kingdom_regional_coin_2: [],
    SMOLocationData.cascade_kingdom_regional_coin_3: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_2: [],
    SMOLocationData.cascade_kingdom_regional_coin_4: [],
    SMOLocationData.cascade_kingdom_regional_coin_5: [],
    SMOLocationData.cascade_kingdom_regional_coin_6: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_3: [],
    SMOLocationData.cascade_kingdom_regional_coin_7: [],
    SMOLocationData.cascade_kingdom_regional_coin_8: [],
    SMOLocationData.cascade_kingdom_regional_coin_9: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_4: [],
    SMOLocationData.cascade_kingdom_regional_coin_10: [],
    SMOLocationData.cascade_kingdom_regional_coin_11: [],
    SMOLocationData.cascade_kingdom_regional_coin_12: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_5: [],
    SMOLocationData.cascade_kingdom_regional_coin_13: [],
    SMOLocationData.cascade_kingdom_regional_coin_14: [],
    SMOLocationData.cascade_kingdom_regional_coin_15: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_6: [],
    SMOLocationData.cascade_kingdom_regional_coin_16: [],
    SMOLocationData.cascade_kingdom_regional_coin_17: [],
    SMOLocationData.cascade_kingdom_regional_coin_18: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_7: [],
    SMOLocationData.cascade_kingdom_regional_coin_19: [],
    SMOLocationData.cascade_kingdom_regional_coin_20: [],
    SMOLocationData.cascade_kingdom_regional_coin_21: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_8: [],
    SMOLocationData.cascade_kingdom_regional_coin_22: [],
    SMOLocationData.cascade_kingdom_regional_coin_23: [],
    SMOLocationData.cascade_kingdom_regional_coin_24: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_9: [],
    SMOLocationData.cascade_kingdom_regional_coin_25: [],
    SMOLocationData.cascade_kingdom_regional_coin_26: [],
    SMOLocationData.cascade_kingdom_regional_coin_27: [],
    #endregion
    
    #region Cascade Kingdom Post Peace Regional Coins
    SMOLocationData.cascade_kingdom_regional_coin_group_10: [],
    SMOLocationData.cascade_kingdom_regional_coin_28: [],
    SMOLocationData.cascade_kingdom_regional_coin_29: [],
    SMOLocationData.cascade_kingdom_regional_coin_30: [],
    SMOLocationData.cascade_kingdom_regional_coin_31: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_11: [],
    SMOLocationData.cascade_kingdom_regional_coin_32: [],
    SMOLocationData.cascade_kingdom_regional_coin_33: [],
    SMOLocationData.cascade_kingdom_regional_coin_34: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_12: [],
    SMOLocationData.cascade_kingdom_regional_coin_35: [],
    SMOLocationData.cascade_kingdom_regional_coin_36: [],
    SMOLocationData.cascade_kingdom_regional_coin_37: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_13: [],
    SMOLocationData.cascade_kingdom_regional_coin_38: [],
    SMOLocationData.cascade_kingdom_regional_coin_39: [],
    SMOLocationData.cascade_kingdom_regional_coin_40: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_14: [],
    SMOLocationData.cascade_kingdom_regional_coin_41: [],
    SMOLocationData.cascade_kingdom_regional_coin_42: [],
    SMOLocationData.cascade_kingdom_regional_coin_43: [],
    SMOLocationData.cascade_kingdom_regional_coin_group_15: [],
    SMOLocationData.cascade_kingdom_regional_coin_44: [],
    SMOLocationData.cascade_kingdom_regional_coin_45: [],
    SMOLocationData.cascade_kingdom_regional_coin_46: [],    
    #endregion

    #region Cascade Kingdom Chasm Lifts Regional Coins
    SMOLocationData.chasm_lifts_regional_coin_group_1: [],
    SMOLocationData.chasm_lifts_regional_coin_1: [],
    SMOLocationData.chasm_lifts_regional_coin_2: [],
    SMOLocationData.chasm_lifts_regional_coin_3: [],
    SMOLocationData.chasm_lifts_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Regional Coins
    SMOLocationData.sand_kingdom_regional_coin_group_1: [],
    SMOLocationData.sand_kingdom_regional_coin_1: [],
    SMOLocationData.sand_kingdom_regional_coin_2: [],
    SMOLocationData.sand_kingdom_regional_coin_3: [],
    SMOLocationData.sand_kingdom_regional_coin_group_2: [],
    SMOLocationData.sand_kingdom_regional_coin_4: [],
    SMOLocationData.sand_kingdom_regional_coin_5: [],
    SMOLocationData.sand_kingdom_regional_coin_6: [],
    SMOLocationData.sand_kingdom_regional_coin_group_3: [],
    SMOLocationData.sand_kingdom_regional_coin_7: [],
    SMOLocationData.sand_kingdom_regional_coin_8: [],
    SMOLocationData.sand_kingdom_regional_coin_9: [],
    SMOLocationData.sand_kingdom_regional_coin_group_4: [], 
    SMOLocationData.sand_kingdom_regional_coin_10: [], 
    SMOLocationData.sand_kingdom_regional_coin_11: [], 
    SMOLocationData.sand_kingdom_regional_coin_12: [],
    SMOLocationData.sand_kingdom_regional_coin_group_5: [], 
    SMOLocationData.sand_kingdom_regional_coin_13: [],
    SMOLocationData.sand_kingdom_regional_coin_14: [], 
    SMOLocationData.sand_kingdom_regional_coin_15: [],
    SMOLocationData.sand_kingdom_regional_coin_group_6: [],
    SMOLocationData.sand_kingdom_regional_coin_16: [],
    SMOLocationData.sand_kingdom_regional_coin_17: [],
    SMOLocationData.sand_kingdom_regional_coin_group_7: [],
    SMOLocationData.sand_kingdom_regional_coin_18: [],
    SMOLocationData.sand_kingdom_regional_coin_19: [],
    SMOLocationData.sand_kingdom_regional_coin_group_8: [], 
    SMOLocationData.sand_kingdom_regional_coin_20: [],
    SMOLocationData.sand_kingdom_regional_coin_21: [],
    SMOLocationData.sand_kingdom_regional_coin_22: [],
    SMOLocationData.sand_kingdom_regional_coin_group_9: [], 
    SMOLocationData.sand_kingdom_regional_coin_23: [],
    SMOLocationData.sand_kingdom_regional_coin_24: [],
    SMOLocationData.sand_kingdom_regional_coin_25: [],
    SMOLocationData.sand_kingdom_regional_coin_group_10: [], 
    SMOLocationData.sand_kingdom_regional_coin_26: [],
    SMOLocationData.sand_kingdom_regional_coin_27: [],
    SMOLocationData.sand_kingdom_regional_coin_28: [],
    SMOLocationData.sand_kingdom_regional_coin_group_11: [], 
    SMOLocationData.sand_kingdom_regional_coin_29: [],
    SMOLocationData.sand_kingdom_regional_coin_30: [],
    SMOLocationData.sand_kingdom_regional_coin_31: [],
    SMOLocationData.sand_kingdom_regional_coin_group_12: [], 
    SMOLocationData.sand_kingdom_regional_coin_32: [],
    SMOLocationData.sand_kingdom_regional_coin_33: [],
    SMOLocationData.sand_kingdom_regional_coin_34: [],
    SMOLocationData.sand_kingdom_regional_coin_group_13: [], 
    SMOLocationData.sand_kingdom_regional_coin_35: [],
    SMOLocationData.sand_kingdom_regional_coin_36: [],
    SMOLocationData.sand_kingdom_regional_coin_37: [],
    SMOLocationData.sand_kingdom_regional_coin_group_14: [], 
    SMOLocationData.sand_kingdom_regional_coin_38: [],
    SMOLocationData.sand_kingdom_regional_coin_39: [],
    SMOLocationData.sand_kingdom_regional_coin_40: [],
    SMOLocationData.sand_kingdom_regional_coin_group_15: [], 
    SMOLocationData.sand_kingdom_regional_coin_41: [],
    SMOLocationData.sand_kingdom_regional_coin_42: [],
    SMOLocationData.sand_kingdom_regional_coin_group_16: [], 
    SMOLocationData.sand_kingdom_regional_coin_43: [],
    SMOLocationData.sand_kingdom_regional_coin_44: [],
    SMOLocationData.sand_kingdom_regional_coin_45: [],
    SMOLocationData.sand_kingdom_regional_coin_46: [],
    SMOLocationData.sand_kingdom_regional_coin_47: [],
    SMOLocationData.sand_kingdom_regional_coin_48: [],
    SMOLocationData.sand_kingdom_regional_coin_group_17: [], 
    SMOLocationData.sand_kingdom_regional_coin_49: [],
    SMOLocationData.sand_kingdom_regional_coin_50: [],
    SMOLocationData.sand_kingdom_regional_coin_51: [],
    SMOLocationData.sand_kingdom_regional_coin_group_20: [],
    SMOLocationData.sand_kingdom_regional_coin_60: [],
    SMOLocationData.sand_kingdom_regional_coin_61: [],
    SMOLocationData.sand_kingdom_regional_coin_group_21: [], 
    SMOLocationData.sand_kingdom_regional_coin_62: [],
    SMOLocationData.sand_kingdom_regional_coin_63: [],    
    #endregion

    #region Sand Kingdom Purple Coins Post Peace
    SMOLocationData.sand_kingdom_regional_coin_group_18: [],
    SMOLocationData.sand_kingdom_regional_coin_52: [],
    SMOLocationData.sand_kingdom_regional_coin_53: [], 
    SMOLocationData.sand_kingdom_regional_coin_54: [],
    SMOLocationData.sand_kingdom_regional_coin_55: [],
    SMOLocationData.sand_kingdom_regional_coin_group_19: [],
    SMOLocationData.sand_kingdom_regional_coin_56: [],
    SMOLocationData.sand_kingdom_regional_coin_57: [],
    SMOLocationData.sand_kingdom_regional_coin_58: [],
    SMOLocationData.sand_kingdom_regional_coin_59: [],
    #endregion
    
    #region Sand Kingdom Bullet Bill Maze Regional Coins
    SMOLocationData.bullet_bill_maze_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.bullet_bill_maze_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.bullet_bill_maze_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.bullet_bill_maze_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    SMOLocationData.bullet_bill_maze_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ], 
    SMOLocationData.bullet_bill_maze_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ], 
    SMOLocationData.bullet_bill_maze_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMOItemData.vault], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Moe Eye Invisible Maze
    SMOLocationData.moeeye_invisible_maze_regional_coin_group_1: [],
    SMOLocationData.moeeye_invisible_maze_regional_coin_1: [],
    SMOLocationData.moeeye_invisible_maze_regional_coin_2: [],
    SMOLocationData.moeeye_invisible_maze_regional_coin_3: [],
    SMOLocationData.moeeye_invisible_maze_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Ice Cave
    SMOLocationData.ice_cave_regional_coin_group_1: [],
    SMOLocationData.ice_cave_regional_coin_1: [],
    SMOLocationData.ice_cave_regional_coin_2: [],
    SMOLocationData.ice_cave_regional_coin_group_2: [], 
    SMOLocationData.ice_cave_regional_coin_3: [],
    SMOLocationData.ice_cave_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Upper Pyramid
    SMOLocationData.pyramid_upper_interior_regional_coin_group_1: [],
    SMOLocationData.pyramid_upper_interior_regional_coin_1: [],
    SMOLocationData.pyramid_upper_interior_regional_coin_2: [],
    SMOLocationData.pyramid_upper_interior_regional_coin_3: [],
    #endregion

    #region Sand Kingdom Strange Neighborhood
    SMOLocationData.strange_neighborhood_regional_coin_group_1: [],
    SMOLocationData.strange_neighborhood_regional_coin_1: [],
    SMOLocationData.strange_neighborhood_regional_coin_2: [],
    SMOLocationData.strange_neighborhood_regional_coin_group_2: [], 
    SMOLocationData.strange_neighborhood_regional_coin_3: [], 
    SMOLocationData.strange_neighborhood_regional_coin_4: [], 
    SMOLocationData.strange_neighborhood_regional_coin_5: [],
    #endregion

    #region Underground Ruins 
    SMOLocationData.underground_ruins_regional_coin_group_1: [],
    SMOLocationData.underground_ruins_regional_coin_1: [],
    SMOLocationData.underground_ruins_regional_coin_2: [],
    SMOLocationData.underground_ruins_regional_coin_3: [],
    SMOLocationData.underground_ruins_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [SMOItemData.up_throw], SMORuleOperation.NONE)
    ],
    SMOLocationData.underground_ruins_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [SMOItemData.up_throw], SMORuleOperation.NONE)
    ],
    SMOLocationData.underground_ruins_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [SMOItemData.up_throw], SMORuleOperation.NONE)
    ],
    SMOLocationData.underground_ruins_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [SMOItemData.up_throw], SMORuleOperation.NONE)
    ], 
    SMOLocationData.underground_ruins_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [SMOItemData.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [SMOItemData.up_throw], SMORuleOperation.NONE)
    ],
    #endregion

    #region Jaxi Ruins
    SMOLocationData.jaxi_ruins_regional_coin_group_1: [],
    SMOLocationData.jaxi_ruins_regional_coin_1: [], 
    SMOLocationData.jaxi_ruins_regional_coin_2: [], 
    SMOLocationData.jaxi_ruins_regional_coin_group_2: [], 
    SMOLocationData.jaxi_ruins_regional_coin_3: [], 
    SMOLocationData.jaxi_ruins_regional_coin_4: [], 
    SMOLocationData.jaxi_ruins_regional_coin_5: [], 
    SMOLocationData.jaxi_ruins_regional_coin_group_3: [], 
    SMOLocationData.jaxi_ruins_regional_coin_6: [], 
    SMOLocationData.jaxi_ruins_regional_coin_7: [],
    SMOLocationData.jaxi_ruins_regional_coin_8: [], 
    #endregion
}

