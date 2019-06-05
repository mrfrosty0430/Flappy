import pygame


class Bird(pygame.sprite.Sprite):

	def __init__(self,width,height):
		self.screen_height,self.screen_width = height,width
		# self.image = pygame.transform.scale(pygame.image.load('Assets/test-1.png'),(35,35))
		self.die = False
		self.x = 40
		self.y = 40
		self.initX = self.x
		self.initY = self.y
		self.vy = 0
		self.gravity = 0.8
		self.width,self.height = 30,30
		self.image = pygame.transform.scale(pygame.image.load('Assets/test-1.png'),(self.width,self.height))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)


		super().__init__()


	def update(self):
		if (self.y >= self.screen_width-30):
			self.die = True
		self.vy += self.gravity
		self.y += self.vy 
		# self.rect = self.image.get_rect()
		self.gravity = 0.8
		self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
		# print(self.rect)
		self.mask = pygame.mask.from_surface(self.image)

