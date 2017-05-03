def get_ciphertexts():
    ciphertexts = []
    with open("8.txt", 'r') as ct_file:
        ciphertexts = ct_file.readlines()
    # Reduce multiple lines to a single string with \n chars removed
    ciphertexts = [ct.strip() for ct in ciphertexts]
    
    return ciphertexts


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


if __name__ == "__main__":

    ciphertexts = get_ciphertexts()

    unique_blocks_per_ct = []
    for ciphertext in ciphertexts:
        ct_blocks = list(split_by_n(ciphertext, 32)) # 16 bytes
        unique_blocks = len(set(ct_blocks))
        unique_blocks_per_ct.append((unique_blocks, ciphertext))

    unique_blocks_per_ct.sort(key=lambda tup: tup[0], reverse=True)

    print(unique_blocks_per_ct)
    print("\nThe last ^ ciphertext(s) is our candidate.")


