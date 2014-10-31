def revealSelf(self):
    return '{0} {1}'.format(self.id, self.data)

class SymbolBase:
    def led(self):
        raise SyntaxError('No led(.) function defined!')
    def nud(self):
        raise SyntaxError('No nud(.) function defined!')

class Context:
    PREFIX_UNARY = 1
    POSTFIX_UNARY = 2
    BINARY = 3
    def __init__(self):
        self.symbolTable = {}

    def setParser(self, parser):
        self.parser = parser

    def symbol(self, id, bindingPower = 0, Type = True):
        if id not in self.symbolTable:
            class Symbol(SymbolBase):
                def __init__(self):
                    self.data = []

            symClass = Symbol
            symClass.id = id
            symClass.left = Type
            symClass.bindingPower = bindingPower
            symClass.__repr__ = revealSelf
            self.symbolTable[id] = symClass
            return symClass
        else:
            return self.symbolTable[id]

    def addOperator(self, id, bindingPower = 0):
        symClass = self.symbol(id)
        symClass.bindingPower = bindingPower
        #symClass.nud = self.nud
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
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id)
        symClass.arity = self.BINARY
        symClass.bindingPower = bindingPower
        #symClass.nud = self.nud
        symClass.led = led
        return symClass

    def addPostfixOperator(self, id, bindingPower = 0):
        thisContext = self
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.parser.lexer.advance()
            return self
        symClass = self.symbol(id)
        symClass.arity = self.POSTFIX_UNARY
        symClass.bindingPower = bindingPower
        #symClass.nud = self.nud
        symClass.led = led
        return symClass

    def addPrefixOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id)
        symClass.arity = self.PREFIX_UNARY
        symClass.bindingPower = bindingPower
        symClass.nud = nud
        return symClass

    def addPrefixInfixOperator(self, id, infixBindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.prefixBindingPower)
            self.data.append(returnedToken)
            return self
        sym = self.addInfixOperator(id, infixBindingPower)
        sym.prefixBindingPower = 120
        sym.nud = nud


    def prefixNud(self):
        pass

    def perfixLed(self, leftToken = None):
        return self

    def createLiteral(self, value):
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance()
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
            thisContext.parser.lexer.advance()
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
            thisContext.parser.lexer.advance()
            return self
        sym = self.symbol('(systemToken)')
        sym.arity = None
        sym.__repr__ = revealSelf
        sym.nud = nud
        symObj = sym()
        symObj.data.append(value)
        return symObj

    def createToken(self, word):
        if word is None:
            return self.createSystemToken('(end)')
        elif word.isidentifier():
            return self.createIdentifier(word)
        elif word.isnumeric():
            return self.createLiteral(word)
        else:
            symClass = self.symbol(word)
            if symClass is not None:
                return symClass()
            else:
                raise SyntaxError('Syntax error: \'{0}\' is an unknown token'.format(word))