
'''
Unlike TCP, UDP is unreliable and conneciton less.
This mean that there is no guarantee that the data
sent will arrive at its destionatin. Connection less
means that there is no connection established between
the sender and reciever, the protocol simply sends the
data away to some address.
'''
import socket
from socket import AF_INET, SOCK_DGRAM

def main():
        host = 'ocelot.aul.fiu.edu'
        port = 5071

        # Create a new UDP socket object
        udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udpSocket.bind((host,port))
        print 'Ready to serve!'
        while True:
            # Receive the client packet along with the address it is coming from
            msg, addr = udpSocket.recvfrom(2048)
            if not msg: # If the client connection was closed...
                break;
            # Send IP address to server
            serverMsg = 'Ping succesful at ' + host
            udpSocket.sendto(serverMsg, addr)
        # End connection with client
        udpSocket.close()

# If this file is currently being executed
if __name__ == '__main__':
        main();

