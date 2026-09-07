from types import NoneType
from typing import Optional, Any
from BaseClasses import Region, Entrance, EntranceType, CollectionState
from rule_builder.options import OptionFilter
from rule_builder.rules import And, CanReachLocation, CanReachRegion, Has, HasAny, HasFromList, HasGroup, Or, True_
from worlds.SuperMarioOdysseyArchipelago.World.smo import SMOWorld
from worlds.SuperMarioOdysseyArchipelago.World.smo.Options import CaptureSanity
from .Data.RuleData import CanCapture, SMOKingdoms, cappy
from .Data.EntranceData import SMOEntranceData
from .Data.ItemData import SMOItemData
from .Entrances import create_entrances, SMORandomizationGroup, SMOEntrance
from .Locations import *
from .Data.RegionData import SMORegion
from .Data.LocationData import SMOLocationData
from .Logic import count_moons, total_moons
from entrance_rando import randomize_entrances, disconnect_entrance_for_randomization




def create_region(self, region_data : tuple):
    """ Creates the regions for Super Mario Odyssey.
            Args:
                self: SMOWorld object for this player's world.
                region_data: Tuple containing region information.
    """
    region = Region(region_data[0], self.player, self.multiworld)
    self.multiworld.regions.append(region)
    if len(region_data) > 2:
        if self.options.goal >= region_data[2] or self.options.entrance_randomization > self.options.entrance_randomization.option_off:
            create_locations(region, *region_data[1])
    else:
        if len(region_data) > 1:
            create_locations(region, *region_data[1])
        else:
            print(region.name)

def connect_region(self, connection_data : tuple):
    """ Connects Super Mario Odyssey Regions
    :param self: SMOWorld object for this player's world.
    :param connection_data: Tuple containing connection information.
    :return:
    """
    cur_region : Region = self.multiworld.get_region(connection_data[0], self.player)
    if isinstance(connection_data[1], dict):
        for connection in connection_data[1].keys():
            if connection in self.multiworld.regions.region_cache[self.player]:
                connecting_region : Region = self.multiworld.get_region(connection, self.player)
                if callable(connection_data[1][connection]):
                    cur_region.connect(connecting_region, f"{cur_region.name} -> {connecting_region.name}", connection_data[1][connection])
                else:
                    cur_region.connect(connecting_region, f"{cur_region.name} -> {connecting_region.name}")


def create_two_way_entrance_rando(cur_region: Region, enter_name: str, exit_name: str, is_sub_area: bool = False,
                                  has_alternate_entrance: bool = False, is_reverse: bool = False) -> tuple[SMOEntrance, SMOEntrance]:
    """
            :param cur_region: current Region.
            :param enter_name: Name of Entrance pair.
            :param exit_name: Name of Entrance pair.
            :param is_sub_area: Is this entrance in a sub area.
            :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
            :return: Tuple containing the Entrance pair.
    """

    region_entry = SMOEntrance(player=cur_region.player, name=enter_name, randomization_type=EntranceType.TWO_WAY,
                                   is_sub_area=is_sub_area, has_alternate_entrance=has_alternate_entrance, is_reverse=is_reverse)

    region_exit = SMOEntrance(player=cur_region.player, name=exit_name, parent=cur_region, randomization_type=EntranceType.TWO_WAY,
                              is_sub_area=is_sub_area, has_alternate_entrance=has_alternate_entrance, is_reverse=is_reverse)

    cur_region.exits.append(region_exit)
    cur_region.entrances.append(region_entry)

    region_entry.connected_region = cur_region

    return region_entry, region_exit

def create_two_way_entrance_rando_pair(cur_region: Region, enter_name: str, exit_name: str, cur_origin_region: Optional[Region] = None,
                                       is_sub_area: bool = False, has_alternate_entrance: bool = False) -> tuple[SMOEntrance, SMOEntrance]:
    """
            :param cur_region: current Region.
            :param enter_name: Name of Entrance pair.
            :param exit_name: Name of Entrance pair.
            :param cur_origin_region: The region the current region descends from.
            :param is_sub_area: Is this entrance in a sub area.
            :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
            :return: Tuple containing the Entrance pair.
    """
    if cur_origin_region:
        region_entry = cur_origin_region.create_er_target(enter_name)
    else:
        region_entry = SMOEntrance(player=cur_region.player, name=enter_name, randomization_type=EntranceType.TWO_WAY,
                                   is_sub_area=is_sub_area, has_alternate_entrance=has_alternate_entrance)

    region_exit = SMOEntrance(player=cur_region.player, name=exit_name, parent=cur_region, randomization_type=EntranceType.TWO_WAY,
                              is_sub_area=is_sub_area, has_alternate_entrance=has_alternate_entrance)

    cur_region.exits.append(region_exit)
    cur_region.entrances.append(region_entry)

    region_entry.connected_region = cur_region

    return region_entry, region_exit

def create_two_way_entrance(cur_region: Region, connecting_region: Region, enter_name: str, exit_name: str,
                                 is_sub_area: bool = False, has_alternate_entrance: bool = False) -> tuple[Entrance, Entrance]:
    """ Creates a pair of Entrances: one exiting ``cur_region``, one entering ``cur_region``
                :param cur_region: current Region.
                :param enter_name: Name of Entrance pair.
                :param exit_name: Name of Entrance pair.
                :param connecting_region: Region this entrance/exit pair connects to.
                :param is_sub_area: Is this entrance in a sub area.
                :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
                :return: Tuple containing the Entrance pair.
    """
    alternate_entrances = {
        SMOEntranceData.top_hat_tower_enter: SMORegion.top_hat_tower,
        SMOEntranceData.top_hat_tower_end: SMORegion.top_hat_tower,
        SMOEntranceData.deepest_underground_shortcut: SMORegion.deepest_underground,
    }
    region_entry, region_exit = create_two_way_entrance_rando(cur_region, enter_name, exit_name, is_sub_area, has_alternate_entrance)

    region_entry.parent_region = connecting_region
    region_exit.connected_region = connecting_region

    region_entry.parent_region.exits.append(region_entry)
    region_entry.parent_region.entrances.append(region_exit)

    return region_entry, region_exit

def create_two_way_entrance_pair(cur_region: Region, connecting_region: Region, enter_name: str, exit_name: str,
                                 is_sub_area: bool = False, has_alternate_entrance: bool = False) -> tuple[Entrance, Entrance, Entrance, Entrance]:
    """ Creates a pair of Entrances: one exiting ``cur_region``, one entering ``cur_region``
                :param cur_region: current Region.
                :param enter_name: Name of Entrance pair.
                :param exit_name: Name of Entrance pair.
                :param connecting_region: Region this entrance/exit pair connects to.
                :param is_sub_area: Is this entrance in a sub area.
                :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
                :return: Tuple containing the Entrance pair.
    """
    alternate_entrances = {
        SMOEntranceData.top_hat_tower_enter: SMORegion.top_hat_tower,
        SMOEntranceData.top_hat_tower_end: SMORegion.top_hat_tower,
        SMOEntranceData.deepest_underground_shortcut: SMORegion.deepest_underground,
    }
    region_entry, region_exit = create_two_way_entrance_rando(cur_region, exit_name, exit_name, is_sub_area, has_alternate_entrance)

    other_entry, other_exit = create_two_way_entrance_rando(connecting_region, enter_name,
                                                            enter_name, is_sub_area, has_alternate_entrance, True)

    region_entry.parent_region = connecting_region
    region_exit.connected_region = connecting_region

    other_entry.parent_region = cur_region
    other_exit.connected_region = cur_region

    return region_entry, region_exit, other_entry, other_exit

def create_one_way_entrance_for_entrance_rando(cur_region: Region, name: str,
                                               is_sub_area: bool = False, has_alternate_entrance: bool = False) ->  Entrance:
    """
            :param cur_region: current Region.
            :param name: Name of Entrance pair.
            :param is_sub_area: Is this entrance in a sub area.
            :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
            :return: One-way Entrance.
    """
    region_entry = SMOEntrance(player=cur_region.player, name=name, parent=cur_region, is_sub_area=is_sub_area,
                              has_alternate_entrance=has_alternate_entrance)

    region_entry.connect(cur_region)

    return region_entry

def create_one_way_exit_for_entrance_rando(cur_region: Region, name: str,
                                           is_sub_area: bool = False, has_alternate_entrance: bool = False) ->  Entrance:
    """
            :param cur_region: current Region.
            :param name: Name of Entrance pair.
            :param is_sub_area: Is this entrance in a sub area.
            :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
            :return: One-way Entrance.
    """
    region_exit = SMOEntrance(player=cur_region.player, name=name, parent=cur_region, is_sub_area=is_sub_area,
                              has_alternate_entrance=has_alternate_entrance)
    cur_region.exits.append(region_exit)

    return region_exit

def create_one_way_entrance(cur_region: Region, name: str, connecting_region: Region,
                            is_sub_area: bool = False, has_alternate_entrance: bool = False) -> Entrance:
    """
                :param cur_region: current Region you are entering.
                :param name: Name of Entrance pair.
                :param connecting_region: Region this entrance/exit pair connects to.
                :param is_sub_area: Is this entrance in a sub area.
                :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
                :return: One-way Entrance.
    """
    alternate_entrances = {
        SMOEntranceData.top_hat_tower_enter: SMORegion.top_hat_tower,
        SMOEntranceData.top_hat_tower_end: SMORegion.top_hat_tower,
        SMOEntranceData.deepest_underground_shortcut: SMORegion.deepest_underground,
    }
    region_entrance = create_one_way_entrance_for_entrance_rando(cur_region, name, is_sub_area, has_alternate_entrance)

    region_entrance.parent_region = connecting_region

    return region_entrance

def create_one_way_exit(cur_region: Region, name: str, connecting_region: Region,
                        is_sub_area: bool = False, has_alternate_entrance: bool = False) -> Entrance:
    """
                :param cur_region: current Region being exited from.
                :param name: Name of Entrance pair.
                :param connecting_region: Region this entrance/exit pair connects to.
                :param is_sub_area: Is this entrance in a sub area.
                :param has_alternate_entrance: Does this over world entrance have another loading zone that leads to the same place normally.
                :return: One-way Entrance.
    """
    alternate_entrances = {
        SMOEntranceData.top_hat_tower_enter: SMORegion.top_hat_tower,
        SMOEntranceData.top_hat_tower_end: SMORegion.top_hat_tower,
        SMOEntranceData.deepest_underground_shortcut: SMORegion.deepest_underground,
    }
    region_exit = create_one_way_exit_for_entrance_rando(cur_region, name, is_sub_area, has_alternate_entrance)

    region_exit.connected_region = connecting_region

    return region_exit

def add_to_er(self, region_entry: Entrance, region_exit: Entrance, sub_area_entry: Entrance,
                                    sub_area_exit: Entrance, is_add: list[bool]) -> None:

    if region_entry and is_add[0]:
        self.sub_area_entrances.append(region_entry)
    # else:
    #     region_entry.connected_region.entrances.remove(region_entry)
    #     for other_target in region_entry.parent_region.exits:
    #         if region_entry.name == other_target.name:
    #             region_entry.parent_region.exits.remove(other_target)

    if region_exit and is_add[1]:
        self.sub_area_exits.append(region_exit)
    # else:
    #     region_exit.parent_region.exits.remove(region_exit)
    #     for other_target in region_exit.connected_region.exits:
    #         if region_exit.name == other_target.name:
    #             region_exit.parent_region.exits.remove(other_target)

    if sub_area_entry and is_add[2]:
        self.sub_area_entrances.append(sub_area_entry)
    # else:
        # sub_area_entry.connected_region.entrances.remove(sub_area_entry)
        # for other_target in sub_area_entry.parent_region.exits:
        #     if sub_area_entry.name == other_target.name:
        #         sub_area_entry.parent_region.exits.remove(other_target)

    if sub_area_exit and is_add[3]:
        self.sub_area_exits.append(sub_area_exit)
    # else:
        # sub_area_exit.parent_region.exits.remove(sub_area_exit)
        # for other_target in sub_area_exit.connected_region.exits:
        #     if sub_area_exit.name == other_target.name:
        #         sub_area_exit.parent_region.exits.remove(other_target)

