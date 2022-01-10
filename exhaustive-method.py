from nltk.corpus import words
import time

password_length = 3
# produce all possible keys (17576 in total) with small letters of size three
import itertools
alphabet = 'abcdefghijklmnopqrstuvwxyz'
keys = [''.join(i) for i in itertools.product(alphabet, repeat = password_length)]

print(f'There are {len(keys)} possible keys of size {password_length}.')

filename = './encrypted-message.txt'
with open(filename, 'r') as f:
    data = [int(n) for n in f.readlines()[0].split(',')]

print(f'Characters in the encrypted message: {len(data)}')

english_words = set(words.words())
def is_english_word(word):
    return word in english_words

candidate_keys = []
start = time.time()
for i in range(len(keys)):
    if i % 1000 == 0 and i > 0:
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
    decrypted_message = ''.join(message)
    # split the final message with the space character and find how many actual words it contains
    # we limit it to words of size > 2 and stop if the text has 5 actual words in the first 20 ones.
    actual_words_found = set()
    
    for w in decrypted_message.split():
        if len(w) > 2 and  is_english_word(w):
            actual_words_found.add(w)
            if len(actual_words_found) >= 10:
                print(f'Found new candidate key! : [{key}] \nWordlist: {actual_words_found}')
                print('-'*53)
                print(f'Decrypted message: {decrypted_message}')
                candidate_keys.append(key)
                break
    
print(f'List of candidate passwords {candidate_keys}.')