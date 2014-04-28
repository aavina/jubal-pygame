#!/usr/bin/env python

import pygame, sys, pyganim, os
from pygame.locals import *
from Player import Player
from Input import Input
from Tile import Tile
from Bullet import Bullet

pygame.init()

FPS = 30 # frames per second settings
fpsClock = pygame.time.Clock()
DURATION = 0.1

# Screen size
SCREEN_X=400
SCREEN_Y=400

# This is the length of the sprite box
LEN_SPRT_X=64
LEN_SPRT_Y=64

# Dimension of the player sprite
DIM_SPRT_X = 24
DIM_SPRT_Y = 60


def main():

    # Determine assets
    sprite_asset, bullet_sound_asset = DetermineAssets()

    # Load sprite assets
    IMAGESDICT, animObjs = LoadSpriteAssets(sprite_asset)

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
    player = Player(IMAGESDICT, animObjs, bullet_sound_asset)
    player.rect.topleft = startX, startY

    # Add tiles
    startx = 0
    starty = SCREEN_Y - LEN_SPRT_Y/2
    tile = Tile(IMAGESDICT['ground'])
    tile.rect.topleft = startx, starty

    # Sprite Groups
    allsprites = pygame.sprite.RenderPlain(player)
    environment = pygame.sprite.RenderPlain(tile)

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

        # Remove bullets that leave screen
        for sprite in allsprites:
            if isinstance(sprite, Bullet):
                if sprite.rect[0] > SCREEN_X or sprite.rect[0] < 0:
                    allsprites.remove(sprite)

        # Update
        allsprites.update(environment)
        environment.update(allsprites)

        # Draw
        allsprites.draw(DISPLAYSURF)
        environment.draw(DISPLAYSURF)

        pygame.display.update()
        fpsClock.tick(FPS)


# Determines what filesystem accessor to use and retreives graphic and sound assets
def DetermineAssets():
    # Find out if in Windows or Unix/Linux then load SpriteSheet
    if os.path.isfile('assets\\jubal_64.png'):
        SHEET = pygame.image.load('assets\\jubal_64.png')
        bullet_sound = pygame.mixer.Sound("assets\\bullet.wav")
    elif os.path.isfile('assets//jubal_64.png'):
        SHEET = pygame.image.load('assets//jubal_64.png')
        bullet_sound = pygame.mixer.Sound("assets//bullet.wav")

    return SHEET, bullet_sound



def LoadSpriteAssets(SHEET):
    # Global dictionary that contains all static images
    IMAGESDICT = {
        'j_normal': SHEET.subsurface(pygame.Rect(22, 2, 24, 60)),
        'j_rightface': SHEET.subsurface(pygame.Rect(18, LEN_SPRT_Y + 4, DIM_SPRT_X, DIM_SPRT_Y)),
        'bullet': SHEET.subsurface(pygame.Rect(LEN_SPRT_X*8, LEN_SPRT_Y*3, 2, 2)),
        'ground': SHEET.subsurface(pygame.Rect(LEN_SPRT_X*4, LEN_SPRT_Y*5, LEN_SPRT_X, LEN_SPRT_Y/2)),
    }

    IMAGESDICT['j_leftface'] = pygame.transform.flip(IMAGESDICT['j_rightface'], True, False)

    # Define the different animation types
    animTypes = 'right_walk shoot_right jump_right'.split()

    # These tuples contain (base_x, base_y, numOfFrames)
    # numOfFrames is in the x-direction
    animTypesInfo = {
        'right_walk':   (LEN_SPRT_X + 24, LEN_SPRT_Y + 4, 4),
        'shoot_right':  (LEN_SPRT_X + 18, 4, 4),
        'jump_right':   (0 + 18, (LEN_SPRT_Y*2) + 4, 7),
        #'normal':       (0, 0, 1),
        #'right_face':   (0, LEN_SPRT_Y, 1),
        #'left_face':    (0, LEN_SPRT_Y*3, 1)
    }

    animObjs = {}
    for animType in animTypes:
        xbase = (animTypesInfo[animType])[0]
        ybase = (animTypesInfo[animType])[1]
        numFrames = (animTypesInfo[animType])[2]
        loopforever = True

        if(animType == 'right_walk'):
            imagesAndDurations = [(SHEET.subsurface(pygame.Rect(xbase+(LEN_SPRT_X*num), ybase, 18, DIM_SPRT_Y)), DURATION) for num in range(numFrames)]
        elif(animType == 'shoot_right'):
            loopforever = False
            imagesAndDurations = [(SHEET.subsurface(pygame.Rect(xbase+(LEN_SPRT_X*num), ybase, 46, LEN_SPRT_Y)), DURATION) for num in range(numFrames)]
        elif(animType == 'jump_right'):
            imagesAndDurations = [(SHEET.subsurface(pygame.Rect(xbase+(LEN_SPRT_X*num), ybase, 24, LEN_SPRT_Y)), DURATION) for num in range(numFrames)]

        animObjs[animType] = pyganim.PygAnimation(imagesAndDurations, loop=loopforever)

    return IMAGESDICT, animObjs



if __name__ == "__main__":
    main()
