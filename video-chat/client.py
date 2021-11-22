import socket
import struct
import threading
import cv2
import random
import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Multi-threaded Video Chat App')
parser.add_argument("--host", type=str, help="Server IP Address")
parser.add_argument("--port", type=str, help="Server Port")
args = parser.parse_args()

ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = args.host
port = int(args.port)

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
            if ClientSocket:
                ClientSocket.sendall(str.encode(str(len(stringData)).ljust(16)))
                ClientSocket.sendall(stringData)

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
        threadNo = recvall(ClientSocket, 16).decode("utf-8")
        length = recvall(ClientSocket, 16).decode("utf-8")
        stringData = recvall(ClientSocket, int(length))
        data = np.fromstring(stringData, dtype="uint8")
        imgdec = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow("Client " + threadNo, imgdec)
        q = cv2.waitKey(1)
        if q == ord("q"):
            cv2.destroyAllWindows()
            break
    ClientSocket.close()
        
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))

inp = threading.Thread(target = inputs)
out = threading.Thread(target = output)
inp.start()
out.start()
