import unittest
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *

class TestParseFlowControl(unittest.TestCase):
    def setUp(self):
        self.flowControlContext = FlowControlContext()
        self.expressionContext = ExpressionContext()
        self.contexts = [self.expressionContext, self.flowControlContext]
        self.flowControlContext.addFlowControlOperator('while', 0)
        self.expressionContext.addPrefixGroupOperator('(', 0)
        self.expressionContext.addPrefixGroupOperator(')', 0)

    def xtest_parse_while_1(self):
        parser = Parser('while ( 1 )', self.contexts)
        token = parser.parse(0)
        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])

    def xtest_parse_while_1_without_closing_bracket_should_raise_an_error(self):
        parser = Parser('while ( 1', [self.flowControlContext])
        self.flowControlContext.setParser(parser)
        self.assertRaises(SyntaxError, parser.parse, 0)

if __name__ == '__main__':
    unittest.main()