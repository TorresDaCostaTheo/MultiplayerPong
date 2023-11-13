class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        self.__y = y
    def __str__(self):
        return "x: "+str(self.x)+" y: "+str(self.y)