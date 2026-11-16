"""
Custom Valorant AF – op.gg Client.

Verbindet sich mit dem Archipelago-Slot (Spiel Manual_Valorant_AF) und schaut jede Minute auf op.gg nach
neuen Valorant-Spielen. Erkannte Checks (Win, Match MVP, Kill Bomb) und das Ziel werden automatisch geschickt.
An Items, Checks und Logik der APWorld ändert dieser Client nichts – er hakt nur ab, was sonst per Hand
im Manual Client geklickt wird.

Start: Archipelago Launcher -> "Custom Valorant AF op.gg Client". Verbinden wie immer, dann die Riot-ID
einfach ins Eingabefeld tippen, z. B.  FireFlo#Fire
"""
import asyncio
import json
import os
import re
import time

import Utils
from CommonClient import (ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, handle_url_arg,
                          logger, server_loop)
from NetUtils import ClientStatus

from .Game import game_name as GAME
from .Items import item_id_to_name, item_name_to_item
from .Locations import location_name_to_id
from .opgg_valorant import AGENT_IDS, OpggError, fetch_agent_ids, fetch_matches

POLL_SECONDS = 60
COUNTING_QUEUES = {"unrated"}          # nur Unrated zählt
KILL_BOMB = 25                         # Standard, falls slot_data nichts liefert
RIOT_ID = re.compile(r"^\s*([^#/!][^#]{0,31}?)\s*#\s*([^\s#]{2,5})\s*$")

AGENTS = sorted(n for n, i in item_name_to_item.items() if "Agenten" in i.get("category", []))
WEAPONS = sorted(n for n, i in item_name_to_item.items() if "Waffen" in i.get("category", []))


class ValorantCommands(ClientCommandProcessor):
    def _cmd_riot(self, *riot_id: str) -> bool:
        """Riot-ID setzen: /riot Name#TAG"""
        if not self.ctx.set_riot_id(" ".join(riot_id)):
            self.output("Format: /riot Name#TAG, z. B. /riot FireFlo#Fire")
            return False
        return True

    def _cmd_unlocks(self) -> bool:
        """Freigeschaltete Agenten, Waffen und Extras anzeigen"""
        self.ctx.show_status()
        return True

    def _cmd_opgg(self) -> bool:
        """op.gg sofort abfragen statt auf die nächste Minute zu warten"""
        self.ctx.poll_event.set()
        return True


