from sprite import Sprite
from virus import Virus

DISPLAY_IDS=True

def display_simulation(window,virusList):
    """Fucntion that diplays the whole simulation"""
    display_virus(window,virusList)

def display_environment(window,environment):
    pass

def display_virus(window,virusList):
    """Fucntion that diplays the virus"""
    for virus in virusList:
        virus.paint(window)
