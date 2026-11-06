"""
AF Kingdom Hearts 3 – manuelle APWorld (kein Mod, kein Speicherzugriff).

Es gibt keine echte KH3-APWorld. Items sind Erlaubnisse: Eine Welt darf erst betreten werden, wenn genug
„Progressive World“ da sind (Reihenfolge wie in der Story), Magie/Keyblades/Attraction Flow/Links erst nach ihrem Item.
Checks werden von Hand abgehakt (Mods im AF-Dashboard → `/send_location`).
Ziel: alle Welten + genug "Heart Piece"s, dann Master Xehanort in Scala ad Caelum besiegen.
"""
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Options import DefaultOnToggle, PerGameCommonOptions, Range, Toggle
from worlds.AutoWorld import WebWorld, World

GAME = "AF Kingdom Hearts 3"
BASE_ID = 7_562_000_000

# Story-Reihenfolge; Olympus ist von Anfang an offen, jede weitere Welt braucht ein „Progressive World“ mehr
WORLDS = [
    "Olympus", "Twilight Town", "Toy Box", "Kingdom of Corona", "Monstropolis",
    "Arendelle", "The Caribbean", "San Fransokyo", "Keyblade Graveyard",
]
PROGRESSIVE_WORLD = "Progressive World"
MACGUFFIN = "Heart Piece"

KEYBLADES = [
    "Hero's Origin", "Shooting Star", "Favorite Deputy", "Ever After", "Happy Gear",
    "Crystal Snow", "Wheel of Fate", "Nano Gear", "Classic Tone", "Grand Chef",
]
MAGIC = ["Fire", "Blizzard", "Thunder", "Water", "Aero", "Cure"]
ABILITIES = ["Attraction Flow", "Links"]
FILLER = ["Munny", "Potion", "Ether", "Synthesis Material"]
TRAPS = [
    "Trap: Kingdom Key Only (until next save point)",
    "Trap: No Magic Next Fight",
    "Trap: No Healing Next Fight",
    "Trap: No Attraction Flow (10 min)",
]


def world_checks(world: str) -> list[str]:
    # Keyblade Graveyard hat kaum Kisten/Lucky Emblems → nur Story-Checks
    checks = [f"{world}: Defeat the World Boss", f"{world}: Complete the World"]
    if world != "Keyblade Graveyard":
        checks += [f"{world}: Find 3 Lucky Emblems", f"{world}: Open 10 Treasure Chests"]
    return checks


GENERAL_CHECKS = [
    "Cook a Dish at the Bistrot",
    "Play a Classic Kingdom Game",
    "Upgrade a Keyblade at a Moogle Shop",
    "Synthesize an Item",
    "Win a Gummi Ship Battle",
]
HARD_CHECKS = ["Beat a Classic Kingdom High Score", "Get an Excellent Dish at the Bistrot"]  # Glück/Skill → EXCLUDED
FINALE = "Scala ad Caelum: Defeat Master Xehanort"

def state_has(state, player: int):
    """has() für tracker_logic-Regeln auf einem CollectionState (Liste = eins davon)."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            return state.has_any(item, player)
        return state.has(item, player, count)
    return has


ALL_ITEMS = [PROGRESSIVE_WORLD, MACGUFFIN] + [f"Keyblade: {k}" for k in KEYBLADES] + \
    [f"Magic: {m}" for m in MAGIC] + ABILITIES + FILLER + TRAPS
ALL_LOCATIONS = [c for w in WORLDS for c in world_checks(w)] + GENERAL_CHECKS + HARD_CHECKS


class LockMagic(DefaultOnToggle):
    """Magie erst nach dem Item benutzen (Cure siehe Start With Cure)."""
    display_name = "Lock Magic"


class StartWithCure(DefaultOnToggle):
    """Cure von Anfang an erlaubt – ohne Cure wird es sehr hart."""
    display_name = "Start With Cure"


class LockKeyblades(DefaultOnToggle):
    """Nur der Kingdom Key ist von Anfang an erlaubt, andere Keyblades erst nach ihrem Item."""
    display_name = "Lock Keyblades"


class HeartPiecesTotal(Range):
    """Wie viele Heart Pieces in der Multiworld verteilt werden."""
    display_name = "Heart Pieces Total"
    range_start = 1
    range_end = 20
    default = 10


class HeartPiecesRequired(Range):
    """Wie viele Heart Pieces fürs Finale nötig sind (wird auf Heart Pieces Total begrenzt)."""
    display_name = "Heart Pieces Required"
    range_start = 1
    range_end = 20
    default = 8


class HardChecks(Toggle):
    """Skill-Checks (Classic-Kingdom-Highscore, Excellent-Gericht) hinzufügen. Dort liegt nie etwas Wichtiges."""
    display_name = "Hard Checks"


class TrapPercentage(Range):
    """Anteil der Füll-Items, die Traps sind (in %)."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 25


@dataclass
class AFKH3Options(PerGameCommonOptions):
    lock_magic: LockMagic
    start_with_cure: StartWithCure
    lock_keyblades: LockKeyblades
    heart_pieces_total: HeartPiecesTotal
    heart_pieces_required: HeartPiecesRequired
    hard_checks: HardChecks
    trap_percentage: TrapPercentage


class AFKH3Item(Item):
    game = GAME


class AFKH3Location(Location):
    game = GAME


class AFKH3Web(WebWorld):
    tutorials = [Tutorial(
        "Setup", "Manuelle Kingdom-Hearts-3-World für AF Charity", "English", "setup_en.md", "setup/en", ["AF Charity"],
    )]


