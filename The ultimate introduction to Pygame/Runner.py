import pygame
from sys import exit
from random import randint

pygame.init()
pygame.display.set_caption("Runner")
pygame.time.set_timer(pygame.USEREVENT, 1000)
screen              = pygame.display.set_mode((800, 450))
clock               = pygame.time.Clock()
sky_surf            = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surf         = pygame.image.load("graphics/ground.png").convert_alpha()
start_time          = pygame.time.get_ticks() // 1000
space_down          = False
game_active         = True
gravity             = 1
score_surf          = None
score_rect          = None
obstacle_rect_list  = []

text_font       = pygame.font.Font(None, 50)
text_surf       = text_font.render("Crash Boom Bang! Restart? (y/n)", False, "Black")
text_rect       = text_surf.get_rect(center = screen.get_rect().center)
text_rect.top   = 350

player_surf         = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect         = player_surf.get_rect(bottomleft = (50, 300))
player_clicked      = False
player_jump_start   = -20
player_speed        = player_jump_start

player_stand_surf   = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surf   = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect   = player_stand_surf.get_rect(center = (400, 200))

snail_surf  = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
fly_surf    = pygame.image.load("graphics/fly/fly1.png").convert_alpha()

def move_obstacles(obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        obstacle_rect.right -= 5
        if obstacle_rect.right < 0: obstacle_rect_list.remove(obstacle_rect)

def is_crash(player_rect, obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        if obstacle_rect.colliderect(player_rect): return True

    return False

def display_crash_screen(screen, score_surf, score_rect, text_surf, text_rect, player_stand_surf, player_stand_rect):
    screen.fill((96, 128, 160))
    screen.blit(score_surf, score_rect)
    screen.blit(player_stand_surf, player_stand_rect)
    screen.blit(text_surf, text_rect)

def display_active_screen(screen, sky_surf, ground_surf, obstacle_rect_list, player_surf, player_rect, snail_surf, fly_surf):
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    screen.blit(player_surf, player_rect)

    for obstacle_rect in obstacle_rect_list: 
        if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
        else:                           screen.blit(fly_surf, obstacle_rect)
        
    score = pygame.time.get_ticks() // 1000 - start_time
    score_surf = text_font.render(f"Score: {score}", False, "Black")
    score_rect = score_surf.get_rect(midbottom = (400, 50))
    screen.blit(score_surf, score_rect)

    return score_surf,score_rect

def move_player(space_down, gravity, player_rect, player_clicked, player_jump_start, player_speed):
    if space_down or player_clicked or player_rect.bottom < 300:
        player_speed += gravity 
        player_rect.bottom += player_speed
        player_clicked = False
        space_down = False
    else:
        player_speed = player_jump_start
        player_rect.bottom = 300

    return player_speed, player_rect

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if is_crash(player_rect, obstacle_rect_list):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: game_active = False

                if event.key == pygame.K_y: 
                    player_rect.bottom  = 300
                    player_speed        = player_jump_start
                    start_time          = pygame.time.get_ticks() // 1000
                    obstacle_rect_list  = []
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: space_down = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos): player_clicked = True

            if event.type == pygame.USEREVENT: 
                if randint(0, 1):   obstacle_rect_list.append(fly_surf.get_rect(bottomleft = (randint(800, 1000), 300)))
                else:               obstacle_rect_list.append(snail_surf.get_rect(bottomleft = (randint(800, 1000), 100)))

    if is_crash(player_rect, obstacle_rect_list):
        display_crash_screen(screen, score_surf, score_rect, text_surf, text_rect, player_stand_surf, player_stand_rect)
    else:
        move_obstacles(obstacle_rect_list)

        player_speed, player_rect = move_player(space_down, gravity, player_rect, player_clicked, player_jump_start, player_speed)

        score_surf, score_rect = display_active_screen(screen, sky_surf, ground_surf, obstacle_rect_list, player_surf, player_rect, snail_surf, fly_surf)    
        
    pygame.display.update()    
    clock.tick(60)
