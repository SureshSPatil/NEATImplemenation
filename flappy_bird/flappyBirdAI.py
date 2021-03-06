#Author: Suresh Patil
#Date: 07/20/2019

import random, math

global edgeDict
edgeDict = []

def sigmoid(x):
	if x > 300:
		return 1
	elif x < -300:
		return 0
	return (1/(1 + round(math.pow(math.e, -x), 5)))

class Organism():
	def __init__(self, numInputNodes, numOutputNodes):
		# self.inputNodes = inputNodes
		self.numInputNodes = numInputNodes
		self.numOutputNodes = numOutputNodes
		self.nodes = [i for i in range(0, numInputNodes + numOutputNodes)]
		self.edges = {}
		self.fitness = -1

	def addEdge(self, sequence, weight):
		if sequence not in edgeDict:
			edgeDict.append(sequence)
		self.edges[edgeDict.index(sequence)]  = [weight, 1]

	def disableEdge(self, iD):
		self.edges[iD][1] = 0

	def addNode(self, iD, sequence, weightPrev, weightNext):
		self.disableEdge(iD)
		newNode = len(self.nodes)
		self.nodes.append(newNode)
		self.addEdge([sequence[0], newNode], weightPrev)
		self.addEdge([newNode, sequence[1]], weightNext)

	def forwardPropHelper(self, inputNodes, curNodeId):
		if curNodeId in self.nodes[0: self.numInputNodes]:
			return inputNodes[curNodeId]

		prevEdges = []

		for idx in self.edges:
			if edgeDict[idx][1] == curNodeId and edgeDict[idx][0] < curNodeId:
				prevEdges.append(idx) 

		# for idx, edg in enumerate(edgeDict):
		# 	if edg[1] == curNodeId:
		# 		if idx in self.edges:
		# 			prevEdges.append(idx)

		layerSum = 0
		# print(prevEdges)
		for idx in prevEdges:
			layerSum += self.forwardPropHelper(inputNodes, edgeDict[idx][0])*float(self.edges[idx][0])*float(self.edges[idx][1])
		# print(layerSum, edgeDict[idx])
		# print(' ')
		return sigmoid(layerSum)

	def forwardProp(self, inputNodes):
		NNoutput = []
		for outputNode in range(self.numInputNodes, self.numInputNodes + self.numOutputNodes):
			NNoutput.append(self.forwardPropHelper(inputNodes, outputNode))

		return NNoutput

def crossbreed(organism1, organism2):

	if len(organism1.edges.keys()) == 0 and len(organism2.edges.keys()) == 0:
		newOrg = Organism(organism2.numInputNodes, organism2.numOutputNodes)
		return newOrg		


	elif len(organism1.edges.keys()) == 0:
		newOrg = Organism(organism2.numInputNodes, organism2.numOutputNodes)
		newOrg.edges = organism2.edges.copy()
		return newOrg

	elif len(organism2.edges.keys()) == 0:
		newOrg = Organism(organism1.numInputNodes, organism1.numOutputNodes)
		newOrg.edges = organism1.edges.copy()
		return newOrg

	maxOrg1 = max(list(organism1.edges.keys()))
	maxOrg2 = max(list(organism2.edges.keys()))

	if organism1.fitness > organism2.fitness:
		relevantEdges = maxOrg1 + 1
	else:
		relevantEdges = maxOrg2 + 1

	crossBredEdges = {}
	for i in range(0, relevantEdges):
		if (i in organism1.edges.keys()) and (i in organism2.edges.keys()):
			if random.randint(0, 1):
				crossBredEdges[i] = organism1.edges[i][:]
			else:
				crossBredEdges[i] = organism2.edges[i][:]

		elif (i in organism1.edges.keys()):
			crossBredEdges[i] = organism1.edges[i][:]

		elif (i in organism2.edges.keys()):
			crossBredEdges[i] = organism2.edges[i][:]

	newOrg = Organism(organism1.numInputNodes, organism1.numOutputNodes)
	newOrg.edges = crossBredEdges
	return newOrg

def cross(newPool, population):
	newGen = []
	for i in range(0, population):
		r1 = random.randint(0, len(newPool) - 1)
		r2 = random.randint(0, len(newPool) - 1)
		newGen.append(crossbreed(newPool[r1], newPool[r2]))
	return newGen

