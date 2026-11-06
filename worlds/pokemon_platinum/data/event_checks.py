# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/event_checks.py
#
# Copyright (C) 2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Mapping
from .locations import LocationCheck, VarCheck, FlagCheck, OnceCheck
import operator

event_checks: Mapping[str, LocationCheck] = {
    "fen_badge": FlagCheck(id=0x9C),
    "met_oak_pal_park": FlagCheck(id=0x242, invert=True),
    "lake_verity_defeat_mars": FlagCheck(id=0xBA),
    "lake_explosion": FlagCheck(id=0xBC2),
    "forest_badge": FlagCheck(id=0x74),
    "cobble_badge": FlagCheck(id=0x9D),
    "galactic_hq_defeat_cyrus": FlagCheck(id=0x235),
    "lake_valor_defeat_saturn": FlagCheck(id=0x13E),
    "lake_acuity_meet_jupiter": FlagCheck(id=0x1B9),
    "icicle_badge": FlagCheck(id=0x9E),
    "eterna_defeat_team_galactic": FlagCheck(id=0x1FD),
    "relic_badge": FlagCheck(id=0x7D),
    "coal_badge": FlagCheck(id=0x75),
    "beacon_badge": FlagCheck(id=0xB6),
    "mine_badge": FlagCheck(id=0x92),
    "beat_cynthia": FlagCheck(id=0x964),
    "distortion_world": FlagCheck(id=0x28F),
    "valley_windworks_defeat_team_galactic": FlagCheck(id=0x1A5),
    "stark_mountain_arrest_team_galactic": FlagCheck(id=0xD6),
    "activate_roaming_moltres_zapdos_articuno": FlagCheck(id=0x99),
    "activate_roaming_cresselia": FlagCheck(id=0x11F),
    "activate_roaming_mesprit": VarCheck(id=0x4059, value=0x4, op=operator.ne),
    "talk_looker_veilstone_galactic": VarCheck(id=0x411F, value=0x3),
    "saw_route_210_barricade": FlagCheck(id=0xBDB),
    "saw_route_215_west_barricade": FlagCheck(id=0xBDC),
    "saw_route_207_barricade": FlagCheck(id=0xBDD),
    "saw_boat_canalave_snowpoint": FlagCheck(id=0xBDE),
    "saw_boat_canalave_pastoria": FlagCheck(id=0xBDF),
    "saw_boat_pastoria_snowpoint": FlagCheck(id=0xBE0),
    "saw_pastoria_barriers": FlagCheck(id=0xBE1),
    "saw_early_sunyshore": FlagCheck(id=0xBE2),
}
