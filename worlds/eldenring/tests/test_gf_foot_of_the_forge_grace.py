"""#1658: Foot of the Forge rides Mountaintops' Lock; Fire Giant stays boss-gated.

Exercise the production slot-data hook against the real generated tables, without
rolling a whole world. Identity/gate evidence comes from the source TSVs, not the
manual arena exclusion that caused the regression.
"""
import csv
from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("worlds.eldenring")

from worlds.eldenring import contract  # noqa: E402
from worlds.eldenring.features.graces import RegionGraceUnlock, RegionGracesFeature  # noqa: E402
from ._util import find_repo_root  # noqa: E402

_REGION = "Mountaintops of the Giants"
_LOCK = f"{_REGION} Lock"
_FOOT = 76508
_FIRE_GIANT = 76509


def _slot(tier=None, *, kept=True, attunement=0):
    options = SimpleNamespace(grace_attunement=SimpleNamespace(value=attunement))
    if tier is not None:
        options.region_grace_unlock = RegionGraceUnlock.from_any(tier)
    world = SimpleNamespace(options=options, _kept=lambda: [_REGION] if kept else [])
    return RegionGracesFeature().slot_data(world)


def test_source_identity_distinguishes_foot_of_the_forge_from_fire_giant():
    root = find_repo_root(str(Path(__file__).parent))
    assert root is not None, "source TSVs require a repository checkout"
    with (Path(root) / "greenfield/grace_flags.tsv").open(encoding="utf-8", newline="") as source:
        graces = {int(row["warpUnlockFlag"]): row for row in csv.DictReader(source, delimiter="\t")}
    assert graces[_FOOT]["placeName"] == "Foot of the Forge"
    assert graces[_FOOT]["mapTile"] == "m60_52_53"
    assert graces[_FIRE_GIANT]["placeName"] == "Fire Giant"
    assert graces[_FIRE_GIANT]["mapTile"] == "m60_53_52"
    with (Path(root) / "greenfield/boss_gated_graces.tsv").open(encoding="utf-8", newline="") as source:
        gates = {int(row["grace_flag"]): row for row in csv.DictReader(source, delimiter="\t")}
    assert _FOOT not in gates
    assert gates[_FIRE_GIANT]["gate_flag"] == "1252520800"
    assert gates[_FIRE_GIANT]["gate_source"] == "emevd:9005810"


@pytest.mark.parametrize("tier", [None, "all"])
def test_default_and_all_grant_foot_of_the_forge_on_mountaintops_unlock(tier):
    slot = _slot(tier)
    assert _FOOT in slot[contract.REGION_GRACES][_LOCK]
    assert _FIRE_GIANT not in slot[contract.REGION_GRACES][_LOCK]
    assert contract.GRACE_ATTUNEMENT not in slot


def test_unkept_mountaintops_grants_no_graces():
    slot = _slot(kept=False, attunement=4)
    assert slot[contract.REGION_GRACES] == {}
    assert contract.GRACE_ATTUNEMENT not in slot


@pytest.mark.parametrize("tier", ["entrance", "landmarks"])
def test_exploration_tiers_keep_their_narrower_bundles(tier):
    bundle = _slot(tier)[contract.REGION_GRACES][_LOCK]
    assert bundle
    assert _FOOT not in bundle
    assert _FIRE_GIANT not in bundle
    assert set(bundle) < set(_slot("all")[contract.REGION_GRACES][_LOCK])


def test_attunement_withholds_foot_of_the_forge_until_bloom():
    slot = _slot("all", attunement=4)
    immediate = slot[contract.REGION_GRACES][_LOCK]
    gate = slot[contract.GRACE_ATTUNEMENT][_LOCK]
    assert _FOOT not in immediate
    assert _FOOT in gate["members"]
    assert _FOOT in gate["bloom"]
    assert gate["threshold"] == 4
    assert set(immediate + gate["bloom"]) == set(_slot("all")[contract.REGION_GRACES][_LOCK])
    assert _FIRE_GIANT not in immediate + gate["members"] + gate["bloom"]

