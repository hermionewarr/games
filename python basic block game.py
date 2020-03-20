#libraries
import pygame
import sys
import random
import time

pygame.init()

#variables
#size
width = 800
height = 600
player_size = 50
player_position = [width/2, height - 2*player_size]
enemy_size = 50
enemy_pos = [random.randint(0,width - enemy_size), 0]
enemy_list = [enemy_pos]

#colours
red = (255,0,0)
blue = (0,0,255)
yellow = (255, 255, 0)
Background_colour = (0,0,0)

speed = 0
num_of_enemies = 0

#display the game window
screen = pygame.display.set_mode((width,height))
game_over = False
score = 0
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("monospace", 35)

#functions
def set_level(score, speed, num_of_enemies):
	speed = score/5 + 5
	num_of_enemies = score/ 5 + 6
	return speed
	return num_of_enemies

def drop_enemies(enemy_list, num_of_enemies):
	delay = random.random()
	if num_of_enemies < 20:
		x = 0.06
	else:
		x=0.2
	if len(enemy_list) < num_of_enemies and delay < x:
		x_pos = random.randint(0, width - enemy_size)
		y_pos = 0
		enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	#make enemy block fall updating emeny position
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < height:
			enemy_pos[1] += speed
		else:
			enemy_list.pop(idx)
			score += 1
	return score		

def collision_check(enemy_list, player_position, score):
	for enemy_pos in enemy_list:
		if detect_collision(player_position, enemy_pos):
			
			return True
	return False		

#function to detect collisions
def detect_collision(player_position, enemy_pos):
	p_x = player_position[0]
	p_y = player_position[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False

#game loop
while not game_over:
	#registers you interating with the screen on the screen
	for event in pygame.event.get():
		#allows you to quit the screen
		if event.type == pygame.QUIT:
			sys.exit()
		#move the block	
		if event.type == pygame.KEYDOWN:

			x = player_position[0]
			y = player_position[1]

			if event.key == pygame.K_LEFT:
				#move box left by the size of box
				x -= player_size
			elif event.key == pygame.K_RIGHT:
				x += player_size
			player_position = [x,y]

	#make the screen black again once the block has moved
	screen.fill(Background_colour)

	#drop the enemies and inscrease the difficulty
	drop_enemies(enemy_list, num_of_enemies)
	score = update_enemy_positions(enemy_list, score)
	speed = set_level (score, speed, num_of_enemies)
	num_of_enemies = set_level(score, speed, num_of_enemies)

	#display score
	text = "Score" + str(score)
	label = myFont.render(text, 1, yellow)
	screen.blit(label, (width - 200, height - 40))

	#end the game condition
	if collision_check(enemy_list, player_position, score):
		#display score
		text = "Final Score: " + str(score)
		label = myFont.render(text, 1, yellow)
		screen.blit(label, (width/3, height/2))
		game_over = True
		#break

	#display the squares
	draw_enemies(enemy_list)
	pygame.draw.rect(screen, red, (player_position[0], player_position[1], player_size, player_size))
	
	clock.tick(30)
	pygame.display.update()
#display final score for 3 secs
pygame.time.delay(3000)
