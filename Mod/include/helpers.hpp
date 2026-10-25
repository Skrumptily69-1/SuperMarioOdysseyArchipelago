#pragma once

#include <string>
#include <cstring>
#include "types.h"

#include "sead/math/seadVector.h"
#include "sead/math/seadQuat.hpp"

#include "al/util.hpp"

#include "logger.hpp"
#include "puppets/PuppetInfo.h"

#include "game/GameData/GameDataFunction.h"

bool isPartOf(const char* w1, const char* w2);

int indexOf(char *w1, char c1);

void logVector(const char* vectorName, sead::Vector3f vector);

void logQuat(const char *quatName, sead::Quatf quat);

sead::Vector3f QuatToEuler(sead::Quatf *quat);

float vecMagnitude(sead::Vector3f const &input);

float quatAngle(sead::Quatf const &q1, sead::Quatf &q2);

bool isInCostumeList(const char *costumeName);
int getIndexCostumeList(const char *costumeName);

int getIndexStickerList(const char *stickerName);
int getIndexSouvenirList(const char *souvenirName);
int getIndexCaptureList(const char *captureName);
int getIndexMoonItemList(const char *moonItemName);

const char *tryGetPuppetCapName(PuppetInfo *info);
const char* tryGetPuppetBodyName(PuppetInfo* info);

const char* tryConvertName(const char* className);

void killMainPlayer(al::LiveActor* actor);
void killMainPlayer(PlayerActorHakoniwa* mainPlayer);

const char* intToCstr(int number);

__attribute__((used)) static const char* costumeNames[] = {
    "Mario",
    "MarioTailCoat",
    "MarioPrimitiveMan",
    "MarioPoncho",
    "MarioGunman",
    "MarioSwimwear",
    "MarioExplorer",
    "MarioScientist",
    "MarioPilot",
    "MarioMaker",
    "MarioGolf",
    "MarioSnowSuit",
    "MarioAloha",
    "MarioSailor",
    "MarioCook",
    "MarioPainter",
    "MarioArmor",
    "MarioHappi",
    "MarioSpaceSuit",
    "Mario64",
    "MarioShopman",
    "MarioNew3DS",
    "MarioMechanic",
    "MarioSuit",
    "MarioPirate",
    "MarioClown",
    "MarioFootball",
    "MarioColorClassic",
    "MarioColorLuigi",
    "MarioColorWario",
    "MarioColorWaluigi",
    "MarioColorGold",
    "MarioDoctor",
    "MarioDiddyKong",
    "MarioKoopa",
    "MarioPeach",
    "Mario64Metal",
    "MarioKing",
    "MarioTuxedo",
    "MarioCaptain",
    "MarioUnderwear",
    "MarioHakama",
    "MarioBone",
    "MarioInvisible"
};
// full costume list from 1.3
// attribute otherwise the build log is spammed with unused warnings
// __attribute__((used)) static const char* costumeNames[] = {
//     "Mario", "Mario3D", "Mario64", "Mario64Metal", "MarioAloha", "MarioArmor",
//     // "MarioArmorWestern", // DLC
//     "MarioBandman",
//     // "MarioBatter", // DLC
//     "MarioBone", "MarioCaptain", "MarioClown", "MarioColorClassic", "MarioColorGold", 
//     "MarioColorLuigi", "MarioColorWaluigi", "MarioColorWario",
//     // "MarioConductor", // DLC
//     "MarioCook", "MarioDiddyKong", "MarioDoctor", "MarioDot", "MarioDot3d", "MarioExplorer",
//     "MarioFootball", "MarioGolf", "MarioGunman", "MarioHakama", "MarioHappi",
//     // "MarioHariet", // DLC
//     // "MarioHigh",
//     "MarioKing", "MarioKoopa", "MarioMaker", "MarioMechanic", "MarioNew3DS", "MarioPainter",
//     "MarioPeach", "MarioPilot", "MarioPirate", "MarioPoncho", "MarioPrimitiveMan", "MarioRacer",
//     //"MarioRango", // DLC
//     //"MarioRsv", // DLC
//     "MarioSailor", "MarioSanta",
//     // "MarioSatellite", // DLC
//     "MarioScientist", "MarioShopman", "MarioSnowSuit", "MarioSpaceSuit",
//     // "MarioSpewart", // DLC
//     "MarioSuit",
//     // "MarioSunshine", // DLC
//     "MarioSwimwear",
//     // "MarioTopper", // DLC
//     "MarioTuxedo",
//     // "MarioZombie" // DLC
// };

