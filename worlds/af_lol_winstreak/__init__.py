"""
AF League of Legends Winstreak – manuelle APWorld (kein Client, keine Riot-API → Vanguard-sicher).

Basiert auf "AF League of Legends", eigener Game-Name + eigene IDs → beide Worlds können parallel installiert sein.
Items sind Erlaubnisse: Nur in freigeschalteten Rollen queuen und nur freigeschaltete Champions picken.
Dazu Keystones und Tier-2-Stiefel als reine Erlaubnisse (nur freigeschaltete benutzen).
Checks: pro Champion "Win a Match as X" + "Get N Kills as X" (Assists zählen nicht) (optional Pentakill).
Checks: automatisch über den "AF LoL Winstreak Client" (op.gg) oder von Hand (Mods → `/send_location`).
Ziel: N Siege in Folge (Standard 5), jeder Sieg mit einem anderen freigeschalteten Champion.
Zählende Queues: Normal Draft, Blind, Swiftplay, Ranked Solo/Flex. Alles andere (ARAM, Arena, …) wird ignoriert.
Keine Hextech Crystals mehr.
"""
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Options import Choice, OptionSet, PerGameCommonOptions, Range, Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, launch_subprocess

GAME = "AF League of Legends Winstreak"
BASE_ID = 7_564_000_000

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

# Keystones nach Baum (Stand DDragon 16.22.1 = Patch 26.22; Phase Rush ist jetzt Stormraider's Surge)
KEYSTONE_TREES = {
    "Precision": ["Press the Attack", "Lethal Tempo", "Fleet Footwork", "Conqueror"],
    "Domination": ["Electrocute", "Dark Harvest", "Hail of Blades"],
    "Sorcery": ["Summon Aery", "Arcane Comet", "Deathfire Touch", "Stormraider's Surge"],
    "Resolve": ["Grasp of the Undying", "Aftershock", "Guardian"],
    "Inspiration": ["Glacial Augment", "Unsealed Spellbook", "First Strike"],
}
KEYSTONES = [k for tree in KEYSTONE_TREES.values() for k in tree]
# Tier-2-Stiefel (Stand DDragon 16.22.1). Boots (Tier 1) sind immer erlaubt.
BOOTS = ["Berserker's Greaves", "Sorcerer's Shoes", "Plated Steelcaps", "Mercury's Treads",
         "Ionian Boots of Lucidity", "Boots of Swiftness", "Gluttonous Greaves"]

CHAMPION_REUSE = "Champion Reuse"  # einmal einen Champion in der Serie doppelt spielen
FILLER = ["Chat Picks Rune", "Mastery Emote Spam"]
TRAPS = [
    "Trap: No Flash Match",
    "Trap: Off-Role Match",
    "Trap: Bronze Bravery Build",
    "Trap: No Wards Match",
    "Trap: Mouse Sensitivity x1.5 Match",
]

HARD_CHECKS = ["Get a Pentakill"]  # Glück → EXCLUDED
FINALE = "Finale: Win Streak"


def champion_checks(champ: str, kills: int) -> list[str]:
    return [f"Win a Match as {champ}", f"Get {kills} Kills as {champ}"]


