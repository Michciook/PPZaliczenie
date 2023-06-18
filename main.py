import pygame
from sys import exit
import math
from settings import *
import random

pygame.init()

# Tworzenie okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realm Of The *** ***")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("Player.png").convert_alpha(), 0, PLAYER_SIZE)
        self.hitbox_rect = self.image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.ability = False
        self.ability_cooldown = 0
        self.current_health = 100
        self.maximum_health = 100
        self.health_bar_length = 400

        self.health_ratio = self.maximum_health / self.health_bar_length

    def basic_health(self):
        pygame.draw.rect(screen, (255, 0, 0), (10,10, self.current_health/self.health_ratio, 25))
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.health_bar_length, 25), 4)

    def player_angle(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_coords[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed

        # obsługa poruszania się po przekątnej
        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

        if keys[pygame.K_SPACE]:
            self.ability = True
            self.ability_use()
        else:
            self.ability = False



    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            self.bullet = Bullet(self.pos[0], self.pos[1], self.angle)
            player_bullet_group.add(self.bullet)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_angle()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        self.basic_health()


class Wizard(Player):
    def ability_use(self):
        if self.ability_cooldown == 0:
            self.ability_cooldown = ABILITY_COOLDOWN
            for i in range(12):
                ability_bullet = Bullet(self.pos[0], self.pos[1], 30*i)
                player_bullet_group.add(ability_bullet)


class Knight(Player):
    def __init__(self):
        Player.__init__(self)
        self.maximum_health = 200
        self.current_health = 200
        self.health_ratio = self.maximum_health / self.health_bar_length
    def ability_use(self):
        if self.ability_cooldown == 0:
            self.ability_cooldown = ABILITY_COOLDOWN
            for i in range(3):
                ability_bullet = Bullet(self.pos[0], self.pos[1], self.angle-30 + (i * 15))
                player_bullet_group.add(ability_bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__(all_sprites_group)
        self.image = pygame.image.load("Bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.x_vel = math.cos(self.angle * (2*math.pi/360)) * self.speed
        self.y_vel = math.sin(self.angle * (2*math.pi/360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = ENEMY_SPEED

        self.position = pygame.math.Vector2(position)
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        self.distance = self.get_vector_distance(player_vector, enemy_vector)

        if self.distance > 200:
            self.direction = (player_vector - enemy_vector).normalize()

        else:
            self.direction = pygame.math.Vector2()

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def is_shooting(self):
        if self.shoot_cooldown == 0 and self.distance < 400:
            self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
            bullet = Bullet(self.position[0], self.position[1],
                            math.degrees(math.atan2(player.hitbox_rect.center[1] - self.position[1],
                                                    player.hitbox_rect.center[0] - self.position[0])))
            enemy_bullet_group.add(bullet)

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def _add_enemy(self):
        if random.randint(0, 1) == 1:
            self.enemy = Enemy((player.pos[0] + random.randint(500,1000),
                                player.pos[1] + random.randint(500,1000)))
        else:
            self.enemy = Enemy((player.pos[0] - random.randint(500, 1000),
                                player.pos[1] - random.randint(500, 1000)))

    def update(self):
        self.hunt_player()
        if random.randint(1, 120) == 1 and len(enemy_group) < 15:
            self._add_enemy()

        self.is_shooting()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


camera = Camera()
player = Knight()

all_sprites_group = pygame.sprite.Group()
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

all_sprites_group.add(player)

enemy = Enemy((1000,1000))

color = (10, 150, 70)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(color)

    camera.custom_draw()
    all_sprites_group.update()

    for bullet in player_bullet_group:
        hit = pygame.sprite.spritecollide(bullet, enemy_group, False)
        for enemys in hit:
            enemys.kill()
            bullet.kill()

    player_hit = pygame.sprite.spritecollide(player, enemy_bullet_group, False)
    for bullet in player_hit:
        player.current_health -= 10
        bullet.kill()

    if player.current_health <= 0:
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(FPS)
