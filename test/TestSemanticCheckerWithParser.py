__author__ = 'admin'

import unittest
from Parser import *
from SemanticChecker import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestSemanticCheckerWithParserDeclarationCheck(unittest.TestCase):
    def setUp(self):
        self.contextManager = ContextManager()
        self.context = Context(self.contextManager)
        self.defaultContext = DefaultContext(self.contextManager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.contextManager)
        self.expressionContext = ExpressionContext(self.contextManager)
        self.flowControlContext = FlowControlContext(self.contextManager)
        self.contexts = [self.expressionContext, self.declarationContext, self.flowControlContext, self.defaultContext]
        self.contextManager.addContext('Default', self.defaultContext)
        self.contextManager.addContext('Declaration', self.declarationContext)
        self.contextManager.addContext('Expression', self.expressionContext)
        self.contextManager.addContext('FlowControl', self.flowControlContext)
        self.contextManager.setCurrentContexts(self.contexts)

    def test_isAllDefined_should_not_raise_given_x_is_globally_defined_and_y_z_are_locally_defined(self):
        lexer = LexerStateMachine('int x; {int y; int z; x = y + z;}', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        parser.semanticChecker.isEnable = True
        try:
            token = parser.parseStatement(0)
            token = parser.parseStatement(0)
        except SyntaxError as e:
            self.fail(e.msg)

    def test_isAllDefined_should_not_raise_given_x_is_undefined_and_y_z_are_locally_defined(self):
        lexer = LexerStateMachine('int a; {int y; int z; x = y + z;}', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        parser.semanticChecker.isEnable = True
        try:
            token = parser.parseStatement(0)
            token = parser.parseStatement(0)
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[1][23]:Undefined reference 'x'" + '\n' +
                             'int a; {int y; int z; x = y + z;}' + '\n' +
                             '                      ^', e.msg)

if __name__ == '__main__':
    unittest.main()
