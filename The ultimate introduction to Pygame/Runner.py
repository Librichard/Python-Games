import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1_image = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        walk2_image = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.walk_images = [walk1_image, walk2_image]
        self.jump_image = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.animation_index = 0
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect(bottomleft = (50, 300))
        self.clicked = False
        self.jump_start = -20
        self.speed = self.jump_start
        self.stand_image = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
        self.stand_image = pygame.transform.rotozoom(self.stand_image, 0, 2)
        self.stand_rect = self.stand_image.get_rect(center = (400, 200))

    def animate(self):
        if self.rect.bottom < 300: self.image = self.jump_image
        else:
            self.animation_index += 0.1
            if self.animation_index >= len(self.walk_images): self.animation_index = 0
            self.image = self.walk_images[int(self.animation_index)]

#####################
#   GLOBAL SETTINGS #
#####################

pygame.init()
pygame.display.set_caption("Runner")

obstacle_timer = pygame.USEREVENT
pygame.time.set_timer(obstacle_timer, 1000)

snail_animation_timer = pygame.USEREVENT + 1
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)

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

player = Player()

snail_glide1_surf   = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_glide2_surf   = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_glide         = [snail_glide1_surf, snail_glide2_surf]
snail_index         = 0
snail_surf          = snail_glide[snail_index]

fly_fly1_surf    = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_fly2_surf    = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_fly          = [fly_fly1_surf, fly_fly2_surf]
fly_index         = 0
fly_surf          = fly_fly[fly_index]

#################
#   FUNCTIONS   #
#################

def move_obstacles(obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        obstacle_rect.right -= 6
        if obstacle_rect.right < 0: obstacle_rect_list.remove(obstacle_rect)

def is_crash(player_rect, obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        if obstacle_rect.colliderect(player_rect): return True

    return False

def display_crash_screen(score_surf, score_rect, text_surf, text_rect, player_stand_surf, player_stand_rect):
    screen.fill((96, 128, 160))
    screen.blit(score_surf, score_rect)
    screen.blit(player_stand_surf, player_stand_rect)
    screen.blit(text_surf, text_rect)

def display_active_screen(sky_surf, ground_surf, obstacle_rect_list, player_surf, player_rect, snail_surf, fly_surf):
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

    return score_surf, score_rect

#################
#   GAME LOOP   #
#################

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if is_crash(player.rect, obstacle_rect_list):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: game_active = False

                if event.key == pygame.K_y: 
                    player.rect.bottom  = 300
                    player.speed        = player.jump_start
                    start_time          = pygame.time.get_ticks() // 1000
                    obstacle_rect_list  = []
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: space_down = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.rect.collidepoint(event.pos): player.clicked = True

            if event.type == obstacle_timer: 
                if randint(0, 1):   obstacle_rect_list.append(fly_surf.get_rect(bottomleft = (randint(800, 1000), 300)))
                else:               obstacle_rect_list.append(snail_surf.get_rect(bottomleft = (randint(800, 1000), 100)))

            if event.type == snail_animation_timer:
                snail_index += 1
                if snail_index >= len(snail_glide): snail_index = 0
                snail_surf = snail_glide[snail_index]

            if event.type == fly_animation_timer:
                fly_index += 1
                if fly_index >= len(fly_fly): fly_index = 0
                fly_surf = fly_fly[fly_index]

    if is_crash(player.rect, obstacle_rect_list):
        display_crash_screen(score_surf, score_rect, text_surf, text_rect, player.stand_image, player.stand_rect)
    else:
        move_obstacles(obstacle_rect_list)

        if space_down or player.clicked or player.rect.bottom < 300:
            player.speed += gravity
            player.rect.bottom += player.speed
            player.clicked = False
            space_down = False
        else:
            player.speed = player.jump_start
            player.rect.bottom = 300

        player.animate()
        score_surf, score_rect = display_active_screen(sky_surf, ground_surf, obstacle_rect_list, player.image, player.rect, snail_surf, fly_surf)
        
    pygame.display.update()    
    clock.tick(60)

#   here is out of the game loop, so we can quit the game
pygame.quit()
