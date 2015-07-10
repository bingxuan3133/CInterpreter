__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *
from ContextManager import *
import copy

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

    def addIntDeclaration(self, id, bindingPower):
        thisContext = self
        def nud(self):
            ddToken = thisContext.createDeclarationAndDefinitionToken()
            ddToken.data = []
            identifierToken = thisContext.contextManager.parser.lexer.advance()
            while True:
                identifierToken = thisContext.contextManager.parser.lexer.peep()
                if identifierToken.id == 'int':
                    raise SyntaxError('2 or more data types in declaration')
                elif identifierToken.id != '(identifier)':
                    raise SyntaxError('expect identifier before ' + identifierToken.id)
                self.data.append(identifierToken)
                expressionToken = thisContext.contextManager.parser.parse(0)
                ddToken.data.append(copy.copy(self))
                self.data = []
                if expressionToken.id != identifierToken.id:  # mean that the tree contain assignment statements
                    ddToken.data.append(expressionToken)
                testToken = thisContext.contextManager.parser.lexer.peep()
                if testToken.id != ',':
                    break
                thisContext.contextManager.parser.lexer.advance()
            return ddToken
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

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

    def addInt(self, id, bindingPower):
        thisContext = self
        def nud(self):
            pass
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.type = 'modifier'
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def addSignedAndUnsigned(self, id, bindingPower):
        thisContext = self
        def nud(self):
            pass
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.type = 'modifier'
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def addLong(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'long'
            self.sign = None
            self.identifier = None
            self.expressionToken = None
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id == '(identifier)':
                self.identifier = nextToken
                self.expressionToken = thisContext.contextManager.parser.parse(0)
            elif nextToken.id == 'long':
                self.modifier = 'long long'
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id == '(identifier)':
                    self.identifier = nextToken
                    self.expressionToken = thisContext.contextManager.parser.parse(0)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        else:
                            raise SyntaxError
                    else:
                        raise SyntaxError
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        else:
                            raise SyntaxError
                    else:
                        raise SyntaxError
            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id == '(identifier)':
                    self.identifier = nextToken
                    self.expressionToken = thisContext.contextManager.parser.parse(0)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id in ('signed', 'unsigned'):
                        self.sign = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken
            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id == '(identifier)':
                    self.identifier = nextToken
                    self.expressionToken = thisContext.contextManager.parser.parse(0)
                elif nextToken.id == 'long':
                    self.modifier = 'long long'
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id == 'int':
                        self.primitive = nextToken.id
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        else:
                            self.errorToken = nextToken
                    else:
                        self.errorToken = nextToken
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    elif nextToken.id == 'long':
                        self.modifier = 'long long'
                        nextToken = thisContext.contextManager.parser.lexer.advance()
                        if nextToken.id == '(identifier)':
                            self.identifier = nextToken
                            self.expressionToken = thisContext.contextManager.parser.parse(0)
                        elif nextToken.id in ('signed', 'unsigned'):
                            self.sign = nextToken.id
                            nextToken = thisContext.contextManager.parser.lexer.advance()
                            if nextToken.id == '(identifier)':
                                self.identifier = nextToken
                                self.expressionToken = thisContext.contextManager.parser.parse(0)
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
            ddToken = thisContext.buildToken(self)
            return ddToken
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.type = 'modifier'
        symClass.nud = nud
        symClass.led = led
        return symClass
        pass

    def addShort(self, id, bindingPower):
        thisContext = self
        def nud(self):
            self.primitive = 'int'
            self.modifier = 'short'
            self.sign = None
            self.identifier = None
            self.expressionToken = None
            self.errorToken = None  # token that causes error

            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id == '(identifier)':
                self.identifier = nextToken
                self.expressionToken = thisContext.contextManager.parser.parse(0)
            elif nextToken.id == 'int':
                self.primitive = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id == '(identifier)':
                    self.identifier = nextToken
                    self.expressionToken = thisContext.contextManager.parser.parse(0)
                elif nextToken.id in ('signed', 'unsigned'):
                    self.sign = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    else:
                        self.errorToken = nextToken
                else:
                        self.errorToken = nextToken
            elif nextToken.id in ('signed', 'unsigned'):
                self.sign = nextToken.id
                nextToken = thisContext.contextManager.parser.lexer.advance()
                if nextToken.id == '(identifier)':
                    self.identifier = nextToken
                    self.expressionToken = thisContext.contextManager.parser.parse(0)
                elif nextToken.id == 'int':
                    self.primitive = nextToken.id
                    nextToken = thisContext.contextManager.parser.lexer.advance()
                    if nextToken.id == '(identifier)':
                        self.identifier = nextToken
                        self.expressionToken = thisContext.contextManager.parser.parse(0)
                    else:
                        self.errorToken = nextToken
                else:
                    self.errorToken = nextToken
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

    def handleError(self, token):
        if token.errorToken.id in (';', '(systemToken)'):
            raise SyntaxError('Expecting (identifier) before ' + token.errorToken.id)
        elif token.errorToken.id in (token.sign, token.modifier, token.primitive):
            raise SyntaxError('Duplication of ' + "'" + token.errorToken.id + "'" + ' in declaration statement')
        elif token.errorToken.id in ('short', 'long'):
            raise SyntaxError("Cannot have both 'short' and 'long' in declaration statement")
        elif token.errorToken.id in ('unsigned', 'signed'):
            raise SyntaxError("Cannot have both 'signed' and 'unsigned' in this declaration statement")

    def buildToken(self, token):
        if token.errorToken is not None:
            self.handleError(token)

        newToken = self.createToken(token.primitive)
        newToken.data.append(token.identifier)
        newToken.modifier = []
        if token.sign is not None:
            newToken.modifier.append(token.sign)
        if token.modifier is not None:
            newToken.modifier.append(token.modifier)
        ddToken = self.createDeclarationAndDefinitionToken()
        ddToken.data.append(newToken)
        if token.expressionToken.id == '=':
            ddToken.data.append(token.expressionToken)
        elif token.expressionToken.id == '(identifier)':
            pass
        else:
            raise SyntaxError
        return ddToken

"""
    def addPrimitive(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.ruleCheck(self)
            return
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.type = 'primitive'
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
        symClass.type = 'modifier'
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
