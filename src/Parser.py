# Pratt's parser implementation
from Lexer import *
from ContextManager import *


class Parser:

    def __init__(self, lexer, contextManager):
        self.lexer = lexer
        self.contextManager = contextManager

    def parse(self, bindingPower):
        token = self.lexer.peep()        # token = leftToken
        token = token.nud()
        token2 = self.lexer.peep()     # token2 = rightToken
        while bindingPower < token2.bindingPower:  # left < right
            token = token2.led(token)
            token2 = self.lexer.peep()
        return token  # number token: come in first time, else operator token: after rolling in the while loop

    def parseStatement(self, bindingPower):
        list = []
        firstToken = self.lexer.peep()
        if firstToken.id == ';':
            self.lexer.advance()
            return None
        for currentContext in self.contextManager.currentContexts:
            if firstToken.id in currentContext.symbolTable:
                returnedToken = self.parse(bindingPower)
                list.append(returnedToken)
                return list

        if firstToken.id == '{':
            returnedToken = self.parse(bindingPower)
        else:
            returnedToken = self.parse(bindingPower)
            self.lexer.peep(';')
            self.lexer.advance()
        list.append(returnedToken)
        return list

    def parseStatements(self, bindingPower):
        list = []
        token = self.lexer.peep()
        while token.id != '}' and token.id != '(systemToken)':
            returnedToken = self.parseStatement(bindingPower)
            if returnedToken is not None:
                list.extend(returnedToken)
            token = self.lexer.peep()
        return list
