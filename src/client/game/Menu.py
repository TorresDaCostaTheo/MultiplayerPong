import pygame_menu
from game import Game
from Const import *
from ClientSocket import ClientSocket
import json

class MainMenu:
    def __init__(self):
        self.PlayerNameInput = ""
        self.BallImagePath = "./src/asset/Balles/jo.png"
        self.ServerInput= ""
        self.PortInput=0
        self.joueur = None

        
        self.menu = pygame_menu.Menu('Pong', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.selector('Choisissez votre balle :', [('Joan', 1), ('Mounira', 2)], onchange=self.set_ball)
        self.menu.add.text_input('Name :', default='', onchange=self.NameValue)
        self.menu.add.text_input('Server :', default='', onchange=self.ServerValue)
        self.menu.add.text_input('Port :', default='', onchange=self.PortValue)
        

        self.menu.add.button('Jouer', self.start_the_game)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)
    

    def connectJoueur(self, username, server, port):
        self.joueur = ClientSocket(username, server, int(port), self.callBackMessage)
        self.joueur.connect()


    def add_values_to_json(self, data):
        with open('data.json', 'a') as json_file:
            print(data)
            json.dump(data, json_file)
            json_file.write('\n')  # Ajoute une nouvelle ligne pour séparer les entrées

    def callBackMessage(self, message):
        # Ajoutez les valeurs au fichier JSON au lieu d'utiliser print
        data = {"message": message}
        self.add_values_to_json(data)

    def start_the_game(self):
        self.connectJoueur(self.PlayerNameInput, self.ServerInput, self.PortInput)
        game = Game(self.joueur)
        game.partie(self.joueur.username, self.BallImagePath)

    def NameValue(self, name):
        self.PlayerNameInput = name
    
    def ServerValue(self, server):
        self.ServerInput = server

    def PortValue(self, port):
        self.PortInput = port

    def set_ball(self, name, value):
        print(value)
        if value == 1:
            self.BallImagePath = "./src/asset/Balles/jo.png"
        if value == 2:
            self.BallImagePath = "./src/asset/Balles/mounira.png"

    def run_menu(self):
        self.menu.mainloop(screen)

# Si vous exécutez le menu en tant que script principal
if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.run_menu()

