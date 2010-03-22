import random
import gtk, gobject, cairo

from sprite import Sprite
from constants import VIRUS_IMAGE
from constants import WINDOW_SIZE
from constants import MAX_FITNESS

DEFAULT_WIDTH=50
DEFAULT_HEIGHT=50

class Virus(Sprite):
    def __init__(self, posX=0, posY=0,
                 tempLevel = 0,
                 phLevel= 0,
                 aggresiveness=0,
                 visibility=0
                 ):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.color=(1,1,1)
        self.maxHp=1000
        self.hp=self.maxHp
        self.isDead=False
        self.velX=0.0
        self.velY=0.0
        self.tempLevel= tempLevel    #0~127
        self.phLevel= phLevel       #0~15
        self.aggresiveness=aggresiveness #0~127
        self.visibility=visibility    #0~127

        self.fitness=0
        self.fitnessPercentage=0

        self.imagen=VIRUS_IMAGE

        #rotation
        self.deltaRot=(float(self.aggresiveness)*100/127)*0.1/100
        self.rot=0

    def __str__(self):
        return "Virus [%d|%d|%d|%d] ->fit:%d @ (%f,%f)" % (self.tempLevel, self.phLevel, self.aggresiveness, self.visibility, self.fitness, self.posX,self.posY)

    def get_type(self):
        return "Virus"

    def update_fitness(self,environment):
        self.tempFitness=127-abs(environment.temp-self.tempLevel)
        self.phFitness=127-(15-abs(environment.ph-self.phLevel))*8.46
        self.reactFitness=127-abs(environment.reactivity-self.aggresiveness)
        self.radarFitness=127-abs(environment.radar-self.visibility)

        self.fitness=self.tempFitness+self.phFitness+self.reactFitness+self.radarFitness

        self.fitnessPercentage=float(self.fitness)*100/MAX_FITNESS

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
        #Sprite.paint(self,window)
        pixbuf = self.imagen
        pixbuf=pixbuf.scale_simple(self.width,self.height,gtk.gdk.INTERP_BILINEAR)

        #temperature representation

        #ph representation

        window.save()
        ThingMatrix = cairo.Matrix ( 1, 0, 0, 1, 0, 0 )

        ## Next, move the drawing to it's x,y
        window.transform ( ThingMatrix ) # Changes the context to reflect that

        cairo.Matrix.translate(ThingMatrix, self.posX+self.width/2,self.posY+self.height/2)
        #aggresiveness representation
        cairo.Matrix.rotate( ThingMatrix, self.rot ) # Do the rotation
        cairo.Matrix.translate(ThingMatrix, -(self.posX+self.width/2),-(self.posY+self.height/2))

        window.transform ( ThingMatrix ) # and commit it to the context

        window.set_source_pixbuf(pixbuf,self.posX,self.posY)
        window.paint()

        window.restore()
        self.rot+=self.deltaRot

        #visibility representation
        

        #ends strange stuff


        #draw fitness line
        if self.fitnessPercentage<=25:
            red=1
            green=0
        else:
            green=((self.fitnessPercentage-25)*1.3333)/100
            red = 1-green
        window.set_source_rgba(red,green,0,1)
        window.rectangle(self.posX+1,self.posY+self.height+1,float(self.fitnessPercentage*(self.width-1)/100), 4)
        window.fill()

        #window.draw(handle, dst, src)

        #draw fitness line container
        window.set_line_width(1)
        window.set_source_rgba(1,1,1,1)
        window.rectangle(self.posX,self.posY+self.height,self.width, 5)
        window.stroke()

