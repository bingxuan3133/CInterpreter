import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Parser import *
from ContextManager import *
from Context import *
from ExpressionContext import *

class TestParseInfix(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext]
        self.expressionContext.addInfixOperator('+', 70)
        self.expressionContext.addInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_2_plus_3(self):
        lexer = LexerStateMachine('2 + 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual(3, token.data[1].data[0])

    def test_parse_2_plus_3_multiply_4(self):
        """
            +
          /   \
        2      *
             /   \
            3     4
        :return:
        """
        lexer = LexerStateMachine('2 + 3 * 4', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual('*', token.data[1].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[1].id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])
        self.assertEqual(4, token.data[1].data[1].data[0])

    def test_parse_2_multiply_3_plus_4(self):
        """
               +
             /   \
            *     4
          /   \
        2      3
        :return:
        """
        lexer = LexerStateMachine('2 * 3 + 4', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('*', token.data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual(4, token.data[1].data[0])

    def test_parse_2_multiply_3_plus_4_minus_5(self):
        """
                  -
                /   \
               +     5
             /   \
            *     4
          /   \
        2      3
        :return:
        """
        lexer = LexerStateMachine('2 * 3 + 4 - 5', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('-', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual('*', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[1].id)
        self.assertEqual('(literal)', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual(4, token.data[0].data[1].data[0])
        self.assertEqual(5, token.data[1].data[0])

    def test_parse_2_multiply_3_plus_4_multiply_5(self):
        """
               +
            /     \
           *       *
         /  \    /  \
        2    3  4    5
        :return:
        """
        lexer = LexerStateMachine('2 * 3 + 4 * 5', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('*', token.data[0].id)
        self.assertEqual('*', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual(4, token.data[1].data[0].data[0])
        self.assertEqual(5, token.data[1].data[1].data[0])

    def test_parse_2_plus_3_multiply_4_plus_5(self):
        """
                +
              /   \
             +     5
           /  \
          2    *
             /  \
            3    4
        :return:
        """
        lexer = LexerStateMachine('2 + 3 * 4 + 5', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual('*', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0].data[0])
        self.assertEqual(4, token.data[0].data[1].data[1].data[0])
        self.assertEqual(5, token.data[1].data[0])

    def test_parse_i_plus_j(self):
        """
          +
        /   \
        i   j
        :return:
        """
        lexer = LexerStateMachine('i + j', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('(identifier)', token.data[0].id)
        self.assertEqual('(identifier)', token.data[1].id)
        self.assertEqual('i', token.data[0].data[0])
        self.assertEqual('j', token.data[1].data[0])

class TestParsePrefix(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext]
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addPrefixOperator('!', 120)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_negative_2_plus_3(self):
        """
                +
              /  \
            -     3
          /
        2
        :return:
        """
        lexer = LexerStateMachine('- 2 + 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0])

    def test_parse_negative_2_plus_negative_3(self):
        """
            +
         /     \
        -       -
        |       |
        2       3
        :return:
        """
        lexer = LexerStateMachine('- 2 + - 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual('-', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])

    def test_parse_negative_2_minus_negative_3(self):
        """
            -
         /     \
        -       -
        |       |
        2       3
        :return:
        """
        lexer = LexerStateMachine('- 2 - - 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('-', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual('-', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])

    def test_parse_not_2_minus_not_3(self):
        """
            -
         /     \
        !       !
        |       |
        2       3
        :return:
        """
        lexer = LexerStateMachine('! 2 - ! 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('!', token.data[0].id)
        self.assertEqual('!', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])

class TestParsePostfix(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext]
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addPrefixOperator('++', 120)
        self.expressionContext.addPrefixOperator('--', 120)
        self.expressionContext.addPostfixOperator('++', 150)
        self.expressionContext.addPostfixOperator('--', 150)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_post_increment_i(self):
        """
        ++
        |
        i
        :return:
        """
        lexer = LexerStateMachine('i ++', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('++', token.id)
        self.assertEqual('(identifier)', token.data[0].id)
        self.assertEqual('i', token.data[0].data[0])
        self.assertEqual(1, len(token.data))

    def test_parse_post_increment_i_plus_pre_decrement_j(self):
        lexer = LexerStateMachine('i ++ + -- j', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('++', token.data[0].id)
        self.assertEqual('--', token.data[1].id)
        self.assertEqual('(identifier)', token.data[0].data[0].id)
        self.assertEqual('(identifier)', token.data[1].data[0].id)
        self.assertEqual('i', token.data[0].data[0].data[0])
        self.assertEqual('j', token.data[1].data[0].data[0])

class TestParsePrefixGroup(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext]
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addInfixOperator('*', 100)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addGroupOperator(')', 0)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_bracket_2_plus_3_mul_4(self):
        """
                *
             /     \
            (       4
            |
            +
          /   \
        2      3
        :return:
        """

        lexer = LexerStateMachine('( 2 + 3 ) * 4', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('*', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('+', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual(4, token.data[1].data[0])

    def test_parse_2_mul_bracket_3_plus_4(self):
        """
            *
         /     \
        2       (
                |
                +
              /   \
            3      4
        :return:
        """
        lexer = LexerStateMachine('2 * ( 3 + 4 )', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('*', token.id)
        self.assertEqual('(', token.data[1].id)
        self.assertEqual('+', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].data[1].id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0].data[0])
        self.assertEqual(4, token.data[1].data[0].data[1].data[0])

    def test_parse_neg_bracket_3_plus_4_(self):
        """
            -
            |
            (
            |
            +
          /   \
        3      4
        :return:
        """
        lexer = LexerStateMachine('- ( 3 + 4 )', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('-', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('+', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[1].id)
        self.assertEqual(3, token.data[0].data[0].data[0].data[0])
        self.assertEqual(4, token.data[0].data[0].data[1].data[0])

    def test_parse_an_empty_bracket_should_raise_an_error(self):
        """
            (
        :return:
        """
        lexer = LexerStateMachine('( )', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)

if __name__ == '__main__':
    unittest.main()