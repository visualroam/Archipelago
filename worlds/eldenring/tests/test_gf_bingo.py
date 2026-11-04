"""Board invariants and generation refusals; no game process required."""
import pytest
from worlds.eldenring.bingo_board import LINES, has_line, is_complete, select_board
from test.bases import WorldTestBase
from Options import OptionError


def _force(monkeypatch, pick):
    """Put one adapter candidate on the last square of a full board, where adapters ship."""
    from worlds.eldenring import bingo_manual
    select = bingo_manual.select
    keep = {"flag", "region", "regions", "state", "counter", "collection", "requirements",
            "supply_goal", "label", "family", "adapter"}
    def forced(pool, seed, eligible, *, automatic=()):
        board = select(pool, seed, eligible, automatic=automatic)
        target = next(c for c in automatic if pick(c))
        board[-1] = dict({k: v for k, v in target.items() if k in keep},
                         location=board[-1]["location"], manual=True)
        return board
    monkeypatch.setattr(bingo_manual, "select", forced)


def test_e3_admitted_deaths_are_script_verified():
    from pathlib import Path
    from ._util import find_repo_root
    from worlds.eldenring.bingo_e3 import DEATHS, REWARD_DEATH
    repo = Path(find_repo_root(__file__))
    root = repo / "elden_ring_artifacts/event"
    if not root.exists():
        pytest.skip("Native EMEVD corpus is unavailable; admission sources documented in module")
    import re
    import csv
    with (repo / "greenfield/flag_lots.tsv").open(encoding="utf-8") as f:
        lot_flags = {int(r["lot"]): int(r["flag"]) for r in csv.DictReader(f, delimiter="\t") if r["table"] == "map"}
    common = (root / "common_func.emevd.dcx.js").read_text(encoding="utf-8")
    for event in (90005300, 90005301):
        body = common.split(f"$Event({event},", 1)[1].split("$Event(", 1)[0]
        assert body.index("WaitFor(CharacterRatioDead(chrEntityId))") < body.index("SetEventFlagID(eventFlagId, ON)")
    for members in DEATHS.values():
        for flag, entity, map_name, _region in members:
            text = (root / f"{map_name}.emevd.dcx.js").read_text(encoding="utf-8")
            match = re.search(rf"InitializeCommonEvent\(0, 9000530[01], {flag}, {entity}, (\d+), [\d.]+, [02]\)", text)
            assert match
            lot = int(match[1])
            if lot:
                assert REWARD_DEATH[lot_flags[lot]] == flag
    moon = (root / "m61_47_44_00.emevd.dcx.js").read_text(encoding="utf-8").split("$Event(2047442360,", 1)[1]
    assert moon.index("WaitFor(CharacterDead(2047440360))") < moon.index("SetNetworkconnectedEventFlagID(2047440360, ON)")


def test_e3_native_rosters_use_distinct_deaths_and_correct_owners():
    from worlds.eldenring.core import TABLES
    from worlds.eldenring import bingo_e3
    cells = bingo_e3.candidates(TABLES, TABLES.regions, 12)
    assert {c["adapter"] for c in cells} == {a for _, a, _, _ in bingo_e3.OBJECTIVES}
    for cell in cells:
        for group in cell.get("counter", []):
            assert len({m["flag"] for m in group["members"]}) == len(group["members"])
            assert sum(m["weight"] for m in group["members"]) >= group["target"]
    assert any(m["flag"] == 2051440310 for c in cells for g in c.get("counter", []) for m in g["members"])
    assert all(m["region"] == "Shadow Keep" for c in cells for g in c.get("counter", []) for m in g["members"] if m["flag"] in {21000470, 21000471})
    assert not bingo_e3.candidates(TABLES, {"Limgrave"}, 6)
    miriam = next(c for c in cells if c["adapter"] == "boss/preceptor-miriam")
    assert {m["flag"] for m in miriam["counter"][0]["members"]} == {34110710, 34110711}
    assert miriam["counter"][0]["target"] == 1
    assert all(m["flag"] != 34110800 for c in cells for g in c.get("counter", []) for m in g["members"])


@pytest.mark.parametrize("adapter", [
    "roster/crucible-knight/2", "roster/crucible-knight/3", "roster/crucible-knight/4", "boss/preceptor-miriam",
    "roster/tree-spirit", "roster/elder-lion/2", "roster/elder-lion/3", "roster/elder-lion/4",
    "roster/furnace-golem/1", "roster/furnace-golem/2", "roster/hippopotamus", "roster/dlc-tree-spirit",
    "boss/black-knight-garrew", "boss/moonrithyll", "boss/madding-hand"])
