'''
Created on Jan 29, 2019

@author: Christian Ransom
'''
# import the pygame module, so you can use it
import pygame
import snake
from collections import deque
from snake import Snake
import snakefood

pygame.init()
screen = pygame.display.set_mode((300,300))
direction = "east"
directionLock = False
mySnake = Snake(0, 0, 0)
food = snakefood.SnakeFood(pygame)
score = 0
running = True

# define a main function
def main():

    global directionLock, mySnake, running
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
        
    mySnake = snake.Snake(10, 50, 50)

    #--------------Main Game Loop-----------------------#
    while running:
        updateGame()
        
        render()
        
        pygame.time.wait(100)
        
        processInput()
        
    
def updateGame():
    #print("updating")
    ''' 
    if food eaten then handle food eaten
        place new snakebody at next move direction
    else
        move tail to next move direction 
        
    '''
    global direction, directionLock, mySnake, score
    if mySnake.collide(food):
        food.spawnFood(pygame)
        mySnake.grow(direction)
        score = score + 100
    elif mySnake.wallCollide(pygame):
        mySnake.die()
        print("YOU CRASHED!")
        pass #handle this somehow later when we have a menu and restart stuff 
    elif mySnake.selfCollide():
        print("You collided with yourself")
        #mySnake.move(direction)
    else:
        mySnake.move(direction)
        
    directionLock = False
    

#do something cool

def resetDirections():
    global directionLock
    directionLock = True

def processInput(): #Handle inputs and events
    global direction, running
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and not directionLock: 
            if event.key == pygame.K_LEFT and direction != "east":
                resetDirections()
                direction = "west"
            elif event.key == pygame.K_RIGHT and direction != "west":
                resetDirections()
                direction = "east"
            elif event.key == pygame.K_DOWN and direction != "north":
                resetDirections()
                direction = "south"
            elif event.key == pygame.K_UP and direction != "south":
                resetDirections()   
                direction = "north"
                
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

def render():
    global mySnake, food, score,pygame
    white = (255,255,255)
    screen.fill(white)
    renderScore()
    mySnake.render(screen, pygame)
    food.render(screen, pygame)
    pygame.display.update()
    
    
def renderScore():
    global score, pygame
    basicfont = pygame.font.SysFont(None, 30)
    text = basicfont.render(str(score), True, (100, 100, 100), (255, 255, 255))
    textrect = text.get_rect()
    textrect.bottomright = screen.get_rect().bottomright
    textrect.x = textrect.x - screen.get_rect().right / 30
    screen.blit(text, textrect)
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()


