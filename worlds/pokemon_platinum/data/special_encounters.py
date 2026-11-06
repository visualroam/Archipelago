# THIS IS AN AUTO-GENERATED FILE. DO NOT MODIFY.
# data_gen_templates/special_encounters.py
#
# Copyright (C) 2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Sequence, Set
from typing import Tuple

regular_honey_tree: Sequence[str] = [
    "combee",
    "wurmple",
    "burmy",
    "cherubi",
    "aipom",
    "heracross",
]

munchlax_honey_tree: Sequence[str] = [
    "munchlax",
]

trophy_garden: Sequence[str] = [
    "eevee",
    "bonsly",
    "happiny",
    "meowth",
    "cleffa",
    "clefairy",
    "igglybuff",
    "plusle",
    "jigglypuff",
    "ditto",
    "castform",
    "minun",
    "mime_jr",
    "marill",
    "chansey",
    "azurill",
]

great_marsh_observatory: Sequence[str] = [
    "carnivine",
    "skorupi",
    "croagunk",
    "quagsire",
    "yanma",
    "tropius",
    "tangela",
    "wooper",
]

great_marsh_observatory_national_dex: Sequence[str] = [
    "toxicroak",
    "kecleon",
    "drapion",
    "kangaskhan",
    "paras",
    "exeggcute",
    "shroomish",
    "gulpin",
]

feebas_fishing: Sequence[str] = [
    "feebas",
]

odd_keystone: Sequence[str] = [
    "spiritomb",
]

roamers: Sequence[str] = [
    "mesprit",
    "cresselia",
    "darkrai",
    "moltres",
    "zapdos",
    "articuno",
]

requiring_national_dex: Set[str] = {"roamers", "great_marsh_observatory_national_dex", "trophy_garden"}

def encounter_string_to_key(s: str) -> Tuple[str, int]:
    i = s.rfind("_")
    return s[:i], int(s[i + 1:])
