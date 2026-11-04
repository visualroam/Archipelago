"""auto_upgrade option -> slot_data['options']['auto_upgrade'] echo (WorldTestBase)."""
import pytest
WorldTestBase = pytest.importorskip("test.bases").WorldTestBase
pytest.importorskip("worlds.eldenring")
from worlds.eldenring import contract  # noqa: E402
GAME = "Elden Ring"

class AutoUpgradeOn(WorldTestBase):
    game = GAME
    options = {"num_regions": 0, "auto_upgrade": True}
    def test_echo_on(self):
        sd = self.world.fill_slot_data()
        assert sd["options"]["auto_upgrade"] == 1, sd["options"]["auto_upgrade"]
        assert isinstance(sd["options"]["auto_upgrade"], int)
        contract.validate_slot_data(sd, strict=True)


class StoneUpgradeOn(WorldTestBase):
    game = GAME
    options = {"num_regions": 0, "auto_upgrade": False,
               "auto_upgrade_from_stones": True}

    def test_stone_history_option_and_feature_tag(self):
        sd = self.world.fill_slot_data()
        assert sd["options"]["auto_upgrade"] == 0
        assert sd["options"]["auto_upgrade_from_stones"] == 1
        assert "stone_auto_upgrade" in sd["requiresClientFeatures"]
        contract.validate_slot_data(sd, strict=True)


class StoneUpgradeOff(WorldTestBase):
    game = GAME
    options = {"num_regions": 0, "auto_upgrade_from_stones": False}

    def test_old_seed_contract_is_unchanged(self):
        sd = self.world.fill_slot_data()
        assert "auto_upgrade_from_stones" not in sd["options"]
        assert "stone_auto_upgrade" not in sd.get("requiresClientFeatures", [])
