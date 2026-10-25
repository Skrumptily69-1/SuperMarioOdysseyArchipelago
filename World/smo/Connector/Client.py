import asyncio
import functools
import typing
from copy import deepcopy

import Utils
from NetUtils import encode, NetworkPlayer, NetworkItem, JSONtoTextParser, JSONMessagePart, ClientStatus
from MultiServer import Endpoint
from CommonClient import get_base_parser, gui_enabled, logger, CommonContext, ClientCommandProcessor
from typing import List, Any
from .Packets import PacketHeader, PacketType, Packet, ItemType, MessageType, ApInfoType

from .Data import inverse_shop_items, shop_items, get_item_type, worlds, world_alias, valid_warps, inverse_worlds, \
    multi_moon_locations, world_prefixes, get_regional_coin_location, id_to_name, regional_coin_location_to_internal, \
    get_in_game_id, get_location_id
from .Player import SMOPlayer

import traceback

from .. import stage_ids, stage_names, regional_coin_groups, shop_location_costs, TextDataOffset, \
    coin_shop_locations_table
from ..Data.ItemData import SMOItemData
from ..Data.RuleData import kingdom_name_to_id, SMOKingdoms
from ..Locations import regional_shop_locations_table, coin_shop_moon_locations

message_types = [
    "ItemSend",
    "Hint",
    "Join",
    "Part",
    "Chat"
]

class SMOJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text

# Add Debug Commands like send_to and shine, etc
class SMOCommandProcessor(ClientCommandProcessor):
    def _cmd_smo(self):
        """Check SMO Connection State"""
        if isinstance(self.ctx, SMOContext):
            logger.info(f"SMO Status: {self.ctx.get_smo_status()}")

    def _cmd_sync(self):
        """Attempt to resync received items"""
        if isinstance(self.ctx, SMOContext):
            logger.info(f"SMO Status: Syncing")
            self.ctx.player_data.item_index = 0
            self.ctx.server_msgs.append({"cmd" : "Sync"})
            # Add the sending locations part here if necessary.

    def _cmd_warp(self, kingdom : str, scenario : int = -1):
        """Warp Mario to another kingdom.
        Change kingdom scenario only if you know what you're doing as it can break the game."""
        if isinstance(self.ctx, SMOContext):
            while kingdom.lower() in world_alias:
                kingdom = world_alias[kingdom]
            if not kingdom in valid_warps:
                warps : str = ""
                for value in valid_warps.values():
                    warps += value + ", "
                warps = warps.removesuffix(", ")
                logger.info(f"{kingdom} is not a valid warp.\nValid warps: {warps}")
            else:
                logger.info(f"Sending Mario to {valid_warps[kingdom]}")
                self.ctx.player_data.add_message(f"Sending Mario to {valid_warps[kingdom]}")
                self.ctx.proxy_msgs.append(Packet(guid=self.ctx.proxy_guid, packet_type=PacketType.ChangeStage,
                                                 packet_data=[kingdom, scenario]))

    def _cmd_slot(self):
        """
        Display the active options according to slot data received from the lobby.
        """
        if isinstance(self.ctx, SMOContext):
            do_not_display = ["entrances", "shop_replace_data", "coin_values",
                              "shop_games", "shop_players", "shop_ap_items",
                              "shine_replace_data", "shine_items", "shine_colors",
                              "shine_slots", "shine_games"]
            for key in self.ctx.slot_data:
                if key not in do_not_display:
                    logger.info(f"{key}: {self.ctx.slot_data[key]}")

    def _cmd_packets(self):
        """
        Display queued packets
        """
        if isinstance(self.ctx, SMOContext):
            packets = []
            for packet in self.ctx.proxy_msgs:
                packets.append(packet.header.packet_type.name)
            logger.info(f"{packets}")


    def _cmd_shop(self, item_name: str):
        """
        Display a shop items text
        """
        if isinstance(self.ctx, SMOContext):
            if self.ctx.is_connected():
                if self.ctx.slot_data:
                    if hasattr(SMOItemData, item_name):
                        item_name = getattr(SMOItemData, item_name)
                    else:
                        logger.info(f"Invalid SMOItemData attribute {item_name}.")
                        return
                    if item_name in regional_shop_locations_table:
                        item_id = regional_shop_locations_table[item_name]
                    elif item_name in coin_shop_locations_table:
                        item_id = coin_shop_locations_table[item_name]
                    else:
                        logger.info(f"No Shop Text for {item_name}.")
                        return
                    item_id = str(item_id)
                    for entry in self.ctx.slot_data['shop_replace_data']:
                        if item_id in self.ctx.slot_data['shop_replace_data'][entry]:
                            data = self.ctx.slot_data['shop_replace_data'][entry][item_id]
                            if data[0] >= TextDataOffset.Regional:
                                game = self.ctx.slot_data['regional_shop_games'][data[0] - TextDataOffset.Regional]
                            else:
                                game = self.ctx.slot_data['shop_games'][data[0]]

                            if data[1] >= TextDataOffset.Regional:
                                slot_name = self.ctx.slot_data['regional_shop_players'][data[1] - TextDataOffset.Regional]
                            else:
                                slot_name = self.ctx.slot_data['shop_players'][data[1]]

                            if data[2] >= TextDataOffset.Regional:
                                item = self.ctx.slot_data['regional_shop_ap_items'][data[2] - TextDataOffset.Regional]
                            else:
                                item = self.ctx.slot_data['shop_ap_items'][data[2]]

                            logger.info(f"{item_name}: {slot_name}'s {item} from '{game}'")

    # def _cmd_unlock(self, kingdom : int, scenario : int = -1):
    #     if isinstance(self.ctx, SMOContext):
    #         logger.info(f"Unlocking Kingdom {kingdom}")
    #         self.ctx.player_data.add_message(f"Kingdom Unlocked")
    #         self.ctx.proxy_msgs.append(Packet(guid=self.ctx.proxy_guid, packet_type=PacketType.Progress,
    #                                       packet_data=[kingdom, scenario]))

    def _cmd_ero(self, entrance_id: str):
        """
        Logs the over world entrance at entrance_id
        """
        if isinstance(self.ctx, SMOContext):
            if len(self.ctx.slot_data) > 0:
                if entrance_id in stage_ids:
                    entrance = self.ctx.slot_data['entrances']['over_world'][str(stage_ids.index(entrance_id))]
                    logger.info(f"{entrance_id} leads to {stage_ids[entrance[0]]} in {stage_names[entrance[1]]}")

    def _cmd_ers(self, entrance_id: str):
        """
        Logs the sub area entrance at entrance_id
        """
        if isinstance(self.ctx, SMOContext):
            if len(self.ctx.slot_data) > 0:
                if entrance_id in stage_ids:
                    entrance = self.ctx.slot_data['entrances']['sub_area'][str(stage_ids.index(entrance_id))]
                    logger.info(f"{entrance_id} leads to {stage_ids[entrance[0]]} in {stage_names[entrance[1]]}")

