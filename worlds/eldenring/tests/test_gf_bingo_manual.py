import pytest
from Options import OptionError
from worlds.eldenring.bingo_manual import select


def pool():
    return [dict(label=f"Rule {family} alternative {variant}", family=str(family), scope=scope)
            for family, scope in enumerate(["base"] * 30 + ["dlc"] * 30)
            for variant in range(3)]


def test_crafting_is_excluded_from_old_and_custom_full_pools():
    rows = [dict(label=f"Rule {i}", family=str(i), scope="base") for i in range(24)]
    rows += [dict(label=" Craft 2 Unique Hefty Pots", family="craft", scope="base")]
    with pytest.raises(OptionError, match="after excluding crafting"):
        select(rows, "craft", {"Limgrave"})
    rows += [dict(label="Do 4 Hefty Cracked Pot checks", family="acquire", scope="base")]
    board = select(rows, "craft", {"Limgrave"})
    assert len(board) == 25
    assert "Do 4 Hefty Cracked Pot checks" in {cell["label"] for cell in board}
    assert not any(cell["label"].strip().casefold().startswith("craft ") for cell in board)


@pytest.mark.parametrize("seed", [1, 7, 42])
@pytest.mark.parametrize("supply", ["Raise your flask to +7", "Reach Scadutree Blessing 10", "Reach Revered Spirit Ash Blessing 5"])
def test_full_pool_existing_detectors_and_restricted_fallback(seed, supply):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from Fill import distribute_items_restrictive
    automatic = ["Defeat Fia's Champions", "Defeat the Grafted Scion at the Chapel of Anticipation", "Defeat Bayle the Dread",
        "Defeat Jori, Elder Inquisitor", "Defeat the Ancient Dragon-Man",
        "Defeat Ancient Dragon Lansseax", "Defeat 3 Shadow Realm dragon bosses",
        "Defeat 5 mounted bosses", "Defeat 2 different Bell Bearing Hunters",
        "Clear 3 caves or grottoes", "Clear 2 gaols", "Clear 3 catacombs",
        "Clear a hero's grave on the Altus Plateau or Mt. Gelmir", "Defeat the Madding Hand",
        "Do 4 Hefty Cracked Pot checks", "Reach rune level 60", supply]
    manual = ["Custom rule A", "Defeat Bloodhound Knight Darriwil with Blaidd summoned",
        "Defeat the sleeping golem in Leyndell", "Custom rule C",
        "Custom rule D", "Made up rule", "Custom rule E", "Custom rule B"]
    rows = [dict(label=label, family=str(i), scope="dlc" if label in {
        "Defeat Bayle the Dread", "Defeat Jori, Elder Inquisitor", "Defeat the Ancient Dragon-Man",
        "Defeat 3 Shadow Realm dragon bosses", "Clear 2 gaols", "Defeat the Madding Hand",
        "Do 4 Hefty Cracked Pot checks", "Reach Scadutree Blessing 10", "Reach Revered Spirit Ash Blessing 5"} else "base")
        for i, label in enumerate(automatic + manual)]
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
        options=dict(bingo_mode=True, bingo_catalogue="full", bingo_manual_pool=rows,
                     bingo_graces=True, enable_dlc=True, dlc_blessing_catchup=False,
                     scadutree_blessing_scope="dlc_only"))
    w = mw.worlds[1]
    board = {c["label"]: c for c in w.gf_bingo_board}
    for label in automatic:
        cell = board[label]
        assert cell.get("flag") or cell.get("counter") or cell.get("state"), label
        assert cell["manual"]
    for label in manual:
        assert not any(board[label].get(k) for k in ("flag", "counter", "state", "collection")), label
    assert board["Reach rune level 60"]["state"] == dict(metric="level", target=60)
    hunters = board["Defeat 2 different Bell Bearing Hunters"]["counter"][0]
    assert hunters["target"] == 2 and len(hunters["members"]) > 2
    assert len({m["region"] for m in hunters["members"]}) > 1
    assert w.gf_bingo_requirements
    assert "bingo_full_predicates_v1" in w.fill_slot_data()["requiresClientFeatures"]
    from worlds.eldenring.features.bingo import evidence_flags
    protected = set().union(*(evidence_flags(c) for c in board.values()))
    flags = {aid: getattr(w, "gf_extra_location_flags", {}).get(aid, flag)
             for region in [w.tables.hub] + sorted(w._kept())
             for _, aid, flag in w._seed_locations(region)}
    assert not protected.intersection(flags[aid] for aid in w.gf_bingo_line_sweep)
    distribute_items_restrictive(mw)
    assert mw.can_beat_game()


def test_full_pool_selects_distinct_families_and_filters_scope():
    board = select(pool(), "fresh", {"Limgrave"})
    assert len(board) == 25
    assert all(c["manual"] and c["flag"] == 0 and c["region"] == "Limgrave" for c in board)
    assert len({c["label"].split()[1] for c in board}) == 25
    assert board == select(pool(), "fresh", {"Limgrave"})
    assert {c["location"] for c in board} == set(range(7786000, 7786025))
    assert all(c["region"] == "Gravesite" for c in select(pool(), "fresh", {"Gravesite"}))
    with pytest.raises(OptionError, match="25 distinct"):
        select(pool()[:30], "fresh", {"Limgrave"})
    with pytest.raises(OptionError, match="scope"):
        select([dict(label="Unknown", family="x", scope="invalid")], "fresh", {"Limgrave"})


