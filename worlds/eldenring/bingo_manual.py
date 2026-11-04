"""Full-pool objectives, with automatic adapters and manual fallback.

The bundled catalogue (bingo_catalogue.json) is used when the host supplies no pool.
It is built from docs/specs/bingo-catalogue-ledger.tsv. Some objectives are adapted
from the Bingo Brawlers community's bingo squares and reworded for Archipelago; credit
and thanks to that community. Each row names its adapter by key, so its wording can
change without losing automatic tracking.
"""
import copy
import json
from importlib.resources import files
import random
from Options import OptionError
from .bingo_board import BINGO_LOCATION_BASE, board_area
from .bingo_eligibility import crafting_goal


def bundled():
    return json.loads(files(__package__).joinpath("bingo_catalogue.json").read_text(encoding="utf-8"))


def select(pool, seed, eligible, *, automatic=(), size=5):
    area = board_area(size)
    if pool == []:
        pool = bundled()
    if not isinstance(pool, list) or not pool or len(pool) > 2000:
        raise OptionError(f"bingo_catalogue: full needs bingo_manual_pool ({area}+ distinct families, at most 2000 variants)")
    families = {}
    for row in pool:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row[k].strip()
                                              for k in ("label", "family", "scope")):
            raise OptionError("bingo_manual_pool entries require nonempty label, family and scope strings")
        if row["scope"] not in {"base", "dlc"} or len(row["label"]) > 500:
            raise OptionError("bingo_manual_pool scope must be base or dlc; labels must be at most 500 characters")
        if crafting_goal(row["label"]):
            continue
        region = "Gravesite" if row["scope"] == "dlc" else "Limgrave"
        if region in eligible:
            families.setdefault(row["family"], []).append({"label": row["label"], "region": region, "scope": row["scope"],
                                                           "detector": row.get("detector")})
    if len(families) < area:
        raise OptionError(f"bingo_manual_pool needs at least {area} distinct families in eligible base/DLC content after excluding crafting goals; only {len(families)} remain; enable DLC, supply a larger custom pool, or reduce bingo_board_size")
    # A bundled row names its adapter. A custom row is tracked only when its complete
    # wording matches a bundled automatic row, with only the action verb normalized;
    # never infer a predicate from a noun substring.
    def normalized(label):
        words = label.casefold().split()
        if words:
            words[0] = {"acquire": "collect", "kill": "defeat"}.get(words[0], words[0])
        return " ".join(words)
    by_label = {(r["scope"], normalized(r["label"])): r["detector"]["adapter"]
                for r in bundled() if r.get("detector")}
    groups = {}
    for candidate in automatic:
        groups.setdefault(candidate["adapter"], []).append(candidate)
    predicates = {}
    for adapter, matches in groups.items():
        candidate = copy.deepcopy(matches[0])
        if len(matches) > 1:
            # An unqualified family accepts any matching encounter, not a randomly
            # chosen region. Prerequisite-bearing alternatives are not interchangeable.
            if any(c.get("requirements") or c.get("regions") for c in matches):
                continue
            members = {c["flag"]: dict(flag=c["flag"], region=c["region"],
                label=c["label"], weight=1) for c in matches}
            candidate.update(flag=0, counter=[dict(target=1, members=list(members.values()))])
        predicates[adapter] = candidate
    # Upgrade-supply squares each reserve a run of progression items on the square
    # surface; like the E1 draw, a board carries at most one.
    rng = random.Random(seed)
    board, supply = [], False
    for family in rng.sample(sorted(families), len(families)):
        cell = dict(rng.choice(families[family]), flag=0, manual=True)
        detector, scope = cell.pop("detector", None), cell.pop("scope")
        adapter = detector["adapter"] if isinstance(detector, dict) else by_label.get((scope, normalized(cell["label"])))
        candidate = predicates.get(adapter)
        if candidate:
            if supply and candidate.get("supply_goal"):
                continue
            supply = supply or bool(candidate.get("supply_goal"))
            cell.update(copy.deepcopy({k: v for k, v in candidate.items() if k in {
                "flag", "region", "regions", "state", "counter", "collection", "requirements", "supply_goal"}}))
        board.append(dict(cell, location=BINGO_LOCATION_BASE + len(board)))
        if len(board) == area:
            return board
    raise OptionError(f"bingo_manual_pool cannot fill {area} squares with at most one upgrade-supply objective; supply a larger custom pool or reduce bingo_board_size")
