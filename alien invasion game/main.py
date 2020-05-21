import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import States
from button import Button
from scoreBoard import ScoreBoard

def run_game():
    #to e able to use the module
    pygame.init()
    #setting the settings object
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.width, ai_setting.legnth) )
    pygame.display.set_caption("Invasion game")
    #setting the charecter object
    ship = Ship(screen)
    bullets = Group()
    aliens = Group()
    stats = States(ai_setting)
    gf.create_fleet(ai_setting, screen, aliens, ship, stats)
    play_button = Button(ai_setting, screen, "Play")
    sb = ScoreBoard(ai_setting, screen, stats)
    clock = pygame.time.Clock()


    while True:
        gf.check_events(stats, play_button, aliens, bullets, ai_setting, ship, screen, sb)
        if stats.game_active:
            #ai_setting.main_music.play(loops=10)
            gf.moving(ship, screen, ai_setting.ship_speed_factor)
            gf.delet_bullets(bullets)
        #clock.tick(ai_setting.fps)
        gf.update_screen(stats, aliens, bullets, ship, ai_setting, screen,
        play_button, sb)



run_game()
