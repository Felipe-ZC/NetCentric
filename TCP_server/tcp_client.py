import socket

def main():
	# host and port of the server 
	host = 'ocelot.aul.fiu.edu'
	port = 5070

	client = socket.socket() # A TCP socket object
	# Try to connect to the server (waits!)
	client.connect((host,port)) # Takes in host & port in a tuple

	# Ask the user for a message to send 
	print 'Send the server a message, press q to quit.'
	clientMsg = ''

	# Process input
	while clientMsg != 'q':
		clientMsg = raw_input("> ")
		client.send(clientMsg) # Send message to server
		serverData = client.recv(1024) # Get server message
		print 'The server returned the following message: ' + str(serverData)

	# End connection with server
	client.close()

# If this file is currently being executed
if __name__ == '__main__':
	main();
