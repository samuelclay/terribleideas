import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup_receiver():
    server_address = ('localhost', 10000)
    print('starting up on %s port %s' % server_address)
    
    sock.bind(server_address)
    sock.listen()
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    

def select_loop():
    readable = [sock] # list of readable sockets.  s is readable if a client is waiting.
    i = 0
    # r will be a list of sockets with readable data
    r,w,e = select.select(readable,[],[],0)
    for rs in r: # iterate through readable sockets
        if rs is sock: # is it the server
            c,a = sock.accept()
            print('\r{}:'.format(a),'connected')
            readable.append(c) # add the client
        else:
            # read from a client
            data = rs.recv(1024)
            if not data:
                print('\r{}:'.format(rs.getpeername()),'disconnected')
                readable.remove(rs)
                rs.close()
            else:
                print('\r{}:'.format(rs.getpeername()),data)
                return data
    # a simple spinner to show activity
    i += 1
    print('/-\|'[i%4]+'\r',end='',flush=True)
    
def receiver_loop():
    connection, client_address = sock.accept()
    try:
        data = connection.recv(11)
        return data
    except Exception as e:
        print(" ---> Exception: %s" % e)
        connection.close()
      