__attribute__((used)) static const char* stickerNames[] = {
    "StickerCap",
    "StickerWaterfall",
    "StickerSand",
    "StickerLake", 
    "StickerForest",
    "StickerClash",
    "StickerCity",
    "StickerSnow",
    "StickerSea",
    "StickerLava",
    "StickerSky",
    "StickerMoon",
    "StickerPeachDokan",
    "StickerPeachCoin",
    "StickerPeachBlock",
    "StickerPeachBlockQuestion",
    "StickerPeach"
};

__attribute__((used)) static const char* souvenirNames[] = {
    "SouvenirHat1",
    "SouvenirHat2",
    "SouvenirFall1",
    "SouvenirFall2",
    "SouvenirSand1",
    "SouvenirSand2",
    "SouvenirLake1",
    "SouvenirLake2",
    "SouvenirForest1",
    "SouvenirForest2",
    "SouvenirCrash1",
    "SouvenirCrash2",
    "SouvenirCity1",
    "SouvenirCity2", 
    "SouvenirSnow1",
    "SouvenirSnow2",
    "SouvenirSea1", 
    "SouvenirSea2", 
    "SouvenirLava1",
    "SouvenirLava2",
    "SouvenirSky1",
    "SouvenirSky2",
    "SouvenirMoon1",
    "SouvenirMoon2",
    "SouvenirPeach1",
    "SouvenirPeach2"
};

__attribute__((used)) static const char* moonItemNames[] = {
    "MoonCity", // 101
    "MoonForest", // 138
    "MoonWaterfall", //211   
    "MoonCap",  //230
    "MoonLava", // 294
    "MoonSky",  // 360
    "MoonClash",// 398
    "MoonLake", // 430
    "MoonSea",  // 460
    "MoonSand", // 565
    "MoonSnow", // 868
    "MoonPeach", // 933
    "MoonMoon" // 1157
};

__attribute__((used)) static const char* captureListNames[] = {
    "Frog",
    "ElectricWire", // Spark pylon
    "KuriboWing", // Paragoomba
    "Wanwan",   // Chain Chomp
    "WanwanBig", // Big Chain Chomp
    "BreedaWanwan", // Broode's Chain Chomp
    "TRex",
    "Fukankun", // Binoculars
    "Killer", // Bullet Bill
    "Megane", // Moe-eye
    "Cactus", 
    "Kuribo", // Goomba
    "BossKnuckleHand", // Knucklotec's Fist
    "BazookaElectric", // Mini Rocket
    "Kakku", // Glydon
    "JugemFishing", // Lakitu
    "Fastener", // Zipper
    "Pukupuku", // Cheep Cheep
    "GotogotonLake", // Puzzle Part (Lake Kingdom)
    "PackunPoison", // Poison Pirana Plant
    "Senobi", // Uproot
    "FireBros", // Fire Bro
    "Tank", // Sherm
    "Gamane", // Coin Coffer
    "Tree",
    "RockForest", // Boulder
    "FukuwaraiFacePartsKuribo", // Gooma Picture Match Piece
    "Imomu", // Tropical Wiggler
    "Guidepost", // Pole
    "Manhole",
    "Car", // Taxi
    "Radicon", // RC Car
    "Byugo", //Ty-foo
    "Yukimaru", // Shiverian Racer
    "PukupukuSnow", // Cheep Cheep (Snow Kingdom)
    "Hosui", // Gushen
    "Bubble", // Lava Bubble
    "HackFork", // Volbonan
    "HammerBros", // Hammer and Pan Bros
    "CarryMeat", // Meat
    "PackunFire", // Fire Pirana Plant
    "Tsukkun", // Pokio
    "Statue", // Jizo
    "StatueKoopa", // Bowser Statue
    "KaronWing", // Para Bones
    "KillerMagnum", // Bonsai Bill
    "Bull", // Chargin' Chuck
    "Koopa", // Bowser
    "AnagramAlphabetCharacter", // Letter
    "GotogotonCity", // Puzzle Part (Metro Kingdom)
    "FukuwaraiFacePartsMario", // Mario Picture Match Piece
    "Yoshi",
};

