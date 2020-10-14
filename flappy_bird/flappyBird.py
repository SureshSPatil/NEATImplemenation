import pygame, random

pygame.init()

winWidth = 370
winHeight = 540

gameHeight = 511

win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("fLaPpY bIrD")

bird = pygame.image.load('bird.png')
bg = pygame.image.load('background.png')

x = int(winWidth/2) - 20
y = int(winHeight/2)

def createPipes():
	pipeHeight = random.randint(1, 7) * 50
	coords = [[winWidth, 0, 50, pipeHeight], [winWidth, pipeHeight + 75, 50, gameHeight - (pipeHeight + 75)]]
	return coords

score = 0

pipes = [createPipes()]
actionPipeIndex = 0
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
	win.blit(bird, (x, y))
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
while run:
	pygame.time.delay(deltaTime)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()

	# if keys[pygame.K_LEFT]:
	# 	x -= vel
	# if keys[pygame.K_RIGHT]:
	# 	x += vel
	# if keys[pygame.K_DOWN]:
	# 	y += vel

	if keys[pygame.K_UP]:
		vertVel = jumpVel

	y += vertVel
	vertVel += fallingVel

	if y < 0:
		y = 0
	elif y > gameHeight - height:
		y = gameHeight - height
		jumpVel = 0
		pipeVel = 0



	# win.fill((135, 206, 235))
	# pygame.draw.circle(win, (255, 255, 0), (x, y), 10)
	# pygame.display.update()


	for pipe in pipes:
		pipe[0][0] += pipeVel
		pipe[1][0] += pipeVel

	if pipes[-1][0][0] <= winWidth - 150:
		pipes.append(createPipes()) 
	elif pipes[0][0][0] <= -50:
		pipes.pop(0)
		actionPipeIndex -= 1

	if x > pipes[actionPipeIndex][0][0] + 25:
		score += 1
		actionPipeIndex += 1 

	# print((x, y, width, height), pipes[actionPipeIndex][1], actionPipeIndex)

	if len(pipes) > 1:
		if doOverlap((x, y, width, height), pipes[actionPipeIndex-1][0]) or doOverlap((x, y, width, height), pipes[actionPipeIndex-1][1]) or doOverlap((x, y, width, height), pipes[actionPipeIndex][0]) or doOverlap((x, y, width, height), pipes[actionPipeIndex][1]):
			jumpVel = 0
			pipeVel = 0
	else:
		if doOverlap((x, y, width, height), pipes[actionPipeIndex][0]) or doOverlap((x, y, width, height), pipes[actionPipeIndex][1]):
			jumpVel = 0
			pipeVel = 0			

	redrawGameWindow()

pygame.quit()