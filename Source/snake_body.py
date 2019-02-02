'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from game_object import GameObject

SNAKE_BODY_SIZE = 10

class SnakeBody(GameObject):
    '''
    classdocs
    '''

    #spawns off screen by default
    def __init__(self, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        global SNAKE_BODY_SIZE 
        self.SNAKE_BODY_SIZE = SNAKE_BODY_SIZE
        super().__init__(x_value, y_value)
    
    
    def render(self, screen, pygame, color):
        global SNAKE_BODY_SIZE
        pygame.draw.rect(screen, color, (self.x, self.y,SNAKE_BODY_SIZE,SNAKE_BODY_SIZE), 3)

    
        