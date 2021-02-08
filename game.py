import pygame
import random
import sys

pygame.init()
# width and height of the window in where the game is displayed not adjustable
WIDTH = 800
HEIGHT = 600
# background colors of the window in where the game is displayed
RED = (255,0,0) 
BLUE = (0,0,255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)
# Player spawn size and spawn position
player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, SPEED):# Sets the speed of the obstacles/enemies
	if score < 20:
		SPEED = 5
	elif score < 40:
		SPEED = 8
	elif score < 60:
		SPEED = 12
	else:
		SPEED = 15
	return SPEED
	# SPEED = score/5 + 1


def drop_enemies(enemy_list): # Spawns the enemies into the game
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list): # Makes the enemies before spawning them into the game
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score): # Updates the position of the enemies in the game
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos): #Checks if a collision is made with a red block/object
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos): #Detects if a collision is made with a red block/object
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False

while not game_over: # Whileloop to continue the game if the variable game_over is false

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN: #What to do when the down arrow key is pressed while playing the game

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:# What to do when the left arrow key is pressed while playing the game
				x -= player_size
			elif event.key == pygame.K_RIGHT:# What to do when the right arrow key is pressed while playing the game 
				x += player_size

			player_pos = [x,y]

	screen.fill(BACKGROUND_COLOR)

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score) 
	SPEED = set_level(score, SPEED)

	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	if collision_check(enemy_list, player_pos):
		game_over = True

		print("Your score was:  ", score) # Prints out the score if the game is finished
		
		break

	draw_enemies(enemy_list)

	pygame.draw.rect(screen, YELLOW, (player_pos[0], player_pos[1], player_size, player_size))

	clock.tick(30)

	
	pygame.display.update()