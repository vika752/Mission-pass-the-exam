import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((700, 700))
YELLOW = (225, 225, 0)
RED = (255, 10, 102)
circle(screen, YELLOW, (350, 350),200)
circle(screen, RED, (300,300),50)
circle(screen, RED, (450,300),30)
polygon(screen, (0, 0, 0), [[200, 270],[360, 260], [350, 250], [200, 230]])
polygon(screen, (0, 0, 0), [[420, 270],[500, 250], [500, 280], [430, 280]])
rect(screen, (0, 0, 0), (270, 400, 200, 70))
circle(screen, (255, 0, 0), (360,490), 50)
rect(screen, YELLOW, (300, 470, 110, 70))
polygon(screen, (255, 255, 255), [[300, 400], [350, 400], [325, 430]])
polygon(screen, (255, 255, 255), [[370, 400],[420, 400], [380, 430]])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()