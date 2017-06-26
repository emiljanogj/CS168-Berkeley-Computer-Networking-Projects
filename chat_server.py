import sys
import socket
import select

host=''
port=9000
recv_buffer=4096
socket_list=[]

def chat_server():
    server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_sock.bind((host,port))
    server_sock.listen(10)
    socket_list.append(server_sock)
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0)
        for s in ready_to_read:
            try: 
                if s==server_sock:
                    con_sock,addr=s.accept()
                    socket_list.append(con_sock)
                    print('Client %s %s connected' %addr)
                    broadcast(server_sock,con_sock,'[%s,%s] entered our chatting room' %addr)
                else:
                    data=s.recv(recv_buffer)
                    if data:
                        broadcast(server_sock,s,'\r'+'['+str(s.getpeername())+']'+':'+str(data))
                    else:
                        socket_list.remove(s)
            except:
                broadcast('Client %s %s is offline' %addr)
                continue
        server_sock.close()

def broadcast(server_sock,sock,message):
    for socket in socket_list:
        if socket!=server_sock and socket!=sock:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in socket_list:
                    socket_list.remove(socket)

if __name__=='__main__':
    sys.exit(chat_server())
        
        
                
            
    
