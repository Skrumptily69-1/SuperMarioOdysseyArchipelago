from enum import IntEnum
from typing import Any, Optional

from BaseClasses import Entrance, EntranceType, Region

#Relevant Functions: Has, HasAll, HasAny, HasGroup, And, Or, Filtered, CanReachLocation, CanReachRegion
from rule_builder.rules import *
from worlds.SuperMarioOdysseyArchipelago.World.smo.Items import SMOItem

from .Data.EntranceData import SMOEntranceData
from .Data.ItemData import SMOItemData
from .Data.LocationData import SMOLocationData
from .Data.RegionData import SMORegion
from .Data.RuleData import SMOEntranceDataType, cappy, CanCapture


def get_multi_entrance_type(entrance_name: str, internal_name : str, internal_stage: str, types: tuple[str, str, str] = ("entrance", "exit", "")) -> str:
    special_cases = ["regional", "coin", "shop", "employee"]
    enter_name, exit_name, fail = types
    entrance_name = entrance_name.lower()
    if enter_name in special_cases and enter_name in entrance_name:
        return enter_name
    elif exit_name in special_cases and exit_name in entrance_name:
        return exit_name

    return (enter_name if (' entrance' in entrance_name or ' beginning' in entrance_name) and enter_name in internal_name_to_entrance[internal_name][
            internal_stage]
        else exit_name if (' end' in entrance_name or ' exit' in entrance_name) and exit_name in internal_name_to_entrance[internal_name][
            internal_stage]
        else fail)

def get_entrance_type(entrance_name: str, internal_name : str, types: tuple[str, str, str] = ("entrance", "end", ""), is_sub_area: bool = False) -> str:
    enter_name, exit_name, fail = types
    entrance_name = entrance_name.lower()
    return (
            (enter_name if (' beginning' in entrance_name or (' entrance' in entrance_name and not is_sub_area)) and enter_name in internal_name_to_entrance[internal_name]
        else exit_name if ' end' in entrance_name and exit_name in internal_name_to_entrance[internal_name] or (' entrance' in entrance_name and is_sub_area)
        else fail))

def has_multiple_exits(stage_name: str, entrances: dict) -> bool:
    return (stage_name in entrances and
            isinstance(entrances[stage_name], dict))

def get_stage_id(entrance : Entrance, original_bindings: dict[str,str], is_exit: bool = False) -> str:
    entrance_name = display_name_to_internal_name[entrance.parent_region.name]
    while " " in entrance_name:
        entrance_name = display_name_to_internal_name[entrance_name]

    stage_name = display_name_to_internal_name[original_bindings[entrance.name]]

    stage_id = ""

    # if "WorldHome" in entrance_name and "SandWorldShop" in stage_name:
    #     print()

    # print(entrance_name, stage_name)
    is_sub_area = "WorldHomeStage" not in entrance_name

    if has_multiple_exits(stage_name, internal_name_to_entrance[entrance_name]):
        load_zone = get_multi_entrance_type(entrance.name, entrance_name, stage_name)
        # print("Multiple Exits")
        if load_zone != "":
            if is_exit and "WorldHomeStage" in entrance_name and "Unique" not in entrance.name:
                stage_id = internal_name_to_entrance[stage_name]["entrance"]
            else:
                if "WorldTownStage" in entrance_name and "Lobby" in stage_name and not is_exit:
                    load_zone = "exit"
                stage_id = internal_name_to_entrance[entrance_name][stage_name][load_zone]
        else:
            if "SandWorldShop" in stage_name:
                load_zone = get_multi_entrance_type(entrance.name if 'Employee' not in entrance.name else "Employee"
                                                    , entrance_name, stage_name, ("shop", "employee", ""))
                stage_id = internal_name_to_entrance[entrance_name][stage_name][load_zone]
            else:
                load_zone = get_multi_entrance_type(entrance.name, entrance_name, stage_name, ("coin", "regional", ""))

            if load_zone != "":
                stage_id = (internal_name_to_entrance[entrance_name][stage_name]
                [load_zone])
            else:
                # print("Deep Woods")
                for entrance_num in range(1, 5):
                    if hasattr(SMOEntranceData, f"deep_woods_{entrance_num}"):
                       if getattr(SMOEntranceData, f"deep_woods_{entrance_num}") in entrance.name:
                            if f"entrance{entrance_num}" in internal_name_to_entrance[entrance_name][stage_name]:
                                stage_id = internal_name_to_entrance[entrance_name][stage_name][f"entrance{entrance_num}"]
                            else:
                                stage_id = internal_name_to_entrance[stage_name][entrance_name][f"entrance{entrance_num}"]

    else:
        if has_multiple_exits(stage_name, internal_name_to_entrance[entrance_name]):
            stage_id = internal_name_to_entrance[entrance_name][stage_name]
        else:
            # print("Normal")
            if len(internal_name_to_entrance[entrance_name]) > 2:
                if "SnowWorldTown" in entrance_name and "Beginning" not in entrance.name:
                    load_zone = stage_name

                elif "SnowWorldTown" in entrance_name and " Beginning" in entrance.name and is_exit:
                    load_zone = "exit"

                elif "SnowWorldTown" in entrance_name and "Lobby" in stage_name and not is_exit:
                    load_zone = "exit"

                elif ("Underground001" in entrance_name and "Shortcut" not in entrance.name or
                      "Press" in entrance_name and "Beginning" in entrance.name and is_exit
                      ):
                    load_zone = "entrance2"

                elif "Underground001" in entrance_name and "Shortcut" in entrance.name and is_exit:
                    load_zone = "exit"

                else:
                    load_zone = get_entrance_type(entrance.name, entrance_name, ("entrance", "exit", stage_name))
            elif "CityWorldShop" in entrance_name:
                load_zone = get_multi_entrance_type(entrance.name, entrance_name, stage_name, ("coin", "regional", ""))

            elif "SandWorldShop" in entrance_name or "SandWorldShop" in stage_name:
                load_zone = get_multi_entrance_type(entrance.name if 'Employee' not in entrance.name else "Employee"
                                                    , entrance_name, stage_name, ("shop", "employee", ""))

            elif "Lobby000Stage" in entrance_name and is_exit:
                load_zone = "exit"

            # elif "SnowWorldTown" in stage_name and "SnowWorldHome" in entrance_name and is_exit:
            #     load_zone = "exit"

            elif "ForestWorldBonusStage" in entrance_name and is_exit:
                load_zone = "exit"

            elif "PressEx" in entrance_name and is_exit:
                load_zone = "exit"

            elif "SphinxEx" in entrance_name and is_exit:
                load_zone = "exit"

            else:
                load_zone = get_entrance_type(entrance.name, entrance_name, ("entrance", "exit", stage_name), is_sub_area)
            if (not is_sub_area) and is_exit:
            # if load_zone == stage_name:
                stage_id = internal_name_to_entrance[stage_name]["entrance"]
            else:
                if ("Underground" in entrance.name and not "Deepest" in entrance.name and "Beginning" in entrance.name or
                    "Lightning Beginning" in entrance.name or "Lanceur Beginning" in entrance.name):
                    stage_id = internal_name_to_entrance[stage_name][entrance_name]
                else:
                    stage_id = internal_name_to_entrance[entrance_name][load_zone]

    if stage_id == "":
        raise Exception(f"stage id failed to parse: {entrance_name}, {stage_name}")

    return stage_id

def get_stage_ids(self, entry: Entrance, _exit: Entrance) -> tuple[str, str]:
    # add proper support for _rev entrances and exits (ex. Shiveria/SnowWorldTownStage)
    exit_stage_id = get_stage_id(_exit, self.original_exit_bindings, True)
    entry_stage_id = get_stage_id(entry, self.original_entrance_bindings)

    return entry_stage_id, exit_stage_id

def get_entrance_pair(self, entrance : str, binding : str) -> tuple[Entrance, Entrance]:
    if entrance in self.multiworld.regions.entrance_cache[self.player]:
        _exit = self.get_entrance(entrance)
    else:
        raise Exception(f"Entrance '{entrance}' does not exist.")
    if binding in self.multiworld.regions.entrance_cache[self.player]:
        entry = self.get_entrance(binding)
    else:
        raise Exception(f"Bound Entrance '{binding}' does not exist")

    return entry, _exit



class SMORandomizationGroup(IntEnum):
        """
        Enumeration of Super Mario Odyssey Entrance Types
        """
        DOOR = 0
        PIPE = 1
        MOON_PIPE = 2
        HIT_BOX = 3
        PAINTING = 4
        ROCKET = 5
        TOP_HAT_ENTER = 6
        TOP_HAT_EXIT = 7
        TOP_HAT_SUB_AREA_ENTER = 8
        TOP_HAT_SUB_AREA_EXIT = 9
        SAND_SHOP_SUB_AREA = 10
        SAND_EMPLOYEE_SUB_AREA = 11


def get_randomization_group(entrance: Entrance) -> SMORandomizationGroup:
    if "Employee" in entrance.name:
        return SMORandomizationGroup.SAND_EMPLOYEE_SUB_AREA
    elif "Sand Kingdom Shop" in entrance.name:
        return SMORandomizationGroup.SAND_SHOP_SUB_AREA

    return SMORandomizationGroup.DOOR

class SMOEntrance(Entrance):
    """
    Finish SMOEntrance Object
    Bool if sub area
    bool if 2 unique over world entrances
    possibly Entrance/SMOEntrance of related reverse entrance.

    """
    is_sub_area : bool
    has_alternate_entrance: bool
    paired_entrance_name: str
    is_reverse: bool

    def __init__(self, player: int, name: str = "", parent: Optional[Region] = None,
                 randomization_group: int = 0, randomization_type: EntranceType = EntranceType.ONE_WAY,
                 is_sub_area: bool = False, has_alternate_entrance: bool = False,
                 is_reverse: bool = False) -> None:

        self.is_sub_area = is_sub_area
        self.has_alternate_entrance = has_alternate_entrance
        self.paired_entrance = ""
        self.is_reverse = is_reverse
        super().__init__(player, name, parent, randomization_group, randomization_type)

display_name_alias = {
    SMORegion.cap_kingdom_intro: "CapWorldHomeStage",
    "Moon Kingdom Peace": SMOEntranceData.moon_kingdom,
    "Day Metro Kingdom": SMOEntranceData.metro_kingdom,
    "Sand Kingdom Peace": SMOEntranceData.sand_kingdom,
    "Luncheon Kingdom Post Broodals": SMOEntranceData.luncheon_kingdom,
    "Sand Kingdom Moon Rock": SMOEntranceData.sand_kingdom,
    "Luncheon Kingdom Meat": SMOEntranceData.luncheon_kingdom,
    SMORegion.infiltrate_bowsers_castle: SMOEntranceData.bowsers_kingdom,
    "Bowser Kingdom Moon Rock": SMOEntranceData.bowsers_kingdom,
    "Lake Kingdom Moon Rock": SMOEntranceData.lake_kingdom,
    "Wooded Kingdom Moon Rock": SMOEntranceData.wooded_kingdom,
    "Metro Kingdom Moon Rock": SMOEntranceData.metro_kingdom,
    "Snow Kingdom Peace": SMOEntranceData.snow_kingdom,
    "Bowser Kingdom Peace": SMOEntranceData.bowsers_kingdom,
    SMORegion.night_metro_kingdom: "CityWorldHomeStage",
    "Bowser Kingdom Smart Bombing": SMOEntranceData.bowsers_kingdom,
    "Moon Kingdom Moon Rock": SMOEntranceData.moon_kingdom,
    "Dark Side Peace": SMOEntranceData.dark_side,
    "Cascade Kingdom Moon Rock": SMOEntranceData.cascade_kingdom,
    "Wooded Kingdom Post Broodals": SMOEntranceData.wooded_kingdom,
    "Cascade Kingdom Peace": SMOEntranceData.cascade_kingdom,
    "Snow Kingdom Moon Rock": SMOEntranceData.snow_kingdom,
    "Lost Kingdom Moon Rock": SMOEntranceData.lost_kingdom,
    "Cap Kingdom Topper": SMOEntranceData.cap_kingdom,
    "Luncheon Kingdom Moon Rock": SMOEntranceData.luncheon_kingdom,
    SMORegion.cloud_kingdom_revisit: SMOEntranceData.cloud_kingdom,
    "Cap Kingdom Moon Rock": SMOEntranceData.cap_kingdom,
    "Wooded Kingdom Peace": SMOEntranceData.wooded_kingdom,
    "Cloud Kingdom Moon Rock": SMOEntranceData.cloud_kingdom,
    "Sand Kingdom Shop Employee Entrance": "SandWorldShopStage",
    "Bowser Kingdom Mecha Broodal": SMOEntranceData.bowsers_kingdom,
    "Ruined Kingdom Moon Rock": SMOEntranceData.ruined_kingdom,
    "Seaside Kingdom Moon Rock": SMOEntranceData.seaside_kingdom,
    SMORegion.dark_side_2: "Special1WorldHomeStage",
    SMORegion.dark_side_3: "Special1WorldHomeStage",
    SMORegion.dark_side_4: "Special1WorldHomeStage",
    SMORegion.dark_side_5: "Special1WorldHomeStage",
}

