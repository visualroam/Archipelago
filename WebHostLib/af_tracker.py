"""
AF Charity: eigener Tracker für jeden Slot und eine Raum-Übersicht.

- /tracker/<id>               → Raum-Übersicht (alle Slots als Karten, Link je Slot)
- /tracker/<id>/<team>/<slot> → Slot-Tracker, für jedes Spiel
- /tracker/<id>/Generic       → alte Tabellen-Übersicht, /generic_tracker/… → alter Slot-Tracker

Welten mit `tracker_logic(slot_data)` (AF-Welten) und alle Manual-Welten bekommen zusätzlich „in Logik / gesperrt“, berechnet aus
denselben Regeln, die die World beim Generieren benutzt. Alle anderen Spiele: Checks, Items, Hinweise.

Abhaken (nur Welten ohne Client, also AF/Manual): Wer den geheimen Link des Slots hat (`…/<slot>#check=<key>`,
steht für den Raum-Besitzer auf der Raum-Seite), kann im Tracker Checks abhaken und das Ziel melden.
Der Tracker legt dafür einen Server-Befehl an (/send_location bzw. /goal), den der Raum binnen ~5 s ausführt.
"""
from __future__ import annotations

import collections
import datetime
import hashlib
import hmac
import re
import shlex
import unicodedata
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import UUID

from flask import abort, jsonify, render_template, request, url_for
from pony.orm import commit

from Utils import utcnow
from . import app
from .models import Command, Room

from NetUtils import ClientStatus, NetworkItem
from worlds.AutoWorld import AutoWorldRegister

STATUS = {
    ClientStatus.CLIENT_UNKNOWN: ("Offline", "off"),
    ClientStatus.CLIENT_CONNECTED: ("Verbunden", "on"),
    ClientStatus.CLIENT_READY: ("Bereit", "on"),
    ClientStatus.CLIENT_PLAYING: ("Spielt", "on"),
    ClientStatus.CLIENT_GOAL: ("Ziel erreicht", "goal"),
}

FLAG_PROGRESSION, FLAG_USEFUL, FLAG_TRAP = 0b001, 0b010, 0b100

_natural = re.compile(r"(\d+)")

# Box-Art wie auf der öffentlichen Seite (packages/shared GAME_CATALOG) – bei neuen Spielen dort UND hier eintragen
GAME_CATALOG = [
    ("Kingdom Hearts 3", ["Kingdom Hearts III"], "369585_IGDB"),
    ("Super Mario Odyssey", [], "493997_IGDB"),
    ("Overwatch", ["Overwatch 2"], "515025"),
    ("Minecraft", [], "27471_IGDB"),
    ("League of Legends", ["LoL"], "21779"),
    ("Pokémon Platin", ["Pokemon Platin", "Pokémon Platinum Version", "Pokemon Platinum"], "19745_IGDB"),
    ("LEGO Star Wars: The Complete Saga", ["Lego Star Wars"], "10209_IGDB"),
    ("Valorant", [], "516575"),
    ("Slime Rancher", [], "491177_IGDB"),
    ("Dark Souls 3", ["Dark Souls III"], "490292_IGDB"),
    ("Elden Ring", [], "512953_IGDB"),
    ("ULTRAKILL", [], "514166_IGDB"),
    ("Ratchet & Clank 3", ["Ratchet and Clank 3", "Ratchet & Clank: Up Your Arsenal"], "4540_IGDB"),
    ("Nine Sols", [], "715052357_IGDB"),
    ("Unfair Flips", [], "1786539857_IGDB"),
    ("R.E.P.O.", [], "1294658629_IGDB"),
]


def game_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", name.lower()))


def cover_url(game: str, width: int = 285) -> Optional[str]:
    """Twitch-Box-Art zum AP-Spielnamen („AF Overwatch“, „Manual_CustomOverwatch_AF“ → Overwatch, „Minecraft Fabric“ → Minecraft)."""
    key = game_key(re.sub(r"^AF\s+", "", game))
    best = None
    for name, aliases, box_art in GAME_CATALOG:
        for candidate in (name, *aliases):
            k = game_key(candidate)
            if key == k:
                return f"https://static-cdn.jtvnw.net/ttv-boxart/{box_art}-{width}x{width * 4 // 3}.jpg"
            if k in key and (best is None or len(k) > best[0]):
                best = (len(k), box_art)
    return f"https://static-cdn.jtvnw.net/ttv-boxart/{best[1]}-{width}x{width * 4 // 3}.jpg" if best else None


def display_game(game: str) -> str:
    """Anzeigename: „Manual_CustomOverwatch_AF“ → „Custom Overwatch · Manual“, sonst unverändert."""
    m = re.match(r"^Manual_(.+?)_[^_]+$", game)
    if not m:
        return game
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", m.group(1)).replace("_", " ")
    return f"{name} · Manual"


def natural_key(text: str):
    return [int(part) if part.isdigit() else part.lower() for part in _natural.split(text)]


def item_kind(flags: int) -> str:
    if flags & FLAG_TRAP:
        return "trap"
    if flags & FLAG_PROGRESSION:
        return "prog"
    if flags & FLAG_USEFUL:
        return "useful"
    return "filler"


def ago(delta: Optional[datetime.timedelta]) -> Optional[str]:
    if delta is None:
        return None
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "gerade eben"
    if seconds < 3600:
        return f"vor {seconds // 60} min"
    if seconds < 86400:
        return f"vor {seconds // 3600} h {seconds % 3600 // 60:02d} min"
    return f"vor {seconds // 86400} Tagen"


