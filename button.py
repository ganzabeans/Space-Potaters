import pygame.font


class Button():

    def __init__(self, ai_settings, screen, b_type):
        """Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.b_type = self.ai_settings.buttons[b_type]

        # set the dimensions and properties of the button
        self.width = self.ai_settings.button_width
        self.height = self.ai_settings.button_height
        self.button_color = self.ai_settings.button_color
        self.text_color = self.ai_settings.button_text_color
        self.font = pygame.font.SysFont(None, 64)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.b_type['position']

        # Button only needs to show once
        self.prep_msg(self.b_type['message'])

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blacnk button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
