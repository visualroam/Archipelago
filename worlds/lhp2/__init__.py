import settings

from typing import Dict, ClassVar, Any, Union
from settings import FilePath

from BaseClasses import Item, Tutorial, ItemClassification
from Options import OptionError
from .Items import LHP2Item, item_data_table, horcrux_names_set, progression_spells, item_name_groups, setup_items
from .Locations import all_location_table, LocationData, setup_locations, location_name_groups
from .Data import ItemName, RegionName
from .Options import LHP2Options
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld, CollectionState


class UTPackPath(FilePath):
    required = False


class LHP2Settings(settings.Group):
    ut_pack_path: Union[UTPackPath, str] = UTPackPath()


class LHP2Web(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Lego Harry Potter 5-7 Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["jrad"]
    )]


def lhp2_map_to_tab_index(data: Any) -> int:
    if data is None or data == "" or data == b"":
        return 0
    try:
        if isinstance(data, str):
            data = data.strip()
            if not data:
                return 0
        map_id = int(data) if not isinstance(data, int) else data
    except (ValueError, TypeError):
        return 0
 
    # Raw game map ID -> hub offset
    # Multiple IDs per area due to Y5/Y6/Y7/Y8 variants
    raw_id_to_hub_offset = {
        # Tent
        4:   0,  98:  0,
        # Wilderness
        5:   1,  99:  1,
        # Cafe
        6:   2,  100: 2,
        # London
        8:   3,  103: 3,  173: 3,  276: 3,
        # King's Cross
        9:   4,  104: 4,  174: 4,  277: 4,
        # Hogsmeade Path
        11:  5,  106: 5,  176: 5,
        # Hogsmeade
        12:  6,  107: 6,  177: 6,
        # Hogsmeade Station
        13:  7,  108: 7,  179: 7,  280: 7,
        # Hogwarts Path
        14:  8,  109: 8,  180: 8,  282: 8,
        # Greenhouse
        15:  9,  110: 9,  181: 9, 283: 9,
        # Training Grounds
        16: 10,  111: 10, 182: 10, 284: 10,
        # Quad
        17: 11,  112: 11, 184: 11, 285: 11,
        # Room of Requirement Corridor
        18: 12,  114: 12, 185: 12, 288: 12,
        # Weasley Courtyard Storage
        19: 13,  115: 13, 186: 13, 289: 13,
        # Weasley Courtyard
        20: 14,  116: 14, 187: 14, 290: 14,
        # Great Hall
        21: 15,  117: 15, 188: 15, 292: 15,
        # Great Hall Lobby
        22: 16,  118: 16, 189: 16, 293: 16,
        # Black Lake
        23: 17,
        # Quidditch Pitch
        24: 18,
        # Thestral Forest
        25: 19,  119: 19, 190: 19, 295: 19,
        # Hogwarts Grounds
        26: 20,  120: 20, 191: 20, 296: 20,
        # Ravenclaw Tower
        27: 21,  121: 21, 192: 21,
        # Gryffindor Common Room
        28: 22,  122: 22, 193: 22, 297: 22,
        # Dorm Lobby (also Slytherin/Hufflepuff Common)
        29: 23,  123: 23, 194: 23, 298: 23,
        # Astronomy Tower
        30: 24,  124: 24, 183: 24,
        # Year 6 Charms
        31: 25,  125: 25, 195: 25,
        # Year 5 Charms
        32: 26,  126: 26, 196: 26, 299: 26,
        # Potions
        33: 27,  127: 27, 197: 27,
        # Divination
        34: 28,  128: 28, 198: 28, 300: 28,
        # DADA
        35: 29,  129: 29, 199: 29, 301: 29,
        # Divination Courtyard
        36: 30,  130: 30, 200: 30, 302: 30,
        # Classroom Lobby
        37: 31,  131: 31, 201: 31, 303: 31,
        # Grand Staircase
        39: 32,  133: 32, 203: 32, 305: 32,
        # Library
        40: 33,  134: 33, 204: 33,
        # Foyer
        41: 34,  135: 34, 205: 34, 306: 34,
        # Madam Malkin's
        366: 35, 372: 35, 378: 35, 382: 35,
        # Knockturn Alley
        367: 36, 373: 36, 379: 36, 385: 36,
        # Leaky Cauldron
        368: 37, 374: 37, 380: 37, 386: 37,
        # Weasley's Wizard Wheezes
        369: 38, 375: 38, 383: 38, 387: 38,
        # Diagon Alley
        370: 39, 376: 39, 384: 39, 388: 39,
    }
 
    # Hub offset -> tab index (0-based index in maps.json)
    hub_offset_to_tab = {
        0:  9,   # Tent
        1:  10,  # Wilderness
        2:  7,   # Cafe
        3:  6,   # London
        4:  8,   # King's Cross Station
        5:  12,  # Hogsmeade Path
        6:  13,  # Hogsmeade
        7:  11,  # Hogsmeade Station
        8:  14,  # Hogwarts Path
        9:  17,  # Greenhouse
        10: 16,  # Training Grounds
        11: 15,  # Quad
        12: 32,  # Room of Requirement Corridor
        13: 30,  # Weasley Courtyard Storage
        14: 29,  # Weasley Courtyard
        15: 31,  # Great Hall
        16: 28,  # Great Hall Lobby
        17: 21,  # Black Lake
        18: 19,  # Quidditch Pitch
        19: 20,  # Thestral Forest
        20: 18,  # Hogwarts Grounds
        21: 26,  # Ravenclaw Tower
        22: 25,  # Gryffindor Common Room
        23: 24,  # Dorm Lobby + Slytherin and Hufflepuff Common Rooms
        24: 40,  # Astronomy Tower
        25: 35,  # Year 6 Charms
        26: 34,  # Year 5 Charms
        27: 37,  # Potions
        28: 39,  # Divination
        29: 36,  # DADA
        30: 38,  # Divination Courtyard
        31: 33,  # Classroom Lobby
        32: 23,  # Grand Staircase
        33: 27,  # Library
        34: 22,  # Foyer
        35: 4,   # Madam Malkin's
        36: 2,   # Knockturn Alley
        37: 5,   # Leaky Cauldron
        38: 3,   # Weasley's Wizard Wheezes
        39: 1,   # Diagon Alley
    }
 
    hub_offset = raw_id_to_hub_offset.get(map_id)
    if hub_offset is not None:
        return hub_offset_to_tab.get(hub_offset, 0)
 
    return 0


