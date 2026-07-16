from enum import IntEnum, StrEnum

#Relevant Functions: Has, HasAll, HasAny, HasGroup, And, Or, Filtered, CanReachLocation, CanReachRegion
from rule_builder.rules import *

from .EntranceData import SMOEntranceData
from .ItemData import SMOItemData as items
from .LocationData import SMOLocationData as loc
from .RegionData import SMORegion


# class SMORuleCondition(IntEnum):
#     """
#     Enumeration of Super Mario Odyssey access rule conditions.
#     """
#     REGION = 0
#     ITEM = 1
#     MOONS = 2
#     TOTAL_MOONS = 3
#     CAPTURE = 4
#     REGIONAL_COINS = 5
#     ENTRANCE = 6
#     TRICK_EASY = 7
#     TRICK_INTERMEDIATE= 8
#     TRICK_HARD = 9
#     GLITCH_EASY = 10
#     GLITCH_INTERMEDIATE = 11
#     GLITCH_HARD = 12
#     ABILITY = 13
#     LOCATION = 14
#     PARENTHESIS_OPEN = 98
#     PARENTHESIS_CLOSE = 99

# class SMORuleOperation(IntEnum):
#     NONE = -1
#     AND = 0
#     OR = 1
#     PARENTHESIS_NONE = 2
#     PARENTHESIS_AND = 3
#     PARENTHESIS_OR = 4

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
cappy: list[str] = [items.cap_throw, items.up_throw, items.down_throw, items.spin_throw]
"""Temporary until item_group_names from __init__.py is properly working"""
@dataclasses.dataclass()
class CanCapture(Rule[TWorld], game="Super Mario Odyssey"):
    item_name: str | FieldResolver
    """The capture to check for"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(
            resolve_field(self.item_name, world, str),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        count = f", count={self.count}" if isinstance(self.count, FieldResolver) or self.count > 1 else ""
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name}{options})"

    class Resolved(Rule.Resolved):
        item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # implementation based on state.has
            return (state.prog_items[self.player][self.item_name] >= 0
                and state.has_any(cappy, self.player))

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: set()}



moon_rule_data : dict[str, Rule] = {
    #region Cap Moons
    loc.frog_jumping_above_the_fog: CanCapture(items.frog),
    loc.frog_jumping_from_the_top_deck: CanCapture(items.frog),
    loc.cap_kingdom_timer_challenge_1: HasAny(*cappy),
    loc.shopping_in_bonneton: True_(),
    loc.the_forgotten_treasure: Has(items.ground_pound),
    loc.taxi_flying_through_bonneton: CanCapture(items.binoculars),
    loc.bonnetter_blockade: CanCapture(items.paragoomba),
    loc.peach_in_the_cap_kingdom: And(CanReachRegion(SMOKingdoms.MUSHROOM), Has(items.jump)),
    loc.found_with_cap_kingdom_art: And(CanReachRegion(SMOKingdoms.MOON), Has(items.ground_pound)),
    #endregion

    #region Cap Moons Top of Top Hat Tower
    loc.good_evening_captain_toad: [],
    loc.cap_kingdom_regular_cup: [
        (SMORuleCondition.ABILITY, [items.jump], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Moons Moon Rock
    loc.next_to_glasses_bridge: [
        (SMORuleCondition.ABILITY, [items.jump], SMORuleOperation.NONE),
    ],
    loc.danger_sign: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE),
    ],
    loc.under_the_big_ones_brim: [
        (SMORuleCondition.ABILITY, [items.jump], SMORuleOperation.NONE),
    ],
    loc.fly_to_the_edge_of_the_fog: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.spin_the_hat_get_a_prize: [],
    loc.hidden_in_a_sunken_hat: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.dive], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.fog_shrouded_platform: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE),
    ],
    loc.bird_traveling_in_the_fog: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, None, SMORuleOperation.NONE),
    ],
    loc.caught_hopping_near_the_ship: [],
    loc.taking_notes_in_the_fog: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE),
    ],
    loc.cap_kingdom_timer_challenge_2: [],
    #endregion

    #region Cap Moons Top of Top Hat Tower Moon Rock
    loc.cap_kingdom_master_cup: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [items.long_jump], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [items.roll], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [SMORuleCondition.ABILITY], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [items.triple_jump], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Moons Poson Tide
    loc.skimming_the_poison_tide: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE),
    ],
    loc.slipping_through_the_poison_tide: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Moons Push Block
    loc.push_block_peril: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),

    ],
    loc.hidden_among_the_push_blocks: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),
    ],
    #endregion

    #region Cap Moons Frog Pond
    loc.searching_the_frog_pond: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY,
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.vault, items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE,
        [items.backflip, items.dive],
        [items.ground_pound_jump, items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.NONE),
        ],

    loc.secrets_of_the_frog_pond: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY,
         [items.vault, items.dive, items.wall_jump], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cap Moons Rolling Lane
    loc.roll_on_and_on: [],
    loc.precision_rolling: [],
    #endregion

    #region Cascade Moons
    loc.our_first_power_moon: [
    (SMORuleCondition.CAPTURE, [items.chain_chomp], SMORuleOperation.NONE)
    ],
    loc.chomp_through_the_rocks: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.chain_chomp], SMORuleOperation.NONE)

    ],
    loc.behind_the_waterfall: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.big_chain_chomp], SMORuleOperation.NONE),
    ],
    loc.multi_moon_atop_the_falls: [
        (SMORuleCondition.CAPTURE, [items.broodes_chain_chomp, items.t_rex], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.broodes_chain_chomp, items.big_chain_chomp], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.broodes_chain_chomp, items.backflip, items.dive, items.wall_jump, items.vault], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cascade Moons Post Peace Moons
    loc.treasure_of_the_waterfall_basin: [],
    loc.on_top_of_the_rubble: [],
    loc.cascade_kingdom_timer_challenge_1: [],
    loc.cascade_kingdom_regular_cup:[
        (SMORuleCondition.ABILITY, [items.roll_boost], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.long_jump], [items.triple_jump], [items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spin], [items.triple_jump], [items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [], SMORuleOperation.NONE),
    ],
    loc.shopping_in_fossil_falls:[],
    loc.sphynx_traveling_to_the_waterfall: [
        (SMORuleCondition.CAPTURE, [items.binoculars], SMORuleOperation.NONE),
    ],
    loc.above_a_high_cliff: [],
    loc.across_the_floating_isles: [],
    loc.cascade_kingdom_timer_challenge_2: [
        (SMORuleCondition.ABILITY, [items.triple_jump], [items.backflip], [items.side_flip],
        [items.ground_pound_jump],[items.spin],[items.double_jump, items.dive], [items.wall_jump, items.dive], SMORuleOperation.NONE),
    ],
    loc.good_morning_captain_toad:[],
    loc.caveman_cave_fan:[
        (SMORuleCondition.ITEM, [items.caveman_headwear, items.caveman_outfit], SMORuleOperation.NONE)
    ],
    loc.peach_in_the_cascade_kingdom: [
        (SMORuleCondition.REGION, SMORegion.mushroom_kingdom, SMORuleOperation.NONE)
    ],
    loc.secret_path_to_fossil_falls: [
        (SMORuleCondition.REGION, SMORegion.seaside_kingdom_peace, SMORuleOperation.AND),
        (SMORuleCondition.REGION, SMORegion.snow_kingdom_peace, SMORuleOperation.NONE),
    ],
    loc.a_tourist_in_the_cascade_kingdom: [
        (SMORuleCondition.REGION, SMORegion.sand_kingdom_peace, SMORuleOperation.AND),
        (SMORuleCondition.REGION, SMORegion.metro_kingdom_peace, SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Moons Moon Revisit Moons
    loc.rolling_rock_by_the_falls: [],
    #endregion

    #region Cascade Moons Moon Rock Moons
    loc.taking_notes_hurry_upward: [],
    loc.bottom_of_the_waterfall_basin: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.under_the_old_electrical_pole: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.caught_hopping_at_the_waterfall: [],
    loc.cascade_kingdom_master_cup: [
        (SMORuleCondition.ABILITY, [items.long_jump], [items.triple_jump], [items.dive], [items.roll_boost], SMORuleOperation.NONE)
    ],
    loc.next_to_the_stone_arch: [],
    loc.guarded_by_a_colossal_fossil: [],
    loc.inside_the_busted_fossil:[

    ],
    loc.treasure_under_the_cliff: [],
    loc.under_the_ground: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.PARENTHESIS_NONE)
    ],
    #endregion

    #region Cascade Kingdom T-Rex Nest Moons
    loc.dinosaur_nest_big_cleanup: [],
    loc.dinosaur_nest_running_wild: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Kingdom Chain Chomp Cave Moons
    loc.nice_shot_with_the_chain_chomp: [
        (SMORuleCondition.CAPTURE, [items.chain_chomp], SMORuleOperation.NONE)
    ],
    loc.very_nice_shot_with_the_chain_chomp:[
        (SMORuleCondition.CAPTURE, [items.chain_chomp], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cascade Kingdom Chasm Lifts Moons
    loc.past_the_chasm_lifts:[],
    loc.hidden_chasm_passage:[],
    #endregion

    #region Cascade Kingdom Gusty Bridges Moons
    loc.across_the_gusty_bridges: [],
    loc.flying_far_away_from_gusty_bridges: [],
    #endregion

    #region Cascade Kingdom Mysterious Clouds Moons
    loc.across_the_mysterious_clouds: [],
    loc.atop_a_wall_among_the_clouds: [],
    #endregion

    #region Sand Kingdom Moons
    loc.atop_the_highest_tower: [],
    loc.moon_shards_in_the_sand: [],
    loc.overlooking_the_desert_town: [],
    loc.alcove_in_the_ruins: [],
    loc.on_the_leaning_pillar: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [], SMORuleOperation.NONE),
    ],
    loc.hidden_room_in_the_flowing_sands: [],
    loc.secret_of_the_mural: [],
    loc.on_top_of_stone_archway: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.spark_pylon], SMORuleOperation.NONE),
    ],
    loc.from_a_crate_in_the_ruins: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.long_jump], [items.dive], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], [items.triple_jump], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [], SMORuleOperation.NONE)
    ],
    loc.where_the_birds_gather: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.top_of_a_dune: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.lost_in_the_luggage: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.inside_a_block_is_a_hard_place: [],
    loc.the_treasure_of_jaxi_ruins: [],
    loc.bird_traveling_the_desert: [],
    loc.desert_gardening_plaza_seed: [],
    loc.desert_gardening_ruins_seed: [],
    loc.desert_gardening_seed_on_the_cliff: [],
    loc.taking_notes_jump_on_the_palm: [
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [], SMORuleOperation.NONE)
    ],
    loc.among_the_five_cactuses: [],
    loc.wandering_cactus: [
        SMORuleCondition.CAPTURE, [items.cactus], SMORuleOperation.NONE
    ],
    loc.found_with_bowsers_kingdom_art: [
        (SMORuleCondition.REGION, [SMORegion.bowsers_kingdom], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.ground_pound],  SMORuleOperation.PARENTHESIS_NONE)
    ],
    #endregion

    #region Sand Kingdom Inverted Pyramid Mural
    loc.secret_of_the_inverted_mural: [],
    #endregion

    #region Sand Kingdom Inverted Pyramid Upper
    loc.hidden_room_in_the_inverted_pyramid: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        #needs to be tested with people
    ],
    #endregion

    #region Sand Kingdom Inverted Pyramid Top
    loc.showdown_on_the_inverted_pyramid: [],
    loc.on_the_statues_tail: [],
    loc.on_the_lone_pillar: [],
    #waiting for kgamer
    #endregion

    #region Sand Kingdom Night Sand
    loc.bullet_bill_breakthrough: [],
    loc.secret_path_to_new_donk_city: [],
    #endregion

    #region Sand Kingdom Underground Ruins
    loc.underground_treasure_chest: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.dive], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.backflip], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.ground_pound_jump], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.ledge_grab], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.spin], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.bullet_bill, items.side_flip], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD,  [items.ground_pound_jump, items.vault, items.dive, items.roll, items.up_throw, items.down_throw], SMORuleOperation.NONE)
    ],
    loc.goomba_tower_assembly: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [items.ground_pound, items.vault, items.dive, items.roll], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Deepest Underground
    loc.the_hole_in_the_desert: [
        (SMORuleCondition.CAPTURE, [items.knucklotecs_fist, items.bullet_bill], SMORuleOperation.OR,),
        (SMORuleCondition.TRICK_HARD, [items.ground_pound_jump, items.vault, items.dive, items.roll, items.up_throw, items.down_throw, items.knucklotecs_fist], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Post Peace
    loc.hang_your_hat_on_the_fountain: [],
    loc.bird_traveling_wastes: [],
    loc.sand_kingdom_timer_challenge_2: [],
    loc.sand_kingdom_timer_challenge_1: [
        (SMORuleCondition.CAPTURE, [items.spark_pylon], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.roll, items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_EASY, [items.crouch, items.wall_jump, items.dive, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump, items.dive, items.vault], SMORuleOperation.NONE)
    ],
    loc.sand_kingdom_timer_challenge_3: [],
    loc.found_in_the_sand_good_dog: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.herding_sheep_in_the_dunes: [],
    loc.fishing_in_the_oasis: [
        (SMORuleCondition.CAPTURE, [items.lakitu], SMORuleOperation.NONE)
    ],
    loc.love_in_the_heart_of_the_desert: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.NONE)
    ],
    loc.youre_quite_a_catch_captain_toad: [
        (SMORuleCondition.CAPTURE, [items.lakitu], SMORuleOperation.NONE)
    ],
    loc.jaxi_reunion: [],
    loc.walking_the_desert: [],
    #endregion

    #region Sand Kingdom Top of Inverted Pyramid Post Peace
    loc.the_lurker_under_the_stone: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.welcome_back_jaxi: [],
    #endregion

    #region Sand Kingdom Sand Shop
    loc.shopping_in_tostarena: [],
    #endregion

    #region Sand Kingdom Slots
    loc.sand_kingdom_slots: [],
    #endregion

    #region Sand Kingdom Moe Eye Sub Area
    loc.the_invisible_maze: [],
    loc.skull_sign_in_the_transparent_maze: [],
    #endregion

    #region Sand Kingdom Bullet Bill Maze
    loc.the_bullet_bill_maze_break_through: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.the_bullet_bill_maze_side_path: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE),
    ],
    #endregion

    #region Sand Kingdom Jaxi Ruins
    loc.jaxi_driver: [],
    loc.jaxi_stunt_driving: [],
    #endregion

    #region Sand Kingdom Strange Neighborhood
    loc.strange_neighborhood: [],
    loc.above_a_strange_neighborhood: [],
    #endregion

    #region Sand Kingdom Sand Rumble
    loc.a_rumble_from_the_sandy_floor: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Employees Only
    loc.employees_only: [],
    #endregion

    #region Sand Kingdom Ice Cave
    loc.ice_cave_treasure: [
        (SMORuleCondition.ABILITY, [items.wall_jump], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Sphynx Vault
    loc.sphynxs_hidden_vault: [],
    #endregion

    #region Sand Kingdom Deepest Underground Peace
    loc.under_the_mummys_curse: [],
    #endregion

    #region Sand Kingdom Deepest Underground Post Game
    loc.binding_band_returned: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Moe Eye Floor
    loc.where_the_transparent_platforms_end: [],
    loc.jump_onto_the_transparent_lift: [],
    #endregion

    #region Sand Kingdom Colassal Ruins
    loc.colossal_ruins_dash_jump: [
        (SMORuleCondition.CAPTURE, [items.spark_pylon], SMORuleOperation.NONE)
    ],
    loc.sinking_colossal_ruins_hurry: [
        (SMORuleCondition.CAPTURE, [items.spark_pylon], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Sand Outfit
    loc.dancing_with_new_friends: [],
    #endregion

    #region Sand Kingdom Sand Kingdom Moon Rock
    loc.jammin_in_the_sand_kingdom: [],
    loc.hat_and_seek_in_the_sand: [],
    loc.sand_kingdom_regular_cup: [],
    loc.sand_kingdom_master_cup: [],
    loc.round_the_world_tourist: [],
    loc.peach_in_the_sand_kingdom: [],
    loc.mighty_leap_from_the_palm_tree: [],
    loc.on_the_north_pillar: [
        (SMORuleCondition.CAPTURE, [items.spark_pylon], SMORuleOperation.NONE)
    ],
    loc.into_the_flowing_sands: [],
    loc.in_the_skies_above_the_canyon: [],
    loc.island_in_the_poison_swamp: [],
    loc.an_invisible_gleam: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.on_the_eastern_pillar: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.NONE)
    ],
    loc.caught_hopping_in_the_desert: [],
    loc.poster_cleanup: [],
    loc.taking_notes_running_down: [],
    loc.taking_notes_in_the_wall_painting: [],
    loc.love_at_the_edge_of_the_desert: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.NONE)
    ],
    loc.more_walking_in_the_desert: [],
    #endregion

    #region Sand Kingdom Freezing Waterway
    loc.through_the_freezing_waterway: [
        (SMORuleCondition.CAPTURE, [items.gushen], SMORuleOperation.NONE)
    ],
    loc.freezing_waterway_hidden_room: [
        (SMORuleCondition.CAPTURE, [items.gushen], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Odyssey
    loc.on_the_lakeshore: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.taking_notes_dive_and_swim: [],
    #endregion

    #region Lake Kingdom Main
    loc.dorrie_back_rider: [],
    loc.cheep_cheep_crossing: [],
    loc.whats_in_the_box: [],
    loc.from_the_broken_pillar: [
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.OR),
        (SMORuleCondition.CAPTURE, [items.cheep_cheep], SMORuleOperation.NONE)
    ],
    loc.moon_shards_in_the_lake: [],
    loc.taking_notes_in_the_cliffside: [],
    loc.our_secret_little_room: [],
    loc.lets_go_swimming_captain_toad: [
        (SMORuleCondition.CAPTURE, [items.cheep_cheep], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.shopping_in_lake_lamode: [],
    loc.i_feel_underdressed: [],
    loc.secret_path_to_lake_lamode: [],
    loc.lake_fishing: [
        (SMORuleCondition.CAPTURE, [items.lakitu], SMORuleOperation.NONE)
    ],
    loc.i_met_a_lake_cheep_cheep: [
        (SMORuleCondition.CAPTURE, [items.cheep_cheep], SMORuleOperation.NONE)
    ],
    loc.broodals_over_the_lake: [],
    loc.end_of_the_hidden_passage: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.treasure_in_the_spiky_waterway: [],
    loc.lake_gardening_spiky_passage_seed: [],
    #endregion

    #region Lake Kingdom Moon Rock
    loc.behind_the_floodgate: [],
    loc.high_flying_leap: [],
    loc.deep_deep_down: [
        (SMORuleCondition.CAPTURE, [items.cheep_cheep], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.rooftop_of_the_water_plaza: [
        (SMORuleCondition.ABILITY, [items.climb, items.ground_pound], SMORuleOperation.OR)
        (SMORuleCondition.TRICK_EASY, [items.spin, items.ledge_grab, items.ground_pound], [items.spin, items.ledge_grab, items.ground_pound],
        [items.backflip, items.ledge_grab , items.ground_pound], [items.ground_pound_jump, items.ledge_grab, items.ground_pound],
        [items.triple_jump, items.ground_pound], [items.dive, items.ground_pound], [items.vault, items.ground_pound], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.bird_traveling_over_the_lake: [],
    loc.love_by_the_lake: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regular_cup: [
        (SMORuleCondition.CAPTURE, [items.cheep_cheep, items.zipper], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_master_cup: [
        (SMORuleCondition.CAPTURE, [items.cheep_cheep, items.zipper], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.taxi_flying_through_lake_lamode: [
        (SMORuleCondition.CAPTURE, [items.binoculars], SMORuleOperation.NONE)
    ],
    loc.that_trendy_pirate_look: [],
    loc.space_is_in_right_now: [],
    loc.that_old_west_style: [],
    loc.peach_in_the_lake_kingdom: [],
    loc.found_with_lake_kingdom_art: [
        (SMORuleCondition.ABILITY, [items.climb, items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_timer_challenge_1: [],
    loc.lake_kingdom_timer_challenge_2: [
        (SMORuleCondition.ABILITY, [items.wall_jump, items.dive], [items.spin, items.ledge_grab], [items.ground_pound_jump, items.ledge_grab]
         [items.ground_pound_jump, items.dive], [items.side_flip, items.ledge_grab], [items.side_flip, items.dive], [items.triple_jump, items.ledge_grab],
         [items.triple_jump, items.dive], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Poison Swamp
    loc.waves_of_poison_hoppin_over: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.NONE)
    ],
    loc.waves_of_poison_hop_to_it: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Zipper Chasm
    loc.unzip_the_chasm: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault], SMORuleOperation.NONE)
    ],
    loc.super_secret_zipper: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Bouncy Flowers
    loc.jump_grab_cling_and_climb: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    loc.jump_grab_and_climb_some_more: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Arch Repair
    loc.a_successful_repair_job: [
        (SMORuleCondition.CAPTURE, [items.puzzle_part_lake_kingdom], SMORuleOperation.NONE)
    ],
    #endregion

    #region Wooded Kingdom Moons
    loc.road_to_sky_garden: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump, items.wall_jump, items.dive], [items.long_jump, items.wall_jump, items.dive], SMORuleOperation.NONE)
    ],
    loc.rolling_rock_in_the_woods: [],
    loc.caught_hopping_in_the_forest: [],
    loc.atop_a_tall_tree: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump, items.vault, items.ledge_grab], SMORuleOperation.NONE),
    ],
    loc.tucked_away_inside_a_tunnel: [
        (SMORuleCondition.CAPTURE, [items.uproot], [items.fire_bro], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.wall_jump, items.backflip],[items.vault, items.dive, items.backflip], [items.ground_pound_jump, items.wall_jump],
        [items.ground_pound_jump, items.dive, items.vault], [items.triple_jump, items.wall_jump], [items.triple_jump, items.vault, items.dive], SMORuleOperation.NONE),
    ],
    loc.the_nut_in_the_red_maze:[
         (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault, items.wall_jump], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump, items.wall_jump, items.dive], [items.long_jump, items.wall_jump, items.dive], SMORuleOperation.NONE)
    ],
    loc.the_nut_at_the_dead_end: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump, items.wall_jump, items.dive], [items.long_jump, items.wall_jump, items.dive], SMORuleOperation.NONE)
    ],
    loc.the_nut_round_the_corner: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.wall_jump, items.backflip, items.dive],[items.vault, items.dive, items.backflip], [items.ground_pound_jump, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive, items.vault], [items.triple_jump, items.wall_jump, items.dive], [items.triple_jump, items.vault, items.dive], SMORuleOperation.NONE),
    ],
    loc.fire_in_the_cave: [],
    loc.shopping_in_steam_gardens: [],
    loc.cracked_nut_on_a_crumbling_tower: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.dive, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump, items.wall_jump, items.dive], [items.long_jump, items.wall_jump, items.dive], SMORuleOperation.NONE)
    ],
    loc.climb_the_cliff_to_get_the_nut: [
        (SMORuleCondition.CAPTURE, [items.uproot], [items.fire_bro], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.wall_jump], SMORuleOperation.OR),
    ],
    #endregion

    #region Sky Garden Tower
    loc.nut_planted_in_the_tower: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [], SMORuleOperation.NONE)
    ],
    loc.stretching_your_legs: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    #endregion

    #region Top of Wooded Kingdom
    loc.flower_thieves_of_sky_garden: [],
    #endregion

    #region Wooded Kingdom Post Broodals
    loc.path_to_the_secret_flower_field: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.behind_the_rock_wall: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.back_way_up_the_mountain: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.thanks_for_the_charge: [
        (SMORuleCondition.ABILITY, [items.climb, items.ground_pound], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive, items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.over_the_cliffs_edge: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.the_nut_that_grew_on_the_tall_fence: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.love_in_the_forest_ruins: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault, items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.backflip, items.wall_jump], SMORuleOperation.PARENTHESIS_NONE)
    ],
    #endregion

    #region Wooded Kingdom Peace
    loc.hey_out_there_captain_toad: [
        (SMORuleCondition.CAPTURE, [items.glydon], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive, items.vault, items.ground_pound, items.roll], SMORuleOperation.NONE)
    ],
    loc.inside_the_rock_in_the_forest: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.NONE)
    ],
    loc.wooded_kingdom_timer_challenge_1: [],
    loc.wooded_kingdom_timer_challenge_2: [
        (SMORuleCondition.ABILITY, [items.downthrow], SMORuleOperation.NONE)
    ],
    loc.swing_around_secret_flower_field: [],
    loc.jammin_in_the_wooded_kingdom: [],
    loc.wooded_kingdom_regular_cup: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive, items.vault, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.peach_in_the_wooded_kingdom: [
        (SMORuleCondition.REGION, [SMORegion.mushroom_kingdom], SMORuleOperation.NONE)
    ],
    loc.secret_path_to_the_steam_gardens: [],
    loc.found_with_wooded_kingdom_art: [
        (SMORuleCondition.REGION, [SMORegion.sand_kingdom], SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, [items.ground_pound], SMORuleOperation.NONE)
    ],
    #endregion

    #region Wooded Kingdom Moon Rock
    loc.high_up_in_the_cave: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.backflip, items.dive, items.triple_jump], SMORuleOperation.NONE)
    ],
    loc.lost_in_the_tall_trees: [
        (SMORuleCondition.CAPTURE, [items.glydon], SMORuleOperation.NONE)
    ],
    loc.looking_down_on_the_goombas: [
        (SMORuleCondition.CAPTURE, [items.glydon], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_HARD, [items.vault, items.dive, items.roll, items.ground_pound], SMORuleOperation.NONE)
    ],
    loc.high_up_on_a_rock_wall: [],
    loc.the_nut_in_the_robot_storeroom: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.climb], SMORuleOperation.NONE)
    ],
    loc.above_the_iron_mountain_path: [],
    loc.the_nut_under_the_observation_deck: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.bird_traveling_the_forest: [],
    loc.invader_in_the_sky_garden: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.ground_pound_jump, items.dive], SMORuleOperation.NONE)
    ],
    loc.hot_hot_hot_from_the_campfire: [
        (SMORuleCondition.CAPTURE, [items.fire_bro], SMORuleOperation.NONE)
    ],
    loc.wooded_kingdom_timer_challenge_3: [],
    loc.moon_shards_in_the_forest: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    loc.taking_notes_on_top_of_the_wall: [
        (SMORuleCondition.ABILITY, [items.roll], SMORuleOperation.NONE)
    ],
    loc.taking_notes_stretching: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    loc.wooded_kingdom_master_cup: [
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive, items.vault, items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.i_met_an_uproot: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    #endregion

    #region Deep Woods Treasure Trap
    loc.deep_woods_treasure_trap: [],
    #endregion

    #region Explorer Outfit
    loc.exploring_for_treasure: [],
    #endregion

    #region Flooding Pipeway
    loc.flooding_pipeway: [],
    loc.flooding_pipeway_ceiling_secret: [
        (SMORuleCondition.ABILITY, [items.wall_jump], SMORuleOperation.NONE)
    ],
    #endregion

    #region Wooded Flower Road
    loc.flower_road_run: [
        (SMORuleCondition.ABILITY, [items.wall_jump], SMORuleOperation.NONE)
    ],
    loc.flower_road_reach: [
        (SMORuleCondition.ABILITY, [items.vault], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sherm Elevator
    loc.elevator_escalation: [],
    loc.elevator_blind_spot: [
        (SMORuleCondition.CAPTURE, [items.sherm], SMORuleOperation.NONE)
    ],
    #endregion

    #region Fog Wondering
    loc.wandering_in_the_fog: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.nut_hidden_in_the_fog: [],
    #endregion

    #region Walking on Clouds
    loc.walking_on_clouds: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    loc.above_the_clouds: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    #endregion

    #region Secret Flower Field
    loc.defend_the_secret_flower_field: [
        (SMORuleCondition.CAPTURE, [items.uproot], SMORuleOperation.NONE)
    ],
    #endregion

    #region Secret Flower Field Peace
    loc.make_the_secret_flower_field_bloom: [
        (SMORuleCondition.ABILITY, [items.spin_throw], SMORuleOperation.NONE)
    ],
    #endregion

    #region Deep Woods
    loc.rolling_rock_in_the_deep_woods: [],
    loc.glowing_in_the_deep_woods: [],
    loc.past_the_peculiar_pipes: [],
    loc.by_the_babbling_brook_in_the_deep_woods: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.NONE)
    ],
    loc.the_hard_rock_in_deep_woods: [
        (SMORuleCondition.CAPTURE, [items.t_rex], SMORuleOperation.NONE)
    ],
    loc.a_treasure_made_of_coins: [
        (SMORuleCondition.CAPTURE, [items.coin_coffer], SMORuleOperation.NONE)
    ],
    loc.beneath_the_roots_of_a_moving_tree: [
        (SMORuleCondition.CAPTURE, [items.tree], SMORuleOperation.NONE)
    ],
    #endregion

    #region Nut Room
    loc.spinning_platforms_treasure: [],
    #endregion

    #region Invisible Road
    loc.invisible_road_danger: [],
    loc.invisible_road_hidden_room: [],
    #endregion

    #region Sheep Herding
    loc.herding_sheep_above_the_forest_fog: [],
    loc.herding_sheep_on_the_iron_bridge: [],
    #endregion

    #region Breakdown Road
    loc.down_and_back_breakdown_road: [],
    loc.below_breakdown_road: [
        (SMORuleCondition.CAPTURE, [items.banzai_bill], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cloud Kingdom Boss Fight
    loc.beat_bowser_in_cloud: [],
    #endregion

    #region Cloud Kingdom Revisit
    loc.peach_in_the_cloud_kingdom: [],
    #endregion

    #region Cloud Kingdom Moon Rock
    loc.digging_in_the_cloud: [
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.high_high_above_the_clouds: [
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.crossing_the_cloud_sea: [],
    loc.taking_notes_up_and_down: [
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    #endregion

    #region Cloud Picture Match
    loc.picture_match_basically_a_goomba: [
        (SMORuleCondition.CAPTURE, (items.picture_match_part_goomba), SMORuleOperation.NONE)
    ],
    #endregion

    #region Cloud Picture Match Post Game
    loc.picture_match_a_stellar_goomba: [
        (SMORuleCondition.CAPTURE, (items.picture_match_part_goomba), SMORuleOperation.NONE)
    ],
    #endregion

    #region King of the Cube
    loc.king_of_the_cube: [],
    loc.the_sixth_face: [],
    #endregion

    #region Lost Kingdom
    loc.atop_a_propeller_pillar: [],
    loc.below_the_cliffs_edge: [],
    loc.inside_the_stone_cage: [],
    loc.on_a_tree_in_the_swamp: [],
    loc.over_the_fuzzies_above_the_swamp: [],
    loc.avoiding_fuzzies_inside_the_wall: [],
    loc.inside_the_rising_stone_pillar: [],
    loc.enjoying_the_view_of_forgotten_isle: [],
    loc.on_the_mountain_road: [],
    loc.a_propeller_pillars_secret: [],
    loc.wrecked_rock_block: [],
    loc.a_butterflys_treasure: [],
    loc.caught_hopping_in_the_jungle: [],
    loc.cave_gardening: [
        (SMORuleCondition.ABILITY, (items.spin_throw), SMORuleOperation.NONE)
    ],
    loc.moon_shards_in_the_jungle: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.NONE),
    ],
    loc.peeking_out_from_under_the_bridge: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.NONE),
    ],
    loc.twist_n_turn_up_treasure: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.NONE),
    ],
    loc.soaring_over_the_forgotten_isle: [
        (SMORuleCondition.CAPTURE, (items.glydon), SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, (items.vault, items.dive, items.roll, items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.the_caged_gold: [],
    loc.get_some_rest_captain_toad: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    loc.shopping_on_forgotten_isle: [
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    #endregion

    #region Lost Kingdom Revisit
    loc.taxi_flying_through_forgotten_isle: [
        (SMORuleCondition.CAPTURE, (items.binoculars), SMORuleOperation.NONE)
    ],
    loc.i_met_a_tropical_wiggler: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.OR),
    ],
    loc.lost_kingdom_regular_cup: [
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    loc.peach_in_the_lost_kingdom: [
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    #endregion

    #region Lost Kingdom Moon Rock
    loc.the_shining_fruit: [],
    loc.jump_down_to_the_top_of_a_tree: [],
    loc.line_it_up_blow_it_up: [],
    loc.taking_notes_stretch_and_shrink: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.OR),
    ],
    loc.lost_kingdom_master_cup: [
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    loc.lost_kingdom_timer_challenge: [
        (SMORuleCondition.ABILITY, (items.climb), SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, (), SMORuleOperation.NONE)
    ],
    #endregion

    #region Tropical Wiggler Swamp
    loc.stretch_and_traverse_the_jungle: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, (), SMORuleOperation.NONE)
    ],
    loc.aglow_in_the_jungle: [
        (SMORuleCondition.CAPTURE, (items.tropical_wiggler), SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, (), SMORuleOperation.NONE)
    ],
    #endregion

    #region Kelpto Lava Bath
    loc.chasing_klepto: [
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.extremely_hot_bath: [
        (SMORuleCondition.CAPTURE, (items.lava_bubble), SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    #endregion

    #region Night Metro Kingdom Building Top
    loc.new_donk_citys_pest_problem: [
        (SMORuleCondition.CAPTURE, items.sherm, SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    #endregion

    #region Night Metro
    loc.inside_an_iron_girder: [],
    loc.swaying_in_the_breeze: [],
    loc.girder_sandwich: [
        (SMORuleCondition.CAPTURE, (items.sherm), SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_EASY, (items.dive, items.vault, items.wall_jump, items.double_jump), SMORuleOperation.NONE)
    ],
    #endregion

    #region Day Metro
    loc.drummer_on_board: [],
    loc.guitarist_on_board: [],
    loc.bassist_on_board: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.NONE)
    ],
    loc.trumpeter_on_board: [
        (SMORuleCondition.ABILITY, (items.ground_pound), (items.vault, items.dive))
    ],
    loc.a_traditional_festival: [],
    loc.glittering_above_the_pool: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.NONE)
    ],
    loc.dizzying_heights: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, (items.climb), SMORuleOperation.NONE)
    ],
    loc.secret_girder_tunnel: [],
    loc.who_piled_garbage_on_this: [
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.hidden_in_the_scrap: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.left_at_the_cafe: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.how_do_they_take_out_the_trash: [
        (SMORuleCondition.CAPTURE, (items.spark_pylon), SMORuleOperation.NONE)
    ],
    loc.city_gardening_building_planter: [],
    loc.city_gardening_plaza_planter: [],
    loc.city_gardening_rooftop_planter: [
        (SMORuleCondition.ABILITY, (items.wall_jump), SMORuleOperation.NONE)
    ],
    loc.how_you_doin_captain_toad: [],
    loc.free_parking_rooftop_hop: [],
    loc.bench_friends: [],
    loc.jump_rope_hero: [],
    loc.jump_rope_genius: [],
    loc.remotely_captured_car: [
        (SMORuleCondition.CAPTURE, (items.rc_car), SMORuleOperation.NONE)
    ],
    loc.found_with_metro_kingdom_art: [
        (SMORuleCondition.REGION, (SMORegion.lake_kingdom), SMORuleOperation.AND),
        (SMORuleCondition.ABILITY, (items.ground_pound), SMORuleOperation.NONE)
    ],
    loc.celebrating_in_the_streets: [],
    #endregion

    #region Metro Kingdom Post Peace

    }



regional_rule_data : dict[str, Rule] = {
    #region Cap Kingdom Regional Coins
    loc.cap_kingdom_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE),
    ],
    loc.cap_kingdom_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.cap_kingdom_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.cap_kingdom_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.cap_kingdom_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.cap_kingdom_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.cap_kingdom_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.cap_kingdom_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.cap_kingdom_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.cap_kingdom_regional_coin_8: [
        (SMORuleCondition.CAPTURE, [items.paragoomba], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_AND),
    (SMORuleCondition.TRICK_EASY, [items.dive], SMORuleOperation.PARENTHESIS_NONE)
    ],
    loc.cap_kingdom_regional_coin_group_3: [],
    loc.cap_kingdom_regional_coin_9: [],
    loc.cap_kingdom_regional_coin_10: [],
    loc.cap_kingdom_regional_coin_11: [],
    loc.cap_kingdom_regional_coin_12: [],
    loc.cap_kingdom_regional_coin_group_4: [],
    loc.cap_kingdom_regional_coin_13: [],
    loc.cap_kingdom_regional_coin_14: [],
    loc.cap_kingdom_regional_coin_15: [],
    loc.cap_kingdom_regional_coin_16: [],
    loc.cap_kingdom_regional_coin_group_5: [],
    loc.cap_kingdom_regional_coin_17: [],
    loc.cap_kingdom_regional_coin_18: [],
    loc.cap_kingdom_regional_coin_19: [],
    loc.cap_kingdom_regional_coin_group_6: [],
    loc.cap_kingdom_regional_coin_20: [],
    loc.cap_kingdom_regional_coin_21: [],
    loc.cap_kingdom_regional_coin_22: [],
    loc.cap_kingdom_regional_coin_group_7: [],
    loc.cap_kingdom_regional_coin_23: [],
    loc.cap_kingdom_regional_coin_24: [],
    loc.cap_kingdom_regional_coin_25: [],
    loc.cap_kingdom_regional_coin_group_8: [],
    loc.cap_kingdom_regional_coin_26: [],
    loc.cap_kingdom_regional_coin_27: [],
    loc.cap_kingdom_regional_coin_28: [],
    loc.cap_kingdom_regional_coin_group_9: [],
    loc.cap_kingdom_regional_coin_29: [],
    loc.cap_kingdom_regional_coin_30: [],
    loc.cap_kingdom_regional_coin_31: [],
    #endregion

    #region Top Hat Tower Regional Coins
    loc.top_hat_tower_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.top_hat_tower_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.top_hat_tower_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.top_hat_tower_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.top_hat_tower_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.backflip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.ledge_grab], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.TRICK_HARD, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_HARD, [items.triple_jump], SMORuleOperation.PARENTHESIS_OR),
    ],
    loc.top_hat_tower_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    loc.top_hat_tower_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    loc.top_hat_tower_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    loc.top_hat_tower_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    loc.top_hat_tower_regional_coin_8: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    loc.top_hat_tower_regional_coin_9: [
        (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.triple_jump], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.vault], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.wall_jump], SMORuleOperation.PARENTHESIS_OR),
        (SMORuleCondition.ENTRANCE, [SMOEntranceData.top_hat_tower_end], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.dive], SMORuleOperation.PARENTHESIS_AND),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.up_throw], SMORuleOperation.PARENTHESIS_NONE),
    ],
    #endregion

    #region Cap Kingdom Frog Pond Regional Coins
    loc.frog_pond_regional_coin_group_1: [
    (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.dive, items.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [items.backflip, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [items.vault, items.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    loc.frog_pond_regional_coin_1: [
    (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.dive, items.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [items.backflip, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [items.vault, items.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    loc.frog_pond_regional_coin_2: [
    (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.dive, items.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [items.backflip, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [items.vault, items.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    loc.frog_pond_regional_coin_3: [
    (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.dive, items.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [items.backflip, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [items.vault, items.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    loc.frog_pond_regional_coin_4: [
    (SMORuleCondition.CAPTURE, [items.frog], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_EASY, [
        [items.dive, items.backflip, items.vault],
        [items.ground_pound_jump, items.dive, items.vault],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_INTERMEDIATE, [
        [items.backflip, items.wall_jump, items.dive],
        [items.ground_pound_jump, items.dive],
    ], SMORuleOperation.OR),
    (SMORuleCondition.TRICK_HARD, [
        [items.vault, items.wall_jump],
    ], SMORuleOperation.NONE),
    ],
    #endregion

    #region Cap Kingdom Poison Tides Regional Coins
    loc.poison_tides_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE,[items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.poison_tides_regional_coin_1: [
        (SMORuleCondition.CAPTURE,[items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.poison_tides_regional_coin_2: [
        (SMORuleCondition.CAPTURE,[items.paragoomba], SMORuleOperation.NONE)
    ],
    loc.poison_tides_regional_coin_3: [
        (SMORuleCondition.CAPTURE,[items.paragoomba], SMORuleOperation.NONE)
    ],
    #endregion

    #region Cap Kingdom Push Block Regional Coins
    loc.pushblocks_regional_coin_group_1: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),
    ],
    loc.pushblocks_regional_coin_1: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),
    ],
    loc.pushblocks_regional_coin_2: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),
    ],
    loc.pushblocks_regional_coin_3: [
        (SMORuleCondition.ABILITY,
        [items.spark_pylon, items.double_jump],
        [items.spark_pylon, items.vault],
        [items.spark_pylon, items.wall_jump],
        [items.spark_pylon, items.dive],
        [items.spark_pylon, items.side_flip], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_EASY,
        [items.spark_pylon, items.ledge_grab], SMORuleOperation.NONE),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.spark_pylon], SMORuleOperation.OR),
    ],
    #endregion

    #region Cascade Kingdom Regional Coins
    loc.cascade_kingdom_regional_coin_group_1: [],
    loc.cascade_kingdom_regional_coin_1: [],
    loc.cascade_kingdom_regional_coin_2: [],
    loc.cascade_kingdom_regional_coin_3: [],
    loc.cascade_kingdom_regional_coin_group_2: [],
    loc.cascade_kingdom_regional_coin_4: [],
    loc.cascade_kingdom_regional_coin_5: [],
    loc.cascade_kingdom_regional_coin_6: [],
    loc.cascade_kingdom_regional_coin_group_3: [],
    loc.cascade_kingdom_regional_coin_7: [],
    loc.cascade_kingdom_regional_coin_8: [],
    loc.cascade_kingdom_regional_coin_9: [],
    loc.cascade_kingdom_regional_coin_group_4: [],
    loc.cascade_kingdom_regional_coin_10: [],
    loc.cascade_kingdom_regional_coin_11: [],
    loc.cascade_kingdom_regional_coin_12: [],
    loc.cascade_kingdom_regional_coin_group_5: [],
    loc.cascade_kingdom_regional_coin_13: [],
    loc.cascade_kingdom_regional_coin_14: [],
    loc.cascade_kingdom_regional_coin_15: [],
    loc.cascade_kingdom_regional_coin_group_6: [],
    loc.cascade_kingdom_regional_coin_16: [],
    loc.cascade_kingdom_regional_coin_17: [],
    loc.cascade_kingdom_regional_coin_18: [],
    loc.cascade_kingdom_regional_coin_group_7: [],
    loc.cascade_kingdom_regional_coin_19: [],
    loc.cascade_kingdom_regional_coin_20: [],
    loc.cascade_kingdom_regional_coin_21: [],
    loc.cascade_kingdom_regional_coin_group_8: [],
    loc.cascade_kingdom_regional_coin_22: [],
    loc.cascade_kingdom_regional_coin_23: [],
    loc.cascade_kingdom_regional_coin_24: [],
    loc.cascade_kingdom_regional_coin_group_9: [],
    loc.cascade_kingdom_regional_coin_25: [],
    loc.cascade_kingdom_regional_coin_26: [],
    loc.cascade_kingdom_regional_coin_27: [],
    #endregion

    #region Cascade Kingdom Post Peace Regional Coins
    loc.cascade_kingdom_regional_coin_group_10: [],
    loc.cascade_kingdom_regional_coin_28: [],
    loc.cascade_kingdom_regional_coin_29: [],
    loc.cascade_kingdom_regional_coin_30: [],
    loc.cascade_kingdom_regional_coin_31: [],
    loc.cascade_kingdom_regional_coin_group_11: [],
    loc.cascade_kingdom_regional_coin_32: [],
    loc.cascade_kingdom_regional_coin_33: [],
    loc.cascade_kingdom_regional_coin_34: [],
    loc.cascade_kingdom_regional_coin_group_12: [],
    loc.cascade_kingdom_regional_coin_35: [],
    loc.cascade_kingdom_regional_coin_36: [],
    loc.cascade_kingdom_regional_coin_37: [],
    loc.cascade_kingdom_regional_coin_group_13: [],
    loc.cascade_kingdom_regional_coin_38: [],
    loc.cascade_kingdom_regional_coin_39: [],
    loc.cascade_kingdom_regional_coin_40: [],
    loc.cascade_kingdom_regional_coin_group_14: [],
    loc.cascade_kingdom_regional_coin_41: [],
    loc.cascade_kingdom_regional_coin_42: [],
    loc.cascade_kingdom_regional_coin_43: [],
    loc.cascade_kingdom_regional_coin_group_15: [],
    loc.cascade_kingdom_regional_coin_44: [],
    loc.cascade_kingdom_regional_coin_45: [],
    loc.cascade_kingdom_regional_coin_46: [],
    #endregion

    #region Cascade Kingdom Chasm Lifts Regional Coins
    loc.chasm_lifts_regional_coin_group_1: [],
    loc.chasm_lifts_regional_coin_1: [],
    loc.chasm_lifts_regional_coin_2: [],
    loc.chasm_lifts_regional_coin_3: [],
    loc.chasm_lifts_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Regional Coins
    loc.sand_kingdom_regional_coin_group_1: [],
    loc.sand_kingdom_regional_coin_1: [],
    loc.sand_kingdom_regional_coin_2: [],
    loc.sand_kingdom_regional_coin_3: [],
    loc.sand_kingdom_regional_coin_group_2: [],
    loc.sand_kingdom_regional_coin_4: [],
    loc.sand_kingdom_regional_coin_5: [],
    loc.sand_kingdom_regional_coin_6: [],
    loc.sand_kingdom_regional_coin_group_3: [],
    loc.sand_kingdom_regional_coin_7: [],
    loc.sand_kingdom_regional_coin_8: [],
    loc.sand_kingdom_regional_coin_9: [],
    loc.sand_kingdom_regional_coin_group_4: [],
    loc.sand_kingdom_regional_coin_10: [],
    loc.sand_kingdom_regional_coin_11: [],
    loc.sand_kingdom_regional_coin_12: [],
    loc.sand_kingdom_regional_coin_group_5: [],
    loc.sand_kingdom_regional_coin_13: [],
    loc.sand_kingdom_regional_coin_14: [],
    loc.sand_kingdom_regional_coin_15: [],
    loc.sand_kingdom_regional_coin_group_6: [],
    loc.sand_kingdom_regional_coin_16: [],
    loc.sand_kingdom_regional_coin_17: [],
    loc.sand_kingdom_regional_coin_group_7: [],
    loc.sand_kingdom_regional_coin_18: [],
    loc.sand_kingdom_regional_coin_19: [],
    loc.sand_kingdom_regional_coin_group_8: [],
    loc.sand_kingdom_regional_coin_20: [],
    loc.sand_kingdom_regional_coin_21: [],
    loc.sand_kingdom_regional_coin_22: [],
    loc.sand_kingdom_regional_coin_group_9: [],
    loc.sand_kingdom_regional_coin_23: [],
    loc.sand_kingdom_regional_coin_24: [],
    loc.sand_kingdom_regional_coin_25: [],
    loc.sand_kingdom_regional_coin_group_10: [],
    loc.sand_kingdom_regional_coin_26: [],
    loc.sand_kingdom_regional_coin_27: [],
    loc.sand_kingdom_regional_coin_28: [],
    loc.sand_kingdom_regional_coin_group_11: [],
    loc.sand_kingdom_regional_coin_29: [],
    loc.sand_kingdom_regional_coin_30: [],
    loc.sand_kingdom_regional_coin_31: [],
    loc.sand_kingdom_regional_coin_group_12: [],
    loc.sand_kingdom_regional_coin_32: [],
    loc.sand_kingdom_regional_coin_33: [],
    loc.sand_kingdom_regional_coin_34: [],
    loc.sand_kingdom_regional_coin_group_13: [],
    loc.sand_kingdom_regional_coin_35: [],
    loc.sand_kingdom_regional_coin_36: [],
    loc.sand_kingdom_regional_coin_37: [],
    loc.sand_kingdom_regional_coin_group_14: [],
    loc.sand_kingdom_regional_coin_38: [],
    loc.sand_kingdom_regional_coin_39: [],
    loc.sand_kingdom_regional_coin_40: [],
    loc.sand_kingdom_regional_coin_group_15: [],
    loc.sand_kingdom_regional_coin_41: [],
    loc.sand_kingdom_regional_coin_42: [],
    loc.sand_kingdom_regional_coin_group_16: [],
    loc.sand_kingdom_regional_coin_43: [],
    loc.sand_kingdom_regional_coin_44: [],
    loc.sand_kingdom_regional_coin_45: [],
    loc.sand_kingdom_regional_coin_46: [],
    loc.sand_kingdom_regional_coin_47: [],
    loc.sand_kingdom_regional_coin_48: [],
    loc.sand_kingdom_regional_coin_group_17: [],
    loc.sand_kingdom_regional_coin_49: [],
    loc.sand_kingdom_regional_coin_50: [],
    loc.sand_kingdom_regional_coin_51: [],
    loc.sand_kingdom_regional_coin_group_20: [],
    loc.sand_kingdom_regional_coin_60: [],
    loc.sand_kingdom_regional_coin_61: [],
    loc.sand_kingdom_regional_coin_group_21: [],
    loc.sand_kingdom_regional_coin_62: [],
    loc.sand_kingdom_regional_coin_63: [],
    #endregion

    #region Sand Kingdom Purple Coins Post Peace
    loc.sand_kingdom_regional_coin_group_18: [],
    loc.sand_kingdom_regional_coin_52: [],
    loc.sand_kingdom_regional_coin_53: [],
    loc.sand_kingdom_regional_coin_54: [],
    loc.sand_kingdom_regional_coin_55: [],
    loc.sand_kingdom_regional_coin_group_19: [],
    loc.sand_kingdom_regional_coin_56: [],
    loc.sand_kingdom_regional_coin_57: [],
    loc.sand_kingdom_regional_coin_58: [],
    loc.sand_kingdom_regional_coin_59: [],
    #endregion

    #region Sand Kingdom Bullet Bill Maze Regional Coins
    loc.bullet_bill_maze_regional_coin_group_1: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_1: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_2: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_3: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    loc.bullet_bill_maze_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [items.bullet_bill], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.vault], SMORuleOperation.NONE)
    ],
    #endregion

    #region Sand Kingdom Moe Eye Invisible Maze
    loc.moeeye_invisible_maze_regional_coin_group_1: [],
    loc.moeeye_invisible_maze_regional_coin_1: [],
    loc.moeeye_invisible_maze_regional_coin_2: [],
    loc.moeeye_invisible_maze_regional_coin_3: [],
    loc.moeeye_invisible_maze_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Ice Cave
    loc.ice_cave_regional_coin_group_1: [],
    loc.ice_cave_regional_coin_1: [],
    loc.ice_cave_regional_coin_2: [],
    loc.ice_cave_regional_coin_group_2: [],
    loc.ice_cave_regional_coin_3: [],
    loc.ice_cave_regional_coin_4: [],
    #endregion

    #region Sand Kingdom Upper Pyramid
    loc.pyramid_upper_interior_regional_coin_group_1: [],
    loc.pyramid_upper_interior_regional_coin_1: [],
    loc.pyramid_upper_interior_regional_coin_2: [],
    loc.pyramid_upper_interior_regional_coin_3: [],
    #endregion

    #region Sand Kingdom Strange Neighborhood
    loc.strange_neighborhood_regional_coin_group_1: [],
    loc.strange_neighborhood_regional_coin_1: [],
    loc.strange_neighborhood_regional_coin_2: [],
    loc.strange_neighborhood_regional_coin_group_2: [],
    loc.strange_neighborhood_regional_coin_3: [],
    loc.strange_neighborhood_regional_coin_4: [],
    loc.strange_neighborhood_regional_coin_5: [],
    #endregion

    #region Underground Ruins
    loc.underground_ruins_regional_coin_group_1: [],
    loc.underground_ruins_regional_coin_1: [],
    loc.underground_ruins_regional_coin_2: [],
    loc.underground_ruins_regional_coin_3: [],
    loc.underground_ruins_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.up_throw], SMORuleOperation.NONE)
    ],
    loc.underground_ruins_regional_coin_4: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.up_throw], SMORuleOperation.NONE)
    ],
    loc.underground_ruins_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.up_throw], SMORuleOperation.NONE)
    ],
    loc.underground_ruins_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.up_throw], SMORuleOperation.NONE)
    ],
    loc.underground_ruins_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.ABILITY, [items.up_throw], SMORuleOperation.NONE)
    ],
    #endregion

    #region Jaxi Ruins
    loc.jaxi_ruins_regional_coin_group_1: [],
    loc.jaxi_ruins_regional_coin_1: [],
    loc.jaxi_ruins_regional_coin_2: [],
    loc.jaxi_ruins_regional_coin_group_2: [],
    loc.jaxi_ruins_regional_coin_3: [],
    loc.jaxi_ruins_regional_coin_4: [],
    loc.jaxi_ruins_regional_coin_5: [],
    loc.jaxi_ruins_regional_coin_group_3: [],
    loc.jaxi_ruins_regional_coin_6: [],
    loc.jaxi_ruins_regional_coin_7: [],
    loc.jaxi_ruins_regional_coin_8: [],
    #endregion

    #region Lake Kingdom Start Regional Coins
    loc.lake_kingdom_regional_coin_group_4: [],
    loc.lake_kingdom_regional_coin_12: [],
    loc.lake_kingdom_regional_coin_13: [],
    loc.lake_kingdom_regional_coin_14: [],
    loc.lake_kingdom_regional_coin_group_6: [],
    loc.lake_kingdom_regional_coin_18: [],
    loc.lake_kingdom_regional_coin_19: [],
    loc.lake_kingdom_regional_coin_20: [],
    loc.lake_kingdom_regional_coin_group_2: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_5: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_6: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_7: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_group_5: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_15: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_16: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_17: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    #endregion

    #region Lake Kingdom Main Regional Coins
    loc.lake_kingdom_regional_coin_group_1: [],
    loc.lake_kingdom_regional_coin_1: [],
    loc.lake_kingdom_regional_coin_2: [],
    loc.lake_kingdom_regional_coin_3: [],
    loc.lake_kingdom_regional_coin_4: [],
    loc.lake_kingdom_regional_coin_group_3: [],
    loc.lake_kingdom_regional_coin_8: [],
    loc.lake_kingdom_regional_coin_9: [],
    loc.lake_kingdom_regional_coin_10: [],
    loc.lake_kingdom_regional_coin_11: [],
    loc.lake_kingdom_regional_coin_group_7: [],
    loc.lake_kingdom_regional_coin_21: [],
    loc.lake_kingdom_regional_coin_22: [],
    loc.lake_kingdom_regional_coin_23: [],
    loc.lake_kingdom_regional_coin_group_8: [],
    loc.lake_kingdom_regional_coin_24: [],
    loc.lake_kingdom_regional_coin_25: [],
    loc.lake_kingdom_regional_coin_26: [],
    loc.lake_kingdom_regional_coin_27: [],
    loc.lake_kingdom_regional_coin_group_9: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_28: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_29: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_30: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_31: [
        (SMORuleCondition.CAPTURE, [items.zipper], SMORuleOperation.NONE)
    ],
    loc.lake_kingdom_regional_coin_group_10: [],
    loc.lake_kingdom_regional_coin_32: [],
    loc.lake_kingdom_regional_coin_33: [],
    loc.lake_kingdom_regional_coin_34: [],
    loc.lake_kingdom_regional_coin_group_11: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.triple_jump, items.vault], [items.ground_pound_jump, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip, items.vault], [items.backflip, items.vault], SMORuleOperation.NONE),
    ],
    loc.lake_kingdom_regional_coin_35: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.triple_jump, items.vault], [items.ground_pound_jump, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip, items.vault], [items.backflip, items.vault], SMORuleOperation.NONE),
    ],
    loc.lake_kingdom_regional_coin_36: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.triple_jump, items.vault], [items.ground_pound_jump, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip, items.vault], [items.backflip, items.vault], SMORuleOperation.NONE),
    ],
    loc.lake_kingdom_regional_coin_37: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.triple_jump, items.vault], [items.ground_pound_jump, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip, items.vault], [items.backflip, items.vault], SMORuleOperation.NONE),
    ],
    loc.lake_kingdom_regional_coin_38: [
        (SMORuleCondition.CAPTURE, [items.goomba], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_EASY, [items.triple_jump, items.vault], [items.ground_pound_jump, items.vault], SMORuleOperation.OR),
        (SMORuleCondition.TRICK_INTERMEDIATE, [items.side_flip, items.vault], [items.backflip, items.vault], SMORuleOperation.NONE),
    ],
    loc.lake_kingdom_regional_coin_group_12: [],
    loc.lake_kingdom_regional_coin_39: [],
    loc.lake_kingdom_regional_coin_40: [],
    loc.lake_kingdom_regional_coin_41: [],
    loc.lake_kingdom_regional_coin_group_13: [],
    loc.lake_kingdom_regional_coin_42: [],
    loc.lake_kingdom_regional_coin_43: [],
    loc.lake_kingdom_regional_coin_44: [],
    loc.lake_kingdom_regional_coin_group_14: [],
    loc.lake_kingdom_regional_coin_45: [],
    loc.lake_kingdom_regional_coin_46: [],
    loc.lake_kingdom_regional_coin_47: [],
    #endregion

    #region Bouncy Flowers Regional Coins
    loc.bouncy_flowers_regional_coin_group_1: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    loc.bouncy_flowers_regional_coin_1: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    loc.bouncy_flowers_regional_coin_2: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    loc.bouncy_flowers_regional_coin_3: [
        (SMORuleCondition.ABILITY, [items.ledge_grab], SMORuleOperation.NONE)
    ],
    #endregion
}
    """
    Potentially relevant code salvaged from Rules.py

    # Regional Coin Items
    regional_totals = {}
    for item, option, kingdom, cost in shop_location_costs:
        if kingdom not in regional_totals:
            regional_totals[kingdom] = 0
        if self.options.goal.value >= option or self.options.entrance_randomization > 0:
            regional_totals[kingdom] += cost # Should be setting cost, not adding to
            self.set_rule(self.get_location(item), create_access_rule(self,[
                (SMORuleCondition.REGIONAL_COINS, [kingdom, regional_totals[kingdom]], SMORuleOperation.NONE)
            ]))

    case SMORuleCondition.MOONS:
        access_rule += f'count_moons(state, "{data[0]}", {self.player}) >= {data[1]}'
        all_access_rules.add(f'count_moons(state, "{data[0]}", {self.player}) >= {data[1]}')
        rules_list.append(lambda state: count_moons(state, data[0], self.player) >= data[1])

    case SMORuleCondition.TOTAL_MOONS:
        access_rule += f'total_moons(state, {self.player}) >= {data}'
        all_access_rules.add(f'total_moons(state, {self.player}) >= {data}')
        rules_list.append(lambda state: total_moons(state, self.player) >= data)

    case SMORuleCondition.REGIONAL_COINS:
        access_rule += f'count_regionals(state, "{data[0]}", {self.player}) >= {data[1]}'
        all_access_rules.add(f'count_regionals(state, "{data[0]}", {self.player}) >= {data[1]}')
        rules_list.append(lambda state: count_regionals(state, data[0], self.player) >= data[1])
    """
