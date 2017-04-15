import binascii
from base64 import b64encode

def hextobase64(hex_str):
    if hex_str.startswith("0x"):
        hex_str = hex_str.split('x')[1]
   
    try:
        ascii_str = binascii.unhexlify(hex_str)
    except binascii.Error as ex:   # Repacking into ValueError exception
        raise ValueError(*ex.args)

    return b64encode(ascii_str).decode("utf-8")