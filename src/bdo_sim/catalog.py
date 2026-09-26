"""Build and validate the catalog of automatically registered Python entities."""

from pathlib import Path

from . import content  # Static imports also make content discoverable by exe builders.
from .definitions import ENTITY_TYPES
from .domain import BonusChest, ChainChest, Item, WeightedChest

ASSETS = Path(__file__).resolve().parent / "assets"


def load_catalog() -> dict[str, Item]:
    result = {key: entity() for key, entity in ENTITY_TYPES.items()}
    for item in result.values():
        if not (ASSETS / item.icon).is_file():
            raise ValueError(f"Нет иконки: {item.icon}")
        if item.crown_value is not None and (type(item.crown_value) is not int or item.crown_value < 0):
            raise ValueError(f"Некорректная стоимость: {item.id}")
        rewards = ()
        if isinstance(item, WeightedChest):
            rewards = item.drops
        elif isinstance(item, BonusChest):
            rewards = item.guaranteed + tuple(d for d, _ in item.extras)
        elif isinstance(item, ChainChest):
            rewards = tuple(d for _, stage in item.stages for d in stage.rewards)
        for reward in rewards:
            if reward.item_id not in result:
                raise ValueError(f"Неизвестная награда: {reward.item_id}")
    return result
