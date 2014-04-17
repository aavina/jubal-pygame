import pygame, sys, time, pyganim
from pygame.locals import *
from Bullet import Bullet

class Tile(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()


    # Sprite group is passed in to check if any bullets hit the tile
    def update(self, allsprites):
    	# Check if any bullets hit. If so, remove them
    	collision_list = pygame.sprite.spritecollide(self, allsprites, False)
    	for sprite in collision_list:
    		if isinstance(sprite, Bullet):
    			allsprites.remove(sprite)