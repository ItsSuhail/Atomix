import pygame
import random
from essentials.random_reaction import *
from essentials.parse import *
from sys import exit


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((900, 500)) # Size of the window
pygame.display.set_caption('Atomix') # Title of the game
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

    def get_screen_coords(self):
        return (self.x+65, self.y+50)
    
    def get_game_surface_coords(self,x,y):
        return (x-65, y-50)

    def distance_from_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], 300
        babloo_x,babloo_y = self.get_screen_coords()
        return ((mouse_x-babloo_x)**2 + (mouse_y-babloo_y)**2)**.5

    def get_text(self):
        return self.text

    def draw(self, screen, append_x=0, append_y=0):
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

        self.x += append_x # Speed along x
        self.y += append_y # Speed along y

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
    
    def spawn_babloo(self,atoms,weights):
        babloo_spawn = Babloo((random.choice(self.possible_x)+random.randint(-25,25)),random.randrange(-30, 5),self.radius,random.choices(population=atoms, weights=weights,k=1)[0],self.font, self.text_color, self.babloo_color)
        self.babloos.append(babloo_spawn)

    def clear_all(self):
        self.babloos.clear()

    def draw(self, screen,append_x, append_y):
        for babloo,index in zip(self.babloos,range(0,len(self.babloos))):
            if babloo.get_coords()[1] > 400:
                del self.babloos[index]
            elif babloo.distance_from_mouse() <= 25:
                del self.babloos[index]
                return babloo.get_text()
            else:
                babloo.draw(screen, append_x, append_y)

            

# Loading sound effects
reaction_complete_sound = pygame.mixer.Sound("assets/sounds/reaction_complete.wav")
successful_collection_sound = pygame.mixer.Sound("assets/sounds/successful_collection.wav")
wrong_answer_sound = pygame.mixer.Sound("assets/sounds/wrong_answer.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# Loading background music
pygame.mixer.music.load('assets/sounds/bg_music.mp3')
# Setting the volume
pygame.mixer.music.set_volume(0.3)
# Playing the music
pygame.mixer.music.play(-1)

# Game states
MENU = "menu" #initial state
PLAY = "play"
ABOUT = "about"
GAME = "game"

# Current state
state = MENU

# Initializing fonts
text_font_1 = pygame.font.Font('assets/fonts/font1.ttf',60)
text_font_2 = pygame.font.Font('assets/fonts/font2.ttf',60)
text_font_2_reg = pygame.font.Font('assets/fonts/font2.ttf',40)
text_font_2_sm = pygame.font.Font('assets/fonts/font2.ttf',25)
text_font_3 = pygame.font.Font('assets/fonts/RobotoSlab-SemiBold.ttf', 28)
text_font_3_sm = pygame.font.Font('assets/fonts/RobotoSlab-SemiBold.ttf', 23)

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

## Rectangles

cursor_rect = cursor_image.get_rect()
big_flask_rect = big_flask.get_rect()

play_rect = pygame.Rect(600, 150, 130, 60) # Inside Main menu scene
about_rect = pygame.Rect(580, 215, 160, 60) # Inside Main menu scene
exit_rect = pygame.Rect(610, 280, 105, 60) # Inside Main menu scene

grade11_rect = pygame.Rect(600, 150, 130, 60) # Inside Game choose scene
grade12_rect = pygame.Rect(580, 215, 160, 60) # Inside Game choose scene
combined_rect = pygame.Rect(610, 280, 105, 60) # Inside Game choose scene

back_rect_1 = pygame.Rect(10,5, 56,28) # Inside Game choose scene


## Babloo Management object
babloo_management = BablooManagement(radius=25, font=text_font_3, text_color=(255,255,255), babloo_color=(25, 200, 25))

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

def game_choose():
    global chosen

    grade11_surface = text_font_2_reg.render('Grade 11', False, 'brown2')
    grade12_surface = text_font_2_reg.render('Grade 12', False, 'brown2')
    combined_surface = text_font_2_reg.render('Combined', False, 'brown2')
    choose_surface = text_font_3_sm.render('Choose a Grade, and complete the reactions thrown at you!', False, 'brown2')
    back_surface_1 = text_font_2_sm.render('BACK', False, 'brown2')

    if grade11_rect.collidepoint(pygame.mouse.get_pos()):
        grade11_surface = text_font_2_reg.render('Grade 11', False, 'cornflowerblue')

    if grade12_rect.collidepoint(pygame.mouse.get_pos()):
        grade12_surface = text_font_2_reg.render('Grade 12', False, 'cornflowerblue')
        
    if combined_rect.collidepoint(pygame.mouse.get_pos()):
        combined_surface = text_font_2_reg.render('Combined', False, 'cornflowerblue')

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_1 = text_font_2_sm.render('BACK', False, 'cornflowerblue')

    screen.blit(background_menu_surface, (0,0))
    screen.blit(rick_morty_surface, (-40,70))
    screen.blit(title_surface, (360,20))
    screen.blit(back_surface_1, (10,5))

    # Grade select menu rectangle
    pygame.draw.rect(screen, 'azure2', (575,150,175, 205), border_radius=25)
    # Objective rectangle
    pygame.draw.rect(screen, 'azure2', (5,450,890,45), border_radius=10)

    screen.blit(grade11_surface, (585,160))
    screen.blit(grade12_surface, (580,225))
    screen.blit(combined_surface, (580,290))
    screen.blit(choose_surface, choose_surface.get_rect(center = (450, 472.5)))

    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)

