def encrypt(message, key):
    tmp_text = ''
    keylen = len(key)
    tmp_key = key.upper()
    i = 0
    for c in message:
        if not c.isalpha():
            tmp_text += c
        else:
            if c.isupper(): a = 'A'
            else: a = 'a'
            tmp_text += chr(ord(a)+((ord(c)-ord(a)) + (ord(tmp_key[i])-ord('A')))% 26)
            i += 1
            if i == keylen: i = 0
    return tmp_text

def decrypt(message, key):
    tmp_text = ''
    keylen = len(key)
    tmp_key = key.upper()
    i = 0
    for c in message:
        if not c.isalpha():
            tmp_text += c
        else:
            if c.isupper(): a = 'A'
            else: a = 'a'
            tmp_text += chr(ord(a)+((ord(c)-ord(a)) - (ord(tmp_key[i])-ord('A')))% 26)
            i += 1
            if i == keylen: i = 0
    return tmp_text

def main():
    message = 'Among the annoying challenges facing the middle class is one that will probably go unmentioned in the next presidential campaign: What happens when the robots come for their jobs? Donot dismiss that possibility entirely. About half of U.S. jobs are at high risk of being automated, according to a University of Oxford study, with the middle class disproportionately squeezed. Lower-income jobs like gardening or day care donot appeal to robots. But many middle-class occupations-trucking, financial advice, software engineering — have aroused their interest, or soon will. The rich own the robots, so they will be fine.'
    key = 'Examination'

    cipher_text = encrypt(message, key)
    decrypted_text = decrypt(cipher_text, key)

    print("加密前的文本是:", message)
    print("加密后的文本是:", cipher_text)
    print("解密后的文本是:", decrypted_text)

if __name__ == '__main__':
    main()