def test_each_native_death_objective_is_fillable(monkeypatch, adapter):
    from Fill import distribute_items_restrictive
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    _force(monkeypatch, lambda c: c.get("adapter") == adapter)
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=42,
        options={"bingo_mode": True, "bingo_catalogue": "full"})
    assert mw.worlds[1].gf_bingo_board[-1]["adapter"] == adapter
    distribute_items_restrictive(mw)
    assert mw.can_beat_game()


def test_e3_inherits_native_reward_access_rules(monkeypatch):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    _force(monkeypatch, lambda c: c.get("adapter") == "boss/moonrithyll")
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=42,
        options={"bingo_mode": True, "bingo_catalogue": "full"})
    w = mw.worlds[1]
    witnesses = [mw.get_location(name, 1) for r in w._kept() for name, aid, flag in w._seed_locations(r) if flag == 530865]
    assert witnesses
    square = mw.get_location("Bingo Square 25", 1)
    state = mw.get_all_state(False)
    assert square.access_rule(state)
    for witness in witnesses:
        witness.access_rule = lambda state: False
    assert not square.access_rule(state)


@pytest.mark.parametrize("seed", [1, 7, 42, 99, 22222])
@pytest.mark.parametrize("extra", [{"enable_dlc": False}, {"dlc_only": True}, {}])
def test_full_boards_fill_and_protect_their_evidence(seed, extra):
    from Fill import distribute_items_restrictive
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.features.bingo import evidence_flags
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
        options={"bingo_mode": True, "bingo_catalogue": "full", "bingo_graces": True, **extra})
    world = mw.worlds[1]
    sd = world.fill_slot_data()
    assert sd["bingoBoard"]["version"] == 5
    assert sd["bingoBoard"]["catalogue"] == "ap-manual-board-v1"
    assert "bingo_manual_v1" in sd["requiresClientFeatures"]
    flags = {f for c in world.gf_bingo_board for f in evidence_flags(c)}
    assert len(world.gf_bingo_board) == 25
    assert not flags.intersection(sd["locationFlags"].get(str(aid), 0) for aid in sd["bingoBoard"]["line_sweep"])
    assert not flags.intersection(sd["locationFlags"].get(str(aid), 0) for members in sd.get("dungeonSweepFlags", {}).values() for aid in members)
    assert sd["areaLockFlags"] == []
    distribute_items_restrictive(mw)
    assert not mw.get_unfilled_locations()
    assert mw.can_beat_game()

def test_all_lines_and_incomplete_lines():
    assert len(LINES) == 12
    for line in LINES:
        done = [i in line for i in range(25)]
        assert has_line(done)
        done[line[0]] = False
        assert not has_line(done)
    assert not is_complete([True] * 12 + [False] * 13, "count", 13)
    assert is_complete([True] * 13 + [False] * 12, "count", 13)
    assert not is_complete([True] * 24 + [False], "blackout", 13)


def test_board_identity_is_order_independent_and_insufficient_pool_refuses():
    candidates = [{"flag": i + 1, "region": "Test", "label": str(i)} for i in range(40)]
    assert select_board(candidates, 7) == select_board(list(reversed(candidates)), 7)
    assert select_board(candidates, 7) != select_board(candidates, 8)
    with pytest.raises(ValueError, match="25 eligible"):
        select_board(candidates[:24], 7)


@pytest.mark.parametrize("extra", [{"vanilla_placement": "all"}, {"natural_progression": True},
                                  {"mario_mode": True}, {"goal": "elden_beast"}])
def test_incompatible_options_fail_actionably(extra):
    class _T(WorldTestBase):
        game = "Elden Ring"
        options = {"bingo_mode": True, "num_regions": 12, **extra}
    t = _T()
    try:
        with pytest.raises(OptionError, match="bingo"):
            t.world_setup(seed=7)
    finally:
        t.tearDown()


def test_objectives_choose_regions_with_prerequisite_closure():
    candidates = [{"flag": i + 1, "region": f"R{i // 15}", "label": str(i)} for i in range(90)]
    board = select_board(candidates, 42, region_limit=3, parents={"R1": "R0"},
                         start_pool={"R2"})
    owners = {c["region"] for c in board}
    kept = owners | ({"R0"} if "R1" in owners else set())
    assert len(board) == 25 and "R2" in owners and len(kept) <= 3
    assert board == select_board(list(reversed(candidates)), 42, region_limit=3,
                                 parents={"R1": "R0"}, start_pool={"R2"})


@pytest.mark.parametrize("seed", [1, 7, 42, 22222])
@pytest.mark.parametrize("extra", [{"enable_dlc": False},
                                  {"num_regions": 0}, {"start_region_pool": ["Limgrave"]}])
def test_kept_regions_are_exactly_objective_owners_and_prerequisites(seed, extra):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.region_spine import parent_chain
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
                         options={"bingo_mode": True, **extra})
    world = mw.worlds[1]
    owners = {c["region"] for c in world.gf_bingo_board}
    expected = owners | {p for r in owners for p in parent_chain(r)}
    assert set(world._kept()) == expected
    assert len(expected) <= world.options.bingo_region_limit.value
    assert owners <= set(world.gf_eligible)


def test_dlc_only_catalogue_fails_actionably():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    with pytest.raises(OptionError, match="bingo needs 25 eligible"):
        setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=7,
                         options={"bingo_mode": True, "dlc_only": True})


def test_start_region_count_and_capacity_refusal():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from BaseClasses import ItemClassification
    from worlds.eldenring.features.progression_surface import apply
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=42,
                         options={"bingo_mode": True, "start_regions": 3})
    world = mw.worlds[1]
    starts = {item.name.removesuffix(" Lock") for item in mw.precollected_items[1]
              if item.name.endswith(" Lock")}
    assert not starts
    assert not any(i.name.endswith(" Lock") for i in mw.itempool)
    sd = world.fill_slot_data()
    assert sd["areaLockFlags"] == []
    points = world.tables.modules["region_graces"].REGION_GRACE_POINTS
    assert all(set(points[r]) <= set(sd["startGraces"]) for r in world._kept())
    assert all(mw.state.can_reach(r, "Region", 1) for r in world._kept())
    # Foreign pressure beyond the square budget must fail before ordinary fill can spill it.
    for item in [i for i in mw.itempool if not i.advancement][:40]:
        item.classification = ItemClassification.progression
    with pytest.raises(OptionError, match="reward capacity"):
        apply(world)


def test_bingo_off_preserves_default_generation():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    world_type = AutoWorldRegister.world_types["Elden Ring"]
    baseline = setup_multiworld(world_type, seed=42, options={"num_regions": 6})
    explicit = setup_multiworld(world_type, seed=42,
                               options={"num_regions": 6, "bingo_mode": False})
    assert [(i.name, i.classification) for i in baseline.itempool] == [
        (i.name, i.classification) for i in explicit.itempool]
    assert [(l.name, l.address) for l in baseline.get_locations()] == [
        (l.name, l.address) for l in explicit.get_locations()]
    assert baseline.worlds[1].fill_slot_data() == explicit.worlds[1].fill_slot_data()
    assert "bingoBoard" not in explicit.worlds[1].fill_slot_data()


@pytest.mark.parametrize("seed", [1, 7, 42, 22222, 99])
@pytest.mark.parametrize("extra", [{"enable_dlc": False}, {"dlc_only": True}, {}])
def test_full_board_generation_and_reward_capacity(seed, extra):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.features.progression_surface import apply
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=seed,
        options={"bingo_mode": True, "bingo_catalogue": "full", **extra})
    w = mw.worlds[1]
    board = w.gf_bingo_board
    assert set(w._kept()) == set(w.gf_eligible)
    assert len(board) == 25 and len({c["label"] for c in board}) == 25
    for name, count in w.gf_bingo_requirements.items():
        assert sum(i.name == name and i.advancement for i in mw.itempool) >= count
    assert len(mw.itempool) == len([l for l in mw.get_unfilled_locations() if l.address is not None])
    apply(w)
    sd = w.fill_slot_data()
    assert sd["bingoBoard"]["version"] == 5
    assert "bingo_manual_v1" in sd["requiresClientFeatures"]
    flags = {c["flag"] for c in board if c["flag"]}
    overrides = getattr(w, "gf_extra_location_flags", {})
    for members in sd.get("dungeonSweepFlags", {}).values():
        assert all(sd["locationFlags"].get(str(aid), overrides.get(aid, 0)) not in flags for aid in members)


