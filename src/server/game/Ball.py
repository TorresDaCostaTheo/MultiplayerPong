from game.shape.Point import Point


class Ball:
    """
    _summary_ Ball class is a class that represents a ball in the game.
    """
    def __init__(self,point:Point,speed) -> None:
        self.__point = point
        self.__defaultSpeed:float = speed
        self.__defaultPoint = point
        self._speed:float = speed
        pass
    def speedUp(self,multiplier):
        if(multiplier < 1):         
           self._speed= self._speed * multiplier
    def reset(self):
        self.__point = self.__defaultPoint
        self._speed = self.__defaultSpeed
    def speedReset(self):
        self._speed = self.__defaultSpeed
    @property
    def coordX(self):
        return self.__point.x
    @coordX.setter
    def coordX(self,coordX:int):
        self.__point.x = coordX
    @property
    def coordY(self):
        return self.__point.y
    @coordY.setter
    def coordY(self,coordY:int):
        self.__point.y = coordY
    @property
    def speed(self):
        return self._speed
    @speed.setter
    def speed(self,speed):
        self._speed = speed
    @property
    def point(self):
        return self.__point
    def __str__(self):
        return f'{{"ball":{{"coordX":{self.point.x},"coordY":{self.point.y},"speed":{self.speed}}}}}'