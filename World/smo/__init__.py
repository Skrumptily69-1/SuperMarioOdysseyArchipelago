import random
from math import floor
from typing import Mapping, Any, TextIO

from schema import Optional

from .Data.EntranceData import SMOEntranceData
from .Data.RegionData import SMORegion
from .Data.ItemData import SMOItemData
from .Data.RuleData import kingdom_name_to_id, SMOKingdoms
from .Options import SMOOptions
from .Items import item_table, SMOItem, filler_item_table, outfits, shop_items, \
    moon_item_table, moon_types, stickers, souvenirs, capture_items, \
    location_hint_list, regional_coin_types, difficulty_items, option_value_to_trick_item, option_value_to_glitch_item, \
    abilities
from .Locations import locations_table, SMOLocation, locations_list, post_game_locations_list, \
    special_locations_table, full_moon_locations_list, story_moons, multi_moons, goals_table, regional_coin_table, \
    regional_coin_groups, regional_coins, regional_coin_groups_table, regional_sub_area_to_kingdom, shop_location_costs, \
    coin_shop_locations_table, regional_shop_locations_table, TextDataOffset, loc_Captures
from .Regions import create_regions
from .Entrances import display_name_to_internal_name, display_name_alias, stage_id_to_name, SMORandomizationGroup, \
    internal_name_to_entrance, stage_names, stage_ids, get_entrance_pair, get_stage_ids, SMOEntrance, \
    get_randomization_group
from BaseClasses import Item, ItemClassification, Entrance, Region, EntranceType, MultiWorld
from worlds.AutoWorld import World
from worlds.LauncherComponents import (Component, components, Type as component_type, SuffixIdentifier, launch as launch_component)
from .Rules import set_rules
from entrance_rando import ERPlacementState, randomize_entrances, disconnect_entrance_for_randomization


def launch_client(*args: str):
    from .Connector.Client import launch
    # print(len(args))
    launch_component(launch, name="SMOClient", args=args)

component = Component("Super Mario Odyssey Client", component_type=component_type.CLIENT,
                      game_name="Super Mario Odyssey", func=launch_client)
components.append(component)

