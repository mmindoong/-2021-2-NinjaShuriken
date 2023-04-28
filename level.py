import pygame
import button
import random
import csv

pygame.init()
clock = pygame.time.Clock()
FPS = 60
#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN,
                                  SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 121 #갯수
level = 0
current_tile = 0

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images
sky1_img = pygame.image.load('img/Level/Background_1.png').convert_alpha()
sky1_img = pygame.transform.scale(sky1_img, (int(sky1_img.get_width() * 2.5),
                                             int(sky1_img.get_height() * 2.5)))
sky2_img = pygame.image.load('img/Level/Background_2.png').convert_alpha()
sky2_img = pygame.transform.scale(sky2_img, (int(sky2_img.get_width() * 2.5),
                                             int(sky2_img.get_height() * 2.5)))
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Level/Tiles/Assets{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('img/Level/save_btn.png').convert_alpha()
save_img = pygame.transform.scale(save_img, (int(save_img.get_width() * 0.5),
                                             int(save_img.get_height() * 0.8)))
load_img = pygame.image.load('img/Level/load_btn.png').convert_alpha()
load_img = pygame.transform.scale(load_img, (int(load_img.get_width() * 0.5),
                                             int(load_img.get_height() * 0.8)))
backup_img = pygame.image.load('img/Level/backup_btn.png').convert_alpha()
backup_img = pygame.transform.scale(backup_img, (int(backup_img.get_width() * 0.5),
                                             int(backup_img.get_height() * 0.8)))

#define colors
BG = (170, 170, 255)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
    random_ground = random.randint(32, 36)
    world_data[ROWS-1][tile] = random_ground
for tile2 in range(0, MAX_COLS):
    random_ground = random.randint(32, 36)
    world_data[ROWS-2][tile2] = random_ground

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#create function for drawing background
def draw_bg():
    screen.fill(BG)
    width = sky1_img.get_width()

    for x in range(5):
        screen.blit(sky2_img, ((x * width) -scroll * 0.5,SCREEN_HEIGHT - sky2_img.get_height()))
    for x in range(7):
        screen.blit(sky1_img,((x * width) -scroll *0.7 ,SCREEN_HEIGHT - sky1_img.get_height()))

#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0),
                         (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    #horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE),
                         (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data): #world_data 리스트에 담겨져있는 에셋가져옴,
        for x, tile in enumerate(row):
            if tile >= 0: #해당 이미지 인덱스에 있는 타일 blit
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#create buttons
save_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT + LOWER_MARGIN - 80, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 80, load_img, 1)
backup_button = button.Button(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT + LOWER_MARGIN - 80, backup_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (40 * button_col), 40 * button_row,
                                img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 7:
        button_row += 1
        button_col = 0

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    #Press UP or DOWN to change level
    #level draw
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT+ LOWER_MARGIN-90)

    #save and load data
    if save_button.draw(screen):
        #save level data
        #pickle_out = open(f'level{level}_data', 'wb')
        #pickle.dump(world_data, pickle_out)
        #pickle_out.close()
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    if backup_button.draw(screen):
        #back up data
        with open(f'level{level}backup_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        #load in level data
        scroll = 0 #0인 지점으로 돌리기
        #world_data = []
        #pickle_in = open(f'level{level}_data', 'rb')
        #world_data = pickle.load(pickle_in)
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    #draw tile panel and tiles
    pygame.draw.rect(screen, BG, (SCREEN_WIDTH,0, SIDE_MARGIN, SCREEN_WIDTH))

    #choose a tile
    button_count = 0
    saved_tile = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 *scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    #add new tiles to the screen
    #마우스 좌표
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE #cell크기로 나눈 몫-> 한 칸 좌표
    x = (pos[0] + scroll) // TILE_SIZE #cell크기로 나눈 몫-> 한 칸 좌표
    y = pos[1] // TILE_SIZE

    #tile 좌표 체크
    pressed = pygame.key.get_pressed()
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1: #마우스 왼쪽
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1: #마우스 오른쪽
            world_data[y][x] = -1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit() #while문 탈출 후 quit