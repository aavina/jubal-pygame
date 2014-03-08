import pygame, sys, time, pyganim
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()

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
    'j_rightstep1': sheet.subsurface(pygame.Rect(SPRT_RECT_X+LEN_SPRT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_rightstep2': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*2), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftface': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*3), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftstep1': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*4), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_leftstep2': sheet.subsurface(pygame.Rect(SPRT_RECT_X+(LEN_SPRT_X*5), SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingright1': sheet.subsurface(pygame.Rect(LEN_SPRT_X, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingright2': sheet.subsurface(pygame.Rect(LEN_SPRT_X*2, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingright3': sheet.subsurface(pygame.Rect(LEN_SPRT_X*3, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingright4': sheet.subsurface(pygame.Rect(LEN_SPRT_X*4, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingleft1': sheet.subsurface(pygame.Rect(LEN_SPRT_X*5, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingleft2': sheet.subsurface(pygame.Rect(LEN_SPRT_X*6, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingleft3': sheet.subsurface(pygame.Rect(LEN_SPRT_X*7, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_shootingleft4': sheet.subsurface(pygame.Rect(LEN_SPRT_X*8, 0, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight1': sheet.subsurface(pygame.Rect(0, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight2': sheet.subsurface(pygame.Rect(LEN_SPRT_X*1, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight3': sheet.subsurface(pygame.Rect(LEN_SPRT_X*2, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight4': sheet.subsurface(pygame.Rect(LEN_SPRT_X*3, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight5': sheet.subsurface(pygame.Rect(LEN_SPRT_X*4, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight6': sheet.subsurface(pygame.Rect(LEN_SPRT_X*5, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpRight7': sheet.subsurface(pygame.Rect(LEN_SPRT_X*6, LEN_SPRT_Y*2, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft1': sheet.subsurface(pygame.Rect(0, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft2': sheet.subsurface(pygame.Rect(LEN_SPRT_X*1, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft3': sheet.subsurface(pygame.Rect(LEN_SPRT_X*2, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft4': sheet.subsurface(pygame.Rect(LEN_SPRT_X*3, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft5': sheet.subsurface(pygame.Rect(LEN_SPRT_X*4, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft6': sheet.subsurface(pygame.Rect(LEN_SPRT_X*5, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y)),
    'j_jumpLeft7': sheet.subsurface(pygame.Rect(LEN_SPRT_X*6, LEN_SPRT_Y*3, LEN_SPRT_X, LEN_SPRT_Y))
    }

rightStepList = [(IMAGESDICT['j_rightstep1'], 0.1),
                 (IMAGESDICT['j_rightstep2'], 0.1)]

leftStepList = [(IMAGESDICT['j_leftstep1'], 0.1),
                 (IMAGESDICT['j_leftstep2'], 0.1)]

shootRightList = [(IMAGESDICT['j_shootingright1'], 0.1),
                  (IMAGESDICT['j_shootingright2'], 0.1),
                  (IMAGESDICT['j_shootingright3'], 0.1),
                  (IMAGESDICT['j_shootingright4'], 0.1)]

shootLeftList = [(IMAGESDICT['j_shootingleft1'], 0.1),
                  (IMAGESDICT['j_shootingleft2'], 0.1),
                  (IMAGESDICT['j_shootingleft3'], 0.1),
                  (IMAGESDICT['j_shootingleft4'], 0.1)]

jumpRightList = [(IMAGESDICT['j_jumpRight1'], 0.1),
                (IMAGESDICT['j_jumpRight2'], 0.1),
                (IMAGESDICT['j_jumpRight3'], 0.1),
                (IMAGESDICT['j_jumpRight4'], 0.1),
                (IMAGESDICT['j_jumpRight5'], 0.1),
                (IMAGESDICT['j_jumpRight6'], 0.1),
                (IMAGESDICT['j_jumpRight7'], 0.1)]

jumpLeftList = [(IMAGESDICT['j_jumpLeft1'], 0.1),
                (IMAGESDICT['j_jumpLeft2'], 0.1),
                (IMAGESDICT['j_jumpLeft3'], 0.1),
                (IMAGESDICT['j_jumpLeft4'], 0.1),
                (IMAGESDICT['j_jumpLeft5'], 0.1),
                (IMAGESDICT['j_jumpLeft6'], 0.1),
                (IMAGESDICT['j_jumpLeft7'], 0.1)]

animObjs = {}

animObjs['right_walk'] = pyganim.PygAnimation(rightStepList)
animObjs['left_walk'] = pyganim.PygAnimation(leftStepList)
animObjs['shoot_right'] = pyganim.PygAnimation(shootRightList)
animObjs['shoot_left'] = pyganim.PygAnimation(shootLeftList)
animObjs['jump_right'] = pyganim.PygAnimation(jumpRightList)
animObjs['jump_left'] = pyganim.PygAnimation(jumpLeftList)

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
