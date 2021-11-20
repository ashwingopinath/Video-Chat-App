import socket
import threading

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1235

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def inputs():
    while True:
        inp = input("Say something:\n")
        ClientSocket.send(str.encode(inp))

def output():
    while True:
        res = ClientSocket.recv(1024)
        print(res.decode('utf-8'))
        print("Say something: ")

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
