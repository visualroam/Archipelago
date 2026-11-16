"""
AF Bot – leerer Slot für den AF-Charity-Bot (@af/ap-client).

Keine Locations, keine Items, Ziel sofort erfüllt. Der Bot verbindet sich mit diesem Slot nur, um
Admin-Befehle zu schicken (z. B. `!admin /deathlink`).

Einzige Ausnahme: die Option `late_start`. Damit kommt ein Streamer logisch erst ab einer bestimmten
Sphere ins Spiel (siehe `LateStart`). Ohne die Option beeinflusst der Slot die Multiworld überhaupt nicht.
"""
import logging
from dataclasses import dataclass
from typing import Dict, List, NamedTuple, Optional

from BaseClasses import CollectionState, Item, ItemClassification, Location, MultiWorld, Region
from Fill import swap_location_item
from Options import OptionDict, OptionError, PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World

logger = logging.getLogger("AF Bot")

# So viele Plätze probieren wir pro Sphere, bevor wir eine Sphere später suchen (jeder Versuch rechnet alle Spheres neu).
MAX_TRIES_PER_SPHERE = 25


class LateStart(OptionDict):
    """
    Streamer, die erst ab einer bestimmten Sphere ins Spiel kommen.

    Pro Streamer (Slot-Name) die gewünschte Sphere und ein Item aus seinem Spiel, das als „Start-Item“ dient:

        late_start:
          DerLiber:
            sphere: 3
            item: Imaginary Cookie

    Alle Checks dieses Streamers verlangen dann das Start-Item, und es liegt bei einem anderen Spieler in
    Sphere (sphere − 1). Vor der gewünschten Sphere hängt also niemand von diesem Streamer ab.
    `sphere` ist 2 oder 3. Später geht nicht verlässlich: Das Progression Balancing zieht den Weg zum
    Start-Item wieder nach vorn (nie vor Sphere 2, deshalb ist 3 sicher).
    Als `item` ein Item nehmen, das im Spiel nichts tut (es wird ganz normal an den Client geschickt).
    Es wird gegen ein Füll-Item des Streamers getauscht, die Zahl der Items bleibt gleich.
    """
    display_name = "Late Start"
    default = {}


@dataclass
class AFBotOptions(PerGameCommonOptions):
    late_start: LateStart


class AFBotWeb(WebWorld):
    tutorials = []


class _Gate(NamedTuple):
    player: int   # der Streamer, der später startet
    item: Item    # sein Start-Item
    sphere: int   # ab dieser Sphere soll er spielen können


def _sendable_spheres(multiworld: MultiWorld) -> Dict[Location, int]:
    """Sphere-Nummer je Check, gezählt wie in den Raum-Daten (und damit wie im AF-Admin-Tracker)."""
    result: Dict[Location, int] = {}
    number = 0
    for sphere in multiworld.get_sendable_spheres():
        if not sphere:
            break  # danach käme nur noch die Menge der unerreichbaren Checks
        number += 1
        for location in sphere:
            result[location] = number
    return result


