import pygame
clock=pygame.time.Clock()

pygame.init()
screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("Nureke's game")
icon=pygame.image.load('pp2/images/icon.png')
pygame.display.set_icon(icon)




bg=pygame.image.load('pp2/images/R.png')
bg_x=0

character_speed=5
character_x=150
character_y=560
is_jump=False
jump_count=7
walk_right=[
    pygame.image.load('pp2/character/right/r1.png'),
    pygame.image.load('pp2/character/right/r2.png'),
    pygame.image.load('pp2/character/right/r3.png'),
    pygame.image.load('pp2/character/right/r4.png')
]

walk_left=[
    pygame.image.load('pp2/character/left/l1.png'),
    pygame.image.load('pp2/character/left/l2.png'),
    pygame.image.load('pp2/character/left/l3.png'),
    pygame.image.load('pp2/character/left/l4.png')
]

player_anim_count=0

running=True
while running:
    
    
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x+1280,0))
    screen.blit(walk_right[player_anim_count],(character_x,character_y))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count],(character_x,character_y))
    else:
        screen.blit(walk_right[player_anim_count],(character_x,character_y))



    if keys[pygame.K_LEFT] and character_x>50:
        character_x-=character_speed
    elif keys[pygame.K_RIGHT] and character_x<300:
        character_x+=character_speed

    if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump=True
    else: 
                if jump_count>=-7:
                    if jump_count>0:
                        character_y-=(jump_count**2)/2
                    else:
                      character_y+=(jump_count**2)/2

                    jump_count-=1
                else:
                     is_jump=False
                     jump_count=7

    if player_anim_count==3:
        player_anim_count=0
    else:
        player_anim_count +=1

        bg_x -=5
        if bg_x==-1280:
            gg_x=0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()

    clock.tick(15)
            
        




    