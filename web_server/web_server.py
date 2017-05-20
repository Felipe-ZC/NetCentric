
import socket,os
from socket import AF_INET, SOCK_STREAM

'''
Creates a new socket binded to ocelot.aul.fiu.edu
and sarts listening for any incoming connections.
Only 1 queued connection is allowed at a time. 

Takes in an integer representing the port number.
Returns a new socket object.
'''
def startServer(port):
        serverSock = socket.socket(AF_INET,SOCK_STREAM)
        serverSock.bind(('ocelot.aul.fiu.edu',port))
        serverSock.listen(1)
        return serverSock

'''
Parses an HTTP GET request and returns the filename 
associated with the request.

Takes in a request message of the form:
    Request-Line                         
    HEADERS
    Blank line
    [ message-body ]          
Returns a string containing the requested filename
'''
def parseMsg(msg):
        # Compute path to requested file
        path  = msg.split()[1].partition('/')[2]
        return '/a/buffalo.cs.fiu.edu./disk/jccl-001/homes/fzuni005/' + path
'''
Processes an HTTP GET request.
'''
def main():
        serverSocket = startServer(5070)
        # Process requests made by client
        while True:
                try:
                        clientSocket, clientAdr = serverSocket.accept() # Get a new connection
                        clientMsg = clientSocket.recv(4096) # Get client message from socket
                        # Recv returns False if the connection was closed
                        if not clientMsg:
                                break
                        print clientMsg
                        # Get directory where rquested file is located
                        fName = parseMsg(clientMsg)
                        # Check if the file exists
                        userFile = open(fName) # Throws IOError if the file was not found
                        userData = userFile.read()
                        userFile.close()
                        HTTP_response = '''HTTP/1.1 200 OK\n\n''' + str(userData)
                        # Send file to client
                        clientSocket.send(HTTP_response)
                        clientSocket.close() # End client session
                        break
                except IOError:
                        # Send the user a 404 error
                        print '404!'
                        msg = 'HTTP/1.1 404 Not Found'
                        clientSocket.send(msg)
                        clientSocket.close()
                        break
        # End server session
        serverSocket.close()


# If this file is currently being executed
if __name__ == '__main__':
        main();
                                                                                                                                                                                                  82,8-15       Bot
                                                                                                                                                       1,0-1         Top
