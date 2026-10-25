from NetUtils import NetworkItem
from .Data import moon_list, id_to_name, goals, worlds
from ..Data.EntranceData import SMOEntranceData
from ..Locations import regional_coins, regional_coin_groups, regional_sub_area_to_kingdom
from ..Data.ItemData import SMOItemData

class SMOPlayer:
    MAX_MOONS: dict[str,int] = {
        "Cascade Story Moon": 1,
        "Sand Story Moon": 2,
        "Wooded Story Moon": 2,
        "Metro Story Moon": 5,
        "Seaside Story Moon": 4,
        "Snow Story Moon": 4,
        "Luncheon Story Moon": 3,
        "Bowser Story Moon": 3,
        "Cascade Multi-Moon": 2,
        "Sand Multi-Moon": 4,
        "Wooded Multi-Moon": 4,
        "Lake Multi-Moon": 1,
        "Metro Multi-Moon": 7,
        "Seaside Multi-Moon": 5,
        "Snow Multi-Moon": 5,
        "Luncheon Multi-Moon": 5,
        "Ruined Multi-Moon": 1,
        "Bowser Multi-Moon": 4,
        "Mushroom Multi-Moon": 5,
        "Dark Side Multi-Moon": 1,
        "Darker Side Multi-Moon": 1
    }

    MAX_REGIONAL_COINS: dict[str,int] = {
        "Cap Kingdom Regional Coin" : 50,
        "Cascade Kingdom Regional Coin" : 50,
        "Sand Kingdom Regional Coin" : 100,
        "Wooded Kingdom Regional Coin" : 100,
        "Lake Kingdom Regional Coin" : 50,
        "Lost Kingdom Regional Coin" : 50,
        "Metro Kingdom Regional Coin" : 100,
        "Seaside Kingdom Regional Coin" : 100,
        "Snow Kingdom Regional Coin" : 50,
        "Luncheon Kingdom Regional Coin" : 100,
        "Bowser's Kingdom Regional Coin" : 100,
        "Moon Kingdom Regional Coin" : 50,
        "Mushroom Kingdom Regional Coin" : 100,
    }


    def __init__(self):
        self.moons: dict[str,int] = {
        "Cap Power Moon": 0,
        "Cascade Power Moon": 2,
        "Sand Power Moon": 4,
        "Wooded Power Moon": 4,
        "Lake Power Moon": 1,
        "Cloud Power Moon": 0,
        "Lost Power Moon": 0,
        "Metro Power Moon": 7,
        "Seaside Power Moon": 5,
        "Snow Power Moon": 5,
        "Luncheon Power Moon": 5,
        "Ruined Power Moon": 1,
        "Bowser Power Moon": 4,
        "Moon Power Moon": 0,
        "Power Star": 6,
        "Dark Side Power Moon": 1,
        "Cascade Story Moon": 0,
        "Sand Story Moon": 0,
        "Wooded Story Moon": 0,
        "Metro Story Moon": 0,
        "Seaside Story Moon": 0,
        "Snow Story Moon": 0,
        "Luncheon Story Moon": 0,
        "Bowser Story Moon": 0,
        "Cascade Multi-Moon": 1,
        "Sand Multi-Moon": 2,
        "Wooded Multi-Moon": 2,
        "Lake Multi-Moon": 0,
        "Metro Multi-Moon": 5,
        "Seaside Multi-Moon": 4,
        "Snow Multi-Moon": 4,
        "Luncheon Multi-Moon": 3,
        "Ruined Multi-Moon": 0,
        "Bowser Multi-Moon": 3,
        "Mushroom Multi-Moon": 0,
        "Dark Side Multi-Moon": 0,
        "Darker Side Multi-Moon": 0,
        "Beat the Game": -1
        }

        self.regional_coins: dict[str,int] = {
            "Cap Kingdom Regional Coin": 0,
            "Cascade Kingdom Regional Coin": 0,
            "Sand Kingdom Regional Coin": 0,
            "Wooded Kingdom Regional Coin": 0,
            "Lake Kingdom Regional Coin": 0,
            "Lost Kingdom Regional Coin": 0,
            "Metro Kingdom Regional Coin": 0,
            "Seaside Kingdom Regional Coin": 0,
            "Snow Kingdom Regional Coin": 0,
            "Luncheon Kingdom Regional Coin": 0,
            "Bowser's Kingdom Regional Coin": 0,
            "Moon Kingdom Regional Coin": 0,
            "Mushroom Kingdom Regional Coin": 0,
        }

        self.regional_group_progress = []

        self.messages : list[str] = []
        self.MAX_MESSAGE_SIZE = 0x42
        self.item_index : int = 0
        self.world_scenarios : dict = {
            "Cap": 1,
            "Cascade": 1,
            "Sand": 1,
            "Wooded": 1,
            "Lake": 1,
            "Cloud": 1,
            "Lost": 1,
            "Metro": 1,
            "Seaside": 1,
            "Snow": 1,
            "Luncheon": 1,
            "Ruined": 1,
            "Bowser": 1,
            "Moon": 1,
            "Mushroom": 1,
            "Dark": 1,
            "Darker": 1
        }
        self.goal : int
        self.current_home_stage : str = ""

        self.game_names: dict[int, str] = {}
        self.slot_names: dict[int, str] = {}
        self.item_names: dict[int, str] = {}

    def reset_moons(self):
        self.moons = {
            "Cap Power Moon": 0,
            "Cascade Power Moon": 2,
            "Sand Power Moon": 4,
            "Wooded Power Moon": 4,
            "Lake Power Moon": 1,
            "Cloud Power Moon": 0,
            "Lost Power Moon": 0,
            "Metro Power Moon": 7,
            "Seaside Power Moon": 5,
            "Snow Power Moon": 5,
            "Luncheon Power Moon": 5,
            "Ruined Power Moon": 1,
            "Bowser Power Moon": 4,
            "Moon Power Moon": 0,
            "Power Star": 6,
            "Dark Side Power Moon": 1,
            "Cascade Story Moon": 0,
            "Sand Story Moon": 0,
            "Wooded Story Moon": 0,
            "Metro Story Moon": 0,
            "Seaside Story Moon": 0,
            "Snow Story Moon": 0,
            "Luncheon Story Moon": 0,
            "Bowser Story Moon": 0,
            "Cascade Multi-Moon": 1,
            "Sand Multi-Moon": 2,
            "Wooded Multi-Moon": 2,
            "Lake Multi-Moon": 0,
            "Metro Multi-Moon": 5,
            "Seaside Multi-Moon": 4,
            "Snow Multi-Moon": 4,
            "Luncheon Multi-Moon": 3,
            "Ruined Multi-Moon": 0,
            "Bowser Multi-Moon": 3,
            "Mushroom Multi-Moon": 0,
            "Dark Side Multi-Moon": 0,
            "Darker Side Multi-Moon": 0,
            "Beat the Game": -1
        }

    def reset_regional_coins(self):
        self.regional_coins = {
            "Cap Kingdom Regional Coin": 0,
            "Cascade Kingdom Regional Coin": 0,
            "Sand Kingdom Regional Coin": 0,
            "Wooded Kingdom Regional Coin": 0,
            "Lake Kingdom Regional Coin": 0,
            "Lost Kingdom Regional Coin": 0,
            "Metro Kingdom Regional Coin": 0,
            "Seaside Kingdom Regional Coin": 0,
            "Snow Kingdom Regional Coin": 0,
            "Luncheon Kingdom Regional Coin": 0,
            "Bowser's Kingdom Regional Coin": 0,
            "Moon Kingdom Regional Coin": 0,
            "Mushroom Kingdom Regional Coin": 0,
        }

    def get_next_moon(self, item : int) -> int:
        """
        Args:
            item: id of the respective Archipelago Item
        Returns:
            next moon id to send to SMO
        """
        item_name : str = id_to_name[item]


        if item_name in self.MAX_MOONS:
            if self.moons[item_name] >= self.MAX_MOONS[item_name]:
                return -1
        elif item_name == "Beat the Game":
            return -2
        moon_id : int = moon_list["Mushroom" if item_name == "Power Star" else item_name.split(" ")[0]][self.moons[item_name]]
        self.moons[item_name] += 1
        return moon_id

    def get_next_regional_coin(self, item: int) -> tuple[str, str, int] | str:
        """
            Args:
                item: id of the respective Archipelago Item
            Returns:
                next Regional Coin (placement_id, stage_name, world_id) to send to SMO
        """
        item_name : str = id_to_name[item]

        if self.regional_coins[item_name] >= self.MAX_REGIONAL_COINS[item_name]:
            return "", "", -1

        placement_id: str = ""
        stage_name: str = ""
        world_id: int = -1

        kingdom = item_name.split()[0]
        world_id = worlds[kingdom]
        stages = [kingdom + " Kingdom"]
        stages += regional_sub_area_to_kingdom[
                      kingdom.lower()] if kingdom.lower() in regional_sub_area_to_kingdom else []

        regional_ids = []
        for stage in stages:
            stage_name = SMOEntranceData.display_name_to_internal_name[
                stage.replace(" Regional Coins", "").replace(" Regional Groups","")]
            for group in regional_coin_groups[stage_name]:
                regional_ids += regional_coin_groups[stage_name][group]
            if len(regional_ids) > self.regional_coins[item_name]:
                break

        if len(regional_ids) <= self.regional_coins[item_name]:
            return f"{kingdom} {len(regional_ids)} {regional_ids}"
        location_id = regional_ids[self.regional_coins[item_name]]
        for coin in regional_coins[stage_name]:
            if regional_coins[stage_name][coin] == location_id:
                placement_id = coin
                break
        self.regional_coins[item_name] += 1
        return placement_id, stage_name, world_id


    def get_regional_group(self, stage: str, location_id: int) -> int:
        """
            Args:
                stage: The name of the stage the Regional Coin is from
                location_id: The id of the Regional Coin location
            Returns:
                complete Regional Coin Group location id
        """
        stage = stage.strip()
        self.regional_group_progress.append(location_id)
        for group in regional_coin_groups[stage]:
            progress : int = 0
            for coin in regional_coin_groups[stage][group]:
                if coin in self.regional_group_progress:
                    progress += 1
            if progress == len(regional_coin_groups[stage][group]):
                for coin in regional_coin_groups[stage][group]:
                    self.regional_group_progress.remove(coin)
                return group

        return -1



    def add_message(self, message : str) -> None:
        """
        Adds message to the player's messages list automatically subdividing the message to fit in a single ChatMessagePacket.
        Args:
            message: The message to add. Must be UTF-8 compatible.
        """
        try:
            message.encode()
        except UnicodeEncodeError:
            raise f"The message ({message}) cannot be UTF-8 encoded."

        if len(message) <= self.MAX_MESSAGE_SIZE:
            self.messages.append(message)
        else:
            message_parts = message.split()
            current_message : str = message_parts.pop(0)
            current_messages : list[str] = []
            while len(message_parts) > 0:
                if len(message_parts[0]) + len(current_message) < self.MAX_MESSAGE_SIZE:
                    current_message += f" {message_parts.pop(0)}"
                else:
                    if len(current_message.replace("\t", "")) > 0:
                        current_messages.append(current_message)
                        current_message = "\t"
                    if len(message_parts[0]) > self.MAX_MESSAGE_SIZE:
                        cut_part = message_parts[0][0:self.MAX_MESSAGE_SIZE - 2] + "-"
                        current_message += cut_part
                        message_parts[0] = message_parts[0][self.MAX_MESSAGE_SIZE - 2:]

            # Make two part message appear in order
            while len(current_messages) > 0:
                self.messages.append(current_messages.pop(-1))
            self.messages.append(current_message)

    def next_messages(self) -> str:
        if len(self.messages) >= 1:
            return self.messages.pop(0)
        return ""

    def check_goal(self, location : int) -> bool:
        if self.goal and self.goal in goals:
            return goals[self.goal] == location
        return False

    def get_scenario_dict(self) -> dict:
        return self.world_scenarios