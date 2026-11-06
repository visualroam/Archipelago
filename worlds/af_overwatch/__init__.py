"""
AF Overwatch – manuelle APWorld (kein Mod, kein Speicherzugriff).

Items sind Erlaubnisse: Ein Hero darf erst gespielt werden, wenn seine Rolle UND der Hero freigeschaltet sind.
Checks werden von Hand abgehakt (Mods im AF-Dashboard → `/send_location`).
Ziel: genug "Pachimari"s sammeln, dann das Finale gewinnen (ein Sieg in jeder Rolle).
"""
from dataclasses import dataclass

from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Options import PerGameCommonOptions, Range, Toggle
from worlds.AutoWorld import WebWorld, World

GAME = "AF Overwatch"
BASE_ID = 7_561_000_000

HEROES = {
    "Tank": [
        "D.Va", "Domina", "Doomfist", "Hazard", "Junker Queen", "Mauga", "Orisa", "Ramattra", "Reinhardt",
        "Roadhog", "Sigma", "Winston", "Wrecking Ball", "Zarya",
    ],
    "Damage": [
        "Anran", "Ashe", "Bastion", "Cassidy", "Echo", "Emre", "Freja", "Genji", "Hanzo", "Junkrat", "Mei",
        "Pharah", "Reaper", "Sierra", "Sojourn", "Soldier: 76", "Sombra", "Symmetra", "Torbjorn", "Tracer",
        "Vendetta", "Venture", "Widowmaker",
    ],
    "Support": [
        "Ana", "Baptiste", "Brigitte", "Illari", "Jetpack Cat", "Juno", "Kiriko", "Lifeweaver", "Lucio",
        "Mercy", "Mizuki", "Moira", "Wuyang", "Zenyatta",
    ],
}
ROLES = list(HEROES)
ROLE_OF = {hero: role for role, heroes in HEROES.items() for hero in heroes}
ALL_HEROES = [h for heroes in HEROES.values() for h in heroes]

MACGUFFIN = "Pachimari"
FILLER = ["Bonus XP", "Spray", "Voice Line"]
TRAPS = ["Trap: Mystery Heroes Match", "Trap: No Ultimate Match", "Trap: Next Kill Must Be Melee"]

STAT_CHECK = {
    "Tank": "Mitigate 8,000 Damage as {}",
    "Damage": "Get 20 Eliminations as {}",
    "Support": "Heal 8,000 as {}",
}
GENERAL_CHECKS = ["Win a Quick Play Match", "Win an Arcade Match"]
ROLE_CHECKS = {role: f"Win a Match as {role}" for role in ROLES}
HARD_CHECKS = ["Get Play of the Game", "Get a 4-Elimination Streak"]  # Glück → EXCLUDED
FINALE = "Finale: Win a Match in Every Role"


def hero_checks(hero: str) -> list[str]:
    return [f"Win a Match as {hero}", STAT_CHECK[ROLE_OF[hero]].format(hero)]


def state_has(state, player: int):
    """has() für tracker_logic-Regeln auf einem CollectionState (Liste = eins davon)."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            return state.has_any(item, player)
        return state.has(item, player, count)
    return has


ALL_ITEMS = [f"Role: {r}" for r in ROLES] + [f"Hero: {h}" for h in ALL_HEROES] + [MACGUFFIN] + FILLER + TRAPS
ALL_LOCATIONS = ([c for h in ALL_HEROES for c in hero_checks(h)] + GENERAL_CHECKS + list(ROLE_CHECKS.values())
                 + HARD_CHECKS)


class HeroesPerRole(Range):
    """Wie viele (zufällige) Heroes pro Rolle im Spiel sind. 2 Checks pro Hero."""
    display_name = "Heroes per Role"
    range_start = 2
    range_end = 14
    default = 5


class StartingHeroes(Range):
    """Wie viele Heroes der Start-Rolle von Anfang an freigeschaltet sind."""
    display_name = "Starting Heroes"
    range_start = 1
    range_end = 3
    default = 2


class PachimarisTotal(Range):
    """Wie viele Pachimaris in der Multiworld verteilt werden."""
    display_name = "Pachimaris Total"
    range_start = 1
    range_end = 30
    default = 12


class PachimarisRequired(Range):
    """Wie viele Pachimaris fürs Finale nötig sind (wird auf Pachimaris Total begrenzt)."""
    display_name = "Pachimaris Required"
    range_start = 1
    range_end = 30
    default = 8


class HardChecks(Toggle):
    """Glücks-Checks (POTG, Streak) hinzufügen. Dort liegt nie etwas Wichtiges."""
    display_name = "Hard Checks"


class TrapPercentage(Range):
    """Anteil der Füll-Items, die Traps sind (in %)."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 25


@dataclass
class AFOverwatchOptions(PerGameCommonOptions):
    heroes_per_role: HeroesPerRole
    starting_heroes: StartingHeroes
    pachimaris_total: PachimarisTotal
    pachimaris_required: PachimarisRequired
    hard_checks: HardChecks
    trap_percentage: TrapPercentage


class AFOverwatchItem(Item):
    game = GAME


class AFOverwatchLocation(Location):
    game = GAME


