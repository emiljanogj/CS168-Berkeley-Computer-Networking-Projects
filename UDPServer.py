from socket import *
portNumber=12000
serverSocket=socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.bind(('',portNumber))
print("The server is ready to receive")
while 1:
    mess,clientAdd=serverSocket.recvfrom(2048)
    modifiedMess=mess.upper()
    serverSocket.sendto(modifiedMess,clientAdd)
