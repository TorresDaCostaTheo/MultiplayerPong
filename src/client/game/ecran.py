import pygame_menu
import pygame

class Ecran:
    def __init__(self, width, height, menu_title, menu_width, menu_height, menu_theme):
        self.surface = pygame.display.set_mode((width, height))
        self.running = True
        self.menu_title=menu_title

        self.menu = pygame_menu.Menu(menu_title, menu_width, menu_height, theme=menu_theme)
    
    
    def set_menu_title(self, new_title):
        self.menu_title = new_title
        self.menu.set_title(new_title)

    def setup_menus_pause(self):
        self.menu.clear()
        # Add content to the menu
        self.menu.add.label('Le jeu est en pause', font_size=20, margin=(0, 20))
            # Add buttons to the menu
        self.menu.add.button('Reprendre')
        self.menu.add.button('Quitter le jeu', pygame_menu.events.EXIT)
    
    def setup_menus_fin(self):
        self.menu.clear()
        # Add content to the menu
        self.menu.add.label('Fin du jeu', font_size=20, margin=(0, 20))
        self.menu.add.label('Le joueur test a gagné', font_size=20, margin=(0, 20))

    def setup_menus_quit(self):
        self.menu.clear()
        self.menu.add.label('Quitter le jeu', font_size=20, margin=(0, 20))

        # Add buttons to the menu
        self.menu.add.button('Oui', self.quit_game)
        self.menu.add.button('Non', self.setup_menus_pause)


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

