import unittest
from aes import AES

class TestBlock(unittest.TestCase):
    """
    Tests raw AES-128 block operations.
    """
    def setUp(self):
        self.aes = AES(b'\00' * 16)

    def test_success(self):
        """ Should be able to encrypt and decrypt block messages. """
        message = b'\01' * 16
        ciphertext = self.aes.encrypt_block(message)
        self.assertEqual(self.aes.decrypt_block(ciphertext), message)

        message = b'a secret message'
        ciphertext = self.aes.encrypt_block(message)
        self.assertEqual(self.aes.decrypt_block(ciphertext), message)

    def test_bad_key(self):
        """ Raw AES requires keys of an exact size. """
        with self.assertRaises(AssertionError):
            AES(b'short key')

        with self.assertRaises(AssertionError):
            AES(b'long key' * 10)

    def test_expected_value_128(self):
        """
        Tests taken from the NIST document, Appendix B:
        http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        """
        message = b'\x32\x43\xF6\xA8\x88\x5A\x30\x8D\x31\x31\x98\xA2\xE0\x37\x07\x34'
        key     = b'\x2B\x7E\x15\x16\x28\xAE\xD2\xA6\xAB\xF7\x15\x88\x09\xCF\x4F\x3C'
        ciphertext = AES(bytes(key)).encrypt_block(bytes(message))
        self.assertEqual(ciphertext, b'\x39\x25\x84\x1D\x02\xDC\x09\xFB\xDC\x11\x85\x97\x19\x6A\x0B\x32')
    
    def test_expected_value_printing(self):
        
        #Tests taken from the NIST document, Appendix B:
        #http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        
        message = b'\x43\x6f\x72\x72\x65\x63\x74\x20\x44\x65\x63\x72\x79\x70\x74\x21'
        key     = b'\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F'
        ciphertext = AES(bytes(key)).encrypt_block_with_printing(bytes(message))
        self.assertEqual(ciphertext,  b'\xF4\x35\x15\x03\xAA\x78\x1C\x52\x02\x67\xD6\x90\xC4\x2D\x1F\x43')    
    def test_decrypt_value_printing(self):
        
        #Tests taken from the NIST document, Appendix B:
        #http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        
        key        = b'\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F'
        ciphertext = b'\xF4\x35\x15\x03\xAA\x78\x1C\x52\x02\x67\xD6\x90\xC4\x2D\x1F\x43'
        message = AES(bytes(key)).decrypt_block_with_printing(bytes(ciphertext))
        self.assertEqual(message, b'\x43\x6f\x72\x72\x65\x63\x74\x20\x44\x65\x63\x72\x79\x70\x74\x21')
        
    
    def test_expected_value2_printing(self):
        """
        Tests taken from the NIST document, Appendix B:
        http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        """
        message = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'
        key     = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        ciphertext = AES(bytes(key)).encrypt_block(bytes(message))
        self.assertEqual(ciphertext,  b'\x69\xc4\xe0\xd8\x6a\x7b\x04\x30\xd8\xcd\xb7\x80\x70\xb4\xc5\x5a')    
    def test_decrypt_value2_printing(self):
        """
        Tests taken from the NIST document, Appendix B:
        http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
        """
        key        = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        ciphertext = b'\x69\xc4\xe0\xd8\x6a\x7b\x04\x30\xd8\xcd\xb7\x80\x70\xb4\xc5\x5a'
        message = AES(bytes(key)).decrypt_block(bytes(ciphertext))
        self.assertEqual(message, b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff')

class TestKeySizes(unittest.TestCase):
    """
    Tests encrypt and decryption using 192- and 256-bit keys.
    """
    def test_192(self):
        aes = AES(b'P' * 24)
        message = b'M' * 16
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_256(self):
        aes = AES(b'P' * 32)
        message = b'M' * 16
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_expected_values192(self):
        message = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
        aes = AES(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17')
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(ciphertext, b'\xdd\xa9\x7c\xa4\x86\x4c\xdf\xe0\x6e\xaf\x70\xa0\xec\x0d\x71\x91')
        self.assertEqual(aes.decrypt_block(ciphertext), message)

    def test_expected_values256(self):
        message = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF'
        aes = AES(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f')
        ciphertext = aes.encrypt_block(message)
        self.assertEqual(ciphertext, b'\x8e\xa2\xb7\xca\x51\x67\x45\xbf\xea\xfc\x49\x90\x4b\x49\x60\x89')
        self.assertEqual(aes.decrypt_block(ciphertext), message)

def run():
    unittest.main()

if __name__ == '__main__':
    run()
