import pygame
import os
import random
import csv
import button
from pygame import mixer


#단축키 -> ctrl+P 파라미터 정보 확인
pygame.init()
mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ninja Shuriken')

# set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
MAX_LEVELS = 3
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 121
screen_scroll = 0
bg_scroll = 0
level = 3
MaxScroll = 10  # 1단계는 10개 필요
EnemyList = []
start_game = False
end_game = False

#define player action movement
moving_left = False
moving_right = False
shoot = False
attack = False
action_cooldown = 0
action_wait_time = 20

#load music and sounds
pygame.mixer.music.load('audio/theme-1.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0, 5000) #ms
jump_fx = pygame.mixer.Sound('audio/SFX_Jump_32.mp3')
pygame.mixer.music.set_volume(0.1)
gameover_fx = pygame.mixer.Sound('audio/game-over.mp3.')
pygame.mixer.music.set_volume(0.3)
kill_fx = pygame.mixer.Sound('audio/kill.mp3')
pygame.mixer.music.set_volume(0.3)
shoot_fx = pygame.mixer.Sound('audio/magic-1.mp3')
pygame.mixer.music.set_volume(0.3)
clear_fx = pygame.mixer.Sound('audio/power-up.mp3')
pygame.mixer.music.set_volume(0.3)
eatitem_fx = pygame.mixer.Sound('audio/gold-1.mp3')
pygame.mixer.music.set_volume(0.3)

#load images
#BUTTON images
start_img = pygame.image.load('img/GUI/Start.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (int(start_img.get_width() * 3.5),
                                             int(start_img.get_height() * 3.5)))
exit_img = pygame.image.load('img/GUI/Exit.png').convert_alpha()
exit_img = pygame.transform.scale(exit_img, (int(exit_img.get_width() * 3.5),
                                             int(exit_img.get_height() * 3.5)))
continue_img = pygame.image.load('img/GUI/Continue.png').convert_alpha()
continue_img = pygame.transform.scale(continue_img, (int(continue_img.get_width() * 3.5),
                                             int(continue_img.get_height() * 3.5)))
quit_img = pygame.image.load('img/GUI/Quit.png').convert_alpha()
quit_img = pygame.transform.scale(quit_img, (int(quit_img.get_width() * 3.5),
                                             int(quit_img.get_height() * 3.5)))
#background
sky1_img = pygame.image.load('img/Level/Background_1.png').convert_alpha()
sky1_img = pygame.transform.scale(sky1_img, (int(sky1_img.get_width() * 2.5),
                                             int(sky1_img.get_height() * 2.355)))
sky2_img = pygame.image.load('img/Level/Background_2.png').convert_alpha()
sky2_img = pygame.transform.scale(sky2_img, (int(sky2_img.get_width() * 2.5),
                                             int(sky2_img.get_height() * 2.355)))
wall_img = pygame.image.load('img/Level/Tiles/Assets29.png').convert_alpha()
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

mainmenu_img = pygame.image.load('img/GUI/Mainmenu.png').convert_alpha()
mainmenu_img = pygame.transform.scale(mainmenu_img, (int(mainmenu_img.get_width()),
                                      int(mainmenu_img.get_height())))
ending_img = pygame.image.load('img/GUI/Ending.png').convert_alpha()
ending_img = pygame.transform.scale(ending_img, (int(ending_img.get_width()),int(ending_img.get_height())))

#tiles img list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Level/Tiles/Assets{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#shuriken
shuriken_img = pygame.image.load('img/icon/shuriken.png').convert_alpha()
shuriken_img = pygame.transform.scale(shuriken_img,
                                            (int(shuriken_img.get_width() * 0.08),
                                            int(shuriken_img.get_height() * 0.08)))
# pick up items
health_item1_img = pygame.image.load('img/icon/yakitori.png').convert_alpha()
health_item1_img = pygame.transform.scale(health_item1_img,
                       (int(health_item1_img.get_width()* 2.0),
                        int(health_item1_img.get_height()* 2.0)))
health_item2_img = pygame.image.load('img/icon/shrimp.png').convert_alpha()
health_item2_img = pygame.transform.scale(health_item2_img,
                       (int(health_item2_img.get_width() * 2.0),
                        int(health_item2_img.get_height() * 2.0)))
health_item3_img = pygame.image.load('img/icon/noodle.png').convert_alpha()
health_item3_img = pygame.transform.scale(health_item3_img,
                       (int(health_item3_img.get_width() * 2.0),
                        int(health_item3_img.get_height() * 2.0)))