def create_regions(self: SMOWorld):
    """ Creates the regions for Super Mario Odyssey.
            Args:
                self: SMOWorld object for this player's world.
    """

    def connect_coin_shops(region_connections : dict):
        region_connections[SMORegion.shop_cap_coin] = None
        # region_connections[SMORegion.shop_cascade_coin] = lambda state: state.can_reach(
        #     self.multiworld.get_region(SMORegion.restored_odyssey, self.player))
        # region_connections[SMORegion.shop_sand_coin] = lambda state: state.can_reach(
        #     self.multiworld.get_region(SMORegion.restored_odyssey, self.player))
        region_connections[SMORegion.shop_lake_coin] = CanReachRegion(SMORegion.odyssey_broken_down)
        region_connections[SMORegion.shop_wooded_coin] = CanReachRegion(SMORegion.odyssey_broken_down)
        region_connections[SMORegion.shop_metro_coin] = CanReachRegion(SMORegion.odyssey_repaired_lost)
        region_connections[SMORegion.shop_seaside_coin] = CanReachRegion(SMORegion.odyssey_sails_branch_2)
        region_connections[SMORegion.shop_luncheon_coin] = CanReachRegion(SMORegion.odyssey_sails_branch_2)
        region_connections[SMORegion.shop_moon_coin] = CanReachRegion(SMORegion.odyssey_complete)
        region_connections[SMORegion.shop_mushroom_coin] = can_reach_mushroom
        region_connections[SMORegion.post_game_coin_outfits] = can_reach_mushroom

    #region Regions

    odyssey_regions = [
        (SMORegion.defunct_odyssey, {}, self.options.goal.option_sand),
        (SMORegion.restored_odyssey, {}, self.options.goal.option_sand),
        (SMORegion.odyssey_interior, {}, self.options.goal.option_sand),
        (SMORegion.odyssey_sail_sand, {}, self.options.goal.option_lake),
        (SMORegion.odyssey_sails_branch_1, {}, self.options.goal.option_metro),
        (SMORegion.odyssey_broken_down, {}, self.options.goal.option_metro),
        (SMORegion.odyssey_repaired_lost, {}, self.options.goal.option_metro),
        (SMORegion.odyssey_sail_metro, {}, self.options.goal.option_luncheon),
        (SMORegion.odyssey_sails_branch_2, {}, self.options.goal.option_luncheon),
        (SMORegion.odyssey_sail_luncheon, {}, self.options.goal.option_moon),
        (SMORegion.odyssey_repaired_ruined, {}, self.options.goal.option_moon),
        (SMORegion.odyssey_complete, {}, self.options.goal.option_moon),
        (SMORegion.odyssey_powered_up_dark, {}, self.options.goal.option_dark),
        (SMORegion.odyssey_powered_up_darker, {}, self.options.goal.option_darker),
        #("Odyssey Turns Gold", self.options.goal.option_sand), # For AUM / All achievements goal possibly


    ]

    world_regions = [
        (SMORegion.menu, {}, self.options.goal.option_sand),
        (SMORegion.cap_kingdom_intro, {}, self.options.goal.option_sand),
        (SMORegion.cap_kingdom_topper, loc_Topper, self.options.goal.option_sand),
        (SMORegion.cap_kingdom, loc_Cap, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom, loc_Cascade, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_upper, loc_Cascade_Upper, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_peace, loc_Cascade_Peace, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_revisit, loc_Cascade_Revisit, self.options.goal.option_sand),
        (SMORegion.sand_kingdom, loc_Sand, self.options.goal.option_sand),
        (SMORegion.night_sand_kingdom, loc_Night_Sand, self.options.goal.option_sand),
        (SMORegion.top_of_the_inverted_pyramid, loc_Sand_Pyramid, self.options.goal.option_sand),
        (SMORegion.sand_kingdom_peace, loc_Sand_Peace, self.options.goal.option_sand),
        (SMORegion.top_of_the_inverted_pyramid_peace, loc_Sand_Pyramid_Peace, self.options.goal.option_sand),
        (SMORegion.wooded_kingdom, loc_Wooded, self.options.goal.option_lake),
        (SMORegion.wooded_kingdom_post_broodals, loc_Wooded_Post_Story1, self.options.goal.option_lake),
        (SMORegion.wooded_kingdom_peace, loc_Wooded_Peace, self.options.goal.option_lake),
        (SMORegion.lake_kingdom, loc_Lake, self.options.goal.option_lake),
        (SMORegion.cloud_kingdom_boss_fight, loc_Post_Cloud, self.options.goal.option_metro),
        (SMORegion.cloud_kingdom_revisit, loc_Cloud, self.options.goal.option_metro),
        (SMORegion.lost_kingdom, loc_Lost, self.options.goal.option_metro),
        (SMORegion.lost_kingdom_revisit, loc_Lost_Revisit, self.options.goal.option_metro),
        (SMORegion.night_metro_kingdom, loc_Night_Metro, self.options.goal.option_metro),
        (SMORegion.day_metro_kingdom, loc_Metro, self.options.goal.option_metro),
        (SMORegion.metro_kingdom_peace, loc_Metro_Peace, self.options.goal.option_metro),
        (SMORegion.seaside_kingdom, loc_Seaside, self.options.goal.option_luncheon),
        (SMORegion.seaside_kingdom_peace, loc_Seaside_Peace, self.options.goal.option_luncheon),
        (SMORegion.snow_kingdom, loc_Snow, self.options.goal.option_luncheon),
        (SMORegion.snow_kingdom_peace, loc_Snow_Peace, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom, loc_Luncheon, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_post_broodals, loc_Luncheon_Post_Spewart, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_meat, loc_Luncheon_Post_Cheese_Rocks, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_peace, loc_Luncheon_Peace, self.options.goal.option_luncheon),
        (SMORegion.ruined_kingdom, loc_Ruined, self.options.goal.option_moon),
        (SMORegion.bowsers_kingdom, loc_Bowser, self.options.goal.option_moon),
        (SMORegion.infiltrate_bowsers_castle, loc_Bowser_Infiltrate, self.options.goal.option_moon),
        (SMORegion.bowser_kingdom_smart_bombing, loc_Bowser_Post_Bombing, self.options.goal.option_moon),
        (SMORegion.bowser_kingdom_mecha_broodal, loc_Bowser_Mecha_Broodal, self.options.goal.option_moon),
        (SMORegion.bowser_kingdom_peace, loc_Bowser_Peace, self.options.goal.option_moon),
        (SMORegion.moon_kingdom, loc_Moon_Post_Moon, self.options.goal.option_moon),
        (SMORegion.moon_kingdom_peace, loc_Moon, self.options.goal.option_moon),
        (SMORegion.mushroom_kingdom, loc_Mushroom, self.options.goal.option_dark),
        (SMORegion.dark_side, {}, self.options.goal.option_dark),
        (SMORegion.dark_side_2, {}, self.options.goal.option_dark),
        (SMORegion.dark_side_3, {}, self.options.goal.option_dark),
        (SMORegion.dark_side_4, {}, self.options.goal.option_dark),
        (SMORegion.dark_side_5, {}, self.options.goal.option_dark),
        (SMORegion.dark_side_peace, loc_Dark, self.options.goal.option_dark),
        (SMORegion.darker_side, {}, self.options.goal.option_darker),
        (SMORegion.darker_side_tower, loc_Darker, self.options.goal.option_darker),
        (SMORegion.cap_kingdom_moon_rock, loc_Cap_Postgame, self.options.goal.option_dark),
        (SMORegion.cascade_kingdom_moon_rock, loc_Cascade_Postgame, self.options.goal.option_dark),
        (SMORegion.sand_kingdom_moon_rock, loc_Sand_Postgame, self.options.goal.option_dark),
        (SMORegion.wooded_kingdom_moon_rock, loc_Wooded_Postgame, self.options.goal.option_dark),
        (SMORegion.lake_kingdom_moon_rock, loc_Lake_Postgame, self.options.goal.option_dark),
        (SMORegion.cloud_kingdom_moon_rock, loc_Cloud_Postgame, self.options.goal.option_dark),
        (SMORegion.lost_kingdom_moon_rock, loc_Lost_Postgame, self.options.goal.option_dark),
        (SMORegion.metro_kingdom_moon_rock, loc_Metro_Postgame, self.options.goal.option_dark),
        (SMORegion.seaside_kingdom_moon_rock, loc_Seaside_Postgame, self.options.goal.option_dark),
        (SMORegion.snow_kingdom_moon_rock, loc_Snow_Postgame, self.options.goal.option_dark),
        (SMORegion.luncheon_kingdom_moon_rock, loc_Luncheon_Postgame, self.options.goal.option_dark),
        (SMORegion.ruined_kingdom_moon_rock, loc_Ruined_Postgame, self.options.goal.option_dark),
        (SMORegion.bowser_kingdom_moon_rock, loc_Bowser_Postgame, self.options.goal.option_dark),
        (SMORegion.moon_kingdom_moon_rock, loc_Moon_Postgame, self.options.goal.option_dark),

    ]

    capture_regions = [
        (SMORegion.frog, {SMOItemData.frog: 3701}),
        (SMORegion.spark_pylon, {SMOItemData.spark_pylon: 3702}),
        (SMORegion.paragoomba, {SMOItemData.paragoomba: 3703}),
        (SMORegion.chain_chomp, {SMOItemData.chain_chomp: 3704}),
        (SMORegion.big_chain_chomp, {SMOItemData.big_chain_chomp: 3705}),
        (SMORegion.broodes_chain_chomp, {SMOItemData.broodes_chain_chomp: 3706}),
        (SMORegion.t_rex, {SMOItemData.t_rex: 3707}),
        (SMORegion.binoculars, {SMOItemData.binoculars: 3708}),
        (SMORegion.bullet_bill, {SMOItemData.bullet_bill: 3709}),
        (SMORegion.moe_eye, {SMOItemData.moe_eye: 3710}),
        (SMORegion.cactus, {SMOItemData.cactus: 3711}),
        (SMORegion.goomba, {SMOItemData.goomba: 3712}),
        (SMORegion.knucklotecs_fist, {SMOItemData.knucklotecs_fist: 3713}),
        (SMORegion.mini_rocket, {SMOItemData.mini_rocket: 3714}),
        (SMORegion.glydon, {SMOItemData.glydon: 3715}),
        (SMORegion.lakitu, {SMOItemData.lakitu: 3716}),
        (SMORegion.zipper, {SMOItemData.zipper: 3717}),
        (SMORegion.cheep_cheep, {SMOItemData.cheep_cheep: 3718}),
        (SMORegion.puzzle_part_lake_kingdom, {SMOItemData.puzzle_part_lake_kingdom: 3719}),
        (SMORegion.poison_piranha_plant, {SMOItemData.poison_piranha_plant: 3720}),
        (SMORegion.uproot, {SMOItemData.uproot: 3721}),
        (SMORegion.fire_bro, {SMOItemData.fire_bro: 3722}),
        (SMORegion.sherm, {SMOItemData.sherm: 3723}),
        (SMORegion.coin_coffer, {SMOItemData.coin_coffer: 3724}),
        (SMORegion.tree, {SMOItemData.tree: 3725}),
        (SMORegion.boulder, {SMOItemData.boulder: 3726}),
        (SMORegion.picture_match_part_goomba, {SMOItemData.picture_match_part_goomba: 3727}),
        (SMORegion.tropical_wiggler, {SMOItemData.tropical_wiggler: 3728}),
        (SMORegion.pole, {SMOItemData.pole: 3729}),
        (SMORegion.manhole, {SMOItemData.manhole: 3730}),
        (SMORegion.taxi, {SMOItemData.taxi: 3731}),
        (SMORegion.rc_car, {SMOItemData.rc_car: 3732}),
        (SMORegion.ty_foo, {SMOItemData.ty_foo: 3733}),
        (SMORegion.shiverian_racer, {SMOItemData.shiverian_racer: 3734}),
        (SMORegion.cheep_cheep_snow_kingdom, {SMOItemData.cheep_cheep_snow_kingdom: 3735}),
        (SMORegion.gushen, {SMOItemData.gushen: 3736}),
        (SMORegion.lava_bubble, {SMOItemData.lava_bubble: 3737}),
        (SMORegion.volbonan, {SMOItemData.volbonan: 3738}),
        (SMORegion.hammer_bro, {SMOItemData.hammer_bro: 3739}),
        (SMORegion.meat, {SMOItemData.meat: 3740}),
        (SMORegion.fire_piranha_plant, {SMOItemData.fire_piranha_plant: 3741}),
        (SMORegion.pokio, {SMOItemData.pokio: 3742}),
        (SMORegion.jizo, {SMOItemData.jizo: 3743}),
        (SMORegion.bowser_statue, {SMOItemData.bowser_statue: 3744}),
        (SMORegion.parabones, {SMOItemData.parabones: 3745}),
        (SMORegion.banzai_bill, {SMOItemData.banzai_bill: 3746}),
        (SMORegion.chargin_chuck, {SMOItemData.chargin_chuck: 3747}),
        (SMORegion.bowser, { SMOItemData.bowser: 3748}),
        (SMORegion.letter, { SMOItemData.letter: 3749}, self.options.goal.option_dark),
        (SMORegion.puzzle_part_metro_kingdom, {SMOItemData.puzzle_part_metro_kingdom: 3750}, self.options.goal.option_dark),
        (SMORegion.picture_match_part_mario, {SMOItemData.picture_match_part_mario: 3751}, self.options.goal.option_dark),
        (SMORegion.yoshi, { SMOItemData.yoshi: 3752}, self.options.goal.option_dark),
    ]

    sub_area_regions = [
        (SMORegion.top_hat_tower, {}),
        (SMORegion.frog_pond, sub_area_frog),
        (SMORegion.poison_tides, sub_area_poison_tide),
        (SMORegion.push_block, sub_area_push_block),
        (SMORegion.rolling_lane, sub_area_rolling),
        (SMORegion.chain_chomp_cave, sub_area_chain_chomp),
        (SMORegion.t_rex_nest, sub_area_trex_nest),
        (SMORegion.chasm_lifts, sub_area_cascade_2d),
        (SMORegion.gusty_bridges, sub_area_gusty_bridges),
        (SMORegion.mysterious_clouds, sub_area_mysterious_clouds),
        (SMORegion.moe_eye_invisible_maze, sub_area_invisible_maze),
        (SMORegion.bullet_bill_maze, sub_area_bullet_bill_maze),
        (SMORegion.jaxi_ruins, sub_area_jaxi),
        (SMORegion.strange_neighborhood, sub_area_strange_neighborhood),
        (SMORegion.sand_outfit, sub_area_sand_outfit),
        (SMORegion.sand_rumbling_floor_house, sub_area_sand_rumbling_floor),
        (SMORegion.employees_only, sub_area_sand_employee),
        (SMORegion.ice_cave, sub_area_jaxi_ruins),
        (SMORegion.sand_sphynx_vault, sub_area_sand_sphinx),
        (SMORegion.sand_slots, sub_area_sand_slots),
        (SMORegion.inverted_pyramid_lower_interior, {}),
        # (SMORegion.inverted_pyramid_mural, loc_Sand_Pyramid_Mural),
        (SMORegion.inverted_pyramid_upper_interior, sub_area_inverted_pyramid),
        (SMORegion.underground_ruins, sub_area_sand_underground),
        (SMORegion.deepest_underground, sub_area_sand_arena),
        (SMORegion.deepest_underground_peace, sub_area_sand_arena_peace),
        (SMORegion.deepest_underground_post_game, sub_area_sand_arena_post),
        (SMORegion.moe_eye_invisible_floor, sub_area_transparent_platform),
        (SMORegion.colossal_ruins, sub_area_colossal_ruins),
        (SMORegion.freezing_waterway, sub_area_freezing_waterway),
        (SMORegion.arch_repair, sub_area_repair),
        (SMORegion.zipper_chasm, sub_area_zipper),
        (SMORegion.bouncy_flowers, sub_area_jump_grab_climb),
        (SMORegion.poison_swamp, sub_area_waves_poison),
        (SMORegion.deep_woods_treasure_trap, sub_area_woods_treasure_trap),
        (SMORegion.explorer_outift, sub_area_explorer),
        (SMORegion.flooding_pipeway, sub_area_flooding_pipe),
        (SMORegion.wooded_flower_road, sub_area_flower_road),
        (SMORegion.sherm_elevator, sub_area_elevator_escalation),
        (SMORegion.fog_wandering, sub_area_wooded_fog),
        (SMORegion.walking_on_clouds, sub_area_wooded_clouds),
        (SMORegion.sky_garden_tower, {}), # Add locations
        (SMORegion.secret_flower_field, sub_area_flower_field),
        (SMORegion.secret_flower_field_peace, sub_area_flower_field_peace),
        (SMORegion.deep_woods, sub_area_deep_woods), # Add Locations
        (SMORegion.nut_room, sub_area_nut_room),
        (SMORegion.invisible_road, sub_area_wooded_invisible_road),
        (SMORegion.sheep_herding, sub_area_sheep),
        (SMORegion.breakdown_road, sub_area_wooded_breakdown_road),
        (SMORegion.cloud_picture_match, sub_area_cloud_picture),
        (SMORegion.cloud_post_game_picture_match, sub_area_cloud_picture_post),
        (SMORegion.king_of_the_cube, sub_area_cube),
        (SMORegion.tropical_wiggler_swamp, sub_area_jungle),
        (SMORegion.klepto_lava_bath, sub_area_klepto),
        (SMORegion.metro_slots, sub_area_metro_slots),
        (SMORegion.rc_race, sub_area_rc),
        (SMORegion.rc_race_post_game, sub_area_rc_post),
        (SMORegion.private_room, sub_area_private_room),
        (SMORegion.city_hall, sub_area_city_hall),
        (SMORegion.crowded_street, sub_area_crowd),
        (SMORegion.builder_outfit, sub_area_rewiring),
        (SMORegion.metro_siege, sub_area_siege),
        (SMORegion.rotating_maze, sub_area_rotating_maze),
        (SMORegion.high_rise, sub_area_high_rise),
        (SMORegion.bullet_billding, sub_area_bullet_billding),
        (SMORegion.t_rex_escape, sub_area_motor_scooter),
        (SMORegion.projection_room, sub_area_big_screen),
        (SMORegion.pitch_black_island, sub_area_pitch_black),
        (SMORegion.swinging_scaffolding, sub_area_swinging_scaffolding),
        (SMORegion.vanishing_road, sub_area_motor_daredevil),
        (SMORegion.crowded_street_post_game, sub_area_crowd_post_game),
        (SMORegion.sewers, sub_area_sewer),
        (SMORegion.sewers_post_game, sub_area_sewer_post_game),
        (SMORegion.sandy_bottom, sub_area_sandy_bottom),
        (SMORegion.seaside_waterway, sub_area_seaside_waterway),
        (SMORegion.seaside_sphynx_vault, sub_area_seaside_sphynx),
        (SMORegion.seaside_rumbling_room, sub_area_seaside_rumble),
        (SMORegion.resort_outfit, sub_area_resort),
        (SMORegion.wading_in_the_cloud_sea, sub_area_cloud_sea),
        (SMORegion.narrow_valley, sub_area_valley),
        (SMORegion.sinking_island, sub_area_seaside_stretch),
        (SMORegion.pokio_bomb_aiming, sub_area_seaside_pokio),
        (SMORegion.spinning_maze, sub_area_seaside_maze),
        (SMORegion.icicle_barrier_post_game, sub_area_icicle_post),
        (SMORegion.ice_wall_barrier_post_game, sub_area_ice_wall_post),
        (SMORegion.gusty_barrier_post_game, sub_area_gusty_barrier_post),
        (SMORegion.snowy_mountain_barrier_post_game, sub_area_snowy_mountain_post),
        (SMORegion.shiveria, sub_area_shiveria),
        (SMORegion.shiveria_peace, sub_area_shiveria_peace),
        (SMORegion.snowline_circuit, sub_area_snowline),
        (SMORegion.iceburn_circuit, sub_area_iceburn),
        (SMORegion.freezing_room, sub_area_snow_outfit),
        (SMORegion.ice_trace_walking, sub_area_snow_koopa),
        (SMORegion.rocket_flower_dash, sub_area_snow_dashing),
        (SMORegion.freezing_water, sub_area_snow_freezing_water),
        (SMORegion.ty_foo_sliding_puzzle, sub_area_blowing),
        (SMORegion.above_the_clouds, sub_area_snow_spinning),
        (SMORegion.snow_flower_road, sub_area_snow_flower_road),
        (SMORegion.magma_swamp, sub_area_magma_swamp),
        (SMORegion.luncheon_treasure_vault, sub_area_veggies),
        (SMORegion.chef_outfit, sub_area_cook),
        (SMORegion.fork_flickin, sub_area_forks),
        (SMORegion.cheese_excavate, sub_area_cheese),
        (SMORegion.magma_narrow_path, sub_area_lava_bubble),
        (SMORegion.spinning_athletics, sub_area_spinning_athletics),
        (SMORegion.cascading_magma, sub_area_luncheon_story),
        (SMORegion.luncheon_slots, sub_area_luncheon_slots),
        (SMORegion.rotating_gears_with_bitefrost, sub_area_gear_steps),
        (SMORegion.volcano_cave, sub_area_volcano_cave),
        (SMORegion.lava_islands, sub_area_lava_islands),
        (SMORegion.roulette_tower, sub_area_roulette_tower),
        (SMORegion.chargin_chuck_arena, sub_area_ruined_charging),
        (SMORegion.folding_screen, sub_area_samurai),
        (SMORegion.bowsers_treasure_vault, sub_area_bowser_vault),
        (SMORegion.jizos_adventure, sub_area_jizo_adventure),
        (SMORegion.spinning_tower, sub_area_spinning_tower),
        (SMORegion.hexagon_tower, sub_area_hexagon_tower),
        (SMORegion.wooden_tower, sub_area_wooden_tower),
        (SMORegion.dashing_above_the_clouds, sub_area_bowser_clouds),
        (SMORegion.moon_cave, sub_area_moon_cave),
        (SMORegion.inside_the_church, sub_area_church),
        (SMORegion.dot_galaxy, sub_area_galaxy, self.options.goal.option_dark),
        (SMORegion.giant_swings, sub_area_swings, self.options.goal.option_dark),
        (SMORegion.moon_sphynx_vault, sub_area_sphynx_moon, self.options.goal.option_dark),
        (SMORegion.mushroom_picture_match, sub_area_mushroom_picture, self.options.goal.option_dark),
        (SMORegion.peachs_castle, sub_area_castle, self.options.goal.option_dark),
        (SMORegion.castle_courtyard, sub_area_64, self.options.goal.option_dark),
        (SMORegion.mushroom_well, sub_area_mushroom_well, self.options.goal.option_dark),
        (SMORegion.yoshi_in_the_sea_of_clouds, sub_area_yoshi_clouds, self.options.goal.option_dark),
        (SMORegion.knucklotec_rematch, sub_area_rematch_tostarena, self.options.goal.option_dark),
        (SMORegion.torkdrift_rematch, sub_area_rematch_steam_gardens, self.options.goal.option_dark),
        (SMORegion.mollosque_lanceur_rematch, sub_area_rematch_bubblaine, self.options.goal.option_dark),
        (SMORegion.mecha_wiggler_rematch, sub_area_rematch_metro, self.options.goal.option_dark),
        (SMORegion.cookatiel_rematch, sub_area_rematch_volbono, self.options.goal.option_dark),
        (SMORegion.lord_of_lightning_rematch, sub_area_rematch_crumbleden, self.options.goal.option_dark),
        (SMORegion.painting_room_knucklotec, {}),
        (SMORegion.painting_room_torkdrift, {}),
        (SMORegion.painting_room_mollusque_lanceur, {}),
        (SMORegion.painting_room_mecha_wiggler, {}),
        (SMORegion.painting_room_cookatiel, {}),
        (SMORegion.painting_room_lord_of_lightning, {}),
        (SMORegion.dark_side_breakdown_road, sub_area_darker_breakdown, self.options.goal.option_darker),
        (SMORegion.dark_side_invisible_road, sub_area_darker_invisible, self.options.goal.option_darker),
        (SMORegion.dark_side_vanishing_road, sub_area_darker_vanishing, self.options.goal.option_darker),
        (SMORegion.dark_side_under_siege, sub_area_darker_yoshi_siege, self.options.goal.option_darker),
        (SMORegion.dark_side_sinking_island, sub_area_darker_yoshi_sinking, self.options.goal.option_darker),
        (SMORegion.dark_side_magma_swamp, sub_area_darker_yoshi_magma, self.options.goal.option_darker),
        (SMORegion.dark_side_topper, {}),
        (SMORegion.dark_side_harriet, {}),
        (SMORegion.dark_side_rango, {}),
        (SMORegion.dark_side_spewart, {}),
        (SMORegion.darker_side_entrance, {}),
        (SMORegion.darker_side_climb, {}),
        (SMORegion.darker_side_bowser, {}),
        (SMORegion.darker_side_end, {}),
        # (SMORegion.sand_kingdom_shop, loc_Sand_Shop), # Add Shop Room Sub Areas
        # (SMORegion.lake_kingdom_shop, loc_Lake_Shop),
        # (SMORegion.lost_kingdom_shop, loc_Lost_Shop),
        # (SMORegion.metro_kingdom_shop, loc_Metro_Shop),
        # (SMORegion.snow_kingdom_shop, loc_Snow_Shop),
        # (SMORegion.luncheon_kingdom_shop, loc_Luncheon_Shop),
        # (SMORegion.bowser_kingdom_shop, loc_Bowser_Shop),
        # (SMORegion.moon_kingdom_shop, loc_Moon_Shop),
        # (SMORegion.mushroom_kingdom_shop, loc_Mushroom_Shop),
    ]

    shop_regions = [
        (SMORegion.odyssey_outfit, loc_odyssey_outfit),
        (SMORegion.cap_kingdom_shop, loc_Cap_Shop),
        (SMORegion.cascade_kingdom_shop, loc_Cascade_Shop),
        (SMORegion.sand_kingdom_shop, loc_Sand_Shop, self.options.goal.option_sand),
        (SMORegion.wooded_kingdom_shop, loc_Wooded_Shop, self.options.goal.option_lake),
        (SMORegion.lake_kingdom_shop, loc_Lake_Shop, self.options.goal.option_lake),
        (SMORegion.lost_kingdom_shop, loc_Lost_Shop, self.options.goal.option_metro),
        (SMORegion.metro_kingdom_shop, loc_Metro_Shop, self.options.goal.option_metro),
        (SMORegion.seaside_kingdom_shop, loc_Seaside_Shop, self.options.goal.option_luncheon),
        (SMORegion.snow_kingdom_shop, loc_Snow_Shop, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_shop, loc_Luncheon_Shop, self.options.goal.option_luncheon),
        (SMORegion.bowser_kingdom_shop, loc_Bowser_Shop, self.options.goal.option_moon),
        (SMORegion.moon_kingdom_tuxedo, loc_Moon_Outfit, self.options.goal.option_moon),
        (SMORegion.moon_kingdom_shop, loc_Moon_Shop, self.options.goal.option_moon),
        (SMORegion.mushroom_kingdom_shop, loc_Mushroom_Shop, self.options.goal.option_dark),
        (SMORegion.post_game_coin_outfits, loc_Postgame_Shop, self.options.goal.option_dark),
        (SMORegion.dark_side_outfit, loc_Dark_Outfit, self.options.goal.option_darker),
        (SMORegion.darker_side_outfit, loc_Darker_Outfit, self.options.goal.option_darker),
        (SMORegion.shop_cap_coin, shop_cap_coin, self.options.goal.option_sand),
        (SMORegion.shop_wooded_coin, shop_wooded_coin, self.options.goal.option_metro),
        (SMORegion.shop_lake_coin, shop_lake_coin, self.options.goal.option_metro),
        (SMORegion.shop_metro_coin, shop_metro_coin, self.options.goal.option_metro),
        (SMORegion.shop_seaside_coin, shop_seaside_coin, self.options.goal.option_luncheon),
        (SMORegion.shop_luncheon_coin, shop_luncheon_coin, self.options.goal.option_luncheon),
        (SMORegion.shop_moon_coin, shop_moon_coin, self.options.goal.option_darker),
        (SMORegion.shop_mushroom_coin, shop_post_game_coin, self.options.goal.option_darker),
    ]

    regional_group_regions = [
        (SMORegion.cap_kingdom_regional_groups, cap_kingdom_regional_groups, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_regional_groups, cascade_kingdom_regional_groups, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_peace_regional_groups, cascade_kingdom_peace_regional_groups, self.options.goal.option_sand),
        (SMORegion.sand_kingdom_regional_groups, sand_kingdom_regional_groups, self.options.goal.option_sand),
        (SMORegion.sand_kingdom_peace_regional_groups, sand_kingdom_peace_regional_groups, self.options.goal.option_metro),
        (SMORegion.sand_kingdom_pyramid_over_world_regional_groups, sand_kingdom_pyramid_over_world_regional_groups,
         self.options.goal.option_sand),
        (SMORegion.wooded_kingdom_regional_groups, wooded_kingdom_regional_groups, self.options.goal.option_metro),
        (SMORegion.lake_kingdom_regional_groups, lake_kingdom_regional_groups, self.options.goal.option_metro),
        (SMORegion.lost_kingdom_regional_groups, lost_kingdom_regional_groups, self.options.goal.option_metro),
        (SMORegion.metro_kingdom_regional_groups, metro_kingdom_regional_groups, self.options.goal.option_metro),
        (SMORegion.night_metro_kingdom_regional_groups, night_metro_kingdom_regional_groups, self.options.goal.option_metro),
        (SMORegion.seaside_kingdom_regional_groups, seaside_kingdom_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.snow_kingdom_regional_groups, snow_kingdom_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_regional_groups, luncheon_kingdom_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_post_meat_regional_groups, luncheon_kingdom_post_meat_regional_groups,
         self.options.goal.option_luncheon),
        (SMORegion.bowsers_kingdom_regional_groups, bowsers_kingdom_regional_groups, self.options.goal.option_moon),
        (SMORegion.bowsers_kingdom_peace_regional_groups, bowsers_kingdom_peace_regional_groups, self.options.goal.option_moon),
        (SMORegion.moon_kingdom_regional_groups, moon_kingdom_regional_groups, self.options.goal.option_moon),
        (SMORegion.mushroom_kingdom_regional_groups, mushroom_kingdom_regional_groups, self.options.goal.option_dark),
        (SMORegion.top_hat_tower_regional_groups, top_hat_tower_regional_groups, self.options.goal.option_sand),
        (SMORegion.frog_pond_regional_groups, frog_pond_regional_groups, self.options.goal.option_sand),
        (SMORegion.push_blocks_regional_groups, pushblocks_regional_groups, self.options.goal.option_sand),
        (SMORegion.poison_tides_regional_groups, poison_tides_regional_groups, self.options.goal.option_sand),
        (SMORegion.chasm_lifts_regional_groups, chasm_lifts_regional_groups, self.options.goal.option_sand),
        (SMORegion.bullet_bill_maze_regional_groups, bullet_bill_maze_regional_groups, self.options.goal.option_sand),
        (SMORegion.jaxi_ruins_regional_groups, jaxi_ruins_regional_groups, self.options.goal.option_sand),
        (SMORegion.strange_neighborhood_regional_groups, strange_neighborhood_regional_groups, self.options.goal.option_sand),
        (SMORegion.moe_eye_invisible_maze_regional_groups, moeeye_invisible_maze_regional_groups, self.options.goal.option_sand),
        (SMORegion.ice_cave_regional_groups, ice_cave_regional_groups, self.options.goal.option_sand),
        (SMORegion.pyramid_upper_interior_regional_groups, pyramid_upper_interior_regional_groups, self.options.goal.option_sand),
        (SMORegion.underground_ruins_regional_groups, underground_ruins_regional_groups, self.options.goal.option_sand),
        (SMORegion.sky_garden_tower_regional_groups, sky_garden_tower_regional_groups, self.options.goal.option_metro),
        (SMORegion.flooded_pipes_regional_groups, flooded_pipes_regional_groups, self.options.goal.option_metro),
        (SMORegion.deep_woods_regional_groups, deep_woods_regional_groups, self.options.goal.option_metro),
        (SMORegion.walking_on_clouds_regional_groups, walking_on_clouds_regional_groups, self.options.goal.option_metro),
        (SMORegion.wooded_flower_road_regional_groups, wooded_flower_road_regional_groups, self.options.goal.option_metro),
        (SMORegion.sherm_elevator_regional_groups, sherm_elevator_regional_groups, self.options.goal.option_metro),
        (SMORegion.bouncy_flowers_regional_groups, bouncy_flowers_regional_groups, self.options.goal.option_metro),
        (SMORegion.city_hall_regional_groups, city_hall_regional_groups, self.options.goal.option_metro),
        (SMORegion.sewers_regional_groups, sewers_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.bullet_billding_regional_groups, bullet_billding_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.high_rise_regional_groups, high_rise_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.trex_escape_regional_groups, trex_escape_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.sea_cave_regional_groups, sea_cave_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.shiveria_regional_groups, shiveria_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.snowline_regional_groups, snowline_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.cascading_magma_regional_groups, cascading_magma_regional_groups, self.options.goal.option_luncheon),
        (SMORegion.magma_narrow_path_regional_groups, magma_narrow_path_regional_groups, self.options.goal.option_moon),
        (SMORegion.spinning_athletics_regional_groups, spinning_athletics_regional_groups, self.options.goal.option_moon),
        (SMORegion.fork_flickin_regional_groups, fork_flickin_regional_groups, self.options.goal.option_moon),
        (SMORegion.moon_cave_regional_groups, moon_cave_regional_groups, self.options.goal.option_moon),
        (SMORegion.peachs_castle_regional_groups, peachs_castle_regional_groups, self.options.goal.option_dark),
        ]

    regional_coin_regions = [
        (SMORegion.cap_kingdom_regional_coins, cap_kingdom_regional_coins, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_regional_coins, cascade_kingdom_regional_coins, self.options.goal.option_sand),
        (SMORegion.cascade_kingdom_peace_regional_coins, cascade_kingdom_peace_regional_coins,
         self.options.goal.option_sand),
        (SMORegion.sand_kingdom_regional_coins, sand_kingdom_regional_coins, self.options.goal.option_sand),
        (
        SMORegion.sand_kingdom_peace_regional_coins, sand_kingdom_peace_regional_coins, self.options.goal.option_metro),
        (SMORegion.sand_kingdom_pyramid_over_world_regional_coins, sand_kingdom_pyramid_over_world_regional_coins,
         self.options.goal.option_sand),
        (SMORegion.wooded_kingdom_regional_coins, wooded_kingdom_regional_coins, self.options.goal.option_metro),
        (SMORegion.lake_kingdom_regional_coins, lake_kingdom_regional_coins, self.options.goal.option_metro),
        (SMORegion.lost_kingdom_regional_coins, lost_kingdom_regional_coins, self.options.goal.option_metro),
        (SMORegion.metro_kingdom_regional_coins, metro_kingdom_regional_coins, self.options.goal.option_metro),
        (SMORegion.night_metro_kingdom_regional_coins, night_metro_kingdom_regional_coins,
         self.options.goal.option_metro),
        (SMORegion.seaside_kingdom_regional_coins, seaside_kingdom_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.snow_kingdom_regional_coins, snow_kingdom_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_regional_coins, luncheon_kingdom_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.luncheon_kingdom_post_meat_regional_coins, luncheon_kingdom_post_meat_regional_coins,
         self.options.goal.option_luncheon),
        (SMORegion.bowsers_kingdom_regional_coins, bowsers_kingdom_regional_coins, self.options.goal.option_moon),
        (SMORegion.bowsers_kingdom_peace_regional_coins, bowsers_kingdom_peace_regional_coins,
         self.options.goal.option_moon),
        (SMORegion.moon_kingdom_regional_coins, moon_kingdom_regional_coins, self.options.goal.option_moon),
        (SMORegion.mushroom_kingdom_regional_coins, mushroom_kingdom_regional_coins, self.options.goal.option_dark),
        (SMORegion.top_hat_tower_regional_coins, top_hat_tower_regional_coins, self.options.goal.option_sand),
        (SMORegion.frog_pond_regional_coins, frog_pond_regional_coins, self.options.goal.option_sand),
        (SMORegion.push_blocks_regional_coins, pushblocks_regional_coins, self.options.goal.option_sand),
        (SMORegion.poison_tides_regional_coins, poison_tides_regional_coins, self.options.goal.option_sand),
        (SMORegion.chasm_lifts_regional_coins, chasm_lifts_regional_coins, self.options.goal.option_sand),
        (SMORegion.bullet_bill_maze_regional_coins, bullet_bill_maze_regional_coins, self.options.goal.option_sand),
        (SMORegion.jaxi_ruins_regional_coins, jaxi_ruins_regional_coins, self.options.goal.option_sand),
        (SMORegion.strange_neighborhood_regional_coins, strange_neighborhood_regional_coins,
         self.options.goal.option_sand),
        (SMORegion.moe_eye_invisible_maze_regional_coins, moeeye_invisible_maze_regional_coins,
         self.options.goal.option_sand),
        (SMORegion.ice_cave_regional_coins, ice_cave_regional_coins, self.options.goal.option_sand),
        (SMORegion.pyramid_upper_interior_regional_coins, pyramid_upper_interior_regional_coins,
         self.options.goal.option_sand),
        (SMORegion.underground_ruins_regional_coins, underground_ruins_regional_coins, self.options.goal.option_sand),
        (SMORegion.sky_garden_tower_regional_coins, sky_garden_tower_regional_coins, self.options.goal.option_metro),
        (SMORegion.flooded_pipes_regional_coins, flooded_pipes_regional_coins, self.options.goal.option_metro),
        (SMORegion.deep_woods_regional_coins, deep_woods_regional_coins, self.options.goal.option_metro),
        (SMORegion.walking_on_clouds_regional_coins, walking_on_clouds_regional_coins, self.options.goal.option_metro),
        (
        SMORegion.wooded_flower_road_regional_coins, wooded_flower_road_regional_coins, self.options.goal.option_metro),
        (SMORegion.sherm_elevator_regional_coins, sherm_elevator_regional_coins, self.options.goal.option_metro),
        (SMORegion.bouncy_flowers_regional_coins, bouncy_flowers_regional_coins, self.options.goal.option_metro),
        (SMORegion.city_hall_regional_coins, city_hall_regional_coins, self.options.goal.option_metro),
        (SMORegion.sewers_regional_coins, sewers_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.bullet_billding_regional_coins, bullet_billding_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.high_rise_regional_coins, high_rise_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.trex_escape_regional_coins, trex_escape_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.sea_cave_regional_coins, sea_cave_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.shiveria_regional_coins, shiveria_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.snowline_regional_coins, snowline_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.cascading_magma_regional_coins, cascading_magma_regional_coins, self.options.goal.option_luncheon),
        (SMORegion.magma_narrow_path_regional_coins, magma_narrow_path_regional_coins, self.options.goal.option_moon),
        (SMORegion.spinning_athletics_regional_coins, spinning_athletics_regional_coins, self.options.goal.option_moon),
        (SMORegion.fork_flickin_regional_coins, fork_flickin_regional_coins, self.options.goal.option_moon),
        (SMORegion.moon_cave_regional_coins, moon_cave_regional_coins, self.options.goal.option_moon),
        (SMORegion.peachs_castle_regional_coins, peachs_castle_regional_coins, self.options.goal.option_dark),
    ]

    #endregion

    # Sub areas which have two or more over world exits that lead into them
    alternate_entrances = {
        SMOEntranceData.deepest_underground_shortcut: SMORegion.deepest_underground,
        SMOEntranceData.metro_kingdom_shop: SMORegion.metro_kingdom_shop,
        SMOEntranceData.metro_kingdom_shop_regional: SMORegion.metro_kingdom_shop,
        SMOEntranceData.inverted_pyramid_upper_interior_reverse: SMORegion.inverted_pyramid_upper_interior,
        #SMOEntranceData.sky_garden_tower: SMORegion.metro_kingdom_shop,
        SMOEntranceData.deep_woods_1 : SMORegion.deep_woods,
        SMOEntranceData.deep_woods_3 : SMORegion.deep_woods,
        SMOEntranceData.deep_woods_2 : SMORegion.wooded_kingdom,
        SMOEntranceData.deep_woods_4 : SMORegion.wooded_kingdom,
    }

    rocket_sub_areas = [
        SMOEntranceData.strange_neighborhood,
        SMOEntranceData.fog_wandering,
        SMOEntranceData.high_rise,
        SMOEntranceData.wading_in_the_cloud_sea,
        SMOEntranceData.roulette_tower,
        SMOEntranceData.mushroom_picture_match,
    ]

    access_requirement_sub_areas = [
        "Sand Costume Bonus (Dancing Room)",
        "Strange Neighborhood",
        "Secret Flower Field",
        "Fog Wandering",
        "Deep Woods: Costume Bonus (Treasure Chest)",
        "Zipper Chasm",
        "RC Race",
        "Rotating Maze",
        "Metro Siege",
        "High Rise",
        "Sewers",
        "Wading in the Cloud Sea",
        "Ty-Foo Sliding Puzzle",
        "Luncheon Costume Bonus (Cooking Pots)",
        "Roulette Tower",
        "Folding Screen",
        "Yoshi in the Sea of Clouds",
        "Painting Room: Lord of Lightning",
        "Mushroom Picture Match",
        "Castle Courtyard",
        "Dark Side Topper",
        "Deepest Underground",
        "Freezing Room",
    ]

    can_reach_mushroom = And(CanReachRegion(SMORegion.mushroom_kingdom), CanReachRegion(SMORegion.odyssey_complete))
    can_reach_deep_moon_cave = And(
        CanCapture(SMOItemData.parabones),
        CanCapture(SMOItemData.sherm),
        CanCapture(SMOItemData.spark_pylon)
    )
    can_reach_end_moon_cave = And(can_reach_deep_moon_cave, CanCapture(SMOItemData.banzai_bill))

    #region Connections

    odyssey_connections = [
        (SMORegion.defunct_odyssey, {
            SMORegion.restored_odyssey: And(
                CanReachRegion(SMORegion.cascade_kingdom_peace),
                HasGroup("Cascade Moons", self.moon_counts[SMOKingdoms.CASCADE])
            ),
            SMORegion.odyssey_interior: True_(),
            SMORegion.cap_kingdom: True_(),
            SMORegion.cascade_kingdom: True_(),
                                     }),
        (SMORegion.restored_odyssey, {
            SMORegion.cascade_kingdom_revisit: True_(),
            SMORegion.sand_kingdom: True_(),
            SMORegion.odyssey_sail_sand: HasGroup("Sand Moons", self.moon_counts[SMOKingdoms.SAND]),
            SMORegion.odyssey_outfit: True_(),
        }),
        (SMORegion.odyssey_interior, {
            SMORegion.restored_odyssey: True_()
        }),
        (SMORegion.odyssey_sail_sand, {
            SMORegion.lake_kingdom: True_(),
            SMORegion.odyssey_sails_branch_1: HasGroup("Lake Moons", self.moon_counts[SMOKingdoms.LAKE]),
        }),
        (SMORegion.odyssey_sails_branch_1, {
            SMORegion.odyssey_broken_down: And(
                HasGroup("Lake Moons", self.moon_counts[SMOKingdoms.LAKE]),
                HasGroup("Wooded Moons", self.moon_counts[SMOKingdoms.WOODED]),
            ),
            SMORegion.wooded_kingdom: True_(),
        }),
        (SMORegion.odyssey_broken_down, {
            SMORegion.cloud_kingdom_boss_fight: True_(),
            SMORegion.lost_kingdom: True_(),
            SMORegion.cloud_kingdom_revisit: True_(),
            SMORegion.odyssey_repaired_lost: HasGroup("Lost Moons", self.moon_counts[SMOKingdoms.LOST]),
        }),
        (SMORegion.odyssey_repaired_lost, {
            SMORegion.night_metro_kingdom: CanCapture(SMOItemData.spark_pylon),
            SMORegion.lost_kingdom_revisit: True_(),
            SMORegion.odyssey_sail_metro: HasGroup("Metro Moons", self.moon_counts[SMOKingdoms.METRO]),
        }),
        (SMORegion.odyssey_sail_metro, {
            SMORegion.snow_kingdom: True_(),
            SMORegion.odyssey_sails_branch_2: HasGroup("Snow Moons", self.moon_counts[SMOKingdoms.SNOW]),
        }),
        (SMORegion.odyssey_sails_branch_2, {
            SMORegion.seaside_kingdom: True_(),
            SMORegion.luncheon_kingdom: And(
                HasGroup("Snow Moons", self.moon_counts[SMOKingdoms.SNOW]),
                HasGroup("Seaside Moons", self.moon_counts[SMOKingdoms.SEASIDE]),
            ),
            SMORegion.odyssey_sail_luncheon: HasGroup("Luncheon Moons", self.moon_counts[SMOKingdoms.LUNCHEON]),
        }),
        (SMORegion.odyssey_sail_luncheon, {
            SMORegion.ruined_kingdom: True_(),
            SMORegion.odyssey_repaired_ruined: HasGroup("Ruined Moons", self.moon_counts[SMOKingdoms.RUINED]),
        }),
        (SMORegion.odyssey_repaired_ruined, {
            SMORegion.bowsers_kingdom: True_(),
            SMORegion.odyssey_complete: And(
                HasGroup("Bowser Moons", self.moon_counts[SMOKingdoms.BOWSER]),
                CanReachRegion(SMORegion.bowser_kingdom_peace)
            )
        }),
        (SMORegion.odyssey_complete, {
            SMORegion.moon_kingdom: True_(),
            SMORegion.moon_kingdom_tuxedo: True_(),
            SMORegion.mushroom_kingdom: CanCapture(SMOItemData.bowser),
            SMORegion.odyssey_powered_up_dark: And(
                CanCapture(SMOItemData.bowser),
                HasGroup("Dark Moons", self.moon_counts[SMOKingdoms.DARK]),
            )
        }),
        (SMORegion.odyssey_powered_up_dark, {
            SMORegion.dark_side : True_(),
            SMORegion.odyssey_powered_up_darker: HasGroup("Darker Moons", self.moon_counts[SMOKingdoms.DARKER]),
        }),
        (SMORegion.odyssey_powered_up_darker, {
            SMORegion.darker_side : True_()
        }),
    ]

    world_connections = [
        (SMORegion.menu, {
            SMORegion.cap_kingdom_intro: True_(),
            SMORegion.cap_kingdom: True_(),
        }),
        (SMORegion.cap_kingdom_intro, {
            SMORegion.top_hat_tower: HasAny(*cappy)
        }),
        (SMORegion.cap_kingdom_topper, {
            SMORegion.cascade_kingdom: True_(),
        }),
        (SMORegion.cap_kingdom, {
            SMORegion.cap_kingdom_moon_rock: CanCapture(SMOItemData.paragoomba),
            SMORegion.cap_kingdom_shop: True_(),
            SMORegion.cap_kingdom_regional_coins: True_(),
            SMORegion.cap_kingdom_regional_groups: True_(),
        }),
        (SMORegion.cascade_kingdom, {
            SMORegion.cascade_kingdom_peace: CanCapture(SMOItemData.broodes_chain_chomp),
            SMORegion.defunct_odyssey: True_(),
            SMORegion.t_rex: CanCapture(SMOItemData.chain_chomp),
            SMORegion.chain_chomp: True_(),
            SMORegion.big_chain_chomp: CanCapture(SMOItemData.chain_chomp),
            SMORegion.broodes_chain_chomp: Or(
                CanCapture(SMOItemData.big_chain_chomp),
                CanCapture(SMOItemData.t_rex)
            ),
            SMORegion.cascade_kingdom_regional_coins: True_(),
            SMORegion.cascade_kingdom_regional_groups: True_(),
        }),
        (SMORegion.cascade_kingdom_peace, {
            SMORegion.cascade_kingdom_peace_regional_coins: True_(),
            SMORegion.cascade_kingdom_peace_regional_groups: True_(),
            SMORegion.cascade_kingdom_moon_rock: HasAny(*cappy),
        }),
        (SMORegion.cascade_kingdom_revisit, {
            SMORegion.cascade_kingdom_shop: True_(),
        }),
        (SMORegion.sand_kingdom, {
            #SMORegion.sand_kingdom_shop: None,
            SMORegion.binoculars: True_(),
            SMORegion.bullet_bill: True_(),
            SMORegion.moe_eye: True_(),
            SMORegion.cactus: True_(),
            SMORegion.night_sand_kingdom: CanReachRegion(SMORegion.top_of_the_inverted_pyramid),
            SMORegion.sand_kingdom_regional_coins: True_(),
            SMORegion.sand_kingdom_regional_groups: True_(),
        }),
        (SMORegion.top_of_the_inverted_pyramid, {
            SMORegion.sand_kingdom_pyramid_over_world_regional_coins: True_(),
            SMORegion.sand_kingdom_pyramid_over_world_regional_groups: True_(),
        }),
        (SMORegion.night_sand_kingdom, {
            SMORegion.underground_ruins: True_(),
        }),
        (SMORegion.sand_kingdom_peace, {
            SMORegion.deepest_underground_peace: True_(),
            SMORegion.mini_rocket: True_(),
            SMORegion.glydon: True_(),
            SMORegion.lakitu: True_(),
            SMORegion.strange_neighborhood: CanCapture(SMOItemData.mini_rocket),
            SMORegion.sand_kingdom_moon_rock: HasAny(*cappy),
            SMORegion.top_of_the_inverted_pyramid: CanCapture(SMOItemData.spark_pylon),
            SMORegion.top_of_the_inverted_pyramid_peace: CanReachRegion(SMORegion.top_of_the_inverted_pyramid),
            SMORegion.sand_kingdom_peace_regional_coins: True_(),
            SMORegion.sand_kingdom_peace_regional_groups: True_(),
        }),
        (SMORegion.wooded_kingdom, {
            SMORegion.wooded_kingdom_post_broodals: CanReachRegion(SMORegion.wooded_kingdom_spewer),
            SMORegion.wooded_kingdom_shop: True_(),
            SMORegion.wooded_kingdom_regional_coins: True_(),
            SMORegion.wooded_kingdom_regional_groups: True_(),
        }),
        (SMORegion.wooded_kingdom_post_broodals, {
            SMORegion.wooded_kingdom_peace: And(
                CanCapture(SMOItemData.sherm),
                CanCapture(SMOItemData.uproot)
            ),
            SMORegion.sherm: True_()
        }),
        (SMORegion.wooded_kingdom_peace, {
            SMORegion.wooded_kingdom_moon_rock: HasAny(*cappy),
        }),
        (SMORegion.lake_kingdom, {
            SMORegion.cheep_cheep: True_(), # CanReachRegion(SMORegion.lake_kingdom_underwater)
            SMORegion.zipper: True_(),
            SMORegion.goomba: True_(), # CanReachRegion(SMORegion.lake_kingdom_pond)
            SMORegion.lakitu: True_(), # CanReachRegion(SMORegion.lake_kingdom_pond)
            #SMORegion.lake_kingdom_shop: None,
            SMORegion.lake_kingdom_moon_rock: HasAny(*cappy),
            SMORegion.lake_kingdom_regional_coins: True_(),
            SMORegion.lake_kingdom_regional_groups: True_(),
        }),
        (SMORegion.cloud_kingdom_boss_fight, {

        }),
        (SMORegion.cloud_kingdom_revisit, {
            SMORegion.cloud_kingdom_moon_rock: HasAny(*cappy),
        }
         ),
        (SMORegion.lost_kingdom, {
            #SMORegion.lost_kingdom_shop: None,
            SMORegion.tropical_wiggler: True_(),
            SMORegion.lost_kingdom_regional_coins: True_(),
            SMORegion.lost_kingdom_regional_groups: True_(),
            SMORegion.lost_kingdom_moon_rock: HasAny(*cappy),
        }),
        (SMORegion.lost_kingdom_revisit, {
            # SMORegion.lost_kingdom_moon_rock: can_reach_mushroom,
        }),
        (SMORegion.night_metro_kingdom, {
            #SMORegion.metro_kingdom_shop: None,
            SMORegion.day_metro_kingdom: And(
                CanCapture(SMOItemData.sherm),
                CanCapture(SMOItemData.spark_pylon)
            ),
            SMORegion.night_metro_kingdom_regional_coins: True_(),
            SMORegion.night_metro_kingdom_regional_groups: True_(),
        }),
        (SMORegion.day_metro_kingdom, {
            SMORegion.pole: True_(),
            SMORegion.manhole: True_(),
            SMORegion.taxi: True_(),
            SMORegion.metro_kingdom_regional_coins: True_(),
            SMORegion.metro_kingdom_regional_groups: True_(),
        }),
        (SMORegion.metro_kingdom_peace, {
            SMORegion.metro_kingdom_moon_rock: HasAny(*cappy),
        }),
        (SMORegion.seaside_kingdom, {
            SMORegion.gushen: True_(),
            SMORegion.seaside_kingdom_shop: True_(),
            SMORegion.seaside_kingdom_peace: CanCapture(SMOItemData.gushen),
            SMORegion.seaside_kingdom_regional_coins: True_(),
            SMORegion.seaside_kingdom_regional_groups: True_(),
        }),
        (SMORegion.seaside_kingdom_peace, {
            SMORegion.seaside_kingdom_moon_rock: HasAny(*cappy),
        }),
        (SMORegion.snow_kingdom, {
            #SMORegion.snow_kingdom_shop: None,
            SMORegion.snow_kingdom_peace: And(
                CanReachRegion(SMORegion.snowline_circuit),
                CanCapture(SMOItemData.shiverian_racer)
            ),
            SMORegion.snow_kingdom_regional_coins: True_(),
            SMORegion.snow_kingdom_regional_groups: True_(),
        }),
        (SMORegion.snow_kingdom_peace, {
            SMORegion.ty_foo: True_(),
            SMORegion.cheep_cheep_snow_kingdom: True_(),
        SMORegion.snow_kingdom_moon_rock: HasAny(*cappy)
        }),
        (SMORegion.luncheon_kingdom, {
            SMORegion.lava_bubble: True_(),
            SMORegion.luncheon_kingdom_post_broodals: True_(),
            SMORegion.luncheon_kingdom_regional_coins: True_(),
            SMORegion.luncheon_kingdom_regional_groups: True_(),
        }),
        (SMORegion.luncheon_kingdom_post_broodals, {
            SMORegion.hammer_bro: True_(),
            #SMORegion.luncheon_kingdom_shop: None,
            SMORegion.luncheon_kingdom_meat: True_(),
        }),
        (SMORegion.luncheon_kingdom_meat, {
            SMORegion.meat: True_(),
            SMORegion.cascading_magma: CanReachLocation("Luncheon Kingdom - Big Pot on the Volcano: Dive In!"),
        }),
        (SMORegion.cascading_magma, {
            SMORegion.luncheon_kingdom_post_meat_regional_coins: True_(),
            SMORegion.luncheon_kingdom_post_meat_regional_groups: True_(),
            SMORegion.cascading_magma_regional_coins: True_(),
            SMORegion.cascading_magma_regional_groups: True_(),
            SMORegion.lava_bubble: True_(),
            SMORegion.luncheon_kingdom_peace: CanCapture(SMOItemData.lava_bubble)
        }),
        (SMORegion.luncheon_kingdom_peace, {
            SMORegion.fire_piranha_plant: True_(),
            SMORegion.luncheon_kingdom_moon_rock: HasAny(*cappy)
        }),
        (SMORegion.ruined_kingdom, {
            SMORegion.spark_pylon: True_(),
            SMORegion.ruined_kingdom_moon_rock: HasAny(*cappy)
        }),
        (SMORegion.bowsers_kingdom, {
            SMORegion.infiltrate_bowsers_castle: CanCapture(SMOItemData.spark_pylon),
            SMORegion.bowsers_kingdom_regional_coins: True_(),
            SMORegion.bowsers_kingdom_regional_groups: True_(),
        }),
        (SMORegion.infiltrate_bowsers_castle, {
            SMORegion.bowser_kingdom_smart_bombing: CanCapture(SMOItemData.pokio) # {difficulty} Trick, just have the pokio hit it lmao
        }),
        (SMORegion.bowser_kingdom_smart_bombing, {
            SMORegion.pokio: True_(),
            SMORegion.jizo: True_(),
            # SMORegion.bowser_kingdom_shop: None,
            SMORegion.bowser_kingdom_mecha_broodal: True_(),
        }),
        (SMORegion.bowser_kingdom_mecha_broodal, {
            SMORegion.bowser_kingdom_peace: CanReachLocation(SMOLocationData.showdown_at_bowsers_castle)
        }),
        (SMORegion.bowser_kingdom_peace, {
            SMORegion.bowser_kingdom_moon_rock: HasAny(*cappy),
            SMORegion.bowsers_kingdom_peace_regional_coins: True_(),
            SMORegion.bowsers_kingdom_peace_regional_groups: True_(),
        }),
        (SMORegion.moon_kingdom, {
            #SMORegion.moon_kingdom_shop: None,
            SMORegion.moon_kingdom_peace: can_reach_mushroom,
            SMORegion.moon_kingdom_regional_coins: True_(),
            SMORegion.moon_kingdom_regional_groups: True_(),
        }),
        (SMORegion.moon_kingdom_peace, {
            SMORegion.moon_kingdom_moon_rock: can_reach_mushroom,
        }), # Once post moon
        (SMORegion.mushroom_kingdom, {
            SMORegion.yoshi: True_(),
            #SMORegion.mushroom_kingdom_shop: True_(),
            SMORegion.mushroom_kingdom_regional_coins: True_(),
            SMORegion.mushroom_kingdom_regional_groups: True_(),
        }),
        (SMORegion.dark_side, {
        }),
        (SMORegion.dark_side_peace, {
            SMORegion.dark_side_outfit: True_(),
        }),
        (SMORegion.darker_side, {

        }),
        (SMORegion.darker_side_tower, {
            SMORegion.darker_side_outfit: True_()
        }),
        (SMORegion.metro_kingdom_moon_rock, {
            SMORegion.letter: True_(),
        }),
    ]

    sub_area_connections = [
        (SMORegion.top_hat_tower, {
            SMORegion.frog: True_(),
            SMORegion.cap_kingdom_topper: And(
                CanCapture(SMOItemData.frog)
            ),
            SMORegion.top_hat_tower_regional_coins: True_(),
            SMORegion.top_hat_tower_regional_groups: True_(),
        }),
        (SMORegion.frog_pond, {
            SMORegion.frog: True_(),
            SMORegion.top_hat_tower_regional_coins: True_(),
            SMORegion.top_hat_tower_regional_groups: True_(),
        }),
        (SMORegion.poison_tides, {
            SMORegion.paragoomba: True_(),
            SMORegion.poison_tides_regional_coins: True_(),
            SMORegion.poison_tides_regional_groups: True_(),
        }),
        (SMORegion.push_block, {
            SMORegion.spark_pylon: True_(),
            SMORegion.push_blocks_regional_coins: True_(),
            SMORegion.push_blocks_regional_groups: True_(),
        }),
        (SMORegion.rolling_lane, {

        }),
        (SMORegion.chain_chomp_cave, {
            SMORegion.chain_chomp: True_()
        }),
        (SMORegion.t_rex_nest, {
            SMORegion.t_rex: True_()
        }),
        (SMORegion.chasm_lifts, {
            SMORegion.chasm_lifts_regional_coins: True_(),
            SMORegion.chasm_lifts_regional_groups: True_(),
        }),
        (SMORegion.gusty_bridges, {

        }),
        (SMORegion.moe_eye_invisible_maze, {
            SMORegion.moe_eye: True_(),
            SMORegion.moe_eye_invisible_maze_regional_coins: True_(),
            SMORegion.moe_eye_invisible_maze_regional_groups: True_(),
        }),
        (SMORegion.bullet_bill_maze, {
            SMORegion.bullet_bill: True_(),
            SMORegion.bullet_bill_maze_regional_coins: True_(),
            SMORegion.bullet_bill_maze_regional_groups: True_(),
        }),
        (SMORegion.jaxi_ruins, {
            SMORegion.jaxi_ruins_regional_coins: True_(),
            SMORegion.jaxi_ruins_regional_groups: True_(),
        }),
        (SMORegion.strange_neighborhood, {
            SMORegion.goomba: Has(SMOItemData.jump),
            SMORegion.strange_neighborhood_regional_coins: True_(),
            SMORegion.strange_neighborhood_regional_groups: True_(),
        }),
        (SMORegion.sand_outfit, {

        }),
        (SMORegion.sand_rumbling_floor_house, {

        }),
        # (SMORegion.employees_only, {
        #
        # }
        #  ),
        (SMORegion.ice_cave, {
            SMORegion.ice_cave_regional_coins: True_(),
            SMORegion.ice_cave_regional_groups: True_(),
        }),
        (SMORegion.sand_sphynx_vault, {

        }),
        (SMORegion.sand_slots, {

        }),
        (SMORegion.inverted_pyramid_lower_interior, {
            #SMORegion.inverted_pyramid_lower_interior: None
        }),
        (SMORegion.inverted_pyramid_upper_interior, {
            #SMORegion.top_of_the_inverted_pyramid: None
            SMORegion.pyramid_upper_interior_regional_coins: True_(),
            SMORegion.pyramid_upper_interior_regional_groups: True_(),
        }),
        (SMORegion.underground_ruins, {
            #SMORegion.deepest_underground: (lambda state: state.has(SMORegion.bullet_bill,self.player)) if self.options.capture_sanity else None,
            SMORegion.goomba: True_(),
            SMORegion.bullet_bill: Has(SMOItemData.jump),
            SMORegion.underground_ruins_regional_coins: True_(),
            SMORegion.underground_ruins_regional_groups: True_(),
        }),
        (SMORegion.deepest_underground, {
            SMORegion.sand_kingdom_peace: CanCapture(SMOItemData.knucklotecs_fist),
            SMORegion.bullet_bill: True_(),
            SMORegion.knucklotecs_fist: CanCapture(SMOItemData.bullet_bill),
            SMORegion.deepest_underground_post_game: CanReachRegion(SMORegion.sand_kingdom_peace),
        }),
        (SMORegion.deepest_underground_peace, {

        }),
        (SMORegion.deepest_underground_post_game, {

        }),
        (SMORegion.moe_eye_invisible_floor, {
            SMORegion.moe_eye: True_()
        }),
        (SMORegion.colossal_ruins, {

        }),
        (SMORegion.freezing_waterway, {
            SMORegion.gushen: True_()
        }),
        (SMORegion.arch_repair, {
            SMORegion.puzzle_part_lake_kingdom: True_()
        }),
        (SMORegion.zipper_chasm, {
            SMORegion.zipper: True_()
        }),
        (SMORegion.bouncy_flowers, {
            SMORegion.bouncy_flowers_regional_coins: True_(),
            SMORegion.bouncy_flowers_regional_groups: True_(),
        }),
        (SMORegion.poison_swamp, {
            SMORegion.frog: True_()
        }),
        (SMORegion.sky_garden_tower, {
            SMORegion.sky_garden_tower_regional_coins: True_(),
            SMORegion.sky_garden_tower_regional_groups: True_(),
        }),
        (SMORegion.deep_woods_treasure_trap, {

        }),
        (SMORegion.explorer_outift, {

        }),
        (SMORegion.flooding_pipeway, {
            SMORegion.flooded_pipes_regional_coins: True_(),
            SMORegion.flooded_pipes_regional_groups: True_(),
        }),
        (SMORegion.wooded_flower_road, {
            SMORegion.goomba: True_(),
            SMORegion.wooded_flower_road_regional_coins: True_(),
            SMORegion.wooded_flower_road_regional_groups: True_(),
        }),
        (SMORegion.sherm_elevator, {
            SMORegion.sherm: True_(),
            SMORegion.fire_bro: True_(),
            SMORegion.sherm_elevator_regional_coins: True_(),
            SMORegion.sherm_elevator_regional_groups: True_(),
        }),
        (SMORegion.fog_wandering, {
            SMORegion.paragoomba: True_()
        }),
        (SMORegion.walking_on_clouds, {
            SMORegion.uproot: True_(),
            SMORegion.walking_on_clouds_regional_coins: True_(),
            SMORegion.walking_on_clouds_regional_groups: True_(),
        }),
        (SMORegion.secret_flower_field, {
            SMORegion.uproot: True_(),
            SMORegion.secret_flower_field_peace: CanReachRegion(SMORegion.wooded_kingdom_peace),
        }),
        (SMORegion.secret_flower_field_peace, {

        }),
        (SMORegion.deep_woods, {
            SMORegion.t_rex: True_(),
            SMORegion.coin_coffer: True_(),
            SMORegion.boulder: True_(),
            SMORegion.tree: Has(SMOItemData.jump),
            SMORegion.deep_woods_regional_coins: True_(),
            SMORegion.deep_woods_regional_groups: True_(),
        }),
        (SMORegion.nut_room, {

        }),
        (SMORegion.invisible_road, {
            SMORegion.poison_piranha_plant: True_()
        }),
        (SMORegion.sheep_herding, {

        }),
        (SMORegion.breakdown_road, {
            SMORegion.bullet_bill: True_(),
            SMORegion.banzai_bill: True_()
        }),
        (SMORegion.cloud_picture_match, {
            SMORegion.picture_match_part_goomba: True_(),
            SMORegion.cloud_post_game_picture_match: CanReachRegion(SMORegion.wooded_kingdom_moon_rock)
        }),
        (SMORegion.cloud_post_game_picture_match, {
            SMORegion.picture_match_part_goomba: True_()
        }),
        (SMORegion.king_of_the_cube, {

        }),
        (SMORegion.tropical_wiggler_swamp, {
            SMORegion.tropical_wiggler: True_()
        }),
        (SMORegion.klepto_lava_bath, {
            SMORegion.lava_bubble: True_()
        }),
        (SMORegion.metro_slots, {

        }),
        (SMORegion.rc_race, {
            SMORegion.rc_car: True_(),
            SMORegion.rc_race_post_game: CanReachRegion(SMORegion.metro_kingdom_peace)
        }),
        (SMORegion.private_room, {

        }),
        (SMORegion.city_hall, {
            SMORegion.city_hall_regional_coins: True_(),
            SMORegion.city_hall_regional_groups: True_(),
        }),
        (SMORegion.crowded_street, {
            SMORegion.crowded_street_post_game: CanReachRegion(SMORegion.metro_kingdom_peace)
        }),
        (SMORegion.builder_outfit, {
            SMORegion.spark_pylon: True_()
        }),
        (SMORegion.metro_siege, {
            SMORegion.sherm: True_()
        }),
        (SMORegion.rotating_maze, {

        }),
        (SMORegion.high_rise, {
            SMORegion.high_rise_regional_coins: True_(),
            SMORegion.high_rise_regional_groups: True_(),
        }),
        (SMORegion.bullet_billding, {
            SMORegion.bullet_bill: True_(),
            SMORegion.bullet_billding_regional_coins: True_(),
            SMORegion.bullet_billding_regional_groups: True_(),
        }),
        (SMORegion.t_rex_escape, {
            SMORegion.trex_escape_regional_coins: True_(),
            SMORegion.trex_escape_regional_groups: True_(),
        }),
        (SMORegion.projection_room, {

        }),
        (SMORegion.pitch_black_island, {

        }),
        (SMORegion.swinging_scaffolding, {
            SMORegion.hammer_bro: True_()
        }),
        (SMORegion.vanishing_road, {

        }),
        (SMORegion.sewers, {
            SMORegion.metro_kingdom_peace: CanReachRegion(SMORegion.day_metro_kingdom),
            SMORegion.sewers_post_game: And(
                CanReachRegion(SMORegion.day_metro_kingdom),
                CanReachRegion(SMORegion.mushroom_kingdom)
            ),
            SMORegion.sewers_regional_coins: True_(),
            SMORegion.sewers_regional_groups: True_(),
        }),
        (SMORegion.sewers_post_game, {
            SMORegion.puzzle_part_metro_kingdom: True_()
        }),
        (SMORegion.sandy_bottom, {

        }),
        (SMORegion.seaside_waterway, {
            SMORegion.cheep_cheep: True_(),
            SMORegion.sea_cave_regional_coins: True_(),
            SMORegion.sea_cave_regional_groups: True_(),
        }),
        (SMORegion.seaside_sphynx_vault, {

        }),
        (SMORegion.seaside_rumbling_room, {

        }),
        (SMORegion.resort_outfit, {

        }),
        (SMORegion.wading_in_the_cloud_sea, {

        }),
        (SMORegion.narrow_valley, {
            SMORegion.gushen: True_()
        }),
        (SMORegion.sinking_island, {
            SMORegion.uproot: True_(),
        }),
        (SMORegion.pokio_bomb_aiming, {
            SMORegion.pokio: True_()
        }),
        (SMORegion.spinning_maze, {

        }),
        (SMORegion.shiveria, {
            SMORegion.goomba: True_(),
            SMORegion.ty_foo: True_(),
            SMORegion.shiveria_peace: CanReachRegion(SMORegion.snow_kingdom_peace),
            SMORegion.shiveria_regional_coins: True_(),
            SMORegion.shiveria_regional_groups: True_(),
        }),
        (SMORegion.snowline_circuit, {
            SMORegion.shiverian_racer: True_(),
            SMORegion.snow_kingdom_peace: CanCapture(SMOItemData.shiverian_racer),
            SMORegion.snowline_regional_coins: True_(),
            SMORegion.snowline_regional_groups: True_(),
         }),
        (SMORegion.shiveria_peace, {
            SMORegion.icicle_barrier_post_game: CanReachRegion(SMORegion.snow_kingdom_peace),
            SMORegion.ice_wall_barrier_post_game: CanReachRegion(SMORegion.snow_kingdom_peace),
            SMORegion.snowy_mountain_barrier_post_game: CanReachRegion(SMORegion.snow_kingdom_peace),
            SMORegion.gusty_barrier_post_game: CanReachRegion(SMORegion.snow_kingdom_peace),
        }),
        (SMORegion.icicle_barrier_post_game, {
            SMORegion.goomba: True_()
        }),
        (SMORegion.ice_wall_barrier_post_game, {

        }),
        (SMORegion.gusty_barrier_post_game, {
            SMORegion.ty_foo: True_()
        }),
        (SMORegion.snowy_mountain_barrier_post_game, {

        }),
        (SMORegion.magma_swamp, {

        }),
        (SMORegion.luncheon_treasure_vault, {

        }),
        (SMORegion.chef_outfit, {
            SMORegion.lava_bubble: True_()
        }),
        (SMORegion.fork_flickin, {
            SMORegion.volbonan: True_(),
            SMORegion.fork_flickin_regional_coins: True_(),
            SMORegion.fork_flickin_regional_groups: True_(),
        }),
        (SMORegion.cheese_excavate, {
            SMORegion.hammer_bro: True_(),
        }),
        (SMORegion.magma_narrow_path, {
            SMORegion.lava_bubble: True_(),
            SMORegion.magma_narrow_path_regional_coins: True_(),
            SMORegion.magma_narrow_path_regional_groups: True_(),
        }),
        (SMORegion.spinning_athletics, {
            SMORegion.spinning_athletics_regional_coins: True_(),
            SMORegion.spinning_athletics_regional_groups: True_(),
        }),
        (SMORegion.luncheon_slots, {

        }),
        (SMORegion.rotating_gears_with_bitefrost, {
            SMORegion.fire_bro: True_()
        }),
        (SMORegion.volcano_cave, {

        }),
        (SMORegion.lava_islands, {
            SMORegion.lava_bubble: True_()
        }),
        (SMORegion.roulette_tower, {

        }),
        (SMORegion.chargin_chuck_arena, {
            SMORegion.chargin_chuck: True_()
        }),
        (SMORegion.folding_screen, {

        }),
        (SMORegion.bowsers_treasure_vault, {

        }),
        (SMORegion.jizos_adventure, {
            SMORegion.jizo: True_()
        }),
        (SMORegion.spinning_tower, {

        }),
        (SMORegion.hexagon_tower, {
            SMORegion.parabones: True_()
        }),
        (SMORegion.wooden_tower, {
            SMORegion.pokio: True_()
        }),
        (SMORegion.moon_cave, {
            SMORegion.bowser_statue: True_(),
            SMORegion.parabones: True_(),
            SMORegion.sherm: CanCapture(SMOItemData.parabones),
            SMORegion.spark_pylon: CanCapture(SMOItemData.parabones),
            SMORegion.hammer_bro: can_reach_deep_moon_cave,
            SMORegion.banzai_bill: can_reach_deep_moon_cave,
            SMORegion.bullet_bill: can_reach_end_moon_cave,
            SMORegion.moe_eye: can_reach_end_moon_cave,
            SMORegion.chargin_chuck: can_reach_end_moon_cave,
            SMORegion.broodes_chain_chomp: can_reach_end_moon_cave,
            SMORegion.moon_cave_regional_coins: True_(),
            SMORegion.moon_cave_regional_groups: True_(),
        }),
        (SMORegion.inside_the_church, {
            SMORegion.bowser: True_(),
        }),
        (SMORegion.dot_galaxy, {

        }),
        (SMORegion.giant_swings, {

        }),
        (SMORegion.moon_sphynx_vault, {

        }),
        (SMORegion.mushroom_picture_match, {
            SMORegion.picture_match_part_mario: True_()
        }),
        (SMORegion.peachs_castle, {
            SMORegion.peachs_castle_regional_coins: True_(),
            SMORegion.peachs_castle_regional_groups: True_(),
        }),
        (SMORegion.castle_courtyard, {

        }),
        (SMORegion.mushroom_well, {

        }),
        (SMORegion.yoshi_in_the_sea_of_clouds, {
            SMORegion.yoshi: True_()
        }),
        (SMORegion.knucklotec_rematch, {
            SMORegion.knucklotecs_fist: True_()
        }),
        (SMORegion.torkdrift_rematch, {
            SMORegion.uproot: True_()
        }),
        (SMORegion.mollosque_lanceur_rematch, {
            SMORegion.gushen: True_()
        }),
        (SMORegion.mecha_wiggler_rematch, {
            SMORegion.sherm: True_()
        }),
        (SMORegion.cookatiel_rematch, {
            SMORegion.lava_bubble: True_()
        }),
        (SMORegion.lord_of_lightning_rematch, {

        }),
        (SMORegion.dark_side_breakdown_road, {

        }),
        (SMORegion.dark_side_invisible_road, {

        }),
        (SMORegion.dark_side_vanishing_road, {

        }),
        (SMORegion.dark_side_under_siege, {
            SMORegion.yoshi: True_()
        }),
        (SMORegion.dark_side_sinking_island, {
            SMORegion.yoshi: True_()
        }),
        (SMORegion.dark_side_magma_swamp, {
            SMORegion.yoshi: True_()
        }),
        (SMORegion.dark_side_topper, {
            SMORegion.dark_side_2: True_()
        }),
        (SMORegion.dark_side_harriet, {
            SMORegion.dark_side_3: True_()
        }),
        (SMORegion.dark_side_rango, {
            # Make captain toad region
            SMORegion.dark_side_peace: CanCapture(SMOItemData.hammer_bro)
        }),
        (SMORegion.dark_side_spewart, {
            SMORegion.dark_side_4: True_()
        }),
        (SMORegion.darker_side_entrance, {
            SMORegion.goomba: True_(),
            SMORegion.lava_bubble: True_(),
            SMORegion.uproot: CanCapture(SMOItemData.lava_bubble),
            SMORegion.yoshi: And(
                CanCapture(SMOItemData.lava_bubble),
                CanCapture(SMOItemData.uproot)
            ),
            SMORegion.glydon: And(
                CanCapture(SMOItemData.lava_bubble),
                CanCapture(SMOItemData.uproot),
                CanCapture(SMOItemData.yoshi),
            ),
            SMORegion.volbonan: And(
                CanCapture(SMOItemData.lava_bubble),
                CanCapture(SMOItemData.uproot),
                CanCapture(SMOItemData.yoshi),
                CanCapture(SMOItemData.glydon)
            ),
        }),
        (SMORegion.darker_side_climb, {
            SMORegion.pokio: True_()
        }),
        (SMORegion.darker_side_bowser, {
            SMORegion.bowser: True_()
        }),
        (SMORegion.darker_side_end, {
            SMORegion.spark_pylon: True_()
        }),
        # Shops
        (SMOEntranceData.sand_kingdom_shop, {
            SMORegion.sand_kingdom_shop: True_(),
        }),
        (SMOEntranceData.lake_kingdom_shop, {
            SMORegion.lake_kingdom_shop: True_(),
        }),
        (SMOEntranceData.lost_kingdom_shop, {
            SMORegion.lost_kingdom_shop: True_(),
        }),
        (SMORegion.metro_kingdom_shop, {
            SMORegion.metro_kingdom_shop: True_(),
        }),
        (SMOEntranceData.snow_kingdom_shop, {
            SMORegion.snow_kingdom_shop: True_(),
        }),
        (SMOEntranceData.luncheon_kingdom_shop, {
            SMORegion.luncheon_kingdom_shop: True_(),
        }),
        (SMOEntranceData.bowsers_kingdom_shop, {
            SMORegion.bowser_kingdom_shop: True_(),
        }),
        (SMOEntranceData.moon_kingdom_shop, {
            SMORegion.moon_kingdom_shop: True_(),
        }),
        (SMOEntranceData.mushroom_kingdom_shop, {
            SMORegion.mushroom_kingdom_shop: True_(),
        }),
    ]

    # non_entrance_rando_sub_area_connections = [
    #     (SMORegion.inverted_pyramid_lower_interior, {
    #         SMOEntranceData.inverted_pyramid_upper_interior: None,
    #     }),
    #     (SMORegion.inverted_pyramid_upper_interior, {
    #         SMORegion.top_of_the_inverted_pyramid: None,
    #     }),
    # ]

