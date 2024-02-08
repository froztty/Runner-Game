import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_text = pygame.font.Font('font/Pixeltype.ttf', 50) # font, and font size as parameters
game_active = True

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
score_surf = score_text.render('My Game', False, (64, 64, 64)) # text, anti-aliasing (smooth the edges of the text), and color 
score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300)) 

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300)) # midbottom is the position of the rectangle so it is on that point. so try midtop or topright
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # could use a break to get out of the game but we should use sys
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: # there are other thigns to check the event like MOUSEBUTTOWNMOTION or UP
                if player_rect.collidepoint(event.pos)  and player_rect.bottom >= 300: # checks to make sure player is standing on ground
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20 # adds jump motion
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
        
    if game_active:
        screen.blit(sky_surf, (0, 0)) # coords (x, y)
        screen.blit(ground_surf, (0, 300))
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) #surface we need to draw on, color, the thing itself, width, and border radius 
        #pygame.draw.line(screen, 'Black', (0, 0), pygame.mouse.get_pos(), 1) #draw line that follows mouse see documentation.txt
        screen.blit(score_surf, score_rect)
        
        snail_rect.right -= 4
        if snail_rect.right <= 0 : snail_rect.left = 800 # this checks if the right side of the snail is gone then the left side will appear on the other side of the screen
        screen.blit(snail_surf, snail_rect)
        #player_rect.left += 1 # moves player
        
        #Player
        player_gravity += 1
        player_rect.y += player_gravity # there is an increase in speed. adds 2 to 301 then adds 3 to 305 etc. exponential 
        if player_rect.bottom > 300: player_rect.bottom = 300 # prevent the player from going past the ground
        screen.blit(player_surf, player_rect)
        
        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
        
        #mouse_pos = pygame.mouse.get_pos()
        #we can get mouse input or keyboard input via through pygame or in the event loop
        #if player_rect.collidepoint(mouse_pos):
            #print(pygame.mouse.get_pressed())

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')
        # player_rect.colliderect(snail_rect) returns 1 or 0
    else:
        screen.fill('Black')
    
    pygame.display.update()
    clock.tick(60)