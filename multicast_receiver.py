import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup_receiver():
    server_address = ('localhost', 10000)
    print('starting up on %s port %s' % server_address)
    
    sock.bind(server_address)
    sock.listen(1)
    
def receiver_loop():
    connection, client_address = sock.accept()
    try:
        data = connection.recv(999)
        print(data)
        return data
    except:
        connection.close()
      