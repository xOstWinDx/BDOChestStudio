"""Bounded queue, reproducible runs and UI-independent reports."""

from collections import Counter, deque
from dataclasses import dataclass, field
from random import Random
from typing import Mapping

from .domain import Chest, Drop, Item


@dataclass
class Report:
    seed: int
    basket: dict[str, int]
    inventory: Counter = field(default_factory=Counter)
    opened: Counter = field(default_factory=Counter)
    status: str = "running"
    pending: int = 0

    @property
    def total_opened(self):
        return self.opened.total()

    def crowns(self, catalog: Mapping[str, Item]):
        return sum(catalog[key].to_crowns(qty) or 0 for key, qty in self.inventory.items())


@dataclass(frozen=True)
class Opening:
    chest_id: str
    drops: tuple[Drop, ...]


class Simulation:
    def __init__(self, catalog: Mapping[str, Item], basket: Mapping[str, int], seed: int, limit: int = 1_000_000):
        if not basket or any(
            type(q) is not int or q <= 0 or not isinstance(catalog.get(k), Chest) for k, q in basket.items()
        ):
            raise ValueError("Корзина должна содержать сундуки с положительным целым количеством")
        if sum(basket.values()) > limit:
            raise ValueError(f"В корзине допускается не больше {limit:,} сундуков")
        self.catalog = catalog
        self.rng = Random(seed)
        self.limit = limit
        self.queue = deque(basket.items())
        self.report = Report(seed, dict(basket), pending=sum(basket.values()))

    def step(self) -> Opening | None:
        if self.report.status != "running":
            return None
        if not self.queue:
            self.report.status = "complete"
            return None
        if self.report.total_opened >= self.limit:
            self.report.status = "limited"
            return None
        key, count = self.queue.popleft()
        if count > 1:
            self.queue.appendleft((key, count - 1))
        self.report.pending -= 1
        chest = self.catalog[key]
        drops = chest.open(self.rng)
        self.report.opened[key] += 1
        for drop in drops:
            if isinstance(self.catalog[drop.item_id], Chest):
                self.queue.append((drop.item_id, drop.quantity))
                self.report.pending += drop.quantity
            else:
                self.report.inventory[drop.item_id] += drop.quantity
        if not self.queue:
            self.report.status = "complete"
        return Opening(key, drops)

    def cancel(self):
        if self.report.status == "running":
            self.report.status = "cancelled"
