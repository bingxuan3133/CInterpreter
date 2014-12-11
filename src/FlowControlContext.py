
import os,sys
lib_path = os.path.abspath('../src')
sys.path.append(lib_path)

from Context import *
from ContextManager import *

class FlowControlContext(Context):
    def addBlockOperator(self, id, bindingPower = 0 ):
        thisContext = self
        symClass = self.symbol(id, bindingPower)
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
            returnedToken = thisContext.contextManager.parser.parseStatement(self.bindingPower)
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
            body = thisContext.contextManager.parser.parseStatement(self.bindingPower)
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
            #Change the context
            thisContext.contextManager.pushContexts(thisContext.contextManager.currentContexts)
            newContext = thisContext.contextManager.getContext('Expression')
            thisContext.contextManager.setCurrentContexts([newContext])
            nextToken = thisContext.contextManager.parser.lexer.advance()
            if nextToken.id == ')':
                raise SyntaxError('No expression found on the context.')
            returnedToken = thisContext.contextManager.parser.parse(bindingPower)
            headToken.data.append(returnedToken)
            self.data.append(headToken)
            thisContext.contextManager.parser.lexer.peep(')')
            tempContext =  thisContext.contextManager.popContexts()
            thisContext.contextManager.setCurrentContexts(tempContext)
            thisContext.contextManager.parser.lexer.advance()
            returnedToken = thisContext.contextManager.parser.parseStatement(bindingPower)
            self.data.append(returnedToken)
            nextToken = thisContext.contextManager.parser.lexer.peep()
            if nextToken.id == 'else':
                thisContext.contextManager.parser.lexer.advance()
                returnedToken = thisContext.contextManager.parser.parseStatement(bindingPower)
                nextToken.data.append(returnedToken)
                self.data.append(nextToken)
            return self
        def led(self, leftToken):
            return self
        symClass = self.symbol(id, bindingPower)
        symClass.nud = nud
        symClass.led = led
        return symClass
