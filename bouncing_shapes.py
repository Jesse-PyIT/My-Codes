#First Game in Python
import pygame, sys
pygame.init()
gameDisplay = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Racer Race')

white = (255, 255, 255)
magenta = (255, 0, 255)
clock = pygame.time.Clock()
#above is standard start of pygame programs

crashed = False
green_rect = pygame.Rect(400, 100, 150, 150)
blue_rect = pygame.Rect(200, 100, 150, 150)
x, y = 0, 0
xy = 650
xchange = 2
schange = -2
cchange = 2
xx, yy = 650, 450
xc, yc = 400, int(gameDisplay.get_height()/2)
while not crashed:
    xrs = ((x+150),0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True



    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, (0, 255, 0), [x, y, 150, 150])
    pygame.draw.rect(gameDisplay, (0, 0, 255), [xx, yy, 150, 150])
    pygame.draw.circle(gameDisplay, magenta, (xc, yc), 75)

    x += xchange
    xx += schange
    xc += cchange

    if x > 800 - 150:
        xchange = -xchange
    if x < 0:
        xchange = -xchange

    if xx < 0:
        schange = -schange
    if xx > 800-150:
        schange = -schange

    if xc > 800-75:
        cchange = -cchange
    if xc < 75:
        cchange = -cchange
    pygame.display.update()

    #updates one thing
    #pygame.display.flip() updates whole surface
    clock.tick(60)

pygame.quit()

#Basic "Template" for pygame
