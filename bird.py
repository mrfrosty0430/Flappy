import pygame


class Bird(pygame.sprite.Sprite):

	def __init__(self,width,height,prio,startY):
		self.screen_height,self.screen_width = height,width
		# self.image = pygame.transform.scale(pygame.image.load('Assets/test-1.png'),(35,35))
		self.die = False
		self.fitness = 0 
		self.x = 40
		self.y = startY
		self.startY = self.y
		self.prio = prio
		self.initX = self.x
		self.initY = self.y
		self.vy = 0
		self.gravity = 0.8
		self.width,self.height = 30,30
		self.image = pygame.transform.scale(pygame.image.load('Assets/test-1.png'),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)


		super().__init__()

	def __lt__ (self,other):
		return self.fitness < other.fitness

	def __le__ (self,other):
		return self.fitness <= other.fitness

	def __gt__ (self,other):
		return self.fitness > other.fitness

	def __ge__ (self,other):
		return self.fitness >= other.fitness

	def __eq__ (self,other):
		return self.fitness == other.fitness

	def __ne__ (self,other):
		return self.fitness != other.fitness

	def __hash__(self):
		return self.prio
	
	def restart(self):
		self.x = 40
		self.y = self.startY
		self.vy = 0
		self.gravity = 0.8
		self.rect = pygame.Rect(self.x,self.startY,self.width,self.height)
		self.mask = pygame.mask.from_surface(self.image)
		self.fitness = 0
		self.die = False
	


	def update(self):
		if (self.y >= self.screen_width-30 or self.y < 0):
			self.die = True

		self.vy += self.gravity
		self.y += self.vy

		# self.fitness += 1
		self.gravity = 0.8
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		self.mask = pygame.mask.from_surface(self.image)

