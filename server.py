from pyfiglet import Figlet
import os, socket, cv2, pickle,struct # Socket Create

os.system("clear")
pyf = Figlet(font='puffy')
a = pyf.renderText("Multi-Threaded Video Chat App")
b = pyf.renderText("Server")
os.system("tput setaf 3")

print(a)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)# Socket Bind
server_socket.bind(socket_address)# Socket Listen
server_socket.listen(1)
print("Listening at:",socket_address)# Socket Accept

while True:
    client_socket,addr = server_socket.accept()
    print('Connected to:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
    
    while(vid.isOpened()):
        ret,image = vid.read()
        img_serialize = pickle.dumps(image)
        message = struct.pack("Q",len(img_serialize))+img_serialize
        client_socket.sendall(message)
        
        cv2.imshow('Video from Server',image)
        key = cv2.waitKey(10) 
        if key ==13:
            client_socket.close()
