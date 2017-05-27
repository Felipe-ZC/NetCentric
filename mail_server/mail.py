import socket
import os
import time
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
    serverSock.bind(('localhost', port))
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
MAIL CLIENT
'''
def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg
    socket.send(msg + '\r\n')

def startEmail(emailData):
    # Conenct to FIU's email server
    serverName = 'smtp.cis.fiu.edu'
    serverPort = 25
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    # Server should send 220 to indicate succesful connect ion
    recv=send_recv(clientSocket, None, '220')

    clientName = 'User'
    userName= emailData['from'].partition('%40')[0]
    userServer= emailData['from'].partition('%40')[1]
    toName= emailData['to'].partition('%40')[0]
    toServer= emailData['to'].partition('%40')[1]
    #Send HELO command and print server response.
    heloCommand='HELO %s' % clientName
    recvFrom = send_recv(clientSocket, heloCommand, '250')
    #Send MAIL FROM command and print server response.
    fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
    recvFrom = send_recv(clientSocket, fromCommand, '250')
    #Send RCPT TO command and print server response.
    rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
    recvRcpt = send_recv(clientSocket, rcptCommand, '250')
    #Send DATA command and print server response.
    dataCommand='DATA'
    dataRcpt = send_recv(clientSocket, dataCommand, '354')
    #Send message data.
    send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
    send(clientSocket, "From: User <%s@%s>" % (userName, userServer));
    send(clientSocket, emailData['sub']);
    send(clientSocket, "To: %s@%s" % (toName, toServer));
    send(clientSocket, ""); #End of headers
    send(clientSocket, emailData['msg']);
    #Message ends with a single period.
    send_recv(clientSocket, ".", '250');
    #Send QUIT command and get server response.
    quitCommand='QUIT'
    quitRcpt = send_recv(clientSocket, quitCommand, '221')

'''
END MAIL clientSocket
'''

'''
Processes an HTTP GET request, also handles conditional GET.
Takes in a dict containing the headers and their values.
Returns a tuple containing the approprivate values to send
an email through SMTP.
'''
def processGET(headersMap):
    # Holds mail credentials mapped to their values
    valueDict = {}
    vals = headersMap['GET'].partition(" ")[0].partition("/?")[2].split("&")
    # Parse values
    for value in vals:
        tempList = value.split("=")
        valueDict[tempList[0]] = tempList[1]
    print 'vals: ' , vals
    print 'dict' , valueDict

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
            if request == 'GET':
                mailData = processGET(headers)
                startEmail(mailData)

            HTTP_response = '''HTTP/1.1 200 OK\n\nMessage sent succesfully!'''
            cSocket.send(HTTP_response)
            cSocket.close() # End client session'''
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
