import random

from sprite import Sprite

DEFAULT_WIDTH=20
DEFAULT_HEIGHT=20

class Virus(Sprite):
    def __init__(self, posX=0, posY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(0.3,0.6,0.5)

    def __str__(self):
        return "The Virus pos=[%d,%d]" % (self.posX,self.posY)

    def get_type(self):
        return "Virus"

    def update(self):
        Sprite.update(self)

    def paint(self,window):
        Sprite.paint(self,window)

