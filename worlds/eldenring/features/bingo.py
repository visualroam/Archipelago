"""Experimental boss board: square checks are the hard progression surface.

First automatic catalogue is an AP adaptation of boss bingo objectives, not the full
community square export. Encounter flags and arena owners come from our generated EMEVD
tables. The full board adds stat thresholds, rosters, dungeon and item-check adapters.
Full mode retains restricted combat and unimplemented actions with manual fallback.
"""
import hashlib
import json

from BaseClasses import Location
from Options import Choice, Range, Toggle, OptionError, Visibility, OptionList

from ..registry import Feature, register
from ..bingo_board import LOCATION_NAMES, board_area, is_complete, select_board
from .. import contract


class BingoMode(Toggle):
    """An experimental bingo board supplies progression rewards.

    Objectives choose their regions; Num Regions is ignored.
    No Region Lock items; Curated Bingo Graces chooses starting travel.
    Requires a fresh character and the matching bingo client. Default off."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Mode"


class BingoCatalogue(Choice):
    """Choose the boss board or the full board.

    Boss draws one fight per square and keeps only their regions.
    Full draws from the bundled catalogue and keeps every eligible region.
    Its bosses, dungeons, stats and item checks track themselves; the rest are marked by hand.
    Requires the matching bingo client."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Catalogue"
    option_boss_board = 0
    option_full = 4
    # Retired tier names from v0.6.5: each was a partial version of the full board.
    alias_e1 = 4
    alias_e2 = 4
    alias_e3 = 4
    default = 0


class BingoManualPool(OptionList):
    """Optional replacement for the bundled full pool.

    Used by bingo_catalogue: full. Each entry has label, family and scope
    (base or dlc). Alternative variants share a family. Empty uses the bundled pool."""
    display_name = "Manual Bingo Objective Pool"
    visibility = Visibility.none
    default = []


class BingoGraces(Toggle):
    """Start Bingo Mode with a short curated list of graces.

    Base runs grant 12 graces. DLC-only grants Gravesite Plain and Roundtable;
    mixed boards also grant Gravesite Plain when they include DLC objectives.
    Off grants every safe grace in the board's regions. Default off."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Curated Bingo Graces"


# Season 6 download SHA c9f8039e...8509: BingoRandomizer selects Season5MiscPatcher.
# unlockSeason3Graces emits common event 279551111, bank 2003/id 66 for these flags.
# Names/identities cross-checked against grace_flags.tsv; full evidence in the audit doc.
# The same twelve graces are lit on the map at the start of any Season 6 broadcast;
# the binary was only used to confirm their flag ids. Example (map open in the first
# minutes of a base-game match): https://www.youtube.com/watch?v=2CAUuk_kqFo
CURATED_BASE_GRACES = (71190, 76154, 76413, 76303, 76353, 71222,
                       76521, 76551, 71504, 76203, 76225, 71216)
CURATED_DLC_GRACE = 76800  # Gravesite Plain, Season5MiscPatcher.editEMEVD.


def curated_graces(world):
    from ..region_spine import DLC_REGIONS
    kept = set(world._kept())
    flags = list(CURATED_BASE_GRACES) if kept - DLC_REGIONS else [71190]
    if kept & DLC_REGIONS:
        # AP starts in Roundtable: grant the DLC entry now instead of the official
        # Chapel warp and deferred Roundtable unlock. Mixed boards need both routes.
        flags.append(CURATED_DLC_GRACE)
    return flags


class BingoRegionLimit(Range):
    """Cap the boss board's regions, including their prerequisites.

    Objectives are chosen first; unrelated regions are omitted.
    Increase if the selected board cannot fit. The full board keeps every eligible region
    and ignores this. Default six."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Region Limit"
    range_start = 2
    range_end = 12
    default = 6


class BingoGoal(Choice):
    """Finish on a line, a square count, or every square.

    Only applies to Bingo Mode. A line is the short-run default."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Goal"
    option_line = 0
    option_count = 1
    option_blackout = 2
    default = 0


class BingoBoardSize(Range):
    """Width and height of the bingo board, from 5x5 to 12x12.

    Larger boards need enough distinct eligible objectives. The boss board may
    require more regions. Boards above 5x5 require a client supporting board sizes."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Board Size"
    range_start = 5
    range_end = 12
    default = 5


