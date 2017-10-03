import string

def capitalize_words1(val):
    caps = ''
    words = val.split()
    for c in range(0, len(words)):
        word = words[c]
        capword = string.upper(word[0]) + word[1:]
        caps += capword
        if(c < len(words)-1):
            caps += ' '
    return caps

def capitalize_words2(val):
    return string.capwords(val)

def capitalize_words3(val):
    caps = [i[0].upper() + i[1:] for i in val.split()]
    return ' '.join(caps)

val = raw_input("Enter text: ")
print 'Approach 1: capitalized words=', capitalize_words1(val)
print 'Approach 2: capitalized words=', capitalize_words2(val)
print 'Approach 3: capitalized words=', capitalize_words3(val)
