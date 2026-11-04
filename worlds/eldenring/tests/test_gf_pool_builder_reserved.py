"""Regression: pool_builder must reserve ALL non-juice pool contributors, not just region Locks.

pool_builder sizes its juice to the "true remaining Rune tail" = Rune-fallback checks minus the slots
the OTHER pool contributors already consume. That reserve used to be just len(kept) (one Lock per kept
region), so progressive copies (and, until their deletion on 2026-10-06, Boss Keys) went uncounted ->
juice over-provisioned and the over-provision trim dropped REAL vanilla gear past the Rune tail (count
stayed exact via range(slots), so it was a silent precision bug, not a crash). core.create_items now
runs pool_builder LAST and records the exact consumed-slot count on the world.

The collision case this file drove (boss_keys ON + juice_pct 100) went with the Boss Keys feature.
"""
import pytest

WorldTestBase = pytest.importorskip("test.bases").WorldTestBase
pytest.importorskip("worlds.eldenring")

from worlds.eldenring.tables.data import LOCATIONS, HUB  # noqa: E402
from ._util import world_items, world_pool_items  # noqa: E402
from worlds.eldenring.features.pool_builder import PoolBuilderFeature  # noqa: E402

GAME = "Elden Ring"


