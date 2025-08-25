import pygame
import random

class Settings:
    def __init__(self):
        # Screen settings
        self.bg_color = (0, 0, 0)
        
        # Ship settings
        self.ship_speed = 3
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colors = [
                (255, 255, 255),
                (255, 240, 0),     
                (255, 140, 0),     
                (255, 60, 0),      
                 ]
        self.bullet_color = random.choice(self.bullet_colors)
        self.bullets_allowed = 5
        self.bullet_fire_rate = 30  # ms between shots
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  
        self.alien_rows = 1 # Starting rows
        
        # Game difficulty
        self.speedup_scale = 1.1

    def increase_difficulty(self):
        """Increase game speed settings"""
        self.alien_speed *= self.speedup_scale
        self.alien_rows = min(self.alien_rows + 0.5, 5)  # Cap at 5 rows