def test_e1_every_family_has_an_adapter():
    from worlds.eldenring import bingo_e1, bingo_manual
    from worlds.eldenring.tables.boss_healthbars import BOSS_HEALTHBARS
    from worlds.eldenring.tables.boss_sweeps import SWEEP_ARENA_REGION, SWEEP_REGION
    eligible = set(SWEEP_ARENA_REGION.values()) | {"Stormveil", "Liurnia"}
    cells = bingo_e1.candidates(BOSS_HEALTHBARS, SWEEP_ARENA_REGION, eligible, sweep_regions=SWEEP_REGION)
    adapters = set(bingo_e1.BOSSES) | {a for _, targets, _, _ in bingo_e1.STATE_GOALS for _, a in targets}
    assert {c["adapter"] for c in cells} == adapters
    assert len({c["adapter"] for c in cells if "state" in c}) == 14
    bundled = {r["detector"]["adapter"] for r in bingo_manual.bundled() if r.get("detector")}
    assert adapters <= bundled
    for c in cells:
        if c["flag"]:
            assert c["flag"] in BOSS_HEALTHBARS
    assert all(c["flag"] != 15000850 for c in cells if c["adapter"] == "boss/loretta-caria")
    assert all(c["flag"] == 31110800 for c in cells if c["adapter"] == "boss/putrid-crystalian-trio")


@pytest.mark.parametrize("extra", [{"enable_dlc": False}, {"dlc_only": True}, {}])
def test_curated_graces_change_travel_only(extra):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.region_spine import DLC_REGIONS
    from worlds.eldenring.features.bingo import CURATED_BASE_GRACES, CURATED_DLC_GRACE
    world_type = AutoWorldRegister.world_types["Elden Ring"]
    opts = {"bingo_mode": True, "bingo_catalogue": "full", **extra}
    baseline = setup_multiworld(world_type, seed=42, options=opts)
    curated = setup_multiworld(world_type, seed=42, options={**opts, "bingo_graces": True})
    w = curated.worlds[1]
    sd = w.fill_slot_data()
    assert w.gf_bingo_board == baseline.worlds[1].gf_bingo_board
    assert [(i.name, i.classification) for i in curated.itempool] == [
        (i.name, i.classification) for i in baseline.itempool]
    names = w.tables.modules["region_graces"].REGION_GRACE_POINTS
    all_warp_flags = {f for flags in names.values() for f in flags} | {71190}
    expected = set(CURATED_BASE_GRACES) if set(w._kept()) - DLC_REGIONS else {71190}
    if set(w._kept()) & DLC_REGIONS:
        expected.add(CURATED_DLC_GRACE)
    assert set(sd["startGraces"]) & all_warp_flags == expected
    assert sd["startGraces"][0] == 71190  # Existing client sentinel remains a real grace.
    assert sd["areaLockFlags"] == [] and sd["regionGraces"] == {}
    assert not any(i.name.endswith(" Lock") for i in curated.itempool)
    assert sd["regionOpenFlags"] == {}  # Open tracker regions without extra anchor-grace grants.


def test_curated_graces_ignored_outside_bingo():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    world_type = AutoWorldRegister.world_types["Elden Ring"]
    baseline = setup_multiworld(world_type, seed=42, options={"num_regions": 6})
    enabled = setup_multiworld(world_type, seed=42, options={"num_regions": 6, "bingo_graces": True})
    assert baseline.worlds[1].fill_slot_data()["startGraces"] == enabled.worlds[1].fill_slot_data()["startGraces"]


@pytest.mark.parametrize("seed", [1,7,42,22222,99])
@pytest.mark.parametrize("extra", [{"enable_dlc": False},{"dlc_only": True},{}])
def test_full_board_counters_have_supported_contributors(seed,extra):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.features.bingo import evidence_flags
    mw=setup_multiworld(AutoWorldRegister.world_types["Elden Ring"],seed=seed,
        options={"bingo_mode":True,"bingo_catalogue":"full",**extra})
    w=mw.worlds[1]
    sd=w.fill_slot_data()
    assert any(c.get("counter") for c in w.gf_bingo_board), "no counter square was drawn, so nothing was checked"
    hits={}
    for c in w.gf_bingo_board:
        for f in evidence_flags(c): hits[f]=hits.get(f,0)+1
        for g in c.get("counter",[]):
            assert sum(m["weight"] for m in g["members"]) >= g["target"]
            assert len({(m["flag"], m.get("unit", 0)) for m in g["members"]}) == len(g["members"])
            assert all(m["region"] in w._kept() for m in g["members"])
    assert len(mw.itempool) == len([l for l in mw.get_unfilled_locations() if l.address is not None])
    for members in sd.get("dungeonSweepFlags",{}).values():
        assert all(sd["locationFlags"].get(str(aid),0) not in hits for aid in members)


