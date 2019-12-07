# Tom Lancaster and Pat Rademacher (c) December 2019
# CS 494/594 - Internetworking Protocols - IRC Project
# File - server.py
# Info: Python program to implement server side of chat room. 


import socket
import select
import sys
import _thread
import threading
import time
import os
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8083
IP_address = socket.gethostname()
server_ip = socket.gethostbyname(IP_address) 
print("\nServer's IP Address is " + server_ip + "\n\n")
IP_file = open("server_ip_address.txt", "w")
IP_file.write(server_ip)
IP_file.close()
users = 0
chatroom_names = {"Main Room": [], "Sports": [], "Cars": []}
read_existing_users = open("existing_users.txt", "r")
for line in read_existing_users:
        users = users + 1
        line = line.split()
        if (len(line)) != 4:
                print("\nThe input file is not correct")
read_existing_users.close()
existing_users = [['' for q in range (4)] for y in range (users)]
read_existing_users = open("existing_users.txt", "r")
users = 0
for line in read_existing_users:
        line = line.split()
        for j in range(4):
                existing_users[users][j] = line[j]
        users = users + 1

read_existing_users.close()
client_status = True
intro = True
currently = 'Main Room'

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, port))
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100)

list_of_clients = []
list_of_IP = []
clients_info = []

###################################################################
#     Classes & Functions
###################################################################
def client_crash_test(response, usrname):
        if len(response)==0:   # length of data peeked 0?
            print(usrname + " has disconnected.")  # client disconnected
            return True

def client_crash_test_login(response):
        if len(response)==0:
            print("Unknown client program has crashed and left.")
            return True

