import pygame
import pygame_menu
from Const import *
from Striker import Striker
from Ball import Ball
from ecran import Ecran


class Game:
    def __init__(self, joueur):
        pygame.init()
        self.joueur = joueur
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.player1_name = joueur.username
        self.player2_name = ""
        self.send_message_interval = 0.1  # Envoyer un message toutes les 0.5 secondes
        self.last_send_time = pygame.time.get_ticks()
        self.pause=False

    def partie(self, player1Score, player2Score, BallImage):
        running = True
        player1 = Striker(20, 0, 40, 100, 10, GREEN, StrikerGaucheImagePath, self.joueur)
        player2 = Striker(WIDTH-50, 0, 40, 100, 10, RED, StrikerDroitImagePath, self.joueur)
        ball = Ball(WIDTH//2, HEIGHT//2, 50, 60, WHITE, BallImage)
        ecran = Ecran(WIDTH, HEIGHT, '', 400, 300, pygame_menu.themes.THEME_DARK,self.joueur)

        listOfplayers = [player1, player2]

        self.player1YFac, self.player2YFac = 0, 0
        self.player1Score = player1Score
        self.player2Score = player2Score
        

        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player2YFac = -1
                    if event.key == pygame.K_DOWN:
                        self.player2YFac = 1
                    if event.key == pygame.K_z:
                        self.player1YFac = -1
                    if event.key == pygame.K_s:
                        self.player1YFac = 1
                    if event.key == pygame.K_ESCAPE:
                        self.pause=True
                        self.joueur.send_data_game(self.joueur.username, self.player1YFac,self.pause)
                        ecran.set_menu_title('Pause')
                        ecran.setup_menus_pause(self)
                        ecran.run("pause")
                    
                
                if self.pause==True:
                        self.joueur.send_data_game(self.joueur.username, self.player1YFac,self.pause)
                        ecran.set_menu_title('Pause')
                        ecran.setup_menus_pause(self)
                        ecran.run("pause")

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player2YFac = 0
                    if event.key == pygame.K_z or event.key == pygame.K_s:
                        self.player1YFac = 0

            for player in listOfplayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()

            player1.update(self.player1YFac)
            player2.update(self.player2YFac)
            point = ball.update()

            if point == -1:
                self.player1Score += 1
            elif point == 1:
                self.player2Score += 1
            if point:
                ball.reset()

            player1.display()
            player2.display()
            ball.display()

            player1.displayScore(f"{self.player1_name} : ", self.player1Score, 100, 20, WHITE)
            player2.displayScore(f"{self.player2_name} : ", self.player2Score, WIDTH-100, 20, WHITE)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_send_time > self.send_message_interval * 1000:
                self.joueur.send_data_game(self.joueur.username,self.player1YFac,self.pause)
                self.last_send_time = current_time

            if self.player1Score == 10:
                self.pause=True
                self.joueur.send_data_game(self.joueur.username, self.player1YFac,self.pause)
                ecran.set_menu_title('Fin')
                ecran.setup_menus_fin(self,self.player1_name)
                ecran.run("fin")
            elif self.player2Score ==10:
                self.pause=True
                self.joueur.send_data_game(self.joueur.username, self.player1YFac,self.pause)
                ecran.set_menu_title('Fin')
                ecran.setup_menus_fin(self,self.player2_name)
                ecran.run("fin")

                
            pygame.display.update()
            self.clock.tick(FPS)

    def update_player_name2(self, player2_name):
        if self.player2_name == "":
            self.player2_name = player2_name

    def update_player_fac2(self, player2YFac):
        self.player2YFac = player2YFac

    def update_pause(self, pause):
        self.pause=pause