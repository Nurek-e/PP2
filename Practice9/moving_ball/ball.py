import pygame
x=300
y=300
radius=25
speed=20

def move(key):
    global x,y
    if key==pygame.K_RIGHT:
          if x+radius+speed<=600:
           x+=speed
    
    if key==pygame.K_LEFT:
        if x-radius-speed>=0:
            x-=speed

    if key==pygame.K_UP:
        if y-radius-speed>=0:
            y-=speed

    if key==pygame.K_DOWN:
          if y+radius+speed<=600:
           y+=speed


def draw(screen):
    pygame.draw.circle(screen, ('Red'), (x, y), radius)