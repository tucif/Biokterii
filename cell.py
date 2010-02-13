import random
from sprite import Sprite

DEFAULT_WIDTH=40
DEFAULT_HEIGHT=40

class Cell(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.posX=random.randint(0,400)
        self.posY=random.randint(0,400)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(0.0,0.0,1.0)
        self.alpha=0.8

    def __str__(self):
        return "A cell id:%d pos=[%d,%d]"% (self.id,self.posX,self.posY)

    def update(self):
        Sprite.update(self)

    def paint(self,window):
         Sprite.paint(self,window)
         