'''
Created on Jan 29, 2019

@author: Christian Ransom
'''

class GameObject:
    
    def __init__(self, x_value, y_value, a_size):
        self.x = x_value
        self.y = y_value
        self.size = a_size
        self.color = (0, 0, 0)
    
    def collide(self, other):
        return (self.x == other.x and self.y == other.y)
            