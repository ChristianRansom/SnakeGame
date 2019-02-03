'''
Created on Jan 29, 2019

@author: Christian Ransom
'''

class GameObject:
    
    def __init__(self, x_value, y_value):
        self.x = x_value
        self.y = y_value
        self.color = (255, 255, 255)
    
    def collide(self, other):
        return (self.x == other.x and self.y == other.y)
            