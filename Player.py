import pygame, sys, time, pyganim
from pygame.locals import *
from Bullet import *

kWalkSpeed = 3
kJumpSpeed = 4
kJumpClockDelay = 500

class Player(pygame.sprite.Sprite):
	def __init__(self, imagesdict, graphics, bullet_sound):
		pygame.sprite.Sprite.__init__(self)
		self.imagesdict = imagesdict
		self.graphics = graphics
		self.bullet_sound = bullet_sound

		self.facingRight = True
		self.jumping = False
		self.falling = False
		self.shooting = False
		self.bulletcreated = False
		self.jumpClock = 0
		self.direction = NONE

		self.image = self.imagesdict['j_rightface']
		self.rect = self.image.get_rect()


	def update(self, environment):

		# Check horizontal and shooting movement
		self.checkHorizontalAndShooting(environment)

		# Check vertical movement
		self.checkVertical(environment)

		# Check if idle
		if self.direction == NONE and self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.image = self.imagesdict['j_rightface']
		elif self.direction == NONE and not self.facingRight and not self.shooting and not self.jumping and not self.falling:
			self.image = self.imagesdict['j_leftface']



	# Check if moving horizontally or shooting
	def checkHorizontalAndShooting(self, environment):
		moving = False
		
		if self.shooting and self.direction == LEFT:
			if self.graphics['shoot_left'].isFinished():
				self.shooting = False
				self.bulletcreated = False
				self.image = self.imagesdict['j_leftface']
			else:
				self.graphics['shoot_left'].play()
				self.image = self.graphics['shoot_left'].getCurrentFrame()
		        if self.graphics['shoot_left']._propGetCurrentFrameNum() == 1 and not self.bulletcreated:
		            startx = self.rect[0]
		            starty = self.rect[1] + 22
		            bullet = Bullet(LEFT, self.imagesdict['bullet'])
		            bullet.rect.topleft = startx, starty
		            (self.groups())[0].add(bullet)
		            self.bulletcreated = True
		elif self.shooting and self.direction == RIGHT:
			if self.graphics['shoot_right'].isFinished():
				self.shooting = False
				self.bulletcreated = False
				self.image = self.imagesdict['j_rightface']
			else:
				self.graphics['shoot_right'].play()
				self.image = self.graphics['shoot_right'].getCurrentFrame()
		        if self.graphics['shoot_right']._propGetCurrentFrameNum() == 1 and not self.bulletcreated:
		            startx = self.rect[0] + 64
		            starty = self.rect[1] + 22
		            bullet = Bullet(RIGHT, self.imagesdict['bullet'])
		            bullet.rect.topleft = startx, starty
		            (self.groups())[0].add(bullet)
		            self.bulletcreated = True
		elif self.direction == LEFT:
			self.graphics['left_walk'].play()
			self.image = self.graphics['left_walk'].getCurrentFrame()
			oldpos, newpos = self.rect, self.rect.move((-kWalkSpeed,0))
			moving = True
		elif self.direction == RIGHT:
			self.graphics['right_walk'].play()
			self.image = self.graphics['right_walk'].getCurrentFrame()
			oldpos, newpos = self.rect, self.rect.move((kWalkSpeed,0))
			moving = True

		# Check for horizontal collision
		if moving:
			moving = False
			self.rect = newpos
			collision_list = pygame.sprite.spritecollide(self, environment, False)

			if len(collision_list) > 0:
				# Revert back to old position if there's a collision
				self.rect = oldpos



	# Check if moving vertically
	# Sprite group environment is passed in to check for any collisions
	def checkVertical(self, environment):
		moving = False
		
		if self.jumping:
			# Change to jumping sprite if not shooting
			if not self.shooting:
				dirstr = ''
				if self.facingRight:
					dirstr = 'jump_right'
				else:
					dirstr = 'jump_left'
				self.graphics[dirstr].play()
				self.image = self.graphics[dirstr].getCurrentFrame()
			# Set sprite to move
			oldpos, newpos = self.rect, self.rect.move((0,-kJumpSpeed))
			moving = True
			# Check if we've reached end of jump timer
			if(pygame.time.get_ticks() - (self.jumpClock+kJumpClockDelay)) > 0:
				self.jumpClock = 0
				self.jumping = False
				self.falling = True
		elif self.falling:
			# Change to facing sprite if not shooting
			if not self.shooting:
				if self.facingRight:
					dirstr = 'j_rightface'
				else:
					dirstr = 'j_leftface'
				self.image = self.imagesdict[dirstr]
			oldpos, newpos = self.rect, self.rect.move((0,kJumpSpeed))
			moving = True

			# Let sprite fall until bounds are met
			if self.rect[1] + kJumpSpeed + 64 <= 400:
				self.rect = newpos
			else:
				self.falling = False
				moving = False

		# Check vertical collision
		if moving:
			moving = False
			self.rect = newpos
			collision_list = pygame.sprite.spritecollide(self, environment, False)
			if len(collision_list) > 0:
				# Revert back to old position if there's a collision
				self.rect = oldpos

				# If we're falling, stop
				if self.falling:
					self.falling = False



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
			# Play bullet sound
			self.bullet_sound.play()
			self.shooting = True
			# Set and start sprite animation
			if self.facingRight:
				self.graphics['shoot_right'].play()
				self.image = self.graphics['shoot_right'].getCurrentFrame()
				self.direction = RIGHT
			else:
				self.graphics['shoot_left'].play()
				self.image = self.graphics['shoot_left'].getCurrentFrame()
				self.direction = LEFT
