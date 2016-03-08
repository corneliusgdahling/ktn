# -*- coding: utf-8 -*-
import socket
import sys
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """
    data = " ".join(sys.argv[1:])

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        try:
            self.run()
        finally:
            self.connection.close()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        print 'Connected'
        self.connection.sendall(self.data + "\n")
        received = self.connection.recv(1024)
        print "Sent:     {}".format(self.data)
        print "Received: {}".format(received)
        
    def disconnect(self):
        # TODO: Handle disconnection
        self.disconnect(self)

    def login(self):
        # TODO: kode for inlogging
        pass

    def logout(self):
        # TODO: kode for utlogging
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass

        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
