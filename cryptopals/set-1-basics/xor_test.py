import unittest
from base64 import b64encode
from binascii import unhexlify
from xor import xor

# Run tests with python -m unittest file.py
class XorTests(unittest.TestCase):

    def test_Xor_Str1OddLength_Succeeds(self):
        test_str1 = "11111"
        test_str2 = "2222"
        with self.assertRaises(ValueError):
            xor(test_str1, test_str2)


    def test_Xor_Str1andStr2DifferentLength_Succeeds(self):
        test_str1 = "1111"
        test_str2 = "222222"
        with self.assertRaises(ValueError):
            xor(test_str1, test_str2)


    def test_Xor_MSBResultIsZero_ResultLengthSameAsInput(self):
        test_str1 = "1f1f"
        test_str2 = "1b37"
        # 0x1f1f ^ 0x1b37 = 0x0428 = 0x0428
        self.assertEqual(xor(test_str1, test_str2), '0428')


    def test_Xor_CryptoPalsControlTest_Succeeds(self):
        test_str1 = "1c0111001f010100061a024b53535009181c"
        test_str2 = "686974207468652062756c6c277320657965"
        expected_result = "746865206b696420646f6e277420706c6179"
        self.assertEqual(expected_result, xor(test_str1, test_str2))