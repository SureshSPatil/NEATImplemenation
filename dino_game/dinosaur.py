import pygame, random

pygame.init()

winWidth = 900
winHeight = 250

# population = 100

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
	offShift = random.randint(0, 10)*30

	cactiType = random.randint(0, 4)
	if cactiType == 0:
		cactus = [winWidth + offShift, gameHeight - 45, winWidth + 30 + offShift, gameHeight, cactiDict[0], 0]
	elif cactiType == 1:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 40 + offShift, gameHeight, cactiDict[1], 0]
	elif cactiType == 2:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 60 + offShift, gameHeight, cactiDict[2], 0]
	elif cactiType == 3:
		cactus = [winWidth + offShift, gameHeight - 38, winWidth + 85 + offShift, gameHeight, cactiDict[3], 0]
	elif cactiType == 4 and score > 400:
		addHeight = 40 * random.randint(1, 3)
		cactus = [winWidth + offShift, gameHeight - addHeight, winWidth + 50 + offShift, gameHeight - addHeight + 30, pteroDict[0], pteroDict[1], 1]
	else:
		cactus = [winWidth + offShift, gameHeight - 30, winWidth + 60 + offShift, gameHeight, cactiDict[2], 0]

	return cactus


cacti = [createObstacle()]
actionCactusIndex = 0
cactiVel = -20

width = 50
height = 50
duckHeight = 30
vertVel = 0
jumpVel = -25
fallingVel = 5

x = int(winWidth/10)
y = 150

dinoHitBoxes = [[[int(winWidth/10), y], [int(winWidth/10) + 30, y + height], [int(winWidth/10) + 30, y], [int(winWidth/10) + width, y - 29 + height]], [[int(winWidth/10), y - duckHeight + height], [int(winWidth/10) + width + 10, y + height]]]

runParity = 0
gameOver = False
downPressed = False

def doOverlap(l1, r1, l2, r2):
	if (l1[0] > r2[0] or l2[0] > r1[0]):
		return False
	if (l1[1] > r2[1] or l2[1] > r1[1]):
		return False
	# print(l1, r1, l2, r2)
	return True


def redrawGameWindow():
	# win.fill((135, 206, 235))
	win.blit(bg, (0, 0))

	if gameOver:
		win.blit(rexGameOver, (x, y))
	elif y < gameHeight - height:
		win.blit(rexJump, (x, y))
	elif downPressed:
		if runParity:
			win.blit(rexDuckR, (x, y))
		else:
			win.blit(rexDuckL, (x, y))
	elif runParity:
		win.blit(rexR, (x, y))
	else:
		win.blit(rexL, (x, y))

	for cact in cacti:
		if cact[-1]:
			if runParity:
				win.blit(cact[-2], (cact[0], cact[1]))
			else:
				win.blit(cact[-3], (cact[0], cact[1]))
		else:
			win.blit(cact[-2], (cact[0], cact[1]))

	font = pygame.font.Font('freesansbold.ttf', 12) 
	text = font.render('Score: ' + str(score), True, (255, 255, 255)) 
	textRect = text.get_rect()   
	textRect.center = (9*(winWidth // 10), winHeight // 8) 

	win.blit(text, textRect)

	pygame.display.update()

deltaTime = 100
run = True
while run:
	pygame.time.delay(deltaTime)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_UP] and y == gameHeight - height:
		vertVel = jumpVel
		downPressed = False
	elif keys[pygame.K_DOWN] and y >= gameHeight - height:
		y = gameHeight - duckHeight
		downPressed = True
	else:
		downPressed = False

	y += vertVel
	vertVel += fallingVel

	if downPressed and y >= gameHeight - duckHeight:
		vertVel = 0
		y = gameHeight - duckHeight
	
	if (not downPressed) and y >= gameHeight - height:
		vertVel = 0
		y = gameHeight - height


	dinoHitBoxes = [[[int(winWidth/10), y], [int(winWidth/10) + 30, y + height], [int(winWidth/10) + 30, y], [int(winWidth/10) + width, y - 29 + height]], [[int(winWidth/10), y - duckHeight + height], [int(winWidth/10) + width + 10, y + height]]]


	if downPressed:
		# print(dinoHitBoxes[1][0], dinoHitBoxes[1][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3]))
		if doOverlap(dinoHitBoxes[1][0], dinoHitBoxes[1][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])):
			cactiVel = 0
			jumpVel = 0
			fallingVel = 0
			gameOver = True
			run = False

	else:
		if doOverlap(dinoHitBoxes[0][0], dinoHitBoxes[0][1], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])) or doOverlap(dinoHitBoxes[0][2], dinoHitBoxes[0][3], (cacti[actionCactusIndex][0], cacti[actionCactusIndex][1]), (cacti[actionCactusIndex][2], cacti[actionCactusIndex][3])):
			cactiVel = 0
			jumpVel = 0
			fallingVel = 0
			gameOver = True
			run = False

	if cacti[actionCactusIndex][0] < x - 115:
		actionCactusIndex += 1 	

	for cact in cacti:
		cact[0] += cactiVel
		cact[2] += cactiVel

	if cacti[-1][0] <= winWidth - 350:
		cacti.append(createObstacle()) 
	elif cacti[0][0] <= -200:
		cacti.pop(0)
		actionCactusIndex -= 1		


	redrawGameWindow()
	runParity = (1+runParity)%2
	if cactiVel != 0:
		score += 1
	if score == 100:
		cactiVel += -10
		fallingVel = abs(cactiVel)/4
		jumpVel += -10/4