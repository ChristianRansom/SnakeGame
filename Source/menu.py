from tkinter import *
from tkinter import ttk
import snake
import default_game
import sys

class Menu: 
    
    def __init__(self, game):
        
        self.default_game = game
        self.root = Tk()
        self.root.title("Feet to Meters")
        try:
            score_file = open("HighScore.txt", "r")
        except FileNotFoundError:
            score_file = open("HighScore.txt", "w") #creates the file if it doesn't exist
            score_file.write(str(game.score))
            high_score = game.score
        else:
            old_score = score_file.read()
            score_file.close() #close the read version of the file
            
            print("old score: " + old_score)
            if int(old_score) < game.score:
                score_file = open("HighScore.txt", "w")
                high_score = str(game.score)
                score_file.write(str(game.score))
            else:
                high_score = old_score
                 
        score_file.close()
        
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        
        restart_button = ttk.Button(mainframe, text="Restart", command=self.restart_game).grid(column=2, row=1)
        quit_button = ttk.Button(mainframe, text="Quit", command=self.quit_game).grid(column=2, row=2)
        score = ttk.Label(mainframe, text = "Score: " + str(game.score), justify = CENTER).grid(column=2, row=3)
        score = ttk.Label(mainframe, text = "High Score: " + str(high_score), justify = CENTER).grid(column=2, row=4)

        mainframe.focus_force()
        
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.root.bind('<Return>', self.restart_game)
        self.root.mainloop()
        
    #need args* paramater because its passed by tk for the input types of frames
    def restart_game(self, *args):
        try:
            print("making a new snake")
            self.root.unbind("<Return>")
            self.default_game.restart()
            self.root.destroy()
        except ValueError:
            pass
        
    def quit_game(self):
        sys.exit(0)

     
    