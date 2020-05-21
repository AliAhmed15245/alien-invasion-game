import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()

        self.ai_settings = ai_settings
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width,
        ai_settings.alien_bullet_height)

        self.y = float(self.rect.y)
        self.color = self.ai_settings.alien_bullet_color
        self.speed_factor = self.ai_settings.alien_bullet_speed_factor


    def update(self):
        """ to move the bullet upwards"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)