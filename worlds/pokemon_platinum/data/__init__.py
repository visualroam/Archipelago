# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/__init__.py
#
# Copyright (C) 2025-2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Mapping
from enum import StrEnum

class Hm(StrEnum):
    CUT = "HM01 Cut"
    FLY = "HM02 Fly"
    SURF = "HM03 Surf"
    STRENGTH = "HM04 Strength"
    DEFOG = "HM05 Defog"
    ROCK_SMASH = "HM06 Rock Smash"
    WATERFALL = "HM07 Waterfall"
    ROCK_CLIMB = "HM08 Rock Climb"
    FLASH = "TM70 Flash"

    def badge_item(self) -> str | None:
        match self:
            case Hm.CUT: return "Forest Badge"
            case Hm.FLY: return "Cobble Badge"
            case Hm.SURF: return "Fen Badge"
            case Hm.STRENGTH: return "Mine Badge"
            case Hm.DEFOG: return "Relic Badge"
            case Hm.ROCK_SMASH: return "Coal Badge"
            case Hm.WATERFALL: return "Beacon Badge"
            case Hm.ROCK_CLIMB: return "Icicle Badge"
            case _: return None

    def tmhm_id(self) -> int:
        match self:
            case Hm.CUT: return 92
            case Hm.FLY: return 93
            case Hm.SURF: return 94
            case Hm.STRENGTH: return 95
            case Hm.DEFOG: return 96
            case Hm.ROCK_SMASH: return 97
            case Hm.WATERFALL: return 98
            case Hm.ROCK_CLIMB: return 99
            case Hm.FLASH: return 69

