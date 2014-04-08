import pygame, sys, time, pyganim
from pygame.locals import *
from Bullet import *
from GameMap import *

kWalkSpeed = 3
kJumpSpeed = 4
kJumpClockDelay = 200

class Player(pygame.sprite.Sprite):
	def __init__(self, imagesdict,graphics):
		pygame.sprite.Sprite.__init__(self)
		self.imagesdict = imagesdict
		self.graphics = graphics

		self.facingRight = True
		self.jumping = False
		self.falling = False
		self.shooting = False
		self.bulletcreated = False
		self.jumpClock = 0
		self.direction = NONE

		self.image = self.imagesdict['j_rightface']
		self.rect = self.image.get_rect()

	'''
	def draw(self):
		if self.shooting and self.facingRight:
			if self.graphics['shoot_right'].isFinished():
				self.shooting = self.bulletcreated = False
				self.displaysurf.blit(self.imagesdict['j_rightface'],self.position)
			else:
				self.graphics['shoot_right'].blit(self.displaysurf,self.position)
				# Create bullet after gun explosion
				if self.graphics['shoot_right']._propGetCurrentFrameNum() == 1 and not self.bulletcreated:
					startx = self.position[0] + self.len_sprt_x
					starty = self.position[1] + 22
					bullet = Bullet(self.displaysurf, self.imagesdict['bullet'], RIGHT, startx, starty)
					self.bulletcreated = True
		elif self.shooting and not self.facingRight:
			if self.graphics['shoot_left'].isFinished():
				self.shooting = self.bulletcreated = False
				self.displaysurf.blit(self.imagesdict['j_leftface'],self.position)
			else:
				self.graphics['shoot_left'].blit(self.displaysurf,self.position)
				if self.graphics['shoot_left']._propGetCurrentFrameNum() == 1 and not self.bulletcreated:
					startx = self.position[0]
					starty = self.position[1] + 22
					bullet = Bullet(self.displaysurf, self.imagesdict['bullet'], LEFT, startx, starty)
					self.bulletcreated = True
		elif self.direction == LEFT and not self.jumping and not self.falling:
			self.graphics['left_walk'].play()
			self.graphics['left_walk'].blit(self.displaysurf, self.position)
		elif self.direction == RIGHT and not self.jumping and not self.falling:
			self.graphics['right_walk'].play()
			self.graphics['right_walk'].blit(self.displaysurf, self.position)
        # Handle jumping
		if self.jumping and not self.shooting:
			dirstr = ''
			if self.facingRight:
				dirstr = 'jump_right'
			else:
				dirstr = 'jump_left'
			self.graphics[dirstr].play()
			self.graphics[dirstr].blit(self.displaysurf, self.position)
		elif self.falling and not self.shooting:
			if self.facingRight:
				self.displaysurf.blit(self.imagesdict['j_rightface'],self.position)
			else:
				self.displaysurf.blit(self.imagesdict['j_leftface'],self.position)

		# Idle
		if self.direction == NONE and self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.displaysurf.blit(self.imagesdict['j_rightface'],self.position)
		elif self.direction == NONE and not self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.displaysurf.blit(self.imagesdict['j_leftface'],self.position)			
		'''

	def update(self):
		# Check if moving horizontally
		if self.direction == LEFT and not self.shooting:
			self.graphics['left_walk'].play()
			self.image = self.graphics['left_walk'].getCurrentFrame()
			newpos = self.rect.move((-kWalkSpeed,0))
			self.rect = newpos
		elif self.direction == RIGHT and not self.shooting:
			self.graphics['right_walk'].play()
			self.image = self.graphics['right_walk'].getCurrentFrame()
			newpos = self.rect.move((kWalkSpeed,0))
			self.rect = newpos

		# Check if moving vertically
		if self.jumping:
			newpos = self.rect.move((0,-kJumpSpeed))
			self.rect = newpos
			if(pygame.time.get_ticks() - (self.jumpClock+kJumpClockDelay)) > 0:
				self.jumpClock = 0
				self.jumping = False
				self.falling = True
		elif self.falling:
			newpos = self.rect.move((0, kJumpSpeed))
			if self.rect[1] + kJumpSpeed + 64 <= 400:
				self.rect = newpos
			else:
				self.falling = False

		# Idle
		if self.direction == NONE and self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.image = self.imagesdict['j_rightface']
		elif self.direction == NONE and not self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.image = self.imagesdict['j_leftface']		


	def moveLeft(self):
		self.direction = LEFT
		self.facingRight = False


	def moveRight(self):
		self.direction = RIGHT
		self.facingRight = True


	def stopMoving(self):
		self.direction = NONE


	def jump(self):
		if not self.jumping and not self.falling:
			self.jumping = True
			self.jumpClock = pygame.time.get_ticks()


	def shoot(self):
		if not self.shooting:
			self.shooting = True
			if self.facingRight:
				self.graphics['shoot_right'].play()
				self.direction = RIGHT
			else:
				self.graphics['shoot_left'].play()
				self.direction = LEFT