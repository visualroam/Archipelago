"""
AF LoL Winstreak Client – verbindet sich mit dem Archipelago-Slot und schaut regelmäßig auf op.gg nach neuen Spielen.

Start: Archipelago Launcher → "AF LoL Winstreak Client". Verbinden wie immer (/connect …), dann die Riot-ID
einfach ins Eingabefeld tippen, z. B.  menniphi#EUW  (Region optional dahinter: menniphi#EUW EUNE).
Erkannte Checks und das Ziel werden automatisch an den Server geschickt.
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

from . import BOOTS, CHAMPION_REUSE, CHAMPIONS, GAME, KEYSTONES, ROLES, AFLeagueWorld
from .opgg import OpggError, fetch_matches
from .rules import Permissions, evaluate, update_streak

POLL_SECONDS = 60
PERMIT_PREFIXES = ("Champion: ", "Role: ", "Keystone: ", "Boots: ")
RIOT_ID = re.compile(r"^\s*([^#/!][^#]{0,31}?)\s*#\s*([A-Za-z0-9]{2,5})(?:\s+([A-Za-z]{2,4}\d?))?\s*$")
ITEM_NAMES = {v: k for k, v in AFLeagueWorld.item_name_to_id.items()}
LOCATION_IDS = AFLeagueWorld.location_name_to_id


class WinstreakCommands(ClientCommandProcessor):
    def _cmd_riot(self, *riot_id: str) -> bool:
        """Riot-ID setzen: /riot Username#Tag [Region]  (Region Standard EUW)"""
        if not self.ctx.set_riot_id(" ".join(riot_id)):
            self.output("Format: /riot Username#Tag [Region], z. B. /riot Username#Tag EUW")
            return False
        return True

    def _cmd_streak(self) -> bool:
        """Aktuelle Serie und Freischaltungen anzeigen"""
        self.ctx.show_status()
        return True

    def _cmd_unlocks(self) -> bool:
        """Zeigt, was ab Start da ist und was schon freigeschaltet wurde"""
        self.ctx.show_status()
        return True

    def _cmd_opgg(self) -> bool:
        """op.gg sofort abfragen statt auf die nächste Runde zu warten"""
        self.ctx.poll_event.set()
        return True


