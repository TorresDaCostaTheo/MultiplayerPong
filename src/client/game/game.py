import pygame
import pygame_menu
import socket
from Const import *
from Striker import Striker
from Ball import Ball
from ecran import Ecran

# Initialisation de Pygame
pygame.init()

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialisation de l'horloge
clock = pygame.time.Clock()

def main():
    running = True

    # Définir les objets
    player1 = Striker(20, 0, 10, 100, 10, GREEN)
    player2 = Striker(WIDTH-30, 0, 10, 100, 10, RED)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)
    ecran = Ecran(900, 650, '', 400, 300, pygame_menu.themes.THEME_DARK)

    listOfplayers = [player1, player2]

    # Initial parameters of the players
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                if event.key == pygame.K_z:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1
                if event.key == pygame.K_ESCAPE:
                    ecran.set_menu_title('Pause')
                    ecran.setup_menus_pause()
                    ecran.run()
                    


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_z or event.key == pygame.K_s:
                    player1YFac = 0

        # Collision detection
        for player in listOfplayers:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        # Updating the objects
        player1.update(player1YFac)
        player2.update(player2YFac)
        point = ball.update()

        # -1 -> player_1 has scored
        # +1 -> player_2 has scored
        # 0 -> None of them scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset its position
        if point: 
            ball.reset()
        
        if player1Score == 10 or player2Score == 10 :
             ecran.set_menu_title('Fin')
             ecran.setup_menus_fin()
             ecran.run()
                
        # Displaying the objects on the screen
        player1.display()
        player2.display()
        ball.display()

        # Displaying the scores of the players
        player1.displayScore("player_1 : ", player1Score, 100, 20, WHITE)
        player2.displayScore("player_2 : ", player2Score, WIDTH-100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

    def partie(self, player_name):
        running = True
  
        # Initialisation des objets
        player1 = Striker(20, 0, 10, 100, 10, GREEN)
        player2 = Striker(WIDTH-30, 0, 10, 100, 10, RED)
        ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

        listOfplayers = [player1, player2]

        # Paramètres initiaux des joueurs
        player1Score, player2Score = 0, 0
        player1YFac, player2YFac = 0, 0
        
        # Créer un socket et se connecter à un serveur
	      #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	      #sock.connect(("127.0.0.1", 5555))
        
        while running:
            self.screen.fill(BLACK)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player2YFac = -1
                    if event.key == pygame.K_DOWN:
                        player2YFac = 1
                    if event.key == pygame.K_z:
                        player1YFac = -1
                    if event.key == pygame.K_s:
                        player1YFac = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2YFac = 0
                    if event.key == pygame.K_z or event.key == pygame.K_s:
                        player1YFac = 0

            # Détection des collisions
            for player in listOfplayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()
                    
                    
            player1.update(player1YFac)
            #player1.sendStrikerToServer(sock)
            player2.update(player2YFac)
            #player2.sendStrikerToServer(sock)
            point = ball.update()
            #ball.sendBallToServer(sock)

            # -1 -> player_1 a marqué
            # +1 -> player_2 a marqué
            # 0 -> Aucun d'eux n'a marqué
            if point == -1:
                player1Score += 1
            elif point == 1:
                player2Score += 1

            # Quelqu'un a marqué
            # un point et la balle est hors limites.
            # Donc, nous réinitialisons sa position
            if point:
                ball.reset()

            # Affichage des objets à l'écran
            player1.display()
            player2.display()
            ball.display()

            # Affichage des scores des joueurs
            player1.displayScore(f"{player_name} : ",
                                player1Score, 100, 20, WHITE)
            player2.displayScore("player_2 : ",
                                player2Score, WIDTH-100, 20, WHITE)

            pygame.display.update()
            self.clock.tick(FPS)

# Si vous exécutez le jeu en tant que script principal

if __name__ == "__main__":
    game_instance = Game()
    game_instance.partie("Player_1")
    pygame.quit()
