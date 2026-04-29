import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 600, 600

# Size of one cell in the grid
CELL = 20

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro")

# Clock controls the game speed
clock = pygame.time.Clock()

# Font for score and level text
font = pygame.font.SysFont("Verdana", 20)

# Snake starts with one block
snake = [(100, 100)]

# Initial movement direction: right
dx, dy = CELL, 0

# Initial score
score = 0

# Initial level
level = 1

# Initial snake speed
speed = 10

# Every 4 food items, level increases
FOOD_FOR_NEXT_LEVEL = 4

# ===== NEW: food lifetime (milliseconds) =====
FOOD_LIFETIME = 5000  # 5 seconds


# Function to generate food with weight
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:

            # ===== NEW: random weight =====
            weight = random.choice([1, 2, 3])

            # ===== NEW: color based on weight =====
            if weight == 1:
                color = (255, 0, 0)      # red
            elif weight == 2:
                color = (255, 255, 0)    # yellow
            else:
                color = (0, 0, 255)      # blue

            # ===== NEW: spawn time =====
            spawn_time = pygame.time.get_ticks()

            return (x, y, weight, color, spawn_time)


# Generate the first food
food = generate_food()

running = True

# Main game loop
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

    # Wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False

    # Self collision
    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    # ===== NEW: unpack food =====
    fx, fy, weight, color, spawn_time = food

    # ===== NEW: food timer check =====
    current_time = pygame.time.get_ticks()
    if current_time - spawn_time > FOOD_LIFETIME:
        # food disappears and respawns
        food = generate_food()

    # Eat food
    if new_head == (fx, fy):
        # ===== NEW: add weight instead of +1 =====
        score += weight

        food = generate_food()

        if score % FOOD_FOR_NEXT_LEVEL == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw background
    screen.fill((30, 30, 30))

    # Grid
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

    # Draw snake
    for i, segment in enumerate(snake):
        green_value = max(80, 255 - i * 5)
        color_snake = (0, green_value, 0)

        pygame.draw.rect(
            screen,
            color_snake,
            (segment[0], segment[1], CELL, CELL),
            border_radius=5
        )

    # ===== NEW: draw food with color =====
    pygame.draw.rect(
        screen,
        color,
        (fx, fy, CELL, CELL),
        border_radius=5
    )

    # Text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()