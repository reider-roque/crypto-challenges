import unittest
from base64 import b64encode
from single_byte_xor_cipher import letter_frequency_rank

# Run tests with python -m unittest file.py
class SingleByteXorCipherTests(unittest.TestCase):

    def test_LetterFrequencyRankedPlaintexts_NonPrintableCharacterString_RanksAs100(self):
        test = b'\xe8\xc4\xc4\xc0\xc2\xc5\xcc\x8b\xe6\xe8\x8c\xd8\x8b\xc7\xc2\xc0\xce\x8b\xca\x8b\xdb\xc4\xde\xc5\xcf\x8b\xc4\xcd\x8b\xc9\xca\xc8\xc4\xc5'
        letter_frequency_ranked_plaintexts = letter_frequency_rank([test])
        self.assertEqual(letter_frequency_ranked_plaintexts[0][1], 100)