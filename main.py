# coding: utf-8

from annealing.simulatedAnnealing import start_simulation
import gtk
#import cairo
import gobject
import pygtk
import random
#from datetime import datetime
from math import pow, sqrt

pygtk.require('2.0')

from sprite import Sprite
from virus import Virus 
from virus import DEFAULT_WIDTH as VIRUS_WIDTH, DEFAULT_HEIGHT as VIRUS_HEIGHT
from cell import Cell
from cell import DEFAULT_WIDTH as CELL_WIDTH, DEFAULT_HEIGHT as CELL_HEIGHT
from healthStation import HealthStation
from healthStation import DEFAULT_HEIGHT as HS_HEIGHT, DEFAULT_WIDTH as HS_WIDTH
from antibody import Antibody
from display import display_simulation
from hud import Hud

TOTAL_CELLS = 8
TOTAL_VIRUS = 1
TOTAL_HS = 2
TOTAL_ANTIBODIES = 0
WINDOW_SIZE = 700

vir =[Virus(
           random.randint(0,WINDOW_SIZE-VIRUS_WIDTH),
           random.randint(0,WINDOW_SIZE-VIRUS_HEIGHT)
            ) for i in xrange(TOTAL_VIRUS)]
cellList=[Cell(
                random.randint(0,WINDOW_SIZE-CELL_WIDTH),
                random.randint(0,WINDOW_SIZE-CELL_HEIGHT)
                ) for i in xrange(TOTAL_CELLS)]
stationList=[HealthStation(
                            WINDOW_SIZE/TOTAL_CELLS,
                            random.randint(0,WINDOW_SIZE-HS_WIDTH),
                            random.randint(0,WINDOW_SIZE-HS_HEIGHT)
                            ) for i in xrange(TOTAL_HS)]

antibodyList=[Antibody() for i in xrange(TOTAL_ANTIBODIES)]

annealedCells = cellList+stationList



def update_annealing(widget, lienzo):
    lienzo.annealedCells = start_simulation(lienzo, vir)

