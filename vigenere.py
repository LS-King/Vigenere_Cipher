from itertools import cycle


def encrypt(message, key):
    tmp_text = ''
    tmp_key = key.upper()
    alpha_pool = cycle(tmp_key)
    for ch in message:
        if not ch.isalpha():
            tmp_text += ch
        else:
            if ch.isupper():
                a = 'A'
            else:
                a = 'a'
            tmp_text += chr(ord(a)+((ord(ch)-ord(a)) + (ord(next(alpha_pool))-ord('A'))) % 26)
    return tmp_text


def decrypt(message, key):
    tmp_text = ''
    tmp_key = key.upper()
    alpha_pool = cycle(tmp_key)
    for ch in message:
        if not ch.isalpha():
            tmp_text += ch
        else:
            if ch.isupper():
                a = 'A'
            else:
                a = 'a'
            tmp_text += chr(ord(a)+((ord(ch)-ord(a)) - (ord(next(alpha_pool))-ord('A'))) % 26)
    return tmp_text


def main():
    message = 'Common sense is not so common.'
    key = 'PIZZA'

    print("加密前的文本是:", message)

    cipher_text = encrypt(message, key)
    print("加密后的文本是:", cipher_text)

    decrypted_text = decrypt(cipher_text, key)
    print("解密后的文本是:", decrypted_text)


if __name__ == '__main__':
    main()
