import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from ExpressionContext import *
from ContextManager import *

class MyTestCase(unittest.TestCase):
    def testCreateInfixOperator(self):
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        addClass = expressionContext.addInfixOperator('+', 70)
        subClass = expressionContext.addInfixOperator('-', 70)
        self.assertEqual(expressionContext .symbolTable['+'], addClass)
        self.assertEqual(expressionContext.symbolTable['-'], subClass)

    def testCreatePrefixOperator(self):
        manager = ContextManager()
        context = Context(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext]

        addClass = expressionContext.addPrefixOperator('+', 200)
        subClass = expressionContext.addPrefixOperator('-', 200)
        self.assertEqual(expressionContext.symbolTable['+'], addClass)
        self.assertEqual(expressionContext.symbolTable['-'], subClass)

    def test_(self):
        pass

if __name__ == '__main__':
    unittest.main()
