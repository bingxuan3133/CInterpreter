# Pratt's parser implementation

import os,sys
from LexerStateMachine import *
from SemanticChecker import *
from ScopeBuilder import ScopeBuilder
from Context import *

class Parser:
    def __init__(self, lexer, contextManager):
        self.lexer = lexer
        self.contextManager = contextManager
        self.scopeBuilder = ScopeBuilder()
        self.semanticChecker = SemanticChecker(self.scopeBuilder)

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
        elif firstToken.id == '{':            # For one block of statements
            self.scopeBuilder.buildScope(firstToken)
            returnedToken = self.parse(bindingPower)
            self.scopeBuilder.destroyCurrentScope()
            list.append(returnedToken)
            return list
        elif firstToken and firstToken.id in self.contextManager.getContext('FlowControl').symbolTable:  # For some context that do not need ';'
            returnedToken = self.parse(bindingPower)
            self.scopeBuilder.buildScope(returnedToken)
            list.append(returnedToken)
            return list
        else:                               # For one statement
            returnedToken = self.parse(bindingPower)
            if returnedToken.id == '(multiple)':  # For declaration & definition
                list.extend(returnedToken.data)
                self.lexer.peep(';')
                self.lexer.advance()
                return list
            else:
                self.scopeBuilder.buildScope(returnedToken)
                self.semanticChecker.semanticCheck(returnedToken)
                self.lexer.peep(';')
                self.lexer.advance()
                list.append(returnedToken)
                return list

    def parseStatements(self, bindingPower):
        list = []
        token = self.lexer.peep()
        while token.id != '}' and token.id != 'EOF':
            returnedToken = self.parseStatement(bindingPower)
            if returnedToken is not None:
                list.extend(returnedToken)
            token = self.lexer.peep()
        return list
