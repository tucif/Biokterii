import gtk

WINDOW_SIZE=700
TRAINING_ZONE_LIMIT=WINDOW_SIZE-100

TOTAL_VIRUS = 1
MAX_CELLS = 5  #Max number of cells on screen
TRAIN_CELLS=15


#imagenes
VIRUS_IMAGE=gtk.gdk.pixbuf_new_from_file("./resources/virus/virus.png")
STATION_OFF=gtk.gdk.pixbuf_new_from_file("./resources/healthStation/healthStationOff.png")
STATION_ON=gtk.gdk.PixbufAnimation("./resources/healthStation/healthStationOn.gif")
     