def test_e2_full_catalogue_exposes_source_blockers():
    from worlds.eldenring.core import TABLES
    from worlds.eldenring import bingo_e2
    cells,unavailable=bingo_e2.candidates(TABLES,TABLES.regions,12)
    assert len(bingo_e2.CATALOGUE)==125
    # Too few distinct encounters exist for the top counts, and one Blessing has no known place.
    assert set(unavailable)=={"roster/red-wolf/3","roster/tibia-mariner/4","check/blessing-of-marika/3"}
    assert len({c["adapter"] for c in cells})==122
    # Miniboss partner bars cannot become independent dungeon completions.
    for c in cells:
        for g in c.get("counter",[]):
            assert all(m["flag"] not in {12020801,31110801,31110802,30100801} for m in g["members"])


def test_e2_catalogue_matches_objective_ledger():
    from worlds.eldenring import bingo_manual
    from worlds.eldenring.bingo_e2 import CATALOGUE
    bundled = {r["detector"]["adapter"]: r for r in bingo_manual.bundled() if r.get("detector")}
    assert len({r["adapter"] for r in CATALOGUE}) == len(CATALOGUE)
    for row in CATALOGUE:
        ours = bundled[row["adapter"]]
        assert (ours["family"], ours["scope"], ours["label"]) == (row["family"], row["scope"], row["label"])


def test_e2_collection_squares_count_vanilla_location_pickups():
    """A collect square is a counter over the items' vanilla check flags, never possession."""
    from worlds.eldenring.core import TABLES
    from worlds.eldenring import bingo_e2
    cells, _ = bingo_e2.candidates(TABLES, TABLES.regions, 6)
    kinds = {r["adapter"]: r["kind"] for r in bingo_e2.CATALOGUE}
    checks = [c for c in cells if kinds[c["adapter"]] == "collection"]
    assert len({c["adapter"] for c in checks}) == 42
    where = {flag: region for region, rows in TABLES.locations.items() for _name, _aid, flag in rows}
    item_at = {flag: TABLES.location_item.get(aid) for rows in TABLES.locations.values() for _name, aid, flag in rows}
    for c in checks:
        assert "collection" not in c and not c["requirements"] and not c.get("supply_goal")
        assert c["label"].startswith("Do ")
        (group,) = c["counter"]
        assert 1 <= group["target"] <= len(group["members"])
        for m in group["members"]:
            assert where[m["flag"]] == m["region"] != TABLES.hub
            assert "sweep-granted" not in m["label"] and "[f" not in m["label"]
    blade = next(c for c in checks if c["family"] == "check/fingerslayer-blade")
    assert blade["label"] == "Do the Fingerslayer Blade check"
    assert [item_at[m["flag"]] for m in blade["counter"][0]["members"]] == ["Fingerslayer Blade"]
    pots = next(c for c in checks if c["adapter"] == "check/cracked-pot")
    assert pots["label"] == "Do 10 Cracked Pot checks"
    assert {item_at[m["flag"]] for m in pots["counter"][0]["members"]} == {"Cracked Pot"}


