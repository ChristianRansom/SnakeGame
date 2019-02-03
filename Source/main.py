'''
Created on Jan 29, 2019
@author: Christian Ransom
'''
# import the pygame module, so you can use it
import pygame
import snake
from snake import Snake
import snake_food

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((240,240))
direction = "east"
direction_lock = False
game_snake = Snake()
score = 0
running = True
eaten = False
SNAKE_SIZE = 20
food = 0

# define a main function
def main():

    global direction_lock, game_snake, running, food
    # initialize the pygame module
    # load and set the logo
    logo = pygame.image.load("SnakeIcon.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("SNAKE")
     
    # create a surface on screen 
    white = (255,255,255)
    screen.fill(white)
    #pygame.draw.rect(screen, (0,0,0), (10,10,10,10), 3)
    pygame.display.update()
    # define a variable to control the main loop
    
    game_snake = snake.Snake(3, SNAKE_SIZE, 0, 0)
    food = snake_food.SnakeFood(pygame, SNAKE_SIZE, game_snake)

    #--------------Main Game Loop-----------------------#
    while running:
        
        process_input()

        update_game()
        
        render()
        
        pygame.time.wait(100)

def update_game():
    ''' 
    if food eaten then handle food eaten
        place new snake_body at next move direction
    else
        move tail to next move direction 
        
    '''
    global direction, direction_lock, game_snake, score, eaten
    if game_snake.alive:
        if eaten:
            food.spawn_food(pygame, game_snake)
            game_snake.grow(direction)
            eaten = False
        else:  
            game_snake.move(direction)
        if game_snake.collide(food):
            eat_sound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
            eat_sound.play()
            score = score + 100
            eaten = True
        elif game_snake.wall_collide(pygame):
            game_snake.die(pygame)
            print("YOU CRASHED!")
        elif game_snake.self_collide():
            game_snake.die(pygame)
            print("You collided with yourself")
            #game_snake.move(direction)
        
    direction_lock = False


def process_input(): #Handle inputs and events
    global direction, running, direction_lock
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and not direction_lock: 
            if event.key == pygame.K_LEFT and direction != "east":
                direction_lock = True
                direction = "west"
            elif event.key == pygame.K_RIGHT and direction != "west":
                direction_lock = True
                direction = "east"
            elif event.key == pygame.K_DOWN and direction != "north":
                direction_lock = True
                direction = "south"
            elif event.key == pygame.K_UP and direction != "south":
                direction_lock = True  
                direction = "north"
                
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

def render():
    global game_snake, food, score, pygame
    white = (255,255,255)
    screen.fill(white)
    render_score()
    game_snake.render(screen, pygame)
    food.render(screen, pygame)
    pygame.display.update()
    
    
def render_score():
    global score, pygame
    basicfont = pygame.font.SysFont(None, 30)
    text = basicfont.render(str(score), True, (100, 100, 100), (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.bottomright = screen.get_rect().bottomright
    text_rect.x = text_rect.x - screen.get_rect().right / 30
    screen.blit(text, text_rect)
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()


