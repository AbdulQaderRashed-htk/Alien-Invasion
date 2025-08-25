import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        
        # Load alien image and set rect
        self.image = pygame.image.load('alien.bmp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 22))
        self.rect = self.image.get_rect()
        
        # Start each new alien near top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien hits edge"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move alien right or left"""
        self.x += (self.settings.alien_speed * 
                  self.settings.fleet_direction)
        self.rect.x = self.x