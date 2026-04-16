import clock
import pygame

pygame.init()


screen=pygame.display.set_mode((600,600))
pygame.display.set_caption("Mickey Clock")

fps=pygame.time.Clock()

running=True
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    clock.draw(screen)
    pygame.display.flip()
    fps.tick(60)
pygame.quit()