display_name_to_internal_name = {
    SMOEntranceData.cap_kingdom:"CapWorldHomeStage",
    SMOEntranceData.top_hat_tower:"CapWorldTowerStage",
    SMOEntranceData.poison_tides:"PoisonWaveExStage",
    SMOEntranceData.push_blocks:"PushBlockExStage",
    SMOEntranceData.frog_pond:"FrogSearchExStage",
    SMOEntranceData.rolling_lane:"RollingExStage",
    SMOEntranceData.cascade_kingdom:"WaterfallWorldHomeStage",
    SMOEntranceData.t_rex_nest:"TrexPoppunExStage",
    SMOEntranceData.chain_chomp_cave:"WanwanClashExStage",
    SMOEntranceData.chasm_lifts:"Lift2DExStage",
    SMOEntranceData.mysterious_clouds:"CapAppearExStage",
    SMOEntranceData.gusty_bridges:"WindBlowExStage",
    SMOEntranceData.sand_kingdom:"SandWorldHomeStage",
    SMOEntranceData.sand_kingdom_shop:"SandWorldShopStage",
    SMOEntranceData.sand_slots:"SandWorldSlotStage",
    SMOEntranceData.sand_costume_bonus_dancing_room:"SandWorldCostumeStage",
    SMOEntranceData.sand_sphynx_vault:"SandWorldSecretStage",
    SMOEntranceData.sand_rumbling_floor_house:"SandWorldVibrationStage",
    SMOEntranceData.inverted_pyramid_lower_interior:"SandWorldPyramid000Stage",
    SMOEntranceData.inverted_pyramid_mural:"SandWorldHomeStage",
    SMOEntranceData.inverted_pyramid_upper_interior:"SandWorldPyramid001Stage",
    SMOEntranceData.top_of_the_inverted_pyramid: "SandWorldHomeStage",
    SMOEntranceData.underground_ruins:"SandWorldUnderground000Stage",
    SMOEntranceData.deepest_underground:"SandWorldUnderground001Stage",
    SMOEntranceData.ice_cave:"SandWorldPressExStage",
    SMOEntranceData.moe_eye_invisible_maze:"SandWorldMeganeExStage",
    SMOEntranceData.bullet_bill_maze:"SandWorldKillerExStage",
    SMOEntranceData.jaxi_ruins:"SandWorldSphinxExStage",
    SMOEntranceData.strange_neighborhood:"SandWorldRotateExStage",
    SMOEntranceData.moe_eye_invisible_floor:"MeganeLiftExStage",
    SMOEntranceData.colossal_ruins:"RocketFlowerExStage",
    SMOEntranceData.freezing_waterway:"WaterTubeExStage",
    SMOEntranceData.lake_kingdom:"LakeWorldHomeStage",
    SMOEntranceData.lake_kingdom_shop:"LakeWorldShopStage",
    SMOEntranceData.arch_repair:"GotogotonExStage",
    SMOEntranceData.zipper_chasm:"FastenerExStage",
    SMOEntranceData.bouncy_flowers:"TrampolineWallCatchExStage",
    SMOEntranceData.poison_swamp:"FrogPoisonExStage",
    SMOEntranceData.wooded_kingdom:"ForestWorldHomeStage",
    SMOEntranceData.sky_garden_tower:"ForestWorldTowerStage",
    SMOEntranceData.secret_flower_field:"ForestWorldBossStage",
    SMORegion.deep_woods:"ForestWorldWoodsStage",
    SMOEntranceData.deep_woods_costume_bonus_treasure_chest:"ForestWorldWoodsCostumeStage",
    SMOEntranceData.deep_woods_treasure_trap:"ForestWorldWoodsTreasureStage",
    SMOEntranceData.spinning_platforms_treasure_vault:"ForestWorldBonusStage", # Unsure
    SMOEntranceData.flooding_pipeway:"ForestWorldWaterExStage",
    SMOEntranceData.fog_wandering:"FogMountainExStage",
    SMOEntranceData.wooded_flower_road:"RailCollisionExStage",
    SMOEntranceData.sherm_elevator:"ShootingElevatorExStage",
    SMOEntranceData.walking_on_clouds:"ForestWorldCloudBonusExStage",
    SMOEntranceData.invisible_road:"PackunPoisonExStage",
    SMOEntranceData.sheep_herding:"AnimalChaseExStage",
    SMOEntranceData.breakdown_road:"KillerRoadExStage",
    SMOEntranceData.cloud_kingdom:"CloudWorldHomeStage",
    SMOEntranceData.cloud_picture_match:"FukuwaraiKuriboStage",
    SMOEntranceData.king_of_the_cube:"Cube2DExStage",
    SMOEntranceData.lost_kingdom:"ClashWorldHomeStage",
    SMOEntranceData.lost_kingdom_shop:"ClashWorldShopStage",
    SMOEntranceData.tropical_wiggler_swamp:"ImomuPoisonExStage",
    SMOEntranceData.klepto_lava_bath:"JangoExStage",
    SMOEntranceData.metro_kingdom:"CityWorldHomeStage",
    SMORegion.metro_kingdom_shop:"CityWorldShop01Stage",
    SMOEntranceData.metro_kingdom_shop:"CityWorldShop01Stage",
    SMOEntranceData.metro_kingdom_shop_regional:"CityWorldShop01Stage", # Might Change
    SMOEntranceData.metro_slots:"CityWorldSandSlotStage",
    SMOEntranceData.city_hall:"CityWorldMainTowerStage",
    SMOEntranceData.sewers:"CityWorldFactoryStage",
    SMOEntranceData.rc_race:"RadioControlExStage",
    SMOEntranceData.private_room:"Note2D3DRoomExStage",
    SMOEntranceData.projection_room:"Theater2DExStage",
    SMOEntranceData.crowded_street:"CityPeopleRoadStage",
    SMOEntranceData.builder_outfit:"ElectricWireExStage",
    SMOEntranceData.metro_siege:"ShootingCityExStage",
    SMOEntranceData.rotating_maze:"CapRotatePackunExStage",
    SMOEntranceData.high_rise:"PoleGrabCeilExStage",
    SMOEntranceData.bullet_building:"PoleKillerExStage",
    SMOEntranceData.t_rex_escape:"TrexBikeExStage",
    SMOEntranceData.pitch_black_island:"DonsukeExStage",
    SMOEntranceData.swinging_scaffolding:"SwingSteelExStage",
    SMOEntranceData.vanishing_road:"BikeSteelExStage",
    SMOEntranceData.snow_kingdom:"SnowWorldHomeStage",
    SMOEntranceData.snow_kingdom_shop:"SnowWorldShopStage",
    SMOEntranceData.freezing_room:"SnowWorldCostumeStage",
    SMOEntranceData.ice_trace_walking:"IceWalkerExStage",
    SMOEntranceData.shiveria:"SnowWorldTownStage",
    SMOEntranceData.snowline_circuit_lobby:"SnowWorldLobby000Stage",
    "Snowline Circuit: Class S Lobby":"SnowWorldLobby001Stage",
    "Snowline Circuit: Class A":"SnowWorldRace000Stage",
    "Snowline Circuit: Class S":"SnowWorldRace001Stage",
    "Snowline Circuit: Tutorial":"SnowWorldRaceTutorialStage",
    SMOEntranceData.iceburn_circuit_class_a_lobby:"SnowWorldLobbyExStage",
    "Iceburn Circuit: Class A":"SnowWorldRaceExStage",
    "Iceburn Circuit: Class S":"SnowWorldRaceHardExStage",
    SMOEntranceData.rocket_flower_dash:"IceWaterDashExStage",
    SMOEntranceData.freezing_water:"IceWaterBlockExStage",
    SMOEntranceData.ty_foo_sliding_puzzle:"ByugoPuzzleExStage",
    SMOEntranceData.above_the_clouds:"SnowWorldCloudBonusExStage",
    SMOEntranceData.snow_flower_road:"KillerRailCollisionExStage",
    SMOEntranceData.seaside_kingdom:"SeaWorldHomeStage",
    SMOEntranceData.seaside_costume_bonus_dancing_room:"SeaWorldCostumeStage",
    SMOEntranceData.seaside_sphynx_treasure_vault:"SeaWorldSecretStage",
    SMOEntranceData.seaside_rumbling_floor_cave:"SeaWorldVibrationStage",
    SMOEntranceData.underwater_tunnel:"SeaWorldUtsuboCaveStage",
    SMOEntranceData.sandy_bottom:"SeaWorldSneakingManStage",
    SMOEntranceData.wading_in_the_cloud_sea:"CloudExStage",
    SMOEntranceData.narrow_valley:"WaterValleyExStage",
    SMOEntranceData.sinking_island:"SenobiTowerExStage",
    SMOEntranceData.pokio_bomb_aiming:"ReflectBombExStage",
    SMOEntranceData.spinning_maze:"TogezoRotateExStage",
    SMOEntranceData.luncheon_kingdom:"LavaWorldHomeStage",
    SMOEntranceData.luncheon_kingdom_shop:"LavaWorldShopStage",
    SMOEntranceData.luncheon_costume_bonus_cooking_pots:"LavaWorldCostumeStage",
    SMOEntranceData.luncheon_slots:"LavaBonus1Zone",
    SMOEntranceData.luncheon_treasure_vault:"LavaWorldTreasureStage",
    SMOEntranceData.magma_swamp:"LavaWorldUpDownExStage",
    SMOEntranceData.magma_narrow_path:"LavaWorldBubbleLaneExStage",
    SMOEntranceData.fork_flickin:"ForkExStage",
    SMOEntranceData.cheese_excavate:"LavaWorldExcavationExStage",
    SMOEntranceData.spinning_athletics:"LavaWorldClockExStage",
    SMOEntranceData.rotating_gears_with_bitefrost:"GabuzouClockExStage",
    SMOEntranceData.volcano_cave:"CapAppearLavaLiftExStage",
    SMOEntranceData.lava_islands:"LavaWorldFenceLiftExStage",
    SMOEntranceData.ruined_kingdom:"BossRaidWorldHomeStage",
    SMOEntranceData.roulette_tower:"DotTowerExStage",
    SMOEntranceData.chargin_chuck_arena:"BullRunExStage",
    SMOEntranceData.bowsers_kingdom:"SkyWorldHomeStage",
    SMOEntranceData.bowsers_kingdom_shop:"SkyWorldShopStage",
    SMOEntranceData.folding_screen:"SkyWorldCostumeStage",
    SMOEntranceData.bowsers_treasure_vault:"SkyWorldTreasureStage",
    SMOEntranceData.spinning_tower:"TsukkunRotateExStage",
    SMOEntranceData.jizos_adventure:"JizoSwitchExStage",
    SMOEntranceData.dashing_above_the_clouds:"SkyWorldCloudBonusExStage",
    SMOEntranceData.hexagon_tower:"KaronWingTowerStage",
    SMOEntranceData.wooden_tower:"TsukkunClimbExStage",
    SMOEntranceData.moon_kingdom:"MoonWorldHomeStage",
    SMOEntranceData.moon_kingdom_shop:"MoonWorldShopRoom",
    SMOEntranceData.moon_sphynx_vault:"MoonWorldSphinxRoom",
    SMOEntranceData.moon_cave:"MoonWorldCaptureParadeStage",
    SMOEntranceData.inside_the_church:"MoonWorldWeddingRoomStage",
    "Inside the Church 2 (possibly unused)":"MoonWorldWeddingRoom2Stage",
    "Moon":"MoonWorldKoopa1Stage",
    #"Moon":"MoonWorldKoopa2Stage",
    "Bowser Caverns:":"MoonWorldBasementStage",
    SMOEntranceData.dot_galaxy:"Galaxy2DExStage",
    SMOEntranceData.giant_swings:"MoonAthleticExStage",
    SMOEntranceData.dark_side:"Special1WorldHomeStage",
    SMOEntranceData.dark_side_topper:"Special1WorldTowerStackerStage",
    SMOEntranceData.dark_side_hariet:"Special1WorldTowerBombTailStage",
    SMOEntranceData.dark_side_spewart:"Special1WorldTowerFireBlowerStage",
    SMOEntranceData.dark_side_rango:"Special1WorldTowerCapThrowerStage",
    SMOEntranceData.dark_side_breakdown_road:"KillerRoadNoCapExStage",
    SMOEntranceData.dark_side_invisible_road:"PackunPoisonNoCapExStage",
    SMOEntranceData.dark_side_vanishing_road:"BikeSteelNoCapExStage",
    SMOEntranceData.dark_side_siege:"ShootingCityYoshiExStage",
    SMOEntranceData.dark_side_sinking_island:"SenobiTowerYoshiExStage",
    SMOEntranceData.dark_side_magma_swamp:"LavaWorldUpDownYoshiExStage",
    SMOEntranceData.darker_side:"Special2WorldHomeStage",
    SMOEntranceData.darker_side_main:"Special2WorldLavaStage",
    SMOEntranceData.darker_side_pokio:"Special2WorldCloudStage",
    SMOEntranceData.darker_side_bowser:"Special2WorldKoopaStage",
    SMOEntranceData.darker_side_end:"Special2WorldLavaStage",
    SMOEntranceData.darker_side_tower:"Special2WorldHomeStage",
    "Mushroom Kingdom":"PeachWorldHomeStage",
    SMOEntranceData.peachs_castle:"PeachWorldCastleStage",
    SMOEntranceData.mushroom_kingdom_shop:"PeachWorldShopStage",
    SMOEntranceData.castle_courtyard:"PeachWorldCostumeStage",
    SMOEntranceData.mushroom_picture_match:"FukuwaraiMarioStage",
    SMOEntranceData.painting_room_knucklotec:"PeachWorldPictureBossKnuckleStage",
    SMOEntranceData.painting_room_torkdrift:"PeachWorldPictureBossForestStage",
    SMOEntranceData.painting_room_mecha_wiggler:"PeachWorldPictureMofumofuStage",
    SMOEntranceData.painting_room_mollusque_lanceur:"PeachWorldPictureGiantWanderBossStage",
    SMOEntranceData.painting_room_cookatiel:"PeachWorldPictureBossMagmaStage",
    SMOEntranceData.painting_room_lord_of_lightning:"PeachWorldPictureBossRaidStage",
    SMOEntranceData.knucklotec_rematch:"RevengeBossKnuckleStage",
    SMOEntranceData.torkdrift_rematch:"RevengeForestBossStage",
    SMOEntranceData.mecha_wiggler_rematch:"RevengeMofumofuStage",
    SMOEntranceData.mollusque_lanceur_rematch:"RevengeGiantWanderBossStage",
    SMOEntranceData.cookatiel_rematch:"RevengeBossMagmaStage",
    SMOEntranceData.lord_of_lightning_rematch:"RevengeBossRaidStage",
    SMOEntranceData.yoshi_in_the_sea_of_clouds:"YoshiCloudExStage",
    SMOEntranceData.mushroom_well:"DotHardExStage",
    **display_name_alias,
}



