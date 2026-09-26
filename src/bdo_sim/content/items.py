"""Final inventory items. Values are per unit; None means unknown."""

from ..definitions import AbstractItem

FULL_OUTFIT_ICON = "icons/full_outfit.webp"
CRON_CHEST_ICON = "icons/cron_chest.webp"
CRON_BUNDLE_ICON = "icons/cron_bundle.webp"
CRON_STONE_ICON = "icons/cron_stone.webp"
CAPHRAS_STONE_ICON = "icons/caphras_stone.webp"


class FullOutfit(AbstractItem):
    id = "full_outfit"
    name = "[Ивент] Сундук с полным комплектом"
    name_en = "[Event] Full Outfit Box"
    icon = FULL_OUTFIT_ICON
    rarity = "epic"
    crown_value = 993


class UnstableDarkHunger(AbstractItem):
    id = "unstable_dark_hunger"
    name = "[Ивент] Нестабильный источник темного насыщения"
    name_en = "[Event] Unstable Dark Hunger's Origin"
    icon = "icons/unstable_dark_hunger.webp"
    rarity = "rare"
    crown_value = None


class CronChest100(AbstractItem):
    id = "cron_chest_100"
    name = "Сундук с Камнями Крон (100 шт.)"
    name_en = "Cron Stone Chest (100 pcs)"
    icon = CRON_CHEST_ICON
    rarity = "common"
    crown_value = 100


class CronBundle5000(AbstractItem):
    id = "cron_bundle_5000"
    name = "Сверток с Камнями Крон (5000 шт.)"
    name_en = "Cron Stone Bundle (5,000 pcs)"
    icon = CRON_BUNDLE_ICON
    rarity = "epic"
    crown_value = 5000


class CronBundle2000(AbstractItem):
    id = "cron_bundle_2000"
    name = "Сверток с Камнями Крон (2000 шт.)"
    name_en = "Cron Stone Bundle (2,000 pcs)"
    icon = CRON_BUNDLE_ICON
    rarity = "epic"
    crown_value = 2000


class CronBundle1000(AbstractItem):
    id = "cron_bundle_1000"
    name = "Сверток с Камнями Крон (1000 шт.)"
    name_en = "Cron Stone Bundle (1,000 pcs)"
    icon = CRON_BUNDLE_ICON
    rarity = "uncommon"
    crown_value = 1000


class CronStone500(AbstractItem):
    id = "cron_stone_500"
    name = "Камень Крон (500 шт.)"
    name_en = "Cron Stone (500 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 500


class CronStone400(AbstractItem):
    id = "cron_stone_400"
    name = "Камень Крон (400 шт.)"
    name_en = "Cron Stone (400 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 400


class CronStone200(AbstractItem):
    id = "cron_stone_200"
    name = "Камень Крон (200 шт.)"
    name_en = "Cron Stone (200 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 200


class CronStone250(AbstractItem):
    id = "cron_stone_250"
    name = "Камень Крон (250 шт.)"
    name_en = "Cron Stone (250 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 250


class CronStone300(AbstractItem):
    id = "cron_stone_300"
    name = "Камень Крон (300 шт.)"
    name_en = "Cron Stone (300 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 300


class CronStone(AbstractItem):
    id = "cron_stone"
    name = "Камень Крон"
    name_en = "Cron Stone"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 1


class AdviceOfValks200(AbstractItem):
    id = "advice_of_valks_200"
    name = "Совет Валкса (+200)"
    name_en = "Advice of Valks (+200)"
    icon = "icons/advice_of_valks_200.webp"
    rarity = "rare"
    crown_value = None


class AdviceOfValks170(AbstractItem):
    id = "advice_of_valks_170"
    name = "Совет Валкса (+170)"
    name_en = "Advice of Valks (+170)"
    icon = "icons/advice_of_valks_170.webp"
    rarity = "rare"
    crown_value = None


class CronStone150(AbstractItem):
    id = "cron_stone_150"
    name = "Камень Крон (150 шт.)"
    name_en = "Cron Stone (150 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 150


class CronStone100(AbstractItem):
    id = "cron_stone_100"
    name = "Камень Крон (100 шт.)"
    name_en = "Cron Stone (100 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 100


class AdviceOfValks150(AbstractItem):
    id = "advice_of_valks_150"
    name = "Совет Валкса (+150)"
    name_en = "Advice of Valks (+150)"
    icon = "icons/advice_of_valks_150.webp"
    rarity = "rare"
    crown_value = None


class ArtisansMemory(AbstractItem):
    id = "artisans_memory"
    name = "Память мастера"
    name_en = "Artisan's Memory"
    icon = "icons/artisans_memory.webp"
    rarity = "rare"
    crown_value = None


class OutfitSelectionBox(AbstractItem):
    id = "outfit_selection_box"
    name = "[Ивент] Сундук с полным комплектом на выбор"
    name_en = "[Event] Full Outfit Selection Box"
    icon = "icons/full_outfit.webp"
    rarity = "epic"
    crown_value = 993


class SupportBoxV(AbstractItem):
    id = "support_box_v"
    name = "[Ивент] Сундук помощи V"
    name_en = "[Event] Support Box V"
    icon = "icons/support_box_v.webp"
    rarity = "common"
    crown_value = None


class SupportBoxIV(AbstractItem):
    id = "support_box_iv"
    name = "[Ивент] Сундук помощи IV"
    name_en = "[Event] Support Box IV"
    icon = "icons/support_box_iv.webp"
    rarity = "common"
    crown_value = None