class user:
        def __init__(self, connection, address):
                self.connection = connection
                self.address = address[0]
        
        def create_new_user(self):
                message = "\n\nType 'EXIT' at anytime to leave. Type 'BACK' to go to previous screen.\n\n\n\nPlease enter your first name:  "
                self.connection.sendto(message.encode(), (self.address, port))
                firstname_response = str(self.connection.recv(1024).decode())
                client_crash_test_login(firstname_response)
                firstname_response = firstname_response.strip()
                message = "\n\nPlease enter your last name: "
                self.connection.sendto(message.encode(), (self.address, port))
                lastname_response = str(self.connection.recv(1024).decode())
                client_crash_test_login(lastname_response)
                lastname_response = lastname_response.strip()
                message = "\n\nPlease enter your desired username: "
                self.connection.sendto(message.encode(), (self.address, port))
                username_response = str(self.connection.recv(1024).decode())
                client_crash_test_login(username_response)
                username_response = username_response.strip()
                while True:
                        i = 0
                        does_user_exist = False
                        for i in range(len(existing_users)):
                                if username_response == existing_users[i][0]:
                                        message = "\n\nSorry, that username is already taken\nTry a new one: "
                                        self.connection.sendto(message.encode(), (self.address, port))
                                        username_response = str(self.connection.recv(1024).decode())
                                        client_crash_test_login(username_response)
                                        username_response = username_response.strip()
                                        does_user_exist = True
                                        break
                        if does_user_exist == False:
                                break
                message = "\n\nCool beans, the username " + username_response + " is available!\n\nPlease enter your password: "
                self.connection.sendto(message.encode(), (self.address, port))
                password_response = str(self.connection.recv(1024).decode())
                client_crash_test_login(password_response)
                password_response = password_response.strip()
                message = "\n\nPlease enter your password again: "
                self.connection.sendto(message.encode(), (self.address, port))
                password2_response = str(self.connection.recv(1024).decode())
                client_crash_test_login(password2_response)
                password2_response = password2_response.strip()
                while password_response != password2_response:
                        message = "\n\nThose didn't match! Please enter your password again: "
                        self.connection.sendto(message.encode(), (self.address, port))
                        password2_response = str(self.connection.recv(1024).decode())
                        password2_response = password2_response.strip()
                username = username_response
                password = password_response
                firstname = firstname_response
                lastname = lastname_response
                return username, password, firstname, lastname
        
        def existing_user(self):
                find_existing_user = False
                username = ''
                while True:
                        message = "\n\nPlease type in your username: "
                        self.connection.sendto(message.encode(), (self.address, port))
                        response = str(self.connection.recv(1024).decode())
                        client_crash_test_login(response) 
                        response = response.strip()
                        forloopbreak = False
                        for i in range(len(existing_users)):
                                if forloopbreak == True:
                                        break
                                if response == existing_users[i][0]:
                                        find_existing_user = True
                                        message = "\n\nWelcome back, " + existing_users[i][2] + "\n\nPlease type in the password for " + response + ":"
                                        self.connection.sendto(message.encode(), (self.address, port))
                                        password_response = str(self.connection.recv(1024).decode())
                                        client_crash_test_login(password_response)
                                        password_response = password_response.strip()
                                        while password_response != existing_users[i][1]:
                                                message = "\n\nSorry, " + existing_users[i][2] + ", that is not your correct password.\n\nPlease type in the password for " + response + ":"
                                                self.connection.sendto(message.encode(), (self.address, port))
                                                password_response = str(self.connection.recv(1024).decode())
                                                password_response = password_response.strip()
                                        if password_response == existing_users[i][1]:
                                                username = existing_users[i][0]
                                                password = existing_users[i][1]
                                                firstname = existing_users[i][2]
                                                lastname = existing_users[i][3]
                                                forloopbreak = True
                                                break
                        if find_existing_user == False:
                                message = "\n\nHmm...we could not find the username " + response + ":"
                                self.connection.sendto(message.encode(), (self.address, port))
                        else:
                                return username, password, firstname, lastname
                                break

        def login(self):
                main_screen = True
                go_back = True
                invalid_input = True
                login_responses = ["L", "l", "N", "n", "EXIT", "exit", "back", "BACK"]
                response = ''
                while True:
                        welcome = True
                        if (main_screen == True) and (go_back == True):
                                welcome_message = "Welcome to PAT CHAT! A chatroom with attitude.\n\n"
                                welcome_message = welcome_message + "Please type 'n' and hit ENTER if you are new user."
                                welcome_message = welcome_message + "\n\nPlease type 'l' if you are an existing user and "
                                welcome_message = welcome_message + "would like to login. \n\n\Please type 'EXIT' to logoff"
                                self.connection.sendto(welcome_message.encode(), (self.address, port))
                                go_back = False
                        response = str(self.connection.recv(1024).decode())
                        client_crash_test_login(response)
                        response = response.strip()
                        print(response)
                        for i in range(len(login_responses)):
                                if str(response) == str(login_responses[i]):
                                        invalid_input = False
                        while invalid_input == True:
                                message = "Sorry, I could not compute your input, which means you did it incorrectly, no offense, but I know since I'm a COMPUTER!...\n\n"
                                message = message + "Please try again, or type 'BACK' for previous screen, or get the FRICK out of here by typing 'EXIT'\n\n"
                                message = message + "If your feelings are hurt, you'll get over it (....or not.)"
                                self.connection.sendto(message.encode(), (self.address, port))
                                main_screen = False
                                response = self.connection.recv(1024).decode()
                                #client_crash_test_login(response)
                                response = str(response.strip())
                                print(response)
                                for i in range(len(login_responses)):
                                        if response == login_responses[i]:
                                                invalid_input = False
                                                break
                        if response == login_responses[0] or response == login_responses[1]:
                                username, password, firstname, lastname = self.existing_user()
                                user = user_info(self.connection, self.address, username, password, firstname, lastname)
                        elif response == login_responses[2] or response == login_responses[3]:
                                message = "\n\nSweet dude (or dudette), let's get you rolling with a new account!\n\n"
                                self.connection.sendto(message.encode(), (self.address, port))
                                username, password, firstname, lastname = self.create_new_user()
                                user = user_info(self.connection, self.address, username, password, firstname, lastname)
                                print(user.firstname)
                                add_new_user = [user.username + ' ', user.password + ' ', user.firstname + ' ', user.lastname]
                                existing_users.append(add_new_user)
                                print(existing_users)
                                write_existing_users = open("existing_users.txt", "a")
                                for j in range(4):
                                        write_existing_users.write(add_new_user[j])
                                write_existing_users.close()
                                main_screen = False
                        elif response == login_responses[6] or response == login_responses[7]:
                                if main_screen == True:
                                        go_back = False
                                if main_screen == False:
                                        main_screen = True
                                        go_back = True
                        elif response == login_responses[4] or response == login_responses[5]: 
                                message = "OH!...okay...well...so long, farewell, I don't care that\
                                           you're leaving...hope you have a GOOD TIME!\n \
                                           I'm not crying! You're crying!"
                                self.connection.sendto(message.encode(), (self.address[0], port))
                                welcome = False
                        if welcome == False:
                                return False
                                break
                        elif welcome == True:
                                return user
                                break
                        
class user_info(user):
        def __init__(self, connection, address, username, password, firstname, lastname):
                super().__init__(connection, address)
                self.username = username
                self.password = password
                self.firstname = firstname
                self.lastname = lastname      
                
