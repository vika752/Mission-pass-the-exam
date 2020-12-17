import os
import random
import pygame, sys

def load_image(name, color_key=None):
    fullname = os.path.join('image', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

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

f = open("config.txt", encoding="utf8")
s = f.read().split()
Presents = int(s[0])
flag_hero = s[1]
f.close()
# создаем звуковой объект
# воспроизводим его (фоновая музыка)
# splat = pygame.mixer.Sound("image\fon.wav")
# splat.set_volume(0.1)  # громкость фоновой музыки
# present = pygame.mixer.Sound("image\present.wav")
# present.set_volume(0.5)
# jump = pygame.mixer.Sound("image\jump.wav")  # звук прыжка
# jump.set_volume(0.2)

# splat.play()


'''Считывание ТОПа лидеров'''

name_player = []
coins = []

with open('Statistics.txt') as input_file:
    for line in input_file:
        if len(line.strip()) == 0:
            continue  # пустые строки и строки-комментарии пропускаем

        tokens = line.split()
        name_player.append(str(tokens[0]))
        coins.append(str(tokens[1]))

top = sorted([(name_player[i], coins[i]) for i in range(len(name_player))], key=lambda x: int(x[1]), reverse=True)


'''
создание класса, в котором прописывается сам студент(лыжник);
его движение, используя модуль pygame.sprite
'''


class Person(pygame.sprite.Sprite):
    if flag_hero == 'boy':
        imag2 = load_image("boy2.png", -1)
        imag2 = pygame.transform.scale(imag2, (imag2.get_width() // 6, imag2.get_height() // 6))

        imag1 = load_image("boy1.png", -1)
        imag1 = pygame.transform.scale(imag1, (imag1.get_width() // 6, imag1.get_height() // 6))

        image = load_image("boye.png", -1)
        image = pygame.transform.scale(image, (image.get_width() // 6, image.get_height() // 6))

    else:
        imag2 = load_image("girl2.png", -1)
        imag2 = pygame.transform.scale(imag2, (imag2.get_width() // 6, imag2.get_height() // 6))

        imag1 = load_image("girl1.png", -1)
        imag1 = pygame.transform.scale(imag1, (imag1.get_width() // 6, imag1.get_height() // 6))

        image = load_image("girle.png", -1)
        image = pygame.transform.scale(image, (image.get_width() // 6, image.get_height() // 6))

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
            self.Vx = -15
            self.Vy = 18
            self.nap = 999
            self.z = False
            self.image = Person.imag2
        elif self.nap != 999:
            self.Vx = 15
            self.Vy = 18
            self.nap = 999
            self.z = False
            self.image = Person.imag1

    def update(self):
        if self.rect.centerx <= 50 and self.z:
            self.nap = 0
            self.Vx = 0
            self.Vy = 0
            self.rect.centerx = 50
            self.image = Person.image
        elif self.rect.centerx >= 525 and self.z:
            self.nap = 1
            self.rect.centerx = 525
            self.Vx = 0
            self.Vy = 0
            self.image = Person.image
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
    k = random.choice([3.4 + 0.2 * i for i in range(5)])
    abst1 = load_image("abst.png", -1)
    image = pygame.transform.scale(abst1, (int(abst1.get_width() / k), int(abst1.get_height() / k)))

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


def for_statistics(score):
    global top
    for i in range(0, len(name_player)):
        if int(top[i][1]) < score:
            run = True
            name = ""
            font = pygame.font.Font(None, 50)
            while run:
                all_sprites.draw(screen)
                for evt in pygame.event.get():
                    if evt.type == pygame.KEYDOWN:
                        if evt.key == pygame.K_RETURN and name:
                            last_record = top[i]
                            top[i] = (name, score)
                            for j in range(5):
                                try:
                                    last_record, top[i+j+1] = top[i+j+1], last_record
                                except:
                                    break
                            f = open("Statistics.txt", 'w')
                            for i in top:
                                f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
                            f.close()
                            return
                        elif evt.unicode.isalpha():
                            name += evt.unicode
                        elif evt.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        elif evt.key == pygame.K_ESCAPE:
                            return
                    elif evt.type == pygame.QUIT:
                        f = open("config.txt", 'w')
                        f.write(str(Presents) + ' ' + flag_hero)
                        f.close()

                        f = open("Statistics.txt", 'w')
                        for i in top:
                            f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
                        f.close()

                        exit()
                font = pygame.font.Font(None, 50)
                text = font.render("{}".format(str(name)), 1, (0, 0, 0))
                screen.blit(text, (340, 340))

                font = pygame.font.Font(None, 50)
                text = font.render("{}".format(str(xxx.score)), 1, (250, 50, 100))
                screen.blit(text, (290, 50))

                font = pygame.font.Font(None, 50)
                text = font.render("{}".format(str(Presents)), 1, (0, 0, 0))
                screen.blit(text, (290, 680))

                font = pygame.font.Font(None, 50)
                text = font.render("Вы побили один из рекородов!", 1, (0, 0, 0))
                screen.blit(text, (0, 300))

                font = pygame.font.Font(None, 50)
                text = font.render("Введите ваше имя:", 1, (0, 0, 0))
                screen.blit(text, (0, 340))

                fpsClock.tick(FPS)
                pygame.display.flip()
                screen.fill('white')


class Present(pygame.sprite.Sprite):
    image = load_image("present.png", -1)
    image = pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3))

    def __init__(self, x):
        super().__init__(all_sprites)
        self.image = Present.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = x
        self.rect.centery = 0
        self.v = random.choice(range(7, 12))

    def update(self):
        self.rect.centery += self.v
        if self.rect.centery > 800:
            self.kill()


# cоздаем класс меню
class Menu:
    def __init__(self, punkts=[400, 350, u'Punkt', (250, 250, 30), (250, 30, 250)]):
        self.punkts = punkts
        self.menu()

        screen.fill((50, 50, 50))

    # функция отрисовки всех пунктов меню (название пов-сти, шрифт, номер эл-та)
    def render(self, pov, font, num_punkt):
        # перебирает все элементы списка по пунктам
        for i in self.punkts:
            # условие, в к-м проверяется совп-ет ли номер текущ-го пункта с номером, к-й был передан функции
            if num_punkt == i[5]:
                pov.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                pov.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    # функция, в к-й реализуется сцена меню
    def menu(self):
        window = pygame.display.set_mode((height, width))
        pygame.font.init()
        pygame.display.set_caption('menu')
        screen = pygame.Surface((height, width))
        pygame.key.set_repeat(1, 1)
        done = True
        font_menu = pygame.font.Font('font.ttf', 70)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        global flag_hero
        while done:
            screen.fill((0, 150, 200))
            # блок управления мышью в меню
            mp = pygame.mouse.get_pos()
            # проверяем, не пересекается ли мышь с пунктом меню
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    f = open("config.txt", 'w')
                    f.write(str(Presents) + ' ' + flag_hero)
                    f.close()

                    f = open("Statistics.txt", 'w')
                    for i in top:
                        f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
                    f.close()

                    sys.exit()
                    # блок перемещения по меню, с помощью клавиш
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        mini_punkts = [(260, 300, u'BOY', (11, 0, 77), (255, 255, 255), 4),
                                       (255, 340, u'GIRL', (11, 0, 77), (255, 255, 255), 5)]
                        mini_menu = Menu(mini_punkts)
                    elif punkt == 2:
                        mini2_punkts = [(260, 500, u'EXIT', (11, 0, 77), (255, 255, 255), 6),
                                        (175, 300, name_player[0] + ' - ' + coins[0], (11, 0, 77), (255, 255, 255), 10),
                                        (175, 340, name_player[1] + ' - ' + coins[1], (11, 0, 77), (255, 255, 255), 10),
                                        (175, 380, name_player[2] + ' - ' + coins[2], (11, 0, 77), (255, 255, 255), 10),
                                        (175, 420, name_player[3] + ' - ' + coins[3], (11, 0, 77), (255, 255, 255), 10),
                                        (175, 460, name_player[4] + ' - ' + coins[4], (11, 0, 77), (255, 255, 255), 10)]
                        Menu(mini2_punkts)
                    elif punkt == 3:
                        f = open("Statistics.txt", 'w')
                        for i in top:
                            f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
                        f.close()

                        f = open("config.txt", 'w')
                        f.write(str(Presents) + ' ' + flag_hero)
                        f.close()

                        exit()
                    elif punkt == 4:
                        flag_hero = 'boy'
                        done = False
                    elif punkt == 5:
                        flag_hero = 'girl'
                        done = False
                    elif punkt == 6:
                        done = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = False

            window.blit(screen, (0, 30))
            pygame.display.flip()


# Строки для работы меню
punkts = [(260, 300, u'PLAY', (11, 0, 77), (255, 255, 255), 0),
          (175, 340, u'CHOOSE THEME', (11, 0, 77), (255, 255, 255), 1),
          (210, 380, u'STATISTICS', (11, 0, 77), (255, 255, 255), 2),
          (260, 420, u'EXIT', (11, 0, 77), (255, 0, 0), 3)]
menu = Menu(punkts)

# создание группы спрайтов в игре
all_sprites = pygame.sprite.Group()

n1 = pygame.sprite.Sprite()
n1.image = load_image("end1.png", -1)
n1.rect = n1.image.get_rect()
n1.rect.centerx, n1.rect.centery = 54, 250

n2 = pygame.sprite.Sprite()
n2.image = load_image("end2.png", -1)
n2.rect = n2.image.get_rect()
n2.rect.centerx, n2.rect.centery = 546, 250

all_sprites.add(n1)
all_sprites.add(n2)

xxx = Person((25, 500))

FPS = 60
fpsClock = pygame.time.Clock()

# цикл игры
while running:
    screen.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = Menu(punkts)
            else:
                xxx.jump()
                # jump.play()

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
                    font = pygame.font.Font(None, 50)
                    text = font.render("Использовать 3 подарка", 1, (0, 0, 0))
                    screen.blit(text, (50, 300))

                    font = pygame.font.Font(None, 50)
                    text = font.render("для продолжения игры?", 1, (0, 0, 0))
                    screen.blit(text, (50, 340))
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
                                for_statistics(xxx.score)  # функция добавляющая результат в стистику, при взятии рекорда
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
                for_statistics(xxx.score)  # функция добавляющая результат в стистику, при взятии рекорда
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
            # present.play()  # музыка начисления баллов
            break

    all_sprites.draw(screen)
    # обновление
    all_sprites.update()
    xxx.z = True

    for i in range(len(top)):
        name_player[i] = str(top[i][0])
        coins[i] = str(top[i][1])

    # отображение кол-ва баллов (в нижней части экрана)
    font = pygame.font.Font(None, 50)
    text = font.render("{}".format(str(xxx.score)), 1, (250, 50, 100))
    screen.blit(text, (290, 50))

    # отображение времени (в верхней части экрана)
    font = pygame.font.Font(None, 50)
    text = font.render("{}".format(str(Presents)), 1, (0, 0, 0))
    screen.blit(text, (290, 680))
    xxx.tick += 1
    fpsClock.tick(FPS)
    pygame.display.flip()

f = open("config.txt", 'w')
f.write(str(Presents) + ' ' + flag_hero)
f.close()

pygame.quit()