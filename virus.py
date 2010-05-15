import gtk
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
        self.maxHp=1000

        self.hp=self.maxHp
        self.deltaHp=1
        self.transHp=self.hp

        self.isDead=False
        self.velX=0.0;
        self.velY=0.0;

    def __str__(self):
        return "The Virus  hp:%d pos=[%d,%d]" % (self.hp,self.posX,self.posY)

    def get_type(self):
        return "Virus"

    def update(self):
        print "virus update"
        Sprite.update(self)
        self.posX+=self.velX
        self.posY+=self.velY
        if self.hp<=0:
            self.isDead=True

        if self.transHp<self.hp-1:
            self.transHp+=self.deltaHp
        elif self.transHp>self.hp+1:
            self.transHp-=self.deltaHp
        elif self.transHp != self.hp:
            self.transHp=self.hp

    def paint(self,window):
        pass

