import pygame
import random

pygame.init()
pygame.mixer.init()

#pygame.mixer.music.play()

#variable declaration

#speed
clock = pygame.time.Clock()
fps = 60

#screen resolution and title
screen_width = 864
screen_height = 636
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TGameZ 2D Flappy Bird')
pygame.display.set_icon(pygame.image.load("./img/gameIcon.png"))
#score properties
ScoreFont = pygame.font.SysFont('Cantarell Extra Bold', 65)
scoreColor = (random.randint(0, 255), random.randint(0, 255),random.randint(0, 150))

#gameplay properties
click = False
deco_speed =4  
game_over = False
pipe_gap = 165
pipe_frequency = 1400
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pipe_passed = False

#deco
background = pygame.image.load('img/bg.png')
logoDeco = pygame.image.load('img/logo.png')
restartButton = pygame.image.load('img/restart.png')
level1Button= pygame.image.load('img/level1.png')
level2Button= pygame.image.load('img/level2.png')
level3Button= pygame.image.load('img/level3.png')
select_levelDeco = pygame.image.load('img/select_level.png')

class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for imgnum in range(2, 4):
			img = pygame.image.load(f'img/bird{imgnum}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.velocity = 0
		self.clicked = False

	def update(self):

		if click == True:
			#fall
			self.velocity += 0.5
			if self.velocity > 8:
				self.velocity = 8
			if self.rect.bottom < 800:
				self.rect.y += int(self.velocity)

		if game_over == False:
			#jump
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
				self.clicked = True
				self.velocity = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#manage animation
			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#adjust bird
			self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/pipe.png')
		self.rect = self.image.get_rect()
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]

	def update(self):
		self.rect.x -= deco_speed
		if self.rect.right < 0:
			self.kill()

#button and skeleton
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):

		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check if mouse is over the button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action
	
class Deco():
	def __init__(self, x,y,image):
		self.image= image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def display(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))	

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

bird_pos = Bird(100, int(screen_height / 2))

bird_group.add(bird_pos)

#create restart, level button and decorations instances
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, restartButton)
level1 = Button(screen_width // 2 - 90, screen_height // 2 , level1Button)
level2 = Button(screen_width // 2 - 90, screen_height // 2 +100, level2Button)
level3 = Button(screen_width // 2 - 90, screen_height // 2 +200, level3Button)
logo = Deco(screen_width // 2 - 70, screen_height // 2 - 250, logoDeco)
select_level = Deco(screen_width // 2 - 170, screen_height // 2 - 150, select_levelDeco)
running = True
while running:
	
	clock.tick(fps)

	#draw background
	screen.blit(background, (0,0))

	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pipe_passed == False:
			pipe_passed = True
		if pipe_passed == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pipe_passed = False

	#display score
	scoreDisp = ScoreFont.render(str(score), True, scoreColor)
	screen.blit(scoreDisp, (int(screen_width / 2), 20))

	#look for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) :
		game_over = True

	#check if bird has hit the ground or reach the sky
	if bird_pos.rect.bottom >= screen_height or bird_pos.rect.bottom < 0:
		game_over = True
		click = False
    
	if game_over == False and click == True:

		#generate new pipes
		currentTime = pygame.time.get_ticks()
		if currentTime - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = currentTime
   
		pipe_group.update()

	
	#check for game over and reset
	if game_over == True:
			logo.display()
			select_level.display()	
		#if button.draw() == True:
			if level1.draw() == True:
				#pygame.mixer.music.stop()
				game_over = False
				pipe_group.empty()
				bird_pos.rect.x = 100
				bird_pos.rect.y = int(screen_height / 2)
				pipe_gap = 190
				pipe_frequency = 1600
				last_pipe = pygame.time.get_ticks() - pipe_frequency
				score = 0
			if level2.draw() == True:
				#pygame.mixer.music.stop()
				game_over = False
				pipe_group.empty()
				bird_pos.rect.x = 100
				bird_pos.rect.y = int(screen_height / 2)
				score = 0
			if level3.draw() == True:
				#pygame.mixer.music.stop()
				game_over = False
				pipe_group.empty()
				bird_pos.rect.x = 100
				bird_pos.rect.y = int(screen_height / 2)
				pipe_gap = 150
				pipe_frequency = 1200
				last_pipe = pygame.time.get_ticks() - pipe_frequency
				score = 0
			

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN and click == False and game_over == False:
			click = True

	pygame.display.update()

pygame.quit()
