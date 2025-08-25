import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings
        
        # Load ship image and get its rect
        self.image = pygame.image.load('pictures/ship.bmp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 64)) 
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start ship at bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        
        # Store decimal value for ship's center
        self.center = float(self.rect.centerx)

    def update(self):
        """Update ship's position"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed
            
        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on screen"""
        self.center = self.screen_rect.centerx

    def blitme(self):
        """Draw ship at current location"""
        self.screen.blit(self.image, self.rect)