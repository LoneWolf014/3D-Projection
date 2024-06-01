# PACKAGES
import pygame as pg
import sys
import math
#### MAP WORLD #######################################################################
# CONSTANTS
HEIGHT = 480
WIDTH = HEIGHT*2
MAP_SIZE = 16
TILE_SIZE = int((WIDTH/2)/MAP_SIZE)
# CONSTANTS USED IN RAYCASTING ALGORITHM
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi/3
HALF_FOV = FOV/2
CASTED_RAYS = 120
STEP_ANGLE = FOV/CASTED_RAYS
SCALE = (WIDTH/2)/CASTED_RAYS
# TEXTURES
sky = pg.image.load("sky.png")
sky_trans = pg.transform.scale(sky, (HEIGHT, 240*2))
#PLAYER_WORLD#########################################################################
#PLAYER CONSTANTS
PLAYER_X = HEIGHT/2
PLAYER_Y = HEIGHT/2
PLAYER_ANGLE = math.pi
PLAYER_SPEED = 5
#set map
MAP = (
    "1111111111111111"
    "1___1__________1"
    "1___1__________1"
    "1___1__________1"
    "1______________1"
    "1______________1"
    "1_______1111___1"
    "1__________1___1"
    "1__________1___1"
    "1__________1___1"
    "1______________1"
    "1______________1"
    "1______1_______1"
    "1______1_______1"
    "1______1_______1"
    "1111111111111111"
)

#init pygame
pg.init()

#create window
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("raycasting #1")

#init timer
clock = pg.time.Clock()

#draw map
def draw_map():
    for row in range (16):
        for col in range (16):
            
            square = row * MAP_SIZE + col

            pg.draw.rect(
                win, (255, 255, 255) if MAP[square] == "1" else (100, 100, 100),
                (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE-1, TILE_SIZE-1)
            )
    #draw player direction
    pg.draw.line(win, (255, 255, 0), (PLAYER_X, PLAYER_Y),
                                     (PLAYER_X - math.sin(PLAYER_ANGLE) * 100 ,
                                      PLAYER_Y + math.cos(PLAYER_ANGLE) * 100), 2)
    #draw player FOV
    pg.draw.line(win, (255, 255, 0), (PLAYER_X, PLAYER_Y),
                                     (PLAYER_X - math.sin(PLAYER_ANGLE - HALF_FOV) * 100 ,
                                      PLAYER_Y + math.cos(PLAYER_ANGLE - HALF_FOV) * 100), 2)
    
    pg.draw.line(win, (255, 255, 0), (PLAYER_X, PLAYER_Y),
                                     (PLAYER_X - math.sin(PLAYER_ANGLE + HALF_FOV) * 100 ,
                                      PLAYER_Y + math.cos(PLAYER_ANGLE + HALF_FOV) * 100), 2)
    #draw player
    pg.draw.circle(win, (0, 255, 0), (PLAYER_X, PLAYER_Y), 8)
##############################################################################################
###############
###############
# RAY CASTING ALGORITHM ###########################################################
def cast_rays():
    #define left most angle of FOV
    start_angle =  PLAYER_ANGLE - HALF_FOV

    #loop condition
    for ray in range(CASTED_RAYS):
        #cast ray step by step
        for depth in range(MAX_DEPTH):
            # get ray target co-ordinates 
            target_x = PLAYER_X - math.sin(start_angle) * depth
            target_y = PLAYER_Y + math.cos(start_angle) * depth
            
            #convert target x, y coordinates to map row, col
            row = int(target_y / TILE_SIZE)
            col = int(target_x / TILE_SIZE)

            #Calculate MAP SQUARE INDEX
            square = row * MAP_SIZE + col

            #if ray is collided with the wall then the cast should stop and as indication that it 
            # hits the wall we are setting the color to the wall which hits the FOV
            if MAP[square] == "1":
                pg.draw.rect(win, (0, 255, 0),
                                   (col * TILE_SIZE,
                                   row * TILE_SIZE,
                                   TILE_SIZE-1,
                                   TILE_SIZE-1))
                # draw casted ray
                pg.draw.line(win, (0, 0, 255), (PLAYER_X, PLAYER_Y), (target_x, target_y))

                #color shading or shadowing the walls
                color = 255 / (1+ depth * depth * 0.0001)

                # fixing fish eye effect
                depth *= math.cos(PLAYER_ANGLE - start_angle)

                #calculate wall height
                wall_height = 21000/(depth + 0.0001)

                #draw 3D projection (rectangle by rectangle)
                pg.draw.rect(win, (color, 0/color, 0/color), (
                             HEIGHT + ray *  SCALE, 
                             HEIGHT/2 - wall_height/2,
                             SCALE, wall_height))
                break
        #increment angle by a single step
        start_angle += STEP_ANGLE
