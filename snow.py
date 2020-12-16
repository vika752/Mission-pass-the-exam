import pygame, sys, os
from pygame.draw import *
from pygame.locals import *
pygame.init()

FPS = 50
W = 720
H = 600
screen = pygame.display.set_mode((W, H))
screen.fill((255, 255, 255))

#загружаем картинки

snow_surf = [pygame.image.load('/Users/demo/Desktop/snow1.0.png'), pygame.image.load('/Users/demo/Desktop/snow1.1.png'), pygame.image.load('/Users/demo/Desktop/snow1.2.png'), pygame.image.load('/Users/demo/Desktop/snow1.3.png')]

#Задаем цвет, начальные координаты и радиус шарика, который станет определителем событий
WHITE = (255, 255, 255)
x = 0
y = 0 
r = 20
dx = 5

#Начало главного цикла


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            pygame.display.update()

    screen.fill(WHITE)
    pygame.draw,circle(screen, WHITE, (x,y), r)
    x += dx
    snow_rect = snow_surf[0].get_rect(bottomright=(W, H))
    screen.blit(snow_surf[0], snow_rect)
    
# В зависимости от положения шарика, меняется картина фона

    if x > 150 and x<350: 
        snow_rect = snow_surf[1].get_rect(bottomright=(W, H))
        screen.blit(snow_surf[1], snow_rect)
        
    if x > 350 and x< 500:
        snow_rect = snow_surf[2].get_rect(bottomright=(W, H))
        screen.blit(snow_surf[2], snow_rect)
        

    if x > 500 and x<720:
        snow_rect = snow_surf[3].get_rect(bottomright=(W, H))
        screen.blit(snow_surf[3], snow_rect)
        
    if x==720 or x==0:
        dx = dx * -1
        
    pygame.display.flip()

clock.tick(20) 
pygame.quit()