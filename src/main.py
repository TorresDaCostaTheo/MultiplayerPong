import pygame
from Const import *
from Striker import Striker
from Ball import Ball


# Game Manager

def main():
	running = True

	# Defining the objects
	player1 = Striker(20, 0, 10, 100, 10, GREEN)
	player2 = Striker(WIDTH-30, 0, 10, 100, 10, RED)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

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
		# So, we reset it's position
		if point: 
			ball.reset()

		# Displaying the objects on the screen
		player1.display()
		player2.display()
		ball.display()

		# Displaying the scores of the players
		player1.displayScore("player_1 : ", 
						player1Score, 100, 20, WHITE)
		player2.displayScore("player_2 : ", 
						player2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)	 


if __name__ == "__main__":
	main()
	pygame.quit()
