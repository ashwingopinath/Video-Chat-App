import socket
import os
from _thread import *
import pickle
import struct
import cv2

ServerSocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("HOST IP:", host_ip)
# host = '127.0.0.1'
host = host_ip
port1 = 9999
port2 = 8003
socket_address1 = (host, port1)
socket_address2 = (host, port2)
ThreadCount = 0
threads = []
ThreadCount_aud = 0
threads_aud = []
try:
    ServerSocket1.bind(socket_address1)
    ServerSocket2.bind(socket_address2)
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket1.listen(5)
print("Listening at:",socket_address1)
ServerSocket2.listen(5)
print("Listening at:",socket_address2)

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
                client.sendall(str.encode(str(thread).ljust(16))) # New
                client.sendall(length)
                client.sendall(stringData)    
    connection.close()

def threaded_audio(connection, thread):
    aud_data = b""
    payload_size = struct.calcsize("Q")
    while True:
        if connection:
            length = recvall(connection, 16)
            frame_data = recvall(connection, int(length))
        for i in range(ThreadCount_aud):
            (client, threadNo) = threads_aud[i]
            if thread != threadNo:
                client.sendall(str.encode(str(thread).ljust(16)))
                client.sendall(length)
                client.sendall(frame_data)
    connection.close() 

while True:
    Client1, address1 = ServerSocket1.accept()
    print("Client_vid:\n", Client1)
    print('Connected to: ' + address1[0] + ':' + str(address1[1]))
    Client2, address2 = ServerSocket2.accept()
    print("Client_aud:\n", Client2)
    print('Connected to: ' + address2[0] + ':' + str(address2[1]))
    ThreadCount += 1
    threads.append((Client1, ThreadCount))
    start_new_thread(threaded_client, (Client1, ThreadCount))
    ThreadCount_aud += 1
    threads_aud.append((Client2, ThreadCount_aud))
    start_new_thread(threaded_audio, (Client2, ThreadCount_aud))
    print('Thread Number: ' + str(ThreadCount))
ServerSocket1.close()
ServerSocket2.close()
