"""
AF Valorant – manuelle APWorld (kein Mod, kein Speicherzugriff → Vanguard-sicher).

Items sind Erlaubnisse: Ein Agent darf erst gespielt werden, wenn sein Item da ist.
Checks werden von Hand abgehakt (Mods im AF-Dashboard → `/send_location`).
Ziel: genug "Radianite Shard"s sammeln, dann das Finale gewinnen.
"""
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Options import PerGameCommonOptions, Range, Toggle
from worlds.AutoWorld import WebWorld, World

GAME = "AF Valorant"
BASE_ID = 7_560_000_000

AGENTS = [
    "Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor",
    "Iso", "Jett", "KAY/O", "Killjoy", "Miks", "Neon", "Omen", "Phoenix", "Raze", "Reyna",
    "Sage", "Skye", "Sova", "Tejo", "Veto", "Viper", "Vyse", "Waylay", "Yoru",
]

SHARD = "Radianite Shard"
FILLER = ["Bonus Credits", "Ult Orb", "Spray"]
TRAPS = ["Trap: Sheriff Only Round", "Trap: No Abilities Round", "Trap: Sensitivity x1.5 Match"]

GENERAL_CHECKS = [
    "Win a Pistol Round",
    "Get First Blood",
    "Plant the Spike 5 Times",
    "Finish Top 3 in Deathmatch",
    "Win a Spike Rush Match",
]
HARD_CHECKS = ["Win a 1v2 Clutch", "Get an Ace"]  # Glück → EXCLUDED, dort liegt nie Wichtiges
FINALE = "Finale: Win an Unrated Match"


def agent_checks(agent: str) -> list[str]:
    return [f"Win a Match as {agent}", f"Get 15 Kills as {agent}"]


def state_has(state, player: int):
    """has() für tracker_logic-Regeln auf einem CollectionState (Liste = eins davon)."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            return state.has_any(item, player)
        return state.has(item, player, count)
    return has


ALL_ITEMS = [f"Agent: {a}" for a in AGENTS] + [SHARD] + FILLER + TRAPS
ALL_LOCATIONS = [c for a in AGENTS for c in agent_checks(a)] + GENERAL_CHECKS + HARD_CHECKS


class StartingAgents(Range):
    """Wie viele Agents von Anfang an freigeschaltet sind."""
    display_name = "Starting Agents"
    range_start = 1
    range_end = 5
    default = 3


class AgentPoolSize(Range):
    """Wie viele (zufällige) Agents insgesamt im Spiel sind. Bestimmt die Zahl der Checks (2 pro Agent)."""
    display_name = "Agent Pool Size"
    range_start = 5
    range_end = len(AGENTS)
    default = 12


class ShardsTotal(Range):
    """Wie viele Radianite Shards in der Multiworld verteilt werden."""
    display_name = "Radianite Shards Total"
    range_start = 1
    range_end = 30
    default = 12


class ShardsRequired(Range):
    """Wie viele Shards fürs Finale nötig sind (wird auf Shards Total begrenzt)."""
    display_name = "Radianite Shards Required"
    range_start = 1
    range_end = 30
    default = 8


class HardChecks(Toggle):
    """Glücks-Checks (Clutch, Ace) hinzufügen. Dort liegt nie etwas Wichtiges."""
    display_name = "Hard Checks"


class TrapPercentage(Range):
    """Anteil der Füll-Items, die Traps sind (in %)."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 25


@dataclass
class AFValorantOptions(PerGameCommonOptions):
    starting_agents: StartingAgents
    agent_pool_size: AgentPoolSize
    shards_total: ShardsTotal
    shards_required: ShardsRequired
    hard_checks: HardChecks
    trap_percentage: TrapPercentage


class AFValorantItem(Item):
    game = GAME


class AFValorantLocation(Location):
    game = GAME


