"""Blacksmith workshop tables supplied for the October 2026 content update.

Chances are conditional per opening, not the rounded aggregate chances.
Selection boxes remain terminal rewards: no selection contents were supplied.
"""

from ..definitions import AbstractChest, AbstractBonusChest, Loot
from . import items


class BlacksmithWorkshopChest(AbstractChest):
    id = "blacksmith_workshop_chest"
    name = "Сундук мастерской кузнеца"
    name_en = "Blacksmith Workshop Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(EliteBlacksmithChest, quantity=1, chance=50),
            Loot(BlacksmithMaterialsChestI, quantity=1, chance=50),
        )


class EliteBlacksmithChest(AbstractChest):
    id = "elite_blacksmith_chest"
    name = "Элитный сундук кузнеца"
    name_en = "Elite Blacksmith Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(SturdyBlacksmithChest, quantity=1, chance=50),
            Loot(BlacksmithMaterialsChestII, quantity=1, chance=50),
        )


class SturdyBlacksmithChest(AbstractChest):
    id = "sturdy_blacksmith_chest"
    name = "Прочный сундук кузнеца"
    name_en = "Sturdy Blacksmith Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(ExquisiteBlacksmithChest, quantity=1, chance=50),
            Loot(BlacksmithMaterialsChestIII, quantity=1, chance=50),
        )


class ExquisiteBlacksmithChest(AbstractChest):
    id = "exquisite_blacksmith_chest"
    name = "Изысканный сундук кузнеца"
    name_en = "Exquisite Blacksmith Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(BlacksmithMasterpieceChest, quantity=1, chance=50),
            Loot(BlacksmithWorkshopChest, quantity=2, chance=50),
        )


class BlacksmithMasterpieceChest(AbstractBonusChest):
    id = "blacksmith_masterpiece_chest"
    name = "Сундук шедевров кузнеца"
    name_en = "Blacksmith Masterpiece Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(MasterPremiumEnhancementChest, quantity=1),
            Loot(items.BlacksmithSpiritSeal, quantity=5),
        )

    @classmethod
    def bonus_loot(cls):
        return ()


class BlacksmithMaterialsChestI(AbstractBonusChest):
    id = "blacksmith_materials_chest_i"
    name = "Сундук материалов кузнеца I"
    name_en = "Blacksmith Materials Chest I"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(items.CronStone, quantity=100),
            Loot(BlacksmithAdvice, quantity=2),
            Loot(items.BlacksmithSpiritSeal, quantity=1),
        )

    @classmethod
    def bonus_loot(cls):
        return ()


class BlacksmithMaterialsChestII(AbstractBonusChest):
    id = "blacksmith_materials_chest_ii"
    name = "Сундук материалов кузнеца II"
    name_en = "Blacksmith Materials Chest II"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(items.CronStone, quantity=300),
            Loot(BlacksmithAdvice, quantity=3),
            Loot(items.BlacksmithSpiritSeal, quantity=3),
        )

    @classmethod
    def bonus_loot(cls):
        return ()


class BlacksmithMaterialsChestIII(AbstractBonusChest):
    id = "blacksmith_materials_chest_iii"
    name = "Сундук материалов кузнеца III"
    name_en = "Blacksmith Materials Chest III"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(items.CronStone, quantity=500),
            Loot(BlacksmithAdvice, quantity=5),
            Loot(items.BlacksmithSpiritSeal, quantity=4),
        )

    @classmethod
    def bonus_loot(cls):
        return ()


class BlacksmithAdvice(AbstractChest):
    id = "blacksmith_advice"
    name = "Совет кузнеца"
    name_en = "Blacksmith Advice"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.MemoryFragment, quantity=5, chance=15),
            Loot(items.CronStone, quantity=5, chance=15),
            Loot(items.SharpBlackCrystalShard, quantity=2, chance=15),
            Loot(ExpertBlacksmithAdvice, quantity=1, chance=55),
        )


class ExpertBlacksmithAdvice(AbstractChest):
    id = "expert_blacksmith_advice"
    name = "Совет кузнеца-эксперта"
    name_en = "Expert Blacksmith Advice"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.MemoryFragment, quantity=10, chance=15),
            Loot(items.CronStone, quantity=10, chance=15),
            Loot(items.SharpBlackCrystalShard, quantity=4, chance=15),
            Loot(MasterBlacksmithAdvice, quantity=1, chance=55),
        )


