import socket

def main():
        # Host this server on ocelot
        hostName = 'ocelot.aul.fiu.edu'
        port = 5070

        server = socket.socket()
        # Binds the above socket to the localhost.
        # Takes in address and port as a tuple.
        server.bind((hostName,port))

        # Have the server start listening for TCP connections.
        # Only 1 queued connection is allowed at a time.
        server.listen(1)

        client, clientAddr = server.accept() # Get a new connection and its address
        print 'New connection from: ' + str(clientAddr)

        # As long as the server is communicating with the client
        while True:
                # Holds data recieved from a client (Max: 1024 bytes)
                clientData = client.recv(1024)
                if not clientData: # recv returns False if the connection is closed
                        break
                print 'Message from client: ' + str(clientData)
                clientData = str(clientData).upper() # Convert client data as a string to uppercase
                # Return data to client
                print 'Preparing to send: ' + str(clientData)
                client.send(clientData)

        # End connection with client
        client.close()

# If this file is currently being executed
if __name__ == '__main__':
        main();

