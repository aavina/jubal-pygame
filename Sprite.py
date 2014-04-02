class Sprite:

  def __init__(self, displaysurf, surface, x, y, updateable):
    self.displaysurf = displaysurf
    self.surface = surface
    self.position = (x,y)
    self._updateable = updateable


  def draw(self):
    self.displaysurf.blit(self.surface, self.position)

  def update(self):
    return