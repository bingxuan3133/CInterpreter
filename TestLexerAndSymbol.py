import unittest
from Lexer import *
from Context import *

class TestLexerAndSymbol(unittest.TestCase):
    def testLexertAndSymbolGetIdentifierAndLiteral(self):
        context = Context()
        lexer = Lexer('xyz 1234', [context])
        token = lexer.peep()
        self.assertEqual(token.id, '(identifier)')
        self.assertEqual(token.data[0], 'xyz')
        token = lexer.advance()
        self.assertEqual(token.id, '(literal)')
        self.assertEqual(token.data[0], 1234)

    def testGetInfixAddAndSubOperatorTokens(self):
        context = Context()
        context.addInfixOperator('+', 70)
        context.addInfixOperator('-', 70)
        lexer = Lexer('+ -', [context])
        token = lexer.peep()
        self.assertEqual(token.id, '+')
        self.assertEqual(token.arity, Context.BINARY)
        token = lexer.advance()
        self.assertEqual(token.id, '-')
        self.assertEqual(token.arity, Context.BINARY)

if __name__ == '__main__':
    unittest.main()