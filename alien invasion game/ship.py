import pygame
from pygame.sprite import Sprite
#making a class for the player chareacter
class Ship(Sprite):
    def __init__(self, screen):
        super(Ship, self).__init__()
        self.screen = screen
        #to set the size of the image and load it
        self.image = pygame.Surface((64, 64))
        self.image = pygame.image.load('images\ship.bmp')
        #to traet image and screen as rectangles
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #to change the position of image to x:center, y:bottom
        self.rect.centerx =self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False


    #to draw the image
    def blitme(self):
        self.screen.blit(self.image, self.rect)#self.rect is the position which is (450, 700)

    # to center the ship uf collided with the fleet
    def center(self):
        self.rect.centerx = self.screen_rect.centerx