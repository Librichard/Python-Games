import pygame
from sys import exit
from random import randint

WINDOW_TITLE = "Runner"
SCREEN_SIZE = (800, 450)
GROUND_Y = 300
GRAVITY = 1
OBSTACLE_TIMER_INTERVAL_MS = 1000
SNAIL_ANIMATION_INTERVAL_MS = 500
FLY_ANIMATION_INTERVAL_MS = 200
OBSTACLE_SPEED = 6
OBSTACLE_MIN_X = 800
OBSTACLE_MAX_X = 1000
ALTERNATE_OBSTACLE_BOTTOM = 100
GAME_OVER_BACKGROUND = (96, 128, 160)
GAME_OVER_TEXT = "Crash Boom Bang! Restart? (y/n)"
GAME_OVER_TEXT_TOP = 350
FONT_SIZE = 50
TEXT_COLOR = "Black"
SCORE_POSITION = (400, 50)
FRAME_RATE = 60

class Player(pygame.sprite.Sprite):
    START_X = 50
    STAND_POSITION = (400, 200)
    IMAGE_SCALE = 2
    ANIMATION_STEP = 0.1
    JUMP_START = -20

    def __init__(self):
        super().__init__()
        walk1_image = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        walk2_image = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.jump_image = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.stand_image = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
        self.stand_image = pygame.transform.rotozoom(self.stand_image, 0, self.IMAGE_SCALE)
        self.walk_images = [walk1_image, walk2_image]
        self.animation_index = 0
        self.image = self.walk_images[0]
        self.rect = self.image.get_rect(bottomleft = (self.START_X, GROUND_Y))
        self.clicked = False
        self.speed = self.JUMP_START
        self.stand_rect = self.stand_image.get_rect(center = self.STAND_POSITION)

    def get_stand_image(self):
        return self.stand_image

    def get_stand_rect(self):
        return self.stand_rect

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def is_clicked(self):
        return self.clicked

    def set_clicked(self, clicked):
        self.clicked = clicked

    def reset_speed(self):
        self.speed = self.JUMP_START

    def update_speed(self):
        self.speed += GRAVITY

    def animate(self):
        if self.rect.bottom < GROUND_Y: self.image = self.jump_image
        else:
            self.animation_index += self.ANIMATION_STEP
            if self.animation_index >= len(self.walk_images): self.animation_index = 0
            self.image = self.walk_images[int(self.animation_index)]

class Snail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        snail1_image = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
        snail2_image = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
        self.images = [snail1_image, snail2_image]
        self.animation_index = 0
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()

    def animate(self):
        self.animation_index += 1
        if self.animation_index >= len(self.images): self.animation_index = 0
        self.image = self.images[self.animation_index]

class Fly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly1_image = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
        fly2_image = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
        self.images = [fly1_image, fly2_image]
        self.animation_index = 0
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()

    def animate(self):
        self.animation_index += 1
        if self.animation_index >= len(self.images): self.animation_index = 0
        self.image = self.images[self.animation_index]

#####################
#   GLOBAL SETTINGS #
#####################

pygame.init()
pygame.display.set_caption(WINDOW_TITLE)

OBSTACLE_TIMER = pygame.USEREVENT
pygame.time.set_timer(OBSTACLE_TIMER, OBSTACLE_TIMER_INTERVAL_MS)

SNAIL_ANIMATION_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(SNAIL_ANIMATION_TIMER, SNAIL_ANIMATION_INTERVAL_MS)

FLY_ANIMATION_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(FLY_ANIMATION_TIMER, FLY_ANIMATION_INTERVAL_MS)

screen              = pygame.display.set_mode(SCREEN_SIZE)
clock               = pygame.time.Clock()
sky_surf            = pygame.image.load("graphics/Sky.png").convert_alpha()
ground_surf         = pygame.image.load("graphics/ground.png").convert_alpha()
start_time          = pygame.time.get_ticks() // 1000
space_down          = False
game_active         = True
score_surf          = None
score_rect          = None
obstacle_rect_list  = []

text_font       = pygame.font.Font(None, FONT_SIZE)
text_surf       = text_font.render(GAME_OVER_TEXT, False, TEXT_COLOR)
text_rect       = text_surf.get_rect(center = screen.get_rect().center)
text_rect.top   = GAME_OVER_TEXT_TOP

player = Player()

snail = Snail()
fly = Fly()

#################
#   FUNCTIONS   #
#################

def move_obstacles(obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        obstacle_rect.right -= OBSTACLE_SPEED
        if obstacle_rect.right < 0: obstacle_rect_list.remove(obstacle_rect)

def is_crash(player_rect, obstacle_rect_list):
    for obstacle_rect in obstacle_rect_list:
        if obstacle_rect.colliderect(player_rect): return True

    return False

def display_crash_screen(score_surf, score_rect, text_surf, text_rect, player_stand_surf, player_stand_rect):
    screen.fill(GAME_OVER_BACKGROUND)
    screen.blit(score_surf, score_rect)
    screen.blit(player_stand_surf, player_stand_rect)
    screen.blit(text_surf, text_rect)

def display_active_screen(sky_surf, ground_surf, obstacle_rect_list, player_surf, player_rect, snail_surf, fly_surf):
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, GROUND_Y))
    screen.blit(player_surf, player_rect)

    for obstacle_rect in obstacle_rect_list: 
        if obstacle_rect.bottom == GROUND_Y: screen.blit(snail_surf, obstacle_rect)
        else:                           screen.blit(fly_surf, obstacle_rect)
        
    score = pygame.time.get_ticks() // 1000 - start_time
    score_surf = text_font.render(f"Score: {score}", False, TEXT_COLOR)
    score_rect = score_surf.get_rect(midbottom = SCORE_POSITION)
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

        if is_crash(player.get_rect(), obstacle_rect_list):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: game_active = False

                if event.key == pygame.K_y: 
                    player.get_rect().bottom = GROUND_Y
                    player.reset_speed()
                    start_time          = pygame.time.get_ticks() // 1000
                    obstacle_rect_list  = []
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: space_down = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.get_rect().collidepoint(event.pos): player.set_clicked(True)

            if event.type == OBSTACLE_TIMER:
                if randint(0, 1):   obstacle_rect_list.append(fly.image.get_rect(bottomleft = (randint(OBSTACLE_MIN_X, OBSTACLE_MAX_X), GROUND_Y)))
                else:               obstacle_rect_list.append(snail.image.get_rect(bottomleft = (randint(OBSTACLE_MIN_X, OBSTACLE_MAX_X), ALTERNATE_OBSTACLE_BOTTOM)))

            if event.type == SNAIL_ANIMATION_TIMER:
                snail.animate()

            if event.type == FLY_ANIMATION_TIMER:
                fly.animate()

    if is_crash(player.get_rect(), obstacle_rect_list):
        display_crash_screen(score_surf, score_rect, text_surf, text_rect, player.get_stand_image(), player.get_stand_rect())
    else:
        move_obstacles(obstacle_rect_list)

        if space_down or player.is_clicked() or player.get_rect().bottom < GROUND_Y:
            player.update_speed()
            player.get_rect().bottom += player.speed
            player.set_clicked(False)
            space_down = False
        else:
            player.reset_speed()
            player.get_rect().bottom = GROUND_Y

        player.animate()
        score_surf, score_rect = display_active_screen(sky_surf, ground_surf, obstacle_rect_list, player.get_image(), player.get_rect(), snail.image, fly.image)
        
    pygame.display.update()    
    clock.tick(FRAME_RATE)

#   here is out of the game loop, so we can quit the game
pygame.quit()
