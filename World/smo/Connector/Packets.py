from enum import Enum
from ctypes import c_short as short, c_ushort as ushort, c_byte as sbyte, c_ubyte as byte, c_byte, c_ubyte
from typing import Any

class PacketType(Enum):
    Unknown : short = 0
    Init : short = 1
    PlayerInfo : short = 2
    HackCapInfo : short = 3
    GameInfo : short = 4
    TagInfo : short = 5
    Connect : short = 6
    Disconnect : short = 7
    CostumeInfo : short = 8
    CaptureInfo : short = 10
    ChangeStage : short = 11
    Command : short = 12
    ArchipelagoChat : short = 13
    SlotData : short = 20
    UnlockWorld : short = 21
    Check : short = 22
    DeathLink : short = 23
    SentChecks : short = 24
    ApInfo : short = 25
    ShopReplace : short = 26
    ShineReplace : short = 27
    ShineColor : short = 28
    ArchipelagoConnect : short = 29
    #UDPInit : short = 26
    #HolePunch : short = 27

class ConnectionType(Enum):
    Connect = 0
    Reconnect = 1

class ItemType(Enum):
    SentCheck = -11
    ShopMoonScout = -10
    MoonRockScout = -9
    StickerScout = -8
    SouvenirScout = -7
    CapScout = -6
    ClothesScout = -5
    LifeUpHeart = -4
    LifeHeart = -3
    Coins = -2
    Moon = -1
    Clothes = 0
    Cap = 1
    Souvenir = 2
    Sticker = 3
    RegionalCoin = 4
    Capture = 5
    MoonRock = 6
    HealthUpgrade = 7
    WalletUpgrade = 8

class CappyMessageType(Enum):
    Connect = 0
    Moon = 1
    MultiMoon = 2
    RegionalCoin = 3
    Cap = 4
    Clothes = 5
    Sticker = 6
    Souvenir = 7
    Capture = 8
    MoonRock = 9
    HealthUpgrade = 10
    WalletUpgrade = 11
    Coins = 12

class ApInfoType(Enum):
    Games = 0
    Players = 1
    Items = 2


class MessageType(Enum):
    Chat = 0
    System = 1
    Private = 2

#region Check Packets

