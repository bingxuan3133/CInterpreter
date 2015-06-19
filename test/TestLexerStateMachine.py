__author__ = 'Jing'
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

import unittest
from LexerStateMachine import *
from Context import *
from ContextManager import *

class TestLexer(unittest.TestCase):

    def setUp(self):
        pass

    def testAdvance(self):
        manager = ContextManager()
        context = Context(manager)
        lexer = LexerStateMachine(""" hi krizz
                          987 456 """, context)
        self.assertEqual(lexer.peep().data[0], 'hi')
        self.assertEqual(lexer.advance().data[0], 'krizz')
        self.assertEqual(lexer.advance().data[0], 987)
        self.assertEqual(lexer.advance().data[0], 456)

    def test_peep_should_raise_error_when_the_returned_symbol_is_not_equal_to_the_expected_symbol(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        self.assertRaises(SyntaxError, lexer.peep, '*')

    def test_peep_should_not_raise_error_when_the_returned_symbol_is_equal_to_the_expected_symbol(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        lexer.peep()
        #self.assertRaises(None, lexer.peep, '(')

    def test_peep_should_not_raise_error_when_the_expected_symbol_is_none(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        lexer = LexerStateMachine('(', context)
        lexer.peep()

    def test_advance_should_raise_error_when_the_returned_token_is_not_equal_to_the_expected_token(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        self.assertRaises(SyntaxError, lexer.advance, '*')

    def test_advance_should_not_raise_error_when_the_returned_token_is_equal_to_the_expected_token(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        lexer.advance()
        #self.assertRaises(None, lexer.advance, ')')

    def test_advance_should_not_raise_error_when_expected_symbol_is_none(self):
        manager = ContextManager()
        context = Context(manager)
        manager.setCurrentContexts([context])
        context.addOperator('(')
        context.addOperator(')')
        lexer = LexerStateMachine('( )', context)
        lexer.advance()




