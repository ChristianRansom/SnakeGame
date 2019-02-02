'''
Created on Jan 29, 2019
@author: Christian Ransom
'''
# import the pygame module, so you can use it
import pygame
import snake
from snake import Snake
import snake_food

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((300,300))
direction = "east"
direction_lock = False
game_snake = Snake(0, 0, 0)
food = snake_food.SnakeFood(pygame)
score = 0
running = True

# define a main function
def main():

    global direction_lock, game_snake, running
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
    
    game_snake = snake.Snake(3, 50, 50)

    #--------------Main Game Loop-----------------------#
    while running:
        update_game()
        
        render()
        
        pygame.time.wait(100)
        
        process_input()
        

def update_game():
    #print("updating")
    ''' 
    if food eaten then handle food eaten
        place new snake_body at next move direction
    else
        move tail to next move direction 
        
    '''
    global direction, direction_lock, game_snake, score
    if game_snake.alive:
        if game_snake.collide(food):
            deathSound = pygame.mixer.Sound("GUI Sound Effects_038.wav")
            deathSound.play()
            food.spawn_food(pygame)
            game_snake.grow(direction)
            score = score + 100
        elif game_snake.wall_collide(pygame):
            game_snake.die(pygame)
            print("YOU CRASHED!")
            pass #handle this somehow later when we have a menu and restart stuff 
        elif game_snake.self_collide():
            game_snake.die(pygame)
            print("You collided with yourself")
            #game_snake.move(direction)
        else:
            game_snake.move(direction)
        
    direction_lock = False

#do something cool
def reset_directions():
    global direction_lock
    direction_lock = True

def process_input(): #Handle inputs and events
    global direction, running
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and not direction_lock: 
            if event.key == pygame.K_LEFT and direction != "east":
                reset_directions()
                direction = "west"
            elif event.key == pygame.K_RIGHT and direction != "west":
                reset_directions()
                direction = "east"
            elif event.key == pygame.K_DOWN and direction != "north":
                reset_directions()
                direction = "south"
            elif event.key == pygame.K_UP and direction != "south":
                reset_directions()   
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


