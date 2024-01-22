import pygame.font

class Button:
    """A class to build buttons for the game"""

    def __init__(self, ai_game, msg):
        """Initialize button atributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_colour = (0, 135, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        


        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        # self.msg_image_rect.center = self.rect.center

    def draw_play_button(self):
        """Draw blank button and then draw message."""
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.screen.fill(self.button_colour, self.rect)
        self.msg_image_rect.center = self.rect.center
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_diff_buttons(self):
        """Draw three blank buttons and then draw the messages inside"""
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.screen.fill(self.button_colour, self.rect)
        self.msg_image_rect.center = (self.rect.center - 20)
        self.screen.blit(self.msg_image, self.msg_image_rect)