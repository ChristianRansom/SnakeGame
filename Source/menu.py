from tkinter import *
from tkinter import ttk
import snake
import default_game
import sys
import tkinter.scrolledtext as tkst
from socket import *
import pickle
from PIL import ImageTk,Image  

class Menu: 
    
    def __init__(self, game):
        
        self.default_game = game
        self.root = Tk()
        self.root.title("Snake")
        self.winner = False
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
        #score = ttk.Label(mainframe, text = "High Score: " + str(high_score), justify = CENTER).grid(column=2, row=4)
        
        
        self.save_score(mainframe)
        

        
        self.display_score(mainframe)
        
        if self.winner:
            canvas = Canvas(mainframe, width = 300, height = 300)
            canvas.grid(column=2, row=6)
            img = ImageTk.PhotoImage(Image.open("trophy.png"))
            canvas.create_image(20,20, anchor=NW, image=img)
        
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

     
    def save_score(self, mainframe):
        try:
            server_name = '165.227.51.19' #My server
            #server_name = '157.230.131.10' #Micaiah's server
            serverPort = 10000
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((server_name, serverPort))
            
            message_type = "Submit Score"
            player_name = "Christian_Ransom"
            game_type = "Default"
            game_version = "1.0"
            extra = "File"
            
            score_message = message_type + "|" + str(self.default_game.score) + "|" + player_name + "|" + game_type + "|" + game_version + "|" + extra     
            print(score_message)
            clientSocket.send(score_message.encode()) #Send score info
            modifiedSentence = clientSocket.recv(1024) #receive reply 
            reply = modifiedSentence.decode()
            arguments = reply.split("|", -1)
            #print(arguments)
            print('From Server: ', reply)
            self.rank = arguments[1]
            self.top_ten = arguments[2]
            

            
            if arguments[3] == "True": #The player won the game
                print("You won, waiting to recieve file")
                file = self.recieve_file(clientSocket)
                self.winner = True
                #self.display_image(mainframe, file)
            
            clientSocket.close()
        except ConnectionRefusedError:
            self.rank = "Error"
            self.top_ten = "Error"
            print("Error connecting or communicating to the score database server")
            
    def display_score(self, mainframe):
        score = ttk.Label(mainframe, text = "Your Rank: " + str(self.rank), justify = CENTER).grid(column=2, row=4)
        txt = tkst.ScrolledText(mainframe,width=40,height=10)
        txt.grid(column=2, row=5)
        top_ten = self.top_ten
        top_ten_list = top_ten.split(",", -1)
        
        temp = 1
        for i in top_ten_list[:-1]:
            txt.insert(INSERT, str(temp) + ": " + str(i) + "\n")
            temp = temp + 1
    

    def recieve_file(self, s):
        ''' inspired by 
        https://stackoverflow.com/questions/35363975/sending-a-file-over-tcp-sockets
        '''
        f = open('trophy.png', 'wb')
        l = s.recv(4096)
        print("Recieving...")
        while (l):
            print("Recieving...")
            f.write(l)
            l = s.recv(4096)
        f.close()
        print('Done receiving')
        return f

    ''' Multi-threading inspired by 
    https://scorython.wordpress.com/2016/06/27/multithreading-with-tkinter/
    '''
            
            