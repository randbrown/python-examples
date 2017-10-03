import string

def reverse_each_word(val):
    rev = []
    words = val.split()
    for w in range(0, len(words)):
        word = words[w]
        revword = ''
        for c in range(len(word)-1, -1, -1):
            revword += word[c]
        rev += [revword]
    return string.join(rev)

val = raw_input("Enter text: ")
print 'each word reversed=', reverse_each_word(val)
