'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import game


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
    
    
    def render(self, screen, pygame, color, tile_height, tile_width):
        #Tile size is how big the squares are on the screen grid
        #self.size Allows a body to render bigger or smaller than a tile size
        #self x and y refer to which tile, not the pixel
        pygame.draw.rect(screen, color, (self.x * tile_height, self.y * tile_width, self.size * tile_height, self.size * tile_width), tile_height // 7)

    
        