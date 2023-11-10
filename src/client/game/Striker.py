import pygame
from Const import *

class Striker:
    def __init__(self, posx, posy, width, height, speed, color, image_path):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.playerRect = self.image.get_rect(topleft=(self.posx, self.posy))

    def display(self):
        screen.blit(self.image, self.playerRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.playerRect.topleft = (self.posx, self.posy)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.playerRect
