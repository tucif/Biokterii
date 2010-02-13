import random
from sprite import Sprite

DEFAULT_WIDTH=5
DEFAULT_HEIGHT=5

class Antibody(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.posX=random.randint(0,400)
        self.posY=random.randint(0,400)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(1,1,1)

    def __str__(self):
        return "Antivirus id:\d, pos=[\d,\d]" % (self.id,self.posX,self.posY)

    def update(self):
        Sprite.update(self)

    def paint(self,window):
        Sprite.paint(self,window)

