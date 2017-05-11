# Reverses the user's input, valid input are strings or integers and doubles.

# Reverses the order of arg
def reverse(arg):
	# Get size of string
	size = len(arg)
	# Holds reversed version of arg
	reverse = ''
	# Holds index of first element in arg
	first = 0
	# Holds index of last element in arg
	last = size - 1

	# Iterate through list backwards
	while first <= last:
		# Add characters in arg to reverse
		reverse += arg[last]
		# Update last
		last -= 1

	# Once arg has been iterated through, return reverse
	return reverse


# Prompt user
print 'Welcome to reverse.py! Please enter a word or number, when done press the return key (enter)'
# Holds user input
user_in = raw_input()
# Print results
print 'Original: ' + user_in
print 'Reverse ' + reverse(user_in)


	