def game():
    global babloo_management, spawn, score, reaction_shown, reaction, collected_string, blanked, atoms, weights, blanked_string, reactants_str, products_str, is_product, fade, outside, chosen

    if fade !=0:
        fade -= 3
        if fade < 0:
            fade = 0
    
    if not reaction_shown:
        reaction_shown = True
        reaction_dict = random_reaction(chosen)
        reactants = reaction_dict['reactants']
        products = reaction_dict['products']
        unblankables = reaction_dict['unblankables']
        atoms = list(reaction_dict['ele_symbols'])
        weights = [7]*len(atoms)
        atoms.extend(['2','3','4','5','6','7'])
        weights.extend([4,4,2,2,1,1])
        
        if random.choice([-1,1]) == 1:
            is_product = True
            
            choice = random.choice(products)
            while (choice in unblankables):
                choice = random.choice(products)
            blanked = unparser_no_bs(choice)
            products_ = products.copy()
            products_.remove(choice)

            reactants_str = " + ".join(list(map(unparser_no_bs, reactants)))
            products_str = " + ".join(list(map(unparser_no_bs, products_)))
            
            blanked_string = "_"*len(blanked)
        else:
            choice = random.choice(reactants)
            while (choice in unblankables):
                choice = random.choice(reactants)
            blanked = unparser_no_bs(choice)
            reactants_ = reactants.copy()
            reactants_.remove(choice)

            products_str = " + ".join(list(map(unparser_no_bs, products)))
            reactants_str = " + ".join(list(map(unparser_no_bs, reactants_)))
            
            blanked_string = "_"*len(blanked)
            
    if is_product:
        if products_str != '':
            products_final_str = products_str + " + " + blanked_string
        else:
            products_final_str = blanked_string
        reaction = reactants_str + " --> " + products_final_str
    else:
        if reactants_str != "":
            reactants_final_str = reactants_str + " + " + blanked_string
        else:
            reactants_final_str = blanked_string
        reaction = reactants_final_str + " --> " + products_str

    # Game surface
    game_surface = pygame.Surface((770,400), pygame.SRCALPHA)

    back_surface_1 = text_font_2_sm.render('BACK', False, 'brown2')

    reaction_display_surface = pygame.Surface((700,40), pygame.SRCALPHA)
    reaction_display_rect = reaction_display_surface.get_rect(center = (screen.get_width()//2, 30))
    reaction_display_surface.set_alpha(255)
    reaction_surface = text_font_3.render(reaction, False, 'yellow')
    
    
    score_surface = text_font_3.render(f'Score: {score}',False, 'white')
    blanked_surface = text_font_3.render(blanked, False, (255, 125, 0, fade))
    faded_surface = pygame.Surface((blanked_surface.get_width(), blanked_surface.get_height()), pygame.SRCALPHA)
    faded_surface.fill((255, 255, 255, 0))
    faded_surface.set_alpha(fade)

    if len(reaction) > 35:
        reaction_surface = text_font_3_sm.render(reaction, False, 'yellow')

    reaction_rect = reaction_surface.get_rect(center = (reaction_display_surface.get_width()/2, 20))
    score_rect = score_surface.get_rect(center = (screen.get_width()/2, 475))
    blanked_rect = blanked_surface.get_rect(center = (faded_surface.get_width()/2, faded_surface.get_height()/2))
    faded_surface_rect = faded_surface.get_rect(center = (game_surface.get_width()/2, game_surface.get_height()/2))
    
    faded_surface.blit(blanked_surface, blanked_rect)

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_1 = text_font_2_sm.render('BACK', False, 'cornflowerblue')

    screen.blit(background_menu_surface, (0,0))
    screen.blit(back_surface_1, (10,5))
    pygame.draw.rect(reaction_display_surface, (225, 100, 0, 250), (0,0,700,50), border_radius=5)
    reaction_display_surface.blit(reaction_surface, reaction_rect)
    screen.blit(reaction_display_surface, reaction_display_rect)
    pygame.draw.rect(game_surface, (255, 255, 255, 200), (0,0, 770, 400), border_radius=15)

    if spawn and fade == 0 and not outside:
        babloo_management.spawn_babloo(atoms,weights)
        spawn=False
    
    collected = None
    if fade == 0:
        # Speed can be changed here
        collected = babloo_management.draw(game_surface,random.random()*(random.choice([-2,2])), 2+random.random())

    if collected and not outside:
        collected_string = collected_string + collected
        if blanked == collected_string:
            reaction_complete_sound.play()
            blanked_string = collected_string
            collected_string = ""
            score += 1
            reaction_shown = False

        elif blanked.startswith(collected_string):
            successful_collection_sound.play()
            diff = len(blanked) - len(collected_string)
            blanked_string = collected_string + "_"*diff

        else:
            wrong_answer_sound.play()
            fade = 255
            collected_string = ""
            blanked_string = "_"*len(blanked)
        

    game_surface.blit(faded_surface, faded_surface_rect)
    screen.blit(game_surface, (65,50))

    #Custom cursor
    mouse_x, mouse_actual_y = pygame.mouse.get_pos()
    mouse_y = 300
    
    # If mouse is inside the game surface, show big flask. Else, show small flask
    if mouse_x > 65 and mouse_x < 835 and mouse_actual_y > 38 and mouse_actual_y < 460:
        outside = False
        big_flask_rect.center = (mouse_x,mouse_y+50)
        screen.blit(big_flask,big_flask_rect)
    else:
        outside = True
        cursor_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_image, cursor_rect)
    screen.blit(score_surface, score_rect)

def about():
    back_surface_2 = text_font_2_sm.render('BACK', False, 'brown2')

    credits_trans_surface = pygame.Surface((670,125), pygame.SRCALPHA)

    developedby_surface = text_font_3.render('Developed by: Suhail Hasan and Audad Ahmed', False, "white")
    databasemanagement_surface = text_font_3.render('Database managed by: Audad Ahmed', False, "white")
    gameidea_surface = text_font_3.render('Game Idea by: Suhail Hasan', False, "white")
    

    if back_rect_1.collidepoint(pygame.mouse.get_pos()):
        back_surface_2 = text_font_2_sm.render('BACK', False, 'cornflowerblue')


    screen.blit(background_menu_surface, (0,0))
    screen.blit(credit_surface, (360,20))
    screen.blit(back_surface_2, (10,5))

    pygame.draw.rect(credits_trans_surface, (225, 100, 0, 200), (0,0, 670, 125), border_radius=25)
    credits_trans_surface.blit(developedby_surface, (10,10))
    credits_trans_surface.blit(gameidea_surface, (10,40))
    credits_trans_surface.blit(databasemanagement_surface, (10,70))
    screen.blit(credits_trans_surface, credits_trans_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/2)))

    #Custom cursor
    cursor_rect.center = pygame.mouse.get_pos()
    screen.blit(cursor_image,cursor_rect)

def reset():
    global spawn, babloo_management, score, reaction_shown, reaction, collected_string, atoms, weights, blanked, blanked_string, reactants_str, products_str, is_product, fade, outside, chosen
    score = 0
    reaction_shown = False
    reaction = ""
    collected_string = ""
    atoms = []
    weights = []
    blanked = "" # Blanked component of the reaction
    blanked_string = "" # Blanked text shown consisting of underscores and collected atoms
    reactants_str = ""
    products_str = ""
    is_product = False
    fade = 0
    outside = False
    chosen = ""
    spawn = False
    babloo_management.clear_all()
    
spawn = False
score = 0
reaction_shown = False
reaction = ""
collected_string = ""
atoms = []
weights = []
blanked = "" # Blanked component of the reaction
blanked_string = "" # Blanked text shown consisting of underscores and collected atoms
reactants_str = ""
products_str = ""
is_product = False
fade = 0
outside = False
chosen = ""

fps = 60
pygame.time.set_timer(pygame.USEREVENT, 700)

while (True):

    if state == MENU:
        fps = 120
        menu()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()
                    
                    state = PLAY

                elif about_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()
                    
                    state = ABOUT

                elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()
                    
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
                    click_sound.play()

                    state = MENU
                
                elif grade11_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()

                    chosen = "11"
                    state = GAME

                elif grade12_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()

                    chosen = "12"
                    state = GAME
                
                elif combined_rect.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()

                    chosen = "C"
                    state = GAME
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    if state == ABOUT:
        about()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_rect_1.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()

                    state = MENU
                
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    if state == GAME:
        game()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_rect_1.collidepoint(pygame.mouse.get_pos()):
                    click_sound.play()

                    state = PLAY
                    reset()            

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.USEREVENT: # When the timer ticks, spawns a babloo
                spawn = True

    pygame.display.update()
    clock.tick(fps) #Sets maximum frame rate (ceiling)
