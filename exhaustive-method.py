from nltk.corpus import words
import time

password_length = 3
# produce all possible keys (17576 in total) with small letters of size three
import itertools
alphabet = 'abcdefghijklmnopqrstuvwxyz'
keys = [''.join(i) for i in itertools.product(alphabet, repeat = password_length)]

print(f'There are {len(keys)} possible keys of size {password_length}.')

filename = 'p059_cipher.txt'
with open(filename, 'r') as f:
    data = [int(n) for n in f.readlines()[0].split(',')]

print(f'Characters in the encrypted message: {len(data)}')

def is_english_word(word):
    return word in words.words()

w = 'dogs'
res = is_english_word(w)

print('Word {} {} an english word'.format(w, ('is' if res else 'is not')))

start = time.time()
for i in range(len(keys)):
    if i % 50 == 0 and i > 0:
        print(f'Reached {i}-th key: {keys[i]}, seconds elapsed: {round(time.time()-start, 2)}')
        
    # find the total actual english words from this message
    key = keys[i]
    # translate key to ascii code
    ascii_key = [ord(c) for c in key]
    message = []
    for i in range(len(data)):
        # find the key index that we are going to use to decipher the character of the message
        key_index = i % len(key)
        xor = data[i] ^ ascii_key[key_index]
        # decipher the int xor result to the character with chr() function 
        message.append(chr(xor))
    # combine all message in a string
    message = ''.join(message)
    # split the final message with the space character and find how many actual words it contains
    # if more than 5 words are found, potentially this is the right key.
    actual_words_found = set()
    for w in message.split():
        if is_english_word(w):
            actual_words_found.add(w)
    if len(actual_words_found) > 10:
        print(f'Found new candidate key! Wordlist: {actual_words_found} Key that was used: {key}')
        print(f'Decrypted message: {message}')
        
# abp, adp