def status_of(tracker_data, team: int, player: int) -> Tuple[str, str]:
    return STATUS.get(tracker_data.get_player_client_status(team, player), ("Offline", "off"))


def world_of(game: str):
    return AutoWorldRegister.world_types.get(game)


def visible_players(tracker_data) -> List[Tuple[int, int]]:
    """Echte Spieler-Slots ohne versteckte Welten (AF Bot)."""
    result = []
    for team, players in tracker_data.get_all_players().items():
        for player in players:
            world = world_of(tracker_data.get_player_game(player))
            if world is not None and getattr(world, "hidden", False):
                continue
            result.append((team, player))
    return result


# ─── Gruppen für Spiele ohne eigene Logik ────────────────────────────────────

_PREFIX_SEPARATORS = (" :: ", ": ", " - ")


def group_locations(game: str, names: List[str]) -> Dict[str, List[str]]:
    """Location-Namen in Abschnitte teilen: zuerst die kleinste location_name_group der World,
    sonst ein gemeinsames Präfix („Caelid :: …“, „Olympus: …“), sonst „Sonstige“."""
    wanted = set(names)
    world = world_of(game)
    groups: Dict[str, List[str]] = collections.defaultdict(list)
    rest = list(names)

    if world is not None:
        candidates = sorted(
            ((title, set(members) & wanted) for title, members in world.location_name_groups.items()
             if title != "Everywhere"),
            key=lambda g: (len(g[1]), g[0]),
        )
        candidates = [(t, m) for t, m in candidates if 0 < len(m) < len(wanted)]
        if candidates:
            placed = set()
            for title, members in candidates:
                for name in members - placed:
                    groups[title].append(name)
                placed |= members
            rest = [n for n in names if n not in placed]

    for separator in _PREFIX_SEPARATORS:
        counts = collections.Counter(n.split(separator, 1)[0] for n in rest if separator in n)
        if sum(c for c in counts.values() if c >= 3) >= len(rest) / 2:
            remaining = []
            for name in rest:
                prefix = name.split(separator, 1)[0] if separator in name else None
                if prefix and counts[prefix] >= 3:
                    groups[prefix].append(name)
                else:
                    remaining.append(name)
            rest = remaining
            break

    if rest:
        groups["Sonstige" if groups else "Alle Checks"].extend(rest)
    return {title: sorted(members, key=natural_key)
            for title, members in sorted(groups.items(), key=lambda g: (g[0] == "Sonstige", natural_key(g[0])))}


# ─── Logik ───────────────────────────────────────────────────────────────────
# Zwei Quellen, gleiche Form {rules, goal, counters, groups}:
#   - AF-Welten: World.tracker_logic(slot_data) – dieselben Regeln wie set_rules
#   - Manual-Welten: die „requires“-Strings aus locations.json, ausgewertet wie im Manual-Framework

def make_has(inventory: collections.Counter, missing: List[str]) -> Callable[..., bool]:
    """has() für Regeln: zählt im Inventar und merkt sich, was fehlt. Manual-Regeln nutzen has.inventory/has.missing."""
    def has(item, count: int = 1) -> bool:
        if isinstance(item, (list, tuple, set)):
            ok = any(inventory[name] > 0 for name in item)
            if not ok:
                options = sorted(item, key=natural_key)
                missing.append("eins von: " + ", ".join(options) if len(options) <= 4
                               else f"eins von {len(options)}: " + ", ".join(options[:3]) + ", …")
            return ok
        ok = inventory[item] >= count
        if not ok:
            missing.append(item if count == 1 else f"{item} {inventory[item]}/{count}")
        return ok
    has.inventory = inventory
    has.missing = missing
    return has


def evaluate(rule: Optional[Callable], inventory: collections.Counter) -> Tuple[bool, List[str]]:
    if rule is None:
        return True, []
    missing: List[str] = []
    ok = bool(rule(make_has(inventory, missing)))
    return ok, missing


def is_manual(world) -> bool:
    return world is not None and hasattr(world, "location_name_to_location") and hasattr(world, "item_name_to_item")


def has_logic(world) -> bool:
    return world is not None and (hasattr(world, "tracker_logic") or is_manual(world))


_MANUAL_TOKEN = re.compile(r"\|[^|]+\||\{[^{}]+\}|\(|\)|\band\b|\bor\b", re.IGNORECASE)
_MANUAL_COUNT = re.compile(r"^\s*(\d+%?|ALL|HALF)\s*$", re.IGNORECASE)


