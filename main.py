import sys 

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initilise the game, and create game resources."""
        pygame.init() # Initilising the pygame atributes for it to work!
        self.clock = pygame.time.Clock() # Using this to set a consistant framerate
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # Creates a full screen instead of pixle sized
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion") # Title of window

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
           self._check_events()
           self.ship.update()
           self.bullets.update()

           # Get rid of bullets that have disappeared
           for bullet in self.bullets.copy():
               if bullet.rect.bottom <=0:
                   self.bullets.remove(bullet)
           
           self._update_screen()
           self.clock.tick(60) # 60fps
           
    def _check_events(self):
            """Respond to keypresses and mouse events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # This handles the exit of the program
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events_(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events_(event)
                        
    def _check_keydown_events_(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet_()

    def _check_keyup_events_(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet_(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the ew screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() # Drawing the ship

        pygame.display.flip() # This produces the refreshed screen


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()