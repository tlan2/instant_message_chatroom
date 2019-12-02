# Python program to implement server side of chat room. 
import socket
import select
import sys
import _thread
import threading
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8083
# checks whether sufficient arguments have been provided 
#if len(sys.argv) != 3: 
#       print("Correct usage: script, IP address, port number")
#       exit() 

# takes the first argument from command prompt as IP address 
IP_address = socket.gethostname()
server_ip = socket.gethostbyname(IP_address) #str(sys.argv[1]) 
print("\nServer's IP Address is " + server_ip + "\n\n")
IP_file = open("server_ip_address.txt", "w")
IP_file.write(server_ip)
IP_file.close()
x = 0
chatroom_names = {"Main Room": [], "Sports": [], "Cars": []}
read_existing_users = open("existing_users.txt", "r")
for line in read_existing_users:
        x = x + 1
        line = line.split()
        if (len(line)) != 4:
                print("\nThe input file is not correct")
read_existing_users.close()
existing_users = [['' for q in range (4)] for y in range (x)]
print(existing_users)
read_existing_users = open("existing_users.txt", "r")
x = 0
for line in read_existing_users:
        line = line.split()
        for j in range(4):
                existing_users[x][j] = line[j]
        x = x + 1

read_existing_users.close()
print(len(existing_users))
print(x)
client_status = True
intro = True

# takes second argument from command prompt as port number 
#Port = 8081 #int(sys.argv[2]) 

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

class user:
        def __init__(self, connection, address):
                self.connection = connection
                self.address = address[0]
        
        def create_new_user(self):
                message = "\n\nType 'EXIT' at anytime to leave. Type 'BACK' to go to previous screen.\n\n\n\nPlease enter your first name:  "
                self.connection.sendto(message.encode(), (self.address, port))
                firstname_response = str(self.connection.recv(1024).decode())
                firstname_response = firstname_response.strip()
                message = "\n\nPlease enter your last name: "
                self.connection.sendto(message.encode(), (self.address, port))
                lastname_response = str(self.connection.recv(1024).decode())
                lasttname_response = lastname_response.strip()
                message = "\n\nPlease enter your desired username: "
                self.connection.sendto(message.encode(), (self.address, port))
                username_response = str(self.connection.recv(1024).decode())
                username_response = username_response.strip()
                while True:
                        i = 0
                        does_user_exist = False
                        for i in range(len(existing_users)):
                                if username_response == existing_users[i][0]:
                                        message = "\n\nSorry, that username is already taken\nTry a new one: "
                                        self.connection.sendto(message.encode(), (self.address, port))
                                        username_response = str(self.connection.recv(1024).decode())
                                        username_response = username_response.strip()
                                        does_user_exist = True
                                        break
                        if does_user_exist == False:
                                break
                message = "\n\nCool beans, the username " + username_response + " is available!\n\nPlease enter your password: "
                self.connection.sendto(message.encode(), (self.address, port))
                password_response = str(self.connection.recv(1024).decode())
                password_response = password_response.strip()
                message = "\n\nPlease enter your password again: "
                self.connection.sendto(message.encode(), (self.address, port))
                password2_response = str(self.connection.recv(1024).decode())
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
                                welcome_message = "Welcome to PAT CHAT!\n\nPlease type 'n' and hit ENTER if you are new user.'\n\nPlease type 'l' if you are an existing user and would like to login. \n\nPlease type 'EXIT' to logoff"
                                self.connection.sendto(welcome_message.encode(), (self.address, port))
                                go_back = False
                        response = str(self.connection.recv(1024).decode())
                        response = response.strip()
                        print(response)
                        for i in range(len(login_responses)):
                                if str(response) == str(login_responses[i]):
                                        invalid_input = False
                        while invalid_input == True:
                                message = "Sorry, I could not compute your input, which means you did it incorrectly\nno offense, but I know since I'm a COMPUTER! ...dumbass\n\nPlease try again, or type 'BACK' for previous screen,\nor get the FRICK out of here by typing 'EXIT'"
                                self.connection.sendto(message.encode(), (self.address, port))
                                main_screen = False
                                response = self.connection.recv(1024).decode()
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
                                message = "\n\nSweet, let's get you rolling with a new account!\n\n"
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
                                message = "OH!...okay...well...so long, farewell, I don't care that you're leaving...hope you have a GOOD TIME!"
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
        
        #create_a_chatroom(conn, address, username)
        #print(chatroom_names)
        #join_a_chatroom(conn, address, username)
       # print(chatroom_names)
        #list_people_in_chatroom(conn, address, username)
        # sends a message to the client whose user object is conn
        message = "You have successfully signed in -- welcome to PAT CHAT! You are in the main room. Type'!' to see the main menu"
        conn.sendto(message.encode(), (address, port))
        while True:
                        try:
                                message = conn.recv(1024).decode()
                                if message:
                                        message = message.strip()
                                        if message == '!':
                                                main_menu(conn, address, username)
                                        """prints the message and address of the 
                                        user who just sent the message on the server 
                                        terminal"""
                                        print("<" + username + "> " + message)
                                        #user_identifier = "<" + username + "> "
                                        #conn.sendto(user_identifier.encode(), (addr, port))
                                        # Calls broadcast function to send message to all 
                                        #message_to_send = "<" + username + "> " + message
                                        #broadcast(message_to_send, conn)
                        
                                else:
                                        """message may have no content if the connection 
                                        is broken, in this case we remove the connection"""
                                        remove(conn)  
                        except:                                      
                                continue        

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, conn):
        for i in range(len(list_of_clients)):
                if list_of_clients[i]!=connection:
                        try:
                                list_of_clients[i].sendto(message.encode(), (list_of_IP[i], port))
                        except:
                                list_of_clients[i].close()

                                #if the link is broken, we remove the client"""
                                #remove(list_of_clients[i]) 
                                remove(list_of_clients[i])
