from Sprite import *

# Directions to move
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NONE = 'none'

# Speed of bullet
BULLETSPEED = 10

class Bullet(Sprite):
	def __init__(self, displaysurf, surface, direction, startx, starty):
		self.displaysurf = displaysurf
		self.surface = surface
		self.position = (startx, starty)
		self.direction = direction
		self._updateable = True

	def draw(self):
		self.displaysurf.blit(self.surface, self.position)


	def update(self):
		if self.direction == RIGHT:
			new_x = self.position[0] + BULLETSPEED
			new_y = self.position[1]
		else:
			new_x = self.position[0] - BULLETSPEED
			new_y = self.position[1]

		self.position = (new_x, new_y)