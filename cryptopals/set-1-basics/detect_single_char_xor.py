from binascii import unhexlify
from itertools import takewhile
from pprint import pprint

from single_byte_xor_cipher import (
    get_possible_keys, 
    get_possible_plaintexts, 
    letter_frequency_rank,
    mostly_letters_rank,
    printable_characters_rank
)



if __name__ == "__main__":
    ciphertexts = []
    with open("4.txt", 'r') as ct_file:
        ciphertexts = ct_file.readlines()
    ciphertexts = [ct.strip() for ct in ciphertexts]

    all_plaintexts = []
    for ciphertext in ciphertexts:
        keys = get_possible_keys(ciphertext)
        plaintexts = get_possible_plaintexts(ciphertext, keys)
        filtered_plaintexts = mostly_letters_rank(plaintexts)
        filtered_plaintexts.sort(key=lambda tup: tup[1], reverse=True)
        
        # The 0.8 threshold can be played with here
        filter_threshold = 0.8
        filtered_plaintexts = takewhile(
            lambda tup: tup[1] > filter_threshold, filtered_plaintexts)

        # Flattening a list of (plaintext, rank) tuples to a list of plaintexts
        plaintexts = [pt_ranked[0] for pt_ranked in filtered_plaintexts]

        filtered_plaintexts = letter_frequency_rank(plaintexts)
        all_plaintexts.extend(filtered_plaintexts)

    all_plaintexts.sort(key=lambda tup: abs(1 - tup[1]), reverse=True)
    
    pprint(all_plaintexts)
