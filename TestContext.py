import unittest
from Context import *


class MyTestCase(unittest.TestCase):
    def testCreateInfixOperator(self):
        context = Context()
        addClass = context.addInfixOperator('+', 70)
        subClass = context.addInfixOperator('-', 70)
        self.assertEqual(context.symbolTable['+'], addClass)
        self.assertEqual(context.symbolTable['-'], subClass)

    def testCreatePrefixOperator(self):
        context = Context()
        addClass = context.addPrefixOperator('+', 200)
        subClass = context.addPrefixOperator('-', 200)
        self.assertEqual(context.symbolTable['+'], addClass)
        self.assertEqual(context.symbolTable['-'], subClass)

    def test_(self):
        pass

if __name__ == '__main__':
    unittest.main()
