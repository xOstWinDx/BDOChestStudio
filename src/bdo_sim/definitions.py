"""Declarative entity classes: registration happens when their module is imported."""

from abc import abstractmethod
from dataclasses import dataclass
from itertools import accumulate
import math
import re

from .domain import Item, Drop, WeightedChest, BonusChest, ChainChest, ChainStage
from .rarity import Rarity


ENTITY_TYPES: dict[str, type[Item]] = {}


class EntityDefinition:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Helper bases have no own id. Every named entity registers exactly once.
        if "id" in cls.__dict__:
            if not isinstance(cls.id, str) or not re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", cls.id):
                raise ValueError(f"{cls.__name__}: id must use English snake_case")
            if cls.id in ENTITY_TYPES:
                raise ValueError(f"Duplicate entity id: {cls.id}")
            for field in ("id", "name", "name_en", "icon"):
                if not isinstance(getattr(cls, field, None), str) or not getattr(cls, field):
                    raise ValueError(f"{cls.__name__}: missing {field}")
            ENTITY_TYPES[cls.id] = cls

    @classmethod
    def metadata(cls):
        return {key: getattr(cls, key) for key in ("id", "name", "icon", "rarity", "crown_value")}


def probability(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError(f"Invalid probability: {value}")
    return value


@dataclass(frozen=True)
class Loot:
    """A reference to an entity class, an amount, and a weight/bonus chance."""

    item: type[Item]
    quantity: int = 1
    chance: float = 100

    def __post_init__(self):
        if not isinstance(self.item, type) or not issubclass(self.item, Item):
            raise ValueError("Loot must reference an Item class")
        if type(self.quantity) is not int or self.quantity < 1:
            raise ValueError("Reward quantity must be a positive integer")
        probability(self.chance)
        if ENTITY_TYPES.get(self.item.id) is not self.item:
            raise ValueError(f"Unregistered reward: {self.item.__name__}")

    def drop(self):
        return Drop(self.item.id, self.quantity)

    @property
    def rarity(self) -> Rarity:
        return Rarity.from_chance(self.chance)


class AbstractItem(EntityDefinition, Item):
    id: str  # Stable English snake_case key; required on every concrete entity.

    def __init__(self):
        super().__init__(**self.metadata())


class AbstractChest(EntityDefinition, WeightedChest):
    """One weighted reward per opening. Tables may reference self/later classes."""

    @classmethod
    @abstractmethod
    def loot_table(cls) -> tuple[Loot, ...]:
        raise NotImplementedError

    def __init__(self):
        table = self.loot_table()
        weights = tuple(entry.chance for entry in table)
        if not weights or sum(weights) <= 0:
            raise ValueError(f"{type(self).__name__}: empty loot table")
        super().__init__(**self.metadata(), drops=tuple(e.drop() for e in table), cumulative=tuple(accumulate(weights)))


class AbstractBonusChest(EntityDefinition, BonusChest):
    @classmethod
    @abstractmethod
    def guaranteed_loot(cls) -> tuple[Loot, ...]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def bonus_loot(cls) -> tuple[Loot, ...]:
        raise NotImplementedError

    def __init__(self):
        guaranteed = self.guaranteed_loot()
        if any(e.chance != 100 for e in guaranteed):
            raise ValueError("Guaranteed rewards must have a 100% chance")
        super().__init__(
            **self.metadata(),
            guaranteed=tuple(e.drop() for e in guaranteed),
            extras=tuple((e.drop(), e.chance) for e in self.bonus_loot()),
        )


@dataclass(frozen=True)
class Stage:
    chance: float
    next_stage: str | None
    rewards: tuple[Loot, ...]

    def resolve(self):
        if any(e.chance != 100 for e in self.rewards):
            raise ValueError("Stage rewards must have a 100% chance")
        return ChainStage(probability(self.chance), self.next_stage, tuple(e.drop() for e in self.rewards))


class AbstractChainChest(EntityDefinition, ChainChest):
    @classmethod
    @abstractmethod
    def chain_stages(cls) -> dict[str, Stage]:
        raise NotImplementedError

    def __init__(self):
        stages = self.chain_stages()
        if self.start not in stages:
            raise ValueError("Unknown starting stage")
        for current in stages:
            seen = set()
            while current is not None:
                if current in seen or current not in stages:
                    raise ValueError("Cycle or unknown chain stage")
                seen.add(current)
                current = stages[current].next_stage
        super().__init__(
            **self.metadata(), start=self.start, stages=tuple((key, stage.resolve()) for key, stage in stages.items())
        )