stage_id_to_name = {
    # "bikereturn": "BikeSteelExStage",
    # "bike": "BikeSteelExStage",
    "bike": "BikeSteelExStage",
    "bikereturn": "BikeSteelExStage",
    "BossRaidWorldMoonEx02_Exit": "BullRunExStage",
    "BossRaidWorldMoonEx02_Enter": "BullRunExStage",
    "CapAppearExEnt": "CapAppearExStage",
    "CapAppearExExit": "CapAppearExStage",
    "LavaLiftExdokan": "CapAppearLavaLiftExStage",
    "LavaLiftEx": "CapAppearLavaLiftExStage",
    "Goal": "CapWorldTowerStage",
    "Ex": "CapWorldTowerStage",
    "gunsyudokan": "CityPeopleRoadStage",
    "gunsyu": "CityPeopleRoadStage",
    "main_enter": "CityWorldMainTowerStage",
    "main_exit": "CityWorldMainTowerStage",
    "shop_corect": "CityWorldShop01Stage",
    "shop_coin": "CityWorldShop01Stage",
    "densendokan": "ElectricWireExStage",
    "densen": "ElectricWireExStage",
    "bonus2": "ForestWorldBonusStage",
    "bonus": "ForestWorldBonusStage",
    "boss001": "ForestWorldBossStage",
    # "boss001": "ForestWorldBossStage",
    "Tower001": "ForestWorldTowerStage",
    "Tower002": "ForestWorldTowerStage",
    "EX_Water": "ForestWorldWaterExStage",
    "EX_Water_Exit": "ForestWorldWaterExStage",
    "Jyukai001v": "ForestWorldWoodsStage",
    "Jyukai002": "ForestWorldWoodsStage",
    "Jyukai003v": "ForestWorldWoodsStage",
    "Jyukai004": "ForestWorldWoodsStage",
    # "Jyukai001v": "ForestWorldWoodsStage",
    # "Jyukai001v": "ForestWorldWoodsStage",
    "ForkEX": "ForkExStage",
    # "ForkEX": "ForkExStage",
    "LakeWorldMoonEX1b": "FrogPoisonExStage",
    "LakeWorldMoonEX1a": "FrogPoisonExStage",
    "GabuzouClockEx": "GabuzouClockExStage",
    "GabuzouClockExdokan": "GabuzouClockExStage",
    "dot00": "Galaxy2DExStage",
    "dot01": "Galaxy2DExStage",
    "EX_IceWater_Exit": "IceWaterBlockExStage",
    "EX_IceWater": "IceWaterBlockExStage",
    "EX_IceWaterDash_Exit": "IceWaterDashExStage",
    "EX_IceWaterDash": "IceWaterDashExStage",
    "imomu_02": "ImomuPoisonExStage",
    "imomu_01": "ImomuPoisonExStage",
    "jizo02": "JizoSwitchExStage",
    "jizo01": "JizoSwitchExStage",
    "EX_RailCol2_Exit": "KillerRailCollisionExStage",
    "EX_RailCol2": "KillerRailCollisionExStage",
    "PechoBubbleExDokan": "LavaWorldBubbleLaneExStage",
    "PechoBubbleEx": "LavaWorldBubbleLaneExStage",
    "BBQExDokan": "LavaWorldClockExStage",
    "BBQEx": "LavaWorldClockExStage",
    "CostumeOut": "LavaWorldCostumeStage",
    "CostumeEventWorldLava": "LavaWorldCostumeStage",
    "FenceLiftEx": "LavaWorldFenceLiftExStage",
    "FenceLiftExdokan": "LavaWorldFenceLiftExStage",
    "KeyMoveExDokan": "LavaWorldUpDownExStage",
    "KeyMoveEx": "LavaWorldUpDownExStage",
    "Lift2DExit": "Lift2DExStage",
    "Lift2D": "Lift2DExStage",
    "meganelift02": "MeganeLiftExStage",
    "meganelift01": "MeganeLiftExStage",
    "moon_exit": "MoonAthleticExStage",
    "moon": "MoonAthleticExStage",
    "vvv": "MoonWorldCaptureParadeStage",
    "bbb": "MoonWorldCaptureParadeStage",
    "PoisonEx_Exit": "PackunPoisonExStage",
    "PoisonEx": "PackunPoisonExStage",
    "BossRaidA": "PeachWorldPictureBossRaidStage",
    "BossRaidB": "PeachWorldPictureBossRaidStage",
    "GiantWanderBossA": "PeachWorldPictureGiantWanderBossStage",
    "GiantWanderBossB": "PeachWorldPictureGiantWanderBossStage",
    "PoisonWaveExExit": "PoisonWaveExStage",
    "PoisonWaveExEnt": "PoisonWaveExStage",
    "boureturn": "PoleKillerExStage",
    "bou": "PoleKillerExStage",
    "PushBlockExStageEntDokan": "PushBlockExStage",
    "PushBlockExStageEnt": "PushBlockExStage",
    "EX_RailCollision_Exit": "RailCollisionExStage",
    "EX_RailCollision": "RailCollisionExStage",
    "SeaWorldMoonEX1a": "ReflectBombExStage",
    "SeaWorldMoonEX1b": "ReflectBombExStage",
    "rollinggoal": "RollingExStage",
    "rollingstart": "RollingExStage",
    "doukutu2": "SandWorldKillerExStage",
    "doukutu1": "SandWorldKillerExStage",
    "anki2": "SandWorldMeganeExStage",
    "wall": "SandWorldMeganeExStage",
    "arijigoku1": "SandWorldPressExStage",
    "arijigoku2": "SandWorldPressExStage",
    "arijigoku": "SandWorldPressExStage",
    "run00return": "SandWorldSphinxExStage",
    "run00": "SandWorldSphinxExStage",
    "PukupukuCaveGoal": "SeaWorldUtsuboCaveStage",
    "PukupukuCaveStart": "SeaWorldUtsuboCaveStage",
    "SeaWorldEX3b": "SenobiTowerExStage",
    "SeaWorldEX3a": "SenobiTowerExStage",
    "taxi": "ShootingCityExStage",
    "taxireturn": "ShootingCityExStage",
    "EX_Tankuro_Exit": "ShootingElevatorExStage",
    "EX_Tankuro": "ShootingElevatorExStage",
    "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    # "sora001": "SkyWorldCloudBonusExStage",
    "BombTailRoomStart": "Special1WorldTowerBombTailStage",
    "BombTailRoomGoal": "Special1WorldTowerBombTailStage",
    "CapThrowerRoomGoal": "Special1WorldTowerCapThrowerStage",
    "CapThrowerRoomStart": "Special1WorldTowerCapThrowerStage",
    "FireBlowerRoomStart": "Special1WorldTowerFireBlowerStage",
    "FireBlowerRoomGoal": "Special1WorldTowerFireBlowerStage",
    "StackerRoomStart": "Special1WorldTowerStackerStage",
    "StackerRoomGoal": "Special1WorldTowerStackerStage",
    "MoonGoal": "Special2WorldLavaStage",
    "CP_Entrance": "Special2WorldLavaStage",
    "gragrareturn": "SwingSteelExStage",
    "gragra": "SwingSteelExStage",
    "CapTrampolineB": "TrampolineWallCatchExStage",
    "CapTrampolineA": "TrampolineWallCatchExStage",
    "bike02return": "TrexBikeExStage",
    "bike02": "TrexBikeExStage",
    "tukkun001_exit": "TsukkunClimbExStage",
    "tukkun001_enter": "TsukkunClimbExStage",
    "tukkun000_exit": "TsukkunRotateExStage",
    "tukkun000_enter": "TsukkunRotateExStage",
    "WanwanExGoal": "WanwanClashExStage",
    "WanwanExStart": "WanwanClashExStage",
    "EX_2DHosui_Exit": "WaterTubeExStage",
    "EX_2DHosui": "WaterTubeExStage",
    "SeaWorldEX1b": "WaterValleyExStage",
    "SeaWorldEX1a": "WaterValleyExStage",
    "WindBlowExGoal": "WindBlowExStage",
    "WindBlowExStart": "WindBlowExStage",

    # Dead Ends
    "EX_AnimalChase": "AnimalChaseExStage",
    "ByugoPuzzle": "ByugoPuzzleExStage",
    "kaitendokan": "CapRotatePackunExStage",
    "under001enter": "CityWorldFactoryStage",
    "Bonus": "CityWorldSandSlotStage",
    "Kinopio": "ClashWorldShopStage",
    "cube": "Cube2DExStage",
    "donsuke": "DonsukeExStage",
    "PeachWorldEx2a": "DotHardExStage",
    "FastenerEx": "FastenerExStage",
    "EXCloud": "ForestWorldCloudBonusExStage",
    "Explorer_Bonus": "ForestWorldWoodsCostumeStage",
    "TreasureTree": "ForestWorldWoodsTreasureStage",
    "FrogSearchExStageEnt": "FrogSearchExStage",
    "Fukuwarai": "FukuwaraiKuriboStage",
    "Goton": "GotogotonExStage",
    "HomeEntrance": "HomeShipInsideStage",
    "FigureWalker": "IceWalkerExStage",
    "ClashWorldMoonEX2": "JangoExStage",
    "Patakaron02": "KaronWingTowerStage",
    "KillerRoad": "KillerRoadExStage",
    "LakeWorldShop": "LakeWorldShopStage",
    "MartinCubeEx": "LavaWorldExcavationExStage",
    "shop_lava": "LavaWorldShopStage", # "shop"
    "TreasureEventWorldLava": "LavaWorldTreasureStage",
    # "None": "MoonWorldKoopa1Stage",
    # "None": "MoonWorldKoopa2Stage",
    "ddd": "MoonWorldShopRoom",
    "ggg": "MoonWorldSphinxRoom",
    "aaa": "MoonWorldWeddingRoomStage",
    "onpu": "Note2D3DRoomExStage",
    "PeachCastleGate": "PeachWorldCastleStage",
    "BossForestA": "PeachWorldPictureBossForestStage",
    "BossKnuckleA": "PeachWorldPictureBossKnuckleStage",
    "BossMagmaA": "PeachWorldPictureBossMagmaStage",
    "MofumofuA": "PeachWorldPictureMofumofuStage",
    "PeachWorldShopA": "PeachWorldShopStage",
    "car": "RadioControlExStage",
    "rocket": "RocketFlowerExStage",
    "abc": "SandWorldCostumeStage",
    "pyramid01": "SandWorldPyramid000Stage",
    "pyramid04": "SandWorldPyramid001Stage",
    "hide": "SandWorldSecretStage",
    "bar1": "SandWorldShopStage",
    "town(sand)": "SandWorldSlotStage", # "town"
    "Yadokari00": "SandWorldUnderground001Stage",
    "shindo": "SandWorldVibrationStage",
    "CostumeEventSeaWorld": "SeaWorldCostumeStage",
    "TreasureEventWorldSea": "SeaWorldSecretStage",
    "RoomEventWorldSea": "SeaWorldSneakingManStage",
    "shindo_Lv2": "SeaWorldVibrationStage",
    "byoubu": "SkyWorldCostumeStage",
    "shop(sky)": "SkyWorldShopStage", # "shop"
    "shop_dress": "SkyWorldTreasureStage",
    "EX_SkyBonus": "SnowWorldCloudBonusExStage",
    "SnowCostumeEx": "SnowWorldCostumeStage",
    "RaceTrackExit": "SnowWorldLobby000Stage",
    "MoonRace": "SnowWorldLobbyExStage",
    "ShopDoor": "SnowWorldShopStage",
    "room2_start": "Special2WorldCloudStage",
    "room3_goal": "Special2WorldKoopaStage",
    "theater": "Theater2DExStage",
    "SeaWorldMoonEX2": "TogezoRotateExStage",
    "RexPoppunEx": "TrexPoppunExStage",
    "PeachWorldEx1a": "YoshiCloudExStage",
    "SnowUGEnt": "SnowWorldTownStage",
    "icestart": "SandWorldUnderground000Stage",
    "biru": "SandWorldRotateExStage",
    "EX_Mist": "FogMountainExStage",
    "tenjo": "PoleGrabCeilExStage",
    "SeaWorldEX2": "CloudExStage",
    "town(lava)": "LavaBonus1Zone", # "town"
    "BossRaidWorldEx01_Eixt": "DotTowerExStage",
    "BikeSteelNoCapEx_Exit": "BikeSteelNoCapExStage",
    "PackunPoisonNoCapEx_Exit": "PackunPoisonNoCapExStage",
    "ShootingCityYoshiEx": "ShootingCityYoshiExStage",
    "SenobiTowerYoshiEx": "SenobiTowerYoshiExStage",
    "LavaWorldUpDownYoshiEx": "LavaWorldUpDownYoshiExStage",
    "SenobiTowerYoshiEx_Exit": "SenobiTowerYoshiExStage",
    "LavaWorldUpDownYoshiEx_Exit": "LavaWorldUpDownYoshiExStage",
    "ShootingCityYoshiEx_Exit": "ShootingCityYoshiExStage",
    "KillerRoadNoCapEx": "KillerRoadNoCapExStage",
    "BikeSteelNoCapEx": "BikeSteelNoCapExStage",
    "PackunPoisonNoCapEx": "PackunPoisonNoCapExStage",
    "PictureBossMagma": "PeachWorldPictureBossMagmaStage",
    "PictureMofumofu": "PeachWorldPictureMofumofuStage",
    "PictureBossRaid": "PeachWorldPictureBossRaidStage",
    # "BossRaidA": "PeachWorldPictureBossRaidStage",
    # "BossRaidB": "PeachWorldPictureBossRaidStage",
    "PictureBossForest": "PeachWorldPictureBossForestStage",
    "PictureBossKnuckle": "PeachWorldPictureBossKnuckleStage",
    "PictureGiantWanderBoss": "PeachWorldPictureGiantWanderBossStage",

    "start(cookatiel)": "RevengeBossMagmaStage",
    "start(wiggler)": "RevengeMofumofuStage",
    "start(dragon)": "RevengeBossRaidStage",
    "start(torkdrift)": "RevengeForestBossStage",
    "start(knucklotec)": "RevengeBossKnuckleStage",
    "start(mollusque)": "RevengeGiantWanderBossStage",

    "Fukuwarai2": "FukuwaraiMarioStage",
    "CostumeEventWorldPeach": "PeachWorldCostumeStage",

}

