from Context import *
from ContextManager import *

class ExpressionContext(Context):
    def addOperator(self, id, bindingPower, nud, led):
        symClass = self.symbol(id)
        symClass.bindingPower = bindingPower
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addInfixOperator(self, id, bindingPower = 0):
        """
        Add Infix operator into symbol table
        :param id:
        :param bindingPower:
        :return:
        """
        thisContext = self
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id)
        symClass.arity = self.BINARY
        symClass.bindingPower = bindingPower
        #symClass.nud = self.nud
        symClass.led = led
        return symClass

    def addPrefixOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id)
        symClass.arity = self.PREFIX_UNARY
        symClass.bindingPower = bindingPower
        symClass.nud = nud
        return symClass

    def addPostfixOperator(self, id, bindingPower = 0):
        thisContext = self
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            return self
        symClass = self.symbol(id)
        symClass.arity = self.POSTFIX_UNARY
        symClass.bindingPower = bindingPower
        #symClass.nud = self.nud
        symClass.led = led
        return symClass

    def addPrefixInfixOperator(self, id, infixBindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.prefixBindingPower)
            self.data.append(returnedToken)
            return self
        sym = self.addInfixOperator(id, infixBindingPower)
        sym.prefixBindingPower = 120
        sym.nud = nud

    def addPrefixGroupOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(')')
            thisContext.contextManager.parser.lexer.advance()
            return self
        def led(self, leftToken):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.addOperator(id, bindingPower, nud, led)
        return sym