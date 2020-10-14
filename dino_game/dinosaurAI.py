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
		self.fitness = 0

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

#FIXME
def tournamentSelect(oldGen, population):
	return 5

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
	prevEdges = []
	while len(prevEdges) == 0:
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

winWidth = 900
winHeight = 250

population = 100

gameHeight = 200

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Dino Run")

rexL = pygame.image.load('rexL.png')
rexR = pygame.image.load('rexR.png')
rexDuckL = pygame.image.load('rexDuckL.png')
rexDuckR = pygame.image.load('rexDuckR.png')
rexJump = pygame.image.load('rexJump.png')
rexGameOver = pygame.image.load('rexGameOver.png')

bg = pygame.image.load('background.png')

cactiDict = [pygame.image.load('cactus0.png'), pygame.image.load('cactus1.png'), pygame.image.load('cactus2.png'), pygame.image.load('cactus3.png')]
pteroDict = [pygame.image.load('pteroU.png'), pygame.image.load('pteroD.png')]


score = 0

def createObstacle():
	offShift = random.randint(1, 10)*(30*(1 + score/500))

	cactiType = random.randint(0, 6)
	if cactiType == 0:
		cactus = [winWidth + offShift, gameHeight - 45, winWidth + 30 + offShift, gameHeight, cactiType,cactiDict[0], 0]
	elif cactiType == 1:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 40 + offShift, gameHeight, cactiType,cactiDict[1], 0]
	elif cactiType == 2:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 60 + offShift, gameHeight, cactiType,cactiDict[2], 0]
	elif cactiType == 3:
		cactus = [winWidth + offShift, gameHeight - 38, winWidth + 85 + offShift, gameHeight, cactiType,cactiDict[3], 0]
	elif cactiType == 4 and score > 0:
		# addHeight = 40 * random.randint(1, 3)
		cactus = [winWidth + offShift, gameHeight - 40, winWidth + 50 + offShift, gameHeight, cactiType,pteroDict[0], pteroDict[1], 1]
	elif cactiType == 5 and score > 0:
		cactus = [winWidth + offShift, gameHeight - 80, winWidth + 50 + offShift, gameHeight - 80 + 30, cactiType,pteroDict[0], pteroDict[1], 1]
	elif cactiType == 6 and score > 0:
		cactus = [winWidth + offShift, gameHeight - 120, winWidth + 50 + offShift, gameHeight - 120 + 30, cactiType,pteroDict[0], pteroDict[1], 1]

	else:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 60 + offShift, gameHeight, cactiType ,cactiDict[2], 0]

	return cactus


cacti = [createObstacle()]
actionCactusIndex = 0
cactiVel = -40

width = 50
height = 50
duckHeight = 30
vertVel = 0
jumpVel = (5/4)*cactiVel
fallingVel = cactiVel/(-4)

x = int(winWidth/10)
y = 150

dinoHitBoxes = []
dinosaurs = []
for i in range(0, population):
	dinosaurs.append([x, y, False, 0])
	dinoHitBoxes.append([[[int(winWidth/10), y], [int(winWidth/10) + 30, y + height], [int(winWidth/10) + 30, y], [int(winWidth/10) + width, y - 29 + height]], [[int(winWidth/10), y - duckHeight + height], [int(winWidth/10) + width + 10, y + height]]])



runParity = 0
gameOver = False

def doOverlap(l1, r1, l2, r2):
	if (l1[0] > r2[0] or l2[0] > r1[0]):
		return False
	if (l1[1] > r2[1] or l2[1] > r1[1]):
		return False
	# print(l1, r1, l2, r2)
	return True

generationCount = 0

