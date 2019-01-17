import pygame, sys, math

width = 1024
height = 720
radius = 300.0
goblin = 0.0
boatx = 0.1
boaty = 0.0
bspeed = 1.0
gspeeds = [3.5, 4.0, 4.2, 4.4, 4.6]
gspeed_ix = 0
speed_mult = 3.0
clicking = False
actual_level = 1

def restart():
	global goblin, boatx, boaty, clicking, actual_level
	goblin = 0.0
	boatx = 0.1
	boaty = 0.0
	clicking = False
	actual_level = 1

pygame.init()
window = pygame.display.set_mode((width, height))

def clear():
	radius_mult = bspeed / gspeeds[gspeed_ix]

	window.fill((0,80,0))
	pygame.draw.circle(window, (0,0,128), (int(width/2), int(height/2)), int(radius*1.00), 0)
	pygame.draw.circle(window, (200,200,200), (int(width/2), int(height/2)), int(radius*radius_mult), 1)

def redraw(draw_text=False,win=False):
	clear()

	pygame.draw.circle(window, (255,255,255), (int(width/2 + boatx),int(height/2 + boaty)), 6, 2)
	pygame.draw.circle(window, (255,0,0), (int(width/2 + radius*math.cos(goblin)),int(height/2 + radius*math.sin(goblin))), 6, 0)

	if draw_text:
		font = pygame.font.Font(None, 72)
		if win:
			text = font.render("Escaped!", 1, (255, 255, 255))
		else:
			text = font.render("You Were Eaten", 1, (255, 0, 0))
		textpos = text.get_rect()
		textpos.centerx = window.get_rect().centerx
		textpos.centery = height/2
		window.blit(text, textpos)

	font = pygame.font.Font(None, 48)
	text = font.render("Goblin Speed: " + str(gspeeds[gspeed_ix]), 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = width/2
	textpos.centery = height - 20
	window.blit(text, textpos)

	pygame.display.flip()

def updateGoblin():
	global goblin
	gspeed = gspeeds[gspeed_ix]
	newang = math.atan2(boaty, boatx)
	diff = newang - goblin
	if diff < math.pi: diff += math.pi*2.0
	if diff > math.pi: diff -= math.pi*2.0
	if abs(diff)*radius <= gspeed * speed_mult:
		goblin = newang
	else:
		goblin += gspeed * speed_mult / radius if diff > 0.0 else -gspeed * speed_mult / radius
	if goblin < math.pi: goblin += math.pi*2.0
	if goblin > math.pi: goblin -= math.pi*2.0

def moveBoat(x,y):
	global boatx, boaty
	dx = x - boatx
	dy = y - boaty
	mag = math.sqrt(dx*dx + dy*dy)
	if mag <= bspeed * speed_mult:
		boatx = x
		boaty = y
	else:
		boatx += bspeed * speed_mult * dx/mag
		boaty += bspeed * speed_mult * dy/mag

def detectWin():
	global gspeed_ix
	global actual_level
	if boatx*boatx + boaty*boaty > radius*radius:
		diff = math.atan2(boaty, boatx) - goblin
		if diff < math.pi: diff += math.pi*2.0
		if diff > math.pi: diff -= math.pi*2.0
		while True:
			is_win = abs(diff) > 0.000001
			redraw(True, is_win)
			events = [event.type for event in pygame.event.get()]
			if pygame.QUIT in events:
				sys.exit(0)
			elif pygame.MOUSEBUTTONDOWN in events:
				restart()
				if is_win:
					gspeed_ix += 1
					actual_level += 1
				break

clock = pygame.time.Clock()
clear()
while True:
	x = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		clicking = pygame.mouse.get_pressed()[0]
		if pygame.mouse.get_pressed()[2]:
				restart()

	if clicking:
		x,y = pygame.mouse.get_pos()
		moveBoat(x - width/2, y - height/2)
	updateGoblin()
	detectWin()
	if actual_level == len(gspeeds):
		break
	redraw()
	clock.tick(60)
sys.exit(0)
