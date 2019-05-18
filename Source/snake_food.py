'''
Created on Jan 31, 2019

@author: Christian Ransom
'''
from game_object import GameObject
import random 
import game
import pygame

MAX_POINTS = 200 #Max points that can be gotten
MIN_POINTS = 50 #Minimum of points after the full decay time has happened
DECAY_START = 20 #The average amount of decay that should happen each move 
DECAY_FACTOR = .5 #How much higher does the score decrement start as a factor of the decay base
GRACE_PERIOD = 8 #number of moves before food starts to decay

class SnakeFood(GameObject):

    def __init__(self, size, a_snake, tile_height, tile_width, x_value = -1000, y_value = -1000):
        '''
        Constructor
        '''
        super().__init__(x_value, y_value, size)
        self.spawn_food(a_snake)
        self.score_animation_life = 0
        self.animation_score = 0
        self.animation_x = 0
        self.animation_y = 0
        self.reset_food()
        #Spread the color change over the decay time
        self.color_change = 255 // (DECAY_START * DECAY_FACTOR)
        
    def reset_food(self):
        self.food_color = (0,0,0)
        self.score = MAX_POINTS
        self.score_decrement = DECAY_START
        self.age = 0
        self.eaten = False 

    def update(self):
        self.age += 1
        if self.age > GRACE_PERIOD:
            if self.score - self.score_decrement >= MIN_POINTS: 
                self.score -= self.score_decrement
            else:
                self.score = MIN_POINTS
            if self.score_decrement - DECAY_FACTOR > 0:
                self.score_decrement -= DECAY_FACTOR
                
        if self.eaten:
            self.score_animation_life = 10
            self.animation_score = self.score
            self.animation_x = self.x
            self.animation_y = self.y

    def render(self, screen, tile_height, tile_width):
        if self.age > GRACE_PERIOD and self.score - self.score_decrement >= MIN_POINTS:
            if self.food_color[0] + self.color_change < 255: #Max color change
                color_change = self.food_color[0] + self.color_change
                self.food_color = (color_change, color_change, 0)
        
        if self.eaten: #Save location of eaten food to display score text
            self.score_animation_life = 10
            self.animation_score = self.score
            self.animation_x = self.x
            self.animation_y = self.y
        
        if self.score_animation_life > 0: #how long to keep the score animation around
            self.render_food_points(screen, tile_height, tile_width)
            self.score_animation_life = self.score_animation_life - 1
        
        pygame.draw.rect(screen, self.food_color, (self.x * tile_height, self.y * tile_width, self.size * tile_height, self.size * tile_width), tile_height // 7)
     
    def spawn_food(self, snake):
        #This method doesn't create a new food. It just moves this food to a new random location
        success = False
        while not success: #Keep trying to spawn new food until a free spot is found
            self.x = random.randrange(0, game.GRID_SIZE, 1)
            self.y = random.randrange(0, game.GRID_SIZE, 1)
            success = True
            for body in snake.q:
                if self.collide(body): #If we try and put food on the snake, we've failed
                    success = False
        self.reset_food()
    
    def render_food_points(self, screen, tile_height, tile_width):
        basicfont = pygame.font.SysFont(None, 30)
        score_color = (255, 255, 255)
        if self.animation_score == 200:
            score_color = (255, 255, 0)
        text = basicfont.render(str(int(self.animation_score)), True, (100, 100, 100), score_color)
        text_rect = text.get_rect()
        
        text_rect.x = self.animation_x * tile_height
        text_rect.y = self.animation_y * tile_width
        screen.blit(text, text_rect)
        
        
        