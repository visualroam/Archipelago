"""
AF League of Legends – manuelle APWorld (kein Client, keine Riot-API → Vanguard-sicher).

Ersatz für die alte LoLAP-World (seit 2024 nicht gepflegt, lädt Champions beim Generieren aus dem Netz).
Items sind Erlaubnisse: Nur in freigeschalteten Rollen queuen und nur freigeschaltete Champions picken.
Checks werden von Hand abgehakt (Mods im AF-Dashboard → `/send_location`).
Ziel: alle Rollen + genug "Hextech Crystal"s, dann das Finale gewinnen.
"""
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Options import Choice, OptionSet, PerGameCommonOptions, Range, Toggle
from worlds.AutoWorld import WebWorld, World

GAME = "AF League of Legends"
BASE_ID = 7_563_000_000

ROLES = ["Top", "Jungle", "Mid", "Bot", "Support"]

# Feste Reihenfolge = feste IDs: neue Champions nur hinten anhängen
CHAMPIONS = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
    "Aurelion Sol", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn", "Camille",
    "Cassiopeia", "Cho'Gath", "Corki", "Darius", "Diana", "Dr. Mundo", "Draven", "Ekko", "Elise", "Evelynn",
    "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves",
    "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia", "Ivern", "Janna", "Jarvan IV", "Jax",
    "Jayce", "Jhin", "Jinx", "K'Sante", "Kai'Sa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina",
    "Kayle", "Kayn", "Kennen", "Kha'Zix", "Kindred", "Kled", "Kog'Maw", "LeBlanc", "Lee Sin", "Leona",
    "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai", "Master Yi", "Milio",
    "Miss Fortune", "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko", "Nidalee", "Nilah",
    "Nocturne", "Nunu & Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana", "Quinn",
    "Rakan", "Rammus", "Rek'Sai", "Rell", "Renata Glasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze",
    "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion",
    "Sivir", "Skarner", "Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra", "Tahm Kench", "Taliyah",
    "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere", "Twisted Fate", "Twitch", "Udyr",
    "Urgot", "Varus", "Vayne", "Veigar", "Vel'Koz", "Vex", "Vi", "Viego", "Viktor", "Vladimir",
    "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo", "Yone", "Yorick", "Yuumi",
    "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra", "Aurora", "Ambessa", "Mel",
    "Yunara",
]

MACGUFFIN = "Hextech Crystal"
FILLER = ["Blue Essence", "Ward Skin", "Emote"]
TRAPS = [
    "Trap: No Flash Match",
    "Trap: Off-Role Match",
    "Trap: Chat Picks the Build",
    "Trap: No Wards Match",
    "Trap: Mouse Sensitivity x1.5 Match",
]

GENERAL_CHECKS = [
    "Get First Blood",
    "Destroy a Turret",
    "Take a Dragon",
    "Take Baron Nashor",
    "Win an ARAM Match",
]
ROLE_CHECKS = {role: f"Win a Match as {role}" for role in ROLES}
HARD_CHECKS = ["Get a Pentakill", "Steal Baron or Dragon"]  # Glück → EXCLUDED
FINALE = "Finale: Win a Draft Match"


def champion_checks(champ: str, kills: int) -> list[str]:
    return [f"Win a Match as {champ}", f"Get {kills} Takedowns as {champ}"]


def state_has(state, player: int):
    """has() für tracker_logic-Regeln auf einem CollectionState (Liste = eins davon)."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            return state.has_any(item, player)
        return state.has(item, player, count)
    return has


ALL_ITEMS = [f"Role: {r}" for r in ROLES] + [f"Champion: {c}" for c in CHAMPIONS] + [MACGUFFIN] + FILLER + TRAPS
# Die Takedown-Zahl steht im Location-Namen → jede Stufe braucht eine eigene, feste ID
TAKEDOWN_STEPS = [5, 10, 15]
ALL_LOCATIONS = ([f"Win a Match as {c}" for c in CHAMPIONS]
                 + [f"Get {k} Takedowns as {c}" for c in CHAMPIONS for k in TAKEDOWN_STEPS]
                 + GENERAL_CHECKS + list(ROLE_CHECKS.values()) + HARD_CHECKS)


class ChampionPoolSize(Range):
    """Wie viele (zufällige) Champions im Spiel sind. 2 Checks pro Champion."""
    display_name = "Champion Pool Size"
    range_start = 5
    range_end = len(CHAMPIONS)
    default = 20


class ChampionPool(OptionSet):
    """Nur aus diesen Champions auswählen (leer = alle). Für den eigenen Champion-Pool des Streamers."""
    display_name = "Champion Pool"
    valid_keys = CHAMPIONS


class StartingChampions(Range):
    """Wie viele Champions von Anfang an freigeschaltet sind."""
    display_name = "Starting Champions"
    range_start = 1
    range_end = 5
    default = 3


class Takedowns(Choice):
    """Kills + Assists, die ein Champion-Check verlangt."""
    display_name = "Takedowns per Champion Check"
    option_5 = 5
    option_10 = 10
    option_15 = 15
    default = 10


class CrystalsTotal(Range):
    """Wie viele Hextech Crystals in der Multiworld verteilt werden."""
    display_name = "Hextech Crystals Total"
    range_start = 1
    range_end = 30
    default = 12


class CrystalsRequired(Range):
    """Wie viele Hextech Crystals fürs Finale nötig sind (wird auf Crystals Total begrenzt)."""
    display_name = "Hextech Crystals Required"
    range_start = 1
    range_end = 30
    default = 8


class HardChecks(Toggle):
    """Glücks-Checks (Pentakill, Steal) hinzufügen. Dort liegt nie etwas Wichtiges."""
    display_name = "Hard Checks"


class TrapPercentage(Range):
    """Anteil der Füll-Items, die Traps sind (in %)."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 25