class CheckPacket:
    OBJ_ID_SIZE = 0x40
    STAGE_NAME_SIZE = 0x30
    SENDER_NAME_SIZE = 0x40
    location_id : int
    # Shop Items
    item_type : ItemType
    # Prevent Repeat Filler ETC
    index : int
    # OBJ ID
    obj_id : str
    # Stage
    stage : str
    # Coins
    amount : int
    sender_name : str


    SIZE : short = 16 + OBJ_ID_SIZE + STAGE_NAME_SIZE + SENDER_NAME_SIZE

    def __init__(self, packet_bytes : bytearray = None, location_id : int = None, item_type : int = None, index : int = None, obj_id : str = None, stage : str = None, amount : int = None, sender_name : str = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.location_id = location_id
            self.item_type = ItemType(item_type)
            self.index = index
            self.obj_id = obj_id
            self.stage = stage
            self.amount = amount
            self.sender_name = sender_name

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.location_id.to_bytes(4, "little", signed=True)
        data += self.item_type.value.to_bytes(4, "little", signed=True)
        data += self.index.to_bytes(4, "little", signed=True)
        data += self.obj_id.encode()
        while len(data) < 12 + self.OBJ_ID_SIZE:
            data += b"\x00"
        data += self.stage.encode()
        while len(data) < 12 + self.OBJ_ID_SIZE + self.STAGE_NAME_SIZE:
            data += b"\x00"
        data += self.amount.to_bytes(4, "little", signed=True)
        data += self.sender_name.encode()
        while len(data) < 16 + self.OBJ_ID_SIZE + self.STAGE_NAME_SIZE + self.SENDER_NAME_SIZE:
            data += b"\x00"
        if len(data) != self.SIZE:
            raise f"CheckPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.location_id  = int.from_bytes(data[offset:offset + 4], "little")
        offset += 4
        self.item_type  = ItemType(int.from_bytes(data[offset:offset + 4], "little",signed=True))
        offset += 4
        self.index  = int.from_bytes(data[offset:offset + 4], "little",signed=True)
        offset += 4
        self.obj_id = data[offset:offset + self.OBJ_ID_SIZE].decode()
        offset += self.OBJ_ID_SIZE
        self.stage = data[offset:offset + self.STAGE_NAME_SIZE].decode()
        offset += self.STAGE_NAME_SIZE
        self.amount  = int.from_bytes(data[offset:offset + 4], "little")
        offset += 4
        self.sender_name = data[offset:offset + self.SENDER_NAME_SIZE].decode()
        offset += self.SENDER_NAME_SIZE
        count = 0
        for char in self.obj_id:
            count += 1 if char != '\0' else 0
        self.obj_id = self.obj_id[0:count]
        count = 0
        for char in self.stage:
            count += 1 if char != '\0' else 0
        self.stage = self.stage[0:count]
        count = 0
        for char in self.sender_name:
            count += 1 if char != '\0' else 0
        self.sender_name = self.sender_name[0:count]

class SentChecksPacket:
    check_type: ItemType
    checks : list[int]
    SIZE : short = 202

    def __init__(self, packet_bytes : bytearray = None, check_type : ItemType = None, checks : list[int] = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.check_type = check_type
            self.checks = checks

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.check_type.value.to_bytes(length=2, byteorder="little", signed=True)
        for i in range(100):
            if i < len(self.checks):
                data += self.checks[i].to_bytes(length=2, byteorder="little", signed=True)

            else:
                filler = 0
                data += filler.to_bytes(length=2, byteorder="little", signed=True)


        if len(data) != self.SIZE:
            raise f"SentChecksPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        # Shouldn't be necessary

#endregion

#region Server Packets

# ADD MessageType and GUID to __init__
class ChatMessagePacket:
    MESSAGE_SIZE : int = 0x4B
    GUID_SIZE : int = 16
    other_guid : bytearray
    message_type : MessageType
    message : str
    SIZE : short = MESSAGE_SIZE + 4 + GUID_SIZE

    def __init__(self, packet_bytes : bytearray = None, guid : bytearray = None, message_type : MessageType = None, message : str = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.other_guid = guid
            self.message_type = message_type
            self.message = message

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        size : int = 0
        #data += self.other_guid

        while len(data) < self.GUID_SIZE:
            data += b"\x00"

        data += self.message_type.value.to_bytes(4, "little")

        for char in self.message:
            if size < self.MESSAGE_SIZE:
                data += char.encode()
                size += 1
            else:
                raise "Message too long exception"

        while len(data) < self.SIZE:
            data += b"\x00"
            size += 1
        if len(data) != self.SIZE:
            raise f"ChatMessagePacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data


    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

        offset = 0
        self.other_guid = data[offset:offset + self.GUID_SIZE]
        offset += self.GUID_SIZE
        self.message_type =  MessageType(int.from_bytes(data[offset:offset + 4], "little"))
        self.message = data[offset:offset + self.MESSAGE_SIZE].decode("utf8")
        offset += self.MESSAGE_SIZE
        self.message = self.message.strip()


class SlotDataPacket:
    cascade : int
    sand : int
    wooded : int
    lake : int
    lost : int
    metro : int
    seaside : int
    snow : int
    luncheon : int
    ruined : int
    bowser : int
    dark : int
    darker : int
    goal : int
    regionals : bool
    captures : bool
    entrance_randomization : bool
    SIZE : short = 30

    def __init__(self, packet_bytes : bytearray = None, cascade : int = None, sand : int = None, wooded : int = None,
                 lake : int = None, lost : int = None, metro : int = None, seaside : int = None, snow : int = None,
                 luncheon : int = None, ruined : int = None, bowser : int = None, dark : int = None, darker : int = None,
                 goal: int = None, regionals : bool = None, captures : bool = None, entrance_randomization : bool = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.cascade = cascade
            self.sand = sand
            self.wooded = wooded
            self.lake = lake
            self.lost = lost
            self.metro = metro
            self.seaside = seaside
            self.snow = snow
            self.luncheon = luncheon
            self.ruined = ruined
            self.bowser = bowser
            self.dark = dark
            self.darker = darker
            self.goal = goal
            self.regionals = regionals
            self.captures = captures
            self.entrance_randomization = entrance_randomization

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.cascade.to_bytes(2, "little")
        data += self.sand.to_bytes(2, "little")
        data += self.wooded.to_bytes(2, "little")
        data += self.lake.to_bytes(2, "little")
        data += self.lost.to_bytes(2, "little")
        data += self.metro.to_bytes(2, "little")
        data += self.seaside.to_bytes(2, "little")
        data += self.snow.to_bytes(2, "little")
        data += self.luncheon.to_bytes(2, "little")
        data += self.ruined.to_bytes(2, "little")
        data += self.bowser.to_bytes(2, "little")
        data += self.dark.to_bytes(2, "little")
        data += self.darker.to_bytes(2, "little")
        data += self.goal.to_bytes(1, "little")
        data += self.regionals.to_bytes(1, "little")
        data += self.captures.to_bytes(1, "little")
        data += self.entrance_randomization.to_bytes(1, "little")
        if len(data) != self.SIZE:
            raise f"CountsPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.cascade = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.sand = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.wooded = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.lake = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.lost = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.metro = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.seaside = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.snow = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.luncheon = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.ruined = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.bowser = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.dark = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.darker = int.from_bytes(data[offset:offset + 2], "little")
        offset += 2
        self.goal = int.from_bytes(data[offset:offset + 1], "little")
        offset += 1
        self.regionals = bool.from_bytes(data[offset:offset + 1], "little")
        offset += 1
        self.captures = bool.from_bytes(data[offset:offset + 1], "little")
        offset += 1
        self.entrance_randomization = bool.from_bytes(data[offset:offset + 1], "little")





#endregion

class ChangeStagePacket:
    ID_SIZE : int  = 0x10
    STAGE_SIZE : int = 0x30
    stage : str
    stage_id : str
    scenario : sbyte
    sub_scenario_type : byte
    SIZE : int = 0x42

    def __init__(self, packet_bytes = None , stage : str = "", stage_id : str = "", scenario : int = -1, sub_scenario_type : int = 0):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.stage = stage
            self.stage_id = stage_id
            self.scenario = c_byte(int(scenario))
            self.sub_scenario_type = c_ubyte(sub_scenario_type)

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.stage.encode()
        while len(data) < self.STAGE_SIZE:
            data += b"\x00"
        data += self.stage_id.encode()
        while len(data) < self.STAGE_SIZE + self.ID_SIZE:
            data += b"\x00"
        int_value : int = self.scenario.value
        data += int_value.to_bytes(1, "little", signed=True)
        int_value2 : int = self.sub_scenario_type.value
        data += int_value2.to_bytes(1, "little", signed=False)
        if len(data) != self.SIZE:
            raise f"ChangeStagePacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.stage = data[offset:self.STAGE_SIZE].decode()
        offset += self.STAGE_SIZE
        self.stage_id = data[offset:offset + self.ID_SIZE].decode()
        offset += self.ID_SIZE
        self.scenario = sbyte(int.from_bytes(data[offset:offset + 1], "little"))
        offset += 1
        self.sub_scenario_type = byte(int.from_bytes(data[offset:offset + 1], "little"))

class ApInfoPacket:
    INFO_SIZE : int = 64
    info_type : int = -1
    index1 : int = -1
    index2 : int = -1
    index3 : int = -1
    info : list[str] = []

    SIZE : short = INFO_SIZE * 3 + 8

    def __init__(self, info_type: int, index1 : int, index2 : int, index3 : int, info : list[str]):
        self.info_type = info_type
        self.index1 = index1
        self.index2 = index2
        self.index3 = index3
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.info_type.to_bytes(2,"little")
        data += self.index1.to_bytes(2,"little")
        data += self.index2.to_bytes(2,"little")
        data += self.index3.to_bytes(2,"little")
        # print(self.info_type)
        # print(self.index1)
        # print(self.index2)
        # print(self.index3)
        # print(self.info)

        for i in range(3):
            if i < len(self.info):
                if len(self.info[i]) > self.INFO_SIZE:
                    data += self.info[i][:self.INFO_SIZE].encode()
                else:
                    data += self.info[i].encode()

            while len(data) < 8 + self.INFO_SIZE * (i + 1):
                data += b"\x00"

        if len(data) != self.SIZE:
            raise f"ApInfoPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info_type = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index1 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index2 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.index3 = int.from_bytes(data[offset:2], "little")
        offset += 2
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))
        offset += self.INFO_SIZE
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))
        offset += self.INFO_SIZE
        self.info.append(data[offset:offset + self.INFO_SIZE].decode("utf-16"))

