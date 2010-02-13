from virus import Virus
from cell import Cell
from healthStation import HealthStation
from antibody import Antibody

vir = Virus()
cellList=[Cell() for i in xrange(10)]
stationList=[HealthStation() for i in xrange(3)]
antibodyList=[Antibody() for i in xrange(4)]

def display(window):
    """Fucntion that diplays the whole simulation"""
    vir.paint(window)
    for cell in cellList:
        cell.paint(window)
    for station in stationList:
        station.paint(window)
    for antibody in antibodyList:
        antibody.paint(window)

