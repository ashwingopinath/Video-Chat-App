import socket
import os
from _thread import *
import pickle
import struct
import cv2

ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
print("Listening at:",socket_address) # Socket Accept


def threaded_client(connection, thread):
    connection.sendall(str.encode('\n\nWelcome to the Server\n\n'))
    while True:
        if connection:
            # vid = cv2.VideoCapture(0)
            msg = connection.recv(4*1024)
        else:
            break
        
        for i in range(ThreadCount):
            (client, threadNo) = threads[i]
            client.sendall(msg)
        
            # cv2.imshow("Thread " + str(thread), img)
    
    connection.close()


    # #     data = connection.recv(2048)
    # #     if not data:
    # #         break
    # #     reply = str(thread) + ': ' + data.decode('utf-8')
    # #     for i in range(ThreadCount):
    # #         (client, threadNo) = threads[i]
    # #         print(threadNo)
    # #         # if threadNo != i + 1: 
    # #         client.sendall(str.encode(reply))
    # #         print("reached here")
    # connection.close()

while True:
    Client, address = ServerSocket.accept()
    print("Client:\n", Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    threads.append((Client, ThreadCount))
    start_new_thread(threaded_client, (Client, ThreadCount))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