class ShopReplace:
    info_type : int = 255
    info : list[list[int]] = []

    SIZE : short = 177

    def __init__(self, info_type: int, info : list[list[int]]):
        self.info_type = info_type
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.info_type.to_bytes(1,"little", signed=False)

        for vals in self.info:
            for value in vals:
                data += value.to_bytes(1,"little", signed=False)

        while len(data) < self.SIZE:
            filler = 255
            data += filler.to_bytes(1, "little", signed=False)

        if len(data) != self.SIZE:
            raise f"ShopReplace failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info_type = data[offset]
        offset += 1
        for i in range(11):
            self.info.append([data[offset], data[offset+1], data[offset+2], data[offset+3]])
            offset += 4

class ShineReplace:
    info : dict[str | list[int]] = []

    SIZE : short = 200

    def __init__(self, info : dict[str | list[int]]):
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()

        for i in range(100):
            if i < len(self.info):
                data += self.info[str(i)][0].to_bytes(1,"little", signed=False)
                data += self.info[str(i)][1].to_bytes(1,"little", signed=False)

            else:
                filler = 127
                data += filler.to_bytes(1,"little", signed=True)
                filler = 255
                data += filler.to_bytes(1,"little", signed=False)

        if len(data) != self.SIZE:
            raise f"ShineReplace failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        for i in range(100):
            self.info[str(i)] = [data[offset], data[offset+1]]
            offset += 2

