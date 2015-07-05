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
        thisContext = self
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
