from bird import Bird
from pipe import Pipe_up
from pipe import Pipe_down
import random
import pygame
import math
import time
import numpy as np



class obj():
	def __init__(self,x,a,z,b,yHat):
		self.x = x
		self.a = a
		self.z = z
		self.b = b
		self.yHat = yHat


def NNForward(x,alpha,beta):
	a = np.array(np.dot(alpha,x)).flatten()
	z = 1 / (1 + (np.exp(-a)))
	z = np.append([1],z)
	b = np.array(np.dot(beta,z)).flatten()
	yHat = np.array(np.exp(b) / np.sum(np.exp(b))).flatten()
	o = obj(x,a,z,b,yHat)
	return o

def NNBackward(x,y,alpha,beta,o):
	gy = -1 * y / o.yHat
	gb = np.matrix(o.yHat - y )
	gbeta = np.dot(gb.transpose(),np.matrix(o.z.transpose()))
	gz = (np.dot(beta.transpose(),gb.transpose()))[1:]
	z = np.matrix(o.z[1:])
	ga = np.multiply(np.multiply(gz,z.transpose()),(1-z).transpose())
	galpha = np.dot(ga,np.matrix(x))
	return galpha,gbeta


def initialize(width,height):
	population_size = 10
	hidden_layer = 5
	input_layer = 2
	bird_list = pygame.sprite.Group()
	for pop_idx in range(population_size):
		bird = Bird(width,height,pop_idx,40 + 40  * pop_idx)

		#initialize alpha beta layers

		alpha = np.zeros((hidden_layer,input_layer))
		beta = np.zeros((input_layer,hidden_layer+1))
		for i in range(hidden_layer):
			for j in range(input_layer):
				if j == 0:
					alpha[i][j] = 0
				else:
					alpha[i][j] = random.uniform(-0.5,0.5)


		for i in range(input_layer):
			for j in range(hidden_layer+1):
				if j == 0:
					beta[i][j] = 0
				else:
					beta[i][j] = random.uniform(-0.5,0.5)

		bird.alpha = alpha
		bird.beta = beta

		bird_list.add(bird)

	return bird_list




def make_crossover(max1,max2):
	alpha_1 = max1.alpha
	beta_1 = max1.beta

	alpha_2 = max2.alpha
	beta_2 = max2.beta
	offspring = []
	print(wtf)
	for i in range(5):
		#alpha crossover`

		cross_length_alpha = random.randint(0,len(alpha_1)-1)
		# print(beta_2[0].shape)
		new_alpha_a = np.concatenate([alpha_1[:cross_length_alpha],alpha_2[cross_length_alpha:] ])
		new_alpha_b = np.concatenate([alpha_2[:cross_length_alpha],alpha_1[cross_length_alpha:] ])


		#beta crossover
		cross_length_beta1 = random.randint(0,len(beta_1[0])-1)
		new_beta_a1 = np.concatenate([(beta_1[0])[:cross_length_beta1],(beta_2[0])[cross_length_beta1:] ])
		# print(new_beta_a1.shape)
		new_beta_b1 = np.concatenate([(beta_2[0])[:cross_length_beta1],(beta_1[0])[cross_length_beta1:] ])

		cross_length_beta2 = random.randint(0,len(beta_1[0])-1)
		new_beta_a2 = np.concatenate([(beta_1[1])[:cross_length_beta2],(beta_2[1])[cross_length_beta2:] ])
		new_beta_b2 = np.concatenate([(beta_2[1])[:cross_length_beta2],(beta_1[1])[cross_length_beta2:] ])

		# print(new_beta_a2.shape)
		# print(new_beta_b2.shape)
		# quit()
		offspring_a = (new_alpha_a,np.array([new_beta_a1,new_beta_a2]))
		offspring_b = (new_alpha_b,np.array([new_beta_b1,new_beta_b2]))
		print(offspring_b[0])
		print(offspring_b[1])
		offspring.append(offspring_a)
		offspring.append(offspring_b)


	return offspring


def apply_mutation(offsprings):
	for offspring in offsprings:
		#alpha mutation
		alpha = offspring[0]
		for row in range (len(alpha)):
			for col in range(1,len(alpha[row])):
				if random.random() < 1/len(alpha):
					alpha[row][col] += random.uniform(-0.10,0.10)

		#beta mutation
		beta = offspring[1]
		# print(beta.shape)
		for row in range (len(beta)):
			for col in range (1,len(beta[row])):
				if random.random() < 1/len(beta[row]):
					beta[row][col] += random.uniform(-0.10,0.10)


	return offsprings