def clientthread(conn, address, username):
        
        message = "You have successfully signed in -- welcome to PAT CHAT! You are in the main room. Type '!' to see the main menu at anytime."
        message = message + "\n\nYou will need to be in the main menu in order to play with the different cool components PAT CHAT has to offer.\n\n"
        conn.sendto(message.encode(), (address, port))
        print('\n\n\n\n' + address + '\n\n\n')
        for usernames in chatroom_names:
            if username not in chatroom_names['Main Room']:
                chatroom_names['Main Room'].append(username)
        currently = 'Main Room'
        boc = True
        bts = False
        remove_bool = False 
        while True:
                        try:
                                message = conn.recv(1024).decode()
                                if client_crash_test(message, username) or message.strip() == 'exit' or message.strip() == 'EXIT':
                                    #remove(conn, address, username)
                                    remove_bool = True
                                    break
                                elif message:
                                        message = message.strip()
                                        while message == '!':
                                                currently, boc, bts = main_menu(conn, address, username, currently, boc, bts)
                                                print("currently = " + currently)
                                                message = conn.recv(1024).decode()
                                                message = message.strip()
                                        """prints the message and address of the 
                                        user who just sent the message on the server 
                                        terminal"""
                                        print("<" + username + "> " + message)
                                        message_to_send = "<" + username + "> " + message
                                        broadcast(message_to_send, conn, address, username, currently, boc, bts)
                        
                                else:
                                        """message may have no content if the connection 
                                        is broken, in this case we remove the connection"""
                                        remove(conn, address, username)
                        except:                                      
                                continue        
        if remove_bool == True:
            remove(conn, address, username)

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection, address, username, currently, boc, bts):
        if boc == True and bts == False:
            for name in chatroom_names[currently]:
                if name != username:
                    for i in range(len(clients_info)):
                        if name == clients_info[i][0]:
                            clients_info[i][1].sendto(message.encode(), (clients_info[i][2], port))
        else:
            #message = username + " from " + currently + " says: " +  message + '\n\n'
            server_message = "\n\nAlright, cool, please select which room(s) you would like to send the message you just typed:\n\n"
            server_message = server_message + "If you want to do multiple rooms, separate the numbers by a comma\n\n"
            server_message = server_message + "For example: 1, 3, 7\n\n"
            i = 1
            rooms_user_is_in = []
            for key, value in chatroom_names.items():
                if username in value:
                    server_message = server_message + str(i) + ': ' + key + '\n'
                    rooms_user_is_in.append(key)
                    i = i + 1
            connection.sendto(server_message.encode(), (address, port))
            response = connection.recv(1024).decode()
            response = str(response.strip())
            room_values = response.split(",")
            print(room_values)
            for i in range(len(room_values)):
                print(room_values[i])
                room_values[i] = int(room_values[i]) - 1
                print(str(room_values[i]))
            j = 0
            rooms_to_send = []
            for i in range(len(rooms_user_is_in)):
                if i == room_values[j]:
                    rooms_to_send.append(rooms_user_is_in[i])
                    j = j + 1
            print(rooms_to_send)
            for name in rooms_to_send:
                for names in chatroom_names[name]:
                    if names != username:
                        for i in range(len(clients_info)):
                            if names == clients_info[i][0]:
                                new_message =  "From " + currently + " to members of " + name + ": " +  message + '\n\n'
                                clients_info[i][1].sendto(new_message.encode(), (clients_info[i][2], port))


"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection, address, username):
        if connection in list_of_clients:
                        list_of_clients.remove(connection)
        if address in list_of_IP:
                        list_of_IP.remove(address)
        for i in range(len(clients_info)):
                        if username == clients_info[i][0]:
                            del(clients_info[i])
                            break
        for name in chatroom_names:
            if username in chatroom_names[name]:
                chatroom_names[name].remove(username)

