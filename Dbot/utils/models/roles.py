class GameRole:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.game_assigned = kwargs.get("game_assigned")
        self.game_detection_strings = [value for value in kwargs.get("game_detection_string").split(",")]

