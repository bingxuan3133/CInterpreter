from Context import *
import Error

class ExpressionContext(Context):
    def __init__(self, contextManeger):
        Context.__init__(self, contextManeger)
        self.addPrefixInfixOperator('+', 70)
        self.addPrefixInfixOperator('-', 70)
        self.addPrefixInfixOperator('*', 100)
        self.addByReferenceOperator('&', 100)
        self.addInfixOperator('/', 100)
        self.addInfixOperator('%', 100)
        self.addInfixOperator('=', 1)
        self.addInfixOperator('!=', 25)
        self.addInfixOperator('|', 15)
        self.addInfixOperator('||', 5)
        self.addInfixOperator('&&', 6)
        self.addInfixOperator('==', 10)
        self.addInfixOperator('<', 10)
        self.addInfixOperator('<=', 10)
        self.addInfixOperator('>', 10)
        self.addInfixOperator('>=', 10)
        self.addPostfixOperator('++', 150)
        self.addPostfixOperator('--', 150)

        self.addGroupOperator('(', 0)
        self.addBlockOperator('{', 0)
        self.addOperator(',', 0)
        self.addOperator(';', 0)
        self.addOperator('}', 0)
        self.addOperator(')', 0)

        self.addPrintOperator('print', 0)

    def addInfixOperator(self, id, bindingPower = 0):
        """
        Add Infix operator into symbol table
        :param id:
        :param bindingPower:
        :return:
        """
        thisContext = self
        def nud(self):
            raise SyntaxError(Error.generateErrorMessageWithOneArguement('Expect (literal) or (identifier) before {}', self, self.id))
        def led(self, leftToken):
            self.arity = thisContext.BINARY  # some token has prefix and infix characteristic
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self

        symClass = self.symbol(id, bindingPower)
        symClass.arity = self.BINARY
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addPrefixOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self

        symClass = self.symbol(id, bindingPower)
        symClass.arity = self.PREFIX_UNARY
        symClass.nud = nud
        return symClass

    def addPostfixOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            raise SyntaxError(Error.generateErrorMessageWithNoArguement('Expect (identifier) before {}', self, self.id))
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            return self

        symClass = self.symbol(id, bindingPower)
        symClass.arity = self.POSTFIX_UNARY
        #symClass.nud = self.nud
        symClass.led = led
        return symClass

    def addPrefixInfixOperator(self, id, bindingPower = 0):
        thisContext = self
        symClass = self.addInfixOperator(id, bindingPower)
        def nud(self):
            self.arity = thisContext.PREFIX_UNARY
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(120)
            self.data.append(returnedToken)
            return self
        symClass.nud = nud
        return symClass

    def addByReferenceOperator(self, id, bindingPower = 0):
        thisContext = self
        symClass = self.addInfixOperator(id, 20)
        def nud(self):
            self.arity = thisContext.PREFIX_UNARY
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(120)
            idenToken = thisContext.getIdentifier(returnedToken)
            if idenToken is None:
                raise SyntaxError(Error.generateErrorMessageWithNoArguement('(literal) do not have address', returnedToken))
            self.data.append(returnedToken)
            return self
        symClass.nud = nud
        return symClass

    def addGroupOperator(self, id, bindingPower = 0):
        thisContext = self
        def nud(self):
            thisContext.contextManager.pushCurrentContexts()
            thisContext.contextManager.setCurrentContextsByName('Expression', 'Default')
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            thisContext.contextManager.popContexts()
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(')')
            thisContext.contextManager.parser.lexer.advance()
            return self
        def led(self, leftToken):
            thisContext.contextManager.parser.lexer.advance()
            return self
        sym = self.addOperator(id, bindingPower, nud, led)
        return sym

    def addBlockOperator(self, id, bindingPower = 0 ):
        thisContext = self
        def led(self):
            return self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedList = thisContext.contextManager.parser.parseStatements(bindingPower)
            self.data = returnedList
            thisContext.contextManager.parser.lexer.peep('}')
            thisContext.contextManager.parser.lexer.advance()
            return self
        symClass = self.addOperator(id, bindingPower)  # removed the nud and led
        symClass.nud = nud
        symClass.led = led
        return

    def addPrintOperator(self, id, bindingPower = 0 ):
        thisContext = self
        def nud(self):
            print(thisContext.contextManager.parser.lexer.advance())
            print(thisContext.contextManager.parser.lexer.peep('('))
            print(thisContext.contextManager.parser.lexer.advance())
            token = thisContext.contextManager.parser.parse(0)
            self.data.append(token)
            print(thisContext.contextManager.parser.lexer.peep(')'))
            print(thisContext.contextManager.parser.lexer.advance())
            return self
        def led(self):
            return self
        symClass = self.addOperator(id, bindingPower)  # removed the nud and led
        symClass.nud = nud
        symClass.led = led
        return

    def getIdentifier(self, token):
        """
        This is a helper function used to retrieve the identifier on the left most of an token tree
        :param token:
        :return: token  - identifier is found and return
                 None   - no identifier is found
        """
        if hasattr(token, 'id') and token.id == '(identifier)':
            return token
        else:
            if hasattr(token, 'data') and len(token.data) > 0:
                token = self.getIdentifier(token.data[0])
                return token
            else:
                return None