import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Atomix')

text_font = pygame.font.Font('assets/fonts/font2.ttf',60)
background_surface = pygame.image.load('assets/images/bgb.png')
rick_surface = pygame.image.load('assets/images/rick.png')

play_surface = text_font.render('PLAY', False, 'Orange')


clock = pygame.time.Clock()

while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(background_surface, (0,0))
    screen.blit(rick_surface, (0,0))
    screen.blit(play_surface, (600,200))

    pygame.display.update()
    clock.tick(60) #Sets maximum frame rate (ceiling)