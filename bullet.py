import pygame
from pygame.sprite import Sprite
import random

class Bullet(Sprite):
    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen
        
        # Create bullet rect at (0,0) then set position
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Store bullet position as decimal number
        self.y = float(self.rect.y)
        
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed

    def update(self):
        """shoot bullet up screen"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)