'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from abc import ABC, abstractmethod
import pygame
from pygame.constants import RESIZABLE
GRID_SIZE = 12
import thorpy
import sys
import default_game
from snake import Snake
from snake_body import SnakeBody

class Game(object):
    '''
    classdocs
    '''

    def __init__(self, game_speed = 10):
        '''
        Constructor
        '''

        #initialize the pygame module and sound
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        
        self.game_speed = game_speed
        logo = pygame.image.load("SnakeIcon.jpg")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("SNAKE")
        self.screen = pygame.display.set_mode((240,240), RESIZABLE)
        self.running = True
        white = (255,255,255)
        self.screen.fill(white)
        pygame.draw.rect(self.screen, (0,0,0), (10,10,10,10), 3)
        pygame.display.update()
        self.clock = pygame.time.Clock()
        
        self.tile_height = 20
        self.tile_width = 20
        self.calc_tile_size()
        
    def quit_function(self):
        pygame.quit()

    '''
    #Logan's Code
        
    #Start Menu
    pygame.init()
    pygame.key.set_repeat(300, 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((240,240))
    screen.fill((255,255,255))
    
    #Create buttons and place them in a box
    play_button = thorpy.make_button("Play", func=thorpy.functions.quit_func)
    #options_button = thorpy.make_button("Difficulty", func=thorpy.functions.quit_func)
    quit_button = thorpy.make_button("Quit", func=quit_function)
    box = thorpy.Box(elements=[play_button, quit_button])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen
    box.set_center((120,120))
    box.blit()
    box.update()

    #Menu loop
    menu_start = True
    while menu_start == True:
          pygame.init()
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 menu_start = False
                 break
              menu.react(event)
    '''
    
    #def easy_function():
        #print("Easy")
        #snake = SnakeBody(10, -1000, -1000)
        #game_snake = Snake(3, 20, 0, 0)
        #thorpy.functions.quit_func()

    #def medium_function():
        #print("Medium")
        #snake = SnakeBody(20, -1000, -1000)
        #game_snake = Snake(6, 20, 0, 0)
        #thorpy.functions.quit_func()

    #def hard_function():
        #print("Hard")
        #snake = SnakeBody(50, -1000, -1000)
        #game_snake = Snake(9, 20, 0, 0)
        #thorpy.functions.quit_func()
    
    #Difficulty Menu
    #pygame.init()
    #pygame.key.set_repeat(300, 30)
    #clock = pygame.time.Clock()
    #screen = pygame.display.set_mode((240,240))
    #screen.fill((255,255,255))
    #easy_button = thorpy.make_button("Easy", func=easy_function)
    #medium_button = thorpy.make_button("Medium", func=medium_function)
    #hard_button = thorpy.make_button("Hard", func=hard_function)
    #box = thorpy.Box(elements=[easy_button, medium_button, hard_button])
    #menu = thorpy.Menu(box)
    #for element in menu.get_population():
        #element.surface = screen
    #box.set_center((120,120))
    #box.blit()
    #box.update()
        
    #menu_start = True
    #while menu_start == True:
          #for event in pygame.event.get():
              #if event.type == pygame.QUIT:
                 #menu_start = False
                 #break
              #menu.react(event)
    #--------------------------------------------------------------
              

    def start(self):
        #---------------------Main Game Loop---------------------#
        while self.running:
        
            self.process_input()
    
            self.update_game()
            
            self.render()
            
            self.clock.tick(self.game_speed)
            #pygame.time.wait(100)


    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def update_game(self):
        pass
    
    @abstractmethod
    def render(self):
        pass
    
    def calc_tile_size(self):
        #Calcualtes the maximum size for the tiles 
        h, w = pygame.display.get_surface().get_size()
        
        self.tile_height = h // GRID_SIZE
        self.tile_width = w // GRID_SIZE
        
        