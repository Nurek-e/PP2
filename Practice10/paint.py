import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen.fill(WHITE)

clock = pygame.time.Clock()

color = BLACK
radius = 5
mode = "draw"

drawing = False
start_pos = None

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_e:
                color = WHITE
            if event.key == pygame.K_d:
                mode = "draw"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_s:
                mode = "rect"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "circle":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                radius_circle = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

            if mode == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1,x2), min(y1,y2),
                                   abs(x1-x2), abs(y1-y2))
                pygame.draw.rect(screen, color, rect, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing and mode == "draw":
                pygame.draw.circle(screen, color, event.pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()