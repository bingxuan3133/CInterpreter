import unittest
from Context import *
from Parser import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.context.addInfixOperator('*', 100)
        self.context.addPrefixInfixOperator('+', 70)
        self.context.addPrefixInfixOperator('-', 70)

    def test_parse_2_plus_3(self):
        parser = Parser('2 + 3', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('2 + 3 * 4', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('2 * 3 + 4', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('2 * 3 + 4 - 5', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('2 * 3 + 4 * 5', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('2 + 3 * 4 + 5', [self.context])
        self.context.setParser(parser)
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

    def test_parse_negative_2_plus_3(self):
        """
                +
              /  \
            -     3
          /
        2
        :return:
        """
        parser = Parser('- 2 + 3', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('- 2 + - 3', [self.context])
        self.context.setParser(parser)
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
        parser = Parser('- 2 - - 3', [self.context])
        self.context.setParser(parser)
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
        self.context.addPrefixOperator('!', 120)
        parser = Parser('! 2 - ! 3', [self.context])
        self.context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('-', token.id)
        self.assertEqual('!', token.data[0].id)
        self.assertEqual('!', token.data[1].id)
        self.assertEqual('(literal)', token.data[0].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[0])

    def xtest_parse_post_increment_i(self):
        self.context.addInfixOperator('++', 150)
        parser = Parser('i ++', [self.context])
        self.context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('(identifier)', token.id)
        self.assertEqual('i', token.data[0])
        self.assertEqual('++', token.data[1].id)

    def xtest_parse_i_plus_j(self):
        parser = Parser('i + j', [self.context])
        self.context.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('+', token.id)
        self.assertEqual('(identifier)', token.data[0].id)
        self.assertEqual('(identifier)', token.data[1].id)
        self.assertEqual('i', token.data[0].data[0])
        self.assertEqual('j', token.data[1].data[0])

if __name__ == '__main__':
    unittest.main()