class LHP2World(World):
    """
    Save the Wizarding World from Lord Voldemort!
    """
    game = "Lego Harry Potter 5-7"
    options_dataclass = LHP2Options
    options: LHP2Options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_data_table.items() if data.code is not None}
    location_name_to_id = {name: data.id for name, data in all_location_table.items()}

    seed_location_table: Dict[str, int]
    seed_item_table: Dict[str, int]
    starting_items: list[tuple[str, int]] = []

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    data_version = 1.2
    web = LHP2Web()

    # Settings
    settings_key = "lhp2_settings"
    settings: ClassVar[LHP2Settings]
    
    # Universal Tracker
    tracker_world: ClassVar = {
        "external_pack_key": "ut_pack_path",
        "map_page_maps": ["maps/maps.json"],
        "map_page_locations": ["locations/levels.json", "locations/hub.json"],
        "map_page_layouts": ["layouts/tabs.json"],
        "map_page_setting_key": "Slot:{player}:map",
        "map_page_index": lhp2_map_to_tab_index,
    }

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    ut_can_gen_without_yaml = True

    def generate_early(self):
        self.validate_yaml()
        self.choose_starting_levels()
        self.choose_starting_spells()

        if self.options.StartingDetectors.value == 1:
            self.multiworld.push_precollected(self.create_item(ItemName.char_token_detect_unlock))
            self.multiworld.push_precollected(self.create_item(ItemName.red_brick_detect_unlock))
            self.multiworld.push_precollected(self.create_item(ItemName.crest_detect_unlock))
            self.multiworld.push_precollected(self.create_item(ItemName.gb_detect_unlock))
            self.starting_items.append((ItemName.char_token_detect_unlock, self.player))
            self.starting_items.append((ItemName.red_brick_detect_unlock, self.player))
            self.starting_items.append((ItemName.crest_detect_unlock, self.player))
            self.starting_items.append((ItemName.gb_detect_unlock, self.player))

        if self.options.StartingFastMagic.value == 1:
            self.multiworld.push_precollected(self.create_item(ItemName.fast_magic_unlock))
            self.multiworld.push_precollected(self.create_item(ItemName.fast_dig_unlock))
            self.starting_items.append((ItemName.fast_magic_unlock, self.player))
            self.starting_items.append((ItemName.fast_dig_unlock, self.player))

        for name in self.options.start_inventory:
            self.starting_items.append((name, self.player))

        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Lego Harry Potter 5-7" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Lego Harry Potter 5-7"]
                    self.options.EndGoal.value = slot_data["EndGoal"]
                    self.options.NumHorcruxRequired.value = slot_data["NumHorcruxRequired"]
                    self.options.NumLevelsRequired.value = slot_data["NumLevelsRequired"]
                    self.options.ShuffleCharacterTokens.value = slot_data["ShuffleCharacterTokens"]
                    self.options.ShuffleRedBricks.value = slot_data["ShuffleRedBricks"]
                    self.options.ShuffleJokeSpells.value = slot_data["ShuffleJokeSpells"]
                    self.options.ShuffleGoldBrickPurchases.value = slot_data["ShuffleGoldBrickPurchases"]
                    self.options.CheaperShops.value = slot_data["CheaperShops"]
                    self.options.HardPurchases.value = slot_data["HardPurchases"]
                    self.options.LowMultiplierPriceMinimum.value = slot_data["LowMultiplierPriceMinimum"]
                    self.options.HighMultiplierPriceMinimum.value = slot_data["HighMultiplierPriceMinimum"]

    def validate_yaml(self):
        if (self.options.NumStartLevels >
                (len(self.options.StartingLevelOptions.value) - len(self.options.DisabledLevels.value))):
            raise OptionError("You want to start with more levels than are in the starting pool")
        if self.options.HighMultiplierPriceMinimum.value < self.options.LowMultiplierPriceMinimum.value:
            raise OptionError("The High Multiplier must be larger than the Low Multiplier")
        if self.options.EndGoal.value == 0:
            if "The Flaw in the Plan" in self.options.DisabledLevels.value:
                raise OptionError("You can't disable The Flaw in the Plan in Voldemort Wincon.")
        if self.options.EndGoal.value == 2:
            if self.options.NumLevelsRequired.value > (24 - len(self.options.DisabledLevels.value)):
                raise OptionError("You want more levels to win than are enabled.")
        if self.options.ShuffleCharacterTokens.value == 2:
            if len(self.options.DisabledLevels.value) > 0:
                raise OptionError("Disabled Levels is incompatible with Character Tokens requiring Purchase Only.")

    def create_regions(self):
        self.seed_location_table = setup_locations(self.options)
        create_regions(self.multiworld, self.options, self.player, self.seed_location_table)

    def create_item(self, name: str) -> Item:
        data = item_data_table[name]
        item = LHP2Item(name, data.classification, data.code, self.player)
        return item

    def create_items(self):
        itempool = []
        seed_items = setup_items(self.options)

        # Build the full pool
        for name, data in seed_items.items():
            itempool += [self.create_item(name) for _ in range(data.qty)]

        # Remove starting items for selected player
        for name, player in self.starting_items:
            if player != self.player:
                continue

            for i in itempool:
                if i.name == name and i.player == self.player:
                    itempool.remove(i)
                    break

        # Fill extra locations
        extra_locations = len(self.seed_location_table) - len(itempool)
        print(f"{self.player_name} has {extra_locations} extra locations")
        if extra_locations > 0:
            while extra_locations > 0:
                itempool.append(self.create_item("Purple Stud"))
                extra_locations -= 1

        # Remove Playable Characters if extra locations is negative
        if extra_locations < 0:
            needed = -extra_locations
            removable = [i for i in itempool if i.code < 400212 and i.classification is ItemClassification.filler]
            for i in removable[:needed]:
                itempool.remove(i)

        self.multiworld.itempool.extend(itempool)

    def set_rules(self):
        set_rules(self)

    def choose_starting_levels(self):
        levels_pushed: int = 0

        for name in self.options.DisabledLevels.value:
            self.options.StartingLevelOptions.value.remove(name)

        while levels_pushed < self.options.NumStartLevels.value:
            starting_level = self.random.choice(self.options.StartingLevelOptions.value)
            self.options.StartingLevelOptions.value.remove(starting_level)
            starting_level = starting_level + ": Level Unlocked"
            self.multiworld.push_precollected(self.create_item(starting_level))
            self.starting_items.append((starting_level, self.player))
            levels_pushed += 1

    def choose_starting_spells(self):
        starting_spells = list(progression_spells)
        spells_pushed: int = 0
        print(f"{self.player_name} has {self.options.NumStartSpells.value} starting spells")
        while spells_pushed < self.options.NumStartSpells.value:
            spell = self.random.choice(starting_spells)
            starting_spells.remove(spell)
            self.multiworld.push_precollected(self.create_item(spell))
            self.starting_items.append((spell, self.player))
            spells_pushed += 1

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if changed:
            name = item.name
            if name in horcrux_names_set and state.count(name, self.player) == 1:
                # Count was 0 before super().collect().
                # Increase unique horcrux count.
                state.prog_items[self.player]["UNIQUE_HORCRUX"] += 1
        return changed

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            name = item.name
            if name in horcrux_names_set and state.count(name, self.player) == 0:
                # Count was 1 before super().remove().
                # Decrease unique horcrux count.
                state.prog_items[self.player]["UNIQUE_HORCRUX"] -= 1
        return changed

    def fill_slot_data(self):
        return {
            "EndGoal": self.options.EndGoal.value,
            # "CollectiblesRequired": self.options.CollectibleQuantity.value,
            # "FlawInThePlanCondition": self.options.FlawInThePlanCondition.value,
            "NumHorcruxRequired": self.options.NumHorcruxRequired.value,
            "NumLevelsRequired": self.options.NumLevelsRequired.value,
            "ShuffleCharacterTokens": self.options.ShuffleCharacterTokens.value,
            "ShuffleRedBricks": self.options.ShuffleRedBricks.value,
            "ShuffleJokeSpells": self.options.ShuffleJokeSpells.value,
            "ShuffleGoldBrickPurchases": self.options.ShuffleGoldBrickPurchases.value,
            "CheaperShops": self.options.CheaperShops.value,
            "HardPurchases": self.options.HardPurchases.value,
            "LowMultiplierPriceMinimum": self.options.LowMultiplierPriceMinimum.value,
            "HighMultiplierPriceMinimum": self.options.HighMultiplierPriceMinimum.value,
            "FasterDuels": self.options.FasterDuels.value,
        }
