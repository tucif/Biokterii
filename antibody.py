import random
from sprite import Sprite

DEFAULT_WIDTH=5
DEFAULT_HEIGHT=5

class Antibody(Sprite):
    def __init__(self, posX=0, posY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(1,1,1)

    def __str__(self):
        return "Antivirus id:%d, pos=[%d,%d]" % (self.id,self.posX,self.posY)

    def update(self):
        Sprite.update(self)

    def paint(self,window):
        Sprite.paint(self,window)