class MasterBlacksmithAdvice(AbstractChest):
    id = "master_blacksmith_advice"
    name = "Совет кузнеца-мастера"
    name_en = "Master Blacksmith Advice"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.MemoryFragment, quantity=20, chance=12.5),
            Loot(items.CronStone, quantity=20, chance=12.5),
            Loot(items.SharpBlackCrystalShard, quantity=6, chance=12.5),
            Loot(items.UnstableDarkHunger, quantity=1, chance=12.5),
            Loot(GrandmasterBlacksmithAdvice, quantity=1, chance=50),
        )


class GrandmasterBlacksmithAdvice(AbstractChest):
    id = "grandmaster_blacksmith_advice"
    name = "Совет кузнеца-грандмастера"
    name_en = "Grandmaster Blacksmith Advice"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.MemoryFragment, quantity=20, chance=12.5),
            Loot(items.CronStone, quantity=20, chance=12.5),
            Loot(items.SharpBlackCrystalShard, quantity=6, chance=12.5),
            Loot(items.UnstableDarkHunger, quantity=2, chance=12.5),
            Loot(SpecialistBlacksmithAdvice, quantity=1, chance=50),
        )


class SpecialistBlacksmithAdvice(AbstractBonusChest):
    id = "specialist_blacksmith_advice"
    name = "Совет кузнеца-специалиста"
    name_en = "Specialist Blacksmith Advice"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(items.MemoryFragment, quantity=50),
            Loot(items.CronStone, quantity=50),
            Loot(items.SharpBlackCrystalShard, quantity=10),
            Loot(items.UnstableDarkHunger, quantity=3),
        )

    @classmethod
    def bonus_loot(cls):
        return ()


class SpecialistPremiumEnhancementChest(AbstractChest):
    id = "specialist_premium_enhancement_chest"
    name = "Премиум-сундук усиления специалиста"
    name_en = "Specialist Premium Enhancement Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfitBox70, quantity=1, chance=0.15),
            Loot(items.FullOutfitBox30, quantity=1, chance=0.25),
            Loot(items.FullOutfitBox15, quantity=1, chance=0.4),
            Loot(items.FullOutfitBox7, quantity=1, chance=13.5),
            Loot(items.CronStone6500, quantity=1, chance=13.5),
            Loot(items.FullOutfit, quantity=6, chance=13.5),
            Loot(items.CronStone5500, quantity=1, chance=13.5),
            Loot(items.FullOutfit, quantity=5, chance=13.5),
            Loot(items.CronBundle4500, quantity=1, chance=13.5),
            Loot(items.FullOutfit, quantity=4, chance=18.2),
        )


class GrandmasterPremiumEnhancementChest(AbstractChest):
    id = "grandmaster_premium_enhancement_chest"
    name = "Премиум-сундук усиления грандмастера"
    name_en = "Grandmaster Premium Enhancement Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfitBox40, quantity=1, chance=0.15),
            Loot(items.FullOutfitBox20, quantity=1, chance=0.25),
            Loot(items.FullOutfitBox10, quantity=1, chance=0.7),
            Loot(items.FullOutfitBox7, quantity=1, chance=1),
            Loot(items.CronBundle4500, quantity=1, chance=9),
            Loot(SpecialistPremiumEnhancementChest, quantity=1, chance=10),
            Loot(items.FullOutfit, quantity=4, chance=11),
            Loot(items.CronBundle3500, quantity=1, chance=13),
            Loot(items.FullOutfit, quantity=3, chance=15),
            Loot(items.CronBundle2500, quantity=1, chance=17),
            Loot(items.FullOutfit, quantity=2, chance=22.9),
        )


class MasterPremiumEnhancementChest(AbstractChest):
    id = "master_premium_enhancement_chest"
    name = "Премиум-сундук усиления мастера"
    name_en = "Master Premium Enhancement Chest"
    icon = "icons/chest.svg"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfitBox20, quantity=1, chance=0.15),
            Loot(items.FullOutfitBox10, quantity=1, chance=0.25),
            Loot(items.UnstableDarkHunger, quantity=50, chance=3),
            Loot(items.ValksAdvice200Chest, quantity=1, chance=5),
            Loot(items.CronBundle2500, quantity=1, chance=7),
            Loot(items.UnstableDarkHunger, quantity=20, chance=7),
            Loot(items.EnhancementSupportSelectionChest, quantity=1, chance=12.6),
            Loot(items.FullOutfit, quantity=2, chance=15),
            Loot(items.CronBundle1500, quantity=1, chance=15),
            Loot(items.FullOutfit, quantity=1, chance=15),
            Loot(GrandmasterPremiumEnhancementChest, quantity=1, chance=20),
        )
