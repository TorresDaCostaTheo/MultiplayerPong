import pygame_menu
import json
from Const import *
from ClientSocket import ClientSocket
from game import Game
from ecran import Ecran

class MainMenu:
    def __init__(self):
        self.PlayerNameInput = ""
        self.BallImagePath = "./src/asset/Balles/jo.png"
        self.ServerInput = ""
        self.PortInput = 0
        self.joueur = None
        self.game=None
        self.nom_joueur1 = ""
        self.nom_joueur2=""

        self.menu = pygame_menu.Menu('Pong', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.selector('Choisissez votre balle :', [('Joan', 1), ('Mounira', 2)], onchange=self.set_ball)
        self.menu.add.text_input('Nom :', default='', onchange=self.NameValue)
        self.menu.add.text_input('Serveur :', default='', onchange=self.ServerValue)
        self.menu.add.text_input('Port :', default='', onchange=self.PortValue)

        self.menu.add.button('Jouer', self.start_the_game)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)

    def connectJoueur(self, username, server, port):
        self.joueur = ClientSocket(username, server, int(port), self.callBack)
        self.joueur.connect()

    def callBack(self, message):
        print(message)
        try:
            data = json.loads(message)

            if 'Joueurs' in data:
                joueurs = data['Joueurs']

                for joueur in joueurs:
                    self.nom_joueur1 = joueur.get("nomJoueur1", "")
                    self.nom_joueur2 = joueur.get("nomJoueur2", "")                        

                    score_joueur1_str = joueur.get("score1", "")
                    score_joueur2_str = joueur.get("score2", "")

                    score_joueur1 = int(score_joueur1_str) if score_joueur1_str else 0
                    score_joueur2 = int(score_joueur2_str) if score_joueur2_str else 0        

                    player1YFac_str = joueur.get("player1YFac", "")
                    player2YFac_str = joueur.get("player2YFac", "")

                    player1YFac = int(player1YFac_str) if player1YFac_str else 0
                    player2YFac = int(player2YFac_str) if player2YFac_str else 0

                    if self.game:
                        self.game.update_player_names(self.nom_joueur1, self.nom_joueur2)
                        self.game.update_player_fac(player1YFac, player2YFac)
                        self.game.update_player_score(score_joueur1, score_joueur2)

        except json.JSONDecodeError as e:
            print("Erreur lors du décodage du message JSON:", e)

    def start_the_game(self):
        self.connectJoueur(self.PlayerNameInput, self.ServerInput, self.PortInput)
        self.joueur.send_message("", 0, 0, self.joueur.username, 0, 0)

        #if self.nom_joueur1 != "" and self.nom_joueur2 != "":  # Vérifier s'il y a deux joueurs pour commencer le jeu
        self.game = Game(self.joueur)
        self.game.partie(0, 0, self.BallImagePath)
        #else:
            #ecran = Ecran(screen.get_width(), screen.get_height(), '', 400, 300, pygame_menu.themes.THEME_DARK)
            #ecran.set_menu_title('Attente')
            #ecran.setup_menus_Attente()
            #ecran.run()

    def NameValue(self, name):
        self.PlayerNameInput = name

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
