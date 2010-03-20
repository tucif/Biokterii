import random;

class Environment:
    def __init__(self):
        self.posX=0;
        self.posY=0;
        self.width=0;
        self.height=0;

        #properties
        self.temp= random.randint(0,100)    #0~100
        self.ph=random.randint(0,14)       #0~14
        self.reactivity=random.randint(0,100) #0~100
        self.radar=random.randint(0,100)    #0~100