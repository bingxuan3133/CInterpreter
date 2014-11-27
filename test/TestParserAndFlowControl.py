import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Context import *
from DefaultContext import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *
from ContextManager import *

class TestParseWhileFlowControl(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext, self.flowControlContext, self.defaultContext]

        self.flowControlContext.addWhileControl('while', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addOperator(')', 0)
        self.expressionContext.addPostfixOperator('++', 150)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.defaultContext.addKeyword('while')

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_while_1(self):
        lexer = Lexer('while ( 1 ) ;', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])

    def test_parse_while_1_while_1(self):
        lexer = Lexer('while ( 1 ) while ( 1 ) ;', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('while', token.data[1].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(1, token.data[1].data[0].data[0])

    def test_parse_while_1_do_something(self):
        lexer = Lexer('while ( 1 ) i ++ ;', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('++', token.data[1].id)
        self.assertEqual('(identifier)', token.data[1].data[0].id)
        self.assertEqual('i', token.data[1].data[0].data[0])

    def test_parse_while_while_1_should_raise_an_error(self):
        lexer = Lexer('while ( while ( 1 ) ) ;', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        self.assertRaises(SyntaxError, parser.parse, 0)

    def test_parse_while_1_without_closing_bracket_should_raise_an_error(self):
        lexer = Lexer('while ( 1', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)

    # while control with block statement
    def test_parse_while_1_empty_block_statement(self):
        """
            while
            /   \
           1     {
        :return:
        """
        self.flowControlContext.addBlockOperator('{', 0)
        lexer = Lexer('while ( 1 ) { }', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('{', token.data[1].id)

    def test_parse_while_1_block_statement_with_while_1_with_block_statement(self):
        """
            while
            /   \
           1     {
                 |- while
                    /   \
                   1     {
        :return:
        """
        lexer = Lexer('while ( 1 ) { while ( 1 ) { } } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('while', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].data[0].id)
        self.assertEqual(1, token.data[1].data[0].data[0].data[0])
        self.assertEqual('{', token.data[1].data[0].data[1].id)

    def test_parse_while_1_block_statement_with_while_1(self):
        """
            while
            /   \
           1     {
                 |- while
                    /
                   1
        :return:
        """
        lexer = Lexer('while ( 1 ) { while ( 1 ) ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('while', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].data[0].id)
        self.assertEqual(1, token.data[1].data[0].data[0].data[0])

    def test_parse_while_1_do_few_statements(self):
        """
            while
            /   \
           1     {
                 |- 2 + 3
                 |- i
                 |- j
        :return:
        """
        lexer = Lexer('while ( 1 ) { 2 + 3 ; i ; j ; }', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('+', token.data[1].data[0].id)
        self.assertEqual('(literal)', token.data[1].data[0].data[0].id)
        self.assertEqual(2, token.data[1].data[0].data[0].data[0])
        self.assertEqual('(literal)', token.data[1].data[0].data[1].id)
        self.assertEqual(3, token.data[1].data[0].data[1].data[0])
        self.assertEqual('(identifier)', token.data[1].data[1].id)
        self.assertEqual('i', token.data[1].data[1].data[0])
        self.assertEqual('(identifier)', token.data[1].data[2].id)
        self.assertEqual('j', token.data[1].data[2].data[0])

class TestParseDoWhileFlowControl(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext, self.flowControlContext, self.defaultContext]

        self.flowControlContext.addDoWhileControl('do', 0)
        self.flowControlContext.addOperator('while', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addOperator(')', 0)
        self.expressionContext.addPostfixOperator('++', 150)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.defaultContext.addKeyword('while')

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_do_while(self):
        lexer = Lexer('do 2 + 3 ; while ( 1 ) ;', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('do', token.id)
        self.assertEqual('+', token.data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[1].data[0])
        self.assertEqual('while', token.data[1].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(1, token.data[1].data[0].data[0])

class TestParseIfFlowControl(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.expressionContext, self.flowControlContext, self.defaultContext]

        self.flowControlContext.addDoWhileControl('do', 0)
        self.flowControlContext.addOperator('while', 0)
        self.flowControlContext.addOperator('else',0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addGroupOperator('(', 0)
        self.expressionContext.addOperator(')', 0)
        self.expressionContext.addPostfixOperator('++', 150)
        self.expressionContext.addPrefixInfixOperator('+', 70)

        self.flowControlContext.addIfControl('if', 0)
        self.expressionContext.addInfixOperator('==', 10)
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addInfixOperator('*', 100)
        self.defaultContext.addKeyword('while')

        self.defaultContext.addKeyword('if')

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parse_will_build_an_if_AST(self):
        """
                if
            /       \
           (        {
           |
           ==
          / \
        2    3
        :return:
        """

        lexer = Lexer('if ( 2 == 3 ) { } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)

    def test_parse_will_build_an_if_AST_that_contain_expression(self):
        """
                if
            /       \
            (       {
            |
           ==
          / \
        2    3
        :return:
        """
        lexer = Lexer(' if ( 2 == 3 ) { 5 * 6 ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('*', token.data[1].data[0].id)
        self.assertEqual(5, token.data[1].data[0].data[0].data[0])
        self.assertEqual(6, token.data[1].data[0].data[1].data[0])

    def test_parse_will_build_an_if_else_AST(self):
        """
                if      -  else
            /       \        |
            (       {        {
            |
           ==
          / \
        2    3
        :return:
        """
        lexer = Lexer(' if ( 2 == 3 ) { }\
                        else { } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)


        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('else', token.data[2].id)
        self.assertEqual('{', token.data[2].data[0].id)

    def test_parse_will_raise_error_if_the_if_statement_contain_no_condition(self):

        lexer = Lexer(' if ( ) ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)

    def test_parse_will_build_an_if_statement_with_expression_inside(self):
        """
                if
            /       \
            (       {
           ==       |
          / \       |
        2    3      =
                  /   \
                 x     *
                     /   \
                    2    3
        :return:
        """
        lexer = Lexer(' if ( 2 == 3 ) { x = 2 * 3 ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)

        token = parser.parse(0)
        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('=', token.data[1].data[0].id)
        self.assertEqual('x', token.data[1].data[0].data[0].data[0])
        self.assertEqual('*', token.data[1].data[0].data[1].id)
        self.assertEqual(2, token.data[1].data[0].data[1].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[1].data[1].data[0])

    def test_parse_will_build_an_if_statement_with_multiple_expression_inside(self):
        """
                if
            /       \
            (       {
            |       |
           ==       |
          / \       |
        2    3      =
                  /   \
                 x     *
                     /   \
                    2    3
        :return:
        """
        lexer = Lexer('if ( 2 == 3 ) { x = 2 * 3 ;\
                                        y = 5 + 7 ; } ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        token = parser.parse(0)

        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('{', token.data[1].id)
        self.assertEqual('=', token.data[1].data[0].id)
        self.assertEqual('x', token.data[1].data[0].data[0].data[0])
        self.assertEqual('*', token.data[1].data[0].data[1].id)
        self.assertEqual(2, token.data[1].data[0].data[1].data[0].data[0])
        self.assertEqual(3, token.data[1].data[0].data[1].data[1].data[0])
        self.assertEqual('=', token.data[1].data[1].id)
        self.assertEqual('y', token.data[1].data[1].data[0].data[0])
        self.assertEqual('+', token.data[1].data[1].data[1].id)
        self.assertEqual(5, token.data[1].data[1].data[1].data[0].data[0])
        self.assertEqual(7, token.data[1].data[1].data[1].data[1].data[0])

    def test_parse_will_build_an_if_statement_without_the_brace(self):
        """
                if
            /       \
           ==       {
          / \       |
        2    3      =
                  /   \
                 x     *
                     /   \
                    2    3
        :return:
        """

        lexer = Lexer('if ( 2 == 3 ) x = 2 * 3 ; ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        token = parser.parse(0)

        self.assertEqual('if', token.id)
        self.assertEqual('(', token.data[0].id)
        self.assertEqual('==', token.data[0].data[0].id)
        self.assertEqual(2, token.data[0].data[0].data[0].data[0])
        self.assertEqual(3, token.data[0].data[0].data[1].data[0])
        self.assertEqual('=', token.data[1].id)
        self.assertEqual('x', token.data[1].data[0].data[0])
        self.assertEqual('*', token.data[1].data[1].id)
        self.assertEqual(2, token.data[1].data[1].data[0].data[0])
        self.assertEqual(3, token.data[1].data[1].data[1].data[0])

    def test_parse_throw_an_error_if_the_brace_does_not_close(self):

        lexer = Lexer('( 2 == 3 ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        self.assertRaises(SyntaxError, parser.parse, 0)

    def test_parse_throw_an_error_if_the_if_is_being_in_the_condition_brace(self):
        lexer = Lexer('if ( if ( x == 2 ) ) ', self.context)
        parser = Parser(lexer)
        self.manager.setParser(parser)
        self.assertRaises(SyntaxError, parser.parse, 0)

if __name__ == '__main__':
    unittest.main()