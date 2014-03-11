import pygame, sys, time, pyganim
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()
DURATION = 0.1

# Screen size
SCREEN_X=400
SCREEN_Y=400

# This is the lentgh of the sprite
LEN_SPRT_X=64
LEN_SPRT_Y=64

# This is where the sprite is found on the sheet
SPRT_RECT_X=0  
SPRT_RECT_Y=LEN_SPRT_Y

# Rate of movement
MOVEMENT_RATE_X = 4
MOVEMENT_RATE_Y = 4

# Load the sprite sheet
sheet = pygame.image.load('jubal_64.png')


# Global dictionary that contains all Surface objects
IMAGESDICT = {
    'j_normal': sheet.subsurface(pygame.Rect(0, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_rightface': sheet.subsurface(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftface': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*3), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
}

# Define the different animation types
animTypes = 'right_walk left_walk shoot_right shoot_left jump_right jump_left'.split()

# These tuples contain (base_x, base_y, numOfFrames)
# numOfFrames is in the x-direction
animTypesInfo = {
    'right_walk':   (SPRT_RECT_X+LEN_SPRT_X, SPRT_RECT_Y, 2),
    'left_walk':    (SPRT_RECT_X+(LEN_SPRT_X*4), SPRT_RECT_Y, 2),
    'shoot_right':  (LEN_SPRT_X, 0, 4),
    'shoot_left':   (LEN_SPRT_X*5, 0, 4),
    'jump_right':   (0, LEN_SPRT_Y*2, 7),
    'jump_left':    (0, LEN_SPRT_Y*3, 7)
}

animObjs = {}
for animType in animTypes:
    xbase = (animTypesInfo[animType])[0]
    ybase = (animTypesInfo[animType])[1]
    numFrames = (animTypesInfo[animType])[2]
    imagesAndDurations = [(sheet.subsurface(pygame.Rect(xbase+(LEN_SPRT_X*num), ybase, LEN_SPRT_X, LEN_SPRT_Y)), DURATION) for num in range(numFrames)]
    loopforever = True
    if(animType == 'shoot_right' or animType == 'shoot_left'):
        loopforever = False

    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations, loop=loopforever)


# Key variables
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

FACING_RIGHT = True

keyPressed = False

DISPLAYSURF = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Make the screen

sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #find the sprite you want
img = 'j_normal'
jubal = IMAGESDICT[img]

BLACK = (0,0,0)

# Calculate starting position
startX = SCREEN_X/2 - LEN_SPRT_X/2
startY = SCREEN_Y - LEN_SPRT_Y

# Initialize starting position
position = (startX, startY)

moveDown = moveLeft = moveRight = playerShooting = playerDirection = False
playerJumping = playerFalling = False

