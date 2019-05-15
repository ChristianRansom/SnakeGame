'''
Created on Jan 31, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import snake_body
import random 
import game

class SnakeFood(GameObject):
    '''
    classdocs
    '''

    def __init__(self, pygame, size, a_snake, tile_height, tile_width, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        super().__init__(x_value, y_value, size)
        self.spawn_food(pygame, a_snake, tile_height, tile_width)
        self.food_color = (0,0,0)
    
    def render(self, screen, pygame, tile_height, tile_width):
        pygame.draw.rect(screen, self.food_color, (self.x * tile_height, self.y * tile_width, self.size * tile_height, self.size * tile_width), tile_height // 7)

    #This method doesn't create a new food. It just moves this food to a new random location 
    def spawn_food(self, pygame, snake, tile_height, tile_width):
        success = False
        #w, h = pygame.display.get_surface().get_size()
        while not success: #Keep trying to spawn new food until a free spot is found
            self.x = random.randrange(0, game.GRID_SIZE, 1)
            self.y = random.randrange(0, game.GRID_SIZE, 1)
            success = True
            for body in snake.q:
            #print("body location")
            #print(body.x)
            #print(body.y)
                if self.collide(body): #If we try and put food on the snake, we've failed
                    success = False

        
        
        
        