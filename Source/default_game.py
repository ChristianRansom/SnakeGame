'''
Created on Feb 4, 2019

@author: Christian Ransom
'''
from game import Game, GRID_SIZE
import snake
import snake_food
import pygame
import sys
import main
import thorpy

SNAKE_SIZE = 1
GAME_VERSION = 1.81
MAX_JUMP_COOLDOWN = 7

class Default_Game(Game):

    def __init__(self, screen, difficulty, player_name = ""):
        super(Default_Game, self).__init__(screen, difficulty)
        self.game_snake = snake.Snake(5, SNAKE_SIZE, 0, 0)
        self.food = snake_food.SnakeFood(SNAKE_SIZE, self.game_snake, self.tile_height, self.tile_width)
        self.player_name = player_name
        self.passthrough = True
        self.direction_lock = False
        self.score_multiplier = 1
        self.restart()
        self.multiplier_animation_life = 0
        self.start()

    def restart(self):
        self.game_snake = snake.Snake(5, SNAKE_SIZE, 0, 0)
        self.food.spawn_food(self.game_snake) #spawning food in random location not ontop of snake
        self.score = 0
        self.direction_lock = False
        self.direction = "east"
        self.score = 0
        self.eaten = False
        self.crashed = False
        self.jump_cooldown = 0
        self.set_up_thorpy()


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
                    if self.jump_cooldown <= 0:
                        self.game_snake.jumped = True
                        jump_sound = pygame.mixer.Sound(main.resource_path("Mario_Jumping-Mike_Koenig-989896458.wav"))
                        jump_sound.play()
            if event.type == pygame.VIDEORESIZE: #handle the window resizing
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.calc_tile_size()
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)
                
    def update_game(self):
        
        if self.game_snake.alive:
            if self.food.eaten:
                #if food is eaten, grow. This happens on the move after the food is first collided with
                self.food.spawn_food(self.game_snake)
                self.game_snake.grow(self.direction)
                if len(self.game_snake.q) % 10 == 0: #Snake length is divisible by 10 
                    self.increase_multiplier()
            else:  #Normal movement with nothing happening
                move_sound = pygame.mixer.Sound(main.resource_path("103336__fawfulgrox__low-bloop.wav"))
                move_sound.set_volume(.05)
                move_sound.play()
                self.game_snake.move(self.direction)
            if self.game_snake.jumped:
                self.jump_cooldown = MAX_JUMP_COOLDOWN
                
            self.detect_collisions()
            self.food.update(self.score_multiplier)
            self.direction_lock = False

    def increase_multiplier(self):
        self.score_multiplier += 1
        '''https://freesound.org/people/ProjectsU012/sounds/341695/'''
        multiplier_sound = pygame.mixer.Sound(main.resource_path("341695__projectsu012__coins-1.wav"))
        multiplier_sound.set_volume(.05)
        multiplier_sound.play()
        self.multiplier_animation_life = 15
        
    def detect_collisions(self):
        if self.game_snake.wall_collide():
            if self.passthrough == True:
                self.pass_through()
            else:
                self.game_over()
        if self.game_snake.self_collide():
            self.game_over()
        if self.game_snake.collide(self.food):
            #colliding with food
            self.score += int(self.food.get_score(self.score_multiplier))
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
        self.render_multiplier_animation()
        self.game_snake.render(self.screen, self.tile_height, self.tile_width)
        self.food.render(self.screen, self.tile_height, self.tile_width, self.score_multiplier)
        self.render_jump_cooldown()
        self.render_score()
        pygame.display.update()
    
    #create text and place in text box
    def render_score(self):
        bottom_offset = 20
        score_color = (0, 0, 0)
        basicfont = pygame.font.SysFont("Arial", 25)
        score_text = basicfont.render("Score: " + str(int(self.score)), True, score_color)
        score_rect = score_text.get_rect()
        score_rect.bottomright = self.screen.get_rect().bottomright
        score_rect.x = score_rect.x - self.screen.get_rect().right / 30
        score_rect.y -= bottom_offset
        self.screen.blit(score_text, score_rect)
        
        multiplier_text = basicfont.render(("Multiplier: " + str(self.score_multiplier)) + "x", True, score_color)
        multiplier_rect = multiplier_text.get_rect()
        multiplier_rect.bottomright = self.screen.get_rect().bottomright
        multiplier_rect.x = 0 + self.screen.get_rect().right / 30
        multiplier_rect.y -= bottom_offset
        
        length_text = basicfont.render(("Length: " + str(len(self.game_snake.q))), True, score_color)
        length_rect = length_text.get_rect()
        length_rect.bottomright = self.screen.get_rect().bottomright
        length_rect.x = 0 + self.screen.get_rect().right / 30
        length_rect.y -= (multiplier_rect.height + bottom_offset)
        self.screen.blit(length_text, length_rect)
        self.screen.blit(multiplier_text, multiplier_rect)
        
    def render_multiplier_animation(self):
        if self.multiplier_animation_life > 0: #how long to keep the score animation around
            self.multiplier_animation_life -= 1
            
            basicfont = pygame.font.SysFont("Arial", 50)
            multiplier_animation_color = (100, 100, 100)
            text = basicfont.render((str(int(self.score_multiplier)) + "x"), True, multiplier_animation_color)
            text_rect = text.get_rect()
            
            #Center it 
            w = self.tile_width * GRID_SIZE
            h = self.tile_height * GRID_SIZE
            
            text_rect.y = h // 2 - text_rect.width // 2
            text_rect.x = w // 2 - text_rect.height // 2
            
            self.screen.blit(text, text_rect)
    
    def render_jump_cooldown(self):
        if self.jump_cooldown >= 0:
            percent_left = (MAX_JUMP_COOLDOWN - self.jump_cooldown) / MAX_JUMP_COOLDOWN
            self.jump_bar.set_life(percent_left)
            self.jump_cooldown -= 1
        
        w, h = pygame.display.get_surface().get_size()
        self.jump_bar.surface = self.screen
        
        
        self.main_box.set_center((w // 2, h - 50))
        x = 0
        y = self.tile_height * GRID_SIZE
        width = self.tile_width * GRID_SIZE
        height = self.tile_height * 2
        self.main_box.set_size((width, height))
        
        self.jump_box.set_center((w // 2, h - 50))
        self.main_box.blit()
        self.main_box.update()

    def set_up_thorpy(self):
        self.jump_bar = thorpy.LifeBar("jump cool-down")
        self.jump_box = thorpy.Box([self.jump_bar])
        self.main_box = thorpy.Box([self.jump_box])
        #other_box = thorpy.Box()
        menu = thorpy.Menu(self.main_box)
        
        