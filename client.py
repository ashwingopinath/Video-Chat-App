import socket
import cv2
import pickle
import struct
import threading
import time

def sending(port, ip) :
    # Creating the socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Getting the IP Address of localhost
    hostName = socket.gethostname()
    hostIP = socket.gethostbyname(hostName)
    hostIP = ip

    print(f'Server hosted at : {hostIP}:{port}')

    # Binding the socket with IP and Port
    s.bind((hostIP, port))
    s.listen(5)

    while True :
        # Accepting connection from clients
        # Here c is the client socket
        c, addr = s.accept()
        print(f'{addr} joined')

        if c :
            # Capturing video
            vid = cv2.VideoCapture(0)

            while (vid.isOpened()) :
                ret, img = vid.read()

                # Serializing the image (We can only send data in byte form)
                img_serialized = pickle.dumps(img)

                message = struct.pack("Q",len(img_serialized))+img_serialized
                c.sendall(message)
                    


def receive(port, ip) :
    # Defining socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    while True :
        try :
            # Connecting to the server
            s.connect((ip, port))
            break
        except :
            continue

    print('Connection Established')

    # The received data is stored here
    data = b""
    metadata_size = struct.calcsize("Q")

    while True :
        while len(data) < metadata_size:
            packet = s.recv(4*1024) 
            if not packet:
                break
            data += packet
        
        packed_msg_size = data[:metadata_size]
        data = data[metadata_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += s.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)

        cv2.imshow("Receiving Video from B",frame)
        cv2.waitKey(10)

YourIP = input('Enter your IP : ')
YourPort = int(input('Enter your port : '))
RecvIP = input('Enter sender IP : ')
RecvPort = int(input('Enter sender port : '))


x1 = threading.Thread(target=sending, args=(YourPort,YourIP,))
x2 = threading.Thread(target=receive, args=(RecvPort,RecvIP,))

x1.start()
x2.start()