def main_menu(connection, address, username, currently, boc, bts):
        main_menu_strings = ['c', 'C', 'j', 'J', 'l', 'L', 'cl', 'CL', 'r', 'R', 'm1', 'M1', 'sm', 'SM', 'SR', 'sr', 'ci', 'CI', 'back', 'BACK']
        message = '\n\nMAIN MENU:\n\n\nEnter "c" or "C" to create a chatroom -- this will automatically put you in the chatroom you create'
        message = message + '\n\nEnter "j" or "J" to join a chatroom\n\n'
        message = message + '\Enter "cl" or "CL" to list all chatrooms\n\n' 
        message = message + 'Enter "l" or "L" to list members in a chatroom\n\n'
        message = message + 'Enter "m1" or "M1" if you want your message to be seen by those who are in whatever room you are currently in\n\n'
        message = message + 'Enter "sm" or "SM" if you want your message to be seen by members in a room or multiple rooms you are a part of\n\n' 
        message = message + 'Enter "r" or "R" to remove yourself from a room you are currently in or are a part of\n\n'
        message = message + 'Enter "ci" or "CI" to show what chatroom you are currently in\n\n'
        message = message + 'Enter "back" or "BACK" to go to the previous screen\n\n'
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        if client_crash_test(response, username):
            return currently, boc, bts
        response = str(response.strip())
        if response == main_menu_strings[0] or response == main_menu_strings[1]:
                currently = create_a_chatroom(connection, address, username)
                return currently, boc, bts
        elif response == main_menu_strings[2] or response == main_menu_strings[3]: 
                currently = join_a_chatroom(connection, address, username)
                return currently, boc, bts
        elif response == main_menu_strings[4] or response == main_menu_strings[5]:
                list_people_in_chatroom(connection, address, username)
                return currently, boc, bts
        elif response == main_menu_strings[6] or response == main_menu_strings[7]:
                list_all_chatrooms(connection, address, username)
                return currently, boc, bts
        elif response == main_menu_strings[8] or response == main_menu_strings[9]:
                currently = remove_user_from_chatroom(connection, address, username)
                return currently, boc, bts
        elif response == main_menu_strings[10] or response == main_menu_strings[11]:
                boc = True
                bts = False
                return currently, boc, bts
        elif response == main_menu_strings[12] or response == main_menu_strings[13]:
                boc = False
                bts = True
                return currently, boc, bts
        elif response == main_menu_strings[16] or response == main_menu_strings[17]:
                message = '\n\nYou are currently in ' + currently
                connection.sendto(message.encode(), (address, port))
                return currently, boc, bts
        elif response == main_menu_strings[18] or response == main_menu_strings[19]:
                return currently, boc, bts

def create_a_chatroom(connection, address, username):
        message = "\nCool, what do you want to name your chatroom?\n"
        connection.sendto(message.encode(), (address, port))
        while True:
            screen = False
            response = connection.recv(1024).decode()
            if client_crash_test(response, username):
                break
            response = str(response.strip())
            if response not in chatroom_names:
                chatroom_names[response]=[]
                chatroom_names[response].append(username)
                message = '\n\nAlrighty, you have created the chatroom: ' + response
                connection.sendto(message.encode(), (address, port))
                currently_in = response
                screen = True
            else:
                message = "\n\nSorry dawg, that chatroom name is already taken! Try another one\n\n"
                connection.sendto(message.encode(), (address, port))
                screen = False
            if screen == True:
                return currently_in
                break

def join_a_chatroom(connection, address, username):
    message = "\nCool, what chatroom do you want to join?\n"
    connection.sendto(message.encode(), (address, port))
    while True:
        screen = False
        i = 1
        for key in chatroom_names.keys():
            if i == 1:
                message = str(i) + ': ' + key + '\n'
            else:
                message = message + str(i) + ': ' + key + '\n'
            i = i + 1
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        if client_crash_test(response, username):
            break
        response = str(response.strip())
        if response in chatroom_names:
            chatroom_names[response].append(username)
            currently_in = response
            screen = True
            break
        elif response.isdigit():
            response = int(response)
            response = response - 1
            i = 0
            if response not in range(len(chatroom_names)):
                screen = False
            else: 
                for chatroom_name in chatroom_names:
                    if response == i:
                        screen = True
                        chatroom_names[chatroom_name].append(username)
                        currently_in = chatroom_name
                        break
                    else:
                        i = i + 1
        if screen == True:
            message = "\nCool, you have successfully joined and are currently in: " + currently_in + "\n"
            connection.sendto(message.encode(), (address, port))
            return currently_in
            break
        else:
            message = "\n\nSorry, that input is not recognized. Try again..."
            connection.sendto(message.encode(), (address, port))