# Change send message and related calls to send packet and serialize and deserialize using the packet of the respective packet type.
# Make sure to receive packets on the connection to send checks through to the AP Server from this client.

class SMOContext(CommonContext):
    command_processor = SMOCommandProcessor
    game = "Super Mario Odyssey"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy : asyncio.Server
        self.proxy_chat = None
        self.gamejsontotext = SMOJSONToTextParser(self)
        self.autoreconnect_task = None
        self.endpoint = None
        self.items_handling = 0b111
        self.room_info = None
        self.connected_msg = None
        self.game_connected : bool = False
        self.awaiting_info : bool = False
        self.full_inventory: List[Any] = []
        self.server_msgs: List[Any] = []
        self.server_comm_task = None
        self.proxy_msgs : List[Packet] = []
        self.proxy_guid : bytearray = bytearray()
        self.player_data : SMOPlayer = SMOPlayer()
        self.player = None
        self.slot_data : dict = {}
        #self.checked_locations : set
        self.ping_task = None
        self.awaiting_connection : bool = False
        self.disconnect_timer : int = 120
        self.logged_in : bool = False
        self.multi_moon_anim : bool = False
        self.death_link_enabled : bool = False
        self.allowed_packets : list = [PacketType.Init.value]
        # Make Simplified SMOPlayer, SMONetworkPlayer
        # That only contains a list of packets to be synced, current stage, and
        # guid. Other important info may be needed.
        # Have a dict of Slot Names -> SMONetworkPlayer
        # Make a UDP server to send player packets (movement, etc)
        # probably on the same port (1027)
        # Tunnel player packets through AP Lobby connection
        # Use Set and Get commands

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(SMOContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_smo_status(self) -> str:
        if not self.game_connected:
            return "Not connected to Super Mario Odyssey"

        return "Connected to Super Mario Odyssey"

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def connect_to_archipelago(self):
        payload = {
            'cmd': 'Connect',
            'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
            'tags': self.tags, 'items_handling': self.items_handling,
            'uuid': Utils.get_unique_identifier(), 'game': self.game, "slot_data": self.want_slot_data,
        }

        self.server_msgs.append(payload)

    # Handle APChatMessage here
    def on_print_json(self, args: dict):
        text = self.gamejsontotext(deepcopy(args["data"]))
        if "type" in args and args["type"] in message_types:
            if args["type"] == "Hint":
                print(args)
            self.player_data.add_message(text)

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def update_items(self):
        # just to be safe - we might still have an inventory from a different room
        if not self.is_connected():
            return

        self.server_msgs.append({"cmd": "ReceivedItems", "index": 0, "items": self.full_inventory})

    def queue_ap_info_from_list(self, info_list: list[str], info_type: ApInfoType, text_offset: TextDataOffset = TextDataOffset.Common):
        info_list_length = len(info_list)
        for i in range(0, info_list_length, 3):
            j = i + text_offset
            if i + 3 < info_list_length:
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                             packet_data=[info_type.value, j, j + 1, j + 2,
                                                          info_list[i:i + 3]]))
            else:
                self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
                                             packet_data=[info_type.value, j, j + 1, j + 2,
                                                          info_list[i:info_list_length]]))
    def forward_slot_data(self):
        """
        Forwards Slot Data from Archipelago Lobby connection to SMO
        :return:
        """
        # print(self.slot_data)
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.SlotData,
              packet_data=[self.slot_data["counts"]["cascade"],
                           self.slot_data["counts"]["sand"],
                           self.slot_data["counts"]["wooded"], self.slot_data["counts"]["lake"],
                           self.slot_data["counts"]["lost"], self.slot_data["counts"]["metro"],
                           self.slot_data["counts"]["seaside"],
                           self.slot_data["counts"]["snow"],
                           self.slot_data["counts"]["luncheon"],
                           self.slot_data["counts"]["ruined"],
                           self.slot_data["counts"]["bowser"], self.slot_data["counts"]["dark"],
                           self.slot_data["counts"]["darker"],
                           self.slot_data["goal"],
                           self.slot_data["death_link"], self.slot_data["capture_sanity"],
                           self.slot_data["entrance_randomization"] > 0]))



        # Games
        self.queue_ap_info_from_list(self.slot_data["shop_games"], ApInfoType.Games)

        # Players
        self.queue_ap_info_from_list(self.slot_data["shop_players"], ApInfoType.Players)

        # Items
        self.queue_ap_info_from_list(self.slot_data["shop_ap_items"], ApInfoType.Items)

        regional_shop_id_list = [2537, 2575, 2581, 2577, 2538, 2576]
        for i in regional_shop_locations_table:
            regional_shop_id_list.append(regional_shop_locations_table[i])

        items = []
        for i in range(2501, 2539):
            if i in regional_shop_id_list:
                continue
            if str(i) in self.slot_data["shop_replace_data"]["caps"]:
                items.append(self.slot_data["shop_replace_data"]["caps"][str(i)])
            else:
                pass
                # items.append([254,254,254,254])
        for i in range(2577, 2582):
            if i in regional_shop_id_list:
                continue
            if str(i) in self.slot_data["shop_replace_data"]["caps"]:
                items.append(self.slot_data["shop_replace_data"]["caps"][str(i)])

            else:
                pass
                # items.append([254,254,254,254])
        # logger.info(f"caps: {items}")
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[0, items]))
        #print(len(items), items)

        items = []
        for i in range(2539, 2582):
            if i in regional_shop_id_list:
                continue
            if str(i) in self.slot_data["shop_replace_data"]["clothes"]:
                items.append(self.slot_data["shop_replace_data"]["clothes"][str(i)])
            else:
                items.append([254,254,254,254])
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[1, items]))
        # logger.info(f"clothes: {items}")

        #print(len(items), items)

        # Colors
        print(self.slot_data["shine_colors"])
        data = [[]]
        for shine_uid in range(0, 1168):
            if len(data[-1]) == 51:
                data.append([])
            if shine_uid > 1167:
                break
            if str(shine_uid) in self.slot_data["shine_colors"]:
                data[-1].append([shine_uid, self.slot_data["shine_colors"][str(shine_uid)]])
        print(data)
        for i in data:
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShineColor,
                                          packet_data=[i]))
            #print(self.proxy_msgs[-1].packet.info)

        # Checked locations
        data = [[]]
        for loc in self.checked_locations:
            if len(data[-1]) == 100:
                data.append([])
            if loc < 1167:
                data[-1].append(loc)
        for i in data:
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.SentChecks,
                                              packet_data=[ItemType.Moon, i]))

        data = [[]]
        for loc in self.checked_locations:
            if len(data[-1]) == 100:
                data.append([])
            if 2700 <= loc < 4025:
                if self.slot_data["regional_coins"] == 1:
                    for stage in regional_coin_groups:
                        if loc in regional_coin_groups[stage]:
                            for group_member in regional_coin_groups[stage][loc]:
                                data[-1].append(regional_coin_location_to_internal[group_member])
                                if len(data[-1]) == 100:
                                    data.append([])
                            logger.info(f"{data}")
                else:
                    data[-1].append(regional_coin_location_to_internal[loc])
        for i in data:
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.SentChecks,
                                          packet_data=[ItemType.RegionalCoin, i]))

        # Load Zones
        over_world = []
        sub_area = []
        # 50 connections per packet
        for i in range(259):
            if str(i) in self.slot_data["entrances"]["over_world"]:
                over_world.append((i, self.slot_data["entrances"]["over_world"][str(i)][0],
                              self.slot_data["entrances"]["over_world"][str(i)][1]))

            if str(i) in self.slot_data["entrances"]["sub_area"]:
                sub_area.append((i, self.slot_data["entrances"]["sub_area"][str(i)][0],
                                   self.slot_data["entrances"]["sub_area"][str(i)][1]))



        for i in range(0, len(over_world), 50):
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace,
                                          packet_data=[5, over_world[i:(i + 50
                                                                    if (i + 50 < len(over_world))
                                                                    else len(over_world))]]))

        for i in range(0, len(sub_area), 50):
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace,
                                          packet_data=[6, sub_area[i:(i + 50
                                                                    if (i + 50 < len(sub_area))
                                                                    else len(sub_area))]]))

        if self.player_data.current_home_stage != "":
            self.forward_shine_data()

    def forward_shine_data(self):
        world_id = world_prefixes.index(self.player_data.current_home_stage)
        self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShineReplace,
                                         packet_data=[self.slot_data["shine_replace_data"][str(world_id)]]))

        # Slot Names
        self.queue_ap_info_from_list(self.slot_data["shine_slots"][str(world_id)], ApInfoType.Players, TextDataOffset.Moons)

        # Items
        #print(self.slot_data["shine_replace_data"][str(world_id)])
        self.queue_ap_info_from_list(self.slot_data["shine_items"][str(world_id)], ApInfoType.Items, TextDataOffset.Moons)

        # merge all into one packet with a specific regional type
        items = [[],[]]
        text_lists = ["regional_shop_games", "regional_shop_players", "regional_shop_ap_items"]
        text = [[],[],[]]
        shine_text = [[],[],[]]
        for entry in shop_location_costs:
            location = str(regional_shop_locations_table[entry[0]])
            kingdom_id = kingdom_name_to_id[entry[2]]
            if world_id == kingdom_id:
                for shop_type in self.slot_data["shop_replace_data"]:
                    if location in self.slot_data["shop_replace_data"][shop_type]:
                        items[0].append(self.slot_data["shop_replace_data"][shop_type][location])
                        for i in range(len(text)):
                            if self.slot_data["shop_replace_data"][shop_type][location][i] >= TextDataOffset.Regional:
                                text[i].append(self.slot_data[text_lists[i]][
                                                   self.slot_data["shop_replace_data"][shop_type][location][
                                                       i] - TextDataOffset.Regional])
                                items[0][-1][i] = len(text[i]) - 1 + TextDataOffset.Regional

        text_lists = ["shine_games", "shine_slots", "shine_items"]
        world_indexed = ["shine_slots", "shine_items"]

        for location, kingdom in coin_shop_moon_locations:
            location_id = str(regional_shop_locations_table[location])
            kingdom_id = kingdom_name_to_id[kingdom]
            if world_id == kingdom_id:
                if location_id in self.slot_data["shop_replace_data"]["moons"]:
                    items[1].append(self.slot_data["shop_replace_data"]["moons"][location_id])
                    for i in range(len(shine_text)):
                        if self.slot_data["shop_replace_data"]["moons"][location_id][i] >= TextDataOffset.Shop_Moon:
                            if text_lists[i] in world_indexed:
                                shine_text[i].append(self.slot_data[text_lists[i]]['-1'][
                                                         self.slot_data["shop_replace_data"]["moons"][location_id][
                                                             i] - TextDataOffset.Shop_Moon])
                            else:
                                shine_text[i].append(self.slot_data[text_lists[i]][
                                                   self.slot_data["shop_replace_data"]["moons"][location_id][
                                                       i] - TextDataOffset.Shop_Moon])


                            items[1][-1][i] = len(shine_text[i]) - 1 + TextDataOffset.Shop_Moon

        # logger.info(f"items: {items}, text: {text}, shine_text: {shine_text}")
        for i in range(len(items)):
            self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[i+2, items[i]]))

        for i in range(len(text)):
            self.queue_ap_info_from_list(text[i], ApInfoType(i), TextDataOffset.Regional)

        for i in range(len(shine_text)):
            self.queue_ap_info_from_list(shine_text[i], ApInfoType(i), TextDataOffset.Shop_Moon)

    # def send_cappy_message(self, location_id: int):
    #     cappy_message = []
    #     cappy_message_text = [[],[]]
    #     for i in range(len(cappy_message_text)):
    #         current = cappy_message_text[i]
    #         current_length = len(current)
    #         for j in range(0, current_length,3):
    #             k = j + TextDataOffset.Cappy
    #             if j + 3 < current_length:
    #                 #        print(self.slot_data["shop_games"][i:i + 3])
    #                 self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
    #                                               packet_data=[i, k, k + 1, k + 2,
    #                                                            current[j:j + 3]]))
    #             else:
    #                 #        print(self.slot_data["shop_games"][i:i + 3])
    #                 self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.ApInfo,
    #                                               packet_data=[i, k, k + 1, k + 2, current[
    #                                                                                j:current_length]]))s
    #
    #     self.proxy_msgs.append(
    #         Packet(guid=self.proxy_guid, packet_type=PacketType.ShopReplace, packet_data=[4, items[i]]))

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if self.death_link_enabled:
            super().on_deathlink(data)
            death_link_packet : Packet = Packet(guid=self.proxy_guid, packet_type=PacketType.DeathLink)
            self.proxy_msgs.append(death_link_packet)
            self.last_death_link = data["time"]

    # Handle sending packets to SMO here
    def on_package(self, cmd: str, args: dict):
        match cmd:
            case "Connected":
                json = args
                me: NetworkPlayer
                if "slot_info" in json.keys():
                    json["slot_info"] = {}
                if "players" in json.keys():

                    for n in json["players"]:
                        if n.slot == json["slot"] and n.team == json["team"]:
                            me = n
                            break

                    # Only put our player info in there as we actually need it
                    json["players"] = [me]
                    self.slot_data = json["slot_data"]
                    #self.checked_locations = json["checked_locations"]
                self.player = me
                self.player_data.add_message(f"Connected to Archipelago as {me.name} playing Super Mario Odyssey")
                # Send slot data to SMO
                self.forward_slot_data()
                self.player_data.goal = self.slot_data["goal"]
                self.death_link_enabled = self.slot_data["death_link"]
                self.logged_in = True

                if self.death_link_enabled:
                    self.server_msgs.append({"cmd" : "ConnectUpdate", "tags" : ["AP", "DeathLink"]})
                self.server_msgs.append({"cmd" : "Get", "keys" : [f"{self.player.name}_scenarios"]})
                # if DEBUG:
                #     print(json)
                self.connected_msg = encode([json])
                if self.awaiting_info:
                    self.server_msgs.append(self.room_info)
                    self.update_items()
                    self.awaiting_info = False

            case "RoomUpdate":
                # Same story as above
                json = args
                if "players" in json.keys():
                    json["players"] = []

                self.server_msgs.append(json)

            case "ReceivedItems":
                # Handle Sending various collect packets to SMO here
                if self.multi_moon_anim:
                    return


                if args["index"] == 0:
                    self.full_inventory.clear()
                    # not sure if this is needed?
                    self.player_data.reset_moons()
                    self.player_data.reset_regional_coins()

                    self.player_data.item_index = 0
                    print("Accept full inventory.")

                if args["index"] != self.player_data.item_index:
                    print("Next index mismatch, syncing.")
                    self.server_msgs.append({"cmd" : "Sync"})
                else:
                    self.player_data.item_index += 1

                for item in args["items"]:
                    net_item = NetworkItem(*item)
                    self.full_inventory.append(net_item)

                    packet = None
                    item_type = ItemType(get_item_type(net_item.item))
                    item_id = get_in_game_id(self.player_data, item_type, net_item.item)
                    item_name = ""
                    if net_item.item in id_to_name:
                        item_name = id_to_name[net_item.item]
                    index = args["index"]
                    sender_name = self.player_names[net_item.player] if net_item.player != self.slot else ""
                    packet = Packet(guid=self.proxy_guid, packet_type=PacketType.Check,
                                    packet_data=[item_id, item_type, index, item_name, "", 0,
                                                 sender_name])


                    # logger.info(f"Item Type: {ItemType(item_type).name}, Net Item: {net_item.item}, Item Name: {id_to_name[net_item.item]}")
                    match item_type:
                        # Moons
                        case ItemType.Moon:
                            moon_item_name = id_to_name[net_item.item].split()[0]
                            if "Power" in moon_item_name:
                                moon_item_name = SMOKingdoms.MUSHROOM
                            if "Bowser" in moon_item_name:
                                moon_item_name = SMOKingdoms.BOWSER
                            moon_item = kingdom_name_to_id[moon_item_name]
                            if moon_item > 15:
                                moon_item += 17

                            packet.packet.amount = moon_item
                            if item_id == -1:
                                logger.info(f"Received nonexistent moon. This is either caused by a bug or the use of commands to give"
                                                f" this slot more of a type of moon than can possibly exist.")

                        # Regional Coins
                        case ItemType.RegionalCoin:
                            # Packet must contain placementId, stageName, and worldId
                            # WorldId stored in amount
                            # logger.info(f"Next Coin: {id_to_name[net_item.item]}")
                            regional_coin = self.player_data.get_next_regional_coin(net_item.item)
                            # logger.info(f"Next Coin: {regional_coin}")
                            if regional_coin[2] != -1:
                                packet.packet.obj_id = regional_coin[0]
                                packet.packet.stage = regional_coin[1]
                                packet.packet.amount = regional_coin[2]

                        # Filler
                        case ItemType.Coins:
                            if str(net_item.location) in self.slot_data["coin_values"][str(net_item.player)]:
                                packet.packet.amount = self.slot_data["coin_values"][str(net_item.player)][str(net_item.location)]
                            else:
                                print(packet.packet.sender_name, " location id: ", net_item.location)
                        # Flag items
                        case -4:
                            pass
                    if packet:
                        if packet.header.packet_type == PacketType.Check:
                            if packet.packet.location_id < 0:
                                logger.info(f"Invalid Location ID in packet {packet.packet.location_id}.")
                                logger.info(f"Invalid item in packet {net_item.item}, {packet.packet.item_type.name}.")
                            else:
                                self.proxy_msgs.append(packet)
                        else:
                            self.proxy_msgs.append(packet)

                self.server_msgs.append(args)

            case "RoomInfo":
                self.seed_name = args["seed_name"]
                self.room_info = args

            case "Retrieved":
                pass
                # if f"{self.player.name}_scenarios" in args["keys"] and args["keys"][f"{self.player.name}_scenarios"] is dict:
                #     for key in self.player_data.world_scenarios.keys():
                #         if self.player_data.world_scenarios[key] <= args["keys"][f"{self.player.name}_scenarios"][key]:
                #             self.player_data.world_scenarios[key] = args["keys"][f"{self.player.name}_scenarios"][key]
                #     #for world in self.player_data.world_scenarios.keys():
                #         #self.proxy_msgs.append(Packet(guid=self.proxy_guid, packet_type=PacketType.Progress,
                #         #                             packet_data=[inverse_worlds[world], self.player_data.world_scenarios[world]]))
                #         #pass
                #
                #     self.server_msgs.append({"cmd": "Set", "key": f"{self.player.name}_scenarios",
                #                              "operations": [
                #                                  {"operation": "replace", "value": self.player_data.world_scenarios}]})
                # else:
                #     self.server_msgs.append({"cmd" : "Set", "key" : f"{self.player.name}_scenarios",
                #                             "operations" : [{ "operation" : "replace", "value" : self.player_data.world_scenarios}]})

            case _:
                if cmd != "PrintJSON":
                    self.server_msgs.append(args)

    def run_gui(self):
        from kvui import GameManager

        class SMOManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Super Mario Odyssey Client"

        self.ui = SMOManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