class AFValorantWeb(WebWorld):
    tutorials = [Tutorial(
        "Setup", "Manuelle Valorant-World für AF Charity", "English", "setup_en.md", "setup/en", ["AF Charity"],
    )]


class AFValorantWorld(World):
    """Valorant als manuelle Archipelago-World: Agents freischalten, Checks per Mod abhaken."""

    game = GAME
    web = AFValorantWeb()
    options_dataclass = AFValorantOptions
    options: AFValorantOptions
    topology_present = False

    item_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_ITEMS)}
    location_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_LOCATIONS)}
    item_name_groups = {"Agents": {f"Agent: {a}" for a in AGENTS}, "Traps": set(TRAPS)}

    def generate_early(self) -> None:
        pool_size = self.options.agent_pool_size.value
        starting = min(self.options.starting_agents.value, pool_size)
        self.agent_pool = sorted(self.random.sample(AGENTS, pool_size))
        self.starting_agents = sorted(self.random.sample(self.agent_pool, starting))
        # Shards dürfen nicht mehr sein als freie Locations (nach den Agent-Items).
        # Hard Checks zählen nicht: EXCLUDED, dort darf nichts Progressives liegen.
        locations = 2 * pool_size + len(GENERAL_CHECKS)
        free = locations - (pool_size - starting)
        self.shards_required = min(self.options.shards_required.value, self.options.shards_total.value, free)

    def create_regions(self) -> None:
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        names = [c for a in self.agent_pool for c in agent_checks(a)] + GENERAL_CHECKS
        if self.options.hard_checks:
            names += HARD_CHECKS
        self.location_names = list(names)  # für slot_data → AF-Dashboard (Checks abhaken)
        for name in names:
            loc = AFValorantLocation(self.player, name, self.location_name_to_id[name], menu)
            if name in HARD_CHECKS:
                loc.progress_type = LocationProgressType.EXCLUDED
            menu.locations.append(loc)

        # Finale als Event (keine echte Location-ID) mit Sieg-Item
        finale = AFValorantLocation(self.player, FINALE, None, menu)
        finale.place_locked_item(AFValorantItem("Victory", ItemClassification.progression, None, self.player))
        menu.locations.append(finale)

    def create_item(self, name: str) -> AFValorantItem:
        if name.startswith("Agent: ") or name == SHARD:
            cls = ItemClassification.progression
        elif name in TRAPS:
            cls = ItemClassification.trap
        else:
            cls = ItemClassification.filler
        return AFValorantItem(name, cls, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        for agent in self.starting_agents:
            self.multiworld.push_precollected(self.create_item(f"Agent: {agent}"))

        items = [self.create_item(f"Agent: {a}") for a in self.agent_pool if a not in self.starting_agents]
        unfilled = self.multiworld.get_unfilled_locations(self.player)
        slots = len(unfilled)
        open_slots = sum(1 for loc in unfilled if loc.progress_type != LocationProgressType.EXCLUDED)
        shards = max(self.shards_required, min(self.options.shards_total.value, open_slots - len(items)))
        items += [self.create_item(SHARD) for _ in range(shards)]
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
        pool: list[str] = slot_data["agent_pool"]
        required = slot_data["shards_required"]
        rules = {name: (lambda has, a=agent: has(f"Agent: {a}")) for agent in pool for name in agent_checks(agent)}
        rules[FINALE] = lambda has: has(SHARD, required)
        return {
            "rules": rules,
            "goal": FINALE,
            "counters": [{"item": SHARD, "required": required}],
            "groups": [{"title": "Agents", "items": [f"Agent: {a}" for a in pool]}],
        }

    def set_rules(self) -> None:
        for name, rule in self.tracker_logic(self.fill_slot_data())["rules"].items():
            self.get_location(name).access_rule = lambda state, r=rule: r(state_has(state, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "locations": self.location_names,
            "agent_pool": self.agent_pool,
            "starting_agents": self.starting_agents,
            "shards_required": self.shards_required,
        }