def list_people_in_chatroom(connection, address, username):
        message = "\nCool, you want to see who's in a chatroom? Which one?\n"
        connection.sendto(message.encode(), (address, port))
        while True:
            screen = False
            i = 1
            for key in chatroom_names.keys():
                if i == 1:
                    message = str(i) + ': ' + key + '\n'
                else:
                    message = message + str(i) + ': ' + key + '\n'
                i = i + 1
            connection.sendto(message.encode(), (address, port))
            response = connection.recv(1024).decode()
            if client_crash_test(response, username):
                break
            response = str(response.strip())
            if response in chatroom_names:
                message = "Users in " + response + ":"
                for q in range(len(chatroom_names[response])):
                    message = message + ' ' + chatroom_names[response][q]
                connection.sendto(message.encode(), (address, port))
                screen = True
                break
            elif response.isdigit():
                response = int(response)
                response = response - 1
                i = 0
                if response not in range(len(chatroom_names)):
                    screen = False
                else:
                    for chatroom_name in chatroom_names:
                        if response == i:
                            message = "Users in " + chatroom_name  + ":"
                            for q in range(len(chatroom_names[chatroom_name])):
                                message = message + ' ' + chatroom_names[chatroom_name][q]
                            connection.sendto(message.encode(), (address, port))
                            screen = True
                            break
                        else:
                            i = i + 1
            if screen == True:
                break
            else:
                message = "\n\nSorry, that input is not recognized. Try again..."
                connection.sendto(message.encode(), (address, port))



def list_all_chatrooms(connection, address, username):
    message = "\n\nCool, here are all the chatrooms available:\n\n"
    i = 1
    for key in chatroom_names.keys():
        message = message + str(i) + ': ' + key + '\n'
        i = i + 1
    connection.sendto(message.encode(), (address, port))

def remove_user_from_chatroom(connection, address, username):
    message = "\n\nCool, what chatroom do you want to remove yourself from?\n\n"
    name_of_removed_room = ''
    while True:
        screen = False
        i = 1
        rooms_user_is_in = []
        for key, value in chatroom_names.items():
            if username in value:
                message = message + str(i) + ': ' + key + '\n'
                rooms_user_is_in.append(key)
                i = i + 1
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        if client_crash_test(response, username):
            break
        response = str(response.strip())
        if response in rooms_user_is_in:
                chatroom_names[response].remove(username)
                rooms_users_is_in.remove(response)
                currently_in = chatroom_names['Main Room']
                screen = True
                break
        elif response.isdigit():
            response = int(response)
            response = response - 1
            i = 0
            if response not in range(len(rooms_user_is_in)):
                screen = False
            else:
                for chatroom_name in rooms_user_is_in:
                        print("chatroom_name = " + chatroom_name + " and i = " + str(i))
                        if response == i:
                            if chatroom_name in chatroom_names:
                                chatroom_names[chatroom_name].remove(username)
                                name_of_removed_room = chatroom_name
                            rooms_user_is_in.remove(chatroom_name)
                            screen = True
                            currently_in = 'Main Room'
                            if username not in chatroom_names['Main Room']:
                                chatroom_names['Main Room'].append(username)
                            break
                        else:
                            i = i + 1
            if screen == True:
                message = "\n\nYou have successfully removed yourself from " + name_of_removed_room
                connection.sendto(message.encode(), (address, port))
                return currently_in
                break
            else:
                message = "\n\nSorry, that input is not recognized. Try again..."
                connection.sendto(message.encode(), (address, port))


                
while True:

        """Accepts a connection request and stores two parameters, 
        conn which is a socket object for that user, and addr 
        which contains the IP address of the client that just 
        connected"""
        conn, addr = server.accept()
        """Maintains a list of clients for ease of broadcasting 
        a message to all available people in the chatroom"""
        list_of_clients.append(conn)
        list_of_IP.append(addr[0])
        username = addr[0]
        exitt = False
        server_exit = 'server exit'
        for q in range(len(list_of_IP)):
                if list_of_IP[q] != addr[0]:
                        welcome_message = addr[0] + " has joined the room!"
                        list_of_clients[q].sendto(welcome_message.encode(), (list_of_IP[q], port))

        # prints the address of the user that just connected 
        print(addr[0] + " connected")
        # creates and individual thread for every user 
        # that connects 
        client = user(conn, addr)
        client = client.login()
        if client == False:
                remove(conn, addr[0], client.username)
                conn.close()
                
        else:
                clients_info.insert(0, [client.username, client.connection, addr[0]])
                print(clients_info)
                client.address = addr[0]
                main_thread = threading.Thread(target=clientthread, args=(client.connection, client.address, client.username))
                main_thread.start()
                if input() == server_exit:
                    message = "\n\nThe server has closed down intentionally and turned itself off\n\n"
                    client.connection.sendto(message.encode(), (addr[0], port))
                    break
                
time.sleep(2)
conn.close()
server.close()
time.sleep(2)
os._exit(0)

