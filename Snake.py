'''
§________________________________________§

	♦ Created by: Andrés Felipe Mejía ♦
	♦ Creado por: Andrés Felipe Mejía ♦
§________________________________________§
'''


import pygame, sys
from pygame.locals import *
from random import randint as rand

#-----------------------------------------GLOBAL VARIABLES---------------------------------------------------------------
WIDTH = 1100
HEIGHT = 600
XSIZE = 20
YSIZE = 20
SCORE = 0
SPEED = 9

#------------------------------------------------------------------------ CLASSES OF THE GAME-----------------------------------------------------------




# ---------------------------------------------------------------------------- MAP CLASS ---------------------------------------------------------------------------------

class Map(pygame.sprite.Sprite):
	def __init__(self):
		self.gray = (89, 87, 93)

	def drawMap(self):
		for x in range(WIDTH):
			for y in range(HEIGHT):
				pygame.draw.rect(SCREEN, self.gray, (x*XSIZE, y*YSIZE, XSIZE, YSIZE), 1)


# ---------------------------------------------------------------------------- FOOD CLASS ---------------------------------------------------------------------------------

class Food(Map):
	def __init__(self):
		self.foodColor = (70, 15, 168)
		super(Food, self).__init__()
		self.__xpos = rand(1, WIDTH // XSIZE) * XSIZE - XSIZE
		self.__ypos = rand(1, HEIGHT // YSIZE) * YSIZE - XSIZE
		


	def drawFood(self):
		pygame.draw.rect(SCREEN, self.foodColor, (self.__xpos, self.__ypos, XSIZE, YSIZE))


	def eat(self, x, y):
		global SCORE, SPEED

		if x == self.__xpos and y == self.__ypos:
			# Delete before pos
			pygame.draw.rect(SCREEN, self.gray, (self.__xpos, self.__ypos, XSIZE, YSIZE), 1)

			# Reset food pos
			self.__xpos = rand(1, WIDTH // XSIZE) * XSIZE - XSIZE
			self.__ypos = rand(1, HEIGHT // YSIZE) * YSIZE - XSIZE
			pygame.draw.rect(SCREEN, self.foodColor, (self.__xpos, self.__ypos, XSIZE, YSIZE))

			# Increment the player score and increases the snake size
			SCORE += 1
			if not SCORE % 4:
				SPEED += 1

			return True

	def changeColor(self):
		self.foodColor = [rand(1, 255), rand(1, 255), rand(1, 255)]


# ---------------------------------------------------------------------------- SNAKE CLASS ---------------------------------------------------------------------------------

class Snake(Food):
	def __init__(self):
		pygame.init()
		pygame.font.init()
		super().__init__()
		self.snakeColor = (12, 117, 185)
		self.__xpos = 10 * XSIZE
		self.__ypos = 10 * YSIZE
		self.textFont = pygame.font.SysFont('Comic Sans MS', 30)
		self.bg = (0, 0, 0)
		self.body = [ [self.__xpos, self.__ypos], [self.__xpos + XSIZE, self.__ypos], [self.__xpos + XSIZE * 2, self.__ypos] ]
		self.snakeSize = 3
		for i in range(100):
			self.body.append([i, i])

		self.xdir = 1
		self.ydir = -1
		self.clock = pygame.time.Clock()
		#self.Existence()
		self.__main()
		

	def __main(self):
		while True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


			self.body[0] = [self.__xpos, self.__ypos]
			#self.controls()
			#self.changePos()
			self.time = self.clock.tick(SPEED)
			self.changePos()
			SCREEN.fill(self.bg)
			super().drawFood()
			if super().eat(self.__xpos, self.__ypos):
				self.snakeSize += 1
			self.controls()
			self.drawScore()
			self.drawSnake()
			self.movement()
			#self.makeSnake()
			self.collideBorders()
			self.collideBody()

			pygame.display.flip()

	
	def controls(self):
		key = pygame.key.get_pressed()
		
		# Verify if the player pressed a key to movement
		if key[K_DOWN] and self.ydir != 1 or key[K_s] and self.ydir != 1:
			self.ydir = 0
			self.xdir = -1

		elif key[K_UP] and self.ydir != 0 or key[K_w] and self.ydir != 0:
			self.ydir = 1
			self.xdir = -1

		if key[K_RIGHT] and self.xdir != 0 or key[K_d] and self.xdir != 0: # 
			self.xdir = 1
			self.ydir = -1

		elif key[K_LEFT] and self.xdir != 1 or key[K_a] and self.xdir != 1: # 
			self.xdir = 0
			self.ydir = -1

		# Tricks
		if key[K_g] and pygame.key.get_mods() & pygame.KMOD_SHIFT:
			self.snakeColor = [rand(1, 255), rand(1, 255), rand(1, 255)]

		elif key[K_f] and pygame.key.get_mods() & pygame.KMOD_SHIFT:
			super().changeColor()


	def changePos(self):

		for i in range(self.snakeSize-1, 0, -1):
			# Change the position of every unit of the body
			self.body[i][0] = self.body[i-1][0]
			self.body[i][1] = self.body[i-1][1]



	def movement(self):

		if self.ydir == 1:
			self.__ypos -= YSIZE # Ir hacia arriba

		elif self.ydir == 0:
			self.__ypos += YSIZE # Ir hacia abajo

		if self.xdir == 1:
			self.__xpos += XSIZE # Ir a la derecha

		elif self.xdir == 0:
			self.__xpos -= XSIZE # Ir a la izquierda

		#print(self.body[:self.snakeSize])

	def drawSnake(self):

		for i in range(self.snakeSize):
			pygame.draw.rect(SCREEN, self.snakeColor, (self.body[i][0], self.body[i][1], XSIZE, YSIZE))


	def drawScore(self):
		score = self.textFont.render(('Score _> ' + str(SCORE)), False, (255, 255, 255))
		SCREEN.blit(score, (20, 20))

	# End game
	def gameOver(self, end=False):
		game_over = self.textFont.render('GAME OVER', False, (1, 114, 145))
		SCREEN.blit(game_over, (WIDTH // 2 - 100, HEIGHT // 2 - 15))
		pygame.time.delay(3000)
		sys.exit()

	# If collide with a border
	def collideBorders(self):
		if self.__xpos <= -XSIZE or self.__xpos >= WIDTH:
			self.gameOver(True)

		elif self.__ypos <= -YSIZE or self.__ypos >= HEIGHT:
			self.gameOver(True)  


	# If collide with his own body
	def collideBody(self):
		if self.body[0] in self.body[2:self.snakeSize]:
			print('Body')
			self.gameOver(True)

	'''
	def Existence(self):
		text = self.textFont.render("¡Por favor, no destruyas la efímera existencia de la serpiente! :(", False, (1, 114, 145))
		SCREEN.blit(text, (WIDTH // 2 - 450, HEIGHT // 2 - 15))
		pygame.display.flip()
		pygame.time.delay(2000)
	'''
			

# ---------------------------------------------------------------------------- MAIN ---------------------------------------------------------------------------------

if __name__ == '__main__':
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Snake')

	game = Snake()
