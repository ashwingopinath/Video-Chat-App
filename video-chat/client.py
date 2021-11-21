import socket
import struct
import threading
import cv2
# from server import Client
import pickle

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1236

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def inputs():
    while True:
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            ret, img = vid.read()
            img_serialized = pickle.dumps(img)
            msg = struct.pack("Q", len(img_serialized)) + img_serialized
            ClientSocket.sendall(msg)

def output():
    data = b""
    metadata_size = struct.calcsize("Q")
    while True:
        while len(data) < metadata_size:
            packet = ClientSocket.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:metadata_size]
        data = data[metadata_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += ClientSocket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Thread", frame)
        cv2.waitKey(10)
        
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
