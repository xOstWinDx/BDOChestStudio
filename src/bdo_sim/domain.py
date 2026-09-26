"""Domain entities: no GUI, persistence or global random state."""

from __future__ import annotations

from abc import ABC, abstractmethod
from bisect import bisect_right
from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    icon: str
    rarity: str = "common"
    crown_value: int | None = None

    def to_crowns(self, quantity: int = 1) -> int | None:
        return None if self.crown_value is None else self.crown_value * quantity


@dataclass(frozen=True)
class Drop:
    item_id: str
    quantity: int


@dataclass(frozen=True)
class Chest(Item, ABC):
    @abstractmethod
    def open(self, rng: Random) -> tuple[Drop, ...]:
        """Resolve one opening, including all independent rewards."""


@dataclass(frozen=True)
class WeightedChest(Chest):
    drops: tuple[Drop, ...] = ()
    cumulative: tuple[float, ...] = ()

    def open(self, rng: Random) -> tuple[Drop, ...]:
        index = bisect_right(self.cumulative, rng.random() * self.cumulative[-1])
        return (self.drops[min(index, len(self.drops) - 1)],)


@dataclass(frozen=True)
class BonusChest(Chest):
    guaranteed: tuple[Drop, ...] = ()
    extras: tuple[tuple[Drop, float], ...] = ()

    def open(self, rng: Random) -> tuple[Drop, ...]:
        return self.guaranteed + tuple(drop for drop, chance in self.extras if rng.random() * 100 < chance)


@dataclass(frozen=True)
class ChainStage:
    chance: float
    next_stage: str | None
    rewards: tuple[Drop, ...]


@dataclass(frozen=True)
class ChainChest(Chest):
    stages: tuple[tuple[str, ChainStage], ...] = ()
    start: str = "s0"

    def open(self, rng: Random) -> tuple[Drop, ...]:
        stages = dict(self.stages)
        current = self.start
        while True:
            stage = stages[current]
            if stage.next_stage is None or rng.random() * 100 >= stage.chance:
                return stage.rewards
            current = stage.next_stage