def redrawGameWindow():
	# win.fill((135, 206, 235))
	win.blit(bg, (0, 0))

	# if gameOver:
	# 	win.blit(rexGameOver, (x, y))

	for dinosaur in dinosaurs:
		if dinosaur[1] < gameHeight - height:
			win.blit(rexJump, (dinosaur[0], dinosaur[1]))
		elif dinosaur[2]:
			if runParity:
				win.blit(rexDuckR, (dinosaur[0], dinosaur[1]))
			else:
				win.blit(rexDuckL, (dinosaur[0], dinosaur[1]))
		elif runParity:
			win.blit(rexR, (dinosaur[0], dinosaur[1]))
		else:
			win.blit(rexL, (dinosaur[0], dinosaur[1]))

	for cact in cacti:
		if cact[-1]:
			if runParity:
				win.blit(cact[-2], (cact[0], cact[1]))
			else:
				win.blit(cact[-3], (cact[0], cact[1]))
		else:
			win.blit(cact[-2], (cact[0], cact[1]))

	# pygame.draw.rect(win, (0, 0, 0),(cacti[actionCactusIndex][0], cacti[actionCactusIndex][1], cacti[actionCactusIndex][2] - cacti[actionCactusIndex][0], cacti[actionCactusIndex][3] - cacti[actionCactusIndex][1]), 2)

	font = pygame.font.Font('freesansbold.ttf', 12) 
	text = font.render( 'Generation: ' + str(generationCount) + ' ' + 'Score: ' + str(score), True, (255, 255, 255)) 
	textRect = text.get_rect()   
	textRect.center = (8*(winWidth // 10), winHeight // 8) 

	win.blit(text, textRect)

	pygame.display.update()

deltaTime = 100
run = True

orgs = [Organism(5, 3) for i in range(0, population)]


while run:
	cactiVel = -20
	jumpVel = -25
	fallingVel = 5


	cactiPassed = 0
	print("Generation:", generationCount)
	dinosaurIndices = [i for i in range(0, population)]
	jumps = [1 for i in range(0, population)]
	typesMastered = [set() for i in range(0, population)]

	while run and len(dinosaurIndices) > 0:
		
		pygame.time.delay(deltaTime)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False


		for i, dinosaur in enumerate(dinosaurs):

			if i in dinosaurIndices:
				oVal = orgs[i].forwardProp([cacti[actionCactusIndex][0] - dinosaur[0], cacti[actionCactusIndex][2] - cacti[actionCactusIndex][0], (gameHeight - cacti[actionCactusIndex][3]) - duckHeight, cacti[actionCactusIndex][3] - cacti[actionCactusIndex][1], cactiVel])

				if oVal.index(max(oVal)) == 0 and dinosaur[1] == gameHeight - height:
					dinosaur[3] = jumpVel
					jumps[i] += 1
					dinosaur[2] = False
				elif oVal.index(max(oVal)) == 1 and dinosaur[1] >= gameHeight - height:
					dinosaur[1] = gameHeight - duckHeight
					dinosaur[2] = True
				else:
					dinosaur[2] = False

				dinosaur[1] += dinosaur[3]
				dinosaur[3] += fallingVel


				if dinosaur[2] and dinosaur[1] >= gameHeight - duckHeight:
					vertVel = 0
					dinosaur[1] = gameHeight - duckHeight
				
				if (not dinosaur[2]) and dinosaur[1] >= gameHeight - height:
					vertVel = 0
					dinosaur[1] = gameHeight - height


				dinoHitBoxes[i] = [[[int(winWidth/10), dinosaur[1]], [int(winWidth/10) + 30, dinosaur[1] + height], [int(winWidth/10) + 30, dinosaur[1]], [int(winWidth/10) + width, dinosaur[1] - 29 + height]], [[int(winWidth/10), dinosaur[1] - duckHeight + height], [int(winWidth/10) + width + 10, dinosaur[1] + height]]]

				if dinosaur[2] and dinosaur[0] > 0:
						# print(dinoHitBoxes[1][0], dinoHitBoxes[1][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3]))
					if doOverlap(dinoHitBoxes[i][1][0], dinoHitBoxes[i][1][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])):
							# cactiVel = 0
							# jumpVel = 0
							# fallingVel = 0
							# gameOver = True
							# run = False
						orgs[i].fitness = len(typesMastered[i]) + ((score - jumps[i])/500)
						dinosaurIndices.remove(i)
						dinosaur[0] = -6000


				elif dinosaur[0] > 0:
					if doOverlap(dinoHitBoxes[i][0][0], dinoHitBoxes[i][0][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])) or doOverlap(dinoHitBoxes[i][0][2], dinoHitBoxes[i][0][3], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])):
							# cactiVel = 0
							# jumpVel = 0
							# fallingVel = 0
							# gameOver = True
							# run = False
						orgs[i].fitness = len(typesMastered[i]) + ((score - jumps[i])/500)
						dinosaurIndices.remove(i)
						dinosaur[0] = -6000

		prevActionI = actionCactusIndex

		if cacti[actionCactusIndex][0] < (int(winWidth/10) - (cacti[actionCactusIndex][2] - cacti[actionCactusIndex][0])) - width:
			if cacti[actionCactusIndex][-1]:
				if cacti[actionCactusIndex][-4] not in typesMastered[i]:
					typesMastered[i].add(cacti[actionCactusIndex][-4])
			elif cacti[actionCactusIndex][-3] not in typesMastered[i]:
				typesMastered[i].add(cacti[actionCactusIndex][-3])
			actionCactusIndex += 1 	

		for cact in cacti:
			cact[0] += cactiVel
			cact[2] += cactiVel

		# if actionCactusIndex - prevActionI > 0 or cacti[-1][0] <= winWidth - ((cactiVel)**2):
		if cacti[-1][0] < winWidth//3:
			cacti.append(createObstacle()) 

		if cacti[0][0] <= -((cactiVel)**2):
			cacti.pop(0)
			actionCactusIndex -= 1		


		redrawGameWindow()
		# print(cactiVel)
		runParity = (1+runParity)%2
		if score/50 == score//50:
			# print('here')
			oldCactiVel = cactiVel
			cactiPassed += 1
			cactiVel += -1
			jumpVel = (cactiVel/oldCactiVel)*jumpVel
			fallingVel = (cactiVel/oldCactiVel)**2 * fallingVel
			
			# jumpVel += -1
			# fallingVel = abs(cactiVel)/4

		score += 1

	newGen = selection(orgs, len(orgs))
	# fitnesses = []
	# for org in newGen:
	# 	fitnesses.append(org.fitness)
	mutatedGen = [newGen[0]] + mutate(newGen[0:len(newGen) - 1], 0.05)
	orgs = mutatedGen
	for org in orgs:
		org.fitness = 0
	# print(fitnesses)
	print("Max Score for Generation:", score)
	dinoHitBoxes = []
	score = 0
	dinosaurs = []
	cacti = [createObstacle()]
	actionCactusIndex = 0
	for i in range(0, population):
		dinosaurs.append([x, y, False, 0])
		dinoHitBoxes.append([[[int(winWidth/10), y], [int(winWidth/10) + 30, y + height], [int(winWidth/10) + 30, y], [int(winWidth/10) + width, y - 29 + height]], [[int(winWidth/10), y - duckHeight + height], [int(winWidth/10) + width + 10, y + height]]])

	generationCount += 1

print(orgs[0].edges)
print(edgeDict)
