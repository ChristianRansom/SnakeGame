'''0.
Created on Jan 29, 2019
@author: Christian Ransom
'''
# import the pygame module, so you can use it
import pygame
import default_game
 
# define a main function
def main():
    
    #initialize the pygame module and sound
    #Sound needs to be initialized first to work properly
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    default_game.Default_Game()
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()