
import socket, time
from socket import AF_INET, SOCK_DGRAM

def main():
        hostName = "ocelot.aul.fiu.edu"
        portNum = 5071

        # UDP socket
        client = socket.socket(AF_INET,SOCK_DGRAM)

        # Prompt user for input
        print 'Send any message to ping the server, send \'q\' to quit.'
        msg = ''

        while msg != 'q':
                msg = raw_input('>')
                # Sends the message to the server
                client.sendto(msg,(hostName,portNum))
                # Used to calculate rtt
                sendTimeMillis = int(round(time.time() * 1000))
                # End the connection if the server takes more than 20 ms to respond
                client.settimeout(0.02)
                # Get and display server response
                serverMsg , serverAdr = client.recvfrom(2048)
                recieveTimeMillis = int(round(time.time() * 1000))
                print 'The server says: ' + serverMsg
                print 'RTT: ' + str(recieveTimeMillis - sendTimeMillis) + ' milliseconds'
        # End connection to the server
        client.close()

# For the main module
if __name__ == '__main__':
        main();
