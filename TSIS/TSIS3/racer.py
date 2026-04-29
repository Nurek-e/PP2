import pygame
import random
import os
from persistence import add_score


WIDTH = 500
HEIGHT = 700

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)

LANES = [110, 190, 270, 350]

FINISH_DISTANCE = 3000


def load_image(path, size, fallback_color):
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, size)
        return image

    image = pygame.Surface(size)
    image.fill(fallback_color)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()

        self.image = load_image("assets/Player.png", (45, 80), BLUE)

        if color_name == "red":
            self.image.fill(RED)
        elif color_name == "green":
            self.image.fill(GREEN)
        elif color_name == "yellow":
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)

        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 60:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 60:
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.image = load_image("assets/Enemy.png", (45, 80), RED)
        self.rect = self.image.get_rect()

        self.speed = speed
        self.respawn([])

    def respawn(self, blocked_rects):
        safe = False

        while not safe:
            self.rect.center = (random.choice(LANES), random.randint(-500, -80))
            safe = True

            for rect in blocked_rects:
                if self.rect.colliderect(rect):
                    safe = False

    def move(self):
        self.rect.y += self.speed


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.size = 22
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.weight = 1
        self.respawn([])

    def respawn(self, blocked_rects):
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            color = YELLOW
        elif self.weight == 2:
            color = GREEN
        else:
            color = ORANGE

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, color, (self.size // 2, self.size // 2), self.size // 2)

        safe = False

        while not safe:
            self.rect.center = (random.choice(LANES), random.randint(-400, -40))
            safe = True

            for rect in blocked_rects:
                if self.rect.colliderect(rect):
                    safe = False

    def move(self, speed):
        self.rect.y += speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind, speed):
        super().__init__()

        self.kind = kind
        self.speed = speed

        self.image = pygame.Surface((55, 40))

        if self.kind == "barrier":
            self.image.fill(RED)
        elif self.kind == "oil":
            self.image.fill(BLACK)
        else:
            self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-600, -80))

    def move(self):
        self.rect.y += self.speed


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind, speed):
        super().__init__()

        self.kind = kind
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 6000

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if self.kind == "nitro":
            color = BLUE
        elif self.kind == "shield":
            color = PURPLE
        else:
            color = GREEN

        pygame.draw.circle(self.image, color, (15, 15), 15)

        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-500, -60))

    def move(self):
        self.rect.y += self.speed

    def expired(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.life_time


class RacerGame:
    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Verdana", 20)
        self.big_font = pygame.font.SysFont("Verdana", 45)

        self.background_y1 = 0
        self.background_y2 = -HEIGHT

        if os.path.exists("assets/AnimatedStreet.png"):
            self.background = pygame.image.load("assets/AnimatedStreet.png").convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        else:
            self.background = None

        self.sound = None
        if os.path.exists("assets/crash.wav"):
            self.sound = pygame.mixer.Sound("assets/crash.wav")

        self.reset()

    def reset(self):
        difficulty = self.settings["difficulty"]

        if difficulty == "easy":
            self.base_speed = 4
            self.spawn_limit = 2
        elif difficulty == "hard":
            self.base_speed = 7
            self.spawn_limit = 4
        else:
            self.base_speed = 5
            self.spawn_limit = 3

        self.game_speed = self.base_speed

        self.player = Player(self.settings["car_color"])

        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.coins.add(Coin())
        self.all_sprites.add(self.coins)

        for i in range(2):
            enemy = Enemy(self.game_speed)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        self.score = 0
        self.coins_count = 0
        self.distance = 0

        self.active_power = None
        self.power_end_time = 0
        self.has_shield = False

        self.last_obstacle_spawn = pygame.time.get_ticks()
        self.last_power_spawn = pygame.time.get_ticks()

        self.finished = False
        self.game_over = False
        self.saved = False

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, self.background_y1))
            self.screen.blit(self.background, (0, self.background_y2))
        else:
            self.screen.fill((70, 70, 70))

            pygame.draw.rect(self.screen, (50, 50, 50), (70, 0, 360, HEIGHT))

            for lane_x in LANES:
                pygame.draw.line(self.screen, WHITE, (lane_x + 40, 0), (lane_x + 40, HEIGHT), 2)

        self.background_y1 += self.game_speed
        self.background_y2 += self.game_speed

        if self.background_y1 >= HEIGHT:
            self.background_y1 = -HEIGHT

        if self.background_y2 >= HEIGHT:
            self.background_y2 = -HEIGHT

    def spawn_obstacles(self):
        current_time = pygame.time.get_ticks()

        delay = max(700, 1800 - self.distance // 5)

        if current_time - self.last_obstacle_spawn > delay:
            if len(self.obstacles) < self.spawn_limit:
                kind = random.choice(["barrier", "oil", "pothole"])
                obstacle = Obstacle(kind, self.game_speed)

                if abs(obstacle.rect.centerx - self.player.rect.centerx) < 50:
                    obstacle.rect.y -= 250

                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)

            self.last_obstacle_spawn = current_time

    def spawn_powerups(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_power_spawn > 7000:
            if len(self.powerups) == 0 and self.active_power is None:
                kind = random.choice(["nitro", "shield", "repair"])
                power = PowerUp(kind, self.game_speed)
                self.powerups.add(power)
                self.all_sprites.add(power)

            self.last_power_spawn = current_time

    def apply_powerup(self, power):
        if power.kind == "nitro":
            self.active_power = "nitro"
            self.power_end_time = pygame.time.get_ticks() + 4000
            self.game_speed += 4

        elif power.kind == "shield":
            self.active_power = "shield"
            self.has_shield = True

        elif power.kind == "repair":
            self.score += 50

            for obstacle in self.obstacles:
                obstacle.kill()
                break

    def update_powerup_timer(self):
        if self.active_power == "nitro":
            if pygame.time.get_ticks() > self.power_end_time:
                self.game_speed = self.base_speed + self.coins_count // 5
                self.active_power = None

    def check_collisions(self):
        enemy_hit = pygame.sprite.spritecollideany(self.player, self.enemies)

        if enemy_hit:
            if self.has_shield:
                self.has_shield = False
                self.active_power = None
                enemy_hit.respawn([])
            else:
                self.end_game()

        obstacle_hit = pygame.sprite.spritecollideany(self.player, self.obstacles)

        if obstacle_hit:
            if obstacle_hit.kind == "oil":
                self.player.speed = 3
                obstacle_hit.kill()

            elif obstacle_hit.kind == "pothole":
                self.score = max(0, self.score - 20)
                obstacle_hit.kill()

            elif obstacle_hit.kind == "barrier":
                if self.has_shield:
                    self.has_shield = False
                    self.active_power = None
                    obstacle_hit.kill()
                else:
                    self.end_game()

        coin_hit = pygame.sprite.spritecollideany(self.player, self.coins)

        if coin_hit:
            self.coins_count += coin_hit.weight
            self.score += coin_hit.weight * 10

            if self.coins_count % 5 == 0:
                self.base_speed += 1
                self.game_speed += 1

            coin_hit.respawn([])

        power_hit = pygame.sprite.spritecollideany(self.player, self.powerups)

        if power_hit:
            if self.active_power is None or power_hit.kind == "repair":
                self.apply_powerup(power_hit)
                power_hit.kill()

    def update_sprites(self):
        self.player.speed = 7
        self.player.move()

        for enemy in self.enemies:
            enemy.speed = self.game_speed
            enemy.move()

            if enemy.rect.top > HEIGHT:
                self.score += 5
                enemy.respawn([])

        for coin in self.coins:
            coin.move(self.game_speed)

            if coin.rect.top > HEIGHT:
                coin.respawn([])

        for obstacle in self.obstacles:
            obstacle.speed = self.game_speed
            obstacle.move()

            if obstacle.rect.top > HEIGHT:
                obstacle.kill()

        for power in self.powerups:
            power.speed = self.game_speed
            power.move()

            if power.rect.top > HEIGHT or power.expired():
                power.kill()

    def update_distance_and_difficulty(self):
        self.distance += self.game_speed // 2

        if self.distance % 500 < 5:
            if len(self.enemies) < self.spawn_limit:
                enemy = Enemy(self.game_speed)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.end_game()

    def draw_ui(self):
        remaining = max(0, FINISH_DISTANCE - self.distance)

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        coins_text = self.font.render("Coins: " + str(self.coins_count), True, WHITE)
        distance_text = self.font.render("Distance: " + str(self.distance), True, WHITE)
        remaining_text = self.font.render("Finish in: " + str(remaining), True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(coins_text, (10, 35))
        self.screen.blit(distance_text, (10, 60))
        self.screen.blit(remaining_text, (10, 85))

        if self.active_power:
            if self.active_power == "nitro":
                left = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
                text = "Power: Nitro " + str(left) + "s"
            elif self.active_power == "shield":
                text = "Power: Shield active"
            else:
                text = "Power: None"

            power_text = self.font.render(text, True, YELLOW)
            self.screen.blit(power_text, (260, 10))

    def end_game(self):
        if not self.saved:
            total_score = self.score + self.distance // 10 + self.coins_count * 5

            if self.finished:
                total_score += 300

            self.score = total_score
            add_score(self.username, self.score, self.distance, self.coins_count)
            self.saved = True

        self.game_over = True

    def run_frame(self):
        self.draw_background()

        if not self.game_over:
            self.spawn_obstacles()
            self.spawn_powerups()
            self.update_sprites()
            self.check_collisions()
            self.update_powerup_timer()
            self.update_distance_and_difficulty()

            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, sprite.rect)

            self.draw_ui()

        return self.game_over