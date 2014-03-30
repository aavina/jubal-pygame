import pygame, sys, time, pyganim
from pygame.locals import *
from Player import Player
from Input import Input
from Tile import Tile

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()
DURATION = 0.1

# Screen size
SCREEN_X=400
SCREEN_Y=400

# This is the length of the sprite
LEN_SPRT_X=64
LEN_SPRT_Y=64

# This is where the sprite is found on the sheet
SPRT_RECT_X=0  
SPRT_RECT_Y=LEN_SPRT_Y

# Load the sprite SHEET
SHEET = pygame.image.load('jubal_64.png')

# Global dictionary that contains all static images
IMAGESDICT = {
    'j_normal': SHEET.subsurface(pygame.Rect(0, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_rightface': SHEET.subsurface(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftface': SHEET.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*5), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'bullet': SHEET.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*8), SPRT_RECT_Y*3, 2, 2)),
    'ground': SHEET.subsurface(pygame.Rect(0, SPRT_RECT_Y*4, LEN_SPRT_X, LEN_SPRT_Y)),
}

# Define the different animation types
animTypes = 'right_walk left_walk shoot_right shoot_left jump_right jump_left right_face left_face normal'.split()

# These tuples contain (base_x, base_y, numOfFrames)
# numOfFrames is in the x-direction
animTypesInfo = {
    'right_walk':   (SPRT_RECT_X+LEN_SPRT_X, SPRT_RECT_Y, 4),
    'left_walk':    (SPRT_RECT_X+(LEN_SPRT_X*6), SPRT_RECT_Y, 4),
    'shoot_right':  (LEN_SPRT_X, 0, 4),
    'shoot_left':   (LEN_SPRT_X*5, 0, 4),
    'jump_right':   (0, LEN_SPRT_Y*2, 7),
    'jump_left':    (0, LEN_SPRT_Y*3, 7),
    'normal':       (0, 0, 1),
    'right_face':   (0, LEN_SPRT_Y, 1),
    'left_face':    (0, LEN_SPRT_Y*3, 1)
}

animObjs = {}
for animType in animTypes:
    xbase = (animTypesInfo[animType])[0]
    ybase = (animTypesInfo[animType])[1]
    numFrames = (animTypesInfo[animType])[2]
    imagesAndDurations = [(SHEET.subsurface(pygame.Rect(xbase+(LEN_SPRT_X*num), ybase, LEN_SPRT_X, LEN_SPRT_Y)), DURATION) for num in range(numFrames)]
    loopforever = True
    if(animType == 'shoot_right' or animType == 'shoot_left'):
        loopforever = False

    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations, loop=loopforever)

# Main game surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Make the screen

SHEET.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #find the sprite you want

# Colors
BLACK = (0,0,0)

# Calculate starting position of player
startX = SCREEN_X/2 - LEN_SPRT_X/2
startY = SCREEN_Y - (LEN_SPRT_Y*2)

# Hold info on keys pressed, held, released
keyinput = Input()

# Initialize Player and a tile
player = Player(DISPLAYSURF, IMAGESDICT, LEN_SPRT_X, LEN_SPRT_Y, SCREEN_X, SCREEN_Y, animObjs, startX, startY)
tile = Tile(DISPLAYSURF, IMAGESDICT, 0, SCREEN_Y-LEN_SPRT_Y)

# Start game loop
while True:
    # Clear key info
    keyinput.clearKeys()

    # Draw screen black
    DISPLAYSURF.fill(BLACK)

    # Check for game events
    for event in pygame.event.get():
        # Reset player direction
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            # Handle key presses
            keyinput.keyDownEvent(event.key)
        elif event.type == KEYUP:
            keyinput.keyUpEvent(event.key)

    # Player horizontal logic
    if keyinput.isKeyHeld(K_LEFT) and keyinput.isKeyHeld(K_RIGHT):
        player.stopMoving()
    elif keyinput.isKeyHeld(K_LEFT):
        player.moveLeft()
    elif keyinput.isKeyHeld(K_RIGHT):
        player.moveRight()
    elif keyinput.wasKeyPressed(K_SPACE):
        player.shoot()
    elif keyinput.wasKeyPressed(K_ESCAPE):
        pygame.quit()
        sys.exit()
    else:
        player.stopMoving()

    # Vertical logic
    if keyinput.wasKeyPressed(K_UP):
        player.jump()

    # Draw player
    player.draw()
    tile.draw()

    # Update player
    player.update()

    pygame.display.update()
    fpsClock.tick(FPS)