class AFOverwatchWeb(WebWorld):
    tutorials = [Tutorial(
        "Setup", "Manuelle Overwatch-World für AF Charity", "English", "setup_en.md", "setup/en", ["AF Charity"],
    )]


class AFOverwatchWorld(World):
    """Overwatch als manuelle Archipelago-World: Rollen + Heroes freischalten, Checks per Mod abhaken."""

    game = GAME
    web = AFOverwatchWeb()
    options_dataclass = AFOverwatchOptions
    options: AFOverwatchOptions
    topology_present = False

    item_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_ITEMS)}
    location_name_to_id = {name: BASE_ID + i for i, name in enumerate(ALL_LOCATIONS)}
    item_name_groups = {
        "Roles": {f"Role: {r}" for r in ROLES},
        "Heroes": {f"Hero: {h}" for h in ALL_HEROES},
        "Traps": set(TRAPS),
    }

    def generate_early(self) -> None:
        per_role = self.options.heroes_per_role.value
        self.hero_pool = {role: sorted(self.random.sample(heroes, per_role)) for role, heroes in HEROES.items()}
        self.starting_role = self.random.choice(ROLES)
        self.starting_heroes = sorted(self.random.sample(self.hero_pool[self.starting_role],
                                                         min(self.options.starting_heroes.value, per_role)))
        # Pachimaris dürfen nicht mehr sein als freie Locations (nach Rollen- und Hero-Items).
        # Hard Checks zählen nicht: EXCLUDED, dort darf nichts Progressives liegen.
        locations = 6 * per_role + len(GENERAL_CHECKS) + len(ROLE_CHECKS)
        free = locations - (len(ROLES) - 1) - (3 * per_role - len(self.starting_heroes))
        self.pachimaris_required = min(self.options.pachimaris_required.value,
                                       self.options.pachimaris_total.value, free)

    def create_regions(self) -> None:
        menu = Region(self.origin_region_name, self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        names = [c for heroes in self.hero_pool.values() for h in heroes for c in hero_checks(h)]
        names += GENERAL_CHECKS + list(ROLE_CHECKS.values())
        if self.options.hard_checks:
            names += HARD_CHECKS
        self.location_names = list(names)  # für slot_data → AF-Dashboard (Checks abhaken)
        for name in names:
            loc = AFOverwatchLocation(self.player, name, self.location_name_to_id[name], menu)
            if name in HARD_CHECKS:
                loc.progress_type = LocationProgressType.EXCLUDED
            menu.locations.append(loc)

        finale = AFOverwatchLocation(self.player, FINALE, None, menu)
        finale.place_locked_item(AFOverwatchItem("Victory", ItemClassification.progression, None, self.player))
        menu.locations.append(finale)

    def create_item(self, name: str) -> AFOverwatchItem:
        if name.startswith(("Role: ", "Hero: ")) or name == MACGUFFIN:
            cls = ItemClassification.progression
        elif name in TRAPS:
            cls = ItemClassification.trap
        else:
            cls = ItemClassification.filler
        return AFOverwatchItem(name, cls, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        self.multiworld.push_precollected(self.create_item(f"Role: {self.starting_role}"))
        for hero in self.starting_heroes:
            self.multiworld.push_precollected(self.create_item(f"Hero: {hero}"))

        items = [self.create_item(f"Role: {r}") for r in ROLES if r != self.starting_role]
        items += [self.create_item(f"Hero: {h}") for heroes in self.hero_pool.values() for h in heroes
                  if h not in self.starting_heroes]
        unfilled = self.multiworld.get_unfilled_locations(self.player)
        slots = len(unfilled)
        open_slots = sum(1 for loc in unfilled if loc.progress_type != LocationProgressType.EXCLUDED)
        count = max(self.pachimaris_required, min(self.options.pachimaris_total.value, open_slots - len(items)))
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
        pool: dict[str, list[str]] = slot_data["hero_pool"]
        required = slot_data["pachimaris_required"]

        def can_play(has, role: str) -> bool:
            return all([has(f"Role: {role}"), has([f"Hero: {h}" for h in pool[role]])])

        rules = {}
        for role, heroes in pool.items():
            for hero in heroes:
                for name in hero_checks(hero):
                    rules[name] = lambda has, r=role, h=hero: all([has(f"Role: {r}"), has(f"Hero: {h}")])
            rules[ROLE_CHECKS[role]] = lambda has, r=role: can_play(has, r)
        rules[FINALE] = lambda has: all([has(MACGUFFIN, required), *[can_play(has, r) for r in ROLES]])
        return {
            "rules": rules,
            "goal": FINALE,
            "counters": [{"item": MACGUFFIN, "required": required}],
            "groups": [{"title": "Rollen", "items": [f"Role: {r}" for r in ROLES]}]
            + [{"title": f"Heroes · {r}", "items": [f"Hero: {h}" for h in pool[r]]} for r in ROLES],
        }

    def set_rules(self) -> None:
        for name, rule in self.tracker_logic(self.fill_slot_data())["rules"].items():
            self.get_location(name).access_rule = lambda state, r=rule: r(state_has(state, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "locations": self.location_names,
            "hero_pool": self.hero_pool,
            "starting_role": self.starting_role,
            "starting_heroes": self.starting_heroes,
            "pachimaris_required": self.pachimaris_required,
        }