def main():
	width, height = 500,500
	bird_list = initialize(width,height)
	pipe_sprite_list = pygame.sprite.Group()
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
	pipe_up_list = []
	new_pipe_up_list = []
	pipe_down_list = []
	new_pipe_down_list = []

	for i in range(4):
		pipe_up_height = random.randint(50,250)
		pipe_down_height = height-90-pipe_up_height
		pipe_up = Pipe_up(width,height,i*200,pipe_up_height)
		pipe_down = Pipe_down(width,height,i*200,pipe_down_height)
		new_pipe_up_list.append(pipe_up)
		new_pipe_down_list.append(pipe_down)
		pipe_up_list.append(pipe_up)
		pipe_down_list.append(pipe_down)

	# Event loop
	start_count = False
	count = 0
	moves = []
	def play():
		nonlocal pipe_down_list
		nonlocal pipe_up_list

		score = 0
		learningRate = 0.1
		start_count = False
		count = 0
		while 1:
			# print("here")
			screen.fill((255,255,255))
			if count == 10:
					count = 0
			count+=1

			for bird in bird_list:
				if not bird.die:
					bird.fitness += 0.01
			for event in pygame.event.get():

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						for bird in bird_list:
							print("\n\n\n\n")
							print(bird.alpha)
							print("\n")
							print(bird.beta)
					if event.key == pygame.K_SPACE:
						print("presed")
						for bird in bird_list:
							bird.restart()
						for i in range(4):
							pipe_up_height = random.randint(50,250)
							pipe_down_height = height-90-pipe_up_height
							pipe_up = Pipe_up(width,height,i*200,pipe_up_height)
							pipe_down = Pipe_down(width,height,i*200,pipe_down_height)
							new_pipe_up_list.append(pipe_up)
							new_pipe_down_list.append(pipe_down)
							pipe_up_list.append(pipe_up)
							pipe_down_list.append(pipe_down)

			playing = False

			for bird in bird_list:
				if not bird.die:
					playing = True

			if playing:
				# print(len(bird_list))
				for bird in bird_list:
					if not bird.die:

						if count == 10:
							hor_dis = pipe_down_list[0].x - bird.x + bird.width
							vert_dis = pipe_down_list[0].pipe_height - bird.y + 45
							print(vert_dis)
							temp = [(vert_dis),(hor_dis)]
							x = np.asarray(temp)
							o = NNForward(x,bird.alpha,bird.beta)
							# print("alpha shape", bird.alpha.shape)
							# print("beta shape", bird.beta.shape)
							# print(bird.beta)
							yHat = o.yHat
							print(np.max(yHat))
							print(yHat)
							# argMax = np.argmax(yHat)
							if yHat[1] >= 0.5:
								# y = np.array([1,0])
								print("bird", bird.prio, "wants to jump")
								bird.vy -= 10
							# else:
								# y = np.array([0,1])
						bird.update()

						pipe_down_hit = pygame.sprite.spritecollide(bird, pipe_down_list,False,pygame.sprite.collide_mask)
						pipe_up_hit = pygame.sprite.spritecollide(bird, pipe_up_list,False,pygame.sprite.collide_mask)
						if pipe_down_hit or pipe_up_hit:
							bird.fitness -= abs(bird.y - pipe_down_list[0].pipe_height) * 0.05
							bird.die = True
				for i in range(4):
					pipe_down = pipe_down_list[i]
					pipe_up = pipe_up_list[i]
					pipe_down.update()
					pipe_up.update()
					if (pipe_up.x == -50):

						pipe_up_height = random.randint(50,250)
						pipe_down_height = height-90-pipe_up_height
						new_x = pipe_up_list[3].x + 200 - width + 50
						pipe_up = Pipe_up(width,height,new_x,pipe_up_height)
						pipe_down = Pipe_down(width,height,new_x,pipe_down_height)
						pipe_up_list.append(pipe_up)
						pipe_down_list.append(pipe_down)
						score +=1

				if len(pipe_up_list) > 4:
					pipe_up_list.pop(0)
					pipe_down_list.pop(0)

			else:
				#choose 2 parents for genetic algorithm
				fitness_list = []
				for bird in bird_list:
					fitness_list.append((bird.fitness,bird))
				sorted_list = sorted(fitness_list, key=lambda tup: tup[1])
				max_1 = (sorted_list[-1])[1]
				max_2 = (sorted_list[-2])[1]
				mutated_offsprings = make_crossover(max_1,max_2)
				# mutated_offsprings = apply_mutation(offsprings)
				pipe_down_list = []
				pipe_up_list = []
				for i in range(4):
					pipe_up_height = random.randint(50,250)
					pipe_down_height = height-90-pipe_up_height
					pipe_up = Pipe_up(width,height,i*200,pipe_up_height)
					pipe_down = Pipe_down(width,height,i*200,pipe_down_height)
					new_pipe_up_list.append(pipe_up)
					new_pipe_down_list.append(pipe_down)
					pipe_up_list.append(pipe_up)
					pipe_down_list.append(pipe_down)
				for bird in bird_list:
					bird.restart()

				count = 0
				for bird in bird_list:
					bird.alpha = mutated_offsprings[count][0]
					bird.beta = mutated_offsprings[count][1]
					count += 1
			for i in range(4):
				pipe_up = pipe_up_list[i]
				screen.blit(pipe_up.image,(pipe_up.x,pipe_up.y))
				pipe_down = pipe_down_list[i]
				screen.blit(pipe_down.image,(pipe_down.x,pipe_down.y))
			for bird in bird_list:
				if not bird.die:
					screen.blit(bird.image,(bird.x,bird.y))
			pygame.display.update()

	play()









if __name__ == '__main__':
	main()
