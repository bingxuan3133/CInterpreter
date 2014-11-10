
import unittest
from Lexer import *
from Context import *

class TestLexer(unittest.TestCase):

    def testLexerShouldSplitTo2StatementsAndSplitEachToWords(self):
        context = Context()
        lex = Lexer(""" hello world
                        1234 9 yx abc """, [context])
        self.assertEqual(lex.lists[0], ["hello", "world"])
        self.assertEqual(lex.lists[1], ["1234", "9", "yx", "abc"])

    def test_Advance_Will_return_the_next_value(self):
        context = Context()
        lexer = Lexer(""" hi krizz
                          987 456 """, [context])
        self.assertEqual(lexer.advance().data[0], 'krizz')
        self.assertEqual(lexer.advance().data[0], 987)
        self.assertEqual(lexer.advance().data[0], 456)
        self.assertEqual(lexer.peep().data[0], 456)

    def test_Advance_will_throw_an_error_when_the_symbol_read_is_not_same_as_the_expectedSymbol(self):
        context = Context()
        lexer = Lexer(""" int a ; """, [context])
        try:
            lexer.advance("a")
            print("The program failed because the exception does not throw.")
        except SyntaxError as e:
            self.assertEqual('Expected a but is (identifier)',e.args[0])

if __name__ == '__main__':
    unittest.main()