async def ping_loop(ctx : SMOContext):
    while not ctx.exit_event.is_set():
        if ctx.endpoint:
            if ctx.disconnect_timer == 0:
                ctx.game_connected = False
            ctx.disconnect_timer = 1
        await asyncio.sleep(1.0)



async def proxy_chat(ctx : SMOContext):
    try:
        clear_msgs : bool = False
        while not ctx.exit_event.is_set():
            # if (len(ctx.player_data.messages) > 0 or clear_msgs) and ctx.game_connected:
            #     msg_packet : Packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.ArchipelagoChat,
            #                                  packet_data=[[], MessageType.Chat, ctx.player_data.next_messages()])
            #     ctx.proxy_msgs.append(msg_packet)
            #     if len(ctx.player_data.messages) == 0 and not clear_msgs:
            #         clear_msgs = True
            #     else:
            #         clear_msgs = False
            if ctx.multi_moon_anim:
                await asyncio.sleep(27.0)
                ctx.multi_moon_anim = False
                ctx.server_msgs.append({"cmd": "Sync"})


            else:
                await asyncio.sleep(5.0)
    except Exception as e:
        logger.exception(e)


async def handle_proxy(reader : asyncio.StreamReader, writer : asyncio.StreamWriter, ctx : SMOContext) -> None:
    data : bytearray
    packet : Packet
    ctx.endpoint = Endpoint(writer.transport.get_extra_info("socket"))
    ctx.awaiting_connection = True
    try:
        while True:
            data : bytearray = bytearray(await reader.read(PacketHeader.SIZE))
            packet = Packet(guid=ctx.proxy_guid, header_bytes=data)
            if len(ctx.proxy_guid) == 0:
                if len(packet.header.guid) != 0:
                    ctx.proxy_guid = packet.header.guid
                    if len(ctx.proxy_msgs) > 0:
                        for queued_packet in ctx.proxy_msgs:
                            if queued_packet.header.guid == "None":
                                queued_packet.header.guid = ctx.proxy_guid

            packet_size : int = packet.header.packet_size.value
            data = bytearray(await reader.read(packet_size))
            packet.deserialize(data)

            if packet.header.packet_type != PacketType.Unknown:
                if hasattr(packet, "packet"):
                    if packet_size != packet.packet.SIZE:

                        logger.info(
                            f"Packet {packet.header.packet_type.name}, Packet Size {packet_size}, AP SIZE {packet.packet.SIZE}")
                ctx.disconnect_timer = 30
                # Prevent appending server message before connected to server.
            match packet.header.packet_type:
                case PacketType.Connect:
                    if ctx.proxy_guid != packet.header.guid:
                        ctx.proxy_guid = packet.header.guid
                    init_packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.Init)
                    # logger.info(f"max players {init_packet.packet.max_players}, version {init_packet.packet.server_version}")
                    # Insert init packet at 0 in queue so other packets added before aren't dropped.
                    ctx.proxy_msgs.insert(0, init_packet)
                    # Only log initial connection
                    logger.info("SMO Connected")
                    if ctx.awaiting_connection:
                        ctx.awaiting_connection = False
                        ctx.game_connected = True
                    needs_slot_data : bool = True
                    for queued_packet in ctx.proxy_msgs:
                        if queued_packet.header.packet_type == PacketType.SlotData:
                            needs_slot_data = False
                            break
                    if len(ctx.slot_data) > 0 and needs_slot_data:
                        ctx.forward_slot_data()
                        if ctx.player_data.current_home_stage in world_prefixes:
                            ctx.forward_shine_data()
                    ctx.server_msgs.append({"cmd": "Sync"})

                case PacketType.Disconnect:
                    ctx.game_connected = False
                    break

                case PacketType.ArchipelagoConnect:
                    if packet.packet.host_name != "":
                        if packet.packet.port != 0:
                            ctx.port = packet.packet.port
                        await ctx.connect(f"{packet.packet.host_name}:{ctx.port}")
                    if packet.packet.password != "":
                        ctx.password = packet.packet.password
                    if packet.packet.slot_name != "":
                        ctx.auth = packet.packet.slot_name
                    ctx.connect_to_archipelago()

                case PacketType.ChangeStage:
                    stage : str = packet.packet.stage
                    if stage[0:stage.index("World")] != ctx.player_data.current_home_stage:
                        ctx.player_data.current_home_stage = stage[0:stage.index("World")]
                        print(f"Player Changed Home Stage to {ctx.player_data.current_home_stage}")

                        if ctx.is_connected() and ctx.player_data.current_home_stage in world_prefixes:
                            ctx.forward_shine_data()

                case PacketType.Check:
                    print(packet.packet.location_id, packet.packet.item_type)
                    item_type : ItemType = ItemType(packet.packet.item_type.value)
                    location_id = get_location_id(item_type, packet.packet.location_id)
                    match item_type:
                        # Scouting
                        case ItemType.ShopMoonScout:
                            world_id = world_prefixes.index(ctx.player_data.current_home_stage)
                            for location, kingdom in coin_shop_moon_locations:
                                location_id = regional_shop_locations_table[location]
                                kingdom_id = kingdom_name_to_id[kingdom]
                                if world_id == kingdom_id:
                                    ctx.server_msgs.append(
                                        {"cmd": "LocationScouts", "locations": [location_id], "create_as_hint": 2})

                        case ItemType.MoonRockScout:
                            pass

                        case ItemType.StickerScout:
                            ctx.server_msgs.append({"cmd": "LocationScouts", "locations": [location_id], "create_as_hint": 2})
                            # logger.info(f"Scouted Location: {ItemType(item_type).name} {location_id}")

                        case ItemType.SouvenirScout:
                            ctx.server_msgs.append({"cmd": "LocationScouts", "locations": [location_id], "create_as_hint": 2})
                            # logger.info(f"Scouted Location: {ItemType(item_type).name} {location_id}")

                        case ItemType.CapScout:
                            ctx.server_msgs.append({"cmd": "LocationScouts", "locations": [location_id], "create_as_hint": 2})
                            # logger.info(f"Scouted Location: {ItemType(item_type).name} {location_id}")

                        case ItemType.ClothesScout:
                            ctx.server_msgs.append({"cmd": "LocationScouts", "locations": [location_id], "create_as_hint": 2})
                            # logger.info(f"Scouted Location: {ItemType(item_type).name} {location_id}")

                        # Locations
                        case ItemType.Moon:
                            print(f"Got {location_id}")
                            if location_id in multi_moon_locations:
                                ctx.multi_moon_anim = True
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations" : [location_id]})
                            if ctx.player_data.check_goal(location_id):
                                ctx.server_msgs.append({"cmd" : "StatusUpdate", "status" : ClientStatus.CLIENT_GOAL})
                                print("Goal achieved")

                        case ItemType.Clothes:
                            print(f"Got Clothes {location_id}")
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                        case ItemType.Cap:
                            print(f"Got Cap {location_id}")
                            print(f"Got adjusted Cap {location_id}")
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                        case ItemType.Souvenir:
                            print(f"Got Souvenir {location_id}")
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                        case ItemType.Sticker:
                            print(f"Got Sticker {location_id}")
                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                        case ItemType.RegionalCoin:
                            location_id = get_regional_coin_location(packet.packet.stage, packet.packet.obj_id)
                            # logger.info(f"Got Regional Coin {packet.packet.stage}, {packet.packet.obj_id}, {location_id}")
                            if location_id not in ctx.checked_locations and ctx.is_connected():
                                # Append Cappy Message Data for Sent Text Box
                                location = str(location_id)
                                if location in ctx.slot_data["text_less_locations"]:
                                    receiver, item_name = ctx.slot_data["text_less_locations"][location]
                                    receiver_name = ctx.player_names[receiver]
                                    msg_packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.Check,
                                                    packet_data=[-1, ItemType.SentCheck, -1, item_name, "", 0,
                                                                 receiver_name])
                                    ctx.proxy_msgs.append(msg_packet)
                                else:
                                    logger.info(f"Location {location} not in 'text_lass_locations'")

                            if location_id != -1:
                                if ctx.slot_data["regional_coins"] == 1:
                                    location_id = ctx.player_data.get_regional_group(packet.packet.stage, location_id)
                                    if location_id != -1:
                                        ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                                else:
                                    ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})

                        case ItemType.Capture:
                            print(f"Got Capture {location_id}")
                            if location_id not in ctx.checked_locations and ctx.is_connected():
                                # Append Cappy Message Data for Sent Text Box
                                location = str(location_id)
                                if location in ctx.slot_data["text_less_locations"]:
                                    receiver, item_name = ctx.slot_data["text_less_locations"][location]
                                    receiver_name = ctx.player_names[receiver]
                                    msg_packet = Packet(guid=ctx.proxy_guid, packet_type=PacketType.Check,
                                                    packet_data=[-1, ItemType.SentCheck, -1, item_name, "", 0,
                                                                 receiver_name])
                                    ctx.proxy_msgs.append(msg_packet)
                                else:
                                    logger.info(f"Location {location} not in 'text_lass_locations'")

                            ctx.server_msgs.append({"cmd": "LocationChecks", "locations": [location_id]})
                        # Add Regional Coin

                case PacketType.DeathLink:
                    if ctx.death_link_enabled:
                        await ctx.send_death()
                    else:
                        ctx.death_link_enabled = True
                        ctx.server_msgs.append({"cmd": "ConnectUpdate", "tags": ["AP", "DeathLink"]})
                        await ctx.send_death()


                # case PacketType.ArchipelagoChat:
                #     logger.info(f"Message Received")
                #     logger.info(f"{packet.packet.message}")

            if len(ctx.proxy_msgs) > 0 and ctx.game_connected:
                # num_bytes = 0
                # packets = 0
                # for i in ctx.proxy_msgs:
                #     num_bytes += 20
                #     num_bytes += i.packet.SIZE
                #     if num_bytes < 4096:
                #         packets += 1


                #print(num_bytes)
                #print(packets)
                packet_send_offset : int = 0
                for i in range(len(ctx.proxy_msgs)):
                    if ctx.proxy_msgs[0].header.packet_type == PacketType.Check and ctx.player_data.current_home_stage == "":
                        packet_send_offset += 1
                        #print("Skipping packet cannot be sent now")
                        continue
                    response : Packet = ctx.proxy_msgs.pop(packet_send_offset)
                    b = response.serialize()
                    # allowed_packets = [PacketType.Init, PacketType.ArchipelagoChat]
                    if response.header.packet_type.value in ctx.allowed_packets or True:
                        # logger.info(
                        #     f"header {len(response.header.serialize())} {response.header.packet_type.name} {len(response.packet.serialize())}")
                        writer.write(b)
                        await writer.drain()
                    if response.header.packet_type == PacketType.Connect:
                        await asyncio.sleep(5.0)


                    # for message in ctx.proxy_msgs:
                    #     print(message.header.packet_type)
                #await asyncio.sleep(0.25)

            if not ctx.game_connected and not ctx.awaiting_connection:
                break
    except Exception as e:
        print("Connection Error ", e)
        traceback.print_exc()
        ctx.player_data.item_index = 0
        ctx.player_data.current_home_stage = ""
        ctx.awaiting_connection = True
        writer.close()


