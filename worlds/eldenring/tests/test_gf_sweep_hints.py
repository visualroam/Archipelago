"""Hints must describe the owning slot's emitted sweeps, not the static corpus."""
import pytest

from test.general import setup_multiworld
from worlds.AutoWorld import AutoWorldRegister, call_all, data_package_checksum
from worlds.eldenring import sweep_hints
from worlds.eldenring.features.boss_locks import DUNGEON_SWEEPS


def test_shared_package_keeps_ids_and_identity_but_removes_sweep_promises():
    world = AutoWorldRegister.world_types["Elden Ring"]
    original = dict(world.location_name_to_id)
    package = world.get_data_package_data()
    assert original == world.location_name_to_id
    assert set(package["location_name_to_id"].values()) == set(original.values())
    assert len(package["location_name_to_id"]) == len(original)
    assert any("may be sweep-granted by" in name for name in original)
    for name, aid in original.items():
        assert package["location_name_to_id"][sweep_hints.location_name(name)] == aid
    for members in package["location_name_groups"].values():
        assert set(members) <= package["location_name_to_id"].keys()
    checksum = package.pop("checksum")
    assert checksum == data_package_checksum(package)


@pytest.mark.parametrize("opener", ["may be sweep-granted by", "also granted by"])
def test_removes_old_and_current_clause_without_losing_flag(opener):
    assert sweep_hints.location_name(
        f"Weeping :: Gold-Tinged Excrement, {opener} Ancient Hero of Zamor (m60_42_33) [f1043347040]"
    ) == "Weeping :: Gold-Tinged Excrement [f1043347040]"


def test_two_players_have_independent_hints_for_the_same_pickup():
    world = AutoWorldRegister.world_types["Elden Ring"]
    mw = setup_multiworld([world, world], seed=4242, options=[
        {"num_regions": 0, "dungeon_sweep": "all"},
        {"num_regions": 0, "dungeon_sweep": "bosses"},
    ])
    hints = {}
    call_all(mw, "extend_hint_information", hints)
    heal = next(aid for name, aid in world.location_name_to_id.items() if "[f1043347040]" in name)
    assert hints[1][heal] == "Manual pickup"
    assert hints[2][heal] == "Swept by Ancient Hero of Zamor"
    for player in mw.player_ids:
        wire = mw.worlds[player].fill_slot_data().get("dungeonSweepFlags", {})
        paid = {aid for members in wire.values() for aid in members}
        locations = {loc.address for loc in mw.get_locations(player) if loc.address is not None}
        assert {aid for aid, text in hints[player].items() if text != "Manual pickup"} == paid & locations


@pytest.mark.parametrize("options", [
    {"dungeon_sweep": "none"},
    {"dungeon_sweep": "minidungeons", "full_area_sweeps": True},
    {"dungeon_sweep": "bosses", "region_sweep": True},
])
def test_hint_hook_matches_final_wire_with_options_and_bingo_reservations(options):
    world = AutoWorldRegister.world_types["Elden Ring"]
    mw = setup_multiworld(world, seed=4242, options=options)
    slot = mw.worlds[1]
    wire = slot.fill_slot_data().get("dungeonSweepFlags", {})
    reserved = next((aid for members in wire.values() for aid in members), None)
    slot.gf_bingo_protected_checks = {reserved} if reserved is not None else set()
    hints = {}
    call_all(mw, "extend_hint_information", hints)
    wire = slot.fill_slot_data().get("dungeonSweepFlags", {})
    paid = {aid for members in wire.values() for aid in members}
    locations = {loc.address for loc in mw.get_locations(1) if loc.address is not None}
    candidates = {aid for members in DUNGEON_SWEEPS.values() for aid in members}
    assert set(hints[1]) == locations & (candidates | paid)
    assert {aid for aid, text in hints[1].items() if text != "Manual pickup"} == paid & locations
    if reserved in hints[1]:
        assert hints[1][reserved] == "Manual pickup"
    if reserved is not None:
        slot.gf_bingo_line_sweep = [reserved]
        call_all(mw, "extend_hint_information", hints)
        assert hints[1][reserved] == "Collected by a bingo line"