def test_full_pool_unique_square_uses_global_distinct_checks():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from Fill import distribute_items_restrictive
    rows = [dict(label="Do 10 different talisman checks", family="base-082", scope="base")]
    rows += [dict(label=f"Manual {i}", family=str(i), scope="base") for i in range(24)]
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=7,
        options=dict(bingo_mode=True, bingo_catalogue="full", bingo_manual_pool=rows, bingo_graces=True))
    w = mw.worlds[1]
    cell = next(c for c in w.gf_bingo_board if c["label"] == rows[0]["label"])
    assert cell["manual"] and cell["counter"][0]["target"] == 10
    assert len({m["unit"] for m in cell["counter"][0]["members"]}) > 80
    assert "bingo_unique_checks_v1" in w.fill_slot_data()["requiresClientFeatures"]
    assert set(w._kept()) == set(w.gf_eligible)
    distribute_items_restrictive(mw)
    assert mw.can_beat_game()
    from worlds.eldenring.features.bingo import counter_total
    members = cell["counter"][0]["members"]
    regions = {m["region"] for m in members}
    region = max(regions, key=lambda r: counter_total([m for m in members if m["region"] == r]))
    assert counter_total([m for m in members if m["region"] == region]) >= 10
    # Prove optional regions are not conjunctive prerequisites for this square.
    for location in mw.get_locations(1):
        if location.address not in range(7786000, 7786025):
            location.access_rule = lambda state: True
    state = mw.get_all_state(False)
    state.can_reach = lambda name, kind, player: name == region
    square = mw.get_location(f"Bingo Square {cell['location'] - 7786000 + 1:02d}", 1)
    assert square.access_rule(state)
    state.can_reach = lambda name, kind, player: False
    assert not square.access_rule(state)


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_full_manual_generation_retains_regions_and_negotiates_client(seed):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from Fill import distribute_items_restrictive
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
        options=dict(bingo_mode=True, bingo_catalogue="full", bingo_manual_pool=pool(),
                     bingo_graces=True, enable_dlc=True))
    distribute_items_restrictive(mw)
    world = mw.worlds[1]
    sd = world.fill_slot_data()
    assert sd["bingoBoard"]["version"] == 5
    assert sd["requiresClientFeatures"].count("bingo_manual_v1") == 1
    assert not sd["regionOpenFlags"] and not sd["areaLockFlags"] and not sd["regionGraces"]
    assert set(world._kept()) == set(world.gf_eligible)
    assert len(sd["bingoBoard"]["cells"]) == 25
    assert all(c["manual"] for c in sd["bingoBoard"]["cells"])
    assert mw.can_beat_game()


def test_bundled_catalogue_is_ours_and_every_detector_resolves():
    """Own ids and wording; a detector key must name an adapter, never wording."""
    from worlds.eldenring import bingo_manual, bingo_e1
    from worlds.eldenring.bingo_e2 import CATALOGUE
    from worlds.eldenring.bingo_e3 import OBJECTIVES
    rows = bingo_manual.bundled()
    assert len(rows) == 267 and len({r["id"] for r in rows}) == len(rows)
    assert len({(r["scope"], r["label"]) for r in rows}) == len(rows)
    assert all(set(r) <= {"id", "family", "scope", "label", "detector"} for r in rows)
    assert all(not r["id"].startswith("S6-") and not r["family"].startswith("S6-") for r in rows)
    for scope in ("base", "dlc"):
        assert len({r["family"] for r in rows if r["scope"] == scope}) >= 25
    adapters = ({r["adapter"] for r in CATALOGUE} | {a for _, a, _, _ in OBJECTIVES} | set(bingo_e1.BOSSES)
                | {a for _, targets, _, _ in bingo_e1.STATE_GOALS for _, a in targets})
    detectors = [r["detector"] for r in rows if "detector" in r]
    assert len(detectors) == 202
    for d in detectors:
        assert set(d) == {"adapter"} and d["adapter"] in adapters, d
    # One wording everywhere: a detector table and the bundled row it serves agree.
    said = {r["adapter"]: r["label"] for r in CATALOGUE} | {a: label for _, a, label, _ in OBJECTIVES}
    for r in rows:
        if r.get("detector", {}).get("adapter") in said:
            assert said[r["detector"]["adapter"]] == r["label"]
    assert not any(r["label"].startswith(("Collect ", "Acquire ")) for r in rows)
    blade = next(r for r in rows if r["id"] == "check/fingerslayer-blade")
    assert blade["label"] == "Do the Fingerslayer Blade check"


def test_bundled_catalogue_matches_its_ledger():
    import subprocess
    import sys
    from pathlib import Path
    from ._util import find_repo_root
    root = find_repo_root(__file__)
    if root is None:
        pytest.skip("repo-only: the ledger is not packaged")
    result = subprocess.run([sys.executable, str(Path(root) / "tools/build_bingo_catalogue.py"), "--check"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("seed", [1, 7, 42])
@pytest.mark.parametrize("extra", [{}, {"enable_dlc": False}])
def test_full_catalogue_generates_from_the_bundled_pool(seed, extra):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring import bingo_manual
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
        options={"bingo_mode": True, "bingo_catalogue": "full", **extra})
    board = mw.worlds[1].gf_bingo_board
    labels = {r["label"] for r in bingo_manual.bundled()}
    assert len(board) == 25 and all(cell["label"] in labels for cell in board)
    assert not any("detector" in cell or "scope" in cell for cell in board)
    tracked = [c for c in board if c.get("flag") or c.get("counter") or c.get("state") or c.get("collection")]
    assert len(tracked) >= 10, "the bundled pool lost its automatic tracking"