#endregion

    # ADD Painting Regions and Connections
    for region in odyssey_regions:
        create_region(self, region)

    for region in world_regions:
        create_region(self, region)

    for region in sub_area_regions:
        create_region(self,region)

    for region in shop_regions:
        create_region(self, region)

    if self.options.regional_coins == self.options.regional_coins.option_groups:
        for region in regional_group_regions:
            create_region(self, region)
    else:
        for region in regional_coin_regions:
            create_region(self, region)

    if self.options.capture_sanity:
        for region in capture_regions:
            create_region(self, region)

    for world, connections in world_connections:
        for key in connections.keys():
            if "Kingdom Shop" in key:
                connect_coin_shops(connections)
                break

    for world, connections in sub_area_connections:
        for key in connections.keys():
            if "Kingdom Shop" in key:
                connect_coin_shops(connections)
                break

    for connection in odyssey_connections:
        connect_region(self, connection)

    for connection in world_connections:
        connect_region(self, connection)

    for connection in sub_area_connections:
        connect_region(self, connection)
        # req_caps = []
        # for key in connection[1]:
        #     if key in capture_items:
        #         req_caps.append(key)
        # if len(req_caps) > 0:
        #     reg = self.get_region(connection[0])
        #     req_caps_str = "["
        #     for cap in req_caps:
        #         req_caps_str += f"SMOItemData.{cap.lower().replace("'", "").replace(" ", "_").replace("-", "_").replace(")", "").replace("(", "")}, "
        #     req_caps_str = req_caps_str[:-2] + "]"
        #     for location in reg.locations:
        #         print(f'set_rule(self.get_location(SMOLocationData.{location.name.lower().replace(" ", "_").replace("-", "").replace("!", " ").replace(":", "")
        #             }), create_access_rule(self, '  + "[\n" + "\t\t\t(SMORuleCondition.CAPTURE, " + f"{req_caps_str}, SMORuleOperation.NONE)" + "\n\t\t\t]))")

    self.world_exits, self.world_sub_area_exits, self.non_dead_end_sub_areas = create_entrances(self)

    # One way sub area entrance: one exit no entrance from world region, one entrance no exit to sub area region
    # One way sub area exit: Exit no Entrance from sub area region, Entrance no Exit into world region
    mismatch = 0
    # if self.options.entrance_randomization.value == self.options.entrance_randomization.option_chaos:
    #     blank_enter, blank_exit = create_two_way_entrance(self.get_region("Menu"), self.get_region(SMORegion.cap_kingdom_intro),
    #                                                       f"EMPTY Entrance", f"EMPTY Exit")
    #
    #
    #
    #     # blank_enter, blank_exit = create_two_way_entrance(self.get_region(SMORegion.cap_kingdom_intro), self.get_region("Menu"),
    #     #                                                   f"EMPTY Exit", f"EMPTY Entrance")
    #     self.sub_area_entrances.append(blank_enter)
    #     self.sub_area_exits.append(blank_exit)
    for data in self.world_exits:
        region, exits = data
        for world_exit in exits.keys():
            is_add: bool = True
            cur_reg : Region = self.get_region(region)
            # if "Kingdom" in region and region != region[:region.index("Kingdom") + 7] and region[:region.index("Kingdom") + 7] in world_regions and "Intro" not in region:
            #     origin_region = self.get_region(region[:region.index("Kingdom") + 7])
            cur_sub_area : Region = self.get_region(alternate_entrances[world_exit] if world_exit in alternate_entrances else world_exit)
            region_entry, region_exit = None, None
            sub_area_entry, sub_area_exit = None, None

            match self.options.entrance_randomization.value:
                case self.options.entrance_randomization.option_chaos:

                    if world_exit in locked_sub_area:
                        is_add = False

                    # Treat every over world sub area door as one two-way entrance

                    region_entry, region_exit, sub_area_entry, sub_area_exit = create_two_way_entrance_pair(cur_reg, cur_sub_area,
                                                                                                            f"{world_exit} Beginning",
                                                                                                            f"{region} {world_exit} Entrance")


                    # if "Darker Side" in world_exit:
                    #     print()
                    if "Rematch" in world_exit:
                        add_override = [False, False, True, True]
                    else:
                        add_override = [True, True, True, True]

                    region_exit.is_exit = True
                    sub_area_exit.is_exit = True

                    add_to_er(self, region_entry, region_exit, sub_area_entry, sub_area_exit, [False, False, False, False] if not is_add else add_override)


                    # Make exception for sub areas with multiple unique entrances to different parts of an over world stage
                    if world_exit in unique_exit_sub_area:
                        cur_reg = self.get_region(unique_exit_sub_area[world_exit])
                        region_entry, region_exit, sub_area_entry, sub_area_exit = create_two_way_entrance_pair(cur_reg, cur_sub_area,
                                                                                                                f"{world_exit} Unique Exit End",
                                                                                                                f"{region} {world_exit} Unique Exit End")
                        # sub_area_entry, sub_area_exit = create_two_way_entrance(cur_sub_area, cur_reg,
                        #                                                         f"{world_exit} Unique Exit End",
                        #                                                         f"{region} {world_exit} Unique Exit End")

                        add_override = [True, True, False, True]

                        region_exit.is_exit = True
                        sub_area_exit.is_exit = True

                        add_to_er(self, region_entry, region_exit, sub_area_entry, sub_area_exit, [False, False, False, False] if not is_add else [True, True, True, True])


                    # Treat every sub area as a pair of two-way entrances
                    #   One for entrance / beginning
                    #   One for exit / ending
                    elif world_exit in self.non_dead_end_sub_areas:
                        # region_entry, region_exit, sub_area_entry, sub_area_exit = create_two_way_entrance_pair(cur_sub_area, cur_reg,
                        #                                                                                         f"{world_exit} Sub Area Exit",
                        #                                                                                       f"{world_exit} Sub Area End")

                        region_entry, region_exit = create_two_way_entrance_rando(cur_sub_area, f"{world_exit} Sub Area End", f"{world_exit} Sub Area End")

                        region_entry.parent_region = cur_reg
                        region_exit.connected_region = cur_reg
                        # region_exit = create_one_way_exit(cur_reg, f"{{}}")
                        # sub_area_exit = create_one_way_exit(cur_sub_area, f"{world_exit} Sub Area Exit", cur_reg, True, False)
                        # sub_area_entry.randomization_type = EntranceType.ONE_WAY
                        # crea
                        # sub_area_entry, sub_area_exit = create_two_way_entrance_rando(cur_sub_area,
                        #                     f"{world_exit} Sub Area Exit Exit",
                        #                     f"{world_exit} Sub Area End")
                        #
                        # sub_area_entry.parent_region = cur_reg
                        # sub_area_exit.connected_region = cur_reg

                        add_override = [True, True, False, False]

                        region_exit.is_exit = True
                        sub_area_exit.is_exit = True

                        add_to_er(self, region_entry, region_exit, None, None, add_override)

                        # region_entry.parent_region = connecting_region
                        # region_exit.connected_region = connecting_region

                        # Rocket sub area access rule
                        if callable(exits[world_exit]):
                            if world_exit in rocket_sub_areas:
                                # print(world_exit)
                                sub_area_entry.access_rule = exits[world_exit]
                                sub_area_exit.access_rule = exits[world_exit]


                    # Add entrance access rule
                    if callable(exits[world_exit]):
                        # print(world_exit)
                        access_rule = exits[world_exit]
                        region_exit.access_rule = exits[world_exit]

                    pass

                # shuffle
                case self.options.entrance_randomization.option_shuffle:
                    region_entry, region_exit = create_two_way_entrance(cur_reg, cur_sub_area, f"{world_exit} Beginning",
                                                                        f"{region} {world_exit} Entrance")

                    if world_exit in locked_sub_area:
                        is_add = False
                    # region_entry, region_exit = create_two_way_entrance_pair(cur_reg, f"{region} {world_exit} Entrance", cur_sub_area)
                    # sub_area_entry, sub_area_exit = create_two_way_entrance_pair(cur_sub_area, f"{world_exit}", cur_reg)

                    if callable(exits[world_exit]):
                        # print(world_exit)
                        access_rule = exits[world_exit]
                        region_exit.access_rule = exits[world_exit]

                    if world_exit in unique_exit_sub_area:
                        cur_reg = self.get_region(unique_exit_sub_area[world_exit])
                        region_entry, region_exit = create_two_way_entrance(cur_reg, cur_sub_area, f"{world_exit} End",
                                                                            f"{region} {world_exit} End")

                    if add_to_er:
                        if region_entry:
                            self.sub_area_entrances.append(region_entry)
                        if region_exit:
                            self.sub_area_exits.append(region_exit)
                        if sub_area_entry:
                            self.sub_area_entrances.append(sub_area_entry)
                        if sub_area_exit:
                            self.sub_area_exits.append(sub_area_exit)


                    if world_exit not in one_way_enter_sub_area and world_exit not in one_way_exit_sub_area and world_exit in self.non_dead_end_sub_areas:
                        self.valid_top_hat_replacements.append(world_exit if world_exit not in alternate_entrances else alternate_entrances[world_exit])

                case self.options.entrance_randomization.option_off:
                    # Treat every sub area as a single two-way entrance to a dead end.
                    # Except ones that have multiple unique entrances to different parts of an over world stage

                    region_entry, region_exit = create_two_way_entrance(cur_reg, cur_sub_area, f"{world_exit} Beginning",
                                                                        f"{region} {world_exit} Entrance")


                    if callable(exits[world_exit]):
                        # print(world_exit)
                        access_rule = exits[world_exit]
                        region_exit.access_rule = exits[world_exit]


                    if world_exit in unique_exit_sub_area:
                        cur_reg = self.get_region(unique_exit_sub_area[world_exit])
                        region_entry, region_exit = create_two_way_entrance(cur_reg, cur_sub_area, f"{world_exit} Unique Exit End",
                                                                            f"{region} {world_exit} Unique Exit End")
                        #print("test")


