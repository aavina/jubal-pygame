# Directions to move
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
NONE = 'none'

# Speed of bullet
BULLETSPEED = 10

class Bullet:
	def __init__(self, displaysurf, imagesdict, direction, startx, starty):
		self.displaysurf = displaysurf
		self.imagesdict = imagesdict
		self.direction = direction
		self.position = (startx, starty)


	def draw(self):
		self.displaysurf.blit(self.imagesdict['bullet'],self.position)


	def update(self):
		if self.direction == RIGHT:
			new_x = self.position[0] + BULLETSPEED
			new_y = self.position[1]
		else:
			new_x = self.position[0] - BULLETSPEED
			new_y = self.position[1]

		self.position = (new_x, new_y)