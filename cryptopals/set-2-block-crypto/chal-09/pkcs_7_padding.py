def pad(plaintext, block_size):

    if block_size < 2 or block_size > 255:
        raise ValueError("block_size cannot be less than 2 and greater than 255")

    last_block_size = len(plaintext) % block_size
    pad_size = block_size - last_block_size
    if pad_size == 0:
        pad_size = 16
    pad_byte = bytes([pad_size])
    
    plaintext += pad_size * pad_byte

    return plaintext


if __name__ == "__main__":
    plaintext = b"YELLOW SUBMARINE"
    padded_plaintext = pad(plaintext, 20)

    print(padded_plaintext)