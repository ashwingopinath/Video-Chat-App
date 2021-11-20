import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1235
ThreadCount = 0
threads = []
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, thread):
    connection.sendall(str.encode('\n\nWelcome to the Server\n\n'))
    while True:
        data = connection.recv(2048)
        if not data:
            break
        reply = str(thread) + ': ' + data.decode('utf-8')
        for i in range(ThreadCount):
            (client, threadNo) = threads[i]
            print(threadNo)
            # if threadNo != i + 1: 
            client.sendall(str.encode(reply))
            print("reached here")
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
