import unittest

import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from ContextManager import *
from DefaultContext import *
from DeclarationContext import *
from ExpressionContext import *
from FlowControlContext import *

class TestContextManager(unittest.TestCase):
    def setUp(self):
        self.manager = ContextManager()
        self.expression = ExpressionContext(self.manager)
        self.flowControl = FlowControlContext(self.manager)

    def test_context_manager_function_should_work_properly(self):
        self.manager.addContext('Expression', self.expression)
        self.manager.addContext('FlowControl', self.flowControl)
        self.assertIn(self.expression, self.manager.contexts.values())
        self.assertIn(self.flowControl, self.manager.contexts.values())

        self.assertEqual(self.expression, self.manager.getContext('Expression'))
        self.assertEqual(self.flowControl, self.manager.getContext('FlowControl'))

        self.manager.setCurrentContexts(self.expression)
        self.assertEqual(self.expression, self.manager.getCurrentContexts())
        self.manager.setCurrentContexts([self.expression, self.flowControl])
        self.assertEqual([self.expression, self.flowControl], self.manager.getCurrentContexts())

    def test_setCurrentContexts_should_take_in_contextName_and_add_into_currentContexts(self):
        self.manager.addContext('Expression', self.expression)
        self.manager.addContext('FlowControl', self.flowControl)
        self.manager.setCurrentContextsByName('Expression', 'FlowControl')
        self.assertEqual([self.expression, self.flowControl], self.manager.currentContexts)
        self.manager.setCurrentContextsByName('Expression')
        self.assertEqual([self.expression], self.manager.currentContexts)

    def test_popContexts_from_contextsStack(self):
        self.manager.contextsStack = [[self.expression, self.flowControl], [self.expression]]
        returnedContext = self.manager.popContexts()
        self.assertEqual([self.expression], returnedContext)

    def test_pushContexts_into_contextsStack(self):
        self.manager.contextsStack = [[self.expression]]
        self.manager.pushContexts([self.expression, self.flowControl])
        self.assertEqual([[self.expression], [self.expression, self.flowControl]], self.manager.contextsStack)

    def test_pushCurrentContexts_into_contextsStack(self):
        self.manager.contextsStack = [[self.expression]]
        self.manager.currentContexts = [self.expression, self.flowControl]
        self.manager.pushCurrentContexts()
        self.assertEqual([[self.expression], [self.expression, self.flowControl]], self.manager.contextsStack)

    def test_popContexts_should_raise_overflow_error_given_contextsStack_is_empty(self):
        self.manager.contextsStack = []
        self.assertRaises(RuntimeError, self.manager.popContexts)

if __name__ == '__main__':
    unittest.main()