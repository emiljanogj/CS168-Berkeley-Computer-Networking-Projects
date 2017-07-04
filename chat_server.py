import sys, socket, select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
channels={}

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    SOCKET_LIST.append(server_socket)
 
    print("Chat server started on port " + str(PORT))
 
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        for sock in ready_to_read:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        if data[0]=='\\':
                            actions=data.split(' ')
                            actions[0]=actions[0][1:]
                            for i in range(0,len(actions)):
                                actions[i]=actions[i].strip()
                            if (actions[0]=='join' or actions[0]=='create') and len(actions)<3:
                                msg='Not enough arguments for the command {0}\n'.format(actions[0])
                                sock.send(msg)
                            elif actions[0]=='list':
                                ch=''
                                for k in channels:
                                    ch+=str(k)
                                    ch+=' '
                                ch+='\n'
                                sock.send(ch)
                            elif actions[0]=='create':
                                chanFound=False
                                for k in channels:
                                    if k==actions[1]:
                                        chanFound=True
                                if chanFound:
                                    msg='Channel {0} already exists\n'.format(actions[1])
                                    sock.send(msg)
                                else:
                                    for k in channels:
                                        if sock in channels[k]:
                                            channels[k].remove(sock)
                                    channels[actions[1]]=[]
                                    channels[actions[1]].append(sock)
                                    print('Socket added succesfully to channel')
                            elif actions[0]=='join':
                                keyFound=False
                                for k in channels:
                                    if k==actions[1]:
                                        keyFound=True
                                if keyFound:
                                    for k in channels:
                                        if sock in channels[k]:
                                            channels[k].remove(sock)
                                    channels[actions[1]].append(sock)
                                else:
                                    msg='Channel {0} is not yet created\n'.format(actions[1],actions[1])
                                    sock.send(msg)
                        else:
                            print('Sending regular messages')
                            msg=data.split(' ')
                            name=msg[len(msg)-1]
                            msg=msg[0:len(msg)-1]
                            data=' '.join(str(x) for x in msg)
                            chan=' '
                            for k in channels:
                                if sock in channels[k]:
                                    chan=k
                            if chan!=' ':
                                broadcast(server_socket, sock, "\r" + '[' + name + '] ' + data,chan)  
                    else:
                        chname=' '
                        for k in channels:
                            if sock in channels[k]:
                                chname=k
                                channels[k].remove(sock)
                        if chname!=' ':
                            broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr,chname) 

                except:
                    chname=' '
                    for k in channels:
                        if sock in channels[k]:
                            chname=k
                    if chname!=' ':
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr,chname)
                    continue

    server_socket.close()
    
def broadcast (server_socket, sock, message,chan):
    print('Channel is '+chan)
    print(len(channels[chan]))
    for socket in channels[chan]:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
if __name__ == "__main__":

    sys.exit(chat_server())

