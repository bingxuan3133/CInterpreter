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

class MyTestCase(unittest.TestCase):
    def test_default_context(self):
        manager = ContextManager()
        context = Context(manager)
        default = DefaultContext(manager)
        default.addKeyword('if')
        default.addKeyword('while')
        manager.setCurrentContexts([default])
        self.assertRaises(SyntaxError, Lexer, 'if', context)  # lexer = Lexer('if', context)
        lexer = Lexer('123 if', context)
        self.assertRaises(SyntaxError, lexer.advance)   # lexer.advance()

if __name__ == '__main__':
    unittest.main()
