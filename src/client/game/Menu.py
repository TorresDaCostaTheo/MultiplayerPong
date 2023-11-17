import pygame_menu
import json
from Const import *
from ClientSocket import ClientSocket
from game import Game
from ecran import Ecran

class MainMenu:
    def __init__(self):
        self.playerInput=""
        self.nom_joueur2=""
        self.BallImagePath = "./src/asset/Balles/jo.png"
        self.ServerInput = ""
        self.PortInput = 0
        self.joueur = None
        self.game=None
        self.ball_position = None

        self.menu = pygame_menu.Menu('Pong', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.selector('Choisissez votre balle :', [('Joan', 1), ('Mounira', 2)], onchange=self.set_ball)
        self.menu.add.text_input('Nom :', default='', onchange=self.NameValue)
        self.menu.add.text_input('Serveur :', default='', onchange=self.ServerValue)
        self.menu.add.text_input('Port :', default='', onchange=self.PortValue)

        self.menu.add.button('Jouer', self.start_the_game)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)

        ecran = Ecran(WIDTH, HEIGHT, '', 400, 300, pygame_menu.themes.THEME_DARK,self.joueur)

    def connectJoueur(self, username, server, port):
        self.joueur = ClientSocket(username, server, int(port), self.callBack)
        self.joueur.connect()

    def callBack(self, message):
        print(message)
        try:
            data = json.loads(message)

            if 'player' in data:
                joueurs = data['Player']
                for joueur in joueurs:
                    temp=joueur.get("namePlayer", "")
                    if self.playerInput!= temp:
                        self.nom_joueur2 = joueur.get("namePlayer", "")
                        
                    if self.game:
                        if self.playerInput!=self.nom_joueur2:
                            self.nom_joueur2 = joueur.get("namePlayer", "")                            
                            playerYFac_str = joueur.get("playerYFac", "")
                            pause = joueur.get("pause", "")
                                                 
                            playerYFac = int(playerYFac_str) if playerYFac_str else 0

                            self.game.update_player_name2(self.nom_joueur2)
                            self.game.update_player_fac2(playerYFac)
                            self.game.update_pause(pause)

        except json.JSONDecodeError as e:
            print("Erreur lors du décodage du message JSON:", e)

    def start_the_game(self):
        self.connectJoueur(self.playerInput, self.ServerInput, self.PortInput)

        self.joueur.send_message(self.joueur.username, 0,False,0,0)
        self.game = Game(self.joueur)
    

        # self.joueur.send_message(self.joueur.username, 0,False)
        self.game = Game(self.joueur)
        ecran = Ecran(WIDTH, HEIGHT, '', 400, 300, pygame_menu.themes.THEME_DARK,self.joueur)
        self.joueur.sendMessage(self.joueur.username, 0)
        self.game.partie(0, 0, self.BallImagePath)

    def NameValue(self, name):
        self.playerInput = name

    def ServerValue(self, server):
        self.ServerInput = server

    def PortValue(self, port):
        self.PortInput = port

    def set_ball(self, name, value):
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
    pygame.quit()