class ShineColor:
    info : list[list[int]] = []

    SIZE : short = 51*3

    def __init__(self, info : list[list[int]]):
        self.info = info

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()

        for i in range(51):
            if i < len(self.info):
                data += self.info[i][0].to_bytes(2,"little")
                data += self.info[i][1].to_bytes(1,"little", signed=True)

            else:
                filler = 0
                data += filler.to_bytes(2,"little")
                data += filler.to_bytes(1,"little", signed=True)

        if len(data) != self.SIZE:
            print(len(data))
            raise f"ShineColor failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset : int = 0
        self.info = []
        print(int.from_bytes(data[offset:offset+2], "little"))
        print(int.from_bytes(data[offset:offset+2], "little", signed=True))
        for i in range(83):
            self.info.append([int.from_bytes(data[offset:offset+2],"little", signed=True), data[offset+3]])
            offset += 3

class DeathLinkPacket:
    SIZE : short = 0x0

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

#region Connection Packets

class ConnectPacket:
    CLIENT_NAME_SIZE : int = 32
    connection_type : ConnectionType
    max_player_count : int = 8
    client_name : str = ""
    SIZE : short = 4 + 2 + CLIENT_NAME_SIZE


    def __init__(self, packet_bytes : bytearray = None , connection_type : ConnectionType = ConnectionType.Connect, max_players : int = 8, client_name = None):
        if packet_bytes:
            self.deserialize(packet_bytes)
        else:
            self.connection_type = connection_type
            self.max_player_count = max_players
            self.client_name = client_name

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        value = self.connection_type.value
        data += value.to_bytes(4,"little")
        data += self.max_player_count.to_bytes(2,"little")
        data += self.client_name.encode("utf-8")

        while len(data) < self.SIZE:
            data += b"\x00"

        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

        self.connection_type = ConnectionType(int.from_bytes(data[0:4],"little"))
        self.max_player_count = int.from_bytes(data[4:6], "little")
        self.client_name = data[6:].decode("utf-8")