class AFBotWorld(World):
    """Leerer Slot für den AF-Charity-Bot: keine Checks, keine Items."""

    game = "AF Bot"
    web = AFBotWeb()
    hidden = True  # nicht in den Spiel-Listen der Website anzeigen
    topology_present = False
    options_dataclass = AFBotOptions
    options: AFBotOptions

    # Je ein Dummy-Eintrag: Der WebHost lehnt Uploads mit leeren Item-/Location-Tabellen ab
    # ("Key 'item_name_to_id' error"). Erzeugt werden beide nie – der Slot bleibt leer.
    item_name_to_id = {"Nothing": 7_559_000_000}
    location_name_to_id = {"Bot Slot": 7_559_000_000}

    late_gates: List[_Gate]

    def create_regions(self) -> None:
        self.late_gates = []
        self.multiworld.regions.append(Region(self.origin_region_name, self.player, self.multiworld))

    def create_items(self) -> None:
        pass

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: True

    def create_item(self, name: str) -> Item:
        raise KeyError(f"AF Bot has no items ({name})")

    # --- late_start -------------------------------------------------------------------------------------------------
    # Ablauf: (1) vor dem Füllen bekommt der Streamer ein Start-Item, das alle seine Checks verlangen.
    #         (2) nach dem Füllen legen wir das Start-Item gezielt in die Sphere davor und sperren den Platz.
    #         (3) ganz am Ende (nach dem Progression Balancing) prüfen wir das Ergebnis und schreiben es ins Log.

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        # Läuft nach dem pre_fill aller Spieler: deren eigene Vorab-Platzierungen sind dann schon erledigt.
        for bot in multiworld.get_game_worlds(cls.game):
            bot._create_gates()

    @classmethod
    def stage_post_fill(cls, multiworld: MultiWorld) -> None:
        for bot in multiworld.get_game_worlds(cls.game):
            for gate in bot.late_gates:
                bot._place_gate(gate)

    @classmethod
    def stage_finalize_multiworld(cls, multiworld: MultiWorld) -> None:
        gates = [gate for bot in multiworld.get_game_worlds(cls.game) for gate in bot.late_gates]
        if not gates:
            return
        spheres = _sendable_spheres(multiworld)
        for gate in gates:
            name = multiworld.get_player_name(gate.player)
            location = gate.item.location
            first = min((s for loc, s in spheres.items() if loc.player == gate.player), default=None)
            if first is None or location not in spheres:
                raise Exception(f"AF Bot late_start: {name} hat nach dem Generieren keinen erreichbaren Check.")
            logger.info(f"late_start: {name} startet in Sphere {first}. Start-Item „{gate.item.name}“ liegt in "
                        f"Sphere {spheres[location]} bei {multiworld.get_player_name(location.player)}.")
            if first < gate.sphere:
                raise Exception(f"AF Bot late_start: {name} startet schon in Sphere {first} statt {gate.sphere}.")

    def _create_gates(self) -> None:
        multiworld = self.multiworld
        for name, config in sorted(self.options.late_start.value.items()):
            if not isinstance(config, dict) or set(config) != {"sphere", "item"}:
                raise OptionError(f"AF Bot late_start: „{name}“ braucht genau `sphere` und `item`.")
            sphere, item_name = config["sphere"], config["item"]
            if sphere not in (2, 3):
                raise OptionError(f"AF Bot late_start: `sphere` für „{name}“ muss 2 oder 3 sein.")
            player = multiworld.world_name_lookup.get(name)
            if player is None or player in multiworld.groups or player == self.player:
                names = ", ".join(multiworld.get_player_name(p) for p in multiworld.player_ids if p != self.player)
                raise OptionError(f"AF Bot late_start: Spieler „{name}“ gibt es nicht. Vorhanden: {names}")
            world = multiworld.worlds[player]
            if item_name not in world.item_name_to_id:
                raise OptionError(f"AF Bot late_start: „{item_name}“ ist kein Item von {world.game} ({name}).")
            locations = list(multiworld.get_locations(player))
            if not locations:
                raise OptionError(f"AF Bot late_start: {name} hat keine Checks.")

            # Start-Item gegen ein Füll-Item des Streamers tauschen, damit Items und Checks weiter aufgehen.
            index = self._replaceable_index(player, item_name)
            if index is None:
                raise OptionError(f"AF Bot late_start: {name} hat kein Füll-Item im Pool, das Platz machen könnte.")
            gate_item = world.create_item(item_name)
            gate_item.classification = ItemClassification.progression_skip_balancing
            multiworld.itempool[index] = gate_item

            # Alle Checks (und das Ziel) des Streamers verlangen das Start-Item. Gezählt werden nur Items, die
            # als Progression gelten – gleichnamige Füll-Items im Pool öffnen die Sperre also nicht.
            def has_gate(state: CollectionState, _name: str = item_name, _player: int = player) -> bool:
                return state.has(_name, _player)

            for location in locations:
                old_rule = location.access_rule
                location.access_rule = lambda state, old=old_rule, has=has_gate: has(state) and old(state)
            old_goal = multiworld.completion_condition[player]
            multiworld.completion_condition[player] = lambda state, old=old_goal, has=has_gate: has(state) and old(state)

            self.late_gates.append(_Gate(player, gate_item, sphere))

    def _replaceable_index(self, player: int, item_name: str) -> Optional[int]:
        """Index eines Items im Pool, das dem Start-Item Platz macht: am liebsten dasselbe Item, sonst Füllmaterial."""
        own = [(i, item) for i, item in enumerate(self.multiworld.itempool) if item.player == player]
        preferences = (
            lambda item: item.name == item_name and not item.advancement,
            lambda item: item.classification == ItemClassification.filler,
            lambda item: not item.advancement and not item.useful,
            lambda item: not item.advancement,
        )
        for wanted in preferences:
            for index, item in own:
                if wanted(item):
                    return index
        return None

    def _place_gate(self, gate: _Gate) -> None:
        multiworld = self.multiworld
        name = multiworld.get_player_name(gate.player)
        location = gate.item.location
        before = _sendable_spheres(multiworld)
        if location is None or location not in before:
            raise Exception(f"AF Bot late_start: Start-Item von {name} wurde nicht erreichbar platziert.")

        wanted = gate.sphere - 1
        current = before[location]
        if current != wanted:
            location = self._move_gate(gate, location, before, wanted) or location
        if before[location] < wanted:
            raise Exception(f"AF Bot late_start: Für {name} war kein Platz in Sphere {wanted} oder später frei. "
                            f"Bitte neu generieren (anderer Seed).")
        # Gesperrte Plätze fasst das Progression Balancing nicht an.
        location.locked = True

    def _move_gate(self, gate: _Gate, location: Location, before: Dict[Location, int],
                   wanted: int) -> Optional[Location]:
        """Tauscht das Start-Item mit einem unwichtigen Item in Sphere `wanted` (notfalls später). Gibt den neuen
        Platz zurück oder None, wenn kein Tausch geklappt hat."""
        multiworld = self.multiworld
        state = CollectionState(multiworld)
        current = before[location]
        # Liegt das Item schon später als gewünscht, suchen wir nur davor – später wäre keine Verbesserung.
        last = max(before.values()) if current < wanted else current - 1
        for sphere in range(wanted, last + 1):
            candidates = sorted(
                other for other, number in before.items()
                if number == sphere and other.player != gate.player and not other.locked
                and not other.item.advancement
                and other.can_fill(state, gate.item, False) and location.can_fill(state, other.item, False)
            )
            multiworld.random.shuffle(candidates)
            for candidate in candidates[:MAX_TRIES_PER_SPHERE]:
                swap_location_item(location, candidate, check_locked=False)
                after = _sendable_spheres(multiworld)
                # Nichts darf unerreichbar werden, und der neue Platz darf nicht früher drankommen als geplant.
                if after.keys() >= before.keys() and after[candidate] >= wanted:
                    before.clear()
                    before.update(after)
                    return candidate
                swap_location_item(location, candidate, check_locked=False)
        return None
