import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from beam import Beam
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start AI in an active state.
        self.game_active = False

        # self.play_button = Button(self, "Play")

        self._make_difficulty_buttons()



    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_projectiles()
                self._update_aliens()
                

            self._update_screen()
            self.clock.tick(60)

    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.hard_button.rect.top = (
            self.hard_button.rect.top + 1.5*self.hard_button.rect.height)
        
        self.easy_button.rect.left = (
            self.easy_button.rect.left - 1.5*self.easy_button.rect.width)
        self.hard_button.rect.left = (
            self.hard_button.rect.left + 1.5*self.hard_button.rect.width)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_LSHIFT:
            self.ship.booster = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_c:
            self._fire_beam()
        elif event.key == pygame.K_p:
            if not self.game_active:
                self._start_game()        
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_stats()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_LSHIFT:
            self.ship.booster = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        if self.easy_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty_level = 'easy'
            self._start_game()
        if self.medium_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty_level = 'medium'
            self._start_game()
        if self.hard_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.difficulty_level = 'hard'
            self._start_game()

    def _start_game(self):
        """Start a new game if triggered"""
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.game_active = True
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(new_bullet)

    def _fire_beam(self):
        new_beam = Beam(self)
        if len(self.beams) < self.settings.beams_allowed:
            self.beams.add(new_beam)
        
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        
        if self.stats.ships_left > 0:
            # Decrement ships left
            print(self.stats.ships_left)
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            self.beams.empty()

            # Create a new fleet and center the ship.
            self._create_fleet
            self.ship.center_ship()
            self.sb.prep_ships()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_projectiles(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet position
        self.bullets.update()
        self.beams.update()
        
        #Get rid of bullets and beams that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for beam in self.beams.copy():
            if beam.rect.bottom <= 0:
                self.beams.remove(beam)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True) or pygame.sprite.groupcollide(
            self.beams, self.aliens, False, True)
        
         
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.beams.empty()
            self.settings.increase_speed()
            self.sb.increase_level()
            self.sb.prep_level()
            self._create_fleet()
            self.ship.center_ship()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there is no room left
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        start_x, start_y = 2 * alien_width, 2 * alien_height
        current_x = start_x
        current_y = start_y

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2.5 * alien_width

            # Finished a row' reset x vlaue, and increment y value
            current_x = start_x
            current_y += 2.5 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reacehd the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """ Redraw the screen during each pass through the loop."""
        self.screen.fill(self.settings.bg_colour)

        if not self.game_active:
            # self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        else:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for beam in self.beams.sprites():
                beam.draw_beam()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.sb.show_score()

        pygame.display.flip()
        
if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()