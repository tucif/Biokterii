import random

from sprite import Sprite

DEFAULT_WIDTH=20
DEFAULT_HEIGHT=20

class Virus(Sprite):
    def __init__(self, posX=0, posY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(1,1,1)
        self.maxHp=1000
        self.hp=self.maxHp
        self.isDead=False
        self.velX=0.0
        self.velY=0.0
        self.tempLevel= random.randint(0,100)    #0~100
        self.phLevel=random.randint(0,14)       #0~14
        self.aggresiveness=random.randint(0,100) #0~100
        self.visibility=random.randint(0,100)    #0~100

    def __str__(self):
        return "Virus  [%d|%d|%d|%d]" % (self.tempLevel, self.phLevel, self.aggresiveness, self.visibility)

    def get_type(self):
        return "Virus"

    def update(self):
        Sprite.update(self)
        self.color=(float(self.tempLevel)/100,0,1-float(self.tempLevel)/100)

        self.posX+=self.velX
        self.posY+=self.velY
        if self.hp<=0:
            self.isDead=True
        else:
            self.isDead=False;

    def paint(self,window):
        Sprite.paint(self,window)

