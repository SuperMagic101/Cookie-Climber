import pygame
import time
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1920, 1080))
x = screen.get_width()
y = screen.get_height()

# images and stuff
og_bridge = pygame.image.load("bridge.png").convert_alpha()
bridge = pygame.transform.scale(og_bridge, (x, y))

og_room1 = pygame.image.load("startroom.png").convert_alpha()
room1 = pygame.transform.scale(og_room1, (x, y))
room2 = pygame.transform.scale(og_room1, (x, y))

def stage():
	screen.fill((30, 0, 0))
	screen.blit(quitbutton, quitRect)
	screen.blit(room1, (0, 0))
	screen.blit(room2, (0, -1*(y*levfactor)))
	screen.blit(bridge, (0, 0))


color = (255, 0, 0)

levfactor = 575/1080
floor = levfactor*1080 - 50
l_wall = 640/1920 * x
r_wall = 1180/1920 * x
levelCount = 0
score = levelCount * 100

class Cookie(pygame.sprite.Sprite):
	def __init__(self, imgs: list, height: int = 128, width: int = 128, health: int = 100, atk: int = 20):
		super().__init__()

		self.height = height
		self.width = width
		self.health = health
		self.atk = atk
		self.image = pygame.Surface([width, height])
		pygame.draw.rect(self.image, color, pygame.Rect(0, 0, 1, 1))

		ogleft = pygame.image.load(imgs[0]).convert_alpha()
		self.left = pygame.transform.scale(ogleft, (width, height))

		ogright = pygame.image.load(imgs[1]).convert_alpha()
		self.right = pygame.transform.scale(ogright, (width, height))

		ogleft_attack = pygame.image.load(imgs[2]).convert_alpha()
		self.left_attack = pygame.transform.scale(ogleft_attack, (width, height))

		ogright_attack = pygame.image.load(imgs[3]).convert_alpha()
		self.right_attack = pygame.transform.scale(ogright_attack, (width, height))

		self.rect = self.image.get_rect()
		self.rect.x = x/2
		self.rect.y = floor

		self.cookiex = self.rect.x
		self.cookiey = self.rect.y
		self.lastmove = self.left

		self.moving = False
		self.move_timer = 0

		self.jumping = False
		self.jump_timer = 0

		self.attacking = False
		self.attack_timer = 0

	def drawCookie(self):
		screen.blit(self.lastmove, (self.cookiex, self.cookiey))

	def moveLeft(self, pixels):
		self.moving = True
		self.rect.x -= pixels
		self.cookiex = self.rect.x
		if not self.attacking:
			self.lastmove = self.left
		self.move_timer = 10
	
	def moveRight(self, pixels):
		self.moving = True
		self.rect.x += pixels
		self.cookiex = self.rect.x
		if not self.attacking:
			self.lastmove = self.right
		self.move_timer = 10

	def jump(self, direction):
		jump_height = self.height
		self.rect.y -= jump_height
		self.cookiey = self.rect.y
		self.lastmove = direction
		self.jumping = True
		self.jump_timer = 90
			
	def attackLeft(self):
		self.attacking = True
		self.rect.x -= 150 
		self.cookiex = self.rect.x
		self.lastmove = self.left_attack
		if self.rect.x < l_wall:
			self.rect.x = l_wall
			self.cookiex = self.rect.x
		self.attack_timer = 60

	def attackRight(self):
		self.attacking = True
		self.rect.x += 150 
		self.cookiex = self.rect.x
		self.lastmove = self.right_attack
		if self.rect.x > r_wall:
			self.rect.x = r_wall
			self.cookiex = self.rect.x
		self.attack_timer = 60

player = Cookie(["cookiee_stand_left.png", "cookiee_stand_right.png", "cookiee_attack_left.png", "cookiee_attack_right.png"], 128, 128)

class GumDrop(pygame.sprite.Sprite):
	def __init__(self, imgs, height, width, health, atk, speed):
		super().__init__()
		self.imgs = imgs
		self.height = height
		self.width = width
		self.health = health
		self.atk = atk
		self.speed = speed
				
		self.image = pygame.Surface([width, height])
		pygame.draw.rect(self.image, color, pygame.Rect(0, 0, 1, 1))
		self.rect = self.image.get_rect()

		self.rect.x = l_wall + 100
		self.rect.y = floor

		self.gumdropx = self.rect.x
		self.gumdropy = self.rect.y

		self.moving = False
		self.move_timer = 0

	def pickGumDrop(self, ticker):
		oggumdrop = pygame.image.load(self.imgs[ticker % 3]).convert_alpha()
		gumdrop = pygame.transform.scale(oggumdrop, (self.width, self.height))
		return gumdrop

	def drawGumDrop(self):
		screen.blit(self.pickGumDrop(levelCount), (self.gumdropx, self.gumdropy))

	def gumMoveLeft(self):
		self.moving = True
		self.rect.x -= self.speed
		self.gumdropx = self.rect.x
		self.move_timer = 10

	def gumMoveRight(self):
		self.moving = True
		self.rect.x += self.speed
		self.gumdropx = self.rect.x
		self.move_timer = 10

