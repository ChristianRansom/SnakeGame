'''
Created on Apr 19, 2019

@author: Christian Ransom
'''
from socket import *
import pickle
import random

def main():
    serverPort = 10000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024).decode()
        print("From Client: " + message)
        arguments = message.split("|", -1)
        score_index = 1
        score = int(arguments[score_index]) #type check this first
        arguments[score_index] = score
        game_type = arguments[3]
        game_version = arguments[4]
        extra = arguments[5]
        score_entries = []

        file_name = "scores_" + game_type + "_" + game_version + ".bin"
        try:
            binary_file = open(file_name, "rb+")
        except FileNotFoundError:
            print("No score file found... making one now")
            binary_file = open(file_name, "wb")
            #print("Arguments: " + str(arguments))
            pickle.dump([arguments], binary_file)
            print("|" + str(arguments[score_index]) + "|" )
            rank = 0
        else:
            file_entry = []
            while True:
                try:
                    file_entry = pickle.load(binary_file)
                    #print("File entry: " + str(file_entry))
                except EOFError:
                    break
            score_entries = file_entry

            rank = binary_insert(score_entries, arguments, 0, len(score_entries) -1)

            pickle.dump(score_entries, binary_file)
    
            binary_file.close()
            
        top_ten = ""
        if len(score_entries) >= 10:
            top_scores_list = 10
        else:
            top_scores_list = len(score_entries) 
        for i in range(top_scores_list):
            top_ten = top_ten + str(score_entries[i][score_index]) + " - " + str(score_entries[i][2]) + ", "
        message_type = "Reply Rank"
        is_winner = (rank < 3)
        reply = message_type + "|" + str(rank + 1) + "|" + str(top_ten) + "|" + str(is_winner) + "|" + extra
        connectionSocket.send(reply.encode())
        
        if is_winner and extra == "File":
            file = open('trophy.png','rb')
            send_file(file, connectionSocket)
        
        connectionSocket.close()
    
    
'''Binary Insertion based on code from 
https://www.geeksforgeeks.org/python-program-for-binary-insertion-sort/'''
def binary_insert(arr, val, start, end): 
    score_index = 1
    # we need to distinugish whether we should insert 
    # before or after the left boundary. 
    # +imagine [0] is the last step of the binary search 
    # and we need to decide where to insert -1 
    if start == end:
        #print(str(val[score_index]) + " < " + str(arr[start][score_index]))
        #print(start)
        if val[score_index] < arr[start][score_index]:
            arr.insert(start + 1, val)
            return start + 1
        else: 
            arr.insert(start, val)
            return start
    # this occurs if we are moving beyond left\'s boundary 
    # meaning the left boundary is the least position to 
    # find a number greater than val 
    if start > end: 
        arr.insert(start, val) 
        return start 
    elif end < start:
        arr.insert(end + 1, val) 
        return end + 1
  
    mid = (start+end) // score_index
    #print("mid " + str(mid))
    if val[score_index] > arr[mid][score_index]: 
        #print("putting in in top half putting cuz " + str(val[score_index]) + " > " + str(arr[mid][score_index]))
        return binary_insert(arr, val, start, mid-1) 
    elif val[score_index] < arr[mid][score_index]:
        #print("putting if in bottom half cuz " + str(val[score_index]) + " < " + str(arr[mid][score_index]))
        return binary_insert(arr, val, mid+1, end) 
    else: 
        arr.insert(mid + 1, val)
        return mid + 1
    
def send_file(f, s):
    '''
    inspired by 
    https://stackoverflow.com/questions/35363975/sending-a-file-over-tcp-sockets
    '''
    print("Sending...")
    l = f.read(4096)
    while (l):
        print("Sending...")
        s.send(l)
        l = f.read(4096)
    f.close()
    print("Done Sending")

if __name__ == '__main__':
    main()