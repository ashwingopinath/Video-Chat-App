import socket
import struct
import threading
import cv2
import random
# from server import Client
import pickle
import numpy as np

import pyshine as ps

ClientSocket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ClientSocket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = input("Enter server IP: ")
port1 = int(input("Enter video port: "))
port2 = int(input("Enter audio port: "))
# host = '127.0.0.1'
# port = 1236

print('Waiting for connection')
try:
    ClientSocket1.connect((host, port1))
    ClientSocket2.connect((host, port2))
except socket.error as e:
    print(str(e))

encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def inputs():
    vid = cv2.VideoCapture(0)
    while True:
        while vid.isOpened():
            ret, img = vid.read() #video
            res, imgenc = cv2.imencode(".jpg", img, encode_params) #vid
            data = np.array(imgenc) #vid
            stringData = data.tostring() #vid
            if ClientSocket1:
                ClientSocket1.sendall(str.encode(str(len(stringData)).ljust(16)))
                ClientSocket1.sendall(stringData)

def audio_input():
    mode =  'send'
    name = 'SERVER TRANSMITTING AUDIO'
    audio,context= ps.audioCapture(mode=mode)
    while True:
        frame = audio.get() #audio
        aud = pickle.dumps(frame) #audio

        length = str.encode(str(len(aud)).ljust(16))
        if ClientSocket2:
            ClientSocket2.sendall(length)
            ClientSocket2.sendall(aud)
      

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
    while True:
        threadNo = recvall(ClientSocket1, 16).decode("utf-8")
        length = recvall(ClientSocket1, 16).decode("utf-8")
        #print("length:", length)
        stringData = recvall(ClientSocket1, int(length))
        data = np.fromstring(stringData, dtype="uint8")
        #print("data:", data)
        imgdec = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("Thread " + threadNo, imgdec)
        cv2.waitKey(1)
    ClientSocket1.close()


def audio_output():
    mode =  'get'
    name = 'CLIENT RECEIVING AUDIO'
    audio,context = ps.audioCapture(mode=mode)
    aud_data = b""
    while True:
        threadNo = recvall(ClientSocket2,16).decode("utf-8")
        length = recvall(ClientSocket2, 16).decode("utf-8")
        frame_data = recvall(ClientSocket2, int(length))
        frame = pickle.loads(frame_data)
        audio.put(frame)
    ClientSocket2.close() 
        
Response = ClientSocket1.recv(1024)
print(Response.decode('utf-8'))

inp = threading.Thread(target = inputs)
out = threading.Thread(target = output)
audio_inp = threading.Thread(target = audio_input)
audio_out = threading.Thread(target = audio_output)

audio_inp.start()
inp.start()
audio_out.start()
out.start()

