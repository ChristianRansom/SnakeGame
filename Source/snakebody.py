'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from gameobject import GameObject

bodyColor = (0,128,0)
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
        global bodyColor, SNAKE_BODY_SIZE
        self.bodyColor = bodyColor
        self.SNAKE_BODY_SIZE = SNAKE_BODY_SIZE
        super().__init__(xValue, yValue)
        
    def render(self, screen, pygame):
        global SNAKE_BODY_SIZE, bodyColor
        pygame.draw.rect(screen, bodyColor, (self.x, self.y,SNAKE_BODY_SIZE,SNAKE_BODY_SIZE), 3)

        
    
        