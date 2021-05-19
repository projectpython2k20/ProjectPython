import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
import os
import random
import time




pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Εξεταστική on the run')


#define font
font = pygame.font.Font('./fonts/BAUHS93.TTF', 70)
font_score = pygame.font.Font('./fonts/BAUHS93.TTF', 30)
font_bar = pygame.font.Font('./fonts/arial.ttf', 15)
critical_v1 = pygame.font.Font('./fonts/BAUHS93.TTF', 70)



#define game variables
tile_size = 40
game_over = 0
level =1
max_levels = 10
score = 0
tile_types = 1


#define colours
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255 , 0 , 0 )
black = (0,0,0)
green = (0,255,0)
BG = (144,201,120)
yellow = (255, 255, 0)


#load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
healthbar_img = pygame.image.load('img/healthbar.png')
energy_img = pygame.image.load('img/energy.png')
healthbar_scale = pygame.transform.scale(healthbar_img, (190, 50))
energy_scale = pygame.transform.scale(energy_img, (250, 160))
wllp = pygame.image.load('img/wallpapper01.png')
wp = pygame.transform.scale(wllp, (800, 800))

#pick up boxes
health_box = pygame.image.load('img/coffee.png').convert_alpha()
monster_img = pygame.image.load('img/monster.png').convert_alpha()
item_boxes = {
	'Coffee'	: health_box,
	'Monster'	: monster_img,
}


