from game.shape.Rectangle import Rectangle
from game.shape.Point import Point


class Striker(Rectangle):
    def __init__(self,player:int) -> None:
        super().__init__()
        self.__coordY = 0
        x=0
        if player == 1:
            x = 0
        else :
            x = 170
            print(x)
        self.defineRectangle(Point(x,self.__coordY),Point(x+10,self.__coordY+50))
    def ballTouchStriker(self,point:Point):
        return self.is_inside_rectangle(point)
    @property
    def coordY(self):
        return self.__coordY
    @coordY.setter
    def coordY(self,coordY):
        self.__coordY = coordY
    def __str__(self) -> str:
        return "coordY: "+str(self.coordY)
    