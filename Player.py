import pygame, sys, time, pyganim
from pygame.locals import *
from Bullet import *

kWalkSpeed = 4
kJumpSpeed = 4
kJumpClockDelay = 200

class Player:
	def __init__(self, displaysurf, imagesdict, len_sprt_x, len_sprt_y, scn_x, scn_y, graphics, x, y):
		self.displaysurf = displaysurf
		self.imagesdict = imagesdict
		self.len_sprt_x = len_sprt_x
		self.len_sprt_y = len_sprt_y
		self.screen_x = scn_x
		self.screen_y = scn_y
		self.graphics = graphics
		self.position = (x, y)
		self.facingRight = True
		self.jumping = False
		self.falling = False
		self.shooting = False
		self.bulletcreated = False
		self.jumpClock = 0
		self.direction = NONE
		self.bullets = []


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
					bullet = Bullet(self.displaysurf, self.imagesdict, RIGHT, startx, starty)
					self.bullets.append(bullet)
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
					bullet = Bullet(self.displaysurf, self.imagesdict, LEFT, startx, starty)
					self.bullets.append(bullet)
					self.bulletcreated = True
		elif self.direction == LEFT:
			self.graphics['left_walk'].play()
			self.graphics['left_walk'].blit(self.displaysurf, self.position)
		elif self.direction == RIGHT:
			self.graphics['right_walk'].play()
			self.graphics['right_walk'].blit(self.displaysurf, self.position)

        # Handle jumping
		if self.jumping:
			dirstr = ''
			if self.facingRight:
				dirstr = 'jump_right'
			else:
				dirstr = 'jump_left'
			self.graphics[dirstr].play()
			self.graphics[dirstr].blit(self.displaysurf, self.position)
		elif self.falling:
			if self.facingRight:
				self.displaysurf.blit(self.imagesdict['j_rightface'],self.position)
			else:
				self.displaysurf.blit(self.imagesdict['j_leftface'],self.position)

		# Idle
		if self.direction == NONE and self.facingRight and not self.shooting:
			self.displaysurf.blit(self.imagesdict['j_rightface'],self.position)
		elif self.direction == NONE and not self.facingRight and not self.shooting:
			self.displaysurf.blit(self.imagesdict['j_leftface'],self.position)

		# Draw bullets (if any)
		for bullet in self.bullets:
			bullet.draw()

	def update(self):
		# Check if moving horizontally
		if self.direction == LEFT:
			mv_x = self.position[0] - kWalkSpeed
			mv_y = self.position[1]
			if(mv_x > 0):
				self.position = (mv_x, mv_y)
		elif self.direction == RIGHT:
			mv_x = self.position[0] + kWalkSpeed
			mv_y = self.position[1]
			if((mv_x + self.len_sprt_x) < self.screen_x):
				self.position = (mv_x, mv_y)

		# Check if moving vertically
		if self.jumping:
			mv_x = self.position[0]
			mv_y = self.position[1] - kJumpSpeed
			if mv_y > 0:
				self.position = (mv_x, mv_y)
			if(pygame.time.get_ticks() - (self.jumpClock+kJumpClockDelay)) > 0:
				self.jumpClock = 0
				self.jumping = False
				self.falling = True
		elif self.falling:
			mv_x = self.position[0]
			mv_y = self.position[1] + kJumpSpeed
			if mv_y + self.len_sprt_y < self.screen_y:
				self.position = (mv_x, mv_y)
			else:
				self.falling = False

		# Update bullets
		for bullet in self.bullets:
			bulletx = bullet.position[0]
			if bulletx > self.screen_x or bulletx < 0:
				self.bullets.remove(bullet)
			else:
				bullet.update()

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