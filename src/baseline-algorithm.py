# given a text and key / password this function encrypts / decrypts by
# applying the XOR function
def encryption_algorithm(text, key):
    ascii_key = [ord(c) for c in key]
    ascii_text = [ord(c)for c in text]
    message = []
    for i in range(len(text)):
        key_index = i % len(key)
        xor =  ascii_text[i] ^ ascii_key[key_index]
        message.append(chr(xor))
    return ''.join(message)

text = 'I am a beautiful green tree.'
key = 'password'
encrypted_text = encryption_algorithm(text, key)
print('encrypted_text: ' + encrypted_text)
decrypted_text = encryption_algorithm(encrypted_text, key)
print('decrypted_text: ' + decrypted_text)