def state_has(state, player: int):
    """has() für tracker_logic-Regeln auf einem CollectionState (Liste = eins davon)."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            return state.has_any(item, player)
        return state.has(item, player, count)
    return has


ALL_ITEMS = ([f"Role: {r}" for r in ROLES] + [f"Champion: {c}" for c in CHAMPIONS]
             + [f"Keystone: {k}" for k in KEYSTONES] + [f"Boots: {b}" for b in BOOTS]
             + [CHAMPION_REUSE] + FILLER + TRAPS)
# Die Kill-Zahl steht im Location-Namen → jede Stufe braucht eine eigene, feste ID
KILL_STEPS = [5, 10, 15]
ALL_LOCATIONS = ([f"Win a Match as {c}" for c in CHAMPIONS]
                 + [f"Get {k} Kills as {c}" for c in CHAMPIONS for k in KILL_STEPS]
                 + HARD_CHECKS)


class ChampionPoolSize(Range):
    """Wie viele (zufällige) Champions im Spiel sind. 2 Checks pro Champion (Sieg + Kills)."""
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


class Kills(Choice):
    """Kills in einem Match, die ein Champion-Check verlangt. Assists zählen nicht."""
    display_name = "Kills per Champion Check"
    option_5 = 5
    option_10 = 10
    option_15 = 15
    default = 10


class StreakLength(Range):
    """Wie viele Siege in Folge fürs Ziel nötig sind. Jeder Sieg der Serie mit einem anderen Champion,
    eine Niederlage setzt die Serie zurück. Der Champion-Pool wird mindestens so groß gemacht."""
    display_name = "Win Streak Length"
    range_start = 2
    range_end = 10
    default = 5


class StartingKeystones(Range):
    """Wie viele Keystones von Anfang an frei sind (jeder aus einem anderen Runen-Baum)."""
    display_name = "Starting Keystones"
    range_start = 1
    range_end = 5
    default = 3


class ChampionReuseCount(Range):
    """Wie viele "Champion Reuse" im Pool liegen. Jedes erlaubt einmal, einen Champion in der Serie doppelt zu spielen."""
    display_name = "Champion Reuse Count"
    range_start = 0
    range_end = 10
    default = 3


class HardChecks(Toggle):
    """Glücks-Check (Pentakill) hinzufügen. Dort liegt nie etwas Wichtiges."""
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
    kills: Kills
    streak_length: StreakLength
    starting_keystones: StartingKeystones
    champion_reuse_count: ChampionReuseCount
    hard_checks: HardChecks
    trap_percentage: TrapPercentage



def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="AFLoLWinstreakClient", args=args)


components.append(Component("AF LoL Winstreak Client", func=launch_client, component_type=Type.CLIENT,
                            game_name=GAME, supports_uri=True,
                            description="Liest neue Spiele von op.gg und schickt Checks automatisch."))

class AFLeagueItem(Item):
    game = GAME


class AFLeagueLocation(Location):
    game = GAME


class AFLeagueWeb(WebWorld):
    tutorials = [Tutorial(
        "Setup", "Manuelle League-of-Legends-Winstreak-World für AF Charity", "English", "setup_en.md", "setup/en", ["AF Charity"],
    )]


class AFLeagueWorld(World):
    """League of Legends als manuelle Archipelago-World: Rollen + Champions freischalten, Checks per Mod abhaken,
    Ziel ist eine Siegesserie mit lauter verschiedenen Champions."""

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
        "Keystones": {f"Keystone: {k}" for k in KEYSTONES},
        "Boots": {f"Boots: {b}" for b in BOOTS},
        "Traps": set(TRAPS),
    }

    def generate_early(self) -> None:
        allowed = [c for c in CHAMPIONS if not self.options.champion_pool.value or c in self.options.champion_pool.value]
        self.streak_length = self.options.streak_length.value
        if len(allowed) < self.streak_length:
            raise Exception(f"{self.player_name}: Champion Pool hat nur {len(allowed)} Champions, "
                            f"die Winstreak braucht aber {self.streak_length} verschiedene.")
        # Pool muss mindestens so groß sein wie die Serie, sonst ist das Ziel unmöglich
        size = min(max(self.options.champion_pool_size.value, self.streak_length), len(allowed))
        self.champion_pool = sorted(self.random.sample(allowed, size))
        self.starting_champions = sorted(self.random.sample(self.champion_pool,
                                                            min(self.options.starting_champions.value, size)))
        self.starting_roles = sorted(self.random.sample(ROLES, 2), key=ROLES.index)
        self.kills = self.options.kills.value
        trees = self.random.sample(list(KEYSTONE_TREES), self.options.starting_keystones.value)
        self.starting_keystones = [self.random.choice(KEYSTONE_TREES[t]) for t in trees]

    def create_regions(self) -> None:
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        names = [n for c in self.champion_pool for n in champion_checks(c, self.kills)]
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
        if name.startswith(("Champion: ", "Role: ")):
            # Rollen stehen in der Logik (irgendeine Rolle) → müssen progression sein, sonst zählt der State sie nicht
            cls = ItemClassification.progression
        elif name.startswith(("Keystone: ", "Boots: ")) or name == CHAMPION_REUSE:
            # reine Erlaubnisse: nützlich, aber die Logik braucht sie nicht
            cls = ItemClassification.useful
        elif name in TRAPS:
            cls = ItemClassification.trap
        else:
            cls = ItemClassification.filler
        return AFLeagueItem(name, cls, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        for role in self.starting_roles:
            self.multiworld.push_precollected(self.create_item(f"Role: {role}"))
        for champ in self.starting_champions:
            self.multiworld.push_precollected(self.create_item(f"Champion: {champ}"))

        for key in self.starting_keystones:
            self.multiworld.push_precollected(self.create_item(f"Keystone: {key}"))

        items = [self.create_item(f"Champion: {c}") for c in self.champion_pool if c not in self.starting_champions]
        slots = len(self.multiworld.get_unfilled_locations(self.player))
        # Erlaubnisse in den Pool; was bei kleinem Champion-Pool keinen Platz hat, gibt's ab Start
        permits = ([f"Role: {r}" for r in ROLES if r not in self.starting_roles]
                   + [f"Keystone: {k}" for k in KEYSTONES if k not in self.starting_keystones]
                   + [f"Boots: {b}" for b in BOOTS])
        self.random.shuffle(permits)
        free = slots - len(items)
        for name in permits[free:]:
            self.multiworld.push_precollected(self.create_item(name))
        items += [self.create_item(name) for name in permits[:free]]
        reuse = min(self.options.champion_reuse_count.value, slots - len(items))
        items += [self.create_item(CHAMPION_REUSE) for _ in range(reuse)]
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
        kills = slot_data["kills"]
        streak = slot_data["streak_length"]
        roles = [f"Role: {r}" for r in ROLES]
        champs = [f"Champion: {c}" for c in pool]

        # Ein Match braucht immer eine freie Rolle UND einen freien Champion
        rules = {}
        for champ in pool:
            for name in champion_checks(champ, kills):
                rules[name] = lambda has, c=champ: all([has(f"Champion: {c}"), has(roles)])
        # Ziel: eine freie Rolle + so viele verschiedene Champions wie die Serie lang ist.
        # Bewusst nur Einzel-has() (kein has(liste, n)), damit der AF-Tracker die Regel 1:1 versteht.
        rules[FINALE] = lambda has: all([has(roles), sum(1 for c in champs if has(c)) >= streak])
        return {
            "rules": rules,
            "goal": FINALE,
            "counters": [],
            "groups": [{"title": "Rollen", "items": roles}, {"title": "Champions", "items": champs},
                       {"title": "Keystones", "items": [f"Keystone: {k}" for k in KEYSTONES]},
                       {"title": "Stiefel", "items": [f"Boots: {b}" for b in BOOTS]}],
        }

    def set_rules(self) -> None:
        for name, rule in self.tracker_logic(self.fill_slot_data())["rules"].items():
            self.get_location(name).access_rule = lambda state, r=rule: r(state_has(state, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "locations": self.location_names,
            "champion_pool": self.champion_pool,
            "starting_roles": self.starting_roles,
            "starting_champions": self.starting_champions,
            "starting_keystones": self.starting_keystones,
            "kills": self.kills,
            "streak_length": self.streak_length,
        }
