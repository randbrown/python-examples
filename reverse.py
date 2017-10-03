def reverse(val):
    rev = ''
    for c in range(len(val)-1, -1, -1):
        rev += val[c]
    return rev

val = raw_input("Enter text: ")
print 'reversed=', reverse(val)