enemy = GumDrop(["green_gumdrop.png", "red_gumdrop.png", "blue_gumdrop.png"], 160, 160, (levelCount + 1)*100, 30, (levelCount + 1)*5)

titlefont = pygame.font.SysFont("timesnewroman",  60, True)
title = titlefont.render("Cookie Climber", True, color)
titleRect = title.get_rect()
titleRect.center = (x/2, y/5)

buttonfont = pygame.font.SysFont("timesnewroman", 36)

quitbutton = buttonfont.render("Quit", True, color)
quitRect = quitbutton.get_rect()
quitRect.center = (x/2, y/2 + 50)

backbutton = buttonfont.render("Back", True, color)

startbutton = buttonfont.render("Start", True, color)
startRect = startbutton.get_rect()
startRect.center = (x/2, y/2 - 50)

aboutbutton = buttonfont.render("About", True, color)
aboutRect = aboutbutton.get_rect()
aboutRect.center = (x/2, y/2)

level = buttonfont.render("Level", True, color)
levelRect = level.get_rect()
levelRect.center = (x/2, y/2)

readingfont = pygame.font.SysFont("timesnewroman", 16)

f = open("aboutMenu.txt")
blurb1 = readingfont.render(f.readline(60), True, color)
f.readline()
blurb2 = readingfont.render(f.readline(62), True, color)
f.readline()
blurb3 = readingfont.render(f.readline(64), True, color)
f.readline()
blurb4 = readingfont.render(f.readline(86), True, color)
f.readline()
blurb5 = readingfont.render(f.readline(68), True, color)

blurb1Rect = blurb1.get_rect()
blurb2Rect = blurb2.get_rect()
blurb3Rect = blurb3.get_rect()
blurb4Rect = blurb4.get_rect()
blurb5Rect = blurb5.get_rect()

blurb1Rect.center = (x/2, y/2 - 30)
blurb2Rect.center = (x/2, y/2 - 10)
blurb3Rect.center = (x/2, y/2 + 10)
blurb4Rect.center = (x/2, y/2 + 30)
blurb5Rect.center = (x/2, y/2 + 50)

menu_left = quitRect.center[0] - 1/2 * quitRect.width
menu_right = quitRect.center[0] + 1/2 * quitRect.width

start_top = startRect.center[1] - 1/2 * startRect.height
start_bottom = startRect.center[1] + 1/2 * startRect.height

about_top = aboutRect.center[1] - 1/2 * aboutRect.height
about_bottom = aboutRect.center[1] + 1/2 * aboutRect.height

quit_top = quitRect.center[1] - 1/2 * quitRect.height
quit_bottom = quitRect.center[1] + 1/2 * quitRect.height

level_top = levelRect.center[1] - 1/2 * levelRect.height
level_bottom = levelRect.center[1] + 1/2 * levelRect.height

running = True
startMenu = True
aboutScreen = False
gameStarted = False
levelChange = False

