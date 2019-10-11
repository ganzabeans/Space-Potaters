class GameStats():
    """Track statistics for Space Potaters"""

    def __init__(self, ai_settings):
        """initialziae statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Is true when a rewrite is needed
        self.rewrite = False

        # Start Alien Invasion in an inactive state
        self.game_active = False
        self.check_hs = False

        # High score read from file
        hs_file = open('high_scores.txt', 'r')
        for line in hs_file:
            self.hs_list = line.split()
        hs_file.close()

        # find all - time high score
        self.hs_list.sort(key=int, reverse=True)

        self.high_score = int(self.hs_list[0])

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self, current_score):
        """Writes high over high score"""

        # check to make sure list is in decending order
        self.hs_list.sort(key=int, reverse=True)

        for x in range(len(self.hs_list)):
            if current_score > int(self.hs_list[x]):
                self.hs_list.insert(x, current_score)
                self.rewrite = True
                break

        if self.rewrite:
            hs_file = open('high_scores.txt', 'w')
            for x in range(0, 10):
                hs_file.write(str(self.hs_list[x]) + " ")
            hs_file.close()
