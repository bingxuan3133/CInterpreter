def revealSelf(self):
    return '{0} {1}'.format(self.id, self.data)


class SymbolBase:
    def led(self):
        raise SyntaxError('No led(.) function defined!')

    def nud(self):
        raise SyntaxError('No nud(.) function defined!')

    def generateByteCode(self):
        raise SyntaxError('No generation function defined!')


class Context:
    PREFIX_UNARY = 1
    POSTFIX_UNARY = 2
    BINARY = 3

    def __init__(self, contextManager):
        self.symbolTable = {}
        self.contextManager = contextManager

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
            return self.symbolTable[id]

    def addOperator(self, id, bindingPower = 0, nud = None, led = None):
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def createLiteral(self, value):
        thisContext = self

        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.symbol('(literal)')
        sym.arity = None
        sym.__repr__ = revealSelf
        sym.nud = nud
        symObj = sym()
        symObj.data.append(int(value))
        return symObj

    def createIdentifier(self, value):
        thisContext = self

        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.symbol('(identifier)')
        sym.content = None
        sym.arity = None
        sym.type = 'name'
        sym.__repr__ = revealSelf
        sym.nud = nud
        symObj = sym()
        symObj.data.append(value)
        return symObj

    def createSystemToken(self, value):
        thisContext = self

        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.symbol('(systemToken)')
        sym.arity = None
        sym.__repr__ = revealSelf
        sym.nud = nud
        symObj = sym()
        symObj.data.append(value)
        return symObj

    def createFloatingPoint(self, value):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            return self

        sym = self.symbol('(floating)')
        sym.arity = None
        sym.__repr__ = revealSelf
        sym.nud = nud
        symObj = sym()
        symObj.data.append(float(value))
        return symObj

    def createToken(self, word, line=0, column=0, length =0, originalString=""):
        for currentContext in self.contextManager.currentContexts:
            if word in currentContext.symbolTable:
                symClass = currentContext.symbol(word)
                if symClass is not None:
                    newToken = symClass()
                    newToken.line = line
                    newToken.column = column - length
                    newToken.length = length
                    newToken.oriString = originalString
                    return newToken

        if word is None:
            newToken = self.createSystemToken('(end)')
        elif word.isidentifier():
            newToken = self.createIdentifier(word)
        elif word.isnumeric():
            newToken = self.createLiteral(word)
        elif self.isFloat(word):
            newToken = self.createFloatingPoint(word)
        else:
            raise SyntaxError('Syntax error: [' + word + '] is an unknown token')
        newToken.line = line
        newToken.column = column - length
        newToken.length = length
        newToken.oriString = originalString
        return newToken

    def isFloat(self, Unknown):
        try:
            float(Unknown)
            return True
        except:
            return False
