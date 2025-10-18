import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Atomix')
pygame.mouse.set_visible(False)

class Babloo:
    def __init__(self, x, y, radius, text, font, text_color=(0, 0, 0), babloo_color=(173, 216, 230)):
        """
        Initializes a Babloo instance.

        Parameters:
        - x, y: center coordinates of babloo on the game surface
        - radius: radius of babloo
        - text: text to display inside the babloo
        - font: a pygame.font.Font object
        - text_color: color of the text (default: black)
        - babloo_color: color of the babloo (default: light blue)
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.font = font
        self.text_color = text_color
        self.babloo_color = babloo_color

        # Calculate surface size (a bit bigger than the babloo to avoid clipping)
        self.surface_size = radius * 2 + 10
        
    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return (self.x,self.y)

    def draw(self, screen, append_x=0, append_y=0):
        self.x += append_x # Speed along x
        self.y += append_y # Speed along y

        self.surface = pygame.Surface((self.surface_size, self.surface_size), pygame.SRCALPHA)

        # The rect of the surface (positioned so that (x, y) is at the center of the babloo on the game surface)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
        center_in_surface = (self.surface_size // 2, self.surface_size // 2)
        
        # Drawing the babloo
        pygame.draw.circle(self.surface, self.babloo_color, center_in_surface, self.radius)

        # Rendering and bliting the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=center_in_surface)
        self.surface.blit(text_surface, text_rect)
        screen.blit(self.surface, self.rect)

class BablooManagement:
    possible_x = [55, 130, 205, 280, 355, 405, 505, 580, 655]

    def __init__(self, *babloos, radius=25, font, text_color=(0, 0, 0), babloo_color=(173, 216, 230)):
        self.babloos = list(babloos)
        self.radius = radius
        self.font = font
        self.text_color = text_color
        self.babloo_color = babloo_color

    def add_babloo(self, babloo):
        self.babloos.append(babloo)
    
    def spawn_babloo(self,atoms):
        babloo_spawn = Babloo((random.choice(self.possible_x)+random.randint(-25,25)),random.randrange(-30, 5),self.radius,random.choice(atoms),self.font, self.text_color, self.babloo_color)
        self.babloos.append(babloo_spawn)

    def draw(self, screen,append_x, append_y):
        for babloo,index in zip(self.babloos,range(0,len(self.babloos))):
            if babloo.get_coords()[1] > 400:
                # print('deleting')
                del self.babloos[index]
            babloo.draw(screen, append_x, append_y)
            

# Game states
MENU = "menu" #initial state
PLAY = "play"
ABOUT = "about"
GAME = "game"

# Current state
state = MENU
spawn = False

# Initializing fonts
text_font_1 = pygame.font.Font('assets/fonts/font1.ttf',60)
text_font_2 = pygame.font.Font('assets/fonts/font2.ttf',60)
text_font_2_sm = pygame.font.Font('assets/fonts/font2.ttf',25)
text_font_3 = pygame.font.Font('assets/fonts/RobotoSlab-SemiBold.ttf', 28)

# Clock
clock = pygame.time.Clock()

# Defining surfaces
background_menu_surface = pygame.image.load('assets/images/bgb.png')
cursor_image = pygame.image.load('assets/images/flask.png')
cursor_image = pygame.transform.scale(cursor_image, (32,32))
big_flask = pygame.image.load('assets/images/bigflask.png')
big_flask = pygame.transform.scale(big_flask, (95,120))
rick_surface = pygame.image.load('assets/images/rick.png')
rick_morty_surface = pygame.image.load('assets/images/rickmorty.png')
title_surface = text_font_2.render('ATOMIX', False, 'white')
credit_surface = text_font_2.render('CREDITS', False, 'white')

# Rectangles
cursor_rect = cursor_image.get_rect()
big_flask_rect = big_flask.get_rect()
play_rect = pygame.Rect(600, 150, 130, 60) # Inside Main menu scene
about_rect = pygame.Rect(580, 215, 160, 60) # Inside Main menu scene
exit_rect = pygame.Rect(610, 280, 105, 60) # Inside Main menu scene
back_rect_1 = pygame.Rect(10,5, 56,28) # Inside Game choose scene

def menu():
    play_surface = text_font_2.render('PLAY', False, 'brown2')
    about_surface = text_font_2.render('ABOUT', False, 'brown2')
    exit_surface = text_font_2.render('EXIT', False, 'brown2')

    if play_rect.collidepoint(pygame.mouse.get_pos()):
        play_surface = text_font_2.render('PLAY', False, 'cornflowerblue')

    if about_rect.collidepoint(pygame.mouse.get_pos()):
        about_surface = text_font_2.render('ABOUT', False, 'cornflowerblue')
        
    if exit_rect.collidepoint(pygame.mouse.get_pos()):
        exit_surface = text_font_2.render('EXIT', False, 'cornflowerblue')

    screen.blit(background_menu_surface, (0,0))
    # Menu rectangle
    pygame.draw.rect(screen, 'azure2', (575,150,175, 205), border_radius=25)

    screen.blit(rick_surface, (0,75))
    screen.blit(play_surface, (600,150))
    screen.blit(about_surface, (580,215))
    screen.blit(exit_surface, (610,280))
    screen.blit(title_surface, (360,20))
    
    # Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())

def game_choose():
    back_surface_1 = text_font_2_sm.render('BACK', False, 'brown2')


    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_1 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(rick_morty_surface, (-40,70))
    screen.blit(title_surface, (360,20))
    screen.blit(back_surface_1, (10,5))


    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())

# b1 = Babloo(random.randint(25,700), -20, 25, "C", text_font_3, (255,255,255), (25, 200, 25))
# b2 = Babloo(random.randint(25,700), 5, 25, "C", text_font_3, (255,255,255), (25, 200, 25))
# b3 = Babloo(random.randint(25,700), 15, 25, "C", text_font_3, (255,255,255), (25, 200, 25))
b = BablooManagement(radius=25, font=text_font_3, text_color=(255,255,255), babloo_color=(25, 200, 25))
def game():
    global b,spawn
    back_surface_1 = text_font_2_sm.render('BACK', False, 'brown2')
    game_surface = pygame.Surface((770,400), pygame.SRCALPHA)

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_1 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(back_surface_1, (10,5))

    pygame.draw.rect(game_surface, (255, 255, 255, 200), (0,0, 770, 400), border_radius=15)
    if spawn:
        b.spawn_babloo(['H','O','N','C'])
        spawn=False
    b.draw(game_surface,random.random()*(random.choice([-2,2])), 3)
    # pygame.draw.circle(game_surface, (0,255,255), (x, y), 25)
    screen.blit(game_surface, (65,50))


    #Custom cursor
    big_flask_rect.center = pygame.mouse.get_pos()
    screen.blit(big_flask,big_flask_rect)
    # pygame.mouse.set_visible(True)
    # print(pygame.mouse.get_pos())


def about():
    back_surface_2 = text_font_2_sm.render('BACK', False, 'brown2')
    credits_trans_surface = pygame.Surface((670,250), pygame.SRCALPHA)
    developedby_surface = text_font_3.render('Developed by: Suhail Hasan and Audad Ahmed', False, "white")
    databasemanagement_surface = text_font_3.render('Database managed by: Audad Ahmed', False, "white")
    gameidea_surface = text_font_3.render('Game Idea by: Suhail Hasan', False, "white")
    
    

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_2 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(credit_surface, (360,20))
    screen.blit(back_surface_2, (10,5))

    pygame.draw.rect(credits_trans_surface, (255, 180, 30, 150), (0,0, 670, 250), border_radius=25)
    credits_trans_surface.blit(developedby_surface, (10,10))
    credits_trans_surface.blit(gameidea_surface, (10,40))
    credits_trans_surface.blit(databasemanagement_surface, (10,70))
    screen.blit(credits_trans_surface, (65,100))

    

    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())


state = GAME

fps = 60
pygame.time.set_timer(pygame.USEREVENT, 500)
while (True):

    if state == MENU:
        fps = 120
        menu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    state = PLAY
                elif about_rect.collidepoint(pygame.mouse.get_pos()):
                    state = ABOUT
                elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
    if state == PLAY:
        game_choose()

        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_rect_1.collidepoint(pygame.mouse.get_pos()):
                    state = MENU
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    if state == ABOUT:
        about()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_rect_1.collidepoint(pygame.mouse.get_pos()):
                    state = MENU
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    if state == GAME:
        game()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_rect_1.collidepoint(pygame.mouse.get_pos()):
                    state = MENU
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.USEREVENT:
                spawn = True

    pygame.display.update()
    clock.tick(fps) #Sets maximum frame rate (ceiling)
