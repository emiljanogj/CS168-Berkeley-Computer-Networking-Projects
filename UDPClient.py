from socket import *
serverName='hostname'
portNumber=12000
clientSocket=socket(socket.AF_INET,socket.SOCK_DGRAM)
message=raw_input('Enter the input data: ')
clientSocket.sendto(message,(serverName,portNumber))
recMess,servAdd=clientSocket.recvfrom(2048)
print(recMess)
clientSocket.close()