#load  sounds
sound_hurt_enemy=pygame.mixer.Sound('clips/grunt.wav')
jump02 = pygame.mixer.music.load('clips/jump02.wav')
coin02 = pygame.mixer.music.load('clips/coin02.wav')
lava02 = pygame.mixer.music.load('clips/lava02.wav')
grass02 = pygame.mixer.music.load('clips/grass02.wav')
enemies = pygame.mixer.music.load('clips/enemy_hit.wav')
next_stage = pygame.mixer.music.load('clips/next_stage.wav')
pygame.mixer.music.load('clips/music.wav')
pygame.mixer.Channel(0).play(pygame.mixer.Sound('clips/music.wav'),maxtime=600)
pygame.mixer.music.play(-1, 0.0, 5000)
##pygame.mixer.music.load('clips/Boss.wav')
#pygame.mixer.music.play(-1,0.0,5000)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, red, (0, 300), (screen_width, 300))
#function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()
	item_box_group.empty()
	tree_group.empty()
	vine_group.empty()
	big_stone_group.empty()
	stone_group.empty()
	

	#load in level data and create world
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action
	
	

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([0, 0])
		self.rect = self.image.get_rect()
		self.reset(x, y)
		self.health = 100
		self.max_health = self.health
		self.alive = True
		self.energy = 1000
		self.max_energy = self.energy
		self.sprint = False
		

	def update(self, game_over):
		dx = 0
		dy = 0
		health = 100
		energy = 1000
		walk_cooldown = 4
		col_thresh = 20
		player.energy += 1.5
		if player.energy > player.max_energy:
			player.energy = player.max_energy

		if game_over == 0:
			#get keypresses			
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False and player.energy > 75: 
				pygame.mixer.Channel(0).play(pygame.mixer.Sound('clips/jump02.wav'),maxtime=600)
				player.energy -= 75
				self.vel_y = -15
				self.jumped = True
			if player.energy < 0:
					self.vel_y = 0
					player.energy = 0
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 3
				self.counter += 1
				self.direction = -1
				if key[pygame.K_LSHIFT]:		
					dx -= 3
					self.counter += 1
					self.direction = -1
					player.energy -= 5
					if player.energy <= 0:
						dx += 2
						walk_cooldown = 12
						self.counter -= 1
						self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 3
				self.counter += 1
				self.direction = 1
				if key[pygame.K_LSHIFT]:		
					dx += 2
					self.counter += 1
					self.direction = 1
					player.energy -= 5
					if player.energy <= 0:
						dx -= 2
						walk_cooldown = 12
						self.counter += 1
						self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]
			if key[pygame.K_LEFT] == True and key[pygame.K_RIGHT] == True:
				self.counter = 0
			if key[pygame.K_SPACE] and key[pygame.K_LSHIFT] and self.jumped == False and self.in_air == False and player.energy > 50 and (key[pygame.K_RIGHT] or key[pygame.K_LEFT]) :
				self.vel_y = -15
				self.jumped = True
				if key[pygame.K_SPACE] == False:
					self.jumped = False
			
			
			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0

				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False

			#check for collision with enemies
			for enemy in blob_group:
				if pygame.sprite.spritecollide(self, blob_group, False):
					pygame.mixer.Channel(2).play(pygame.mixer.Sound('clips/enemy_hit.wav'),maxtime=5000)
					if  self.direction == 1:
						dx -=  20
						

					if  self.direction == -1:
						dx +=  20
						
					player.health -= 12.5
					if player.health <= 0:
						game_over = -1

			#check wall collision
			if self.rect.centerx > screen_width:
				self.rect.centerx = screen_width
			if self.rect.centerx < 0:
				self.rect.centerx = 0


			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				pygame.mixer.Channel(2).play(pygame.mixer.Sound('clips/lava02.wav'),maxtime=5000)
            
			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				pygame.mixer.Channel(2).play(pygame.mixer.Sound('clips/next_stage.wav'),maxtime=5000)
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			draw_text("KOPHKES", font, red, (screen_width // 2) - 140, screen_height // 2-50)

			draw_text('kalo septembrh!', font, red, (screen_width // 2) - 250, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5


		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over

	

	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 60))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')
		underground_dirt01 = pygame.image.load('img/underground_dirt01.png')
		underground_dirt02 = pygame.image.load('img/underground_dirt02.png')
		underground_dirt03 = pygame.image.load('img/underground_dirt03.png')
		underground_dirt04 = pygame.image.load('img/underground_dirt04.png')
		underground_dirt05 = pygame.image.load('img/underground_dirt05.png')
		
		
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size - 10)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				if tile == 9:
					img = pygame.transform.scale(underground_dirt01, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 10:
					img = pygame.transform.scale(underground_dirt02, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 11:
					img = pygame.transform.scale(underground_dirt03, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 12:
					img = pygame.transform.scale(underground_dirt04, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 13:
					img = pygame.transform.scale(underground_dirt05, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 15:
					tree = Tree(col_count * tile_size, row_count * tile_size - (tile_size  - 20))
					tree_group.add(tree)
				if tile == 16:
					vine = Vine(col_count * tile_size, row_count * tile_size - (tile_size+10))
					vine_group.add(vine)
				if tile == 17:
					stone = Stone(col_count * tile_size, row_count * tile_size - (tile_size - 60))
					stone_group.add(stone)
				if tile == 18:
					big_stone = Big_Stone(col_count * tile_size, row_count * tile_size - (tile_size - 60))
					big_stone_group.add(big_stone)
				if tile == 19:#create health box
					item_box = ItemBox('Coffee', col_count * tile_size, row_count * tile_size)
					item_box_group.add(item_box)
				if tile == 20:
					item_box = ItemBox('Monster', col_count * tile_size, row_count * tile_size)
					item_box_group.add(item_box)
				col_count += 1
			row_count += 1
			    


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/enemy.png')
		self.image = pygame.transform.scale(self.image, (tile_size, tile_size + 25))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/thranio_pipi_ligo_pio_megalo.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y


	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1




class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/ects.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

class Water(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/water02.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Vine(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/vine.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size + 50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Tree(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/tree.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Stone(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/stone.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Big_Stone(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/big_stone.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))


	def update(self):
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Coffee':
				player.health += 50
				if player.health > player.max_health:
					player.health = player.max_health
			if self.item_type == 'Monster':
				player.energy += 500
				if player.energy > player.max_energy:
					player.energy = player.energy
			self.kill()
class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x 
		self.y = y 
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, black, (self.x + 28, self.y - 26, 150, 26))
		pygame.draw.rect(screen, red, (self.x + 28, self.y - 25, 150, 26))
		pygame.draw.rect(screen, green, (self.x + 28, self.y - 25, 150 * ratio, 26))
		screen.blit(healthbar_scale, (self.x - 2, self.y - 40, 154, 24))

class Energy():
	def __init__(self, x, y, energy, max_energy):
		self.x = x 
		self.y = y 
		self.energy = energy
		self.max_energy = max_energy

	def draw(self, energy):
		#update with new health
		self.energy = energy
		#calculate health ratio
		ratio = self.energy / self.max_energy
		pygame.draw.rect(screen, black, (self.x + 20, self.y - 27, 150, 27))
		pygame.draw.rect(screen, red, (self.x + 22, self.y - 24, 150, 22))
		pygame.draw.rect(screen, yellow, (self.x + 22, self.y - 24, 150 * ratio, 22))
		screen.blit(energy_scale, (self.x - 30, self.y - 95, 154, 24))


blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
vine_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
big_stone_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

player = Player(50, screen_height - 130)
#create health_bar
health_bar = HealthBar(10, 75, player.health, player.health)
energy = Energy(10, 120, player.energy, player.energy)

def pause_menu():
	
	paused = True
	while paused:
		screen.blit(wp,(0,0))
		draw_text('Paused', font, white, (screen_width // 2) - 100, (screen_height // 2)- 300)
		draw_text('Press esc to continue', font, white, (screen_width // 2) - 300, (screen_height // 2)- 200)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					paused = False
		if start_button.draw():
			paused = False
		if exit_button.draw():
			pygame.quit()
			quit()
		

		pygame.display.update()
        	 
				
				
						
                
        #gameDisplay.fill(white)
#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)



#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 300, screen_height // 2 + 20, start_img)
exit_button = Button(screen_width // 2 + 100, screen_height // 2 + 20, exit_img)


run = True
paused = False
while run:						#game loop 

	clock.tick(fps)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100))
	#show player health
		
	world.draw()
	health_bar.draw(player.health)
	energy.draw(player.energy)
	draw_text(str(player.health) + '/' + str(player.max_health), font_bar, black,tile_size + 50 , 52)
	draw_text(str(player.energy) + '/' + str(player.max_energy), font_bar, black,tile_size + 40 , 98)
	if game_over == 0:
			blob_group.update()
			platform_group.update()
			item_box_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				pygame.mixer.Channel(1).play(pygame.mixer.Sound('clips/coin02.wav'),maxtime=600)
				score += 1
			draw_text('X' + str(score), font_score, white, tile_size +5, 10)

			if pygame.sprite.spritecollide(player, coin_group, True):
				pygame.mixer.Channel(1).play(pygame.mixer.Sound('clips/coin02.wav'),maxtime=600)
				score += 1
			draw_text('X' + str(score), font_score, white, tile_size +5, 10)

	blob_group.draw(screen)
	platform_group.draw(screen)
	lava_group.draw(screen)
	coin_group.draw(screen)
	exit_group.draw(screen)
	water_group.draw(screen)
	vine_group.draw(screen)
	tree_group.draw(screen)
	stone_group.draw(screen)
	big_stone_group.draw(screen)
	item_box_group.draw(screen)

	game_over = player.update(game_over)

		#if player has died
	if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				player.health = 100
				game_over = 0
				score = 0
				player.energy = 1000
	answer = False
	ques = ["Η δομή της ακολουθίας χρησιμοποιείται για την επίλυση πολύπλοκων προβλημάτων?",
        "Οι μη προκαθορισμένοι τύποι επανάληψης χρησιμοποιούν υποχρεωτικά την εντολή for.",
        'Στη διπλή ή σύνθετη δομή επιλογής το else: , εκτελείται στην περίπτωση όπου η αρχική συνθήκη είναι False. ',
        'Η συνάρτηση range(), επιστρέφει μία λίστα αριθμών έτσι όπως αυτή ορίζεται μέσα στις παραμέτρους της',
        'Οι ονομασίες που δίνουμε στον ορισμό της συνάρτησης ονομάζονται παράμετροι , ενώ οι τιμές που δίνουμε όταν καλούμε τη συνάρτηση ονομάζονται ορίσματα',
        'Για να ορίσουμε μία συνάρτηση χρησιμοποιούμε τη χαρακτηριστική λέξη function , ακολουθεί ένα όνομα που ταυτοποιεί την εκάστοτε συνάρτηση και ένα ζευγάρι παρενθέσεων που μπορούν να περικλείουν ονόματα μεταβλητών, ενώ η γραμμή τελειώνει με άνω και κάτω τελεία',
        'Στις εμφωλευμένες δομές επανάληψης ο εσωτερικός βρόχος που περικλείεται μέσα στον εξωτερικό ολοκληρώνεται τελευταίος.',
        'Η δομή της επιλογής if χρησιμοποιείται , όταν θέλουμε να εκτελεστεί μια ακολουθία εντολών , εφόσον πληρείτε μία συγκεκριμένη συνθήκη. '
        ]

	answers=[False,False,True,False,True,True,False,True]
	# rand=random.choice(ques)
	pick =random.randint(0,7)
	rand07= ques[pick]

#if player has completed the level
	if game_over == 1:
		
				if level <10:
					from easygui import *
					import sys
					
					# message / information to be displayed on the screen
					message = rand07
					
					# title of the window
					title = "testing your knowlegde time:"
					
					# choices for yes and no button
					choices = ["True", "False"]
					
					# creating a yes no box
					output = ynbox(message, title, choices)

					if answers[pick]==True:		
						if output==True:															#epelekse true
							score+=5
							# message / information to be displayed on the screen
							message ="Ορθός!!"

							# title of the window
							title = "CORRECT"
							# creating a message box
							msg = msgbox(message, title)
							if level==9:
								level += 1
							else:
								level +=2

						if output==False:
							score -=5
							if score<=0:
								score = 0
							# message / information to be displayed on the screen
							message = "Λυπάμαι"
						
							# title of the window
							title = "FALSE"
						
							# creating a message box
							msg = msgbox(message, title)
							level += 1

					if answers[pick]==False:
						if output==False:																#epelekse false
							score+=5
								# message / information to be displayed on the screen
							message ="Ορθός!!"

								# title of the window
							title = "Correct"
								# creating a message box
							msg = msgbox(message, title)
							if level==9:
									level += 1
							else:
									level += 2
						else:
							score -=5
							if score<=0:
								score = 0
							# message / information to be displayed on the screen
							message = "Wrong"
							# title of the window
							title = " Incorrect"
							# creating a message box
							msg = msgbox(message, title)
							level += 1
							
					
			#reset game and go to next level		
				if level < max_levels:
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					player.energy = 1000
				else:
					draw_text('Ante, pires kai ptuxio', font, blue, (screen_width // 2) - 300, screen_height // 2)
					if restart_button.draw():
						level = 1
						#reset level
						world_data = []
						world = reset_level(level)
						game_over = 0
						score = 0
						player.energy = 1000

	
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				paused = True
				pause_menu()

	pygame.display.update()
		
pygame.quit()