"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection):
        if connection in list_of_clients:
                        list_of_clients.remove(connection)

def main_menu(connection, address, username):
        #print('\n\nMAIN MENU:\n\n'):
        main_menu_strings = ['c', 'C', 'j', 'J', 'l', 'L', 'back', 'BACK']
        message = '\n\nMAIN MENU:\n\nEnter "c" or "C" to create a chatroom\n\nEnter "j" or "J" to join a chatroom\n\nEnter "l" or "L" to list members in a chatroom\n\nEnter "back" or "BACK" to go to the previoius screen\n\n'
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        response = str(response.strip())
        if response == main_menu_strings[0] or response == main_menu_strings[1]:
                create_a_chatroom(connection, address, username) 
        elif response == main_menu_strings[2] or response == main_menu_strings[3]: 
                join_a_chatroom(connection, address, username)
        elif response == main_menu_strings[4] or response == main_menu_strings[5]:
                list_people_in_chatroom(connection, address, username)
def create_a_chatroom(connection, address, username):
        message = "\nCool, what do you want to name your chatroom?\n"
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        response = str(response.strip())
        chatroom_names[response]=[]
        chatroom_names[response].append(username)
        #peopleons_in_chat.append(chatroom_name)
        #for i in range(len(people_in_chat)):
                #if people_in_chat[i] == chatroom_name:
                        #people_in_chat.insert(i+1, username)
                        #break

def join_a_chatroom(connection, address, username):
        message = "\nCool, what chatroom do you want to join?\n"
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        chatroom_name = str(response.strip())
        if chatroom_name in chatroom_names:
                chatroom_names[chatroom_name].append(username)
                print(chatroom_names)
def list_people_in_chatroom(connection, address, username):
        message = "\nCool, you want to see who's in a chatroom? Which one?\n"
        connection.sendto(message.encode(), (address, port))
        response = connection.recv(1024).decode()
        chatroom_name = str(response.strip())
        message = "Users in " + chatroom_name + ":"
        #connection.sendto(message.encode(), (address, port))
        if chatroom_name in chatroom_names:
                for i in range(len(chatroom_names[chatroom_name])):
                       message = message + ' ' + chatroom_names[chatroom_name][i]
        connection.sendto(message.encode(), (address, port))
        #print("Users in " + chatroom_name + ":")
        #for i in range(x, len(people_in_chat)):
        #        if people_in_chat[i] != chatroom_name and people_in_chat[i] not in chatroom_names:
        #                print(people_in_chat[i])
        #        if people_in_chat[i] != chatroom_name and people_in_chat[i] in chatroom_names:
        #                break
                
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
                remove(conn)
                conn.close()
                
        else:
                
                #message = "\n\nYou are in the main room. Type'!' to see the main menu"
                #conn.sendto(message.encode(), (client.address, port))
                threading.Thread(target=clientthread, args=(client.connection, client.address, client.username)).start()
                
conn.close()
server.close()