internal_name_to_entrance = {
    "BikeSteelExStage": {
        "entrance": "bike",
        "exit": "bikereturn",
    },
    "BullRunExStage": {
        "exit": "BossRaidWorldMoonEx02_Exit",
        "entrance": "BossRaidWorldMoonEx02_Enter",
    },
    "CapAppearExStage": {
        "entrance": "CapAppearExEnt",
        "exit": "CapAppearExExit",
    },
    "CapAppearLavaLiftExStage": {
        "exit": "LavaLiftExdokan",
        "entrance": "LavaLiftEx",
    },
    "CapWorldTowerStage": {
        "exit": "Goal",
        "entrance": "Ex",
    },
    "CityPeopleRoadStage": {
        "exit": "gunsyudokan",
        "entrance": "gunsyu",
    },
    "CityWorldMainTowerStage": {
        "entrance": "main_enter",
        "exit": "main_exit",
    },
    "CityWorldShop01Stage": {
        "regional": "shop_corect",
        "coin": "shop_coin",
    },
    "ElectricWireExStage": {
        "exit": "densendokan",
        "entrance": "densen",
    },
    "ForestWorldBonusStage": {
        "exit": "bonus2",
        "entrance": "bonus",
    },
    "ForestWorldBossStage": {
        "entrance": "boss001",
        "exit": "boss002",
    },
    "ForestWorldTowerStage": {
        "entrance": "Tower001",
        "exit": "Tower002",
    },
    "ForestWorldWaterExStage": {
        "entrance": "EX_Water",
        "exit": "EX_Water_Exit",
    },
    "ForestWorldWoodsStage": {
        "ForestWorldHomeStage": {
            "entrance1": "Jyukai001",
            "entrance2": "Jyukai002",
            "entrance3": "Jyukai003",
            "entrance4": "Jyukai004",
        },
        "ForestWorldWoodsCostumeStage": "Explorer_Bonus",
        "ForestWorldWoodsTreasureStage": "TreasureTree",
    },
    "ForkExStage": {
        "entrance": "ForkEX",
        "exit": "ForkEX2",
    },
    "FrogPoisonExStage": {
        "exit": "LakeWorldMoonEX1b",
        "entrance": "LakeWorldMoonEX1a",
    },
    "GabuzouClockExStage": {
        "entrance": "GabuzouClockEx",
        "exit": "GabuzouClockExdokan",
    },
    "Galaxy2DExStage": {
        "entrance": "dot00",
        "exit": "dot01",
    }, # Check
    "IceWaterBlockExStage": {
        "exit": "EX_IceWater_Exit",
        "entrance": "EX_IceWater",
    },
    "IceWaterDashExStage": {
        "exit": "EX_IceWaterDash_Exit",
        "entrance": "EX_IceWaterDash",
    },
    "ImomuPoisonExStage": {
        "exit": "imomu_02",
        "entrance": "imomu_01",
    },
    "JizoSwitchExStage": {
        "exit": "jizo02",
        "entrance": "jizo01",
    },
    "KillerRailCollisionExStage": {
        "exit": "EX_RailCol2_Exit",
        "entrance": "EX_RailCol2",
    },
    "LavaWorldBubbleLaneExStage": {
        "exit": "PechoBubbleExDokan",
        "entrance": "PechoBubbleEx",
    },
    "LavaWorldClockExStage": {
        "exit": "BBQExDokan",
        "entrance": "BBQEx",
    },
    "LavaWorldCostumeStage": {
        "exit": "CostumeOut",
        "entrance": "CostumeEventWorldLava",
    },
    "LavaWorldFenceLiftExStage": {
        "entrance": "FenceLiftEx",
        "exit": "FenceLiftExdokan",
    },
    "LavaWorldUpDownExStage": {
        "exit": "KeyMoveExDokan",
        "entrance": "KeyMoveEx",
    },
    "Lift2DExStage": {
        "exit": "Lift2DExit",
        "entrance": "Lift2D",
    },
    "MeganeLiftExStage": {
        "exit": "meganelift02",
        "entrance": "meganelift01",
    },
    "MoonAthleticExStage": {
        "exit": "moon_exit",
        "entrance": "moon",
    },
    "MoonWorldCaptureParadeStage": {
        "exit": "bbb",
        "entrance": "ccc",
    },
    "PackunPoisonExStage": {
        "exit": "PoisonEx_Exit",
        "entrance": "PoisonEx",
    },
    "PeachWorldPictureBossRaidStage": {
        "entrance": "BossRaidA",
        #"entrance": "BossRaidB",
        "exit": "PictureBossRaid",
    },
    "PeachWorldPictureGiantWanderBossStage": {
        "entrance": "GiantWanderBossA",
        #"exit": "GiantWanderBossB",
        "exit": "PictureGiantWanderBoss",
    },
    "PoisonWaveExStage": {
        "exit": "PoisonWaveExExit",
        "entrance": "PoisonWaveExEnt",
    },
    "PoleKillerExStage": {
        "exit": "boureturn",
        "entrance": "bou",
    },
    "PushBlockExStage": {
        "exit": "PushBlockExStageEntDokan",
        "entrance": "PushBlockExStageEnt",
    },
    "RailCollisionExStage": {
        "exit": "EX_RailCollision_Exit",
        "entrance": "EX_RailCollision",
    },
    "ReflectBombExStage": {
        "entrance": "SeaWorldMoonEX1a",
        "exit": "SeaWorldMoonEX1b",
    },
    "RollingExStage": {
        "exit": "rollinggoal",
        "entrance": "rollingstart",
    },
    "SandWorldKillerExStage": {
        "exit": "doukutu2",
        "entrance": "doukutu1",
    },
    "SandWorldMeganeExStage": {
        "exit": "anki2",
        "entrance": "wall",
    },
    "SandWorldPressExStage": {
        "entrance": "arijigoku",
        "entrance2": "arijigoku1",
        "exit": "arijigoku2",
    },
    "SandWorldSphinxExStage": {
        "exit": "run00return",
        "entrance": "aaaSand",
        "entrance2": "run00",
    },
    "SeaWorldUtsuboCaveStage": {
        "exit": "PukupukuCaveGoal",
        "entrance": "PukupukuCaveStart",
    },
    "SenobiTowerExStage": {
        "exit": "SeaWorldEX3b",
        "entrance": "SeaWorldEX3a",
    },
    "ShootingCityExStage": {
        "entrance": "taxi",
        "exit": "taxireturn",
    },
    "ShootingElevatorExStage": {
        "exit": "EX_Tankuro_Exit",
        "entrance": "EX_Tankuro",
    },
    "SkyWorldCloudBonusExStage": {
        "entrance": "sora001",
        "exit": "sora001",
    },
    "Special1WorldTowerBombTailStage": {
        "entrance": "BombTailRoomStart",
        "exit": "BombTailRoomGoal",
    },
    "Special1WorldTowerCapThrowerStage": {
        "exit": "CapThrowerRoomGoal",
        "entrance": "CapThrowerRoomStart",
    },
    "Special1WorldTowerFireBlowerStage": {
        "entrance": "FireBlowerRoomStart",
        "exit": "FireBlowerRoomGoal",
    },
    "Special1WorldTowerStackerStage": {
        "entrance": "StackerRoomStart",
        "exit": "StackerRoomGoal",
    },
    "Special2WorldLavaStage": {
        "exit": "MoonGoal",
        "entrance": "CP_Entrance",
        "Special2WorldCloudStage": {
            "entrance": "room2_start",
            "exit": "room2_goal",
        },
        "Special2WorldKoopaStage": {
            "exit": "room3_goal",
            "entrance": "room3_start",
        },
    },
    "SwingSteelExStage": {
        "exit": "gragrareturn",
        "entrance": "gragra",
    },
    "TrampolineWallCatchExStage": {
        "exit": "CapTrampolineB",
        "entrance": "CapTrampolineA",
    },
    "TrexBikeExStage": {
        "exit": "bike02return",
        "entrance": "bike02",
    },
    "TsukkunClimbExStage": {
        "exit": "tukkun001_exit",
        "entrance": "tukkun001_enter",
    },
    "TsukkunRotateExStage": {
        "exit": "tukkun000_exit",
        "entrance": "tukkun000_enter",
    },
    "WanwanClashExStage": {
        "exit": "WanwanExGoal",
        "entrance": "WanwanExStart",
    },
    "WaterTubeExStage": {
        "exit": "EX_2DHosui_Exit",
        "entrance": "EX_2DHosui",
    },
    "WaterValleyExStage": {
        "exit": "SeaWorldEX1b",
        "entrance": "SeaWorldEX1a",
    },
    "WindBlowExStage": {
        "exit": "WindBlowExGoal",
        "entrance": "WindBlowExStart",
    },
    "AnimalChaseExStage": {
        "entrance": "EX_AnimalChase",
    },
    "ByugoPuzzleExStage": {
        "entrance": "ByugoPuzzle",
    },
    "CapRotatePackunExStage": {
        "entrance": "kaitendokan",
    },
    "CityWorldFactoryStage": {
        "entrance": "under001enter",
    },
    "CityWorldSandSlotStage": {
        "entrance": "Bonus",
    },
    "ClashWorldShopStage": {
        "entrance": "Kinopio",
    },
    "Cube2DExStage": {
        "entrance": "cube",
    },
    "DonsukeExStage": {
        "entrance": "donsuke",
    },
    "DotHardExStage": {
        "entrance": "PeachWorldEx2a",
    },
    "FastenerExStage": {
        "entrance": "FastenerEx",
    },
    "ForestWorldCloudBonusExStage": {
        "entrance": "EXCloud",
    },
    "ForestWorldWoodsCostumeStage": {
        "entrance": "Explorer_Bonus",
    },
    "ForestWorldWoodsTreasureStage": {
        "entrance": "TreasureTree",
    },
    "FrogSearchExStage": {
        "entrance": "FrogSearchExStageEnt",
    },
    "FukuwaraiKuriboStage": {
        "entrance": "Fukuwarai",
    },
    "GotogotonExStage": {
        "entrance": "Goton",
    },
    "HomeShipInsideStage": {
        "entrance": "HomeEntrance",
    },
    "IceWalkerExStage": {
        "entrance": "FigureWalker",
    },
    "JangoExStage": {
        "entrance": "ClashWorldMoonEX2",
    },
    "KaronWingTowerStage": {
        "entrance": "Patakaron02",
    },
    "KillerRoadExStage": {
        "entrance": "KillerRoad",
    },
    "LakeWorldShopStage": {
        "entrance": "LakeWorldShop",
    },
    "LavaWorldExcavationExStage": {
        "entrance": "MartinCubeEx",
    },
    "LavaWorldShopStage": {
        "entrance": "shop_lava",
    },
    "LavaWorldTreasureStage": {
        "entrance": "TreasureEventWorldLava",
    },
    "MoonWorldShopRoom": {
        "entrance": "ddd",
    },
    "MoonWorldSphinxRoom": {
        "entrance": "ggg",
    },
    "MoonWorldWeddingRoomStage": {
        "entrance": "aaa",
        "secret": "fff",
    },
    "Note2D3DRoomExStage": {
        "entrance": "onpu",
    },
    "PeachWorldCastleStage": {
        "entrance": "PeachCastleGate",
    },
    "PeachWorldPictureBossForestStage": {
        "entrance": "BossForestA",
        "exit": "PictureBossForest",
    },
    "PeachWorldPictureBossKnuckleStage": {
        "entrance": "BossKnuckleA",
        "exit": "PictureBossKnuckle",
    },
    "PeachWorldPictureBossMagmaStage": {
        "entrance": "BossMagmaA",
        "exit": "PictureBossMagma",
    },
    "PeachWorldPictureMofumofuStage": {
        "entrance": "MofumofuA",
        "exit": "PictureMofumofu",
    },
    "PeachWorldShopStage": {
        "entrance": "PeachWorldShopA",
    },
    "RadioControlExStage": {
        "entrance": "car",
    },
    "RocketFlowerExStage": {
        "entrance": "rocket",
    },
    "SandWorldCostumeStage": {
        "entrance": "abc",
    },
    "SandWorldPyramid000Stage": {
        "entrance": "pyramid01",
        "exit": "pyramid02"
    },
    "SandWorldPyramid001Stage": {
        "entrance": "pyramid03",
        "exit": "pyramid04",
    },
    "SandWorldSecretStage": {
        "entrance": "hide",
    },
    "SandWorldShopStage": {
        "shop": "bar1",
        "employee": "bar2",
    },
    "SandWorldSlotStage": {
        "entrance": "town"
    },
    "SandWorldUnderground001Stage": {
        "entrance": "start",
        "exit": "Out",
        "entrance2": "Yadokari00"
    },
    "SandWorldVibrationStage": {
        "entrance": "shindo",
    },
    "SeaWorldCostumeStage": {
        "entrance": "CostumeEventSeaWorld",
    },
    "SeaWorldSecretStage": {
        "entrance": "TreasureEventWorldSea",
    },
    "SeaWorldSneakingManStage": {
        "entrance": "RoomEventWorldSea",
    },
    "SeaWorldVibrationStage": {
        "entrance": "shindo_Lv2",
    },
    "SkyWorldCostumeStage": {
        "entrance": "byoubu",
    },
    "SkyWorldShopStage": {
        "entrance": "shop"
    },
    "SkyWorldTreasureStage": {
        "entrance": "shop_dress",
    },
    "SnowWorldCloudBonusExStage": {
        "entrance": "EX_SkyBonus",
    },
    "SnowWorldCostumeStage": {
        "entrance": "SnowCostumeEx",
    },
    "SnowWorldLobby000Stage": {
        "entrance": "RaceEntrance",
        "exit": "RaceTrackExit",
    },
    "SnowWorldLobbyExStage": {
        "entrance": "MoonRace",
    },
    "SnowWorldShopStage": {
        "entrance": "ShopDoor",
    },
    "Special2WorldCloudStage": {
        "entrance": "room2_start",
        "exit": "room2_goal",
    },
    "Special2WorldKoopaStage": {
        "exit": "room3_goal",
        "entrance": "room3_start",
    },
    "Theater2DExStage": {
        "entrance": "theater",
    },
    "TogezoRotateExStage": {
        "entrance": "SeaWorldMoonEX2",
    },
    "TrexPoppunExStage": {
        "entrance": "RexPoppunEx",
    },
    "YoshiCloudExStage": {
        "entrance": "PeachWorldEx1a",
    },
    "SnowWorldTownStage": {
        "entrance": "SnowUGEnt",
        "exit": "SnowUGExit",
        "SnowWorldCostumeStage": "SnowCostumeEx",
        "SnowWorldLobby000Stage": {
            "entrance": "RaceEntrance",
            "exit": "RaceTrackExit",
        },
        "SnowWorldShopStage": "ShopDoor",
    },
    "SandWorldUnderground000Stage": {
        "entrance": "icestart",
        "exit": "Yadokari00",
    },
    "SandWorldRotateExStage": {
        "entrance": "biru",
        "exit": "birureturn",
    },
    "FogMountainExStage": {
        "entrance": "EX_Mist",
    },
    "PoleGrabCeilExStage": {
        "entrance": "tenjo",
        "exit": "tenjo2",
    },
    "CloudExStage": {
        "entrance": "SeaWorldEX2",
        "exit": "SeaWorldEX2Return",
    },
    "LavaBonus1Zone": {
        "entrance": "town_lava",
    },
    "DotTowerExStage": {
        "entrance": "BossRaidWorldEx01_Eixt",
        "exit": "BossRaidWorldEx01_Eixt2"
    },
    "BikeSteelNoCapExStage": {
        "exit": "BikeSteelNoCapEx_Exit",
        "entrance": "BikeSteelNoCapEx",
    },
    "PackunPoisonNoCapExStage": {
        "exit": "PackunPoisonNoCapEx_Exit",
        "entrance": "PackunPoisonNoCapEx",
    },
    "ShootingCityYoshiExStage": {
        "entrance": "ShootingCityYoshiEx",
        "exit": "ShootingCityYoshiEx_Exit",
    },
    "SenobiTowerYoshiExStage": {
        "entrance": "SenobiTowerYoshiEx",
        "exit": "SenobiTowerYoshiEx_Exit",
    },
    "LavaWorldUpDownYoshiExStage": {
        "entrance": "LavaWorldUpDownYoshiEx",
        "exit": "LavaWorldUpDownYoshiEx_Exit",
    },
    "KillerRoadNoCapExStage": {
        "entrance": "KillerRoadNoCapEx",
    },
    "RevengeBossMagmaStage": {
        "entrance": "PictureBossMagma",
        "exit": 'PictureBossMagma'
    },
    "RevengeMofumofuStage": {
        "entrance": "PictureMofumofu",
        "exit": 'PictureMofumofu'
    },
    "RevengeBossRaidStage": {
        "entrance": "PictureBossRaid",
        "exit": 'PictureBossRaid'
    },
    "RevengeForestBossStage": {
        "entrance": "PictureBossForest",
        "exit": 'PictureBossForest'
    },
    "RevengeBossKnuckleStage": {
        "entrance": "PictureBossKnuckle",
        "exit": 'PictureBossKnuckle'
    },
    "RevengeGiantWanderBossStage": {
        "entrance": "PictureGiantWanderBoss",
        "exit": 'PictureGiantWanderBoss'
    },
    "FukuwaraiMarioStage": {
        "entrance": "Fukuwarai2",
    },
    "PeachWorldCostumeStage": {
        "entrance": "CostumeEventWorldPeach",
    },

    # Over worlds
    # replace with SMOEntranceData.name : id
    'CapWorldHomeStage': {
        'CapWorldTowerStage':
            {
                'entrance' : 'Ex',
                'exit': 'Goal'
            },
        'PoisonWaveExStage': 'PoisonWaveExExit',
        'FrogSearchExStage': 'FrogSearchExStageEnt',
        'PushBlockExStage': 'PushBlockExStageEntDokan',
        'RollingExStage': 'rollinggoal',
        # 'rollingstart': 'RollingExStage', # don't come out of entrance if exit pipe is available
        },

    'WaterfallWorldHomeStage': {
        'TrexPoppunExStage': 'RexPoppunEx',
        'WanwanClashExStage': 'WanwanExGoal',
        'Lift2DExStage': 'Lift2DExit',
        'CapAppearExStage': 'CapAppearExExit',
        'WindBlowExStage': 'WindBlowExGoal',
        },

    'SandWorldHomeStage': {
        'SandWorldPyramid000Stage': {
            'entrance': 'pyramid01',
            'exit': 'pyramid02',
        },
        'SandWorldPyramid001Stage': {
            'entrance': 'pyramid03',
            'exit': 'pyramid04',
        },
        'SandWorldShopStage': {
            'shop': 'bar1',
            'employee': 'bar2',
        },
        'SandWorldSecretStage': 'hide',
        'SandWorldUnderground001Stage': 'Out',
        'SandWorldMeganeExStage': 'anki2',
        'SandWorldPressExStage': {
            'entrance0': 'arijigoku',
            'entrance': 'arijigoku1',
            'exit': 'arijigoku2',
        },
        'SandWorldSphinxExStage': {
            "entrance0": 'aaa',
            "entrance": 'run00',
            "exit": 'run00return',
        },
        'SandWorldKillerExStage': {
            "entrance": 'doukutu1',
            "exit": 'doukutu2',
        },
        'SandWorldVibrationStage': 'shindo',
        'SandWorldUnderground000Stage': 'Under01',
        'MeganeLiftExStage': 'meganelift02',
        'RocketFlowerExStage': 'rocket',
        'WaterTubeExStage': 'EX_2DHosui_Exit',
        'SandWorldCostumeStage': 'abc',
        'SandWorldSlotStage': 'town',
        'SandWorldRotateExStage': 'birureturn',
        "SandWorldPyramidMural": {
            'entrance': 'pyramid02',
            'exit': 'pyramid03',
        },
    },

    'ForestWorldHomeStage': {
        'ForestWorldTowerStage': {
            'entrance': 'Tower001',
            'exit': 'Tower002'
            },
        'ForestWorldBossStage': 'boss002',
        'ForestWorldWoodsStage':{
            'entrance1': 'Jyukai001v',
            'entrance3': 'Jyukai003v',
        },

        'FogMountainExStage': 'EX_Mist',
        'ForestWorldCloudBonusExStage': 'EXCloud',
        'ForestWorldWaterExStage': 'EX_Water_Exit',
        'ForestWorldBonusStage': 'bonus2',
        'RailCollisionExStage': 'EX_RailCollision_Exit',
        'ShootingElevatorExStage': 'EX_Tankuro_Exit',
        'AnimalChaseExStage': 'EX_AnimalChase',
        'PackunPoisonExStage': 'PoisonEx_Exit',
        'KillerRoadExStage': 'KillerRoad', # Might need a new exit pipe for coming out of this exit in wrong scenario
        },

    'LakeWorldHomeStage': {
        'FrogPoisonExStage': 'LakeWorldMoonEX1b',
        'GotogotonExStage': 'Goton',
        'TrampolineWallCatchExStage': 'CapTrampolineB',
        'LakeWorldShopStage': 'LakeWorldShop',
        'FastenerExStage' : 'FastenerEx'
        },

    'CloudWorldHomeStage': {
        'FukuwaraiKuriboStage': 'Fukuwarai',
        'Cube2DExStage': 'cube',
        },

    'ClashWorldHomeStage': {
        'ClashWorldShopStage': 'Kinopio',
        'JangoExStage': 'ClashWorldMoonEX2',
        'ImomuPoisonExStage': 'imomu_02',
    },

    'CityWorldHomeStage': {
        'CityWorldMainTowerStage': {
            "entrance": 'main_enter',
            'exit': 'main_exit',
        },
        'CityWorldShop01Stage': {
            'regional': 'shop_corect',
            'coin': 'shop_coin',
        },
        'Note2D3DRoomExStage': 'onpu',
        'RadioControlExStage': 'car',
        'CityWorldSandSlotStage': 'Bonus',
        'CapRotatePackunExStage': 'kaitendokan',
        'CityPeopleRoadStage': {
            'entrance': 'gunsyu',
            'exit': 'gunsyudokan',
        },
        'ShootingCityExStage': 'taxi',
        'Theater2DExStage': 'theater',
        'CityWorldFactoryStage': 'under001enter',
        'PoleKillerExStage': 'boureturn',
        'ElectricWireExStage': 'densendokan',
        'TrexBikeExStage': 'bike02return',
        'SwingSteelExStage': 'gragrareturn',
        'DonsukeExStage': 'donsuke',
        'BikeSteelExStage': 'bikereturn',
        'PoleGrabCeilExStage': 'tenjo',
        },

    'SeaWorldHomeStage': {
        'SeaWorldVibrationStage': 'shindo_Lv2',
        'TogezoRotateExStage': 'SeaWorldMoonEX2',
        'ReflectBombExStage': 'SeaWorldMoonEX1b',
        'SeaWorldCostumeStage': 'CostumeEventSeaWorld',
        'WaterValleyExStage': 'SeaWorldEX1b',
        'SenobiTowerExStage': 'SeaWorldEX3b',
        'SeaWorldSneakingManStage': 'RoomEventWorldSea',
        'SeaWorldUtsuboCaveStage': {
            'entrance': 'PukupukuCaveStart',
            'exit': 'PukupukuCaveGoal',
        },
        'SeaWorldSecretStage': 'TreasureEventWorldSea',
        'CloudExStage': 'SeaWorldEX2Return'
        },

    'SnowWorldHomeStage': {
        'IceWaterDashExStage': 'EX_IceWaterDash_Exit',
        'ByugoPuzzleExStage': 'ByugoPuzzle',
        'IceWalkerExStage': 'FigureWalker',
        'SnowWorldCloudBonusExStage': 'EX_SkyBonus',
        'SnowWorldLobbyExStage': 'MoonRace',
        'SnowWorldTownStage': 'SnowUGExit',
        'IceWaterBlockExStage': 'EX_IceWater_Exit',
        'TestShirai011Stage': 'EX_IceWaterDash_Exit',
        'KillerRailCollisionExStage': 'EX_RailCol2_Exit',
        },

    'LavaWorldHomeStage': {
        'ForkExStage': 'ForkEX',
        'LavaWorldExcavationExStage': 'MartinCubeEx',
        'LavaWorldUpDownExStage': 'KeyMoveExDokan',
        'LavaWorldBubbleLaneExStage': 'PechoBubbleExDokan',
        'LavaWorldClockExStage': 'BBQExDokan',
        'LavaWorldCostumeStage': 'CostumeOut',
        'LavaWorldFenceLiftExStage': 'FenceLiftExdokan',
        'CapAppearLavaLiftExStage': 'LavaLiftExdokan',
        'GabuzouClockExStage': 'GabuzouClockExdokan',
        'LavaBonus1Zone': 'town_lava',
        'LavaWorldShopStage': 'shop_lava',
        'LavaWorldTreasureStage': 'TreasureEventWorldLava',
        },

    'BossRaidWorldHomeStage': {
        'DotTowerExStage': 'BossRaidWorldEx01_Eixt',
        'BullRunExStage': 'BossRaidWorldMoonEx02_Exit',
        },

    'SkyWorldHomeStage': {
        'SkyWorldShopStage': 'shop',
        'SkyWorldCostumeStage':'byoubu',
        'SkyWorldCloudBonusExStage':'sora001',
        'SkyWorldTreasureStage':'shop_dress',
        'TsukkunRotateExStage':'tukkun000_exit',
        'JizoSwitchExStage':'jizo02',
        'TsukkunClimbExStage':'tukkun001_exit',
        'KaronWingTowerStage':'Patakaron02',
        },

    'MoonWorldHomeStage': {
        'MoonWorldWeddingRoomStage': {
            'entrance':'aaa',
            'secret': 'fff',
        },
        'MoonWorldCaptureParadeStage': {
            'exit':'vvv',
            'entrance': 'bbb',
        },
        'MoonWorldSphinxRoom': 'ggg',
        'MoonWorldShopRoom': 'ddd',
        'Galaxy2DExStage': 'dot01',
        'MoonAthleticExStage': 'moon_exit',
        },

    'PeachWorldHomeStage': {
        'PeachWorldCastleStage': 'PeachCastleGate',
        'PeachWorldShopStage': 'PeachWorldShopA',
        'PeachWorldPictureBossMagmaStage': 'BossMagmaA',
        'PeachWorldPictureMofumofuStage': 'MofumofuA',
        'PeachWorldPictureBossKnuckleStage': 'BossKnuckleA',
        'PeachWorldPictureBossForestStage': 'BossForestA',
        'YoshiCloudExStage': 'PeachWorldEx1a',
        'PeachWorldPictureGiantWanderBossStage': 'GiantWanderBossB',
        'PeachWorldPictureBossRaidStage': 'BossRaidB',
        'DotHardExStage': 'PeachWorldEx2a',
        'PeachWorldCostumeStage': 'CostumeEventWorldPeach',
        'FukuwaraiMarioStage': 'Fukuwarai2',
        },

    'Special1WorldHomeStage': {

        'Special1WorldTowerCapThrowerStage': {
            'entrance': 'CapThrowerRoomStart',
            'exit': 'CapThrowerRoomGoal',
        },
        'Special1WorldTowerBombTailStage': {
            'entrance': 'BombTailRoomStart',
            'exit': 'BombTailRoomGoal',
        },
        'Special1WorldTowerFireBlowerStage': {
            'entrance': 'FireBlowerRoomStart',
            'exit': 'FireBlowerRoomGoal',
        },
        'Special1WorldTowerStackerStage': {
            'entrance': 'StackerRoomStart',
            'exit': 'StackerRoomGoal',
        },
        'BikeSteelNoCapExStage': 'BikeSteelNoCapEx_Exit',
        'PackunPoisonNoCapExStage': 'PackunPoisonNoCapEx_Exit',
        'SenobiTowerYoshiExStage': 'SenobiTowerYoshiEx_Exit',
        'LavaWorldUpDownYoshiExStage': 'LavaWorldUpDownYoshiEx_Exit',
        'ShootingCityYoshiExStage': 'ShootingCityYoshiEx_Exit',
        'KillerRoadNoCapExStage': 'KillerRoadNoCapEx',
        },

    'Special2WorldHomeStage': {
        'Special2WorldLavaStage': {
            'entrance':'CP_Entrance',
            'exit': 'MoonGoal',
            }
        },
}

