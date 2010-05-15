import gtk
import random

from sprite import Sprite

DEFAULT_WIDTH=35
DEFAULT_HEIGHT=35

class HealthStation(Sprite):
    def __init__(self, healRatio, posX=0, posY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.healRatio = random.randint(400,800)
        self.isDead=False

    def __str__(self):
        return "Health Station | heals: %d | Order: " % (self.healRatio)

    def get_type(self):
        return "Health Station"

    def update(self):
        Sprite.update(self)

    def paint(self,window):
        pass

