from Context import *
from ContextManager import *

class DefaultContext(Context):
    def addAllOperators(self):
        self.addOperator(';', 200)
        self.addOperator('+', 200)
        self.addOperator('-', 200)
        self.addOperator('++', 200)
        self.addOperator('--', 200)

    def addOperator(self, id, bindingPower = 0, nud = None, led = None):
        thisContext = self
        def nud(self):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Do not expect {} here\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
        def led(self, token):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Do not expect {} here\n{}\n{}"\
                             .format(self.line,self.column,self.oriString,caretMessage))
        symClass = self.symbol(id)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addKeyword(self, id):
        def nud(self):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Do not expect {} here\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
        def led(self, token):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Do not expect {} here\n{}\n{}"\
                             .format(self.line,self.column,self.oriString,caretMessage))
        symClass = self.symbol(id)
        symClass.nud = nud
        symClass.led = led
        return symClass
