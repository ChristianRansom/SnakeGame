from tkinter import *
from tkinter import ttk, simpledialog
import default_game
import tkinter.scrolledtext as tkst
from socket import *
from PIL import ImageTk,Image
import threading
import queue
import pygame
import thorpy
import main

class Menu: 
    
    def __init__(self, game):
    
        self.root = Tk() #Could swap this to a frame or something
        self.game = game
        self.winner = False
        
        self.root.title("Snake")
        
        self.get_player_name(self.root)
        
        self.root.mainloop()
    
    def get_player_name(self, root):
        #A gui for the user to input their name before the score is saved and rank displayed
        Label(root, text="Name").grid(row=0)
        
        self.e1 = Entry(root)
        
        self.e1.grid(row=0, column=1)
        self.e1.insert(END, self.game.player_name)
        
        submit_name_btn = ttk.Button(root, text="Enter", command=self.submit_player_name)
        submit_name_btn.grid(column=0, row=2, columnspan=2)
        self.e1.focus_force()
        self.root.bind('<Return>', self.submit_player_name)

    #need args* paramater because its passed by tk for the input types of frames
    def submit_player_name(self, *args):
        #submits the player name to save the score and display ranking info
        name_input = self.e1.get()
        if(name_input == "" or ' ' in name_input or ',' in name_input): #checks for valid name name_input
            Label(self.root, text="Name cannot be empty, contain spaces, or contain commas").grid(row=1, columnspan=2)
        else:
            self.game.player_name = name_input
            for child in self.root.winfo_children():
                child.destroy()
            
            self.save_score_thread() #start saving score in a separate thread

            self.build_score_display()
    
    def save_score_thread(self):
        '''Multi threading inspired by 
        https://scorython.wordpress.com/2016/06/27/multithreading-with-tkinter/
        '''
        self.new_thread = None
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.save_score)
        self.new_thread.start()
        self.root.after(100, self.listen_for_result)

    def listen_for_result(self):
        '''
        Check if there is something in the queue
        '''
        try:
            self.res = self.thread_queue.get(0)
            #self.mylabel.config(text='Loop terminated')
            
            self.display_rankings(self.root)

            if self.winner:
                canvas = Canvas(self.root, width = 300, height = 300)
                canvas.grid(column=2, row=6)
                img = ImageTk.PhotoImage(Image.open("trophy.png"))
                canvas.create_image(20,20, anchor=NW, image=img)
        except queue.Empty:
            #Continues to check if the save_score thread is finished
            self.root.after(100, self.listen_for_result) 
            
        
    def build_score_display(self):
        #Displays the main end screen buttons and information 
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        ttk.Button(self.root, text="Restart", command=self.restart_game).grid(column=2, row=1)
        ttk.Button(self.root, text="Quit", command=self.quit_game).grid(column=2, row=2)
        ttk.Label(self.root, text = "Score: " + str(self.game.score), justify = CENTER).grid(column=2, row=3)
        self.loading_label = ttk.Label(self.root, text = "Loading Rankings... ", justify = CENTER)
        self.loading_label.grid(column=2, row=4)
        
        self.root.focus_force()
        
        for child in self.root.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.root.bind('<Return>', self.restart_game)
        
    def save_score(self):
        try:
            server_name = '165.227.51.19' #My server
            #server_name = '157.230.131.10' #Micaiah's server
            serverPort = 10000
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((server_name, serverPort))
            
            message_type = "Submit Score"
            player_name = self.game.player_name
            game_type = "testing"
            game_version = str(default_game.GAME_VERSION)
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
            self.thread_queue.put(self.rank)
            self.top_ten = arguments[2]
            
            if arguments[3] == "True": #The player won the game
                print("You won, waiting to recieve file")
                file = self.recieve_file(clientSocket)
                self.winner = True
                #self.display_image(mainframe, file)
            
            clientSocket.close()
        except ConnectionRefusedError:
            self.rank = "Error connecting to database"
            self.top_ten = "Error"
            self.thread_queue.put("Error")
            print("Error connecting or communicating to the score database server")
            
    def display_rankings(self, frame):
        #Displays the results from the server about score ranking and info
        self.loading_label.config(text= "Rank: " + str(self.rank))
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

    def quit_game(self):
        sys.exit(0)
        
    #need args* paramater because its passed by tk for the input types of frames
    def restart_game(self, screen, *args):
        default_game.Default_Game(screen)
        '''
        try:
            print("making a new snake")
            self.root.unbind("<Return>")
            self.game.restart()
            self.root.destroy()
        except ValueError:
            pass
        '''


class New_Menu(Menu):
    
    def __init__(self, screen):
        #screen = pygame.display.set_mode((main.DEFAULT_SIZE))
        screen.fill((255,255,255))
        #Create buttons and place them in a box
        play_button = thorpy.make_button("Play", func=self.restart_game, params={'screen':screen })
        quit_button = thorpy.make_button("Quit", func=self.quit_game)
        self.box = thorpy.Box(elements=[play_button, quit_button])
        
        menu = thorpy.Menu(self.box)
        
        self.render(screen, menu)
    
        #Menu loop
        menu_start = True
        while menu_start == True:
            #pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.restart_game(screen)
                if event.type == pygame.QUIT:
                    menu_start = False
                    break
                menu.react(event) #Handles function binding to buttons and gui elements
                
    def render(self, screen, menu):
        white = (255,255,255)
        screen.fill(white)
        h, w = pygame.display.get_surface().get_size()
        for element in menu.get_population():
            element.surface = screen
        self.box.set_center((h // 2, w // 2))
        self.box.blit()
        self.box.update()