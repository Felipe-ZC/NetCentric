
import socket
import os
import smtp
from datetime import datetime
from socket import AF_INET, SOCK_STREAM

# Custom Exception, signals 304 error
class Error_304(Exception):
    pass

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
Parses HTTP request headers into a dictionary holding
each header and its value.
Takes in a string containing an HTTP request message.
Returns a dicotary of headers:values.
'''
def parseHeaders(headers):
    # Holds header to value mapping
    headersDict = {}
    # Separate each line in the request message
    headersList = headers.split('\r\n')
    #print headersList
    # For each item in the list of headers...
    for item in headersList:
        # Separate header from value
        temp = item.partition(" ")
        # Map header to value in a dict
        headersDict[temp[0]] = temp[2]
    # Testing only
    print headersDict
    return headersDict

'''
Compares two dates in the following format:
day month(Abbreviation) year time(GMT)

Takes in two dates as strings.
Returns true if d1 comes after d2, false otherwise
'''
def compareDates(d1, d2):
    # Convert string dates to datetime objects
    date1 = datetime.strptime(d1, '%d %b %Y %H:%M:%S')
    date2 = datetime.strptime(d2, '%d %b %Y %H:%M:%S')
    if date1 >= date2:
	       return True
    else:
	       return False


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
Processes an HTTP GET request, also handles conditional GET.
Takes in a dict containing the headers and their values.
Returns a suitable HTTP response message as a string.
'''
def processGET(headersMap):
    # Compute path for requested file
    path = headersMap['GET'].partition(" ")[0]
    fullPath = '/a/buffalo.cs.fiu.edu./disk/jccl-001/homes/fzuni005/' + path
    # Check if file exists, raise IOError if nonexistent file is found
    usrFile = open(fullPath)
    usrData = usrFile.read()
    usrFile.close()
    # Get date file was last modified
    lastModified = datetime.fromtimestamp(
        os.path.getmtime(fullPath)).strftime('%d %b %Y %H:%M:%S')

    # Check for If-Modified-Since [O(1)]
    if 'If-Modified-Since:' in headersMap:
        # Get requested date, save only day, month, year and time
        requestDate = headersMap['If-Modified-Since:']
        print 'requestedDate: ' + requestDate + ' lastModified: ' + str(lastModified)
        # Check if the requested file meets the date criteria
        if not compareDates(lastModified, requestDate):
            raise Error_304("304 error")

    # Success
    return '''HTTP/1.1 200 OK\nLast-Modified:'''  + str(lastModified) + '''\nContent-Type: text/html'''  + '''\n\n''' + usrData


'''
Processes an HTTP Post request.
Takes in a dictionary containing the headers mapped to their values.
Returns an HTTP response.
'''
def processPost(headers,cliMsg):
    # Check where to post data (Email)
    if headers['POST'] == '/public_html/felipe_server/mail_server HTTP/1.1':
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
    serverSocket = startServer(5070)
    # Process requests made by client
    while True:
        try:
            clientSocket, clientAdr = serverSocket.accept()  # Get a new connection
            clientMsg = clientSocket.recv(4096)  # Get client message from socket
            # Recv returns False if the connection was closed
            if not clientMsg:
                break
            print 'Request:\n'+ clientMsg
            # Get request method and headers mapped to their values
            request, headers = parseMsg(clientMsg)
            if request == 'GET':
                HTTP_response = processGET(headers)
                print 'Response:\n' + HTTP_response
                clientSocket.send(HTTP_response)
            if request == 'POST':
                HTTP_response = processPost(headers,clientMsg)
                print 'Response:\n' + HTTP_response
                clientSocket.send(HTTP_response)
            # userFile = open(fName) # Throws IOError if the file was not found
            # userData = userFile.read()
            # userFile.close()
            # response = HTTP/1.1 200 OK\nContent-Type: text/plain\nLast-Modified: + str(lastMod) + '\n\n' + str(userData)
            # Send file to client
            clientSocket.close() # End client session'''
        except (IOError,OSError):
            # Send the user a 404 error
            print '404!'
            msg = 'HTTP/1.1 404 Not Found\n\n 404 Not Found!'
            clientSocket.send(msg)
            clientSocket.close()
        except Error_304:
            # The user a 304 error
            print '304!'
            # fName, lastMod = parseMsg(clientMsg)
            msg = 'HTTP/1.1 304 Not Modified\n\n' + ' File has not been modified since requested date'
            clientSocket.send(msg)
            clientSocket.close()

    # End server session
    serverSocket.close()

# If this file is currently being executed
if __name__ == '__main__':
    main();
