def factorial(f):
	factrl = 1
	for x in range(1,f+1):
		factrl *= x
		
	return factrl

n = input("Enter a number ")
print(str(n) + "!" + "=" + str(factorial(n)))
