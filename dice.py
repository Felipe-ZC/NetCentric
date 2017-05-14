import time

# Simulates the roll of a dice, num_dice is used to 
# determine the number of dice rolled, sides if used
# to determine the number of faces on the dice
def roll(num_dice,sides): 
	# Check for errors
	if(num_dice < 1 or sides <1):
		raise ValueError('Number of dice or faces is invalid!')
	print 'Rolling ' + str(num_dice) +  ' dice!'
	# Roll num_dice times
	for x in range(1, num_dice + 1):
		# Get time since epoch in miliseconds
		seed = int(time.time()*1000)
		# Number on the dice
		number = (seed % sides) + 1
		print number,
		# Wait 1 second
		time.sleep(1)

while True:
	try:
		# Prompt user
		dice_num = input("Enter the number of dice to roll: ")
		faces = input("Enter the number of faces on the dice: ")
		# Roll the dice
		roll(dice_num,faces)
		# Prompt user
		user_in = raw_input('Roll again? (y/n) ')
		if(user_in == 'n'):
			break
	# Catch ValueError exception
	except ValueError as err:
		print(err.args)
		print 'Try again!'
