"""
AF Bot – leerer Slot für den AF-Charity-Bot (@af/ap-client).

Keine Locations, keine Items, Ziel sofort erfüllt. Der Bot verbindet sich mit diesem Slot nur, um
Admin-Befehle zu schicken (z. B. `!admin /deathlink`), und beeinflusst die Multiworld überhaupt nicht.
"""
from BaseClasses import Item, Region
from worlds.AutoWorld import WebWorld, World


class AFBotWeb(WebWorld):
    tutorials = []


class AFBotWorld(World):
    """Leerer Slot für den AF-Charity-Bot: keine Checks, keine Items."""

    game = "AF Bot"
    web = AFBotWeb()
    hidden = True  # nicht in den Spiel-Listen der Website anzeigen
    topology_present = False

    # Je ein Dummy-Eintrag: Der WebHost lehnt Uploads mit leeren Item-/Location-Tabellen ab
    # ("Key 'item_name_to_id' error"). Erzeugt werden beide nie – der Slot bleibt leer.
    item_name_to_id = {"Nothing": 7_559_000_000}
    location_name_to_id = {"Bot Slot": 7_559_000_000}

    def create_regions(self) -> None:
        self.multiworld.regions.append(Region(self.origin_region_name, self.player, self.multiworld))

    def create_items(self) -> None:
        pass

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: True

    def create_item(self, name: str) -> Item:
        raise KeyError(f"AF Bot has no items ({name})")
