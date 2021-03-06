'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import game
import pygame

class SnakeBody(GameObject):
    '''
    classdocs
    '''

    #spawns off screen by default
    def __init__(self, size, x_value = -1000, y_value = -1000):
        '''
        size is relative to tile size 
        Constructor
        '''
        super(SnakeBody, self).__init__(x_value, y_value, size)
        self.color = (0,128,0) #Green
    
    
    def render(self, screen, color, tile_width, tile_height):
        '''tile width and height are how big the squares are on the screen grid are
        self.size Allows a body to render bigger or smaller than a tile size
        self x and y refer to which tile, not the pixel'''
        
        center_x = self.x * tile_width + tile_width // 2
        center_y = self.y * tile_height + tile_height // 2
        
        super().render(screen, color, center_x, center_y, self.size * tile_width, self.size * tile_height, tile_height // 7)
        

    
        