from game.Striker import Striker

"""
 Player class is a class that represents a player in the game.
"""
class Player:
    """
    Constructor of the Player class.
    """
    def __init__(self,posX:int,name:str) -> None:
        self.__striker = Striker(posX)
        self.__name = name
        pass
    def sendData():
        pass
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self._name = name
    @property
    def striker(self):
        return self.__striker
    @striker.setter
    def striker(self,striker):
        self.__striker = striker
    def __str__(self):
        return "name: "+str(self.name)+" striker: "+str(self.striker.perimeter)