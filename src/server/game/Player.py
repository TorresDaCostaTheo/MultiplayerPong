from game.Striker import Striker

"""
 Player class is a class that represents a player in the game.
"""
class Player:
    """
    Constructor of the Player class.
    """
    def __init__(self,id:int,name:str) -> None:
        self.__striker = Striker(id)
        self.__name = name
        self.__score = 0
        pass
    def sendData():
        pass
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self,score):
        self.__score = score
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
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,id):
        self.__id = id
    def __str__(self):
        return "name: "+str(self.name)+" striker: "+str(self.striker.perimeter)