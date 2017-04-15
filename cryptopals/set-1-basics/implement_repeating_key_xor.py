from binascii import hexlify, unhexlify
from itertools import takewhile
from pprint import pprint

from xor import xor


def repeat_str_to_len(string, length):
    quotient, remainder = divmod(length, len(string))
    return string * quotient + string[:remainder]


if __name__ == "__main__":
    plaintext = (
"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""")

    plaintext_hex = hexlify(plaintext.encode())
    keylen = len(plaintext)
    key_hex = hexlify(repeat_str_to_len("ICE", keylen).encode())
    ciphertext = xor(plaintext_hex, key_hex)

    print(ciphertext)