# Tom Lancaster and Pat Rademacher (c) December 2019
# CS 494/594 - Internetworking Protocols - IRC Project
# File - client.py

import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip_file=open("server_ip_address.txt", "r")
if server_ip_file.mode == 'r':
    IP_address = server_ip_file.read()
    print('\nserver IP address you are connecting to is ' + IP_address + "\n")

# ---- This line won't work on the PSU network for some reason ---
#IP_address = socket.gethostname()

Port = 8083 
IP_address = '131.252.208.103' 
server.connect((IP_address, Port)) 
turn_user_name_on = False
username = ''  
username_var = 0

def server_crash_test(message):
    if not message:
        print("\nServer is down!\n")
        sys.exit()

try: 

    while True:

        sockets_list = [sys.stdin, server]

        """ 
        There are two possible input situations. Either the 
        user wants to give manual input to send to other people, 
        or the server is sending a message to be printed on the 
        screen. Select returns from sockets_list, the stream that 
        is reader for input. So for example, if the server wants 
        to send a message, then the if condition will hold true 
        below. If the user wants to send a message, the else 
        condition will evaluate as true.
        """
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
        for socks in read_sockets:
            logout = False
            if socks == server and logout == False:
                message = str(socks.recv(1024).decode())
                server_crash_test(message)
                message = message.strip()
                message_cue = 'You have successfully signed in -- welcome to PAT CHAT! A chat room with attitude.'
                if message_cue in message:
                    print(message)

                else:
                    print(message)
            else:
                username_output = ">>"
                message = sys.stdin.readline()
                if message.strip() == "exit" or message.strip() == "EXIT":
                    logout = True
                total_output = username_output + " " + message.strip()
                if turn_user_name_on == False:
                    server.sendto(message.encode(),(IP_address, Port))
                    print(total_output)
                    sys.stdout.flush()
                else:
                    server.sendto(message.encode(),(IP_address, Port))
                    print(total_output)
                    sys.stdout.flush()
        
        if logout == True:
            for i in range(100000):
                message = "Thanks for using PAT CHAT! You will be missed (by some more than others)."
                print(message)
            server.close()
            sys.exit()

except KeyboardInterrupt:
    print("\n\nThe program has crashed! Please restart and try again.\n")
    server.close()
    sys.exit()
        
server.close()
            
        

            
