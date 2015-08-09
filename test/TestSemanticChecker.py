__author__ = 'admin'

import unittest
from Parser import *
from SemanticChecker import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestSemanticCheckerAssignmentCheck(unittest.TestCase):
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

    def test_getIdentifierType(self):
        declToken = self.declarationContext.createDeclarationOrDefinitionToken('(decl)')
        intToken = self.context.createToken('int')
        xToken = self.context.createToken('x')
        declToken.data.append(intToken)
        declToken.data.append(xToken)

        semanticChecker = SemanticChecker()
        types = semanticChecker.getIdentifierDeclarationType(declToken)
        self.assertEqual(['int'], types)

    def test_getIdentifierType_return_a_list_of_types_of_an_identifier(self):
        declToken = self.declarationContext.createDeclarationOrDefinitionToken('(decl)')
        ptrToken = self.context.createToken('*')
        intToken = self.context.createToken('int')
        xToken = self.context.createToken('x')
        intToken.data.append(ptrToken)
        declToken.data.append(intToken)
        declToken.data.append(xToken)

        semanticChecker = SemanticChecker()
        types = semanticChecker.getIdentifierDeclarationType(declToken)
        self.assertEqual(['int', '*'], types)

    def test_isDefined_return_True_when_x_is_defined(self):
        lexer = LexerStateMachine('int x; x = 0;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatements(0)
            semanticChecker.checkIfIdentifierIsDefined(token[1].data[0])
        except SyntaxError as e:
            self.fail(e.msg)

class TestSemanticCheckerDeclarationCheck(unittest.TestCase):
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

    def test_isDefined_return_True_when_x_is_defined(self):
        lexer = LexerStateMachine('int x; x = 0;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatements(0)
            semanticChecker.checkIfIdentifierIsDefined(token[1].data[0])
        except SyntaxError as e:
            self.fail(e.msg)

    def test_isAllDefined_should_not_raise_given_x_y_z_is_defined(self):
        lexer = LexerStateMachine('int x; int y; int z; x = y + z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
        except SyntaxError as e:
            self.fail(e.msg)

    def test_isDefined_will_raise_when_x_is_not_defined(self):
        lexer = LexerStateMachine('x = 0;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfIdentifierIsDefined(token[0].data[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[1][1]:Undefined reference 'x'" + '\n' +
                             'x = 0;' + '\n' +
                             '^', e.msg)

    def test_isAllDefined_should_not_raise_given_x_is_defined(self):
        lexer = LexerStateMachine('int x;\nint y = x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
        except SyntaxError as e:
            self.assertEqual("Error[3][9]:Undefined reference 'y'" + '\n' +
                             'x = 2 + y;' + '\n' +
                             '        ^', e.msg)

    def test_isAllDefined_should_raise_given_y_is_not_defined(self):
        lexer = LexerStateMachine('int x;\nx = 0;\nx = 2 + y;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
        except SyntaxError as e:
            self.assertEqual("Error[3][9]:Undefined reference 'y'" + '\n' +
                             'x = 2 + y;' + '\n' +
                             '        ^', e.msg)

    def test_isAllDefined_should_raise_given_y_is_not_defined_before_its_declaration(self):
        lexer = LexerStateMachine('int x = y;\nint y;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Undefined reference 'y'" + '\n' +
                             'int x = y;' + '\n' +
                             '        ^', e.msg)

    def test_isAllDefined_should_raise_given_x_has_invalid_type(self):
        lexer = LexerStateMachine('int x; *x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfTypeValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Invalid type of 'x'" + '\n' +
                             'int x; *x;' + '\n' +
                             '       ^', e.msg)

    def test_isAllDefined_should_not_raise_given_x_has_valid_type(self):
        lexer = LexerStateMachine('int *x; *x;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfTypeValid(token[0])
        except SyntaxError as e:
            self.fail('Should not raise')

if __name__ == '__main__':
    unittest.main()
