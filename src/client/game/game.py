import pygame
import pygame_menu
from Const import *
from Striker import Striker
from Ball import Ball
from ecran import Ecran

pygame.init()

class Game:
    def __init__(self, joueur):
        pygame.init()
        self.joueur = joueur
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.rotate_ball = False

    def partie(self, player_name, BallImage):
        running = True

        player1 = Striker(20, 0, 40, 100, 10, GREEN, StrikerGaucheImagePath)
        player2 = Striker(WIDTH-50, 0, 40, 100, 10, RED, StrikerDroitImagePath)
        ball = Ball(WIDTH//2, HEIGHT//2, 50, 60, WHITE, BallImage)
        ecran = Ecran(900, 600, '', 400, 300, pygame_menu.themes.THEME_DARK)

        listOfplayers = [player1, player2]

        player1Score, player2Score = 0, 0
        player1YFac, player2YFac = 0, 0

        while running:
            self.screen.fill(BLACK)

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
                    if event.key == pygame.K_c:
                        self.rotate_ball = True
                    if event.key == pygame.K_v:
                        self.rotate_ball = False
                        
                    if event.key == pygame.K_ESCAPE:
                        ecran.set_menu_title('Pause')
                        ecran.setup_menus_pause(self)
                        ecran.run()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2YFac = 0
                    if event.key == pygame.K_z or event.key == pygame.K_s:
                        player1YFac = 0

            for player in listOfplayers:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()

            player1.update(player1YFac)
            player2.update(player2YFac)
            point = ball.update()

            if point == -1:
                player1Score += 1
                # self.joueur.send_message(self.joueur.username, player1Score)
            elif point == 1:
                player2Score += 1
                # self.joueur.send_message(self.joueur.username, player2Score)

            if player1Score == 10 or player2Score == 10:
                ecran.set_menu_title('Fin')
                ecran.setup_menus_fin(self)
                ecran.run()

            if point:
                ball.reset()

            player1.display()
            player2.display()
            ball.display()
            
            if self.rotate_ball:
                ball.rotate()

            player1.displayScore(f"{player_name} : ",
                                player1Score, 100, 20, WHITE)
            player2.displayScore("player_2 : ",
                                player2Score, WIDTH-100, 20, WHITE)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game_instance = Game("joueur")
    game_instance.partie("Player_1", "./src/asset/Balles/jo.png")
    pygame.quit()

