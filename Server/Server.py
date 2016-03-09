# -*- coding: utf-8 -*-
import SocketServer
from datetime import datetime
import time
import json
import re
import threading
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

all_messages = []
users = []

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    global all_messages
    global users

    def timestamp(self):
        return datetime.now().strftime("%H:%M")

    def broadcast(self, data):
        all_messages.append(data)


    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.connection = self.request
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.logged_in = False
        self.sentdata = 0


        print 'Client connected: ' + self.ip + ':' + str(self.port)


        self.t = threading.Thread(target=self.send_updates)
        self.t.setDaemon=True
        self.t.start()

        while True:

            data = self.connection.recv(1024).strip()

            if data:
                print(data)
                self.process_data(data)
            else:
                print ('Client disconnected!')
                break

    def finish(self):
        try:
            users.remove(self.username)
        except:
            pass

    def process_data(self, data):
        decoded = json.loads(data)

        if decoded['request'] == 'login':
          self.login(decoded.get('username', ''))

        if not self.logged_in:
            return

        if decoded['request'] == 'logout':
          self.logout()

        if decoded['request'] == 'names':
            for i in range(0,len(users)):
                self.send({'response':'names','users':users[i]})

        if decoded['request'] == 'message':
            if decoded.get("message", "") != "":
                padd=" "*(len(max(users, key=len))-len(self.username))
                message = self.timestamp()+padd+" %s| %s"%(self.username, decoded['message'])
                self.broadcast(message)



    def login(self, username):
        if(not re.match(r'^[A-Za-z0-9_]+$', username)):
            self.send({'response':'login', 'error':'Invalid username!', 'username':username})
            return
        if not username in users:
            self.username = username
            users.append(username)
            self.logged_in = True
            self.send({'response':'login', 'username':self.username})
            self.broadcast("*** " + self.username + " has joined the chat.")

        else:
            self.send({'response': 'login', 'error':'Name already taken!', 'username':username})

    def logout(self):
        try:
            users.remove(self.username)
            self.logged_in = False
            self.send({'response': 'logout', 'nick': self.username})
            self.broadcast("*** " + self.username + " has left the chat.")
        except ValueError:
            self.send({'response': 'logout', 'error':'Not logged in!', 'nick': self.username})

    def send(self, data):
        self.request.sendall(json.dumps(data))

    def send_updates(self):
        while True:
            if self.sentdata < len(all_messages) and self.logged_in:
                    for x in range(self.sentdata, len(all_messages)):
                        self.send({"response":"message", "message":all_messages[x]})
                        self.sentdata += 1
            time.sleep(0.2) #0.2 seconds


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = '', 9999
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()