def create_locations(region: Region, *locations: str, location_table = locations_table):
    """
    :param region: The Region to add locations too
    :param locations: locations
    :param location_table: name to id dict of world locations
    :return: None
    """
    region.locations += ([SMOLocation(region.player, location_name, location_table[location_name], region) for location_name in locations])

# Cannot go back through entrance or sub area cannot be done in reverse
one_way_enter_sub_area = [
    SMOEntranceData.spinning_platforms_treasure_vault,
    #SMOEntranceData.underground_ruins,
    #SMOEntranceData.ice_cave,
    SMOEntranceData.inverted_pyramid_upper_interior,
    SMOEntranceData.darker_side_main,
    SMOEntranceData.darker_side_pokio,
    SMOEntranceData.darker_side_bowser,
    SMOEntranceData.darker_side_end,
    SMOEntranceData.secret_flower_field,
    # SMOEntranceData.knucklotec_rematch,
    # SMOEntranceData.torkdrift_rematch,
    # SMOEntranceData.mecha_wiggler_rematch,
    # SMOEntranceData.mollusque_lanceur_rematch,
    # SMOEntranceData.cookatiel_rematch,
    # SMOEntranceData.lord_of_lightning_rematch,
    SMOEntranceData.deepest_underground_shortcut,
    SMOEntranceData.moe_eye_invisible_floor,
    SMOEntranceData.t_rex_escape,
    # SMOEntranceData.knucklotec_rematch,
    # SMOEntranceData.torkdrift_rematch,
    # SMOEntranceData.mecha_wiggler_rematch,
    # SMOEntranceData.mollusque_lanceur_rematch,
    # SMOEntranceData.cookatiel_rematch,
    # SMOEntranceData.lord_of_lightning_rematch,

]

