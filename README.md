# Pat Chat 

Internet Chat Relay Program - Fall 2019 - CS494/594 - Internetworking Protocols - Nirupama Bulusu

### About
Created in November/December 2020 with [Patrick Rademacher](https://github.com/PatRademacher) for our CS494/594 Internetworking Protocols class. 
The project involved writing a RFC document, designing the Application Layer protocol, and then implementing a server and client based on the design. 

### Features
* Very simple IRC-like protocol
* Basic CLI client
* Server handles many clients at once
* Multi-channel support

### Running 

To run the application, begin by starting the server module:

python3 server.py

Then, make a number of duplicate terminal windows within the same folder. In each of the other windows start a single client: 

python3 client.py 

The clients will then be able to communicate with each other via the shared server, create and join rooms, etc. 

### Python Modules 

* socket
* _thread
* threading
* sys
