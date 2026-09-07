from collections.abc import Callable
import dataclasses
from enum import IntEnum, StrEnum
from typing import Any, override

from BaseClasses import CollectionState, Location
from rule_builder.field_resolvers import FieldResolver, resolve_field
from rule_builder.options import OptionFilter
from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import Rule, TWorld, True_
from . import SMOWorld, regional_coin_table, regional_coin_groups, regional_coin_groups_table
from .Data.RegionData import SMORegion
from .Data.ItemData import SMOItemData
from .Data.EntranceData import SMOEntranceData
from .Data.LocationData import SMOLocationData
from .Data.RuleData import SMOEntranceDataType, SMOKingdoms, regional_rule_data, \
    moon_rule_data
from .Locations import shop_location_costs
from .Items import capture_items
from .Options import CaptureSanity, SMOOptions
from .Logic import total_moons, count_moons, count_regionals, can_complete_story

"""Temporary until item_group_names from __init__.py is properly working"""
cappy: list[str] = [SMOItemData.cap_throw, SMOItemData.up_throw, SMOItemData.down_throw, SMOItemData.spin_throw]
@dataclasses.dataclass()
class CanCapture(Rule[TWorld], game="Super Mario Odyssey"):
    item_name: str | FieldResolver
    """The capture to check for"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return (True_() if OptionFilter(CaptureSanity, 1).check(world.options) else self).Resolved(
            resolve_field(self.item_name, world, str),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.item_name}{options})"

    class Resolved(Rule.Resolved):
        item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return (state.prog_items[self.player][self.item_name] >= 0
                and state.has_any(cappy, self.player)
                and state.can_reach_region(self.item_name, self.player))

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: set()}

scenarios: dict[str, list[str]] = {
    "cap": ["First Visit", "Revisit/peace", "Post-game", "Moon Rock"],
    "cascade": ["First Visit", "Revisit/peace", "Post-game", "Moon Rock"],
    "sand": ["First Visit", "Night", "Peace", "Post-game", "Moon Rock"],
    "wooded": ["First Visit", "Post-Spewart", "Peace", "Post-game", "Moon Rock"],
    "lake": ["First Visit", "Peace", "Post-game", "Moon Rock"],
    "cloud": ["First Visit", "Revisit/peace", "Post-game", "Moon Rock"],
    "lost": ["First Visit", "Revisit/peace", "Post-game", "Moon Rock"],
    "metro": ["Night", "Day", "Festival", "Peace", "Post-game", "Balloon World", "Festival Revisit?", "Moon Rock"],
    "seaside": ["First Visit", "Peace", "Post-game", "Moon Rock"],
    "snow": ["First Visit", "Peace", "Post-game", "Moon Rock"],
    "luncheon": ["First Visit", "Post-meat", "Post-game", "KFR", "Volcano-less", "Volcano-less", "Peace", "Moon Rock", "Balloon World", "Bruncheon"],
    "ruined": ["First Visit", "Peace", "Post-game", "Moon Rock"],
    "bowsers": ["First Visit", "Peace", "Post-game", "Moon Rock"],
    "moon": ["First Visit", "Peace/Postgame", "Moon Rock"],
    "mushroom": ["Rushroom", "Post-game", "World Peace?"],
    "dark": ["First Visit", "Peace"],
    "darker": ["First Visit", "Peace"]
}

default_progression = [0, 1, 2, 3]
# Notably, last element of list is moon rock if applicable
scenario_progression: dict[str, list[int]] = {
    "cap": default_progression,
    "cascade": default_progression,
    "sand": [0, 1, 2, 3, 4],
    "wooded": [0, 1, 2, 3, 4],
    "lake": default_progression,
    "cloud": default_progression,
    "lost": default_progression,
    "metro": [0, 1, 3, 4, 7], # Not sure if the "festival" scenario needs to be included here, if it is needed, its [0, 1, 2, 3, 4, 7]
    "seaside": default_progression,
    "snow": default_progression,
    "luncheon": [0, 1, 6, 2, 7], # If Bruncheon needs to be included, append '9' to the start of the list
    "ruined": default_progression,
    "bowsers": default_progression,
    "moon": [0, 1, 2],
    "mushroom": [0, 1, 2],
    "dark": [0, 1],
    "darker": [0, 1]
}

@dataclasses.dataclass()
class HasStoryProgress(Rule[TWorld], game="Super Mario Odyssey"):
    kingdom_name: str | FieldResolver
    """The Kingdom we're checking progress in"""

    scenarios: list[int] | FieldResolver
    """Possible scenarios for the location"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return self.Resolved(
            (resolve_field(self.kingdom_name, world, str).split(" ")[0].lower().replace("'", "")),
            resolve_field(self.scenarios, world, list[int]),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.kingdom_name}, {self.scenarios}{options})"

    class Resolved(Rule.Resolved):
        kingdom: str
        scenarios: list[int]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            kingdom_scenarios = scenario_progression.get(self.kingdom, [])
            story_event_count = state.prog_items[self.player][f"{self.kingdom}_story_progress"]
            if story_event_count == len(kingdom_scenarios)-1: # If they're in latest possible scenario, its accessible
                return True

            # If at ANY point deeper into the scenario progression can a moon become inaccessible
            # it cannot be considered in logic due to Archipelago rules.
            for i in range(len(kingdom_scenarios)):
                if kingdom_scenarios[i] == self.scenarios[-1] and story_event_count >= i:
                    return True
                if story_event_count <= i and kingdom_scenarios[i] not in self.scenarios:
                    return False
            return True

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {f"{self.kingdom}_story_progress": set()}


def set_rules(self : SMOWorld) -> None:
    """ Sets the placement rules for Super Mario Odyssey.
        Args:
            self: SMOWorld object for this player's world.
            options: The options from this player's yaml.
    """


    for location in self.get_locations():
        if location.name in moon_rule_data:
            if location.access_rule != Location.access_rule:
                print(location.name)
            else:
                self.set_rule(location, moon_rule_data[location.name])

        if location.name in regional_coin_table:
            for stage in regional_coin_groups:
                for regional_group_id in regional_coin_groups[stage]:
                    if location.address in regional_coin_groups[stage][regional_group_id]:
                        for regional_group_name in regional_coin_groups_table:
                            if regional_coin_groups_table[regional_group_name] == regional_group_id:
                                if regional_group_name in regional_rule_data:
                                    self.set_rule(location, regional_rule_data[regional_group_name])
                                else:
                                    break

    # for i in all_access_rules:
    #
    #     print(i)

    # for debugging purposes, you may want to visualize the layout of your world. Uncomment the following code to
# write a PlantUML diagram to the file "my_world.puml" that can help you see whether your regions and locations
# are connected and placed as desired

    from Utils import visualize_regions
    visualize_regions(self.get_region(SMORegion.defunct_odyssey), "my_world.puml")
