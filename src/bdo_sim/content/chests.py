"""Concrete chests. Probabilities preserve the original prototype tables."""

from ..definitions import AbstractChest, AbstractBonusChest, AbstractChainChest, Loot, Stage
from . import items


class ButterflyChest(AbstractChest):
    id = "butterfly_chest"
    name = "Сундук грез бабочки"
    name_en = "Butterfly Dream Chest"
    icon = "icons/butterfly_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(RadiantDreamChest, quantity=1, chance=10.0),
            Loot(BrilliantDreamChest, quantity=1, chance=30.0),
            Loot(GlimmeringDreamChest, quantity=1, chance=60.0),
        )


class RadiantDreamChest(AbstractChest):
    id = "radiant_dream_chest"
    name = "Сундук сияющей мечты"
    name_en = "Radiant Dream Chest"
    icon = "icons/radiant_dream_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(LimitBreakChest, quantity=3, chance=0.1),
            Loot(LimitBreakChest, quantity=1, chance=1.0),
            Loot(PremiumEnhancementChest, quantity=1, chance=5.0),
            Loot(items.FullOutfit, quantity=1, chance=10.0),
            Loot(RadiantDreamChest, quantity=2, chance=15.0),
            Loot(SweetEnhancementChest, quantity=1, chance=34.0),
            Loot(RareCronBundle, quantity=1, chance=34.9),
        )


class BrilliantDreamChest(AbstractChest):
    id = "brilliant_dream_chest"
    name = "Сундук яркой мечты"
    name_en = "Brilliant Dream Chest"
    icon = "icons/brilliant_dream_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(LimitBreakChest, quantity=1, chance=0.1),
            Loot(PremiumEnhancementChest, quantity=1, chance=1.0),
            Loot(SweetEnhancementChest, quantity=1, chance=8.0),
            Loot(BrilliantDreamChest, quantity=2, chance=10.0),
            Loot(RareCronBundle, quantity=1, chance=12.0),
            Loot(MysteriousTreasureChest, quantity=1, chance=16.0),
            Loot(RadiantDreamChest, quantity=1, chance=20.0),
            Loot(ValuableCronBundle, quantity=1, chance=32.9),
        )


class GlimmeringDreamChest(AbstractChest):
    id = "glimmering_dream_chest"
    name = "Сундук мерцающей мечты"
    name_en = "Glimmering Dream Chest"
    icon = "icons/glimmering_dream_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(PremiumEnhancementChest, quantity=1, chance=0.1),
            Loot(ValuableCronBundle, quantity=1, chance=4.0),
            Loot(ButterflyChest, quantity=1, chance=14.5),
            Loot(items.UnstableDarkHunger, quantity=5, chance=16.0),
            Loot(BrilliantDreamChest, quantity=1, chance=20.0),
            Loot(items.CronChest100, quantity=1, chance=45.4),
        )


class LimitBreakChest(AbstractChest):
    id = "limit_break_chest"
    name = "Сундук для преодоления предела"
    name_en = "Limit Break Chest"
    icon = "icons/limit_break_chest.webp"
    rarity = "epic"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfit, quantity=50, chance=0.2),
            Loot(items.FullOutfit, quantity=20, chance=0.4),
            Loot(items.CronStone, quantity=10000, chance=2.0),
            Loot(items.FullOutfit, quantity=7, chance=5.0),
            Loot(items.CronStone, quantity=5500, chance=7.0),
            Loot(items.FullOutfit, quantity=5, chance=10.0),
            Loot(items.CronStone, quantity=4500, chance=11.0),
            Loot(items.FullOutfit, quantity=3, chance=13.0),
            Loot(items.CronStone, quantity=3500, chance=13.0),
            Loot(items.FullOutfit, quantity=4, chance=38.4),
        )


class PremiumEnhancementChest(AbstractChest):
    id = "premium_enhancement_chest"
    name = "Комплексный премиум-сундук усиления"
    name_en = "Comprehensive Premium Enhancement Chest"
    icon = "icons/premium_enhancement_chest.webp"
    rarity = "common"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfit, quantity=50, chance=0.12),
            Loot(items.FullOutfit, quantity=20, chance=0.25),
            Loot(items.FullOutfit, quantity=10, chance=1.0),
            Loot(items.UnstableDarkHunger, quantity=70, chance=2.0),
            Loot(items.FullOutfit, quantity=5, chance=3.0),
            Loot(items.UnstableDarkHunger, quantity=40, chance=6.0),
            Loot(items.UnstableDarkHunger, quantity=30, chance=8.0),
            Loot(items.CronStone, quantity=1500, chance=15.0),
            Loot(items.FullOutfit, quantity=3, chance=19.0),
            Loot(items.FullOutfit, quantity=2, chance=45.63),
        )


