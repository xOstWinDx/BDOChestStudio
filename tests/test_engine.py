import json
import random
import tempfile
import unittest
from pathlib import Path

from bdo_sim.catalog import load_catalog
from bdo_sim.domain import BonusChest, ChainChest, ChainStage, Chest, Drop, WeightedChest
from bdo_sim.engine import Simulation
from bdo_sim.storage import History


def run(sim):
    while sim.report.status == "running":
        sim.step()
    return sim.report


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_catalog_matches_frozen_legacy_results(self):
        fixture = Path(__file__).parent / "fixtures" / "legacy_results.json"
        for expected in json.loads(fixture.read_text(encoding="utf-8")):
            key, seed = expected["chest_id"], expected["seed"]
            with self.subTest(chest=key, seed=seed):
                report = run(Simulation(self.catalog, {key: expected["quantity"]}, seed))
                self.assertEqual(dict(report.inventory), expected["inventory"])
                self.assertEqual(report.total_opened, expected["total_opened"])
                self.assertEqual(report.crowns(self.catalog), expected["crowns"])

    def test_recursive_limit_preserves_pending(self):
        chest = WeightedChest("c", "c", "", drops=(Drop("c", 2),), cumulative=(100,))
        report = run(Simulation({"c": chest}, {"c": 1}, 0, limit=50))
        self.assertEqual((report.status, report.total_opened, report.pending), ("limited", 50, 51))

    def test_valks_are_terminal_items_without_queue_steps(self):
        self.assertEqual(sum(isinstance(item, Chest) for item in self.catalog.values()), 18)
        gold = next(item for item in self.catalog.values() if item.name == "Золотой сверток с сокровищами")

        class AlwaysDrop:
            def random(self):
                return 0

        sim = Simulation(self.catalog, {gold.id: 1}, 1)
        sim.rng = AlwaysDrop()
        opening = sim.step()
        advice = [d for d in opening.drops if "Совет Валкса" in self.catalog[d.item_id].name]
        self.assertEqual(len(advice), 3)
        for drop in advice:
            self.assertNotIsInstance(self.catalog[drop.item_id], Chest)
            self.assertEqual(sim.report.inventory[drop.item_id], drop.quantity)
        self.assertEqual(sim.report.total_opened, 1)

    def test_concrete_chests_and_typed_nested_rewards(self):
        from bdo_sim.content.chests import ButterflyChest, RadiantDreamChest

        self.assertIsInstance(self.catalog[ButterflyChest.id], ButterflyChest)
        self.assertIs(ButterflyChest.loot_table()[0].item, RadiantDreamChest)
        self.assertEqual(len({type(item) for item in self.catalog.values()}), 60)

    def test_bonus_rewards_are_independent(self):
        chest = BonusChest(
            "c",
            "c",
            "",
            guaranteed=(Drop("a", 1),),
            extras=((Drop("a", 2), 100), (Drop("a", 4), 100), (Drop("a", 8), 0)),
        )
        self.assertEqual(sum(d.quantity for d in chest.open(random.Random(2))), 7)

    def test_chain_stops_or_advances(self):
        end = ChainStage(0, None, (Drop("b", 1),))
        for chance, expected in ((0, "a"), (100, "b")):
            chest = ChainChest("c", "c", "", stages=(("s0", ChainStage(chance, "end", (Drop("a", 1),))), ("end", end)))
            self.assertEqual(chest.open(random.Random(1))[0].item_id, expected)

    def test_cancel_and_invalid_baskets(self):
        key = next(k for k, v in self.catalog.items() if isinstance(v, Chest))
        for basket in ({}, {key: 0}, {key: -1}, {key: 1.5}, {key: True}, {"missing": 1}):
            with self.assertRaises(ValueError):
                Simulation(self.catalog, basket, 1)
        sim = Simulation(self.catalog, {key: 10}, 1)
        sim.step()
        sim.cancel()
        before = sim.report.total_opened
        self.assertIsNone(sim.step())
        self.assertEqual(sim.report.total_opened, before)
        self.assertEqual(sim.report.status, "cancelled")

    def test_history_survives_reopen(self):
        key = next(k for k, v in self.catalog.items() if isinstance(v, Chest))
        report = run(Simulation(self.catalog, {key: 5}, 2))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "history.sqlite3"
            History(path).save(report)
            count, inventory, opened = History(path).totals()
            self.assertEqual(count, 1)
            self.assertEqual(inventory, report.inventory)
            self.assertEqual(opened, report.opened)


if __name__ == "__main__":
    unittest.main()
