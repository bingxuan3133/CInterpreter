__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *

class DeclarationContext(Context):
    def createDeclarationOrDefinitionToken(self, word):
        sym = self.symbol(word)
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
                caretMessage = ' '*(returnedToken.column-1)+'^'
                raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(returnedToken.line,returnedToken.column,returnedToken.id,returnedToken.oriString,caretMessage))
            self.data.append(returnedToken)
            return self
        def led(self, token):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting ; before {}\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addSubscript(self, id, bindingPower):  # []
        thisContext = self
        def nud(self):
            caretMessage = ' '*(self.column-1)+'^'
            raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(self.line,self.column,self.id,self.oriString,caretMessage))
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
            self.sign = 'signed'
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
            self.sign = 'signed'
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
            self.sign = 'signed'
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
        while hasattr(token, 'data') and token.data[0] is not None:
            if hasattr(token, 'id') and token.id == '(identifier)':  # check does token.id exists
                return token
            token = token.data[0]
        return None  # no identifier found

    def removeIdentifier(self, token):
        if token.data[0].id == '(identifier)':
            token.data.remove(token.data[0])
        else:
            self.removeIdentifier(token.data[0])

    def handleError(self, token):
        caretMessage = ' '*(token.errorToken.column-1)+'^'
        if token.errorToken.id in (';', '(systemToken)'):
            raise SyntaxError("Error[{}][{}]:Expecting (identifier) before {}\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in (token.sign, token.modifier, token.primitive):
            raise SyntaxError("Error[{}][{}]:Duplication of '{}' in declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in ('short', 'long'):
            raise SyntaxError("Error[{}][{}]:Cannot have both 'short' and 'long' in declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.oriString,caretMessage))
        elif token.errorToken.id in ('unsigned', 'signed'):
            raise SyntaxError("Error[{}][{}]:Cannot have both 'signed' and 'unsigned' in this declaration statement\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.oriString,caretMessage))
        else:
            raise SyntaxError("Error[{}][{}]:{} causes error\n{}\n{}"\
                             .format(token.errorToken.line,token.errorToken.column,token.errorToken.id,token.errorToken.oriString,caretMessage))

    def buildToken(self, token):
        if token.errorToken is not None:
            self.handleError(token)
        multiple = self.createDeclarationOrDefinitionToken('(multiple)')  # (multiple) carry multiple tokens
        for identifier, expression in zip(token.identifierList, token.expressionList):  # zip used to loop 2 list in one time
            primitiveToken = self.createToken(token.primitive)
            primitiveToken.sign = token.sign
            primitiveToken.modifier = token.modifier
            declToken = self.createDeclarationOrDefinitionToken('(decl)')  # declaration token
            declToken.data.append(primitiveToken)
            if expression is None or expression.id in ('(identifier)', '*', '(', '['):
                primitiveToken.data.append(expression)
                self.removeIdentifier(primitiveToken)
                declToken.data.append(identifier)
                multiple.data.append(declToken)
            elif expression.id == '=':
                primitiveToken.data.append(expression.data[0])
                self.removeIdentifier(primitiveToken)
                declToken.data.append(identifier)
                defToken = self.createDeclarationOrDefinitionToken('(def)')  # definition token
                defToken.data.append(declToken)
                defToken.data.append(expression.data[1])  # get definition
                multiple.data.append(defToken)
            else:
                raise SyntaxError
        return multiple
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
