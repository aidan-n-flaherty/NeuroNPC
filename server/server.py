#OUTDATED- DO NOT USE OR COMMENT

import socket
import server.socketManager as socketManager
from engine.core.world import World

from _thread import *
import threading

hostName = ""
port = 8080
 
def serverThread(socket):
    world = World()

    while True:
        data = socketManager.receiveMessage(socket)
        
        if not data:
            print('Client terminated connection')

            socket.release()
            break


 
    socket.close()
 
 
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((hostName, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(10)
    print("socket is listening")
 
    while True:
        sock, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(serverThread, (sock,))
    
    s.close()
 
if __name__ == '__main__':
    server()