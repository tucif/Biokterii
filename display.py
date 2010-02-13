from virus import Virus
from cell import Cell


vir = Virus()

cellLst=[Cell() for i in xrange(10)]

def display(window):
    """Fucntion that diplays the whole simulation"""
    vir.paint(window)
    for cell in cellLst:
        cell.paint(window)

