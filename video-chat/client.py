import socket
import struct
import threading
import cv2
import random
# from server import Client
import pickle
import numpy as np

ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = input("Enter server IP: ")
port = int(input("Enter port: "))
# host = '127.0.0.1'
# port = 1236

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def inputs():
    while True:
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            ret, img = vid.read()
            res, imgenc = cv2.imencode(".jpg", img, encode_params)
            data = np.array(imgenc)
            stringData = data.tostring()
            # img_serialized = pickle.dumps(img)
            # msg = struct.pack("Q", len(img_serialized)) + img_serialized
            ClientSocket.sendall(str.encode(str(len(stringData)).ljust(16)))
            ClientSocket.sendall(stringData)
            # ClientSocket.sendall(msg)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def output():
    # data = b""
    # metadata_size = struct.calcsize("Q")
    # print("metadata_size:", metadata_size)
    while True:
        # while len(data) < metadata_size:
        #     packet = ClientSocket.recv(4*1024)
        #     if not packet:
        #         break
        #     data += packet
        # packed_msg_size = data[:metadata_size]
        # data = data[metadata_size:]
        # msg_size = struct.unpack("Q", packed_msg_size)[0]

        # while len(data) < msg_size:
        #     data += ClientSocket.recv(4*1024)
        # frame_data = data[:msg_size]
        # data = data[msg_size:]
        # frame = pickle.loads(frame_data)
        threadNo = recvall(ClientSocket, 16).decode("utf-8")
        length = recvall(ClientSocket, 16).decode("utf-8")
        print("length:", length)
        # print("length:", length)
        stringData = recvall(ClientSocket, int(length))
        data = np.fromstring(stringData, dtype="uint8")
        print("data:", data)
        imgdec = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("Thread " + threadNo, imgdec)
        cv2.waitKey(1)
        
        # res = ClientSocket.recv(1024)
        # print(res.decode('utf-8'))
        # print("Say something: ")

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
# while True:
#     Response = ClientSocket.recv(1024)
#     print(Response.decode('utf-8'))
#     Input = input('Say Something: ')
#     ClientSocket.send(str.encode(Input))

inp = threading.Thread(target = inputs)
out = threading.Thread(target = output)
inp.start()
out.start()
# ClientSocket.close()