class BingoSquareCount(Range):
    """Squares needed for the count goal; line and blackout ignore this."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo Square Count"
    range_start = 1
    range_end = 144
    default = 13


class BingoLineSweepSize(Range):
    """Release a batch of native checks on the first completed line.

    Progression stays on squares. Already collected members reduce payout.
    Zero disables the bonus. Applies to every Bingo Goal."""
    visibility = Visibility.all & ~Visibility.simple_ui
    display_name = "Bingo First Line Sweep"
    range_start = 0
    range_end = 50
    default = 20


def active(world):
    return bool(getattr(getattr(world.options, "bingo_mode", None), "value", 0))


def full(world):
    return active(world) and world.options.bingo_catalogue.value == 4


def counter_total(members):
    """Alternative pickup flags for the same original item are one distinct unit."""
    units = {}
    for m in members:
        key = ("item", m["unit"]) if m.get("unit") else ("flag", m["flag"])
        units[key] = max(units.get(key, 0), m["weight"])
    return sum(units.values())


def evidence_flags(cell):
    return {cell["flag"]} - {0} | {m["flag"] for g in cell.get("counter", []) for m in g["members"]}


def square_ids(world):
    return frozenset(c["location"] for c in getattr(world, "gf_bingo_board", ()))


def permits_progression(world, location, item):
    return not active(world) or not item.advancement or location.address in square_ids(world)


def draw_regions(world, start_pool):
    """Draw objectives first, then retain only their owners and prerequisite closure."""
    if not active(world):
        return
    for field in ("vanilla_placement", "natural_progression", "mario_mode"):
        if bool(getattr(getattr(world.options, field, None), "value", 0)):
            raise OptionError(f"bingo_mode does not yet support {field}; disable {field} for the boss-board prototype")
    if getattr(world, "gf_goal_choice", "auto") != "auto":
        raise OptionError("bingo_mode replaces goal; set goal to auto and choose bingo_goal instead")
    size = world.options.bingo_board_size.value
    area = board_area(size)
    if world.options.bingo_goal.current_key == "count" and world.options.bingo_square_count.value > area:
        raise OptionError(f"bingo_square_count cannot exceed {area} squares on a {size}×{size} board")
    BOSS_HEALTHBARS = world.tables.modules["boss_healthbars"].BOSS_HEALTHBARS
    SWEEP_ARENA_REGION = world.tables.modules["boss_sweeps"].SWEEP_ARENA_REGION
    # Simple dungeon/field encounters only: legacy fights can require quests, final-arena
    # gates, or preceding bosses. Those need action-specific logic before joining this catalogue.
    from . import great_runes
    # Major-rune/festival fights have additional access mechanics and detection overrides.
    excluded_flags = set(great_runes.GREAT_RUNE_DETECT_FLAGS.values())
    kept = set(world.gf_eligible)
    if world.options.bingo_catalogue.value == 4:
        from ..bingo_manual import select
        from .. import bingo_e1, bingo_e2, bingo_e3
        from .scaling import blessing_mode
        automatic = bingo_e1.candidates(BOSS_HEALTHBARS, SWEEP_ARENA_REGION, kept,
            progressive_flasks=bool(world.options.progressive_flasks.value),
            blessing_mode=blessing_mode(world),
            sweep_regions=world.tables.modules["boss_sweeps"].SWEEP_REGION)
        extra, _ = bingo_e2.candidates(world.tables, kept, len(kept), global_rosters=True)
        automatic += extra
        automatic += bingo_e3.candidates(world.tables, kept, len(kept), global_rosters=True)
        world.gf_bingo_board = select(world.options.bingo_manual_pool.value,
            f"{world.multiworld.seed}:{world.player}:full", kept, automatic=automatic, **({"size": size} if size != 5 else {}))
        # Source objectives span quests and arbitrary locations: retain every eligible
        # region rather than inventing per-objective ownership or access predicates.
        world.gf_bingo_anchor_pool = kept & start_pool if start_pool else {"Limgrave", "Gravesite"} & kept
        return list(world.gf_eligible)
    candidates = [{"flag": flag, "region": SWEEP_ARENA_REGION[flag],
                   "label": f"Defeat {info[3]} ({SWEEP_ARENA_REGION[flag]})"}
                  for flag, info in BOSS_HEALTHBARS.items()
                  if flag not in excluded_flags and info[2] in {"field", "catacomb", "cave", "tunnel"}
                  and info[3] and SWEEP_ARENA_REGION.get(flag) in kept]
    try:
        from ..region_spine import REGION_PARENT
        board = select_board(candidates, f"{world.multiworld.seed}:{world.player}:boss-board-v1",
                             region_limit=world.options.bingo_region_limit.value,
                             parents=REGION_PARENT, start_pool=(), starts=1, size=size)
    except ValueError as e:
        raise OptionError(f"{e}; increase bingo_region_limit or broaden the eligible content") from e
    world.gf_bingo_board = board
    regions = {r for cell in board for r in cell.get("regions", [cell["region"]])}
    world.gf_bingo_anchor_pool = regions & start_pool if start_pool else regions - set(REGION_PARENT)
    from ..region_spine import parent_chain
    kept = regions | {parent for region in regions for parent in parent_chain(region)}
    if not kept <= set(world.gf_eligible):
        raise OptionError("bingo objective prerequisites are outside the eligible region pool")
    return [region for region in world.gf_eligible if region in kept]


def prepare(world):
    """Reserve native bonus checks after feature ownership has been resolved."""
    if not active(world):
        return
    kept = set(world._kept())
    from . import evidence_progression_hosts
    MISSABLE_LOCATIONS = world.tables.modules["missable_locations"].MISSABLE_LOCATIONS
    trusted = evidence_progression_hosts.trusted_aps() - set(MISSABLE_LOCATIONS)
    overrides = getattr(world, "gf_extra_location_flags", {})
    native = [(aid, overrides.get(aid, flag)) for region in [world.tables.hub] + sorted(kept)
              for _name, aid, flag in world._seed_locations(region)]
    eligible = {aid for region in kept for _name, aid, _flag in world._seed_locations(region)
                if aid in trusted}
    groups = {}
    boss_flags = set(world.tables.modules["boss_healthbars"].BOSS_HEALTHBARS)
    # A square's own evidence must be earned by hand: the line bonus and every dungeon
    # sweep leave those physical pickups alone (see gf_bingo_protected_checks below).
    board_flags = set().union(*(evidence_flags(c) for c in world.gf_bingo_board))
    for aid, flag in native:
        if flag and flag not in boss_flags and flag not in board_flags:
            groups.setdefault(flag, set()).add(aid)
    flags = sorted(groups, key=lambda flag: hashlib.sha256(
        f"{world.multiworld.seed}:{world.player}:line:{flag}".encode()).digest())
    members, limit = [], world.options.bingo_line_sweep_size.value
    for flag in flags:
        group = groups[flag]
        # A flag flush completes the whole physical pickup, so never reserve only part of it.
        if group <= eligible and len(members) + len(group) <= limit:
            members.extend(sorted(group))
    world.gf_bingo_line_sweep = members
    # Every bingo catalogue replaces the rune ending.
    world.gf_required_runes = []
    # Detection overrides for major bosses also appear as native checks. No synthetic
    # sweep may assert the same defeat evidence. Native flag polling remains available.
    world.gf_bingo_protected_checks = {aid for aid, flag in native if flag in board_flags}
    if full(world):
        requirements = {}
        for cell in world.gf_bingo_board:
            for name, count in cell.get("requirements", []):
                requirements[name] = max(requirements.get(name, 0), count)
        world.gf_bingo_requirements = requirements
        # The progressive feature owns its supply AND ladder. Raise its declared floor
        # before either is constructed, rather than injecting copies invisible to its ladder.
        floor = requirements.get("Progressive Flask Upgrade", 0)
        if floor:
            world.options.flask_upgrade_minimum.value = max(floor, world.options.flask_upgrade_minimum.value)
    # Existing extra-location seam keeps the native pool allocator count-neutral.
    world.gf_extra_locations = list(getattr(world, "gf_extra_locations", ())) + \
        [(name, aid, 0) for name, aid in LOCATION_NAMES.items() if aid in square_ids(world)]


@register
class Bingo(Feature):
    name = "bingo"
    OPTIONS = {"bingo_mode": BingoMode, "bingo_catalogue": BingoCatalogue, "bingo_graces": BingoGraces, "bingo_region_limit": BingoRegionLimit, "bingo_goal": BingoGoal,
               "bingo_board_size": BingoBoardSize, "bingo_square_count": BingoSquareCount, "bingo_line_sweep_size": BingoLineSweepSize,
               "bingo_manual_pool": BingoManualPool}

    def create_regions(self, world):
        if not active(world):
            return
        hub = world.multiworld.get_region("Roundtable Hold", world.player)
        for name, aid in LOCATION_NAMES.items():
            if aid not in square_ids(world):
                continue
            hub.locations.append(Location(world.player, name, aid, hub))

    def create_items(self, world):
        if not active(world):
            return []
        from BaseClasses import ItemClassification
        supplies = []
        for name, count in getattr(world, "gf_bingo_requirements", {}).items():
            if name == "Progressive Flask Upgrade":
                continue  # Existing progressive feature supplies the raised floor.
            for _ in range(count):
                item = world.create_item(name)
                item.classification = ItemClassification.progression
                supplies.append(item)
        return supplies + [world.create_item(world.get_filler_item_name()) for _ in world.gf_bingo_board]

    def set_rules(self, world):
        if not active(world):
            return
        mw, player = world.multiworld, world.player
        board = world.gf_bingo_board
        from BaseClasses import ItemClassification
        flask_count = getattr(world, "gf_bingo_requirements", {}).get("Progressive Flask Upgrade", 0)
        for item in mw.itempool:
            if item.player == player and item.name == "Progressive Flask Upgrade" and flask_count:
                item.classification = ItemClassification.progression
                flask_count -= 1
        # Join defeat identity to native boss reward checks. Their final rules include
        # legacy keys and action-specific quest gates, assigned by later features.
        rewards = world.tables.modules["boss_reward_lots"].BOSS_REWARD_DEFEAT
        if full(world):
            from ..bingo_e3 import REWARD_DEATH
            rewards = {**rewards, **REWARD_DEATH}
        native = {}
        for region in world._kept():
            for name, aid, flag in world._seed_locations(region):
                detect = getattr(world, "gf_extra_location_flags", {}).get(aid, flag)
                defeat = rewards.get(flag, detect)
                native.setdefault(defeat, []).append(mw.get_location(name, player))
        def reachable(state, cell):
            if not cell.get("counter") and not all(state.can_reach(r, "Region", player) for r in cell.get("regions", [cell["region"]])):
                return False
            if not all(state.has(name, player, count) for name, count in cell.get("requirements", [])):
                return False
            def can_fight(flag, region):
                witnesses = native.get(flag, ())
                return state.can_reach(region, "Region", player) and (not witnesses or any(loc.access_rule(state) for loc in witnesses))
            if "counter" in cell:
                return all(counter_total([m for m in g["members"] if can_fight(m["flag"], m["region"])]) >= g["target"] for g in cell["counter"])
            return can_fight(cell["flag"], cell["region"])
        for cell in board:
            loc = mw.get_location(f"Bingo Square {cell['location'] - min(LOCATION_NAMES.values()) + 1:02d}", player)
            loc.access_rule = lambda state, c=cell: reachable(state, c)
        # Both own and incoming advancement obey this hard surface; no exemptions or widening.
        for loc in mw.get_locations(player):
            prev = loc.item_rule
            loc.item_rule = lambda item, p=prev, l=loc: p(item) and permits_progression(world, l, item)
        goal = world.options.bingo_goal.current_key
        count = world.options.bingo_square_count.value
        mw.completion_condition[player] = lambda state: is_complete(
            [reachable(state, c) for c in board], goal, count, world.options.bingo_board_size.value)

    def slot_data(self, world):
        if not active(world):
            return {}
        cells = [{k: v for k, v in c.items() if k in {"location", "flag", "region", "label", "state", "counter", "collection", "manual"}}
                 for c in world.gf_bingo_board]
        payload = {"version": 1, "catalogue": "ap-boss-board-v1", "cells": cells,
                   "goal": world.options.bingo_goal.current_key,
                   "count": min(world.options.bingo_square_count.value, len(cells)),
                   "line_sweep": world.gf_bingo_line_sweep}
        features = ["bingo_v1"]
        if full(world):
            payload.update(version=5, catalogue="ap-manual-board-v1")
            features = ["bingo_manual_v1"]
            if any(c.get("flag") or c.get("state") or c.get("counter") or c.get("collection") for c in cells):
                features.append("bingo_full_predicates_v1")
        if world.options.bingo_board_size.value != 5:
            payload["size"] = world.options.bingo_board_size.value
            features.append("bingo_board_sizes_v1")
        payload["hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if any(m.get("unit") for c in cells for g in c.get("counter", []) for m in g["members"]):
            features.append("bingo_unique_checks_v1")
        return {contract.BINGO_BOARD: payload, contract.REQUIRES_CLIENT_FEATURES: features}
