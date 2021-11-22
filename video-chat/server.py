import socket
import os
from _thread import *
import pickle
import struct
import cv2

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("HOST IP:", host_ip)
# host = '127.0.0.1'
host = host_ip
port = 9999
socket_address = (host, port)
ThreadCount = 0
threads = []
try:
    ServerSocket.bind(socket_address)
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
print("Listening at:",socket_address)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def threaded_client(connection, thread):
    connection.sendall(str.encode('\n\nWelcome to the Server\n\n'))
    while True:
        if connection:
            length = recvall(connection, 16)
            stringData = recvall(connection, int(length))        
        for i in range(ThreadCount):
            (client, threadNo) = threads[i]
            if thread != threadNo:
                if client:
                    client.sendall(str.encode(str(thread).ljust(16))) # New
                    client.sendall(length)
                    client.sendall(stringData)    
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print("Client:\n", Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    threads.append((Client, ThreadCount))
    start_new_thread(threaded_client, (Client, ThreadCount))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
