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
        self.collider = True
    
    def collide(self, other):
        if self.collider and other.collider:
            return (self.x == other.x and self.y == other.y)
        return False
            