stage_names = [
    "AnimalChaseExStage",
    "BikeSteelExStage",
    "BossRaidWorldHomeStage",
    "BullRunExStage",
    "ByugoPuzzleExStage",
    "CapAppearExStage",
    "CapAppearLavaLiftExStage",
    "CapRotatePackunExStage",
    "CapWorldHomeStage",
    "CapWorldTowerStage",
    "CityPeopleRoadStage",
    "CityWorldFactoryStage",
    "CityWorldHomeStage",
    "CityWorldMainTowerStage",
    "CityWorldSandSlotStage",
    "CityWorldShop01Stage",
    "ClashWorldHomeStage",
    "ClashWorldShopStage",
    "CloudWorldHomeStage",
    "Cube2DExStage",
    "DonsukeExStage",
    "DotHardExStage",
    "ElectricWireExStage",
    "FastenerExStage",
    "ForestWorldBonusStage",
    "ForestWorldBossStage",
    "ForestWorldCloudBonusExStage",
    "ForestWorldHomeStage",
    "ForestWorldTowerStage",
    "ForestWorldWaterExStage",
    "ForestWorldWoodsCostumeStage",
    "ForestWorldWoodsStage",
    "ForestWorldWoodsTreasureStage",
    "ForkExStage",
    "FrogPoisonExStage",
    "FrogSearchExStage",
    "FukuwaraiKuriboStage",
    "GabuzouClockExStage",
    "Galaxy2DExStage",
    "GotogotonExStage",
    "HomeShipInsideStage",
    "IceWalkerExStage",
    "IceWaterBlockExStage",
    "IceWaterDashExStage",
    "ImomuPoisonExStage",
    "JangoExStage",
    "JizoSwitchExStage",
    "KaronWingTowerStage",
    "KillerRailCollisionExStage",
    "KillerRoadExStage",
    "LakeWorldHomeStage",
    "LakeWorldShopStage",
    "LavaWorldBubbleLaneExStage",
    "LavaWorldClockExStage",
    "LavaWorldCostumeStage",
    "LavaWorldExcavationExStage",
    "LavaWorldFenceLiftExStage",
    "LavaWorldHomeStage",
    "LavaWorldShopStage",
    "LavaWorldTreasureStage",
    "LavaWorldUpDownExStage",
    "Lift2DExStage",
    "MeganeLiftExStage",
    "MoonAthleticExStage",
    "MoonWorldCaptureParadeStage",
    "MoonWorldHomeStage",
    "MoonWorldKoopa1Stage",
    "MoonWorldKoopa2Stage",
    "MoonWorldShopRoom",
    "MoonWorldSphinxRoom",
    "MoonWorldWeddingRoomStage",
    "Note2D3DRoomExStage",
    "PackunPoisonExStage",
    "PeachWorldCastleStage",
    "PeachWorldHomeStage",
    "PeachWorldPictureBossForestStage",
    "PeachWorldPictureBossKnuckleStage",
    "PeachWorldPictureBossMagmaStage",
    "PeachWorldPictureBossRaidStage",
    "PeachWorldPictureGiantWanderBossStage",
    "PeachWorldPictureMofumofuStage",
    "PeachWorldShopStage",
    "PoisonWaveExStage",
    "PoleKillerExStage",
    "PushBlockExStage",
    "RadioControlExStage",
    "RailCollisionExStage",
    "ReflectBombExStage",
    "RocketFlowerExStage",
    "RollingExStage",
    "SandWorldCostumeStage",
    "SandWorldHomeStage",
    "SandWorldKillerExStage",
    "SandWorldMeganeExStage",
    "SandWorldPressExStage",
    "SandWorldPyramid000Stage",
    "SandWorldPyramid001Stage",
    "SandWorldSecretStage",
    "SandWorldShopStage",
    "SandWorldSlotStage",
    "SandWorldSphinxExStage",
    "SandWorldUnderground000Stage",
    "SandWorldUnderground001Stage",
    "SandWorldVibrationStage",
    "SeaWorldCostumeStage",
    "SeaWorldHomeStage",
    "SeaWorldSecretStage",
    "SeaWorldSneakingManStage",
    "SeaWorldUtsuboCaveStage",
    "SeaWorldVibrationStage",
    "SenobiTowerExStage",
    "ShootingCityExStage",
    "ShootingElevatorExStage",
    "SkyWorldCloudBonusExStage",
    "SkyWorldCostumeStage",
    "SkyWorldHomeStage",
    "SkyWorldShopStage",
    "SkyWorldTreasureStage",
    "SnowWorldCloudBonusExStage",
    "SnowWorldCostumeStage",
    "SnowWorldHomeStage",
    "SnowWorldLobby000Stage",
    "SnowWorldLobbyExStage",
    "SnowWorldShopStage",
    "SnowWorldTownStage",
    "Special1WorldHomeStage",
    "Special1WorldTowerBombTailStage",
    "Special1WorldTowerCapThrowerStage",
    "Special1WorldTowerFireBlowerStage",
    "Special1WorldTowerStackerStage",
    "Special2WorldCloudStage",
    "Special2WorldHomeStage",
    "Special2WorldKoopaStage",
    "Special2WorldLavaStage",
    "SwingSteelExStage",
    "Theater2DExStage",
    "TogezoRotateExStage",
    "TrampolineWallCatchExStage",
    "TrexBikeExStage",
    "TrexPoppunExStage",
    "TsukkunClimbExStage",
    "TsukkunRotateExStage",
    "WanwanClashExStage",
    "WaterfallWorldHomeStage",
    "WaterTubeExStage",
    "WaterValleyExStage",
    "WindBlowExStage",
    "YoshiCloudExStage",
    'SandWorldRotateExStage',
    'FogMountainExStage',
    'PoleGrabCeilExStage',
    'CloudExStage',
    'LavaBonus1Zone',
    'DotTowerExStage',
    'BikeSteelNoCapExStage',
    'PackunPoisonNoCapExStage',
    'ShootingCityYoshiExStage',
    'SenobiTowerYoshiExStage',
    'LavaWorldUpDownYoshiExStage',
    'KillerRoadNoCapExStage',
    'RevengeBossMagmaStage',
    'RevengeMofumofuStage',
    'RevengeBossRaidStage',
    'RevengeForestBossStage',
    'RevengeBossKnuckleStage',
    'RevengeGiantWanderBossStage',
    'FukuwaraiMarioStage',
    'PeachWorldCostumeStage',
]

