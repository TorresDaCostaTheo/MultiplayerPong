from enum import Enum
from game.shape.Point import Point

class VerticalLine(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = -1
class HorizontalLine(Enum):
    TOP = 0
    BOTTOM = 1
    NONE = -1

class Rectangle:
    def __init__(self,point1:Point=None,point2:Point=None):
        if point1 is not None and point2 is not None:
            self.__point1 = point1
            self.__point2 = point2
            self.__perimeter = self.__getPerimeter()
    
    def isOnRectangle(self,point:Point)->bool:
        return (
            point.x >= self.__point1.x and
            point.x <= self.__point2.x and
            point.y >= self.__point1.y and
            point.y <= self.__point2.y
        )
    def isOutRectangle(self,point:Point)->bool:
        return(
            point.x < self.__point1.x and
            point.x > self.__point2.x and
            point.y < self.__point1.y and
            point.y > self.__point2.y 
        )
    def defineRectangle(self,point1:Point,point2:Point):
        self.__point1 = point1
        self.__point2 = point2
        self.__perimeter = self.__getPerimeter()
    def move(self,y:int):
        self.__point1.y += y
        self.__point2.y += y
    def is_inside_rectangle(self,point:Point):
        return self.__point1.x <= point.x <= self.__point2.x and self.__point1.y <= point.y <= self.__point2.y
    def touchVertical(self,point:Point):
        if point.x >= self.__point1.x:
            return VerticalLine.LEFT
        elif point.x <= self.__point2.x:
            return VerticalLine.RIGHT
        else:
            return VerticalLine.NONE
    def touchHorizontal(self,point:Point):
        if point.y >= self.__point1.y:
            return HorizontalLine.TOP
        elif point.y <= self.__point2.y:
            return HorizontalLine.BOTTOM
        else:
            return HorizontalLine.NONE
        
    def __getPerimeter(self):
        return (self.width +self.length) * 2
    @property
    def length(self):
        return abs(self.__point1.y - self.__point2.y)
    @property
    def width(self):
        return abs(self.__point1.x - self.__point2.x)
    @property
    def perimeter(self):
        return self.__perimeter
    @property
    def point1(self):
        return self.__point1
    @point1.setter
    def point1(self,point1):
        self.__point1 = point1
    @property
    def point2(self):
        return self.__point2
    @point2.setter
    def point2(self,point2):
        self.__point2 = point2
    def __str__(self):
        return "point1: "+str(self.point1)+" point2: "+str(self.point2)
    
    