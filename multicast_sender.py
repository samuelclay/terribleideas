import socket

def send_message(message):
  MCAST_GRP = '224.1.1.1'
  MCAST_PORT = 5007
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
  sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
  
if __name__ == "__main__":
    while 1:
        send_message("Hello world")