class SMOWorld(World):
    """Super Mario Odyssey is a 3-D Platformer where Mario sets off across the world with his companion Cappy to save Princess Peach and Cappy's sister Tiara from Bowser's wedding plans."""
    game = "Super Mario Odyssey"

    #settings_key = "smo_settings"
    #settings : SMOSettings

    options_dataclass = SMOOptions
    options: SMOOptions

    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    # instead of dynamic numbering, IDs could be part of data
    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {**item_table, **moon_types, **regional_coin_types, **{f"{amount} Coins" : 9999 for amount in range(50,1000)}}

    location_name_to_id = locations_table
    # Number of Power Moons required to leave each kingdom
    default_moon_counts = {
        SMOKingdoms.CASCADE: 5,
        SMOKingdoms.SAND: 16,
        SMOKingdoms.LAKE: 8,
        SMOKingdoms.WOODED: 16,
        SMOKingdoms.LOST: 10,
        SMOKingdoms.METRO: 20,
        SMOKingdoms.SNOW: 10,
        SMOKingdoms.SEASIDE: 10,
        SMOKingdoms.LUNCHEON: 18,
        SMOKingdoms.RUINED: 3,
        SMOKingdoms.BOWSER: 8,
        SMOKingdoms.DARK: 250,
        SMOKingdoms.DARKER: 500
    }

    default_regional_counts = {
        SMOKingdoms.CAP: 50,
        SMOKingdoms.CASCADE: 50,
        SMOKingdoms.SAND: 100,
        SMOKingdoms.LAKE: 50,
        SMOKingdoms.WOODED: 100,
        SMOKingdoms.LOST: 50,
        SMOKingdoms.METRO: 100,
        SMOKingdoms.SNOW: 50,
        SMOKingdoms.SEASIDE: 100,
        SMOKingdoms.LUNCHEON: 100,
        SMOKingdoms.BOWSER: 100,
        SMOKingdoms.MOON: 50,
        SMOKingdoms.MUSHROOM: 100,
    }

    # Number of Power Moons required to unlock post game outfits.
    outfit_moon_counts = {
        SMOItemData.luigi_cap : 160,
        SMOItemData.luigi_suit : 180,
        "Doctor Headwear" : 220,
        "Doctor Outfit" : 240,
        "Waluigi Cap" : 260,
        "Waluigi Suit" : 280,
        "Diddy Kong Hat" : 300,
        "Diddy Kong Suit" : 320,
        "Wario Cap" : 340,
        "Wario Suit" : 360,
        "Hakama" : 380,
        "Bowser's Top Hat" : 420,
        "Bowser's Tuxedo" : 440,
        "Bridal Veil" : 460,
        "Bridal Gown" : 480,
        "Gold Mario Cap" : 500,
        "Gold Mario Suit" : 500,
        "Metal Mario Cap" : 500,
        "Metal Mario Suit" : 500
    }

    # Maximum number of Power Moons for any given kingdom's progression
    max_counts = {
        SMOKingdoms.CASCADE: 19,
        SMOKingdoms.SAND: 65,
        SMOKingdoms.LAKE: 28,
        SMOKingdoms.WOODED: 53,
        SMOKingdoms.LOST: 20,
        SMOKingdoms.METRO: 57,
        SMOKingdoms.SNOW: 35,
        SMOKingdoms.SEASIDE: 51,
        SMOKingdoms.LUNCHEON: 53,
        SMOKingdoms.RUINED: 6,
        SMOKingdoms.BOWSER: 40,
        SMOKingdoms.MUSHROOM: 43, # Needs recount
        SMOKingdoms.DARK: 375,
        SMOKingdoms.DARKER: 750
    }
    # Number of Power Moon checks in each kingdom
    max_checks = {
        SMOKingdoms.CAP: 31,
        SMOKingdoms.CASCADE: 42,
        SMOKingdoms.SAND: 93,
        SMOKingdoms.LAKE: 44,
        SMOKingdoms.WOODED: 80,
        SMOKingdoms.CLOUD: 9,
        SMOKingdoms.LOST: 35,
        SMOKingdoms.METRO: 85,
        SMOKingdoms.SNOW: 57,
        SMOKingdoms.SEASIDE: 73,
        SMOKingdoms.LUNCHEON: 72,
        SMOKingdoms.RUINED: 12,
        SMOKingdoms.BOWSER: 64,
        SMOKingdoms.MOON: 38,
        SMOKingdoms.MUSHROOM: 55,
        SMOKingdoms.DARK: 26,
        SMOKingdoms.DARKER: 3
    }

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "Cap Moons": {SMOItemData.cap_power_moon},
        "Cascade Moons": {SMOItemData.cascade_power_moon, SMOItemData.cascade_story_moon, SMOItemData.cascade_multi_moon},
        "Sand Moons": {SMOItemData.sand_power_moon, SMOItemData.sand_story_moon, SMOItemData.sand_multi_moon},
        "Lake Moons": {SMOItemData.lake_power_moon, SMOItemData.lake_multi_moon},
        "Wooded Moons": {SMOItemData.wooded_power_moon, SMOItemData.wooded_story_moon, SMOItemData.wooded_multi_moon},
        "Cloud Moons": {SMOItemData.cloud_power_moon},
        "Lost Moons": {SMOItemData.lost_power_moon},
        "Metro Moons": {SMOItemData.metro_power_moon, SMOItemData.metro_story_moon, SMOItemData.metro_multi_moon},
        "Snow Moons": {SMOItemData.snow_power_moon, SMOItemData.snow_story_moon, SMOItemData.snow_multi_moon},
        "Seaside Moons": {SMOItemData.seaside_power_moon, SMOItemData.seaside_story_moon, SMOItemData.seaside_multi_moon},
        "Luncheon Moons": {SMOItemData.luncheon_power_moon, SMOItemData.luncheon_story_moon, SMOItemData.luncheon_multi_moon},
        "Ruined Moons": {SMOItemData.ruined_power_moon, SMOItemData.ruined_multi_moon},
        "Bowser Moons": {SMOItemData.bowser_power_moon, SMOItemData.bowser_story_moon, SMOItemData.bowser_multi_moon},
        "Moon Moons": {SMOItemData.moon_power_moon},
        "Mushroom Moons": {SMOItemData.power_star, SMOItemData.mushroom_multi_moon},
        "Dark Moons": {SMOItemData.dark_side_power_moon, SMOItemData.dark_side_multi_moon},
        "Darker Moons": {SMOItemData.darker_side_multi_moon},
        "Cappy": {SMOItemData.cap_throw, SMOItemData.up_throw, SMOItemData.down_throw, SMOItemData.spin_throw}
    }



    def __init__(self, multiworld: "MultiWorld", player: int):
        # Number of Power Moons required to leave each kingdom
        self.moon_counts = {
            SMOKingdoms.CASCADE: 5,
            SMOKingdoms.SAND: 16,
            SMOKingdoms.LAKE: 8,
            SMOKingdoms.WOODED: 16,
            SMOKingdoms.LOST: 10,
            SMOKingdoms.METRO: 20,
            SMOKingdoms.SNOW: 10,
            SMOKingdoms.SEASIDE: 10,
            SMOKingdoms.LUNCHEON: 18,
            SMOKingdoms.RUINED: 3,
            SMOKingdoms.BOWSER: 8,
            SMOKingdoms.MUSHROOM: 0,
            SMOKingdoms.DARK: 250,
            SMOKingdoms.DARKER: 500
        }
        # Number of moons placed for each kingdom
        self.placement_counts = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]

        # Number of regionals required for each kingdom in progression
        self.needed_regionals = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]
        # list of item names for shine locations by hint list index
        self.shine_items: dict[int, list[str]] = {}
        # list of slot names for shine locations by hint list index
        self.shine_slots: dict[int, list[str]] = {}
        # look up data to replace shine names in game
        self.shine_replace_data = {}
        # shine id to color change
        self.shine_colors: dict[int, int] = {}
        self.color_list: list[int] = []
        # Shop Shine Game Name Replacements
        self.shine_games: list[str] = []
        # Shop Item Game Name Replacements
        self.shop_games: list[str] = []
        self.shop_players: list[str] = []
        self.shop_ap_items: list[str] = []
        self.regional_shop_games: list[str] = []
        self.regional_shop_players: list[str] = []
        self.regional_shop_ap_items: list[str] = []
        self.shop_replace_data = {}
        # The value of a coin item by location
        self.coin_values = {}
        # Dict of location_id -> (item_name, player_name) for non-local items
        self.text_less_locations = {}
        self.world_exits: list[tuple[str, dict]] = []
        self.world_sub_area_exits = []
        self.non_dead_end_sub_areas = []
        # Sub Area Entrances allowed for randomization
        self.sub_area_entrances: list[Entrance] = []
        # Sub area Exits allowed for randomization.
        self.sub_area_exits: list[Entrance] = []
        self.valid_top_hat_replacements: list[str] = []
        self.top_hat_tower_bind: str = ""
        self.randomized_entrances: ERPlacementState = None
        self.original_entrance_bindings : dict[str, str] = {}
        self.original_exit_bindings : dict[str, str] = {}
        self.entrance_data: dict[str, dict[int, tuple[int, int, bool]]] = { "over_world": {}, "sub_area": {}}
        super().__init__(multiworld, player)


    def generate_early(self):
        pass
        # self.multiworld.early_items[self.player]["Cascade Multi-Moon"] = 1
        # self.multiworld.early_items[self.player]["Cascade Story Moon"] = 1
        # self.multiworld.early_items[self.player]["Cascade Power Moon"] = self.moon_counts[SMOKingdoms.CASCADE]-4
        # if self.options.capture_sanity.value == self.options.capture_sanity.option_true:
        #     self.multiworld.early_items[self.player]["Broode's Chain Chomp"] = 1
        #     self.multiworld.early_items[self.player]["Chain Chomp"] = 1
        #     self.multiworld.early_items[self.player]["T-Rex"] = 1

    def create_regions(self):
        if self.options.counts > 0:
            self.randomize_moon_amounts()

        create_regions(self)

        # if self.options.entrance_randomization.value > self.options.entrance_randomization.option_off:
            # sub_area_index = random.randint(0, len(self.valid_top_hat_replacements) - 1)
            # self.top_hat_tower_bind = self.valid_top_hat_replacements[sub_area_index]
            # print(self.top_hat_tower_bind)

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        classification: ItemClassification = ItemClassification.filler
        if name in filler_item_table.keys():
            classification = ItemClassification.filler
        else:
            if name == "Beat the Game" and self.options.goal == self.options.goal.option_moon:
                classification = ItemClassification.progression_skip_balancing
            elif name in outfits:
                if outfits.index(name) <= 33:
                    classification = ItemClassification.progression_skip_balancing
            elif name in shop_items:
                # Until achievements implemented if possible
                # some outfits for dark and darker goals not handled correctly
                classification = ItemClassification.filler
            elif name in capture_items:
                if self.options.goal < self.options.goal.option_dark and capture_items.index(name) >= 48 and self.options.entrance_randomization == 0:
                    classification = ItemClassification.filler
                else:
                    classification = ItemClassification.progression
            elif name in moon_types:
                kingdom = name.replace(" Power Moon", "").replace(" Multi-Moon", "").replace(" Story Moon", "")
                index = kingdom_name_to_id[kingdom]
                self.placement_counts[index] += 1
                if self.placement_counts[index] <= self.moon_counts[kingdom]:
                    classification = ItemClassification.progression
                else:
                    classification = ItemClassification.useful

            elif name in regional_coin_types:
                classification = ItemClassification.progression

            elif name in abilities:
                classification = ItemClassification.progression

        item: SMOItem

        # if classification == ItemClassification.progression_skip_balancing and name in self.item_name_groups["Cascade"]:
        #     print(name)
        item = SMOItem(name, classification, self.player, item_id)
        return item

    def create_items(self):
        pool : list = []

        # Additively build pool
        #region Moons
        locations: list = []
        for location in self.get_locations():
            if location.name in [*outfits, *shop_items, *capture_items]:
                continue
            else:
                locations += [location.name]
        #print(locations)


        revised_counts = [
            0,
            min(floor(self.moon_counts[SMOKingdoms.CASCADE] * self.options.extra_moons.value / 100.0),
                self.max_counts[SMOKingdoms.CASCADE]),
            min(floor(self.moon_counts[SMOKingdoms.SAND] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.SAND]),
            min(floor(self.moon_counts[SMOKingdoms.WOODED] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.WOODED]),
            min(floor(self.moon_counts[SMOKingdoms.LAKE] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.LAKE]),
            0,
            min(floor(self.moon_counts[SMOKingdoms.LOST] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.LOST]),
            min(floor(self.moon_counts[SMOKingdoms.METRO] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.METRO]),
            min(floor(self.moon_counts[SMOKingdoms.SEASIDE] * self.options.extra_moons.value / 100.0),
                self.max_counts[SMOKingdoms.SEASIDE]),
            min(floor(self.moon_counts[SMOKingdoms.SNOW] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.SNOW]),
            min(floor(self.moon_counts[SMOKingdoms.LUNCHEON] * self.options.extra_moons.value / 100.0),
                self.max_counts[SMOKingdoms.LUNCHEON]),
            min(floor(self.moon_counts[SMOKingdoms.RUINED] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.RUINED]),
            min(floor(self.moon_counts[SMOKingdoms.BOWSER] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.BOWSER]),
            0,
            0,
            0,
            0,
        ]

        # revised_counts = [
        #     0,
        #     min(floor(self.moon_counts[SMOKingdoms.CASCADE] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.CASCADE]),
        #     min(floor(self.moon_counts[SMOKingdoms.SAND] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.SAND]),
        #     min(floor(self.moon_counts[SMOKingdoms.WOODED] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.WOODED]),
        #     min(floor(self.moon_counts[SMOKingdoms.LAKE] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.LAKE]),
        #     0,
        #     min(floor(self.moon_counts[SMOKingdoms.LOST] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.LOST]),
        #     min(floor(self.moon_counts[SMOKingdoms.METRO] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.METRO]),
        #     min(floor(self.moon_counts[SMOKingdoms.SEASIDE] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.SEASIDE]),
        #     min(floor(self.moon_counts[SMOKingdoms.SNOW] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.SNOW]),
        #     min(floor(self.moon_counts[SMOKingdoms.LUNCHEON] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.LUNCHEON]),
        #     min(floor(self.moon_counts[SMOKingdoms.RUINED] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.RUINED]),
        #     min(floor(self.moon_counts[SMOKingdoms.BOWSER] * self.options.extra_moons.value / 100.0), self.max_counts[SMOKingdoms.BOWSER]),
        #     0,
        #     0,
        #     0,
        #     0,
        # ]
        if self.options.goal == self.options.goal.option_dark:
            kingdoms : list = list(range(15))
            while sum(revised_counts[0:15]) < self.moon_counts[SMOKingdoms.DARK]:
                index = kingdoms[random.randint(0, len(kingdoms) - 1)]
                revised_counts[index] += 1
                if revised_counts[index] == self.max_checks[kingdom_name_to_id[index].lower()]:
                    kingdoms.remove(index)
        elif self.options.goal == self.options.goal.option_darker:
            kingdoms: list = list(range(16))
            while sum(revised_counts[0:16]) < self.moon_counts[SMOKingdoms.DARKER]:
                index = kingdoms[random.randint(0, len(kingdoms) - 1)]
                revised_counts[index] += 1
                if revised_counts[index] == self.max_checks[kingdom_name_to_id[index].lower()]:
                    kingdoms.remove(index)

        for kingdom in story_moons.keys():
            for i in range(len(story_moons[kingdom])):
                if story_moons[kingdom][i] in locations:
                    pool.append(f"{kingdom} Story Moon")
                    self.placement_counts[kingdom_name_to_id[kingdom]] += 1
                    self.placement_counts[15] += 1
                    self.placement_counts[16] += 1
        for kingdom in multi_moons.keys():
            for i in range(len(multi_moons[kingdom])):
                if multi_moons[kingdom][i] in locations:
                    pool.append(f"{kingdom} Multi-Moon")
                    self.placement_counts[kingdom_name_to_id[kingdom]] += 3
                    self.placement_counts[15] += 3
                    self.placement_counts[16] += 3

        for kingdom in kingdom_name_to_id:
            index = kingdom_name_to_id[kingdom]
            while self.placement_counts[index] < revised_counts[index]:
                pool.append(f"{kingdom} Power Moon")
                self.placement_counts[index] += 1
                self.placement_counts[15] += 1
                self.placement_counts[16] += 1


        # for location in locations:
        #     # found : bool = False
        #     for index in range(len(kingdom_name_to_id)):
        #         if location in full_moon_locations_list[index]:
        #             item = ""
        #             if (placement_counts[index] < revised_counts[index]
        #                 or (kingdom_name_to_id[index] in story_moons and location in story_moons[kingdom_name_to_id[index]])
        #                 or (index < 14 and kingdom_name_to_id[index] in multi_moons and location in multi_moons[kingdom_name_to_id[index]])):
        #                 # found = True
        #                 item: str = kingdom_name_to_id[index]
        #                 place : bool = False
        #
        #                 if "Dark" in item:
        #                     item += " Side"
        #                 # Multi
        #                 if kingdom_name_to_id[index] in multi_moons and location in multi_moons[kingdom_name_to_id[index]]:
        #                     item += " Multi-Moon"
        #                     # Prevent placement of duplicate goal Multi-Moon
        #                     if location == goals_table[self.options.goal.value]:
        #                         break
        #                     place = not self.options.story >= 2
        #                 elif kingdom_name_to_id[index] in story_moons and location in story_moons[kingdom_name_to_id[index]]:
        #                     item += " Story Moon"
        #                     place = not (self.options.story == 1 or self.options.story == 3)
        #                 else:
        #                     if kingdom_name_to_id[index] == "Mushroom":
        #                         item = "Power Star"
        #                     else:
        #                         item += " Power Moon"
        #
        #                 placement_counts[index] += 3 if "Multi" in item else 1
        #
        #                 if place:
        #                     self.get_location(location).place_locked_item(self.create_item(item))
        #                     break
        #             else:
        #                 pass
        #                 #print(location)
        #             if item != "":
        #                 if "Snow" in item:
        #                     pass
        #                     #print (item)
        #                 pool.append(item)
        #             break
        #     # if not found:
        #     #     print(location)
        for kingdom in kingdom_name_to_id:
            index = kingdom_name_to_id[kingdom]
            moon_item = f"{kingdom} Power Moon"
            while self.placement_counts[index] > revised_counts[index]:
                if moon_item in pool:
                    pool.remove(moon_item)
                    self.placement_counts[index] -= 1
                else:
                    break
            self.placement_counts[index] = 0

        #endregion Moons

        for item in self.multiworld.early_items[self.player]:
            while item in pool:
                pool.remove(item)

        locations : list = []

        for location in self.get_locations():
            if location.name in outfits or location.name in shop_items:
                locations += [location.name]

        #region Shops
        item_names : list = []
        # Outfits
        for location in outfits:
            if location in locations:
                if self.options.shop_sanity == "outfits" or self.options.shop_sanity == "all":
                    pool.append(location)
                elif self.options.shop_sanity == "shuffle":
                    item_names.append(location)
                else:
                    self.get_location(location).place_locked_item(self.create_item(location))

        # Souvenirs and stickers
        for location in shop_items:
            if location in locations:
                if self.options.shop_sanity == "non_outfits" or self.options.shop_sanity == "all":
                    pool.append(location)
                else:
                    self.get_location(location).place_locked_item(self.create_item(location))

        # Shop sanity shuffle
        if self.options.shop_sanity == "shuffle":
            while len(item_names) > 0:
                item = item_names.pop(random.randint(0, len(item_names) - 1))
                self.get_location(item).place_locked_item(self.create_item(item))

        #endregion Shops

        #region Captures
        locations: list = []
        for location in self.get_locations():
            if location.name in capture_items and not location.item:
                locations += [location.name]
            # else:
            #      print(location.name)

        for location in locations:
            if self.options.capture_sanity.value == self.options.capture_sanity.option_true:
                if location in capture_items and not location in self.multiworld.early_items[self.player]:
                    pool.append(location)
            else:
                # Push all captures into inventory when disabled
                self.push_precollected(self.create_item(location))

        #endregion Captures

        #region Regional Coins
        locations: list = []
        for location in self.get_locations():
            if (location.name in regional_coin_table or location.name in regional_coin_groups_table) and not location.item:
                locations += [location]

        for location in locations:
            kingdom = ""
            if "Kingdom" in location.name:
                kingdom = location.name.replace("'", "").split()[0].lower()
            else:
                for place in regional_sub_area_to_kingdom:
                    if location.parent_region.name in regional_sub_area_to_kingdom[place]:
                        kingdom = place.lower()
                        break
            match self.options.regional_coins.value:
                case self.options.regional_coins.option_groups:
                    pool.append(getattr(SMOItemData, f"{kingdom}_kingdom_regional_group"))

                case self.options.regional_coins.option_individual:
                    pool.append(getattr(SMOItemData, f"{kingdom}_kingdom_regional_coin"))

                case self.options.regional_coins.option_off:
                    location.place_locked_item(self.create_item(getattr(SMOItemData, f"{kingdom}_kingdom_regional_coin")))

        #endregion Regional Coins

        #region Abilities

        for ability in abilities:
            if self.options.ability_sanity.value == self.options.ability_sanity.option_true:
                if ability not in [SMOItemData.jump, SMOItemData.cap_throw]:
                    pool.append(ability)
                else:
                    self.push_precollected(self.create_item(ability))
            else:
                # Push all captures into inventory when disabled
                self.push_precollected(self.create_item(ability))
        #endregion Abilities

        for difficulty in range(self.options.trick_logic.value):
            self.push_precollected(self.create_item(option_value_to_trick_item[difficulty]))
        for difficulty in range(self.options.glitch_logic.value):
            self.push_precollected(self.create_item(option_value_to_glitch_item[difficulty]))

        # Remove start_inventory items from pool
        for start_item in self.options.start_inventory:
            for num in range(self.options.start_inventory[start_item]):
                pool.remove(start_item)

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        pool += [self.get_filler_item_name() for _ in range(total_locations - len(pool))]
        #print(len(pool), needed_items)


        for i in pool:
            self.multiworld.itempool += [self.create_item(i)]

    def set_rules(self):
        set_rules(self, self.options)

    def connect_entrances(self) -> None:
        def get_coupled_entrance(source_region, source_exit_name: str) -> Entrance | None:
            for reverse_entrance in source_region.entrances:
                if reverse_entrance.name == source_exit_name:
                    return reverse_entrance
            else:
                return None

        def get_coupled_exit(target_region: Region, target_entrance_name: str) -> Entrance | None:
            for reverse_exit in target_region.exits:
                if reverse_exit.name == target_entrance_name:
                    return reverse_exit
            else:
                return None

        def on_connect(state: ERPlacementState, placed_exits: list[SMOEntrance], placed_entrances: list[SMOEntrance]) -> bool:
            """
            Use this to connect over world sub area end to the same placement as its enter counterpart and vise versa
            Return True when a placement is made so generator performs another sweep
            """
            has_placed: bool = False
            for _exit in placed_exits:
                # if "Sub Area Exit" in
                pass

            for _entrance in placed_entrances:
                if isinstance(_entrance, SMOEntrance):
                    if not _entrance.is_sub_area and not _entrance.has_alternate_entrance:
                        if _entrance.paired_entrance != "":
                            other_exit = self.get_entrance(_entrance.paired_entrance)

                            if other_exit:
                                other_exit.parent_region = _entrance.connected_region
                                if state.coupled and other_exit.randomization_type == EntranceType.TWO_WAY:
                                    coupled_exit = get_coupled_exit(other_exit.connected_region, other_exit.name)
                                    if coupled_exit:
                                        coupled_exit.connected_region = _entrance.connected_region
                                has_placed = True

            return has_placed

            # SOMEWHERE in reassigning of top hat, exits and entrances become unequal
        if self.options.entrance_randomization > 0:

            # intro = self.get_region(SMORegion.cap_kingdom_intro)
            # topper = self.get_region(SMORegion.cap_kingdom_topper)
            # bind_region = self.get_region(self.top_hat_tower_bind)
            # top_hat = self.get_region(SMORegion.top_hat_tower)

            # if len(self.sub_area_entrances) != len(self.sub_area_exits):
            #    raise Exception("Mismatch. ", f"Entrances: {len(self.sub_area_entrances)} Exits: {len(self.sub_area_exits)}")

            added_entrances = []
            for entrance in self.sub_area_entrances:
                if entrance.name in self.original_entrance_bindings:
                    raise "Duplicate entrance name"
                self.original_entrance_bindings[entrance.name] = entrance.parent_region.name if entrance.parent_region else "None"
                randomization_group = get_randomization_group(entrance)
                if entrance.randomization_type == EntranceType.ONE_WAY:
                    disconnect_entrance_for_randomization(entrance, randomization_group,
                                                          f"{entrance.name}")
                    if entrance not in self.get_entrances():
                        raise Exception(f"Attempted to disconnect entrance '{entrance.name}' not in entrance cache")
                    pass
                else:
                    entrance.randomization_group = randomization_group
                    # if " Entrance" in entrance.name and entrance.parent_region == bind_region:
                    #     disconnect_entrance_for_randomization(entrance,  SMORandomizationGroup.TOP_HAT_ENTER)
                    #
                    # elif " End" in entrance.name and entrance.parent_region == bind_region:
                    #     disconnect_entrance_for_randomization(entrance,  SMORandomizationGroup.TOP_HAT_ENTER)
                    #
                    #
                    # elif entrance.parent_region == intro:
                    #     disconnect_entrance_for_randomization(entrance, SMORandomizationGroup.TOP_HAT_EXIT)
                    #
                    # elif entrance.parent_region == topper:
                    #     disconnect_entrance_for_randomization(entrance, SMORandomizationGroup.TOP_HAT_EXIT)
                    #
                    # else:
                    entrance.parent_region = None
                    if entrance.connected_region:
                        # disconnect_entrance_for_randomization(entrance, SMORandomizationGroup.DOOR)
                        # for added_target in entrance.parent_region.entrances:
                        #     if added_target.name == entrance.name:
                        #         added_entrances.append(added_target)
                        pass


            # for entrance in added_entrances:
            #     self.sub_area_entrances.append(entrance)

            for possible_exit in self.sub_area_exits:
                if possible_exit.name in self.original_exit_bindings:
                    raise "Duplicate entrance name"
                self.original_exit_bindings[possible_exit.name] = possible_exit.connected_region.name

                # if f"{self.top_hat_tower_bind} Entrance" in possible_exit.name and possible_exit.parent_region == bind_region:
                #     possible_exit.randomization_group = SMORandomizationGroup.TOP_HAT_EXIT
                #
                # elif f"{self.top_hat_tower_bind} End" in possible_exit.name and possible_exit.parent_region == bind_region :
                #     possible_exit.randomization_group = SMORandomizationGroup.TOP_HAT_EXIT
                #
                # elif possible_exit.parent_region == intro:
                #     possible_exit.randomization_group = SMORandomizationGroup.TOP_HAT_ENTER
                #
                # elif possible_exit.parent_region == topper:
                #     possible_exit.randomization_group = SMORandomizationGroup.TOP_HAT_ENTER

                possible_exit.connected_region = None
                pass

            no_target_group = {
                SMORandomizationGroup.DOOR: [SMORandomizationGroup.DOOR, SMORandomizationGroup.PIPE, SMORandomizationGroup.SAND_SHOP_SUB_AREA, SMORandomizationGroup.SAND_EMPLOYEE_SUB_AREA],
                SMORandomizationGroup.SAND_SHOP_SUB_AREA: [SMORandomizationGroup.DOOR, SMORandomizationGroup.PIPE],
                SMORandomizationGroup.SAND_EMPLOYEE_SUB_AREA: [SMORandomizationGroup.DOOR, SMORandomizationGroup.PIPE],
                SMORandomizationGroup.TOP_HAT_ENTER: [SMORandomizationGroup.TOP_HAT_EXIT],
                SMORandomizationGroup.TOP_HAT_EXIT: [SMORandomizationGroup.TOP_HAT_ENTER],
                # SMORandomizationGroup.TOP_HAT_SUB_AREA_ENTER: [SMORandomizationGroup.TOP_HAT_ENTER],
                # SMORandomizationGroup.TOP_HAT_SUB_AREA_EXIT: [SMORandomizationGroup.TOP_HAT_EXIT],
            }
            # print(f"Entrances: {len(self.sub_area_entrances)}, Exits: {len(self.sub_area_exits)}")
            self.randomized_entrances = randomize_entrances(self, coupled=True, target_group_lookup=no_target_group,
                                                            exits=self.sub_area_exits, er_targets=self.sub_area_entrances)
            #print(self.randomized_entrances.entrance_lookup)

            from Utils import visualize_regions
            visualize_regions(self.get_region("Menu"), "smo_er.puml")

        # Finish Regional Coin Rules in Rules.py
        # Fix some exits not having a corresponding entrance

    def get_filler_item_name(self) -> str:
        # Add more Filler Item Types
        return "Coins"

    def generate_basic(self) -> None:
        pass

    def randomize_moon_amounts(self):
        """ Randomizes the moon requirements for progressing to each kingdom."""
        if self.options.counts == 1:
            for key in self.moon_counts.keys():
                if key != SMOKingdoms.DARK and key != SMOKingdoms.DARKER:
                    self.moon_counts[key] = 1
            kingdoms = list(self.moon_counts.keys())
            kingdoms.remove(SMOKingdoms.DARK)
            kingdoms.remove(SMOKingdoms.DARKER)
            count = 0
            for kingdom in kingdoms:
                count += self.moon_counts[kingdom]
            while count != 124 and len(kingdoms) > 0:
                selected = kingdoms[random.randint(0, len(kingdoms)-1)]
                self.moon_counts[selected] += 1
                count += 1
                if self.moon_counts[selected] == self.max_counts[selected]:
                    kingdoms.remove(selected)
        elif self.options.counts == 2:
            for key in self.moon_counts.keys():
                if key != SMOKingdoms.DARK and key != SMOKingdoms.DARKER:
                    self.moon_counts[key] = 1
            self.moon_counts[SMOKingdoms.RUINED] = 3
            kingdoms = list(self.moon_counts.keys())
            kingdoms.remove(SMOKingdoms.DARK)
            kingdoms.remove(SMOKingdoms.DARKER)
            kingdoms.remove(SMOKingdoms.RUINED)
            count = 3
            for kingdom in kingdoms:
                count += self.moon_counts[kingdom]
            while count != 124:
                selected = kingdoms[random.randint(0, len(kingdoms)-1)]
                self.moon_counts[selected] += 1
                count += 1
                if self.moon_counts[selected] == self.max_counts[selected]:
                    kingdoms.remove(selected)
        elif self.options.counts == 3:
            for key in self.moon_counts.keys():
                self.moon_counts[key] = random.randint(int(self.moon_counts[key] * 0.8), int(self.moon_counts[key] * 1.25))

        elif self.options.counts == 4:
            for key in self.moon_counts.keys():
                self.moon_counts[key] = random.randint(int(self.moon_counts[key] * 1.0), int(self.moon_counts[key] * 2.0))
        if self.moon_counts[SMOKingdoms.DARK] > self.moon_counts[SMOKingdoms.DARKER]:
            temp = self.moon_counts[SMOKingdoms.DARKER]
            self.moon_counts[SMOKingdoms.DARKER] = self.moon_counts[SMOKingdoms.DARK]
            self.moon_counts[SMOKingdoms.DARK] = temp
        for key in self.moon_counts.keys():
            if self.moon_counts[key] > self.max_counts[key]:
                self.moon_counts[key] = self.max_counts[key]
        if self.options.counts == 1 or self.options.counts == 2:
            kingdoms = list(self.moon_counts.keys())
            kingdoms.remove(SMOKingdoms.DARK)
            kingdoms.remove(SMOKingdoms.DARKER)
            count = 0
            for kingdom in kingdoms:
                count += self.moon_counts[kingdom]
            if count != 124:
                raise Exception("Moon count exception! Moons required to beat the game is not 124, was " + str(count))
        # Change all outfit moon requirements to a proportion based on random Dark Side count
        # for key in self.outfit_moon_counts.keys():
        #     self.outfit_moon_counts[key] = int(self.outfit_moon_counts[key] * (self.moon_counts[SMOKingdoms.DARK]/250))
            # if self.outfit_moon_counts[key] > self.moon_counts[SMOKingdoms.DARK]:
            #     self.outfit_moon_counts[key] = self.moon_counts[SMOKingdoms.DARK] - 1


    def bind_game_entrances(self) -> None:
        """
            Creates a list of entrance bindings that link in-game entrances to different Stage Names and Stage Ids
        """
        entry : Entrance
        missing_bindings = []
        for entry in self.randomized_entrances.placements:
            # if entry.name == "Top Hat Tower Entrance":
            #     print(entry.name, entry.connected_region)
            # if entry.connected_region.name == SMORegion.cap_kingdom_topper:
            #     print(entry.name, entry.connected_region)
            # if entry.parent_region.name not in display_name_to_internal_name.keys():
            #     if entry.parent_region.name not in missing_bindings and entry.parent_region.name not in display_name_alias.keys():
            #         missing_bindings.append(entry.parent_region.name)
            # if entry.connected_region.name not in display_name_to_internal_name.keys():
            #     if entry.connected_region.name not in missing_bindings and entry.connected_region.name not in display_name_alias.keys():
            #         missing_bindings.append(entry.connected_region.name)
            # if "Invisible Road" in entry.name:
            #     print(f"{entry.name}, {entry.parent_region}, {entry.connected_region}, {entry.paired_entrance}, {entry.is_sub_area}")
            pass

        for unique_entry in missing_bindings:
            pass
            #print(f'"{unique_entry}",')

        for key in display_name_to_internal_name.keys():
            if display_name_to_internal_name[key] not in list(stage_id_to_name.values()):
                pass
                #print(key)

        #set_stage_ids = set(stage_ids)

        # for i in range(len(stage_ids)):
        #     if stage_ids.index(stage_ids[i]) != i:
        #         print(i, stage_ids[i])

        # for i in set_stage_ids:
        #     print(f"'{i}',")

        missing_maps = []
        missing_stage_ids = []

        for i in internal_name_to_entrance:
            if i not in stage_names:
                missing_maps.append(i)


            for j in internal_name_to_entrance[i]:
                if isinstance(internal_name_to_entrance[i][j], dict):
                    for k in internal_name_to_entrance[i][j]:
                        if internal_name_to_entrance[i][j][k] not in stage_ids and internal_name_to_entrance[i][j][k] not in missing_stage_ids:
                            missing_stage_ids.append(internal_name_to_entrance[i][j][k])
                else:
                    if internal_name_to_entrance[i][j] not in stage_ids and internal_name_to_entrance[i][j] not in missing_stage_ids:
                        missing_stage_ids.append(internal_name_to_entrance[i][j])

        # for i in missing_maps:
        #     print(f"'{i}',")
        #
        # for i in missing_stage_ids:
        #     print(f"'{i}',")

        repeats = {}
        repeat_entrances = {}
        is_all_reverse: bool = True

        for entrance, binding in self.randomized_entrances.pairings:
            entry, _exit = get_entrance_pair(self, entrance, binding)


            enter_stage_id, exit_stage_id = get_stage_ids(self, entry, _exit)
            entry_name = display_name_to_internal_name[entry.parent_region.name]
            exit_name = display_name_to_internal_name[_exit.parent_region.name]
            while " " in entry_name:
                entry_name = display_name_to_internal_name[entry_name]
            while " " in exit_name:
                exit_name = display_name_to_internal_name[exit_name]
            entry_stage_name = display_name_to_internal_name[self.original_entrance_bindings[entry.name]]

            exit_stage_id_index = stage_ids.index(exit_stage_id)
            enter_stage_id_index = stage_ids.index(enter_stage_id)
            entry_index = stage_names.index(entry_name)

            # if exit_stage_id_index in self.entrance_data["over_world"] and exit_stage_id_index in self.entrance_data["sub_area"]:
            if exit_stage_id in repeats:
                repeats[exit_stage_id] += 1
            else:
                repeats[exit_stage_id] = 1
                # raise Exception(f"Duplicate ER Entry Error ({exit_stage_id_index}, {exit_stage_id}, {enter_stage_id_index}, {entry_name}), "
                #                 f"({stage_ids[self.entrance_data["over_world"][exit_stage_id_index][0]]}, {stage_names[self.entrance_data["over_world"][exit_stage_id_index][1]]})"
                #                 f"({stage_ids[self.entrance_data["sub_area"][exit_stage_id_index][0]]}, {stage_names[self.entrance_data["sub_area"][exit_stage_id_index][1]]})")
            over_world_ids = ["WorldHomeStage", "Revenge", "SnowWorldTown", "Underground000"]

            is_over_world = False
            for over_world_id in over_world_ids:
                is_over_world = (over_world_id in exit_name ) or ("WorldHomeStage" not in exit_name and "Entrance" in _exit.name) # and not "Beginning" in _exit.name
                if is_over_world:
                    break

            excluded_stage_ids = ["SnowUGEnt", "SnowUGExit"]
            if is_over_world and exit_stage_id in excluded_stage_ids:
                if "SnowWorldTown" in exit_name:
                    is_over_world = False


            if exit_stage_id != "None":
                if exit_stage_id_index not in self.entrance_data["over_world" if is_over_world and not exit_stage_id_index in self.entrance_data["over_world"] else "sub_area"]:
                    self.entrance_data["over_world" if is_over_world and not exit_stage_id_index in self.entrance_data["over_world"] else "sub_area"][exit_stage_id_index] = (enter_stage_id_index, entry_index, entry_stage_name == entry_name)

                    if exit_stage_id_index in self.entrance_data['over_world'] and "WorldHomeStage" in exit_name:
                        repeat_entrances[exit_stage_id_index] = []
                        repeat_entrances[exit_stage_id_index].append(f"OVER WORLD {entrance}, {binding}: ({stage_ids[exit_stage_id_index]},"
                              f" {stage_ids[self.entrance_data['over_world'][exit_stage_id_index][0]]},"
                              f" {stage_names[self.entrance_data['over_world'][exit_stage_id_index][1]]}, {entry.is_reverse})")
                    if exit_stage_id_index in self.entrance_data['sub_area'] and not "WorldHomeStage" in exit_name:
                        repeat_entrances[exit_stage_id_index] = []
                        repeat_entrances[exit_stage_id_index].append(f"SUB AREA {entrance}, {binding}: ({stage_ids[exit_stage_id_index]},"
                              f" {stage_ids[self.entrance_data['sub_area'][exit_stage_id_index][0]]},"
                              f" {stage_names[self.entrance_data['sub_area'][exit_stage_id_index][1]]}, {entry.is_reverse})")

                else:
                    # if exit_stage_id_index in self.entrance_data['over_world'] and "WorldHomeStage" in exit_name:
                    #     repeat_entrances.append(f"OVER WORLD ({stage_ids[exit_stage_id_index]},"
                    #           f" {stage_ids[self.entrance_data['over_world'][exit_stage_id_index][0]]},"
                    #           f" {stage_names[self.entrance_data['over_world'][exit_stage_id_index][1]]}, {entry.is_reverse})")
                    # if exit_stage_id_index in self.entrance_data['sub_area'] and not "WorldHomeStage" in exit_name:
                    #     repeat_entrances.append(f"SUB AREA ({stage_ids[exit_stage_id_index]},"
                    #           f" {stage_ids[self.entrance_data['sub_area'][exit_stage_id_index][0]]},"
                    #           f" {stage_names[self.entrance_data['sub_area'][exit_stage_id_index][1]]}, {entry.is_reverse})")

                    if exit_stage_id_index in self.entrance_data['over_world'] and "WorldHomeStage" in exit_name:
                        repeat_entrances[exit_stage_id_index].append(f"REPEAT OVER WORLD {entrance}, {binding}: ({stage_ids[exit_stage_id_index]},"
                              f" {stage_ids[self.entrance_data['over_world'][exit_stage_id_index][0]]},"
                              f" {stage_names[self.entrance_data['over_world'][exit_stage_id_index][1]]}, {entry.is_reverse}),"
                                                f"({self.original_entrance_bindings[entrance]}, {self.original_exit_bindings[binding]})")
                    if exit_stage_id_index in self.entrance_data['sub_area'] and not "WorldHomeStage" in exit_name:
                        repeat_entrances[exit_stage_id_index].append(f"REPEAT SUB AREA {entrance}, {binding}: ({stage_ids[exit_stage_id_index]},"
                              f" {stage_ids[self.entrance_data['sub_area'][exit_stage_id_index][0]]},"
                              f" {stage_names[self.entrance_data['sub_area'][exit_stage_id_index][1]]}, {entry.is_reverse}),"
                                                f"({self.original_entrance_bindings[entrance]}, {self.original_exit_bindings[binding]})")

                    if is_all_reverse:
                        is_all_reverse = entry.is_reverse

        # for i in repeats:
        #     if repeats[i] > 2:
        #         print(i, repeats[i])
        #
        # if is_all_reverse:
        #     print("All incorrect repeats were reverse entrances/exits.")
        #
        # count = 0
        # for i in repeat_entrances:
        #     if len(repeat_entrances[i]) > 1:
        #         count += 1
        #         for k in repeat_entrances[i]:
        #             print(k)
        #
        # print("Repeated Entrances: ", count)

        # for index in range(len(stage_ids)):
        #     cur_id = stage_ids[index]
        #     if (index not in self.entrance_data["over_world"] and index in self.entrance_data["sub_area"]
        #             and not "exdokan" in cur_id.lower() and not "exit" in cur_id.lower() and not "goal" in cur_id.lower()
        #             and not "return" in cur_id.lower() and not "2" == cur_id[-1] and not "b" == cur_id.lower()[-1]
        #             and not "out" in cur_id.lower()):
        #         print(f"Over world missing: {cur_id}")
        #     elif index not in self.entrance_data["sub_area"] and index in self.entrance_data["over_world"]:
        #         print(f"Sub area missing: {cur_id}")
        #     elif index not in self.entrance_data["over_world"] and index not in self.entrance_data["sub_area"]:
        #         print(f"Stage Id missing: {cur_id}")
            # if index == stage_ids.index("SnowUGEnt"):
            #     print(f"{self.entrance_data["sub_area"][index]}, {self.entrance_data["over_world"][index]}")


    # Change regionals to be dependent on the option
    def fill_slot_data(self) -> Mapping[str, Any]:
        # Entrance Rando
        if self.options.entrance_randomization:
            for stage_id in sorted(stage_ids):
                pass
                # print(f'"{stage_id}",')
            self.bind_game_entrances()

            # print(len(self.original_entrance_bindings))
            # print(len(self.original_exit_bindings))
            # print(len(stage_ids))
            # print(len(stage_names))
            # print(len(self.entrance_data))
            #
            # print("Finished entrance rando slot data")
            for entry in self.entrance_data["over_world"]:
                enter_stage_id_index, entry_index, nothing = self.entrance_data["over_world"][entry]
                prefixes = ["PictureBoss", "bar1", "Jyukai", "bar2", "taxi", "Race"]
                for prefix in prefixes:
                    if prefix in stage_ids[enter_stage_id_index] or prefix in stage_ids[entry]:
                        # print(f"{stage_ids[entry]}: {stage_ids[enter_stage_id_index]}, {stage_names[entry_index]}")
                        pass
            for entry in self.entrance_data["sub_area"]:
                enter_stage_id_index, entry_index, nothing = self.entrance_data["sub_area"][entry]
                prefixes = ["PictureBoss" "bar1", "Jyukai", "bar2", "taxi", "Race"]
                for prefix in prefixes:
                    if prefix in stage_ids[enter_stage_id_index] or prefix in stage_ids[entry]:
                        # print(f"{stage_ids[entry]}: {stage_ids[enter_stage_id_index]}, {stage_names[entry_index]}")
                        pass

        for player in range(1, self.multiworld.players + 1):
            if not player in self.coin_values:
                self.coin_values[player] = {}
            for location in self.multiworld.get_locations(player):
                if location.item.player == self.player:
                    #region Generate Coin Values
                    if location.item.game == self.game and location.item.name == SMOItemData.coins:
                        rand_num = self.random.randint(0,99)
                        if rand_num < 44:
                            coin_amount = self.random.randint(50, 100)
                            location.item.name = f"{str(coin_amount)} " + location.item.name
                            self.coin_values[location.player][location.address] = coin_amount
                        elif rand_num < 74:
                            coin_amount = self.random.randint(101, 250)
                            location.item.name = f"{str(coin_amount)} " + location.item.name
                            self.coin_values[location.player][location.address] = coin_amount
                        elif rand_num < 89:
                            coin_amount = self.random.randint(251, 500)
                            location.item.name = f"{str(coin_amount)} " + location.item.name
                            self.coin_values[location.player][location.address] = coin_amount
                        elif rand_num < 96:
                            coin_amount = self.random.randint(501, 750)
                            location.item.name = f"{str(coin_amount)} " + location.item.name
                            self.coin_values[location.player][location.address] = coin_amount
                        elif rand_num < 100:
                            coin_amount = self.random.randint(751, 1000)
                            location.item.name = f"{str(coin_amount)} " + location.item.name
                            self.coin_values[location.player][location.address] = coin_amount

                        # Fixes item_name_to_id calls with coins
                        # start_id = self.item_name_to_id[SMOItemData.coins]
                        # if location.item.name not in self.item_name_to_id:
                        #     start_id += 1
                        #     self.item_name_to_id[location.item.name] = start_id

                    #endregion


        # Changing regional coin classification depending on shop item classification
        # may not be feasible due to player order inconsistencies
        # # Regional Coin Items
        # regional_totals = {}
        # for item, option, kingdom, cost in shop_location_costs:
        #     if kingdom not in regional_totals:
        #         regional_totals[kingdom] = 0
        #     if self.options.goal.value >= option or self.options.entrance_randomization > 0:
        #         regional_totals[kingdom] += cost
        #         self.get_location(item)
        #
        # shop_item_classifications = {}
        # for location, option, kingdom, cost in shop_location_costs:
        #     if kingdom not in shop_item_classifications:
        #         shop_item_classifications[kingdom] = []
        #
        #     shop_item_classifications[kingdom].append(self.get_location(location[0]).item.classification)


        # Interpret current game spheres
        # for sphere in self.multiworld.get_spheres():
        #     for location in sphere:
        #         if

        # Color handling
        match self.options.colors.value:
            case self.options.colors.option_off:
                self.color_list = [0, 0, 5, 2, 7, 0, 0, 1, 8, 4, 6, 0, 3, 9, 64, 9, 9, 27]
                for location in self.get_locations():
                    for kingdom in range(17):
                        if location.name in full_moon_locations_list[kingdom]:
                            self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[kingdom]

            case self.options.colors.option_kingdom_random:
                colors = list(range(30))
                for i in range(17):
                    self.color_list.append(colors.pop(self.random.randint(0, len(colors) - 1)))
                for location in self.get_locations():
                    for kingdom in range(17):
                        if location.name in full_moon_locations_list[kingdom]:
                            self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[kingdom]

            case self.options.colors.option_item:
                self.color_list = [0, 15, 5, 2, 7, 11, 14, 1, 8, 4, 6, 17, 3, 9, 64, 9, 9, 10, 12, 16, 18, 19]
                for location in self.get_locations():
                    for kingdom in range(17):
                        if self.location_name_to_id[location.name] < 1168:
                            if location.item.game == self.game:
                                if location.item.name in capture_items:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[18]
                                elif location.item.name in stickers or location.item.name in souvenirs:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[19]
                                elif location.item.name in outfits:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[20]
                                elif kingdom_name_to_id[kingdom] in location.item.name:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[kingdom]
                                    break

                            else:
                                self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[21]
                                break

            case self.options.colors.option_classification:
                pass

            case self.options.colors.option_item_random:
                colors = list(range(30))
                colors.append(64)
                for i in range(22):
                    self.color_list.append(colors.pop(self.random.randint(0, len(colors) - 1)))
                for location in self.get_locations():
                    for kingdom in range(17):
                        if self.location_name_to_id[location.name] < 1168:
                            if location.item.game == self.game:
                                if location.item.name in capture_items:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[18]
                                elif location.item.name in stickers or location.item.name in souvenirs:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[19]
                                elif location.item.name in outfits:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[20]
                                elif kingdom_name_to_id[kingdom] in location.item.name:
                                    self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[
                                        kingdom]
                                    break

                            else:
                                self.shine_colors[self.location_name_to_id[location.name]] = self.color_list[21]
                                break

            case self.options.colors.option_classification_random:
                pass

            case self.options.colors.option_chaos:
                for location in self.get_locations():
                    if self.location_name_to_id[location.name] < 1168:
                        self.shine_colors[self.location_name_to_id[location.name]] = self.random.randint(0,30)
                        if self.random.randint(0,3) == 0:
                            self.shine_colors[self.location_name_to_id[location.name]] += 64


        self.shop_replace_data["caps"] = {}
        self.shop_replace_data["clothes"] = {}
        self.shop_replace_data["stickers"] = {}
        self.shop_replace_data["souvenirs"] = {}
        self.shop_replace_data["moons"] = {}
        self.shop_games = []
        self.shop_players = []
        self.shop_ap_items = []
        self.regional_shop_games = []
        self.regional_shop_players = []
        self.regional_shop_ap_items = []
        self.shine_games = []
        self.shine_slots[-1] = []
        self.shine_items[-1] = []
        self.text_less_locations = {}
        for location in self.get_locations():
            is_coin_item = location.name in coin_shop_locations_table
            is_regional_item = location.name in regional_shop_locations_table
            is_moon_item = "Shopping" in location.name
            is_text_less = location.item.player != self.player and \
                (location.name in regional_coin_table or location.name in regional_coin_groups_table or location.name in loc_Captures)

            if is_coin_item or is_regional_item or is_moon_item:
                game = location.item.game.replace("_", " ")
                player_name = self.multiworld.get_player_name(location.item.player)
                item_name = location.item.name.replace("_", " ")
                if is_coin_item:
                    if not player_name in self.shop_players:
                        self.shop_players.append(player_name)
                    if not item_name in self.shop_ap_items:
                        self.shop_ap_items.append(item_name)
                    if not game in self.shop_games:
                        self.shop_games.append(game)
                if is_regional_item and not is_moon_item:
                    if not player_name  in self.regional_shop_players and not player_name in self.shop_players:
                        self.regional_shop_players.append(player_name)
                    if not item_name in self.regional_shop_ap_items and not item_name in self.shop_ap_items:
                        self.regional_shop_ap_items.append(item_name)
                    if not game in self.regional_shop_games and not game in self.shop_games:
                        self.regional_shop_games.append(game)
                if is_moon_item:
                    if not player_name in self.shine_slots[-1] and not player_name in self.shop_players:
                        self.shine_slots[-1].append(player_name)
                    if not item_name in self.shine_items[-1] and not location.item.name in self.shop_ap_items:
                        self.shine_items[-1].append(item_name)
                    if not game in self.shine_games and not game in self.shop_games:
                        self.shine_games.append(game)
            if is_text_less:
                self.text_less_locations[location.address] = (location.item.player, location.item.name)

        # Fill extra common slot names
        for i in range(1, self.multiworld.players):
            player_name = self.multiworld.get_player_name(i)
            if player_name not in self.shop_players:
                self.shop_players.append(player_name)
                if not len(self.shop_players) < 37:
                    break

        self.shop_games = sorted(self.shop_games)
        self.shop_players = sorted(self.shop_players)
        self.shop_ap_items = sorted(self.shop_ap_items)
        self.regional_shop_games = sorted(self.regional_shop_games)
        self.regional_shop_players = sorted(self.regional_shop_players)
        self.regional_shop_ap_items = sorted(self.regional_shop_ap_items)
        self.shine_games = sorted(self.shine_games)
        self.shine_slots[-1] = sorted(self.shine_slots[-1])
        self.shine_items[-1] = sorted(self.shine_items[-1])

        # add common list lookup
        for world_id in range(len(location_hint_list)):
            self.shine_replace_data[world_id] = {}
            self.shine_items[world_id] = []
            self.shine_slots[world_id] = []

        for location in self.get_locations():
            for world_id in range(len(location_hint_list)):
                if self.location_name_to_id[location.name] in location_hint_list[world_id]:
                    item_name = location.item.name.replace('_', ' ')
                    slot_name = self.multiworld.get_player_name(location.item.player)
                    if not item_name in self.shine_items[world_id] and not item_name in self.shop_ap_items:
                        self.shine_items[world_id].append(item_name)
                    if not slot_name in self.shine_slots[world_id] and not slot_name in self.shop_players:
                        self.shine_slots[world_id].append(slot_name)

        # Sort shine item and slot lists
        for world_id in range(len(location_hint_list)):
            self.shine_items[world_id] = sorted(self.shine_items[world_id])
            self.shine_slots[world_id] = sorted(self.shine_slots[world_id])

        for world_id in range(len(location_hint_list)):
            for hint_id in range(len(location_hint_list[world_id])):
                for key in list(location_hint_list[world_id].keys()):
                    if location_hint_list[world_id][key] == hint_id:
                        loc_name = self.location_id_to_name[key]
                        if loc_name in self.multiworld.regions.location_cache[self.player]:
                            location = self.multiworld.get_location(loc_name, self.player)
                            slot_name = self.multiworld.get_player_name(location.item.player)
                            item_name = location.item.name.replace('_', ' ')
                            slot_index: int = (self.shine_slots[world_id].index(slot_name)
                                               + TextDataOffset.Moons) if slot_name not in self.shop_players\
                                else self.shop_players.index(slot_name)
                            name_index: int = (self.shine_items[world_id].index(item_name)
                                               + TextDataOffset.Moons) if item_name not in self.shop_ap_items\
                                else self.shop_ap_items.index(item_name)
                            self.shine_replace_data[world_id][hint_id] = [slot_index, name_index]
                        else:
                            self.shine_replace_data[world_id][hint_id] = [255, 255]


        for location in self.get_locations():
                if self.location_name_to_id[location.name] < 2582 :
                    if "Shopping" in location.name:
                        game = location.item.game.replace("_", " ")
                        slot_name = self.multiworld.get_player_name(location.item.player)
                        item = location.item.name.replace("_", " ")
                        game_index = self.shop_games.index(
                            game) if game in self.shop_games else (self.shine_games.index(
                            game) + TextDataOffset.Shop_Moon)
                        player_index = self.shop_players.index(
                            slot_name) if slot_name in self.shop_players else (self.shine_slots[-1].index(
                            slot_name) + TextDataOffset.Shop_Moon)
                        item_index = self.shop_ap_items.index(
                            item) if item in self.shop_ap_items else (self.shine_items[-1].index(
                            item) + TextDataOffset.Shop_Moon)

                        self.shop_replace_data["moons"][self.location_name_to_id[location.name]] = [game_index,
                        player_index, item_index, location.item.classification.value]
                    else:
                        if (2539 > self.location_name_to_id[location.name] > 2500 or 2582 > self.location_name_to_id[location.name] > 2576)  and (location.name in coin_shop_locations_table or location.name in regional_shop_locations_table):
                            game = location.item.game.replace("_", " ")
                            slot_name = self.multiworld.get_player_name(location.item.player)
                            item = location.item.name.replace("_", " ")
                            game_index = self.shop_games.index(game) if game in self.shop_games else (self.regional_shop_games.index(game) + TextDataOffset.Regional)
                            player_index = self.shop_players.index(slot_name) if slot_name in self.shop_players else (self.regional_shop_players.index(slot_name) + TextDataOffset.Regional)
                            item_index = self.shop_ap_items.index(item) if item in self.shop_ap_items else (self.regional_shop_ap_items.index(item) + TextDataOffset.Regional)
                            self.shop_replace_data["caps"][self.location_name_to_id[location.name]] = [game_index,
                            player_index,
                            item_index, location.item.classification.value]
                        if self.location_name_to_id[location.name] > 2538 and (location.name in coin_shop_locations_table or location.name in regional_shop_locations_table):
                            game = location.item.game.replace("_", " ")
                            slot_name = self.multiworld.get_player_name(location.item.player)
                            item = location.item.name.replace("_", " ")
                            game_index = self.shop_games.index(
                                game) if game in self.shop_games else (self.regional_shop_games.index(
                                game) + TextDataOffset.Regional)
                            player_index = self.shop_players.index(
                                slot_name) if slot_name in self.shop_players else (self.regional_shop_players.index(
                                slot_name) + TextDataOffset.Regional)
                            item_index = self.shop_ap_items.index(
                                item) if item in self.shop_ap_items else (self.regional_shop_ap_items.index(
                                item) + TextDataOffset.Regional)
                            self.shop_replace_data["clothes"][self.location_name_to_id[location.name]] = [game_index, player_index,
                                                                                                          item_index, location.item.classification.value]
                if location.name in stickers:
                    game = location.item.game.replace("_", " ")
                    slot_name = self.multiworld.get_player_name(location.item.player)
                    item = location.item.name.replace("_", " ")
                    game_index = self.shop_games.index(
                        game) if game in self.shop_games else (self.regional_shop_games.index(game) + TextDataOffset.Regional)
                    player_index = self.shop_players.index(slot_name) if slot_name in self.shop_players else (self.regional_shop_players.index(slot_name) + TextDataOffset.Regional)
                    item_index = self.shop_ap_items.index(
                        item) if item in self.shop_ap_items else (self.regional_shop_ap_items.index(item) + TextDataOffset.Regional)
                    self.shop_replace_data["stickers"][self.location_name_to_id[location.name]] = [game_index,
                    player_index,
                    item_index, location.item.classification.value]
                if location.name in souvenirs:
                    game = location.item.game.replace("_", " ")
                    slot_name = self.multiworld.get_player_name(location.item.player)
                    item = location.item.name.replace("_", " ")
                    game_index = self.shop_games.index(
                        game) if game in self.shop_games else (
                                self.regional_shop_games.index(game) + TextDataOffset.Regional)
                    player_index = self.shop_players.index(slot_name) if slot_name in self.shop_players else (
                                self.regional_shop_players.index(slot_name) + TextDataOffset.Regional)
                    item_index = self.shop_ap_items.index(
                        item) if item in self.shop_ap_items else (
                                self.regional_shop_ap_items.index(item) + TextDataOffset.Regional)

                    self.shop_replace_data["souvenirs"][self.location_name_to_id[location.name]] = [game_index,
                                        player_index,
                                        item_index, location.item.classification.value]

        return {**(self.options.as_dict("goal", "colors", "regional_coins", "capture_sanity", "ability_sanity", "entrance_randomization", "death_link")), "counts" : self.moon_counts,
                "shine_games": self.shine_games ,"shine_slots" : self.shine_slots, "shine_items" : self.shine_items, "shine_replace_data" : self.shine_replace_data, "shine_colors" : self.shine_colors,
                "shop_games" : self.shop_games, "shop_players" : self.shop_players, "shop_ap_items" : self.shop_ap_items,
                "regional_shop_games" : self.regional_shop_games, "regional_shop_players" : self.regional_shop_players, "regional_shop_ap_items" : self.regional_shop_ap_items,
                "shop_replace_data" : self.shop_replace_data, "coin_values" : self.coin_values, "text_less_locations": self.text_less_locations,
                "entrances" : self.entrance_data}


    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.counts > 0:
            text = f"{'Moon Requirements:':33}"
            for key in self.moon_counts.keys():
                if kingdom_name_to_id[key] <= self.options.goal:
                    text += f"\n{'':33}{(key + (' Kingdom: ' if kingdom_name_to_id[key] < self.options.goal.option_dark else ' Side: '))}{str(self.moon_counts[key])}"
            spoiler_handle.write(text)

        if self.options.entrance_randomization > 0:
            text = f"{'\nRandomized Entrances:':33}"
            for er_from, er_to in self.randomized_entrances.pairings:
                text += f"\n{'':5}{er_from} -> {er_to}"
            spoiler_handle.write(text)

    def generate_output(self, output_directory: str):
        pass
        # if self.options.colors.value or self.options.counts.value > 0 or self.options.shop_sanity.value > 0:
        #     out_base = output_path(output_directory, self.multiworld.get_out_file_name_base(self.player))
        #     patch = SMOProcedurePatch(player=self.player, player_name=self.multiworld.get_player_name(self.player))
        #     write_patch(self, patch)
        #     patch.write(os.path.join(output_directory, f"{out_base}{patch.patch_file_ending}"))

    def interpret_slot_data(self, slot_data: dict[str, any]) -> dict[str, any]:
        """Parse slot data for Universal Tracker to properly validate logic and track progression."""
        relevant_data = {}

        # Parse moon count requirements for each kingdom
        relevant_data["MoonCounts"] = slot_data["counts"]

        # Parse game options
        relevant_data["Goal"] = slot_data["goal"]
        relevant_data["Colors"] = slot_data["colors"]
        relevant_data["CaptureSanity"] = slot_data["capture_sanity"]

        # Parse shine data structures (for hint system)
        relevant_data["ShineItems"] = slot_data["shine_items"]
        relevant_data["ShineReplaceData"] = slot_data["shine_replace_data"]
        relevant_data["ShineColors"] = slot_data["shine_colors"]

        # Parse shop data structures
        relevant_data["ShopGames"] = slot_data["shop_games"]
        relevant_data["ShopPlayers"] = slot_data["shop_players"]
        relevant_data["ShopAPItems"] = slot_data["shop_ap_items"]
        relevant_data["ShopReplaceData"] = slot_data["shop_replace_data"]

        # Parse coin values
        relevant_data["CoinValues"] = slot_data["coin_values"]

        return relevant_data