class AFKH3World(World):
    """Kingdom Hearts 3 als manuelle Archipelago-World: Welten, Magie und Keyblades freischalten, Checks per Mod abhaken."""

    game = GAME
    web = AFKH3Web()
    options_dataclass = AFKH3Options
    options: AFKH3Options
    topology_present = False

    item_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_ITEMS)}
    location_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_LOCATIONS)}
    item_name_groups = {
        "Keyblades": {f"Keyblade: {k}" for k in KEYBLADES},
        "Magic": {f"Magic: {m}" for m in MAGIC},
        "Traps": set(TRAPS),
    }

    def generate_early(self) -> None:
        self.locked = []
        if self.options.lock_keyblades:
            self.locked += [f"Keyblade: {k}" for k in KEYBLADES]
        if self.options.lock_magic:
            self.locked += [f"Magic: {m}" for m in MAGIC if not (m == "Cure" and self.options.start_with_cure)]
        self.locked += ABILITIES
        # Heart Pieces dürfen nicht mehr sein als freie Locations (nach Welten- und Erlaubnis-Items).
        # Hard Checks zählen nicht: EXCLUDED, dort darf nichts Progressives liegen.
        locations = sum(len(world_checks(w)) for w in WORLDS) + len(GENERAL_CHECKS)
        free = locations - (len(WORLDS) - 1) - len(self.locked)
        self.hearts_required = max(1, min(self.options.heart_pieces_required.value,
                                          self.options.heart_pieces_total.value, free))

    def create_regions(self) -> None:
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        names = [c for w in WORLDS for c in world_checks(w)] + GENERAL_CHECKS
        if self.options.hard_checks:
            names += HARD_CHECKS
        self.location_names = list(names)  # für slot_data → AF-Dashboard (Checks abhaken)
        for name in names:
            loc = AFKH3Location(self.player, name, self.location_name_to_id[name], menu)
            if name in HARD_CHECKS:
                loc.progress_type = LocationProgressType.EXCLUDED
            menu.locations.append(loc)

        finale = AFKH3Location(self.player, FINALE, None, menu)
        finale.place_locked_item(AFKH3Item("Victory", ItemClassification.progression, None, self.player))
        menu.locations.append(finale)

    def create_item(self, name: str) -> AFKH3Item:
        if name in (PROGRESSIVE_WORLD, MACGUFFIN):
            cls = ItemClassification.progression
        elif name in TRAPS:
            cls = ItemClassification.trap
        elif name in FILLER:
            cls = ItemClassification.filler
        else:
            cls = ItemClassification.useful  # Erlaubnisse: machen es leichter, sperren aber keine Checks
        return AFKH3Item(name, cls, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        items = [self.create_item(PROGRESSIVE_WORLD) for _ in WORLDS[1:]]
        items += [self.create_item(name) for name in self.locked]
        unfilled = self.multiworld.get_unfilled_locations(self.player)
        slots = len(unfilled)
        open_slots = sum(1 for loc in unfilled if loc.progress_type != LocationProgressType.EXCLUDED)
        count = max(self.hearts_required, min(self.options.heart_pieces_total.value, open_slots - len(items)))
        items += [self.create_item(MACGUFFIN) for _ in range(count)]
        while len(items) < slots:
            items.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool += items

    def get_filler_item_name(self) -> str:
        if self.random.randint(1, 100) <= self.options.trap_percentage.value:
            return self.random.choice(TRAPS)
        return self.random.choice(FILLER)

    @staticmethod
    def tracker_logic(slot_data: dict) -> dict:
        """Regeln + Anzeige für den AF-Tracker im WebHost. set_rules nutzt dieselben Regeln → kein Auseinanderlaufen.
        Regel = Funktion von has(item | [items…] (eins davon), count=1)."""
        worlds: list[str] = slot_data["worlds"]
        required = slot_data["heart_pieces_required"]
        locked: list[str] = slot_data.get("locked", [])
        # Story-Reihenfolge: Welt n braucht n× Progressive World
        rules = {name: (lambda has, n=i: has(PROGRESSIVE_WORLD, n))
                 for i, world in enumerate(worlds) if i > 0 for name in world_checks(world)}
        rules[FINALE] = lambda has: all([has(PROGRESSIVE_WORLD, len(worlds) - 1), has(MACGUFFIN, required)])
        groups = [{"title": "Welten", "progressive": PROGRESSIVE_WORLD, "items": worlds}]
        for title, prefix in (("Keyblades", "Keyblade: "), ("Magie", "Magic: ")):
            items = [n for n in locked if n.startswith(prefix)]
            if items:
                groups.append({"title": title, "items": items})
        abilities = [n for n in locked if n in ABILITIES]
        if abilities:
            groups.append({"title": "Fähigkeiten", "items": abilities})
        return {
            "rules": rules,
            "goal": FINALE,
            "counters": [{"item": MACGUFFIN, "required": required},
                         {"item": PROGRESSIVE_WORLD, "required": len(worlds) - 1}],
            "groups": groups,
        }

    def set_rules(self) -> None:
        for name, rule in self.tracker_logic(self.fill_slot_data())["rules"].items():
            self.get_location(name).access_rule = lambda state, r=rule: r(state_has(state, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "locations": self.location_names,
            "worlds": WORLDS,
            "locked": self.locked,
            "heart_pieces_required": self.hearts_required,
        }
