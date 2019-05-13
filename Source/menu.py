from tkinter import *
from tkinter import ttk, simpledialog
import snake
import default_game
import sys
import tkinter.scrolledtext as tkst
from socket import *
from PIL import ImageTk,Image  

class Menu: 
    
    def __init__(self, game):
    
        self.root = Tk()
        self.game = game
        self.winner = False
        
        self.root.title("Snake")
        
        #self.build_score_display(self.root)
        
        self.get_player_name(self.root)
        #self.end_screen(self.root)
        
        #self.local_score_save(game)
        
        #self.save_score(mainframe)

        #self.display_score(mainframe)
        
       
        #self.root.after(1000, self.get_player_name)

        self.root.mainloop()
    
    
    def get_player_name(self, root):
        Label(root, text="Name").grid(row=0)
        
        self.e1 = Entry(root)
        
        self.e1.grid(row=0, column=1)
        self.e1.insert(END, self.game.player_name)
        
        submit_name_btn = ttk.Button(root, text="Enter", command=self.submit_player_name)
        submit_name_btn.grid(column=0, row=1)
        cancel_btn = ttk.Button(root, text="Skip", command=self.restart_game).grid(column=1, row=1)
        self.e1.focus_force()
        self.root.bind('<Return>', self.submit_player_name)

        
    def submit_player_name(self,  *args):
        self.game.player_name = self.e1.get()
            
        for child in self.root.winfo_children():
            child.destroy()
        self.build_score_display()
        

    #need args* paramater because its passed by tk for the input types of frames
    def restart_game(self, *args):
        try:
            print("making a new snake")
            self.root.unbind("<Return>")
            self.game.restart()
            self.root.destroy()
        except ValueError:
            pass
    
    def build_score_display(self):
        root = self.root
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        restart_button = ttk.Button(mainframe, text="Restart", command=self.restart_game).grid(column=2, row=1)
        quit_button = ttk.Button(mainframe, text="Quit", command=self.quit_game).grid(column=2, row=2)
        score = ttk.Label(mainframe, text = "Score: " + str(self.game.score), justify = CENTER).grid(column=2, row=3)
        
        if self.winner:
            canvas = Canvas(mainframe, width = 300, height = 300)
            canvas.grid(column=2, row=6)
            img = ImageTk.PhotoImage(Image.open("trophy.png"))
            canvas.create_image(20,20, anchor=NW, image=img)
        
        #mainframe.focus_force()
        
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.root.bind('<Return>', self.restart_game)
        
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
            player_name = self.game.player_name
            game_type = "Default"
            game_version = "1.2"
            extra = "File"
            
            score_message = message_type + "|" + str(self.game.score) + "|" + player_name + "|" + game_type + "|" + game_version + "|" + extra     
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
            
    def display_score(self, frame):
        score = ttk.Label(frame, text = "Your Rank: " + str(self.rank), justify = CENTER).grid(column=2, row=4)
        txt = tkst.ScrolledText(frame,width=40,height=10)
        txt.grid(column=2, row=5)
        top_ten = self.top_ten
        top_ten_list = top_ten.split(",", -1)
        
        temp = 1
        for i in top_ten_list[:-1]:
            txt.insert(INSERT, str(temp) + ": " + str(i) + "\n")
            temp = temp + 1
    
    def local_score_save(self, game):
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
            
            