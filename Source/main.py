'''0.
Created on Jan 29, 2019
@author: Christian Ransom
'''
import pygame
import menu
import sys
import os

DEFAULT_SIZE = (500,600)
#50 extra for the game info bar 

def main():
    
    #initialize the pygame module and sound
    #Sound needs to be initialized first to work properly
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    
    screen = pygame.display.set_mode((DEFAULT_SIZE), pygame.RESIZABLE)
    #default_game.Default_Game()
    menu.Menu(screen)

def resource_path(relative_path):
    """ Get absolute path to resource. Required for PyInstaller to build in one file"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.getcwd())
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()