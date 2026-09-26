"""Drop rarity is relative to the current chest, not the item's market value."""

from enum import IntEnum


class Rarity(IntEnum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4
    MYTHIC = 5

    @classmethod
    def from_chance(cls, chance: float):
        chance = round(chance, 10)  # Cumulative weights can introduce tiny float errors.
        if chance <= 0.1:
            return cls.MYTHIC
        if chance <= 1:
            return cls.LEGENDARY
        if chance <= 5:
            return cls.EPIC
        if chance <= 15:
            return cls.RARE
        if chance <= 35:
            return cls.UNCOMMON
        return cls.COMMON
