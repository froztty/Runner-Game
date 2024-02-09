import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time 
    score_surf = score_text.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # delete rectangles if its off the screen
        
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    #play walking animation if the player is on floor
    # display the jump surface when player is not on floor
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_text = pygame.font.Font('font/Pixeltype.ttf', 50) # font, and font size as parameters
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# score_surf = score_text.render('My Game', False, (64, 64, 64)) # text, anti-aliasing (smooth the edges of the text), and color 
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_rect = snail_surf.get_rect(bottomright = (600, 300)) 

fly_surf = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300)) # midbottom is the position of the rectangle so it is on that point. so try midtop or topright
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#player_stand = pygame.transform.scale(player_stand, (200, 275)) # width and height. replacing the new scaled image of the old one
#player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = score_text.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = score_text.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400, 330))

#Timer
obstacle_timer = pygame.USEREVENT + 1 # atleast one event happens
pygame.time.set_timer(obstacle_timer, 1500) # trigger every 1500ms

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
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100),210)))
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
            
        
    if game_active:
        screen.blit(sky_surf, (0, 0)) # coords (x, y)
        screen.blit(ground_surf, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) #surface we need to draw on, color, the thing itself, width, and border radius 
        # #pygame.draw.line(screen, 'Black', (0, 0), pygame.mouse.get_pos(), 1) #draw line that follows mouse see documentation.txt
        # screen.blit(score_surf, score_rect)
        score = display_score()
        
        # snail_rect.right -= 4
        # if snail_rect.right <= 0 : snail_rect.left = 800 # this checks if the right side of the snail is gone then the left side will appear on the other side of the screen
        #screen.blit(snail_surf, snail_rect)
        #player_rect.left += 1 # moves player
        
        #Player
        player_gravity += 1
        player_rect.y += player_gravity # there is an increase in speed. adds 2 to 301 then adds 3 to 305 etc. exponential 
        if player_rect.bottom > 300: player_rect.bottom = 300 # prevent the player from going past the ground
        player_animation()
        screen.blit(player_surf, player_rect)
        
        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list) # we run the function and moves it and then it gets updated
        
        # collision
        game_active = collisions(player_rect, obstacle_rect_list)
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        
        #mouse_pos = pygame.mouse.get_pos()
        #we can get mouse input or keyboard input via through pygame or in the event loop
        #if player_rect.collidepoint(mouse_pos):
            #print(pygame.mouse.get_pressed())

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('jump')
        # player_rect.colliderect(snail_rect) returns 1 or 0
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() # removes all the items inside once the game ends
        player_rect.midbottom = (80, 300)
        player_gravity = 0                  #makes sure that the player doesnt die from the fly and spawns where it was left off
        
        score_message = score_text.render(f'Your score: {score}',False,(111,196,169))
        score_msg_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_msg_rect)

    pygame.display.update()
    clock.tick(60)