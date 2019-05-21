'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from game import Game, GRID_SIZE
import snake
from snake import Snake
import snake_food
import menu
import pygame

SNAKE_SIZE = 1
GAME_VERSION = 1.6

class Default_Game(Game):

    def __init__(self, screen):
        super(Default_Game, self).__init__(screen)
        self.game_snake = snake.Snake(3, SNAKE_SIZE, 0, 0)
        self.food = snake_food.SnakeFood(SNAKE_SIZE, self.game_snake, self.tile_height, self.tile_width)
        self.player_name = ""
        self.passthrough = True
        self.direction_lock = False

        self.restart()

        self.start()

    def restart(self):
        self.game_snake = snake.Snake(6, SNAKE_SIZE, 0, 0)
        self.food.spawn_food(self.game_snake)
        self.score = 0
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False
        self.crashed = False


    def process_input(self): #Handle inputs and events
        self.game_snake.jumped = False
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
                elif event.key == pygame.K_SPACE:
                    self.game_snake.jumped = True
            if event.type == pygame.VIDEORESIZE: #handle the window resizing
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.calc_tile_size()
            if event.type == pygame.QUIT:
                self.running = False
                
    def update_game(self):
        
        if self.game_snake.alive:
            if self.food.eaten:
                #if food is eaten, grow. This happens on the move after the food is first collided with
                self.food.spawn_food(self.game_snake)
                self.game_snake.grow(self.direction)
            else:  #Normal movement with nothing happening
                move_sound = pygame.mixer.Sound("103336__fawfulgrox__low-bloop.wav")
                move_sound.set_volume(.05)
                move_sound.play()
                self.game_snake.move(self.direction)
                
            self.detect_collisions()
            self.food.update()
            self.direction_lock = False

    def detect_collisions(self):
        if self.game_snake.wall_collide():
            if self.passthrough == True:
                self.pass_through()
            else:
                self.game_over()
        elif self.game_snake.self_collide():
            self.game_over()
        if self.game_snake.collide(self.food):
            #colliding with food
            eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
            eat_sound.play()
            self.score += int(self.food.score)
            self.food.eaten = True
            
    def game_over(self):
        self.game_snake.die()
        self.render()
        self.running = False
        print("You crashed")
    
    def pass_through(self):
        tail = self.game_snake.q.popleft()
        #print("x " + str(self.game_snake.head.x))
        #print("y " + str(self.game_snake.head.y))
        #right side case
        if self.game_snake.head.x >= GRID_SIZE:
            tail.x = 0
            tail.y = self.game_snake.head.y 
            #now set to the passthrough ^^^

        #left side case
        if self.game_snake.head.x < 0:
            tail.x = GRID_SIZE - 1
            tail.y = self.game_snake.head.y 
            #now set to the passthrough ^^^
          
        #top side case
        if self.game_snake.head.y < 0:
            tail.y = GRID_SIZE - 1
            tail.x = self.game_snake.head.x
            #now set to the passthrough ^^^
       
        #bottom side case
        if self.game_snake.head.y >= GRID_SIZE:
            tail.x = self.game_snake.head.x
            tail.y = 0 
            #now set to the passthrough ^^^
      
        #attach head to tale and the rest will follow
        self.game_snake.head = tail
        self.game_snake.q.append(tail)
        
    def render(self):
        white = (255,255,255)
        self.screen.fill(white)
        self.render_score()
        self.game_snake.render(self.screen, self.tile_height, self.tile_width)
        self.food.render(self.screen, self.tile_height, self.tile_width)
        pygame.display.update()
    
    #create text and place in text box
    def render_score(self):
        basicfont = pygame.font.SysFont(None, 30)
        text = basicfont.render(str(self.score), True, (100, 100, 100), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.bottomright = self.screen.get_rect().bottomright
        text_rect.x = text_rect.x - self.screen.get_rect().right / 30
        self.screen.blit(text, text_rect)
