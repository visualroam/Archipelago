"""
Regeln für den op.gg-Tracker: Welches Match zählt, was ist erlaubt, welche Checks gibt es, wie läuft die Serie.
Reine Funktionen ohne Archipelago-Abhängigkeit → leicht testbar.
"""
import re
from dataclasses import dataclass, field

# op.gg game_type. Normal Draft, Blind und Swiftplay laufen bei op.gg alle als "NORMAL".
COUNTING_QUEUES = {"SOLORANKED", "FLEXRANKED", "RANKED", "NORMAL"}
COUNTING_MAP = "SUMMONERS_RIFT"
REMAKE_SECONDS = 300  # kürzere Spiele = Remake → zählen gar nicht

POSITION_TO_ROLE = {
    "TOP": "Top", "JUNGLE": "Jungle", "MID": "Mid", "MIDDLE": "Mid",
    "ADC": "Bot", "BOTTOM": "Bot", "BOT": "Bot", "SUPPORT": "Support", "UTILITY": "Support",
}

# Riot-Perk-IDs → Keystone (DDragon 16.22.1)
KEYSTONE_IDS = {
    8005: "Press the Attack", 8008: "Lethal Tempo", 8021: "Fleet Footwork", 8010: "Conqueror",
    8112: "Electrocute", 8128: "Dark Harvest", 9923: "Hail of Blades",
    8214: "Summon Aery", 8229: "Arcane Comet", 8230: "Stormraider's Surge", 8992: "Deathfire Touch",
    8437: "Grasp of the Undying", 8439: "Aftershock", 8465: "Guardian",
    8351: "Glacial Augment", 8360: "Unsealed Spellbook", 8369: "First Strike",
}

# Tier-3-Stiefel zählen als ihr Tier-2-Stiefel
BOOT_UPGRADES = {
    "Swiftmarch": "Boots of Swiftness",
    "Crimson Lucidity": "Ionian Boots of Lucidity",
    "Chainlaced Crushers": "Mercury's Treads",
    "Armored Advance": "Plated Steelcaps",
    "Spellslinger's Shoes": "Sorcerer's Shoes",
    "Immortal Path": "Gluttonous Greaves",
    "Gunmetal Greaves": "Berserker's Greaves",
}


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


@dataclass
class Permissions:
    champions: set
    roles: set
    keystones: set
    boots: set                                       # freigeschaltete Tier-2-Stiefel
    boots_all: set = field(default_factory=set)      # alle Tier-2-Stiefel der World


@dataclass
class Evaluation:
    game_id: str
    counted: bool                 # zählt dieses Match überhaupt (Queue/Map/kein Remake)?
    reason: str = ""              # warum nicht gezählt / Regelverstoß
    win: bool = False
    champion: str = ""            # Name wie in der World (oder op.gg-Name, wenn unbekannt)
    role: str = ""
    kills: int = 0
    legal: bool = False           # nur freigeschaltete Sachen benutzt?
    violations: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    checks: list = field(default_factory=list)


def evaluate(game: dict, perms: Permissions, all_champions: list, kills_needed: int,
             riot_name: str = "") -> Evaluation:
    ev = Evaluation(game_id=str(game.get("id")), counted=False)
    gtype = (game.get("game_type") or "").upper()
    gmap = (game.get("game_map") or "").upper()
    if gmap != COUNTING_MAP or gtype not in COUNTING_QUEUES:
        ev.reason = f"Modus {gtype or '?'} zählt nicht"
        return ev
    if (game.get("game_length_second") or 0) < REMAKE_SECONDS:
        ev.reason = "Remake"
        return ev
    parts = game.get("participants") or []
    me = None
    for p in parts:
        s = p.get("summoner") or {}
        if not riot_name or norm(s.get("game_name")) == norm(riot_name):
            me = p
            break
    me = me or (parts[0] if parts else None)
    if not me:
        ev.reason = "Keine Spielerdaten"
        return ev
    stats = me.get("stats") or {}
    result = (stats.get("result") or "").upper()
    if result not in ("WIN", "LOSE"):
        ev.reason = "Remake"
        return ev

    ev.counted = True
    ev.win = result == "WIN"
    ev.kills = int(stats.get("kill") or 0)

    by_norm = {norm(c): c for c in all_champions}
    raw_champ = me.get("champion_name") or ""
    ev.champion = by_norm.get(norm(raw_champ), raw_champ)
    if ev.champion not in perms.champions:
        ev.violations.append(f"Champion {ev.champion} nicht freigeschaltet")

    pos = (me.get("position") or "").upper()
    ev.role = POSITION_TO_ROLE.get(pos, "")
    if not ev.role:
        ev.warnings.append(f"Rolle unbekannt ({pos or 'leer'}) – nicht geprüft")
    elif ev.role not in perms.roles:
        ev.violations.append(f"Rolle {ev.role} nicht freigeschaltet")

    rune_id = (me.get("rune") or {}).get("primary_rune_id")
    keystone = KEYSTONE_IDS.get(rune_id)
    if rune_id and not keystone:
        ev.warnings.append(f"Keystone-ID {rune_id} unbekannt – nicht geprüft")
    elif keystone and keystone not in perms.keystones:
        ev.violations.append(f"Keystone {keystone} nicht freigeschaltet")

    all_boots = {norm(b): b for b in perms.boots_all}
    for item in me.get("items_names") or []:
        boot = BOOT_UPGRADES.get(item, item)
        if norm(boot) in all_boots and all_boots[norm(boot)] not in perms.boots:
            ev.violations.append(f"Stiefel {all_boots[norm(boot)]} nicht freigeschaltet")

    ev.legal = not ev.violations
    if not ev.legal:
        ev.reason = "; ".join(ev.violations)
        return ev
    if ev.win:
        ev.checks.append(f"Win a Match as {ev.champion}")
    if ev.kills >= kills_needed:
        ev.checks.append(f"Get {kills_needed} Kills as {ev.champion}")
    if int(stats.get("largest_multi_kill") or 0) >= 5:
        ev.checks.append("Get a Pentakill")
    return ev


def update_streak(streak: list, ev: Evaluation, reuse_left: int) -> tuple[list, int, str]:
    """Gibt (neue Serie, verbrauchte Champion Reuses, Meldung) zurück. streak = Liste der Champions."""
    if not ev.counted:
        return streak, 0, ""
    if not ev.legal:
        return [], 0, "Serie zurückgesetzt (Regelverstoß)" if streak else ""
    if not ev.win:
        return [], 0, "Serie zurückgesetzt (Niederlage)" if streak else ""
    if ev.champion in streak:
        if reuse_left > 0:
            return streak + [ev.champion], 1, f"Champion Reuse für {ev.champion} verbraucht"
        return [ev.champion], 0, f"{ev.champion} war schon in der Serie → neue Serie startet"
    return streak + [ev.champion], 0, ""