class DisconnectPacket:
    # Empty Packet just to signal disconnect
    SIZE : short = 0

class ArchipelagoConnectPacket:
    host_name: str
    port: int
    slot_name: str
    password: str
    FIELD_SIZE = 64
    SIZE: short = 64 * 3 + 2

    def __init__(self, packet_bytes : bytearray = None):
        if packet_bytes:
            self.deserialize(packet_bytes)

    def serialize(self) -> bytearray:
        pass
        # data : bytearray = bytearray()

    def deserialize(self, data: bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)

        offset = 0
        self.host_name = data[offset:offset + self.FIELD_SIZE].decode(encoding="utf-8")
        count = 0
        for char in self.host_name:
            count += 1 if char != '\0' else 0
        self.host_name = self.host_name[0:count]
        offset += self.FIELD_SIZE
        self.port = int.from_bytes(data[offset:offset + 2], byteorder="little", signed=False)
        offset += 2
        self.slot_name = data[offset:offset + self.FIELD_SIZE].decode(encoding="utf-8")
        count = 0
        for char in self.slot_name:
            count += 1 if char != '\0' else 0
        self.slot_name = self.slot_name[0:count]
        offset += self.FIELD_SIZE
        self.password = data[offset:offset + self.FIELD_SIZE].decode(encoding="utf-8")
        count = 0
        for char in self.password:
            count += 1 if char != '\0' else 0
        self.password = self.password[0:count]
        offset += self.FIELD_SIZE



class InitPacket:
    max_players : int = 4
    server_version : str = "Archipelago"
    SERVER_VERSION_SIZE = 32
    SIZE : int = 2 + SERVER_VERSION_SIZE

    def serialize(self) -> bytearray:
        data : bytearray = bytearray()
        data += self.max_players.to_bytes(2, "little")
        data += self.server_version.encode("utf-8", "ignore")

        while len(data) < self.SIZE:
            data += b'\x00'

        if len(data) != self.SIZE:
            raise f"InitPacket failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data


    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        self.max_players = int.from_bytes(data[0:self.SIZE], "little")

#endregion

class PacketHeader:
    GUID_SIZE : int = 16
    guid : bytearray
    packet_type : PacketType
    packet_size : short
    SIZE : short = 16 + 2 + 2

    def __init__(self, header_bytes : bytearray = None, guid : bytearray = None,  packet_type : PacketType = PacketType.Init):
        if header_bytes:
            self.deserialize(header_bytes)
        else:
            self.guid = guid
            self.packet_type = packet_type

    def serialize(self) -> bytearray:
        data: bytearray = bytearray()
        data += self.guid

        while len(data) < self.GUID_SIZE:
            data += b"\x00"
        int_value: int = self.packet_type.value
        data += int_value.to_bytes(2, "little", signed=True)
        int_value2 : int = self.packet_size
        data += int_value2.to_bytes(2, "little", signed=True)
        if len(data) != self.SIZE:
            raise f"PacketHeader failed to serialize. bytearray is incorrect size {self.SIZE}."
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        if data is bytes:
            data = bytearray(data)
        offset = 0
        self.guid = data[offset:self.GUID_SIZE]
        offset += self.GUID_SIZE
        packet_type = int.from_bytes(data[offset:offset + 2], "little")

        offset += 2
        self.packet_size = short(int.from_bytes(data[offset:offset + 2], "little"))

        if packet_type <= PacketType.ArchipelagoConnect.value:
            self.packet_type = PacketType(packet_type)
        else:
            self.packet_type = PacketType(0)


