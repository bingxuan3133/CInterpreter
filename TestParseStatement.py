import unittest
from ContextManager import *
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        expressionContext = ExpressionContext(self.manager)
        flowControlContext = FlowControlContext(self.manager)
        self.contexts = [expressionContext, flowControlContext]

        flowControlContext.addBlockOperator('{', 0)
        expressionContext.addPrefixInfixOperator('+', 70)
        expressionContext.addPrefixInfixOperator('-', 70)
        expressionContext.addInfixOperator('*', 100)
        expressionContext.addInfixOperator('/', 100)
        expressionContext.addInfixOperator('==', 20)
        expressionContext.addOperator(';')
        self.context.addOperator('}', 0)
        #flowControlContext.addBlockOperator('}', 0)
        flowControlContext.addIfControl('if', 0)
        expressionContext.addGroupOperator('(', 0)
        expressionContext.addGroupOperator(')', 0)

        self.manager.addContext('Expression', expressionContext)
        self.manager.addContext('FlowControl', flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_will_return_None_for_an_empty_brace(self):
        """
            {
        :return:
        """
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer('{ } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        flowControlContext = FlowControlContext(self.manager)
        token = flowControlContext.parseStatement(0)
        self.assertEqual('{', token.id)
        self.assertEqual([], token.data)

    def test_parse_will_ignore_the_semicolon_in_the_brace(self):
        """
            {
        :return:
        """
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer('{ ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        flowControlContext = FlowControlContext(self.manager)
        token = flowControlContext.parseStatement(0)
        self.assertEqual('{', token.id)
        self.assertEqual([], token.data)

    def test_parse_will_build_an_ast_for_expression_in_the_brace(self):
        """
            {
            |
            +
          /   \
         2     3
        :return:
        """
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer('{ 2 + 3 ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        flowControlContext = FlowControlContext(self.manager)
        token = flowControlContext.parseStatement(0)
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
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer('{ 2 + 3 ; \
                        3 * 4 ; \
                        5 / 9 ; \
                        } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        flowControlContext = FlowControlContext(self.manager)
        token = flowControlContext.parseStatement(0)
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
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer(' { 2 + 3 * 8 / 9 ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        flowControlContext = FlowControlContext(self.manager)
        token = flowControlContext.parseStatement(0)

        self.assertEqual('{', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual('/', token.data[0].data[1].id)
        self.assertEqual('*', token.data[0].data[1].data[0].id)
        self.assertEqual(3, token.data[0].data[1].data[0].data[0].data[0])
        self.assertEqual(8, token.data[0].data[1].data[0].data[1].data[0])
        self.assertEqual(9, token.data[0].data[1].data[1].data[0])

    def test_parseStatement_will_throw_an_error_when_the_brace_is_not_closed(self):
        flowControlContext = FlowControlContext(self.manager)
        lexer = Lexer('{ 2 + 3 ; ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        flowControlContext = FlowControlContext(self.manager)
        self.assertRaises(SyntaxError, flowControlContext.parseStatement, 0)


    def test_parseStatement_will_parse_a_statement_that_contain_no_statements_in_the_brace(self):
        """
                if
            /       \
           (        {
           |
           ==
          / \
        x    2
        :return:
        """
        lexer = Lexer(' if ( x == 2 ) { } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        token = parser.parse(0)
        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual('x', token.data[0].data[0].data[0].data[0])
        self.assertEqual(2, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)

if __name__ == '__main__':
    unittest.main()
