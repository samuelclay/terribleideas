import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.connect(server_address)
    while 1:
        try:
            sock.sendall(b"Hello world")
        except Exception as e:
            print(" ---> Exception: %s" % e)
