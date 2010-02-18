from sprite import Sprite

ID_PADDING=[0,-5]

class Hud():
    def __init__(self):
        self.allVisible=True
        self.idVisible=True
        self.boundingBoxVisible=True
        self.window=None;

    def display(self,window,objectList):

        if self.allVisible:
            if self.idVisible:
                for object in objectList:
                    if isinstance(object,Sprite):
                        text=str(object)+str(objectList.index(object))
                        posXText=object.posX+object.width/2-(len(text)/2)*5
                        posYText=object.posY+ID_PADDING[1]
                        window.move_to(posXText,posYText)
                        window.set_source_rgba(1,1,1,0.7)
                        window.show_text(text)