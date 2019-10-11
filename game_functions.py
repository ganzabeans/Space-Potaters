import sys
from time import sleep
import pygame
import random
import pygame.mask

from bullet import Bullet
from alien import Alien
from alien_bullet import Abullet
from mini_boom import Mini_Boom
from bunker import Bunker


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, a_bullets, background, bunker, high_score_button,
                 back_button):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if stats.game_active:
                stats.save_high_score(stats.score)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, ship,
                                 bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, a_bullets, mouse_x,
                              mouse_y, background, bunker)
            check_hs_button(stats, sb, mouse_x, mouse_y, background,
                            high_score_button)
            check_back_button(stats, sb, mouse_x, mouse_y, background,
                              back_button)


def check_back_button(stats, sb, mouse_x, mouse_y,
                      background, back_button):
    """Display stats when player clicks high scores button"""
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and stats.check_hs:
        # change show scores bool to false
        stats.check_hs = False
        # switch to start screen
        background.switch_to(0)


def check_hs_button(stats, sb, mouse_x, mouse_y,
                    background, high_score_button):
    """Display stats when player clicks high scores button"""
    button_clicked = high_score_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.check_hs:
        # change show scores bool to true
        stats.check_hs = True
        # display high scores
        sb.prep_hs()
        # set background screen
        background.switch_to(1)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, a_bullets, mouse_x, mouse_y,
                      background, bunker):
    """Start a new game when player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and not stats.check_hs:
        # restart game settings
        ai_settings.initialize_dynamic_settings()

        # Hide mouse
        pygame.mouse.set_visible(False)
        # restart game stats
        stats.reset_stats()
        stats.game_active = True

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty group sprites
        aliens.empty()
        bullets.empty()
        a_bullets.empty()
        bunker.empty()

        # create a new fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Crete bunkers
        for letter in ai_settings.potato:
            bunker.add(Bunker(ai_settings, screen, letter))
        # set background screen
        background.switch_to(1)


def check_keydown_events(event, ai_settings, stats, sb, screen, ship, bullets):
    """respond to keypress"""
    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        if stats.game_active:
            stats.save_high_score(stats.score)
        sys.exit()
    if not ship.explosion:
        if event.key == pygame.K_RIGHT:
            # move ship to the right
            ship.moving_right = True
        if event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """respond to key release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  a_bullets, play_button, timer, bunker, background,
                  high_score_button, back_button, kabooms, ufo):
    """ Update images on the sceen and flip to the new screen """
    # fill screen
    screen.fill(ai_settings.bg_color)

    # update background
    background.blitme()

    if stats.game_active:
        # bunker
        for sack in bunker.sprites():
            sack.blitme()

        # Redraw all bullets behind ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for a_bullet in a_bullets.sprites():
            a_bullet.draw_a_bullet()
        # Ship
        if ship.explosion:
            ship.ship_animate(ai_settings, timer)
        else:
            ship.blitme()
        # redraw aliens
        for alien in aliens.sprites():
            alien.alien_animate(ai_settings, timer)

        # redraw ufo
        ufo.update()
        if ufo.active:
            ufo.blitme()

        # draw explosion!
        for boom in kabooms.sprites():
            if boom.active:
                boom.mini_boom(ai_settings, timer)
                boom.blitme()
            else:
                kabooms.remove(boom)

        # turn off ufo score for sb
        if ufo.x > 3600:
            sb.ufo_score = False
        # Draw score info
        sb.show_score()

    # draw play button and high score buttonat start
    if not stats.game_active:
        if not stats.check_hs:
            play_button.draw_button()
            high_score_button.draw_button()
            if background.b_type == 1:
                sb.display_end_score()
        else:
            # show back button on displaying high scores
            back_button.draw_button()
            sb.display_high_scores()

    pygame.display.flip()


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


""" SHIP METHODS """


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
             a_bullets, bunker, timer, full_reset):
    """Respond to ship being hit by alien"""
    # 1st check invinsibility
    if not ship.invinsible:

        if stats.ships_left > 0:

            # ship animation
            ship.set_explosion()
            ship.ship_animate(ai_settings, timer)

            # Decrement ships_left
            stats.ships_left -= 1

            # update scoreboard
            sb.prep_ships()

            # Empty bullet list
            bullets.empty()

            # Empty the list of aliens and a_bullets if full reset
            if full_reset:
                aliens.empty()
                a_bullets.empty()
                # Create a new fleet and center the ship
                create_fleet(ai_settings, screen, ship, aliens)
                # save high score if needed
                stats.save_high_score(stats.score)

        else:
            stats.game_active = False
            # set mouse visible
            pygame.mouse.set_visible(True)
            stats.save_high_score(stats.score)