stage_ids = [
    'jizo01',
    'dot00',
    'start',
    'LavaWorldUpDownYoshiEx_Exit',
    'CapTrampolineB',
    'PoisonWaveExEnt',
    'arijigoku',
    'SeaWorldEX1a',
    'BossRaidWorldMoonEx02_Exit',
    'SeaWorldEX1b',
    'under001enter',
    'Tower002',
    'SeaWorldMoonEX1b',
    'Bonus',
    'None', # Not needed
    'KeyMoveEx',
    'ShootingCityYoshiEx_Exit',
    'CP_Entrance',
    'PoisonEx_Exit',
    'donsuke',
    'cube',
    'pyramid03',
    'vvv',
    'EX_RailCollision_Exit',
    'main_enter',
    'boureturn',
    'moon',
    'pyramid02',
    'bar1',
    'FrogSearchExStageEnt',
    'FireBlowerRoomGoal',
    'MoonRace',
    'gunsyu',
    'Jyukai002',
    'LakeWorldMoonEX1b',
    'BBQExDokan',
    'BossKnuckleA',
    'Kinopio',
    'StackerRoomStart',
    'Tower001',
    'bbb',
    'aaa',
    'KeyMoveExDokan',
    'run00',
    'CostumeEventSeaWorld',
    'dot01',
    'bike02',
    'tukkun000_enter',
    'RaceEntrance',
    'SnowCostumeEx',
    'wall',
    'tukkun001_exit',
    'FenceLiftEx',
    'CostumeOut',
    'FenceLiftExdokan',
    'MofumofuA',
    'BBQEx',
    'WindBlowExStart',
    'Lift2D',
    'Fukuwarai',
    'LakeWorldMoonEX1a',
    'EXCloud',
    'SeaWorldMoonEX1a',
    'SenobiTowerYoshiEx_Exit',
    'Jyukai003',
    'BombTailRoomGoal',
    'EX_AnimalChase',
    'ForkEX',
    'town',
    'town_lava',
    'PeachWorldEx2a',
    'main_exit',
    'Goton',
    'CapAppearExEnt',
    'WanwanExStart',
    'bou',
    'Explorer_Bonus',
    'ddd',
    'EX_IceWaterDash',
    'abc',
    'CapAppearExExit',
    'BossRaidB',
    'jizo02',
    'LavaLiftEx',
    'EX_SkyBonus',
    'BikeSteelNoCapEx_Exit',
    'imomu_02',
    'meganelift02',
    'Jyukai001v',
    'ggg',
    'taxireturn',
    'shop_dress',
    'room2_start',
    'room3_start',
    'sora001',
    'TreasureEventWorldSea',
    'arijigoku2',
    'rocket',
    'CapTrampolineA',
    'EX_IceWater_Exit',
    'Jyukai001',
    'LakeWorldShop',
    'EX_RailCollision',
    'bonus',
    'kaitendokan',
    'shindo',
    'PushBlockExStageEnt',
    'pyramid01',
    'densendokan',
    'EX_RailCol2',
    'StackerRoomGoal',
    'Ex',
    'icestart',
    'PechoBubbleExDokan',
    'PechoBubbleEx',
    'onpu',
    'PeachWorldEx1a',
    'SeaWorldEX3b',
    'EX_Tankuro_Exit',
    'PackunPoisonNoCapEx_Exit',
    'SeaWorldMoonEX2',
    'meganelift01',
    'PushBlockExStageEntDokan',
    'GiantWanderBossA',
    'moon_exit',
    'Goal',
    'car',
    'bar2',
    'RaceTrackExit',
    'ShootingCityYoshiEx',
    'bike02return',
    'shindo_Lv2',
    'room2_goal',
    'EX_IceWater',
    'ShopDoor',
    'ByugoPuzzle',
    'EX_Water_Exit',
    'BombTailRoomStart',
    'taxi',
    'densen',
    'ClashWorldMoonEX2',
    'GabuzouClockEx',
    'MartinCubeEx',
    'FireBlowerRoomStart',
    'ccc',
    'PeachCastleGate',
    'SenobiTowerYoshiEx',
    'RexPoppunEx',
    'PukupukuCaveGoal',
    'tukkun001_enter',
    'gragrareturn',
    'EX_Water',
    'WanwanExGoal',
    'Lift2DExit',
    'theater',
    'Yadokari00',
    'BossForestA',
    'imomu_01',
    'PeachWorldShopA',
    'rollinggoal',
    'EX_2DHosui_Exit',
    'LavaLiftExdokan',
    'GabuzouClockExdokan',
    'anki2',
    'boss001',
    'FastenerEx',
    'FigureWalker',
    'shop',
    'shop_lava',
    'CapThrowerRoomStart',
    'ForkEX2',
    'arijigoku1',
    'CapThrowerRoomGoal',
    'Jyukai003v',
    'pyramid04',
    'doukutu2',
    'PoisonWaveExExit',
    'SnowUGEnt',
    'BossMagmaA',
    'KillerRoad',
    'PoisonEx',
    'BossRaidWorldMoonEx02_Enter',
    'bonus2',
    'SnowUGExit',
    'BossRaidA',
    'Jyukai004',
    'Out',
    'EX_IceWaterDash_Exit',
    'hide',
    'byoubu',
    'shop_coin',
    'fff',
    'bike',
    'PukupukuCaveStart',
    'boss002',
    'GiantWanderBossB',
    'MoonGoal',
    'Patakaron02',
    'doukutu1',
    'gunsyudokan',
    'room3_goal',
    'EX_2DHosui',
    'run00return',
    'WindBlowExGoal',
    'EX_Tankuro',
    'RoomEventWorldSea',
    'LavaWorldUpDownYoshiEx',
    'rollingstart',
    'bikereturn',
    'shop_corect',
    'EX_RailCol2_Exit',
    'Under01',
    'SeaWorldEX3a',
    'TreasureEventWorldLava',
    'TreasureTree',
    'CostumeEventWorldLava',
    'tukkun000_exit',
    'gragra',
    'PictureBossRaid',
    'PictureGiantWanderBoss',
    'biru',
    'birureturn',
    'EX_Mist',
    'tenjo',
    'tenjo2',
    'SeaWorldEX2',
    'BossRaidWorldEx01_Eixt',
    'BossRaidWorldEx01_Eixt2',
    'BikeSteelNoCapEx',
    'PackunPoisonNoCapEx',
    'KillerRoadNoCapEx',
    'PictureBossMagma',
    'PictureMofumofu',
    'PictureBossForest',
    'PictureBossKnuckle',
    'Fukuwarai2',
    'CostumeEventWorldPeach',
    'SeaWorldEX2Return',
    'aaaSand',
]

