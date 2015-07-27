# Pratt's parser implementation

from LexerStateMachine import *
from Scope import ScopeBuilder

class Parser:
    def __init__(self, lexer, contextManager):
        self.lexer = lexer
        self.contextManager = contextManager
        self.scopeBuilder = ScopeBuilder()

    def parse(self, bindingPower):
        try:
            token = self.lexer.peep()        # token = leftToken
            token = token.nud()
            token2 = self.lexer.peep()     # token2 = rightToken
            while bindingPower < token2.bindingPower:  # left < right
                token = token2.led(token)
                token2 = self.lexer.peep()
            return token  # number token: come in first time, else operator token: after rolling in the while loop
        except SyntaxError as e:
            errorMSG = self.processException(e)
            raise SyntaxError(errorMSG )

    def parseStatement(self, bindingPower):
        try:
            list = []
            firstToken = self.lexer.peep()
            if firstToken.id == ';':
                self.lexer.advance()
                return None
            elif firstToken.id == '{':            # For one block of statements
                #self.scopeBuilder.buildScope(firstToken)
                returnedToken = self.parse(bindingPower)
                flowControlContext = self.contextManager.getContext('FlowControl')
                #self.scopeBuilder.buildScope(Context.createToken(flowControlContext, '}'))  # Create '}' token for scopeBuilder
                list.append(returnedToken)
                return list
            elif firstToken.id in self.contextManager.getContext('FlowControl').symbolTable:  # For some context that do not need ';'
                returnedToken = self.parse(bindingPower)
                #self.scopeBuilder.buildScope(returnedToken)
                list.append(returnedToken)
                return list
            else:                               # For one statement
                returnedToken = self.parse(bindingPower)
                if returnedToken.id == '(declaration&definition)':  # For declaration & definition
                    list.extend(returnedToken.data)
                    #self.scopeBuilder.buildScope(returnedToken.data[0])
                    self.lexer.peep(';')
                    return list
        except SyntaxError as e:
            errorMSG  = self.processException(e)
            raise SyntaxError (errorMSG )
        #self.scopeBuilder.buildScope(returnedToken)
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

    def processException(self, e):
        temp = e.msg.split('\n')
        tempToken = self.lexer.peep()
        caretMessage = ' '*(tempToken.column-1)+'^'
        if temp.__len__() == 1:
            MSG="Error[{}][{}]:{}\n{}\n{}".format(tempToken.line,tempToken.column,temp[0],tempToken.oriString,caretMessage)
        else:
            temp = temp[0].split(':')
            temp[0]="Error[{}][{}]".format(tempToken.line,tempToken.column)
            temp[0]=temp[0]+':'+temp[1]
            MSG = temp[0] + '\n' + tempToken.oriString + '\n' + caretMessage
        return MSG