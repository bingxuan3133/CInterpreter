__author__ = 'JingWen'

import os,sys
lib_path = os.path.abspath('\..\src')
sys.path.append(lib_path)

from Context import *
from ContextManager import *
import copy

class DeclarationContext(Context):
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
            if identifierToken.id == 'int':
                raise SyntaxError('2 or more data types in declaration')
            while True:
                identifierToken = thisContext.contextManager.parser.lexer.peep()
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
            testToken = thisContext.contextManager.parser.lexer.peep(';')
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
