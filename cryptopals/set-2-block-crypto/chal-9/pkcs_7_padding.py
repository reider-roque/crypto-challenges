def pad(plaintext, block_size):

    if block_size < 2 or block_size > 255:
        raise ValueError("block_size cannot be less than 2 and greater than 255")

    last_block = plaintext[-block_size:]
    if len(last_block) == block_size:
        pad_byte = bytes([block_size])
        plaintext += block_size * pad_byte
    elif len(last_block) < block_size:
        pad_byte = bytes([block_size - len(last_block)])
        plaintext += (block_size - len(last_block)) * pad_byte
    else:
        raise RuntimeError("Something's weird happen. There is probably an error in the algorithm")

    return plaintext


if __name__ == "__main__":
    plaintext = b"YELLOW SUBMARINE"
    padded_plaintext = pad(plaintext, 20)

    print(padded_plaintext)