class SweetEnhancementChest(AbstractChest):
    id = "sweet_enhancement_chest"
    name = "Сладкий премиум-сундук усиления"
    name_en = "Sweet Premium Enhancement Chest"
    icon = "icons/sweet_enhancement_chest.webp"
    rarity = "common"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.FullOutfit, quantity=30, chance=0.1),
            Loot(items.FullOutfit, quantity=10, chance=0.2),
            Loot(items.UnstableDarkHunger, quantity=30, chance=2.0),
            Loot(items.AdviceOfValks200, quantity=1, chance=5.0),
            Loot(items.FullOutfit, quantity=2, chance=12.0),
            Loot(items.AdviceOfValks170, quantity=1, chance=12.0),
            Loot(items.FullOutfit, quantity=1, chance=33.7),
            Loot(items.CronStone, quantity=500, chance=35.0),
        )


class RareCronBundle(AbstractChest):
    id = "rare_cron_bundle"
    name = "Редкий сверток с Камнями Крон"
    name_en = "Rare Cron Stone Bundle"
    icon = "icons/rare_cron_bundle.webp"
    rarity = "uncommon"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.CronBundle5000, quantity=1, chance=0.05),
            Loot(items.CronBundle2000, quantity=1, chance=0.25),
            Loot(items.CronBundle1000, quantity=1, chance=0.5),
            Loot(items.CronStone500, quantity=1, chance=3.0),
            Loot(items.CronStone400, quantity=1, chance=10.0),
            Loot(RareCronBundle, quantity=2, chance=20.0),
            Loot(items.CronStone200, quantity=1, chance=17.0),
            Loot(items.CronStone250, quantity=1, chance=18.0),
            Loot(items.CronStone300, quantity=1, chance=31.2),
        )


class MysteriousTreasureChest(AbstractChest):
    id = "mysterious_treasure_chest"
    name = "Сундук таинственных сокровищ"
    name_en = "Mysterious Treasure Chest"
    icon = "icons/mysterious_treasure_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.CronBundle2000, quantity=1, chance=0.5),
            Loot(items.CronBundle1000, quantity=1, chance=1.5),
            Loot(items.UnstableDarkHunger, quantity=20, chance=2.5),
            Loot(items.AdviceOfValks150, quantity=1, chance=2.5),
            Loot(items.ArtisansMemory, quantity=30, chance=13.0),
            Loot(MysteriousTreasureChest, quantity=2, chance=15.0),
            Loot(items.CronStone, quantity=400, chance=20.0),
            Loot(items.CronStone, quantity=250, chance=45.0),
        )


class ValuableCronBundle(AbstractChest):
    id = "valuable_cron_bundle"
    name = "Ценный сверток с Камнями Крон"
    name_en = "Valuable Cron Stone Bundle"
    icon = "icons/valuable_cron_bundle.webp"
    rarity = "uncommon"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.CronBundle2000, quantity=1, chance=0.25),
            Loot(items.CronBundle1000, quantity=1, chance=0.5),
            Loot(items.CronStone500, quantity=1, chance=1.0),
            Loot(items.CronStone400, quantity=1, chance=2.0),
            Loot(items.CronStone300, quantity=1, chance=4.0),
            Loot(ValuableCronBundle, quantity=2, chance=8.0),
            Loot(items.CronStone250, quantity=1, chance=12.0),
            Loot(items.CronStone200, quantity=1, chance=25.0),
            Loot(items.CronStone150, quantity=1, chance=20.25),
            Loot(items.CronStone100, quantity=1, chance=15.0),
            Loot(ValuableCronBundle, quantity=1, chance=12.0),
        )