ammo_item_img = pygame.image.load('img/icon/ammo_shuriken.png').convert_alpha()
ammo_item_img = pygame.transform.scale(ammo_item_img,
                                            (int(ammo_item_img.get_width() * 2.5),
                                            int(ammo_item_img.get_height() * 2.5)))
clear_item_img = pygame.image.load('img/icon/clearitem.png').convert_alpha()
clear_item_img = pygame.transform.scale(clear_item_img,
                       (int(clear_item_img.get_width() * 2.0),
                        int(clear_item_img.get_height() * 2.0)))
heart_img = pygame.image.load('img/icon/heart.png').convert_alpha()
heart_img = pygame.transform.scale(heart_img,
                       (int(heart_img.get_width() * 2.0),
                        int(heart_img.get_height() * 2.0)))
item_boxes = {'Health_1': health_item1_img,
              'Health_2': health_item2_img,
              'Health_3': health_item3_img,
              'Ammo': ammo_item_img,
              'Clear': clear_item_img}

#define colors
BG = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
#define font
font = pygame.font.SysFont('Futura', 30)

def draw_ending():
    screen.fill(BG)
    screen.blit(ending_img, (0,0))

def draw_menu():
    screen.fill(BG)
    screen.blit(mainmenu_img, (0,0))

def draw_text (text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_bg(): #remove trail by overwriting background
    screen.fill(BG)
    width = sky1_img.get_width()

    for x in range(5):
        screen.blit(sky2_img, (x * width -bg_scroll * 0.5, SCREEN_HEIGHT - sky2_img.get_height() - 50))
    for x in range(7):
        screen.blit(sky1_img,(x * width -bg_scroll * 0.7 ,SCREEN_HEIGHT - sky1_img.get_height() - 50))

#function to reset level
def reset_level():
    enemy_group.empty()
    shuriken_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    kill_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

class Ninja(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type #create instance to determine character's type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo #표창 갯수
        self.shoot_cooldown = 0 #shoot delay
        self.health = 100
        self.max_health = self.health
        self.direction = 1 #direction vector
        self.velocity_y = 0
        self.jump = False #jump 횟수 limit
        self.in_air = True #바닥에 닿으면 False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #split animation
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_countdown = 0
        self.damage = False #데미지 애니메이션
        self.clear = 0 #clear 위한 scroll 갯수
        self.randomcount = 0
        self.actiondone = False

        #load all images for the players
        animation_types = ['idle', 'run', 'jump', 'x', 'shoot', 'hurt', 'attack']
        for animation in animation_types:
            #temp_list 초기화하여 애니메이션 타입 다 넣기
            temp_list = []
            #python function : count how many items are within a folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                #ex_img/Player/jump 경로의 jump_0.png부터 3까지 반복
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{animation}_{i}.png').convert_alpha()
                img = pygame.transform.scale(img,
                                             (int(img.get_width()* scale), int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        # action 별 리스트별로 animation list에서 관리
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(10,0)
        self.rect = self.rect.inflate(-10, 0)
        if self.char_type == 'Enemy':
           self.rect = self.rect.move(10, 0)
           self.rect = self.rect.inflate(-10, 0)
           self.width = self.image.get_width() - 20
        self.rect.center = (x, y)
        self.width = self.image.get_width() - 10
        self.height = self.image.get_height()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0 #the change in x , reset movement variables
        dy = 0

        #assign movement variables if moving left or right
        if moving_left == True:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right == True:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11 #high number
            self.jump = False
            self.in_air = True
        #apply gravity
        self.velocity_y += GRAVITY #going to be decresed by gravity toward the ground
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y

        #check for collision
        for tile in world.obstacle_list:
            #check collistion in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
                if self.char_type == 'Enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check collistion in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground (jumping)
                if self.velocity_y < 0:
                    self.velocity_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground (falling)
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        #check for collision with bamboo
        if pygame.sprite.spritecollide(self, kill_group, False):
            self.health = 0

        #check for collision with clear
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'Player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'Player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll, level_complete


    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            # player의 coordinate와 direction을 기준으로 생성
            if self.direction == -1:
                shuriken = Shuriken(self.rect.centerx - (1.2 * self.rect.size[0]),
                                self.rect.centery , self.direction) #(0.1 * self.rect.size[1])
            else:
                shuriken = Shuriken(self.rect.centerx + (1.2 * self.rect.size[0]),
                                    self.rect.centery + (0.1 * self.rect.size[1]), self.direction)
            self.ammo -= 1 #reduce ammo
            shoot_fx.play()

    def check_collide(self): #check what enemey attacked
        if pygame.sprite.collide_rect(self, player) and self.char_type == 'Enemy':
            return True

    def attack(self, target):
        if pygame.sprite.collide_rect(self, target):
            shoot_fx.play()
            target.health -= 35
            target.update_action(5)

    def ai(self):
        self.DELAY = 0
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect) and self.action != 5:
                #stop running and face the player
                self.update_action(0) #0: idle
                if random.randint(1, 100) == 1:
                    #shoot
                    self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
            #scroll
            self.rect.x += screen_scroll

    def dropscroll(self):
        if self.alive == False and self.actiondone == True :
            self.kill()
            item = ItemBox('Clear', self.rect.x, self.rect.y + 20)
            item_box_group.add(item)

    def droprandom(self):
        if self.alive == False and self.randomcount == 0:
            self.randomcount += 1
            randomrange = random.randint(1,5)
            if randomrange == 1:
                self.kill()
                randdomtype = random.randint(1,4)
                if randdomtype == 1:
                    itemtype = 'Health_1'
                elif randdomtype == 2:
                    itemtype = 'Health_2'
                elif randdomtype == 3:
                    itemtype = 'Health_3'
                elif randdomtype == 4:
                    itemtype = 'Ammo'

                item = ItemBox(itemtype, self.rect.x, self.rect.y + 20)
                item_box_group.add(item)

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 200
        self.image = self.animation_list[self.action][self.frame_index]
        #chek if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1 #animation list의 인덱스에 따라 이미지 업데이트
        #range of out 처리
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3 : #action is death
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.actiondone = True
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) #3 : died(x)
            # scroll
            self.rect.x += screen_scroll
            if self.char_type == 'Player':
                gameover_fx.play()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #x aixs에 대해서만 flip
        #pygame.draw.rect(screen, RED, self.rect, 1)

    def drawenemyhealth(self):
        percent = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.rect.x + 20, self.rect.y, 50, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.x + 20, self.rect.y, 50 * percent, 10))

