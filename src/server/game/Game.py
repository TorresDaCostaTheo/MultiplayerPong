
from enum import Enum
import threading
from time import sleep

from game.Player import Player
from game.Ball import Ball
from game.shape.Rectangle import HorizontalLine, Rectangle, VerticalLine
from game.shape.Point import Point

class State(Enum):
    WAITING = 1
    STARTED = 2
    ENDED = 3
    PAUSE = 4
class Game:
    _instance = None
    def __init__(self,frameSecond:int = 25) -> None:
        self.__players:list[Player] = [Player(1,"Joueur1"),Player(2,"Joueur2")]
        self.__state = State.WAITING
        self.__game_thread = threading.Thread(target=self.game,daemon=True)
        self.__frameSecond = frameSecond
    """_summary_
    """
    def start(self):
        self.__game_thread.start()
        self.__ball = Ball(Point(100,100),3)
        self.__board = GameBoard(self.__players,self.__ball,self.__frameSecond)
        self.__state = State.STARTED
        self.__board.moveBall()
        print("Game started")
        pass
    def waiting(self):
        #Function to send waiting message to players
        #Callback for when a player trigger serverThread
        print("Waiting for players...")
        """Stop the game 
        """
    def pause(self):
        
        pass
    
    def game(self):
        pass
    """
    Method kick the player of the match and display winner players
    """
    def end(self)->bool:
        return True
        pass
    def join(self):
        self.__players.append(Player())
        pass
    def quit(self,player:Player):
        self.__players.remove(player)
        pass
    def sendBallCoord(self,coordX,coordY):
        self.__ball.coordX = coordX
        self.__ball.coordY = coordY
        pass
    
    @property
    def players(self):  
        return self.__players
    @property
    def frameSecond(self):
        return self.__frameSecond
    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class GameBoard():
    """Board of the game
    """
    def __init__(self,players:list[Player],ball:Ball,frameSecond:int) -> None:
        self.__players = players
        self.__ball = ball
        self.__board = Rectangle(Point(0,0),Point(200,200))
        self.__frameSecond = frameSecond
        self.__switchDirection = False
        self.__switchLatitude = True
        pass
        """
        __comments__ Method to move ball in board and check collision with board and striker
        """    
    def moveBall(self):
        slope = 1
         
        while True:
            print(self.__ball.__str__())
            self.__ball.coordY = slope*self.__ball.coordX +0
            if(self.__board.isOnRectangle(Point(self.__ball.coordX,self.__ball.coordY))):
               #  print("Ball is on board")
               pass
            else:
                # ball touch top border y = max
                if(self.__board.touchHorizontal(Point(self.__ball.coordX,self.__ball.coordY)) == HorizontalLine.TOP):
                #    print("Ball is on top")
                    self.__switchLatitude = True
                # ball touch bottom border y = 0
                elif(self.__board.touchHorizontal(Point(self.__ball.coordX,self.__ball.coordY)) == HorizontalLine.BOTTOM):
                 #   print("Ball is on bottom")
                    self.__switchLatitude = False
                # ball touch left border x = 0
                if(self.__board.touchVertical(Point(self.__ball.coordX,self.__ball.coordY)) == VerticalLine.LEFT):
                 #   print("Ball is on left")
                    self.__switchDirection = False
                #ball touch right border x = max
                elif(self.__board.touchVertical(Point(self.__ball.coordX,self.__ball.coordY)) == VerticalLine.RIGHT):
                    self.__switchDirection = True
               #     print("Ball is on right")
            self.__isTouchStriker()
            if self.__switchDirection:
                self.__ball.coordX += self.__ball.speed
            else:
                self.__ball.coordX-= self.__ball.speed
            if self.__switchLatitude:
                slope = 1
            else:
                slope = -1
            sleep(1/self.__frameSecond)
    def __isTouchStriker(self):
        if(self.__players.__len__()==2):
            for player in self.__players:
                if  player.striker.ballTouchStriker(self.__ball.point) :
                    print("Ball is on striker"+ player.__str__())
                    print("Switch direction "+str(self.__switchDirection))
                    self.__switchDirection = not self.__switchDirection
                    print(self.__switchDirection)
                    self.__ball.speedUp(1.1)
                continue
            return True