class GoldenTreasureChest(AbstractChest):
    id = "golden_treasure_chest"
    name = "Сундук с золотыми сокровищами"
    name_en = "Golden Treasure Chest"
    icon = "icons/golden_treasure_chest.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(ShiningTreasureChest, quantity=1, chance=1.0),
            Loot(GoldenTreasureBundle, quantity=1, chance=49.0),
            Loot(SilverTreasureBundle, quantity=1, chance=50.0),
        )


class ShiningTreasureChest(AbstractChest):
    id = "shining_treasure_chest"
    name = "Сверкающий ларец с сокровищами"
    name_en = "Shining Treasure Box"
    icon = "icons/shining_treasure_chest.webp"
    rarity = "epic"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(LimitBreakChest, quantity=10, chance=0.1),
            Loot(PremiumEnhancementChest, quantity=20, chance=0.2),
            Loot(PremiumEnhancementChest, quantity=5, chance=5.0),
            Loot(LimitBreakChest, quantity=2, chance=9.0),
            Loot(items.OutfitSelectionBox, quantity=6, chance=13.0),
            Loot(LimitBreakChest, quantity=1, chance=17.0),
            Loot(items.OutfitSelectionBox, quantity=5, chance=21.0),
            Loot(items.OutfitSelectionBox, quantity=4, chance=34.7),
        )


class GoldenTreasureBundle(AbstractBonusChest):
    id = "golden_treasure_bundle"
    name = "Золотой сверток с сокровищами"
    name_en = "Golden Treasure Bundle"
    icon = "icons/golden_treasure_bundle.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(ValuableScrollChest, quantity=1),
            Loot(ValuableCronBundle, quantity=1),
        )

    @classmethod
    def bonus_loot(cls):
        return (
            Loot(items.OutfitSelectionBox, quantity=50, chance=0.01),
            Loot(items.OutfitSelectionBox, quantity=30, chance=0.02),
            Loot(items.OutfitSelectionBox, quantity=5, chance=0.25),
            Loot(ShiningTreasureChest, quantity=1, chance=0.5),
            Loot(items.AdviceOfValks250, quantity=1, chance=2.0),
            Loot(items.AdviceOfValks200, quantity=1, chance=5.0),
            Loot(items.UnstableDarkHunger, quantity=5, chance=10.0),
            Loot(items.AdviceOfValks150, quantity=1, chance=10.0),
            Loot(items.SupportBoxV, quantity=1, chance=15.0),
            Loot(items.SupportBoxIV, quantity=1, chance=20.0),
            Loot(items.UnstableDarkHunger, quantity=3, chance=25.0),
            Loot(GoldenTreasureChest, quantity=1, chance=27.0),
            Loot(MysteriousTreasureChest, quantity=1, chance=35.0),
            Loot(SweetEnhancementChest, quantity=1, chance=50.0),
            Loot(items.ArtisansMemory, quantity=3, chance=50.0),
            Loot(EternalTruth, quantity=1, chance=50.0),
            Loot(CautionaryAdvice, quantity=1, chance=70.0),
        )


class SilverTreasureBundle(AbstractBonusChest):
    id = "silver_treasure_bundle"
    name = "Серебряный сверток с сокровищами"
    name_en = "Silver Treasure Bundle"
    icon = "icons/silver_treasure_bundle.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def guaranteed_loot(cls):
        return (
            Loot(ValuableScrollChest, quantity=1),
            Loot(items.CronChest200, quantity=1),
        )

    @classmethod
    def bonus_loot(cls):
        return (
            Loot(items.OutfitSelectionBox, quantity=30, chance=0.01),
            Loot(items.OutfitSelectionBox, quantity=15, chance=0.02),
            Loot(items.OutfitSelectionBox, quantity=4, chance=0.1),
            Loot(items.AdviceOfValks200, quantity=1, chance=2.0),
            Loot(items.AdviceOfValks170, quantity=1, chance=5.0),
            Loot(items.UnstableDarkHunger, quantity=3, chance=5.0),
            Loot(items.SupportBoxV, quantity=1, chance=10.0),
            Loot(items.AdviceOfValks130, quantity=1, chance=10.0),
            Loot(GoldenTreasureBundle, quantity=1, chance=10.0),
            Loot(items.UnstableDarkHunger, quantity=2, chance=15.0),
            Loot(GoldenTreasureChest, quantity=1, chance=15.0),
            Loot(items.SupportBoxIV, quantity=1, chance=20.0),
            Loot(MysteriousCronBundle, quantity=1, chance=37.5),
            Loot(MysteriousTreasureChest, quantity=1, chance=37.5),
            Loot(items.ArtisansMemory, quantity=3, chance=50.0),
            Loot(EternalTruth, quantity=1, chance=50.0),
            Loot(CautionaryAdvice, quantity=1, chance=70.0),
        )


