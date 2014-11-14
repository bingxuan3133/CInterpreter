import unittest
from Parser import *
from ContextManager import *
from Context import *
from ExpressionContext import *

class TestParseInfix(unittest.TestCase):
    def test_parse_2_plus_3(self):
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 + 3', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 + 3 * 4', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 * 3 + 4', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('+', 70)
        expressionContext.addInfixOperator('-', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 * 3 + 4 - 5', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 * 3 + 4 * 5', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 + 3 * 4 + 5', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('i + j', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('(identifier)', token.data[0].id)
        self.assertEqual('(identifier)', token.data[1].id)
        self.assertEqual('i', token.data[0].data[0])
        self.assertEqual('j', token.data[1].data[0])

class TestParsePrefix(unittest.TestCase):
    def test_parse_negative_2_plus_3(self):
        """
                +
              /  \
            -     3
          /
        2
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addPrefixOperator('-', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('- 2 + 3', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addPrefixOperator('-', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('- 2 + - 3', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addPrefixInfixOperator('-', 70)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('- 2 - - 3', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('-', 70)
        expressionContext.addPrefixOperator('!', 120)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('! 2 - ! 3', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('!', token.data[0].id)
        self.assertEqual('!', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])

    def test_parse_post_increment_i(self):
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addPostfixOperator('++', 150)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('i ++', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('++', token.id)
        self.assertEqual('(identifier)', token.data[0].id)
        self.assertEqual('i', token.data[0].data[0])
        self.assertEqual(1, len(token.data))

    def test_parse_post_increment_i_plus_pre_decrement_j(self):
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addPostfixOperator('++', 150)
        expressionContext.addPrefixOperator('--', 120)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('i ++ + -- j', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('+', token.id)
        self.assertEqual('++', token.data[0].id)
        self.assertEqual('--', token.data[1].id)
        self.assertEqual('(identifier)', token.data[0].data[0].id)
        self.assertEqual('(identifier)', token.data[1].data[0].id)
        self.assertEqual('i', token.data[0].data[0].data[0])
        self.assertEqual('j', token.data[1].data[0].data[0])

class TestParsePrefixGroup(unittest.TestCase):
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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addInfixOperator('*', 100)
        expressionContext.addGroupOperator('(', 0)
        expressionContext.addGroupOperator(')', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('( 2 + 3 ) * 4', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addInfixOperator('*', 100)
        expressionContext.addGroupOperator('(', 0)
        expressionContext.addGroupOperator(')', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('2 * ( 3 + 4 )', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addInfixOperator('+', 70)
        expressionContext.addPrefixInfixOperator('-', 70)
        expressionContext.addGroupOperator('(', 0)
        expressionContext.addGroupOperator(')', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('- ( 3 + 4 )', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

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
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addGroupOperator('(', 0)
        expressionContext.addGroupOperator(')', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('( )', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)


    def test_parse_will_identify_the_braces(self):
        """
            {
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual([], token.data)

    def test_parse_will_identify_the_braces_inside_the_brace(self):
        """
            {
            |
            {
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ { } } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual('{', token.data[0].id)


    def test_parse_will_identify_the_semicolon_in_the_braces(self):
        """
            {
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ ; } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)

    def test_parse_will_point_to_the_next_location_after_finished_parse(self):
        """
            {
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ ; } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual('(end)', parser.lexer.peep().data[0])

    def test_parse_will_build_an_ast_for_expression_in_the_brace(self):
        """
            {
            |
            +
          /   \
         2     3
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addInfixOperator('+',70)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ 2 + 3 ; } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])

    def test_parse_will_build_an_ast_for_expressions_in_the_brace(self):
        """
                {           -   /
            /       \        /     \
            +       *       5       9
          /   \    /    \
         2     3  3     4
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addInfixOperator('+',70)
        expressionContext.addInfixOperator('*',100)
        expressionContext.addInfixOperator('/',100)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ 2 + 3 ; \
                        3 * 4 ; \
                        5 / 9 ; \
                        } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)

        self.assertEqual('{', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual('*', token.data[1].id)
        self.assertEqual(3, token.data[1].data[0].data[0])
        self.assertEqual(4, token.data[1].data[1].data[0])
        self.assertEqual('/', token.data[2].id)
        self.assertEqual(5, token.data[2].data[0].data[0])
        self.assertEqual(9, token.data[2].data[1].data[0])

    def test_parse_will_build_an_AST_for_longer_expression_in_the_brace(self):
        """
            {
            |
            +
          /   \
         2     /
             /  \
            *   9
          /  \
         3    8
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addInfixOperator('+',70)
        expressionContext.addInfixOperator('*',100)
        expressionContext.addInfixOperator('/',100)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ 2 + 3 * 8 / 9 ; } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        token = parser.parse(0)

        self.assertEqual('{', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual('/', token.data[0].data[1].id)
        self.assertEqual('*', token.data[0].data[1].data[0].id)
        self.assertEqual(3, token.data[0].data[1].data[0].data[0].data[0])
        self.assertEqual(8, token.data[0].data[1].data[0].data[1].data[0])
        self.assertEqual(9, token.data[0].data[1].data[1].data[0])


    def test_parse_throw_an_error_when_the_semicolon_is_missing(self):
        """
            {
            |
            +
          /   \
         2     3
        :return:
        """
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        expressionContext.addBlockOperator('{', 0)
        expressionContext.addInfixOperator('+',70)
        expressionContext.addOperator(';')
        expressionContext.addBlockOperator('}', 0)

        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('{ 2 + 3 } ', context)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)
        self.assertRaises(SyntaxError, parser.parse, 0)
if __name__ == '__main__':
    unittest.main()