map_header_labels: Mapping[str, str] = {
    "canalave_city": "Canalave City",
    "eterna_city": "Eterna City",
    "pastoria_city": "Pastoria City",
    "sunyshore_city": "Sunyshore City",
    "pokemon_league": "Pokemon League",
    "oreburgh_mine_b1f": "Oreburgh Mine",
    "oreburgh_mine_b2f": "Oreburgh Mine Basement",
    "valley_windworks_outside": "Valley Windworks",
    "eterna_forest": "Eterna Forest",
    "fuego_ironworks_outside": "Fuego Ironworks",
    "mt_coronet_1f_south": "Mt. Coronet South",
    "mt_coronet_2f": "Mt. Coronet 2nd Floor",
    "mt_coronet_3f": "Mt. Coronet 3rd Floor",
    "mt_coronet_outside_north": "Mt. Coronet Outside (North)",
    "mt_coronet_outside_south": "Mt. Coronet Outside (South)",
    "mt_coronet_4f_rooms_1_and_2": "Mt. Coronet 4th Floor First Part",
    "mt_coronet_4f_room_3": "Mt. Coronet 4th Floor Second Part",
    "mt_coronet_5f": "Mt. Coronet 5th Floor",
    "mt_coronet_6f": "Mt. Coronet 6th Floor",
    "mt_coronet_1f_tunnel_room": "Mt. Coronet Tunnel up to Northern Part",
    "mt_coronet_1f_north_room_2": "Mt. Coronet Northernmost Room",
    "mt_coronet_1f_north_room_1": "Mt. Coronet North",
    "mt_coronet_b1f": "Mt. Coronet Basement",
    "solaceon_ruins_maniac_tunnel_room": "Solaceon Ruins Maniac Tunnel Room",
    "solaceon_ruins_room_2_northeast_dead_end": "Solaceon Ruins Norheast Dead-end of 2nd Room",
    "solaceon_ruins_room_1_northwest_dead_end": "Solaceon Ruins Northwest Dead-end of 1st Room",
    "solaceon_ruins_room_2": "Solaceon Ruins 2nd Room",
    "solaceon_ruins_room_1_southeast_dead_end": "Solaceon Ruins Southeast Dead-end of 1st Room",
    "solaceon_ruins_room_3": "Solaceon Ruins 3rd Room",
    "solaceon_ruins_room_2_southeast_dead_end": "Solaceon Ruins Southeast Dead-end of 2nd Room",
    "solaceon_ruins_room_6_southeast_dead_end": "Solaceon Ruins Southeast Dead-end of 6th Room",
    "solaceon_ruins_room_5_southwest_dead_end": "Solaceon Ruins Southwest Dead-end of 5th Room",
    "solaceon_ruins_room_3_northwest_dead_end": "Solaceon Ruins Northwest Dead-end of 3rd Room",
    "solaceon_ruins_room_3_southwest_dead_end": "Solaceon Ruins Southwest Dead-end of 3rd Room",
    "solaceon_ruins_room_4": "Solaceon Ruins 4th Room",
    "solaceon_ruins_room_6": "Solaceon Ruins 6th Room",
    "solaceon_ruins_room_5": "Solaceon Ruins 5th Room",
    "solaceon_ruins_room_7": "Solaceon Ruins 7th Room",
    "solaceon_ruins_room_4_southeast_dead_end": "Solaceon Ruins Southeast Dead-end of 4th Room",
    "solaceon_ruins_room_6_northwest_dead_end": "Solaceon Ruins Northwest Dead-end of 6th Room",
    "victory_road_1f": "Victory Road 1st Floor",
    "victory_road_2f": "Victory Road 2nd Floor",
    "victory_road_b1f": "Victory Road Basement",
    "victory_road_1f_room_1": "Victory Road Post-game Area 1",
    "victory_road_1f_room_2": "Victory Road Post-game Area 2",
    "victory_road_1f_room_3": "Victory Road Post-game Area 3",
    "ravaged_path": "Ravaged Path",
    "oreburgh_gate_1f": "Oreburgh Gate",
    "oreburgh_gate_b1f": "Oreburgh Gate Basement",
    "stark_mountain_outside": "Stark Mountain Outside",
    "stark_mountain_room_1": "Stark Mountain 1st Room",
    "stark_mountain_room_2": "Stark Mountain 2nd Room",
    "sendoff_spring": "Sendoff Spring",
    "snowpoint_temple_1f": "Snowpoint Temple 1st Floor",
    "snowpoint_temple_b1f": "Snowpoint Temple 1st Basement",
    "snowpoint_temple_b2f": "Snowpoint Temple 2nd Basement",
    "snowpoint_temple_b3f": "Snowpoint Temple 3rd Basement",
    "snowpoint_temple_b4f": "Snowpoint Temple 4th Basement",
    "snowpoint_temple_b5f": "Snowpoint Temple 5th Basement",
    "wayward_cave_1f": "Wayward Cave",
    "wayward_cave_b1f": "Wayward Cave Basement",
    "trophy_garden": "Trophy Garden",
    "iron_island": "Iron Island Outside",
    "iron_island_1f": "Iron Island 1st Floor",
    "iron_island_b1f_left_room": "Iron Island 1st Basement Left",
    "iron_island_b1f_right_room": "Iron Island 1st Basement Right",
    "iron_island_b2f_right_room": "Iron Island 2nd Basement Right",
    "iron_island_b2f_left_room": "Iron Island 2nd Basement Left",
    "iron_island_b3f": "Iron Island 3rd Basement",
    "old_chateau": "Old Chateau",
    "old_chateau_dining_area": "Old Chateau Dining Area",
    "old_chateau_side_rooms": "Old Chateau Side Rooms",
    "old_chateau_corridor": "Old Chateau Corridor",
    "old_chateau_back_west_room": "Old Chateau Back West Room",
    "old_chateau_back_middle_west_room": "Old Chateau Back Middle West Room",
    "old_chateau_back_middle_room": "Old Chateau Back Middle Room",
    "old_chateau_middle_east_room": "Old Chateau Middle East Room",
    "old_chateau_back_middle_east_room": "Old Chateau Back Middle East Room",
    "old_chateau_back_east_room": "Old Chateau Back East Room",
    "lake_verity": "Lake Verity",
    "lake_valor": "Lake Valor",
    "lake_acuity": "Lake Acuity",
    "valor_lakefront": "Valor Lakefront",
    "acuity_lakefront": "Acuity Lakefront",
    "route_201": "Route 201",
    "route_202": "Route 202",
    "route_203": "Route 203",
    "route_204_south": "Route 204 South",
    "route_204_north": "Route 204 North",
    "route_205_south": "Route 205 South",
    "route_205_north": "Route 205 North",
    "route_206": "Route 206",
    "route_207": "Route 207",
    "route_208": "Route 208",
    "route_209": "Route 209",
    "route_209_lost_tower_1f": "Lost Tower 1st Floor",
    "route_209_lost_tower_2f": "Lost Tower 2nd Floor",
    "route_209_lost_tower_3f": "Lost Tower 3rd Floor",
    "route_209_lost_tower_4f": "Lost Tower 4th Floor",
    "route_209_lost_tower_5f": "Lost Tower 5th Floor",
    "route_210_south": "Route 210 South",
    "route_210_north": "Route 210 North",
    "route_211_west": "Route 211 West",
    "route_211_east": "Route 211 East",
    "route_212_north": "Route 212 North",
    "route_212_south": "Route 212 South",
    "route_213": "Route 213",
    "route_214": "Route 214",
    "route_215": "Route 215",
    "route_216": "Route 216",
    "route_217": "Route 217",
    "route_218": "Route 218",
    "route_219": "Route 219",
    "route_221": "Route 221",
    "route_222": "Route 222",
    "route_224": "Route 224",
    "route_225": "Route 225",
    "route_227": "Route 227",
    "route_228": "Route 228",
    "route_229": "Route 229",
    "twinleaf_town": "Twinleaf Town",
    "celestic_town": "Celestic Town",
    "resort_area": "Resort Area",
    "route_220": "Route 220",
    "route_223": "Route 223",
    "route_226": "Route 226",
    "route_230": "Route 230",
    "great_marsh_1": "Great Marsh 1st Area",
    "great_marsh_2": "Great Marsh 2nd Area",
    "great_marsh_3": "Great Marsh 3rd Area",
    "great_marsh_4": "Great Marsh 4th Area",
    "great_marsh_5": "Great Marsh 5th Area",
    "great_marsh_6": "Great Marsh 6th Area",
    "maniac_tunnel": "Maniac Tunnel",
    "solaceon_ruins_room_5_southeast_deadend": "Solaceon Ruins Southeast Dead-end of 5th Room",
    "eterna_forest_outside": "Eterna Forest Outside",
    "floaroma_meadow": "Floaroma Meadow",
}
