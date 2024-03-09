from dataclasses import dataclass


@dataclass
class GameRole:
    name: str
    game_assigned: str
    game_detection_string: str
