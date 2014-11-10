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

    def symbol(self, id, bindingPower = 0):
        if id not in self.symbolTable:
            class Symbol(SymbolBase):
                def __init__(self):
                    self.data = []

            symClass = Symbol
            symClass.id = id
            symClass.bindingPower = bindingPower
            symClass.__repr__ = revealSelf
            self.symbolTable[id] = symClass
            return symClass
        else:
            return self.symbolTable[id]

    #The following function is to add the relevant function into the context for
    def addOperator(self, id, bindingPower=0, nud=None, led=None):
        symClass = self.symbol(id,bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addInfixOperator(self, id, bindingPower = 0):
        thisContext = self
        def led(self, leftToken):
            thisContext.parser.lexer.advance()
            self.data.append(leftToken)
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        def nud(self):
            thisContext.parser.lexer.advance()
            return self

        symClass = self.symbol(id, bindingPower)
        symClass.arity = self.BINARY
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addPostfixOperator(self, id, bindingPower = 0):
        thisContext = self
        def led(self, leftToken):
            thisContext.parser.lexer.advance()
            self.data.append(leftToken)
            return self
        def nud(self):
            thisContext.parser.lexer.advance()
            return self

        symClass = self.symbol(id,bindingPower)
        symClass.arity = self.POSTFIX_UNARY
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addPrefixOperator(self, id, bindingPower = 0):
        thisContext = self
        symClass = self.symbol(id,bindingPower)
        symClass.arity = self.PREFIX_UNARY
        def led(self):
            return self

        def nud(self):
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self

        symClass.nud = nud
        symClass.led = led
        return symClass

    def addInfixPrefixOperator(self, id, bindingPower = 0):
        thisContext = self
        symClass = self.addInfixOperator(id,bindingPower)

        def nud(self):
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(120)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id,bindingPower)
        symClass.arity = self.PREFIX_UNARY
        symClass.nud = nud
        return symClass


    #The following function is used to create a token when createToken() is been called.
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
        #sym.nud = nud
        symObj = sym()
        symObj.data.append(value)
        return symObj

    #This function is use to determine which function should be used to create a token.
    def createToken(self, word):
        if word is None:
            return self.createSystemToken('(end)')
        elif word.isnumeric():
            return self.createLiteral(word)
        elif word in self.symbolTable:
            symClass = self.symbol(word)
            return symClass()
        elif word.isidentifier():
            return self.createIdentifier(word)

    #The following function is use in expression context.
    def addBlockOperator(self,id,bindingPower = 0 ):
        thisContext = self
        symClass = self.symbol(id,bindingPower)
        def led(self):
            return self

        def nud(self):
            returnedToken =None
            nextToken = thisContext.parser.lexer.advance()
            if(nextToken.id== ';'):
                nextToken = thisContext.parser.lexer.advance()
            while(nextToken.id != '}'):
                returnedToken = thisContext.parser.parse(self.bindingPower)
                self.data.append(returnedToken)
                nextToken = thisContext.parser.lexer.advance()

            thisContext.parser.lexer.advance()
            return self

        symClass.nud = nud
        symClass.led = led
        return symClass

    def addGroupOperator(self, id, bindingPower = 0): #for bracket ( and )
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            if thisContext.parser.lexer.peep().id == ')':
                thisContext.parser.lexer.advance()
            return self
        def led(self, leftToken):
            thisContext.parser.lexer.advance()
            return self
        symClass = self.symbol(id,bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    #The following is use for flow control
    def addControl(self,id,bindingPower=0):
        thisContext = self
        def nud(self):
            thisContext.parser.lexer.advance('(')
            thisContext.parser.lexer.advance()
            returnedToken = thisContext.parser.parse(bindingPower)
            self.data.append(returnedToken)
            thisContext.parser.lexer.advance('{')
            returnedToken = thisContext.parser.parse(bindingPower)
            self.data.append(returnedToken)
            returnedToken = thisContext.parser.lexer.peep()
            if (returnedToken.id == 'else'):
                thisContext.parser.lexer.advance('{')
                returnedToken.data.append(thisContext.parser.parse(bindingPower))
                self.data.append(returnedToken)
            return self
        def led(self, leftToken):
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
