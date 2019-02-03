'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from game_object import GameObject


class SnakeBody(GameObject):
    '''
    classdocs
    '''

    #spawns off screen by default
    def __init__(self, size, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        super().__init__(x_value, y_value, size)
    
    
    def render(self, screen, pygame, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size), 3)

    
        