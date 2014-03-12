import pygame, sys, time, pyganim
from pygame.locals import *

class Input:

	def __init__(self):
		# Private dictionaries
		self._releasedKeys = {}
		self._heldKeys = {}
		self._pressedKeys = {}

	# Clears the released/held key dictionaries
	def clearKeys(self):
		self._releasedKeys.clear()
		self._pressedKeys.clear()


	def keyDownEvent(self, key):
		self._pressedKeys[key] = True
		self._heldKeys[key] = True


	def keyUpEvent(self, key):
		self._releasedKeys[key] = True
		self._heldKeys[key] = False


	def wasKeyPressed(self, key):
		return self._pressedKeys.get(key)
		return ret


	def wasKeyReleased(self, key):
		return self._releasedKeys.get(key)


	def isKeyHeld(self, key):
		return self._heldKeys.get(key)
