import random
import unittest

from bdo_sim.catalog import load_catalog
from bdo_sim.content.items import CronStone
from bdo_sim.definitions import ENTITY_TYPES, AbstractChest, AbstractChainChest, Loot, Stage


class DefinitionTests(unittest.TestCase):
    def setUp(self):
        saved = dict(ENTITY_TYPES)

        def restore():
            ENTITY_TYPES.clear()
            ENTITY_TYPES.update(saved)

        self.addCleanup(restore)

    def test_new_subclass_automatically_enters_catalog(self):
        class ExampleChest(AbstractChest):
            id = "test_example"
            name = "Пример"
            name_en = "Example"
            icon = "icons/chest.svg"

            @classmethod
            def loot_table(cls):
                return (Loot(CronStone, quantity=7),)

        chest = load_catalog()[ExampleChest.id]
        self.assertIsInstance(chest, ExampleChest)
        self.assertEqual(chest.open(random.Random(1))[0].quantity, 7)
        with self.assertRaisesRegex(ValueError, "Duplicate"):

            class Duplicate(ExampleChest):
                id = ExampleChest.id

    def test_invalid_loot_rejected(self):
        for qty in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                Loot(CronStone, quantity=qty)
        for chance in (-1, 101, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                Loot(CronStone, chance=chance)
        with self.assertRaises(ValueError):
            Loot("item:unknown")

    def test_invalid_chain_rejected(self):
        class CyclicChest(AbstractChainChest):
            id = "test_cycle"
            name = "Цикл"
            name_en = "Cycle"
            icon = "icons/chest.svg"

            @classmethod
            def chain_stages(cls):
                return {"s0": Stage(100, "s0", (Loot(CronStone),))}

        with self.assertRaisesRegex(ValueError, "Cycle"):
            load_catalog()

    def test_empty_table_and_missing_icon_rejected(self):
        class EmptyChest(AbstractChest):
            id = "test_empty"
            name = "Пустой"
            name_en = "Empty"
            icon = "icons/chest.svg"

            @classmethod
            def loot_table(cls):
                return ()

        with self.assertRaisesRegex(ValueError, "empty loot"):
            load_catalog()
        del ENTITY_TYPES[EmptyChest.id]

        class MissingIcon(EmptyChest):
            id = "test_icon"
            icon = "icons/missing.png"

            @classmethod
            def loot_table(cls):
                return (Loot(CronStone),)

        with self.assertRaisesRegex(ValueError, "Нет иконки"):
            load_catalog()

    def test_non_english_or_malformed_id_rejected(self):
        for key in ("сундук", "chest:example", "UpperCase", "bad__id", "bad-id", ""):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "snake_case"):
                type("BadId", (AbstractChest,), {"id": key})

    def test_all_entities_use_unique_english_ids(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog), 60)
        for key in catalog:
            self.assertRegex(key, r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
