# Tom Lancaster and Pat Rademacher (c) December 2019
# CS 494/594 - Internetworking Protocols - IRC Project

import socket
import select
import sys
#import pyttsx3

i = 18 #What does this stand for?

'''engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[19])
rate = engine.getProperty('rate')
print("rate = " + str(rate))
rate = rate + 50
print("now rate = " + str(rate))
engine.setProperty('rate', rate)'''

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#if len(sys.argv) != 3: 
#       print("Correct usage: script, IP address, port number")  DEPRECATE?
#       exit() 

server_ip_file=open("server_ip_address.txt", "r")
if server_ip_file.mode == 'r':
    IP_address = server_ip_file.read()
    print('server IP address you are connecting to is ' + IP_address)
#IP_address = socket.gethostname() #str(sys.argv[1]) 
Port = 8083 #int(sys.argv[2])
IP_address = '131.252.217.155' 
server.connect((IP_address, Port)) 
turn_user_name_on = False
username = ''  
username_var = 0   
while True:

    #if server.close():
        #print("you have been disconnected from the network either through the server or an error connection\nPlease try running the program again")
    # maintains a list of possible input streams DEPRECATE?

    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the 
        user wants to give manual input to send to other people, 
        or the server is sending a message to be printed on the 
        screen. Select returns from sockets_list, the stream that 
        is reader for input. So for example, if the server wants 
        to send a message, then the if condition will hold true 
        below.If the user wants to send a message, the else 
        condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        logout = False
        if socks == server and logout == False:
            #voices = engine.getProperty('voices')
            #engine.setProperty('voices', voices[19]) DEPRECATE?
            message = str(socks.recv(1024).decode())
            message = message.strip()
            message_cue = 'You have successfully signed in -- welcome to PAT CHAT! A chat room with attitude.'
            if message_cue in message:
                print(message)

                #username = message.replace('You have successfully signed in -- welcome to PAT CHAT!', ' ')
                #turn_user_name_on = True
                #username = username.strip() DEPRECATE?
            else:
                print(message)
                #voice_message = str(message)
                #engine.say(message)
                #engine.runAndWait()
                #engine.stop()
        else:
            username_output = "<" + username + ">"
            message = sys.stdin.readline()
            if message.strip() == "exit" or message.strip() == "EXIT":
                logout = True
            total_output = username_output + " " + message.strip()
            if turn_user_name_on == False:
                server.sendto(message.encode(),(IP_address, Port))
            else:
                server.sendto(message.encode(),(IP_address, Port))
                print(total_output)
            sys.stdout.flush()
        if logout == True:
            for i in range(100000):
                message = "Thanks for using PAT CHAT! You will be missed (by some more than others.)"
                print(message)
            server.close()
            exit
server.close()
            
        

            