__attribute__((used)) static const char* changeStageIdList[] = {
    "EX_AnimalChase",
    "bikereturn",
    "bike",
    "BossRaidWorldMoonEx02_Enter",
    "BossRaidWorldMoonEx02_Exit",
    "BossRaidWorldMoonEx02_Enter",
    "BossRaidWorldMoonEx02_Exit",
    "ByugoPuzzle",
    "CapAppearExExit",
    "CapAppearExEnt",
    "LavaLiftEx",
    "LavaLiftExdokan",
    "kaitendokan",
    "start",
    "Ex",
    "Goal",
    "PushBlockExStageEnt",
    "PoisonWaveExEnt",
    "FrogSearchExStageEnt",
    "PushBlockExStageEntDokan",
    "rollinggoal",
    "rollingstart",
    "Ex",
    "Goal",
    "gunsyu",
    "gunsyudokan",
    "under001enter",
    "main_enter",
    "main_exit",
    "shop_corect",
    "shop_coin",
    "onpu",
    "bou",
    "car",
    "under001enter",
    "densen",
    "Bonus",
    "kaitendokan",
    "bike02",
    "gunsyu",
    "taxi",
    "theater",
    "under001enter",
    "boureturn",
    "kaitendokan",
    "densendokan",
    "gunsyudokan",
    "bike02return",
    "gragra",
    "bike",
    "gragrareturn",
    "donsuke",
    "bikereturn",
    "main_exit",
    "main_enter",
    "Bonus",
    "shop_coin",
    "shop_corect",
    "Kinopio",
    "ClashWorldMoonEX2",
    "imomu_01",
    "imomu_02",
    "Kinopio",
    "Fukuwarai",
    "cube",
    "cube",
    "donsuke",
    "PeachWorldEx2a",
    "densen",
    "densendokan",
    "FastenerEx",
    "bonus",
    "bonus2",
    "boss001",
    "boss001",
    "EXCloud",
    "Tower001",
    "boss001",
    "Jyukai001",
    "Jyukai003",
    "EX_Tankuro",
    "EX_RailCollision",
    "Tower002",
    "Tower002",
    "EXCloud",
    "EX_Water_Exit",
    "boss002",
    "bonus2",
    "EX_RailCollision_Exit",
    "EX_Tankuro_Exit",
    "EX_Water",
    "bonus",
    "EX_AnimalChase",
    "PoisonEx",
    "PoisonEx_Exit",
    "KillerRoad",
    "Tower002",
    "Tower001",
    "EX_Water_Exit",
    "EX_Water",
    "Explorer_Bonus",
    "Jyukai001v",
    "Jyukai002",
    "Jyukai004",
    "Jyukai003v",
    "TreasureTree",
    "TreasureTree",
    "ForkEX",
    "ForkEX2",
    "LakeWorldMoonEX1a",
    "LakeWorldMoonEX1b",
    "FrogSearchExStageEnt",
    "Fukuwarai",
    "GabuzouClockExdokan",
    "GabuzouClockEx",
    "dot01",
    "dot00",
    "Goton",
    "HomeEntrance",
    "FigureWalker",
    "EX_IceWater",
    "EX_IceWater_Exit",
    "EX_IceWaterDash",
    "EX_IceWaterDash_Exit",
    "imomu_01",
    "imomu_02",
    "ClashWorldMoonEX2",
    "jizo01",
    "jizo02",
    "Patakaron02",
    "EX_RailCol2",
    "EX_RailCol2_Exit",
    "KillerRoad",
    "LakeWorldMoonEX1a",
    "LakeWorldMoonEX1b",
    "LakeWorldShop",
    "PechoBubbleEx",
    "PechoBubbleExDokan",
    "BBQEx",
    "BBQExDokan",
    "CostumeEventWorldLava",
    "CostumeOut",
    "MartinCubeEx",
    "FenceLiftExdokan",
    "FenceLiftEx",
    "ForkEX",
    "KeyMoveEx",
    "PechoBubbleEx",
    "MartinCubeEx",
    "KeyMoveExDokan",
    "PechoBubbleExDokan",
    "BBQExDokan",
    "CostumeOut",
    "FenceLiftEx",
    "FenceLiftExdokan",
    "LavaLiftEx",
    "LavaLiftExdokan",
    "GabuzouClockEx",
    "GabuzouClockExdokan",
    "shop",
    "TreasureEventWorldLava",
    "KeyMoveEx",
    "KeyMoveExDokan",
    "Lift2D",
    "Lift2DExit",
    "meganelift01",
    "meganelift02",
    "moon",
    "moon_exit",
    "bbb",
    "vvv",
    "aaa",
    "bbb",
    "ccc",
    "fff",
    "ggg",
    "ddd",
    "vvv",
    "moon",
    "dot00",
    "dot01",
    "moon_exit",
    "None",
    "None",
    "ddd",
    "ggg",
    "aaa",
    "onpu",
    "PoisonEx",
    "PoisonEx_Exit",
    "PeachCastleGate",
    "PeachCastleGate",
    "PeachWorldShopA",
    "BossMagmaA",
    "MofumofuA",
    "BossKnuckleA",
    "BossForestA",
    "PeachWorldEx2a",
    "PeachWorldEx1a",
    "GiantWanderBossA",
    "BossRaidA",
    "GiantWanderBossB",
    "BossRaidB",
    "PeachWorldEx2a",
    "BossForestA",
    "BossKnuckleA",
    "BossMagmaA",
    "BossRaidB",
    "BossRaidA",
    "GiantWanderBossB",
    "GiantWanderBossA",
    "MofumofuA",
    "PeachWorldShopA",
    "PoisonWaveExEnt",
    "PoisonWaveExExit",
    "bou",
    "boureturn",
    "PushBlockExStageEnt",
    "PushBlockExStageEntDokan",
    "car",
    "EX_RailCollision",
    "EX_RailCollision_Exit",
    "SeaWorldMoonEX1b",
    "SeaWorldMoonEX1a",
    "rocket",
    "rollingstart",
    "rollinggoal",
    "abc",
    "arijigoku",
    "doukutu1",
    "aaa",
    "pyramid01",
    "wall",
    "pyramid02",
    "pyramid03",
    "pyramid04",
    "bar2",
    "hide",
    "icestart",
    "pyramid04",
    "start",
    "pyramid01",
    "anki2",
    "arijigoku2",
    "run00",
    "arijigoku1",
    "doukutu2",
    "shindo",
    "Under01",
    "Out",
    "meganelift01",
    "meganelift02",
    "rocket",
    "EX_2DHosui",
    "EX_2DHosui_Exit",
    "doukutu1",
    "doukutu2",
    "wall",
    "anki2",
    "arijigoku2",
    "arijigoku1",
    "pyramid01",
    "pyramid04",
    "hide",
    "bar1",
    "town",
    "run00",
    "run00return",
    "Yadokari00",
    "Under01",
    "Yadokari00",
    "shindo",
    "CostumeEventSeaWorld",
    "shindo_Lv2",
    "SeaWorldMoonEX2",
    "SeaWorldMoonEX1a",
    "SeaWorldMoonEX1b",
    "TreasureEventWorldSea",
    "RoomEventWorldSea",
    "PukupukuCaveStart",
    "PukupukuCaveGoal",
    "shindo_Lv2",
    "SeaWorldEX3a",
    "SeaWorldEX3b",
    "taxireturn",
    "taxi",
    "EX_Tankuro",
    "EX_Tankuro_Exit",
    "sora001",
    "sora001",
    "sora001",
    "sora001",
    "sora001",
    "sora001",
    "sora001",
    "byoubu",
    "shop",
    "shop",
    "shop_dress",
    "EX_SkyBonus",
    "SnowCostumeEx",
    "EX_IceWaterDash",
    "SnowUGEnt",
    "ByugoPuzzle",
    "FigureWalker",
    "EX_SkyBonus",
    "MoonRace",
    "SnowUGExit",
    "EX_IceWater_Exit",
    "EX_IceWaterDash_Exit",
    "EX_RailCol2_Exit",
    "EX_RailCol2",
    "RaceTrackExit",
    "MoonRace",
    "ShopDoor",
    "RaceEntrance",
    "RaceTrackExit",
    "StackerRoomStart",
    "StackerRoomGoal",
    "BombTailRoomStart",
    "FireBlowerRoomStart",
    "CapThrowerRoomStart",
    "BombTailRoomGoal",
    "FireBlowerRoomGoal",
    "CapThrowerRoomGoal",
    "BikeSteelNoCapEx_Exit",
    "PackunPoisonNoCapEx_Exit",
    "ShootingCityYoshiEx",
    "SenobiTowerYoshiEx",
    "LavaWorldUpDownYoshiEx",
    "SenobiTowerYoshiEx_Exit",
    "LavaWorldUpDownYoshiEx_Exit",
    "ShootingCityYoshiEx_Exit",
    "BombTailRoomGoal",
    "BombTailRoomStart",
    "CapThrowerRoomStart",
    "CapThrowerRoomGoal",
    "FireBlowerRoomGoal",
    "FireBlowerRoomStart",
    "StackerRoomGoal",
    "StackerRoomStart",
    "room2_start",
    "CP_Entrance",
    "MoonGoal",
    "room3_goal",
    "CP_Entrance",
    "room2_start",
    "room2_goal",
    "MoonGoal",
    "gragra",
    "gragrareturn",
    "theater",
    "SeaWorldMoonEX2",
    "CapTrampolineA",
    "CapTrampolineB",
    "bike02",
    "bike02return",
    "RexPoppunEx",
    "tukkun001_enter",
    "tukkun001_exit",
    "tukkun000_enter",
    "tukkun000_exit",
    "WanwanExStart",
    "WanwanExGoal",
    "Lift2D",
    "RexPoppunEx",
    "WanwanExStart",
    "WanwanExGoal",
    "Lift2DExit",
    "CapAppearExExit",
    "WindBlowExStart",
    "WindBlowExGoal",
    "CapAppearExEnt",
    "EX_2DHosui",
    "EX_2DHosui_Exit",
    "SeaWorldEX1a",
    "SeaWorldEX1b",
    "WindBlowExStart",
    "WindBlowExGoal",
    "PeachWorldEx1a",
};

