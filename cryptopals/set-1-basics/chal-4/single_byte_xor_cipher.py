from binascii import unhexlify
from pprint import pprint

from xor import xor


def get_possible_keys(ciphertext):
    key_len = len(ciphertext) // 2
    # Generate list of potential keys
    possible_keys = []
    for i in range(256):
        hex_num = hex(i).split('x')[1].zfill(2)
        possible_keys.append(hex_num * key_len)

    return possible_keys


def get_possible_plaintexts(ciphertext, keys):
    plaintexts = []
    for key in keys:
        plaintext = unhexlify(xor(ciphertext, key))
        plaintexts.append(plaintext)

    return plaintexts


def printable_characters_rank(plaintexts):
    """Return a list of (plaintext, rank) tuples where the higher the rank,
       the less non-printable characters are in the plaintext
    """
    ranked_plaintexts = []
    for plaintext in plaintexts:
        printable_chars_count = 0
        for byte in plaintext:
            # Chars between 0x20 and 0x7E are printable ASCII chars
            if byte >= 32 and byte <= 126:
                printable_chars_count +=1 
        rank = printable_chars_count / len(plaintext)
        ranked_plaintexts.append((plaintext, rank))

    ranked_plaintexts.sort(key=lambda tup: tup[1])

    return ranked_plaintexts


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
    for plaintext in plaintexts:
        letter_count = 0
        for byte in plaintext:
            if is_letter(byte):
                letter_count +=1
            elif chr(byte) in additional_allowed_chars:
                letter_count += 1
        rank = letter_count / len(plaintext)
        ranked_plaintexts.append((plaintext, rank))

    ranked_plaintexts.sort(key=lambda tup: tup[1])

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
    for plaintext in plaintexts:
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
        for key in plaintext_letter_frequencies:
            plaintext_letter_frequencies[key] = plaintext_letter_frequencies[key] / len(plaintext_letter_frequencies)

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

        ranked_plaintexts.append((plaintext, rank))

    # The closer the rank to number 1, the better
    ranked_plaintexts.sort(key=lambda tup: abs(1 - tup[1]), reverse=True)

    return ranked_plaintexts


if __name__ == "__main__":
    ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

    keys = get_possible_keys(ciphertext)
    plaintexts = get_possible_plaintexts(ciphertext, keys)

    # printable_characters_ranked_plaintexts = mostly_letters_rank(plaintexts)
    # pprint(printable_characters_ranked_plaintexts)

    letter_frequency_ranked_plaintexts = letter_frequency_rank(plaintexts)
    pprint(letter_frequency_ranked_plaintexts)