def longest_word(sen): 
    words = sen.split()
    words.sort(key=len, reverse=True)
    return words[0] if words else None

longest = longest_word(raw_input("Enter some words: "))  
print 'Longest word is: ', longest
