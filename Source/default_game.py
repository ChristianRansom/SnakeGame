'''
Created on Feb 4, 2019

@author: Christian Ransom
Adpated and edited by Micaiah Christopher
'''
from game import Game
import snake
from snake import Snake
import snake_food
import menu
import pygame
import snake_power_up
import multi_food
from random import randint

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
        self.power_up = snake_power_up.SnakePower(pygame, SNAKE_SIZE, self.game_snake, 255, 0, 0)
        self.orange_food = snake_power_up.SnakePower(pygame, SNAKE_SIZE, self.game_snake, 255, 165, 0)
        self.slow_down = snake_power_up.SnakePower(pygame, SNAKE_SIZE, self.game_snake, 0, 0, 255)
        self.blue_zone = 0
        #self.speed = game
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False
        self.power = False
        self.power_spawn = False
        self.show_many = False
        self.red = False
        self.blue = False
        self.orange = False
        self.slow = False
        self.power_list = [0, 1, 2]
        self.power_index = 0
        self.choose_power = randint(0, 2)
        self.multi_list = self.multi_food_appear()

        print(len(self.multi_list))
        self.counter = randint(0, 5)
        self.game_snake.no_damage = False
        self.keys_list = self.game_snake.controls #grab the created snake objects control scheme
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
                self.food.spawn_food(pygame, self.game_snake)

                self.game_snake.grow(self.direction)
                self.eaten = False
            else:  
                move_sound = pygame.mixer.Sound("103336__fawfulgrox__low-bloop.wav")
                move_sound.set_volume(.05)
                move_sound.play()
                self.game_snake.move(self.direction)
            if self.game_snake.collide(self.food):
                eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                eat_sound.play()
                self.score = self.score + 100
                self.eaten = True
            elif self.game_snake.wall_collide(pygame):
                self.game_snake.die(pygame, self.screen)
                self.power = False
                self.red = False
                self.blue = False
                self.orange = False
                self.show_many = False
                self.power_index = 0
                self.game_speed = 10
                self.counter = randint(0, 5)
                self.render()
                my_menu = menu.Menu(self)
                print("YOU CRASHED!")
            elif self.game_snake.self_collide():
                self.game_snake.die(pygame, self.screen)
                self.power = False
                self.red = False
                self.blue = False
                self.orange = False
                self.show_many = False
                self.power_index = 0
                self.game_speed = 10
                self.counter = randint(0,5)
                self.render()
                my_menu = menu.Menu(self)
                print("You collided with yourself")
                #game_snake.move(direction)

            #if self.power:
                #self.power_up.spawn_power(pygame, self.game_snake)
                #self.power = False

            elif self.blue == True and self.game_snake.collide(self.slow_down):
                eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                eat_sound.play()
                self.game_speed = 3
                #self.power_spawn = False
                #self.power = True
                #self.blue = False
                self.slow = True
                self.counter = randint(0, 5)
                self.slow_down.spawn_power(pygame, self.game_snake)
                self.blue = False


            elif self.red == True and self.game_snake.collide(self.power_up):
                self.game_snake.shrink(self.direction)
                eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                eat_sound.play()
                #self.power = False
                self.power_spawn = False
                self.counter = randint(0,5)
                self.power_up.spawn_power(pygame, self.game_snake)
                self.red = False

            elif self.orange == True and self.game_snake.collide(self.orange_food):
                self.show_many = True
                self.orange = False
                eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                eat_sound.play()
                self.orange_food.spawn_power(pygame, self.game_snake)

            if self.show_many == True:
                i = 0

                while i < len(self.multi_list):

                    if self.game_snake.collide(self.multi_list[i]):
                        object = self.multi_list[i]
                        eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
                        eat_sound.play()
                        self.score = self.score + 20
                        self.game_snake.grow(self.direction)
                        self.multi_list.remove(object)
                    i += 1



        self.direction_lock = False
 
    def process_input(self): #Handle inp uts and events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and not self.direction_lock: 
                if event.key == self.keys_list[0] and self.direction != "east":
                    self.direction_lock = True
                    self.direction = "west"
                elif event.key == self.keys_list[1] and self.direction != "west":
                    self.direction_lock = True
                    self.direction = "east"
                elif event.key == self.keys_list[2] and self.direction != "north":
                    self.direction_lock = True
                    self.direction = "south"
                elif event.key == self.keys_list[3] and self.direction != "south":
                    self.direction_lock = True  
                    self.direction = "north"
                elif event.key == ord('p'):
                    pause_menu = menu.Menu(self)
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
        #self.slow_down.render(self.screen, pygame)

        if self.slow == True and self.counter > 90:
            self.game_speed = 10
            #self.power = False


        if self.red:
            print("red is rendered")
            self.blue = False
            self.orange = False
            self.power_up.render(self.screen, pygame)

        elif self.blue:
            print("blue is rendered")
            self.red = False
            self.orange = False
            self.slow_down.render(self.screen, pygame)

        elif self.orange:
            print("orange is rendered")
            self.blue = False
            self.red = False
            self.orange_food.render(self.screen, pygame)

        if self.show_many:
            for object in self.multi_list:
                object.render(self.screen, pygame)


        if len(self.multi_list) < 10 and self.show_many == False:
            self.multi_list = self.multi_food_appear()
            #self.show_many = False


        if 120 > self.counter >= 60 and self.power == False:

            selected_power = self.power_list[self.power_index]
            print("Selected power", selected_power)
            self.power = True

            if selected_power == 0:
                    #self.place_power()
                    self.counter += 1
                    #self.choose_power = randint(0, 2)
                    self.show_many = False
                    self.red = True
                    self.power_index = 1
            elif selected_power == 1:
                #self.show_many = True
                self.orange = True
                #self.choose_power = randint(0, 2)
                self.counter += 1
                self.power_index = 2

            elif selected_power == 2:
                print("2 was chosen")
                self.show_many = False
                self.blue = True
                self.counter += 20
                self.power_index = 0

        else:
            self.counter += 1

        if self.counter == 180:
            self.power = False
            self.red = False

            self.blue = False
            self.orange = False
            self.counter = randint(5, 10)

            self.show_many = False
            self.power_up.spawn_power(pygame, self.game_snake)
            self.orange_food.spawn_power(pygame, self.game_snake)
            self.slow_down.spawn_power(pygame, self.game_snake)
        pygame.display.update()

    def place_power(self):
        self.power_up.spawn_power(pygame, self.game_snake)
        self.power_spawn = True

    def multi_food_appear(self):
        list = []
        i = 0
        while i < 10:
            object = snake_power_up.SnakePower(pygame, SNAKE_SIZE, self.game_snake, 255, 165, 0)
            list.append(object)
            i += 1
        return list

    def choose_power(self):
        index = randint(1, 3)
        print(index)
        return index

    
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
        self.power_up.spawn_power(pygame, self.game_snake)
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False