@dataclass
class AFLeagueOptions(PerGameCommonOptions):
    champion_pool_size: ChampionPoolSize
    champion_pool: ChampionPool
    starting_champions: StartingChampions
    takedowns: Takedowns
    crystals_total: CrystalsTotal
    crystals_required: CrystalsRequired
    hard_checks: HardChecks
    trap_percentage: TrapPercentage


class AFLeagueItem(Item):
    game = GAME


class AFLeagueLocation(Location):
    game = GAME


class AFLeagueWeb(WebWorld):
    tutorials = [Tutorial(
        "Setup", "Manuelle League-of-Legends-World für AF Charity", "English", "setup_en.md", "setup/en", ["AF Charity"],
    )]


class AFLeagueWorld(World):
    """League of Legends als manuelle Archipelago-World: Rollen + Champions freischalten, Checks per Mod abhaken."""

    game = GAME
    web = AFLeagueWeb()
    options_dataclass = AFLeagueOptions
    options: AFLeagueOptions
    topology_present = False

    item_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_ITEMS)}
    location_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_LOCATIONS)}
    item_name_groups = {
        "Roles": {f"Role: {r}" for r in ROLES},
        "Champions": {f"Champion: {c}" for c in CHAMPIONS},
        "Traps": set(TRAPS),
    }

    def generate_early(self) -> None:
        allowed = [c for c in CHAMPIONS if not self.options.champion_pool.value or c in self.options.champion_pool.value]
        size = min(self.options.champion_pool_size.value, len(allowed))
        self.champion_pool = sorted(self.random.sample(allowed, size))
        self.starting_champions = sorted(self.random.sample(self.champion_pool,
                                                            min(self.options.starting_champions.value, size)))
        self.starting_role = self.random.choice(ROLES)
        self.kills = self.options.takedowns.value
        # Crystals dürfen nicht mehr sein als freie Locations (nach Rollen- und Champion-Items).
        # Hard Checks zählen nicht: EXCLUDED, dort darf nichts Progressives liegen.
        locations = 2 * size + len(GENERAL_CHECKS) + len(ROLE_CHECKS)
        free = locations - (len(ROLES) - 1) - (size - len(self.starting_champions))
        self.crystals_required = max(1, min(self.options.crystals_required.value,
                                            self.options.crystals_total.value, free))

    def create_regions(self) -> None:
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        names = [n for c in self.champion_pool for n in champion_checks(c, self.kills)]
        names += GENERAL_CHECKS + list(ROLE_CHECKS.values())
        if self.options.hard_checks:
            names += HARD_CHECKS
        self.location_names = list(names)  # für slot_data → AF-Dashboard (Checks abhaken)
        for name in names:
            loc = AFLeagueLocation(self.player, name, self.location_name_to_id[name], menu)
            if name in HARD_CHECKS:
                loc.progress_type = LocationProgressType.EXCLUDED
            menu.locations.append(loc)

        finale = AFLeagueLocation(self.player, FINALE, None, menu)
        finale.place_locked_item(AFLeagueItem("Victory", ItemClassification.progression, None, self.player))
        menu.locations.append(finale)

    def create_item(self, name: str) -> AFLeagueItem:
        if name.startswith(("Role: ", "Champion: ")) or name == MACGUFFIN:
            cls = ItemClassification.progression
        elif name in TRAPS:
            cls = ItemClassification.trap
        else:
            cls = ItemClassification.filler
        return AFLeagueItem(name, cls, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        self.multiworld.push_precollected(self.create_item(f"Role: {self.starting_role}"))
        for champ in self.starting_champions:
            self.multiworld.push_precollected(self.create_item(f"Champion: {champ}"))

        items = [self.create_item(f"Role: {r}") for r in ROLES if r != self.starting_role]
        items += [self.create_item(f"Champion: {c}") for c in self.champion_pool if c not in self.starting_champions]
        unfilled = self.multiworld.get_unfilled_locations(self.player)
        slots = len(unfilled)
        open_slots = sum(1 for loc in unfilled if loc.progress_type != LocationProgressType.EXCLUDED)
        count = max(self.crystals_required, min(self.options.crystals_total.value, open_slots - len(items)))
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
        pool: list[str] = slot_data["champion_pool"]
        kills = slot_data["takedowns"]
        required = slot_data["hextech_crystals_required"]
        roles = [f"Role: {r}" for r in ROLES]
        champs = [f"Champion: {c}" for c in pool]

        # Ein Match braucht immer eine freie Rolle UND einen freien Champion
        rules = {}
        for champ in pool:
            for name in champion_checks(champ, kills):
                rules[name] = lambda has, c=champ: all([has(f"Champion: {c}"), has(roles)])
        for role, name in ROLE_CHECKS.items():
            rules[name] = lambda has, r=role: all([has(f"Role: {r}"), has(champs)])
        rules[FINALE] = lambda has: all([has(MACGUFFIN, required), *[has(r) for r in roles], has(champs)])
        return {
            "rules": rules,
            "goal": FINALE,
            "counters": [{"item": MACGUFFIN, "required": required}],
            "groups": [{"title": "Rollen", "items": roles}, {"title": "Champions", "items": champs}],
        }

    def set_rules(self) -> None:
        for name, rule in self.tracker_logic(self.fill_slot_data())["rules"].items():
            self.get_location(name).access_rule = lambda state, r=rule: r(state_has(state, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "locations": self.location_names,
            "champion_pool": self.champion_pool,
            "starting_role": self.starting_role,
            "starting_champions": self.starting_champions,
            "takedowns": self.kills,
            "hextech_crystals_required": self.crystals_required,
        }
