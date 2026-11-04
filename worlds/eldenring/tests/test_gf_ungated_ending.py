"""An ending with NO requirement is refused at generation (#1652).

Found in a real 0.6.1.7 multidata: `ending_condition: region_locks` (an old yaml, from when the
policy default was items_held) with the new default `goal_region_unlock_policy: none` and
`goal: promised_consort`. Zero required runes, zero required Locks, zero required Ability Unlocks:
the withheld Enir Ilim entrance rule was `has_all(())` -- always true -- so all 106 Enir Ilim checks
sat in sphere 0, no Enir Ilim Lock was minted, and the client's goal_gate opened the region on
connect. Logic and client agreed, so nothing noticed. `core._lint_goal_gate` refuses it.
"""
import pytest

pytest.importorskip("test.bases")
pytest.importorskip("worlds.eldenring")
from Options import OptionError  # noqa: E402


def _generate(**options):
    from test.general import setup_multiworld  # noqa: E402
    from worlds.eldenring.core import GreenfieldEldenRingWorld  # noqa: E402
    return setup_multiworld(GreenfieldEldenRingWorld, ("generate_early",), options=options)


@pytest.mark.parametrize("goal", ["auto", "promised_consort", "malenia", "elden_beast"])
def test_region_locks_with_policy_none_is_refused(goal):
    with pytest.raises(OptionError) as excinfo:
        _generate(num_regions=4, goal=goal, ending_condition="region_locks",
                  goal_region_unlock_policy="none")
    msg = str(excinfo.value)
    # Both options named, and both ways out.
    for needle in ("ending_condition", "goal_region_unlock_policy", "great_runes", "items_held"):
        assert needle in msg, msg


def test_the_reported_seed_shape_is_refused():
    # The 0.6.1.7 report: region_locks, policy left at its default (none), PCR goal.
    with pytest.raises(OptionError, match="no requirement"):
        _generate(num_regions=4, goal="promised_consort", ending_condition="region_locks")


def test_great_runes_with_zero_eligible_runes_is_refused(monkeypatch):
    # Shuffle off -> no Great Rune is in the pool, so great_runes clamps to 0. item_shuffle is
    # FROZEN on (defaults.py), so no yaml reaches this today; patch the predicate so the guard is
    # still exercised if it is ever unfrozen.
    from worlds.eldenring.core import GreenfieldEldenRingWorld
    monkeypatch.setattr(GreenfieldEldenRingWorld, "_shuffle_on", lambda self: False)
    with pytest.raises(OptionError, match="no eligible Great Runes"):
        _generate(num_regions=4, ending_condition="great_runes",
                  goal_region_unlock_policy="none")


@pytest.mark.parametrize("options", [
    dict(ending_condition="region_locks", goal_region_unlock_policy="items_held"),
    dict(ending_condition="region_locks", goal_region_unlock_policy="regions_completed"),
    dict(ending_condition="great_runes", goal_region_unlock_policy="none"),
    dict(ending_condition="region_locks", goal_region_unlock_policy="none",
         required_bosses=["starscourge_radahn"]),
], ids=["items_held", "regions_completed", "great_runes", "required_bosses"])
def test_any_real_requirement_generates(options):
    _generate(num_regions=4, goal="promised_consort", **options)
