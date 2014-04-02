from Sprite import Sprite

class GameMap:
  def __init__(self, displaysurf, imagesdict, screen_x, screen_y):
    self.displaysurf = displaysurf
    self.imagesdict = imagesdict
    self._sprites = []
    self.screen_x = screen_x
    self.screen_y = screen_y


  def addSprite(self, sprite):
    self._sprites.append(sprite)


  def draw(self):
    for sprite in self._sprites:
      sprite.draw()


  def update(self):
    for sprite in self._sprites:
      if sprite._updateable:
        sprite.update()
        if sprite.position[0] > self.screen_x or sprite.position[0] < 0:
          self._sprites.remove(sprite)
        elif sprite.position[1] > self.screen_y or sprite.position[1] < 0:
          self._sprites.remove(sprite)