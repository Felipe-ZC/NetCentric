
# max_of_three takes 3 arguments and returns the largest of those 3
def max_of_three(x,y,z):
	if(x > y and x > z): return z
	elif(y > x and y > z): return y
	else: return z

print("Enter 3 numbers")
a = input("Enter the 1st number ")
b = input("Enter the 2nd number ")
c = input("Enter the 3rd number ")
max = str(max_of_three(a,b,c))
print("The greatest number is " + max)