class ValuableScrollChest(AbstractChest):
    id = "valuable_scroll_chest"
    name = "Сундук ценных свитков"
    name_en = "Valuable Scroll Chest"
    icon = "icons/valuable_scroll_chest.webp"
    rarity = "common"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.OldMoonSpecialSpell, quantity=1, chance=5.0),
            Loot(items.OldMoonFortune, quantity=1, chance=10.0),
            Loot(items.ItemCollectionScroll, quantity=2, chance=28.0),
            Loot(items.GiovanGrolinScroll, quantity=1, chance=28.0),
            Loot(items.CombatSkillExpScroll, quantity=1, chance=29.0),
        )


class EternalTruth(AbstractChainChest):
    id = "eternal_truth"
    name = "[Ивент] Вечная истина"
    name_en = "[Event] Eternal Truth"
    icon = "icons/eternal_truth.webp"
    rarity = "legendary"
    crown_value = None
    start = "s0"

    @classmethod
    def chain_stages(cls):
        return {
            "s0": Stage(chance=60.0, next_stage="s1", rewards=(Loot(items.CaphrasStone2, quantity=1),)),
            "s1": Stage(chance=55.0, next_stage="s2", rewards=(Loot(items.CaphrasStone4, quantity=1),)),
            "s2": Stage(chance=50.0, next_stage="s3", rewards=(Loot(items.CaphrasStone6, quantity=1),)),
            "s3": Stage(chance=40.0, next_stage="final", rewards=(Loot(items.CaphrasStone8, quantity=1),)),
            "final": Stage(
                chance=0.0,
                next_stage=None,
                rewards=(
                    Loot(items.CaphrasStone10, quantity=1),
                    Loot(items.TokenOfFate, quantity=1),
                ),
            ),
        }


class CautionaryAdvice(AbstractChainChest):
    id = "cautionary_advice"
    name = "[Ивент] Предостерегающий совет"
    name_en = "[Event] Cautionary Advice"
    icon = "icons/cautionary_advice.webp"
    rarity = "rare"
    crown_value = None
    start = "s0"

    @classmethod
    def chain_stages(cls):
        return {
            "s0": Stage(chance=50.0, next_stage="s1", rewards=(Loot(items.CronStone3, quantity=1),)),
            "s1": Stage(chance=45.0, next_stage="s2", rewards=(Loot(items.CronStone6, quantity=1),)),
            "s2": Stage(chance=40.0, next_stage="s3", rewards=(Loot(items.CronStone9, quantity=1),)),
            "s3": Stage(chance=35.0, next_stage="final", rewards=(Loot(items.CronStone12, quantity=1),)),
            "final": Stage(
                chance=0.0,
                next_stage=None,
                rewards=(
                    Loot(items.CronStone15, quantity=1),
                    Loot(items.TokenOfFate, quantity=1),
                ),
            ),
        }


class MysteriousCronBundle(AbstractChest):
    id = "mysterious_cron_bundle"
    name = "Таинственный сверток с Камнями Крон"
    name_en = "Mysterious Cron Stone Bundle"
    icon = "icons/mysterious_cron_bundle.webp"
    rarity = "chest"
    crown_value = None

    @classmethod
    def loot_table(cls):
        return (
            Loot(items.CronBundle2000, quantity=1, chance=0.25),
            Loot(items.CronBundle1000, quantity=1, chance=0.5),
            Loot(items.CronStone500, quantity=1, chance=1.0),
            Loot(items.CronStone300, quantity=1, chance=1.25),
            Loot(items.CronStone200, quantity=1, chance=5.0),
            Loot(items.CronStone150, quantity=1, chance=15.0),
            Loot(items.CronStone100, quantity=1, chance=25.0),
            Loot(items.CronStone75, quantity=1, chance=28.0),
            Loot(items.CronStone50, quantity=1, chance=24.0),
        )
