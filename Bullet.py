import pygame

# Directions to move
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NONE = 'none'

# Speed of bullet
BULLETSPEED = 10

class Bullet(pygame.sprite.Sprite):
	def __init__(self, direction, image):
		pygame.sprite.Sprite.__init__(self)
		self.direction = direction
		self.image = image
		self.rect = self.image.get_rect()


	def update(self, environment):
		if self.direction == RIGHT:
			newpos = self.rect.move(BULLETSPEED,0)
			self.rect = newpos
		else:
			newpos = self.rect.move(-BULLETSPEED,0)
			self.rect = newpos
