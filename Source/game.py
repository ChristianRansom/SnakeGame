'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from abc import ABC, abstractmethod
import pygame
from pygame.constants import RESIZABLE

GRID_SIZE = 12

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
        self.screen = pygame.display.set_mode((480,480), RESIZABLE)
        self.running = True
        white = (255,255,255)
        self.screen.fill(white)
        #pygame.draw.rect(screen, (0,0,0), (10,10,10,10), 3)
        pygame.display.update()
        self.clock = pygame.time.Clock()
        
        self.tile_height = 20
        self.tile_width = 20
        self.calc_tile_size()
        
        
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
        
        