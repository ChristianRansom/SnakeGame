'''
Created on Jan 31, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import random 

class SnakeFood(GameObject):
    '''
    classdocs
    '''

    def __init__(self, pygame, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        super().__init__(x_value, y_value)
        self.spawn_food(pygame)
        self.food_color = (0,0,0)
    
    def render(self, screen, pygame):
        pygame.draw.rect(screen, self.food_color, (self.x, self.y,10,10), 3)
        
    #This method doesn't create a new food. It just moves this food to a new random location 
    def spawn_food(self, pygame):
        w, h = pygame.display.get_surface().get_size()
        self.x = random.randrange(0, h - 10, 10)
        self.y = random.randrange(0, w - 10, 10)
        #print("self x and y")
        #print(self.x)
        #print(self.y)
        
        
        
        