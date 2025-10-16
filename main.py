import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Atomix')
# pygame.mouse.set_visible(False)

# Game states
MENU = "menu" #initial state
PLAY = "play"
ABOUT = "about"

# Current state
state = MENU


# Initializing fonts
text_font_1 = pygame.font.Font('assets/fonts/font1.ttf',60)
text_font_2 = pygame.font.Font('assets/fonts/font2.ttf',60)

# Clock
clock = pygame.time.Clock()

# Defining surfaces
background_menu_surface = pygame.image.load('assets/images/bgb.png')
cursor_image = pygame.image.load('assets/images/flask.png')
cursor_image = pygame.transform.scale(cursor_image, (32,32))
rick_surface = pygame.image.load('assets/images/rick.png')
rick_morty_surface = pygame.image.load('assets/images/rickmorty.png')
title_surface = text_font_2.render('ATOMIX', False, 'white')
# play_surface = text_font_2.render('PLAY', False, 'brown2')
# about_surface = text_font_2.render('ABOUT', False, 'brown2')
# exit_surface = text_font_2.render('EXIT', False, 'brown2')

# Cursor rectangle
cursor_rect = cursor_image.get_rect()
play_rect = pygame.Rect(600, 150, 130, 60)
about_rect = pygame.Rect(580, 215, 160, 60)
exit_rect = pygame.Rect(610, 280, 105, 60)


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

def game():
    screen.blit(background_menu_surface, (0,0))
    screen.blit(rick_morty_surface, (-20,0))
    
    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)


while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if state == MENU:
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
                
    if state == PLAY:
        game()

    pygame.display.update()
    clock.tick(60) #Sets maximum frame rate (ceiling)