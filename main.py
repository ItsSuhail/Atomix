import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Atomix')
pygame.mouse.set_visible(False)

# Game states
MENU = "menu" #initial state
PLAY = "play"
ABOUT = "about"

# Current state
state = MENU


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
rick_surface = pygame.image.load('assets/images/rick.png')
rick_morty_surface = pygame.image.load('assets/images/rickmorty.png')
title_surface = text_font_2.render('ATOMIX', False, 'white')
credit_surface = text_font_2.render('CREDITS', False, 'white')

# Rectangles
cursor_rect = cursor_image.get_rect()
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
    screen.blit(title_surface, (325,20))
    
    # Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())

def game_choose():
    back_surface_1 = text_font_2_sm.render('BACK', False, 'brown2')


    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_1 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(rick_morty_surface, (-40,0))
    screen.blit(title_surface, (325,20))
    screen.blit(back_surface_1, (10,5))


    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())

def about():
    back_surface_2 = text_font_2_sm.render('BACK', False, 'brown2')
    credits_trans_surface = pygame.Surface((670,250), pygame.SRCALPHA)
    developedby_surface = text_font_3.render('Developed by: Suhail Hasan and Audad Ahmed', False, "white")
    

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_2 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(credit_surface, (325,20))
    screen.blit(back_surface_2, (10,5))

    pygame.draw.rect(credits_trans_surface, (255, 180, 30, 150), (0,0, 670, 250), border_radius=25)
    credits_trans_surface.blit(developedby_surface, (10,10))
    screen.blit(credits_trans_surface, (65,100))

    

    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)
    # print(pygame.mouse.get_pos())



fps = 60
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


    pygame.display.update()
    clock.tick(fps) #Sets maximum frame rate (ceiling)