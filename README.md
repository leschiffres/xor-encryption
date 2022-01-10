# xor-encryption
An algorithm to find the encryption / decryption key of a given message.

This algorithm is inspired by this [Project Euler Problem](https://projecteuler.net/problem=59). 

## Encryption Method

The idea is that to decrypt/encrypt message one can use the **XOR** function along with a **key / password**. The reason why this is so useful is the property of the XOR function that `using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.`

Concretely, one can take the pure text and translate each character to its corresponding ASCII code, do the same with the password characters and then XOR them. Since their lengths are not the same the key is repeated cyclically throughout the message.

| **Example**|
|-|
|Given the text `I am a beautiful green tree.` and password `dog` then their corresponding ASCII codes would be `[73, 32, 97, 109, 32, 97, 32, 98, 101, 97, 117, 116, 105, 102, 117, 108, 32, 103, 114, 101, 101, 110, 32, 116, 114, 101, 101, 46]` and `[100, 111, 103]`. Thus, the encrypted message would be `[73 XOR 100, 32 XOR 111, 97 XOR 103, 109 XOR 100 ...]` which would be equal to `[45, 79, 6, 9, 79, 6, 68, 13, 2, 5, 26, 19, 13, 9, 18, 8, 79, 0, 22, 10, 2, 10, 79, 19, 22, 10, 2, 74]`. Thus getting the latter ASCII codes and applying the XOR function along with `[100, 111, 103]` (the keys corresponding ASCII codes), would give us the initial message |

Remarks:
- In python3, one can convert a character `c` into ASCII by using the function `ord(c)`.
- In python3, one can convert an ASCII code `n` into a character by using the function `chr(n)`.

## Breaking the password

But how one can actually break such a password given just the encrypted message?

### Exhaustive Method

[exhaustive-method.py](./exhaustive-method.py)

In the [project euler's instance](./encrypted-message.txt) we know that the password length is equal to 3 including only small characters, which really makes our lives easier. We could do this exhaustively by trying the `26*26*26 = 17576` possible passwords and try to find how many actual english words are found inside the text after the decryption. Thus, we decrypt the message, split the words by the space character and then try to find if each word exists in the english dictionary. To obtain a suitable set of english words we use the nltk package (`from nltk.corpus import words`).

### Frequency Method

[character-frequency.py](./character-frequency.py)

While the exhaustive method in this case works fast due to its limited search space, it can be really slow when the password length significantly increases. However, we can limit the search space by exploitting the fact, that some letters in the english alphabet, are more frequent than others. According to https://en.wikipedia.org/wiki/Letter_frequency the most frequent letters are `'e', 't', 'a', 'o', 'i', 'n', 's']`, but the letter `e` seems to be appearing more frequently than the rest.

By assuming that the most frequent ones are the character `'e'` & the empty space `' '`, we can get the most frequent encoded ascii character in each position and xor with `'e'` or `' '` to find a potential character. 

The algorithm we use is the following:

1. In this case we consider that the most frequent characters are `'e', 'a', 'i', 'o', ' '`. 
2. Then for each password digit we collect its corresponding ASCII codes of the encrypted message and find the most frequent one. 
3. The most frequent one should be one of the letters in the above list (we can extend this to consider the first `k` most frequent characters)
4. Thus, we build a list of candidate keys by considering the cartesian product for each password digit e.g if the most frequent code at digit 1 is 69 we XOR it with each of the ASCII codes of `'e', 'a', 'i', 'o', ' '` and get a list of potential codes.
5. Finally we repeat the process to estimate if a decrypted message is a proper english one, using the same method as in the exhaustive apprach, i.e. split the words by the space character and then try to find if each word exists in the english dictionary.

This approach is more efficient since the candidate keys now are 125 rather than ~ 17K. 