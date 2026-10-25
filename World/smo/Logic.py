from BaseClasses import CollectionState

from .Items import outfits, shop_items, moon_types
from .Locations import  regional_coin_groups, regional_sub_area_to_kingdom, multi_moons, story_moons
from .Data.RegionData import SMORegion
from .Data.EntranceData import SMOEntranceData

def count_moons(state: CollectionState, kingdom : str, player: int) -> int:
    """ Counts the number of in logic moons available for a given kingdom.
        Args:
            state: The CollectionState of the current player.
            kingdom: A string containing the kingdom name.
            player: The index of this world's player.
        Return:
            Count of the moons for Kingdom 'kingdom'
    """
    amt = 0
    player_prog_items = state.prog_items[player]
    # for item_name in self.multiworld.worlds[player].item_name_groups[kingdom]:
    #     if state.has(item_name, player):
    #         amt += player_prog_items[item_name] if "Multi-Moon" not in item_name else 3
    amt += 0 if not kingdom.capitalize() + " Power Moon" in player_prog_items else player_prog_items[kingdom.capitalize() + " Power Moon"]
    amt += 0 if not kingdom.capitalize() + " Story Moon" in player_prog_items else player_prog_items[kingdom.capitalize() + " Story Moon"]
    amt += 0 if not kingdom.capitalize() + " Multi-Moon" in player_prog_items else player_prog_items[kingdom.capitalize() + " Multi-Moon"] * 3

    return amt


def total_moons(state: CollectionState, player: int) -> int:
    """Returns the cumulative count of items from an item group present in state.
        Args:
            state: The CollectionState of the current player.
            player: The index of this world's player.
        Return:
            The number of total in logic power moons.
    """
    amt = 0
    player_prog_items = state.prog_items[player]
    for item_name in state.multiworld.worlds[player].item_names:
        if item_name in moon_types:
            amt += player_prog_items[item_name] if "Multi-Moon" not in item_name else player_prog_items[item_name] * 3

    #print (amt)
    return amt

def can_complete_story(state: CollectionState, kingdom: str, player: int) -> bool:
    """ Returns true if all locations required to complete a given `kingdom` story are reachable
        Args:
                state: The CollectionState of the current player.
                kingdom: The kingdom to check
                player: The index of this world's player.
        Return:
            Whether the story in 'kingdom' is completable.
    """
    is_reachable = True
    moons = multi_moons[kingdom]
    if kingdom in story_moons:
        moons += story_moons[kingdom]
    for moon in moons:
        if not state.can_reach_location(moon, player):
            is_reachable = False
            break
    return is_reachable


def count_regionals(state: CollectionState, kingdom: str, player: int) -> int:
    """ Counts the number of in logic regional coins available for a given kingdom.
        Args:
            state: The CollectionState of the current player.
            kingdom: A string containing the kingdom name.
            player: The index of this world's player.
        Return:
            Count of the regional coins for Kingdom 'kingdom'
    """

    amt = 0
    player_prog_items = state.prog_items[player]
    if kingdom.capitalize() + " Kingdom Regional Coin" in player_prog_items:
        amt += player_prog_items[kingdom.capitalize() + " Kingdom Regional Coin"]

    elif kingdom.capitalize() + " Kingdom Regional Coins" in player_prog_items:
        num_groups = player_prog_items[kingdom.capitalize() + " Kingdom Regional Coins"]
        stages = ([kingdom + " Kingdom"] +
                  regional_sub_area_to_kingdom[kingdom.lower()]) if kingdom.lower() in regional_sub_area_to_kingdom else []

        for stage in stages:
            if " Regional" in stage:
                stage = stage[0:stage.index(" Regional")]
            internal_stage = SMOEntranceData.display_name_to_internal_name[stage]
            for group in regional_coin_groups[internal_stage]:
                if num_groups > 0:
                    amt += len(regional_coin_groups[internal_stage][group])
                    num_groups -= 1

    return amt