# The world entrance this connects to is normally one way
one_way_exit_sub_area = [
    # SMOEntranceData.darker_side_main,
    # SMOEntranceData.darker_side_pokio,
    # SMOEntranceData.darker_side_bowser,
    # SMOEntranceData.darker_side_end,
    SMOEntranceData.ice_cave,
    SMOEntranceData.inverted_pyramid_mural,
    #SMOEntranceData.darker_side_main,
    SMOEntranceData.darker_side_pokio,
    SMOEntranceData.darker_side_bowser,
    SMOEntranceData.darker_side_end,
    #SMOEntranceData.secret_flower_field,

    SMOEntranceData.deepest_underground_shortcut,
    #SMOEntranceData.bullet_bill_maze,
    SMOEntranceData.deep_woods_2,
    SMOEntranceData.deep_woods_4,
]

locked_sub_area = [
    SMOEntranceData.inside_the_church,
    # SMOEntranceData.top_hat_tower,
    # SMOEntranceData.ty_foo_sliding_puzzle, # To prevent hanging entrance during randomization, randomize/shuffle only two dead ends to prevent this...
    # SMOEntranceData.deepest_underground_shortcut
    ]

unique_exit_sub_area = {
    SMOEntranceData.top_hat_tower: SMORegion.cap_kingdom_topper,
    SMOEntranceData.inverted_pyramid_lower_interior: SMORegion.sand_kingdom,
    # SMOEntranceData.inverted_pyramid_mural: SMORegion.inverted_pyramid_upper_interior,
    SMOEntranceData.inverted_pyramid_upper_interior: SMORegion.top_of_the_inverted_pyramid,
    # SMOEntranceData.deepest_underground_shortcut: SMORegion.sand_kingdom,
    SMOEntranceData.bullet_bill_maze: SMORegion.sand_kingdom,
    SMOEntranceData.sky_garden_tower: SMORegion.wooded_kingdom,
    SMOEntranceData.underwater_tunnel: SMORegion.seaside_kingdom,
    #SMOEntranceData.secret_flower_field: SMORegion.wooded_kingdom,
    SMOEntranceData.ice_cave: SMORegion.sand_kingdom,
    SMOEntranceData.moon_cave: SMORegion.moon_kingdom,
    # SMOEntranceData.painting_room_knucklotec: SMORegion.knucklotec_rematch,
    # SMOEntranceData.painting_room_torkdrift: SMORegion.torkdrift_rematch,
    # SMOEntranceData.painting_room_mecha_wiggler: SMORegion.mecha_wiggler_rematch,
    # SMOEntranceData.painting_room_mollusque_lanceur: SMORegion.mollosque_lanceur_rematch,
    # SMOEntranceData.painting_room_cookatiel: SMORegion.cookatiel_rematch,
    # SMOEntranceData.painting_room_lord_of_lightning: SMORegion.lord_of_lightning_rematch,
    SMOEntranceData.dark_side_topper: SMORegion.dark_side_2,
    SMOEntranceData.dark_side_hariet: SMORegion.dark_side_3,
    SMOEntranceData.dark_side_spewart: SMORegion.dark_side_4,
    SMOEntranceData.dark_side_rango: SMORegion.dark_side_5,
    SMOEntranceData.darker_side_main: SMORegion.darker_side_tower,
    # SMOEntranceData.darker_side_pokio: SMORegion.darker_side_entrance,
    # SMOEntranceData.darker_side_bowser: SMORegion.darker_side_entrance,
    SMOEntranceData.darker_side_end: SMORegion.darker_side_entrance,


}