def test_unique_objectives_cover_all_eligible_source_checks():
    from worlds.eldenring.core import TABLES
    from worlds.eldenring import bingo_e2, bingo_e3
    from worlds.eldenring.features.bingo import counter_total
    cells, _ = bingo_e2.candidates(TABLES, TABLES.regions, 6)
    for row in bingo_e2.CATALOGUE:
        if row["kind"] != "collection" or not row.get("distinct"):
            continue
        candidates = [c for c in cells if c["adapter"] == row["adapter"]]
        assert len(candidates) == 1
        (group,) = candidates[0]["counter"]
        expected = bingo_e2._vanilla_rows(bingo_e2._collection(row, TABLES), TABLES, TABLES.regions)
        assert {(m["flag"], m["unit"]) for m in group["members"]} == {(m["flag"], m["unit"]) for m in expected}
        assert counter_total(group["members"]) >= group["target"]
    talismans = next(c for c in cells if c["adapter"] == "check/talismans-10-unique-talismans")
    assert len(talismans["regions"]) > 6
    assert counter_total(talismans["counter"][0]["members"]) > 80
    materials = next(c for c in cells if c["adapter"] == "check/top-upgrade-materials/3")
    assert counter_total(materials["counter"][0]["members"]) == 4
    assert len(materials["counter"][0]["members"]) > 4
    # A second physical copy does not manufacture another distinct material.
    members = materials["counter"][0]["members"]
    same = [m for m in members if m["unit"] == members[0]["unit"]]
    assert len(same) > 1 and counter_total(same) == 1
    small = bingo_e3.candidates(TABLES, TABLES.regions, 6)
    wide = bingo_e3.candidates(TABLES, TABLES.regions, 50)
    for cell in small:
        if "different" in cell["label"].casefold() and cell.get("counter"):
            assert cell in wide


@pytest.mark.parametrize("family", ["check/cracked-pot", "check/fingerslayer-blade", "check/sorceries",
    "check/memory-stone", "check/haligtree-medallion", "check/hefty-pot", "check/gravebird-set"])
def test_check_squares_are_never_swept_and_fill(monkeypatch, family):
    """The square's pickups stay physical: no dungeon sweep or line bonus may grant them."""
    from Fill import distribute_items_restrictive
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.features.bingo import evidence_flags
    _force(monkeypatch, lambda c: c.get("family") == family)
    mw = setup_multiworld(AutoWorldRegister.world_types["Elden Ring"], seed=42,
        options={"bingo_mode": True, "bingo_catalogue": "full"})
    w = mw.worlds[1]
    cell = next(c for c in w.gf_bingo_board if c.get("family") == family)
    flags = evidence_flags(cell)
    assert flags and 0 not in flags
    sd = w.fill_slot_data()
    overrides = getattr(w, "gf_extra_location_flags", {})
    flag_of = lambda aid: sd["locationFlags"].get(str(aid), overrides.get(aid, 0))
    swept = [aid for members in sd.get("dungeonSweepFlags", {}).values() for aid in members]
    assert swept, "no dungeon sweep was emitted, so the exemption was never exercised"
    assert not flags.intersection(map(flag_of, swept))
    assert not flags.intersection(map(flag_of, sd["bingoBoard"]["line_sweep"]))
    distribute_items_restrictive(mw)
    assert mw.can_beat_game()


@pytest.mark.parametrize("size", range(5, 13))
def test_board_dimensions_lines_and_goals(size):
    from worlds.eldenring.bingo_board import lines, LOCATION_NAMES
    area = size * size
    for line in lines(size):
        done = [i in line for i in range(area)]
        assert has_line(done, size)
        assert is_complete(done, "line", 1, size)
        assert not is_complete(done, "blackout", 1, size)
    assert not has_line([False] * area, size)
    assert is_complete([True] * area, "blackout", 1, size)
    assert not is_complete([True] * (area - 1) + [False], "count", area, size)
    assert len(LOCATION_NAMES) == 144


@pytest.mark.parametrize("size", range(6, 13))
def test_board_size_seed_sweep_and_family_capacity(size):
    from worlds.eldenring.bingo_manual import select
    rows = [{"label": f"Objective {i}", "family": str(i), "scope": "base"} for i in range(144)]
    candidates = [{"flag": i + 1, "region": "R", "label": str(i)} for i in range(144)]
    for seed in range(12):
        board = select(rows, seed, {"Limgrave"}, size=size)
        assert len(board) == size * size
        assert len({c["label"] for c in board}) == size * size
        assert len(select_board(candidates, seed, region_limit=1, size=size)) == size * size
    with pytest.raises(OptionError, match=f"{size * size} distinct families"):
        select(rows[:size * size - 1], 0, {"Limgrave"}, size=size)
    with pytest.raises(ValueError, match="eligible boss encounters"):
        select_board(candidates[:size * size - 1], 0, size=size)


