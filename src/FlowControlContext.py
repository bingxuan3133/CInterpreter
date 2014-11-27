
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Context import *
from ContextManager import *

class FlowControlContext(Context):
    def parseStatement(self, bindingPower):
        firstToken = self.contextManager.parser.lexer.peep()
        if firstToken.id == ';':
            self.contextManager.parser.lexer.advance()
            returnedToken = None
        elif firstToken.id == '{':
            returnedToken = self.contextManager.parser.parse(bindingPower)
        elif firstToken.id in self.symbolTable:  # avoid handling ';' for flow control operators
            returnedToken = self.contextManager.parser.parse(bindingPower)
        else:
            returnedToken = self.contextManager.parser.parse(bindingPower)
            self.contextManager.parser.lexer.peep(';')
            self.contextManager.parser.lexer.advance()
        return returnedToken

    def parseStatements(self, bindingPower):
        list = []
        token = self.contextManager.parser.lexer.peep()
        while token.id != '}' and token.id != '(systemToken)':
            returnedToken = self.parseStatement(bindingPower)
            if returnedToken is not None:
                list.append(returnedToken)
            token = self.contextManager.parser.lexer.peep()
        return list

    def addBlockOperator(self, id, bindingPower = 0 ):
        thisContext = self
        symClass = self.symbol(id, bindingPower)
        def led(self):
            return self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            returnedList = thisContext.parseStatements(bindingPower)
            self.data = returnedList
            thisContext.contextManager.parser.lexer.peep('}')
            thisContext.contextManager.parser.lexer.advance()
            return self
        symClass = self.addOperator(id, bindingPower)  # removed the nud and led
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addWhileControl(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance('(')
            contexts = thisContext.contextManager.getCurrentContexts()
            thisContext.contextManager.pushContexts(contexts)  # save context
            default = thisContext.contextManager.getContext('Default')
            expression = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([expression, default])
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(self.bindingPower)
            self.data.append(returnedToken)
            thisContext.contextManager.parser.lexer.peep(')')
            contexts = thisContext.contextManager.popContexts()  # pop previously saved context
            thisContext.contextManager.setCurrentContexts(contexts)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.parseStatement(self.bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self):
            pass
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addDoWhileControl(self, id, bindingPower):
        thisContext = self
        def nud(self):
            thisContext.contextManager.parser.lexer.advance()
            body = thisContext.parseStatement(self.bindingPower)
            thisContext.contextManager.parser.lexer.peep('while')
            thisContext.contextManager.parser.lexer.advance('(')
            contexts = thisContext.contextManager.getCurrentContexts()
            thisContext.contextManager.pushContexts(contexts)  # save context
            default = thisContext.contextManager.getContext('Default')
            expression = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([expression, default])
            thisContext.contextManager.parser.lexer.advance()
            condition = thisContext.contextManager.parser.parse(self.bindingPower)
            thisContext.contextManager.parser.lexer.peep(')')
            contexts = thisContext.contextManager.popContexts()  # pop previously saved context
            thisContext.contextManager.setCurrentContexts(contexts)
            thisContext.contextManager.parser.lexer.advance()
            self.data.append(condition)
            self.data.append(body)
            return self
        def led(self):
            pass
        symClass = self.symbol(id,bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass

    def addIfControl(self,id,bindingPower=0):
        thisContext = self
        def nud(self):
            headToken = thisContext.contextManager.parser.lexer.advance('(')
            thisContext.contextManager.pushContexts(thisContext.contextManager.currentContexts)
            newContext = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([newContext])
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            headToken.data.append(returnedToken)
            self.data.append(headToken)
            thisContext.contextManager.parser.lexer.peep(')')
            tempContext =  thisContext.contextManager.popContexts()
            thisContext.contextManager.setCurrentContexts(tempContext)
            nextToken = thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.parseStatement(bindingPower)
            self.data.append(returnedToken)
            return self
        def led(self, leftToken):
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
