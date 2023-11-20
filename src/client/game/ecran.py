import pygame_menu
import pygame
import threading
from pygame.locals import QUIT, USEREVENT
import time

global_pause = True
global_nom_joueur2 = ""

class Ecran:
    def __init__(self, width, height, menu_title, menu_width, menu_height, menu_theme, joueur):
        self.surface = pygame.display.set_mode((width, height))
        self.running = True
        self.menu_title = menu_title
        self.joueur = joueur
        self.menu = pygame_menu.Menu(menu_title, menu_width, menu_height, theme=menu_theme)
        self.event_queue = pygame.event.Event(USEREVENT)  # Création d'un événement personnalisé

    def set_menu_title(self, new_title):
        self.menu_title = new_title
        self.menu.set_title(new_title)

    def setup_menus_attente(self, instance_jeu):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Attente du second joueur', font_size=20, margin=(0, 20))

        name_player2=self.return_nom_joueur2()
        if name_player2 != "":
            instance_jeu.partie(0, 0, "./src/asset/Balles/jo.png")

    def setup_menus_pause(self, instance_jeu):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Le jeu est en pause', font_size=20, margin=(0, 20))

        # Ajoutez des boutons au menu
        self.menu.add.button('Reprendre le jeu',lambda:self.display_pause(instance_jeu))

        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)

    def display_pause(self,instance_jeu):
        self.joueur.send_data_game(self.joueur.username, instance_jeu.player1YFac, False)
        self.set_menu_title("Attente")
        self.setup_verification_pause(instance_jeu)
        self.run("attente pause")

    def setup_verification_pause(self,instance_jeu):
        self.menu.clear()
        pause=self.return_pause()
    
        if pause==False:
            instance_jeu.partie(instance_jeu.player1Score, instance_jeu.player2Score, "./src/asset/Balles/jo.png")

    def setup_menus_fin(self, instance_jeu,winner):
        self.menu.clear()
        # Ajoutez du contenu au menu
        self.menu.add.label('Fin du jeu', font_size=20, margin=(0, 20))
        self.menu.add.label('Le joueur {} a gagné'.format(winner), font_size=20, margin=(0, 20))
        self.menu.add.button('Recommencer une partie',lambda:self.display_fin(instance_jeu))
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)
    

    def display_fin(self,instance_jeu):
        self.joueur.send_data_game(self.joueur.username, instance_jeu.player1YFac, False)
        self.set_menu_title("Attente")
        self.setup_verification_fin(instance_jeu)
        self.run("attente fin")

    def setup_verification_fin(self,instance_jeu):
        self.menu.clear()
        pause=self.return_pause()
    
        if pause==False:
            instance_jeu.partie(0, 0, "./src/asset/Balles/jo.png")

    def run(self,current_state):
        while self.running:
            # Traitement de la file d'attente des événements personnalisés
            events=pygame.event.get()
            for event in events:
                if current_state == "attente":
                    if event.type == USEREVENT:
                        self.setup_menus_attente(event.instance_jeu)
                if current_state == "attente pause":
                    if event.type == USEREVENT:
                        self.setup_verification_pause(event.instance_jeu)
                if current_state == "attente fin":
                    if event.type == USEREVENT:
                        self.setup_verification_fin(event.instance_jeu)
                if current_state != "attente" and current_state != "attente pause" and current_state != "attente fin":
                        if event.type == pygame.QUIT:
                            self.running=False
                        
            if current_state == "attente" and current_state == "attente pause" and current_state == "attente fin":
                # Mettez à jour les menus
                self.menu.update([])
            else:
                self.menu.update(events)  # Vous pouvez ajouter des paramètres spécifiques pour la pause si nécessaire
                        
            # Dessinez les menus
            self.surface.fill((0, 0, 0))
            self.menu.draw(self.surface)

            pygame.display.flip()

    def update_nom_joueur2(self, nom_joueur2, instance_jeu):
        global global_nom_joueur2
        global_nom_joueur2= nom_joueur2        
        # Ajoutez l'événement personnalisé à la file d'attente
        pygame.event.post(self.event_queue)
        # Ajoutez l'instance_jeu comme attribut de l'événement
        self.event_queue.instance_jeu = instance_jeu
    
    def return_nom_joueur2(self):
        global global_nom_joueur2
        return global_nom_joueur2

    def update_pause(self, pause,instance_jeu):
        global global_pause
        global_pause = pause  # Mettre à jour la variable globale
        pygame.event.post(self.event_queue)
        # Ajoutez l'instance_jeu comme attribut de l'événement
        self.event_queue.instance_jeu = instance_jeu

    def return_pause(self):
        global global_pause
        return global_pause