class ManualRules:
    """Wertet Manual-„requires“ aus: |Item|, |Item:3|, |@Kategorie:5|, |…:ALL|, |…:HALF|, |…:50%|, and/or/Klammern,
    {OptionCount(@Kat, option)}, {OptionCountPercent(…)}, {YamlEnabled(o)}, {YamlDisabled(o)}.
    Unbekannte {Funktionen} gelten als erfüllt (lieber zu offen als fälschlich gesperrt)."""

    def __init__(self, world, slot_data: Dict[str, Any]):
        self.items: Dict[str, Dict[str, Any]] = world.item_name_to_item
        self.groups: Dict[str, set] = {k: set(v) for k, v in world.item_name_groups.items()}
        self.options = slot_data or {}

    # Ziel-Anzahl und vorhandene Anzahl für „Item“ oder „@Kategorie“
    def _total(self, ref: str) -> int:
        names = self.groups.get(ref[1:], set()) if ref.startswith("@") else {ref}
        return sum(int(self.items.get(n, {}).get("count", 1)) for n in names)

    def _have(self, ref: str, inventory) -> int:
        if ref.startswith("@"):
            return sum(inventory[n] for n in self.groups.get(ref[1:], ()))
        return inventory[ref]

    def _need(self, ref: str, spec: str) -> int:
        spec = spec.strip().upper()
        if spec == "ALL":
            return self._total(ref)
        if spec == "HALF":
            return max(1, self._total(ref) // 2)
        if spec.endswith("%"):
            return max(1, self._total(ref) * int(spec[:-1]) // 100)
        return int(spec)

    def _check(self, ref: str, need: int, inventory) -> Tuple[bool, List[str]]:
        have = self._have(ref, inventory)
        if have >= need:
            return True, []
        label = ref[1:] if ref.startswith("@") else ref
        return False, [label if need == 1 and not ref.startswith("@") else f"{label} {have}/{need}"]

    def _item(self, token: str, inventory) -> Tuple[bool, List[str]]:
        inner = token[1:-1].strip()
        if inner in self.items or inner[1:] in self.groups and inner.startswith("@"):
            return self._check(inner, 1, inventory)
        if ":" in inner:
            ref, spec = inner.rsplit(":", 1)
            if _MANUAL_COUNT.match(spec):
                return self._check(ref.strip(), self._need(ref.strip(), spec), inventory)
        return self._check(inner, 1, inventory)

    def _func(self, token: str, inventory) -> Tuple[bool, List[str]]:
        m = re.match(r"\{\s*(\w+)\s*\((.*)\)\s*\}$", token, re.S)
        if not m:
            return True, []
        name, args = m.group(1), [a.strip() for a in m.group(2).split(",")]
        if name in ("OptionCount", "OptionCountPercent") and len(args) == 2:
            value = self.options.get(args[1])
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return True, []
            spec = f"{int(value)}%" if name == "OptionCountPercent" else str(int(value))
            if spec in ("0", "0%"):
                return True, []
            return self._check(args[0], self._need(args[0], spec), inventory)
        if name == "YamlEnabled" and args:
            return bool(self.options.get(args[0])), []
        if name == "YamlDisabled" and args:
            return not self.options.get(args[0]), []
        return True, []

    def compile(self, requires) -> Optional[Callable]:
        if not requires:
            return None
        if isinstance(requires, list):  # Listen-Form: alle Items nötig, {"or": [...]} = eins davon
            parts = []
            for entry in requires:
                if isinstance(entry, dict) and "or" in entry:
                    parts.append("(" + " or ".join(f"|{x}|" for x in entry["or"]) + ")")
                else:
                    parts.append(f"|{entry}|")
            requires = " and ".join(parts)
        tokens = _MANUAL_TOKEN.findall(str(requires))

        def rule(has) -> bool:
            ok, missing = self._parse(tokens, has.inventory)
            has.missing.extend(missing)
            return ok
        return rule

    def _parse(self, tokens: List[str], inventory) -> Tuple[bool, List[str]]:
        pos = 0

        def expr():
            nonlocal pos
            ok, miss = term()
            while pos < len(tokens) and tokens[pos].lower() == "or":
                pos += 1
                ok2, miss2 = term()
                if ok or ok2:
                    ok, miss = True, []
                else:  # beide offen → den kürzeren Weg zeigen
                    miss = min(miss, miss2, key=len)
            return ok, miss

        def term():
            nonlocal pos
            ok, miss = factor()
            while pos < len(tokens) and tokens[pos].lower() == "and":
                pos += 1
                ok2, miss2 = factor()
                ok, miss = ok and ok2, miss + miss2
            return ok, miss

        def factor():
            nonlocal pos
            if pos >= len(tokens):
                return True, []
            token = tokens[pos]
            pos += 1
            if token == "(":
                result = expr()
                if pos < len(tokens) and tokens[pos] == ")":
                    pos += 1
                return result
            if token.startswith("|"):
                return self._item(token, inventory)
            if token.startswith("{"):
                return self._func(token, inventory)
            return True, []

        return expr()

    def counters(self, requires) -> List[Dict[str, Any]]:
        """Zähl-Ziele aus dem Goal: |@Kat:N|, |Item:N|, {OptionCount(@Kat, o)} – je Ziel der kleinste Wert."""
        found: Dict[str, int] = {}
        for token in _MANUAL_TOKEN.findall(str(requires or "")):
            ref, need = None, None
            if token.startswith("|"):
                inner = token[1:-1].strip()
                if ":" in inner and inner not in self.items:
                    r, spec = inner.rsplit(":", 1)
                    if _MANUAL_COUNT.match(spec):
                        ref, need = r.strip(), self._need(r.strip(), spec)
            elif token.startswith("{"):
                m = re.match(r"\{\s*(OptionCount(?:Percent)?)\s*\((.*)\)\s*\}$", token, re.S)
                if m:
                    args = [a.strip() for a in m.group(2).split(",")]
                    value = self.options.get(args[1]) if len(args) == 2 else None
                    if isinstance(value, int) and not isinstance(value, bool) and value > 0:
                        ref = args[0]
                        need = self._need(ref, f"{value}%" if m.group(1).endswith("Percent") else str(value))
            if ref and need and need > 1:
                found[ref] = min(found.get(ref, need), need)
        return [{"item": ref[1:] if ref.startswith("@") else ref,
                 "names": sorted(self.groups.get(ref[1:], ())) if ref.startswith("@") else [ref],
                 "required": need} for ref, need in found.items()]


def manual_logic(world, slot_data: Dict[str, Any]) -> Dict[str, Any]:
    manual = ManualRules(world, slot_data)
    locations: Dict[str, Dict[str, Any]] = world.location_name_to_location
    rules = {name: manual.compile(loc.get("requires")) for name, loc in locations.items()}

    victories = [name for name, loc in locations.items() if loc.get("victory")]
    goal = None
    if victories:
        index = slot_data.get("goal") if isinstance(slot_data.get("goal"), int) else 0
        goal = victories[index] if 0 <= index < len(victories) else victories[0]

    # Freischaltungen: Kategorien der Fortschritts-Items (ohne versteckte/Traps), Überschneidungen nur einmal
    hidden = {name for name, cat in (getattr(world, "category_table", {}) or {}).items()
              if isinstance(cat, dict) and cat.get("hidden")}
    progression = [i for i in world.item_name_to_item.values()
                   if (i.get("progression") or i.get("progression_skip_balancing")) and not i.get("trap")]
    order: List[str] = []
    members: Dict[str, List[str]] = collections.defaultdict(list)
    for item in progression:
        for cat in item.get("category", []):
            if cat not in hidden:
                if cat not in members:
                    order.append(cat)
                members[cat].append(item["name"])
    covered: set = set()
    chosen = []
    for cat in sorted(order, key=lambda c: len(members[c])):
        if set(members[cat]) - covered:
            chosen.append(cat)
            covered |= set(members[cat])
    groups = [{"title": cat, "items": members[cat]} for cat in order if cat in chosen]

    return {
        "rules": rules,
        "goal": goal,
        "counters": manual.counters(locations[goal].get("requires")) if goal else [],
        "groups": groups,
    }


def logic_source(game: str, slot_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    world = world_of(game)
    if world is None or not slot_data:
        return None
    try:
        if hasattr(world, "tracker_logic"):
            return world.tracker_logic(slot_data)
        if is_manual(world):
            return manual_logic(world, slot_data)
    except Exception:  # alter Seed ohne passende slot_data → einfach ohne Logik anzeigen
        return None
    return None


def build_logic(game: str, slot_data: Dict[str, Any], inventory: collections.Counter) -> Optional[Dict[str, Any]]:
    logic = logic_source(game, slot_data)
    if not logic:
        return None

    goal_name = logic.get("goal")
    goal_ok, goal_missing = evaluate(logic["rules"].get(goal_name), inventory) if goal_name else (False, [])
    counters = []
    for c in logic.get("counters", []):
        have = sum(inventory[n] for n in c["names"]) if "names" in c else inventory[c["item"]]
        counters.append({"item": c["item"], "have": have, "required": c["required"],
                         "pct": min(100, round(100 * have / c["required"])) if c["required"] else 100})

    groups = []
    for group in logic.get("groups", []):
        progressive = group.get("progressive")
        if progressive:
            have = inventory[progressive]
            items = [{"name": n, "owned": i <= have, "next": i == have + 1} for i, n in enumerate(group["items"])]
        else:
            items = [{"name": n, "owned": inventory[n] > 0, "next": False} for n in group["items"]]
        groups.append({"title": group["title"], "items": items,
                       "owned": sum(i["owned"] for i in items), "total": len(items)})

    return {
        "rules": logic["rules"],
        "goal": {"name": goal_name, "ok": goal_ok, "missing": goal_missing} if goal_name else None,
        "counters": counters,
        "groups": groups,
    }


def _unlock_names(game: str, slot_data: Dict[str, Any]) -> set:
    logic = logic_source(game, slot_data)
    if not logic:
        return set()
    names = set()
    for c in logic.get("counters", []):
        names.update(c.get("names", [c["item"]]))
    for group in logic.get("groups", []):
        names.update(group["items"] if not group.get("progressive") else [group["progressive"]])
    return names


def inventory_by_name(tracker_data, team: int, player: int) -> collections.Counter:
    """Inventar nach Item-Namen, inkl. Start-Items."""
    game = tracker_data.get_player_game(player)
    inventory = collections.Counter()
    for item_id, count in tracker_data.get_player_inventory_counts(team, player).items():
        inventory[tracker_data.item_id_to_name[game][item_id]] += count
    return inventory


# ─── Abhaken (Welten ohne Client) ────────────────────────────────────────────

def can_check_off(game: str) -> bool:
    """Nur Welten, die ohnehin von Hand abgehakt werden (AF-/Manual-Welten), nie echte Spiele mit Client."""
    world = world_of(game)
    return world is not None and not getattr(world, "hidden", False) and has_logic(world)


def check_key(room_id: UUID, team: int, player: int) -> str:
    secret = app.config["SECRET_KEY"]
    secret = secret if isinstance(secret, bytes) else str(secret).encode()
    return hmac.new(secret, f"af-check:{room_id}:{team}:{player}".encode(), hashlib.sha256).hexdigest()[:24]


def admin_key(room_id: UUID) -> str:
    """Admin-Schlüssel pro Raum: darf jeden Slot abhaken (auch echte Spiele) und sieht den Admin-Tracker."""
    secret = app.config["SECRET_KEY"]
    secret = secret if isinstance(secret, bytes) else str(secret).encode()
    return hmac.new(secret, f"af-admin:{room_id}".encode(), hashlib.sha256).hexdigest()[:24]


def is_admin(room, key: str) -> bool:
    return bool(key) and hmac.compare_digest(key, admin_key(room.id))


def admin_link(room) -> Optional[str]:
    if not room.tracker:
        return None
    return url_for("af_admin_tracker", tracker=room.tracker, _external=True) + f"#admin={admin_key(room.id)}"


app.jinja_env.globals["af_admin_link"] = admin_link


def check_links(room) -> List[Dict[str, Any]]:
    """Abhak-Links pro Slot – nur für den Raum-Besitzer auf der (nicht gecachten) Raum-Seite."""
    if not room.tracker:
        return []
    links = []
    for slot in sorted(room.seed.slots, key=lambda s: s.player_id):
        if can_check_off(slot.game):
            url = url_for("get_player_tracker", tracker=room.tracker, tracked_team=0, tracked_player=slot.player_id,
                          _external=True)
            links.append({"player": slot.player_id, "name": slot.player_name, "game": display_game(slot.game),
                          "url": f"{url}#check={check_key(room.id, 0, slot.player_id)}"})
    return links


app.jinja_env.globals["af_check_links"] = check_links


@app.route("/tracker/<suuid:tracker>/<int:team>/<int:player>/check", methods=["GET", "POST"])
def af_check_off(tracker: UUID, team: int, player: int):
    from .tracker import TrackerData  # hier importieren: tracker.py importiert dieses Modul ebenfalls

    room = Room.get(tracker=tracker)
    if room is None:
        abort(404)
    tracker_data = TrackerData(room)
    if player not in tracker_data._multidata["slot_info"] or team != 0:
        abort(404)
    game = tracker_data.get_player_game(player)
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else {}
    key = request.args.get("key", "") if request.method == "GET" else str(data.get("key", ""))
    admin = is_admin(room, key)  # Admin darf jeden Slot, auch echte Spiele mit Client
    valid = admin or (can_check_off(game) and hmac.compare_digest(key, check_key(room.id, team, player)))
    if request.method == "GET":
        return jsonify(ok=valid, admin=admin)
    if not valid:
        return jsonify(ok=False, error="Link ungültig"), 403

    name = tracker_data.get_player_name(player)
    if data.get("goal"):
        if tracker_data.get_player_client_status(team, player) == ClientStatus.CLIENT_GOAL:
            return jsonify(ok=True, already=True)
        logic = build_logic(game, tracker_data.get_slot_data(player), inventory_by_name(tracker_data, team, player))
        if not admin and (not logic or not logic["goal"] or not logic["goal"]["ok"]):
            return jsonify(ok=False, error="Das Ziel ist laut Logik noch nicht erreichbar."), 409
        command = f"/goal {shlex.quote(name)}"
    else:
        try:
            location = int(data.get("location"))
        except (TypeError, ValueError):
            return jsonify(ok=False, error="Location fehlt"), 400
        if location not in tracker_data.get_player_locations(player):
            return jsonify(ok=False, error="Diese Location gehört nicht zu diesem Slot"), 400
        if location in tracker_data.get_player_checked_locations(team, player):
            return jsonify(ok=True, already=True)
        command = f"/send_location {shlex.quote(name)} {location}"

    Command(room=room, commandtext=command)
    # Raum aufwecken, falls er schläft (wie ein Aufruf der Raum-Seite) – sonst wartet der Befehl
    now = utcnow()
    if now - room.last_activity > datetime.timedelta(minutes=1):
        room.last_activity = now
    commit()
    return jsonify(ok=True)


# ─── Admin-Tracker: alle Slots, Abhaken überall, „wo hängt's“ ──────────────────

@app.route("/tracker/<suuid:tracker>/admin")
def af_admin_tracker(tracker: UUID):
    """Nur die Hülle – Daten (mit Spoilern) holt die Seite per POST mit dem Admin-Schlüssel."""
    room = Room.get(tracker=tracker)
    if room is None:
        abort(404)
    return render_template("af/admin.html", room=room)


@app.route("/tracker/<suuid:tracker>/admin/data", methods=["POST"])
def af_admin_data(tracker: UUID):
    from .tracker import TrackerData

    room = Room.get(tracker=tracker)
    if room is None:
        abort(404)
    data = request.get_json(silent=True) or {}
    if not is_admin(room, str(data.get("key", ""))):
        return jsonify(ok=False, error="Admin-Link ungültig"), 403
    return jsonify(ok=True, **admin_overview(TrackerData(room)))


@app.route("/tracker/<suuid:tracker>/<int:team>/<int:player>/release", methods=["POST"])
def af_release(tracker: UUID, team: int, player: int):
    """Admin: offene Checks eines Slots freigeben – eine Sphere, alle bis zu einer Sphere oder den ganzen Rest.
    Gedacht für Streamer, die ausfallen (wie AP-Dropbot, nur per Klick)."""
    from .tracker import TrackerData

    room = Room.get(tracker=tracker)
    if room is None:
        abort(404)
    data = request.get_json(silent=True) or {}
    if not is_admin(room, str(data.get("key", ""))):
        return jsonify(ok=False, error="Admin-Link ungültig"), 403
    tracker_data = TrackerData(room)
    if player not in tracker_data._multidata["slot_info"] or team != 0:
        abort(404)
    name = tracker_data.get_player_name(player)
    mode = data.get("mode")
    open_ids = set(tracker_data.get_player_locations(player)) - tracker_data.get_player_checked_locations(team, player)
    if not open_ids:
        return jsonify(ok=True, count=0)

    if mode == "all":
        command, count = f"/release {shlex.quote(name)}", len(open_ids)
    elif mode in ("sphere", "upto"):
        try:
            target = int(data.get("sphere"))
        except (TypeError, ValueError):
            return jsonify(ok=False, error="Sphere fehlt"), 400
        sphere_of = {}
        for index, sphere in enumerate(tracker_data.get_spheres()):
            for location in sphere.get(player, ()):
                sphere_of[location] = index
        ids = sorted(i for i in open_ids if i in sphere_of
                     and (sphere_of[i] == target if mode == "sphere" else sphere_of[i] <= target))
        if not ids:
            return jsonify(ok=True, count=0)
        command, count = f"/send_location_ids {shlex.quote(name)} " + " ".join(map(str, ids)), len(ids)
    else:
        return jsonify(ok=False, error="mode muss sphere, upto oder all sein"), 400

    Command(room=room, commandtext=command)
    now = utcnow()
    if now - room.last_activity > datetime.timedelta(minutes=1):
        room.last_activity = now
    commit()
    return jsonify(ok=True, count=count)


def admin_overview(tracker_data, team: int = 0) -> Dict[str, Any]:
    """Alle Slots + Engpässe. Spoiler-lastig, daher nur über den Admin-Schlüssel."""
    names = tracker_data.get_room_long_player_names()
    games = tracker_data.get_room_games()
    item_names = tracker_data.item_id_to_name
    location_names = tracker_data.location_id_to_name
    activity = tracker_data.get_room_last_activity()
    players = [p for t, p in visible_players(tracker_data)]
    all_players = tracker_data.get_all_players()[team]

    sphere_of: Dict[Tuple[int, int], int] = {}
    for index, sphere in enumerate(tracker_data.get_spheres()):
        for slot, locations in sphere.items():
            for location in locations:
                sphere_of[slot, location] = index

    checked = {p: tracker_data.get_player_checked_locations(team, p) for p in all_players}
    slot_spheres = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))  # Slot → Sphere → [erl., ges.]
    waiting = collections.defaultdict(collections.Counter)   # Empfänger → {Halter: Anzahl}
    holding = collections.defaultdict(collections.Counter)   # Halter → {Empfänger: Anzahl}
    open_prog = []                                           # alle offenen Fortschritts-Checks
    spheres = collections.defaultdict(lambda: [0, 0])        # Sphere → [erledigt, gesamt]
    for p in all_players:
        game = games[(team, p)]
        for location, (item, receiver, flags) in tracker_data.get_player_locations(p).items():
            sphere = sphere_of.get((p, location))
            done = location in checked[p]
            if sphere is not None:
                spheres[sphere][1] += 1
                spheres[sphere][0] += done
                slot_spheres[p][sphere][1] += 1
                slot_spheres[p][sphere][0] += done
            if done or not flags & FLAG_PROGRESSION:
                continue
            holding[p][receiver] += 1
            waiting[receiver][p] += 1
            open_prog.append({
                "sphere": sphere if sphere is not None else 999,
                "slot": p, "slot_name": names[(team, p)],
                "location_id": location, "location": location_names[game][location],
                "item": item_names[games[(team, receiver)]][item],
                "receiver": receiver, "receiver_name": names[(team, receiver)] if receiver != p else "selbst",
            })
    open_prog.sort(key=lambda e: (e["sphere"], natural_key(e["slot_name"]), natural_key(e["location"])))
    frontier = open_prog[0]["sphere"] if open_prog else None

    slots = []
    for p in players:
        game = games[(team, p)]
        total = len(tracker_data.get_player_locations(p))
        done = len(checked[p])
        delta = activity.get((team, p))
        status_text, status_class = status_of(tracker_data, team, p)
        entry = {
            "player": p, "name": names[(team, p)], "game": display_game(game), "cover": cover_url(game),
            "status": status_text, "status_class": status_class,
            "idle": int(delta.total_seconds()) if delta is not None else None, "last_activity": ago(delta),
            "done": done, "total": total, "pct": round(100 * done / total) if total else 100,
            "url": url_for("get_player_tracker", tracker=tracker_data.room.tracker, tracked_team=team, tracked_player=p),
            "checkable": can_check_off(game),
            "waiting": sum(c for h, c in waiting[p].items() if h != p),
            "waiting_on": [{"slot": h, "name": names[(team, h)], "count": c}
                           for h, c in waiting[p].most_common() if h != p][:5],
            "own_open": waiting[p][p],
            "holding": sum(c for r, c in holding[p].items() if r != p),
            "holding_for": [{"slot": r, "name": names[(team, r)], "count": c}
                            for r, c in holding[p].most_common() if r != p][:5],
            "next": next((e for e in open_prog if e["slot"] == p), None),
            "spheres": [{"index": i, "done": d, "total": t} for i, (d, t) in sorted(slot_spheres[p].items())],
            "logic": None,
        }
        inventory = inventory_by_name(tracker_data, team, p)
        logic = build_logic(game, tracker_data.get_slot_data(p), inventory)
        if logic:
            open_ids = set(tracker_data.get_player_locations(p)) - checked[p]
            playable = sum(1 for loc in open_ids
                           if evaluate(logic["rules"].get(location_names[game][loc]), inventory)[0])
            entry["logic"] = {"playable": playable, "locked": len(open_ids) - playable,
                              "goal_ok": bool(logic["goal"] and logic["goal"]["ok"])}
        slots.append(entry)

    edges = [{"from": h, "to": r, "count": c} for h in players for r, c in holding[h].items()
             if r != h and r in players and c > 0]
    # „Jetzt“: nur wichtige Items aus den frühesten offenen Spheres – das, was gerade wirklich blockiert
    now = collections.Counter((e["slot"], e["receiver"]) for e in open_prog
                              if frontier is not None and e["sphere"] <= frontier + 2 and e["slot"] != e["receiver"])
    edges_now = [{"from": h, "to": r, "count": c} for (h, r), c in now.items() if h in players and r in players]
    return {
        "room": {"done": sum(len(checked[p]) for p in players),
                 "total": sum(len(tracker_data.get_player_locations(p)) for p in players),
                 "goals": sum(1 for s in slots if s["status_class"] == "goal"),
                 "frontier": frontier, "spheres_total": len(spheres)},
        "slots": slots,
        "edges": edges,
        "edges_now": edges_now,
        "spheres": [{"index": i, "done": d, "total": t} for i, (d, t) in sorted(spheres.items())],
        "bottleneck": [e for e in open_prog if frontier is not None and e["sphere"] <= frontier + 1][:60],
    }


# ─── Slot-Tracker ────────────────────────────────────────────────────────────

def render_af_player_tracker(tracker_data, team: int, player: int) -> str:
    game = tracker_data.get_player_game(player)
    games = tracker_data.get_room_games()
    names = tracker_data.get_room_long_player_names()
    item_names = tracker_data.item_id_to_name
    location_names = tracker_data.location_id_to_name

    inventory = inventory_by_name(tracker_data, team, player)

    # Empfangene Items: Reihenfolge, Herkunft, Art
    received: List[NetworkItem] = list(tracker_data.get_player_received_items(team, player))
    starting = tracker_data.get_player_starting_inventory(player)
    item_info: Dict[str, Dict[str, Any]] = {}
    def sender_label(net_item: NetworkItem) -> str:
        if not net_item.player:
            return "per Spende/Admin"
        if net_item.player == player:
            return "selbst gefunden"
        return "von " + names.get((team, net_item.player), "Server")

    for item_id in starting:
        name = item_names[game][item_id]
        info = item_info.setdefault(name, {"name": name, "count": 0, "kind": "filler", "order": -1, "start": True,
                                           "sources": collections.Counter()})
        info["count"] += 1
        info["sources"]["Start-Item"] += 1
    for order, net_item in enumerate(received):
        name = item_names[game][net_item.item]
        info = item_info.setdefault(name, {"name": name, "count": 0, "kind": "filler", "order": order, "start": False,
                                           "sources": collections.Counter()})
        info["count"] += 1
        info["order"] = order
        info["sources"][sender_label(net_item)] += 1
        kind = item_kind(net_item.flags)
        if kind != "filler":
            info["kind"] = kind
    if logic_unlocks := _unlock_names(game, tracker_data.get_slot_data(player)):
        for info in item_info.values():
            if info["kind"] == "filler" and info["name"] in logic_unlocks:
                info["kind"] = "prog"
    kind_rank = {"prog": 0, "useful": 1, "filler": 2, "trap": 3}
    items = sorted(item_info.values(), key=lambda i: (kind_rank[i["kind"]], natural_key(i["name"])))
    for info in items:  # „von menniphi, eybutti (2×) · Start-Item“
        label = lambda who, n: f"{who} ({n}×)" if n > 1 else who
        senders = [label(who[4:], n) for who, n in info["sources"].most_common() if who.startswith("von ")]
        others = [label(who, n) for who, n in info["sources"].most_common() if not who.startswith("von ")]
        info["from"] = " · ".join((["von " + ", ".join(senders)] if senders else []) + others)

    recent = []
    for index, net_item in reversed(list(enumerate(received))):
        sender_game = games.get((team, net_item.player), game)
        recent.append({
            "n": index + 1,
            "name": item_names[game][net_item.item],
            "kind": item_kind(net_item.flags),
            "from": names.get((team, net_item.player), "Server") if net_item.player else "Spende/Admin (Server)",
            "from_slot": net_item.player if net_item.player and net_item.player != player else None,
            "self": net_item.player == player,
            "location": location_names[sender_game][net_item.location] if net_item.location > 0 else None,
        })

    # Hinweise
    hints = sorted(tracker_data.get_player_hints(team, player), key=lambda h: (h.found, h.receiving_player != player))
    looking_for, to_find, found_hints = [], [], []
    for hint in hints:
        entry = {
            "item": item_names[games[(team, hint.receiving_player)]][hint.item],
            "location": location_names[games[(team, hint.finding_player)]][hint.location],
            "finder": names.get((team, hint.finding_player)),
            "finder_slot": hint.finding_player,
            "receiver": names.get((team, hint.receiving_player)),
            "receiver_slot": hint.receiving_player,
            "entrance": hint.entrance,
            "kind": item_kind(hint.item_flags),
        }
        if hint.found:
            found_hints.append(entry)
        elif hint.receiving_player == player:
            looking_for.append(entry)
        else:
            to_find.append(entry)
    hinted_here = {
        location_names[game][h.location]: f"{item_names[games[(team, h.receiving_player)]][h.item]} → "
                                          f"{names.get((team, h.receiving_player))}"
        for h in hints if h.finding_player == player and not h.found
    }

    # Checks
    location_ids = tracker_data.get_player_locations(player)
    checked_ids = tracker_data.get_player_checked_locations(team, player)
    logic = build_logic(game, tracker_data.get_slot_data(player), inventory)

    def found_at(location_id: int) -> Optional[Dict[str, Any]]:
        """Was an einer (erledigten) Location lag und wer es bekommen hat – kein Spoiler, ist ja schon gefunden."""
        meta = location_ids.get(location_id)
        if not meta:
            return None
        item_id, receiver, flags = meta[0], meta[1], meta[2]
        receiver_game = games.get((team, receiver), game)
        return {"item": item_names[receiver_game][item_id], "kind": item_kind(flags),
                "to": "selbst" if receiver == player else names.get((team, receiver), "?"),
                "to_slot": receiver if receiver != player else None}

    rows = []
    for location_id in location_ids:
        name = location_names[game][location_id]
        done = location_id in checked_ids
        state, missing = ("done", []) if done else ("open", [])
        if logic and not done:
            ok, missing = evaluate(logic["rules"].get(name), inventory)
            state = "logic" if ok else "locked"
        rows.append({"id": location_id, "name": name, "label": name, "state": state, "missing": missing,
                     "found": found_at(location_id) if done else None,
                     "hint": hinted_here.get(name)})

    if logic:
        titles = {"logic": "Jetzt spielbar", "locked": "Gesperrt", "done": "Erledigt"}
        sections = []
        for state in ("logic", "locked", "done"):
            members = sorted((r for r in rows if r["state"] == state), key=lambda r: natural_key(r["name"]))
            if members:
                sections.append({"title": titles[state], "rows": members, "state": state,
                                 "done": sum(r["state"] == "done" for r in members), "total": len(members)})
    else:
        by_name = {r["name"]: r for r in rows}
        sections = []
        for title, members in group_locations(game, list(by_name)).items():
            section_rows = [by_name[n] for n in members]
            for row in section_rows:  # Abschnittsname steht schon im Titel: „Caelid :: X“ → „X“
                for separator in _PREFIX_SEPARATORS:
                    if row["name"].startswith(title + separator):
                        row["label"] = row["name"][len(title + separator):]
                        break
            sections.append({"title": title, "rows": section_rows, "state": None,
                             "done": sum(r["state"] == "done" for r in section_rows), "total": len(section_rows)})

    checks_done = len(checked_ids)
    checks_total = len(location_ids)
    status_text, status_class = status_of(tracker_data, team, player)
    counts = collections.Counter(r["state"] for r in rows)

    return render_template(
        "af/player.html",
        room=tracker_data.room,
        team=team,
        player=player,
        player_name=names[(team, player)],
        game=display_game(game),
        cover=cover_url(game),
        checkable=can_check_off(game),
        status_text=status_text,
        status_class=status_class,
        last_activity=ago(tracker_data.get_player_last_activity(team, player)),
        checks_done=checks_done,
        checks_total=checks_total,
        pct=round(100 * checks_done / checks_total) if checks_total else 100,
        counts=counts,
        logic=logic,
        sections=sections,
        items=items,
        items_total=sum(inventory.values()),
        recent=recent,
        looking_for=looking_for,
        to_find=to_find,
        found_hints=found_hints,
        slots=[{"team": t, "player": p, "name": names[(t, p)], "game": display_game(games[(t, p)])}
               for t, p in visible_players(tracker_data)],
        saving_second=tracker_data.get_room_saving_second(),
    )


# ─── Raum-Übersicht ──────────────────────────────────────────────────────────

def render_af_room_tracker(tracker_data) -> str:
    names = tracker_data.get_room_long_player_names()
    games = tracker_data.get_room_games()
    activity = tracker_data.get_room_last_activity()
    cards = []
    for team, player in visible_players(tracker_data):
        total = len(tracker_data.get_player_locations(player))
        done = len(tracker_data.get_player_checked_locations(team, player))
        status_text, status_class = status_of(tracker_data, team, player)
        delta = activity.get((team, player))
        cards.append({
            "team": team,
            "player": player,
            "name": names[(team, player)],
            "game": display_game(games[(team, player)]),
            "cover": cover_url(games[(team, player)]),
            "done": done,
            "total": total,
            "pct": round(100 * done / total) if total else 100,
            "status_text": status_text,
            "status_class": status_class,
            "last_activity": ago(delta),
            "idle": delta.total_seconds() if delta is not None else None,
            "items": sum(tracker_data.get_player_inventory_counts(team, player).values()),
            "logic": has_logic(world_of(games[(team, player)])),
        })
    # Aktive zuerst, dann nach Fortschritt
    cards.sort(key=lambda c: (c["status_class"] == "goal", c["idle"] is None, -c["pct"], natural_key(c["name"])))

    done = sum(c["done"] for c in cards)
    total = sum(c["total"] for c in cards)
    return render_template(
        "af/room.html",
        room=tracker_data.room,
        cards=cards,
        done=done,
        total=total,
        pct=round(100 * done / total) if total else 100,
        goals=sum(c["status_class"] == "goal" for c in cards),
        online=sum(c["status_class"] == "on" for c in cards),
        saving_second=tracker_data.get_room_saving_second(),
    )