async def comm_loop(ctx : SMOContext):
    while not ctx.exit_event.is_set():
        if not ctx.is_connected():
            ctx.logged_in = False
        if len(ctx.server_msgs) > 0 and ctx.logged_in:
            await ctx.send_msgs(ctx.server_msgs)
            ctx.server_msgs.clear()
        await asyncio.sleep(0.1)


def launch(*launch_args: str):
    async def main():
        parser = get_base_parser()
        args = parser.parse_args(launch_args)

        ctx = SMOContext(args.connect, args.password)
        logger.info("Starting Super Mario Odyssey proxy server")

        ctx.proxy = asyncio.start_server(functools.partial(handle_proxy, ctx=ctx), "0.0.0.0", 1027)
        ctx.proxy_chat = asyncio.create_task(proxy_chat(ctx) , name="ChatLoop")
        ctx.ping_task = asyncio.create_task(ping_loop(ctx), name="PingLoop")
        ctx.server_comm_task = asyncio.create_task(comm_loop(ctx), name="CommLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_chat
        await ctx.ping_task
        await ctx.server_comm_task
        # Make ping task wait 1-second intervals
        # Add counter member to ctx
        # if packet of any kind is read from stream,
        # reset counter to 5
        # if counter is 0 when ping task runs,
        # send ping packet to SMO reset counter, set awaiting_ping member of ctx true
        # when ping packet received, set awaiting_ping to false
        # if counter reaches 0 and awaiting_ping is true,
        # set game_connected to false.
        # test without ping packet to see if enough packets
        # saturate the stream to keep connection open with Mario idle
        # if not then implement the above.

        await ctx.exit_event.wait()


    Utils.init_logging("SMOClient")
    # options = Utils.get_options()

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()