def reverse_word_order(val):
    rev = ''
    words = val.split()
    for c in range(len(words)-1, -1, -1):
        rev += words[c]
        if c >-1:
            rev += ' '
    return rev

val = raw_input("Enter text: ")
print 'reversed word order=', reverse_word_order(val)