while running == True:
	if gameStarted == True:
		player.atk = (levelCount + 2)//2 * 20

		if player.rect.y < floor and player.jumping == True:
			if player.jump_timer > 0:
				player.jump_timer -= 1
			else:
				player.rect.y = floor
				player.cookiey = player.rect.y
				player.jumping = False
		
		if player.attacking == True:
			if player.attack_timer > 0:
				player.attack_timer -= 1
			else:
				player.attacking = False
				if player.lastmove == player.left_attack:
					player.lastmove = player.left
				elif player.lastmove == player.right_attack:
					player.lastmove = player.right

		if player.moving == True:
			if player.move_timer > 0:
				player.move_timer -= 1
			else:
				player.moving = False

		if enemy.moving == True:
			if enemy.move_timer > 0:
				enemy.move_timer -= 1
			else:
				enemy.moving = False

		if (enemy.gumdropx - enemy.width/3) <= player.cookiex <= (enemy.gumdropx + enemy.width/3) and not player.jumping:
			if player.attacking and (not hasattr(player, 'damage_cooldown') or player.damage_cooldown <= 0):
				enemy.health -= player.atk
				player.damage_cooldown = 300
			elif not player.attacking and (not hasattr(enemy, 'damage_cooldown') or enemy.damage_cooldown <= 0):
				player.health -= enemy.atk
				enemy.damage_cooldown = 300 
		
		# Handle damage cooldowns
		if hasattr(player, 'damage_cooldown') and player.damage_cooldown > 0:
			player.damage_cooldown -= 1
		if hasattr(enemy, 'damage_cooldown') and enemy.damage_cooldown > 0:
			enemy.damage_cooldown -= 1

		if player.health <= 0:
			startMenu = True
			gameStarted = False
			player.health = 100
			continue

		if enemy.health <= 0:
			levelChange = True

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player.cookiex >= l_wall and not player.moving:
			player.moveLeft(10)
		if keys[pygame.K_RIGHT] and player.cookiex <= r_wall and not player.moving:
			player.moveRight(10)
		if keys[pygame.K_UP] and player.rect.y >= floor and not player.jumping: 
			player.jump(player.lastmove)
		if keys[pygame.K_LEFT] and keys[pygame.K_SPACE] and not player.attacking:
			player.attackLeft()
		if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE] and not player.attacking:
			player.attackRight()

		if enemy.health > 0:
			if enemy.gumdropx < player.cookiex and not enemy.moving:
				enemy.gumMoveRight()
			elif enemy.gumdropx > player.cookiex and not enemy.moving:
				enemy.gumMoveLeft()

		if levelChange == True:			
			score += 100
			screen.fill((30, 0, 0))

			for i in range(0, int(levfactor*1080/5)):
				time.sleep(0.015)
				screen.blit(room1, (0, i*5))
				screen.blit(room2, (0, (i-levfactor*1080/5)*5))
				screen.blit(bridge, (0, 0))
				pygame.display.update()
			levelChange = False
			levelCount += 1
			enemy.health = (levelCount + 1)*100
		else:
			screen.fill((30, 0, 0))
			screen.blit(quitbutton, quitRect)
			screen.blit(room1, (0, 0))
			screen.blit(room2, (0, -1*(y*levfactor)))
			screen.blit(bridge, (0, 0))
			
			phealth = buttonfont.render("Player Health: " + str(player.health), True, color)
			ehealth = buttonfont.render("Enemy Health: " + str(enemy.health), True, color)
			phealthRect = phealth.get_rect()
			ehealthRect = ehealth.get_rect()
			phealthRect.center = (x/5, y/5)
			ehealthRect.center = (4*x/5, y/5)
			
			screen.blit(phealth, phealthRect)
			screen.blit(ehealth, ehealthRect)


			levelheader = buttonfont.render("Level " + str(levelCount), True, color)
			scoreheader = buttonfont.render("Score: " + str(score), True, color)

			levelheadRect = levelheader.get_rect()
			levelheadRect.center = (2*x/5, y/5)
			scoreheadRect = scoreheader.get_rect()
			scoreheadRect.center = (3*x/5, y/5)
			screen.blit(levelheader, levelheadRect)
			screen.blit(scoreheader, scoreheadRect)

			player.drawCookie()
			enemy.drawGumDrop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if menu_left <= mouse[0] <= menu_right and quit_top <= mouse[1] <= quit_bottom:
					running = False
				elif menu_left <= mouse[0] <= menu_right and level_top <= mouse[1] <= level_bottom:
					levelChange = True

		pygame.display.update()

	for event in pygame.event.get():
		mouse = pygame.mouse.get_pos()

		if startMenu == True:			
			screen.fill((30, 0, 0))
			screen.blit(title, titleRect)
			screen.blit(startbutton, startRect)
			screen.blit(aboutbutton, aboutRect)
			quitRect.center = (x/2, y/2 + 50)
			screen.blit(quitbutton, quitRect)

			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if menu_left <= mouse[0] <= menu_right and quit_top <= mouse[1] <= quit_bottom:
					running = False
				elif menu_left <= mouse[0] <= menu_right and start_top <= mouse[1] <= start_bottom:
					gameStarted = True
					startMenu = False
					break
				elif menu_left <= mouse[0] <= menu_right and about_top <= mouse[1] <= about_bottom:
					aboutScreen = True
					startMenu = False

		if aboutScreen == True:
			screen.fill((30, 0, 0))
			quitRect.center = (x/5, 4*y/5)
			screen.blit(backbutton, quitRect)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if (x/5 - quitRect.width/2) <= mouse[0] <= (x/5 + quitRect.width/2) and (4*y/5 - quitRect.height/2) <= mouse[1] <= (4*y/5 + quitRect.height/2):
					aboutScreen = False
					startMenu = True
			screen.blit(blurb1, blurb1Rect)
			screen.blit(blurb2, blurb2Rect)
			screen.blit(blurb3, blurb3Rect)
			screen.blit(blurb4, blurb4Rect)
			screen.blit(blurb5, blurb5Rect)
			if event.type == pygame.QUIT:
				running = False
			
		pygame.display.update()



pygame.quit()