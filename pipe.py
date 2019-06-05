import pygame
import random


class Pipe_up(pygame.sprite.Sprite):

	def __init__(self,width,height,start_x,pipe_height):
		self.screen_height,self.screen_width = height,width
		self.pipe_height = pipe_height
		self.image= pygame.transform.scale(pygame.image.load('Assets/pipe.png'),(50,self.pipe_height))
		self.x = self.screen_width-50+start_x
		self.y = self.screen_height-self.pipe_height
		self.rect = pygame.Rect(self.x,self.y,50,self.pipe_height)
		self.mask = pygame.mask.from_surface(self.image)
		# pipe_total = self.screen_height - 90
		# pipe_up = random.randint(50,250)
		# pipe_down = pipe_total - pipe_up

		# self.image_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets/pipe.png'),(50,pipe_down)),180)
		# self.image_up = pygame.transform.scale(pygame.image.load('Assets/pipe.png'),(50,pipe_up))
		# self.down_x = self.screen_width - 50 + start_x
		# self.down_y = 0
		# self.up_x = self.screen_width-50 + start_x
		# self.up_y = self.screen_height-pipe_up
		# self.width = 0 
		# self.up_height = pipe_up
		# self.down_height = pipe_down
		# self.rect = self.image_down.get_rect()
		# self.mask = pygame.mask.from_surface(self.image_down)


		super().__init__()

	def update(self):
		self.x -= 5
		self.rect = pygame.Rect(self.x,self.y,50,self.pipe_height)

class Pipe_down(pygame.sprite.Sprite):
	def __init__(self,width,height,start_x,pipe_height):
		self.screen_height,self.screen_width = height,width
		self.pipe_height = pipe_height
		self.image= pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Assets/pipe.png'),(50,self.pipe_height)),180)
		self.x = self.screen_width-50+start_x
		self.y = 0
		self.rect = self.rect = pygame.Rect(self.x,self.y,50,self.pipe_height)
		self.mask = pygame.mask.from_surface(self.image)
		# pipe_total = self.screen_height - 90
		# pipe_up = random.randint(50,250)
		# pipe_down = pipe_total - pipe_up

		super().__init__()

	def update(self):
		self.x -= 5
		self.rect = pygame.Rect(self.x,self.y,50,self.pipe_height)
