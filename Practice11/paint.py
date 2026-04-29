import pygame
import math

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

# 🔥 NEW: previous mouse position
last_pos = None

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # COLORS
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_e:
                color = WHITE

            # MODES
            if event.key == pygame.K_d:
                mode = "draw"
            if event.key == pygame.K_c:
                mode = "circle"
            if event.key == pygame.K_s:
                mode = "rect"

            # NEW SHAPES
            if event.key == pygame.K_q:
                mode = "square"
            if event.key == pygame.K_t:
                mode = "right_triangle"
            if event.key == pygame.K_y:
                mode = "equilateral_triangle"
            if event.key == pygame.K_h:
                mode = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos  # 🔥 важно

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None  # 🔥 сброс

            end_pos = event.pos
            x1, y1 = start_pos
            x2, y2 = end_pos

            # CIRCLE
            if mode == "circle":
                dx = x2 - x1
                dy = y2 - y1
                radius_circle = int((dx**2 + dy**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

            # RECTANGLE
            if mode == "rect":
                rect = pygame.Rect(min(x1,x2), min(y1,y2),
                                   abs(x1-x2), abs(y1-y2))
                pygame.draw.rect(screen, color, rect, 2)

            # SQUARE
            if mode == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                rect = pygame.Rect(x1, y1, side, side)
                pygame.draw.rect(screen, color, rect, 2)

            # RIGHT TRIANGLE
            if mode == "right_triangle":
                points = [(x1, y1), (x2, y1), (x1, y2)]
                pygame.draw.polygon(screen, color, points, 2)

            # EQUILATERAL TRIANGLE
            if mode == "equilateral_triangle":
                side = abs(x2 - x1)
                p1 = (x1, y1)
                p2 = (x1 + side, y1)
                h = int((math.sqrt(3) / 2) * side)
                p3 = (x1 + side // 2, y1 - h)
                pygame.draw.polygon(screen, color, [p1, p2, p3], 2)

            # RHOMBUS
            if mode == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2

                points = [
                    (cx, cy - dy),
                    (cx + dx, cy),
                    (cx, cy + dy),
                    (cx - dx, cy)
                ]
                pygame.draw.polygon(screen, color, points, 2)

        # 🔥 FIXED DRAW (smooth)
        if event.type == pygame.MOUSEMOTION:
            if drawing and mode == "draw":
                pygame.draw.line(screen, color, last_pos, event.pos, radius * 2)
                last_pos = event.pos

    pygame.display.flip()
    clock.tick(60)

pygame.quit()