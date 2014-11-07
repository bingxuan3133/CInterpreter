from Context import *

class FlowControlContext(Context):
    def addFlowControlOperator(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance('(')
            thisContext.parser.contexts = [thisContext]
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.parser.lexer.peep(')')
            thisContext.parser.lexer.advance()
            return self
        def led(self):
            pass
        symClass = self.symbol(id)
        symClass.bindingPower = bindingPower
        symClass.nud = nud
        symClass.led = led
        return symClass