import unittest
from base64 import b64encode
from binascii import unhexlify
from break_repeating_key_xor import get_hamming_distance

# Run tests with python -m unittest file.py
class HexToBase64Tests(unittest.TestCase):

    def test_GetHammingDistance_CryptoPalsControlTest(self):
        str1 = "this is a test"
        str2 = "wokka wokka!!!"
        expected_result = 37
        self.assertEqual(expected_result, get_hamming_distance(str1, str2))