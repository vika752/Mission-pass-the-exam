
import pygame, sys, random

pygame.init()

display_width = 800
display_heght = 600

display = pygame.display.set_mode((display_width, display_height))
#colors

class Button():
    def__init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = (20, 240, 50)
        self.active_color = (20, 250, 50)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse  = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + self.width and y < mouse{1] < y + self.height:
        pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

    
        
        if click[0] == 1 and action is not None:
                action() 
    else:
        pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height)) 
    
    print_text(messege, x=10, y=10)
 
def print_text(message, x, y, font_color = (0,0,0), font_type = 'PingPong.ttf', font_size =30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type,render(messege, True, font_color)
    display.blit(text, (x,y))


          
def show_menu():
    menu_background = pygame.image.load('/Users/demo/Documents/menu.jpg')
    start_btn = Button(300, 70)
    quit_btn = Button(120, 70)

    show = True
 
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT;
                pygame.quit()
                quit()
    
    display.blit(menu_background, (0,0)) 
    start_btn.draw(300,200,"Start game", start_game, 50)
    quit_btn.draw(350,300,"QUIT", quit , 50) 
   
    pygame.diplay.update()
    clock.tick(60)


def start_game()
#передаем цикл, который запускает игру.

show_menu()
#меню должно повляться перед запустением игры