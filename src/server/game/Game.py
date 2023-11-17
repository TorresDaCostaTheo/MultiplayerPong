
from calendar import c
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
class Game(threading.Thread):
    _instance = None
    def __init__(self,server,callback,frameSecond:int = 60) -> None: # type: ignore
        super().__init__(target=self.game)
        self.__frameSecond = frameSecond
        self.__players:list[Player] = []
        self.__lock = threading.Lock()
        # self.__players:list[Player] = [Player(1,"Joueur1",None),Player(2,"Joueur2",None)]
        self.__state = State.WAITING
        self.__server = server
        self.__callback = callback
        print(self.__state)       
        
        """_summary_ Method to start the game
        """
    def starting(self):
        self.__ball = Ball(Point(100,100),3)
        self.__board = GameBoard(self.__players,self.__ball,self.__frameSecond)
        #resize location of strikers
        dimension =  round(self.__board.board.point1.x * 0.8)
        for player in self.__players:
            player.striker.defineRectangle(Point(0+dimension,10),Point(0+dimension+10,60))
        self.__state = State.STARTED
        print("Game started")
    
    def waiting(self):
        #Function to send waiting message to players
        #Callback for when a player trigger serverThread
        if self.__players.__len__() == 2:
            self.starting()
    def pause(self):
        
        pass
    def startGame(self):
        for player in self.__players:
            if(player.score == 2):
                self.__state = State.ENDED
                return player
        return None

    def game(self):
        print("Game loop")
        playerWinner:Player|None = None
        while True:
            if self.__players.__len__() > 2:
                self.__state = State.PAUSE
                break
            elif self.__players.__len__() <= 0 and self.__state == State.STARTED:
                self.__state = State.ENDED
            if self.__state == State.WAITING:
                self.waiting()
            if self.__state == State.ENDED:
                self.end("win",self.__players[1])
                break
            if self.__state == State.STARTED:
                self.startGame()
                self.__board.moveBall()
                self.__callback()
            if self.__state == State.PAUSE:
                pass
            sleep(1/self.__frameSecond)

    """
    Method kick the player of the match and display winner players
    Supprimer print pour avoir callback à la place
    """
    def end(self,reason:str,player:Player)->bool:
        if(reason == "kick"):
            pass
        elif(reason == "win"):
            print(player.name+" win the game")
        return True
    def joinPlayer(self,player:Player):
        print("Joining player "+player.__str__())
        with self.__lock:
            if self.__players.__len__() >= 2:
                return False
            else:
                self.__players.append(player)
                return True
    def quit(self,id:int):
        with self.__lock:
            player_with_id = next((player for player in self.__players if player.id == id),None)
            if player_with_id is not None:
                self.__players.remove(player_with_id)
                return True
            else:
                return False
    
    @property
    def players(self):  
        return self.__players
    @property
    def frameSecond(self):
        return self.__frameSecond
    @classmethod
    def getInstance(cls,server,callback): # type: ignore
        if cls._instance is None:
            cls._instance = cls(server=server,callback=callback) # type: ignore
        return cls._instance
    @property
    def thread(self):
        return super()
    @property
    def state(self):
        return self.__state

class GameBoard():
    """Board of the game
    """
    def __init__(self,players:list[Player],ball:Ball,frameSecond:int) -> None:
        self.__players = players
        self.__ball = ball
        self.__board = Rectangle(Point(0,0),Point(600,900))
        self.__frameSecond = frameSecond
        self.__switchDirection = False
        self.__switchLatitude = True
        pass
        """
        __comments__ Method to move ball in board and check collision with board and striker
        """    
    def moveBall(self):
        slope = 1
        self.__ball.coordY = slope*self.__ball.coordX +0
        if(self.__board.isOnRectangle(Point(self.__ball.coordX,self.__ball.coordY))):
            # print("Ball is on board")
            pass
        else:
            self.__isTouchBoard()
        self.__isTouchStriker()
        if self.__switchDirection:
            self.__ball.coordX += self.__ball.speed
        else:
            self.__ball.coordX-= self.__ball.speed
        if self.__switchLatitude:
            slope = 1
        else:
            slope = -1
        
    
    
    def __isTouchBoard(self):
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
                print("Score player 2")
                self.__players[1].score += 1
                self.__switchDirection = not self.__switchDirection
                self.__ball.reset()
            #ball touch right border x = max
            elif(self.__board.touchVertical(Point(self.__ball.coordX,self.__ball.coordY)) == VerticalLine.RIGHT):
                print("Score player 1")
                self.__players[0].score += 1
                self.__switchDirection = not self.__switchDirection
                self.__ball.reset()        
        
    def __isTouchStriker(self):
        if(self.__players.__len__()==2):
            for player in self.__players:
                if  player.striker.ballTouchStriker(self.__ball.point) :
                    print("Ball is on striker"+ player.__str__())
                    print("Switch direction "+str(self.__switchDirection))
                    self.__switchDirection = not self.__switchDirection
                    print(self.__switchDirection)
                    self.__ball.speedUp(1.1)
                    
            return True
    @property
    def board(self):
        return self.__board