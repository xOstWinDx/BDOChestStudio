"""Presentation probabilities, without consuming or changing simulation randomness."""

from dataclasses import dataclass

from .domain import Drop, WeightedChest, BonusChest, ChainChest, Chest
from .rarity import Rarity


@dataclass(frozen=True)
class Outcome:
    drop: Drop
    chance: float

    @property
    def rarity(self):
        return Rarity.from_chance(self.chance)


def outcomes(chest):
    if isinstance(chest, WeightedChest):
        previous = 0
        result = []
        for drop, cumulative in zip(chest.drops, chest.cumulative):
            result.append(Outcome(drop, (cumulative - previous) / chest.cumulative[-1] * 100))
            previous = cumulative
        return result
    if isinstance(chest, BonusChest):
        return [Outcome(d, 100) for d in chest.guaranteed] + [Outcome(d, p) for d, p in chest.extras]
    if isinstance(chest, ChainChest):
        stages = dict(chest.stages)
        current, reach, result = chest.start, 1.0, []
        while current is not None:
            stage = stages[current]
            stop = 1 if stage.next_stage is None else 1 - stage.chance / 100
            result.extend(Outcome(d, reach * stop * 100) for d in stage.rewards)
            reach *= stage.chance / 100
            current = stage.next_stage
        return result
    return []


def sorted_chests(catalog):
    chests = {k: v for k, v in catalog.items() if isinstance(v, Chest)}
    tables = {k: outcomes(v) for k, v in chests.items()}
    # Bounded expected number of nested openings handles self-drops and cycles.
    scores = dict.fromkeys(chests, 0.0)
    for _ in range(6):
        scores = {
            k: sum(
                o.chance / 100 * o.drop.quantity * (1 + scores[o.drop.item_id])
                for o in table
                if o.drop.item_id in chests
            )
            for k, table in tables.items()
        }
    pinned = {"butterfly_chest": 0, "golden_treasure_chest": 1}
    return sorted(chests.values(), key=lambda c: (pinned.get(c.id, 2), -scores[c.id], c.id))
