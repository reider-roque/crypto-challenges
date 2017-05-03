import unittest
from base64 import b64encode
from binascii import unhexlify
from hextobase64 import hextobase64

# Run tests with python -m unittest file.py
class HexToBase64Tests(unittest.TestCase):

    def test_HexToBase64_HexInUppercase_Succeeds(self):
        test_input = "0xAB12CD"
        expected_result = b64encode(unhexlify(b"ab12cd")).decode("utf-8")
        self.assertEqual(expected_result, hextobase64(test_input))

    def test_HexToBase64_HexStartsWith0x_Succeeds(self):
        test_input = "0xab12cd"
        expected_result = b64encode(unhexlify(b"ab12cd")).decode("utf-8")
        self.assertEqual(expected_result, hextobase64(test_input))

    def test_HexToBase64_HexStartsWithout0x_Succeeds(self):
        test_input = "ab12cd"
        expected_result = b64encode(unhexlify(b"ab12cd")).decode("utf-8")
        self.assertEqual(expected_result, hextobase64(test_input))

    def test_HexToBase64_HexContainsNonHexChars_ExceptionThrown(self):
        test_input = "ab12cdk!"
        with self.assertRaises(ValueError):
            hextobase64(test_input)

    def test_HexToBase64_HexStrOddLength_ExceptionThrown(self):
        test_input = "ab12cd4"
        with self.assertRaises(ValueError):
            hextobase64(test_input)

    def test_HexToBase64_CryptoPalsControlTest_Succeeds(self):
        test_input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        expected_result = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        self.assertEqual(expected_result, hextobase64(test_input))