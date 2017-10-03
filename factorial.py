def factorial(n):
    return 1 if n <2 else n*factorial(n-1)

for i in range(0, 10):
    print i, ' factorial =', factorial(i)