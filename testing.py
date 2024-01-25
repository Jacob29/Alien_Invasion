class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self):
        """Initialize statistics"""

        self.reset_stats()

        self.high_score = 10

    def reset_stats(self):
            """Init statistics that can change during the game"""
            self.score = 0
            self.level = 1

    def save_stats(self):
         save_high_score = open("highscore.txt", "w")
         save_high_score.write(str(self.high_score))
         print("Test")


test = GameStats()
test.save_stats()