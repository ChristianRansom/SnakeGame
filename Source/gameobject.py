'''
Created on Jan 29, 2019

@author: Christian Ransom
'''

class GameObject:

    
    def __init__(self, xValue, yValue):
        self.x = xValue
        self.y = yValue
        self.color = (255, 255, 255)
    
    def setX(self, xValue):
        self.x = xValue
                
    def setY(self, xYalue):
        self.y = xYalue

    def getX(self):
        return self.x
                
    def getY(self):
        return self.y