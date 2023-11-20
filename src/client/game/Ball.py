import pygame
import json
from Const import *
import time

class Ball:

    def __init__(self, posx, posy, radius, speed, color, BallImagePath):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = 8
        self.color = color
        self.xFac = -1
        self.yFac = -1
        self.image = pygame.image.load(BallImagePath)
        self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))
        self.rect = self.image.get_rect(center=(self.posx, self.posy))
        self.firstTime = 1

    def display(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # Mise à jour de la position du rectangle
        self.rect.center = (self.posx, self.posy)

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            self.xFac *= -1  # Invert the direction only during the first time
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            self.xFac *= -1  # Invert the direction only during the first time
            return -1
        else:
            return 0




    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac = -1
        
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac = 1
        self.xFac = -1
        self.firstTime = 1
        self.speed = 8
        self.rect.center = (self.posx, self.posy)


    def hit(self):
        self.xFac *= -1
        self.speed *= 1.1

    def getRect(self):
        return self.rect
      	
    def sendBallToServer(self,sock):
        ballJson=json.dumps(self.__dict__)
        print(ballJson)
        sock.send(ballJson.encode())
    

    def update_ball(self,coordX,coordY,speed):
        self.posx=coordX
        self.posy=coordY
        self.speed=speed
