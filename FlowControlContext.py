from Context import *
from ContextManager import *

class FlowControlContext(Context):
    def addFlowControlOperator(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance('(')
            context = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setContexts([context])               # Will be implement as push into stack later
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(')')
            context2 = thisContext.contextManager.getContext('FlowControl')
            thisContext.contextManager.setContexts([context, context2])     # Will be implement as pop from stack later
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id)
        symClass.bindingPower = bindingPower
        symClass.nud = nud
        symClass.led = led
        return symClass
