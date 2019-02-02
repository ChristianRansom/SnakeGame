'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from gameobject import GameObject

bodyColor = (0,0,128)
SNAKE_BODY_SIZE = 10

class SnakeBody(GameObject):
    '''
    classdocs
    '''



    #spawns off screen by default
    def __init__(self, xValue = -1000, yValue = -1000):
        '''
        Constructor
        '''
        global SNAKE_BODY_SIZE
        self.bodyColor = SNAKE_BODY_SIZE
        self.SNAKE_BODY_SIZE = 10
        super().__init__(xValue, yValue)
        
    def render(self, screen, pygame):
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y,10,10), 3)

        
    
        