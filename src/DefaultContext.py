from Context import *
from ContextManager import *

class DefaultContext(Context):
    def __init__(self, contextManager):
        Context.__init__(self, contextManager)
        self.addOperator(',', 0)
        self.addOperator('*', 0)
        self.addOperator('+', 0)
        self.addOperator('-', 0)
        self.addOperator('++', 0)
        self.addOperator('--', 0)
        self.addOperator('if', 0)
        self.addOperator('while', 0)

    def addOperator(self, id, bindingPower = 0, nud = None, led = None):
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