""" BULLET METHODS """


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create new bullet and add to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
                   a_bullets, bunker, kabooms, ufo):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Destroy bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # destorys if aliens and bullets make contact
    check_bullet_alien_collissions(ai_settings, screen, stats, sb, ship,
                                   aliens, bullets, a_bullets, kabooms)

    # destroys bullet on alien's bullet collisions
    check_bullet_collisions(ai_settings, screen, stats, sb, ship,
                            aliens, bullets, a_bullets, kabooms)

    # destorys bunker if hits
    check_bullet_bunker_collissions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, a_bullets, bunker,
                                    kabooms)
    # destory ufo if hits
    check_bullet_ufo_collision(sb, stats, bullets, ufo)


def check_bullet_ufo_collision(sb, stats, bullets, ufo):
    if pygame.sprite.spritecollideany(ufo, bullets):
        ufo_position = ufo.rect.center
        points = random.randint(1, 5) * 100
        sb.ufo_points(points, ufo_position)
        stats.score += points
        ufo.x = 3000


def check_bullet_bunker_collissions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, a_bullets, bunker,
                                    kabooms):
    """Respond to bullet bunker collision"""
    for bullet in bullets.copy():
        for sack in bunker.copy():
            b_coordinate = pygame.sprite.collide_mask(sack, bullet)
            if b_coordinate:
                kabooms.add(Mini_Boom(ai_settings, screen,
                                      (bullet.rect.x - 23,
                                       bullet.rect.y - 30)))
                bullets.remove(bullet)
                bunker_hit(b_coordinate, sack, direction=-1,
                           ai_settings=ai_settings)


def check_bullet_alien_collissions(ai_settings, screen, stats, sb, ship,
                                   aliens, bullets, a_bullets, kabooms):
    """Respond to alien w bullet collision"""
    # if so, get rid of bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                kabooms.add(Mini_Boom(ai_settings, screen, alien.rect.topleft))
                stats.score += (alien.get_value() + 10 * (stats.level - 1))
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # if entire fleet is destoryed, start a new level
        bullets.empty()
        a_bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

        # increase level
        stats.level += 1
        ai_settings.increase_speed()
        sb.prep_level()


def check_bullet_collisions(ai_settings, screen, stats, sb, ship,
                            aliens, bullets, a_bullets, kabooms):
    """Respond to bullet w alien bullet collision"""
    # if so, get rid of bullet and the allien bullet
    collisions = pygame.sprite.groupcollide(bullets, a_bullets, True, True)
    if collisions:
        for bullets in collisions.values():
            for bullet in bullets:
                kabooms.add(Mini_Boom(ai_settings, screen,
                                      (bullet.rect.x - 23,
                                       bullet.rect.y - 30)))


""" ALIEN METHODS """


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  a_bullets, bunker, timer):
    """
    Check if the fleet is at an edge, and
    then Update the positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisons
    if pygame.sprite.spritecollideany(ship, aliens):
        full_reset = True
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
                 a_bullets, bunker, timer, full_reset)

    # look for aliens hitting bottom of screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets,
                        a_bullets, bunker, timer)

    # launch alien bullets
    if timer.a_bullet_dict['switch']:
        fire_alien_bullet(ai_settings, screen, stats, aliens, a_bullets)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of alieans that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    # set type of alien based on row
    if row_number < 3:
        alien_type = row_number
    else:
        alien_type = 2
    # set animation state based on position
    anim_start = alien_number % 2
    alien = Alien(ai_settings, screen, alien_type, anim_start)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alean and find the number of aliens in a row
    alien = Alien(ai_settings, screen, 1, 0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets,
                        a_bullets, bunker, timer):
    """ Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            full_reset = True
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
                     a_bullets, bunker, timer, full_reset)
            break


""" ALIEN BULLET METHODS """


