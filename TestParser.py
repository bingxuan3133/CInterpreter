import unittest
from Context import *
from Parser import *

class MyTestCase(unittest.TestCase):
    def test_parse_2_plus_3(self):
        context = Context()
        addClass = context.addInfixOperator('+', 70)
        end = context.addInfixOperator('(end)', 0)
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
        addClass = context.addInfixOperator('+', 70)
        mulClass = context.addInfixOperator('*', 100)
        end = context.addInfixOperator('(end)', 0)

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
        mulClass = context.addInfixOperator('*', 100)
        addClass = context.addInfixOperator('+', 70)
        end = context.addInfixOperator('(end)', 0)

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
        mulClass = context.addInfixOperator('*', 100)
        addClass = context.addInfixOperator('+', 70)
        subClass = context.addInfixOperator('-', 70)
        end = context.addInfixOperator('(end)', 0)

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
        mulClass = context.addInfixOperator('*', 100)
        addClass = context.addInfixOperator('+', 70)
        end = context.addInfixOperator('(end)', 0)

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
        mulClass = context.addInfixOperator('*', 100)
        addClass = context.addInfixOperator('+', 70)
        end = context.addInfixOperator('(end)', 0)

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
        context.addPrefixOperator('!',120)
        context.addInfixOperator('+', 70)
        context.addInfixOperator('(end)', 0)

        parser = Parser('! 2 + 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('!', token.data[0].id)
        self.assertEqual( 2 , token.data[0].data[0].data[0])
        self.assertEqual( 3 , token.data[1].data[0])


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
        context.addPrefixOperator('-',120)
        context.addInfixOperator('+', 70)
        context.addInfixOperator('(end)', 0)

        parser = Parser('- 2 + 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual( 2 , token.data[0].data[0].data[0])
        self.assertEqual( 3 , token.data[1].data[0])


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
        context.addPrefixOperator('-',120)
        context.addInfixOperator('+', 70)
        context.addInfixOperator('(end)', 0)

        parser = Parser(' 2 + - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual( 3 , token.data[1].data[0].data[0])
        self.assertEqual( '-' , token.data[1].id)


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
        context.addPrefixOperator('-',120)
        context.addInfixOperator('-', 70)
        context.addInfixOperator('(end)', 0)

        parser = Parser(' 2 - - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual(2, token.data[0].data[0])
        self.assertEqual( '-' , token.data[1].id)
        self.assertEqual( 3 , token.data[1].data[0].id)

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
        classMinus = context.addInfixOperator('-', 70)
        classMinus.nud = nud
        context.addInfixOperator('(end)', 0)

        parser = Parser(' - 2 - 3 ', [context])
        context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('-', token.data[0].id)
        self.assertEqual( 3 , token.data[1].data[0])
        self.assertEqual( 2 , token.data[0].data[0].data[0])


if __name__ == '__main__':
    unittest.main()
