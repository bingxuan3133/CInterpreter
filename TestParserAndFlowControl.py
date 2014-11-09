import unittest
from Context import *
from ExpressionContext import *
from FlowControlContext import *
from Parser import *
from ContextManager import *

class TestParseFlowControl(unittest.TestCase):
    def test_parse_while_1(self):
        manager = ContextManager()
        context = Context(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext, flowControlContext]

        flowControlContext.addFlowControlOperator('while', 0)
        expressionContext.addPrefixGroupOperator('(', 0)
        expressionContext.addPrefixGroupOperator(')', 0)

        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('while ( 1 )', manager.currentContexts)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])

    def test_parse_while_1_while_1(self):
        manager = ContextManager()
        context = Context(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext, flowControlContext]

        flowControlContext.addFlowControlOperator('while', 0)
        expressionContext.addPrefixGroupOperator('(', 0)
        expressionContext.addPrefixGroupOperator(')', 0)

        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('while ( 1 ) while ( 1 )', manager.currentContexts)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('while', token.data[1].id)
        self.assertEqual('(literal)', token.data[1].data[0].id)
        self.assertEqual(1, token.data[1].data[0].data[0])

    def test_parse_while_1_do_something(self):
        manager = ContextManager()
        context = Context(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext, flowControlContext]

        flowControlContext.addFlowControlOperator('while', 0)
        expressionContext.addPrefixGroupOperator('(', 0)
        expressionContext.addPrefixGroupOperator(')', 0)
        expressionContext.addPostfixOperator('++', 150)

        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('while ( 1 ) i ++', manager.currentContexts)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        token = parser.parse(0)

        self.assertEqual('while', token.id)
        self.assertEqual('(literal)', token.data[0].id)
        self.assertEqual(1, token.data[0].data[0])
        self.assertEqual('++', token.data[1].id)
        self.assertEqual('(identifier)', token.data[1].data[0].id)
        self.assertEqual('i', token.data[1].data[0].data[0])


    def test_parse_while_while_1_should_raise_an_error(self):
        manager = ContextManager()
        context = Context(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext, flowControlContext]

        flowControlContext.addFlowControlOperator('while', 0)
        expressionContext.addPrefixGroupOperator('(', 0)
        expressionContext.addPrefixGroupOperator(')', 0)

        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('while ( while ( 1 ) )', manager.currentContexts)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)

    def test_parse_while_1_without_closing_bracket_should_raise_an_error(self):
        manager = ContextManager()
        context = Context(manager)
        flowControlContext = FlowControlContext(manager)
        expressionContext = ExpressionContext(manager)
        contexts = [expressionContext, flowControlContext]

        flowControlContext.addFlowControlOperator('while', 0)
        expressionContext.addPrefixGroupOperator('(', 0)
        expressionContext.addPrefixGroupOperator(')', 0)

        manager.addContext('FlowControl', flowControlContext)
        manager.addContext('Expression', expressionContext)
        manager.setContexts(contexts)

        lexer = Lexer('while ( 1', manager.currentContexts)
        parser = Parser(lexer, contexts)
        manager.setParser(parser)

        self.assertRaises(SyntaxError, parser.parse, 0)

if __name__ == '__main__':
    unittest.main()