class World():
    def __init__(self):
        self.obstacle_list = []
    def process_data(self, data):
        self.level_length = len(data[0]) #columns
        #각 레벨 csv 파일 읽히기
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0 :
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE #크기 고정
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 54 or tile == 66 or tile == 120: #KILL
                        kill = Kill(img, x * TILE_SIZE, y * TILE_SIZE)
                        kill_group.add(kill)
                    elif tile == 106: #ammo
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 107: #health2
                        item_box = ItemBox('Health_2', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 108: #health1
                        item_box = ItemBox('Health_1', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 105:  # health3
                        item_box = ItemBox('Health_3', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 113: #scroll
                        item_box = ItemBox('Clear', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 0:
                        decoration = Decoration(wall_img, x* TILE_SIZE, y* TILE_SIZE)
                        decoration_group.add(decoration)
                        enemy = Ninja('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1, 2, 10)
                        EnemyList.append(enemy)
                        enemy_group.add(enemy)
                    elif tile == 109 or tile == 0 : #create enemy
                        enemy = Ninja('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1, 2, 10)
                        EnemyList.append(enemy)
                        enemy_group.add(enemy)
                    elif tile == 110: #create player
                        player = Ninja('Player', x * TILE_SIZE, y* TILE_SIZE, 1, 4, 10)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile >= 115 and tile <= 116 or tile == 118 or tile ==119: #create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 4 or tile == 5 or tile == 6 or tile ==7 or tile ==8 or tile ==9 or tile ==10 or tile == 11 or tile == 78 or tile==79\
                            or tile == 12 or tile == 13or tile ==19  or tile == 21 or tile == 23 or tile ==24  or tile ==25  \
                            or tile ==26  or tile ==27  or tile == 40 or tile == 41 or tile==58 or tile == 50 or tile==51 or tile== 52 or tile== 53 \
                            or tile == 62 or tile== 63 or tile == 64 or tile==65 or tile== 110 or tile ==111 or tile==112 or tile==95 or tile==85 or tile == 86 or tile== 96 or tile==44 or tile ==29 \
                            or tile == 114 or tile == 117:
                         decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                         decoration_group.add(decoration)
                    else: #obstacle
                        self.obstacle_list.append(tile_data)
        return player, health_bar, EnemyList

    def world_draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll #scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE- self.image.get_height()))
    def update(self):
        self.rect.x += screen_scroll

class Kill(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-10,0)
        self.rect.midtop = ((x-5) + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        self.rect.x += screen_scroll
        # check if the player has picked up the item
        if pygame.sprite.collide_rect(self, player):
            player.health = 0

    #def draw(self):
        #pygame.draw.rect(screen, RED, self.rect, 1)

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y): #초기화할 때 item_type 지정
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2,
                            y+ (TILE_SIZE - self.image.get_height()))
    def update(self):
        #scroll
        self.rect.x += screen_scroll

    def eat(self):
        #check if the player has picked up the item
        if pygame.sprite.collide_rect(self, player):
            #checck what kind of item it was
            if self.item_type == 'Health_1':
                player.health += 10
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Health_2': #shrimp.png
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Health_3': #noodle.png
                player.health += 50
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 5
            elif self.item_type == 'Clear':
                player.clear += 1
            eatitem_fx.play()
            #delete the item
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health
        percent = self.health / self.max_health
        screen.blit(heart_img, (self.x , self.y + 3))
        pygame.draw.rect(screen, RED, (self.x + 25, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x + 25, self.y, 150 * percent, 20))

class Shuriken(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        self.group = shuriken_group
        pygame.sprite.Sprite.__init__(self, self.group)
        self.speed = 10
        self.image = shuriken_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y) #x,y 좌표를 센터에 두어 관리함
        self.direction = direction

    def update(self):
        #move shuriken
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if shuriken has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check for collistion with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check collistion with characters
        if pygame.sprite.spritecollide(player, shuriken_group, False):
            if player.alive:
                player.health -= 30
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, shuriken_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()


#create button
start_button = button.Button(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT //2 + 90, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH//2 + 30, SCREEN_HEIGHT //2 + 90, exit_img, 1)
continue_button = button.Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT //2 - 50, continue_img, 1)
quit_button = button.Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT //2 + 50, quit_img, 1)

#create sprite groups
enemy_group = pygame.sprite.Group()
shuriken_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
kill_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#load in level data and create world
with open(f'level{level}_data.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar, EnemyList = world.process_data(world_data)

#Scroll 가지는 적 임의 생성
EnemyList = random.sample(EnemyList, 5)
print(EnemyList)

run = True
while run:
    clock.tick(FPS)

    if start_game == False: #main menu
        #draw menu
        screen.fill(BG)
        draw_menu()
        #add button
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    elif end_game == True:
        screen.fill(BG)
        draw_ending()

    else:
        #play game
        draw_bg()
        #draw world map
        world.world_draw()

        #update and draw groups
        shuriken_group.update()
        exit_group.update()
        item_box_group.update()
        kill_group.update()
        exit_group.draw(screen)
        kill_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        item_box_group.draw(screen)
        shuriken_group.draw(screen)
        player.update()
        player.draw() #screen draw

        #sho player health
        health_bar.draw(player.health)

        #show ammo
        draw_text('Shuriken: ', font, WHITE, 10, 35)
        for x in range(player.ammo):
            screen.blit(shuriken_img, (100 + (x * 20), 20))
        #show scroll
        draw_text(f'Scroll: {player.clear}/10', font, WHITE, 10, 60)

        #for bamboo in kill_group:
         #   bamboo.draw()

        target = None
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()
            enemy.drawenemyhealth()
            enemy.check_collide()
            if enemy.check_collide() == True:
                target = enemy
            if enemy in EnemyList:
                enemy.dropscroll()
        if player.alive:
            #player attack cooltime
            action_cooldown += 1
            #shoot shuriken
            if shoot: #공중, 이동하면서도 shoot 가능
                player.shoot()
            #update player acitons
            if player.in_air:
                player.update_action(2) #2 : jump
            elif shoot:
                player.update_action(4)  # 4 : shoot
                player.shoot()
            elif attack:
                player.update_action(6) #6 : attack
            elif moving_right or moving_left:
                player.update_action(1) #1 : run
            else:
                player.update_action(0) #0 : idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll

            #check if player has completed the level
            if level_complete and player.clear >= 10:
                clear_fx.play()
                level += 1
                MaxScroll += 5
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    # load world data
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar, EnemyList = world.process_data(world_data)
                else:
                    #play game
                    end_game = True

        else:
            screen_scroll = 0
            if continue_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                #load world data
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player, health_bar, EnemyList = world.process_data(world_data)
            if quit_button.draw(screen):
                run = False

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                for item in item_box_group:
                    item.eat()
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_LCTRL and action_cooldown >= action_wait_time:
                attack = True
                if attack == True and target != None:
                    player.attack(target)
                    target.update_action(5)
                action_cooldown = 0
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_LCTRL:
                attack = False
    pygame.display.update()
pygame.quit()