def encrypt(plaintext: str, enc_key: list) -> str:
    ciphertext = [None] * len(plaintext)
    for i in range(len(plaintext)):
        ciphertext[i] = plaintext[enc_key[i]]
    return ''.join(ciphertext)

def decrypt(ciphertext: str, enc_key: list) -> str:
    plaintext = [None] * len(ciphertext)
    for i in range(len(ciphertext)):
        plaintext[enc_key[i]] = ciphertext[i]
    return ''.join(plaintext)


if  __name__ == "__main__":
    text = input()
    enc_key = [i for i in range(2, len(text), 3)] + [i for i in range(0, len(text), 3)] + [i for i in range(1, len(text), 3)]
    # print(encrypt(text, enc_key))
    print(decrypt(text, enc_key))