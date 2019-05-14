'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from game import Game
import snake
from snake import Snake
import snake_food
import menu
import pygame
import copy

SNAKE_SIZE = 20

class Default_Game(Game):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.game_snake = snake.Snake(3, SNAKE_SIZE, 0, 0)
        self.food = snake_food.SnakeFood(pygame, SNAKE_SIZE, self.game_snake)
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False
        #set default for passing through walls
        self.passthrough = True
        #set default for crash checker
        self.crashed = False
        print(self.passthrough)
        self.start()


    def update_game(self):
        ''' 
        if food eaten then handle food eaten
            place new snake_body at next move direction
        else
            move tail to next move direction 
                
        '''
        if self.game_snake.alive:
            if self.eaten:
                #if food is eaten, grow
                self.food.spawn_food(pygame, self.game_snake)
                self.game_snake.grow(self.direction)
                self.eaten = False
            else:  
                move_sound = pygame.mixer.Sound("103336__fawfulgrox__low-bloop.wav")
                move_sound.set_volume(.05)
                move_sound.play()
                self.game_snake.move(self.direction)
            if self.game_snake.collide(self.food):
                #colliding with food
                eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                eat_sound.play()
                self.score = self.score + 100
                self.eaten = True
            elif self.game_snake.wall_collide(pygame):
                #MAIN
                #printing out the x and y coordiantes 
                if self.passthrough == True:
                    self.pass_through()
                else:
                    print("you crashed")
                    self.game_snake.die(pygame, self.screen)
                    self.render()
                    #set crashed to false so that it only states once and stops loop
                    my_menu = menu.Menu(self)
                
            elif self.game_snake.self_collide():
                self.game_snake.die(pygame, self.screen)
                self.render()
                my_menu = menu.Menu(self)
                print("You collided with yourself")

        self.direction_lock = False

    def pass_through(self):
        #number of squares 
        w, h = pygame.display.get_surface().get_size()
        tail = self.game_snake.q.popleft()
        
        #right side case
        if self.game_snake.head.x >= w:
            tail.x = 0
            tail.y = self.game_snake.head.y 
            #now set to the passthrough ^^^

        #left side case
        if self.game_snake.head.x < 0:
            tail.x = w - tail.size
            tail.y = self.game_snake.head.y 
            #now set to the passthrough ^^^
          
        #top side case
        if self.game_snake.head.y < 0:
            tail.y = h - tail.size
            tail.x = self.game_snake.head.x
            #now set to the passthrough ^^^
       
        #bottom side case
        if self.game_snake.head.y >= h:
            tail.x = self.game_snake.head.x
            tail.y = 0 
            #now set to the passthrough ^^^
      
        #attach head to tale and the rest will follow
        self.game_snake.head = copy.copy(tail)
        self.game_snake.q.append(tail)
        
    def process_input(self): #Handle inputs and events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and not self.direction_lock: 
                if event.key == pygame.K_LEFT and self.direction != "east":
                    self.direction_lock = True
                    self.direction = "west"
                elif event.key == pygame.K_RIGHT and self.direction != "west":
                    self.direction_lock = True
                    self.direction = "east"
                elif event.key == pygame.K_DOWN and self.direction != "north":
                    self.direction_lock = True
                    self.direction = "south"
                elif event.key == pygame.K_UP and self.direction != "south":
                    self.direction_lock = True  
                    self.direction = "north"
                    
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.running = False

    def render(self):
        white = (255,255,255)
        self.screen.fill(white)
        self.render_score()
        self.game_snake.render(self.screen, pygame)
        self.food.render(self.screen, pygame)
        pygame.display.update()
    
    #create text and place in text box
    def render_score(self):
        basicfont = pygame.font.SysFont(None, 30)
        text = basicfont.render(str(self.score), True, (100, 100, 100), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.bottomright = self.screen.get_rect().bottomright
        text_rect.x = text_rect.x - self.screen.get_rect().right / 30
        self.screen.blit(text, text_rect)
        
    def restart(self):
        self.game_snake = snake.Snake(3, SNAKE_SIZE, 0, 0)
        self.food.spawn_food(pygame, self.game_snake)
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False


