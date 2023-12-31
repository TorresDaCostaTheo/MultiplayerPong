import pygame
pygame.init()
# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

StrikerDroitImagePath = "./src/asset/Strikers/mainDroite.png"
StrikerGaucheImagePath = "./src/asset/Strikers/mainGauche.png"
clock = pygame.time.Clock() 
FPS = 60

pygame_icon = pygame.image.load('./src/asset/InstaPongLogo.png')
pygame.display.set_icon(pygame_icon)
