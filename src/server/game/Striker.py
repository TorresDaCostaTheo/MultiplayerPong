from game.shape.Rectangle import Rectangle
from game.shape.Point import Point


class Striker(Rectangle):
    def __init__(self,player:int) -> None:
        super().__init__()
        x=0
        if player == 1:
            x = 0
        else :
            x = 170
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
    