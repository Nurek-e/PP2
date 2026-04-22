import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,255,0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("pp2/Practice10/images/AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")

game_over_text = font.render("Game Over", True, BLACK)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("pp2/Practice10/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), -20)

    def move(self):
        self.rect.move_ip(0,SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = -20
            self.rect.center = (random.randint(40,SCREEN_WIDTH-40), -20)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("pp2/Practice10/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


def reset_game():
    global SPEED, SCORE, COINS, P1, enemies, coins, all_sprites

    SPEED = 5
    SCORE = 0
    COINS = 0

    P1 = Player()
    E1 = Enemy()
    E2 = Enemy()
    C1 = Coin()

    enemies = pygame.sprite.Group(E1, E2)
    coins = pygame.sprite.Group(C1)

    all_sprites = pygame.sprite.Group(P1, E1, E2, C1)


reset_game()

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

game_over = False

while True:
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == INC_SPEED:
                SPEED += 0.5

        if game_over:
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                    game_over = False

    DISPLAYSURF.blit(background, (0,0))

    if not game_over:

        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound('pp2/Practice10/images/crash.wav').play()
            game_over = True

        if pygame.sprite.spritecollideany(P1, coins):
            COINS += 1
            for coin in coins:
                coin.rect.top = -20
                coin.rect.center = (random.randint(40,SCREEN_WIDTH-40), -20)

    else:
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30,250))

        restart_text = font_small.render("Press R to Restart", True, WHITE)
        DISPLAYSURF.blit(restart_text, (100, 320))

    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)

    DISPLAYSURF.blit(score_text, (10,10))
    DISPLAYSURF.blit(coin_text, (280,10))

    pygame.display.update()
    FramePerSec.tick(FPS)