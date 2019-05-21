'''0.
Created on Jan 29, 2019
@author: Christian Ransom
'''
import pygame
import default_game
import menu

DEFAULT_SIZE = (500,500)

def main():
    
    #initialize the pygame module and sound
    #Sound needs to be initialized first to work properly
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    
    screen = pygame.display.set_mode((DEFAULT_SIZE), pygame.RESIZABLE)
    #default_game.Default_Game()
    menu.Menu(screen)
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()