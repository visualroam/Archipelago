"""Ability Unlocks are confined to the progression surface (colombius, 2026-10-06).

A Boss-only surface put Unlock: Roll and Unlock: L1 in merchant slots, because the surface exempted
every `Unlock:` item and left it to the general fill. Now they are confined like any other restricted
item. Early-declared ones (Roll) go on a surface host reachable from the start.
"""
import pytest

WorldTestBase = pytest.importorskip("test.bases").WorldTestBase
pytest.importorskip("worlds.eldenring")

from worlds.eldenring.features import progression_surface as surface  # noqa: E402

GAME = "Elden Ring"


class BossSurfaceConfinesUnlocks(WorldTestBase):
    """colombius's shape: shops are checks, the surface is bosses, seven abilities locked."""
    game = GAME
    options = {
        "num_regions": 0,
        "enable_dlc": True,
        "shop_checks": True,
        "progression_surface": {"Boss", "MajorBoss"},
        "locked_abilities": {"crouch", "heal", "jump", "l1", "l2", "r2", "roll"},
        "ability_lock_mode": "progressive",
        "ability_unlocks_required": True,
    }

    def _unlock_locations(self):
        return {loc.item.name: loc for loc in self.multiworld.get_locations(self.player)
                if loc.item is not None and loc.item.player == self.player
                and loc.item.name.startswith("Unlock: ")}

    def test_every_unlock_lands_on_the_surface(self):
        allowed = surface.surface_ap_ids(self.world, ["Boss", "MajorBoss"])
        confined = self._unlock_locations()
        self.assertEqual(len(confined), 7, sorted(confined))
        off = {name: loc.name for name, loc in confined.items() if loc.address not in allowed}
        self.assertFalse(off, "Unlocks placed off the progression surface: %s" % off)

    def test_the_selected_surface_is_used_before_the_ladder_widens(self):
        """~166 boss hosts against ~50 confined items: nothing needs a wider rung. Before the tiered
        order the bootstrap plan ignored the selection and put 36 of 43 items off it."""
        allowed = surface.surface_ap_ids(self.world, ["Boss", "MajorBoss"])
        confined = [loc for loc in self.multiworld.get_locations(self.player)
                    if loc.item is not None and loc.item.player == self.player
                    and surface.is_restricted_progression(loc.item, self.player)]
        # WITNESS: Locks + Great Runes + seven Unlocks were placed, so an empty `off` is the
        # surface holding, not a filter that matched nothing (test_gf_vacuous_pass).
        self.assertGreater(len(confined), 40)
        off = [(loc.item.name, loc.name) for loc in confined if loc.address not in allowed]
        self.assertFalse(off, "%d confined item(s) off the selected surface: %s" % (len(off), off[:8]))

    def test_roll_is_on_a_start_reachable_surface_host(self):
        """Alaric, 2026-10-06: early AND on the surface. Placed in pre_fill, so its early_items
        declaration is withdrawn and AP's early fill has nothing left to scatter."""
        self.assertIn("Unlock: Roll", self.world.gf_prog_surface_early)
        self.assertNotIn("Unlock: Roll", self.multiworld.early_items[self.player])
        host = self._unlock_locations()["Unlock: Roll"]
        self.assertIn(host.address, surface.surface_ap_ids(self.world, ["Boss", "MajorBoss"]),
                      host.name)
        start = self.multiworld.state.copy()
        start.sweep_for_advancements(
            locations=[loc for loc in self.multiworld.get_filled_locations() if loc.address is None])
        self.assertTrue(host.can_reach(start), "%s is not reachable from the start" % host.name)
