__author__ = 'admin'

import unittest
from SemanticChecker import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.context = Context(self.manager)
        self.defaultContext = DefaultContext(self.manager)
        self.defaultContext.addKeyword('int')
        self.declarationContext = DeclarationContext(self.manager)
        self.declarationContext.addInt('int', 0)
        self.declarationContext.addPointer('*', 0)
        self.expressionContext = ExpressionContext(self.manager)
        self.flowControlContext = FlowControlContext(self.manager)
        self.expressionContext.addOperator(';', 0)
        self.expressionContext.addInfixOperator('=', 20)
        self.expressionContext.addInfixOperator('+', 70)
        self.expressionContext.addInfixOperator('-', 70)
        self.flowControlContext.addBlockOperator('{', 0)
        self.flowControlContext.addOperator('}', 0)
        self.contexts = [self.declarationContext, self.expressionContext, self.flowControlContext, self.defaultContext]
        self.manager.addContext('Default', self.defaultContext)
        self.manager.addContext('Declaration', self.declarationContext)
        self.manager.addContext('Expression', self.expressionContext)
        self.manager.addContext('FlowControl', self.flowControlContext)
        self.manager.setCurrentContexts(self.contexts)

    def test_getIdentifierType(self):
        declToken = self.declarationContext.createDeclarationOrDefinitionToken('(decl)')
        intToken = self.context.createToken('int')
        xToken = self.context.createToken('x')
        declToken.data.append(intToken)
        declToken.data.append(xToken)

        semanticChecker = SemanticChecker()
        types = semanticChecker.getIdentifierType(declToken)

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
        types = semanticChecker.getIdentifierType(declToken)

        self.assertEqual(['int', '*'], types)


if __name__ == '__main__':
    unittest.main()