def fire_alien_bullet(ai_settings, screen, stats, aliens, a_bullets):
    # as level goes up, alien, rate of bullets increases
    for n in range(stats.level):
        for alien in aliens.sprites():
            pick_alien = random.randint(0, len(aliens))
            if pick_alien == 0:
                new_a_bullet = Abullet(ai_settings, screen, alien.rect.centerx,
                                       alien.rect.bottom)
                a_bullets.add(new_a_bullet)
                break


def update_a_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
                     a_bullets, bunker, timer):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    a_bullets.update()

    # Destroy bullets that have disappeared
    for a_bullet in a_bullets.copy():
        if a_bullet.rect.top >= ai_settings.screen_height:
            a_bullets.remove(a_bullet)

    check_a_bullet_ship_collissions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, a_bullets, bunker, timer)

    check_a_bullet_bunker_collissions(ai_settings, screen, stats, sb, ship,
                                      aliens, bullets, a_bullets, bunker)


def check_a_bullet_ship_collissions(ai_settings, screen, stats, sb, ship,
                                    aliens, bullets, a_bullets, bunker, timer):
    """Respond to ship w alien bullet collision"""
    # if so, get rid of bullet and the ship, don't restart aliens
    collisions = pygame.sprite.spritecollide(ship, a_bullets, True)
    if collisions:
        full_reset = False
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets,
                 a_bullets, bunker, timer, full_reset)


def check_a_bullet_bunker_collissions(ai_settings, screen, stats, sb, ship,
                                      aliens, bullets, a_bullets, bunker):
    """Respond to bullet bunker collision"""
    for a_bullet in a_bullets.copy():
        for sack in bunker.copy():
            b_coordinate = pygame.sprite.collide_mask(sack, a_bullet)
            if b_coordinate:
                a_bullets.remove(a_bullet)
                bunker_hit(b_coordinate, sack, direction=1,
                           ai_settings=ai_settings)


""" Bunker functions """


def bunker_hit(b_coordinate, sack, direction, ai_settings):
    # Sets range of which pixels to destroy
    x, y = b_coordinate[0], b_coordinate[1]

    # adjust for offset
    y += ai_settings.bunker_bullet_offset * direction

    # set max y range
    # test for bullets going down
    if y == sack.height and direction == 1:
        y_range = (0, 0)
    # test for bullets going up
    elif y == 0 and direction == -1:
        y_range = 0
    else:
        y_range = bunker_set_y_max(y, sack, direction, ai_settings)

    # set max x range
    if x == 0:
        x_L_range = 0
    elif x == sack.width:
        x_R_range = 0
    else:
        x_L_range = bunker_set_x(x, sack, direction=ai_settings.bunker_left,
                                 ai_settings=ai_settings)
        x_R_range = bunker_set_x(x, sack, direction=ai_settings.bunker_right,
                                 ai_settings=ai_settings)

    # send coordinates and range to bunker
    sack.destory_self(x, y, y_range, xmin=x_L_range, xmax=x_R_range,
                      direction=direction)


def bunker_set_y_max(y, sack, direction, ai_settings):
    """Sets range of deletion for y values in bunker"""
    bunker_max = ai_settings.bunker_max
    # for alien bullets, set range in bounds
    if direction == 1:
        if (bunker_max + y) <= sack.height:
            return bunker_max
        while(bunker_max + y) > sack.height:
            bunker_max -= bunker_max
        return bunker_max
    # for player bullets, set range in bounds
    if direction == -1:
        if (y - bunker_max) >= 0:
            return bunker_max
        while (y - bunker_max) < 0:
            bunker_max -= bunker_max
        return bunker_max

    # default if falls through
    return bunker_max


def bunker_set_x(x, sack, direction, ai_settings):
    """Sets range of deletion for x values in bunker"""
    bunker_max = ai_settings.bunker_max
    # for right bullets, set range in bounds
    if direction == 1:
        if (bunker_max + x) <= sack.width:
            return bunker_max
        while(bunker_max + x) > sack.width:
            bunker_max -= bunker_max
        return bunker_max
    # for left bullets, set range in bounds
    if direction == -1:
        if (x - bunker_max) >= 0:
            return bunker_max
        while (x - bunker_max) < 0:
            bunker_max -= bunker_max
        return bunker_max

    # default if falls through
    return bunker_max
