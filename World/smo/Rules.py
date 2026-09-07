from collections.abc import Callable
import dataclasses
from enum import IntEnum, StrEnum
from typing import Any

from BaseClasses import CollectionState, Location
from rule_builder.field_resolvers import FieldResolver
from rule_builder.options import OptionFilter
from worlds.generic.Rules import set_rule, add_rule
from rule_builder.rules import Rule, TWorld, True_
from . import SMOWorld, regional_coin_table, regional_coin_groups, regional_coin_groups_table
from .Data.RegionData import SMORegion
from .Data.ItemData import SMOItemData
from .Data.EntranceData import SMOEntranceData
from .Data.LocationData import SMOLocationData
from .Data.RuleData import SMORuleCondition, SMORuleOperation, SMOEntranceDataType, SMOKingdoms, regional_rule_data, \
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
