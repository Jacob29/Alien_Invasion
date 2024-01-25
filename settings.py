class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_booster = 3
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        

        # Beam settings
        self.beam_speed = 20
        self.beam_width = 350
        self.beam_height = 60
        self.beam_colour = (5, 213, 196)
        self.beams_allowed = 1
        
        # Alien settings
        self.fleet_drop_speed = 10




        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.difficulty_level = "medium"

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty_level == 'easy':
            self.ship_speed = 10
            self.bullet_speed = 3.5
            self.alien_speed = 0.65
            self.bullets_allowed = 20
        if self.difficulty_level == 'medium':
            self.ship_speed = 1.5
            self.bullet_speed = 100
            self.alien_speed = 1.0
            self.bullets_allowed = 10
        if self.difficulty_level == 'hard':
            self.ship_speed = 1.2
            self.bullet_speed = 2
            self.alien_speed = 10
            self.bullets_allowed = 7

        # Scoring settings
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale