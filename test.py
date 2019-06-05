from bird import Bird
from pipe import Pipe
import random
# from neuralnet import *
import pygame
import time 
import numpy as np



class obj():
	def __init__(self,x,a,z,b,yHat):
		self.x = x
		self.a = a
		self.z = z
		self.b = b
		self.yHat = yHat
		# self.J = J


def NNForward(x,alpha,beta):
	# print("Forward")
	a = np.array(np.dot(alpha,x)).flatten()
	z = 1 / (1 + (np.exp(-a)))
	z = np.append([1],z)
	# print(z.shape)
	b = np.array(np.dot(beta,z)).flatten()
	yHat = np.array(np.exp(b) / np.sum(np.exp(b))).flatten()
	# J = -1 * np.dot(y.transpose(),np.log(yHat))
	# print(J)
	o = obj(x,a,z,b,yHat)
	# print(a.shape,z.shape,b.shape,yHat.shape,J)
	# print(J)
	return o

def NNBackward(x,y,alpha,beta,o):
	gy = -1 * y / o.yHat
	# print(np.diag(gy))
	# print("this is ",(np.matrix(o.yHat).transpose() * np.matrix(o.yHat)))
	gb = np.matrix(o.yHat - y )
	# print(gb.shape)
	# gb = np.matrix(np.dot(gy.transpose(),(np.diag(o.yHat) - (np.matrix(o.yHat).transpose() * np.matrix(o.yHat)))))
	# print(gb.shape)
	gbeta = np.dot(gb.transpose(),np.matrix(o.z.transpose()))
	# print(gbeta.shape)
	# print(beta.shape,gb.shape)

	gz = (np.dot(beta.transpose(),gb.transpose()))[1:]
	# print(gz.shape)
	# print(gz)
	# print(gz[1:])
	z = np.matrix(o.z[1:])
	ga = np.multiply(np.multiply(gz,z.transpose()),(1-z).transpose())
	# print("----")
	# print("----")
	# print("----")
	# print("x,ga")
	# print(x,ga)
	galpha = np.dot(ga,np.matrix(x))
	# quit()
	return galpha,gbeta


def train():
	temp = [(395, 202.0, 1), (345, 85.99999999999997, 1), (300, -86.80000000000013, 0), (295, -77.60000000000014, 1), (245, -29.600000000000136, 1), (220, -35.600000000000136, 0), (195, 2.3999999999998636, 1), (145, 18.399999999999864, 1), (100, -35.600000000000136, 0), (95, -26.400000000000148, 1), (45, 21.599999999999852, 1), (0, -3.6000000000001364, 0), (-5, 5.599999999999852, 1), (-55, 53.59999999999985, 1), (95, -12.400000000000148, 1), (90, -20.00000000000017, 0), (45, 33.99999999999983, 1), (-5, 17.99999999999983, 1), (-55, -78.00000000000017, 1), (125, -24.800000000000182, 0), (95, 18.399999999999807, 1), (45, 26.399999999999807, 1), (25, 7.199999999999818, 0), (-5, 50.39999999999981, 1), (-55, 58.39999999999981, 1), (105, -71.80000000000018, 0), (95, -54.200000000000216, 1), (420, 195.0, 0), (395, 233.0, 1), (345, 249.0, 1), (295, 185.0, 1), (245, 40.99999999999994, 1), (210, -107.40000000000015, 0), (195, -82.20000000000016, 1), (150, -49.80000000000018, 0), (145, -40.60000000000019, 1), (95, 7.399999999999807, 1), (60, -6.600000000000193, 0), (45, 18.599999999999795, 1), (-5, 50.599999999999795, 1), (-55, 2.5999999999997954, 1), (125, -30.000000000000227, 0), (95, 13.199999999999761, 1), (45, 21.19999999999976, 1), (15, -12.400000000000261, 0), (-5, 19.59999999999974, 1), (-55, 43.59999999999974, 1), (110, -19.200000000000273, 0), (95, 5.999999999999716, 1), (45, 37.999999999999716, 1), (-5, -10.000000000000284, 1), (-55, -138.00000000000034, 1), (130, -25.00000000000034, 0), (95, 22.599999999999625, 1), (45, 22.599999999999625, 1), (15, -15.800000000000352, 0), (-5, 16.199999999999648, 1), (-50, 41.399999999999636, 0), (-55, 50.599999999999625, 1), (100, -70.40000000000038, 0), (100, -70.40000000000038, 1), (395, 193.0, 1), (345, 76.99999999999997, 1), (315, -31.000000000000057, 0), (295, 0.9999999999999432, 1), (245, 24.999999999999943, 1), (195, -31.000000000000057, 1), (185, -51.80000000000007, 0), (145, -0.6000000000000796, 1), (95, -8.60000000000008, 1), (90, -13.800000000000068, 0), (45, 40.19999999999993, 1), (-5, 24.199999999999932, 1), (-35, -23.800000000000068, 0), (-55, 8.199999999999932, 1), (95, 4.199999999999932, 1), (75, -8.60000000000008, 0), (45, 34.59999999999991, 1), (395, 261.0, 1), (345, 144.99999999999997, 1), (295, -51.000000000000114, 1), (290, -75.00000000000011, 0), (245, -21.000000000000114, 1), (195, -37.000000000000114, 1), (180, -57.40000000000015, 0), (145, -9.800000000000182, 1), (95, -9.800000000000182, 1), (80, -25.400000000000148, 0), (45, 22.199999999999818, 1), (-5, 22.199999999999818, 1), (-50, -46.20000000000016, 0), (-55, -37.00000000000017, 1), (95, 34.99999999999983, 1), (45, 2.9999999999998295, 1), (35, -13.00000000000017, 0), (-5, 38.19999999999982, 1), (-55, 30.199999999999818, 1), (95, -21.800000000000182, 0), (95, -21.800000000000182, 1), (45, 34.19999999999982, 1), (-5, 10.199999999999818, 1), (-10, 3.3999999999998067, 0), (-55, 57.39999999999981, 1), (110, -49.400000000000205, 0), (95, -24.200000000000216, 1), (45, 7.799999999999784, 1), (35, 4.599999999999795, 0), (-5, 55.799999999999784, 1), (-55, 47.799999999999784, 1), (130, -57.80000000000024, 0), (100, -14.60000000000025, 1), (50, -6.60000000000025, 1), (40, -14.60000000000025, 0), (0, 36.59999999999974, 1), (-50, 28.59999999999974, 1), (105, 0.5999999999997385, 1), (95, -26.60000000000025, 0), (55, 24.59999999999974, 1), (5, 16.59999999999974, 1), (-10, -1.4000000000002615, 0), (-45, 46.199999999999704, 1), (110, -7.800000000000296, 1), (90, -30.2000000000003, 0), (60, 12.999999999999687, 1), (10, 20.999999999999687, 1), (-40, -51.00000000000034, 1), (140, -34.00000000000034, 0), (115, 3.999999999999659, 1), (65, 19.99999999999966, 1), (35, -8.800000000000352, 0), (15, 23.199999999999648, 1), (-35, 47.19999999999965, 1), (120, 93.19999999999965, 1), (75, -25.600000000000364, 0), (70, -16.400000000000375, 1), (20, 31.599999999999625, 1), (-15, 17.599999999999625, 0), (-30, 42.79999999999961, 1), (140, -101.40000000000038, 0), (125, -76.20000000000039, 1), (85, -44.20000000000039, 0), (75, -26.600000000000392, 1), (25, 13.399999999999608, 1), (-10, -6.2000000000003865, 0), (-25, 18.999999999999602, 1)]
	trainData = []
	for data in temp:
		normx = (data[0]-500)/500
		normy = (data[1]-500)/500
		trainData.append((normx,normy,data[2]))


	trainOutput = []
	learningRate = 0.1
	for data in trainData:
		temp = [data[0],data[1]]
		features = np.asarray(temp)
		oneHot = np.zeros(2)
		oneHot[data[2]] = 1
		trainOutput.append((features,oneHot))
	hidden = 5
	alpha = np.zeros((hidden,2))
	for i in range(hidden):
		for j in range(2):
			if j == 0:
				alpha[i][j] = 0
			else:
				alpha[i][j] = random.uniform(-0.1,0.1)
	beta = np.zeros((2,hidden+1))
	for i in range(2	):
		for j in range(hidden+1):
			if j == 0:
				beta[i][j] = 0
			else:
				beta[i][j] = random.uniform(-0.1,0.1)

	for i in range(50):
		# print("epoch = ",i+1)
		for (x,y) in trainOutput:
			o = NNForward(x,alpha,beta)#pass parameters
			galpha,gbeta = NNBackward(x,y,alpha,beta,o)
			alpha = alpha - galpha * learningRate
			beta = beta - gbeta * learningRate

	return alpha,beta




def collision_up (bird_x, bird_y, bird_width, bird_height, pipe_x, pipe_y, pipe_width,pipe_height):
	# horiontal collisions
	# print(bird_y)
	if (bird_x + bird_width >= pipe_x and bird_x <= pipe_x + pipe_width):
		# print("in range")

		if (bird_y + bird_height >= pipe_y):

			# print(pipe_y)
			print("collision detected with up pipe")
			return True
	return False


def collision_down (bird_x, bird_y, bird_width, bird_height, pipe_x, pipe_y, pipe_width,pipe_height):
	# horiontal collisions
	# print(bird_y)
	if (bird_x + bird_width >= pipe_x and bird_x <= pipe_x + pipe_width):
		# print("in range")

		if (bird_y <= pipe_y + pipe_height):

			# print(pipe_y)
			print("collision detected with down pipe")
			return True
	return False




def main():
	width, height = 500,500
	flappy = Bird(width,height)
	bird_list = pygame.sprite.Group()
	pipe_sprite_list = pygame.sprite.Group()
	bird_list.add(flappy)
	
	alpha, beta = train()
	print("done training")
	pygame.init()
	width, height = 500,500
	screen = pygame.display.set_mode((500, 500))
	pygame.display.set_caption('Basic Pygame program')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Display some text
	font = pygame.font.Font(None, 36)
	text = font.render("Hello There", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)
	init_state = True
	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()
	pipe_list = [] 
	new_pipe_list = []
	score = 0
	for i in range(4):
		pipe = Pipe(width,height,i*200)
		# pipe_list.append(Pipe(width,height,i * 300))
		new_pipe_list.append(pipe)
		pipe_list.append(pipe)
	# Event loop
	start_count = False
	count = 0
	moves = []
	def play(alpha,beta):
		print("hi")
		nonlocal moves
		width, height = 500,500
		flappy = Bird(width,height)
		bird_list = pygame.sprite.Group()
		pipe_sprite_list = pygame.sprite.Group()
		bird_list.add(flappy)
		pipe_list = [] 
		new_pipe_list = []
		score = 0
		for i in range(4):
			pipe = Pipe(width,height,i*200)
			# pipe_list.append(Pipe(width,height,i * 300))
			new_pipe_list.append(pipe)
			pipe_list.append(pipe)
		# Event loop
		start_count = False
		count = 0
		while 1:
			screen.fill((255,255,255))
			# if init_state:
			count+=1



			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()

					# get a list of all sprites that are under the mouse cursor
					clicked_sprites = [s for s in bird_list if s.rect.collidepoint(pos)]
					print(clicked_sprites)
				if event.type == pygame.KEYDOWN:
					# print('hi')
					if event.key == pygame.K_TAB:
						print(moves)
					if event.key == pygame.K_SPACE:
						# print('hi')
						hor_dis = pipe_list[0].down_x - flappy.x + flappy.width
						vert_dis = pipe_list[0].down_height - flappy.y + 45
						moves.append((hor_dis,vert_dis,0))
						flappy.vy = -10
				
			bird_list.draw(screen)

			pygame.display.update()

	play(alpha,beta)
		








if __name__ == '__main__':
	main()