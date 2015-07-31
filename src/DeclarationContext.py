__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *

class DeclarationContext(Context):
    def __init__(self, *args, **kwargs):
        super(DeclarationContext, self).__init__(*args, **kwargs)
        self.modifier = []
        self.modifierCount = 0
        self.primitiveCount = 0

    def createDeclarationAndDefinitionToken(self):
        sym = self.symbol('(declaration&definition)')
        sym.arity = None
        sym.__repr__ = revealSelf
        symObj = sym()
        return symObj

    def addPointer(self, id, bindingPower):  # *
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            if thisContext.getIdentifier(returnedToken) is None:
                raise SyntaxError('expect identifier before here')
            self.data.append(returnedToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addSubscript(self, id, bindingPower):  # []
        thisContext = self
        def nud(self):
            raise SyntaxError("expected expression before '[' token")  # error handling
        def led(self, leftToken):
            self.data.append(leftToken)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(']')
            thisContext.contextManager.parser.lexer.advance()
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addInt(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = None
            self.sign = None
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                expressionToken = thisContext.contextManager.parser.parse(0)
                self.identifierList.append(thisContext.getIdentifier(expressionToken))
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'short':
                self.modifier = 'short'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'long':
                self.modifier = 'long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'short':
                    self.modifier = 'short'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'long':
                    self.modifier = 'long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken

        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addSignedAndUnsigned(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = None
            self.sign = self.id
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                expressionToken = thisContext.contextManager.parser.parse(0)
                self.identifierList.append(thisContext.getIdentifier(expressionToken))
                self.expressionList.append(expressionToken)

            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'short':
                    self.modifier = 'short'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'long':
                    self.modifier = 'long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'long':
                self.modifier = 'long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id == 'short':
                self.modifier = 'short'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:  # Deal with assignment or comma in declaration statement
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addLong(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'long'
            self.sign = None
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()

            if nextToken.id in ('(identifier)', '*', '('):
                expressionToken = thisContext.contextManager.parser.parse(0)
                self.identifierList.append(thisContext.getIdentifier(expressionToken))
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'long':
                self.modifier = 'long long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken

            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id in ('(identifier)', '*', '('):
                            expressionToken = thisContext.contextManager.parser.parse(0)
                            self.identifierList.append(thisContext.getIdentifier(expressionToken))
                            self.expressionList.append(expressionToken)
                        elif nextToken.id in ('signed', 'unsigned'):
                            self.sign = nextToken.id
                            nextToken = thisContext.contextManager.parser.lexer.advance()
                            if nextToken.id in ('(identifier)', '*', '('):
                                expressionToken = thisContext.contextManager.parser.parse(0)
                                self.identifierList.append(thisContext.getIdentifier(expressionToken))
                                self.expressionList.append(expressionToken)
                            else:
                                self.errorToken = nextToken
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken

        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addShort(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'short'
            self.sign = None
            self.identifierList = []
            self.expressionList = []
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id in ('(identifier)', '*', '('):
                expressionToken = thisContext.contextManager.parser.parse(0)
                self.identifierList.append(thisContext.getIdentifier(expressionToken))
                self.expressionList.append(expressionToken)
            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                        self.errorToken = nextToken

            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id in ('(identifier)', '*', '('):
                        expressionToken = thisContext.contextManager.parser.parse(0)
                        self.identifierList.append(thisContext.getIdentifier(expressionToken))
                        self.expressionList.append(expressionToken)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken

            else:
                self.errorToken = nextToken

            while True:
                nextToken = thisContext.contextManager.parser.lexer.peep()
                if nextToken.id != ',':
                    break
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id in ('(identifier)', '*', '('):
                    expressionToken = thisContext.contextManager.parser.parse(0)
                    self.identifierList.append(thisContext.getIdentifier(expressionToken))
                    self.expressionList.append(expressionToken)
                else:
                    self.errorToken = nextToken
            ddToken = thisContext.buildToken(self)
            return ddToken

        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def getIdentifier(self, token):
        if token.id == '(identifier)':
            return token
        else:
            while hasattr(token, 'data') and token.data[0] is not False:
                token = token.data[0]
                if hasattr(token, 'id') and token.id == '(identifier)':  # check does token.id exists
                    return token
            return None  # no identifier found

    def handleError(self, token):
        if token.errorToken.id in (';', '(systemToken)'):
            raise SyntaxError('Expecting (identifier) before ' + token.errorToken.id)
        elif token.errorToken.id in (token.sign, token.modifier, token.primitive):
            raise SyntaxError('Duplication of ' + "'" + token.errorToken.id + "'" + ' in declaration statement')
        elif token.errorToken.id in ('short', 'long'):
            raise SyntaxError("Cannot have both 'short' and 'long' in declaration statement")
        elif token.errorToken.id in ('unsigned', 'signed'):
            raise SyntaxError("Cannot have both 'signed' and 'unsigned' in this declaration statement")
        else:
            raise SyntaxError(token.errorToken.id + " causes error")

    def buildToken(self, token):
        if token.errorToken is not None:
            self.handleError(token)
        ddToken = self.createDeclarationAndDefinitionToken()
        for identifier, expression in zip(token.identifierList, token.expressionList):  # zip used to loop 2 list in one time
            primitiveToken = self.createToken(token.primitive)
            primitiveToken.modifier = []
            primitiveToken.sign = token.sign
            primitiveToken.modifier = token.modifier
            ddToken.data.append(primitiveToken)
            if expression.id == '=':
                primitiveToken.data.append(identifier)
                ddToken.data.append(expression)
            elif expression.id in ('(identifier)', '*', '(', '['):
                primitiveToken.data.append(expression)
            else:
                raise SyntaxError
        return ddToken

"""
    def addPointerDeclaration(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        # symClass.led = led
        return symClass
        pass


    def addPrimitive(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.ruleCheck(self)
            return
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def addModifier(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.ruleCheck(self)
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def ruleCheck(self, token):
        if token.type == 'modifier':
            self.modifier.append(token.id)
            self.modifierCount += 1
        elif token.type == 'primitive':
            self.primitiveCount += 1
        return
"""

"""
        elif firstToken.id == 'int':

            firstToken = deepcopy(secondToken)
            identifierName = self.lexer.advance()
            firstToken.data.append(identifierName)
            list.append(firstToken)
            if self.lexer.peep().id != '(systemToken)':
                tempToken =self.lexer.peep()
                returnedToken = self.parse(bindingPower)
                if returnedToken.id != tempToken.id:
                    list.append(returnedToken)

            while self.lexer.peep().id == ',':
                firstToken = deepcopy(secondToken)
                identifierName = self.lexer.advance()
                firstToken.data.append(identifierName)
                list.append(firstToken)
                if self.lexer.peep().id != '(systemToken)':
                    tempToken =self.lexer.peep()
                    returnedToken = self.parse(bindingPower)
                    if returnedToken.id != tempToken.id:
                        list.append(returnedToken)
            return list
"""