def selection(oldGen, population):
	#Determine Sorting methodology (sortedOldGen = sort(oldGen, fitness))
	# sortedOldGen = oldGen # REPLACE THIS

	# print([org.fitness for org in oldGen])

	sortedOldGen = sorted(oldGen, key=lambda x: x.fitness, reverse=True)

	newGen = []
	newGen.append(sortedOldGen[0])
	newPool = sortedOldGen[0:len(sortedOldGen)//2]

	# print(newPool[0])
	# print(newPool[1])
	# print([org.fitness for org in newPool])

	sumOfPool = sum([org.fitness for org in newPool])

	for i in range(0, int((population - 1)/4 + 0.5)):
		#conside replacing to representative prob
		rand = random.random()
		x = 0
		count = 0
		while x < rand:
			x += newPool[count].fitness/sumOfPool
			count += 1

		# newIdx = int( (random.random()) * len(newPool))
		newGen.append(newPool[count - 1])
		# newGen.append(newPool[random.randint(0,len(newPool) - 1)])

	newGen += cross(newPool, int((population - 1)*3/4 + 0.5))
	return newGen

def mutate_enable_disable(org):
	specEdges = list(org.edges.keys())
	idx = specEdges[random.randint(0, len(specEdges) - 1)]

	org.edges[idx][1] = 1 - org.edges[idx][1]


def mutate_weight_shift(org):
	specEdges = list(org.edges.keys())
	idx = specEdges[random.randint(0, len(specEdges) - 1)]

	org.edges[idx][0] *= random.uniform(0, 2)


def mutate_weight_random(org):
	specEdges = list(org.edges.keys())
	idx = specEdges[random.randint(0, len(specEdges) - 1)]

	org.edges[idx][0] = random.uniform(-2, 2)

def mutate_link(org):
	# print((org.numInputNodes + org.numOutputNodes))
	initialLinks = org.nodes[0:org.numInputNodes] + org.nodes[(org.numInputNodes + org.numOutputNodes):len(org.nodes)]
	initialNode = initialLinks[random.randint(0, len(initialLinks) - 1)]

	if initialNode < org.numInputNodes:
		finalLinks = org.nodes[org.numInputNodes:len(org.nodes)]
	else:
		finalLinks = org.nodes[org.numInputNodes:org.numInputNodes + org.numOutputNodes] + org.nodes[initialNode + 1:len(org.nodes)]

	finalNode = finalLinks[random.randint(0, len(finalLinks) - 1)]

	org.addEdge([initialNode, finalNode], random.uniform(-2, 2))

def mutate_node(org):
	nextNodePoss = org.nodes[org.numInputNodes:org.numInputNodes + org.numOutputNodes]
	nextNode = nextNodePoss[random.randint(0, len(nextNodePoss) - 1)]

	prevEdges = []
	for idx in org.edges:
		if edgeDict[idx][1] == nextNode:
			prevEdges.append(idx)

	prevEdge = prevEdges[random.randint(0, len(prevEdges) - 1)]
	prevNode = edgeDict[prevEdge][0]

	org.addNode(prevEdge, [prevNode, nextNode], 1, random.uniform(-2, 2))

def mutate(newGen, percentage):
	mutatedGen = []
	mutated = []
	newGenIndices = [i for i in range(0, len(newGen))]

	for i in range(0, int(len(newGen)*percentage)):
		remaining = list(set(newGenIndices) - set(mutated))
		idx = remaining[random.randint(0, len(remaining) - 1)]
		nextMutant = newGen[idx]

		if len(nextMutant.edges) == 0:
			mutate_link(nextMutant)
			mutatedGen.append(nextMutant)
			mutated.append(idx)
		else:
			typ = random.randint(0, 4)

			if typ == 0:
				mutate_link(nextMutant)
				mutatedGen.append(nextMutant)
				mutated.append(idx)				
			elif typ == 1:
				mutate_node(nextMutant)
				mutatedGen.append(nextMutant)
				mutated.append(idx)						
			elif typ == 2:
				mutate_enable_disable(nextMutant)
				mutatedGen.append(nextMutant)
				mutated.append(idx)	
			elif typ == 3:
				mutate_weight_shift(nextMutant)
				mutatedGen.append(nextMutant)
				mutated.append(idx)
			elif typ == 4:
				mutate_weight_random(nextMutant)
				mutatedGen.append(nextMutant)
				mutated.append(idx)

	for i in list(set(newGenIndices) - set(mutated)):
		mutatedGen.append(newGen[i])

	return mutatedGen

import pygame

pygame.init()

winWidth = 370
winHeight = 540

population = 100

gameHeight = 511

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("fLaPpY bIrD")

bird = pygame.image.load('bird.png')
bg = pygame.image.load('background.png')




def createPipes():
	pipeHeight = random.randint(1, 7) * 50
	coords = [[winWidth, 0, 50, pipeHeight], [winWidth, pipeHeight + 100, 50, gameHeight - (pipeHeight + 100)]]
	return coords

score = 0
oldScore = 0

def reset(x, y, birds, pipes, actionPipeIndex):
	x = int(winWidth/2) - 20
	y = int(winHeight/2)
	birds = [[x, y, 0] for i in range(0, population)]
	pipes = [createPipes()]
	actionPipeIndex = 0
	return x, y, birds, pipes, actionPipeIndex


x = int(winWidth/2) - 20
y = int(winHeight/2)
birds = [[x, y, 0] for i in range(0, population)]
pipes = [createPipes()]
actionPipeIndex = 0

orgs = [Organism(4, 1) for i in range(0, population)]

pipeVel = -5
width = 30
height = 23
vertVel = 0
jumpVel = -15
deltaTime = 100
fallingVel = 5

def doOverlap(r1, r2):

    if (r1[0] > r2[0] + r2[2] or r2[0] > r1[0] + r1[2]):
        return False; 

    if (r1[1] > r2[1] + r2[3] or r2[1] > r1[1] + r1[3]):
        return False; 
  
    return True; 


def redrawGameWindow():
	# win.fill((135, 206, 235))
	win.blit(bg, (0, 0))

	for brd in birds:
		win.blit(bird, (brd[0], brd[1]))
	# pygame.draw.rect(win, (0, 0, 0), (x, y, width, height), 2)

	for pipe in pipes:
		pygame.draw.rect(win, (0, 255, 0), pipe[0])
		pygame.draw.rect(win, (0, 255, 0), pipe[1])

	font = pygame.font.Font('freesansbold.ttf', 12) 
	text = font.render('Score: ' + str(score), True, (255, 255, 255)) 
	textRect = text.get_rect()   
	textRect.center = (winWidth // 2, winHeight // 8) 

	win.blit(text, textRect)

	pygame.display.update()


run = True
generationCount = 0
while run:
	print('Generation:', generationCount)
	distance = 0
	birdsIn = [i for i in range (0, population)]

	while run and (len(birdsIn) > 0):
		pygame.time.delay(deltaTime)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

	# 	keys = pygame.key.get_pressed()

	# 	# if keys[pygame.K_LEFT]:
	# 	# 	x -= vel
	# 	# if keys[pygame.K_RIGHT]:
	# 	# 	x += vel
	# 	# if keys[pygame.K_DOWN]:
	# 	# 	y += vel
		for i, brd in enumerate(birds):
		#	BIRD SPECIFIC 
		# 	if keys[pygame.K_UP]:
		# 		vertVel = jumpVel
			# print(edgeDict)
			# print(orgs[i].edges)
			oVal = orgs[i].forwardProp([pipes[actionPipeIndex][0][0] + 50 - (brd[0] + width), pipes[actionPipeIndex][0][3] - (brd[1]), brd[2], pipes[actionPipeIndex][1][1] - (brd[1] + height)])
			if oVal[0] >= 0.5:
				brd[2] = jumpVel

		# 	y += vertVel
		# 	vertVel += fallingVel

			brd[1] += brd[2]
			brd[2] += fallingVel

			if brd[1] < 0 and i in birdsIn:
				# orgs[i].fitness += -3*(brd[1] - (pipes[actionPipeIndex][0][3] + 50)) + distance
				orgs[i].fitness = distance
				birds[i][0] = -100
				birdsIn.remove(i)
				continue
			elif brd[1] > gameHeight - height and i in birdsIn:
				# orgs[i].fitness += -3*(brd[1] - (pipes[actionPipeIndex][0][3] + 50)) + distance
				orgs[i].fitness = distance
				birds[i][0] = -100
				birdsIn.remove(i)
				continue

			if len(pipes) > 1 and i in birdsIn:
				if doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex-1][0]) or doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex-1][1]) or doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex][0]) or doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex][1]):
					# orgs[i].fitness += -3*(brd[1] - (pipes[actionPipeIndex][0][3] + 50)) + 10*distance
					orgs[i].fitness = distance
					birds[i][0] = -100
					birdsIn.remove(i)
					continue
			else:
				if doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex][0]) or doOverlap((brd[0], brd[1], width, height), pipes[actionPipeIndex][1])  and i in birdsIn:
					# orgs[i].fitness += -3*(brd[1] - (pipes[actionPipeIndex][0][3] + 50)) + 10*distance
					orgs[i].fitness = distance
					birds[i][0] = -100
					birdsIn.remove(i)
					continue	

		

		if pipes[actionPipeIndex][0][0] == winWidth//2 - 50:
			score += 1
		if pipes[actionPipeIndex][0][0] < winWidth//2 - 75:
			actionPipeIndex += 1 



	# 	# win.fill((135, 206, 235))
	# 	# pygame.draw.circle(win, (255, 255, 0), (x, y), 10)
	# 	# pygame.display.update()


		for pipe in pipes:
			pipe[0][0] += pipeVel
			pipe[1][0] += pipeVel

		distance += 1

		if pipes[-1][0][0] <= winWidth - 200:
			pipes.append(createPipes()) 
		if pipes[0][0][0] <= -50:
			pipes.pop(0)
			actionPipeIndex -= 1

		redrawGameWindow()

	newGen = selection(orgs, len(orgs))
	# fitnesses = []
	# for org in newGen:
	# 	fitnesses.append(org.fitness)
	mutatedGen = [newGen[0]] + mutate(newGen[1:len(newGen)], 0.15)
	orgs = mutatedGen
	for org in orgs:
		org.fitness = -1
	# print(fitnesses)
	print("Max Score for Generation:", score)
	oldScore = score
	score = 0
	distance = 0

	x, y, birds, pipes, actionPipeIndex = reset(x, y, birds, pipes, actionPipeIndex)
	generationCount += 1

	# 	# print((x, y, width, height), pipes[actionPipeIndex][1], actionPipeIndex)