def create_entrances(self):
    world_sub_area_exits = [
        # (SMORegion.cap_kingdom_intro, {
        #     SMOEntranceData.top_hat_tower: None,
        # }),
        # (SMORegion.cap_kingdom_topper, {
        #     SMOEntranceData.top_hat_tower_end: None,
        # }),
        (SMORegion.cap_kingdom, {
            SMOEntranceData.poison_tides: Or(
                CanCapture(SMOItemData.paragoomba),
                CanReachRegion(SMORegion.cap_kingdom_topper)
            ),
            SMOEntranceData.frog_pond: HasAny(*cappy),
            SMOEntranceData.rolling_lane: Has(SMOItemData),
        }),
        (SMORegion.cap_kingdom_topper, {
            SMOEntranceData.push_blocks: HasAny(*cappy)
        }),
        # (SMORegion.cap_kingdom_moon_rock, {}
        #
        # , SMORuleOperation.NONE)
        (SMORegion.cascade_kingdom, {
            SMOEntranceData.chasm_lifts: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.cascade_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.t_rex_nest: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.cascade_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.chain_chomp_cave: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.cascade_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.gusty_bridges: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.cascade_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.mysterious_clouds: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.cascade_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.cascade_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.sand_kingdom, {
            SMOEntranceData.ice_cave: None,
            SMOEntranceData.bullet_bill_maze: None,
            SMOEntranceData.jaxi_ruins: None,
            SMOEntranceData.inverted_pyramid_lower_interior: None,
            SMOEntranceData.inverted_pyramid_upper_interior: create_access_rule(self, [
                (SMORuleCondition.ENTRANCE,
                 [SMORegion.sand_kingdom, f"{SMOEntranceData.inverted_pyramid_lower_interior} Unique Exit",
                  SMOEntranceDataType.EXIT], SMORuleOperation.OR),
                (SMORuleCondition.ENTRANCE,
                 [SMORegion.sand_kingdom, f"{SMOEntranceData.inverted_pyramid_upper_interior} Unique Exit",
                  SMOEntranceDataType.EXIT], SMORuleOperation.NONE)
            ]),
            SMOEntranceData.moe_eye_invisible_maze: None,
            SMOEntranceData.sand_kingdom_shop: None,
            SMOEntranceData.sand_sphynx_vault: None,
            SMOEntranceData.underground_ruins: None,
            SMOEntranceData.sand_costume_bonus_dancing_room : (create_access_rule(self, [
                (SMORuleCondition.ITEM ,[SMOItemData.sombrero, SMOItemData.poncho], SMORuleOperation.OR),
                (SMORuleCondition.ITEM, [SMOItemData.skeleton_suit], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.sand_slots: None,
            SMOEntranceData.sand_kingdom_employee: None,
            SMOEntranceData.sand_rumbling_floor_house: None,
            SMOEntranceData.deepest_underground_shortcut: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.sand_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.strange_neighborhood: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, [SMOItemData.mini_rocket], SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.sand_kingdom_peace, SMORuleOperation.NONE)
                 ])),
            SMOEntranceData.colossal_ruins: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.sand_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.freezing_waterway: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.sand_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.moe_eye_invisible_floor: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.sand_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.sand_kingdom_peace, {
        #
        # }),
        (SMORegion.top_of_the_inverted_pyramid, {
            #SMOEntranceData.inverted_pyramid_upper_interior_reverse: None,
        }),
        # (SMORegion.sand_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.wooded_kingdom, {
            SMOEntranceData.sky_garden_tower: None,
            SMOEntranceData.deep_woods_1: None,
            SMOEntranceData.deep_woods_3: None,
            SMOEntranceData.flooding_pipeway: None,
            SMOEntranceData.sherm_elevator: None,
            SMOEntranceData.wooded_flower_road: None,
            SMOEntranceData.secret_flower_field: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.sherm, SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.wooded_kingdom_post_broodals, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.spinning_platforms_treasure_vault: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.wooded_kingdom_post_broodals, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.walking_on_clouds: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.cascade_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.fog_wandering: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.mini_rocket, SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.wooded_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.sheep_herding: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.wooded_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.invisible_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.wooded_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.breakdown_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.wooded_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.wooded_kingdom_post_broodals, {
        #
        # }),
        # (SMORegion.wooded_kingdom_peace, {
        #     }),
        # (SMORegion.wooded_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.deep_woods, {
            SMOEntranceData.deep_woods_costume_bonus_treasure_chest: (create_access_rule( self, [
                (SMORuleCondition.ITEM, [SMOItemData.explorer_hat, SMOItemData.explorer_outfit], SMORuleOperation.NONE),
            ])),
            SMOEntranceData.deep_woods_treasure_trap: None,
            SMOEntranceData.deep_woods_2: None,
            SMOEntranceData.deep_woods_4: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.wooded_kingdom_post_broodals, SMORuleOperation.NONE)
            ])),
        }),
        (SMORegion.lake_kingdom, {
            SMOEntranceData.arch_repair: None,
            SMOEntranceData.zipper_chasm: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, [SMOItemData.zipper], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.bouncy_flowers: None,
            SMOEntranceData.lake_kingdom_shop: None,
            SMOEntranceData.poison_swamp: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.lake_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.lake_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.cloud_kingdom_revisit, {
            SMOEntranceData.cloud_picture_match: None,
            SMOEntranceData.king_of_the_cube: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.cloud_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.cloud_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.lost_kingdom, {
            SMOEntranceData.lost_kingdom_shop: None,
            SMOEntranceData.klepto_lava_bath: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.lost_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.tropical_wiggler_swamp: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.lost_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.lost_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.night_metro_kingdom, {
            SMOEntranceData.city_hall: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.spark_pylon, SMORuleOperation.OR),
                (SMORuleCondition.TRICK_EASY, SMORuleCondition.CAPTURE, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.metro_kingdom_shop: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.spark_pylon, SMORuleOperation.OR),
                (SMORuleCondition.TRICK_EASY, SMORuleCondition.CAPTURE, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.metro_kingdom_shop_regional: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.spark_pylon, SMORuleOperation.OR),
                (SMORuleCondition.TRICK_EASY, SMORuleCondition.CAPTURE, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.private_room: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.bullet_building: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.rc_race: (create_access_rule(self, [
                    (SMORuleCondition.CAPTURE, SMOItemData.rc_car, SMORuleOperation.AND),
                    (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.builder_outfit: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.AND),
                (SMORuleCondition.ITEM, [SMOItemData.builder_helmet, SMOItemData.builder_outfit], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.metro_slots: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.rotating_maze: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.manhole, SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.t_rex_escape: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.crowded_street: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.metro_siege: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.taxi, SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.high_rise: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.mini_rocket, SMORuleOperation.AND),
                (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.sewers: (create_access_rule(self, [
                    (SMORuleCondition.CAPTURE, SMOItemData.manhole, SMORuleOperation.AND),
                    (SMORuleCondition.REGION, SMORegion.day_metro_kingdom, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.projection_room: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.metro_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.swinging_scaffolding: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.metro_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.vanishing_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.metro_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.pitch_black_island: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.metro_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.day_metro_kingdom, {
        #     }),
        # (SMORegion.metro_kingdom_sewers, {
        #     SMOEntranceData.sewers: None,
        # }),
        # (SMORegion.metro_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.seaside_kingdom, {
            SMOEntranceData.seaside_rumbling_floor_cave: None,
            SMOEntranceData.spinning_maze: None,
            SMOEntranceData.wading_in_the_cloud_sea: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.mini_rocket, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.sandy_bottom: None,
            SMOEntranceData.narrow_valley: None,
            SMOEntranceData.sinking_island: None,
            SMOEntranceData.seaside_costume_bonus_dancing_room: None,
            SMOEntranceData.seaside_sphynx_treasure_vault: None,
            SMOEntranceData.underwater_tunnel: None,
            SMOEntranceData.pokio_bomb_aiming: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.seaside_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.seaside_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.snow_kingdom, {
            SMOEntranceData.shiveria: None,
            SMOEntranceData.rocket_flower_dash: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.ty_foo_sliding_puzzle: (create_access_rule(self, [
                    (SMORuleCondition.CAPTURE, SMOItemData.ty_foo, SMORuleOperation.AND),
                    (SMORuleCondition.REGION ,SMORegion.snow_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.ice_trace_walking: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.above_the_clouds: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.freezing_water: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.snow_flower_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.iceburn_circuit_class_a_lobby: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.snow_kingdom_moon_rock, SMORuleOperation.NONE)
                ])),
        }),
        # (SMORegion.snow_kingdom_peace, {
        #
        # }),
        # (SMORegion.snow_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.luncheon_kingdom, {
            SMOEntranceData.magma_swamp: None,
            SMOEntranceData.fork_flickin: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_post_broodals, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.luncheon_kingdom_shop: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_post_broodals, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.luncheon_costume_bonus_cooking_pots: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_post_broodals, SMORuleOperation.AND),
                (SMORuleCondition.ITEM,[SMOItemData.chef_hat, SMOItemData.chef_suit], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.luncheon_slots: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_post_broodals, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.cheese_excavate: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_meat, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.spinning_athletics: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_meat, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.magma_narrow_path: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_meat, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.luncheon_treasure_vault: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_meat, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.volcano_cave: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.rotating_gears_with_bitefrost: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.lava_islands: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.luncheon_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
        }),
        # (SMORegion.luncheon_kingdom_post_broodals, {
        #
        # }),

        # (SMORegion.luncheon_kingdom_meat, {
        #
        # }),
        # (SMORegion.luncheon_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.ruined_kingdom, {
            SMOEntranceData.roulette_tower: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE,[SMORegion.mini_rocket], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.chargin_chuck_arena: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.ruined_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
        }),
        # (SMORegion.ruined_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.infiltrate_bowsers_castle, {
            SMOEntranceData.bowsers_kingdom_shop: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_smart_bombing, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.folding_screen: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_smart_bombing, SMORuleOperation.AND),
                (SMORuleCondition.ITEM,[SMOItemData.samurai_helmet, SMOItemData.samurai_armor], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.dashing_above_the_clouds: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_mecha_broodal, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.spinning_tower: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_peace, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.jizos_adventure: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_peace, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.bowsers_treasure_vault: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_peace, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.hexagon_tower: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.wooden_tower: (create_access_rule(self, [
                (SMORuleCondition.REGION, SMORegion.bowser_kingdom_moon_rock, SMORuleOperation.NONE)
            ])),
        }),
        # (SMORegion.bowser_kingdom_smart_bombing, {
        #     }),
        # (SMORegion.bowser_kingdom_mecha_broodal, {
        #
        # }),
        # (SMORegion.bowser_kingdom_peace, {
        #
        # }),
        # (SMORegion.bowser_kingdom_moon_rock, {
        #
        # }),
        (SMORegion.moon_kingdom, {
            SMOEntranceData.inside_the_church: None,
            SMOEntranceData.moon_cave: None,
        }),
        (SMORegion.moon_kingdom_peace, {
            SMOEntranceData.moon_sphynx_vault: None,
            SMOEntranceData.moon_kingdom_shop: None,
        }),
        (SMORegion.moon_kingdom_moon_rock, {
            SMOEntranceData.giant_swings: None,
            SMOEntranceData.dot_galaxy: None,
        }),
        (SMORegion.mushroom_kingdom, {
            SMOEntranceData.peachs_castle: None,
            SMOEntranceData.mushroom_kingdom_shop: None,
            SMOEntranceData.painting_room_cookatiel: None,
            SMOEntranceData.painting_room_mecha_wiggler: None,
            SMOEntranceData.painting_room_knucklotec: None,
            SMOEntranceData.painting_room_torkdrift: None,
            SMOEntranceData.mushroom_well: None,
            SMOEntranceData.yoshi_in_the_sea_of_clouds: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.yoshi, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.painting_room_mollusque_lanceur: None,
            SMOEntranceData.painting_room_lord_of_lightning: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.yoshi, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.mushroom_picture_match : (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.mini_rocket, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.castle_courtyard : (create_access_rule(self, [
                (SMORuleCondition.ITEM, [SMOItemData.mario_64_cap, SMOItemData.mario_64_suit], SMORuleOperation.OR),
                (SMORuleCondition.ITEM, [SMOItemData.metal_mario_cap, SMOItemData.metal_mario_suit], SMORuleOperation.NONE)
            ])),
        }),
        (SMORegion.dark_side, {
            SMOEntranceData.dark_side_topper: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.spark_pylon, SMORuleOperation.NONE)
            ])),
            SMOEntranceData.dark_side_vanishing_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.dark_side_invisible_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.dark_side_breakdown_road: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.dark_side_siege: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.dark_side_sinking_island: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
            SMOEntranceData.dark_side_magma_swamp: (create_access_rule(self, [
                (SMORuleCondition.REGION,SMORegion.dark_side_peace, SMORuleOperation.NONE)
                ])),
        }),
        (SMORegion.dark_side_2 , {
            SMOEntranceData.dark_side_hariet: None,
        }),
        (SMORegion.dark_side_3 , {
            SMOEntranceData.dark_side_spewart: None,
        }),
        (SMORegion.dark_side_4 , {
            SMOEntranceData.dark_side_rango: None,
        }),

        # (SMORegion.dark_side_peace, {
        #
        # }),
        (SMORegion.darker_side, {
            SMOEntranceData.darker_side_main: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.frog, SMORuleOperation.NONE)
            ])),
        }),
        (SMORegion.darker_side_entrance, {
            SMOEntranceData.darker_side_pokio: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, [SMOItemData.lava_bubble, SMOItemData.uproot, SMOItemData.yoshi, SMOItemData.glydon, SMOItemData.volbonan], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.darker_side_bowser: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, SMOItemData.pokio, SMORuleOperation.NONE)
            ])),
        }),
        # (SMORegion.darker_side_climb, {
        #
        # }),
        # (SMORegion.darker_side_bowser, {
        #     SMOEntranceData.darker_side_end: (create_access_rule(self, [
        #         (SMORuleCondition.CAPTURE, SMOItemData.bowser, SMORuleOperation.NONE)
        #     ])),
        # }),
        # (SMORegion.darker_side_end, {
        #     SMOEntranceData.darker_side_tower: (create_access_rule(self, [
        #         (SMORuleCondition.CAPTURE, SMOItemData.spark_pylon, SMORuleOperation.NONE)
        #     ])),
        # }),

        # sub_areas
        # (SMORegion.top_hat_tower, {
        #     SMOEntranceData.top_hat_tower_end: (create_access_rule(self, [
        #         (SMORuleCondition.CAPTURE, SMOItemData.frog , SMORuleOperation.NONE)
        #     ])),
        # }),

        # (SMORegion.inverted_pyramid_lower_interior, {
        #     SMOEntranceData.inverted_pyramid_mural: None,
        # }),
        # (SMORegion.inverted_pyramid_mural, {
        #     SMOEntranceData.inverted_pyramid_upper_interior: None,
        # }),
        # (SMORegion.inverted_pyramid_upper_interior, {
        #     SMOEntranceData.top_of_the_inverted_pyramid: None,
        # }),
        (SMORegion.underground_ruins, {
            SMOEntranceData.deepest_underground: (create_access_rule(self, [
                (SMORuleCondition.CAPTURE, [SMOItemData.bullet_bill, SMOItemData.knucklotecs_fist], SMORuleOperation.NONE)
            ])),
        }),


        (SMORegion.shiveria, {
            SMOEntranceData.snowline_circuit_lobby: None,
            SMOEntranceData.freezing_room: (create_access_rule(self, [
                (SMORuleCondition.ITEM, [SMOItemData.snow_hood, SMOItemData.snow_suit], SMORuleOperation.NONE)
            ])),
            SMOEntranceData.snow_kingdom_shop: None,
        }),






        (SMORegion.painting_room_knucklotec, {
            SMOEntranceData.knucklotec_rematch: None,
        }),
        (SMORegion.painting_room_torkdrift, {
            SMOEntranceData.torkdrift_rematch: None,
        }),
        (SMORegion.painting_room_mecha_wiggler, {
            SMOEntranceData.mecha_wiggler_rematch: None,
        }),
        (SMORegion.painting_room_mollusque_lanceur, {
            SMOEntranceData.mollusque_lanceur_rematch: None,
        }),
        (SMORegion.painting_room_cookatiel, {
            SMOEntranceData.cookatiel_rematch: None,
        }),
        (SMORegion.painting_room_lord_of_lightning, {
            SMOEntranceData.lord_of_lightning_rematch: None,
        }),


        # (, {}),
        # (, {}),
        # (, {}),
        # (, {}),
    ]
    # Entrances to sub-areas that you could just walk back out of
    sub_area_coupled_entrances = [
        SMOEntranceData.top_hat_tower,
        SMOEntranceData.push_blocks,
        SMOEntranceData.poison_tides,
        SMOEntranceData.frog_pond,
        SMOEntranceData.rolling_lane,
        SMOEntranceData.chasm_lifts,
        SMOEntranceData.t_rex_nest,
        SMOEntranceData.chain_chomp_cave,
        SMOEntranceData.gusty_bridges,
        SMOEntranceData.mysterious_clouds,
        SMOEntranceData.ice_cave,
        SMOEntranceData.bullet_bill_maze,
        SMOEntranceData.jaxi_ruins,
        SMOEntranceData.inverted_pyramid_lower_interior,
        # SMOEntranceData.inverted_pyramid_mural,
        SMOEntranceData.moe_eye_invisible_maze,
        SMOEntranceData.sand_kingdom_shop,
        SMOEntranceData.sand_sphynx_vault,
        SMOEntranceData.underground_ruins,
        SMOEntranceData.inverted_pyramid_upper_interior,
        SMOEntranceData.deepest_underground,
        SMOEntranceData.sand_rumbling_floor_house,
        SMOEntranceData.strange_neighborhood,
        SMOEntranceData.colossal_ruins,
        SMOEntranceData.freezing_waterway,
        SMOEntranceData.moe_eye_invisible_floor,
        SMOEntranceData.sky_garden_tower,
        SMOEntranceData.deep_woods_1,
        SMOEntranceData.deep_woods_2,
        SMOEntranceData.deep_woods_3,
        SMOEntranceData.deep_woods_4,
        SMOEntranceData.flooding_pipeway,
        SMOEntranceData.sherm_elevator,
        SMOEntranceData.wooded_flower_road,
        SMOEntranceData.secret_flower_field,
        SMOEntranceData.walking_on_clouds,
        SMOEntranceData.fog_wandering,
        SMOEntranceData.sheep_herding,
        SMOEntranceData.invisible_road,
        SMOEntranceData.breakdown_road,
        SMOEntranceData.poison_swamp,
        SMOEntranceData.cloud_picture_match,
        SMOEntranceData.king_of_the_cube,
        SMOEntranceData.lost_kingdom_shop,
        SMOEntranceData.klepto_lava_bath,
        SMOEntranceData.tropical_wiggler_swamp,
        SMOEntranceData.city_hall,
        SMOEntranceData.metro_kingdom_shop,
        SMOEntranceData.metro_kingdom_shop_regional,
        SMOEntranceData.private_room,
        SMOEntranceData.bullet_building,
        SMOEntranceData.rc_race,
        SMOEntranceData.builder_outfit,
        SMOEntranceData.metro_slots,
        SMOEntranceData.rotating_maze,
        SMOEntranceData.t_rex_escape,
        SMOEntranceData.crowded_street,
        SMOEntranceData.metro_siege,
        SMOEntranceData.high_rise,
        SMOEntranceData.sewers,
        SMOEntranceData.projection_room,
        SMOEntranceData.swinging_scaffolding,
        SMOEntranceData.vanishing_road,
        SMOEntranceData.pitch_black_island,
        SMOEntranceData.seaside_rumbling_floor_cave,
        SMOEntranceData.spinning_maze,
        SMOEntranceData.wading_in_the_cloud_sea,
        SMOEntranceData.pokio_bomb_aiming,
        SMOEntranceData.rocket_flower_dash,
        SMOEntranceData.shiveria,
        SMOEntranceData.ty_foo_sliding_puzzle,
        SMOEntranceData.ice_trace_walking,
        SMOEntranceData.above_the_clouds,
        SMOEntranceData.freezing_water,
        SMOEntranceData.snow_flower_road,
        SMOEntranceData.iceburn_circuit_class_a_lobby,
        SMOEntranceData.fork_flickin,
        SMOEntranceData.magma_swamp,
        SMOEntranceData.cheese_excavate,
        SMOEntranceData.spinning_athletics,
        SMOEntranceData.magma_narrow_path,
        SMOEntranceData.volcano_cave,
        SMOEntranceData.rotating_gears_with_bitefrost,
        SMOEntranceData.lava_islands,
        SMOEntranceData.roulette_tower,
        SMOEntranceData.chargin_chuck_arena,
        SMOEntranceData.bowsers_kingdom_shop,
        SMOEntranceData.inside_the_church,
        SMOEntranceData.moon_cave,
        SMOEntranceData.moon_sphynx_vault,
        SMOEntranceData.moon_kingdom_shop,
        SMOEntranceData.giant_swings,
        SMOEntranceData.dot_galaxy,
        SMOEntranceData.peachs_castle,
        SMOEntranceData.mushroom_kingdom_shop,
        SMOEntranceData.painting_room_cookatiel,
        SMOEntranceData.painting_room_mecha_wiggler,
        SMOEntranceData.painting_room_knucklotec,
        SMOEntranceData.painting_room_torkdrift,
        SMOEntranceData.mushroom_well,
        SMOEntranceData.yoshi_in_the_sea_of_clouds,
        SMOEntranceData.painting_room_mollusque_lanceur,
        SMOEntranceData.painting_room_lord_of_lightning,
        SMOEntranceData.mushroom_picture_match,
        SMOEntranceData.dark_side_topper,
        SMOEntranceData.dark_side_hariet,
        SMOEntranceData.dark_side_spewart,
        SMOEntranceData.dark_side_rango,
        SMOEntranceData.dark_side_vanishing_road,
        SMOEntranceData.dark_side_invisible_road,
        SMOEntranceData.dark_side_siege,
        SMOEntranceData.dark_side_sinking_island,
        SMOEntranceData.dark_side_magma_swamp,
        SMOEntranceData.darker_side_main,
        SMOEntranceData.darker_side_pokio,
        SMOEntranceData.darker_side_bowser,
        SMOEntranceData.darker_side_end,
        SMOEntranceData.darker_side_tower,
        SMOEntranceData.luncheon_treasure_vault,
        SMOEntranceData.snowline_circuit_lobby,
        SMOEntranceData.sandy_bottom,
        SMOEntranceData.sand_slots,
        SMOEntranceData.sand_costume_bonus_dancing_room,
        SMOEntranceData.sand_kingdom_employee,
        SMOEntranceData.arch_repair,
        SMOEntranceData.zipper_chasm,
        SMOEntranceData.bouncy_flowers,
        SMOEntranceData.seaside_costume_bonus_dancing_room,
        SMOEntranceData.sinking_island,
        SMOEntranceData.deep_woods_costume_bonus_treasure_chest,
        SMOEntranceData.deep_woods_treasure_trap,
        SMOEntranceData.spinning_platforms_treasure_vault,
        SMOEntranceData.underwater_tunnel,
        SMOEntranceData.seaside_sphynx_treasure_vault,
        SMOEntranceData.narrow_valley,
        SMOEntranceData.luncheon_costume_bonus_cooking_pots,
        SMOEntranceData.luncheon_slots,
        SMOEntranceData.folding_screen,
        SMOEntranceData.dashing_above_the_clouds,
        SMOEntranceData.bowsers_treasure_vault,
        SMOEntranceData.jizos_adventure,
        SMOEntranceData.spinning_tower,
        SMOEntranceData.hexagon_tower,
        SMOEntranceData.wooden_tower,
        SMOEntranceData.castle_courtyard,
        SMOEntranceData.knucklotec_rematch,
        SMOEntranceData.torkdrift_rematch,
        SMOEntranceData.mecha_wiggler_rematch,
        SMOEntranceData.mollusque_lanceur_rematch,
        SMOEntranceData.cookatiel_rematch,
        SMOEntranceData.lord_of_lightning_rematch,
        SMOEntranceData.freezing_room,
        SMOEntranceData.dark_side_breakdown_road,
        SMOEntranceData.deepest_underground_shortcut,
        SMOEntranceData.lake_kingdom_shop,
        SMOEntranceData.snow_kingdom_shop,
        SMOEntranceData.luncheon_kingdom_shop,
        ]
        # If the sub area is NOT just a dead end, and has an exit on the opposite side of the sub-area
    sub_area_unique_exits = [
        SMOEntranceData.top_hat_tower,
        SMOEntranceData.push_blocks,
        SMOEntranceData.poison_tides,
        SMOEntranceData.rolling_lane,
        SMOEntranceData.chasm_lifts,
        SMOEntranceData.chain_chomp_cave,
        SMOEntranceData.gusty_bridges,
        SMOEntranceData.mysterious_clouds,
        SMOEntranceData.ice_cave,
        SMOEntranceData.bullet_bill_maze,
        SMOEntranceData.jaxi_ruins,
        SMOEntranceData.inverted_pyramid_lower_interior,
        # SMOEntranceData.inverted_pyramid_mural,
        SMOEntranceData.moe_eye_invisible_maze,
        # SMOEntranceData.underground_ruins,
        SMOEntranceData.inverted_pyramid_upper_interior,
        SMOEntranceData.strange_neighborhood,
        SMOEntranceData.freezing_waterway,
        SMOEntranceData.moe_eye_invisible_floor,
        SMOEntranceData.sky_garden_tower,
        # SMOEntranceData.deep_woods_1,
        # SMOEntranceData.deep_woods_3,
        SMOEntranceData.flooding_pipeway,
        SMOEntranceData.sherm_elevator,
        SMOEntranceData.wooded_flower_road,
        SMOEntranceData.secret_flower_field,
        SMOEntranceData.invisible_road,
        SMOEntranceData.poison_swamp,
        SMOEntranceData.tropical_wiggler_swamp,
        SMOEntranceData.city_hall,
        # SMOEntranceData.metro_kingdom_shop,
        SMOEntranceData.bullet_building,
        SMOEntranceData.builder_outfit,
        SMOEntranceData.t_rex_escape,
        SMOEntranceData.crowded_street,
        SMOEntranceData.metro_siege,
        SMOEntranceData.high_rise,
        SMOEntranceData.swinging_scaffolding,
        SMOEntranceData.vanishing_road,
       # SMOEntranceData.spinning_maze # ?,
        SMOEntranceData.wading_in_the_cloud_sea,
        SMOEntranceData.pokio_bomb_aiming,
        SMOEntranceData.rocket_flower_dash,
        SMOEntranceData.freezing_water,
        SMOEntranceData.snow_flower_road,
        SMOEntranceData.fork_flickin,
        SMOEntranceData.magma_swamp,
        SMOEntranceData.spinning_athletics,
        SMOEntranceData.magma_narrow_path,
        SMOEntranceData.volcano_cave,
        SMOEntranceData.rotating_gears_with_bitefrost,
        SMOEntranceData.lava_islands,
        SMOEntranceData.roulette_tower,
        SMOEntranceData.chargin_chuck_arena,
        SMOEntranceData.moon_cave,
        SMOEntranceData.giant_swings,
        SMOEntranceData.dot_galaxy,
        SMOEntranceData.painting_room_cookatiel,
        SMOEntranceData.painting_room_mecha_wiggler,
        SMOEntranceData.painting_room_knucklotec,
        SMOEntranceData.painting_room_torkdrift,
        SMOEntranceData.painting_room_mollusque_lanceur,
        SMOEntranceData.painting_room_lord_of_lightning,
        SMOEntranceData.dark_side_topper,
        SMOEntranceData.dark_side_hariet,
        SMOEntranceData.dark_side_spewart,
        SMOEntranceData.dark_side_rango,
        SMOEntranceData.dark_side_vanishing_road,
        SMOEntranceData.dark_side_invisible_road,
        SMOEntranceData.dark_side_siege,
        SMOEntranceData.dark_side_sinking_island,
        SMOEntranceData.dark_side_magma_swamp,
        SMOEntranceData.darker_side_main,
        SMOEntranceData.bouncy_flowers,
        SMOEntranceData.sinking_island,
        SMOEntranceData.underwater_tunnel,
        SMOEntranceData.narrow_valley,
        SMOEntranceData.luncheon_costume_bonus_cooking_pots,
        SMOEntranceData.jizos_adventure,
        SMOEntranceData.spinning_tower,
        SMOEntranceData.wooden_tower,
        # SMOEntranceData.spinning_platforms_treasure_vault, # ? oneway?,
        # SMOEntranceData.shiveria,
        # SMOEntranceData.deepest_underground_shortcut,
        SMOEntranceData.darker_side_pokio,
        SMOEntranceData.darker_side_bowser,
        # SMOEntranceData.darker_side_end,
    ]

    return world_sub_area_exits, sub_area_coupled_entrances, sub_area_unique_exits