jumpClock = 0
while True:
    DISPLAYSURF.fill(BLACK)

    # Check for game events
    for event in pygame.event.get():
        # Reset player direction
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and not playerShooting:
            # Handle key presses
            keyPressed = True
            if event.key == K_LEFT:
                FACING_RIGHT = False
                playerDirection = LEFT
                moveLeft = True
            elif event.key == K_RIGHT:
                FACING_RIGHT = True
                playerDirection = RIGHT
                moveRight = True
            elif event.key == K_UP and not playerJumping and not playerFalling:
                playerJumping = True
                jumpClock = pygame.time.get_ticks()
            elif event.key == K_DOWN:
                playerDirection = DOWN
                moveDown = True
            elif event.key == K_SPACE:
                playerShooting = True
                if FACING_RIGHT:
                    animObjs['shoot_right'].play()
                    playerDirection = RIGHT
                else:
                    animObjs['shoot_left'].play()
                    playerDirection = LEFT
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == KEYUP and not playerShooting:
            if event.key == K_LEFT:
                moveLeft = False
                playerDirection = LEFT
            elif event.key == K_RIGHT:
                moveRight = False
                playerDirection = RIGHT
            elif event.key == K_UP:
                if FACING_RIGHT:
                    playerDirection = RIGHT
                else:
                    playerDirection = LEFT
            elif event.key == K_DOWN:
                moveDown = False
                playerDirection = DOWN
            elif event.key == K_SPACE:
                if FACING_RIGHT:
                    playerDirection = RIGHT
                else:
                    playerDirection = LEFT

    # Check for movement
    if moveLeft or moveRight or playerJumping or playerShooting or playerFalling:
        if playerShooting and FACING_RIGHT:
            if animObjs['shoot_right'].isFinished():
                playerShooting = False
                playerDirection = RIGHT
                DISPLAYSURF.blit(IMAGESDICT['j_rightface'],position)
            else:
                animObjs['shoot_right'].blit(DISPLAYSURF, position)
        elif playerShooting and not FACING_RIGHT:
            if animObjs['shoot_left'].isFinished():
                playerShooting = False
                playerDirection = LEFT
                DISPLAYSURF.blit(IMAGESDICT['j_leftface'],position)
            else:
                animObjs['shoot_left'].blit(DISPLAYSURF, position)
        elif playerDirection == LEFT:
            mv_x = position[0] - MOVEMENT_RATE_X
            mv_y = position[1]
            if(mv_x > 0):
                position = (mv_x, mv_y)
            animObjs['left_walk'].play()
            animObjs['left_walk'].blit(DISPLAYSURF, position)
        elif playerDirection == RIGHT:
            mv_x = position[0] + MOVEMENT_RATE_X
            mv_y = position[1]
            if((mv_x + LEN_SPRT_X) < SCREEN_X):
                position = (mv_x, mv_y)
            animObjs['right_walk'].play()
            animObjs['right_walk'].blit(DISPLAYSURF, position)

        # Falling Mechanics
        if playerJumping and FACING_RIGHT:
            mv_x = position[0]
            mv_y = position[1] - MOVEMENT_RATE_Y
            if(mv_y > 0):
                position = (mv_x, mv_y)
            animObjs['jump_right'].play()
            animObjs['jump_right'].blit(DISPLAYSURF, position)
            if (pygame.time.get_ticks() - (jumpClock+200)) > 0:
                jumpClock = 0
                playerJumping = False
                playerFalling = True
        elif playerJumping and not FACING_RIGHT:
            mv_x = position[0]
            mv_y = position[1] - MOVEMENT_RATE_Y
            if(mv_y > 0):
                position = (mv_x, mv_y)
            animObjs['jump_left'].play()
            animObjs['jump_left'].blit(DISPLAYSURF, position)
            if (pygame.time.get_ticks() - (jumpClock+200)) > 0:
                jumpClock = 0
                playerJumping = False
                playerFalling = True
        elif playerFalling and FACING_RIGHT:
            mv_x = position[0]
            mv_y = position[1] + MOVEMENT_RATE_Y
            if((mv_y + LEN_SPRT_Y) < SCREEN_X):
                position = (mv_x, mv_y)
            else:
                playerFalling = False
            DISPLAYSURF.blit(IMAGESDICT['j_rightface'],position)
        elif playerFalling and not FACING_RIGHT:
            mv_x = position[0]
            mv_y = position[1] + MOVEMENT_RATE_Y
            if((mv_y + LEN_SPRT_Y) < SCREEN_X):
                position = (mv_x, mv_y)
            else:
                playerFalling = False
            DISPLAYSURF.blit(IMAGESDICT['j_leftface'],position)
    else:
        # Standing
        if playerDirection == DOWN:
            DISPLAYSURF.blit(IMAGESDICT['j_normal'],position)
        if FACING_RIGHT == False:
            DISPLAYSURF.blit(IMAGESDICT['j_leftface'],position)
        elif FACING_RIGHT:
            DISPLAYSURF.blit(IMAGESDICT['j_rightface'],position)

    pygame.display.update()
    fpsClock.tick(FPS)
