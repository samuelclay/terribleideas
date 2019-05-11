import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    while 1:
        try:
            server_address = ('localhost', 10000)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)
            sock.sendall(b"Hello world")
        except Exception as e:
            print(" ---> Exception: %s" % e)
            break
