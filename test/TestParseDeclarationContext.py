__author__ = 'JingWen'

import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Parser import *
from Context import *
from ContextManager import *
from DeclarationContext import *
from DefaultContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestDeclarationContextStartingWithShort(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_addShort_nud_given_short_x(self):
        lexer = LexerStateMachine('short x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addShort_nud_given_short_int_x(self):
        lexer = LexerStateMachine('short int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addShort_nud_given_short_unsigned_x(self):
        lexer = LexerStateMachine('short unsigned x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addShort_nud_given_short_int_signed_x(self):
        lexer = LexerStateMachine('short signed int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addShort_nud_given_short_unsigned_int_x(self):
        lexer = LexerStateMachine('short unsigned int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addShort_nud_given_short_x_with_assignment(self):
        lexer = LexerStateMachine('short x = 5 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            token = parser.parseStatement(0)
            self.assertEqual('int', token[0].id)
            self.assertEqual(None, token[0].sign)
            self.assertEqual('short', token[0].modifier)
            self.assertEqual('x', token[0].data[0].data[0])
            self.assertEqual('=', token[1].id)
            self.assertEqual('x', token[1].data[0].data[0])
            self.assertEqual(5, token[1].data[1].data[0])
        except SyntaxError as e:
            self.fail('should not raise Exception')

    def test_addShort_nud_given_short_without_identifier(self):
        lexer = LexerStateMachine('short ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting (identifier) before ;", e.msg)

    def test_addShort_nud_given_short_without_identifier_and_semicolon(self):
        lexer = LexerStateMachine('short', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting (identifier) before (systemToken)", e.msg)

    def test_addShort_nud_given_short_without_semicolon(self):
        lexer = LexerStateMachine('short x ', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting ; before (systemToken)", e.msg)

    def test_addShort_nud_given_short_x_int(self):
        lexer = LexerStateMachine('short x int ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting ; before int", e.msg)

    def test_addShort_nud_given_short_long_x(self):
        lexer = LexerStateMachine('short long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Cannot have both 'short' and 'long' in declaration statement", e.msg)

    def test_addShort_nud_given_short_short_x(self):
        lexer = LexerStateMachine('short short x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Duplication of 'short' in declaration statement", e.msg)


class TestDeclarationContextStartingWithLong(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_addLong_nud_given_long_x(self):
        lexer = LexerStateMachine('long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_long_x(self):
        lexer = LexerStateMachine('long long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_long_int_x(self):
        lexer = LexerStateMachine('long long int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_long_int_unsigned_x(self):
        lexer = LexerStateMachine('long long int unsigned x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_long_signed_x(self):
        lexer = LexerStateMachine('long long signed x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_long_unsigned_int_x(self):
        lexer = LexerStateMachine('long long unsigned int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_unsigned_x(self):
        lexer = LexerStateMachine('long unsigned x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_signed_long_x(self):
        lexer = LexerStateMachine('long signed long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_unsigned_long_x(self):
        lexer = LexerStateMachine('long unsigned long int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_signed_int_x(self):
        lexer = LexerStateMachine('long signed int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_unsigned_int_long_x(self):
        lexer = LexerStateMachine('long unsigned int long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_int_x(self):
        lexer = LexerStateMachine('long int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_int_long_x(self):
        lexer = LexerStateMachine('long int long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_int_long_signed_x(self):
        lexer = LexerStateMachine('long int long signed x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_int_unsigned_x(self):
        lexer = LexerStateMachine('long int unsigned x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addLong_nud_given_long_int_signed_long_x(self):
        lexer = LexerStateMachine('long int signed long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

class TestDeclarationContextStartingWithSignedOrUnsigned(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_addSignedAndUnsigned_nud_given_signed_x(self):
        lexer = LexerStateMachine('signed x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_x(self):
        lexer = LexerStateMachine('unsigned int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_short_x(self):
        lexer = LexerStateMachine('signed int short x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_long_x(self):
        lexer = LexerStateMachine('unsigned int long x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_int_long_long_x(self):
        lexer = LexerStateMachine('signed int long long x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_x(self):
        lexer = LexerStateMachine('unsigned long x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_int_x(self):
        lexer = LexerStateMachine('signed long int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_int_long_x(self):
        lexer = LexerStateMachine('unsigned long int long x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_signed_short_x(self):
        lexer = LexerStateMachine('signed short x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_short_int_x(self):
        lexer = LexerStateMachine('unsigned short int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_long_x(self):
        lexer = LexerStateMachine('signed long long x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addSignedAndUnsigned_nud_given_unsigned_long_long_int_x(self):
        lexer = LexerStateMachine('unsigned long long int x;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

class TestDeclarationContextStartingWithInt(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_addInt_nud_given_int_x(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_short_x(self):
        lexer = LexerStateMachine('int short x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_long_long_signed_x(self):
        lexer = LexerStateMachine('int long long signed x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_long_x(self):
        lexer = LexerStateMachine('int long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_long_unsigned_x(self):
        lexer = LexerStateMachine('int long unsigned x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_long_signed_long_x(self):
        lexer = LexerStateMachine('int long signed long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_signed_x(self):
        lexer = LexerStateMachine('int signed x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_unsigned_short_x(self):
        lexer = LexerStateMachine('int unsigned short x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_unsigned_long_x(self):
        lexer = LexerStateMachine('int unsigned long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('unsigned', token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_addInt_nud_given_int_signed_long_long_x(self):
        lexer = LexerStateMachine('int signed long long x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)
        token = parser.parseStatement(0)

        self.assertEqual('int', token[0].id)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('long long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

class TestDeclarationContextWithAssignmentAndComa(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.expressionContext.addPrefixInfixOperator('-', 70)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addShort('short', 0)
        self.declarationContext.addLong('long', 0)
        self.declarationContext.addSignedAndUnsigned('signed', 0)
        self.declarationContext.addSignedAndUnsigned('unsigned', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_int_x_without_semicolon(self):
        lexer = LexerStateMachine('int x', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_int_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_int_y_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, int y ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_coma_but_left_empty_will_raise_SyntaxError(self):
        lexer = LexerStateMachine('int x, ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parseStatement, 0)

    def test_int_x_x(self):
        lexer = LexerStateMachine('int x x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Expecting ; before (identifier)", e.msg)

    def test_int_x(self):
        lexer = LexerStateMachine('int x ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])

    def test_int_x_equal_to_2(self):
        lexer = LexerStateMachine('int x = 2 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(2, token[1].data[1].data[0])

    def test_short_x_equal_to_2(self):
        lexer = LexerStateMachine('short x = 2 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(2, token[1].data[1].data[0])

    def test_long_x_equal_to_2(self):
        lexer = LexerStateMachine('long x = 2 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].sign)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(2, token[1].data[1].data[0])

    def test_int_x_y_and_z(self):
        lexer = LexerStateMachine('int x , y , z ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('int', token[1].id)
        self.assertEqual('y', token[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('z', token[2].data[0].data[0])

    def test_short_x_y_and_z(self):
        lexer = LexerStateMachine('short x , y , z ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('short', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('int', token[1].id)
        self.assertEqual('short', token[1].modifier)
        self.assertEqual('y', token[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('short', token[2].modifier)
        self.assertEqual('z', token[2].data[0].data[0])

    def test_long_x_y_and_z(self):
        lexer = LexerStateMachine('long x , y , z ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('long', token[0].modifier)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('int', token[1].id)
        self.assertEqual('long', token[1].modifier)
        self.assertEqual('y', token[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('long', token[2].modifier)
        self.assertEqual('z', token[2].data[0].data[0])

    def test_signed_x_y_and_z(self):
        lexer = LexerStateMachine('signed x = - 1 , y = - 2 , z = - 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual(None, token[0].modifier)
        self.assertEqual('signed', token[0].sign)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual('-', token[1].data[1].id)
        self.assertEqual(1, token[1].data[1].data[0].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual(None, token[2].modifier)
        self.assertEqual('signed', token[2].sign)
        self.assertEqual('y', token[2].data[0].data[0])
        self.assertEqual('=', token[3].id)
        self.assertEqual('y', token[3].data[0].data[0])
        self.assertEqual('-', token[3].data[1].id)
        self.assertEqual(2, token[3].data[1].data[0].data[0])
        self.assertEqual('int', token[4].id)
        self.assertEqual(None, token[4].modifier)
        self.assertEqual('signed', token[4].sign)
        self.assertEqual('z', token[4].data[0].data[0])
        self.assertEqual('=', token[5].id)
        self.assertEqual('z', token[5].data[0].data[0])
        self.assertEqual('-', token[5].data[1].id)
        self.assertEqual(3, token[5].data[1].data[0].data[0])

    def test_int_x_y_and_z_with_some_initialization(self):
        lexer = LexerStateMachine('int x = 3 , y , z = 2 + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(3, token[1].data[1].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('y', token[2].data[0].data[0])
        self.assertEqual('int', token[3].id)
        self.assertEqual('z', token[3].data[0].data[0])
        self.assertEqual('=', token[4].id)
        self.assertEqual('z', token[4].data[0].data[0])
        self.assertEqual('+', token[4].data[1].id)
        self.assertEqual(2, token[4].data[1].data[0].data[0])
        self.assertEqual(3, token[4].data[1].data[1].data[0])

    def test_int_x_y_z_with_initialization(self):  ################################################# should fail?
        lexer = LexerStateMachine('int x = 3 , y = 2 + 3 , z = y + 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('x', token[0].data[0].data[0])
        self.assertEqual('=', token[1].id)
        self.assertEqual('x', token[1].data[0].data[0])
        self.assertEqual(3, token[1].data[1].data[0])
        self.assertEqual('int', token[2].id)
        self.assertEqual('y', token[2].data[0].data[0])
        self.assertEqual('=', token[3].id)
        self.assertEqual('y', token[3].data[0].data[0])
        self.assertEqual('+', token[3].data[1].id)
        self.assertEqual(2, token[3].data[1].data[0].data[0])
        self.assertEqual(3, token[3].data[1].data[1].data[0])
        self.assertEqual('int', token[4].id)
        self.assertEqual('z', token[4].data[0].data[0])
        self.assertEqual('=', token[5].id)
        self.assertEqual('z', token[5].data[0].data[0])
        self.assertEqual('+', token[5].data[1].id)
        self.assertEqual('y', token[5].data[1].data[0].data[0])
        self.assertEqual(3, token[5].data[1].data[1].data[0])

    def test_expression_with_separate_initialization(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                      int y = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('int', token[0].data[2].id)
        self.assertEqual('y', token[0].data[2].data[0].data[0])
        self.assertEqual('=', token[0].data[3].id)
        self.assertEqual('y', token[0].data[3].data[0].data[0])
        self.assertEqual(15, token[0].data[3].data[1].data[0])

    def test_nested_bracers(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                         { int y = 5 ; }\
                         { int z = 15 ; } }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('{', token[0].data[2].id)
        self.assertEqual('int', token[0].data[2].data[0].id)
        self.assertEqual('y', token[0].data[2].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[2].data[1].id)
        self.assertEqual('y', token[0].data[2].data[1].data[0].data[0])
        self.assertEqual(5, token[0].data[2].data[1].data[1].data[0])
        self.assertEqual('{', token[0].data[3].id)
        self.assertEqual('int', token[0].data[3].data[0].id)
        self.assertEqual('z', token[0].data[3].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[3].data[1].id)
        self.assertEqual('z', token[0].data[3].data[1].data[0].data[0])
        self.assertEqual(15, token[0].data[3].data[1].data[1].data[0])

    def test_declaration_expression_declaration(self):
        lexer = LexerStateMachine('{ int x = 3 ;\
                                     x = 5 + 10 ;\
                                     int z = 15 ; }', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('{', token[0].id)
        self.assertEqual('int', token[0].data[0].id)
        self.assertEqual('x', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[0].data[1].id)
        self.assertEqual('x', token[0].data[1].data[0].data[0])
        self.assertEqual(3, token[0].data[1].data[1].data[0])
        self.assertEqual('=', token[0].data[2].id)
        self.assertEqual('x', token[0].data[2].data[0].data[0])
        self.assertEqual('+', token[0].data[2].data[1].id)
        self.assertEqual(5, token[0].data[2].data[1].data[0].data[0])
        self.assertEqual(10, token[0].data[2].data[1].data[1].data[0])
        self.assertEqual('int', token[0].data[3].id)
        self.assertEqual('z', token[0].data[3].data[0].data[0])
        self.assertEqual('=', token[0].data[4].id)
        self.assertEqual('z', token[0].data[4].data[0].data[0])
        self.assertEqual(15, token[0].data[4].data[1].data[0])

    def test_int_int_will_raiseException(self):
        lexer = LexerStateMachine('int int x = 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        try:
            parser.parseStatement(0)
        except SyntaxError as e:
            self.assertEqual("Duplication of 'int' in declaration statement", e.msg)

"""

class TestPointerDeclaration(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.expressionContext = ExpressionContext(self.manager)
        self.contexts = [self.declarationContext, self.expressionContext, self.defaultContext, self.flowControlContext]
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addPrefixInfixOperator('+', 70)
        self.declarationContext.addIntDeclaration('int', 0)
        self.declarationContext.addPointerDeclaration('*', 120)
        self.expressionContext.addOperator(',', 0)
        self.expressionContext.addOperator(';', 0)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)

        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_int_pointer(self):
        lexer = Lexer('int * ptr ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('*', token[0].data[0].id)
        self.assertEqual('ptr', token[0].data[0].data[0].data[0])


    def test_int_pointer_equal_3(self):
        lexer = Lexer('int * ptr = 3 ;', self.context)
        parser = Parser(lexer, self.manager)
        self.manager.setParser(parser)

        token = parser.parseStatement(0)
        self.assertEqual('int', token[0].id)
        self.assertEqual('*', token[0].data[0].id)
        self.assertEqual('ptr', token[0].data[0].data[0].data[0])
        self.assertEqual('=', token[1].data[0].id)
        self.assertEqual('ptr', token[1].data[0].data[0])
        self.assertEqual('3', token[1].data[0].data[1])
"""

if __name__ == '__main__':
    unittest.main()