class WinstreakContext(CommonContext):
    game = GAME
    items_handling = 0b111  # alle Items inkl. Startinventar
    command_processor = WinstreakCommands

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.slot_data: dict | None = None
        self.state: dict = {}
        self.state_file: str | None = None
        self.poll_event = asyncio.Event()
        self.poll_task: asyncio.Task | None = None

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
            if self.state.get("riot_id"):
                logger.info(f"op.gg-Tracker aktiv für {self.state['riot_id']} ({self.state['region']}).")
            else:
                logger.info("Gib jetzt deine Riot-ID ein: Username#Tag  (Region optional: Username#Tag EUW)")
            self.poll_event.set()
        elif cmd == "ReceivedItems" and self.slot_data is not None:
            if args.get("index") == 0:
                # erster Abgleich nach dem Verbinden: komplette Übersicht
                self.show_status()
            else:
                new = self.received_names()[-len(args.get("items", [])):] if args.get("items") else []
                new = [n for n in new if n.startswith(PERMIT_PREFIXES) or n == CHAMPION_REUSE]
                if new:
                    logger.info(f"Neu freigeschaltet: {', '.join(new)}")

    def on_user_say(self, text: str):
        # Riot-ID kann einfach ins Eingabefeld getippt werden
        if RIOT_ID.match(text) and not self.state.get("riot_id"):
            self.set_riot_id(text)
            return None
        return text

    # ------------------------------------------------------------- Zustand
    def load_state(self):
        folder = Utils.user_path("AF_LoL_Winstreak")
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
        state.setdefault("region", "EUW")
        state.setdefault("seen", [])
        state.setdefault("baseline_done", False)
        state.setdefault("streak", [])
        state.setdefault("reuse_used", 0)
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
        name, tag, region = m.group(1).strip(), m.group(2), (m.group(3) or self.state.get("region") or "EUW").upper()
        changed = norm_id(self.state.get("riot_id")) != norm_id(f"{name}#{tag}")
        self.state.update(riot_id=f"{name}#{tag}", region=region)
        if changed:  # neuer Account → alte Spiele dieses Accounts nicht nachträglich werten
            self.state.update(seen=[], baseline_done=False)
        self.save_state()
        logger.info(f"Riot-ID gesetzt: {name}#{tag} ({region}). Spiele ab jetzt werden gewertet.")
        self.poll_event.set()
        return True

    # ------------------------------------------------------------- Freischaltungen
    def received_names(self) -> list[str]:
        return [ITEM_NAMES.get(i.item, "") for i in self.items_received]

    def unlocked(self) -> Permissions:
        names = set(self.received_names())
        sd = self.slot_data or {}
        champs = {n[10:] for n in names if n.startswith("Champion: ")} | set(sd.get("starting_champions", []))
        roles = {n[6:] for n in names if n.startswith("Role: ")} | set(sd.get("starting_roles", []))
        keys = {n[10:] for n in names if n.startswith("Keystone: ")} | set(sd.get("starting_keystones", []))
        boots = {n[7:] for n in names if n.startswith("Boots: ")}
        return Permissions(champions=champs, roles=roles, keystones=keys, boots=boots, boots_all=set(BOOTS))

    def reuse_left(self) -> int:
        return self.received_names().count(CHAMPION_REUSE) - self.state.get("reuse_used", 0)

    def show_status(self):
        if not self.slot_data:
            logger.info("Noch nicht mit einem Slot verbunden.")
            return
        sd = self.slot_data
        p = self.unlocked()
        need = sd.get("streak_length", 5)
        streak = self.state.get("streak", [])

        def line(title, order, have, start, total):
            start_l = [x for x in order if x in start]
            more = [x for x in order if x in have and x not in start]
            text = f"{title} ({len(start_l) + len(more)}/{total}):  Start: {', '.join(start_l) or '–'}"
            if more:
                text += f"  |  Freigeschaltet: {', '.join(more)}"
            logger.info(text)

        # Startinventar kommt vom Server mit location -2
        start = {ITEM_NAMES.get(i.item, "") for i in self.items_received if i.location == -2}
        start |= {f"Role: {r}" for r in sd.get("starting_roles", [])}
        start |= {f"Champion: {c}" for c in sd.get("starting_champions", [])}
        start |= {f"Keystone: {k}" for k in sd.get("starting_keystones", [])}

        def starts(prefix):
            return {n[len(prefix):] for n in start if n.startswith(prefix)}

        logger.info("========== Freischaltungen ==========")
        line("Rollen", ROLES, p.roles, starts("Role: "), len(ROLES))
        pool = sd.get("champion_pool", [])
        line("Champions", pool, p.champions, starts("Champion: "), len(pool))
        line("Keystones", KEYSTONES, p.keystones, starts("Keystone: "), len(KEYSTONES))
        line("Stiefel (Boots immer erlaubt)", BOOTS, p.boots, starts("Boots: "), len(BOOTS))
        logger.info(f"Champion Reuse übrig: {self.reuse_left()}")
        logger.info(f"Serie: {len(streak)}/{need}  [{', '.join(streak) or '–'}]")
        logger.info("=====================================")

    # ------------------------------------------------------------- op.gg
    async def poll_once(self):
        name, tag = self.state["riot_id"].split("#", 1)
        try:
            games = await asyncio.to_thread(fetch_matches, name, tag, self.state["region"], 20)
        except OpggError as e:
            logger.warning(f"op.gg: {e}")
            return
        seen = set(self.state["seen"])
        if not self.state["baseline_done"]:
            self.state["seen"] = [g["id"] for g in games]
            self.state["baseline_done"] = True
            self.state["start"] = time.time()
            self.save_state()
            logger.info(f"op.gg verbunden: {len(games)} ältere Spiele werden ignoriert. Ab jetzt zählt jedes neue Spiel.")
            return
        new = [g for g in reversed(games) if g.get("id") not in seen]  # älteste zuerst
        if not new:
            return
        if len(new) == len(games) and games:
            logger.warning("Alle 20 Spiele sind neu – evtl. wurden Spiele verpasst (Client war zu lange aus).")

        need_kills = self.slot_data.get("kills", 10)
        need_streak = self.slot_data.get("streak_length", 5)
        found: list[str] = []
        for g in new:
            ev = evaluate(g, self.unlocked(), CHAMPIONS, need_kills, riot_name=name)
            self.state["seen"].append(ev.game_id)
            if not ev.counted:
                logger.info(f"Spiel ignoriert: {ev.reason}")
                continue
            line = (f"{'SIEG' if ev.win else 'Niederlage'} mit {ev.champion}"
                    f"{' (' + ev.role + ')' if ev.role else ''}, {ev.kills} Kills")
            for w in ev.warnings:
                logger.warning(f"  Hinweis: {w}")
            streak, used, msg = update_streak(self.state["streak"], ev, self.reuse_left())
            self.state["streak"] = streak
            self.state["reuse_used"] += used
            if not ev.legal:
                logger.warning(f"{line} – REGELVERSTOSS: {ev.reason}. Keine Checks.")
            else:
                logger.info(f"{line} – Checks: {', '.join(ev.checks) or 'keine'}")
            if msg:
                logger.info(f"  {msg}")
            logger.info(f"  Serie: {len(streak)}/{need_streak} [{', '.join(streak) or '–'}]")
            found += ev.checks
        self.state["seen"] = self.state["seen"][-200:]
        self.save_state()

        ids = {LOCATION_IDS[n] for n in found if n in LOCATION_IDS} & self.missing_locations
        if ids:
            await self.check_locations(ids)
        if len(self.state["streak"]) >= need_streak and not self.finished_game:
            logger.info("ZIEL ERREICHT – Winstreak geschafft!")
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "AF LoL Winstreak Client"
        return ui


def norm_id(riot_id: str | None) -> str:
    return re.sub(r"\s", "", (riot_id or "").lower())


async def poll_loop(ctx: WinstreakContext):
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

    parser = get_base_parser(description="AF LoL Winstreak Client (op.gg-Tracker)")
    parser.add_argument("--name", default=None, help="Slot-Name")
    parser.add_argument("url", nargs="?", help="Archipelago-Verbindungs-URL")
    args = handle_url_arg(parser.parse_args(launch_args), parser=parser)

    async def main():
        ctx = WinstreakContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        ctx.poll_task = asyncio.create_task(poll_loop(ctx), name="op.gg poll")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await ctx.exit_event.wait()
        ctx.poll_task.cancel()
        await ctx.shutdown()

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
