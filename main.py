# coding: utf-8

import gtk
#import cairo
import gobject
import pygtk
import random
#from datetime import datetime

from display import display

pygtk.require('2.0')

#Lienzo es donde se pintara todo
class Lienzo(gtk.DrawingArea):
    def __init__(self, ventana):
        """"""
        super(Lienzo, self).__init__()

        #Cambiar el color de fondo de la ventana
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(0,0,0))
        # Pedir el tamano de la ventana
        self.set_size_request(400,400)

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
        self.init_simulation()

       
        self.draggingObject = None
        self.corriendo = True

        self.objetoSeleccionado=[]


    def actualizar_dragged(self,widget,event):
        if self.draggingObject:
            self.draggingObject.posX=event.x
            self.draggingObject.posY=event.y

    def on_timer(self):
        self.update()
        return True

    def init_simulation(self):
        """Inicializacion de valores"""
        gobject.timeout_add(20, self.on_timer)



    def update(self):
        
        self.queue_draw()

    def paint(self, widget, event):
        """Nuestro metodo de pintado propio"""

        #Se crea un widget de cairo que despues se usara para desplegar
        #todo en la ventana
        cr = widget.window.cairo_create()
        #Le decimos a cairo que pinte su widget por primera vez.
        cr.set_source_rgb(0,0,0)
        cr.paint()

        #pintar a los agentes
        
        display(cr)
        

        

        #pintar efecto de selección sobre un agente
        if self.objetoSeleccionado:
            cr.set_line_width(2)
            cr.set_source_rgba(random.random(), 1, random.random(), 0.3)
            cr.rectangle(self.objetoSeleccionado.posX-20,self.objetoSeleccionado.posY-20,
                            self.objetoSeleccionado.ancho+40, self.objetoSeleccionado.alto+40)

            cr.stroke()

        #pintar la información del agente seleccionado
        

    #Para drag & drop
    def button_press(self,widget,event):
        if event.button == 1:
            self.objetoSeleccionado=[]
            lstTemp = self.listaAgentes + self.listaObjetos
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



class Main(gtk.Window):
    def __init__(self):
        super(Main, self).__init__()
        self.faseActual = 4
        self.set_title('Biokterii')
        self.set_size_request(400,400)
        self.set_resizable(True)
        self.set_position(gtk.WIN_POS_CENTER)
        #mainBox contiene el menu superior, contentBox(menu,lienzo) y el menu inferior
        self.mainBox = gtk.VBox(False,0)
        self.mainBox.set_size_request(400,400)

        
        #contentBox contiene el menu lateral y lienzo
        self.contentBox= gtk.HBox(False,0) #Recibe False para no se homogeneo
        
        self.lienzo=Lienzo(self)
        self.lienzo.set_size_request(400,400)

        self.contentBox.pack_start(self.lienzo, expand=False, fill=True, padding=0)
        
        #Empaquetado de todos los controles
        
        self.mainBox.pack_start(self.contentBox,expand=False, fill=True, padding=0)
        #Agregar la caja que contiene todo a la ventana
        self.add(self.mainBox)
        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def pausar_lienzo(self, widget):
        self.lienzo.pausar()

    def correr_lienzo(self, widget):
        self.lienzo.correr()

    

Main()
gtk.main()
