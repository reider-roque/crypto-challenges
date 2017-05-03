import binascii
from base64 import b64encode
from binascii import unhexlify, hexlify


def xor(str1, str2):
    if len(str1) % 2 != 0:
        raise ValueError("str1 is of odd length.")
    if len(str2) % 2 != 0:
        raise ValueError("str2 is of odd length.")
    if len(str1) != len(str2):
        raise ValueError("Arguments str1 and str2 lenghts differ.")

    int1 = int(str1, 16)
    int2 = int(str2, 16)
    xor_result = hex(int1 ^ int2).split('x')[1]

    # adjust string length
    xor_result = xor_result.zfill(len(str1))

    
    return xor_result


# def xor2(str1, str2):
#     if len(str1) % 2 != 0:
#         raise ValueError("str1 is of odd length.")
#     if len(str2) % 2 != 0:
#         raise ValueError("str2 is of odd length.")
#     if len(str1) != len(str2):
#         raise ValueError("Arguments str1 and str2 lenghts differ.")

#     try:
#         bytestr1 = binascii.unhexlify(str1)
#     except binascii.Error as ex:   # Repacking into ValueError exception
#         raise ValueError("{} in str1".format(ex.args[0]))

#     try:
#         bytestr2 = binascii.unhexlify(str2)
#     except binascii.Error as ex:   # Repacking into ValueError exception
#         raise ValueError("{} in str2".format(ex.args[0]))

#     xored_str = ""
#     for byte1, byte2 in zip(bytestr1, bytestr2):
#         xored_str += chr(byte1 ^ byte2)

#     return hexlify(xored_str.encode())




# test_str1 = "1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c1c0111001f010100061a024b53535009181c"
# test_str2 = "686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965686974207468652062756c6c277320657965"



# def xor_speed_test():
#     b = ""
#     for i in range (1):
#         b = xor(test_str1, test_str2)


# if __name__ == "__main__":
#     # test_str1 = "1c0111001f010100061a024b53535009181c"
#     # test_str2 = "686974207468652062756c6c277320657965"
#     # expected_result = "746865206b696420646f6e277420706c6179"
#     # print("expected_result = {}".format(expected_result))
#     # print("xor1 result = {}".format(xor(test_str1, test_str2)))
#     # print("xor2 result = {}".format(xor2(test_str1, test_str2)))

#     import timeit
#     xor_speed_test()
#     print(timeit.timeit("xor(test_str1, test_str2)", setup="from __main__ import xor, test_str1, test_str2"))
#     print(timeit.timeit("xor2(test_str1, test_str2)", setup="from __main__ import xor2, test_str1, test_str2"))