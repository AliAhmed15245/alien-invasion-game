import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.move_down = False

    def check_edges(self):
        """ check collision with edges and change the direction"""
        if self.rect.right >= self.ai_settings.width:
            self.ai_settings.alien_direction = -1
            self.move_down = True
        elif self.rect.left <= 0:
            self.ai_settings.alien_direction = 1
            self.move_down = True
        else:
            self.move_down = False

    def moving_down(self):
        """ to move the alien downwards"""
        self.rect.y += self.ai_settings.alien_drop_speed

    def update(self):
        self.rect.x += (self.ai_settings.alien_speed_factor_x * self.ai_settings.alien_direction)


    def blitme(self):
        self.screen.blit(self.image, self.rect)