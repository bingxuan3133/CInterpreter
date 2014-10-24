import unittest
from Tokenizer import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        tokenizer = Tokenizer('a 123 b c')
        t = tokenizer.advance()
        print(t.id)
        t = tokenizer.advance()
        print(t.id)
        t = tokenizer.advance()
        print(t.id)
        self.assertEqual(False, False)

if __name__ == '__main__':
    unittest.main