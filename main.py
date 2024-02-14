import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # initilizating the sprite class in itself
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else: 
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        if speed_up:
            self.rect.x -= 10
        else: self.rect.x -= 6 # moves the obstacles
        self.destroy()    

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time 
    score_surf = score_text.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if speed_up:
                obstacle_rect.x -= 10
                print("sped up")
            else:
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
            if player.colliderect(obstacle_rect): 
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # becareful just getting player because it is a single group also u cant get a regular group since there are so many sprites.... its False then the snail gets deleted but doesnt matter in our case
        obstacle_group.empty() # clears all the snails
        death_audio.play()
        return False
    else: return True

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

def draw_flash_effect(screen, flash_color, flash_duration):
    flash_surface = pygame.Surface(screen.get_size())
    flash_surface.fill(flash_color)
    for alpha in range(0, 255, 15):
        flash_surface.set_alpha(alpha)
        screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(flash_duration / 16))

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_text = pygame.font.Font('font/Pixeltype.ttf', 50) # font, and font size as parameters
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(.01)
bg_music.play(loops = -1)
death_audio = pygame.mixer.Sound('audio/death.mp3')
death_audio.set_volume(.1)
speed_up = False

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# score_surf = score_text.render('My Game', False, (64, 64, 64)) # text, anti-aliasing (smooth the edges of the text), and color 
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_rect = snail_surf.get_rect(bottomright = (600, 300)) 
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                if speed_up:
                    pygame.time.set_timer(obstacle_timer, 700)
                else:
                    pygame.time.set_timer(obstacle_timer, 1500)
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']))) # snail has a 75% and fly is 25%
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100),300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100),210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
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
        if score >= 30:
            speed_up = True
        else: speed_up = False
        
        if speed_up == True and score == 30:
            draw_flash_effect(screen, (255, 0, 0), 500)
            
        
        # snail_rect.right -= 4
        # if snail_rect.right <= 0 : snail_rect.left = 800 # this checks if the right side of the snail is gone then the left side will appear on the other side of the screen
        #screen.blit(snail_surf, snail_rect)
        #player_rect.left += 1 # moves player
        
        #Player
        # player_gravity += 1
        # player_rect.y += player_gravity # there is an increase in speed. adds 2 to 301 then adds 3 to 305 etc. exponential 
        # if player_rect.bottom > 300: player_rect.bottom = 300 # prevent the player from going past the ground
        # player_animation()
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list) # we run the function and moves it and then it gets updated
        
        # collision
        game_active = collision_sprite()
        # game_active = collisions(player_rect, obstacle_rect_list)
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
        speed_up = False
        
        score_message = score_text.render(f'Your score: {score}',False,(111,196,169))
        score_msg_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_msg_rect)

    pygame.display.update()
    clock.tick(60)