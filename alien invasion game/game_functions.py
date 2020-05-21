import pygame, sys, time, json
from bullets import Bullet
from alien import Alien
from alien_bullets import AlienBullet

#-----checking events-------
def check_keydown_events(ship, event, bullets, ai_settings, screen, play_button):
    #to move the ship right
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    #to move the ship left
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_p:
        play_button.p_pressed = True
    #to shoot
    if event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed_num:
            new_bullet = Bullet(ai_settings, ship, screen)
            bullets.add(new_bullet)
            ai_settings.ship_shooting_sound.play()


def check_keyup_events(ship, event, play_button):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False



def check_events(stats, play_button, aliens, bullets, ai_settings, ship, screen, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(stats.high_score)
            dump_high_score(stats, "score.json")
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ship, event, bullets, ai_settings, screen, play_button)
        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event, play_button)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
             ai_settings, ship, screen, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
         ai_settings, ship, screen, sb):
    button_clicked =  play_button.rect.collidepoint(mouse_x, mouse_y)
    if (play_button.p_pressed and not stats.game_active) or (button_clicked  and not stats.game_active):
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        sb.prep_level()
        sb.prep_score()
        sb.prep_ships()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship, stats)
        ship.center()

#------ scoring functions-----
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def dump_high_score(stats, file_name):
    with open(file_name, "r+") as f_obj:
        json.dump(stats.high_score, f_obj)


#------alien functions -------
def get_available_numx(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    available_spacex = ai_settings.width - 2*alien.rect.width
    available_numx = int(available_spacex / (1.4*alien.rect.width))
    return available_numx

def get_rows_number(ai_settings, screen, ship):
    alien = Alien(ai_settings, screen)
    available_spacey = ai_settings.legnth - 3*alien.rect.height - ship.rect.height
    available_rows = int(available_spacey / (1.4*alien.rect.height))
    return available_rows

def create_alien(ai_settings, screen, aliens_num, aliens, rows_number, stats):
    for row_num in range(rows_number-1):
        for alien_num in range(aliens_num):
            alien = Alien(ai_settings, screen)
            alien.rect.x =10 + 1.5*alien.rect.width*alien_num
            alien.rect.y = 10+ 1.5*alien.rect.height*row_num
            aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, ship, stats):
    available_numx =  get_available_numx(ai_settings, screen)
    levels5 = check_5levels(stats)
    if levels5:
        available_numy = 3
    else:
        available_numy = get_rows_number(ai_settings, screen, ship)
    create_alien(ai_settings, screen, available_numx, aliens, available_numy, stats)

def alien_moving_down(ai_settings, screen, aliens):
    for alian in aliens:
        if alian.move_down:
            for a in aliens:
                a.moving_down()

def check_aliens_bottom(stats, aliens, bullets, ship, ai_settings, screen, sb):
    sceen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= sceen_rect.bottom:
           ship_hit(stats, aliens, bullets, ship, ai_settings, screen, sb)
           break

def check_5levels(stats):
    if stats.level % 5 == 0:
        return True
def new_alien_image(stats, aliens):
    global available_rows
    levels5 = check_5levels(stats)
    if levels5:
        available_numy = 2
        for alien in aliens:
            alien.image = pygame.image.load("images/alien2.bmp")
            alien.image = pygame.transform.scale(alien.image, (60, 58))


def update_alien(stats, aliens, bullets, ship, ai_settings, screen, sb):
    new_alien_image(stats, aliens)
    aliens.draw(screen)
    for alien in aliens:
        alien.check_edges()
    alien_moving_down(ai_settings, screen, aliens)
    aliens.update()
    #check collision with the ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, ship, ai_settings, screen, sb)
    check_aliens_bottom(stats, aliens, bullets, ship, ai_settings, screen, sb)


#------ship functions-------
def moving(ship, screen, speed):
    """ to move the ship"""
    if ship.moving_right and ship.rect.right < ship.screen_rect.right:
        ship.rect.centerx += speed
    elif ship.moving_left and ship.rect.left > 0:
        ship.rect.centerx -= speed
def ship_hit(stats, aliens, bullets, ship, ai_settings, screen, sb):
    if stats.ships_left > 1:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        ai_settings.ship_hit_sound.play()
        sb.prep_ships()
        create_fleet(ai_settings, screen, aliens, ship, stats)
        ship.center()
        time.sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


#------bullets functions
def check_collision(aliens, bullets, ai_settings, screen, ship, sb, stats):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)#if we make it False True the bullets won't disappear
    if len(aliens) == 0 :
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship, stats)
        ai_settings.new_fleet_sound.play()
    if collision:
        stats.score += ai_settings.alien_pounts
        check_high_score(stats, sb)
        sb.prep_score()

def update_bullet(aliens, bullets, ai_settings, screen, ship, sb, stats):
    """ we draw , check collision and remake the fleet """
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    check_collision(aliens, bullets, ai_settings, screen, ship, sb, stats)
    bullets.update()

def delet_bullets(bullets):
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

#-------alien bullets functions------
def create_alien_bullets(stats, alien_bullets, aliens, ai_settings, screen):
    levels5 = check_5levels(stats)
    if levels5:
        if len(alien_bullets) <= ai_settings.alien_bullets_allowed_num:
            for alien in aliens:
                alien_bullet = AlienBullet(ai_settings, screen)
                alien_bullet.rect.centerx = alien.rect.centerx
                alien_bullet.rect.bottom = alien.rect.bottom
                alien_bullet.rect.y = alien.rect.y
                alien_bullets.add(alien_bullet)

def check_aliens_bullets_collision(alien_bullets, stats, aliens, bullets, ship, ai_settings, screen, sb):
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(stats, aliens, bullets, ship, ai_settings, screen, sb)
        alien_bullets.empty()

    for alien_bullet in alien_bullets:
        if alien_bullet.rect.top >= ai_settings.legnth:
            alien_bullets.remove(alien_bullet)

def add_alien_bullets(alien_bullets, stats, aliens, bullets, ship, ai_settings, screen, sb):
    create_alien_bullets(stats, alien_bullets, aliens, ai_settings, screen)
    for alien_bullet in alien_bullets:
        alien_bullet.draw_bullet()
        alien_bullet.update()
    check_aliens_bullets_collision(alien_bullets, stats, aliens, bullets, ship, ai_settings, screen, sb)


#------updating screen function-------
def update_screen(stats, aliens, bullets, ship, ai_settings, screen, play_button, sb, alien_bullets):
    if stats.game_active:
        screen.fill(ai_settings.bg_color)
        update_bullet(aliens, bullets, ai_settings, screen, ship, sb, stats)
        update_alien(stats, aliens, bullets, ship, ai_settings, screen, sb)
        ship.blitme()
        add_alien_bullets(alien_bullets, stats, aliens, bullets, ship, ai_settings, screen, sb)
        sb.draw_score()
    if not stats.game_active:
        screen.fill(ai_settings.bg_color)
        play_button.draw_button()


    pygame.display.flip()
