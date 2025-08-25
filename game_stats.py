class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit