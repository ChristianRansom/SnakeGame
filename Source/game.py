'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from abc import ABC, abstractmethod
import pygame

class Game(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        
        #initialize the pygame module and sound
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        logo = pygame.image.load("SnakeIcon.jpg")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("SNAKE")
        self.screen = pygame.display.set_mode((240,240))
        self.running = True
        white = (255,255,255)
        self.screen.fill(white)
        #pygame.draw.rect(screen, (0,0,0), (10,10,10,10), 3)
        pygame.display.update()
        
        
    def start(self):
        #---------------------Main Game Loop---------------------#
        while self.running:
        
            self.process_input()
    
            self.update_game()
            
            self.render()
            
            pygame.time.wait(100)


    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def update_game(self):
        pass
    
    @abstractmethod
    def render(self):
        pass