import gtk

from cell import Cell
from sprite import Sprite
from virus import Virus

from constants import VIRUS_IMAGE
from constants import STATION_ON, STATION_OFF

DISPLAY_IDS=True

iterStationOn=STATION_ON.get_iter()

def display_simulation(window,virusList,cellList):
    """Fucntion that diplays the whole simulation"""
    display_lines(window,cellList)
    display_cells(window,cellList)
    display_virus(window,virusList)
    
def display_virus(window,virusList):
    """Fucntion that diplays the virus"""
    for virus in virusList:
        pixbuf = VIRUS_IMAGE
        pixbuf1=pixbuf.scale_simple(virus.width,virus.height,gtk.gdk.INTERP_BILINEAR)

        window.save()
        window.set_source_pixbuf(pixbuf1,virus.posX,virus.posY)
        window.paint()
        window.restore()

        #draw fitness line
        green=((virus.transHp-25)*1.3333)/1000
        red = 1-green
            
        window.set_source_rgba(red,green,0,1)
        window.rectangle(virus.posX+1,virus.posY+virus.height+1,float(virus.transHp*(virus.width-1)/1000), 4)
        window.fill()

        
def display_cells(window, cellList):
    """Fucntion that diplays the cells"""
    for cell in cellList:
        if cell.get_type() == "Health Station":
            if cell.isDead=="True":
                pixbuf=STATION_OFF
            else:
                pixbuf = iterStationOn.get_pixbuf()
                iterStationOn.advance()
                
            pixbuf=pixbuf.scale_simple(cell.width,cell.height,gtk.gdk.INTERP_BILINEAR)
            window.save()
            window.set_source_pixbuf(pixbuf,cell.posX,cell.posY)
            window.paint()
            window.restore()
            
        else:
            cell.paint(window)

def display_lines(window, cellList):
    for i in xrange(len(cellList)-1):
            draw_line_between(window,cellList[i],cellList[i+1])

def draw_line_between(window,sprite1,sprite2):
    """Draws a line between two sprites, if one of them is not a sprite,
    it fails silently"""
    if (isinstance(sprite1,Sprite) and (isinstance(sprite2,Sprite))):
        [sp1CenterX,sp1CenterY]=sprite1.get_center()
        [sp2CenterX,sp2CenterY]=sprite2.get_center()
        window.set_source_rgb(1.0, 1.0, 0.0)
        window.move_to(sp1CenterX,sp1CenterY)
        window.line_to(sp2CenterX,sp2CenterY)
        window.stroke()