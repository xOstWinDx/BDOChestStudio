"""Regression checks for supplied blacksmith chances and nested openings."""

import random
import unittest

from bdo_sim.catalog import load_catalog
from bdo_sim.content import blacksmith as b
from bdo_sim.domain import Chest
from bdo_sim.engine import Simulation


class FixedRandom:
    def __init__(self, values):
        self.values = iter(values)

    def random(self):
        return next(self.values)


class BlacksmithTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_conditional_probabilities(self):
        expected = {
            b.BlacksmithWorkshopChest: [50, 50],
            b.EliteBlacksmithChest: [50, 50],
            b.SturdyBlacksmithChest: [50, 50],
            b.ExquisiteBlacksmithChest: [50, 50],
            b.BlacksmithAdvice: [15, 15, 15, 55],
            b.ExpertBlacksmithAdvice: [15, 15, 15, 55],
            b.MasterBlacksmithAdvice: [12.5, 12.5, 12.5, 12.5, 50],
            b.GrandmasterBlacksmithAdvice: [12.5, 12.5, 12.5, 12.5, 50],
            b.MasterPremiumEnhancementChest: [.15, .25, 3, 5, 7, 7, 12.6, 15, 15, 15, 20],
            b.GrandmasterPremiumEnhancementChest: [.15, .25, .7, 1, 9, 10, 11, 13, 15, 17, 22.9],
            b.SpecialistPremiumEnhancementChest: [.15, .25, .4, 13.5, 13.5, 13.5, 13.5, 13.5, 13.5, 18.2],
        }
        for chest, chances in expected.items():
            with self.subTest(chest=chest.id):
                self.assertEqual([entry.chance for entry in chest.loot_table()], chances)
                self.assertAlmostEqual(sum(chances), 100)
                # Exercise every interval of the actual weighted sampler.
                lower = 0
                for entry in chest.loot_table():
                    actual = chest().open(FixedRandom([(lower + entry.chance / 2) / 100]))
                    self.assertEqual(actual, (entry.drop(),))
                    lower += entry.chance

    def test_materials_award_every_item_and_queue_advice(self):
        for suffix, cron, advice, seals in (("i", 100, 2, 1), ("ii", 300, 3, 3), ("iii", 500, 5, 4)):
            sim = Simulation(self.catalog, {"blacksmith_materials_chest_" + suffix: 1}, 1)
            sim.rng = FixedRandom([0] * advice)
            first = sim.step()
            self.assertEqual(len(first.drops), 3)
            self.assertEqual(sim.report.pending, advice)
            while sim.report.status == "running":
                sim.step()
            self.assertEqual(dict(sim.report.inventory), {
                "cron_stone": cron, "blacksmith_spirit_seal": seals, "memory_fragment": 5 * advice,
            })

    def test_workshop_can_return_two_workshop_chests(self):
        sim = Simulation(self.catalog, {b.BlacksmithWorkshopChest.id: 1}, 1)
        sim.rng = FixedRandom([0, 0, 0, .75])
        for _ in range(4):
            sim.step()
        self.assertEqual(sim.report.pending, 2)
        self.assertEqual(list(sim.queue), [(b.BlacksmithWorkshopChest.id, 2)])

    def test_workshop_masterpiece_and_premium_upgrade_path(self):
        sim = Simulation(self.catalog, {b.BlacksmithWorkshopChest.id: 1}, 1)
        sim.rng = FixedRandom([0, 0, 0, 0, .99, .205, 0])
        while sim.report.status == "running":
            sim.step()
        self.assertEqual(dict(sim.report.inventory), {"blacksmith_spirit_seal": 5, "full_outfit_box_70": 1})
        for chest in (b.MasterPremiumEnhancementChest, b.GrandmasterPremiumEnhancementChest,
                      b.SpecialistPremiumEnhancementChest):
            self.assertEqual(sim.report.opened[chest.id], 1)

    def test_advice_reaches_specialist_and_awards_all_four_items(self):
        sim = Simulation(self.catalog, {b.BlacksmithAdvice.id: 1}, 1)
        sim.rng = FixedRandom([.99] * 4)
        while sim.report.status == "running":
            sim.step()
        self.assertEqual(sim.report.total_opened, 5)
        self.assertEqual(dict(sim.report.inventory), {
            "memory_fragment": 50, "cron_stone": 50, "sharp_black_crystal_shard": 10, "unstable_dark_hunger": 3,
        })

    def test_every_new_chest_is_available_and_finishes(self):
        for key in vars(b).values():
            if isinstance(key, type) and key.__module__ == b.__name__ and issubclass(key, Chest):
                with self.subTest(chest=key.id):
                    sim = Simulation(self.catalog, {key.id: 100}, 20261015)
                    while sim.report.status == "running":
                        sim.step()
                    self.assertEqual(sim.report.status, "complete")
                    self.assertEqual(sim.report.pending, 0)
                    self.assertTrue(sim.report.inventory)
                    self.assertTrue(key().open(random.Random(1)))
