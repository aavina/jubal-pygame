
class Tile:
  def __init__(self, displaysurf, imagesdict, x, y):
    self.displaysurf = displaysurf
    self.imagesdict = imagesdict
    self.position = (x,y)


  def draw(self):
    self.displaysurf.blit(self.imagesdict['ground'], self.position)