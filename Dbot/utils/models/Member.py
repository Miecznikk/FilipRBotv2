from dataclasses import dataclass


@dataclass
class Member:
    id: int
    name: str
    points: int
    minutes_spent: int
    configurator: bool

    def __eq__(self, other):
        return self.name == other.name
