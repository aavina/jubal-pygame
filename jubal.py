import pygame, sys, time, pyganim
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()
DURATION = 0.1

#Screen size
SCREEN_X=400
SCREEN_Y=400

#This is the lentgh of the sprite
LEN_SPRT_X=64
LEN_SPRT_Y=64

#This is where the sprite is found on the sheet
SPRT_RECT_X=0  
SPRT_RECT_Y=LEN_SPRT_Y

# Sprite sheet
sheet = pygame.image.load('jubal_64.png') #Load the sheet


# Global dictionary that contains all Surface objects
IMAGESDICT = {
    'j_normal': sheet.subsurface(pygame.Rect(0, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_rightface': sheet.subsurface(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftface': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*3), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
}

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
    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)


moveConductor = pyganim.PygConductor(animObjs)

# Key variables
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

keyPressed = False

DISPLAYSURF = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Make the screen

sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #find the sprite you want
img = 'j_normal'
jubal = IMAGESDICT[img]

BLACK = (0,0,0)

middleX = SCREEN_X/2 - LEN_SPRT_X/2
middleY = SCREEN_Y/2 - LEN_SPRT_Y/2
backdrop = pygame.Rect(middleX, middleY, SCREEN_X, SCREEN_Y) #make the whole screen so you can draw on it
position = (middleX, middleY)

moveUp = moveDown = moveLeft = moveRight = playerShooting = False

while True:
    DISPLAYSURF.fill(BLACK)

    for event in pygame.event.get():
        # Reset player direction
        playerDirection = None
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            # Handle key presses
            keyPressed = True
            if event.key == K_LEFT:
                playerDirection = LEFT
                moveLeft = True
            elif event.key == K_RIGHT:
                playerDirection = RIGHT
                moveRight = True
            elif event.key == K_UP:
                playerDirection = UP
                moveUp = True
            elif event.key == K_DOWN:
                playerDirection = DOWN
                moveDown = True
            elif event.key == K_SPACE:
                playerShooting = True
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
                playerDirection = LEFT
            elif event.key == K_RIGHT:
                moveRight = False
                playerDirection = RIGHT
            elif event.key == K_UP:
                moveUp = False
                playerDirection = UP
            elif event.key == K_DOWN:
                moveDown = False
                playerDirection = DOWN
            elif event.key == K_SPACE:
                playerShooting = False

    if moveLeft or moveRight or moveUp or playerShooting:
        moveConductor.play()
        if playerDirection == LEFT:
            animObjs['left_walk'].blit(DISPLAYSURF, position)
        elif playerDirection == RIGHT:
            animObjs['right_walk'].blit(DISPLAYSURF, position)
        elif playerDirection == UP:
            animObjs['jump_right'].blit(DISPLAYSURF, position)
        elif playerShooting:
            animObjs['shoot_right'].blit(DISPLAYSURF, position)
    else:
        # Standing
        if playerDirection == LEFT:
            DISPLAYSURF.blit(IMAGESDICT['j_leftface'],backdrop)
        elif playerDirection == RIGHT:
            DISPLAYSURF.blit(IMAGESDICT['j_rightface'],backdrop)
        elif playerDirection == UP:
            DISPLAYSURF.blit(IMAGESDICT['j_rightface'],backdrop)
        elif playerDirection == DOWN:
            DISPLAYSURF.blit(IMAGESDICT['j_normal'],backdrop)

    pygame.display.update()
    fpsClock.tick(FPS)