# MAIN LOOP ##################################################################################
run = True
forward = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            run = False

    #collision detection
    row = int(PLAYER_Y / TILE_SIZE)
    col = int(PLAYER_X / TILE_SIZE)
    #Calculate MAP SQUARE INDEX
    square = row * MAP_SIZE + col

    if MAP[square] == "1":
        if forward:
            PLAYER_X -= -math.sin(PLAYER_ANGLE) * PLAYER_SPEED
            PLAYER_Y -=  math.cos(PLAYER_ANGLE) * PLAYER_SPEED
        else:
            PLAYER_X += -math.sin(PLAYER_ANGLE) * PLAYER_SPEED
            PLAYER_Y +=  math.cos(PLAYER_ANGLE) * PLAYER_SPEED

    #update 2d background
    win.fill((0,0,0))
    #update 3d background
    pg.draw.rect(win, (100, 100, 100), (480, HEIGHT/2, HEIGHT, HEIGHT))
    win.blit(sky_trans, (480, -HEIGHT/2))
    #pg.draw.rect(win, (200, 200, 200), (480, -HEIGHT/2, HEIGHT, HEIGHT))
    #draw 2d map
    draw_map()

    #apply ray casting
    cast_rays()
    #get user input
    keys = pg.key.get_pressed()
    #handle user input
    if keys[pg.K_LEFT]:
        PLAYER_ANGLE -= 0.1
    if keys[pg.K_RIGHT]:
        PLAYER_ANGLE += 0.1
    # Player Movement
    if keys[pg.K_UP]:
        forward = True
        PLAYER_X += -math.sin(PLAYER_ANGLE) * PLAYER_SPEED
        PLAYER_Y +=  math.cos(PLAYER_ANGLE) * PLAYER_SPEED
    if keys[pg.K_DOWN]:
        forward = False
        PLAYER_X -= -math.sin(PLAYER_ANGLE) * PLAYER_SPEED
        PLAYER_Y -=  math.cos(PLAYER_ANGLE) * PLAYER_SPEED 

    #set FPS
    clock.tick(30)

    #display FPS
    fps = str(int(clock.get_fps()))

    #pickup the font
    font = pg.font.SysFont("Technology", 32)

    #create font surface
    fps_surface = font.render("FPS : " + fps, False, (255, 0, 0))

    #print fps to screen
    win.blit(fps_surface, (480,0))
    #update
    pg.display.flip()
pg.quit()
##############################################################################################
   #Player movements extras
"""sin_a = math.sin(PLAYER_ANGLE)
cos_a = math.cos(PLAYER_ANGLE)
dx, dy = 0, 0
speed = PLAYER_SPEED
speed_sin = speed * sin_a
speed_cos = speed * cos_a

if keys[pg.K_w]:
    dx += -speed_sin
    dy += speed_cos
if keys[pg.K_a]:
    dx += speed_cos
    dy += speed_sin
if keys[pg.K_s]:
    dx += speed_sin
    dy += -speed_cos
if keys[pg.K_d]:
    dx += -speed_cos
    dy += -speed_sin
    
    PLAYER_X += dx
    PLAYER_Y += dy """