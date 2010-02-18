from sprite import Sprite
from virus import Virus

DISPLAY_IDS=True

def display_simulation(window,virusList,cellList,antibodyList):
    """Fucntion that diplays the whole simulation"""
    display_virus(window,virusList)
    display_cells(window,cellList)
    display_antibodies(window,antibodyList)
    display_lines(window,cellList)
    
def display_virus(window,virusList):
    """Fucntion that diplays the virus"""
    for virus in virusList:
        virus.paint(window)

def display_cells(window, cellList):
    """Fucntion that diplays the cells"""
    for cell in cellList:
        cell.paint(window)

def display_stations(window, stationList):
    """Fucntion that diplays the recovery stations"""
    for station in stationList:
        station.paint(window)

def display_antibodies(window, antibodyList):
    """Fucntion that diplays the antibodies"""
    for antibody in antibodyList:
        antibody.paint(window)

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