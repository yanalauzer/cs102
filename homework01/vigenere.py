def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    a = 0
    while len(plaintext) > len(keyword):
        keyword += keyword[a]
        a += 1
    for i, _ in enumerate(keyword):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65
            # 65-й элемент - A. А - сдвиг на 0.
            # Если keyword[i] - A, то 65 - 65 = 0, сдвиг на 0
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97
            # 97-й элемент - а.
        if plaintext[i].isalpha():
            c = ord(plaintext[i])
            if plaintext[i].isupper() and c >= 91 - key:
                ciphertext += chr(c - 26 + key)
            elif plaintext[i].islower() and c >= 123 - key:
                ciphertext += chr(c - 26 + key)
            else:
                ciphertext += chr(c + key)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    ab = 0
    while len(ciphertext) > len(keyword):
        keyword += keyword[ab]
        ab += 1
    for i, _ in enumerate(keyword):
        if keyword[i].isupper():
            key = ord(keyword[i]) - 65
        elif keyword[i].islower():
            key = ord(keyword[i]) - 97
        if ciphertext[i].isalpha():
            cb = ord(ciphertext[i])
            if ciphertext[i].isupper() and cb <= 64 + key:
                plaintext += chr(cb + 26 - key)
            elif ciphertext[i].islower() and cb <= 96 + key:
                plaintext += chr(cb + 26 - key)
            else:
                plaintext += chr(cb - key)
        else:
            plaintext += ciphertext[i]
    return plaintext