import socket
import os
import time
import smtp
from datetime import datetime
from socket import AF_INET, SOCK_STREAM

'''
Creates a new socket binded to ocelot.aul.fiu.edu
and sarts listening for any incoming connections.
Only 1 queued connection is allowed at a time.

Takes in an integer representing the port number.
Returns a new socket object.
'''
def startServer(port):
    serverSock = socket.socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('ocelot.aul.fiu.edu', port))
    serverSock.listen(1)
    return serverSock

'''
Parses HTTP request headers into an dictionary holding
each header and its value. The header names are the keys
while the header values are the values.

Takes in a string containing an HTTP request message.
Returns a dicotary of headers:values.
'''
def parseHeaders(headers):
    # Holds header to value mapping
    headersDict = {}
    # Separate each line in the request message
    headersList = headers.split('\n')
    # For each item in the list of headers...
    for item in headersList:
        # Separate header from value
        temp = item.partition(" ")
        # Map header to value in a dict
        headersDict[temp[0]] = temp[2]
    return headersDict

'''
Parses an HTTP request.
Takes in a request message of the form:
    Request-Line
    HEADERS
    Blank line
    [ message-body ]
Returns the request method as well as a dictionary
containing all the headers mapped to their values in
a tuple.
'''
def parseMsg(msg):
    headersMap = parseHeaders(msg)  # Parse http headers [O(n)]
    rMthd = msg.split()[0]  # Get request method (GET,POST,etc.)
    return (rMthd, headersMap)

'''
Processes an HTTP Post request.
Takes in a dictionary containing the headers mapped to their values.
Returns an HTTP response.
'''
def processPost(headers,cliMsg):
    # Check where to post data (Email)
    print 'Sending email.'
    # Parse request payload
    temp = cliMsg.split('\n')
    emailInfo = temp[len(temp)-1].split('&')
    print 'EmailInfo:\n', emailInfo
    emailDict = {}
    for value in emailInfo:
        tempList = value.split('=')
        emailDict[tempList[0]] = tempList[1]
    # Send email to requested location
    print emailDict
    smtp.sendEmail(emailDict)
    # Success
    return '''HTTP/1.1 200 OK\nContent-Type: text/html'''  + '''\n\n''' + '''Email sent succesfully!'''

def main():
    serverSocket = startServer(5010)
    # Process requests made by client
    while True:
        try:
            cSocket, clientAdr = serverSocket.accept()  # Get a new connection
            clientMsg = cSocket.recv(4096)  # Get client message from socket
            # Recv returns False if the connection was closed
            if not clientMsg:
                break
            print clientMsg
            # Get request method and headers mapped to their values
            request, headers = parseMsg(clientMsg)
            if request == 'POST':
                HTTP_response = processPost(headers,clientMsg)
                print 'Response:\n' + HTTP_response
                cSocket.send(HTTP_response)
            # End client session
            cSocket.close()
        except (IOError,OSError):
            # Send the user a 404 error
            print '404!'
            msg = 'HTTP/1.1 404 Not Found\n\n 404 Not Found!'
            cSocket.send(msg)
            cSocket.close()

    # End server session
    serverSocket.close()

# If this file is currently being executed
if __name__ == '__main__':
    main();
