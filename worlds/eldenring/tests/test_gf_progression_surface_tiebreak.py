"""The bootstrap plan breaks host ties by the seeded shuffle, not by location name.

Ties on tier + competition are the common case (a boss host fits nearly every confined item), so a
`loc.name` tiebreak sent every seed's Great Runes to the alphabetically first hosts on the surface:
on six default seeds they spanned 2.0 regions on average, and seed 4 put all seven in Limgrave.
Player report, 2026-10-12. With the shuffled tiebreak the same seeds average 3.7.
"""
import pytest

WorldTestBase = pytest.importorskip("test.bases").WorldTestBase
pytest.importorskip("worlds.eldenring")

SEEDS = range(6)
MIN_MEAN_REGIONS = 3.0


class GreatRunesSpreadAcrossRegions(WorldTestBase):
    game = "Elden Ring"
    options = {"num_regions": 6, "enable_dlc": True, "progression_bias": 100}

    def test_great_rune_hosts_are_not_clustered_by_name(self):
        spans = []
        for seed in SEEDS:
            self.world_setup(seed)
            hosts = [loc.name for loc in self.multiworld.get_locations(self.player)
                     if loc.item is not None and loc.item.player == self.player
                     and "Great Rune" in loc.item.name]
            self.assertTrue(hosts, "seed %d placed no Great Rune" % seed)
            spans.append(len({name.split(" :: ", 1)[0] for name in hosts}))
        mean = sum(spans) / len(spans)
        self.assertGreaterEqual(
            mean, MIN_MEAN_REGIONS,
            "Great Runes cluster by host name again: regions spanned per seed %s" % spans)
