from base64 import b64decode
from binascii import hexlify, unhexlify
from functools import reduce
from itertools import product, takewhile
from pprint import pprint

from xor import xor


def get_hamming_distance(hex_str1, hex_str2):
    xor_res = xor(hex_str1, hex_str2)
    xor_res = unhexlify(xor_res)

    hamming_distance = 0
    for byte in xor_res:
        bits = bin(byte)
        hamming_distance += bits.count("1")

    hamming_distance /= len(xor_res)

    return hamming_distance


def guess_keysize(ciphertext, bs_min=2, bs_max=101):
    ranked_keysizes = []
    for keysize in range(bs_min, bs_max):
        keysize_hex = keysize * 2          # 1 byte takes two hex chars
        fst_block = ciphertext[:keysize_hex]
        snd_block = ciphertext[keysize_hex:keysize_hex*2]
        trd_block = ciphertext[keysize_hex*2:keysize_hex*3]
        frt_block = ciphertext[keysize_hex*3:keysize_hex*4]
        hamming_distance_fst_snd = get_hamming_distance(fst_block, snd_block)
        hamming_distance_snd_trd = get_hamming_distance(snd_block, trd_block)
        hamming_distance_trd_frt = get_hamming_distance(trd_block, frt_block)
        avg_hamming_distance = ( (hamming_distance_fst_snd + hamming_distance_snd_trd +
            hamming_distance_trd_frt) / 3 )

        ranked_keysizes.append((keysize, avg_hamming_distance))

    ranked_keysizes.sort(key=lambda tup: tup[1])

    return ranked_keysizes


def break_ct_into_per_key_byte_groups(ciphertext, keysize):
    ciphertext = unhexlify(ciphertext)
    key_byte_groups = []
    for byte_num in range(keysize):
        key_byte_groups.append(hexlify(ciphertext[byte_num::keysize]))

    return key_byte_groups


def repeat_str_to_len(string, length):
    quotient, remainder = divmod(length, len(string))
    return string * quotient + string[:remainder]


def get_possible_keys(keystream_len):
    # Generate list of potential keys
    possible_keys = []
    for i in range(256):
        hex_num = hex(i).split('x')[1].zfill(2)
        possible_keys.append(hex_num * keystream_len)

    return possible_keys


def get_possible_plaintexts(ciphertext, keys):
    plaintexts = []
    for key in keys:
        plaintext = unhexlify(xor(ciphertext, key))
        plaintexts.append((key[:2], plaintext))

    return plaintexts


def is_letter(char_code):
    """Return True if char_code is a letter character code from the ASCII 
    table. Otherwise return False.
    """
    if isinstance(char_code, str) or isinstance(char_code, bytes):
        char_code = ord(char_code)

    if char_code >= 65 and char_code <= 90:  # uppercase letters
        return True

    if char_code >= 97 and char_code <= 122: # lowercase letters
        return True

    return False


def mostly_letters_rank(plaintexts, additional_allowed_chars=[" "]):
    """Return a list of (plaintext, rank) tuples where the higher the rank,
       the less non-letter characters are in the plaintext
    """
    ranked_plaintexts = []
    for key, plaintext in plaintexts:
        letter_count = 0
        for byte in plaintext:
            if is_letter(byte):
                letter_count +=1
            elif chr(byte) in additional_allowed_chars:
                letter_count += 1
        rank = letter_count / len(plaintext)
        ranked_plaintexts.append((key, plaintext, rank))

    ranked_plaintexts.sort(key=lambda tup: tup[2])

    return ranked_plaintexts


def printable_characters_rank(plaintexts):
    """Return a list of (plaintext, rank) tuples where the higher the rank,
       the less non-printable characters are in the plaintext
    """
    ranked_plaintexts = []
    for key, plaintext in plaintexts:
        printable_chars_count = 0
        for byte in plaintext:
            # Chars between 0x20 and 0x7E are printable ASCII chars
            if byte >= 32 and byte <= 126:
                printable_chars_count +=1 
        rank = printable_chars_count / len(plaintext)
        ranked_plaintexts.append((key, plaintext, rank))

    ranked_plaintexts.sort(key=lambda tup: tup[2])

    return ranked_plaintexts


