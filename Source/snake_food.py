'''
Created on Jan 31, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import snake_body
import random 

class SnakeFood(GameObject):
    '''
    classdocs
    '''

    def __init__(self, pygame, size, a_snake, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        super().__init__(x_value, y_value, size)
        self.spawn_food(pygame, a_snake)
        self.food_color = (0,0,0)
    
    def render(self, screen, pygame):
        pygame.draw.rect(screen, self.food_color, (self.x, self.y, self.size, self.size), 3)
        
    #This method doesn't create a new food. It just moves this food to a new random location 
    def spawn_food(self, pygame, snake):
        success = False
        w, h = pygame.display.get_surface().get_size()
        while not success: #Keep trying to spawn new food until a free spot is found
            self.x = random.randrange(0, h - self.size, self.size)
            self.y = random.randrange(0, w - self.size, self.size)
            success = True
            for body in snake.q:
            #print("body location")
            #print(body.x)
            #print(body.y)
                if self.collide(body): #If we try and put food on the snake, we've failed
                    success = False



        
        
        