class CronChest200(AbstractItem):
    id = "cron_chest_200"
    name = "Сундук с Камнями Крон (200 шт.)"
    name_en = "Cron Stone Chest (200 pcs)"
    icon = CRON_CHEST_ICON
    rarity = "common"
    crown_value = 200


class OldMoonSpecialSpell(AbstractItem):
    id = "old_moon_special_spell"
    name = "[Ивент] Особое заклинание Убывающей Луны"
    name_en = "[Event] Old Moon Special Spell"
    icon = "icons/old_moon_special_spell.webp"
    rarity = "common"
    crown_value = None


class OldMoonFortune(AbstractItem):
    id = "old_moon_fortune"
    name = "Удача Убывающей луны"
    name_en = "Old Moon Fortune"
    icon = "icons/old_moon_fortune.webp"
    rarity = "common"
    crown_value = None


class ItemCollectionScroll(AbstractItem):
    id = "item_collection_scroll"
    name = "Свиток удачи"
    name_en = "Item Collection Increase Scroll"
    icon = "icons/item_collection_scroll.webp"
    rarity = "common"
    crown_value = None


class GiovanGrolinScroll(AbstractItem):
    id = "giovan_grolin_scroll"
    name = "[Ивент] Свиток помощи Йована Гролина"
    name_en = "[Event] Giovan Grolin's Support Scroll"
    icon = "icons/giovan_grolin_scroll.webp"
    rarity = "common"
    crown_value = None


class CombatSkillExpScroll(AbstractItem):
    id = "combat_skill_exp_scroll"
    name = "Свиток «300% к боевому опыту и опыту навыков» (60 мин.)"
    name_en = "Combat & Skill EXP 300% Scroll (60 min)"
    icon = "icons/combat_skill_exp_scroll.webp"
    rarity = "common"
    crown_value = None


class CronStone75(AbstractItem):
    id = "cron_stone_75"
    name = "Камень Крон (75 шт.)"
    name_en = "Cron Stone (75 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 75


class CronStone50(AbstractItem):
    id = "cron_stone_50"
    name = "Камень Крон (50 шт.)"
    name_en = "Cron Stone (50 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 50


class AdviceOfValks250(AbstractItem):
    id = "advice_of_valks_250"
    name = "Совет Валкса (+250)"
    name_en = "Advice of Valks (+250)"
    icon = "icons/advice_of_valks_250.webp"
    rarity = "rare"
    crown_value = None


class AdviceOfValks130(AbstractItem):
    id = "advice_of_valks_130"
    name = "Совет Валкса (+130)"
    name_en = "Advice of Valks (+130)"
    icon = "icons/advice_of_valks_130.webp"
    rarity = "rare"
    crown_value = None


class CaphrasStone2(AbstractItem):
    id = "caphras_stone_2"
    name = "Камень Кафраса (2 шт.)"
    name_en = "Caphras Stone (2 pcs)"
    icon = CAPHRAS_STONE_ICON
    rarity = "uncommon"
    crown_value = None


class CaphrasStone4(AbstractItem):
    id = "caphras_stone_4"
    name = "Камень Кафраса (4 шт.)"
    name_en = "Caphras Stone (4 pcs)"
    icon = CAPHRAS_STONE_ICON
    rarity = "uncommon"
    crown_value = None


class CaphrasStone6(AbstractItem):
    id = "caphras_stone_6"
    name = "Камень Кафраса (6 шт.)"
    name_en = "Caphras Stone (6 pcs)"
    icon = CAPHRAS_STONE_ICON
    rarity = "uncommon"
    crown_value = None


class CaphrasStone8(AbstractItem):
    id = "caphras_stone_8"
    name = "Камень Кафраса (8 шт.)"
    name_en = "Caphras Stone (8 pcs)"
    icon = CAPHRAS_STONE_ICON
    rarity = "uncommon"
    crown_value = None


class CaphrasStone10(AbstractItem):
    id = "caphras_stone_10"
    name = "Камень Кафраса (10 шт.)"
    name_en = "Caphras Stone (10 pcs)"
    icon = CAPHRAS_STONE_ICON
    rarity = "uncommon"
    crown_value = None


class TokenOfFate(AbstractItem):
    id = "token_of_fate"
    name = "[Ивент] Знак судьбы"
    name_en = "[Event] Token of Fate"
    icon = "icons/token_of_fate.webp"
    rarity = "legendary"
    crown_value = None


class CronStone3(AbstractItem):
    id = "cron_stone_3"
    name = "Камень Крон (3 шт.)"
    name_en = "Cron Stone (3 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 3


class CronStone6(AbstractItem):
    id = "cron_stone_6"
    name = "Камень Крон (6 шт.)"
    name_en = "Cron Stone (6 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 6


class CronStone9(AbstractItem):
    id = "cron_stone_9"
    name = "Камень Крон (9 шт.)"
    name_en = "Cron Stone (9 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 9


class CronStone12(AbstractItem):
    id = "cron_stone_12"
    name = "Камень Крон (12 шт.)"
    name_en = "Cron Stone (12 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 12


class CronStone15(AbstractItem):
    id = "cron_stone_15"
    name = "Камень Крон (15 шт.)"
    name_en = "Cron Stone (15 pcs)"
    icon = CRON_STONE_ICON
    rarity = "uncommon"
    crown_value = 15
