import pygame
import time
import os

base = os.path.dirname(__file__)

bg = pygame.image.load(os.path.join(base, "images", "mickeyclock.jpg"))
right = pygame.image.load(os.path.join(base, "images", "right_hand.png"))
left = pygame.image.load(os.path.join(base, "images", "left_hand.png"))

right = pygame.transform.scale(right, (120, 300))
left = pygame.transform.scale(left, (120, 300))

CENTER = (370, 280)


def rotate_center(image, angle, center):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=center)
    return rotated, rect


def draw(screen):
    t = time.localtime()
    sec = t.tm_sec
    minute = t.tm_min

    screen.blit(bg, (0, 0))

    minute_angle = -minute * 6
    sec_angle = -sec * 6

    right_rect = right.get_rect(center=CENTER)
    left_rect = left.get_rect(center=CENTER)

    minute_img, minute_rect = rotate_center(right, minute_angle, CENTER)
    sec_img, sec_rect = rotate_center(left, sec_angle, CENTER)

    screen.blit(minute_img, minute_rect)
    screen.blit(sec_img, sec_rect)