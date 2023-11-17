import pygame_menu
import pygame
import threading
from pygame.locals import QUIT, USEREVENT

class Ecran:
    def __init__(self, width, height, menu_title, menu_width, menu_height, menu_theme, joueur):
        self.surface = pygame.display.set_mode((width, height))
        self.running = True
        self.menu_title = menu_title
        self.joueur = joueur
        self.nom_joueur2 = ""
        self.menu = pygame_menu.Menu(menu_title, menu_width, menu_height, theme=menu_theme)
        self.event_queue = pygame.event.Event(USEREVENT)  # Création d'un événement personnalisé

    def set_menu_title(self, new_title):
        self.menu_title = new_title
        self.menu.set_title(new_title)

    def setup_menus_Attente(self, instance_jeu):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Attendre le second joueur', font_size=20, margin=(0, 20))
        print("récupération du second joueur", self.nom_joueur2)

        if self.nom_joueur2 != "":
            instance_jeu.partie(0, 0, "./src/asset/Balles/jo.png")

    def setup_menus_pause(self, instance_jeu):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Le jeu est en pause', font_size=20, margin=(0, 20))

        # Ajoutez des boutons au menu
        self.menu.add.button('Reprendre le jeu', lambda: self.reprendre_partie(instance_jeu))
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)

    def reprendre_partie(self, instance_jeu):
        instance_jeu.pause = False
        self.joueur.send_message(self.joueur.username, instance_jeu.player1YFac, instance_jeu.pause, 0, 0)
        instance_jeu.partie(instance_jeu.player1Score, instance_jeu.player2Score, "./src/asset/Balles/jo.png")

    def setup_menus_fin(self, instance_jeu):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Fin du jeu', font_size=20, margin=(0, 20))
        self.menu.add.label('Le joueur {} a gagné'.format(instance_jeu.player1_name), font_size=20, margin=(0, 20))
        self.menu.add.button('Recommencer une partie', instance_jeu.partie, 0, 0, "./src/asset/Balles/jo.png")
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)

    def run(self):
        while self.running:
            # Traitement de la file d'attente des événements personnalisés
            for event in pygame.event.get():
                if event.type == USEREVENT:
                    self.setup_menus_Attente(event.instance_jeu)

            # Mettez à jour les menus
            self.menu.update([])

            # Dessinez les menus
            self.surface.fill((0, 0, 0))
            self.menu.draw(self.surface)

            pygame.display.flip()

    def update_nom_joueur2(self, nom_joueur2, instance_jeu):
        self.nom_joueur2 = nom_joueur2
        print("mise à jour du second joueur", self.nom_joueur2)
        
        # Ajoutez l'événement personnalisé à la file d'attente
        pygame.event.post(self.event_queue)
        # Ajoutez l'instance_jeu comme attribut de l'événement
        self.event_queue.instance_jeu = instance_jeu