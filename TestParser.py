import unittest
from Parser import *


class TestInfix(unittest.TestCase):
    def test_parse_2_plus_3(self):
        context = Context()
        context.addInfixOperator('+', 70)
        parser = Parser('2 + 3', [context])
        context.setParser(parser)
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
        context = Context()
        context.addInfixOperator('+', 70)
        context.addInfixOperator('*', 100)

        parser = Parser('2 + 3 * 4', [context])
        context.setParser(parser)
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
        context = Context()
        context.addInfixOperator('*', 100)
        context.addInfixOperator('+', 70)
        parser = Parser('2 * 3 + 4', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('*', token.data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual(4, token.data[1].data[0])

    def test_parse_2_multiply_3_plus_4_will_point_to_the_end_after_finished(self):
        """
               +
             /   \
            *     4
          /   \
        2      3
        :return:
        """
        context = Context()
        context.addInfixOperator('*', 100)
        context.addInfixOperator('+', 70)
        parser = Parser('2 * 3 + 4', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('*', token.data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[1].id)
        self.assertEqual('(literal)', token.data[1].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual(4, token.data[1].data[0])
        self.assertEqual('(end)', parser.lexer.peep().data[0])

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
        context = Context()
        context.addInfixOperator('*', 100)
        context.addInfixOperator('+', 70)
        context.addInfixOperator('-', 70)
        parser = Parser('2 * 3 + 4 - 5', [context])
        context.setParser(parser)
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
        context = Context()
        context.addInfixOperator('*', 100)
        context.addInfixOperator('+', 70)

        parser = Parser('2 * 3 + 4 * 5', [context])
        context.setParser(parser)
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
        context = Context()
        context.addInfixOperator('*', 100)
        context.addInfixOperator('+', 70)

        parser = Parser('2 + 3 * 4 + 5', [context])
        context.setParser(parser)
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


class TestPrefix(unittest.TestCase):
    def test_parse_negation_2_plus_3(self):
        """
                +
              /   \
             !     3
           /
          2
        :return:
        """
        context = Context()
        context.addPrefixOperator('!', 120)
        context.addInfixOperator('+', 70)

        parser = Parser('! 2 + 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('!', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0])

    def test_parse_negative_2_plus_3(self):
        """
                +
              /   \
             -     3
           /
          2
        :return:
        """
        context = Context()
        context.addInfixPrefixOperator('-', 70)
        context.addInfixOperator('+', 70)

        parser = Parser('- 2 + 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0])

    def test_parse_2_plus_negative_3(self):
        """
                +
              /   \
             2     -
                    \
                     3
        :return:
        """
        context = Context()
        context.addInfixPrefixOperator('-', 70)
        context.addInfixOperator('+', 70)

        parser = Parser(' 2 + - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])
        self.assertEqual('-', token.data[1].id)

    def test_parse_2_minus_negative_3(self):
        """
                -
              /   \
             2     -
                    \
                     3
        :return:
        """
        context = Context()
        context.addInfixPrefixOperator('-', 70)

        parser = Parser(' 2 - - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual('-', token.data[1].id)
        self.assertEqual(3, token.data[1].data[0].data[0])

    def test_parse_negative_2_minus_3(self):
        """
                -
              /   \
             -     3
           /
          2
        :return:
        """
        context = Context()
        context.addInfixPrefixOperator('-', 70)

        parser = Parser(' - 2 - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual(3, token.data[1].data[0])
        self.assertEqual(2, token.data[0].data[0].data[0])

    def test_parse_2_plus_not_3(self):
        """
                +
              /   \
             2     !
                    \
                     3
        :return:
        """
        context = Context()
        context.addPrefixOperator('!', 120)
        context.addInfixPrefixOperator('+', 70)
        parser = Parser(' 2 + ! 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual('!', token.data[1].id)
        self.assertEqual(3, token.data[1].data[0].data[0])

    def test_parse_increment_i_minus_10(self):
        """
                -
              /   \
             ++    10
            /
           i
        :return:
        """
        context = Context()
        context.addPrefixOperator('++', 120)
        context.addInfixPrefixOperator('-', 70)
        parser = Parser('++ i - 10 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('++', token.data[0].id)
        self.assertEqual('i', token.data[0].data[0].data[0])
        self.assertEqual(10, token.data[1].data[0])


class TestPostfix(unittest.TestCase):

    def test_parse_i_increment_add_with_4(self):
        """
                +
              /   \
             ++     4
            /
           i
        :return:
        """
        context = Context()
        context.addPostfixOperator('++', 120)
        context.addInfixPrefixOperator('+', 70)
        parser = Parser('i ++ + 4 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('++', token.data[0].id)
        self.assertEqual('i', token.data[0].data[0].data[0])
        self.assertEqual(4, token.data[1].data[0])

    def test_parse_4_plus_i_increment(self):
        """
                +
              /   \
             4     ++
                    \
                     i
        :return:
        """
        context = Context()
        context.addPostfixOperator('++', 120)
        context.addInfixPrefixOperator('+', 70)
        parser = Parser('4 + i ++ ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual(4, token.data[0].data[0])
        self.assertEqual('++', token.data[1].id)
        self.assertEqual('i', token.data[1].data[0].data[0])


class TestBraces(unittest.TestCase):
    def test_parse_will_identify_the_braces(self):
        """
            {
        :return:
        """
        context = Context()
        context.addExpression('{', 0)
        context.addExpression('}', 0)
        context.addExpression(';', 0)
        parser = Parser('{ } ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual([], token.data)

    def test_parse_will_identify_the_semicolon_in_the_braces(self):
        """
            {
        :return:
        """
        context = Context()
        context.addExpression('{', 0)
        #context.addExpression('}',0)
        parser = Parser('{ ; } ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)

    def test_parse_will_point_to_the_next_location_after_finished_parse(self):
        """
            {
        :return:
        """
        context = Context()
        context.addExpression('{', 0)
        #context.addExpression('}',0)
        parser = Parser('{ ; } ', [context])
        context.setParser(parser)
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
        context = Context()
        context.addExpression('{', 0)
        context.addInfixPrefixOperator('+', 70)
        #context.addExpression('}',0)
        parser = Parser('{ 2 + 3 ; } ', [context])
        context.setParser(parser)
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
        context = Context()
        context.addExpression('{', 0)
        context.addInfixPrefixOperator('+', 70)
        context.addInfixOperator('*', 100)
        context.addInfixOperator('/', 100)
        #context.addExpression('}',0)
        parser = Parser('{ 2 + 3 ; \
                        3 * 4 ; \
                        5 / 9 ; \
                        } ', [context])
        context.setParser(parser)
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
        context = Context()
        context.addExpression('{', 0)
        context.addInfixOperator('*', 100)
        context.addInfixOperator('/', 100)
        context.addInfixPrefixOperator('+', 70)
        #context.addExpression('}',0)
        parser = Parser('{ 2 + 3 * 8 / 9 ; } ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('{', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual('/', token.data[0].data[1].id)
        self.assertEqual('*', token.data[0].data[1].data[0].id)
        self.assertEqual(3, token.data[0].data[1].data[0].data[0].data[0])
        self.assertEqual(8, token.data[0].data[1].data[0].data[1].data[0])
        self.assertEqual(9, token.data[0].data[1].data[1].data[0])

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
        context = Context()
        context.addPrefixGroupOperator('(', 0)
        context.addInfixOperator('*', 100)
        context.addInfixPrefixOperator('+', 70)
        #self.context.addPrefixGroupOperator(')', 0)
        parser = Parser('2 * ( 3 + 4 )', [context])
        context.setParser(parser)
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
        context = Context()
        context.addPrefixGroupOperator('(', 0)
        context.addInfixPrefixOperator('-', 70)
        context.addInfixPrefixOperator('+', 70)

        #self.context.addPrefixGroupOperator(')', 0)
        parser = Parser('- ( 3 + 4 )', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('+', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[0].id)
        self.assertEqual('(literal)', token.data[0].data[0].data[1].id)
        self.assertEqual(3, token.data[0].data[0].data[0].data[0])
        self.assertEqual(4, token.data[0].data[0].data[1].data[0])


class TestFlowControl(unittest.TestCase):

    def test_parse_will_build_an_if_AST(self):
        """
                if
            /       \
           ==       {
          / \
        2    3
        :return:
        """
        context = Context()
        #context.addExpression('}',0)
        context.addControl('if', 0)
        context.addInfixOperator('==', 20)
        context.addExpression('{', 0)
        parser = Parser('if ( 2 == 3 ) { } ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('if', token.id)
        self.assertEqual('==', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)

    def test_parse_will_build_an_if_else_AST(self):
        """
                if
            /       \
           ==       {
          / \
        2    3
        :return:
        """
        context = Context()
        #context.addExpression('}',0)
        context.addControl('if', 0)
        context.addInfixOperator('==', 20)
        context.addExpression('{', 0)
        parser = Parser('if ( 2 == 3 ) { }\
                        else { } ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('if', token.id)
        self.assertEqual('==', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('else', token.data[2].id)
        self.assertEqual('{', token.data[2].data[0].id)


if __name__ == '__main__':
    unittest.main()
