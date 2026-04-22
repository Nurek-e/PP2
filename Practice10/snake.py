import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

snake = [(100, 100)]
dx, dy = CELL, 0

def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

score = 0
speed = 10

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    head = snake[0]
    new_head = (head[0] + dx, head[1] + dy)

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False

    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        speed += 0.5
        food = generate_food()
    else:
        snake.pop()

    screen.fill((30, 30, 30))

    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (50,50,50), (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (50,50,50), (0,y), (WIDTH,y))

    for i, segment in enumerate(snake):
        color = (0, 255 - i*5, 0)
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL, CELL), border_radius=5)

    pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], CELL, CELL), border_radius=5)

    text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()