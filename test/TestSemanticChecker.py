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
        types = semanticChecker.getIdentifierDeclarationTypeList(declToken)
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
        types = semanticChecker.getIdentifierDeclarationTypeList(declToken)
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
            self.assertEqual("Error[1][1]:'x' is not declared" + '\n' +
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
            self.assertEqual("Error[3][9]:'y' is not declared" + '\n' +
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
            self.assertEqual("Error[3][9]:'y' is not declared" + '\n' +
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
            self.assertEqual("Error[1][9]:'y' is not declared" + '\n' +
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
            semanticChecker.checkIfTokenTypeValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[1][9]:Invalid type of 'x'" + '\n' +
                             'int x; *x;' + '\n' +
                             '        ^', e.msg)

    def test_isAllDefined_should_not_raise_given_x_is_compatible_to_y_plus_z(self):
        lexer = LexerStateMachine('int *x, *y, *z; x = y + z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
        except SyntaxError as e:
            self.fail('Should not raise')

    def test_isAllDefined_should_raise_given_z_has_invalid_type_in_a_statement(self):
        lexer = LexerStateMachine('int *x, *y, *z;\nx = y + **z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[2][11]:Invalid type of 'z'" + '\n' +
                             'x = y + **z;' + '\n' +
                             '          ^', e.msg)

    def test_isAllDefined_should_raise_given_x_is_not_compatible_to_y_plus_z(self):
        lexer = LexerStateMachine('int *x, *y, *z;\n*x = y + z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[2][4]:Incompatible assignment" + '\n' +
                             '*x = y + z;' + '\n' +
                             '   ^', e.msg)

    def test_checkIfAssignmentValid_should_not_raise_given_the_highest_pointer_level_of_rvalue_equal_pointer_level_of_lvalue(self):
        lexer = LexerStateMachine('int *x, *y, *z;\nx = y + *z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
        except SyntaxError as e:
            self.fail('Should not raise')

    def test_checkIfAssignmentValid_should_raise_given_pointer_level_of_rvalue_is_2_pointer_level_of_lvalue_is_1(self):
        lexer = LexerStateMachine('int *x, *y, *z;\nx = y + &z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[2][3]:Incompatible assignment" + '\n' +
                             'x = y + &z;' + '\n' +
                             '  ^', e.msg)

    def test_checkIfAssignmentValid_should_raise_given_addressof_lvalue_of_assignment(self):
        # addressof = &
        lexer = LexerStateMachine('int *x, *y, *z;\n&x = &y + &z;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[2][4]:Invalid lvalue in assignment" + '\n' +
                             '&x = &y + &z;' + '\n' +
                             '   ^', e.msg)

    def test_checkIfAssignmentValid_should_not_raise_given_assigning_addressof_y_to_a_pointer(self):
        # addressof = &
        lexer = LexerStateMachine('int *x, y;\nx = &y;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
        except SyntaxError as e:
            self.fail('Should not raise')

    def test_checkIfAssignmentValid_should_raise_given_assigning_addressof_5_to_a_pointer(self):
        # addressof = &
        lexer = LexerStateMachine('int *x;\nx = &5;', self.context)
        parser = Parser(lexer, self.contextManager)
        self.contextManager.setParser(parser)
        semanticChecker = SemanticChecker(parser.scopeBuilder)
        try:
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            token = parser.parseStatement(0)
            semanticChecker.checkIfAllIdentifiersAreDefined(token[0])
            semanticChecker.checkIfAllTokenTypeValid(token[0])
            semanticChecker.checkIfAssignmentValid(token[0])
            self.fail('Should raise')
        except SyntaxError as e:
            self.assertEqual("Error[2][4]:(literal) do not have address" + '\n' +
                             'x = &5' + '\n' +
                             '     ^', e.msg)

if __name__ == '__main__':
    unittest.main()
