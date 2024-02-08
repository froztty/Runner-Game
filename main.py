import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_text = pygame.font.Font('font/Pixeltype.ttf', 50) # font, and font size as parameters

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
score_surf = score_text.render('My Game', False, 'Black') # text, anti-aliasing (smooth the edges of the text), and color 

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600, 300)) 

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300)) # midbottom is the position of the rectangle so it is on that point. so try midtop or topright

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # could use a break to get out of the game but we should use sys
            exit()            

    screen.blit(sky_surf, (0, 0)) # coords (x, y)
    screen.blit(ground_surf, (0, 300))
    screen.blit(score_surf, (300, 50))
    snail_rect.right -= 4
    if snail_rect.right <= 0 : snail_rect.left = 800 # this checks if the right side of the snail is gone then the left side will appear on the other side of the screen
    screen.blit(snail_surf, snail_rect)
    #player_rect.left += 1 # moves player
    screen.blit(player_surf, player_rect)
    
    
    
    pygame.display.update()
    clock.tick(60)