__attribute__((used)) static const char* changeStageNameList[] = {
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
};

struct stageConnection {
    //short fromStageIdIndex;
    //short fromStageNameIndex;
    short toStageIdIndex;
    short toStageNameIndex;
};

struct shineReplaceText {
    s8 itemType;
    u8 shineItemNameIndex;
    //s8 color;
};

struct shopReplaceText {
    u8 gameIndex;
    u8 slotIndex;
    u8 apItemNameIndex;
    u8 itemClassification;
};

struct HackActorName {
    const char *className;
    const char *hackName;
};

// attribute otherwise the build log is spammed with unused warnings
__attribute__((used)) static HackActorName classHackNames[] = {
    {"SenobiGeneratePoint", "Senobi"},
    {"KuriboPossessed", "Kuribo"},
    {"KillerLauncher", "Killer"},
    {"KillerLauncherMagnum", "KillerMagnum"},
    {"FireBrosPossessed", "FireBros"},
    {"HammerBrosPossessed", "HammerBros"},
    {"ElectricWire", "ElectricWireMover"},
    {"TRexSleep", "TRex"},
    {"TRexPatrol", "TRex"},
    {"WanwanBig", "Wanwan"},  // FIXME: this will make chain chomp captures always be the small
                              // variant for syncing
    {"Koopa","KoopaHack"}
};

struct Transform
{
    sead::Vector3f *position;
    sead::Quatf *rotation;
};

// From Boss Room Unity Example
class VisualUtils
{

public:
    /* 
    * @brief Smoothly interpolates towards the parent transform.
    * @param moveTransform The transform to interpolate
    * @param targetTransform The transform to interpolate towards.
    * @param timeDelta Time in seconds that has elapsed, for purposes of interpolation.
    * @param closingSpeed The closing speed in m/s. This is updated by SmoothMove every time it is called, and will drop to 0 whenever the moveTransform has "caught up". 
    * @param maxAngularSpeed The max angular speed to to rotate at, in degrees/s.
    */
    static float SmoothMove(Transform moveTransform, Transform targetTransform, float timeDelta,
                            float closingSpeed, float maxAngularSpeed);

    constexpr static const float k_MinSmoothSpeed = 0.1f;
    constexpr static const float k_TargetCatchupTime = 0.2f;
};