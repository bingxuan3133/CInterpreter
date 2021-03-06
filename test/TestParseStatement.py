import unittest

import os, sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from ContextManager import *
from Context import *
from LexerStateMachine import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *

class TestParseStatement(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.contexts = [self.expressionContext, self.flowControlContext]
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_without_expression_after_equal(self):
        lexer = LexerStateMachine('x = ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:

            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
             self.assertEqual("Error[1][5]:Expected a declaration"+'\n'+
                             'x = ;'+'\n'+
                             '    ^', e.msg)


    def test_parseStatement_will_return_None_for_an_empty_statement(self):
        """
            ;
        :return:
        """
        lexer = LexerStateMachine(';', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.assertEqual(None, token)

    def test_parseStatement_should_return_2_plus_3_for_a_2_plus_3_statement(self):
        """
            2 + 3 ;
        :return:
        """
        lexer = LexerStateMachine('2 + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        self.assertEqual('+', token[0].id)
        self.assertEqual(2, token[0].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[0])

    def test_parseStatement_should_raise_SyntaxError_for_a_2_plus_3_statement_without_semicolon(self):
        """
            2 + 3
        :return:
        """
        lexer = LexerStateMachine('2 + 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:

            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][6]:Expecting ; before EOF"+'\n'+
                             '2 + 3'+'\n'+
                             '     ^', e.msg)

    def test_parseStatement_should_raise_SyntaxError_for_a_plus_3_statement_without_semicolon(self):
        """
            2 + 3
        :return:
        """
        lexer = LexerStateMachine('+ 3', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][4]:Expecting ; before EOF"+'\n'+
                             '+ 3'+'\n'+
                             '   ^', e.msg)

class TestParseStatementWithBraces(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.contexts = [self.expressionContext, self.flowControlContext]

        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_parseStatement_should_return_open_brace_token_for_an_empty_brace(self):
        """
            { }
        :return:
        """
        lexer = LexerStateMachine('{ }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual([], token[0].data)

    def test_parseStatement_should_return_open_brace_token_with_empty_data_for_an_empty_statement(self):
        """
            { ; }
        :return:
        """
        lexer = LexerStateMachine('{ ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual([], token[0].data)

    def test_parseStatement_should_return_open_brace_token_with_empty_data_for_3_empty_statements(self):
        """
            { ; ; ; }
        :return:
        """
        lexer = LexerStateMachine('{ ;; ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual([], token[0].data)

    def test_parse_will_build_an_ast_for_expression_in_the_brace(self):
        """
            {
            |
            +
          /   \
         2     3
        :return:
        """
        lexer = LexerStateMachine('{ 2 + 3 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('+', token[0].data[0].id)
        self.assertEqual(2, token[0].data[0].data[0].data[0])
        self.assertEqual(3, token[0].data[0].data[1].data[0])

    def test_parseStatement_should_build_ast_for_double_layers_of_braces(self):
        """
            {
            |
            {
            |
            +
          /   \
         2     3
        :return:
        """
        lexer = LexerStateMachine('{ { 2 + 3 ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('{', token[0].data[0].id)
        self.assertEqual('+', token[0].data[0].data[0].id)
        self.assertEqual(2, token[0].data[0].data[0].data[0].data[0])
        self.assertEqual(3, token[0].data[0].data[0].data[1].data[0])

    def test_parse_will_build_an_ast_for_expressions_in_the_brace(self):
        """
        {----------------------
            |       |         |
            +       *         /
          /   \    /   \    /   \
         2     3  3     4  5     9
        :return:
        """
        lexer = LexerStateMachine('{ 2 + 3 ; \
                        3 * 4 ; \
                        5 / 9 ; \
                        }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('+', token[0].data[0].id)
        self.assertEqual(2, token[0].data[0].data[0].data[0])
        self.assertEqual(3, token[0].data[0].data[1].data[0])
        self.assertEqual('*', token[0].data[1].id)
        self.assertEqual(3, token[0].data[1].data[0].data[0])
        self.assertEqual(4, token[0].data[1].data[1].data[0])
        self.assertEqual('/', token[0].data[2].id)
        self.assertEqual(5, token[0].data[2].data[0].data[0])
        self.assertEqual(9, token[0].data[2].data[1].data[0])

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
        lexer = LexerStateMachine(' { 2 + 3 * 8 / 9 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatements(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('+', token[0].data[0].id)
        self.assertEqual(2, token[0].data[0].data[0].data[0])
        self.assertEqual('/', token[0].data[0].data[1].id)
        self.assertEqual('*', token[0].data[0].data[1].data[0].id)
        self.assertEqual(3, token[0].data[0].data[1].data[0].data[0].data[0])
        self.assertEqual(8, token[0].data[0].data[1].data[0].data[1].data[0])
        self.assertEqual(9, token[0].data[0].data[1].data[1].data[0])

    def test_parseStatement_should_return_a_list_of_tree_if_the_expression_is_long_and_being_in_braces(self):
        lexer = LexerStateMachine('{ x = y + 8 * 16 / 180 - 20 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('=', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('-', token[0].data[0].data[1].id)
        self.assertEqual(20, token[0].data[0].data[1].data[1].data[0])
        self.assertEqual('+', token[0].data[0].data[1].data[0].id)
        self.assertEqual('y', token[0].data[0].data[1].data[0].data[0].data[0])
        self.assertEqual('/', token[0].data[0].data[1].data[0].data[1].id)
        self.assertEqual(180, token[0].data[0].data[1].data[0].data[1].data[1].data[0])
        self.assertEqual('*', token[0].data[0].data[1].data[0].data[1].data[0].id)
        self.assertEqual(8, token[0].data[0].data[1].data[0].data[1].data[0].data[0].data[0])
        self.assertEqual(16, token[0].data[0].data[1].data[0].data[1].data[0].data[1].data[0])

    def test_parseStatement_should_raise_SyntaxError_when_there_is_missing_close_brace(self):
        lexer = LexerStateMachine('{ 2 + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][10]:Expecting } before EOF"+'\n'+
                             '{ 2 + 3 ;'+'\n'+
                             '         ^', e.msg)

    def test_parseStatement_should_raise_SyntaxError_when_there_is_missing_one_close_brace(self):
        lexer = LexerStateMachine('{ 2 + 3 ; { }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][14]:Expecting } before EOF"+'\n'+
                             '{ 2 + 3 ; { }'+'\n'+
                             '             ^', e.msg)

    def test_parseStatement_should_raise_SyntaxError_when_there_is_missing_open_brace(self):
        lexer = LexerStateMachine('2 + 3 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)
        try:
            parser.parseStatement(0)
            raise SyntaxError("Exception test failed")
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Expected a declaration"+'\n'+
                             '2 + 3 ; }'+'\n'+
                             '        ^', e.msg)

if __name__ == '__main__':
    unittest.main()
