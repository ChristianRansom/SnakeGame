'''
Created on Jan 29, 2019

@author: Christian Ransom
'''

class GameObject:
    
    def __init__(self, x_value, y_value):
        self.x = x_value
        self.y = y_value
        self.color = (255, 255, 255)
    
    def set_x(self, x_value):
        self.x = x_value
                
    def set_y(self, y_value):
        self.y = y_value

    def get_x(self):
        return self.x
                
    def get_y(self):
        return self.y
    
    def collide(self, other):
        return (self.x == other.x and self.y == other.y)
            