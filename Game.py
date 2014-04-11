#!/usr/bin/env python

import pygame, sys, pyganim, os
from pygame.locals import *
from Player import Player
from Input import Input

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


def main():

    # Load sprite assets
    IMAGESDICT, animObjs = LoadSpriteAssets()

    # Main game surface
    DISPLAYSURF = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Make the screen

    # Colors
    BLACK = (0,0,0)

    # Calculate starting position of player
    startX = SCREEN_X - LEN_SPRT_X
    startY = SCREEN_Y - LEN_SPRT_Y

    # Hold info on keys pressed, held, released
    keyinput = Input()

    # Initialize gamemap and Player
    player = Player(IMAGESDICT, animObjs)
    player.rect.topleft = startX, startY

    # Sprite Groups
    allsprites = pygame.sprite.RenderPlain(player)

    # Add floor tiles
    #for x in range(0, SCREEN_X/LEN_SPRT_X):
    #    tile = Sprite(DISPLAYSURF, IMAGESDICT['ground'], LEN_SPRT_X*x, SCREEN_Y-LEN_SPRT_Y, False)
    #    gamemap.addSprite(tile)

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
            # Play player shooting animation
            player.shoot()
        elif keyinput.wasKeyPressed(K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif not player.shooting:
            player.stopMoving()

        # Vertical logic
        if keyinput.wasKeyPressed(K_UP):
            player.jump()

        # Update
        allsprites.update()

        # Draw
        allsprites.draw(DISPLAYSURF)

        pygame.display.update()
        fpsClock.tick(FPS)



def LoadSpriteAssets():
    # Find out if in Windows or Unix/Linux then load SpriteSheet
    if os.path.isfile('assets\\jubal_64.png'):
        SHEET = pygame.image.load('assets\\jubal_64.png')
    elif os.path.isfile('assets//jubal_64.png'):
        SHEET = pygame.image.load('assets//jubal_64.png')

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

    return IMAGESDICT, animObjs



if __name__ == "__main__":
    main()
