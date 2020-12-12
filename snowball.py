import pygame, sys, os
from pygame.draw import *
from pygame.locals import *
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 900
HEIGHT = 900
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(abst_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .085 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(100,400,10)
        self.rect.y = random.randrange(-150, -100, 10)
        self.speedy = random.randrange(1,8, 1)
        self.speedx = random.randrange(-3,3, 1)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8,1)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = 200
            self.rect.y = -90
            self.speedy = 3

abst_images = [pygame.image.load('/Users/demo/Documents/abst.png'),pygame.image.load('/Users/demo/Documents/abst2.png')]

background = pygame.image.load('/Users/demo/Documents/snow/snow1.2.png')
background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

for i in range(3):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()



    screen.fill(BLACK)
    screen.blit(background, background_rect)
    
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