#Lienzo es donde se pintara todo
class Lienzo(gtk.DrawingArea):
    def __init__(self, ventana):
        """"""
        super(Lienzo, self).__init__()

        #Cambiar el color de fondo de la ventana
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0,0,0))
        # Pedir el tamano de la ventana
        self.set_size_request(WINDOW_SIZE,WINDOW_SIZE)

        #Asignar la ventana que recibe de paramentro a la ventana que se
        #utilizara en el lienzo
        self.ventana=ventana

        #expose-event es una propiedad de DrawingArea que le dice como
        #dibujares, aqui le decimos que utilize nuestra funcion paint
        #para ese evento en vez del que trae por defaul.
        self.connect("expose-event", self.paint)
        #reconocer cuando oprimes y sueltas el mouse
        self.connect("button_press_event",self.button_press)
        self.connect("button_release_event",self.button_release)
        self.connect("motion_notify_event",self.actualizar_dragged)
        self.set_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.BUTTON_RELEASE_MASK|gtk.gdk.POINTER_MOTION_MASK)

        #Inicializar todos los valores
        self.init_simulation(None)
        self.hud=Hud()
        
        #celulas
        self.annealedCells=cellList+stationList
        self.virus=vir

        self.annealingCompleted=False
        self.initialized=False
        self.allVisited=False
        self.visitedCells=0
        self.nextCell=None

        self.draggingObject = None
        self.corriendo = True

        self.bestEnergy=0
        self.currentEnergy=0
        self.currentTemp=0

        self.objetoSeleccionado=[]

    def actualizar_dragged(self,widget,event):
        if self.draggingObject:
            self.draggingObject.posX=event.x
            self.draggingObject.posY=event.y

    def on_timer(self):
        self.update()
        return True

    def init_simulation(self,widget):
        """Inicializacion de valores"""
        gobject.timeout_add(20, self.on_timer)

    def update(self):
        self.queue_draw()

        if self.annealingCompleted and not vir[0].isDead:
            self.set_virus_vel()
            vir[0].update()        
        for cell in self.annealedCells:
            cell.update();

    

    def set_virus_vel(self):
        if not self.initialized:
            self.initialized=True
            vir[0].posX=self.annealedCells[0].get_center()[0]-(vir[0].width/2)
            vir[0].posY=self.annealedCells[0].get_center()[1]-(vir[0].height/2)
            self.nextCell=self.annealedCells[0]

        [vCenterX,vCenterY]=vir[0].get_center()
        [cCenterX,cCenterY]=self.nextCell.get_center()

        deltaX=abs(vCenterX-cCenterX)
        deltaY=abs(vCenterY-cCenterY)

        if vCenterX>cCenterX:
            vir[0].velX=-1.0*self.vel_with_delta(deltaX,deltaY,'X')
        elif vCenterX<cCenterX:
            vir[0].velX=1.0*self.vel_with_delta(deltaX,deltaY,'X')
        else:
            vir[0].velX=0

        if vCenterY>cCenterY:
            vir[0].velY=-1.0*self.vel_with_delta(deltaX,deltaY,'Y')
        elif vCenterY<cCenterY:
            vir[0].velY=1.0*self.vel_with_delta(deltaX,deltaY,'Y')
        else:
            vir[0].velY=0

        if (vCenterX>cCenterX-1 and vCenterX<cCenterX+1) and (vCenterY>cCenterY-1 and vCenterY<cCenterY+1):
            if self.nextCell in self.annealedCells:
                self.nextCell.isDead="True"
                if self.nextCell.get_type()=="Health Station":
                    self.nextCell.alpha=(0.2);
                if self.nextCell.get_type()=="Cell" and not vir[0].isDead:
                    self.nextCell.deltaRot=0;
                    self.nextCell.alpha=0.2;

                self.visitedCells=1+self.annealedCells.index(self.nextCell)

            if self.visitedCells==len(self.annealedCells):
                self.allVisited=True

            lastCell=self.nextCell

            if not self.allVisited:
                self.nextCell=self.annealedCells[self.visitedCells]
            vir[0].hp-=self.distance(lastCell, self.nextCell)

            if isinstance(lastCell,HealthStation):
                vir[0].hp+=lastCell.healRatio
                if vir[0].hp>vir[0].maxHp:
                    vir[0].hp=vir[0].maxHp

            if vir[0].transHp<=0:
                vir[0].isDead=True

    def distance(self,a, b):
        return sqrt(pow(a.posX - b.posX,2) + pow(a.posY - b.posY,2))

    def vel_with_delta(self,deltaX,deltaY,axis):
        if axis=='X':
            if deltaX>deltaY:
                return 1
            else:
                return deltaX/deltaY
        else:
            if deltaY>deltaX:
                return 1
            else:
                return deltaY/deltaX
            
    def paint(self, widget, event):
        """Nuestro metodo de pintado propio"""

        #Se crea un widget de cairo que despues se usara para desplegar
        #todo en la ventana
        cr = widget.window.cairo_create()
        #Le decimos a cairo que pinte su widget por primera vez.
        cr.set_source_rgb(0,0,0)
        cr.paint()

        #pintar a los agentes
        #display_lines(cr, self.annealedCells)
        display_simulation(cr,vir,self.annealedCells)
        self.hud.display(cr, vir+self.annealedCells)

        cr.move_to(5,15)
        text="Temperature    = %f" % self.currentTemp
        cr.show_text(text)

        cr.move_to(5,30)
        text="Best Energy      = %f" % self.bestEnergy
        cr.show_text(text)
        
        cr.move_to(5,45)
        text="Current Energy = %f" % self.currentEnergy
        cr.show_text(text)

        

        #pintar efecto de selección sobre un agente
        if self.objetoSeleccionado:
            cr.set_line_width(2)
            cr.set_source_rgba(random.random(), 1, random.random(), 0.3)
            cr.rectangle(self.objetoSeleccionado.posX-20,self.objetoSeleccionado.posY-20,
                            self.objetoSeleccionado.width+40, self.objetoSeleccionado.height+40)

            cr.stroke()

        #pintar la información del agente seleccionado
        
  
        
    #Para drag & drop
    def button_press(self,widget,event):
        if event.button == 1:
            self.objetoSeleccionado=[]
            lstTemp = antibodyList+vir+self.annealedCells
            for ob in lstTemp:
                if ob.drag(event.x,event.y):
                    self.draggingObject = ob
                    self.objetoSeleccionado=ob
                    break
                    
    def button_release(self,widget,event):
        if self.draggingObject:
            self.draggingObject.drop(event.x,event.y)
            self.draggingObject = None

    def pausar(self):
        self.corriendo=False

    def correr(self):
        self.corriendo=True

    def regenerar(self):
        for cell in self.annealedCells:
            cell.isDead=False
            if isinstance(cell,Cell):
                cell.hp=cell.maxHp
                cell.deltaRot = 0.05*random.choice([1,-1])
            cell.status=None
            cell.isAvailable=True
            cell.alpha=1

        vir[0].hp=1000
        vir[0].transHp=1000
        vir[0].isDead=False
        self.annealingCompleted=False
        self.initialized=False
        self.allVisited=False
        self.visitedCells=0
        self.nextCell=None

        self.bestEnergy=0
        self.currentEnergy=0
        self.currentTemp=0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Main(gtk.Window):
    def __init__(self):
        super(Main, self).__init__()
        self.faseActual = 4
        self.set_title('Biokterii')
        self.set_size_request(WINDOW_SIZE,WINDOW_SIZE)
        self.set_resizable(True)
        self.set_position(gtk.WIN_POS_CENTER)
        #mainBox contiene el menu superior, contentBox(menu,lienzo) y el menu inferior
        self.mainBox = gtk.VBox(False,0)
        self.mainBox.set_size_request(WINDOW_SIZE,WINDOW_SIZE)

        
        #contentBox contiene el menu lateral y lienzo
        self.contentBox= gtk.HBox(False,0) #Recibe False para no se homogeneo
        
        self.lienzo=Lienzo(self)
        self.lienzo.set_size_request(WINDOW_SIZE-20,WINDOW_SIZE-20)
        
        self.contentBox.pack_start(self.lienzo, expand=True, fill=True, padding=0)


        #Menu bar
        menuBar = gtk.MenuBar()

        filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(filemenu)

        annealMenu = gtk.MenuItem("Annealing")
        annealMenu.connect("activate", update_annealing, self.lienzo)
        filemenu.append(annealMenu)

        restartMenu = gtk.MenuItem("Restart")
        restartMenu.connect("activate", self.regenerar_lienzo)
        filemenu.append(restartMenu)

        exit = gtk.MenuItem("Exit")
        exit.connect("activate", gtk.main_quit)
        filemenu.append(exit)

        menuBar.append(filem)

        menuBox = gtk.HBox(False, 2)
        menuBox.pack_start(menuBar, False, False, 0)


        #Empaquetado de todos los controles
        self.mainBox.pack_start(menuBox,expand=True,fill=True,padding=0)
        self.mainBox.pack_start(self.contentBox,expand=True, fill=True, padding=0)

        #Agregar la caja que contiene todo a la ventana
        self.add(self.mainBox)
        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def pausar_lienzo(self, widget):
        self.lienzo.pausar()

    def correr_lienzo(self, widget):
        self.lienzo.correr()
            
    def regenerar_lienzo(self,widget):
        self.lienzo.regenerar()

if __name__ == '__main__':
    Main()
    gtk.main()
