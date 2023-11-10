import pygame
from Const import *

# Striker class

class Striker:
		# Take the initial position, dimensions, speed and color of the object
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		# Rect that is used to control the position and collision of the object
		self.playerRect = pygame.Rect(posx, posy, width, height)
		# Object that is blit on the screen
		self.player = pygame.draw.rect(screen, self.color, self.playerRect)

	# Used to display the object on the screen
	def display(self):
		self.player = pygame.draw.rect(screen, self.color, self.playerRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Restricting the striker to be below the top surface of the screen
		if self.posy <= 0:
			self.posy = 0
		# Restricting the striker to be above the bottom surface of the screen
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# Updating the rect with the new values
		self.playerRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):

		return self.playerRect
	
	def sendStrikerToServer(self,sock):
		strikerJson=json.dumps(self.__dict__)
		sock.send(strikerJson.encode())