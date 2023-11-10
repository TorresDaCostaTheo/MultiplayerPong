import pygame_menu
from game import Game
from Const import *

class MainMenu:
    def __init__(self):
        self.PlayerNameInput = ""
        self.menu = pygame_menu.Menu('Pong', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.text_input('Name :', default='', onchange=self.NameValue)
        self.menu.add.text_input('Server :', default='', onchange=self.ServerValue)
        self.menu.add.text_input('Port :', default='', onchange=self.PortValue)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def start_the_game(self):
        game = Game()
        game.partie(self.PlayerNameInput)

    def NameValue(self, name):
        self.PlayerNameInput = name
        print("Nom joueur 1: ", self.PlayerNameInput)
    
    def ServerValue(self, server):
        self.ServerInput = server
        print("Server: ", self.ServerInput)

    def PortValue(self, port):
        self.PortInput = port
        print("Port: ", self.PortInput)

    def run_menu(self):
        self.menu.mainloop(screen)

# Si vous exécutez le menu en tant que script principal
if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run_menu()
