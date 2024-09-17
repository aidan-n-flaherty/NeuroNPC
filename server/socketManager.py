import struct
import socket
import json

def generateMessage(obj) -> str:
    msg = json.dumps(obj, default=lambda o: o.__dict__, indent=0)
    msg = struct.pack('>I', len(msg)) + msg

    return msg

def sendMessage(sock: socket, obj) -> None:
    sock.sendall(generateMessage(obj))

def receiveMessage(sock: socket):
    dataLength = recvall(sock, 4)
    if not dataLength:
        return None
    
    msgLength = struct.unpack('>I', dataLength)[0]

    return recvall(sock, msgLength)

def recvall(sock: socket, n: int):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))

        if not packet:
            return None
        
        data.extend(packet)
    
    return json.loads(data)