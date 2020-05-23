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
