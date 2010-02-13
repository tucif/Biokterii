
def display_simulation(window,vir,cellList,stationList,antibodyList):
    """Fucntion that diplays the whole simulation"""
    display_virus(window,vir)
    display_cells(window,cellList)
    display_stations(window,stationList)
    display_antibodies(window,antibodyList)

def display_virus(window,virus):
    """Fucntion that diplays the virus"""
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