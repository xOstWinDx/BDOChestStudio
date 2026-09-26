import unittest

from bdo_sim.catalog import load_catalog
from bdo_sim.content.items import CronStone
from bdo_sim.definitions import Loot
from bdo_sim.domain import Drop, WeightedChest
from bdo_sim.outcomes import outcomes, sorted_chests
from bdo_sim.rarity import Rarity


class OutcomeTests(unittest.TestCase):
    def test_rarity_boundaries(self):
        for chance, expected in [
            (100, Rarity.COMMON),
            (35, Rarity.UNCOMMON),
            (15, Rarity.RARE),
            (5, Rarity.EPIC),
            (1, Rarity.LEGENDARY),
            (0.1, Rarity.MYTHIC),
            (0.1001, Rarity.LEGENDARY),
            (1.001, Rarity.EPIC),
        ]:
            self.assertEqual(Loot(CronStone, chance=chance).rarity, expected)

    def test_weighted_chances_normalized_and_quantities_preserved(self):
        chest = WeightedChest(
            "test", "Test", "", drops=(Drop("cron_stone", 50), Drop("cron_stone", 1)), cumulative=(1, 10)
        )
        table = outcomes(chest)
        self.assertEqual([o.chance for o in table], [10, 90])
        self.assertEqual([o.drop.quantity for o in table], [50, 1])
        self.assertEqual(table[0].rarity, Rarity.RARE)
        self.assertEqual(table[1].rarity, Rarity.COMMON)

    def test_chain_chance_includes_reaching_and_stopping(self):
        table = outcomes(load_catalog()["eternal_truth"])
        self.assertAlmostEqual(table[0].chance, 40)
        self.assertAlmostEqual(table[-1].chance, 6.6)
        self.assertAlmostEqual(sum(o.chance for o in table[:-1]), 100)

    def test_sort_handles_cycles_and_keeps_terminal_chests_last(self):
        catalog = load_catalog()
        ordered = sorted_chests(catalog)
        self.assertEqual([c.id for c in ordered[:2]], ["butterfly_chest", "golden_treasure_chest"])
        ids = [c.id for c in ordered]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertLess(ids.index("radiant_dream_chest"), ids.index("limit_break_chest"))
