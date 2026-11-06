"""
AF Charity: eigener Tracker für jeden Slot und eine Raum-Übersicht.

- /tracker/<id>               → Raum-Übersicht (alle Slots als Karten, Link je Slot)
- /tracker/<id>/<team>/<slot> → Slot-Tracker, für jedes Spiel
- /tracker/<id>/Generic       → alte Tabellen-Übersicht, /generic_tracker/… → alter Slot-Tracker

Welten mit `tracker_logic(slot_data)` (die AF-Welten) bekommen zusätzlich „in Logik / gesperrt“, berechnet aus
denselben Regeln, die die World beim Generieren benutzt. Alle anderen Spiele: Checks, Items, Hinweise.
"""
from __future__ import annotations

import collections
import datetime
import re
import unicodedata
from typing import Any, Callable, Dict, List, Optional, Tuple

from flask import render_template

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
]


def game_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", name.lower()))


def cover_url(game: str, width: int = 285) -> Optional[str]:
    """Twitch-Box-Art zum AP-Spielnamen („AF Overwatch“ → Overwatch, „Minecraft Fabric“ → Minecraft)."""
    key = game_key(re.sub(r"^AF\s+", "", game))
    best = None
    for name, aliases, box_art in GAME_CATALOG:
        for candidate in (name, *aliases):
            k = game_key(candidate)
            if key == k:
                return f"https://static-cdn.jtvnw.net/ttv-boxart/{box_art}-{width}x{width * 4 // 3}.jpg"
            if key.startswith(k) and (best is None or len(k) > best[0]):
                best = (len(k), box_art)
    return f"https://static-cdn.jtvnw.net/ttv-boxart/{best[1]}-{width}x{width * 4 // 3}.jpg" if best else None


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


# ─── Logik (AF-Welten) ───────────────────────────────────────────────────────

def make_has(inventory: collections.Counter, missing: List[str]) -> Callable[..., bool]:
    """has() für tracker_logic-Regeln: zählt im Inventar und merkt sich, was fehlt."""
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
    return has


def evaluate(rule: Optional[Callable], inventory: collections.Counter) -> Tuple[bool, List[str]]:
    if rule is None:
        return True, []
    missing: List[str] = []
    ok = bool(rule(make_has(inventory, missing)))
    return ok, missing


def build_logic(game: str, slot_data: Dict[str, Any], inventory: collections.Counter) -> Optional[Dict[str, Any]]:
    world = world_of(game)
    if world is None or not hasattr(world, "tracker_logic") or not slot_data:
        return None
    try:
        logic = world.tracker_logic(slot_data)
    except Exception:  # alter Seed ohne passende slot_data → einfach ohne Logik anzeigen
        return None

    goal_name = logic.get("goal")
    goal_ok, goal_missing = evaluate(logic["rules"].get(goal_name), inventory) if goal_name else (False, [])
    counters = [{
        "item": c["item"],
        "have": inventory[c["item"]],
        "required": c["required"],
        "pct": min(100, round(100 * inventory[c["item"]] / c["required"])) if c["required"] else 100,
    } for c in logic.get("counters", [])]

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
    world = world_of(game)
    if world is None or not hasattr(world, "tracker_logic") or not slot_data:
        return set()
    try:
        logic = world.tracker_logic(slot_data)
    except Exception:
        return set()
    names = {c["item"] for c in logic.get("counters", [])}
    for group in logic.get("groups", []):
        names.update(group["items"] if not group.get("progressive") else [group["progressive"]])
    return names


# ─── Slot-Tracker ────────────────────────────────────────────────────────────

def render_af_player_tracker(tracker_data, team: int, player: int) -> str:
    game = tracker_data.get_player_game(player)
    games = tracker_data.get_room_games()
    names = tracker_data.get_room_long_player_names()
    item_names = tracker_data.item_id_to_name
    location_names = tracker_data.location_id_to_name

    # Inventar nach Namen (inkl. Start-Items)
    inventory = collections.Counter()
    for item_id, count in tracker_data.get_player_inventory_counts(team, player).items():
        inventory[item_names[game][item_id]] += count

    # Empfangene Items: Reihenfolge, Herkunft, Art
    received: List[NetworkItem] = list(tracker_data.get_player_received_items(team, player))
    starting = tracker_data.get_player_starting_inventory(player)
    item_info: Dict[str, Dict[str, Any]] = {}
    for item_id in starting:
        name = item_names[game][item_id]
        info = item_info.setdefault(name, {"name": name, "count": 0, "kind": "filler", "order": -1, "start": True})
        info["count"] += 1
    for order, net_item in enumerate(received):
        name = item_names[game][net_item.item]
        info = item_info.setdefault(name, {"name": name, "count": 0, "kind": "filler", "order": order, "start": False})
        info["count"] += 1
        info["order"] = order
        kind = item_kind(net_item.flags)
        if kind != "filler":
            info["kind"] = kind
    if logic_unlocks := _unlock_names(game, tracker_data.get_slot_data(player)):
        for info in item_info.values():
            if info["kind"] == "filler" and info["name"] in logic_unlocks:
                info["kind"] = "prog"
    kind_rank = {"prog": 0, "useful": 1, "filler": 2, "trap": 3}
    items = sorted(item_info.values(), key=lambda i: (kind_rank[i["kind"]], natural_key(i["name"])))

    recent = []
    for net_item in reversed(received[-12:]):
        sender_game = games.get((team, net_item.player), game)
        recent.append({
            "name": item_names[game][net_item.item],
            "kind": item_kind(net_item.flags),
            "from": names.get((team, net_item.player), "Server") if net_item.player else "Server",
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

    rows = []
    for location_id in location_ids:
        name = location_names[game][location_id]
        done = location_id in checked_ids
        state, missing = ("done", []) if done else ("open", [])
        if logic and not done:
            ok, missing = evaluate(logic["rules"].get(name), inventory)
            state = "logic" if ok else "locked"
        rows.append({"name": name, "label": name, "state": state, "missing": missing, "hint": hinted_here.get(name)})

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
        game=game,
        cover=cover_url(game),
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
        slots=[{"team": t, "player": p, "name": names[(t, p)], "game": games[(t, p)]}
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
            "game": games[(team, player)],
            "cover": cover_url(games[(team, player)]),
            "done": done,
            "total": total,
            "pct": round(100 * done / total) if total else 100,
            "status_text": status_text,
            "status_class": status_class,
            "last_activity": ago(delta),
            "idle": delta.total_seconds() if delta is not None else None,
            "items": sum(tracker_data.get_player_inventory_counts(team, player).values()),
            "logic": hasattr(world_of(games[(team, player)]), "tracker_logic"),
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