# pygame.quit()

# org = Organism(2, 1)
# # print(org.nodes)
# org.addEdge([0, 2], 2)
# # org.addEdge([1, 2], 2)
# # print(org.edges)
# # print(edgeDict)
# # print(org.forwardProp([1, 1]))

# # org.addNode(0, edgeDict[0], 0, -4)
# # org.fitness = 1

# print(org.edges)
# print(edgeDict)

# mutate_weight_shift(org)


# print(org.edges)
# print(edgeDict)

# orgList = []
# for x in range(0, 5):
# 	newOrg = Organism(2, 1)
# 	newOrg.fitness = random.randint(0, 5)
# 	orgList.append(newOrg)

# print([org.fitness for org in orgList])
# newlist = sorted(orgList, key=lambda x: x.fitness, reverse=True)
# print([org.fitness for org in newlist])

# print(org.forwardProp([1, 1]))
# print(sigmoid(0))

# org2 = Organism(2, 1)
# # # print(org.nodes)
# org2.addEdge([0, 2], 2)
# org2.addEdge([1, 2], 2)

# print(org.edges)
# print(edgeDict)

# mutate_link(org)

# print(org.edges)
# print(edgeDict)
# mutate_node(org)

# print(org.edges)
# print(edgeDict)

# # print(org.edges)
# # print(edgeDict)
# # print(org.forwardProp([1, 1]))

# # org2.addNode(0, edgeDict[0], 0, -4)
# newOrg = crossbreed(org, org2)
# print(org.edges)
# print(org2.edges)
# print(newOrg.edges)
