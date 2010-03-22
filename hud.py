from sprite import Sprite

ID_PADDING=[0,-5]

class Hud():
    def __init__(self):
        self.allVisible=True
        self.idVisible=True
        self.boundingBoxVisible=True
        self.window=None

    def display_viruses(self,window,objectList):

        if self.allVisible:
            if self.idVisible:
                for object in objectList:
                    if isinstance(object,Sprite):
                        text=str(object)
                        posXText=object.posX+object.width/2-(len(text)/2)*5
                        posYText=object.posY+ID_PADDING[1]
                        window.move_to(posXText,posYText)
                        window.set_source_rgba(1,1,1,0.7)
                        window.show_text(text)

    def display_environment(self,window,environmentList):
        for environment in environmentList:
            posXText=environment.posX+5
            posYText=environment.posY+20
            text="Environment properties: temp:%d | ph:%d | reactivity: %d | radars: %d" % (environment.temp,environment.ph,environment.reactivity,environment.radar)

            window.move_to(posXText,posYText)
            window.set_source_rgba(1,1,1,0.7)
            window.show_text(text)

            