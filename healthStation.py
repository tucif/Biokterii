import random

from sprite import Sprite

DEFAULT_WIDTH=15
DEFAULT_HEIGHT=25

class HealthStation(Sprite):
    def __init__(self, healRatio, posX=0, posY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(0.0,1.0,0.0)
        self.healRatio = healRatio

    def __str__(self):
        return "A Health Station id:%d - healRatio:%d" % (self.id,self.healRatio)

    def get_type(self):
        return "Health Station"

    def update(self):
        Sprite.update(self)

    def paint(self,window):
        Sprite.paint(self,window)

