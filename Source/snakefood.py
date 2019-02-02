'''
Created on Jan 31, 2019

@author: Christian Ransom
'''
from gameobject import GameObject
import snakebody
import random 
foodColor = (0,0,0)

class SnakeFood(GameObject):
    '''
    classdocs
    '''


    def __init__(self, pygame, xValue = -1000, yValue = -1000):
        '''
        Constructor
        '''
        super().__init__(xValue, yValue)
        self.spawnFood(pygame)
    
    def render(self, screen, pygame):
        global foodColor
        pygame.draw.rect(screen, foodColor, (self.x, self.y,10,10), 3)
        
    #This method doesn't create a new food. It just moves this food to a new random location 
    def spawnFood(self, pygame):
        w, h = pygame.display.get_surface().get_size()
        tilesHeight = h / snakebody.SNAKE_BODY_SIZE
        tilesWidth = w / snakebody.SNAKE_BODY_SIZE
        print("tilesw and tilesh ")
        print(tilesWidth)
        print(tilesHeight)
        print("random location spawn")
        
        
        self.x = random.randrange(0, h + 1, 10)
        self.y = random.randrange(0, w + 1, 10)

        print("self x and y")
        print(self.x)
        print(self.y)
        
        
        
        