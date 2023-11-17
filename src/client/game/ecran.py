import pygame_menu
import pygame

class Ecran:
    def __init__(self, width, height, menu_title, menu_width, menu_height, menu_theme,joueur):
        self.surface = pygame.display.set_mode((width, height))
        self.running = True
        self.menu_title=menu_title
        self.joueur=joueur
        self.nom_joueur2=""
        self.menu = pygame_menu.Menu(menu_title, menu_width, menu_height, theme=menu_theme)

    def set_menu_title(self, new_title):
        self.menu_title = new_title
        self.menu.set_title(new_title)


    def setup_menus_Attente(self,instance_menu,instance_jeu):
        self.menu.clear()
        # Add content to the menu
        self.menu.add.label('Attendre le second joueur', font_size=20, margin=(0, 20))
        
        if self.nom_joueur2 != "":
            instance_jeu.partie(0, 0, "./src/asset/Balles/jo.png")


    def setup_menus_pause(self,instance_jeu):
        self.menu.clear()
        # Add content to the menu
        self.menu.add.label('Le jeu est en pause', font_size=20, margin=(0, 20))
        
        # Add buttons to the menu
        self.menu.add.button('Reprendre le jeu', lambda: self.reprendre_partie(instance_jeu))
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)


    def reprendre_partie(self,instance_jeu):
        instance_jeu.pause=False
        self.joueur.send_message(self.joueur.username, instance_jeu.player1YFac,instance_jeu.pause,0,0)
        instance_jeu.partie(instance_jeu.player1Score,instance_jeu.player2Score,"./src/asset/Balles/jo.png")


    def setup_menus_fin(self,instance_jeu):
        self.menu.clear()
        # Add content to the menu
        self.menu.add.label('Fin du jeu', font_size=20, margin=(0, 20))
        self.menu.add.label('Le joueur {} a gagné'.format(instance_jeu.player1_name), font_size=20, margin=(0, 20))
        self.menu.add.button('Recommencer une partie',instance_jeu.partie,0,0,"./src/asset/Balles/jo.png")
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Update menus
            self.menu.update(events)

            # Draw menus
            self.surface.fill((0, 0, 0))
            self.menu.draw(self.surface)
        

            pygame.display.flip()


    def update_nom_joueur2(self, nom_joueur2):
        self.nom_joueur2=nom_joueur2