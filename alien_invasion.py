import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
import sys
from time import time

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((600, 800), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.stats = GameStats(self.settings)
        self.ship = Ship(self.screen, self.settings)
        self.bullets = Group()
        self.aliens = Group()
        
        self._create_fleet()
        self.last_shot_time = 0
        self.game_active = True

    def run_game(self):
        """Main game loop"""
        while True:
            self._check_events()
            if self.game_active:
                self._auto_fire_bullets()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _auto_fire_bullets(self):
        """Handle automatic bullet firing"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.settings.bullet_fire_rate:
            self._fire_bullet()
            self.last_shot_time = current_time

    def _fire_bullet(self):
        """Create a new bullet"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create full alien fleet"""
        alien = Alien(self.settings, self.screen)
        alien_width, alien_height = alien.rect.size
        
        # how many aliens fit in a row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determine number of rows
        available_space_y = (self.settings.screen_height - 
                           (3 * alien_height) - 
                           self.ship.rect.height)
        number_rows = int(self.settings.alien_rows)
        
        # Create the fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        """Create single alien"""
        alien = Alien(self.settings, self.screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_bullets(self):
        """Update bullet positions and remove old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            self.stats.score += 10
            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
        
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_difficulty()
            self._create_fleet()

    def _update_aliens(self):
        """Update alien positions and check collisions"""
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to ship being hit by alien"""
        self.stats.ships_left -= 1
        
        if self.stats.ships_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Check if any aliens reach the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens reach an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Score display
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.stats.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Lives display
        lives_text = font.render(f"Lives: {self.stats.ships_left}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))
        
        # Game over message
        if not self.game_active:
            go_font = pygame.font.SysFont(None, 64)
            go_text = go_font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(go_text, (
                self.settings.screen_width/2 - 150,
                self.settings.screen_height/2 - 32
            ))
        
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()