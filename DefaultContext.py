from Context import *
from ContextManager import *

class DefaultContext(Context):
    def addKeyword(self, id):
        symClass = self.symbol(id)
        return symClass

    def symbol(self, id, bindingPower = 0, Type = True):
        if id not in self.symbolTable:
            class Symbol(SymbolBase):
                def __init__(self):
                    self.data = []
            symClass = Symbol
            symClass.id = id
            symClass.bindingPower = bindingPower
            symClass.left = Type
            symClass.__repr__ = revealSelf
            self.symbolTable[id] = symClass
            return symClass
        else:
            raise SyntaxError('Keyword' ' "' + id + '" ' + 'should not be here')