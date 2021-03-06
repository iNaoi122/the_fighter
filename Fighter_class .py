import pygame
import random
import pygame.freetype

X_max = 600
Y_max = 600
speed = int(10)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("Fighters/276274ea71933f0.png").convert(),
                                           (80, 80))
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                X_max / 2,
                490
            )
        )
        self.radius = 20
        # pygame.draw.circle(self.surf, (255, 0, 0), (40, 40), self.radius)
        self.health = 3

    def _move_rect(self, x, y):
        if self.rect.left + x < 0:
            self.rect.left = 0
        elif self.rect.right + x > X_max:
            self.rect.right = X_max
        elif self.rect.top + y < 0:
            self.rect.top = 0
        elif self.rect.bottom + y > Y_max:
            self.rect.bottom = Y_max
        else:
            self.rect.move_ip(x, y)

    def up(self, keys):
        if keys[pygame.K_LEFT]:
            self._move_rect(-speed, 0)
        if keys[pygame.K_RIGHT]:
            self._move_rect(speed, 0)

    def pos_x(self):
        return self.rect.x

    def pos_y(self):
        return self.rect.y

    def shield(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("3573081378.png").convert(), (50, 50))

        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, X_max),
                0
            )
        )
        self.radius = 14
        # pygame.draw.circle(self.surf, (255, 0, 0), (25, 25), self.radius)
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > Y_max:
            self.kill()


class Enemy_ships(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy_ships, self).__init__()
        self.speed = random.randint(1, 8)
        self.surf = pygame.transform.scale(
            pygame.image.load("Fighters/4415f4cb720fa4339dec3272527f16e2--star-wars-ships-star-wars-art.jpg").convert(),
            (30, 30))
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, X_max),
                0
            )
        )
        self.radius = 10
        # pygame.draw.circle(self.surf, (255, 0, 0), (15, 15), self.radius)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > Y_max:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_0, y_0, color, player=True, double=False):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((4, 10))
        self.surf.fill(color)
        if double:
            self.rect = self.surf.get_rect(
                center=(x_0 + 10, y_0)
            )
            self.rect = self.surf.get_rect(
                center=(x_0 + 30, y_0)
            )

        if player:
            self.speed = 10
            self.rect = self.surf.get_rect(
                center=(x_0 + 40, y_0)
            )
        else:
            self.rect=self.surf.get_rect(
                center=(x_0+15, y_0+10)
            )
            self.speed = -10

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()


class Boost(pygame.sprite.Sprite):
    def __init__(self):
        super(Boost, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, X_max),
                0
            )
        )
        self.speed = 5

    # 1 - health 2 - double bullet
    # 3 - x2 - score

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > Y_max:
            self.kill()

    def destroy(self):
        self.kill()


class Health(Boost):
    def __init__(self):
        super(Health, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, X_max),
                0
            )
        )


class Rise_bullet(Boost):
    def __init__(self):
        super(Rise_bullet, self).__init__()
        self.surf.fill((255, 0, 255))


class Score_boost(Boost):
    def __init__(self):
        super(Score_boost, self).__init__()
        self.surf.fill((0, 255, 0))


class Button:
    def __init__(self, x, y, color, size_x, size_y, text):
        self.color = color
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.text = text

    def draw(self, area):
        pygame.draw.rect(area, self.color, (self.x, self.y, self.size_x, self.size_y), 0)

        font = pygame.freetype.SysFont("Arial", 40)

        font.render_to(area, (self.x + 10, self.y + (self.size_y - 40) / 2), "Start", (240, 255, 240))

    def click(self, pos):
        if self.x < pos[0] < self.x + self.size_x:
            if self.y < pos[1] < self.y + self.size_y:
                return True

        return False


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.ex_anim = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(f"Fighters/Explosive/{filename}").convert()
            img = pygame.transform.scale(img, (50, 50))
            img.set_colorkey((0, 0, 0))
            self.ex_anim.append(img)
        self.image = self.ex_anim[0]
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.ex_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.ex_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
