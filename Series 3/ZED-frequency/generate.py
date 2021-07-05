from string import ascii_uppercase
from random import shuffle

def generate():
    frequency = list(map(int, list("01234567890123456789012345")))
    alphabet = list(ascii_uppercase)
    key = list(''.join([alphabet[i] * frequency [i] for i in range(len(alphabet))]))
    shuffle(key)
    return ''.join(key)

if __name__ == '__main__':
   key = generate()
   with open('key.txt', 'w+') as fout:
       fout.write(key)
       fout.flush()
