import os
import random
import pygame, sys

# Инициализация PyGame
pygame.init()
pygame.mixer.init()
mab = 0
# параметры окна игры
height = 600
width = 720
size = height, width
screen = pygame.display.set_mode(size)
running = True
s1 = []
s2 = []
#создаем звуковой объект
#воспроизводим его (фоновая музыка)
splat = pygame.mixer.Sound("fon.wav")
splat.play()

'''
создание класса, в котором прописывается сам студент(лыжник);
его движение, используя модуль pygame.sprite
'''
class Person(pygame.sprite.Sprite):
    image = pygame.Surface((50, 50))
    image.fill((0, 255, 0))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Person.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.nap = 0
        self.z = False
        self.Vx = 0
        self.Vy = 0
        self.tick = 0
        self.score = -1
        self.tickrate = 70

    def jump(self):
        if self.nap and self.nap != 999:
            self.Vx = -20
            self.Vy = 18
            self.nap = 999
            self.z = False
        elif self.nap != 999:
            self.Vx = 20
            self.Vy = 18
            self.nap = 999
            self.z = False

    def update(self):
        if self.rect.centerx <= 25 and self.z:
            self.nap = 0
            self.Vx = 0
            self.Vy = 0
            self.rect.centerx = 25
        elif self.rect.centerx >= 575 and self.z:
            self.nap = 1
            self.rect.centerx = 575
            self.Vx = 0
            self.Vy = 0
        if self.tick % 5 == 0:
            if self.Vy != 0:
                self.Vy -= 2
        if self.rect.centery < 0:
            self.rect.centery = 680
            self.score = int(self.score * 1.5)
            self.tick = 30
            if self.tickrate > 42:
                self.tickrate -= 3
        if self.tick % 100 == 0:
            self.score += 1
        self.rect.centery -= self.Vy
        self.rect.centery += 4
        self.rect.centerx += self.Vx

'''
создание класса, в котором прописываются препятствия;
их движение, используя модуль pygame.sprite
'''
class Snowball(pygame.sprite.Sprite):
    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = Snowball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = 0
        self.v = random.choice(range(12, 20))
        self.rot = random.choice(range(360))
        self.rv = random.choice(range(10))

    def update(self):
        self.rect.centery += self.v
        self.rot += self.rv
        self.image = pygame.transform.rotate(Snowball.image, self.rot)
        if self.rect.centery > 800:
            self.kill()

'''
создание класса, в котором прописываются объекты, за которые 
начисляются баллы
'''
class Present(pygame.sprite.Sprite):
    image = pygame.Surface((50, 50))
    image.fill((255, 255, 0))

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = Present.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = 0
        self.v = random.choice(range(7, 12))
        self.rot = random.choice(range(360))
        self.rv = random.choice(range(30))

    def update(self):
        self.rect.centery += self.v
        self.rot += self.rv
        self.image = pygame.transform.rotate(Present.image, self.rot)
        if self.rect.centery > 800:
            self.kill()

#создание группы спрайтов в игре
all_sprites = pygame.sprite.Group()


xxx = Person((25, 500))

f = open("config.txt", encoding="utf8")
try:
    Presents = int(f.read())
except:
    Presents = 0
f.close()

FPS = 40
fpsClock = pygame.time.Clock()

#цикл игры
while running:
    screen.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            xxx.jump()

    if xxx.tick % xxx.tickrate == 0 and xxx.rect.centery > 150:
        if xxx.nap == 0:
            n = random.choice(range(110, 299))
            n = Snowball(n)
            s1.append(n)
        else:
            n = random.choice(range(299, 488))
            n = Snowball(n)
            s1.append(n)
        if random.choice([0, 1, 2, 3]) == 1:
            n = random.choice(range(110, 488))
            n = Snowball(n)
            s1.append(n)
        if random.choice([0, 1, 2, 3, 4, 5, 6, 7]) == 1:
            n = random.choice(range(110, 488))
            n = Snowball(n)
            s1.append(n)

    if xxx.tick % 100 == 0 and xxx.rect.centery > 80:
        if random.choice([0, 1, 2, 3]) == 1:
            n = Present(random.choice(range(200, 400)))
            s2.append(n)

    if xxx.rect.centery < 0:
        for i in s1:
            i.kill()
        for i in s2:
            i.kill()
        s2 = []
        s1 = []

    for i in s1:
        if pygame.sprite.collide_mask(xxx, i) or xxx.rect.centery > 735:
            if Presents > 2:
                z = True
                while z:
                    all_sprites.draw(screen)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            z = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                Presents = Presents - 3
                                z = False
                                xxx.rect.centerx = 25
                                xxx.rect.centery = 475
                            elif event.key == pygame.K_BACKSPACE:
                                for g in s1:
                                    g.kill()
                                for g in s2:
                                    g.kill()
                                s1 = []
                                s2 = []
                                xxx.kill()
                                xxx = Person((25, 500))
                                z = False
                    font = pygame.font.Font(None, 50)
                    text = font.render("{}".format(str(xxx.score)), 1, (250, 50, 100))
                    screen.blit(text, (290, 50))

                    font = pygame.font.Font(None, 50)
                    text = font.render("{}".format(str(Presents)), 1, (0, 0, 0))
                    screen.blit(text, (290, 680))

                    pygame.display.flip()
            else:
                for g in s1:
                    g.kill()
                for g in s2:
                    g.kill()
                s1 = []
                s2 = []
                xxx.kill()
                xxx = Person((25, 500))
            break

    for i in s2:
        if pygame.sprite.collide_mask(xxx, i):
            s2.remove(i)
            i.kill()
            Presents += 1
            break

    all_sprites.draw(screen)
    #обновление
    all_sprites.update()
    xxx.z = True
    
#отображение кол-ва баллов (в нижней части экрана)
    font = pygame.font.Font(None, 50)
    text = font.render("{}".format(str(xxx.score)), 1, (250, 50, 100))
    screen.blit(text, (290, 50))
    
#отображение времени (в верхней части экрана)
    font = pygame.font.Font(None, 50)
    text = font.render("{}".format(str(Presents)), 1, (0, 0, 0))
    screen.blit(text, (290, 680))

    xxx.tick += 1
    fpsClock.tick(FPS)
    pygame.display.flip()

f = open("config.txt", 'w')
f.write(str(Presents))
f.close()

pygame.quit()
