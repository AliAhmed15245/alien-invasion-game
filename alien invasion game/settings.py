import pygame

#making a class for the game sittings
class Settings:
    def __init__(self, aliens):
        self.aliens = aliens
        #-----screen settings----
        self.width = 900
        self.legnth = 700
        self.bg_color = (230, 230, 230)
        self.main_music = pygame.mixer.Sound("images/music.wav")
        #-----ship settings-----
        self.ship_shooting_sound = pygame.mixer.Sound("images/shooting.wav")
        self.ships_left = 3
        self.ship_hit_sound = pygame.mixer.Sound("images/hit.wav")
        #-----bullet settings-----
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60 ,60
        self.bullets_allowed_num = 5
        #-----alien bullet settings-----
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_color = 60, 60 ,60
        self.alien_bullets_allowed_num = len(self.aliens)
        #-------alien settings------
        self.alien_drop_speed = 6
        self.new_fleet_sound = pygame.mixer.Sound("images/new_fleet.wav")
        #-------main settings--------
        self.speed_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        self.fps = 1000



    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_bullet_speed_factor = 1
        self.alien_speed_factor_x = 1
        self.alien_direction = 1
        self.alien_pounts = 50


    def increase_speed(self):
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor_x *= self.speed_scale
        self.alien_pounts = int(self.score_scale * self.alien_pounts)
        print(self.alien_pounts)

