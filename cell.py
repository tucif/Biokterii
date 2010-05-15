import math
import random
import gtk, gobject, cairo

from sprite import Sprite

from operator import indexOf

DEFAULT_WIDTH=45
DEFAULT_HEIGHT=45

COLOR_LIST=[("Red",[0.8,0.2,0.1]),("Green",[0,0.8,0.3]),("Blue",[0,0.8,0.8])]

OUTER_SHAPE_LIST=["Simple","CircleStroke","CircleFill","Square","DoubleSquare"]
ROT_DIRECTION_LIST=[("Left",-1),("Right",1)]
INNER_SHAPE_LIST=["None","CircleStroke","CircleFill","SquareStroke","SquareFill"]

STATUS_LIST=["Dying","Dead","Repelled"]

MAX_DYING_PARTICLES=40

class Cell(Sprite):
    def __init__(self, posX=0, posY=0, velX=0, velY=0):
        Sprite.__init__(self,posX,posY)
        self.width=DEFAULT_WIDTH
        self.height=DEFAULT_HEIGHT
        self.maxHp=100
        self.hp=self.maxHp
        self.isDead=False

        self.type=type
        self.name="Cell"

        #rotation
        self.deltaRot=0.05*random.choice([1,-1])
        self.transDeltaRot=0.05
        self.deltaDeltaRot=0.0005

        self.rotDirection=-1
        self.rot=0
        self.status=None

        #movement
        self.degreeRot=0
        self.deltaDegreeRot=random.random()/15

        #effects
        self.dyingParticles=[]

        #available
        self.isAvailable=True

        #attributes
        self.outerShape=random.choice(OUTER_SHAPE_LIST)
        self.outerColor,self.outerColorList=random.choice(COLOR_LIST)
        self.outerRotation,self.outerRotationVal=random.choice(ROT_DIRECTION_LIST)

        self.innerShape=random.choice(INNER_SHAPE_LIST)
        if self.innerShape=="None":
            self.innerColor,self.innerColorList=("Black",[0,0,0])
        else:
            self.innerColor,self.innerColorList=random.choice(COLOR_LIST)

    def get_characteristic(self,characName):
        if characName == "outerShape":
            return self.outerShape
        if characName == "outerColor":
            return self.outerColor
        if characName == "outerRotation":
            return self.outerRotation
        if characName == "innerShape":
            return self.innerShape
        if characName == "innerColor":
            return self.innerColor

    def __str__(self):
        return self.name

    def get_type(self):
        return "Cell"

    def update(self):
        Sprite.update(self)
        self.rot+=self.transDeltaRot*self.rotDirection
        self.degreeRot+=self.deltaDegreeRot

        if abs(self.transDeltaRot-self.deltaRot)<=self.deltaDeltaRot*2:
            self.transDeltaRot=self.deltaRot
        elif self.transDeltaRot < self.deltaRot:
            self.transDeltaRot+=self.deltaDeltaRot
        elif self.transDeltaRot > self.deltaRot:
            self.transDeltaRot-=self.deltaDeltaRot

    def paint(self,window):
        window.stroke() #patch to prevent a stray line from appearing between text and cells

        for particle in self.dyingParticles:
            particle.paint(window)

        window.save()
        ThingMatrix = cairo.Matrix ( 1, 0, 0, 1, 0, 0 )
        window.transform ( ThingMatrix )
        cairo.Matrix.translate(ThingMatrix, self.posX+self.width/2,self.posY+self.height/2)
        cairo.Matrix.rotate( ThingMatrix, self.outerRotationVal*self.rot)
        cairo.Matrix.translate(ThingMatrix, -(self.posX+self.width/2),-(self.posY+self.height/2))
        window.transform ( ThingMatrix ) # and commit it to the context

        #draw outer shape
        window.set_line_width(1)
        if self.outerShape=="Simple" or self.outerShape=="CircleStroke" or self.outerShape=="CircleFill":
            window.arc(self.posX+self.width/2, self.posY+self.height/2, self.width/2, 0.5, 2 * math.pi)
            window.set_source_rgba(self.outerColorList[0],self.outerColorList[1],self.outerColorList[2],self.transAlpha)
            window.set_line_width(1)
            window.stroke()
            window.restore()
            window.save()
            cairo.Matrix.translate(ThingMatrix, self.width/2,self.width*0.12)
            window.transform ( ThingMatrix )
            if self.outerShape=="CircleStroke":
                window.arc(self.posX+self.width/2, self.posY+self.height/2, self.width*0.14, 0.0, 2 * math.pi)
                window.set_source_rgba(self.outerColorList[0],self.outerColorList[1],self.outerColorList[2],self.transAlpha)
                window.stroke()
            if self.outerShape=="CircleFill":
                window.arc(self.posX+self.width/2, self.posY+self.height/2, self.width*0.14, 0.0, 2 * math.pi)
                window.set_source_rgba(self.outerColorList[0],self.outerColorList[1],self.outerColorList[2],self.transAlpha)
                window.fill_preserve()
                window.stroke()
            window.restore()

        if self.outerShape=="Square" or self.outerShape=="DoubleSquare":
            window.set_source_rgba(self.outerColorList[0],self.outerColorList[1],self.outerColorList[2],self.transAlpha)
            window.rectangle(self.posX,self.posY,self.width, self.height)
            window.stroke()
            if self.outerShape=="DoubleSquare":
                window.save()
                ThingMatrix = cairo.Matrix ( 1, 0, 0, 1, 0, 0 )
                window.transform ( ThingMatrix )
                cairo.Matrix.translate(ThingMatrix, self.posX+self.width/2,self.posY+self.height/2)
                cairo.Matrix.rotate( ThingMatrix, 4 )
                cairo.Matrix.translate(ThingMatrix, -(self.posX+self.width/2),-(self.posY+self.height/2))
                window.transform ( ThingMatrix ) # and commit it to the context
                window.rectangle(self.posX,self.posY,self.width, self.height)
                window.stroke()
                window.restore()
            window.restore()

        #draw inner shape "None","CircleStroke","CircleFill","SquareStroke","SquareFill"
        if self.innerShape!="None":
            window.set_source_rgba(self.innerColorList[0],self.innerColorList[1],self.innerColorList[2],self.transAlpha)

            window.save()
            window.set_line_width(1)

            if self.innerShape=="CircleStroke":
                window.arc(self.posX+self.width/2, self.posY+self.height/2, self.width*0.2, 0, 2 * math.pi)
                window.stroke()
            if self.innerShape=="CircleFill":
                window.arc(self.posX+self.width/2, self.posY+self.height/2, self.width*0.2, 0, 2 * math.pi)
                window.fill()
            if self.innerShape=="SquareStroke" or self.innerShape=="SquareFill":
                ThingMatrix = cairo.Matrix ( 1, 0, 0, 1, 0, 0 )
                window.transform ( ThingMatrix )
                cairo.Matrix.translate(ThingMatrix, self.posX+self.width/2,self.posY+self.height/2)
                cairo.Matrix.rotate( ThingMatrix, math.sin(self.rot))
                cairo.Matrix.translate(ThingMatrix, -(self.posX+self.width/2),-(self.posY+self.height/2))
                window.transform ( ThingMatrix ) # and commit it to the context
                if self.innerShape=="SquareStroke":
                    window.rectangle((self.posX+self.width/2)-self.width/6,(self.posY+self.height/2)-self.height/6,self.width/3, self.height/3)
                    window.stroke()
                if self.innerShape=="SquareFill":
                    window.rectangle((self.posX+self.width/2)-self.width/6,(self.posY+self.height/2)-self.height/6,self.width/3, self.height/3)
                    window.fill()
            window.restore()