@pytest.mark.parametrize("size", range(6, 13))
def test_large_board_generation_contract_and_pool(size):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.gamename import GAME
    from worlds.eldenring.bingo_board import LOCATION_NAMES
    rows = [{"label": f"Objective {i}", "family": str(i), "scope": "base"} for i in range(144)]
    mw = setup_multiworld(AutoWorldRegister.world_types[GAME], seed=42,
        options={"bingo_mode": True, "bingo_catalogue": "full", "bingo_manual_pool": rows,
                 "bingo_board_size": size, "bingo_goal": "count", "bingo_square_count": size * size})
    w = mw.worlds[1]
    payload = w.fill_slot_data()
    assert payload["bingoBoard"]["size"] == size
    assert "bingo_board_sizes_v1" in payload["requiresClientFeatures"]
    squares = [l for l in mw.get_locations(1) if l.address in LOCATION_NAMES.values()]
    assert len(squares) == size * size
    assert len({l.address for l in mw.get_locations(1) if l.address is not None}) == len([l for l in mw.get_locations(1) if l.address is not None])


def test_count_goal_rejects_board_overflow():
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.gamename import GAME
    with pytest.raises(OptionError, match="cannot exceed 25"):
        setup_multiworld(AutoWorldRegister.world_types[GAME], seed=42,
            options={"bingo_mode": True, "bingo_goal": "count", "bingo_square_count": 26})


@pytest.mark.parametrize("size", (11, 12))
def test_bundled_base_pool_large_board_capacity(size):
    from worlds.eldenring.bingo_manual import select
    with pytest.raises(OptionError, match="only 109 remain"):
        select([], 42, {"Limgrave"}, size=size)
    assert len(select([], 42, {"Limgrave", "Gravesite"}, size=size)) == size * size


@pytest.mark.parametrize("goal", ("line", "blackout"))
def test_ignored_count_is_valid_on_wire(goal):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.gamename import GAME
    mw = setup_multiworld(AutoWorldRegister.world_types[GAME], seed=42,
        options={"bingo_mode": True, "bingo_goal": goal, "bingo_square_count": 144})
    payload = mw.worlds[1].fill_slot_data()
    assert payload["bingoBoard"]["count"] == 25
    assert "size" not in payload["bingoBoard"]
    assert "bingo_board_sizes_v1" not in payload["requiresClientFeatures"]


@pytest.mark.parametrize("size,goal,seed", [(6,"line",41),(9,"count",42),(12,"blackout",43)])
def test_bundled_large_board_actual_fill(size, goal, seed):
    from Fill import distribute_items_restrictive
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.gamename import GAME
    mw = setup_multiworld(AutoWorldRegister.world_types[GAME], seed=seed,
        options={"bingo_mode": True, "bingo_catalogue": "full", "bingo_board_size": size,
                 "bingo_goal": goal, "bingo_square_count": size * size})
    assert len(mw.worlds[1].gf_bingo_board) == size * size
    distribute_items_restrictive(mw)
    assert not mw.get_unfilled_locations()
    assert mw.can_beat_game()


@pytest.mark.parametrize("size", (6, 9, 12))
def test_boss_large_board_actual_capacity(size):
    from test.general import setup_multiworld
    from worlds.AutoWorld import AutoWorldRegister
    from worlds.eldenring.gamename import GAME
    try:
        mw = setup_multiworld(AutoWorldRegister.world_types[GAME], seed=42,
            options={"bingo_mode": True, "bingo_board_size": size, "bingo_region_limit": 12})
    except OptionError as exc:
        assert size == 12 and ("eligible boss encounters" in str(exc) or "cannot fit" in str(exc))
    else:
        assert len(mw.worlds[1].gf_bingo_board) == size * size



def test_e2_counter_wire_labels_are_nonempty():
    from worlds.eldenring.bingo_e2 import candidates
    from worlds.eldenring.core import TABLES
    cells, _ = candidates(TABLES, TABLES.regions, len(TABLES.regions), global_rosters=True)
    assert all(m["label"] for cell in cells for group in cell.get("counter", []) for m in group["members"])
    assert any(m["flag"] == 30130810 for cell in cells for group in cell.get("counter", []) for m in group["members"])



def test_default_board_preserves_legacy_seed_draw():
    import hashlib
    import json
    candidates = [dict(flag=i + 1, region="R", label=str(i)) for i in range(144)]
    board = select_board(candidates, 42)
    # Fingerprint derived from the unmodified v0.6.5.5 selector before adding size.
    assert hashlib.sha256(json.dumps(board, sort_keys=True).encode()).hexdigest() == "6003c93b6f95b80207cebfbbd4849d5b07862fdef66ed21d67dadfbaa04e51d8"
