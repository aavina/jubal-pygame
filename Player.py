import pygame, sys, time, pyganim
from pygame.locals import *
from Bullet import *

kWalkSpeed = 3
kJumpSpeed = 4
kJumpClockDelay = 500

# Character colors
RED_CHARACTER_COLOR = pygame.Color(170, 41, 41, 255)
BLUE_CHARACTER_COLOR = pygame.Color(41, 48, 170, 255)



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

		# Tells if sprite is currently compensating for left-shoot collision detection
		self.move_shoot = False

		self.image = self.imagesdict['j_rightface']
		self.rect = self.image.get_rect()

		self.currentColor = RED_CHARACTER_COLOR


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

		# Change the colors for the current surface image
		pixarr = pygame.PixelArray(self.image)
		if self.currentColor == RED_CHARACTER_COLOR:
			pixarr.replace(BLUE_CHARACTER_COLOR, RED_CHARACTER_COLOR)
		else:
			pixarr.replace(RED_CHARACTER_COLOR, BLUE_CHARACTER_COLOR)
		del pixarr # Must delete or else surface will be locked

	def toggleColor(self):
		if self.currentColor == RED_CHARACTER_COLOR:
			self.currentColor = BLUE_CHARACTER_COLOR
		else:
			self.currentColor = RED_CHARACTER_COLOR

	# Check if moving horizontally or shooting
	def checkHorizontalAndShooting(self, environment):
		moving = False

		if self.shooting:
			if self.graphics['shoot_right'].isFinished():
				self.shooting = False
				self.bulletcreated = False
				self.image = self.imagesdict['j_rightface']
				if self.direction == LEFT:
					self.image = pygame.transform.flip(self.image, True, False)
					self.rect.move_ip(22,0)
					self.move_shoot = False
			else:
				self.graphics['shoot_right'].play()
				self.image = self.graphics['shoot_right'].getCurrentFrame()
				if self.direction == LEFT:
					self.image = pygame.transform.flip(self.image, True, False)
					if not self.move_shoot:
						self.rect.move_ip(-22,0)
						self.move_shoot = True

				# If first frame played already, need to create bullet
		        if self.graphics['shoot_right']._propGetCurrentFrameNum() == 1 and not self.bulletcreated:
		        	if self.direction == RIGHT:
						startx, starty = self.rect[0] + 64, self.rect[1] + 19
						bullet = Bullet(RIGHT, self.imagesdict['bullet'])
						bullet.rect.topleft = startx, starty
						(self.groups())[0].add(bullet)
						self.bulletcreated = True
			        else:
						startx, starty = self.rect[0], self.rect[1] + 19
						bullet = Bullet(LEFT, self.imagesdict['bullet'])
						bullet.rect.topleft = startx, starty
						(self.groups())[0].add(bullet)
						self.bulletcreated = True

		elif self.direction == RIGHT:
			self.graphics['right_walk'].play()
			self.image = self.graphics['right_walk'].getCurrentFrame()
			oldpos, newpos = self.rect, self.rect.move(kWalkSpeed,0)
			moving = True
		elif self.direction == LEFT:
			self.graphics['right_walk'].play()
			self.image = pygame.transform.flip(self.graphics['right_walk'].getCurrentFrame(), True, False)
			oldpos, newpos = self.rect, self.rect.move(-kWalkSpeed,0)
			moving = True


		# Check for horizontal collision
		if moving:
			moving = False
			self.rect = newpos
			collision_list = pygame.sprite.spritecollide(self, environment, False)

			if len(collision_list) > 0:
				# Revert back to old position if there's a collision
				self.rect = oldpos



	# Check if moving vertically.
	# Sprite group environment is passed in to check for any collisions.
	# Also in charge of gravity
	def checkVertical(self, environment):
		moving = False
		self.falling = True
		img = None

		if self.jumping:
			# Change to jumping sprite if not shooting
			if not self.shooting:
				dirstr = ''
				self.graphics['jump_right'].play()
				self.image = self.graphics['jump_right'].getCurrentFrame()
				if not self.facingRight:
					self.image = pygame.transform.flip(self.image, True, False)
			# Set sprite to move
			oldpos, newpos = self.rect, self.rect.move((0,-kJumpSpeed))
			moving = True
			# Check if we've reached end of jump timer
			if(pygame.time.get_ticks() - (self.jumpClock+kJumpClockDelay)) > 0:
				self.jumpClock = 0
				self.jumping = False
				self.falling = True
		elif self.falling:
			# Change to falling sprite if not shooting
			if not self.shooting:
				img = self.graphics['jump_right'].getFrame(2)
				if not self.facingRight:
					img = pygame.transform.flip(img, True, False)

			oldpos, newpos = self.rect, self.rect.move((0,kJumpSpeed))
			moving = True

			# Let sprite fall until bounds are met
			if self.rect[1] + kJumpSpeed + 60 <= 400 and self.rect != newpos:
				self.rect = newpos
			else:
				self.falling = False
				moving = False
				self.graphics['jump_right'].stop()

		# Check vertical collision
		if moving:
			self.rect = newpos
			collision_list = pygame.sprite.spritecollide(self, environment, False)
			if len(collision_list) > 0:
				# Check for special case of collision when shooting
				if self.shooting and self.direction is LEFT:
					newpos2 = self.rect.move(22,0)
					self.rect = newpos2
					collision_list = pygame.sprite.spritecollide(self, environment, False)
					if len(collision_list) > 0:
						self.rect = oldpos
					else:
						self.rect = newpos

				else:
					# Revert back to old position if there's a collision
					self.rect = oldpos

					# If we're falling, stop
					if self.falling:
						self.falling = False
			# Check special case of collision
			elif self.shooting and self.direction is LEFT:
				newpos2 = self.rect.move(22,0)
				self.rect = newpos2
				collision_list = pygame.sprite.spritecollide(self, environment, False)
				if len(collision_list) > 0:
					self.rect = oldpos
				else:
					self.rect = newpos

			elif img != None:
				self.image = img



	def moveLeft(self):
		# Can't turn if shooting
		if not self.shooting:
			self.direction = LEFT
			self.facingRight = False


	def moveRight(self):
		# Can't turn if shooting
		if not self.shooting:
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
			self.graphics['shoot_right'].play()
			self.image = self.graphics['shoot_right'].getCurrentFrame()
			self.direction = RIGHT
			if not self.facingRight:
				self.image = pygame.transform.flip(self.image, True, False)
				self.direction = LEFT