class ValorantContext(CommonContext):
    game = GAME
    items_handling = 0b111  # alle Items inkl. Start-Agent
    command_processor = ValorantCommands

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.slot_data: dict | None = None
        self.state: dict = {}
        self.state_file: str | None = None
        self.poll_event = asyncio.Event()
        self.agent_ids = dict(AGENT_IDS)
        self.agents_refreshed = False

    # ------------------------------------------------------------- Verbindung
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args.get("slot_data") or {}
            self.load_state()
            logger.info(f"Zählende Modi: {', '.join(sorted(self.counting_queues()))}")
            if self.state.get("riot_id"):
                logger.info(f"op.gg-Tracker aktiv für {self.state['riot_id']}.")
            else:
                logger.info("Gib jetzt deine Riot-ID ein, z. B.  FireFlo#Fire")
            self.poll_event.set()
        elif cmd == "ReceivedItems" and self.slot_data is not None:
            for net_item in args.get("items", []):
                name = item_id_to_name.get(net_item.item)
                if name and args.get("index", 0) > 0:
                    logger.info(f"Neu freigeschaltet: {name}")

    def on_user_say(self, text: str):
        if RIOT_ID.match(text) and not self.state.get("riot_id"):
            self.set_riot_id(text)
            return None
        return text

    # ------------------------------------------------------------- Zustand
    def load_state(self):
        folder = Utils.user_path("Custom_Valorant_AF")
        os.makedirs(folder, exist_ok=True)
        seed = self.server_seed_name or self.seed_name or "seed"
        self.state_file = os.path.join(folder, f"{seed}_{self.slot}.json")
        state = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, encoding="utf-8") as f:
                    state = json.load(f)
            except Exception as e:
                logger.warning(f"Konnte {self.state_file} nicht lesen: {e}")
        state.setdefault("riot_id", "")
        state.setdefault("seen", [])
        state.setdefault("baseline_done", False)
        self.state = state

    def save_state(self):
        if not self.state_file:
            return
        tmp = self.state_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=1, ensure_ascii=False)
        os.replace(tmp, self.state_file)

    def set_riot_id(self, text: str) -> bool:
        m = RIOT_ID.match(text)
        if not m:
            return False
        if not self.state_file:
            logger.info("Erst mit dem Archipelago-Server verbinden, dann die Riot-ID eingeben.")
            return True
        new_id = f"{m.group(1).strip()}#{m.group(2)}"
        if norm_id(self.state.get("riot_id")) != norm_id(new_id):
            self.state.update(seen=[], baseline_done=False)  # alte Spiele nicht nachträglich werten
        self.state["riot_id"] = new_id
        self.save_state()
        logger.info(f"Riot-ID gesetzt: {new_id}. Spiele ab jetzt werden gewertet.")
        self.poll_event.set()
        return True

    # ------------------------------------------------------------- Freischaltungen
    def received_names(self) -> set[str]:
        return {item_id_to_name.get(i.item, "") for i in self.items_received}

    def unlocked_agents(self) -> set[str]:
        return {a for a in AGENTS if a in self.received_names()}

    def unlocked_weapons(self) -> set[str]:
        return {w for w in WEAPONS if w in self.received_names()}

    def counting_queues(self) -> set[str]:
        queues = set(COUNTING_QUEUES)
        if (self.slot_data or {}).get("swiftplay_counts"):
            queues.add("swiftplay")
        return queues

    def goal_ready(self) -> bool:
        sd = self.slot_data or {}
        return (len(self.unlocked_agents()) >= int(sd.get("goal_agents", 15))
                and len(self.unlocked_weapons()) >= int(sd.get("goal_weapons", 10)))

    def show_status(self):
        if self.slot_data is None:
            logger.info("Noch nicht mit einem Slot verbunden.")
            return
        sd = self.slot_data
        names = self.received_names()
        agents, weapons = self.unlocked_agents(), self.unlocked_weapons()
        logger.info(f"Agenten ({len(agents)}/{sd.get('goal_agents', 15)} fürs Ziel): {', '.join(sorted(agents)) or '–'}")
        logger.info(f"Waffen ({len(weapons)}/{sd.get('goal_weapons', 10)} fürs Ziel): Classic, {', '.join(sorted(weapons)) or '–'}")
        extras = [e for e in ("Waffen aufheben", "Waffen requesten") if e in names]
        logger.info(f"Extras: {', '.join(extras) or '–'}")
        if self.goal_ready():
            logger.info("Ziel freigeschaltet: Der nächste Unrated-Sieg beendet dein Spiel.")

    # ------------------------------------------------------------- op.gg
    async def poll_once(self):
        if not self.agents_refreshed:
            try:
                self.agent_ids.update(await asyncio.to_thread(fetch_agent_ids))
            except Exception:
                pass  # eingebaute Liste reicht
            self.agents_refreshed = True

        name, tag = self.state["riot_id"].split("#", 1)
        try:
            games = await asyncio.to_thread(fetch_matches, name, tag)
        except OpggError as e:
            logger.warning(f"op.gg: {e}")
            return
        seen = set(self.state["seen"])
        if not self.state["baseline_done"]:
            self.state["seen"] = [g["matchId"] for g in games]
            self.state["baseline_done"] = True
            self.state["start"] = time.time()
            self.save_state()
            logger.info(f"op.gg verbunden: {len(games)} ältere Spiele werden ignoriert. Ab jetzt zählt jedes neue Unrated-Spiel.")
            self.show_status()
            return
        new = [g for g in reversed(games) if g["matchId"] not in seen]  # älteste zuerst
        if not new:
            return
        if len(new) == len(games):
            logger.warning(f"Alle {len(games)} Spiele sind neu – evtl. wurden Spiele verpasst (Client war zu lange aus).")

        found: list[str] = []
        goal = False
        for g in new:
            self.state["seen"].append(g["matchId"])
            queue = g.get("queueId") or "custom"
            if queue not in self.counting_queues():
                logger.info(f"Spiel ignoriert: Modus '{queue}' zählt nicht ({', '.join(sorted(self.counting_queues()))}).")
                continue
            agent = self.agent_ids.get(str(g.get("characterId", "")).upper(), "?")
            won = bool(g.get("won")) and not g.get("draw")
            kills = int(g.get("kills") or 0)
            mvp = is_match_mvp(g)
            need_kills = int((self.slot_data or {}).get("kill_bomb", KILL_BOMB))
            line = (f"{'SIEG' if won else ('Unentschieden' if g.get('draw') else 'Niederlage')} mit {agent}, "
                    f"{kills} Kills{', MATCH MVP' if mvp else ''}")
            if agent not in self.unlocked_agents():
                logger.warning(f"{line} – {agent} ist nicht freigeschaltet. Keine Checks.")
                continue
            checks = []
            if won:
                checks.append(f"{agent} - Win")
            if mvp:
                checks.append(f"{agent} - Match MVP")
            if kills >= need_kills:
                checks.append(f"{agent} - Kill Bomb")
            logger.info(f"{line} – Checks: {', '.join(checks) or 'keine'}")
            found += checks
            if won and self.goal_ready():
                goal = True
        self.state["seen"] = self.state["seen"][-200:]
        self.save_state()

        ids = {location_name_to_id[n] for n in found if n in location_name_to_id} & self.missing_locations
        if ids:
            await self.check_locations(ids)
        if goal and not self.finished_game:
            logger.info("ZIEL ERREICHT – Unrated-Legende!")
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Custom Valorant AF op.gg Client"
        return ui


def is_match_mvp(g: dict) -> bool:
    """Match MVP wie in Valorant: höchster Kampfwert (score) aller Spieler im Match."""
    players = g.get("players") or []
    own = g.get("score")
    if not players or own is None:
        return False
    return own >= max(p.get("score") or 0 for p in players)


def norm_id(riot_id: str | None) -> str:
    return re.sub(r"\s", "", (riot_id or "").lower())


async def poll_loop(ctx: ValorantContext):
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.poll_event.wait(), POLL_SECONDS)
        except asyncio.TimeoutError:
            pass
        ctx.poll_event.clear()
        if ctx.slot is None or ctx.slot_data is None or not ctx.state.get("riot_id"):
            continue
        try:
            await ctx.poll_once()
        except Exception as e:  # Tracker darf nie den Client abschießen
            logger.exception(f"Fehler beim op.gg-Abgleich: {e}")


def launch(*launch_args: str):
    import colorama

    parser = get_base_parser(description="Custom Valorant AF op.gg Client")
    parser.add_argument("--name", default=None, help="Slot-Name")
    parser.add_argument("url", nargs="?", help="Archipelago-Verbindungs-URL")
    args = handle_url_arg(parser.parse_args(launch_args), parser=parser)

    async def main():
        ctx = ValorantContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        poll_task = asyncio.create_task(poll_loop(ctx), name="op.gg poll")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await ctx.exit_event.wait()
        poll_task.cancel()
        await ctx.shutdown()

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
