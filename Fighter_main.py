import sys
from Fighter_class import *
import time
import pygame.freetype
import pygame_menu

BLUE_Bullet = (0, 0, 255)
RED_Bullet = (255, 0, 0)


def game_over_screen(score):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    game_over = pygame_menu.Menu("Game over", 400, 300, theme=pygame_menu.themes.THEME_DEFAULT)
    game_over.add.label(f"Score: {score}")

    game_over.add.button("Quit", pygame_menu.events.EXIT)
    game_over.add.button("Restart", game_cycle)
    game_over.mainloop(screen)


def game_cycle():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((600, 600))
    background = pygame.transform.scale(pygame.image.load("Fighters/o_1b61g3upo10mv9a9fc1ogeq7i9.jpg"), (600, 600))

    add_enemy = pygame.USEREVENT + 1
    add_boost = pygame.USEREVENT + 2

    score_font = pygame.freetype.SysFont("Arial", 20)
    Health_font = pygame.freetype.SysFont("Arial", 20)

    pygame.time.set_timer(add_boost, 500)
    pygame.time.set_timer(add_enemy, 200)

    player = Player()

    # Initializing sprite groups

    bullets_boosts = pygame.sprite.Group()
    health_boosts = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    score_boosts = pygame.sprite.Group()
    explosion = pygame.sprite.Group()
    enemy_ships = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    all_sprites.add(player)

    # Initial values of variables

    double = False
    timer_boost_bullet = 0
    timer_boost_score = 0
    Score = 0
    bonus = 0
    boosted = 1
    time_all = time.perf_counter()
    time_fire_enemy_ships = time.perf_counter()
    while True:
        time_start = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE and double:  # Implementation of a double shot
                    bullet = Bullet(player.pos_x() - 10, player.pos_y(), BLUE_Bullet)
                    bullet_2 = Bullet(player.pos_x() + 10, player.pos_y(), BLUE_Bullet)
                    bullets.add(bullet_2)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    all_sprites.add(bullet_2)

                elif event.key == pygame.K_SPACE:  # Single shot
                    bullet = Bullet(player.pos_x(), player.pos_y(), BLUE_Bullet)
                    bullets.add(bullet)
                    all_sprites.add(bullet)

            elif event.type == add_enemy:
                i = random.randint(1, 2)
                if i == 1:
                    enemy = Enemy()
                    enemies.add(enemy)
                    all_sprites.add(enemy)
                if i == 2:
                    enemy = Enemy_ships()
                    enemy_ships.add(enemy)
                    all_sprites.add(enemy)

            elif event.type == add_boost:
                i = random.randint(1, 3)  # Random selection of the type of boost
                if i == 1:
                    boost = Health()
                    health_boosts.add(boost)
                    all_sprites.add(boost)
                if i == 2:
                    boost = Rise_bullet()
                    bullets_boosts.add(boost)
                    all_sprites.add(boost)
                if i == 3:
                    boost = Score_boost()
                    score_boosts.add(boost)
                    all_sprites.add(boost)

        # Processing button clicks for movement
        key = pygame.key.get_pressed()

        player.up(key)

        # Updating the position of all groups

        all_sprites.update()

        if time.perf_counter() - time_fire_enemy_ships > 0.4:
            time_fire_enemy_ships = time.perf_counter()
            for e in enemy_ships:
                enemy_bullet = Bullet(e.rect.x, e.rect.y, RED_Bullet, False)
                enemy_bullets.add(enemy_bullet)
                all_sprites.add(enemy_bullet)
        explosion.update()

        clock.tick(60)

        screen.blit(background, (0, 0))

        score_font.render_to(screen, (X_max / 2 - 50, 30), f"Score: {round(Score)}", (240, 255, 240))
        Health_font.render_to(screen, (X_max / 2 - 40, 550), f"Health: {player.health}", (240, 255, 240))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        explosion.draw(screen)
        # Collision with objects

        if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle):
            expl = Explosion(player.rect.center)
            explosion.add(expl)
            if player.health - 1 == 0:
                print("Game over")
                print(Score)
                print(time.perf_counter() - time_all)
                print(bonus)
                game_over_screen(round(Score))
            else:
                player.health = player.health - 1
                print("You damaged")

        if pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle):
            expl = Explosion(player.rect.center)
            explosion.add(expl)
            if player.health - 1 == 0:
                print("Game over")
                print(Score)
                print(time.perf_counter() - time_all)
                print(bonus)
                game_over_screen(round(Score))
            else:
                player.health = player.health - 1
                print("You damaged")

        if pygame.sprite.spritecollide(player, enemy_ships, True, pygame.sprite.collide_circle):
            expl = Explosion(player.rect.center)
            explosion.add(expl)
            if player.health - 1 == 0:
                print("Game over")
                print(Score)
                print(time.perf_counter() - time_all)
                print(bonus)
                game_over_screen(round(Score))
            else:
                player.health = player.health - 1
                print("You damaged")

        # Taking boosts and getting bonuses

        if pygame.sprite.spritecollide(player, health_boosts, True, pygame.sprite.collide_circle):
            if player.health < 3:
                player.health += 1
                print("You healthy")
            else:
                print("You health is full")

        if pygame.sprite.spritecollide(player, bullets_boosts, True, pygame.sprite.collide_circle):
            print("You boosted bullets")
            double = True
            timer_boost_bullet = time.perf_counter()
        if time.perf_counter() - timer_boost_bullet >= 2:
            double = False

        if pygame.sprite.spritecollide(player, score_boosts, True, pygame.sprite.collide_circle):
            print("You boosted score")
            boosted = 2
        if time.perf_counter() - timer_boost_score >= 5:
            boosted = 1

        expl = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for ex in expl:
            bonus += 10
            expl = Explosion(ex.rect.center)
            explosion.add(expl)

        expl = pygame.sprite.groupcollide(bullets, enemy_ships, True, True)
        for ex in expl:
            bonus += 50
            expl = Explosion(ex.rect.center)
            explosion.add(expl)

        expl = pygame.sprite.groupcollide(enemies, enemy_ships, True, True)
        for ex in expl:
            expl = Explosion(ex.rect.center)
            explosion.add(expl)

        # Calculation of score

        Score = (time.perf_counter() - time_start) * 100 * boosted + bonus + Score
        pygame.display.flip()
