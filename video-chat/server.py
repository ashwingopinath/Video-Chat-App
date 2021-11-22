import socket
import os
from _thread import *
import pickle
import struct
import cv2

# from client import ClientSocket

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
print("Listening at:",socket_address) # Socket Accept

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
            # vid = cv2.VideoCapture(0)
            length = recvall(connection, 16)
            # print("length:", length.decode("utf-8"))
            stringData = recvall(connection, int(length))
            # connection.sendall(length)
            # connection.sendall(stringData)
        #     data = b""
        #     metadata_size = struct.calcsize("Q")
        #     while len(data) < metadata_size:
        #         packet = connection.recv(1024*1024)
        #         if not packet:
        #             break
        #         data += packet
        #     packed_msg_size = data[:metadata_size]
        #     data = data[metadata_size:]
        #     msg_size = struct.unpack("Q", packed_msg_size)[0]
        #     while len(data) < msg_size:
        #         data += connection.recv(1024*1024)
        #     frm_data = data[:msg_size]
        #     frm = pickle.loads(frm_data)
        #     img_serialized = pickle.dumps(frm)
        #     msg = struct.pack("Q", len(img_serialized)) + img_serialized
        # else:
        #     break
        
        for i in range(ThreadCount):
            (client, threadNo) = threads[i]
            # print("thread:", i+1)
            # print("threadNo:", threadNo)

            if thread != threadNo:
                client.sendall(str.encode(str(thread).ljust(16))) # New
                client.sendall(length)
                client.sendall(stringData)
        
            # client.sendall(msg)
        
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
