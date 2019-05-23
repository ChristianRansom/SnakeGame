import default_game
from socket import *
import threading
import queue
import pygame
import thorpy
import sys

class Menu():
    
    def __init__(self, screen):
        self.initialize(screen)
        
        self.create_gui()
        
        self.set_up()
        
    def initialize(self, screen):
        self.screen = screen
        self.difficulty = "normal"
        thorpy.set_theme('human')
        thorpy.style.MARGINS = (10,10)
        self.elements = []
        self.restart = False
        self.running = True
        
    def create_gui(self):
        #Create buttons and place them in a box
        play_button = thorpy.make_button("Play", func=self.restart_game)
        play_button.set_size((200,50))
        quit_button = thorpy.make_button("Quit", func=self.quit_game)
        box = thorpy.Box([play_button, quit_button])
        self.elements.append(box)
        self.difficulty_button = thorpy.make_button("Difficulty: " + self.difficulty, func=self.select_dificulty)
        self.elements.append(self.difficulty_button)
        
    def select_dificulty(self):
        choices = [("Easy",self.set_easy), ("Normal (Recomended)",self.set_normal), ("Hard",self.set_hard)]
        thorpy.launch_blocking_choices("Difficulty\n", choices) #for auto unblit
        
        self.difficulty_button.set_text("Difficulty: " + self.difficulty)
        self.render()

    def set_up(self):
        self.main_box = thorpy.Box(self.elements)
        self.menu = thorpy.Menu(self.main_box)
        self.render()
        self.start()
    
    def start(self):
        #Menu loop
        while self.running == True:
            for event in pygame.event.get():
                self.send_menu_event(event)
                self.handle_events(event)
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.VIDEORESIZE: #handle the window resizing
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.render()
        #print("menu loop finished")
        self.finish()
        
    def finish(self):
        if self.restart: #Returns the next scene to finish this menu to prevent a 'memory leak'
            return default_game.Default_Game(self.screen, self.difficulty)
        return None
    
    def send_menu_event(self, event):
        self.menu.react(event) #Handles function binding to buttons and gui elements
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.restart_game()
    
    def render(self):        
        white = (255,255,255)
        self.screen.fill(white)
        h, w = pygame.display.get_surface().get_size()
        for element in self.menu.get_population():
            element.surface = self.screen
        self.main_box.set_center((h // 2, w // 2))
        self.main_box.blit()
        self.main_box.update()

        pygame.display.update()
        
    def restart_game(self):
        self.restart = True
        self.running = False
            
    def quit_game(self):
        self.running = False
        sys.exit(0)
    
    def set_easy(self):
        self.difficulty = "easy" 
        
    def set_normal(self):
        self.difficulty = "normal"
        
    def set_hard(self):
        self.difficulty = "hard"
        
class Pause_Menu(Menu):
    
    def __init__(self, screen):
        super(Pause_Menu, self).__init__(screen)
        
class Player_Name_Menu(Menu):
    
    def __init__(self, screen, game, inputer_error = False):
        self.game = game
        self.input_error = inputer_error
        super(Player_Name_Menu, self).__init__(screen)
        
    def create_gui(self):
        score = thorpy.make_text("Score: " + str(self.game.score))
        score.set_font_size(18)
        snake_length = thorpy.make_text("Length: " + str(len(self.game.game_snake.q)))
        snake_length.set_font_size(18)
        #self.score_header = thorpy.MultilineText(text="Loading scores from server...")
        self.score_header = thorpy.make_text(text="Loading...")
        
        self.input = thorpy.Inserter(name="Enter Your Name:", value=self.game.player_name)
        self.input.enter()
        submit_button = thorpy.make_button("Submit", func=self.submit_player_name)
        
        self.elements.append(score)
        self.elements.append(snake_length)
        self.elements.append(self.input)
        self.elements.append(submit_button)
        if self.input_error:
            error_message = thorpy.make_text("The name cannot contain a , or spaces or a |.")    
            self.elements.append(error_message)
            
    def submit_player_name(self):
        self.game.player_name = self.input.get_value()
        self.check_input(self.game.player_name )
        self.running = False

    def check_input(self, input):
        if ',' in input or ' ' in input or "|" in input:
            self.input_error = True
        else:
            self.input_error = False
        
    def send_menu_event(self, event):
        arrow_key = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                arrow_key = True
            elif event.key == pygame.K_RIGHT:
                arrow_key = True
            elif event.key == pygame.K_DOWN:
                arrow_key = True
            elif event.key == pygame.K_UP:
                arrow_key = True  
        if not arrow_key:
            self.menu.react(event) #Handles function binding to buttons and gui elements

    def finish(self):
        if not self.input_error:
            return Score_Menu(self.screen, self.game) #End screen menu
        else:
            return Player_Name_Menu(self.screen, self.game, True) #Ask for name again
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_player_name()
   
class Score_Menu(Menu): 
    
    def __init__(self, screen, game):
        self.game = game
        #This is the proper way to call a super class method
        super(Score_Menu, self).__init__(screen) 
        
    def initialize(self, screen):
        super(Score_Menu, self).initialize(screen)
        self.difficulty = self.game.difficulty
        self.winner = False
        
    def create_gui(self):
        super(Score_Menu, self).create_gui()
        
        self.your_score = thorpy.make_text("Your Score: " + str(self.game.score))
        self.your_score.set_font_size(18)
        snake_length = thorpy.make_text("Length: " + str(len(self.game.game_snake.q)))
        snake_length.set_font_size(16)
        self.rank_text = thorpy.make_text("")
        self.rank_text.set_font_size(18)
        #self.score_header = thorpy.MultilineText(text="Loading scores from server...")
        self.score_header = thorpy.make_text(text="Loading...")
        
        self.elements.append(self.your_score)
        self.elements.append(snake_length)
        self.elements.append(self.rank_text)
        self.elements.append(self.score_header)
        
        self.top_ten_texts = []
        for i in range(10):
            text = thorpy.make_text("")
            self.top_ten_texts.append(text)
            self.elements.append(text)
            
    def set_up(self):
        self.main_box = thorpy.Box(self.elements)
        self.menu = thorpy.Menu(self.main_box)
        #Can't start the network stuff until all the gui elements are created
        self.make_save_score_thread() #start saving score in a separate thread
        self.render()
        self.start()
        
    def finish(self):
        if self.restart: #Returns the next scene to finish this menu to prevent a 'memory leak'
            return default_game.Default_Game(self.screen, self.difficulty, self.game.player_name)
        return None
        
    def make_save_score_thread(self):
        '''Multi threading inspired by 
        https://scorython.wordpress.com/2016/06/27/multithreading-with-tkinter/
        '''
        self.new_thread = None
        self.thread_queue = queue.Queue()
        self.new_thread = threading.Thread(target=self.save_score)
        self.new_thread.start()
        #self.root.after(100, self.listen_for_result)

    def save_score(self):
        try:
            server_name = '165.227.51.19' #My server
            #server_name = '157.230.131.10' #Micaiah's server
            serverPort = 10000
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((server_name, serverPort))
            
            message_type = "Submit Score"
            player_name = self.game.player_name
            game_type = ("testing_" + "default_" + self.game.difficulty)
            game_version = str(default_game.GAME_VERSION)
            extra = "File"
            
            score_message = message_type + "|" + str(int(self.game.score)) + "|" + player_name + "|" + game_type + "|" + game_version + "|" + extra     
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
            
            clientSocket.close()
        except:
            self.rank = "Error"
            self.top_ten = "Error"
            self.thread_queue.put("Error")
            print("Error connecting or communicating to the score database server")
            self.score_header.set_text("Error Connecting to Database")
            self.score_header.center(axis=(True, False))
            self.render()
        else:
            #Edits the text of previously created elements with the data from the remote server
            self.score_header.set_text("High Scores")
            self.score_header.center(axis=(True, False))
            self.rank_text.set_text("Rank: " + str(self.rank))
            self.rank_text.center(axis=(True, False))
    
            self.rankings()
            self.render()
            
    def rankings(self):
        '''Formats the top ten score data received from the server'''
        top_ten = self.top_ten
        top_ten_list = top_ten.split(",", -1)
        counter = 0
        gold = (150,150,50)
        for i in top_ten_list[:-1]:
            self.top_ten_texts[counter].set_text(str(counter + 1) + ": " + str(i))
            self.top_ten_texts[counter].center(axis=(True, False))
            #print(str(counter + 1))
            #print(self.rank)
            if counter + 1 == int(self.rank): #Highlights their rank in the top ten 
                self.top_ten_texts[counter].set_font_color(gold)
            counter = counter + 1



#------------------------Unused---------------------------------------
    def recieve_file(self, s):
        ''' inspired by 
        https://stackoverflow.com/questions/35363975/sending-a-file-over-tcp-sockets
        Recieves a file from the server. 
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
    
    def local_score_save(self, game):
        '''Old unused Method that loads and saves high scores from a local data file'''
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

    