class Packet:
    header : PacketHeader
    packet : Any
    max_size : int = 256 # max size without header

    def __init__(self, guid : bytearray, header_bytes : bytearray = None, packet_type : PacketType = PacketType.Connect, packet_data : list = None):
        if header_bytes:
            self.header = PacketHeader(header_bytes=header_bytes)
        else:
            self.header = PacketHeader(guid=guid, packet_type=packet_type)
            match packet_type:
                case PacketType.Connect:
                    self.packet = ConnectPacket()
                case PacketType.Init:
                    self.packet = InitPacket()
                case PacketType.ChangeStage:
                    self.packet = ChangeStagePacket(stage=packet_data[0], scenario=packet_data[1])
                case PacketType.SlotData:
                    self.packet = SlotDataPacket(cascade=packet_data[0], sand=packet_data[1], wooded=packet_data[2],
                        lake=packet_data[3], lost =packet_data[4], metro=packet_data[5], seaside=packet_data[6],
                        snow=packet_data[7], luncheon=packet_data[8], ruined=packet_data[9], bowser=packet_data[10],
                        dark=packet_data[11], darker=packet_data[12], goal=packet_data[13], regionals=packet_data[14], captures=packet_data[15],
                                                 entrance_randomization=packet_data[16])
                case PacketType.ArchipelagoChat:
                    self.packet = ChatMessagePacket(guid=packet_data[0], message_type=packet_data[1], message=packet_data[2])
                case PacketType.Check:
                    self.packet = CheckPacket(location_id=packet_data[0], item_type=packet_data[1], index=packet_data[2], obj_id=packet_data[3], stage=packet_data[4], amount=packet_data[5], sender_name=packet_data[6])
                case PacketType.DeathLink:
                    self.packet = DeathLinkPacket()
                case PacketType.SentChecks:
                    self.packet = SentChecksPacket(check_type=packet_data[0], checks=packet_data[1])
                case PacketType.ApInfo:
                    self.packet = ApInfoPacket(info_type=packet_data[0], index1=packet_data[1], index2=packet_data[2], index3=packet_data[3], info=packet_data[4])
                case PacketType.ShopReplace:
                    self.packet = ShopReplace(info_type=packet_data[0], info=packet_data[1])
                case PacketType.ShineReplace:
                    self.packet = ShineReplace(info=packet_data[0])
                case PacketType.ShineColor:
                    self.packet = ShineColor(info=packet_data[0])

    def serialize(self) -> bytearray:
        self.header.packet_size = self.packet.SIZE
        data : bytearray = bytearray()
        data += self.header.serialize()
        data += self.packet.serialize()
        return data

    def deserialize(self, data : bytes | bytearray) -> None:
        match self.header.packet_type:
            case PacketType.Connect:
                self.packet = ConnectPacket()
            # case PacketType.Command:
            #     self.packet = CommandP()
            case PacketType.Check:
                self.packet = CheckPacket(packet_bytes=data)
            case PacketType.ArchipelagoChat:
                self.packet = ChatMessagePacket(packet_bytes=data)
            case PacketType.SlotData:
                self.packet = SlotDataPacket(packet_bytes=data)
            case PacketType.DeathLink:
                self.packet = DeathLinkPacket()
            case PacketType.SentChecks:
                self.packet = SentChecksPacket(packet_bytes=data)
            case PacketType.ChangeStage:
                self.packet = ChangeStagePacket(packet_bytes=data)
            case PacketType.ArchipelagoConnect:
                self.packet = ArchipelagoConnectPacket(packet_bytes=data)