def letter_frequency_rank(plaintexts, no_letters_rank=1000000):
    # English letter frequency table comes from here - https://www.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    default_letter_frequencies = {
        'e': 0.1202, 't': 0.0910, 'a': 0.0812, 'o': 0.0768, 'i': 0.0731, 
        'n': 0.0695, 's': 0.0628, 'r': 0.0602, 'h': 0.0592, 'd': 0.0432, 
        'l': 0.0398, 'u': 0.0288, 'c': 0.0271, 'm': 0.0261, 'f': 0.0230, 
        'y': 0.0211, 'w': 0.0209, 'g': 0.0203, 'p': 0.0182, 'b': 0.0149, 
        'v': 0.0111, 'k': 0.0069, 'x': 0.0017, 'q': 0.0011, 'j': 0.0010, 
        'z': 0.0007
    }

    ranked_plaintexts = []
    for key, plaintext in plaintexts:
        plaintext_letter_frequencies = {}
        for byte in plaintext:
            if not is_letter(byte):
                continue # skip further processing for this byte
            char = chr(byte).lower()
            if char in plaintext_letter_frequencies:
                plaintext_letter_frequencies[char] += 1
            else:
                plaintext_letter_frequencies[char] = 1

        # If there were no letters in the plaintext, then skip further processing
        if not plaintext_letter_frequencies:
            continue

        # Replace absolute occurence with relative distribution
        for letter in plaintext_letter_frequencies:
            plaintext_letter_frequencies[letter] = plaintext_letter_frequencies[letter] / len(plaintext_letter_frequencies)

        rank = 0
        for letter in default_letter_frequencies:
            default_letter_frequency = default_letter_frequencies[letter]
            if letter in plaintext_letter_frequencies:
                plaintext_letter_frequency = plaintext_letter_frequencies[letter]
            else:
                plaintext_letter_frequency = 0

            rank += abs(default_letter_frequency - plaintext_letter_frequency)

            # print("DEBUG: letter = {}".format(letter))
            # print("DEBUG: default_letter_frequency = {}".format(default_letter_frequency))
            # print("DEBUG: plaintext_letter_frequency = {}".format(plaintext_letter_frequency))
            # print("DEBUG: rank = {}".format(rank))

        ranked_plaintexts.append((key, plaintext, rank))

    # The closer the rank to number 1, the better
    ranked_plaintexts.sort(key=lambda tup: abs(1 - tup[2]))

    return ranked_plaintexts



if __name__ == "__main__":
    ciphertext = []
    with open("6.txt", 'r') as ct_file:
        ciphertext = ct_file.readlines()
    # Reduce multiple lines to a single string with \n chars removed
    ciphertext = reduce(lambda acc,item: acc+item.strip(), ciphertext, "")
    ciphertext = hexlify(b64decode(ciphertext))

    guessed_keysizes = guess_keysize(ciphertext)
    print("### KEY SIZE GUESSING ###\n")
    pprint(guessed_keysizes)


    KEYSIZE_GUESSES_COUNT = 5
    for keysize, _ in guessed_keysizes[:KEYSIZE_GUESSES_COUNT]:
    # keysize = guessed_keysizes[2][0]
        key_byte_groups = break_ct_into_per_key_byte_groups(ciphertext, keysize)

        print("\n\n### KEY BYTES GUESSING. KEYSIZE: {} ###\n".format(keysize))
        key_byte_num = 0
        for key_byte_group in key_byte_groups:
            print("\n= KEY BYTE #{} GUESSES =\n".format(key_byte_num))
            key_byte_num += 1
            possible_keys = get_possible_keys(len(key_byte_group)//2) # //2 because 1 byte = 2 hex chars
            plaintexts = get_possible_plaintexts(key_byte_group, possible_keys)
            filtered_plaintexts = mostly_letters_rank(plaintexts)
           
            # The 0.8 threshold can be played with here
            filter_threshold = 0.8
            filtered_plaintexts = filter(
                lambda tup: tup[2] > filter_threshold, filtered_plaintexts)

            # Transforming a list of (key, plaintext, rank) tuples to a list of 
            # (key, plaintext) tuples
            plaintexts = [(pt[0], pt[1]) for pt in filtered_plaintexts]

            filtered_plaintexts = letter_frequency_rank(plaintexts)
            for pt in filtered_plaintexts:
                print("{}".format(pt))


    # The key was recovered manually after staring at the output of the
    # above code
    print("\n\n### DECRYPTION ###\n")
    key = '5465726d696e61746f7220583a204272696e6720746865206e6f697365'
    print("# RECOVERED KEY\n\t= {}\n\t= {}\n".format(key, unhexlify(key)))

    print("# RECOVERED CIPHERTEXT\n")
    keystream = repeat_str_to_len(key, len(ciphertext))
    recovered_text = unhexlify(xor(keystream, ciphertext))
    print(recovered_text.decode("utf-8"))

