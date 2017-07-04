import sys, socket, select,time
 
def chat_client():
    if(len(sys.argv) < 4) :
        print('Usage : python chat_client.py client_name hostname port')
        sys.exit()

    host = sys.argv[2]
    port = int(sys.argv[3])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)     
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
     
    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                msg = sys.stdin.readline()
                msg+=' '
                msg+=sys.argv[1]
                s.send(msg)
                try:
                    data=s.recv(2048)
                    sys.stdout.write('[Me]:')
                    sys.stdout.flush()
                    sys.stdout.write(data)
                    sys.stdout.flush()
                except socket.error:
                    time.sleep(0.0000000001)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())


