from nltk.corpus import words
import itertools
import time

filename = './data/encrypted-message.txt'
with open(filename, 'r') as f:
    data = [int(n) for n in f.readlines()[0].split(',')]
print(f'Characters in the encrypted message: {len(data)}')

english_words = set(words.words())
def is_english_word(word):
    return word in english_words

password_length = 3
# frequent_letters = ['e', 't', 'a', 'i', 'o', 'n', 's', ' ']
frequent_letters = ['e', 'a', 'i', 'o', ' ']

# build a dictionary with the frequences of each character
dc = {i:{} for i in range(password_length)}
for i, d in enumerate(data):
    key_index = i % password_length
    if d not in dc[key_index]:
        dc[key_index][d] = 1
    else:
        dc[key_index][d] += 1

# compute the percentage of frequencies for each character
# for i in range(password_length):
#     total_letters = sum(dc[i].values())
#     print(f'There are {total_letters} for character {i} in key')
#     for k in dc[i].keys():
#         dc[i][k] = dc[i][k]/total_letters

# show the most frequent characters
# for i in range(password_length):
#     print(f"{'-'*25} {i} {'-'*25}")
#     freq = {k: v for k, v in sorted(dc[i].items(), key=lambda item: item[1], reverse=True)}
#     for k in list(freq.keys())[0:5]:
#         print(f'{k} : {freq[k]}')        
a = []
for i in range(password_length):
    print(f"{'-'*25} {i} {'-'*25}")
    freq = {k: v for k, v in sorted(dc[i].items(), key=lambda item: item[1], reverse=True)}
    # get the most frequent letter
    for k in list(freq.keys())[0:1]:
        candidates = [chr(k ^ ord(c)) for c in frequent_letters]
        print(f'Most frequent ASCII {k} for password index {i}')
        print(f'Candidate letters: {candidates}')
        a.append(candidates)
        
print('-'*53)

keys = [''.join(s) for s in itertools.product(*a)]
print(f'Total Candidate Keys {len(keys)}')
def encryption_algorithm(ascii_text, key):
    ascii_key = [ord(c) for c in key]
    message = []
    for i in range(len(ascii_text)):
        key_index = i % len(key)
        xor =  ascii_text[i] ^ ascii_key[key_index]
        message.append(chr(xor))
    return ''.join(message)

start = time.time()

candidate_keys = []
for i, key in enumerate(keys):
    if i % 50 == 0 and i > 0:
        print(f'Reached {i}-th key: {keys[i]}, seconds elapsed: {round(time.time()-start, 2)}')
    decrypted_message = encryption_algorithm(data, key)
    actual_words_found = set()
    for w in decrypted_message.split():
        if len(w) > 2 and  is_english_word(w):
            actual_words_found.add(w)
            if len(actual_words_found) > 10:
                print(f'Found new candidate key! : [{key}] \nWordlist: {actual_words_found}')
                print('-'*53)
                print(f'Decrypted message: {decrypted_message}')
                candidate_keys.append(key)
                break
print('-'*53)
print(candidate_keys)