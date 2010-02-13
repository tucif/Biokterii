import random

DEFAULT_WIDTH=10
DEFAULT_HEIGHT=10

class Sprite():
    def __init__(self):
        """Default initial sprite values"""
        self.id=random.randint(0,10000);
        self.posX=0
        self.posY=0
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.colPosX=self.posX
        self.colPosY=self.posY
        self.colWidth=DEFAULT_WIDTH
        self.colHeight=DEFAULT_HEIGHT
        self.isVisible=True
        self.color=(random.random(),random.random(),random.random())
        self.alpha=1.0
    def __str__(self):
        return "Sprite - ID:"+self.id

    def update(self):
        pass

    def paint(self,window):
        """How a sprite is painted by default"""
        if self.isVisible:
            window.rectangle(self.posX,self.posY,self.width,self.height)
            window.set_source_rgba(self.color[0],self.color[1],self.color[2],self.alpha)
            window.fill()
