#this is procedural

import sys
import csv
import random
import numpy as np


class obj():
	def __init__(self,x,a,z,b,yHat,J):
		self.x = x
		self.a = a
		self.z = z
		self.b = b
		self.yHat = yHat
		self.J = J




def NNForward(x,y,alpha,beta):
	# print("Forward")
	a = np.array(np.dot(alpha,x)).flatten()
	z = 1 / (1 + (np.exp(-a)))
	z = np.append([1],z)
	# print(z.shape)
	b = np.array(np.dot(beta,z)).flatten()
	yHat = np.array(np.exp(b) / np.sum(np.exp(b))).flatten()
	J = -1 * np.dot(y.transpose(),np.log(yHat))
	# print(J)
	o = obj(x,a,z,b,yHat,J)
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
	

#fuck everything 
def SGD(trainingData, testData, epochs, hidden,paramDetail,learningRate):
	oneData = trainingData[0][0]
	# print(oneData)
	if paramDetail == 1:
		
		alpha = np.zeros((hidden,len(oneData)))
		for i in range(hidden):
			for j in range(len(oneData)):
				if j == 0:
					alpha[i][j] = 0
				else:
					alpha[i][j] = random.uniform(-0.1,0.1)
		beta = np.zeros((10,hidden+1))
		for i in range(10):
			for j in range(hidden+1):
				if j == 0:
					beta[i][j] = 0
				else:
					beta[i][j] = random.uniform(-0.1,0.1)
		#initialize to [-0.1, 0.1], bias is 0
	elif paramDetail == 2:
		
		alpha = np.zeros((hidden,len(oneData)))
		for i in range(hidden):
			alpha[i][0] = 0
		beta = np.zeros((10,hidden+1))
		for i in range(10):
			beta[i][0] = 0
	# print("alpha is ")
	# print(alpha.shape)
	# print("beta is ")
	# print(beta.shape)
	train = []
	test = []
	for i in range(epochs):
		# print("epoch = ",i+1)
		for (x,y) in trainingData:
			o = NNForward(x,y,alpha,beta)#pass parameters
			galpha,gbeta = NNBackward(x,y,alpha,beta,o)
			alpha = alpha - galpha * learningRate
			beta = beta - gbeta * learningRate
			# print(o.J)
		#training done

		crossEntropyTrain = 0
		crossEntropyTest = 0
		for (x,y) in trainingData:
			o = NNForward(x,y,alpha,beta)#pass parameters
			crossEntropyTrain+= o.J
		train.append(crossEntropyTrain/len(trainingData))	
		for (x,y) in testData:
			o = NNForward(x,y,alpha,beta)#pass parameters
			crossEntropyTest+= o.J
		test.append(crossEntropyTest/len(testData))
	return alpha,beta,train,test

def train(trainData,testData,epochs,hiddenUnits,initFlag,learningRate):
	alpha, beta,train,test = SGD(trainData,testData,epochs,hiddenUnits,initFlag,learningRate)
	return alpha, beta,train,test

def prediction(data,alpha,beta):
	total = 0
	incorrect = 0
	labels= [] 
	for (x,y) in data:
		o = NNForward(x,y,alpha,beta)
		yHat = o.yHat
		argMax = np.argmax(yHat)
		labels.append(argMax)
		if y[argMax]!=1:
			incorrect+=1
		total+=1
	return (incorrect/total	, labels)
# 	D = alpha.shape[0]
# 	M = alpha.shape[1]
# 	K = beta.shape[0]
# 	A = np.zeros(D)
# 	for j in range(D):
# 		for m in range(M):


def main():
	trainInput = sys.argv[len(sys.argv)-9]
	testInput = sys.argv[len(sys.argv)-8]
	trainOut = sys.argv[len(sys.argv)-7]
	testOut = sys.argv[len(sys.argv)-6]
	metricsFile = sys.argv[len(sys.argv)-5]
	epochs = sys.argv[len(sys.argv)-4]
	hiddenUnits = sys.argv[len(sys.argv)-3]
	initFlag = sys.argv[len(sys.argv)-2]
	learningRate = sys.argv[len(sys.argv)-1]

	csvFile =  open(trainInput,"r")
	# print(csvFile)
	inputTrain = [] 
	for line in csvFile:
		splitted = line.split(",")
		temp = []
		temp.append(float(1))
		for num in splitted[1:]:
			temp.append(float(num))
		features = np.asarray(temp)
		oneHot = np.zeros(10)
		oneHot[int(splitted[0])] = 1
		inputTrain.append((features,oneHot))
		# print(oneHot.shape)
		# print(features.shape)
	csvFile = open(testInput,"r")
	inputTest = []
	for line in csvFile:
		splitted = line.split(",")
		temp = []
		temp.append(float(1))
		for num in splitted[1:]:
			temp.append(float(num))
		features = np.asarray(temp)
		oneHot = np.zeros(10)
		oneHot[int(splitted[0])] = 1
		inputTest.append((features,oneHot))
	alpha,beta,trainCE,testCE = train(inputTrain,inputTest,int(epochs),int(hiddenUnits),int(initFlag),float(learningRate))
	(trainError, trainLabels) = prediction(inputTrain,alpha,beta)
	(testError, testLabels) = prediction(inputTest,alpha,beta)



