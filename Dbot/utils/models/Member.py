from dataclasses import dataclass


@dataclass
class Member:
    id: int
    name: str
    points: int
    minutes_spent: int
